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
        splitted = window.location.search.substr(1).split('&'),
        i,
        p;

    for (i = 0; i < splitted.length; i += 1) {
        p = splitted[i].split('=', 2);
        if (p[0] !== "") {
            if (p.length === 1) {
                params[p[0]] = "";
            } else {
                params[p[0]] = Url.decode(p[1]);
            }
        }
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
