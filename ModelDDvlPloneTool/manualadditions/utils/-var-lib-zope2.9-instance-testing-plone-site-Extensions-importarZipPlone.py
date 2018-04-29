import zipfile
import os.path

from Products.CMFCore.utils import getToolByName
extensionesTexto = {".txt":"text/plain", ".stx":"text/structured", ".rst":"text/x-rst", ".html":"text/html", ".htm":"text/html"}
extensionesImagenes = (".png", ".jpg", ".jpeg", ".gif")


countFolders = 0

def getObj(folder, id, default = None):
  values = dict(folder.objectItems())
  return values.get(id, default)

def normalizeId(context, title):
  plone_tool = getToolByName(context, 'plone_utils', None)
  if plone_tool != None and getattr(plone_tool, 'normalizeString') != None:
    id =  plone_tool.normalizeString(title)
    return id
  return None

def generateNewId(context, title):

  id = normalizeId(context, title)
  if id == None:
    countFolders += 1
    id = "ifolder-%s"%str(countFolders)
  return id

def createCascadeObject(folderDestino, path, zip):

  currentFolder = folderDestino
  head, tail = os.path.split(path)

  newFolder = None

  for item in head.split(os.path.sep):
    if item != "":
      id = item
      newFolder = getObj(currentFolder, id, None)
      if newFolder == None:
        try:
          id = currentFolder.invokeFactory("I18NFolder", id=id, title=item)
          newFolder = getObj(currentFolder, id, None)
        except:
          id = currentFolder.invokeFactory("I18NFolder", id=generateNewId(currentFolder, item), title=item)
          newFolder = getObj(currentFolder, id, None)

      if newFolder != None:
        if newFolder.Title() != item:
          newFolder.setTitle(item)
          newFolder.reindexObject()
      else:
        raise Exception, 'No se ha podido crear la carpeta "%s", del path "%s"'%(item, path)

      currentFolder = newFolder

  if tail != "":
    id = tail #normalizeId(currentFolder, tail)
    root, ext = os.path.splitext(tail)
    ext = ext.lower()
    if id != None:
      obj = getObj(currentFolder, id, None)
      if obj == None:
        if ext in extensionesTexto.keys():
          id = currentFolder.invokeFactory(
                "Document",
                id=id,
                title=root, #tail, #Hay que elegir en este caso que queremos dejar, nombre del archivo con o sin extension
                text_format=extensionesTexto[ext],
                text=zip.read(path)
              )
        elif ext in extensionesImagenes:
          id = currentFolder.invokeFactory(
                "Image",
                id=id,
                title=tail,
                image=zip.read(path)
              )
        else:
          id = currentFolder.invokeFactory(
                "File",
                id=id,
                title=tail,
                file=zip.read(path)
              )
      else:
        if ext in extensionesTexto.keys():
          obj.setTitle(root) #Hay que elegir en este caso que titulo queremos dejar, nombre del archivo con o sin extension
          obj.text_format = extensionesTexto[ext]
          obj.setText(zip.read(path))
          obj.reindexObject()
        elif ext in extensionesImagenes:
          obj.setTitle(tail)
          obj.setImage(zip.read(path))
          obj.reindexObject()
        else:
          obj.setTitle(tail)
          obj.setFile(zip.read(path))
          obj.reindexObject()
  return

def importarZipPlone(destino=None, erase=False, data=None, context=None):
  if destino != None and data != None and context != None:
    folderDestino = context.restrictedTraverse(destino)

    if erase:
      #borramos todo el contenido del folderDestino
      ids = folderDestino.objectIds()
      folderDestino.manage_delObjects(ids)
      folderDestino.reindexObject()
 
    try:
      zip = zipfile.ZipFile(data, "r")
      namelist = zip.namelist()
      for item in namelist:
        createCascadeObject(folderDestino, item, zip)

    except Exception, e:
      print "Se ha producido un error extrayendo el ZIP: %s, %s"%(repr(e), str(e))
      raise e

  return

