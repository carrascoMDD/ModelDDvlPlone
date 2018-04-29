
def fi_open(path, mode):
  return file(path, mode)

def fi_read(f):
  return f.read()

def fi_close(f):
  return f.close()

def fi_write(f, string):
  return f.write(string)


