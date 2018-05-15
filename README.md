# generate-config-django-server
Generate config files nginx, supervisor and uwsgi for django project.

Configuration use next structure django project:
```bash
/home/
    ProjectDir/         - Folder for Project and logs
        ProjectDir/     - Base dir Django Project
            ...
            media/
            static/
            manage.py
    env/                - Envirement
        bin/
            activate
            ...
        ...
    logs/               - Folders for all logs
        nginx/
        supervisor/
    file.pid            - Pid file
    file.sock           - Sock file
```


## nginx example .conf

```bash
upstream {upstream_name} {{
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
```

## supervisor example .conf

```bash
[program:{upstream_name}]
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
```

## UWSGI example .ini

```bash
[uwsgi]
project = {upstream_name}
uid = django
base = /home/%(uid)

chdir = {project_dir}
module = wsgi:application
virtualenv = {env_path}
pythonpath=.
pythonpath = {upstream_name}

master = true
processes = 1
callable = app
harakiri = 600

pidfile = {pid_path}
socket = {sock_path}
chmod-socket =  666
vacuum = true
```