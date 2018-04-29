os_listdir = context.os_listdir
os_isdir = context.os_isdir
os_isfile = context.os_isfile
os_join = context.os_join
os_normpath = context.os_normpath

timeFormat = "%d-%m-%Y %H:%M" 

def getStrSize(size):
  gb=1024.0**3
  mb=1024.0**2
  kb=1024.0
  if size >= gb:
    return "%.1f GB"%(size/gb)
  if size >= mb:
    return "%.1f MB"%(size/mb)
  if size >= kb:
    return "%.1f KB"%(size/kb)
  return "%.0f By"%size
    
def isdir(f):
  try:
    return os_isdir(f)
  except:
    return 0

def isfile(f):
  try:
    return os_isfile(f)
  except:
    return 0


def ls(url,path):
  path = os_normpath(path)
  s = '''
    <div class="stx"><br>
    <form name="formulario" method="post">
'''
  #s += ' <br> url = %s, <br>path=%s <br>'%(url,path)
  s  += '<p>Direccion: <input type="text" name="path" value="%s" size="50">&nbsp\n' % path
  s += '<input type="submit" value="Ir" ></p>'
  
  try:
    l = os_listdir(path)
    l.sort(cmp=lambda x,y: cmp(x.lower(), y.lower()))
  except:
    s += "<p><b>No se puede navegar al sitio indicado.<b></p>\n"
    #s += "Error, %s, %s" % (str(ex.__class__), str(ex))
    return s
  
  parent = os_join(path,"..")
  
  s += '<table>\n'
  s += '  <tr><th><input class="noborder" type="checkbox" name="select"/></th><th></th><th>Name</th><th>Size</th><th>Modified</th></tr>\n'
  s += '  <tr><td><input class="noborder" type="checkbox" name="select"/></td><td><img src="folder_icon.gif" noborder title="Folder"></td><td nowrap><a href="%s?path=%s">..</a>%s</td><td>&nbsp;</td><td>&nbsp;</td></tr>\n' % (
   url,parent, "&nbsp;"*50
  )
  for f in l:
    pathCompleto =os_join(path,f) 
    try:
      stat = list(context.os_stat(pathCompleto))
      fsize=stat[6]
      ftime = stat[9]
    except:
      fsize = 0
      ftime = 0
    if isdir(pathCompleto):
      s += '  <tr><td><input class="noborder" type="checkbox" name="select"/></td><td><img src="folder_icon.gif" noborder title="Folder"></td><td><a href="%s?path=%s">%s</a></td><td align="right">&nbsp;%s&nbsp;</td><td>&nbsp;%s&nbsp;</td></tr>\n' % (
        url,
        pathCompleto,
        f, 
        getStrSize(fsize), 
        "%s"%(DateTime(ftime).strftime(timeFormat))
      )
    elif isfile(pathCompleto):
      s += '  <tr><td><input class="noborder" type="checkbox" name="select"/></td><td><img src="document_icon.gif" noborder title="Folder"></td><td><a href="%s/download?path=%s">%s</a></td><td align="right">&nbsp;%s&nbsp;</td><td>&nbsp;%s&nbsp;</td></tr>\n' % (
        url,
        pathCompleto,
        f, 
        getStrSize(fsize), 
        "%s"%(DateTime(ftime).strftime(timeFormat))
      )
    else:
      s += '  <tr><td><input class="noborder" type="checkbox" name="select"/></td><td>?</td><td><i>%s</i></td><td align="right" >&nbsp;</td><td>&nbsp;</td></tr>\n' % (
        f 
      )
  s += "</table>\n"
  s += '<p>\n'
  #s += '<a href="%s?path=/">Ir al raiz</a>&nbsp;\n' % (url)
  s += '<input type="button" value="Ir al raiz" onclick="window.location=\'%s?path=/\'">&nbsp;\n' % url
  s += '<input type="button" value="Copiar" disabled>&nbsp;\n'
  s += '<input type="button" value="Cortar" disabled>&nbsp;\n'
  s += '<input type="button" value="Pegar" disabled>&nbsp;\n'
  s += '<input type="button" value="Renombrar" disabled>&nbsp;\n'
  s += '<input type="button" value="Eliminar" disabled>&nbsp;\n'
  s += '</p>\n</form>\n'
  s += '</div>'
  s += '''
  <form name="formulario2" method="post" enctype="multipart/form-data" >
  <input type="hidden" name="path" value="%s">
  <hr>
  <p>Subir fichero:<p>
  <table border="0" >
    <tr>
      <td>Nombre del fichero:</td>
      <td><input name="name" type="text" size="20" value=""></td>
    </tr>
    <tr>
      <td>fichero:&nbsp;</td>
      <td><input name="file" type="file"></td>
    </tr>
    <tr>
      <td colspan="2" align="right" ><input type="submit" value="enviar"></td>
    </tr>
  </table>''' %path

 
  s += '''<br>
  </form>'''

  return s  
 
 
 

form = context.REQUEST.form
if form.get("file",None) != None:
  context.upload(form.get("name",None),form.get("path",None),form.get("file",None))

url=context.REQUEST.getURL()
if url[-len("/script_view"):] == "/script_view":
  url = url[:-len("/script_view")]

print ls(url=url, path=form.get("path","/var/lib/zope2.9/instance/plone-site/Extensions"))
return printed
