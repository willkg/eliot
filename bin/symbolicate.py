#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Sends a stack for symbolication with a Symbols server using the symbolicate service
# API.

# Usage: ./bin/symbolicate.py CMD FILE

import json
import os
import sys

import click
import jsonschema
import requests


def load_schema(path):
    with open(path) as fp:
        schema = json.load(fp)
    jsonschema.Draft7Validator.check_schema(schema)
    return schema


class RequestError(Exception):
    pass


def request_stack(url, payload, is_debug):
    headers = {"User-Agent": "eliot-symbolicate"}

    if "v4" in url:
        api_version = 4
    else:
        api_version = 5

    if api_version == 4:
        # We have to add the version to the payload, so parse it, add it, and then
        # unparse it.
        payload["version"] = 4

    options = {}
    if is_debug:
        headers["Debug"] = "true"

    # NOTE(willkg): this triggers the Allow-Control-* CORS headers, but maybe we want to
    # make the origin specifiable via the command line arguments
    headers["Origin"] = "http://example.com"

    resp = requests.post(url, headers=headers, json=payload, **options)
    if is_debug:
        click.echo(click.style(f"Response: {resp.status_code} {resp.reason}"))
        for key, val in resp.headers.items():
            click.echo(click.style(f"{key}: {val}"))

    if resp.status_code != 200:
        # The server returned something "bad", so print out the things that
        # would be helpful in debugging the issue.
        click.echo(
            click.style(f"Error: Got status code {resp.status_code}", fg="yellow")
        )
        click.echo(click.style("Request payload:", fg="yellow"))
        click.echo(payload)
        click.echo(click.style("Response:", fg="yellow"))
        click.echo(resp.content)
        raise RequestError()

    return resp.json()


@click.group()
def symbolicate_group():
    """Symbolicate stack data."""


@symbolicate_group.command("print")
@click.option(
    "--api-url",
    default="https://symbolication.services.mozilla.com/symbolicate/v5",
    help="The API url to use.",
)
@click.option(
    "--debug/--no-debug", default=False, help="Whether to include debug info."
)
@click.argument("stackfile", required=False)
@click.pass_context
def print_stack(ctx, api_url, debug, stackfile):
    if not stackfile and not sys.stdin.isatty():
        data = click.get_text_stream("stdin").read()

    else:
        if not os.path.exists(stackfile):
            raise click.BadParameter(
                "Stack file does not exist.",
                ctx=ctx,
                param="stackfile",
                param_hint="stackfile",
            )

        with open(stackfile) as fp:
            data = fp.read()

    try:
        payload = json.loads(data)
    except json.decoder.JSONDecodeError as jde:
        click.echo(f"Error: request is not valid JSON: {jde!r}\n{data!r}")
        return

    response_data = request_stack(api_url, payload, debug)
    if debug:
        click.echo(json.dumps(response_data, indent=2))
    else:
        click.echo(json.dumps(response_data))


@symbolicate_group.command("verify")
@click.option(
    "--api-url",
    default="https://symbolication.services.mozilla.com/symbolicate/v5",
    help="The API url to use.",
)
@click.argument("stackfile", required=False)
@click.pass_context
def verify_symbolication(ctx, api_url, stackfile):
    if not stackfile and not sys.stdin.isatty():
        data = click.get_text_stream("stdin").read()

    else:
        if not os.path.exists(stackfile):
            raise click.BadParameter(
                "Stack file does not exist.",
                ctx=ctx,
                param="stackfile",
                param_hint="stackfile",
            )

        with open(stackfile) as fp:
            data = fp.read()

    if stackfile:
        click.echo(click.style(f"Working on stackfile {stackfile} ...", fg="yellow"))
    else:
        click.echo(click.style("Working on stdin ...", fg="yellow"))

    if "v4" in api_url:
        api_version = 4
    else:
        api_version = 5

    payload = json.loads(data)
    response_data = request_stack(api_url, payload, is_debug=True)

    path = os.path.abspath(f"/app/schemas/symbolicate_api_response_v{api_version}.json")
    schema = load_schema(path)
    try:
        jsonschema.validate(response_data, schema)
        click.echo(click.style(f"Response is valid v{api_version}!", fg="green"))
    except jsonschema.exceptions.ValidationError as exc:
        click.echo(json.dumps(response_data, indent=2))
        click.echo(
            click.style(f"Response is invalid v{api_version}! {exc!r}", fg="red")
        )
        ctx.exit(1)


@symbolicate_group.command("compare")
@click.argument("url1")
@click.argument("url2")
@click.argument("stackfile", required=False)
@click.pass_context
def compare_symbolication(ctx, url1, url2, stackfile):
    if not stackfile and not sys.stdin.isatty():
        data = click.get_text_stream("stdin").read()

    else:
        if not os.path.exists(stackfile):
            raise click.BadParameter(
                "Stack file does not exist.",
                ctx=ctx,
                param="stackfile",
                param_hint="stackfile",
            )

        with open(stackfile) as fp:
            data = fp.read()

    if stackfile:
        click.echo(click.style(f"Working on stackfile {stackfile} ...", fg="yellow"))
    else:
        click.echo(click.style("Working on stdin ...", fg="yellow"))

    if "v4" in url1:
        url1_version = 4
    else:
        url1_version = 5

    if "v4" in url2:
        url2_version = 4
    else:
        url2_version = 5

    if url1_version != url2_version:
        click.echo(
            click.style(f"{url1} and {url2} are different api versions.", fg="red")
        )
        ctx.exit(1)

    api_version = url1_version

    payload = json.loads(data)

    click.echo(click.style(f"Downloading from {url1} ...", fg="yellow"))
    url1_resp = request_stack(url1, payload, is_debug=True)
    click.echo(click.style(f"Downloading from {url2} ...", fg="yellow"))
    url2_resp = request_stack(url2, payload, is_debug=True)

    path = os.path.abspath(f"/app/schemas/symbolicate_api_response_v{api_version}.json")
    schema = load_schema(path)
    try:
        jsonschema.validate(url1_resp, schema)
        click.echo(
            click.style(f"Response from {url1} is valid v{api_version}!", fg="green")
        )
    except jsonschema.exceptions.ValidationError as exc:
        click.echo(json.dumps(url1_resp, indent=2))
        click.echo(
            click.style(
                f"Response from {url1} is invalid v{api_version}! {exc!r}", fg="red"
            )
        )
        ctx.exit(1)

    try:
        jsonschema.validate(url2_resp, schema)
        click.echo(
            click.style(f"Response from {url2} is valid v{api_version}!", fg="green")
        )
    except jsonschema.exceptions.ValidationError as exc:
        click.echo(json.dumps(url1_resp, indent=2))
        click.echo(
            click.style(
                f"Response from {url1} is invalid v{api_version}! {exc!r}", fg="red"
            )
        )
        ctx.exit(1)

    url1_debug = url1_resp.pop("debug", {})
    url2_debug = url2_resp.pop("debug", {})
    if url1_resp != url2_resp:
        click.echo(click.style("url1 resp and url2 resp differ", fg="red"))
        # FIXME: show differences
        ctx.exit(1)

    click.echo(url1_debug)
    click.echo(url2_debug)


if __name__ == "__main__":
    symbolicate_group()
