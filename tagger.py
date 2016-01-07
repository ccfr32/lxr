#!/usr/bin/env python

__all__ = ['processfile', 'processrefs']

def processfile(pathname, releaseid, config, files, index):
    revision = files.filerev(pathname, releaseid)
    fileid = index.fileid(pathname, revision)
    index.setfilerelease(fileid, releaseid)

    if not index.fileindexed(fileid):
        lang = Lang(pathname, releaseid)
        ns = lang.indexfile(pathname, path, fileid, index, config)
        index.flushcache()
        index.setfileindexed(fileid)
        
        
def processrefs(pathname, releaseid, config, files, index):
    revision = files.filerev(pathname, releaseid)
    fileid = index.fileid(pathname, revision)
    
    if not index.filereferenced(fileid):
        lang = Lang(pathname, releaseid)
        ns = lang.referencefile(pathname, path, fileid, index, config)
        index.flushcache()
        index.setfilereferenced(fileid)
        

        
