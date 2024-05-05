#!/usr/bin/python3
"""
creating a tar xip file 
"""
from fabric.operations import local
from datetime import datetime
import os

path_file = "versions/web_static_{}.tgz".format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S"))
command = "tar -cvzf {} web_static".format(path_file)
total_path = "/AirBnB_clone_v2/{}".format(path_file)

def do_pack():
    """Function to compress files(make a .tgz file)"""
    local("mkdir -p versions")
    result = local(command)
    if result.failed:
        return None
    print("web_static packed:",path_file,"->", f"{os.path.getsize(total_path)}Bytes")
