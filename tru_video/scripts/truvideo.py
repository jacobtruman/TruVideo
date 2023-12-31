#!/usr/bin/env python

import argparse

from tru_video import TruVideo


def upper_case(string):
    return string.upper()


def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Run TruVideo Functions',
    )

    parser.add_argument(
        '-d', '--dry_run',
        action='store_true',
        dest='dry_run',
        help='Dry run mode',
        default=False,
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='verbose',
        help='Enable verbose logging',
    )

    parser.add_argument(
        '-p', '--purge',
        action='store_true',
        dest='purge',
        help='Purge successfully converted source files',
    )

    parser.add_argument(
        '-s', '--source',
        dest='source',
        help="Source directory or file",
        default="./",
    )

    parser.add_argument(
        '-o', '--overwrite',
        action='store_true',
        dest='overwrite',
        help='Overwrite existing files',
    )

    parser.add_argument(
        '-c', '--config_file',
        dest='config_file',
        help="Config file",
        default="~/.config/truvideo/config.json",
    )

    parser.add_argument(
        '-l', '--log_level',
        dest='log_level',
        help="Log level",
        type=upper_case,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    truvideo = TruVideo(
        dry_run=args.dry_run,
        verbose=args.verbose,
        log_level=args.log_level,
        source=args.source,
        overwrite=args.overwrite,
        purge=args.purge,
        config_file=args.config_file,
    )

    truvideo.run()

    for video_file, result in truvideo.results.items():
        print(f"{video_file}: processed {'successfully' if result else 'unsuccessfully'}")


if __name__ == '__main__':
    main()
