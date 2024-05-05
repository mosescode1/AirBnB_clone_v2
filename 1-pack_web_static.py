#!/usr/bin/python3
"""
fabric script 
"""


from fabric.operations import local
from datetime import datetime

def do_pack():
    """Web_static compressor"""
    local("mkdir -p versions")
    result = local("tar -cvzf versions/web_static_{}.tgz web_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if result.failed:
        return None
    return result
