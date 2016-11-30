/*jslint
  indent: 4
*/

/*global
  $, L,
  alert, console, document, setTimeout
*/

function coords(s) {
    'use strict';

    var p = s.split('|');
    return new L.latLng(parseFloat(p[0]), parseFloat(p[1]));
}


var App = {};

App.m_map = null;
App.m_selected_code = null;
App.m_marker = null;
App.m_log_markers = [];
App.m_lines = null;
App.m_icon_cache = null;
App.m_icon_log = null;

App.init = function (cache_code) {
    'use strict';

    this.m_map = L.map('map', {maxZoom: 18, zoomControl: false}).setView([50, 1], 3);

    var sidebar = L.control.sidebar('sidebar').addTo(this.m_map),
        osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        osmAttrib = 'Map by <a href="http://www.openstreetmap.org/" target="_blank">OpenStreetMap</a> & contributors',
        osmLayer = new L.tileLayer(osmUrl, {maxZoom: 18, attribution: osmAttrib});
    osmLayer.addTo(this.m_map);
    L.control.zoom({position: 'topright'}).addTo(this.m_map);

    sidebar.open('caches');
    /*setTimeout(function () {
        sidebar.open('caches');
    }, 500);
    */
    /*
    $('#btnUnmarkFound').click( function() {
        unmarkFound();
    });

    $('#txtFilter').on('input', function(e){
        filter();
    });

    $('#btnClearFilter').click( function() {
        $('#txtFilter').val("");
        filter();
    });
    */

    $(document).delegate('*[data-toggle="lightbox"]', 'click', function (event) {
        event.preventDefault();
        $(this).ekkoLightbox();
    });


    this.m_icon_cache = L.AwesomeMarkers.icon({
        prefix: 'fa',
        icon: 'question',
        markerColor: 'cadetblue'
    });
    this.m_icon_log = L.AwesomeMarkers.icon({
        prefix: 'fa',
        icon: 'star',
        markerColor: 'green'
    });

    if (cache_code !== '') {
        this.click(cache_code);
    }
};


App.removeMarkers = function () {
    'use strict';

    var self = this;

    if (self.m_marker) {
        self.m_map.removeLayer(self.m_marker);
        self.m_marker = null;
    }

    $.each(self.m_log_markers, function (i, m) {
        self.m_map.removeLayer(m);
    });
    self.m_log_markers = [];

    if (self.m_lines) {
        self.m_map.removeLayer(self.m_lines);
        self.m_lines = null;
    }
};


App.click = function (cache_code) {
    'use strict';

    var self = this,
        cacheDiv = this.cacheDiv(cache_code);

    if (this.m_selected_code) {
        App.unhighlight(this.m_selected_code);
    }
    App.removeMarkers();
    this.m_selected_code = null;
    
    if (!cacheDiv) {
        history.pushState({}, '', '');
        console.log('Cache nicht gefunden: ' + cache_code);
        alert("Cache '" + cache_code + "' nicht gefunden :(");
        return;
    }

    this.m_selected_code = cache_code;
    App.highlight(this.m_selected_code);

    $('.sidebar-content').scrollTo(cacheDiv);

    $.ajax({
        url: "safaridb.php?code=" + cache_code,
        success: function (response) {
            var cache_coords = coords(response.cache.coords),
                lines = [],
                bounds = new L.latLngBounds(cache_coords);
            bounds.extend(cache_coords);

            self.m_marker = new L.marker(cache_coords, {icon: self.m_icon_cache});
            self.m_marker.addTo(self.m_map);

            $.each(response.logs, function (i, log) {
                if (log.coords !== null) {
                    var comment, content,
                        log_coords = coords(log.coords),
                        m = new L.marker(log_coords, {icon: self.m_icon_log});
                    m.addTo(self.m_map);
                    self.m_log_markers.push(m);
                    lines.push([cache_coords, log_coords]);
                    bounds.extend(log_coords);

                    comment = log.comment;
                    comment = comment.replace( /="resource2/g, '="https://opencaching.de/resource2' );
                    comment = comment.replace( /="lib/g, '="https://opencaching.de/lib' );
                    comment = comment.replace( /src="http:/g, 'src="https:' );

                    content = '<b>' + log.type + '</b> von <b>' + log.user + '</b> am <b>' + log.timestamp.split(" ")[0] + '</b>:<hr />' + comment;
                    if (log.images) {
                        content += '<hr /><div class="logimages">';
                        $.each(log.images, function (i, image) {
                            content += '<a href="' + image.url + '" data-toggle="lightbox" data-title="' + image.caption + '" data-gallery="log"><img class="img-thumbnail" src="' + image.thumb_url + '"/></a>';
                        });
                        content += '</div>';
                    }

                    m.bindPopup(content, {minWidth: 380, maxHeight: 400});
                }
            });

            self.m_lines = new L.multiPolyline(lines);
            self.m_lines.addTo(self.m_map);
            self.m_map.fitBounds(bounds);
        },
        error: function (jqXHR, exception) {
            console.log("AJAX request 'safari.db?code=" + cache_code + "' failed.");
        }
    });
};


App.cacheDiv = function (cache_code) {
    'use strict';
    var div = $('#cache' + cache_code);
    if (div.length) {
        return div;
    }
    return null;
};


App.detailsDiv = function (cache_code) {
    'use strict';

    var div = $('#cache' + cache_code + ' > .details');
    if (div.length) {
        return div;
    }
    return null;
};


App.highlight = function (cache_code) {
    'use strict';

    var div = this.cacheDiv(cache_code);
    if (div) {
        div.addClass('active');
        div = this.detailsDiv(cache_code).show();
        history.pushState({}, '', cache_code);
    } else {
        history.pushState({}, '', '');
    }
};


App.unhighlight = function (cache_code) {
    'use strict';

    var div = this.cacheDiv(cache_code);
    if (div) {
        div.removeClass('active');
        this.detailsDiv(cache_code).hide();
    }
};


App.hideFound = function(user) {
    'use strict';
    
    var self = this,
        all_count = $('.cache').length;
    
    if (this.m_selected_code) {
        App.unhighlight(this.m_selected_code);
        App.removeMarkers();
    }
    $(".cache").removeClass('hidden');
    $("#cachecount").text(all_count);
    if (user === "") {
        return;
    }
    
    $.ajax({
        url: "safaridb.php?user=" + user,
        success: function (response) {
            $.each(response.caches, function (i, code) {
                $("#cache" + code).addClass('hidden');
            });
            $("#cachecount").text((all_count - response.caches.length) + '/' + all_count);
        },
        error: function (jqXHR, exception) {
            console.log("AJAX request 'safari.db?user=" + user + "' failed.");
        }
    });
}
