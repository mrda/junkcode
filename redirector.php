<?php
/*
 * Redirector.php
 *
 * Use Javascript to re-POST user-entered data to a remote host.  Concept built out of various snippets found out on the web.
 * Horribly insecure, but allows cross-site posting without having to modify the remote site to support some sort of authenticated hash pre-authorised login.
 *
 * Copyright (C) 2012.  All Rights Reserved.
 * Michael Davies <michael@the-davies.net>
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License as
 *  published by the Free Software Foundation; either version 2 of the
 *  License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful, but
 *  WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 *  General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
 *  02111-1307, USA.
 *
 */

function repost_to_remote_host($user, $password, $url) {
    print "<html>\n";
    print "    <head>\n";
    print "        <meta http-equiv='Cache-Control' content='no-cache, no-store, must-revalidate' />";
    print "        <meta http-equiv='Pragma' content='no-cache' />";
    print "        <meta http-equiv='Expires' content="0' />";
    print "        <script src='http://ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.min.js' type='text/javascript'></script>\n";
    print "        <script type='text/javascript'>\n";
    print "                function post_to_url(path, params, method) {\n";
    print "                    method = method || 'post';\n";
    print "                    var form = document.createElement('form');\n";
    print "                    form.setAttribute('method', method);\n";
    print "                    form.setAttribute('action', path);\n";
    print "                    for(var key in params) {\n";
    print "                        if(params.hasOwnProperty(key)) {\n";
    print "                            var hiddenField = document.createElement('input');\n";
    print "                            hiddenField.setAttribute('type', 'hidden');\n";
    print "                            hiddenField.setAttribute('name', key);\n";
    print "                            hiddenField.setAttribute('value', params[key]);\n";
    print "                            form.appendChild(hiddenField);\n";
    print "                         }\n";
    print "                    }\n";
    print "                    document.body.appendChild(form);\n";
    print "                    form.submit();\n";
    print "                }\n";
    print "                $(document).ready(function() { ";
    print "                post_to_url('https://$url', {'username':'$user', 'password':'$password', 'other_post_params':'whatever'});\n";
    print "                });\n";
    print "        </script>\n";
    print "    </head>\n";
    print "    <body style='margin: 0px; padding: 0px;'>\n";
    print "<h2>Redirecting you to another website with the same username/password credentials you entered here</h2>\n";
    print "    </body>\n";
    print "</html>\n";
}

?>
