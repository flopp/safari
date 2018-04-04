var LogHeatmap = {};

LogHeatmap.init = function () {
    'use strict';
        
    var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 18,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }),
        latlng = L.latLng(50, 12);

    var map = L.map('map', {center: latlng, zoom: 5, layers: [tiles]});
    var markers = L.markerClusterGroup();
    
    var code = '';
    var name = '';
    var user = '';
    var cache_id = '';
    var log_id = '';
    for (var i = 0; i < logs.length; i++) {
        var a = logs[i];
        if (a.length > 4) {
            code = a[2];
            name = a[3];
            user = a[4];
            cache_id = a[5];
            log_id = a[6];
        } else {
            user = a[2];
            log_id = a[3];
        }
        var marker = L.marker(new L.LatLng(a[0], a[1]));
        var cache_url = 'https://opencaching.de/' + code;
        var log_url = 'https://www.opencaching.de/viewcache.php?cacheid=' + cache_id + '&log=A#log' + log_id;
        marker.bindPopup('<a href="' + cache_url + '" target=_blank>[' + code + '] ' + name + '</a><br /><a href="' + log_url + '" target=_blank>Log von ' + user + '</a>');
        markers.addLayer(marker);
    }

    map.addLayer(markers);
};