# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Import.py
#
# Copyright (c) 2008, 2009, 2010 by Model Driven Development sl and Antonio Carrasco Valero
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




from ModelDDvlPloneTool_Profiling            import ModelDDvlPloneTool_Profiling


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
            #'xml_encoding':             '',
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
            
            'num_elements_imported_by_type':      { },
            
            'num_elements_imported':      0,
            'num_mdd_elements_imported':  0,
            'num_plone_elements_imported': 0,
            'error_reports':            [ ],
            
            
            'num_elements_pasted':         0,
            'num_mdd_elements_pasted':     0,
            'num_plone_elements_pasted':   0,
            'num_attributes_pasted':       0,
            'num_links_pasted':            0,
            'num_elements_failed':         0,
            'num_mdd_elements_failed':     0,
            'num_plone_elements_failed':   0,
            'num_attributes_failed':       0,
            'num_links_failed':            0,
            'num_elements_bypassed':       0,
            'num_mdd_elements_bypassed':   0,
            'num_plone_elements_bypassed': 0,
            'num_attributes_bypassed':     0,
            'num_links_bypassed':          0,
            
        }
        return unInforme
    
    
    
    
    
    

    security.declarePrivate( 'fNewVoidXMLAndBinariesScanResult')    
    def fNewVoidXMLAndBinariesScanResult( self,):
        aResult = {
            'success':                       False,
            'status':                        '',
            'condition':                     None,
            'exception':                     '',
            'is_zip':                        False,
            'xml_full_filename':             '',
            'xml_source':                    '',
            'xml_document':                  None,
            'xml_roots':                     None,
            'files_whole_data_by_full_name': { },
        }
        return aResult
    
        
    
    
    security.declarePrivate( 'fNewVoidXMLSummaryResult')    
    def fNewVoidXMLSummaryResult( self,):
        aResult = {
            'success':                       False,
            'status':                        '',
            'condition':                     None,
            'exception':                     '',
            'accepted_root_node_name':       '',
            'node_names_to_count':           [],
            
            'num_nodes':                     0,
            'num_nodes_by_type':             { },
            
            'xml_document':                  None,
            'xml_roots':                     None,            
        }
        return aResult
    
        
        



    security.declarePrivate( 'fXMLContentSummary')
    def fXMLContentSummary( self,
        theTimeProfilingResults        =None,
        theContextualElement           =None, 
        theXMLSource                   =None,
        theAcceptedXMLRootNodeName     =None,
        theXMLNodeNamesToCount         =None,
        theAdditionalParams            =None):
        """Parse XML source and Scan the XML tree reporting a summary of the number of contained nodes of specified types."
        
        """        
        
        # ##############################################################################
        """Build result structure.
        
        """           
        aXMLSummaryResult = self.fNewVoidXMLSummaryResult()
         
   
        
        
        
        # ##############################################################################
        """Check essential parameters.
        
        """           
        if not theXMLSource:
            aXMLSummaryResult.update( {
                'success':  False,
                'status':   'Empty_theXMLSource',
            })
            return aXMLSummaryResult
        
        
        if not theAcceptedXMLRootNodeName:
            aXMLSummaryResult.update( {
                'success':  False,
                'status':   'No_theAcceptedXMLRootNodeName',
            })
            return aXMLSummaryResult
        
        
        if not theXMLNodeNamesToCount:
            aXMLSummaryResult.update( {
                'success':  False,
                'status':   'No_theXMLNodeNamesToCount',
            })
            return aXMLSummaryResult
        
              
        
        
        aXMLSummaryResult.update( {
            'accepted_root_node_name':  theAcceptedXMLRootNodeName,
            'node_names_to_count':      theXMLNodeNamesToCount,
        })
        
        
        
        
        
        # ##############################################################################
        """Parse encoded contents of .xml file as an XML DOM tree, or fail. The values are encoded as specified in the top meta-element of the xml file.
        
        """      
        unXMLDocument = None
        try:
            unXMLDocument = gfParseStringAsXMLDocument( theXMLSource)
        except:
            None
            
        if not unXMLDocument:
            aXMLSummaryResult.update( {
                'success':  False,
                'status':   'Error_parsing_XML_Source',
            })
            return aXMLSummaryResult
        
        
        aXMLSummaryResult[ 'xml_document'] = unXMLDocument
        
        
        
                   
        # ##############################################################################
        """Select root node of accepted type.
        
        """   
        
        unosXMLRootNodes = unXMLDocument.childNodes
        
        if not unosXMLRootNodes:
            aXMLSummaryResult.update( {
                'success':  False,
                'status':   'Empty_XML_Document_tree',
            })
            return aXMLSummaryResult
        
           
        anAcceptedXMLRootNode = None
        for anXMLRootNode in unosXMLRootNodes:
            anXMLRootNodeName = anXMLRootNode.nodeName
            
            if anXMLRootNodeName == theAcceptedXMLRootNodeName:
                anAcceptedXMLRootNode = anXMLRootNode
                break
                    
        if not anAcceptedXMLRootNode:
            aXMLSummaryResult.update( {
                'success':  False,
                'status':   'No_Accepted_XML_Root_Node',
            })
            return aXMLSummaryResult
        
        
        aXMLSummaryResult[ 'xml_roots'] = [ anAcceptedXMLRootNode,]
        
        
        
        # ##############################################################################
        """Recursively Scan the XML tree reporting a summary of the number of contained nodes of specified types."
        
        """   
        self.pXMLContentSummary( 
            theTimeProfilingResults  =theTimeProfilingResults,
            theContextualElement     =theContextualElement,
            theXMLNode               =anAcceptedXMLRootNode,
            theXMLNodeNamesToCount   =theXMLNodeNamesToCount,
            theXMLSummaryResult      =aXMLSummaryResult,
        )
        
                
        aXMLSummaryResult.update( {
            'success':  True,
        })
        
        return aXMLSummaryResult
    
    
    
    
    
    


    security.declarePrivate( 'pXMLContentSummary')
    def pXMLContentSummary( self,
        theTimeProfilingResults   =None,
        theContextualElement      =None, 
        theXMLNode                =None,
        theXMLNodeNamesToCount    =None,
        theXMLSummaryResult       =None,):
        """Recursively Scan the XML tree reporting a summary of the number of contained nodes of specified types."
        
        """   
    
        if not theXMLNode:
            return self


        
        anXMLNodeName = theXMLNode.nodeName
        if anXMLNodeName in theXMLNodeNamesToCount:
            someNumNodesByName = theXMLSummaryResult.get( 'num_nodes_by_type', None)
            if not ( someNumNodesByName == None):
                someNumNodesByName[ anXMLNodeName] = someNumNodesByName.get( anXMLNodeName, 0) + 1
                
            theXMLSummaryResult[ 'num_nodes'] = theXMLSummaryResult.get( 'num_nodes', 0) + 1
                
        
        someChildrenNodes = theXMLNode.childNodes
        if not someChildrenNodes:
            return self
        
        
        for aChildNode in someChildrenNodes:
            
            self.pXMLContentSummary( 
                theTimeProfilingResults  =theTimeProfilingResults,
                theContextualElement     =theContextualElement,
                theXMLNode               =aChildNode,
                theXMLNodeNamesToCount   =theXMLNodeNamesToCount,
                theXMLSummaryResult      =theXMLSummaryResult,
            )
        
        return self
        
        
        
        
        
    
    

    security.declarePrivate( 'fScanXMLAndBinariesFromUploadedFile')
    def fScanXMLAndBinariesFromUploadedFile( self,
        theTimeProfilingResults        =None,
        theContextualElement           =None, 
        theUploadedFile                =None,
        theAcceptedXMLRootNodeName     =None,
        theExcludedFullFileNames       =None,
        theExcludedFilePostfixes       =None,
        theAdditionalParams            =None):
        """Scan the content of the uploaded file, which may be a single XML file, or a zipped archive with an XML file, and some other files."
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fScanXMLAndBinariesFromUploadedFile', theTimeProfilingResults)
            
        unResult = self.fNewVoidXMLAndBinariesScanResult()

        someExcludedFullFileNames = theExcludedFullFileNames
        if not someExcludedFullFileNames:
            someExcludedFullFileNames = [ ]
            
        someExcludedFilePostfixes = theExcludedFilePostfixes
        if not someExcludedFilePostfixes:
            someExcludedFilePostfixes = [ ]
        
                      
        try:
            try:

                
                # ##############################################################################
                """Check parameters.
                
                """
                if ( theContextualElement == None):
                    unResult.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_ContextualElement,
                    })
                    return unResult
            
        
                if not theUploadedFile:
                    unResult.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_UploadedFile,
                    })
                    return unResult
                                
                
             
                
                
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
                    
                    unResult[ 'is_zip'] = True
                    
                    # ##############################################################################
                    """Find the first .xml file in the tree of files of the zip archive, or fail.
                    
                    """      
                    someXMLFileNamesAndPathsLength = [ ]
                    
                    unXMLPostfix = '.%s' % cMDDXMLFilePostfix.lower()
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
                        unResult.update( { 
                            'success':      False,
                            'status':       cMDDImportStatus_Error_Parameter_UploadedFile_ZipWithoutXMLFile,
                        })
                        return unResult
                                
                    someSortedXMLFileNamesAndPathsLength = sorted( someXMLFileNamesAndPathsLength, lambda aObj, otherObj: cmp( aObj[1], otherObj[ 1]))
                    anXMLFullFileName = someSortedXMLFileNamesAndPathsLength[ 0][ 0]
                       
                    if anXMLFullFileName:
                        
                        someExcludedFullFileNames.append( anXMLFullFileName)
                        
                        unXMLBuffer = self.fZipFileElementContent( unZipFile, anXMLFullFileName)
                        
                                                 
                        if unXMLBuffer:
                            # ##############################################################################
                            """Parse encoded contents of .xml file as an XML DOM tree, or fail. The values are encoded as specified in the top meta-element of the xml file.
                            
                            """      
                            unXMLDocument = None
                            try:
                                unXMLDocument = gfParseStringAsXMLDocument( unXMLBuffer)
                            except:
                                None
                                
                            if unXMLDocument:
                                
                                unResult[ 'xml_document'] = unXMLDocument
                                           
                                unosXMLRootElements = unXMLDocument.childNodes
                                
                                
                                if theAcceptedXMLRootNodeName:
                                    
                                    if unosXMLRootElements:
                                      
                                        for anXMLRootElement in unosXMLRootElements:
                                            anXMLRootElementName = anXMLRootElement.nodeName
                                            
                                            if anXMLRootElementName == theAcceptedXMLRootNodeName:
                                
                                                unResult[ 'xml_roots'] = [ anXMLRootElement, ]
                                                
                                                unResult[ 'xml_full_filename'] = anXMLFullFileName
                                                unResult[ 'xml_source'] = unXMLBuffer
                                                break
                                            
                                else:
                                    
                                    if unXMLDocument.childNodes:
                                        unResult[ 'xml_roots'] = [ unXMLDocument.childNodes[ 0], ]
                                        
                                    else:
                                        unResult[ 'xml_roots'] = []
                                    
                                    unResult[ 'xml_full_filename'] = anXMLFullFileName
                                    unResult[ 'xml_source'] = unXMLBuffer
                    
                    
                                    
                                    
                    # ##############################################################################
                    """Get all files in the zip archive other than: the .xml file, excluded files, or excluded file postfixes.
                    
                    """      
                    for aFullFileName in someFileNames:
                        
                        if not someExcludedFilePostfixes:
                            
                            if not ( aFullFileName in someExcludedFullFileNames):
                        
                                unOtherFileWholeData = self.fZipFileElementContent( unZipFile, aFullFileName)
                                
                                unResult[ 'files_whole_data_by_full_name'][ aFullFileName] = unOtherFileWholeData
                            
                        else:
                            aFileNameHead, aFileNameTail    = os.path.split(    aFullFileName)
                            aBaseFileName, aFileNamePostfix = os.path.splitext( aFileNameTail)
                            
                            if not( aFileNamePostfix in someExcludedFilePostfixes):
                                
                                if not ( aFullFileName in someExcludedFullFileNames):
                                
                                    unOtherFileWholeData = self.fZipFileElementContent( unZipFile, aFullFileName)
                                    
                                    unResult[ 'files_whole_data_by_full_name'][ aFullFileName] = unOtherFileWholeData
                                                        
                            
                            
                            
                    
                    
                else:
                    
                    unResult[ 'is_zip'] = False
                    
                        
                    # ##############################################################################
                    """Attempt Parse encoded contents of .xml file as an XML DOM tree, or fail. The values are encoded as specified in the top meta-element of the xml file.
                    
                    """      
                    theUploadedFile.seek( 0)
                    unXMLBuffer = theUploadedFile.objectvalue()
                    
                    try:
                        theUploadedFile.seek( 0)
                        unXMLDocument = gfParseFileAsXMLDocument( theUploadedFile)
                    except:
                        None
                        
                    if  unXMLDocument:
                        
                        unosXMLRootElements = unXMLDocument.childNodes
                        unResult[ 'xml_roots'] = unosXMLRootElements
                        
                        if theAcceptedXMLRootNodeName:
                            
                            if unosXMLRootElements:
                              
                                for anXMLRootElement in unosXMLRootElements:
                                    anXMLRootElementName = anXMLRootElement.nodeName
                                    
                                    if anXMLRootElementName == theAcceptedXMLRootNodeName:
                        
                                        unResult[ 'xml_full_filename'] = '.xml'
                                        unResult[ 'xml_source']        = unXMLBuffer
                                        break
                                    
                        else:
                            
                            unResult[ 'xml_full_filename'] = '.xml'
                            unResult[ 'xml_source']        = unXMLBuffer
                                
                    
                    
                unResult.update( {
                    'success': True,
                })
                
                return unResult
            
            
                    
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fScanXMLAndBinariesFromUploadedFile \n' 
                try:
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                except:
                    None
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   

                    
                unResult.update( { 
                    'success':      False,
                    'status':       cMDDImportStatus_Error_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unResult
                        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fScanXMLAndBinariesFromUploadedFile', theTimeProfilingResults)
            
    
               
  
    
    
    

    
    
    
    

    security.declarePrivate( 'fImport_UploadedFile')
    def fImport_UploadedFile( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool          =None, 
        theContainerObject             =None, 
        theUploadedFile                =None,
        theMinimumTimeSlice            =None,
        theYieldTimePercent            =None, 
        theReuseIdsForTypes            =None,
        theAdditionalParams            =None):
        """Import into an element a zipped archive with XML file, and any included binary content the attached files and images."
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fImport_UploadedFile', theTimeProfilingResults)
                      
        try:
            unImportReport = None
            try:
                
                
                unImportContext   = self.fNewVoidImportContext()
                unImportReport    = unImportContext.get( 'report', {})
                unosImportErrors  = unImportContext.get( 'import_errors', {})
                
                
                # ##############################################################################
                """Check essential parameters.
                
                """
                
                if ( theModelDDvlPloneTool == None):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_ModelDDvlPloneTool,
                    })
                    return unImportReport
                
                unImportContext[ 'ModelDDvlPloneTool'] = theModelDDvlPloneTool
                

                
                if ( theContainerObject == None):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_ContainerObject,
                    })
                    return unImportReport
                
                unImportReport[  'container_object'] = theContainerObject
                unImportContext[ 'container_object'] = theContainerObject
                
                
        
                if not theUploadedFile:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_UploadedFile,
                    })
                    return unImportReport
                
                unImportContext[ 'uploaded_file'] = theUploadedFile
                
                
                
                # ##############################################################################
                """Analyze uploaded file.
                
                """                      
                
                aScanUploadedFileResult = self.fScanXMLAndBinariesFromUploadedFile(
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theContainerObject             =theContainerObject, 
                    theUploadedFile                =theUploadedFile,
                    theAcceptedXMLRootNodeName     =None,
                    theExcludedFullFileNames       =None,
                    theExcludedFilePostfixes       =None,
                    theAdditionalParams            =theAdditionalParams,
                )
                
                if not ( aScanUploadedFileResult and aScanUploadedFileResult.get( 'success', False)):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_ScanningUploadedFile,
                    })
                    return unImportReport                
                
                
                anXMLFullFileName = aScanUploadedFileResult.get( 'xml_full_filename', False)
                
                otherFilesAndData = aScanUploadedFileResult.get( 'files_whole_data_by_full_name', {})
                
                unImportContext[ 'files_and_data'] = otherFilesAndData

                
                unXMLDocument = aScanUploadedFileResult.get( 'xml_document', None)
                if not unXMLDocument:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Parameter_UploadedFile_ZipWithoutXMLFile,
                    })
                    return unImportReport            
                
                unImportContext[ 'xml_document'] = unXMLDocument

                    
                    

                
             
                # ##############################################################################
                """Get roots of the XML DOM tree
                """      
                
                unosXMLRootElements = aScanUploadedFileResult.get( 'xml_roots', [])
                if not unosXMLRootElements:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_NoRootXMLElements,
                        'filename':     anXMLFullFileName,
                    })
                    return unImportReport
                
                unImportContext[ 'xml_roots'] = unosXMLRootElements
                    
                
                

                
                                
                # ##############################################################################
                """Retrieve tools needed for the service.
                
                """
                aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContainerObject)
                if aModelDDvlPloneTool_Retrieval == None:
                    unImportReport.update( {
                        'success':   False,
                        'status':    cMDDImportStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval,
                    })
                    return unImportReport
                
                unImportContext[ 'ModelDDvlPloneTool_Retrieval'] = aModelDDvlPloneTool_Retrieval
                                    
                
                
                aModelDDvlPloneTool_Mutators = theModelDDvlPloneTool.fModelDDvlPloneTool_Mutators( theContainerObject)
                if aModelDDvlPloneTool_Mutators == None:
                    unImportReport.update( {
                        'success':   False,
                        'status':    cMDDImportStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators,
                    })
                    return unImportReport
                                    
                unImportContext[ 'ModelDDvlPloneTool_Mutators'] = aModelDDvlPloneTool_Mutators

                
                
                
                if theAdditionalParams:
                    unImportContext[ 'additional_params'].update( theAdditionalParams)
                
                    
               
                    
                    
                
                                
                # ##############################################################################
                """Check or Retrieve import, plone and mapping configs.
                
                """
                    
                someMDDImportTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeImportConfigs(   theContainerObject)        
                if not someMDDImportTypeConfigs:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Empty_MDDImportTypeConfigs,
                    })
                    return unImportReport
                unImportContext[ 'mdd_type_configs'] = someMDDImportTypeConfigs
        
                

          
                somePloneImportTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeImportConfigs( theContainerObject)        
                if not somePloneImportTypeConfigs:
                    somePloneImportTypeConfigs = {}
                unImportContext[ 'plone_type_configs'] = somePloneImportTypeConfigs
                
                
                
                
                someMappingConfigs         =  aModelDDvlPloneTool_Retrieval.getMappingConfigs( theContainerObject)        
                if not someMappingConfigs:
                    someMappingConfigs = []
                unImportContext[ 'mapping_configs'] = someMappingConfigs
    
                
                
                allImportTypeConfigs = somePloneImportTypeConfigs.copy()
                allImportTypeConfigs.update( theMDDImportTypeConfigs)
                unImportContext[ 'all_copy_type_configs'] = allImportTypeConfigs
                

                
          
                    
                    
                    
                # ##############################################################################
                """Retrieve translation_service tool to handle the input encoding.
                
                """
                aTranslationService = getToolByName( theContainerObject, 'translation_service', None)      
                if not aTranslationService:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Internal_MissingTool_translation_service,
                    })
                    return unImportReport
                unImportContext[ 'translation_service'] = aTranslationService
                
                   
                
                
                
                # ##############################################################################
                """Import according to parameters set in the context.
                
                """
                self.pImport_inner(
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theImportContext               =unImportContext,
                    theMinimumTimeSlice            =theMinimumTimeSlice,
                    theYieldTimePercent            =theYieldTimePercent,
                    theReuseIdsForTypes            =theReuseIdsForTypes,
                )
                                               
                
                    
                return unImportReport        
            
            
           
            except:
                # ##############################################################################
                """Handle exceptions during import preparation.
                
                """      
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fImport_UploadedFile\n' 
                try:
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                except:
                    None
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unImportReport:
                    unImportReport = { }
                    
                unImportReport.update( { 
                    'success':      False,
                    'status':       cMDDImportStatus_Error_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unImportReport
                        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fImport_UploadedFile', theTimeProfilingResults)
            
    
               
            

                
                
                
    
    
    
    
    

    security.declarePrivate( 'fImport_XMLDocumentAndBinaries')
    def fImport_XMLDocumentAndBinaries( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool          =None, 
        theContainerObject             =None, 
        theXMLDocument                 =None,
        theXMLRootElements             =None,
        theFilesAndData                =None,
        theMDDImportTypeConfigs        =None, 
        thePloneImportTypeConfigs      =None, 
        theMappingConfigs              =None, 
        theMinimumTimeSlice            =None,
        theYieldTimePercent            =None,  
        theReuseIdsForTypes            =None,
        theAdditionalParams            =None):
        """Import into an element the content of an XML node tree, and any referenced binary content, like images."
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fImport_XMLDocumentAndBinaries', theTimeProfilingResults)
                      
        try:
            unImportReport = None
            try:
                
                unImportContext   = self.fNewVoidImportContext()
                unImportReport    = unImportContext.get( 'report', {})
                unosImportErrors  = unImportContext.get( 'import_errors', {})
                
                
                # ##############################################################################
                """Check essential parameters.
                
                """
                
                if ( theModelDDvlPloneTool == None):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_ModelDDvlPloneTool,
                    })
                    return unImportReport
                
                unImportContext[ 'ModelDDvlPloneTool'] = theModelDDvlPloneTool
                
                
                
                if ( theContainerObject == None):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_ContainerObject,
                    })
                    return unImportReport
                
                unImportReport[  'container_object'] = theContainerObject
                unImportContext[ 'container_object'] = theContainerObject
        
                
 
                if not theXMLDocument:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_theXMLDocument,
                    })
                    return unImportReport            
                
                unImportContext[ 'xml_document'] = theXMLDocument

                
                
                
                if not theXMLRootElements:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_theXMLRootElements,
                    })
                    return unImportReport            
                
                unImportContext[ 'xml_roots'] = theXMLRootElements

                    
                
                
                if not theMDDImportTypeConfigs:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_MDDImportTypeConfigs,
                    })
                    return unImportReport
                unImportContext[ 'mdd_type_configs'] = theMDDImportTypeConfigs
        
                
                if theFilesAndData:
                    unImportContext[ 'files_and_data'] = theFilesAndData
                
                if theAdditionalParams:
                    unImportContext[ 'additional_params'].update( theAdditionalParams)
                
          
                    
                    
                    
                
                                
                # ##############################################################################
                """Retrieve tools needed for the service.
                
                """
                aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContainerObject)
                if aModelDDvlPloneTool_Retrieval == None:
                    unImportReport.update( {
                        'success':   False,
                        'status':    cMDDImportStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval,
                    })
                    return unImportReport
                
                unImportContext[ 'ModelDDvlPloneTool_Retrieval'] = aModelDDvlPloneTool_Retrieval
                                    
                
                
                aModelDDvlPloneTool_Mutators = theModelDDvlPloneTool.fModelDDvlPloneTool_Mutators( theContainerObject)
                if aModelDDvlPloneTool_Mutators == None:
                    unImportReport.update( {
                        'success':   False,
                        'status':    cMDDImportStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators,
                    })
                    return unImportReport
                                    
                unImportContext[ 'ModelDDvlPloneTool_Mutators'] = aModelDDvlPloneTool_Mutators

                

                
                
                
                
                                
                # ##############################################################################
                """Check or Retrieve plone and mapping configs.
                
                """
               
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
                

                
          
                    
                    
                    
                # ##############################################################################
                """Retrieve translation_service tool to handle the input encoding.
                
                """
                aTranslationService = getToolByName( theContainerObject, 'translation_service', None)      
                if not aTranslationService:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Internal_MissingTool_translation_service,
                    })
                    return unImportReport
                unImportContext[ 'translation_service'] = aTranslationService
                
                   
                
                
                
                # ##############################################################################
                """Import according to parameters set in the context.
                
                """
                self.pImport_inner(
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theImportContext               =unImportContext,
                    theMinimumTimeSlice            =theMinimumTimeSlice,
                    theYieldTimePercent            =theYieldTimePercent,
                    theReuseIdsForTypes            =theReuseIdsForTypes,
                )
                
                
                    
                return unImportReport        
            
            
           
            except:
                # ##############################################################################
                """Handle exceptions during import preparation.
                
                """      
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
                    'status':       cMDDImportStatus_Error_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unImportReport
                        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fImport_XMLDocumentAndBinaries', theTimeProfilingResults)
            
    
               
            



    

    security.declarePrivate( 'pImport_inner')
    def pImport_inner( self,
        theTimeProfilingResults        =None,
        theImportContext               =None,
        theMinimumTimeSlice            =None,
        theYieldTimePercent            =None,
        theReuseIdsForTypes            =None):
        """Import into an element the content of an XML node tree, and any referenced binary content, like images."
        
        """
        
        from ModelDDvlPloneToolSupport               import fPrettyPrint
        from ModelDDvlPloneTool_Transactions         import ModelDDvlPloneTool_Transactions
        from MDDRefactor_Import                      import MDDRefactor_Import

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'pImport_inner', theTimeProfilingResults)
                      
        try:
            unImportReport = None
            try:
                

                
                # ##############################################################################
                """Check essential parameters.
                
                """
                if not theImportContext:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_ImportContext,
                    })
                    return self
                
                
                
                unImportReport    = theImportContext.get( 'report', {})
                unosImportErrors  = theImportContext.get( 'import_errors', {})
                
                
                aContainerObject = theImportContext.get( 'container_object', None)
                if ( aContainerObject == None):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_ContainerObject,
                    })
                    return self
                
                    
        
                anXMLDocument = theImportContext.get( 'xml_document', None)
                if not anXMLDocument:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_theXMLDocument,
                    })
                    return self            
                

                
                someXMLRootElements = theImportContext.get( 'xml_roots', [])
                if not someXMLRootElements:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_theXMLRootElements,
                    })
                    return self            
                
                
                someFilesAndData = theImportContext.get( 'files_and_data', [])
                #if not someFilesAndData:
                    #unImportReport.update( { 
                        #'success':      False,
                        #'status':       cMDDImportStatus_Error_MissingParameter_theXMLRootElements,
                    #})
                    #return self            
                
                someMDDImportTypeConfigs = theImportContext.get( 'mdd_type_configs', {})
                if not someMDDImportTypeConfigs:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_MDDImportTypeConfigs,
                    })
                    return self

                
                somePloneImportTypeConfigs = theImportContext.get( 'plone_type_configs', {})                
                if not somePloneImportTypeConfigs:
                    somePloneImportTypeConfigs = {}
                
                
                someMappingConfigs = theImportContext.get( 'mapping_configs', {})                
                if not someMappingConfigs:
                    someMappingConfigs = []
    
                    
                allImportTypeConfigs = theImportContext.get( 'all_copy_type_configs', {})    
                if not allImportTypeConfigs:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingParameter_MDDImportTypeConfigs,
                    })
                    return self
                    

                
                
                aModelDDvlPloneTool = theImportContext.get( 'ModelDDvlPloneTool', None)                
                if not aModelDDvlPloneTool:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingTool_ModelDDvlPloneTool,
                    })
                    return self
                
                
                aModelDDvlPloneTool_Retrieval = theImportContext.get( 'ModelDDvlPloneTool_Retrieval', None)                
                if not aModelDDvlPloneTool_Retrieval:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval,
                    })
                    return self
                
                aModelDDvlPloneTool_Mutators = theImportContext.get( 'ModelDDvlPloneTool_Mutators', None)                
                if not aModelDDvlPloneTool_Mutators:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators,
                    })
                    return self
                                

                aTranslationService = theImportContext.get( 'translation_service', None)                
                if not aTranslationService:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Internal_MissingTool_translation_service,
                    })
                    return self
                

                someAdditionalParams = theImportContext.get( 'additional_params', {})
                       
                
                
                
                
                # ##############################################################################
                """Build permissions cache instance.
                
                """      
                unCheckedPermissionsCache = aModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                theImportContext[ 'checked_permissions_cache'] = unCheckedPermissionsCache
                

                    
                
                
                # ##############################################################################
                """Transaction Save point before import to get a clean view on the existing object network.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                
                               
                
                # ##############################################################################
                """Retrieve original object result.
                
                """      
                unContainerObjecResult = self.fRetrieveContainer( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theImportContext            =theImportContext,
                )
                
                if (not unContainerObjecResult) or ( unContainerObjecResult.get( 'object', None) == None):
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Internal_NoContainerRetrieved,
                    })
                    return self
                
                theImportContext[ 'container_object_result'] = unContainerObjecResult
        
                
                
                
                
                
                # ##############################################################################
                """Verify import can be performed on target object, and the object is readable and writtable.
                
                """      
                unAllowImport = unContainerObjecResult.get( 'allow_import', True)
                if not unAllowImport:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Import_NotAllowedInElement,
                    })
                    return self
                
                
                
                unContainerReadPermission = unContainerObjecResult.get( 'read_permission', False)
                if not unContainerReadPermission:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Container_NotReadable,
                    })
                    return self
                    
                
                
                unContainerWritePermission = unContainerObjecResult.get( 'write_permission', False)
                if not unContainerWritePermission:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Container_NotWritable,
                    })
                    return self
                
                
                
                
                
                
                 
                # ##############################################################################
                """Instantiate an object network to traverse parsed XML DOM tree and create or update application elements from XML node data.
                
                """      
                unRefactor = MDDRefactor_Import( 
                    aModelDDvlPloneTool,
                    aModelDDvlPloneTool_Retrieval,
                    aModelDDvlPloneTool_Mutators,
                    someFilesAndData,
                    anXMLDocument,
                    someXMLRootElements,
                    aContainerObject, 
                    unContainerObjecResult, 
                    someMDDImportTypeConfigs,
                    somePloneImportTypeConfigs,
                    allImportTypeConfigs, 
                    someMappingConfigs,
                    MDDRefactor_Import_Exception, # theExceptionToRaise,
                    True, # theAllowPartialCopies,
                    True, # theIgnorePartialLinksForMultiplicityOrDifferentOwner
                    theMinimumTimeSlice,
                    theYieldTimePercent, 
                    theReuseIdsForTypes,
                )  
                if ( not unRefactor) or not unRefactor.vInitialized:
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Internal_Refactor_NotInitialized,
                    })
                    return self
                
                
                
                ## ##############################################################################
                #"""Transaction Save point before import to get a clean view on the existing object network.
                
                #"""      
                #ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                                
                
                
                
                # ##############################################################################
                """Actually traverse parsed XML DOM tree and create or update application elements from XML node data.
                
                """      
                unHuboRefactorException  = False
                unHuboException  = False
                unRefactorResult = False
                try:
                    
                    try:
                        unRefactorResult = unRefactor.fRefactor()
                    
                    except MDDRefactor_Import_Exception:
                        # ##############################################################################
                        """Handle exceptions during import loop.
                        
                        """      
                        
                        unHuboRefactorException = True
                        
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                        
                        unInformeExcepcion = 'Exception during ModelDDvlPloneTool_Refactor::pImport_inner invoking MDDRefactor_Import::fRefactor\n' 
                        try:
                            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        except:
                            None
                        try:
                            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        except:
                            None
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        unImportReport[ 'exception'] = unInformeExcepcion
                                 
                        if cLogExceptions:
                            logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                        
                except:
                    unHuboException = True
                    raise
                                
                
                # ##############################################################################
                """Report import statistics.
                
                """      
                unImportReport.update( {
                    'num_elements_imported':       unRefactor.vNumElementsPasted,
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
                    'num_elements_imported_by_type': ( unRefactor.vNumElementsPastedByType or { }).copy(),
                })
                unImportReport[ 'error_reports'].extend( unRefactor.vErrorReports )
                 
                
                ModelDDvlPloneTool_Transactions().fTransaction_Commit()

                if cLogImportResults:
                    logging.getLogger( 'ModelDDvlPlone').info( 'COMMIT: %s::pImport_inner\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unImportReport, ])))
                    
                    
                if ( not unHuboException) and ( not unHuboRefactorException) and unRefactorResult:
    
                    unImportReport.update( { 
                         'success':      True,
                    })
                    if cLogImportResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'COMMITTED COMPLETED: %s::pImport_inner\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unImportReport, ])))
                    
                else:
                    
                    unImportReport.update( { 
                        'success':      False,
                        'status':       cMDDImportStatus_Error_Internal_Refactor_Failed,
                    })
                    
                    if cLogImportResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'COMMITTED WITH ERRORS during: %s::pImport_inner\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unImportReport, ])))
                    
                    
                return self        
            
            
           
            except:
                # ##############################################################################
                """Handle exceptions during parameters check.
                
                """      
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during pImport_inner\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unImportReport:
                    unImportReport = { }
                    
                unImportReport.update( { 
                    'success':      False,
                    'status':       cMDDImportStatus_Error_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return self
                        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pImport_inner', theTimeProfilingResults)
            
    
                
                
                
               
                       
    
    
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

     