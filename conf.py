#!/usr/bin/env python

import os
from subprocess import Popen, PIPE

current_dir = os.path.dirname(os.path.realpath(__file__))
source_root = os.path.join(current_dir, 'data/source')
template_dir = os.path.join(current_dir, 'temp')
index_dir = os.path.join(current_dir, 'data/index')

config = {
    'swishbin': Popen(["which", "swish-e"], stdout=PIPE).communicate()[0].rstrip(),
    'swishconf': os.path.join(template_dir, 'swish-e.conf'),
    'swishdirbase': index_dir,

    'ectagsbin': Popen(["which", "ctags"], stdout=PIPE).communicate()[0].rstrip(),
    'ectagsconf': '/usr/local/share/lxr/templates/ectags.conf',

    'virtroot': '/lxr',

    'dbhost': 'localhost',
    'dbuser': raw_input('Input DB USER:'),
    'dbpass': raw_input('Input DB PASS:'),
    'dbname': raw_input('Input DB NAME:'),
}

trees = {
    'redispy': {
        'name': 'redispy',
        'desc': 'redis-py',
        'sourceroot': os.path.join(source_root, 'redis-py'),
        'all_versions': ['2.4'],
        'default_version': '2.4',
        'dbname': 'dbi:mysql:dbname=lxr_redispy'
    }
}
