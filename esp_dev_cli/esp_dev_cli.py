from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import click
import sys
import logging

from .docker_command import wrap_command

CONTEXT_SETTINGS = {'help_option_names': [], 'ignore_unknown_options': True}


@click.group(context_settings={'help_option_names': ['-h', '--help']})
def cli():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


@cli.command(help='Show documentation.')
@click.pass_context
def help(ctx):
    print(ctx.parent.get_help())

@cli.command(short_help='''Find hosts by service, role, or inventory.''', context_settings=CONTEXT_SETTINGS)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def ls(args):
    wrap_command('ls', args)

@cli.command(short_help='''Find hosts by service, role, or inventory.''', context_settings=CONTEXT_SETTINGS)
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def make(args):
    wrap_command('make', args)

if __name__ == '__main__':
    cli()