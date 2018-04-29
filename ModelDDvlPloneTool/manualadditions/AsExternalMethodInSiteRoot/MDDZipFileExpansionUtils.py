import os
from StringIO import StringIO
from zipfile  import ZipFile

def MDDInformeContenidoZipFile( thePath, theZipFileName,  theRootDir='', theIsWindows=False):

    aDescomprimirReport = [ ]

    if not thePath or len( thePath) < 1 or not theZipFileName or len( theZipFileName) < 1:
        aDescomprimirReport = [ { 'kind': 'ERROR', 'text': 'Can not expand with unknown Path %s or ZipFileName %s' % ( str( thePath), str( theZipFileName) ) ,  }, ]
        return aDescomprimirReport

    unZipFilePath =  os.path.join( thePath, theZipFileName) 
    
    if not os.path.isfile( unZipFilePath):
        aDescomprimirReport = [ { 'kind': 'ERROR', 'text': 'Zip file is Not a file at %s' % unZipFilePath ,  }, ]
        return aDescomprimirReport
      
    unRootPath = thePath
    if theRootDir:
        unRootPath = os.path.join( thePath, theRootDir) 
        unRootFilesystemPath = unRootPath
        if theIsWindows:
            unRootFilesystemPath = unRootFilesystemPath.replace( '/', '\\')
        
        unReportElement = { 
            'kind':                 'CONTENT', 
            'filename':             theRootDir, 
            'filesystem_filename':  theRootDir, 
            'filepath':             unRootFilesystemPath, 
            'filesize':             0, 
            'esDirEnZip':           True , 
            'esDirEnFilesystem':    os.path.isdir( unRootFilesystemPath), 
            'esFileEnFilesystem':   False,
            'esNewDirectory':       not os.path.isdir( unRootFilesystemPath),
            'esNewFile':            False,
        }
       
        aDescomprimirReport.append( unReportElement) 
        

    unZipFile = None
    try:
        unZipFile = ZipFile( unZipFilePath, "r")  
        if not unZipFile:
            aDescomprimirReport = [ { 'kind': 'ERROR', 'text': 'Not a valid ZIP file at %s' % unZipFilePath ,  }, ]
            return aDescomprimirReport
    
        unosZipInfos = unZipFile.infolist()
        if not unosZipInfos or len( unosZipInfos) < 1:
            aDescomprimirReport = [ { 'kind': 'ERROR', 'text': 'No archived content in ZIP file %s' % unZipFilePath,  }, ]
            return aDescomprimirReport
                    
        for unZipInfo in unosZipInfos:
            unContentFilename            =  unZipInfo.filename
            unContentSize                =  unZipInfo.file_size
            unEsDirectoryInZip           =  unContentFilename[ len( unContentFilename) - 1] == "/"
            
            unFilesystemFilename = unContentFilename
            if theIsWindows:
                unFilesystemFilename = unFilesystemFilename.replace( '/', '\\')
            unContentPath = os.path.join( unRootPath, unContentFilename) 
            if theIsWindows:
                unContentPath = unContentPath.replace( '/', '\\')
            unEsDirectoryInFileSystem =  os.path.isdir( unContentPath)
            unEsFileInFileSystem =  os.path.isfile( unContentPath)
            
            unReportElement = { 
                'kind':                 'CONTENT', 
                'filename':             unContentFilename, 
                'filesystem_filename':  unFilesystemFilename, 
                'filepath':             unContentPath, 
                'filesize':             unContentSize, 
                'esDirEnZip':           unEsDirectoryInZip , 
                'esDirEnFilesystem':    unEsDirectoryInFileSystem, 
                'esFileEnFilesystem':   unEsFileInFileSystem,
                'esNewDirectory':       False,
                'esNewFile':            False,
            }
            if unEsDirectoryInZip and not unEsDirectoryInFileSystem and not unEsFileInFileSystem:
                unReportElement['esNewDirectory']= True    
            elif not unEsDirectoryInZip and not unEsDirectoryInFileSystem and not unEsFileInFileSystem:
                unReportElement['esNewFile']= True   
            elif unEsDirectoryInZip and  (not unEsDirectoryInFileSystem or unEsFileInFileSystem):
                unReportElement = { 'kind': 'ERROR', 'text': 'Directory in ZIP file in filesystem %s' % unContentFilename,  }
            elif not unEsDirectoryInZip and (unEsDirectoryInFileSystem or not unEsFileInFileSystem):
                unReportElement = { 'kind': 'ERROR', 'text': 'FILE in ZIP file but Directory in filesystem %s' % unContentFilename,  }       
            
            aDescomprimirReport.append( unReportElement) 
            
    finally:
        if unZipFile:
            unZipFile.close()
    aSortedDescomprimirReport = sorted( aDescomprimirReport, lambda unRE, otroRE: cmp( unRE.get( 'filepath', ''),  otroRE.get('filepath', '') ))
        
    return aSortedDescomprimirReport    
        







