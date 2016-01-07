#!/usr/bin/env python

import MySQLdb

class Index(object):

    def __init__(self, config, tree):
        self.db  = MySQLdb.connect(host=config['dbhost'],
                                   user=config['dbuser'],         
                                   passwd=config['dbpass'],
                                   db=config['dbname'])
        self.db.autocommit()
        self.cur = self.db.cursor()
        
        self.table_prifix = tree['name']

        self.filenum = 0
        
        self.files = {}
        self.symcache = {}
        self.cntcache = {}


        self.allfiles_select = "select f.fileid, f.filename, f.revision, t.relcount" \
                               " from lxr_files f, lxr_status t"\
                               ", lxr_releases r"\
                               ' where r.releaseid = ?'\
                               '  and  f.fileid = r.fileid'\
                               '  and  t.fileid = r.fileid'\
                               ' order by f.filename, f.revision'\

        self.symbols_insert = "insert into lxr_symbols (symname, symid, symcount)"\
                              ' values (?, ?, 0)'

        self.symbols_byname = "select symid, symcount from lxr_symbols"\
                              ' where symname = ?'

        self.symbols_byid = "select symname from lxr_symbols"\
                            ' where symid = ?'

        self.symbols_setref = ("update lxr_symbols"
                               + ' set symcount = ?'
                               + ' where symid = ?'
                               )

        self.related_symbols_select = ('select s.symid, s.symcount, s.symname'
                                       + " from lxr_symbols s, lxr_definitions d"
                                       + ' where d.fileid = ?'
                                       + '  and  s.symid = d.relid')

        self.delete_symbols = ("delete from lxr_symbols"
                               + ' where symcount = 0'
                               )

        self.definitions_insert = ("insert into lxr_definitions"
                                   + ' (symid, fileid, line, langid, typeid, relid)'
                                   + ' values (?, ?, ?, ?, ?, ?)'
                                   )

        self.definitions_select = ('select f.filename, d.line, l.declaration, d.relid'
                                   + " from lxr_symbols s, lxr_definitions d"
                                   + ", lxr_files f, lxr_releases r"
                                   + ", lxr_langtypes l"
                                   + ' where s.symname = ?'
                                   + '  and  r.releaseid = ?'
                                   + '  and  d.fileid = r.fileid'
                                   + '  and  d.symid  = s.symid'
                                   + '  and  d.langid = l.langid'
                                   + '  and  d.typeid = l.typeid'
                                   + '  and  f.fileid = r.fileid'
                                   + ' order by f.filename, d.line, l.declaration'
                                   )

        self.delete_file_definitions = ("delete from lxr_definitions"
                                        + ' where fileid  = ?'
                                        )

        self.delete_definitions = ("delete from lxr_definitions"
                                   + ' where fileid in'
                                   + ' (select r.fileid'
                                   + "  from lxr_releases r, lxr_status t"
                                   + '  where r.releaseid = ?'
                                   + '   and  t.fileid = r.fileid'
                                   + '   and  t.relcount = 1'
                                   + ' )'
                                   )

        self.releases_insert = ("insert into lxr_releases"
                                + ' (fileid, releaseid)'
                                + ' values (?, ?)'
                                )

        self.releases_select = ("select fileid from lxr_releases"
                                + ' where fileid = ?'
                                + ' and  releaseid = ?'
                                )

        self.delete_one_release = ("delete from lxr_releases"
                                   + ' where fileid = ?'
                                   + '  and  releaseid = ?'
                                   )
        self.delete_releases = ("delete from lxr_releases"
                                + ' where releaseid = ?'
                                )

        self.status_select = ("select status from lxr_status"
                              + ' where fileid = ?'
                              )

        self.status_update = ("update lxr_status"
                              + ' set status = ?'
                              + ' where fileid = ?'
                              )
        self.status_timestamp = ("select indextime from lxr_status"
                                 + ' where fileid = ?'
                                 )

        self.status_update_timestamp = ("update lxr_status"
                                        + ' set indextime = ?'
                                        + ' where fileid = ?'
                                        )

        self.delete_unused_status = ("delete from lxr_status"
                                     + ' where relcount = 0'
                                     )

        self.usages_insert = ("insert into lxr_usages"
                              + ' (fileid, line, symid)'
                              + ' values (?, ?, ?)'
                              )

        self.usages_select = ('select f.filename, u.line'
                              + " from lxr_symbols s, lxr_files f"
                              + ", lxr_releases r, lxr_usages u"
                              + ' where s.symname = ?'
                              + '  and  r.releaseid = ?'
                              + '  and  u.symid  = s.symid'
                              + '  and  f.fileid = r.fileid'
                              + '  and  u.fileid = r.fileid'
                              + ' order by f.filename, u.line'
                              )

        self.delete_file_usages = ("delete from lxr_usages"
                                   + ' where fileid  = ?'
                                   )

        self.delete_usages = ("delete from lxr_usages"
                              + ' where fileid in'
                              + ' (select r.fileid'
                              + "  from lxr_releases r, lxr_status t"
                              + '  where r.releaseid = ?'
                              + '   and  t.fileid = r.fileid'
                              + '   and  t.relcount = 1'
                              + ' )'
                              )

        self.langtypes_insert = ("insert into lxr_langtypes"
                                 + ' (typeid, langid, declaration)'
                                 + ' values (?, ?, ?)'
                                 )

        self.langtypes_select = ("select typeid from lxr_langtypes"
                                 + ' where langid = ?'
                                 + ' and declaration = ?'
                                 )

        self.langtypes_count = ("select count(*) from lxr_langtypes"
                                )

        self.purge_all = ("truncate table lxr_definitions"
                          + ", lxr_usages, lxr_langtypes"
                          + ", lxr_symbols, lxr_releases"
                          + ", lxr_status, lxr_files"
                          + ' cascade'
                          )


    def __delete__(self):
        self.cur.close()
        self.db.commit()
        self.db.close()
        

    def status_insert(self, fileid, status):
        sql = '''insert into %s_status 
        (fileid, relcount, indextime, status)
        values (%s, 0, 0, %s)''' % (self.table_prifix, fileid, status)
        
        return self.cur.execute(sql)
        

    def files_insert(self, filename, revision, fileid):
        sql = "insert into %s_files (filename, revision, fileid) values (%s, %s, %s)" % (
            self.table_prifix, filename, revision, fileid)
        return self.cur.execute(sql)
        
 
    def fileidifexists(self, pathname, revision):
        sql = "select fileid from %s_files where filename = '%s' and revision = '%'" % (
            self.table_prifix, pathname, revision)
        self.cur.execute(sql)
        ids = [row[0] for row in self.cur.fetchall()]
        if ids:
            return ids[0]
        return None

    
    def fileid(self, pathname, revision):
        _id = self.fileidifexists(pathname, revision)
        if _id is None:
            self.filenum += 1
            _id = self.filenum
            self.files_insert(pathname, revision, _id)
            self.status_insert(_id, 0)
        return _id
    

    def fileindexed(self, fileid):
        pass

    def setfileindexed(self, fileid):
        pass
    

    def filereferenced(self, fileid):
        pass

    def setfilereferenced(self, fileid):
        pass
    
    def flushcache(self):
        pass
    
