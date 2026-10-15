#!/usr/bin/env python3
#
# list_models.py - List LLM models available with the EnMaaS gateway
#                  While different options are available, you probably
#                  want 'list_models.py --verify'
#
# Copyright (C) 2026 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

"""
List the models available to opencode via the EnMaaS gateway, grouped by
the actual model vendor.

Three sources are merged:

1. The gateway's OpenAI-compatible /v1/models catalog. Its `owned_by`
   field just reports the serving infrastructure ("vertex"), so vendors
   are inferred from model ID naming conventions instead.

2. Models declared in opencode's config (~/.config/opencode/opencode.jsonc).
   Some EnMaaS deployments -- e.g. rits/zai-org/glm-5-3, served from a
   dedicated vLLM cluster -- are routable through the gateway but are not
   registered in the /v1/models catalog, so opencode only knows about them
   because the config declares them explicitly.

3. opencode's own model catalog (models.dev), for every provider the
   config routes at this gateway without declaring models inline -- this
   is where the OpenAI models come from. By default only the newest model
   per family is included (--all-versions widens this). The gateway does
   not necessarily serve every catalog entry; --verify probes each one
   and hides any that are not served.

Usage:
    python3 list_models.py                    # grouped, human-readable
    python3 list_models.py --json             # grouped JSON
    python3 list_models.py --ids              # flat list of model IDs
    python3 list_models.py --provider openai  # one provider only
    python3 list_models.py --all-versions     # include old catalog versions
    python3 list_models.py --verify           # probe models; hide unserved ones
    python3 list_models.py --no-catalog       # gateway + config only
    python3 list_models.py --config PATH      # alternate opencode config

Requires an API key in the environment: ENMAAS_KEY (or ENMAAS_API_KEY),
or pass it explicitly with --api-key.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

API_URL = "https://api.enmaas.devshift.net/v1/models"
KEY_ENV_VARS = ("ENMAAS_KEY", "ENMAAS_API_KEY")

# Auth header styles to try, in order. Bearer is what the gateway accepts
# today; x-api-key is kept as a fallback in case that ever flips.
AUTH_STYLES = (
    ("Authorization", "Bearer {key}"),
    ("x-api-key", "{key}"),
)

# opencode's model catalog -- this is where its model picker data comes from.
MODELS_DEV_URL = "https://models.dev/api.json"

# Some CDNs (e.g. models.dev's) reject requests with Python's default
# User-Agent, so identify ourselves properly.
USER_AGENT = "list-models.py/1.0"

# Model IDs that are not chat models; --verify skips probing them.
NON_CHAT_TAGS = ("embedding", "image", "whisper", "tts", "realtime", "moderation")

# Map "vendor/model" style namespaces to display names.
NAMESPACE_PROVIDERS = {
    "anthropic": "Anthropic",
    "google": "Google",
    "openai": "OpenAI",
    "meta": "Meta",
    "mistralai": "Mistral AI",
    "moonshotai": "Moonshot AI",
    "xai": "xAI",
    "nvidia": "NVIDIA",
    "amazon": "Amazon",
    "microsoft": "Microsoft",
    "cohere": "Cohere",
    "deepseek": "DeepSeek",
    "qwen": "Alibaba (Qwen)",
    "zai": "Z.ai",
    "zai-org": "Z.ai",
    "enmaas": "EnMaaS",
    "opencode": "OpenCode",
}

# Model-name prefixes -> vendor, checked after namespace handling.
NAME_PREFIXES = (
    (("claude-",), "Anthropic"),
    (("qwen", "qwq"), "Alibaba (Qwen)"),
    (("nova-", "titan-"), "Amazon"),
    (("ernie-",), "Baidu"),
    (("doubao-",), "ByteDance"),
    (("command-", "aya-"), "Cohere"),
    (("deepseek-",), "DeepSeek"),
    (("gemini-", "gemma-", "bard-", "palm-"), "Google"),
    (("llama-",), "Meta"),
    (("phi-", "mai-"), "Microsoft"),
    (("minimax-", "abab-"), "MiniMax"),
    (
        ("mistral-", "mixtral-", "codestral-", "ministral-", "magistral-", "pixtral-"),
        "Mistral AI",
    ),
    (("kimi-", "moonshot-"), "Moonshot AI"),
    (("nemotron-",), "NVIDIA"),
    (("gpt-", "chatgpt-", "codex-", "davinci-", "text-embedding-", "o1", "o3", "o4"), "OpenAI"),
    (("hunyuan-",), "Tencent"),
    (("grok-",), "xAI"),
    (("glm",), "Z.ai"),
)

OTHER = "Other"


def infer_provider(model_id: str) -> str:
    """Guess the vendor behind a model ID from its naming convention."""
    model_id = model_id.strip().lower()
    segments = model_id.split("/")
    # A path segment may itself name a vendor, e.g. "zai-org/glm-5-3"
    # or "rits/zai-org/glm-5-3".
    for segment in segments[:-1]:
        if segment in NAMESPACE_PROVIDERS:
            return NAMESPACE_PROVIDERS[segment]
    name = segments[-1]
    for prefixes, provider in NAME_PREFIXES:
        if name.startswith(prefixes):
            return provider
    return OTHER


def fetch_models(api_url: str, api_key: str, timeout: float) -> list[dict]:
    """GET /v1/models, trying each auth header style until one is accepted."""
    last_error: Exception | None = None
    for header, template in AUTH_STYLES:
        request = urllib.request.Request(
            api_url, headers={header: template.format(key=api_key), "User-Agent": USER_AGENT}
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.load(response)
            return payload.get("data", [])
        except urllib.error.HTTPError as error:
            last_error = error
            if error.code in (401, 403):
                continue  # auth style rejected; try the next one
            raise
    assert last_error is not None
    raise last_error


def strip_jsonc_comments(text: str) -> str:
    """Remove // and /* */ comments from JSONC without touching strings."""
    result = []
    i = 0
    length = len(text)
    in_string = False
    while i < length:
        char = text[i]
        if in_string:
            result.append(char)
            if char == "\\" and i + 1 < length:
                result.append(text[i + 1])
                i += 2
                continue
            if char == '"':
                in_string = False
            i += 1
        elif char == '"':
            in_string = True
            result.append(char)
            i += 1
        elif char == "/" and text[i + 1 : i + 2] == "/":
            while i < length and text[i] != "\n":
                i += 1
        elif char == "/" and text[i + 1 : i + 2] == "*":
            i += 2
            while i + 1 < length and text[i : i + 2] != "*/":
                i += 1
            i += 2
        else:
            result.append(char)
            i += 1
    return "".join(result)


