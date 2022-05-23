#!/usr/bin/python3
# Fabric script (based on the file 1-pack_web_static.py) that distributes
# an archive to your web servers
from fabric.api import put, run, env
from os.path import exists
env.hosts = ['34.138.104.139', '54.89.111.28']


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    Returns False if the file at the path archive_path doesn't exist
    """
    if exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        filename_no_ext = filename.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("mkdir -p {}{}".format(path, filename_no_ext))
        run("tar -xzf /tmp/{} -C {}{}".format(filename, path, filename_no_ext))
        run("rm -rf /tmp/{}".format(filename))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, filename_no_ext))
        run('rm -rf {}{}/web_static'.format(path, filename_no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path,
                                                          filename_no_ext))
        return True
    except Exception:
        return False
