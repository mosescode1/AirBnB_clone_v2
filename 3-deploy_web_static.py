#!/usr/bin/python3
"""Deploying an Archive to my server"""
from fabric.api import *
from datetime import datetime
import sys
import os

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
    if os.path.exists(archive_path) is False:
        return False

    try:
        put(archive_path, "/tmp/")
        file_name = os.path.basename(archive_path).replace(".tgz", "")
        run(
            f"mkdir -p /data/web_static/releases/{file_name}/"
        )
        file = f"xzf /tmp/{file_name}.tgz"
        run(
            f"tar - {file} - C /data/web_static/releases/{file_name} /"
        )
        run(f"rm /tmp/{file_name}.tgz")
        mv_1 = f"/data/web_static/releases/{file_name}/web_static/*"
        run(
            f"mv {mv_1} /data/web_static/releases/{file_name}/"
        )
        run(f"rm -rf /data/web_static/releases/{file_name}/web_static")
        run("rm -rf /data/web_static/current")
        mv_2 = "/data/web_static/releases/{file_name}/"
        run(
            f"ln -s {mv_2} /data/web_static/current"
        )
        print("New version deployed")
        return True
    except Exception as e:
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
    local("mkdir -p versions")
    result = local(f"tar -czvf versions/{file_name} web_static")
    path = os.path.abspath(f"versions/{file_name}")
    size = os.path.getsize(path)
    # print(path)
    if result.failed:
        return None
    print(f"web_static packed: versions/{file_name} -> {size}Bytes")
    return path


def deploy():
    """
    Deploys the web static files by calling the `do_pack` and `do_deploy` functions.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    try:
        path = do_pack()
    except Exception as e:
        return False
    try:
        return do_deploy(path)
    except Exception as e:
        pass
