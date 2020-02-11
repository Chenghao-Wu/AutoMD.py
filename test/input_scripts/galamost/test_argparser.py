#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(description='galamost.')

parser.add_argument('-directory', type=str,nargs=1,
                   help='directory for the simulation')