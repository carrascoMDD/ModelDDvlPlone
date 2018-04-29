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
from cStringIO import StringIO   as clsFastStringIO

from zipfile import ZipFile

from xml.dom.minidom import parseString as gfParseStringAsXMLDocument
from xml.dom.minidom import parse       as gfParseFileAsXMLDocument

from xml.dom.minidom import Document
from xml.dom.minidom import Element
from xml.dom.minidom import Node

from Products.CMFCore.utils import getToolByName

from AccessControl import ClassSecurityInfo



from ModelDDvlPloneTool_ImportExport_Constants import *


from MDD_RefactorComponents                  import MDDRefactor_Import

from ModelDDvlPloneTool_Transactions         import ModelDDvlPloneTool_Transactions

from ModelDDvlPloneTool_Profiling            import ModelDDvlPloneTool_Profiling

from ModelDDvlPloneToolSupport               import fPrettyPrint

cLogExceptions = True
cLogImportResults = True

class MDDRefactor_Import_Exception( Exception): pass




class ModelDDvlPloneTool_Import( ModelDDvlPloneTool_Profiling):
    """
    """
    security = ClassSecurityInfo()

    
    
    security.declarePrivate( 'fTraversalTargetAdditionalParams')    
    def fTraversalTargetAdditionalParams( self,):
        unosParams = {
            'Do_Not_Translate' : True,
            'Retrieve_Minimal_Related_Results': True,
        }
        return unosParams
    
    
    
    security.declarePrivate( 'fTraversalSourcesAdditionalParams')    
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
            'container_object_result':  None,
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
            'xml_encoding':             '',
            'xml_roots':                [ ],
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
        theModelDDvlPloneTool          =None, 
        theModelDDvlPloneTool_Retrieval=None,
        theModelDDvlPloneTool_Mutators =None,
        theContainerObject             =None, 
        theUploadedFile                =None,
        theMDDImportTypeConfigs        =None, 
        thePloneImportTypeConfigs      =None, 
        theMappingConfigs              =None, 
        theMinimumTimeSlice            =None,
        theYieldTimePercent            =None,        
        theAdditionalParams            =None):
        """Import into an element a zipped archive with XML file, and any included binary content the attached files and images."
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fImport', theTimeProfilingResults)
                      
        try:
            unImportReport = None
            try:
                
                # ##############################################################################
                """Transaction Save point before import to get a clean view on the existing object network.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                
                unImportContext   = self.fNewVoidImportContext()
                unImportReport    = unImportContext.get( 'report', {})
                unosImportErrors  = unImportContext.get( 'import_errors', {})
                
                
                # ##############################################################################
                """Check parameters.
                
                """
                if ( theContainerObject == None):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cImportStatus_Error_MissingParameter_ContainerObject,
                    })
                    return unImportReport
                
                unImportReport[ 'container_object'] = theContainerObject
                    
                unImportContext[ 'container_object'] = theContainerObject
        
                if not theUploadedFile:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cImportStatus_Error_MissingParameter_UploadedFile,
                    })
                    return unImportReport
                
                unImportContext[ 'uploaded_file'] = theUploadedFile
                
                
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
                """Analyze uploaded file.
                
                """      
                
                otherFileNames = [ ]
                unXMLDocument = None

                unIsZip = False
                unZipFile = None
                
                
                # ##############################################################################
                """Verify that the uploaded file is a zip archive, or an xml file, or fail.
                
                """      
                try:
                    theUploadedFile.seek( 0)
                    unZipFile = ZipFile( theUploadedFile)  
                except:
                    None
                if unZipFile:
                    # Error if True
                    if not( unZipFile.testzip()):
                        unIsZip = True
 
                
                
                if unIsZip:

                    
                    # ##############################################################################
                    """Find the first .xml file in the tree of files of the zip archive, or fail.
                    
                    """      
                    someXMLFileNamesAndPathsLength = [ ]
                    
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
                                anXMLBaseName     = aBaseName
                                someXMLFileNamesAndPathsLength.append( [ aFullFileName, len( aFullFileName.split( '/'))])
        
                    if not someXMLFileNamesAndPathsLength:
                        unImportReport.update( { 
                            'success':      False,
                            'status':       cImportStatus_Error_Parameter_UploadedFile_ZipWithoutXMLFile,
                        })
                        return unImportReport
                                
                    someSortedXMLFileNamesAndPathsLength = sorted( someXMLFileNamesAndPathsLength, lambda aObj, otherObj: cmp( aObj[1], otherObj[ 1]))
                    anXMLFullFileName = someSortedXMLFileNamesAndPathsLength[ 0][ 0]
                       
                    if not anXMLFullFileName:
                        unImportReport.update( { 
                            'success':      False,
                            'status':       cImportStatus_Error_Parameter_UploadedFile_ZipWithoutXMLFile,
                        })
                        return unImportReport
                    
                    
                    # ##############################################################################
                    """Get all files in the zip archive other than the .xml file.
                    
                    """      
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
                    """Parse encoded contents of .xml file as an XML DOM tree, or fail. The values are encoded as specified in the top meta-element of the xml file.
                    
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
                    
                    
                else:
                        
                    # ##############################################################################
                    """Attempt Parse encoded contents of .xml file as an XML DOM tree, or fail. The values are encoded as specified in the top meta-element of the xml file.
                    
                    """      
                    try:
                        theUploadedFile.seek( 0)
                        unXMLDocument = gfParseFileAsXMLDocument( theUploadedFile)
                    except:
                        None
                        
                    if not unXMLDocument:
                        unImportReport.update( { 
                            'success':      False,
                            'status':       cImportStatus_Error_Parameter_UploadedFile_NotAZipNotAXML,
                        })
                        return unImportReport
                
                    
                unImportContext[ 'xml_document'] = unXMLDocument
                

                
                # ##############################################################################
                """Not really used anymore, as the values in the XML DOM tree are delievered already decoded into unicode, even if the contents of .xml file are encoded as specified in the top meta-element of the xml file.
                
                """      
                unXMLEncoding = unXMLDocument.encoding
                if not unXMLEncoding:
                    unXMLEncoding = cDefaultEncodingForXMLImport
                
                unImportContext[ 'xml_encoding'] = unXMLEncoding
                   
                if not ( unXMLEncoding in cAllEncodingNames):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cImportStatus_Error_XMLEncodingUnknown,
                        'filename':     anXMLFullFileName,
                    })
                    return unImportReport
                
               
                
             
                # ##############################################################################
                """Get roots of the XML DOM tree
                """      
                
                unosXMLRootElements = unXMLDocument.childNodes
                if not unosXMLRootElements:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cImportStatus_Error_NoRootXMLElements,
                        'filename':     anXMLFullFileName,
                    })
                    return unImportReport
                
                unImportContext[ 'xml_roots'] = unosXMLRootElements
                    
                
                
                
                
                # ##############################################################################
                """Retrieve original object result.
                
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
                
                unImportContext[ 'container_object_result'] = unContainerObjecResult
        
                
                # ##############################################################################
                """Verify import can be performed on target object, and the object is readable and writtable.
                
                """      
                unAllowImport = unContainerObjecResult.get( 'allow_import', True)
                if not unAllowImport:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cImportStatus_Error_Import_NotAllowedInElement,
                    })
                    return unImportReport
                
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
                    theModelDDvlPloneTool,
                    theModelDDvlPloneTool_Retrieval,
                    theModelDDvlPloneTool_Mutators,
                    unZipFile, 
                    otherFileNames,
                    unXMLDocument,
                    unXMLEncoding,
                    unosXMLRootElements,
                    theContainerObject, 
                    unContainerObjecResult, 
                    theMDDImportTypeConfigs,
                    somePloneImportTypeConfigs,
                    allImportTypeConfigs, 
                    someMappingConfigs,
                    MDDRefactor_Import_Exception, # theExceptionToRaise,
                    True, # theAllowPartialCopies,
                    True, # theIgnorePartialLinksForMultiplicityOrDifferentOwner
                    theMinimumTimeSlice,
                    theYieldTimePercent,        
                )  
                if ( not unRefactor) or not unRefactor.vInitialized:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cImportStatus_Error_Internal_Refactor_NotInitialized,
                    })
                    return unImportReport
                
                
                
                # ##############################################################################
                """Transaction Save point before import to get a clean view on the existing object network.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                                
                
                unHuboRefactorException  = False
                unHuboException  = False
                unRefactorResult = False
                try:
                    
                    try:
                        unRefactorResult = unRefactor.fRefactor()
                    
                    except MDDRefactor_Import_Exception:
                        
                        unHuboRefactorException = True
                        
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                        
                        unInformeExcepcion = 'Exception during ModelDDvlPloneTool_Refactor::fImport invoking MDDRefactor_Import::fRefactor\n' 
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        unImportReport[ 'exception'] = unInformeExcepcion
                                 
                        if cLogExceptions:
                            logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                        
                except:
                    unHuboException = True
                    raise
                                
                
                unImportReport.update( {
                    'num_elements_pasted':         unRefactor.vNumElementsPasted,
                    'num_mdd_elements_pasted':     unRefactor.vNumMDDElementsPasted,
                    'num_plone_elements_pasted':   unRefactor.vNumPloneElementsPasted,
                    'num_attributes_pasted':       unRefactor.vNumAttributesPasted,
                    'num_links_pasted':            unRefactor.vNumLinksPasted,
                    'num_elements_failed':         unRefactor.vNumElementsFailed,
                    'num_mdd_elements_failed':     unRefactor.vNumMDDElementsFailed,
                    'num_plone_elements_failed':   unRefactor.vNumPloneElementsFailed,
                    'num_attributes_failed':       unRefactor.vNumAttributesFailed,
                    'num_links_failed':            unRefactor.vNumLinksFailed,
                    'num_elements_bypassed':       unRefactor.vNumElementsBypassed,
                    'num_mdd_elements_bypassed':   unRefactor.vNumMDDElementsBypassed,
                    'num_plone_elements_bypassed': unRefactor.vNumPloneElementsBypassed,
                    'num_attributes_bypassed':     unRefactor.vNumAttributesBypassed,
                    'num_links_bypassed':          unRefactor.vNumLinksBypassed,
                })
                unImportReport[ 'error_reports'].extend( unRefactor.vErrorReports )
                 
                
                ModelDDvlPloneTool_Transactions().fTransaction_Commit()

                if cLogImportResults:
                    logging.getLogger( 'ModelDDvlPlone').info( 'COMMIT: %s::fImport\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unImportReport, ])))
                    
                    
                if ( not unHuboException) and ( not unHuboRefactorException) and unRefactorResult:
    
                    unImportReport.update( { 
                         'success':      True,
                    })
                    if cLogImportResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'COMMITTED COMPLETED: %s::fImport\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unImportReport, ])))
                    
                else:
                    
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cImportStatus_Error_Internal_Refactor_Failed,
                    })
                    
                    if cLogImportResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'COMMITTED WITH ERRORS during: %s::fImport\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unImportReport, ])))
                    
                    
                return unImportReport        
            
            
           
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fImport (before start writting or after committing changes)\n' 
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
                        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fImport', theTimeProfilingResults)
            
    
               
            


           
    
    
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

     