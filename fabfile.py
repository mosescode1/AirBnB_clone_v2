#!/usr/bin/python3
"""
creating a tar xip file 
"""
from fabric.operations import local
from datetime import datetime

def do_pack():
    """Function to compress files(make a .tgz file)"""
    local("mkdir -p versions")
    result = local("tar -cvzf versions/web_static_{}.tgz web_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if result.failed:
        return None
    return result
