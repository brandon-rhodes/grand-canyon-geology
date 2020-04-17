#!/usr/bin/env python3

# Cut down a huge GeoJSON polygon file to something manageable.

import argparse
import json
import sys

def main(argv):
    parser = argparse.ArgumentParser(description='Filter our GeoJSON file')
    # parser.add_argument('path', help='Path to GeoJSON file')
    args = parser.parse_args(argv)

    with open('../data/geopolys.geojson') as f:
        j = json.load(f)

    # Save feature metadata.

    feature_colors = {
        feature['properties']['unit']: feature['properties']['color']
        for feature in j['features']
    }
    with open('feature_colors.json', 'w') as f:
        json.dump(feature_colors, f, indent=2)

    # Save a much smaller version of the dataset for testing.

    j['features'] = [
        feature for feature in j['features']
        if feature['properties']['unit'] in ('Mr', 'water')
    ]

    with open('tiny_polys.geojson', 'w') as f:
        json.dump(j, f)

if __name__ == '__main__':
    main(sys.argv[1:])


