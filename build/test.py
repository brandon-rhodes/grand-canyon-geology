# wget https://github.com/mapnik/mapnik/wiki/data/110m-admin-0-countries.zip
# unzip 110m-admin-0-countries.zip

# To see which version of Mapnik:
# mapnik-config --version

import mapnik

f = mapnik.Filter("[unit] = 'water'")

m = mapnik.Map(610,300)
m.background = mapnik.Color('white')

#print(dir(mapnik))

s = mapnik.Style() # style object to hold rules
r = mapnik.Rule() # rule object to hold symbolizers
# to fill a polygon we create a PolygonSymbolizer
polygon_symbolizer = mapnik.PolygonSymbolizer()
polygon_symbolizer.fill = mapnik.Color('#000000') #'#f2eff9')
r.symbols.append(polygon_symbolizer) # add the symbolizer to the rule object

# to add outlines to a polygon we create a LineSymbolizer
# line_symbolizer = mapnik.LineSymbolizer()
# line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
# line_symbolizer.stroke_width = 0.0 #1.0  #0.1
# r.symbols.append(line_symbolizer) # add the symbolizer to the rule object

r.filter = f

s.rules.append(r) # now add the rule to the style and we're done
m.append_style('My Style',s) # Styles are given names only as they are applied to the map

ds = mapnik.Shapefile(file='ne_110m_admin_0_countries.shp')

layer = mapnik.Layer('world') # new layer called 'world' (we could name it anything)
# note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

layer.datasource = ds
layer.styles.append('My Style')
#m.layers.append(layer)

# extent = mapnik.Box2d(-130.0, 30.0, -100.0, 45.0)
# m.zoom_to_box(extent)

#mapnik.Ogr(file='test_point_line.gpx')

#mapnik.load_map(m, 'geopolys.geojson')

# Data looks like:
#     {
#       "type": "Feature",
#       "properties": {
#         "unit": "water",
#         "color": "#ebffff"
#       },
#       "geometry": {
#         "type": "MultiPolygon",
#         "coordinates": [

layer = mapnik.Layer('Geolines')
geolines_datasource = mapnik.Ogr(
    #file='geolines.geojson',
    #layer='geolines',
    # file='geopolys.geojson',
    # layer='geopolys',
    file='tiny_polys.geojson',  # time ./filter.py geopolys.geojson > OUT2
    layer='tiny_polys',
)  # does this add a datasource?

layer.datasource = geolines_datasource
layer.styles.append('My Style')
m.layers.append(layer)

m.zoom_all()
mapnik.render_to_file(m,'world.png', 'png')


# m = mapnik.Map(256,256)
# mapnik.load_map(m, "file.xml")
# m.zoom_all()
# mapnik.render_to_file(m, "the_image.png")
