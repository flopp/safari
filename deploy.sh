#!/bin/bash

set -euo pipefail

for PYTHON in /usr/bin/python3 /usr/local/bin/python3 CANNOT_FIND_PYTHON ; do
    if [ -x $PYTHON ] ; then
        break
    fi
done

if [ ! -x $PYTHON ] ; then
    echo "cannot find python"
    exit 1
fi

BOOTSTRAP_VERSION=4.0.0
FONTAWESOME_VERSION=4.7.0
JQUERY_VERSION=3.3.1
JQUERY_SCROLLTO_VERSION=2.1.2
LEAFLET_VERSION=1.3.1
LEAFLET_AWESOME_MARKERS_VERSION=2.0.2

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
mkdir -p ${D}/img/large
mkdir -p ${D}/img/small
mkdir -p ${D}/js

echo "$(date) - UPDATING CACHES..."
# update thumbnails, create html files

ln -fs $(pwd)/.private/authdata.py py
$PYTHON py/update-db.py
cp -a ${C}/feed.xml ${D}
cp -a ${C}/sidebar.html ${D}
cp -a ${C}/logs.js ${D}
cp -a ${C}/small/* ${D}/img/small
cp -a ${C}/safari.sqlite ${D}/db

# create base files
cp -a static/index.html ${D}
cp -a static/safaridb.php ${D}
cp -a static/.htaccess ${D}
cp -a static/logs.html ${D}
cp -a js/*.js ${D}/js
cp -a css/*.css ${D}/css

sed -i \
    -e "s/TSTAMP/$(date +%s)/g" \
    -e "s/BOOTSTRAP_VERSION/${BOOTSTRAP_VERSION}/g" \
    -e "s/JQUERY_VERSION/${JQUERY_VERSION}/g" \
    -e "s/JQUERY_SCROLLTO_VERSION/${JQUERY_SCROLLTO_VERSION}/g" \
    -e "s/FONTAWESOME_VERSION/${FONTAWESOME_VERSION}/g" \
    -e "s/LEAFLET_VERSION/${LEAFLET_VERSION}/g" \
    -e "s/LEAFLET_AWESOME_MARKERS_VERSION/${LEAFLET_AWESOME_MARKERS_VERSION}/g" \
    ${D}/index.html
sed -i \
    -e "s/TSTAMP/$(date +%s)/g" \
    ${D}/logs.html

if [ -f .private/piwik-code ] ; then
    echo "inserting PIWIK code"
    sed -i '/<!-- PIWIK-CODE -->/ {
        r .private/piwik-code
        g
    }' ${D}/index.html
fi

cp -a static/.htaccess ${D}
cp -a .private/google* ${D}


echo "$(date) - UPDATING THIRD PARTY LIBS..."
# update externals

# leaflet sidebar v2
if [ -d ${C}/ext/sidebar-v2/.git ] ; then
    (cd ${C}/ext/sidebar-v2/ && git pull origin master)
else
    (cd ${C}/ext && git clone https://github.com/Turbo87/sidebar-v2.git)
fi
mkdir -p ${D}/ext/leaflet-sidebar-v2
cp -a ${C}/ext/sidebar-v2/css/leaflet-sidebar.min.css ${D}/ext/leaflet-sidebar-v2
cp -a ${C}/ext/sidebar-v2/js/leaflet-sidebar.js ${D}/ext/leaflet-sidebar-v2

# boostrap lightbox
if [ -d ${C}/ext/bootstrap-lightbox/.git ] ; then
    (cd ${C}/ext/bootstrap-lightbox/ && git pull origin master)
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
