from typing import Dict, List
import argparse
import os
import sys


def ask_for_fields(fields: List[Dict]):
    result = []
    for field in fields:
        key = field['key']
        value = input('please informe the {}: '.format(key))
        result.append({'key': key, 'value': value})
    return result


def get_args():
    parser = argparse.ArgumentParser(
        prog=__package__,
        usage='%(prog)s path [options]',
        description='Create new projects easily based in a template',
        epilog='Enjoy the program! :)'
    )

    parser.add_argument(
        'path',
        metavar='path',
        type=str,
        help='path where the project should be created'
    )

    parser.add_argument(
        '-l',
        '--local',
        action='store',
        default='template',
        help='local folder where the template was defined'
    )

    return parser.parse_args()


def validate_args(args):
    if not os.path.isdir(args.local):
        print('The local path specified does not exist')
        sys.exit()

    return args
