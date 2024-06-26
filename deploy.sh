#!/bin/bash

set -euo pipefail

PYTHON=.env/bin/python

TIMESTAMP=$(date "+%F %T")
TIMESTAMPSMALL=$(date "+%F")
CACHEBUSTER=$(date +%s)
BOOTSTRAP_VERSION=4.0.0
FONTAWESOME_VERSION=4.7.0
JQUERY_VERSION=3.3.1
JQUERY_SCROLLTO_VERSION=2.1.2
LEAFLET_VERSION=1.3.1
LEAFLET_AWESOME_MARKERS_VERSION=2.0.2
LEAFLET_MARKER_CLUSTER_VERSION=1.3.0

function insert_versions() {
    sed -i \
        -e "s/##CACHEBUSTER##/${CACHEBUSTER}/g" \
        -e "s/##LASTUPDATE##/${TIMESTAMP}/g" \
        -e "s/##LASTUPDATESMALL##/${TIMESTAMPSMALL}/g" \
        -e "s/BOOTSTRAP_VERSION/${BOOTSTRAP_VERSION}/g" \
        -e "s/JQUERY_VERSION/${JQUERY_VERSION}/g" \
        -e "s/JQUERY_SCROLLTO_VERSION/${JQUERY_SCROLLTO_VERSION}/g" \
        -e "s/FONTAWESOME_VERSION/${FONTAWESOME_VERSION}/g" \
        -e "s/LEAFLET_VERSION/${LEAFLET_VERSION}/g" \
        -e "s/LEAFLET_AWESOME_MARKERS_VERSION/${LEAFLET_AWESOME_MARKERS_VERSION}/g" \
        -e "s/LEAFLET_MARKER_CLUSTER_VERSION/${LEAFLET_MARKER_CLUSTER_VERSION}/g" \
        $1
}

C=".cache"
D=".deploy"
rm -rf $D
mkdir -p $D

(
echo "$(date) - START UPDATE"

mkdir -p ${C}
mkdir -p ${C}/ext
if [[ "$@" = *keep* ]]; then
    :
else
    rm -rf ${C}/json ${C}/orig ${C}/big ${C}/small
fi

mkdir -p ${D}/css
mkdir -p ${D}/db
mkdir -p ${D}/ext
mkdir -p ${D}/img
mkdir -p ${D}/img/big
mkdir -p ${D}/img/small
mkdir -p ${D}/js

echo "$(date) - UPDATING CACHES..."
# update thumbnails, create html files

ln -fs $(pwd)/.private/authdata.py py
$PYTHON py/update-db.py --cache-dir ${C}
cp -a ${C}/feed.xml ${D}
cp -a ${C}/index.html ${D}
cp -a ${C}/log-data.js ${D}/js
cp -a ${C}/small/* ${D}/img/small
cp -a ${C}/big/* ${D}/img/big
cp -a ${C}/safari.sqlite ${D}/db
cp -a ${C}/list*.html ${D}

# create base files
cp -a static/safaridb.php ${D}
cp -a static/.htaccess ${D}
cp -a static/logs.html ${D}
cp -a static/info.html ${D}
cp -a js/*.js ${D}/js
cp -a css/*.css ${D}/css

for HTML in ${D}/*.html ; do
    insert_versions ${HTML}
done

cp -a static/.htaccess ${D}


echo "$(date) - UPDATING THIRD PARTY LIBS..."
# update externals

# leaflet sidebar v2
if [ -d ${C}/ext/sidebar-v2/.git ] ; then
    (cd ${C}/ext/sidebar-v2/ && git pull --quiet origin master)
else
    (cd ${C}/ext && git clone https://github.com/Turbo87/sidebar-v2.git)
fi
mkdir -p ${D}/ext/leaflet-sidebar-v2
cp -a ${C}/ext/sidebar-v2/css/leaflet-sidebar.min.css ${D}/ext/leaflet-sidebar-v2
cp -a ${C}/ext/sidebar-v2/js/leaflet-sidebar.js ${D}/ext/leaflet-sidebar-v2

# boostrap lightbox
if [ -d ${C}/ext/bootstrap-lightbox/.git ] ; then
    (cd ${C}/ext/bootstrap-lightbox/ && git pull --quiet origin master)
else
    (cd ${C}/ext && git clone https://github.com/ashleydw/lightbox.git bootstrap-lightbox)
fi
mkdir -p ${D}/ext/bootstrap-lightbox
cp -a ${C}/ext/bootstrap-lightbox/dist/ekko-lightbox.min.* ${D}/ext/bootstrap-lightbox


echo "$(date) - COPYING FILES..."
### upload
mkdir -p ~/html/safari/
rsync -avz --progress ${D}/* ${D}/.htaccess ~/html/safari/

echo "$(date) - END UPDATE"
) > ${D}/log
