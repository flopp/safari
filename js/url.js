/*jslint
  indent: 4
*/
/*global
  window
*/

var Url = {};

Url.getParams = function () {
    'use strict';

    var params = {},
        s = window.location.search.substr(1).split('&'),
        i,
        p;

    for (i = 0; i < s.length; i += 1) {
        p = s[i].split('=', 2);
        if (p[0] !== "") {
            if (p.length === 1) {
                params[p[0]] = "";
            } else {
                params[p[0]] = Url.decode(p[1]);
            }
        }
    }
    
    p = window.location.href.match(/.*\/(oc[a-z0-9]+)$/i);
    if (p) {
        params['id'] = p[1].toUpperCase();
    }

    return params;
};


Url.decode = function (s) {
    'use strict';

    var s2 = decodeURIComponent(s.replace(/\+/g, " "));
    // allow for multiple encodings
    if ((s !== s2) && (/%[0-9a-fA-F]{2}/).test(s2)) {
        s2 = Url.decode(s2);
    }
    return s2;
};
