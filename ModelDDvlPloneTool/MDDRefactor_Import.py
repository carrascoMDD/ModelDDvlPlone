# -*- coding: utf-8 -*-
#
# File: MDDRefactor_Import.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Model Driven Development sl and Antonio Carrasco Valero
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# Authors: 
# Model Driven Development sl  Valencia (Spain) www.ModelDD.org 
# Antonio Carrasco Valero                       carrasco@ModelDD.org
#

__author__ = """Model Driven Development sl <ModelDDvlPlone@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'



import sys
import traceback
import logging


import time


from StringIO  import StringIO
from cStringIO import StringIO   as clsFastStringIO




from AccessControl             import ClassSecurityInfo



from OFS.Image                 import Image
from OFS.Image                 import File


from Products.CMFCore          import permissions

from Products.CMFCore.utils    import getToolByName

from xml.dom.minidom           import Node as clsXMLNode





from PloneElement_TraversalConfig               import cPloneTypes

from ModelDDvlPloneTool_Refactor_Constants      import *
from ModelDDvlPloneTool_ImportExport_Constants  import *


from MDDRefactor           import MDDRefactor, MDDRefactor_Role_SourceInfoMgr, MDDRefactor_Role_SourceMetaInfoMgr, MDDRefactor_Role_TargetInfoMgr, MDDRefactor_Role_TargetMetaInfoMgr, MDDRefactor_Role_TimeSliceMgr, MDDRefactor_Role_TraceabilityMgr, MDDRefactor_Role_MapperInfoMgr, MDDRefactor_Role_MapperMetaInfoMgr, MDDRefactor_Role_Walker   
from MDDRefactor_Paste     import MDDRefactor_Paste_Walker, MDDRefactor_Paste_TargetInfoMgr_MDDElement, MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement, MDDRefactor_Paste_MapperInfoMgr, MDDRefactor_Paste_MapperMetaInfoMgr_ConvertTypes




    
# ######################################################
# IMPORT refactoring
# ######################################################
    


            
class MDDRefactor_Import ( MDDRefactor):
    """Agent to perform a paste refactoring.
    
    """
    def __init__( self, 
        theModelDDvlPloneTool,
        theModelDDvlPloneTool_Retrieval,
        theModelDDvlPloneTool_Mutators,
        theFilesAndData, 
        theXMLDocument,
        theXMLRootElements,
        theTargetRoot, 
        theTargetRootResult, 
        theTargetMDDTypeConfigs, 
        theTargetPloneTypeConfigs, 
        theTargetAllTypeConfigs, 
        theMappingConfigs,
        theExceptionToRaise,
        theAllowPartialCopies,
        theIgnorePartialLinksForMultiplicityOrDifferentOwner,
        theMinimumTimeSlice,
        theYieldTimePercent,
        theReuseIdsForTypes,):
        
        
        unInitialContextParms = {
            'files_and_data':           theFilesAndData,
            'xml_document':             theXMLDocument,
            'xml_root_elements':        theXMLRootElements,
            'target_root':              theTargetRoot,
            'target_root_result':       theTargetRootResult,
            'target_mdd_type_configs':  theTargetMDDTypeConfigs,
            'target_plone_type_configs':theTargetPloneTypeConfigs,
            'target_all_type_configs':  theTargetAllTypeConfigs,
            'mapping_configs':          theMappingConfigs,
            'minimum_time_slice':       theMinimumTimeSlice,
            'yield_time_percent':       theYieldTimePercent,
            'reuse_ids_for_types':      theReuseIdsForTypes,
        }
        
        MDDRefactor.__init__(
            self,
            theModelDDvlPloneTool,
            theModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators,
            unInitialContextParms,
            MDDRefactor_Import_SourceInfoMgr_XMLElements(), 
            MDDRefactor_Import_SourceMetaInfoMgr_XMLElements(), 
            MDDRefactor_Import_TargetInfoMgr_MDDElement(), 
            MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement(), 
            MDDRefactor_Paste_MapperInfoMgr(), 
            MDDRefactor_Paste_MapperMetaInfoMgr_ConvertTypes(), 
            MDDRefactor_Import_TraceabilityMgr(), 
            MDDRefactor_Import_TimeSliceMgr(),
            MDDRefactor_Paste_Walker(), 
            True, # theAllowMappings
            theExceptionToRaise,
            theAllowPartialCopies,
            theIgnorePartialLinksForMultiplicityOrDifferentOwner
        )
    
        


         

class MDDRefactor_Import_SourceInfoMgr_XMLElements( MDDRefactor_Role_SourceInfoMgr):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_SourceInfoMgr.fInitInRefactor( self, theRefactor,):
            return False
        

        
        if not self.vRefactor.fGetContextParam( 'xml_document',):
            return False
        
        if not self.vRefactor.fGetContextParam( 'xml_root_elements',):
            return False

        unTargetRoot = self.vRefactor.fGetContextParam( 'target_root',)
        if ( unTargetRoot == None):
            return False
        
        aPloneUtilsTool = getToolByName( unTargetRoot, 'plone_utils', None)
        if ( aPloneUtilsTool == None):
            return False
        
        aSiteEncoding = aPloneUtilsTool.getSiteEncoding()
        if not aSiteEncoding:
            aSiteEncoding = cMDDEncodingUTF8
        
        self.vRefactor.pSetContextParam( 'site_encoding', aSiteEncoding)
        
        return True
    
        
       

    def fElementIdentificationForErrorMsg( self, theSource):
        
        if theSource == None:
            return str( None)
        
        unTitle = self.fGetTitle( theSource)
        unaId   = self.fGetId(    theSource)
        unPath  = self.fGetPath(  theSource)
        unaUID   = self.fGetUID(   theSource)
        
        unaIdentification = 'Title=%s; id=%s; path=%s UID=%s' % ( str( unTitle), str( unaId), str( unPath), str( unaUID),)

        return unaIdentification
    

        
    def fElementIdentificationForErrorMsg_Unicode( self, theSource):        
      
        unaIdentification = self.fElementIdentificationForErrorMsg( theSource)
        unaIdentificationUnicode = ModelDDvlPloneTool().fAsUnicode( self.vRefactor.fGetContextParam( 'target_root'), unaIdentification)
        
        return unaIdentificationUnicode

    
    
    def fGetSiteEncoding( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        aSiteEncoding = self.vRefactor.fGetContextParam( 'site_encoding',)
        return aSiteEncoding
    
    
    
    
    def fGetSourceRoots( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        unosSourceElements = self.vRefactor.fGetContextParam( 'xml_root_elements',) 
        
        unosPloneTypeNames = cPloneTypes.keys()
        
        unosNonPloneElements = [ ]
        
        for unSourceElement in unosSourceElements:
            unTypeName = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unSourceElement)
            if not ( unTypeName in unosPloneTypeNames):
                unosNonPloneElements.append( unSourceElement)
                
        return unosNonPloneElements

    

    
    
    
    def fIsSourceReadable( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            return False
    
        return True
    
    
    
    
    def fIsSourceOk( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameters
        
        allTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',)
        if not allTypeConfigs:
            return False
        
        unSourceType = theSource.nodeName
        
        if unSourceType.endswith( cMDDXMLRelatedMetaTypePostfix):
            unSourceType = unSourceType[:0 - len( cMDDXMLRelatedMetaTypePostfix)]
            
        if not allTypeConfigs.has_key( unSourceType):
            return False
        
        return True
    
    

     
     
    
    def fFromUnicodeToSystemEncoding( self, theXMLString,):
        
        if not theXMLString:
            return ''
        
        if isinstance( theXMLString, unicode):
            unStringUnicode = theXMLString
            
        else:
            
            unStringUnicode = None
            try:
                unStringUnicode = theXMLString.decode( cMDDEncodingUTF8, errors=cMDDEncodingErrorHandleMode_Strict)
            except UnicodeDecodeError:
                None
        
            if not unStringUnicode:
                return None
 
        unSiteEncoding = self.fGetSiteEncoding()
        if not unSiteEncoding:
            unSiteEncoding = cMDDEncodingUTF8
        
        unStringEncoded  = None
        try:
            unStringEncoded = unStringUnicode.encode( unSiteEncoding, cMDDEncodingErrorHandleMode_Strict)      
        except UnicodeEncodeError:
            None
                
        if not unStringEncoded:
            return None
        
        return unStringEncoded
    
    
    
    
    
    def fGetId( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        
        unaId = theSource.getAttribute( cMDDXMLAttributeName_PloneId)
        if unaId:
            unEncoded = self.fFromUnicodeToSystemEncoding( unaId, )
            return unEncoded
        
        unPath = self.fGetPath( theSource)
        if not unPath:
            return ''
        
        unosPathSteps = unPath.split( '/')
        if not unosPathSteps:
            return ''
        
        unaId = unosPathSteps[-1:][ 0]
        
        unEncoded = self.fFromUnicodeToSystemEncoding( unaId, )
        return unEncoded
        
    
    
    def fGetUID( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        
        unaUID = theSource.getAttribute( cMDDXMLAttributeName_PloneUID)
        unEncoded = self.fFromUnicodeToSystemEncoding( unaUID, )
        return unEncoded    
    
    
    
    def fGetPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        
        unPath = theSource.getAttribute( cMDDXMLAttributeName_PlonePath)
        unEncoded = self.fFromUnicodeToSystemEncoding( unPath, )
        return unEncoded    
     
    
    def fGetTitle( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        
        unTitle = theSource.getAttribute( cMDDXMLAttributeName_PloneTitle)
        unEncoded = self.fFromUnicodeToSystemEncoding( unTitle, )
        return unEncoded    
    
    
    
    
    def fOwnerPath( self, theSource):
        #if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            #return ''        
        return ''
    
    
    
    def fRootPath( self, theSource):
        #if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            #return ''
        
        return ''
    
    
    
    def fGetAttributeValue( self, theSource, theAttributeName, theAttributeType):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return None
    
        if ( not theAttributeName) or ( not theAttributeType):
            return None
        
        if theAttributeName.lower() == 'title':
            return self.fGetTitle( theSource)
        elif theAttributeName.lower() == 'id':
            return self.fGetId( theSource)
        elif theAttributeName.lower() == 'path':
            return self.fGetPath( theSource)
        elif theAttributeName.lower() == 'uid':
            return self.fGetUID( theSource)
            
        unosChildNodes = theSource.childNodes
        if not unosChildNodes:
            return None
        
        for unChildNode in unosChildNodes:
            
            unAttrValue = ''
            
            unNodeName = unChildNode.nodeName
            if unNodeName and not ( unNodeName == cMDDXMLElementName_CommentText):
                                
                if unNodeName == theAttributeName:
                    
                    unosAttrChildNodes = unChildNode.childNodes
                    if unosAttrChildNodes:
                        
                        unPloneContentType = unChildNode.getAttribute( cMDDXMLAttributeName_ContentType)
                        
                        if unPloneContentType.startswith( 'text'):
                                                        
                            for unAttrChildNode in unosAttrChildNodes:
                                
                                if unAttrChildNode.nodeType == clsXMLNode.CDATA_SECTION_NODE:
                                    
                                    unAttrValue = unAttrChildNode.nodeValue
                                    if unAttrValue:
                                        unAttrValue = unAttrValue.strip()
                                    break
                        else:
                        
                            for unAttrChildNode in unosAttrChildNodes:
                                    
                                unChildNodeType = unAttrChildNode.nodeType
                        
                                if unChildNodeType == clsXMLNode.TEXT_NODE:
                                    
                                    unAttrValue = unAttrChildNode.nodeValue
                                    if unAttrValue:
                                        unAttrValue = unAttrValue.strip()
                                    break
                                    
                                elif unChildNodeType == clsXMLNode.CDATA_SECTION_NODE:
                                    
                                    unAttrValue = unAttrChildNode.nodeValue
                                    if unAttrValue:
                                        unAttrValue = unAttrValue.strip()
                                    break
                            
                    if not unAttrValue:
                        return None
                    
                    unAttributeType = theAttributeType.lower()
                    
                    if unAttributeType in [ 'string', 'selection',]:
                        unAttrValue = unAttrValue.replace( '\t',' ')
                        unAttrValue = unAttrValue.replace( '\r',' ')
                        unAttrValue = unAttrValue.replace( '\n',' ')
                        unAttrValue = unAttrValue.strip()
                        unAttrValue = self.fFromUnicodeToSystemEncoding( unAttrValue, )
                    
                    elif unAttributeType in [ 'text', ]:
                        unAttrValue = unAttrValue.replace( '\r\n','\n')
                        unAttrValue = unAttrValue.replace( '\r','\n')
                        unAttrValue = unAttrValue.strip()
                        unAttrValue = self.fFromUnicodeToSystemEncoding( unAttrValue, )
                        
                    
                    elif unAttributeType == 'selection':
                        unAttrValue = self.fFromUnicodeToSystemEncoding( unAttrValue, )
                        
                    
                    
                    elif unAttributeType == 'boolean':
                        if unAttrValue.lower() == str( True).lower():
                            unAttrValue = True
                        else:
                            unAttrValue = False
                        
                    elif unAttributeType in [ 'integer' ]:
                        unNumber = None
                        try:
                            unNumber = int( unAttrValue)                                               
                        except:
                            None
                        if not ( unNumber == None):
                            unAttrValue =  unNumber
                        else:
                            unAttrValue = 0
                        
                    elif unAttributeType in [ 'float', 'fixedpoint', ]:
                        unNumber = None
                        try:
                            unNumber = float( unAttrValue)                                               
                        except:
                            None
                        if not ( unNumber == None):
                            unAttrValue =  unNumber
                        else:
                            unAttrValue = 0.0

                        
                    elif unAttributeType in [ 'datetime', 'date', ]:
                        unDate = None
                        try:
                            unDate = DateTime( unAttrValue)                                               
                        except:
                            None
                        if unDate:
                            unAttrValue =  unDate
                        else:
                            unAttrValue = None

                        
                    elif unAttributeType == 'file':
                        unFilePath = unAttrValue
                        unAttrValue = None
                        if unFilePath:
                            
                            unosFileNamesAndData  = self.vRefactor.fGetContextParam( 'files_and_data')
                            
                            if unosFileNamesAndData and ( unosFileNamesAndData.has_key( unFilePath)):
                                unFileData = unosFileNamesAndData.get( unFilePath, None)

                                if unFileData:
                                    unFileId = unChildNode.getAttribute( cMDDXMLAttributeName_PloneId)
                                    if not unFileId:
                                        unFileId = 'file'
                                    unFileTitle = unChildNode.getAttribute( cMDDXMLAttributeName_PloneTitle)
                                    if not unFileTitle:
                                        unFileTitle= unFileId
                                    unFileContentType = unChildNode.getAttribute( cMDDXMLAttributeName_ContentType)
                                    if unFileContentType:
                                        unaFile = File( unFileId, unFileTitle, clsFastStringIO( unFileData), content_type=unFileContentType)
                                    else:
                                        unaFile = File( unFileId, unFileTitle, clsFastStringIO( unFileData),)
                                        
                                    unAttrValue = unaFile
                                
                    elif unAttributeType == 'image':
                        
                        unFilePath = unAttrValue
                        unAttrValue = None
                        if unFilePath:
                            
                            unosFileNamesAndData  = self.vRefactor.fGetContextParam( 'files_and_data')
                            
                            if unosFileNamesAndData and ( unosFileNamesAndData.has_key( unFilePath)):
                                unImageData = unosFileNamesAndData.get( unFilePath, None)

                                if unImageData:
                                    unImageId = unChildNode.getAttribute( cMDDXMLAttributeName_PloneId)
                                    if not unImageId:
                                        unImageId = 'image'
                                    unImageTitle = unChildNode.getAttribute( cMDDXMLAttributeName_PloneTitle)
                                    if not unImageTitle:
                                        unImageTitle = unImageId
                                    unImageContentType = unChildNode.getAttribute( cMDDXMLAttributeName_ContentType)
                                    if unImageContentType:
                                        unaImage = Image( unImageId, unImageTitle, clsFastStringIO( unImageData), content_type=unImageContentType)
                                    else:
                                        unaImage = Image( unImageId, unImageTitle, clsFastStringIO( unImageData), )
                                        
                                    unAttrValue = unaImage
                                    
                    return unAttrValue
            
        return None
            
    

     
    def fZipFileElementContent( self, theZipFile, theFileName):
  
        if not theZipFile or not theFileName:
            return None
        
        unContent = None
        try:
            unContent = theZipFile.read( theFileName)
        except:
            return None
        return unContent
            
    
    
    
    
    def fGetTraversalValues( self, theSource, theTraversalName, theAcceptedSourceTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource) or ( not theTraversalName):
            return []
        
        unosChildNodes = theSource.childNodes
        if not unosChildNodes:
            return []
        
        someAcceptedSourceTypes = theAcceptedSourceTypes
        
        if someAcceptedSourceTypes and self.vRefactor.vSourceMetaInfoMgr.fHasRelationNamed( theSource, theTraversalName):
            for anAcceptedSourceType in someAcceptedSourceTypes:
                someAcceptedSourceTypes.append( anAcceptedSourceType + cMDDXMLRelatedMetaTypePostfix)
            
        for unChildNode in unosChildNodes:
            unNodeName = unChildNode.nodeName
            if unNodeName and not ( unNodeName == cMDDXMLElementName_CommentText):
                                
                if unNodeName == theTraversalName:
                    
                    unosRetrievedElements = [ ]
                    
                    unosSubChildNodes = unChildNode.childNodes
                    if unosSubChildNodes:
                        
                        for unSubChildNode in unosSubChildNodes:
                            
                            unSubChildNodeName = unSubChildNode.nodeName
                            
                            if not ( unSubChildNodeName == cMDDXMLElementName_CommentText):
                                if unSubChildNode.nodeType == clsXMLNode.ELEMENT_NODE:
                                    if ( not someAcceptedSourceTypes) or ( unSubChildNodeName in someAcceptedSourceTypes):
                                        unosRetrievedElements.append( unSubChildNode)
                            
                    return unosRetrievedElements
            
        return []
        

    
    

    
        
    
class MDDRefactor_Import_SourceMetaInfoMgr_XMLElements( MDDRefactor_Role_SourceMetaInfoMgr):
    """
    
    """
    


    def fTypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unTypeName = theSource.nodeName

        if unTypeName.endswith( cMDDXMLRelatedMetaTypePostfix):
            unTypeName = unTypeName[:0 - len( cMDDXMLRelatedMetaTypePostfix)]
        
        unUnicodeTypeName = self.vRefactor.vSourceInfoMgr.fFromUnicodeToSystemEncoding( unTypeName) 
            
        return unUnicodeTypeName
    
    
    
    
    def fGetArchetypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unArchetypeName = theSource.nodeName
        
        if unArchetypeName.endswith( cMDDXMLRelatedMetaTypePostfix):
            unArchetypeName = unArchetypeName[:0 - len( cMDDXMLRelatedMetaTypePostfix)]
        
        unUnicodeArchetypeName = self.vRefactor.vSourceInfoMgr.fFromUnicodeToSystemEncoding( unArchetypeName) 
            
        return unUnicodeArchetypeName
    
    

    
    def fPloneTypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if ( thePloneElement == None):
            return ''
        
        unTypeName  = thePloneElement.nodeName
        
        unUnicodeTypeName = self.vRefactor.vSourceInfoMgr.fFromUnicodeToSystemEncoding( unTypeName) 
            
        return unUnicodeTypeName
    
    
    
    def fPloneArchetypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if ( thePloneElement == None):
            return ''
        
        unPloneTypeName = self.fPloneTypeName( thePloneElement)
        if not unPloneTypeName:
            return ''
        
        unPloneNames = cPloneTypes.get( unPloneTypeName, {})
        if not unPloneNames:
            return ''
        
        unArchetypeName = unPloneNames.get( 'archetype_name', '')
        return unArchetypeName
    
    
    def fPlonePortalType( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if ( thePloneElement == None):
            return ''
        
        unPloneTypeName = self.fPloneTypeName( thePloneElement)
        if not unPloneTypeName:
            return ''
        
        unPloneNames = cPloneTypes.get( unPloneTypeName, {})
        if not unPloneNames:
            return ''
        
        unPortalType = unPloneNames.get( 'portal_type', '')
        return unPortalType
    
    

        
    
    def fTypeConfig( self, theSource, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theSource:
            return {}
        
        unTypeName = self.fTypeName( theSource)
        if not unTypeName:
            return {}
        
        unTypeConfig = self.fTypeConfigForType( unTypeName, theTypeConfigName)
        return unTypeConfig
    
    
        
    
    def fTypeConfigForType( self, theSourceType, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theSourceType:
            return {}

        unTargetAllTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',) 
        if not unTargetAllTypeConfigs:
            return {}
        
        unasTypeConfigs = unTargetAllTypeConfigs.get( theSourceType, {})
        if not unasTypeConfigs:
            return {}
        
        unTypeConfigName = theTypeConfigName
        if ( not unTypeConfigName) or ( unTypeConfigName == 'Default'):
            unTypeConfigName = sorted( unasTypeConfigs.keys())[ 0]
        
        unaTypeConfig = unasTypeConfigs.get( unTypeConfigName, {})
        if not unaTypeConfig:
            return {}
        
        return unaTypeConfig
    
    
    
    def fAggregationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
        if not theSource:
            return []
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasAggregationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and not ( unAggregationName in unasAggregationNames):
                unasAggregationNames.append( unAggregationName)
                
        return unasAggregationNames
    
    
    
    
    def fHasAggregationNamed( self, theSource, theAggregationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        
        if not theSource or not theAggregationName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theAggregationName):
                return True
                
        return False
    
    
    
    def fHasRelationNamed( self, theSource, theRelationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        
        if not theSource or not theRelationName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theRelationName):
                return True
                
        return False

    
       
    def fHasTraversalNamed( self, theSource, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        
        if not theSource or not theTraversalName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theTraversalName):
                return True
            
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theTraversalName):
                return True
                
        return False

    
     
    
    
    def fRelationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
        if not theSource:
            return []
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasRelationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and not ( unRelationName in unasRelationNames):
                unasRelationNames.append( unRelationName)
                
        return unasRelationNames
    
    
    
    
    def fAttributeTypeInSource( self, theSource, theAttributeName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource or not theAttributeName:
            return ''
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return ''
       
        unosAttributeConfigs = unTypeConfig.get( 'attrs', [])
        if not unosAttributeConfigs:
            return ''
     
        for unAttributeConfig in unosAttributeConfigs:
            
            # ACV 20091110 Changed key.  'attribute_name' appears in  results, not configs
            # Don't know how this was working without it - indeed, because it was ignored, or fallbacks applied.
            # unAttributeName = unAttributeConfig.get( 'attribute_name', '')
            unAttributeName = unAttributeConfig.get( 'name', '')
            if unAttributeName and ( unAttributeName == theAttributeName):
                
                unAttributeType = unAttributeConfig.get( 'type', '')
                return unAttributeType
            
        return ''
                
                
    
    
    

class MDDRefactor_Import_TimeSliceMgr( MDDRefactor_Role_TimeSliceMgr):
    """
    
    """
    
    def __init__( self,):
        
        self.vSleepless             = False
        self.vMinimumTimeSlice      = 0
        self.vYieldTimePercent      = 0
        self.vLastSliceMilliseconds = 0
        
        
        

        
    
    
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_TimeSliceMgr.fInitInRefactor( self, theRefactor,):
            return False
        
        unMinimumTimeSlice = 0
        
        unMinimumTimeSliceStr = self.vRefactor.fGetContextParam( 'minimum_time_slice', None) 
        if unMinimumTimeSliceStr:
            try:
                unMinimumTimeSlice = int( unMinimumTimeSliceStr)
            except:
                None
                
        if unMinimumTimeSlice < cMinimumTimeSlice_Minimum:
            unMinimumTimeSlice = 0
            
        if unMinimumTimeSlice > cMinimumTimeSlice_Maximum:
            unMinimumTimeSlice = cMinimumTimeSlice_Maximum
            
            
            
        unYieldTimePercent = 0
        
        unYieldTimePercentStr = self.vRefactor.fGetContextParam( 'yield_time_percent', None) 
        if unYieldTimePercentStr:
            try:
                unYieldTimePercent = int( unYieldTimePercentStr)
            except:
                None

        unYieldTimePercent = int( unYieldTimePercent) 
        if unYieldTimePercent >= 100:
            unYieldTimePercent = unYieldTimePercent % 100
            
        unYieldTimeFraction = ( unYieldTimePercent * 1.0 ) / 100
        
        if ( not unMinimumTimeSlice) or ( unYieldTimeFraction < 0.01):
            self.vSleepless = True
        else:
            self.vSleepless = False
            
        self.vMinimumTimeSlice = unMinimumTimeSlice
        self.vYieldTimePercent = unYieldTimeFraction
        
        return True
        
    
    
    
    
    
        
    def pTimeSlice( self,):
        if self.vSleepless:
            return self    
        
        unMillisNow = int( time.time() * 1000)
        
        if not self.vLastSliceMilliseconds:
            self.vLastSliceMilliseconds = unMillisNow
            return self
        
        unLapsedSinceLastSlice = unMillisNow - self.vLastSliceMilliseconds
        
        if unLapsedSinceLastSlice < self.vMinimumTimeSlice:
            return self
        
        unSleepMilliseconds = ( self.vYieldTimePercent * unLapsedSinceLastSlice) / ( 1 - self.vYieldTimePercent)
        if unSleepMilliseconds <= cYieldMilliseconds_Minimum:
            return self
        
        unSleepMilliseconds = min( unSleepMilliseconds, cYieldMilliseconds_Maximum)
        
        unSleepSeconds = unSleepMilliseconds / 1000
        
        time.sleep( unSleepSeconds)
        
        unMillisAfter = int( time.time() * 1000)
        
        self.vLastSliceMilliseconds = unMillisAfter
        
        return self
    
    
        
    
    

    
                        
    
class MDDRefactor_Import_TraceabilityMgr( MDDRefactor_Role_TraceabilityMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_TraceabilityMgr.__init__( self)
        

        

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_TraceabilityMgr.fInitInRefactor( self, theRefactor,):
            return False
        
                            
        return True
    
                    

    
    def fEstablishTraceabilityLinks( self, theSource, theTarget):
        return True
    
    

    
            
    
    
           

class MDDRefactor_Import_TargetInfoMgr_MDDElement ( MDDRefactor_Paste_TargetInfoMgr_MDDElement):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Paste_TargetInfoMgr_MDDElement.fInitInRefactor( self, theRefactor,):
            return False

        return True
      
    
    
    def fAuditChanges( self,):
        
        if not MDDRefactor_Paste_TargetInfoMgr_MDDElement.fAuditChanges( self):
            return False
        
        unStack = self.vRefactor.fGetContextParam( 'stack', None)
        if ( unStack == None):
            return False
        
        if unStack.fIsSameElementAsRoot():
            return True
        
        return False

     
        
        
    

    
    def fElementToReuse( self, theTargetElement, theTypeToCreate, theSourceResult):
        """Return First Sub Element of Type and same id as the source
        
        """
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        someTypesToReuseIds = self.vRefactor.fGetContextParam( 'reuse_ids_for_types',)
        if not someTypesToReuseIds:
            return None
        
        if not ( theTypeToCreate in someTypesToReuseIds):
            return None
        
        unSourceId            = self.vRefactor.vSourceInfoMgr.fGetId( theSourceResult)
        
        someTargetSubElements =  theTargetElement.objectValues( theTypeToCreate)
        if not someTargetSubElements:
            return None
        
        for unTargetSubElement in someTargetSubElements:
            
            unTargetSubElementId    = unTargetSubElement.getId()
            
            if unTargetSubElementId == unSourceId:
                return unTargetSubElement        
        
        return None    
    
    
    
    
    
    
    