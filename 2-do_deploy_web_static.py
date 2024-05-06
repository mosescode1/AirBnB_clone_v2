#!/usr/bin/python3
"""Deploying an Archive to my server"""
from fabric.api import *
import sys
import os

env.user = sys.argv[-1]
env.key_filename = sys.argv[-3]


env.hosts = ["107.23.92.1", "100.26.249.41"]


def do_deploy(archive_path):
    """
    Deploy a web static archive to the web servers.

    Args:
        archive_path (str): The path to the archive file.

    Returns:
        bool: True if the deployment is successful, False otherwise.
    """
    if not os.path.isfile(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")
        file_name = os.path.basename(archive_path).replace(".tgz", "")
        run(f"mkdir -p /data/web_static/releases/{file_name}/")
        run(f"tar -xzf /tmp/{file_name}.tgz -C /data/web_static/releases/{file_name}/")
        run(f"rm /tmp/{file_name}.tgz")
        run(
            f"mv /data/web_static/releases/{file_name}/web_static/* /data/web_static/releases/{file_name}/"
        )
        run(f"rm -rf /data/web_static/releases/{file_name}/web_static")
        run("rm -rf /data/web_static/current")
        run(
            f"ln -s /data/web_static/releases/{file_name}/ /data/web_static/current")
        print("New version deployed")
        return True
    except Exception as e:
        return False
