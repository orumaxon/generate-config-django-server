#! /usr/bin/python
# -*- coding:utf-8 -*-

base_dir = '/home/maxes/MyProjects/MaxesBlog'
project_name = 'MaxesBlog'

upstream_name = project_name.lower()
server_name = upstream_name + '.*'

sock_file = 'maxesblog.sock'
pid_file = 'maxesblog.pid'
numprocs = 1

env_name = 'env'
user = 'maxes'
processes = 1
