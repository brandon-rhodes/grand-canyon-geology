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

    j['features'] = [
        feature for feature in j['features']
        if feature['properties']['unit'] == 'water'
    ]

    with open('tiny_polys.geojson', 'w') as f:
        json.dump(j, f)

if __name__ == '__main__':
    main(sys.argv[1:])


