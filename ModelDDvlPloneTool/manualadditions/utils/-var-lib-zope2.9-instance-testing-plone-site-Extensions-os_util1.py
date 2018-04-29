import os

def os_getcwd():
  return os.getcwd()

def os_chdir(path):
  return os.chdir(path)

def os_mkdir(path, mode=0777):
  return os.mkdir(path, mode)

def os_rmdir(path):
  return os.rmdir(path)

def os_remove(path):
  return os.remove(path)


