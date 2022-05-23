#!/usr/bin/python3
# Fabric script (based on the file 2-do_deploy_web_static.py)
# that creates and distributes an archive to your web servers
from datetime import datetime
from fabric.api import put, run, env, local
from os.path import exists
env.hosts = ['34.138.104.139', '54.89.111.28']


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


def deploy():
    """
    Call do_pack and do_deploy
    """
    try:
        archive_path = do_pack()
    except Exception:
        return False

    return do_deploy(archive_path)
