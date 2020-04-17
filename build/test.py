#!/usr/bin/env python3

# wget https://github.com/mapnik/mapnik/wiki/data/110m-admin-0-countries.zip
# unzip 110m-admin-0-countries.zip

# To see which version of Mapnik:
# mapnik-config --version

import json
import mapnik

def render():
    merc_srs = (
        '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0'
        ' +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over'
    )

    longlat = mapnik.Projection(
        '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
    )
    merc = mapnik.Projection(merc_srs)
    transform = mapnik.ProjTransform(longlat, merc)

    m = mapnik.Map(400, 500, srs=merc_srs)
    m.background = mapnik.Color('white')
    #m.srs = '+proj=merc +ellps=WGS84 +datum=WGS84 +no_defs'

    #print(dir(mapnik))

    with open('feature_data.json') as f:
        feature_data = json.load(f)

    feature_colors = feature_data['poly_color']
    print(feature_colors['water'])
    print(feature_colors['Mr'])

    s = mapnik.Style() # style object to hold rules

    for name, color in feature_colors.items():
        r = mapnik.Rule() # rule object to hold symbolizers
        polygon_symbolizer = mapnik.PolygonSymbolizer()
        polygon_symbolizer.fill = mapnik.Color(color)
        r.symbols.append(polygon_symbolizer)
        # to add outlines to a polygon we create a LineSymbolizer
        # line_symbolizer = mapnik.LineSymbolizer()
        # line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
        # line_symbolizer.stroke_width = 0.0 #1.0  #0.1
        # r.symbols.append(line_symbolizer) # add the symbolizer to the rule object
        r.filter = mapnik.Filter("[unit] = '{}'".format(name))
        s.rules.append(r) # now add the rule to the style and we're done

    m.append_style('Polys Style', s)

    s = mapnik.Style()

    r = mapnik.Rule()
    line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.stroke = mapnik.Color('rgb(50%,50%,50%)')
    line_symbolizer.stroke_width = 0.5 # 0.1
    r.symbols.append(line_symbolizer)
    s.rules.append(r)

    m.append_style('Lines Style', s)

    # ds = mapnik.Shapefile(file='ne_110m_admin_0_countries.shp')

    # layer = mapnik.Layer('world') # new layer called 'world' (we could name it anything)
    # note: layer.srs will default to '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'

    # layer.datasource = ds
    # layer.styles.append('My Style')
    #m.layers.append(layer)


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


    # Command to create the tiny ones: "time ./filter.py"

    geolines_datasource = mapnik.Ogr(
        #file='geolines.geojson',
        #layer='geolines',
        file='tiny_lines.geojson',
        layer='tiny_lines',
    )

    geopolys_datasource = mapnik.Ogr(
        # file='geopolys.geojson',
        # layer='geopolys',
        file='tiny_polys.geojson',  # Command: "time ./filter.py"
        layer='tiny_polys',
    )

    polys_layer = mapnik.Layer('Polys Layer')
    polys_layer.datasource = geopolys_datasource
    polys_layer.styles.append('Polys Style')
    m.layers.append(polys_layer)

    lines_layer = mapnik.Layer('Lines Layer')
    lines_layer.datasource = geopolys_datasource
    lines_layer.styles.append('Lines Style')
    m.layers.append(lines_layer)

    # m.zoom_all()

    bbox = mapnik.Box2d(-112.2500, 36.0000, -112.0000, 36.2500)
    merc_bbox = transform.forward(bbox)
    m.zoom_to_box(merc_bbox)


    mapnik.render_to_file(m, 'world.png', 'png')

    # m = mapnik.Map(256,256)
    # mapnik.load_map(m, "file.xml")
    # m.zoom_all()
    # mapnik.render_to_file(m, "the_image.png")

if __name__ == '__main__':
    render()
