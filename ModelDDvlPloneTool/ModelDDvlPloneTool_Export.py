# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Export.py
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



import logging
import traceback

from StringIO import StringIO

from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

from xml.dom.minidom import Document
from xml.dom.minidom import Element
from xml.dom.minidom import Node

from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo

from ModelDDvlPloneTool_ImportExport_Constants import *




class ModelDDvlPloneTool_Export:
    """
    """
    security = ClassSecurityInfo()

    
    
    
 
    security.declarePrivate( 'fNewVoidExportReport')    
    def fNewVoidExportReport( self,):
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
    
    
    
    
      
    security.declarePrivate( 'fNewVoidExportContext')    
    def fNewVoidExportContext( self,):
        unInforme = {
            'object':                   None,
            'report':                   self.fNewVoidExportReport(),
            'exported_element_uids':    set(),
            'zip_file':                 None,
            'zip_buffer':               None,
            'xml_document':             None,
            'xml_root':                 [ ],
            'xml_stack':                [ ],
            'images_to_export':         [ ],
            'files_to_export':          [ ],
        }
        return unInforme
    
    
    
    
    
    

    security.declarePrivate( 'fExport')
    def fExport( self,
        theTimeProfilingResults     =None,
        theObject                   =None, 
        theAllExportTypeConfigs     =None, 
        theOutputEncoding           =None,
        theAdditionalParams         =None):
        """Export theObject and its contents into a zip archive, including attached files and images.
        
        """

             
        unExportContext = self.fNewVoidExportContext()
        unExportReport  = unExportContext.get( 'report', {})
        
        
        if ( theObject == None):
            unExportReport.update( { 
                'success':      False,
                'status':       cExportStatus_Error_MissingParameter_Element,
            })
            return unExportReport
            
        unExportContext[ 'object'] = theObject

        if not theAllExportTypeConfigs:
            unExportReport.update( { 
                'success':      False,
                'status':       cExportStatus_Error_MissingParameter_ExportTypeConfigs,
            })
            return unExportReport
        
        unOutputEncoding = theOutputEncoding
        if not unOutputEncoding:
            unOutputEncoding = cXMLEncodingUTF8
        
        # ##############################################################################
        """Retrieve translation_service tool to handle the output encoding.
        
        """
        aTranslationService = getToolByName( theObject, 'translation_service', None)      
        
           
        # ##############################################################################
        """Create in-memory zip file for exported content, to be sent back to the user in the HTTP request response.
        
        """
        unZipBuffer = None
        unZipFile   = None
        
        unZipBuffer      = StringIO()
        unZipFile        = None
        try:
            unZipFile = ZipFile( unZipBuffer, "w", compression=ZIP_DEFLATED)
        except:
            None
        if not unZipFile:
            unZipFile = ZipFile( unZipBuffer, "w", compression=ZIP_STORED)
            
        if not unZipFile:
            unExportReport.update( {
                'success':              False,
                'status':               cExportStatus_Error_Internal_CanNotCreateZipFile,
            })
            return unExportReport
            
        unExportContext.update( {            
            'zip_file':                 unZipFile,
            'zip_buffer':               unZipBuffer,
        })
        
        
        # ##############################################################################
        """Encode in the output encoding, and cache, all meta_type and attribute names.
        
        """
        anEncodedNamesCache = { }
        someEncodingErrors = []
        
        anEncodingResult = self.fEncodeExportNames( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theContextualObject         =theObject, 
            theTranslationService       =aTranslationService,
            theAllExportTypeConfigs     =theAllExportTypeConfigs, 
            theOutputEncoding           =unOutputEncoding,
            theEncodedNamesCache        =anEncodedNamesCache,
            theEncodingErrors           =someEncodingErrors,
            theAdditionalParams         =theAdditionalParams
        )
        
            
        if ( not anEncodingResult) or len( someEncodingErrors):
            unExportReport.update( { 
                'success':      False,
                'status':       cExportStatus_Error_Internal_EncodingErrors,
                'condition':    someEncodingErrors,
            })
            return unExportReport
            

   
        # ##############################################################################
        """Create root of output XML DOM tree.
        
        """
        unXMLDocument = Document()
        unXMLDocument.encoding = unOutputEncoding
        unExportContext.update( {            
            'xml_document':             unXMLDocument,
            'xml_stack':                [ ],
        })
        
        unExportErrors      = [ ]
            
        
        
        unExportResult = self.fExport_Recursive( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theObject                   =theObject, 
            theAllExportTypeConfigs     =theAllExportTypeConfigs, 
            theExportContext            =unExportContext,
            theTranslationService       =aTranslationService,
            theOutputEncoding           =theOutputEncoding,
            theEncodedNamesCache        =anEncodedNamesCache,
            theExportErrors             =unExportErrors,
            theAdditionalParams         =theAdditionalParams)
        
        
        
        
        unExportImagesAndFilesResult = self.fExportImagesAndFiles( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theObject                   =theObject, 
            theAllExportTypeConfigs     =theAllExportTypeConfigs, 
            theExportContext            =unExportContext,
            theTranslationService       =aTranslationService,
            theOutputEncoding           =theOutputEncoding,
            theEncodedNamesCache        =anEncodedNamesCache,
            theExportErrors             =unExportErrors,
            theAdditionalParams         =theAdditionalParams)

        
        
        unXMLString = unXMLDocument.toprettyxml( encoding = unOutputEncoding)
        
        unXMLFileName = '%s.%s' % ( theObject.getId(), cXMLFilePostfix,)
        
        unZipFile.writestr( unXMLFileName, unXMLString)

        unZipFile.close()  
        
        unZIPFileName = '%s.%s' % ( theObject.getId(), cZIPFilePostfix, )
        
        theObject.REQUEST.RESPONSE.setHeader('Content-Type','application/zip')
        theObject.REQUEST.RESPONSE.addHeader("Content-Disposition","filename=%s" % unZIPFileName)
        theObject.REQUEST.RESPONSE.write( unZipBuffer.getvalue()) 
        
        
        
        unExportReport.update( { 
             'success':      True,
        })
        
        return unExportReport
        

           

    security.declarePrivate( 'fExportImagesAndFiles')
    def fExportImagesAndFiles( self,
        theTimeProfilingResults     =None,
        theObject                   =None, 
        theAllExportTypeConfigs     =None, 
        theExportContext            =None,
        theTranslationService       =None,
        theOutputEncoding           =None,
        theEncodedNamesCache        =None,
        theExportErrors             =None,
        theAdditionalParams         =None):
        """Export the files and images found to be exported in the object traversal and export phase.
        
        """

        if ( theObject == None) or ( not theExportContext) or ( not theTranslationService) or ( theExportErrors == None):
            theExportErrors.append( { 
                'success':      False,
                'status':       cExportStatus_Error_Internal_MissingParameters,
            })
            return False

        unZipFile = theExportContext.get( 'zip_file', None)
        if not unZipFile:
            theExportErrors.append( { 
                'success':      False,
                'status':       cExportStatus_Error_Internal_MissingZipFile,
            })
            return False        
        
        someImagesToExport = theExportContext.get( 'images_to_export', [])
        for anImageToExport in someImagesToExport:
            anImageFullFileName = anImageToExport[ 0]
            anImageAsFile       = anImageToExport[ 1]
            
            if anImageFullFileName and anImageAsFile:
                unZipFile.writestr( anImageFullFileName, anImageAsFile.getvalue())
                
        someFilesToExport = theExportContext.get( 'files_to_export', [])
        for anFileToExport in someFilesToExport:
            anFileFullFileName = anFileToExport[ 0]
            anFileAsFile       = anFileToExport[ 1]
            
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
    
    
    
    
   

    security.declarePrivate( 'fExport_Recursive')
    def fExport_Recursive( self,
        theTimeProfilingResults     =None,
        theObject                   =None, 
        theAllExportTypeConfigs     =None, 
        theExportContext            =None,
        theTranslationService       =None,
        theOutputEncoding           =None,
        theEncodedNamesCache        =None,
        theExportErrors             =None,
        theAdditionalParams         =None):
        """Export theObject and its contents into a zip archive, with references to files and images to be attached.
        
        """

        if ( theObject == None) or ( not theAllExportTypeConfigs) or ( not theExportContext) or ( not theTranslationService) or ( theEncodedNamesCache == None) or ( theExportErrors == None):
            theExportErrors.append( { 
                'success':      False,
                'status':       cExportStatus_Error_Internal_MissingParameters,
            })
            return False
        
        unExportReport  = theExportContext.get( 'report', {})
        
        unElementMetaType = theObject.meta_type
        
        unTypeConfig = theAllExportTypeConfigs.get( unElementMetaType, {})
        if not unTypeConfig:
            """Ignore object and do not export it, allowing the caller to continue with other objects, if any.
            
            """
            return True
        
        unXMLStack = theExportContext.get( 'xml_stack', None)
        if ( unXMLStack == None):
            theExportErrors.append( { 
                'success':      False,
                'status':       cExportStatus_Error_Internal_NoXMLStack,
            })
            return False
            
        unXMLDocument = theExportContext.get( 'xml_document', None)
        if ( unXMLDocument == None):
            theExportErrors.append( { 
                'success':      False,
                'status':       cExportStatus_Error_Internal_NoXMLDocument,
            })
            return False
            
        
        
        # ##############################################################################
        """Get metatype name encoded for output from cache .
        
        """
        unElementMetaTypeEncoded = theEncodedNamesCache.get( unElementMetaType, None)
        if not unElementMetaTypeEncoded:
            unExportReport.update( { 
                'success':      False,
                'status':       cExportStatus_Error_Internal_EncodedNameMissing_ElementMetaTypeName,
            })
            return False
         
            
            
            
        # ##############################################################################
        """Create new element in the document and set identifying attributes.
        
        """
        unNewElement = unXMLDocument.createElement( unElementMetaTypeEncoded)
        
        unNewElement.setAttribute( cXMLAttributeName_PloneTitle,    theObject.Title())
        unNewElement.setAttribute( cXMLAttributeName_PloneUID,      theObject.UID())
        unNewElement.setAttribute( cXMLAttributeName_PlonePath,     '/'.join( theObject.getPhysicalPath()))
        
        
        
        # ##############################################################################
        """Add new element to parent, or as root if no current parent, adding the new element to the stack.
        
        """
        if not unXMLStack:
            unXMLDocument.appendChild( unNewElement)
            theExportContext[ 'xml_root'] = unNewElement
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
                unExportReport.update( { 
                    'success':      False,
                    'status':       cExportStatus_Error_Internal_ObjectHasNoSchema,
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
                        theExportErrors.append( { 
                            'status':       cExportStatus_Error_Internal_EncodedNameMissing_AttrName,
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
                                theExportErrors.append( { 
                                    'status':       cExportStatus_Error_Internal_AttributeAccessorNotFound,
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
                                    unInformeExcepcion = 'Exception during fExport_Recursive during invocation of element explicit accessor for attribute\n' 
                                    unInformeExcepcion += 'meta_type=%s path=%s attribute=%s accessor=%s\n' % ( unElementMetaType, '/'.join( theObject.getPhysicalPath()), unAttrName, unAccessor,)
                                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                                    unInformeExcepcion += unaExceptionFormattedTraceback   
                                    
                                    theExportErrors.append( { 
                                        'status':       cExportStatus_Error_Internal_AttributeValueAccessException,
                                        'meta_type':    unElementMetaType,
                                        'attr':         unAttrName,
                                        'path':         '/'.join( theObject.getPhysicalPath()),
                                        'exception':    unInformeExcepcion,
                                    })
                                    aLogger = logging.getLogger( 'ModelDDvlPloneTool_Export::fExport_Recursive')
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
                                unInformeExcepcion = 'Exception during fExport_Recursive during access to element getattribute\n' 
                                unInformeExcepcion += 'meta_type=%s path=%s attribute=%s attributeName=%s\n' % ( unElementMetaType, '/'.join( theObject.getPhysicalPath()), unAttrName, unAttributeName)
                                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                                unInformeExcepcion += unaExceptionFormattedTraceback   
                                
                                theExportErrors.append( { 
                                    'status':       cExportStatus_Error_Internal_AttributeValueAccessException,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'path':         '/'.join( theObject.getPhysicalPath()),
                                    'exception':    unInformeExcepcion,
                                })
                                aLogger = logging.getLogger( 'ModelDDvlPloneTool_Export::fExport_Recursive')
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
                                unInformeExcepcion = 'Exception during fExport_Recursive accessing element attribute\n' 
                                unInformeExcepcion += 'meta_type=%s path=%s attribute=%s\n' % ( unElementMetaType, '/'.join( theObject.getPhysicalPath()), unAttrName,)
                                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                                unInformeExcepcion += unaExceptionFormattedTraceback   
                                
                                theExportErrors.append( { 
                                    'status':       cExportStatus_Error_Internal_AttributeValueAccessException,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'path':         '/'.join( theObject.getPhysicalPath()),
                                    'exception':    unInformeExcepcion,
                                })
                                aLogger = logging.getLogger( 'ModelDDvlPloneTool_Export::fExport_Recursive')
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
                                        'status':       cExportStatus_Error_Internal_EncodingError_AttributeValue_String,
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
                                    'status':       cExportStatus_Error_Internal_EncodingError_AttributeValue_String,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'value':        repr( unImageFullFileName),
                                })
                                unValueStringEncoded = ''
                            
                            theExportContext[ 'images_to_export'].append( [ unImageFullFileName, unaImageAsFile,])
                            
                            
                        elif unObjectAttributeFieldType == 'file':
                            unFileAsFile = unRawValue
                            unFileFullFileName = '/'.join( theObject.getPhysicalPath() + ( theObject.getFilename(), ))

                            unValueStringEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unFileFullFileName, theTranslationService, theOutputEncoding)
                            if ( not unEncodingOk)  or not unValueStringEncoded:
                                theEncodingErrors.append( { 
                                    'status':       cExportStatus_Error_Internal_EncodingError_AttributeValue_String,
                                    'meta_type':    unElementMetaType,
                                    'attr':         unAttrName,
                                    'value':        repr( unFileFullFileName),
                                })
                                unValueStringEncoded = ''
                            
                            theExportContext[ 'files_to_export'].append( [ unFileFullFileName, unFileAsFile,])
                            
                            

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
                                    
                                    unSubItemExportResult = self.fExport_Recursive( 
                                        theTimeProfilingResults     =theTimeProfilingResults,
                                        theObject                   =unSubItem, 
                                        theAllExportTypeConfigs     =theAllExportTypeConfigs, 
                                        theExportContext            =theExportContext,
                                        theTranslationService       =theTranslationService,
                                        theOutputEncoding           =theOutputEncoding,
                                        theEncodedNamesCache        =theEncodedNamesCache,
                                        theExportErrors             =theExportErrors,
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
                                """Export  sorted references to related items.
                                
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
                                                    'status':       cExportStatus_Error_Internal_EncodedNameMissing_ElementMetaTypeName,
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
    
    
    
        
        
        
    
    
    
    
    
    


    security.declarePrivate( 'fEncodeExportNames')
    def fEncodeExportNames( self,
        theTimeProfilingResults     =None,
        theContextualObject         =None, 
        theTranslationService       =None,
        theAllExportTypeConfigs     =None, 
        theOutputEncoding           =None,
        theEncodedNamesCache        =None,
        theEncodingErrors           =None,
        theAdditionalParams         =None):
        """Encode in the output encoding all element and attribute names and selection field voctbulary values.
        
        """

        if ( theContextualObject == None) or ( not theAllExportTypeConfigs) or ( not theOutputEncoding) or ( theEncodedNamesCache == None) or ( theEncodingErrors == None):
            return False
        
        
        todosMetaTypes = theAllExportTypeConfigs.keys()
        for unElementMetaType in todosMetaTypes:
        
            unTypeConfig = theAllExportTypeConfigs.get( unElementMetaType, {})
            if unTypeConfig:
     
                # ##############################################################################
                """Encode meta_type name in output encoding.
                
                """
                unElementMetaTypeEncoded, unEncodingOk = self.fFromSystemEncodingToUnicodeToOutputEncoding( unElementMetaType, theTranslationService, theOutputEncoding)
                if not unEncodingOk:
                    theEncodingErrors.append( { 
                        'status':       cExportStatus_Error_Internal_EncodingError_ElementMetaTypeName,
                        'meta_type':    unElementMetaType,
                    })
                elif not unElementMetaTypeEncoded:
                    theEncodingErrors.append( { 
                        'status':       cExportStatus_Error_Internal_EmptyEncodingResult_ElementMetaTypeName,
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
                                'status':       cExportStatus_Error_Internal_EncodingError_AttrName,
                                'meta_type':    unElementMetaType,
                                'attr':         unAttrName,
                            })
                        elif not unAttrNameEncoded:
                            theEncodingErrors.append( { 
                                'status':       cExportStatus_Error_Internal_EmptyEncodingResult_AttrName,
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
                                'status':       cExportStatus_Error_Internal_EncodingError_AggregationName,
                                'meta_type':    unElementMetaType,
                                'attr':         unAggregationName,
                            })
                        elif not unAttrNameEncoded:
                            theEncodingErrors.append( { 
                                'status':       cExportStatus_Error_Internal_EmptyEncodingResult_AggregationName,
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
                                'status':       cExportStatus_Error_Internal_EncodingError_RelationName,
                                'meta_type':    unElementMetaType,
                                'attr':         unRelationName,
                            })
                        elif not unAttrNameEncoded:
                            theEncodingErrors.append( { 
                                'status':       cExportStatus_Error_Internal_EmptyEncodingResult_RelationName,
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
                        
             
     