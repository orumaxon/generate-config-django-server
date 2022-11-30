#! /usr/bin/python
# -*- coding:utf-8 -*-

base_dir = '/home/user/path_to_project'
project_name = 'MyProject'

upstream_name = project_name.lower()
server_name = upstream_name + '.*'

sock_file = 'my_project.sock'
pid_file = 'my_project.pid'
numprocs = 1

env_name = 'env'
user = 'username'
processes = 1
