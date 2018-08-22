#!/usr/bin/env python

import argparse
import contextlib
import json
import sys

from nbencdec.exporters import EncodedPythonExporter


STRIPPED_NOTEBOOK_MARKER = "# EPY: stripped_notebook: "
EPY_START_MARKER = "# EPY: START "
EPY_TRANSFORM_MARKER = "# EPY: ESCAPE "
EPY_END_MARKER = "# EPY: END "


@contextlib.contextmanager
def stdio_wrapper(stdio_fh):
    yield stdio_fh


def open_possibly_stdio(stdio_handle, filename, mode):
    """
    Given a filename, either return a contextmanager wrapping `stdio_handle` if
    `filename` is "-", or a handle to the file specified in `filename`.
    """
    if filename == "-":
        return stdio_wrapper(stdio_handle)
    else:
        return open(filename, mode)

def decode(args):
    notebook = {
        'cells': []
    }

    with open_possibly_stdio(sys.stdin, args.source, "r") as input_fh:
        iterator = iter(input_fh.readlines())

        # read until we get the stripped notebook marker.
        for line in iterator:
            if line.startswith(STRIPPED_NOTEBOOK_MARKER):
                remainder = line[len(STRIPPED_NOTEBOOK_MARKER):]
                notebook.update(json.loads(remainder))
                break

        while True:
            cell = {
                'metadata': {},
                'source': [],
            }
            # read until the first start marker
            for line in iterator:
                if line.startswith(EPY_START_MARKER):
                    remainder = line[len(EPY_START_MARKER):].rstrip()
                    cell['cell_type'] = remainder

                    expected_transform = EPY_TRANSFORM_MARKER
                    expected_end_marker = EPY_END_MARKER
                    break
            else:
                break

            for line in iterator:
                if line.startswith(expected_end_marker):
                    break
                if line.startswith(expected_transform):
                    remainder = line[len(expected_transform):]
                    cell['source'].append(remainder)
                    continue

                if cell['cell_type'] == 'markdown':
                    line = line[1:]
                cell['source'].append(line)

            if cell['cell_type'] == 'code':
                cell['execution_count'] = None
                cell['outputs'] = []

            # strip the final "\n" from the last line.  it's weird.
            if len(cell['source']) > 0 and cell['source'][-1].endswith("\n"):
                cell['source'][-1] = cell['source'][-1][:-1]

            notebook['cells'].append(cell)

    with open_possibly_stdio(sys.stdout, args.output, "w") as output_fh:
        json.dump(
            notebook, output_fh,
            sort_keys=True, indent=1, separators=(',', ': '))


def encode(args):
    encoder = EncodedPythonExporter()

    with open_possibly_stdio(sys.stdin, args.notebook, "r") as input_fh, \
          open_possibly_stdio(sys.stdout, args.output, "w") as output_fh:
        encoded, _ = encoder.from_file(input_fh)
        output_fh.write(encoded)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    decode_group = subparsers.add_parser("decode")
    decode_group.set_defaults(command=decode)
    decode_group.add_argument("source", help="The python with extra state embedded to reconstitute an .ipynb file")
    decode_group.add_argument("output", help="The reconstituted .ipynb file")

    encode_group = subparsers.add_parser("encode")
    encode_group.set_defaults(command=encode)
    encode_group.add_argument("notebook", help="The .ipynb file to encode to a .py file")
    encode_group.add_argument("output", help="The encoded .py file")

    return parser, parser.parse_args()


def main():
    parser, args = parse_args()

    if args.command is None:
        parser.print_help()
        parser.exit(status=2)
    args.command(args)
