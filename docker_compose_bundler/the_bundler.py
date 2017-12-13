#-*- coding: utf-8 -*-
#!/usr/bin/env python

import yaml
from docker_compose_bundler import __version__
import os
import commands
from functools import partial
import argparse
import textwrap
from pathlib import Path

DEFAULT_COMPOSE_FILE = "docker-compose.yml"


def args_parse():
    global args
    parser = argparse.ArgumentParser(prog='docker_compose_bundler',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(
                                         'bundle docker images to tarball base on docker-compose.yml that can then be used with docker load.\ndocker_compose_bundler -o bundle.tar')
                                     )
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(__version__))
    parser.add_argument('-f, --file', dest="file", default=DEFAULT_COMPOSE_FILE, metavar="FILE",
                        action='store', type=str, help='Specify an alternate compose file (default: docker-compose.yml)')
    parser.add_argument('-p, --project-name', dest="name", default="", metavar="NAME", action='store',
                        type=str, help='Specify an alternate project name (default: directory name)')
    parser.add_argument('--project-directory', dest="directory", default=".", metavar="PATH", action='store',
                        type=str, help='Specify an alternate working directory\n(default: the path of the Compose file)')
    parser.add_argument('-o , --output', dest="output", default="",
                        metavar="string", action='store', type=str, help='Write to a file .tar')
    parser.add_argument('-xz', dest="xz", default=False,action='store_true', help='Write to a xz(docker prerequisites) compressed file .tar.xz ')
    args = parser.parse_args()


def command():
    compose_file_path = Path(args.file)
    directory = Path(args.directory)
    name = args.name
    use_xz = args.xz
    output = Path(args.output)
    if output.suffix == "":
        output.with_suffix(".tar")
    elif output.suffix == ".tar":
        if use_xz:
            output.with_suffix(".xz")
    elif output.suffix == '.xz':
        use_xz = True
    os.chdir(str(directory))
    images = []
    with open(str(compose_file_path)) as f:
        # use safe_load instead load
        dataMap = yaml.safe_load(f)
        dirname = os.path.basename(os.getcwd())
        prefix = dirname.lower().replace("_", "") if name == "" else name
        service_image_name = partial("{0}_{1}".format, prefix)
        for service_k, service_v in dataMap["services"].iteritems():
            if service_v.has_key("build") and service_v.has_key("image"):
                # taged build
                images.append(service_v["image"])
            elif service_v.has_key("build"):
                # use build
                images.append(service_image_name(service_k))
            elif service_v.has_key("image"):
                # use image
                images.append(service_v["image"])
            else:
                pass
    images_str = " ".join(images)
    if use_xz:
        bundle_command = "docker save {images} | xz -zv --threads=0 > {output}".format(
        output=str(output), images=images_str)
    else:
        bundle_command = "docker save -o {output} {images}".format(
        output=str(output), images=images_str)
    
    code,r = commands.getstatusoutput(bundle_command)
    if code != 0:
        raise Exception(r)
    else:
        print(r)


def main():
    args_parse()
    command()
