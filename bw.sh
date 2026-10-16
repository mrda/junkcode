#!/usr/bin/bash
#
# Unlock BitWarden for CLI use, source this file rather than execute it,
# so that BW_SESSION and the bw helper survive into your shell.
# This is idempotent.
#
# Copyright (C) 2026 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html
#

bitwarden_username="${USER}@redhat.com"

# Installed from flatpack.  Flatpak doesn't pass custom env vars into the
# sandbox, so forward the session key ourselves (empty until unlocked).
_bw() { flatpak run --env=BW_SESSION="${BW_SESSION:-}" --command=bw com.bitwarden.desktop "$@"; }

_bw_unlock() {
    # Already have a valid session in this shell?
    if [[ -n "$BW_SESSION" ]] && _bw unlock --check >/dev/null 2>&1; then
        return 0
    fi

    # Reuse a session unlocked by another shell in this login
    local cache="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/bw-session"
    if [[ -s "$cache" ]]; then
        local cached
        cached=$(<"$cache")
        if BW_SESSION="$cached" _bw unlock --check >/dev/null 2>&1; then
            export BW_SESSION="$cached"
            return 0
        fi
        rm -f "$cache"     # stale (e.g. after `bw lock`)
        unset BW_SESSION   # any key we were holding is dead by now
    fi

    # Reauthenticate.  A "locked" vault only needs unlocking; anything
    # else (unauthenticated, fresh install) needs a full login with 2FA.
    local status
    status=$(_bw status | jq -r '.status')

    local master_password
    master_password=$(zenity --password --title="Reauthenticate Bitwarden" --text="Enter Bitwarden Master Password:") || return 1

    if [[ "$status" != "locked" ]]; then
        local code_2fa
        code_2fa=$(zenity --entry --title="Bitwarden 2FA" --text="Enter 2FA Code:" --hide-text)
        # >/dev/null 2>&1 throws bw's chatter away on both streams
        if ! _bw login "$bitwarden_username" "$master_password" --method 0 --code "$code_2fa" >/dev/null 2>&1; then
            echo "Login failed" >&2
            return 1
        fi
    fi

    # --passwordenv wants the NAME of an env var, not the password itself --
    # and flatpak doesn't forward custom env vars into the sandbox, so
    # inject it with --env
    local sessionkey
    if ! sessionkey=$(flatpak run --env=BW_PASSWORD="$master_password" --command=bw com.bitwarden.desktop unlock --passwordenv BW_PASSWORD --raw 2>/dev/null); then
        echo "Unlock failed" >&2
        return 1
    fi
    export BW_SESSION="$sessionkey"

    # Share the new session with other shells in this login
    ( umask 077; printf '%s' "$sessionkey" >"$cache" )

    return 0
}

bw() {
    case "$1" in
        login|logout|lock|status|update|help|--version) _bw "$@"; return ;;
    esac
    _bw_unlock || return 1
    _bw "$@"
}
