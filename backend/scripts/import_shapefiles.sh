#!/bin/bash
# Script para importar Shapefiles o GeoJSON grandes a PostGIS usando ogr2ogr
# Este script asume que corre DENTRO del contenedor 'sigutcuts_backend'

SHAPEFILE_PATH=$1
TABLE_NAME=$2

if [ -z "$SHAPEFILE_PATH" ] || [ -z "$TABLE_NAME" ]; then
    echo "Uso: ./import_shapefiles.sh <ruta_al_archivo> <nombre_tabla>"
    echo "Ejemplo: ./import_shapefiles.sh /insumos/datos_geo/descargas/bosque_nativo.shp conaf_catastro"
    exit 1
fi

echo "Iniciando importación de $SHAPEFILE_PATH a la tabla $TABLE_NAME..."

# Conexión a la base de datos interna de Docker
PG_CONN="PG:host=sigutcuts_db dbname=sigutcuts user=postgres password=postgres"

# ogr2ogr inyecta el archivo, lo re-proyecta a EPSG:4326 y renombra la columna de geometría a 'geom'
ogr2ogr -f "PostgreSQL" \
        $PG_CONN \
        "$SHAPEFILE_PATH" \
        -nln "$TABLE_NAME" \
        -overwrite \
        -t_srs EPSG:4326 \
        -lco GEOMETRY_NAME=geom \
        -lco FID=id \
        --config PG_USE_COPY YES \
        -nlt PROMOTE_TO_MULTI \
        -skipfailures

if [ $? -eq 0 ]; then
    echo "✅ Importación exitosa: La tabla '$TABLE_NAME' está lista en PostGIS."
else
    echo "❌ Error durante la importación."
    exit 1
fi
