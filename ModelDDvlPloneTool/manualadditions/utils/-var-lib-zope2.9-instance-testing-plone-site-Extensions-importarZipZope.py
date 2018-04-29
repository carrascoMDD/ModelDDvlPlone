import zipfile
import os.path

from Products.CMFCore.utils import getToolByName
extensionesTexto = {".txt":"text/plain", ".stx":"text/structured", ".rst":"text/x-rst", ".html":"text/html", ".htm":"text/html"}
#extensionesImagenes = (".png", ".jpg", ".jpeg", ".gif")
extensionesImagenes = {".png":"image/png", ".jpg":"image/jpeg", ".jpeg":"image/jpeg", ".gif":"image/gif"}


countFolders = 0

def getObj(folder, id, default = None):
  values = dict(folder.objectItems())
  resultado = values.get(id, default)
  return resultado
      
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
  for item in head.split(os.path.sep):
    if item != "":
      id = item #utilizaremos item como titulo e id como id (por si el id lo modificamos en algun momento)
      newFolder = getObj(currentFolder, id, None)
      if newFolder == None:
        try:
          currentFolder.manage_addFolder(id, item)
        except:
          id = generateNewId(currentFolder, item)
          currentFolder.manage_addFolder(id, item)
        newFolder = getObj(currentFolder, id, None)

      """
      if newFolder.Title() != item:
        print "item = %s, newFolder = %s"%(item, repr(newFolder))
        newFolder.setTitle(item)
        newFolder.reindexObject()
      """

      currentFolder = newFolder
  if tail != "":
    id = tail #normalizeId(currentFolder, tail)
    root, ext = os.path.splitext(tail)
    ext = ext.lower()
    if id != None:
      obj = getObj(currentFolder,id , None)
      if obj == None:
        if ext in extensionesTexto.keys():
          currentFolder.manage_addDocument(id=id, title=root)
          obj = getObj(currentFolder, id, None)
          obj.manage_edit(data=zip.read(path), title=root)
        elif ext in extensionesImagenes.keys():
          obj = currentFolder.manage_addImage(id=id, file=zip.read(path), title=tail, content_type=extensionesImagenes[ext])
        else:
          obj = currentFolder.manage_addFile(id=id, file=zip.read(path), title=tail) #, precondition="", content_type="")
      else: #FIXME: Hay que ver como se accede a las propiedades de los objetos Zope
        if ext in extensionesTexto.keys():
          obj.manage_edit(data=zip.read(path), title=root)
          obj.reindexObject()
        else: #como Image deriva de File, el metodo manage_changeProperties es el mismo y no hacemos distincion
          obj.manage_changeProperties({"title":tail})
          obj.update_data(zip.read(path))
  return

def importarZipZope(destino=None, erase=False, data=None, context=None):
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

