import os
import string 

class Files(object):
    '''
    `pathname` startswith '/xxxx/xxx.py'
    '''
    
    def __init__(self, tree):
        self.rootpath = tree['sourceroot']
        
    def exists(self, pathname, releaseid):
        return os.path.exists(self.toreal(pathname, releaseid))
    
    def getdir(self, pathname, releaseid):
        dirs, files = [], []
        realpath = self.toreal(pathname, releaseid)
        for i in os.listdir(realpath):
            j = os.path.join(realpath, i)
            if os.path.isdir(j):
                dirs.append(i)
            elif os.path.isfile(j):
                files.append(i)
        return sorted(dirs), sorted(files)

    def getfp(self, pathname, releaseid):
        return open(self.toreal(pathname, releaseid))

    def isdir(self, pathname, releaseid):
        real = self.toreal(pathname, releaseid)
        return os.path.isdir(real)

    def isfile(self, pathname, releaseid):
        real = self.toreal(pathname, releaseid)
        return os.path.isfile(real)
        
    def gettime(self, pathname, releaseid):
        mtime = os.path.getmtime(self.toreal(pathname, releaseid))
        return mtime
    
    def getsize(self, pathname, releaseid):
        return os.path.getsize(self.toreal(pathname, releaseid))

    def gettype(self, pathname, releaseid):
        pathname = pathname.lower()
        idx = pathname.rfind(".")
        if idx > 0:
            ext = pathname[idx+1:]
        else:
            ext = None
        if ext == 'py':
            return 'python'
        elif ext == 'c':
            return 'c'
        elif ext == 'cpp' or ext == 'cc':
            return 'cpp'
        elif ext == 'h':
            return 'cpp'

        if pathname == 'makefile':
            return 'makefile'
        elif pathname == 'readme':
            return 'readme'

        if self.istext(pathname, releaseid):
            return 'text'
        return 'bin'
        

    def parseable(self, pathname, releaseid):
        ftype = self.gettype(pathname, releaseid)
        if ftype == 'python':
            return True
        return False
    
    
    def istext(self, pathname, releaseid):
        filename = self.toreal(pathname, releaseid)
        s = open(filename).read(512)
        text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
        _null_trans = string.maketrans("", "")
        if not s:
            # Empty files are considered text
            return True
        if "\0" in s:
            # Files with null bytes are likely binary
            return False
        # Get the non-text characters (maps a character to itself then
        # use the 'remove' option to get rid of the text characters.)
        t = s.translate(_null_trans, text_characters)
        # If more than 30% non-text characters, then
        # this is considered a binary file
        if float(len(t))/float(len(s)) > 0.30:
            return False
        return True
        
    
    def toreal(self, pathname, releaseid):
        if pathname.startswith("/"):
            pathname = pathname[1:]
        return os.path.abspath(os.path.join(
            self.rootpath, releaseid, pathname))

    
    def filerev(self, pathname, releaseid):
        return "-".join([str(self.getsize(pathname, releaseid)),
                         str(self.gettime(pathname, releaseid))])
    

if __name__ == "__main__":

    from conf import trees
    
    for tree in trees.values():
        st = Files(tree)
        releaseid = tree['default_version']
        pathname = '.'
        print st.getdir(pathname, releaseid)
