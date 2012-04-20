from fabric.api import env, sudo, run
from fabric.context_managers import prefix

##########################
# User management
##########################


def server_create_user(name, target):
    "Create user on the deployment and production servers"
    print("This command can only be executed by the root user")
    env.user = 'root'
    if target == 'dev':
        env.hosts = [env.project_sites['development']['NAME']]
    elif target == 'prod':
        env.hosts = [env.project_sites['production']['NAME']]

    env.host_string = env.hosts[0]
    run('useradd -m {0}'.format(name))
    run('gpasswd -a {0} wheel'.format(name))
    run('passwd {0}'.format(name))
    print("Make sure that the wheel group has sudo rights")
    print("ssh root@[yourserver]")
    print("run visudo manually and uncomment the %wheel group")


##########################
# Server-side stuff
##########################


def server_setup_standardpackages():
    sudo('pacman -S tmux htop git-core --noconfirm')


def server_setup_fullsystemupgrade():
    sudo('pacman -Syyu --noconfirm')


def server_setup_community_repo():
    run('echo \'echo "[archlinuxfr]" >> /etc/pacman.conf\' | sudo -s')
    run('echo \'Server = http://repo.archlinux.fr/$arch\' | sudo -s tee -a /etc/pacman.conf')
    run('echo \'echo " " project_home_stringpacman.conf\' | sudo -s')
    sudo('pacman -Syy yaourt --noconfirm')


def server_setup_mirror():
    """Installs necessary packages on host, depending on distro specified"""
    # Here are the arch-specific installs
    country = "Singapore"
    mirror_url = "http://www.archlinux.org/mirrorlist/?country={0}&protocol=ftp&protocol=http&ip_version=4&use_mirror_status=on".format(country)
    create_tmpfile = run('mktemp --suffix=-mirrorlist')
    tmpfile = create_tmpfile
    run('wget -qO- "{0}" | sed "s/^#Server/Server/g" > "{1}"'.format(mirror_url, tmpfile))
    print('Backing up the original mirrorlist...')
    sudo('mv -if /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.orig;')
    print('Rotating the new list into place...')
    sudo('mv -i "{0}" /etc/pacman.d/mirrorlist;'.format(tmpfile))


def server_setup_bash_profile():
    sudo("echo \"PS1='\\[\\033[0;31m\\]\\H \\l \\[\\033[1;33m\\]\\d \\[\\033[1;36m\\]\\t\\[\\033[0;32m\\] |\\w|\\[\\033[0m\\]\n\\u\\$ ';\" > ~/.bash_profile")


def server_setup_base():
    sudo('pacman -Syy --noconfirm')
    sudo('pacman -S tzdata')
    sudo('pacman -Sy pacman --noconfirm')
    sudo('pacman -S base-devel --noconfirm')
    sudo('pacman -S filesystem --force --noconfirm')
    sudo('rm /etc/profile.d/locale.sh')


def server_setup_python():
    sudo('pacman -S python2 --noconfirm')
    sudo('ln -s /usr/bin/python2 /usr/local/bin/python')  # handle arch-specific quirk
    sudo('pacman -S python2-distribute --noconfirm')
    sudo('pacman -S python2-pip --noconfirm')
    sudo('pip2 install virtualenvwrapper')


def server_setup_python_env():
    sudo('echo \'export WORKON_HOME=$HOME/.virtualenvs\' >> ~/.bash_profile')
    sudo('echo \'export PROJECT_HOME=$HOME/work\' >> ~/.bash_profile')
    sudo('echo \'source `which virtualenvwrapper.sh`\' >> ~/.bash_profile')
    with prefix(env.activate):
        sudo('mkdir $PROJECT_HOME')
