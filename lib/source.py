import os

class SourceTree(object):
    
    def __init__(self, tree):
        self.rootpath = tree['sourceroot']

    def getdir(self, pathname, releaseid):
        dirs, files = [], []
        realpath = self.toreal(pathname, releaseid)
        for i in os.listdir(realpath):
            j = self.toreal(
                os.path.join(pathname, i), releaseid)
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
        
    def getsize(self. pathname, releaseid):
        return os.path.getsize(sef.toreal(pathname, releaseid))
    
    def toreal(self, pathname, releaseid):
        return os.path.abspath(os.path.join(
            self.rootpath, releaseid, pathname))
    

if __name__ == "__main__":
    from ..conf import trees
    
    for tree in trees.values():
        st = SourceTree(tree)
        releaseid = tree['variables']['v']['default']
        pathname = '.'
        print st.getdir(pathname, releaseid)
