#!/usr/bin/python3
"""Deploying an Archive to my server"""
from fabric.api import *
from datetime import datetime
import sys
from os.path import *

if len(sys.argv) > 1:
    env.user = sys.argv[-1]
    env.key_filename = sys.argv[-3]
else:
    print("Please provide a user argument.")
    sys.exit(1)

env.hosts = ["107.23.92.1", "100.26.249.41"]


def deploy_arch(archive_path):
    """
    Deploy a web static archive to the web servers.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    if exists(archive_path) is False:
        return False

    try:
        filename = archive_path.split("/")[-1]
        no_excep = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}/'.format(path, no_excep))
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(filename, path, no_excep))
        run('sudo rm /tmp/{}'.format(filename))
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(path, no_excep))
        run('sudo rm -rf {}{}/web_static'.format(path, no_excep))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, no_excep))
        return True
    except BaseException:
        return False


def do_deploy(archive_path):
    """
    Deploy the specified archive to the remote server.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    return deploy_arch(archive_path)


file_name = "web_static_{}.tgz".format(datetime.now().strftime("%Y%m%d%H%M%S"))


def do_pack():
    """ Function to generate tgz file"""

    try:
        local("mkdir -p versions")
        result = local(f"tar -czvf versions/{file_name} web_static")
        path = abspath(f"versions/{file_name}")
        size = getsize(path)
        # print(path)
        if result.failed:
            return None
        print(f"web_static packed: versions/{file_name} -> {size}Bytes")
        return path
    except Exception:
        return False


def deploy():
    """
    Deploys the web static files by calling the
    `do_pack` and `do_deploy` functions.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
