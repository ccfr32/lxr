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
    'dbuser': 'lxr',
    'dbpass': 'lxrpw',
    'dbprefix'	: 'lxr_'
}

trees = {
    'redispy': {
        'caption': 'Redispy',
        'shortcaption': 'redispy',
        'treename': 'redispy',
        'sourceroot': os.path.join(source_root, 'redis-py'),
        'sourcerootname': '$v',
        'variables': {
            'v': {
                'name': 'Version',
                'range': ['2.4'],
                'default': '2.4'
            }
        },
        'dbname': 'dbi:mysql:dbname=lxr_redispy'
    }
}
