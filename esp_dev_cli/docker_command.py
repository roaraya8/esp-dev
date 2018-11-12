from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import re
import sys
import uuid
import json
import subprocess
import os
import logging


_client = None
def docker():
    global _client
    if not _client:
        _client = client_from_env(version='auto')
    return _client


_image = None
def image():
    global _image
    if not _image :
        _image = 'esp32-dev:latest'
    return _image

def wrap_command(command, args, environment=None):
    container_name = 'esp-dev-cli-%s' % str(uuid.uuid4()).replace('-', '')
    docker_command = [
        'docker', 'run',
        '-i',
        '--name', container_name,
    ]
    if sys.stdout.isatty() and sys.stdin.isatty():
        docker_command.append('-t')

    if environment:
        for key, value in environment.items():
            docker_command += ['-e', '%s=%s' % (key, value)]

    cwd = os.getcwd()
    cwd_unix = make_unix_path(os.getcwd())
    docker_command += [
        '-v', '/var/run/docker.sock:/var/run/docker.sock:rw',
    ]

    if cwd_unix == '/':
        logging.warning('Running from file system root, will not mount present working directory.')
    else:
        docker_command += [
            '-v', '%s:%s:rw' % (cwd, cwd_unix),
        ]

    docker_command += referenced_file_mount_args(args)

    docker_command += [
                          '-w', cwd_unix,
                          image(),
                      ] + [command] + list(args)

    try:
        stdin_has_input = not sys.stdin.isatty()

        proc = subprocess.Popen(
            docker_command, shell=False,
            stdin=subprocess.PIPE if stdin_has_input else None,
        )

        if stdin_has_input:
            proc.stdin.write(sys.stdin.read().encode())
            proc.communicate()
        else:
            proc.wait()

    finally:
        try:
            subprocess.check_output(['docker', 'rm', '-f', container_name], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            # container already removed?
            pass


def referenced_file_mount_args(args):
    mount_args = []
    for arg in args:
        if '/' in arg and os.path.exists(arg) and os.path.isfile(arg):
            abspath = os.path.abspath(os.path.expanduser(arg))
            mount_args += ['-v', '%s:%s:rw' % (abspath, abspath)]
    return mount_args


def make_unix_path(path):
    # TODO: is this general enough?
    path = re.sub(r'^[A-Z]:\\?', '/', path)
    path = path.replace('\\', '/')
    return path


def image_info():
    try:
        output = subprocess.check_output(['docker', 'image', 'inspect', image()])
    except subprocess.CalledProcessError:
        raise ImageNotFound()

    return json.loads(output)


def pull_image():
    try:
        info = image_info()
    except ImageNotFound:
        info = None

    if info is None:
        logging.info('Pulling image with all bundled Spotify commands from GCR')
        subprocess.call(['docker', 'pull', image()])


class ImageNotFound(Exception): pass
