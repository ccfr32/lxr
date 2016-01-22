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
    'ectagsopts': ' '.join(['--options=%s' % os.path.join(template_dir, 'ectags.conf'),
                            '--c-types=+plx',
		            '--eiffel-types=+l',
		            '--fortran-types=+L']),

    'virtroot': '/lxr',

    'dbhost': 'localhost',
    #'dbuser': raw_input('Input DB USER:'),
    #'dbpass': raw_input('Input DB PASS:'),
    #'dbname': raw_input('Input DB NAME:'),
    'dbuser': 'admin',
    'dbpass': 'admin',
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
    },
    
    'sqlalchemy': {
        'name': 'sqlalchemy',
        'desc': 'sqlalchemy',
        'sourceroot': os.path.join(source_root, 'sqlalchemy'),
        'all_versions': ['0.9.7'],
        'default_version': '0.9.7',
    },    
}


def get_c_syntax():
    syntax = {
        'langid': 7,
        'identdef': r'([_a-zA-Z~]|#\s*)\w*',
        'reserved' : '''
        auto
        break
        case     char    const    continue
        default  do      double
        else     enum    extern
        float    for
        goto
        if       int     long
        register return
        short    signed  sizeof   static  struct  switch
        typedef
        union    unsigned
        void     volatile
        while
        #include #define #ifdef   #else   #elif
        #ifndef  #endif  #if      #undef  #error
        #pragma  #warning
        defined
        ''',
        'spec':[
            {'comment': ['/\\*', '\\*/']},
            {'comment': ['//', '\n']},
            {'string': ['"', '"', '\\\\.']},
            {'string': ["'", "'", "\\\\."]},
            {'include': ['#\s*include\b', '\n']}
        ],
        'typemap':{
            'c': 'class',
            'd': 'macro (un)definition',
            'e': 'enumerator',
            'f': 'function definition',
            'g': 'enumeration name',
            # , 'i' : 'interface'
            'l': 'local variable',
            'm': 'class, struct, or union member',
            'n': 'namespace',
            'p': 'function prototype or declaration',
            's': 'structure name',
            't': 'typedef',
            'u': 'union name',
            'v': 'variable definition',
            'x': 'extern or forward variable declaration'
        }
    }
    syntax['reserved'] = syntax['reserved'].split()
    return syntax


def get_cpp_syntax():
    syntax = {
        'langid': 8,
        'identdef': '([_a-zA-Z~]|#\s*)[\w]*',
        'reserved' : '''
	and        and_eq     asm       auto
	bitand     bitor      bool      break
	case       catch      char      class
	const      const_cast continue
	default    delete     do        double  dynamic_cast
	else       enum       explicit  export  extern
	false      float      for       friend
	goto
	if         inline     int
	long
	mutable
	namespace  new        not        not_eq
	operator   or         or_eq
	private    protected  public
	register   reinterpret_cast      return
	short      signed     sizeof     static static_cast
	struct     switch
	template   this       throw      true   try
	typedef    typeid     typename
	union      unsigned   using
	virtual    void       volatile
	wchar_t    while
	xor        xor_eq
	#include   #define    #ifdef     #else   #elif
	#ifndef    #endif     #if        #undef  #error
	#pragma    #warning
	defined
	''' ,
        'spec':[
            {'comment': ['/\\*', '\\*/']},
            {'comment': ['//', '\n']},
            {'string': ['"', '"', '\\\\.']},
            {'string': ["'", "'", "\\\\."]},
            {'include'	: ['#\s*include\b', '\n']}],
        'typemap':{
            'c': 'class',
            'd': 'macro (un)definition',
            'e': 'enumerator',
            'f': 'function definition',
            'g': 'enumeration name',
            # , 'i' : 'interface'
            'l': 'local variable',
            'm': 'class, struct, or union member',
            'n': 'namespace',
            'p': 'function prototype or declaration',
            's': 'structure name',
            't': 'typedef',
            'u': 'union name',
            'v': 'variable definition',
            'x': 'extern or forward variable declaration'
        }
    }
    syntax['reserved'] = syntax['reserved'].split()
    return syntax


def get_python_syntax():
    syntax = {
        'langid': 27,
        'identdef': '[a-zA-Z]\w+',
        'reserved' : '''and  as  assert break class continue def  del elif else  except exec  False finally for from global if  import in  is lambda None not or pass print raise return self True try while with yield''',
        'spec': [
            {'open': '#', 'close': '\n', 'type': 'comment'},
            {'open': '"""', 'close': '"""', 'type': 'string'},
            {'open': "'''", 'close': "'''", 'type': 'string'},
            {'open': '"', 'close': '"', 'type': 'string'},
            {'open': "'", 'close': "'", 'type': 'string'},
            {'open': "\\bimport\\b", 'close': '\n', 'type': 'include'},
            {'open': "\\bfrom\\b", 'close': '\n', 'type': 'include'}
        ],
        
        'typemap': {
            'c': 'class',
            'f': 'function',
            'i': 'import',
            'm': 'class member',
            'v': 'variable'
        },
    }
    syntax['reserved'] = syntax['reserved'].split()
    return syntax


syntaxs = {
    'c': get_c_syntax(),
    'cpp': get_cpp_syntax(),
    'python': get_python_syntax()
}
