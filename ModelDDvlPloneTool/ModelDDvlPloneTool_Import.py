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

import sys
import traceback
import logging

from StringIO import StringIO

from zipfile import ZipFile

from xml.dom.minidom import parseString as gfParseStringAsXMLDocument
from xml.dom.minidom import Document
from xml.dom.minidom import Element
from xml.dom.minidom import Node

from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo

from MDD_RefactorComponents import MDDRefactor_Import


from ModelDDvlPloneTool_ImportExport_Constants import *




cLogExceptions = True



class ModelDDvlPloneTool_Import:
    """
    """
    security = ClassSecurityInfo()

    
    
    security.declarePrivate( 'fTraversalAdditionalParams')    
    def fTraversalTargetAdditionalParams( self,):
        unosParams = {
            'Do_Not_Translate' : True,
            'Retrieve_Minimal_Related_Results': True,
        }
        return unosParams
    
    
    
    security.declarePrivate( 'fTraversalAdditionalParams')    
    def fTraversalSourcesAdditionalParams( self,):
        unosParams = {
            'Do_Not_Translate' : True,
            'Retrieve_Minimal_Related_Results': True,
        }
        return unosParams
    
        
    
    security.declarePrivate( 'fNewVoidImportContext')    
    def fNewVoidImportContext( self,):
        unContext = {
            'container_object':         None,
            'uploaded_file':            None,
            'objects_to_paste':         [],
            'ModelDDvlPloneTool_Retrieval': None,
            'ModelDDvlPloneTool_Mutators': None,
            'checked_permissions_cache': None,
            'mdd_type_configs':         {},
            'plone_type_configs':       {},
            'all_copy_type_configs':    {},
            'mapping_configs':          [],
            'additional_params':        self.fTraversalSourcesAdditionalParams(),
            'report':                   self.fNewVoidImportReport(),
            'translation_service':      None,
            #'source_frames':            [ ],
            #'source_elements':          [ ],
            #'source_elements_by_UID':   { },
            #'source_stack':             [ ],
            #'target_elements':          [ ],
            #'target_elements_by_UID':   { },
            #'target_stack':             [ ],
            'zip_file':                 None,
            'zip_buffer':               None,
            'xml_document':             None,
            'xml_root':                 [ ],
            'images_imported':          [ ],
            'files_imported':           [ ],
        }
        return unContext
    
      
    
    security.declarePrivate( 'fNewVoidImportReport')    
    def fNewVoidImportReport( self,):
        unInforme = {
            'success':                  False,
            'status':                   '',
            'condition':                None,
            'exception':                '',
            'num_elements_imported':      0,
            'num_mdd_elements_imported':  0,
            'num_plone_elements_imported': 0,
            'error_reports':            [ ],
        }
        return unInforme
    
    
    
    
    
    
    

    security.declarePrivate( 'fImport')
    def fImport( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool_Retrieval=None,
        theModelDDvlPloneTool_Mutators =None,
        theContainerObject             =None, 
        theUploadedFile                =None,
        theMDDImportTypeConfigs        =None, 
        thePloneImportTypeConfigs      =None, 
        theMappingConfigs              =None, 
        theAdditionalParams            =None):
        """Import into an element a zipped archive with XML file, and any included binary content the attached files and images."
        
        """

        unImportReport = None
        try:
            
            unImportContext   = self.fNewVoidImportContext()
            unImportReport    = unImportContext.get( 'report', {})
            unosImportErrors  = unImportContext.get( 'import_errors', {})
            
            
            if ( theContainerObject == None):
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_MissingParameter_ContainerObject,
                })
                return unImportReport
                
            unImportContext[ 'container_object'] = theContainerObject
    
            if not theUploadedFile:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_MissingParameter_UploadedFile,
                })
                return unImportReport
            
            unImportContext[ 'uploaded_file'] = theContainerObject
            
            
            if not theMDDImportTypeConfigs:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_MissingParameter_MDDImportTypeConfigs,
                })
                return unImportReport
            unImportContext[ 'mdd_type_configs'] = theMDDImportTypeConfigs
    
            somePloneImportTypeConfigs = thePloneImportTypeConfigs
            if not somePloneImportTypeConfigs:
                somePloneImportTypeConfigs = {}
            unImportContext[ 'plone_type_configs'] = somePloneImportTypeConfigs
            
            
            someMappingConfigs = theMappingConfigs
            if not someMappingConfigs:
                someMappingConfigs = []
            unImportContext[ 'mapping_configs'] = someMappingConfigs

            
            allImportTypeConfigs = somePloneImportTypeConfigs.copy()
            allImportTypeConfigs.update( theMDDImportTypeConfigs)
            unImportContext[ 'all_copy_type_configs'] = allImportTypeConfigs
            
            if not theModelDDvlPloneTool_Retrieval:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval,
                })
                return unImportReport
            unImportContext[ 'ModelDDvlPloneTool_Retrieval'] = theModelDDvlPloneTool_Retrieval
            
            unCheckedPermissionsCache = theModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
            unImportContext[ 'checked_permissions_cache'] = unCheckedPermissionsCache
            
            if not theModelDDvlPloneTool_Mutators:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators,
                })
                return unImportReport
            unImportContext[ 'ModelDDvlPloneTool_Mutators'] = theModelDDvlPloneTool_Mutators
            
            if theAdditionalParams:
                unImportContext[ 'additional_params'].update( theAdditionalParams)
            
            # ##############################################################################
            """Retrieve translation_service tool to handle the input encoding.
            
            """
            aTranslationService = getToolByName( theContainerObject, 'translation_service', None)      
            if not aTranslationService:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_Internal_MissingTool_translation_service,
                })
                return unImportReport
            unImportContext[ 'translation_service'] = aTranslationService
            
               
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
            """Get all files in the zip archive other than the .xml file.
            
            """      
            otherFileNames = [ ]
            for aFullFileName in someFileNames:
                if not ( aFullFileName == anXMLFullFileName):   
                    otherFileNames.append( aFullFileName)
                    
                                
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
            
            unosXMLRootElements = unXMLDocument.childNodes
            if not unosXMLRootElements:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_NoRootXMLElements,
                    'filename':     anXMLFullFileName,
                })
                return unImportReport
            
                
            
            # ##############################################################################
            """Retrieve container object.
            
            """      
            unContainerObjecResult = self.fRetrieveContainer( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theImportContext            =unImportContext,
            )
            
            if (not unContainerObjecResult) or ( unContainerObjecResult.get( 'object', None) == None):
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_Internal_NoContainerRetrieved,
                })
                return unImportReport
    
            unAllowImport = unContainerObjecResult.get( 'allow_import', True)
            if not unAllowImport:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_Import_NotAllowedInElement,
                })
                return unRefactorReport
            
            unContainerReadPermission = unContainerObjecResult.get( 'read_permission', False)
            if not unContainerReadPermission:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_Container_NotReadable,
                })
                return unImportReport
                
            unContainerWritePermission = unContainerObjecResult.get( 'write_permission', False)
            if not unContainerWritePermission:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_Container_NotWritable,
                })
                return unImportReport
            
             
            # ##############################################################################
            """Traverse parsed XML DOM tree and create or update application elements from XML node data.
            
            """      

           
            unRefactor = MDDRefactor_Import( 
                unZipFile, 
                otherFileNames,
                unXMLDocument,
                unosXMLRootElements,
                theContainerObject, 
                unContainerObjecResult, 
                theMDDImportTypeConfigs,
                somePloneImportTypeConfigs,
                allImportTypeConfigs, 
                someMappingConfigs,
            )  
            if ( not unRefactor) or not unRefactor.vInitialized:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_Internal_Refactor_NotInitialized,
                })
                return unImportReport
                
            unRefactorResult = unRefactor.fRefactor()
            
            if unRefactorResult:
                unImportReport.update( { 
                     'success':      True,
                })
            else:
                unImportReport.update( { 
                    'success':      False,
                    'status':       cImportStatus_Error_Internal_Refactor_Failed,
                })
                
            
            return unImportReport        
        
        
       
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during fImport\n' 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            if not unImportReport:
                unImportReport = { }
                
            unImportReport.update( { 
                'success':      False,
                'status':       cImportStatus_Error_Exception,
                'exception':    unInformeExcepcion,
            })
                
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            return unImportReport
                    
        return { 'success': False, }
            


           
    
    
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
    
    
    
    
        
    security.declarePrivate( 'fRetrieveContainer')
    def fRetrieveContainer( self,
        theTimeProfilingResults     =None,
        theImportContext            =None):
        """Retrieve basic information from the target element into which to paste the elements in theObjectsToImport.
        
        """
    
        aContainerResult = None

        if not theImportContext:
            return aContainerResult
        
        unTargetObject = theImportContext.get( 'container_object', None)
        if ( unTargetObject == None):
            return aContainerResult
        
        someMDDCopyTypeConfigs   = theImportContext.get( 'mdd_type_configs',   {})

        unTargetMetaType = unTargetObject.meta_type
        if unTargetMetaType:
        
            unTargetMDDTypeConfig = someMDDCopyTypeConfigs.get( unTargetMetaType, None)
            if unTargetMDDTypeConfig:
                
                aContainerResult = self.fRetrieveContainer_MDD(
                    theTimeProfilingResults,
                    theImportContext,
                    unTargetObject,
                )
                if aContainerResult and not  ( aContainerResult.get( 'object', None) == None):
                    aContainerResult[ 'is_MDD']   = True
                    aContainerResult[ 'is_Plone'] = False
                else:
                    return None
                

                        
            if aContainerResult:
                aContainerReadPermission = aContainerResult.get( 'read_permission', False)
                if not aContainerReadPermission:
                    return None
                
                aContainerWritePermission = aContainerResult.get( 'write_permission', False)
                if not aContainerWritePermission:
                    return None

        return aContainerResult
    
                        
                        



    security.declarePrivate( 'fRetrieveContainer_MDD')
    def fRetrieveContainer_MDD( self,
        theTimeProfilingResults     =None,
        theImportContext             =None,
        theTargetObject             =None):
        """
        
        """
        
        try:
            if not theImportContext:
                return None
           
            if not theTargetObject:
                return None
           
            allCopyTypeConfigs = theImportContext.get( 'all_copy_type_configs', {})
            if not allCopyTypeConfigs:
                return None
                            
            someAdditionalParams = theImportContext.get(  'additional_params', None)
            
            aModelDDvlPloneTool_Retrieval = theImportContext.get( 'ModelDDvlPloneTool_Retrieval', None)
            if not aModelDDvlPloneTool_Retrieval:
                return None
            
            unCheckedPermissionsCache = theImportContext.get( 'checked_permissions_cache', None)
            
            unElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     = theTimeProfilingResults,
                theElement                  = theTargetObject, 
                theParent                   = None,
                theParentTraversalName      = '',
                theTypeConfig               = None, 
                theAllTypeConfigs           = allCopyTypeConfigs, 
                theViewName                 = '', 
                theRetrievalExtents         = [ 'traversals', ],
                theWritePermissions         =[ 'object', 'add', 'add_collection', 'aggregations', ],
                theFeatureFilters           =None, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =someAdditionalParams
            )
            if not unElementResult or not( unElementResult.get( 'object', None) == theTargetObject):
                return None
                        
        
            return unElementResult
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during fImport fRetrieveContainer_MDD\n' 
            unInformeExcepcion += 'source object %s\n' % str( theTargetObject) 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            return None
                    
        return None    
    

    
# #########################
#  Log methods
#

     