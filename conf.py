#!/usr/bin/env python

import os

current_dir = os.path.dirname(os.path.realpath(__file__))
source_root = os.path.join(current_dir, 'source')
template_dir = os.path.join(current_dir, 'temp')
index_dir = os.path.join(current_dir, 'index')

config = {
    'swishbin': '/usr/bin/swish-e',
    'swishconf': os.path.join(template_dir, 'swish-e.conf'),
    'swishdirbase': index_dir,

    'ectagsbin': '/usr/bin/ctags',
    'ectagsconf': '/usr/local/share/lxr/templates/ectags.conf',

    'virtroot': '/lxr',

    'dbhost': 'localhost',
    'dbuser': 'lxr',
    'dbpass': 'lxrpw',
    'dbname': 'lxr',
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
