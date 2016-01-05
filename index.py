#!/usr/bin/env python


class Index(object):

    def __init__(self, config):
        self.files = {}
        self.symcache = {}
        self.cntcache = {}

        self.table_prefix = 'lxr_'

        self.files_insert = "insert into ${prefix}files (filename, revision, fileid) values (?, ?, ?)"
        self.files_select = "select fileid from ${prefix}files where filename = ? and revision = ?"
        self.allfiles_select = "select f.fileid, f.filename, f.revision, t.relcount" \
                               " from ${prefix}files f, ${prefix}status t"\
                               ", ${prefix}releases r"\
                               ' where r.releaseid = ?'\
                               '  and  f.fileid = r.fileid'\
                               '  and  t.fileid = r.fileid'\
                               ' order by f.filename, f.revision'\

        self.symbols_insert = "insert into ${prefix}symbols (symname, symid, symcount)"\
                              ' values (?, ?, 0)'

        self.symbols_byname = "select symid, symcount from ${prefix}symbols"\
                              ' where symname = ?'

        self.symbols_byid = "select symname from ${prefix}symbols"\
                            ' where symid = ?'

        self.symbols_setref = ("update ${prefix}symbols"
                               + ' set symcount = ?'
                               + ' where symid = ?'
                               )

        self.related_symbols_select = ('select s.symid, s.symcount, s.symname'
                                       + " from ${prefix}symbols s, ${prefix}definitions d"
                                       + ' where d.fileid = ?'
                                       + '  and  s.symid = d.relid')

        self.delete_symbols = ("delete from ${prefix}symbols"
                               + ' where symcount = 0'
                               )

        self.definitions_insert = ("insert into ${prefix}definitions"
                                   + ' (symid, fileid, line, langid, typeid, relid)'
                                   + ' values (?, ?, ?, ?, ?, ?)'
                                   )

        self.definitions_select = ('select f.filename, d.line, l.declaration, d.relid'
                                   + " from ${prefix}symbols s, ${prefix}definitions d"
                                   + ", ${prefix}files f, ${prefix}releases r"
                                   + ", ${prefix}langtypes l"
                                   + ' where s.symname = ?'
                                   + '  and  r.releaseid = ?'
                                   + '  and  d.fileid = r.fileid'
                                   + '  and  d.symid  = s.symid'
                                   + '  and  d.langid = l.langid'
                                   + '  and  d.typeid = l.typeid'
                                   + '  and  f.fileid = r.fileid'
                                   + ' order by f.filename, d.line, l.declaration'
                                   )

        self.delete_file_definitions = ("delete from ${prefix}definitions"
                                        + ' where fileid  = ?'
                                        )

        self.delete_definitions = ("delete from ${prefix}definitions"
                                   + ' where fileid in'
                                   + ' (select r.fileid'
                                   + "  from ${prefix}releases r, ${prefix}status t"
                                   + '  where r.releaseid = ?'
                                   + '   and  t.fileid = r.fileid'
                                   + '   and  t.relcount = 1'
                                   + ' )'
                                   )

        self.releases_insert = ("insert into ${prefix}releases"
                                + ' (fileid, releaseid)'
                                + ' values (?, ?)'
                                )

        self.releases_select = ("select fileid from ${prefix}releases"
                                + ' where fileid = ?'
                                + ' and  releaseid = ?'
                                )

        self.delete_one_release = ("delete from ${prefix}releases"
                                   + ' where fileid = ?'
                                   + '  and  releaseid = ?'
                                   )
        self.delete_releases = ("delete from ${prefix}releases"
                                + ' where releaseid = ?'
                                )
        self.status_insert = ("insert into ${prefix}status"
                              + ' (fileid, relcount, indextime, status)'
                              + ' values (?, 0, 0, ?)'
                              )

        self.status_select = ("select status from ${prefix}status"
                              + ' where fileid = ?'
                              )

        self.status_update = ("update ${prefix}status"
                              + ' set status = ?'
                              + ' where fileid = ?'
                              )
        self.status_timestamp = ("select indextime from ${prefix}status"
                                 + ' where fileid = ?'
                                 )

        self.status_update_timestamp = ("update ${prefix}status"
                                        + ' set indextime = ?'
                                        + ' where fileid = ?'
                                        )

        self.delete_unused_status = ("delete from ${prefix}status"
                                     + ' where relcount = 0'
                                     )

        self.usages_insert = ("insert into ${prefix}usages"
                              + ' (fileid, line, symid)'
                              + ' values (?, ?, ?)'
                              )

        self.usages_select = ('select f.filename, u.line'
                              + " from ${prefix}symbols s, ${prefix}files f"
                              + ", ${prefix}releases r, ${prefix}usages u"
                              + ' where s.symname = ?'
                              + '  and  r.releaseid = ?'
                              + '  and  u.symid  = s.symid'
                              + '  and  f.fileid = r.fileid'
                              + '  and  u.fileid = r.fileid'
                              + ' order by f.filename, u.line'
                              )

        self.delete_file_usages = ("delete from ${prefix}usages"
                                   + ' where fileid  = ?'
                                   )

        self.delete_usages = ("delete from ${prefix}usages"
                              + ' where fileid in'
                              + ' (select r.fileid'
                              + "  from ${prefix}releases r, ${prefix}status t"
                              + '  where r.releaseid = ?'
                              + '   and  t.fileid = r.fileid'
                              + '   and  t.relcount = 1'
                              + ' )'
                              )

        self.langtypes_insert = ("insert into ${prefix}langtypes"
                                 + ' (typeid, langid, declaration)'
                                 + ' values (?, ?, ?)'
                                 )

        self.langtypes_select = ("select typeid from ${prefix}langtypes"
                                 + ' where langid = ?'
                                 + ' and declaration = ?'
                                 )

        self.langtypes_count = ("select count(*) from ${prefix}langtypes"
                                )

        self.purge_all = ("truncate table ${prefix}definitions"
                          + ", ${prefix}usages, ${prefix}langtypes"
                          + ", ${prefix}symbols, ${prefix}releases"
                          + ", ${prefix}status, ${prefix}files"
                          + ' cascade'
                          )
