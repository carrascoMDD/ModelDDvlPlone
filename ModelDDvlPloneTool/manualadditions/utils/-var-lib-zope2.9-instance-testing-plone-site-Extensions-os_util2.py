import os

def os_getcwd():
  return os.getcwd()

def os_chdir(path):
  return os.chdir(path)

def os_isdir(path):
  return os.path.isdir(path)

def os_isfile(path):
  return os.path.isfile(path)

def os_listdir(path):
  return os.listdir(path)

def os_join(a, *p):
  return os.path.join(a, *p)

def os_walk(top, topdown=True, onerror=None):
  l=os.walk(top, topdown, onerror)
  return l

def os_recls(path="."):
  result = list()
  for root, dirs, files in os.walk(path):
    for file in files:
      result.append(os.path.normpath(os.path.join(root, file)))
  return result

def os_normpath(path):
  return os.path.normpath(path)

def os_splitext(path):
  return os.path.splitext(path)

def os_mkdir(path, mode=0777):
  return os.mkdir(path, mode)

def os_rmdir(path):
  return os.rmdir(path)

def os_remove(path):
  return os.remove(path)

def os_removedir(path):
  if path in ("/", ""): #paranoia
    return
  for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        os.remove(os.path.join(root, name))
    for name in dirs:
        os.rmdir(os.path.join(root, name))

def os_split(path):
  return os.path.split(path)

def os_samefile(path1, path2):
  return os.path.samefile(path1, path2)

def os_system(cmd):
  return os.system(cmd)

def os_stat(path):
  return os.stat(path)

