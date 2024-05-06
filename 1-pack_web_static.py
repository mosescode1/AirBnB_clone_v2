#!/usr/bin/python3
""" A script that generates tgz archive from the contents """
from fabric.api import local
from datetime import datetime
import os

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