def MDDDescomprimirContenidoZipFile( thePath, theZipFileName,  theRootDir='',  theIsWindows=False):

    unContentReport = MDDInformeContenidoZipFile(  thePath, theZipFileName, theRootDir, theIsWindows )
    if not unContentReport or len( unContentReport) < 1:
        aDescomprimirReport = [ { 'kind': 'ERROR', 'text': 'No content report obtained from Path %s and ZipFileName %s' % ( str( thePath), str( theZipFileName) ) ,} , ]
        return aDescomprimirReport
    
    for unZipContentElement in unContentReport:
        if unZipContentElement.has_key('kind') and unZipContentElement[ 'kind'] == 'ERROR':
            aDescomprimirReport = [ { 'kind': 'ERROR', 'text': 'ERRORS reported by Content report obtained from Path %s and ZipFileName %s' % ( str( thePath), str( theZipFileName) ) ,} , ]
            return aDescomprimirReport
        

    unZipFilePath =  os.path.join( thePath, theZipFileName) 
    if not os.path.isfile( unZipFilePath):
        aDescomprimirReport = [ { 'kind': 'ERROR', 'text':  'Not a file at %s' % unZipFilePath ,} , ]
        return aDescomprimirReport

    aDescomprimirReport = [ ]
    unZipFile = None
    try:
        unZipFile = ZipFile( unZipFilePath, "r")  
        if not unZipFile:
            aDescomprimirReport = [ { 'kind': 'ERROR', 'text': 'Not a valid ZIP file at %s' % unZipFilePath ,} , ]
            return aDescomprimirReport
            
        for unReportElement in unContentReport:
            unContentFilename   = unReportElement[ 'filename']
            unFilesystemFilename= [ 'filesystem_filename']
            unContentFilePath   = unReportElement[ 'filepath']
            unEsDirectoryInZip  = unReportElement[ 'esDirEnZip']
            unEsNewDirectory    = unReportElement[ 'esNewDirectory']
            unEsNewFile         = unReportElement[ 'esNewFile']
            
#debug forcing unexisting dirs
#            unDestinationFilename =  'z' + unContentFilename
#            unDestinationFilePath = os.path.join( thePath, unDestinationFilename) 

            unDestinationFilename = unContentFilename
            unDestinationFilePath = unContentFilePath 
            
            if unEsDirectoryInZip:
                if unEsNewDirectory:
                    os.mkdir( unDestinationFilePath, 0777)                
                    aDescomprimirReport.append( unReportElement)
                else:
                    aDescomprimirReport.append( unReportElement)
            else:
                unContentData = unZipFile.read( unContentFilename)
                unReportElement['data'] = unContentData[:64]
                if unEsNewFile:
                    None
                else:
                    None           
                unFile = None
                try:
                    try:
                        unFile = file( unDestinationFilePath, "w")
                        unFile.write( unContentData)  
                    except:          
                        unReportElement[ 'kind'] = "ERROR"
                        unReportElement[ 'text'] = "Error writing file %s" % unDestinationFilePath
                finally:
                    if unFile:
                        unFile.close()
                
                unReadData=None   
                unReadFile = None                    
                try:
                    try:
                        unReadFile = file( unDestinationFilePath, "r")
                        unReadData = unReadFile.read( )            
                    except:
                        unReportElement[ 'kind'] = "ERROR"
                        unReportElement[ 'text'] = "Error reading to verify written file %s" % unDestinationFilePath
                finally:
                    if unReadFile:
                        unReadFile.close()
 
                if not (unReadData == unContentData):
                    unReportElement[ 'kind'] = "ERROR"
                    unReportElement[ 'text'] = "Failed to verify written data: read data different from written data"
                    
                aDescomprimirReport.append( unReportElement)
                        
        
    finally:
        if unZipFile:
            unZipFile.close()
                
    return aDescomprimirReport
