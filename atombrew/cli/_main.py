import argparse


parser = argparse.ArgumentParser(description="PyNotion command line tool")
subparsers = parser.add_subparsers(dest="command", required=True)
