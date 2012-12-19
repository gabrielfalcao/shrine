#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import optparse


def main(args=sys.argv[1:]):
    base_path = os.path.join(os.getcwdu())

    parser = optparse.OptionParser(
        usage="%prog or type %prog -h (--help) for help",
        version='0.1.0')

    parser.add_option("-c", "--create",
                      dest="name",
                      default=None,
                      help='Name of the project to be created')

    options, args = parser.parse_args(args)
    if args:
        base_path = os.path.abspath(args[0])

    import ipdb;ipdb.set_trace()

if __name__ == '__main__':
    main()
