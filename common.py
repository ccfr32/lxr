
def fileref(desc, css, path, line, *args):

    # Protect against malicious attacks
    path = http_encode(path);
    desc = desc.replace("&", "&amp;")
    desc = desc.replace("<", "&lt;")
    desc = desc.replace(">", "&gt;")
    line = "%04d" % line
    resp = """<a class='css' href="config['virtroot']/source/config['treename'].path.urlargs(args, showattic)#liine>desc<a>"""



def http_encode(path):
    return xxx

def urlargs(*args):
    return xxx
