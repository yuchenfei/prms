import random

from fabric.contrib.files import exists, sed, append
from fabric.api import env, run, local

env.use_ssh_config = True

REPO_URL = 'https://github.com/yuchenfei/prms.git'


def deploy():
    """部署应用至服务器"""
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    """创建目录结构"""
    for subfolder in ('database', 'static', 'media', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    """获取最新代码"""
    if exists(source_folder + '/.git'):
        run('cd %s && git fetch' % (source_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    """更新Django配置文件"""
    settings_path = source_folder + '/prms/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name,)
        )
    sed(settings_path, "'read_default_file': 'prms/my.cnf'", "'read_default_file': '../database/my.cnf'")
    secret_key_file = source_folder + '/prms/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghjiklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    """创建更新虚拟环境"""
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, source_folder
    ))


def _update_static_files(source_folder):
    """更新静态文件"""
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder,
    ))


def _update_database(source_folder):
    """更新数据库"""
    my_cnf = source_folder + '/../database/my.cnf'
    if not exists(my_cnf):
        run('cd %s && cp deploy_tools/my.cnf ../database/my.cnf' % (source_folder,))
        print('请在服务器上完成MySQL配置，然后重新运行fab，配置文件目录：%s/database/my.cnf' % (source_folder,))
    else:
        run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder,))
