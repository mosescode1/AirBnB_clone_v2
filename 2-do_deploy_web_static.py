#!/usr/bin/python3
"""Deploying an Archive to my server"""
from fabric.api import *
import sys
import os

# print(dir(fabric.api))

env.hosts = ["107.23.92.1", "100.26.249.41"]
env.user = sys.argv[-1]

# print(dir(env.__dict__))

# strs = "versions/web_static_20170315003959.tgz"
# val = strs.split("/")[-1].strip(".tgz")
# print(val)


def deploy(archive_path):
    if not archive_path:
        return False
    put(archive_path, "/tmp/")
    file_name = os.path.basename(archive_path).replace(".tgz", "")
    run(f"mkdir -p /data/web_static/releases/{file_name}")
    run(f"tar -xzf /tmp/{file_name}.tgz -C /data/web_static/releases/{file_name}/")
    run(f"rm /tmp/{file_name}.tgz")
    run(f"mv /data/web_static/releases/{file_name}/web_static/* /data/web_static/releases/{file_name}/")
    run(f"rm -rf /data/web_static/releases/{file_name}/web_static")
    run("rm -rf /data/web_static/current")
    run(f"ln -s /data/web_static/releases/{file_name}/ /data/web_static/current")
    print("New version deployed")


def do_deploy(archive_path):
    deploy(archive_path)
