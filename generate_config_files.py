#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
from settings import *

project_dir = os.path.join(base_dir, project_name)

sock_path = os.path.join(base_dir, sock_file)
pid_path = os.path.join(base_dir, pid_file)

env_path = os.path.join(base_dir, env_name)


nginx_config = """upstream {upstream_name} {{
     server unix://{sock_path};
}}

server {{
    listen      80;
    server_name {server_name};
    charset     utf-8;
    access_log  {nginx_access_logs};
    error_log   {nginx_error_logs};

    client_max_body_size 75M;

    location /media  {{
        root {media};
    }}

    location /static {{
        root {static};
    }}

    location / {{
        uwsgi_pass  {upstream_name};
        include     uwsgi_params;
    }}
}}
"""


def nginx():
    conf_filename = '%s_nginx.conf' % upstream_name

    nginx_logs = 'logs/nginx'
    nginx_access_logs = os.path.join(base_dir, nginx_logs, 'access.log')
    nginx_error_logs = os.path.join(base_dir, nginx_logs, 'error.log')

    media = os.path.join(base_dir, project_name, 'media')
    static = os.path.join(base_dir, project_name, 'static')

    config = nginx_config.format(upstream_name=upstream_name,
                                 server_name=server_name,
                                 sock_path=sock_path,
                                 nginx_access_logs=nginx_access_logs,
                                 nginx_error_logs=nginx_error_logs,
                                 media=media,
                                 static=static)

    config_file = open(conf_filename, "w")
    config_file.write(config)
    config_file.close()


supervisor_config = """[program:{upstream_name}]
stdout_logfile={supervisor_out_logs}
stderr_logfile={supervisor_err_logs}
stdout_logfile_maxbytes=100MB
stdout_logfile_backups=30
stdout_capture_maxbytes=1MB
numprocs={numprocs}
process_name={upstream_name}%(process_num)s
directory={project_dir}/
command={uwsgi_cmd}
user={user}
autostart=true
autorestart=true
stopwaitsecs=600
stopsignal=INT
"""


def supervisor():
    conf_filename = '%s_supervisor.conf' % upstream_name

    supervisor_logs = 'logs/supervisor'
    supervisor_out_logs = os.path.join(base_dir, supervisor_logs, upstream_name + '_ru_out.log')
    supervisor_err_logs = os.path.join(base_dir, supervisor_logs, upstream_name + '_ru_err.log')

    uwsgi_cmd = 'uwsgi /etc/uwsgi/{}.ini'.format(upstream_name)

    config = supervisor_config.format(
        upstream_name=upstream_name,
        supervisor_out_logs=supervisor_out_logs,
        supervisor_err_logs=supervisor_err_logs,
        numprocs=numprocs,
        project_dir=project_dir,
        uwsgi_cmd=uwsgi_cmd,
        user=user
    )

    config_file = open(conf_filename, "w")
    config_file.write(config)
    config_file.close()


uwsgi_config = """[uwsgi]
project = {upstream_name}
uid = django
base = /home/%(uid)

chdir = {project_dir}
module = wsgi:application
virtualenv = {env_path}
pythonpath=.
pythonpath = {upstream_name}

master = true
processes = {processes}
callable = app
harakiri = 600

pidfile = {pid_path}
socket = {sock_path}
chmod-socket =  666
vacuum = true
"""


def uwsgi():
    conf_filename = '%s.ini' % upstream_name

    config = uwsgi_config.format(
        upstream_name=upstream_name,
        project_dir=project_dir,
        processes=processes,
        env_path=env_path,
        pid_path=pid_path,
        sock_path=sock_path
    )

    config_file = open(conf_filename, "w")
    config_file.write(config)
    config_file.close()


if __name__ == '__main__':
    nginx()
    supervisor()
    uwsgi()
