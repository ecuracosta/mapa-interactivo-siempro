# librerías
import pandas as pd
import geopandas as gpd
import folium
import webbrowser 
from folium import plugins
from flask import Flask
import requestsapp = Flask(__name__)

app = Flask(__name__)

@app.route("/")
def index():
	# creación del objeto mapa
	mapa = folium.Map(location=[-40.7049374,-65.1248615],zoom_start=4,contro_scale=True,tiles=None)
	# https://github.com/ign-argentina/argenmap
	# https://www.ign.gob.ar/NuestrasActividades/InformacionGeoespacial/ServiciosOGC/Leaflet
	folium.TileLayer(tiles='https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png',
        	          attr='<a href="http://leafletjs.com" title="A JS library for interactive maps">Leaflet</a> | <a href="http://www.ign.gob.ar/AreaServicios/Argenmap/IntroduccionV2" target="_blank">Instituto Geográfico Nacional</a> + <a href="http://www.osm.org/copyright" target="_blank">OpenStreetMap</a>', name='Mapa base del Instituto Geográfico Nacional (IGN)').add_to(mapa)

	# capas de puntos espaciales
	# Iconos en https://fontawesome.com/v4/icons/
	viverosCluster = plugins.MarkerCluster(name='invernaderos, viveros, huertas').add_to(mapa)
	viveros = gpd.read_file('viveros.json')
	viveros['fna'] = viveros['fna'].apply(lambda x: 'Sin Nombre' if x==None else x)
	viverosGPD = folium.GeoJson(viveros)
	for feature in viverosGPD.data['features']:
	    if feature['geometry']['type'] == 'Point':
	        folium.Marker(location=list(reversed(feature['geometry']['coordinates'])),
	            icon=folium.Icon(color='green',icon='leaf',prefix='fa'),
	            popup='<b>Nombre:</b>'+str(feature['properties']['fna'])+'<b>\n</b>'+
	                  '<b>gid:</b>'+str(feature['properties']['gid']),
	                   max_width=4000,min_width=4000).add_to(viverosCluster)

	# capas de polígonos
	barriosPopulares = gpd.read_file('barrios_populares.geojson')
	#style = {'fillColor':'green','lineColor':'black'} COLOREAR EN FUNCION DE UNA COLUMNA
	folium.GeoJson(barriosPopulares,
	               #style_function=lambda x: style,
	               name='barrios populares',
	               zoom_on_click=True,
	               tooltip=folium.GeoJsonTooltip(
	                   fields=['Barrio', 'Provincia', 'Departamento \ Partido', 'Localidad', 
	                           'Año de creación', 'Década de creación', 'Electricidad',
	                           'Cloaca', 'Agua', 'Gas', 'Familias estimadas'],
	                   localize=True)).add_to(mapa)

	folium.LayerControl().add_to(mapa)

    return mapa._repr_html_()

if __name__ == "__main__":
    app.run()