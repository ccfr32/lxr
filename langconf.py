#!/usr/bin/env python

def get_c_syntax():
    syntax = {
        'langid': 7,
        'identdef': '([_a-zA-Z~]|#\s*)\w*',
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
        'langid': 27
        'identdef': '[a-zA-Z]\w+',
        'reserved' : '''and  as  assert break class continue def  del elif else  except exec  False finally for from global if  import in  is lambda None not or pass print raise return self True try while with yield''',
        'spec': [
            {'comment': ['#', '\n']},
            { 'string': [ '"""', '"""', '\\\\.' ] },
            { 'string': [ "'''", "'''", "\\\\." ] },
            {'string': ['"', '"', '\\\\.']},
            {'string': ["'", "'", "\\\\."]},
            {'include': ['\bimport\b', '\n']},
            {'include': ['\bfrom\b', '\n']}],
        
        # Include rules implemented in Python.pm to cope with an
        # endlessly looping case under 'include' patterns.
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