def default_config_paths() -> list[Path]:
    """Where opencode's global config might live."""
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    opencode_dir = config_home / "opencode"
    return [opencode_dir / "opencode.jsonc", opencode_dir / "opencode.json"]


def load_opencode_config(path: Path) -> dict:
    """Load an opencode config file (JSONC) into a dict."""
    return json.loads(strip_jsonc_comments(path.read_text(encoding="utf-8")))


def models_from_config(config: dict) -> set[str]:
    """Collect the model IDs explicitly declared under providers in a config."""
    declared: set[str] = set()
    for provider in config.get("providers", {}).values():
        if isinstance(provider, dict):
            declared.update(str(model_id) for model_id in (provider.get("models") or {}))
    return declared


def fetch_models_dev(timeout: float) -> dict:
    """Fetch opencode's model catalog (models.dev)."""
    request = urllib.request.Request(MODELS_DEV_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def catalog_models_for_config(config: dict, gateway_host: str, catalog: dict) -> dict[str, dict]:
    """models.dev entries for every config provider that is routed at this
    gateway but declares no models of its own -- opencode fills those in
    from its catalog, which is where the OpenAI models come from."""
    merged: dict[str, dict] = {}
    for provider_id, provider in config.get("providers", {}).items():
        if not isinstance(provider, dict) or provider.get("models"):
            continue
        base_url = (provider.get("settings") or {}).get("baseURL", "")
        if urllib.parse.urlsplit(base_url).netloc != gateway_host:
            continue
        for model_id, entry in (catalog.get(provider_id) or {}).get("models", {}).items():
            if isinstance(entry, dict):
                merged[model_id] = entry
    return merged


def newest_per_family(entries: dict[str, dict]) -> set[str]:
    """Pick the newest model of each family (release_date is ISO 8601, so
    plain string comparison orders dates correctly)."""
    best: dict[str, tuple[str, str]] = {}
    for model_id, entry in entries.items():
        family = entry.get("family") or model_id
        key = (str(entry.get("release_date") or ""), model_id)
        if family not in best or key > best[family]:
            best[family] = key
    return {model_id for _, (_, model_id) in best.items()}


def probe_model(api_url: str, api_key: str, model_id: str, timeout: float) -> str:
    """Check that a model is actually served, via a minimal chat request."""
    if any(tag in model_id.lower() for tag in NON_CHAT_TAGS):
        return "non-chat"
    chat_url = api_url.rstrip("/").rsplit("/models", 1)[0] + "/chat/completions"
    # OpenAI reasoning models only accept max_completion_tokens; older
    # OpenAI-compatible backends only accept max_tokens. Try both flavors.
    for params in ({"max_completion_tokens": 16}, {"max_tokens": 16}):
        body = json.dumps(
            {
                "model": model_id,
                "messages": [{"role": "user", "content": "Reply with: OK"}],
                **params,
            }
        ).encode()
        for header, template in AUTH_STYLES:
            request = urllib.request.Request(
                chat_url,
                data=body,
                method="POST",
                headers={"Content-Type": "application/json", header: template.format(key=api_key)},
            )
            try:
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    json.load(response)
                return "ok"
            except urllib.error.HTTPError as error:
                detail = error.read().decode(errors="replace")
                if error.code in (401, 403):
                    continue  # auth style rejected; try the next one
                if error.code == 404:
                    return "not served"
                if "max_tokens" in detail or "max_completion_tokens" in detail:
                    break  # wrong parameter for this model; try the other flavor
                return f"HTTP {error.code}"
            except (urllib.error.URLError, OSError):
                return "network error"
    return "unverifiable"


def group_models(model_ids: Iterable[str]) -> dict[str, list[str]]:
    """Group model IDs by inferred vendor, sorted within each group."""
    groups: dict[str, list[str]] = defaultdict(list)
    for model_id in model_ids:
        groups[infer_provider(model_id)].append(model_id)
    return {provider: sorted(ids) for provider, ids in sorted(groups.items())}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="List models available to opencode via the EnMaaS gateway, "
        "grouped by provider."
    )
    parser.add_argument("--json", action="store_true", help="output grouped JSON")
    parser.add_argument("--ids", action="store_true", help="print a flat list of model IDs")
    parser.add_argument("--provider", metavar="NAME", help="only show this provider (case-insensitive)")
    parser.add_argument("--api-key", help="API key (default: $ENMAAS_KEY or $ENMAAS_API_KEY)")
    parser.add_argument(
        "--config",
        help="opencode config file to merge models from "
        "(default: ~/.config/opencode/opencode.jsonc if it exists)",
    )
    parser.add_argument(
        "--all-versions",
        action="store_true",
        help="include every catalog version, not just the newest per family",
    )
    parser.add_argument(
        "--no-catalog",
        action="store_true",
        help="skip merging models from the models.dev catalog",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="probe non-gateway models with a tiny chat request and hide "
        "the ones that are not served (costs a few tokens each)",
    )
    parser.add_argument("--url", default=API_URL, help=f"models endpoint (default: {API_URL})")
    parser.add_argument("--timeout", type=float, default=15.0, help="request timeout in seconds")
    args = parser.parse_args()

    api_key = args.api_key or next(
        (os.environ[var] for var in KEY_ENV_VARS if os.environ.get(var)), None
    )
    if not api_key:
        print(
            f"error: no API key found; set {' or '.join(KEY_ENV_VARS)} or use --api-key",
            file=sys.stderr,
        )
        return 1

    try:
        models = fetch_models(args.url, api_key, args.timeout)
    except urllib.error.HTTPError as error:
        body = error.read().decode(errors="replace").strip()
        print(f"error: HTTP {error.code} from {args.url}: {body}", file=sys.stderr)
        return 1
    except (urllib.error.URLError, OSError) as error:
        print(f"error: could not reach {args.url}: {error}", file=sys.stderr)
        return 1

    api_ids = {entry["id"] for entry in models if entry.get("id")}

    config: dict | None = None
    if args.config:
        config_path = Path(args.config)
        if not config_path.is_file():
            print(f"error: config file not found: {config_path}", file=sys.stderr)
            return 1
        try:
            config = load_opencode_config(config_path)
        except (OSError, ValueError) as error:
            print(f"error: could not parse {config_path}: {error}", file=sys.stderr)
            return 1
    else:
        for config_path in default_config_paths():
            if config_path.is_file():
                try:
                    config = load_opencode_config(config_path)
                except (OSError, ValueError) as error:
                    print(f"warning: ignoring config {config_path}: {error}", file=sys.stderr)
                break

    # Attribute each model to a source, in priority order: the gateway's
    # own catalog, explicit declarations in the opencode config, then
    # opencode's models.dev catalog for providers routed at this gateway.
    sources: dict[str, str] = {model_id: "gateway" for model_id in api_ids}
    if config:
        for model_id in models_from_config(config) - api_ids:
            sources[model_id] = "config"
        if not args.no_catalog:
            gateway_host = urllib.parse.urlsplit(args.url).netloc
            try:
                catalog = fetch_models_dev(args.timeout)
            except (urllib.error.URLError, OSError, ValueError) as error:
                print(f"warning: could not load the models.dev catalog: {error}", file=sys.stderr)
                catalog = {}
            catalog_entries = catalog_models_for_config(config, gateway_host, catalog)
            selected = (
                set(catalog_entries) if args.all_versions else newest_per_family(catalog_entries)
            )
            for model_id in selected:
                sources.setdefault(model_id, "catalog")

    groups = group_models(sources)

    if args.provider:
        wanted = args.provider.strip().lower()
        known = sorted(groups)
        groups = {p: ids for p, ids in groups.items() if p.lower() == wanted}
        if not groups:
            print(
                f"error: no provider matched {args.provider!r}; "
                f"known providers: {', '.join(known)}",
                file=sys.stderr,
            )
            return 1

    verification: dict[str, str] | None = None
    if args.verify:
        verification = {}
        for model_id in sorted({m for ids in groups.values() for m in ids}):
            if sources[model_id] == "gateway":
                continue  # the gateway's catalog already vouches for these
            status = probe_model(args.url, api_key, model_id, args.timeout)
            verification[model_id] = status
            print(f"verify: {model_id} -> {status}", file=sys.stderr)
        # The final list only keeps models that are actually served:
        # confirmed 404s are dropped. Non-chat models and errored probes
        # are kept, since neither proves the model is unavailable.
        groups = {
            provider: [m for m in ids if verification.get(m) != "not served"]
            for provider, ids in groups.items()
        }
        groups = {provider: ids for provider, ids in groups.items() if ids}

    total = sum(len(ids) for ids in groups.values())
    displayed = {model_id for ids in groups.values() for model_id in ids}

    if args.ids:
        for ids in groups.values():
            for model_id in ids:
                print(model_id)
    elif args.json:
        payload = {
            "total": total,
            "providers": groups,
            "sources": {
                name: sorted(m for m in displayed if sources[m] == name)
                for name in ("gateway", "config", "catalog")
            },
        }
        if verification is not None:
            payload["verification"] = verification
        print(json.dumps(payload, indent=2))
    else:
        for provider, ids in groups.items():
            print(f"{provider} ({len(ids)})")
            for model_id in ids:
                parts = [f"  {model_id}"]
                if sources[model_id] != "gateway":
                    parts.append(f"[{sources[model_id]}]")
                if verification is not None and model_id in verification:
                    parts.append(verification[model_id])
                print("  ".join(parts))
        counts = {"gateway": 0, "config": 0, "catalog": 0}
        for model_id in displayed:
            counts[sources[model_id]] += 1
        breakdown = [
            f"{counts[name]} {label}"
            for name, label in (
                ("gateway", "gateway-listed"),
                ("config", "from opencode config"),
                ("catalog", "from models.dev catalog"),
            )
            if counts[name]
        ]
        summary = (
            f"\nTotal: {total} model{'s' if total != 1 else ''} "
            f"across {len(groups)} provider{'s' if len(groups) != 1 else ''}"
        )
        if breakdown:
            summary += "\n(" + ", ".join(breakdown) + ")"
        if verification is not None:
            excluded = sum(1 for status in verification.values() if status == "not served")
            if excluded:
                summary += (
                    f"\n({excluded} model{'s' if excluded != 1 else ''} excluded: "
                    "not served by the gateway)"
                )
        print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
