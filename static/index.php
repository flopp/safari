<html>
<head>
    <meta charset="UTF-8" />
    
    <title>Safari-Map</title>
    <meta name="description" content="Die Safari-Map zeigt Locationless/Reverse-Geocaches (Safari-Caches) von Opencaching.de sowie die entsprechenden Logeinträge." />

    <link rel="alternate" type="application/atom+xml" title="Safari-Caches Feed" href="https://safari.flopp.net/feed.xml" />
    <link rel="author" href="https://plus.google.com/100782631618812527586" />
    <link rel="image_src" href="img/screenshot.png" />

    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />

    <!-- external stuff from CDN -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/LEAFLET_VERSION/leaflet.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/BOOTSTRAP_VERSION/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/FONTAWESOME_VERSION/css/font-awesome.min.css" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/LEAFLET_AWESOME_MARKERS_VERSION/leaflet.awesome-markers.css" />

    <!-- sidebar-v2 -->
    <link rel="stylesheet" href="ext/leaflet-sidebar-v2/leaflet-sidebar.min.css" />

    <!-- boostrap lightbox -->
    <link rel="stylesheet" href="ext/bootstrap-lightbox/ekko-lightbox.min.css" />

    <!-- local -->
    <link rel="stylesheet" href="css/main.css" />
</head>

