#!/usr/bin/env python

from conf import config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

DBURI = 'mysql+mysqldb://%s:%s@%s:3306/%s?charset=utf8' % (
    config['dbuser'],
    config['dbpass'],
    config['dbhost'],
    config['dbname'])

engine = create_engine(DBURI,
                       encoding="utf8",
                       echo=False,
                       pool_size=5,
                       pool_recycle=10)
MysqlBase = declarative_base()

class Tree(MysqlBase):
    __tablename__ = 'lxr_tree'

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False)
    version = Column(String(32), nullable=False)
    
    
class Definitions(MysqlBase):
    __tablename__ = 'lxr_definitions'

    symid = Column(Integer, nullable=False, primary_key=True)
    fileid = Column(Integer, nullable=False, primary_key=True)
    line = Column(Integer, nullable=False)
    typeid = Column(Integer, nullable=False)
    langid = Column(Integer, nullable=False)
    relid = Column(Integer, nullable=True)
    
    def __init__(self, symid, fileid, line, langid, relid=None):
        self.symid = symid
        self.fileid = fileid
        self.line = line
        self.langid = langid
        self.relid = relid


class LangType(MysqlBase):
    __tablename__ = 'lxr_langtype'

    typeid = Column(Integer, nullable=False, primary_key=True)
    langid = Column(Integer, nullable=False, primary_key=True)
    declaration = Column(Integer, nullable=False, default='')
    
    
class Symbol(MysqlBase):
    __tablename__ = 'lxr_symbol'
    
    symid = Column(Integer, nullable=False, primary_key=True)
    treeid = Column(Integer, nullable=False)
    symname = Column(String(32), nullable=False)
    symcount = Column(Integer, nullable=False, default=1)


class File(MysqlBase):
    __tablename__ = 'lxr_file'

    fileid = Column(Integer, nullable=False, primary_key=True)
    treeid = Column(Integer, nullable=False, primary_key=True)
    filename = Column(String(32), nullable=False)
    

class Usage(MysqlBase):
    __tablename__ = 'lxr_usage'

    symid = Column(Integer, nullable=False, primary_key=True)
    fileid = Column(Integer, nullable=False, primary_key=True)
    line = Column(Integer, nullable=False)

    
    
MysqlBase.metadata.create_all(engine)    
    

    
