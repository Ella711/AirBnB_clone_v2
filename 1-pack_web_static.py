#!/usr/bin/python3
# Fabric script that generates a .tgz archive from the
# contents of the web_static folder
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generate a .tgz archive from contents of web_static folder
    """
    current_time = datetime.now().strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        tgz_filename = "versions/web_static_{}.tgz".format(current_time)
        local("tar -cvzf {} web_static/".format(tgz_filename))
        return tgz_filename
    except Exception:
        return None
