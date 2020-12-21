#!/usr/bin/env python3

# Cut down a huge GeoJSON polygon file to something manageable.

# To do the opposite:
#
# ln -f ../data/geolines.geojson tiny_lines.geojson && ln -f ../data/geopolys.geojson tiny_polys.geojson

import argparse
import json
import sys

def main(argv):
    parser = argparse.ArgumentParser(description='Filter our GeoJSON file')
    parser.add_argument('keeper', help='Layer to keep')
    args = parser.parse_args(argv)

    with open('../data/geolines.geojson') as f:
        geolines = json.load(f)

    with open('../data/geopolys.geojson') as f:
        geopolys = json.load(f)

    # Save feature metadata.

    feature_data = {
        'line_fgdc': {
            feature['properties']['fgdc']: '_'
            for feature in geolines['features']
        },
        'line_original': {
            feature['properties']['original']: '_'
            for feature in geolines['features']
        },
        'poly_color': {
            feature['properties']['unit']: feature['properties']['color']
            for feature in geopolys['features']
        },
    }
    with open('feature_data.json', 'w') as f:
        json.dump(feature_data, f, indent=2)

    # Save a much smaller version of the dataset for testing.

    skip = len(geolines['features']) // 1000
    geolines['features'] = geolines['features'][::skip]

    geopolys['features'] = [
        feature for feature in geopolys['features']
        if feature['properties']['unit'] in ('Mr', 'Pc', 'water', args.keeper)
    ]
    print('Matched {} features'.format(sum(
        1 for feature in geopolys['features']
        if feature['properties']['unit'] == args.keeper
    )))

    with open('tiny_lines.geojson', 'w') as f:
        json.dump(geolines, f)

    with open('tiny_polys.geojson', 'w') as f:
        json.dump(geopolys, f, indent=0, separators=(',', ':'))

if __name__ == '__main__':
    main(sys.argv[1:])
