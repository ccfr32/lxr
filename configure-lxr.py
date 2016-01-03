#!/usr/bin/env python
# coding: utf-8

_usage = '''
The genxref program automatically generates LXR database cross-reference
tokens for a set of URL configuration blocks and source code versions.  These
are both defined in the $lxrconf configuration file.  Each "URL" is a separate
source tree; LXR separates and identifies these by their URL.  Each "version" is
a different version of the source tree being indexed.  See file $lxrconf or
script configure-lxr.pl for configuring URLs and versions.

Valid options are:
  --help             Print a summary of the options.
  --url=URL          Generate tokens for the given URL configuration block.
  --tree=TREE_NAME   To be used in addition to --url in multiple-trees context
                     if LXR configured to identify trees through 'argument'.
  --allurls          Generate tokens for all URL configuration blocks.
  --version=VERSION  Generate tokens for the given version of the code.
  --allversions      Generate tokens for all versions of the code (default).
  --reindexall       Purges existing index data
  --checkonly        Verify tools version and stop
  --accept           Accept parameter suggestions to continue with indexing

Report bugs at http://sourceforge.net/projects/lxr/.
'''

def help():
    print _usage


def main():
    pass


if __name__ == "__main__":
    main()
    
