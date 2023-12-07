#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Prints information about a sym file including whether it kicks up
# a parse error.

# Usage: debug-sym-file.py [SYMFILE]

from contextlib import contextmanager
import os
from time import perf_counter

import click

from eliot.libsymbolic import convert_debug_id, parse_sym_file


@contextmanager
def timer():
    start = perf_counter()
    yield
    click.echo(f"{perf_counter() - start:.3f}s")


@click.command()
@click.argument("symfile")
@click.pass_context
def sym_file_debug(ctx, symfile):
    """Prints information about a sym file including whether it parses correctly."""
    # Print size
    stats = os.stat(symfile)
    click.echo(f"{symfile}")
    click.echo(f"size: {stats.st_size:,}")

    # Print first line
    with open(symfile, "r") as fp:
        firstline = fp.readline().strip()

    parts = firstline.split(" ")
    click.echo(f"first line: {parts}")
    debug_id = convert_debug_id(parts[3])

    # Parse with symbolic and create symcache
    click.echo("parsing sym file with symbolic ... ", nl=False)
    with timer():
        with open(symfile, "rb") as fp:
            data = fp.read()
        parse_sym_file("file.sym", debug_id, data)


if __name__ == "__main__":
    sym_file_debug()
