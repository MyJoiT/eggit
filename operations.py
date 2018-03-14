# -*- coding: utf-8 -*-

from datetime import datetime

from fabric.api import cd, env, get, lcd, local, run, put, prompt

env.hosts = ['47.52.16.229']
env.user = 'joit'
env.password = 'wzws670xs'
# env.warn_only = True

proj_folder = 'eggit'

remote_proj_path_root = '/home/joit/www'
remote_zip_repo_path = '/home/joit/zip'
remote_back_path = '/home/joit/backup'

local_proj_path_root = '/home/joit/Projects/joit'
local_receive_path = '/home/joit/Documents'
local_zip_repo_path = '/home/joit/Repo'

# region thread


def status():
    run('supervisorctl status')


# endregion

# region tools


def tar_and_gz(zip_repo_path, file_name, folder, excludes=[]):
    """TODO: 生成打包并开启gzip压缩的tar命令

    :zip_repo_path: 压缩包的存放目录
    :file_name: tar file name
    :folder: wait for tar
    :returns: tar czvf xxx command

    """
    if not zip_repo_path or not file_name or not folder:
        return None

    cmd_prefix = 'tar '
    if excludes:
        for i, exclude in enumerate(excludes):
            cmd_prefix += '--exclude=%(folder)s/%(exclude)s ' % {
                'folder': folder,
                'exclude': exclude
            }

    cmd = '%(cmd_prefix)s -czvf %(zip_repo_path)s/%(file_name)s %(folder)s' % {
        'cmd_prefix': cmd_prefix,
        'zip_repo_path': zip_repo_path,
        'file_name': file_name,
        'folder': folder
    }

    return cmd


def tgz_file_name(gzip_file_name_prefix):
    """TODO: 生成压缩文件名

    :file_name_prefix: 压缩文件名前缀
    :returns: xxx.20170909120000.tar.gz

    """

    dt = datetime.now().strftime('%Y%m%d%H%M%S')
    gzip_file_name = '%(file_name_prefix)s.%(dt)s.tar.gz' % {
        'file_name_prefix': gzip_file_name_prefix,
        'dt': dt
    }

    return gzip_file_name


# endregion

# region files


def __get_core(gzip_file_name_prefix, path, folder):
    target_root_path = remote_proj_path_root
    if path:
        target_root_path = remote_proj_path_root + path

    gzip_file_name = tgz_file_name(gzip_file_name_prefix)

    with cd(target_root_path):
        cmd = tar_and_gz(remote_zip_repo_path, gzip_file_name, folder)
        run(cmd)

    remote_file_path = '%(remote_zip_repo_path)s/%(zip_file)s' % {
        'remote_zip_repo_path': remote_zip_repo_path,
        'zip_file': gzip_file_name
    }

    get(remote_file_path, local_receive_path)


def get_logs(proj='app'):
    path = '/%(proj_folder)s/src/%(prefix)s_apis' % {
        'proj_folder': proj_folder,
        'prefix': proj
    }
    gzip_file_name_prefix = 'ganten-%s-logs' % proj
    folder = 'logs'

    __get_core(gzip_file_name_prefix, path, folder)


def get_static(proj='app'):
    path = '/%(proj_folder)s/src/%(prefix)s_apis' % {
        'proj_folder': proj_folder,
        'prefix': proj
    }
    gzip_file_name_prefix = 'ganten-%s-static' % proj
    folder = 'static'

    __get_core(gzip_file_name_prefix, path, folder)


def get_src():
    path = '/%s' % proj_folder
    gzip_file_name_prefix = '%s-src' % proj_folder
    folder = 'src'

    __get_core(gzip_file_name_prefix, path, folder)


def get_entire():
    path = None
    gzip_file_name_prefix = 'ganten-entire'

    __get_core(gzip_file_name_prefix, path, proj_folder)


# endregion

# region deploy


def __put_core(gzip_file_name_prefix,
               extra_path,
               folder,
               backup=True,
               backup_gzip_file_name_prefix='backup',
               delete=False):

    if folder == '/' or folder == '~/' or folder == '/home':
        print 'folder error'
        return None

    target = local_proj_path_root

    if extra_path:
        target = local_proj_path_root + extra_path

    gzip_file_name = tgz_file_name(gzip_file_name_prefix)

    with lcd(target):
        cmd = tar_and_gz(
            local_zip_repo_path,
            gzip_file_name,
            folder,
            excludes=['.*', '*cache*'])

        local(cmd)

        put(local_zip_repo_path + '/' + gzip_file_name,
            remote_zip_repo_path + '/' + gzip_file_name)

        with cd(remote_proj_path_root):

            if backup:
                backup_gzip_file_name = tgz_file_name(
                    backup_gzip_file_name_prefix)

                backup_cmd = tar_and_gz(remote_back_path,
                                        backup_gzip_file_name, folder)

                run(backup_cmd)

            if delete:
                sure = prompt(
                    '该操作将导致原有部署被删除，若有备份可恢复，否则将永远无法恢复，是否确定（y/n）',
                    default='n',
                    validate=str)

                if sure == 'y':
                    run('rm -rf %s' % folder)
                    print '删除原有部署完成'
                else:
                    print '取消删除原有部署，原有部署将保留，同时保留新部署的新文件'

            run('mv %(remote_zip_repo_path)s/%(gzip_file_name)s %(remote_proj_path_root)s && \
                tar xzvf %(remote_proj_path_root)s/%(gzip_file_name)s && \
                rm %(remote_proj_path_root)s/%(gzip_file_name)s' % {
                'remote_zip_repo_path': remote_zip_repo_path,
                'gzip_file_name': gzip_file_name,
                'remote_proj_path_root': remote_proj_path_root
            })

            run('supervisorctl restart gantenapp')

            run('supervisorctl restart gantenadmin')

            run('supervisorctl status')


def deploy(backup=True, delete=False):
    gzip_file_name_prefix = 'deploy.%s' % proj_folder
    backup_gzip_file_name_prefix = 'backup.%s' % proj_folder
    extra_path = None

    __put_core(
        gzip_file_name_prefix,
        extra_path,
        proj_folder,
        backup=True,
        backup_gzip_file_name_prefix=backup_gzip_file_name_prefix,
        delete=delete)


def put_file(local, remote):
    local_file_path = local_proj_path_root + '/' + proj_folder + local
    remote_file_path = remote_proj_path_root + '/' + proj_folder + remote

    put(local_file_path, remote_file_path)


#endregion