<body>
    <div id="map" class="sidebar-map"></div>

    <div id="sidebar" class="sidebar collapsed" style="z-index: 1001;">
        <ul class="sidebar-tabs" role="tablist">
            <li><a href="#caches" role="tab"><i class="fa fa-bars"></i></a></li>
            <li><a href="#info" role="tab"><i class="fa fa-info"></i></a></li>
        </ul>

        <div class="sidebar-content">
            <div class="sidebar-pane" id="caches">
                <h1 class="sidebar-header">
                    Safari-Caches <span class="sidebar-close"><i class="fa fa-caret-left"></i></span>
                </h1>
                
                <h2>
                    <i class="fa fa-check"></i> Gefundene ausblenden:
                </h2>
                <form action="javascript:App.hideFound($('#txtUsername').val());">
                    <div class="input-group">
                        <input id="txtUsername" type="text" class="form-control" placeholder="User-Name">
                        <span class="input-group-btn">
                            <button class="btn btn-info" type="submit">Ausblenden</button>
                        </span>
                    </div>
                </form>
                
                <?php require('sidebar.html') ?>
            </div>

            <div class="sidebar-pane" id="info">
                <h1 class="sidebar-header">
                    Infos <span class="sidebar-close"><i class="fa fa-caret-left"></i></span>
                </h1>
        
                <h2>Safari-Caches?</h2>
                <p>
                    Safari-Caches sind virtuelle Caches, die nicht an einen bestimmten Ort gebunden sind, sondern an mehreren Orten gefunden werden können (andere Bezeichnung: 'Locationless/Reverse'-Caches).
                </p>
                <p>
                    Die Aufgabe bei Safari-Caches liegt darin, ein Objekt oder einen Ort zu finden (von dem es auf der Welt mehrere gibt), der vom Cache-Ersteller vorgegeben wurde. Dieser Fund wird dann im Onlinelog bei <a href="http://www.opencaching.de/" target="_blank">Opencaching.de</a> z.B. mit Bildern und Koordinaten zu dokumentiert.
                </p>
                <p>
                    Weitere Infos zu Safari-Caches gibt es im <a href="http://wiki.opencaching.de/index.php/Reverse_(%E2%80%9ELocationless%E2%80%9C)_Caches" target="_blank">Wiki von Opencaching.de</a>
                </p>
                <p>
                    Um über neue Safari-Caches informiert zu werden, kann man folgenden <a href="https://safari.flopp.net/feed.xml" target="_blank"><i class="fa fa-rss"></i> RSS-Feed</a> abonnieren.
                </p>
                
                <h2>Warum wird der Cache X nicht in der Liste angezeigt?</h2>
                <p>
                    Die Liste der Safari-Caches wird nachts automatisch aktualisiert. Dabei werden alle mit dem 'Safari-Attribut' markierten Caches von Opencaching.de übernommen. Ist dieses Attribut nicht gesetzt, landet der Cache hier nicht in der Liste.
                </p>
                <p>
                    Falls ein neuer Cache nach einem Tag hier immer noch nicht gelistet ist, kann auch ein technischer Fehler vorliegen. In diesem Fall wäre ich über einen Mail an <a href="mailto:mail@flopp.net"><i class="fa fa-envelope"></i> mail@flopp.net</a> sehr dankbar.
                </p>
                
                <h2>Warum wird das Log von X beim Cache Y hier nicht angezeigt?</h2>
                <p>
                    Wie die Liste der Safari-Caches, werden die Logs jedes Caches nachts automatisch aktualisiert. Die einzelnen Logs werden dabei nach Koordinaten durchsucht - damit Koordinaten erkannt werden können, müssen sie im Log im Grad/Minuten-Format vorliegen (etwa "N 48 12.345 E 007 34.567").
                </p>
                <p>
                    Nur wenn solche Koordinaten im Log erkannt werden, wird das Log samt Marker hier angezeigt.
                </p>
        
                <h2>Beim Cache X wird kein Bild angezeigt!</h2>
                <p>
                    Beim ausgewählten Cache wird in der Cacheliste ein Vorschaubild angezeigt, wenn eins gefunden werden kann. Folgende Bilder werden dabei in Betracht gezogen:
                </p>
                <ol>
                    <li>Das Vorschaubild des Caches (Häkchen bei "Kartenvorschaubild" in den Bildeinstellungen des Caches bei Opencaching.de),</li>
                    <li>das erste, nicht als Spoiler markierte, Bild in der Bilderliste des Caches bei Opencaching.de,</li>
                    <li>das erste Bild, das in der Cachebeschreibung vorkommt und bei Opencaching.de gehostet wird.</li>
                </ol>

                <h2>Diese Webapp basiert auf folgenden Projekten:</h2>
                <ul>
                    <li><a href="http://www.opencaching.de/okapi" target="_blank">Opencaching API (OKAPI)</a></li>
                    <li><a href="http://getbootstrap.com/" target="_blank">Bootstrap</a></li>
                    <li><a href="http://fontawesome.io/" target="_blank">Font Awesome</a></li>
                    <li><a href="http://leafletjs.com/" target="_blank">Leaflet</a></li>
                    <li><a href="https://github.com/lvoogdt/Leaflet.awesome-markers" target="_blank">Leaflet.awesome-markers</a></li>
                    <li><a href="https://github.com/Turbo87/sidebar-v2" target="_blank">sidebar-v2</a></li>
                    <li><a href="http://jquery.com/" target="_blank">jQuery</a></li>
                    <li><a href="https://github.com/flesler/jquery.scrollTo" target="_blank">jQuery.scrollTo</a></li>
                </ul>
                
                <h2>Allgemein:</h2>
                <p>Die Safari-Map ist ein Projekt von <a href="http://www.florian-pigorsch.de/" target="_blank">Florian Pigorsch</a>. Den Quellcode gibt's bei <a href="https://github.com/flopp/safari" target="_blank">Github</a>.</p>
            </div>
        </div>
    </div>

    <!-- the alert dialog -->
    <div id="dlgAlert" class="modal">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 id="dlgAlertHeader">Modal header</h3>
                </div>
                <div class="modal-body">
                    <div id="dlgAlertMessage">Modal body</div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-dismiss="modal">OK</button>
                </div>
            </div>
        </div>
    </div>

<!-- PIWIK-CODE -->

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/JQUERY_VERSION/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-scrollTo/JQUERY_SCROLLTO_VERSION/jquery.scrollTo.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/LEAFLET_VERSION/leaflet.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/BOOTSTRAP_VERSION/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/LEAFLET_AWESOME_MARKERS_VERSION/leaflet.awesome-markers.min.js"></script>
    
    <script src="ext/leaflet-sidebar-v2/leaflet-sidebar.js"></script>
    <script src="ext/bootstrap-lightbox/ekko-lightbox.min.js"></script>
    
    <script src="js/main.js?t=TSTAMP"></script>
    
    <script>
    $(document).ready( function() {
<?php
        $cache_code = "";
        if (!empty($_GET)) {
            if (isset($_GET['id'])) {
                $cache_code = $_GET['id'];
            }
        }

        echo <<< EOL
        App.init('$cache_code');
EOL;
?>
    });
    </script>
</body>

</html>
