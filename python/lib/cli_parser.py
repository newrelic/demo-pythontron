
import sys
import argparse

class CliParser(object):

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--config", action="store", dest="config_file", help="Pythontron config file", metavar="FILE")
        parser.add_argument("-l", "--logging", action="store", dest="logging_level", default="info", help="trace, info (default), warning, error")
        parser.add_argument("-d", "--debug", action="store", dest="debug_mode", default="Off", help="Enable server debugger. Off by default. Options Off, On")
        if len(sys.argv)==1:
            parser.print_help(sys.stderr)
            sys.exit(1)
        args = parser.parse_args()

        return args