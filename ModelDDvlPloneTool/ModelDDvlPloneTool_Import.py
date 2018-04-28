# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Import.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

import os

import logging
import traceback

from StringIO import StringIO

from zipfile import ZipFile

from xml.dom.minidom import parseString as gfParseStringAsXMLDocument
from xml.dom.minidom import Document
from xml.dom.minidom import Element
from xml.dom.minidom import Node

from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo


from ModelDDvlPloneTool_ImportExport_Constants import *



class ModelDDvlPloneTool_Import:
    """
    """
    security = ClassSecurityInfo()

    
    
    
 
    security.declarePrivate( 'fNewVoidImportReport')    
    def fNewVoidImportReport( self,):
        unInforme = {
            'success':                  False,
            'status':                   '',
            'condition':                None,
            'exception':                '',
            'elements_exported':        0,
            'filename':                 '',
            'images_exported':          0,
            'files_exported':           0,
        }
        return unInforme
    
    
    
    
      
    security.declarePrivate( 'fNewVoidImportContext')    
    def fNewVoidImportContext( self,):
        unInforme = {
            'object':                   None,
            'report':                   self.fNewVoidImportReport(),
            'import_erros':             [ ],
            'imported_elements_by_uid': { },
            'zip_file':                 None,
            'zip_buffer':               None,
            'xml_document':             None,
            'xml_root':                 [ ],
            'images_imported':          [ ],
            'files_exported':           [ ],
        }
        return unInforme
    
    
    
    
    
    

    security.declarePrivate( 'fImport')
    def fImport( self,
        theTimeProfilingResults     =None,
        theObject                   =None, 
        theUploadedFile             =None,
        theAllImportTypeConfigs     =None, 
        theAdditionalParams         =None):
        """Import theObject and its contents into a zip archive, including attached files and images.
        
        """

             
        unImportContext   = self.fNewVoidImportContext()
        unImportReport    = unImportContext.get( 'report', {})
        unosImportErrors  = unImportContext.get( 'import_errors', {})
        
        
        if not theObject:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_MissingParameter_Element,
            })
            return unImportReport
            
        unImportContext[ 'object'] = theObject

        if not theUploadedFile:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_MissingParameter_UploadedFile,
            })
            return unImportReport
        
        
        if not theAllImportTypeConfigs:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_MissingParameter_ImportTypeConfigs,
            })
            return unImportReport
        
        
        
        # ##############################################################################
        """Retrieve translation_service tool to handle the input encoding.
        
        """
        aTranslationService = getToolByName( theObject, 'translation_service', None)      
        
           
        # ##############################################################################
        """Verify that the uploaded file is a zip archive, or fail.
        
        """      
        unIsZip = False
        unZipFile = None
        try:
            unZipFile = ZipFile( theUploadedFile)  
        except:
            None
        if unZipFile:
            # Error if True
            if not( unZipFile.testzip()):
                unIsZip = True
       
        if not unIsZip:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_Parameter_UploadedFile_NotAZip,
            })
            return unImportReport
        
        
        # ##############################################################################
        """Find the first .xml file in the zip archive, or fail.
        
        """      
        unXMLPostfix = '.%s' % cXMLFilePostfix.lower()
        anXMLFullFileName = ''                
        anXMLBaseName = ''                
        someFileNames = unZipFile.namelist()
        for aFullFileName in someFileNames:
                    
            aBaseName = os.path.basename( aFullFileName)
            if aBaseName:
                aBaseNameLower = aBaseName.lower()
                aBaseNamePostfix = os.path.splitext(  aBaseNameLower)[ 1]
                if aBaseNamePostfix == unXMLPostfix:
                    anXMLFullFileName = aFullFileName
                    anXMLBaseName     = aBaseName
                    break
                
        if not anXMLFullFileName:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_Parameter_UploadedFile_ZipWithoutXMLFile,
            })
            return unImportReport
        
        # ##############################################################################
        """Read contents of first .xml file in the zip archive, or fail.
        
        """      
        unXMLBuffer = self.fZipFileElementContent( unZipFile, anXMLFullFileName)
        if len( unXMLBuffer) < 1:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_EmptyXMLFile,
                'filename':     anXMLFullFileName,
            })
            return unImportReport
        
        
        # ##############################################################################
        """Decode the contents of .xml file into unicode, or fail.
        
        """      
        unUnicodeXMLBuffer = u''
        try:
            unUnicodeXMLBuffer = unXMLBuffer.decode( cXMLEncodingUTF8)
        except UnicodeDecodeError:
            None
            
        if len( unUnicodeXMLBuffer) < 1:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_DecodingXMLFileContents,
                'filename':     anXMLFullFileName,
            })
            return unImportReport
            
        
        # ##############################################################################
        """Parse unicode contents of .xml file as an XML DOM tree, or fail.
        
        """      
        unXMLDocument = None
        try:
            unXMLDocument = gfParseStringAsXMLDocument( unXMLBuffer)
        except:
            None
            
        if not unXMLDocument:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_BadXMLFile,
                'filename':     anXMLFullFileName,
            })
            return unImportReport
        
        unosRootElements = unXMLDocument.childNodes
        if not unosRootElements:
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_NoRootXMLElements,
                'filename':     anXMLFullFileName,
            })
            return unImportReport
        
            
         
        # ##############################################################################
        """Traverse parsed XML DOM tree and create or update application elements from XML node data.
        
        """      
        unImportResult = True
        
        for unRootElement in unosRootElements:
            unThisImportResult = self.fImport_Recursive( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theObject                   =theObject, 
                theZipFile                  =unZipFile,
                theXMLDocument              =unXMLDocument,
                theXMLElement               =unRootElement,
                theAllImportTypeConfigs     =theAllImportTypeConfigs, 
                theImportContext            =unImportContext,
                theTranslationService       =aTranslationService,
                theImportErrors             =unosImportErrors,
                theAdditionalParams         =theAdditionalParams)
            unImportResult = unImportResult and unThisImportResult
        
        
        
        
        #unImportImagesAndFilesResult = self.fImportImagesAndFiles( 
            #theTimeProfilingResults     =theTimeProfilingResults,
            #theObject                   =theObject, 
            #theAllImportTypeConfigs     =theAllImportTypeConfigs, 
            #theImportContext            =unImportContext,
            #theTranslationService       =aTranslationService,
            #theOutputEncoding           =theOutputEncoding,
            #theEncodedNamesCache        =anEncodedNamesCache,
            #theImportErrors             =unImportErrors,
            #theAdditionalParams         =theAdditionalParams)

        
        
        
        
        unImportReport.update( { 
             'success':      True,
        })
        
        return unImportReport
        

           
    
    
    security.declarePrivate( 'fZipFileElementContent')    
    def fZipFileElementContent( self, theZipFile, theFileName):
  
        if not theZipFile or not theFileName:
            return None
        
        unContent = None
        try:
            unContent = theZipFile.read( theFileName)
        except:
            return None
        return unContent
    
    
    

    security.declarePrivate( 'fImportImagesAndFiles')
    def fImportImagesAndFiles( self,
        theTimeProfilingResults     =None,
        theObject                   =None, 
        theAllImportTypeConfigs     =None, 
        theImportContext            =None,
        theTranslationService       =None,
        theOutputEncoding           =None,
        theEncodedNamesCache        =None,
        theImportErrors             =None,
        theAdditionalParams         =None):
        """Import the files and images found to be exported in the object traversal and export phase.
        
        """

        if ( not theObject) or ( not theImportContext) or ( not theTranslationService) or ( theImportErrors == None):
            theImportErrors.append( { 
                'success':      False,
                'status':       cImportStatus_Error_Internal_MissingParameters,
            })
            return False

        unZipFile = theImportContext.get( 'zip_file', None)
        if not unZipFile:
            theImportErrors.append( { 
                'success':      False,
                'status':       cImportStatus_Error_Internal_MissingZipFile,
            })
            return False        
        
        someImagesToImport = theImportContext.get( 'images_to_export', [])
        for anImageToImport in someImagesToImport:
            anImageFullFileName = anImageToImport[ 0]
            anImageAsFile       = anImageToImport[ 1]
            
            if anImageFullFileName and anImageAsFile:
                unZipFile.writestr( anImageFullFileName, anImageAsFile.getvalue())
                
        someFilesToImport = theImportContext.get( 'files_to_export', [])
        for anFileToImport in someFilesToImport:
            anFileFullFileName = anFileToImport[ 0]
            anFileAsFile       = anFileToImport[ 1]
            
            if anFileFullFileName and anFileAsFile:
                aWholeData = ''
                aFileDataObject = anFileAsFile.data
                while aFileDataObject:
                    aFileData = aFileDataObject.data
                    if aFileData:
                        aWholeData = aWholeData + aFileData
                        aFileDataObject = aFileDataObject.next
                    else:
                        aFileDataObject = None
                
                unZipFile.writestr( anFileFullFileName, aWholeData)
        
        return True
    
    
   

    security.declarePrivate( 'fImport_Recursive')
    def fImport_Recursive( self,
        theTimeProfilingResults     =None,
        theObject                   =None, 
        theZipFile                  =None,
        theXMLDocument              =None,
        theXMLElement               =None,
        theAllImportTypeConfigs     =None, 
        theImportContext            =None,
        theTranslationService       =None,
        theImportErrors             =None,
        theAdditionalParams         =None):
        """Import theObject and its contents into a zip archive, with references to files and images to be attached.
        
        """

        if ( not theObject) or ( not theZipFile) or ( not theXMLDocument) or ( not theXMLElement) or ( not theAllImportTypeConfigs) or ( not theImportContext) or ( not theTranslationService) or ( theImportErrors == None):
            theImportErrors.append( { 
                'success':      False,
                'status':       cImportStatus_Error_Internal_MissingParameters,
            })
            return False
        
        unImportReport  = theImportContext.get( 'report', {})
        
        unElementMetaType = theObject.meta_type
        
        unTypeConfig = theAllImportTypeConfigs.get( unElementMetaType, {})
        if not unTypeConfig:
            """Ignore object and do not import it, allowing the caller to continue with other objects, if any.
            
            """
            return True

        # ##############################################################################
        """Retrieve imported element type fromd node name.
        
        """
        anImportedTypeName = theXMLElement.nodeName
        

        # ##############################################################################
        """Retrieve identifying attributes from element to import.
        
        """
        anImportedTitle = theXMLElement.getAttribute( cXMLAttributeName_PloneTitle, '')
        anImportedUID   = theXMLElement.getAttribute( cXMLAttributeName_PloneUID,   '')
        anImportedPath  = theXMLElement.getAttribute( cXMLAttributeName_PlonePath,  '')
        
        if unElementMetaType == anImportedTypeName:
            None
        
        # ##############################################################################
        """Add new element to parent, or as root if no current parent, adding the new element to the stack.
        
        """
        if not unXMLStack:
            unXMLDocument.appendChild( unNewElement)
            theImportContext[ 'xml_root'] = unNewElement
        else:
            unParentElement = unXMLStack[ -1 ]
            if unParentElement:
                unParentElement.appendChild( unNewElement)
                
        unXMLStack.append( unNewElement)
                
        
        try:
            
            # ##############################################################################
            """Retrieve the element's schema.
            
            """
            unObjectSchema = theObject.schema
            if not unObjectSchema:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_Internal_ObjectHasNoSchema,
                })
                return False
            
            
            # ##############################################################################
            """Iterate and export each configured attribute.
            
            """
            unosAttrConfigs = unTypeConfig.get( 'attrs', [])
            for unAttrConfig in unosAttrConfigs:
                unAttrName = unAttrConfig.get( 'name', '')
                if unAttrName:
                    
                    aTextContentType = ''
                    
                    unAttrNameEncoded = theEncodedNamesCache.get( unAttrName, None)
                    if not unAttrNameEncoded:
                        theImportErrors.append( { 
                            'status':       cImportStatus_Error_Internal_EncodedNameMissing_AttrName,
                            'meta_type':    unElementMetaType,
                        })
                    else:     
                        unAttrAccessorName = unAttrConfig.get( 'accessor', '')     
                        if unAttrAccessorName:
                            unAccessor = None
                            try:
                                unAccessor = theObject[ unAttrAccessorName]    
                            except:
                                None
                            if not unAccessor:
                                theImportErrors.append( { 
                                    'status':       cImportStatus_Error_Internal_AttributeAccessorNotFound,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'accessor':     unAccessor,
                                    'path':         '/'.join( theObject.getPhysicalPath()),
                                })
                            else:
                                unObjectAttributeFieldType = unAttrConfig.get( 'type', '').lower()
                                try:
                                    unRawValue = unAccessor()
                                except:
                                    unaExceptionInfo = sys.exc_info()
                                    unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                                    unInformeExcepcion = 'Exception during fImport_Recursive during invocation of element explicit accessor for attribute\n' 
                                    unInformeExcepcion += 'meta_type=%s path=%s attribute=%s accessor=%s\n' % ( unElementMetaType, '/'.join( theObject.getPhysicalPath()), unAttrName, unAccessor,)
                                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                                    unInformeExcepcion += unaExceptionFormattedTraceback   
                                    
                                    theImportErrors.append( { 
                                        'status':       cImportStatus_Error_Internal_AttributeValueAccessException,
                                        'meta_type':    unElementMetaType,
                                        'attr':         unAttrName,
                                        'path':         '/'.join( theObject.getPhysicalPath()),
                                        'exception':    unInformeExcepcion,
                                    })
                                    aLogger = logging.getLogger( 'ModelDDvlPloneTool_Import::fImport_Recursive')
                                    aLogger.info( unInformeExcepcion) 
                                
                        unAttributeName = unAttrConfig.get( 'attribute', '')     
                        if unAttributeName:
                            unObjectAttributeFieldType = unAttrConfig.get( 'type', '').lower()
                            if unAttrAccessorName and unRawValue:
                                unAttributeOwner = unRawValue
                            else:
                                unAttributeOwner = theObject
                                
                            try:
                                unRawValue = unAttributeOwner.__getattribute__( unAttributeName)
                                if unRawValue.__class__.__name__ == "ComputedAttribute":
                                    unComputedAttribute = unRawValue
                                    unRawValue = unComputedAttribute.__get__( theObject)
                            except:
                                unaExceptionInfo = sys.exc_info()
                                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                                unInformeExcepcion = 'Exception during fImport_Recursive during access to element getattribute\n' 
                                unInformeExcepcion += 'meta_type=%s path=%s attribute=%s attributeName=%s\n' % ( unElementMetaType, '/'.join( theObject.getPhysicalPath()), unAttrName, unAttributeName)
                                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                                unInformeExcepcion += unaExceptionFormattedTraceback   
                                
                                theImportErrors.append( { 
                                    'status':       cImportStatus_Error_Internal_AttributeValueAccessException,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'path':         '/'.join( theObject.getPhysicalPath()),
                                    'exception':    unInformeExcepcion,
                                })
                                aLogger = logging.getLogger( 'ModelDDvlPloneTool_Import::fImport_Recursive')
                                aLogger.info( unInformeExcepcion) 
                                
                        elif not unAttrAccessorName:
                            if not unObjectSchema.has_key( unAttrName):
                                continue
                            
                            unObjectAttributeField          = unObjectSchema[ unAttrName]
    
                            unRawValue = None
                            try:
                                unRawValue = unObjectAttributeField.getRaw( theObject)
                            except:
                                unaExceptionInfo = sys.exc_info()
                                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                                unInformeExcepcion = 'Exception during fImport_Recursive accessing element attribute\n' 
                                unInformeExcepcion += 'meta_type=%s path=%s attribute=%s\n' % ( unElementMetaType, '/'.join( theObject.getPhysicalPath()), unAttrName,)
                                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                                unInformeExcepcion += unaExceptionFormattedTraceback   
                                
                                theImportErrors.append( { 
                                    'status':       cImportStatus_Error_Internal_AttributeValueAccessException,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'path':         '/'.join( theObject.getPhysicalPath()),
                                    'exception':    unInformeExcepcion,
                                })
                                aLogger = logging.getLogger( 'ModelDDvlPloneTool_Import::fImport_Recursive')
                                aLogger.info( unInformeExcepcion) 
                    
                            unObjectAttributeFieldType      = unObjectAttributeField.type.lower()
                            if unObjectAttributeFieldType == 'computed':
                                unObjectAttributeFieldType = unAttrConfig.get( 'type', '').lower() 
                                
                            unWidget = unObjectAttributeField.widget
                            if unWidget and (unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget') and unObjectAttributeField.__dict__.has_key('vocabulary'):
                                unObjectAttributeFieldType = 'selection'
                            
                        unValueStringEncoded = ''
                        unCreateCDATA = False
                        
                        if unObjectAttributeFieldType in [ 'string', 'text', 'selection',]:  
                            if unObjectAttributeFieldType in [ 'text',]:  
                                if unAttrName == "description":
                                    unCreateCDATA = False
                                else:
                                    unCreateCDATA = True                                    
                                
                                    if unObjectAttributeField:
                                        aTextContentType = unObjectAttributeField.getContentType( theObject)
                                 
                            unValueStringEncoded = ''
                            if unRawValue:
                                unValueStringEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unRawValue, theTranslationService, theOutputEncoding)
                                if ( not unEncodingOk)  or not unValueStringEncoded:
                                    theEncodingErrors.append( { 
                                        'status':       cImportStatus_Error_Internal_EncodingError_AttributeValue_String,
                                        'meta_type':    unElementMetaType,
                                        'attr':         unAttrName,
                                        'value':        repr( unRawValue),
                                    })
                                
                        elif unObjectAttributeFieldType in [ 'boolean', 'integer', 'float','fixedpoint',]:  
                            unValueString = str( unRawValue)
                            unValueStringEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unValueString, theTranslationService, theOutputEncoding)
                            if not unEncodingOk:
                                unValueStringEncoded = ''
                                
                        elif unObjectAttributeFieldType == 'image':
                            unaImage = unRawValue
                            #unaImage = theObject.getImage()
                            if unaImage:                                
                                unaImageAsFile = unaImage.getImageAsFile()
                                unFilename = unaImage.filename
                            else:
                                unaImageAsFile = StringIO()
                                unFilename = theObject.getFilename()
                            if not unFilename:
                                unFilename = theObject.getId()
                            unImageFullFileName = '/'.join( theObject.getPhysicalPath() + ( unFilename, ))
                                
                            unValueStringEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unImageFullFileName, theTranslationService, theOutputEncoding)
                            if ( not unEncodingOk)  or not unValueStringEncoded:
                                theEncodingErrors.append( { 
                                    'status':       cImportStatus_Error_Internal_EncodingError_AttributeValue_String,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'value':        repr( unImageFullFileName),
                                })
                                unValueStringEncoded = ''
                            
                            theImportContext[ 'images_to_export'].append( [ unImageFullFileName, unaImageAsFile,])
                            
                            
                        elif unObjectAttributeFieldType == 'file':
                            unFileAsFile = unRawValue
                            unFileFullFileName = '/'.join( theObject.getPhysicalPath() + ( theObject.getFilename(), ))

                            unValueStringEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unFileFullFileName, theTranslationService, theOutputEncoding)
                            if ( not unEncodingOk)  or not unValueStringEncoded:
                                theEncodingErrors.append( { 
                                    'status':       cImportStatus_Error_Internal_EncodingError_AttributeValue_String,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'value':        repr( unFileFullFileName),
                                })
                                unValueStringEncoded = ''
                            
                            theImportContext[ 'files_to_export'].append( [ unFileFullFileName, unFileAsFile,])
                            
                            

                    unNewAttributeElement    = unXMLDocument.createElement( unAttrNameEncoded)
                    unNewElement.appendChild( unNewAttributeElement)

                    if unValueStringEncoded:
                        
                        if aTextContentType:
                            unNewAttributeElement.setAttribute( cXMLAttributeName_ContentType, aTextContentType)                        

                        unNewAttributeElementData = None
                        if unCreateCDATA:
                            unValueStringEncoded = unValueStringEncoded.replace( ']]>', '')
                            unNewAttributeElementData   = unXMLDocument.createCDATASection( unValueStringEncoded)
                        else:
                            unValueStringEncoded = unValueStringEncoded.replace( '<![CDATA[', '')                                                        
                            unNewAttributeElementData   = unXMLDocument.createTextNode( unValueStringEncoded)
                            
                        unNewAttributeElement.appendChild( unNewAttributeElementData)
        
                        
                        
                        
            # ##############################################################################
            """Iterate and export each configured aggregation or relationship.
            
            """
            unosTraversalConfigs = unTypeConfig.get( 'traversals', [])
            for unTraversalConfig in unosTraversalConfigs:
                unAggregationName = unTraversalConfig.get( 'aggregation_name', '')
                if unAggregationName:
                    # ##############################################################################
                    """Iterate and export recursively each aggregated element from theObject contained objects, which are of one of the configured types.
                    
                    """
                    
                    if unObjectSchema.has_key( unAggregationName):
                                    
                        # ##############################################################################
                        """Determine types of subitems to export.
                        
                        """
                        someAcceptedPortalTypes = set( )
                        
                        someSubItemsConfigs   = unTraversalConfig.get( 'subitems', [])
                        for aSubItemsConfig in someSubItemsConfigs:
                            somePortalTypes = aSubItemsConfig.get( 'portal_types', [])
                            
                            someAcceptedPortalTypes.update( somePortalTypes)
                         
                            
                            
                        # ##############################################################################
                        """Retrieve contained objects of the specified types.
                        
                        """
                        someSubItems = theObject.objectValues( somePortalTypes)
                        
                        
                        
                         
                        if someSubItems:
                            # ##############################################################################
                            """Sort Retrieved contained objects by Id.
                            
                            """
                            someIdsAndSubItems = [ [ aSubItem.getId(), aSubItem, ] for aSubItem in someSubItems]
                            someSortedIdsAndSubItems = sorted( someIdsAndSubItems, lambda unSI, otroSI: cmp( unSI[ 0], otroSI[ 0]))
                        
                            # ##############################################################################
                            """Recursively export retrieved sorted subitems, creating a DOM element for the aggregation, and adding the new element to the stack.
                            
                            """
                            unNewAggregationElement  = unXMLDocument.createElement( unAggregationName)
                            unNewElement.appendChild( unNewAggregationElement)
                            try:
                                unXMLStack.append( unNewAggregationElement)
        
                                for unaIdAndSubItem in someSortedIdsAndSubItems:
                                    unSubItemId = unaIdAndSubItem[ 0]
                                    unSubItem   = unaIdAndSubItem[ 1]
                                    
                                    unSubItemImportResult = self.fImport_Recursive( 
                                        theTimeProfilingResults     =theTimeProfilingResults,
                                        theObject                   =unSubItem, 
                                        theAllImportTypeConfigs     =theAllImportTypeConfigs, 
                                        theImportContext            =theImportContext,
                                        theTranslationService       =theTranslationService,
                                        theOutputEncoding           =theOutputEncoding,
                                        theEncodedNamesCache        =theEncodedNamesCache,
                                        theImportErrors             =theImportErrors,
                                        theAdditionalParams         =theAdditionalParams)
                            finally:   
                                unXMLStack.pop()
                    
                else:
                    unRelationName = unTraversalConfig.get( 'relation_name', '')
                    if unRelationName:
                        # ##############################################################################
                        """Iterate and export a reference to each related element, which are of one of the configured types.
                        
                        """
                        if unObjectSchema.has_key( unRelationName):
                        
                            # ##############################################################################
                            """Determine types of subitems to export.
                            
                            """
                            someAcceptedPortalTypes = set( )
                            
                            someRelatedTypesConfigs   = unTraversalConfig.get( 'related_types', [])
                            for aRelatedItemsConfig in someRelatedTypesConfigs:
                                somePortalTypes = aRelatedItemsConfig.get( 'portal_types', [])
                                
                                someAcceptedPortalTypes.update( somePortalTypes)
                        
                    
                            # ##############################################################################
                            """Retrieve related objects.
                            
                            """
                            unRelationObjectField = unObjectSchema.get( unRelationName, None)
                            if unRelationObjectField:
                                unRelationObjectFieldAccessor = unRelationObjectField.getAccessor( theObject)
                            someRelatedItems = []
                            try:
                                someRelatedItems = unRelationObjectFieldAccessor()
                            except:
                                None
                            
                            if someRelatedItems and not ( someRelatedItems.__class__.__name__ in [ 'list', 'tuple', 'set',]):
                                someRelatedItems = [ someRelatedItems,]
                                
                            
                            # ##############################################################################
                            """Filter retrieved related objects of the specified types.
                            
                            """
                            someRelatedItemsOfRightType = [ ]
                            if someRelatedItems:
                                for aRelatedItem in someRelatedItems:
                                    aRelatedItemMetaType = aRelatedItem.meta_type
                                    if aRelatedItemMetaType in someAcceptedPortalTypes:
                                        someRelatedItemsOfRightType.append( aRelatedItem)
                                    
                                
                            if someRelatedItemsOfRightType:
                                # ##############################################################################
                                """Sort Retrieved related objects by Id.
                                
                                """
                                someIdsAndRelatedItems = [ [ aRelatedItem.getId(), aRelatedItem, ] for aRelatedItem in someRelatedItemsOfRightType]
                                someSortedIdsAndRelatedItems = sorted( someIdsAndRelatedItems, lambda unRI, otroRI: cmp( unRI[ 0], otroRI[ 0]))
                                
                                
                                
                                # ##############################################################################
                                """Import  sorted references to related items.
                                
                                """
                                unNewRelationElement  = unXMLDocument.createElement( unRelationName)
                                unNewElement.appendChild( unNewRelationElement)
                                try:
                                    unXMLStack.append( unNewRelationElement)
                                    
                                    
                                    for unaIdAndRelatedItem in someSortedIdsAndRelatedItems:
                                        unRelatedItemId = unaIdAndRelatedItem[ 0]
                                        unRelatedItem   = unaIdAndRelatedItem[ 1]
                                        
                                        unRelatedMetaType = unRelatedItem.meta_type
                                        
            
                                        # ##############################################################################
                                        """Get related element metatype name from cache in output encoding, or using translation service.
                                        
                                        """
                                        unRelatedMetaTypeEncoded = theEncodedNamesCache.get( unRelatedMetaType, None)
                                        if not unRelatedMetaTypeEncoded:
                                            unRelatedMetaTypeEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unRelatedMetaType, theTranslationService, theOutputEncoding)
                                            if ( not unEncodingOk)  or not unRelatedMetaTypeEncoded:
                                                theEncodingErrors.append( { 
                                                    'status':       cImportStatus_Error_Internal_EncodedNameMissing_ElementMetaTypeName,
                                                    'meta_type':     unRelatedMetaType   
                                                })                                            
                                                unRelatedMetaTypeEncoded = ''
                                            else:
                                                theEncodedNamesCache[ unRelatedMetaType] = unRelatedMetaTypeEncoded    
                                            
                                                
                                                
                                        if unRelatedMetaTypeEncoded:
               
                                            # ##############################################################################
                                            """Create new element to in the document and set identifying attributes to serve as reference to the related object .
                                            
                                            """
                                            unNewRelatedElementReference = unXMLDocument.createElement( unRelatedMetaTypeEncoded)
                                            
                                            unNewRelatedElementReference.setAttribute( cXMLAttributeName_PloneTitle,    unRelatedItem.Title())
                                            unNewRelatedElementReference.setAttribute( cXMLAttributeName_PloneUID,      unRelatedItem.UID())
                                            unNewRelatedElementReference.setAttribute( cXMLAttributeName_PlonePath,     '/'.join( unRelatedItem.getPhysicalPath()))
            
                                            unNewRelationElement.appendChild( unNewRelatedElementReference)
                    
                                finally:   
                                    unXMLStack.pop()
                    
        finally:   
            unXMLStack.pop()
              
                     
        return True
    
    
    
        
        
        
    
    
    
    
    
    


    security.declarePrivate( 'fEncodeImportNames')
    def fEncodeImportNames( self,
        theTimeProfilingResults     =None,
        theContextualObject         =None, 
        theTranslationService       =None,
        theAllImportTypeConfigs     =None, 
        theOutputEncoding           =None,
        theEncodedNamesCache        =None,
        theEncodingErrors           =None,
        theAdditionalParams         =None):
        """Encode in the output encoding all element and attribute names and selection field voctbulary values.
        
        """

        if ( not theContextualObject) or ( not theAllImportTypeConfigs) or ( not theOutputEncoding) or ( theEncodedNamesCache == None) or ( theEncodingErrors == None):
            return False
        
        
        todosMetaTypes = theAllImportTypeConfigs.keys()
        for unElementMetaType in todosMetaTypes:
        
            unTypeConfig = theAllImportTypeConfigs.get( unElementMetaType, {})
            if unTypeConfig:
     
                # ##############################################################################
                """Encode meta_type name in output encoding.
                
                """
                unElementMetaTypeEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unElementMetaType, theTranslationService, theOutputEncoding)
                if not unEncodingOk:
                    theEncodingErrors.append( { 
                        'status':       cImportStatus_Error_Internal_EncodingError_ElementMetaTypeName,
                        'meta_type':    unElementMetaType,
                    })
                elif not unElementMetaTypeEncoded:
                    theEncodingErrors.append( { 
                        'status':       cImportStatus_Error_Internal_EmptyEncodingResult_ElementMetaTypeName,
                        'meta_type':    unElementMetaType,
                    })
                else:
                    theEncodedNamesCache[ unElementMetaType] = unElementMetaTypeEncoded    
                        
            
        
                # ##############################################################################
                """Encode each configured attribute name in output encoding.
                
                """
                unosAttrConfigs = unTypeConfig.get( 'attrs', [])
                for unAttrConfig in unosAttrConfigs:
                    unAttrName = unAttrConfig.get( 'name', '')
                    if unAttrName:
                            
                        unAttrNameEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unAttrName, theTranslationService, theOutputEncoding)
                        if not unEncodingOk:
                            theEncodingErrors.append( { 
                                'status':       cImportStatus_Error_Internal_EncodingError_AttrName,
                                'meta_type':    unElementMetaType,
                                'attr':         unAttrName,
                            })
                        elif not unAttrNameEncoded:
                            theEncodingErrors.append( { 
                                'status':       cImportStatus_Error_Internal_EmptyEncodingResult_AttrName,
                                'meta_type':    unElementMetaType,
                                'attr':         unAttrName,
                            })
                        else:
                            theEncodedNamesCache[ unAttrName] = unAttrNameEncoded    
                                
        
                unosTraversalConfigs = unTypeConfig.get( 'traversals', [])
                for unTraversalConfig in unosTraversalConfigs:
                    
                    unAggregationName = unTraversalConfig.get( 'aggregation_name', '')
                    if unAggregationName:
    
                        unAggregationNameEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unAggregationName, theTranslationService, theOutputEncoding)
                        if not unEncodingOk:
                            theEncodingErrors.append( { 
                                'status':       cImportStatus_Error_Internal_EncodingError_AggregationName,
                                'meta_type':    unElementMetaType,
                                'attr':         unAggregationName,
                            })
                        elif not unAttrNameEncoded:
                            theEncodingErrors.append( { 
                                'status':       cImportStatus_Error_Internal_EmptyEncodingResult_AggregationName,
                                'meta_type':    unElementMetaType,
                                'attr':         unAggregationName,
                            })
                        else:
                            theEncodedNamesCache[ unAggregationName] = unAggregationNameEncoded    

                    unRelationName = unTraversalConfig.get( 'relation_name', '')
                    if unRelationName:
    
                        unRelationNameEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unRelationName, theTranslationService, theOutputEncoding)
                        if not unEncodingOk:
                            theEncodingErrors.append( { 
                                'status':       cImportStatus_Error_Internal_EncodingError_RelationName,
                                'meta_type':    unElementMetaType,
                                'attr':         unRelationName,
                            })
                        elif not unAttrNameEncoded:
                            theEncodingErrors.append( { 
                                'status':       cImportStatus_Error_Internal_EmptyEncodingResult_RelationName,
                                'meta_type':    unElementMetaType,
                                'attr':         unRelationName,
                            })
                        else:
                            theEncodedNamesCache[ unRelationName] = unRelationNameEncoded    

                            
        return True
    
                    
                    
  
    
    security.declarePrivate( 'fFromSystemEncodingToUnicodeToOutputEncoding')    
    def fFromSystemEncodingToUnicodeToOutputEncoding( self, theString, theTranslationService, theOutputEncoding):
        """Convert theString from the assumed system encoding, to unicode, and from unicode to theOutputEncoding. trapping and reporting errors.
        
        """
        
        if not theString  or not theTranslationService:
            return ( '', False,)
        
             
        unStringUnicode  = ''
        try:
            unStringUnicode = theTranslationService.asunicodetype( theString, errors='strict')
        except:
            return ( '', False,)
        
        if not unStringUnicode:
            return ( '', False,)
            
        
        unStringUTF8 = ''
        try:
            unStringUTF8 = theTranslationService.encode( unStringUnicode, theOutputEncoding, errors='strict')
        except:
            return ( '', False,)

        if not unStringUTF8:
            return ( '', False,)
        
        return ( unStringUTF8, True)

     
    
    
    
    
    
    

   
   

   
   
   
   
   






    
# #########################
#  Log methods
#

     
               
    def logInfo( self, theTravCtxt, theMessage):
# DO NOT EXECUTE        
        if True:
            return self
    
        if not theTravCtxt or not theMessage:
            return self
            
        aLogger = theTravCtxt[ 'logger']
        if aLogger:
            aLogger.info( theMessage)                           
            
                 
           
            
    def logDebug( self, theTravCtxt, theMessage):
        if not theTravCtxt or not theMessage:
            return self
            
        aLogger = theTravCtxt[ 'logger']
        if aLogger:
            aLogger.debug( theMessage)                           
            
             
                        
            
    def logError( self, theTravCtxt, theMessage):
        if not theTravCtxt or not theMessage:
            return self
            
        aLogger = theTravCtxt[ 'logger']
        if aLogger:
            aLogger.error( theMessage)                           
                        
             
     