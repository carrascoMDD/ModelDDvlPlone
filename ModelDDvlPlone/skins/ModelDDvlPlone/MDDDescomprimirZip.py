def descomprimirReportHTML( thePath, theZipFileName, theReport):
    print """
<h2>Descomprimir Archivo ZIP</h2> 
<h3>Path: %(Path)s</h3>
<h3>ZipFileName: %(ZipFileName)s</h3>
""" % {
    "Path":         thePath,
    "ZipFileName":  theZipFileName,
    }
    
    if not theReport or len( theReport) < 1:
        print """
<p><strong><font color="Red">No report available about the decompression in path %(Path)s of file named %(ZipFileName)s</font></strong></p>
""" % {
    "Path":         thePath,
    "ZipFileName":  theZipFileName,
    }
    
    for unReportElement in theReport:
        print """
<p>%s</p>
""" % str( unReportElement)
         
    return printed     
     
 
 
aPath = "Unknown Path"
aZipFileName = "Unknown ZipFileName"
aDescomprimirReport = [ ]

aForm = context.REQUEST.form
if not aForm.has_key("Path") or not aForm.get("Path",None) or len( aForm.get("Path",None)) < 1:
    aDescomprimirReport.append("Path request parameter is empty. Can not decompress zip file on an unknown path.")
else:
    aPath = aForm.get("Path",None)
    if not aForm.has_key("ZipFileName") or not aForm.get( "ZipFileName", None) or len( aForm.get( "ZipFileName", None)) < 1:
        aDescomprimirReport.append("ZipFileName request parameter is empty. Can not decompress unknown zip file.")
    else:    
        aZipFileName = aForm.get("ZipFileName",None)
        aRootDir = aForm.get("RootDir",None)
        aIsWindows = aForm.get("IsWindows",None)
        aDescomprimirReport = context.InformeContenidoZipFile( aPath, aZipFileName, aRootDir, aIsWindows)
#        aDescomprimirReport = context.DescomprimirContenidoZipFile( aPath, aZipFileName, aRootDir, aIsWindows)

return descomprimirReportHTML( aPath,  aZipFileName, aDescomprimirReport)
