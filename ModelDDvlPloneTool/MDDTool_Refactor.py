# -*- coding: utf-8 -*-
#
# File: MDDTool_Refactor.py
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


# Zope
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo

from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation

from time import time

from DateTime import DateTime




from Products.CMFCore                    import permissions
from Products.CMFCore.utils              import getToolByName, UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase




from Acquisition  import aq_inner, aq_parent,aq_get









# #######################################################
# #######################################################









class MDDTool_Refactor:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """

    
    security = ClassSecurityInfo()
    
    
    

    

    
    security.declareProtected( permissions.View, 'fImport_UploadedFile')
    def fImport_UploadedFile(self, 
        theTimeProfilingResults     =None,
        theContainerObject          =None, 
        theUploadedFile             =None,
        theMinimumTimeSlice         =None,
        theYieldTimePercent         =None,
        theAdditionalParams         =None):
        """Import into an element a zipped archive with XML file, and any included binary content the attached files and images."
        
        """
                        
        return self.fModelDDvlPloneTool_Import( theContainerObject).fImport_UploadedFile( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool          =self,
            theContainerObject             =theContainerObject, 
            theUploadedFile                =theUploadedFile,
            theMinimumTimeSlice            =theMinimumTimeSlice,
            theYieldTimePercent            =theYieldTimePercent,
            theAdditionalParams            =theAdditionalParams
        )

      
    
    
    
    
    security.declareProtected( permissions.View, 'fImport_XMLDocumentAndBinaries')
    def fImport_XMLDocumentAndBinaries(self, 
        theTimeProfilingResults     =None,
        theContainerObject             =None, 
        theXMLDocument                 =None,
        theXMLRootElements             =None,
        theFilesAndData                =None,
        theMDDImportTypeConfigs        =None, 
        thePloneImportTypeConfigs      =None, 
        theMappingConfigs              =None, 
        theMinimumTimeSlice            =None,
        theYieldTimePercent            =None,        
        theAdditionalParams            =None):
        """Import into an element a zipped archive with XML file, and any included binary content the attached files and images."
        
        """
                        
        return self.fModelDDvlPloneTool_Import( theContainerObject).fImport_XMLDocumentAndBinaries( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool          =self, 
            theContainerObject             =theContainerObject, 
            theXMLDocument                 =theXMLDocument,
            theXMLRootElements             =theXMLRootElements,
            theFilesAndData                =theFilesAndData,
            theMDDImportTypeConfigs        =theMDDImportTypeConfigs, 
            thePloneImportTypeConfigs      =thePloneImportTypeConfigs, 
            theMappingConfigs              =theMappingConfigs, 
            theMinimumTimeSlice            =theMinimumTimeSlice,
            theYieldTimePercent            =theYieldTimePercent,        
            theAdditionalParams            =theAdditionalParams,
                
        )
        
    

    
    security.declareProtected( permissions.View, 'fImport')
    def fImport(self, 
        theTimeProfilingResults     =None,
        theContainerObject          =None, 
        theUploadedFile             =None,
        theMinimumTimeSlice         =None,
        theYieldTimePercent         =None,
        theAdditionalParams         =None):
        """Import into an element a zipped archive with XML file, and any included binary content the attached files and images."
        
        """
        
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContainerObject)

        someMDDImportTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeImportConfigs(   theContainerObject)        
        somePloneImportTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeImportConfigs( theContainerObject)        
        someMappingConfigs         =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(         theContainerObject)        
                
        return self.fModelDDvlPloneTool_Import( theContainerObject).fImport( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool          =self,
            theModelDDvlPloneTool_Retrieval=aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators =self.fModelDDvlPloneTool_Mutators( theContainerObject),
            theContainerObject             =theContainerObject, 
            theUploadedFile                =theUploadedFile,
            theMDDImportTypeConfigs        =someMDDImportTypeConfigs, 
            thePloneImportTypeConfigs      =somePloneImportTypeConfigs, 
            theMappingConfigs              =someMappingConfigs,
            theMinimumTimeSlice            =theMinimumTimeSlice,
            theYieldTimePercent            =theYieldTimePercent,
            theAdditionalParams            =theAdditionalParams
        )

      
    
 
 

    
    security.declareProtected( permissions.View, 'fScanXMLAndBinariesFromUploadedFile')
    def fScanXMLAndBinariesFromUploadedFile(self, 
        theTimeProfilingResults        =None,
        theContextualElement           =None, 
        theUploadedFile                =None,
        theAcceptedXMLRootNodeName     =None,
        theExcludedFullFileNames       =None,
        theExcludedFilePostfixes       =None,
        theAdditionalParams            =None):
        """Scan the content of the uploaded file, which may be a single XML file, or a zipped archive with an XML file, and some other files."
        
        """
        
        return self.fModelDDvlPloneTool_Import( theContextualElement).fScanXMLAndBinariesFromUploadedFile( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theContextualElement           =theContextualElement, 
            theUploadedFile                =theUploadedFile,
            theAcceptedXMLRootNodeName     =theAcceptedXMLRootNodeName, 
            theExcludedFullFileNames       =theExcludedFullFileNames, 
            theExcludedFilePostfixes       =theExcludedFilePostfixes,
            theAdditionalParams            =theAdditionalParams
        )

      
                
        
        
    
    
    
    
    

        
        

    
    security.declareProtected( permissions.View, 'fObjectPaste')
    # security.declareProtected( permissions.AddPortalContent, 'fObjectPaste')
    def fObjectPaste(self, 
        theTimeProfilingResults     =None,
        theContainerObject          =None, 
        theAdditionalParams         =None):
        
        """Invoked from template MDDPaste, used as an alias to the object_paste action.
        Paste into an element the elements previously copied (references held in the clipboard internet browser cookie), and all its contents, reproducing between the copied elements the relations between the original elements.        
        Cookies have not yet been decoded into objects to paste.
        Preferred to the alternative of fPaste below ( transparently paste from usual plone action), to deliver a detailed report of the paste operation and any possible errors. or objects not pasted.
        
        """
        
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContainerObject)
        
        someMDDCopyTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theContainerObject)        
        somePloneCopyTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theContainerObject)        
        someMappingConfigs       =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(       theContainerObject)        
                
        unPasteReport = self.fModelDDvlPloneTool_Refactor( theContainerObject).fObjectPaste( 
            theTimeProfilingResults        = theTimeProfilingResults,
            theModelDDvlPloneTool          = self,
            theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool_Mutators( theContainerObject),
            theContainerObject             = theContainerObject, 
            theMDDCopyTypeConfigs          = someMDDCopyTypeConfigs, 
            thePloneCopyTypeConfigs        = somePloneCopyTypeConfigs, 
            theMappingConfigs              = someMappingConfigs, 
            theAdditionalParams            = theAdditionalParams
        )
        
        unosImpactedObjectsUIDs = unPasteReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theContainerObject).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerObject, unosImpactedObjectsUIDs)
            
        return unPasteReport
        

    
    
    
    
    
    security.declareProtected( permissions.View, 'fPaste')
    # security.declareProtected( permissions.AddPortalContent, 'fPaste')
    def fPaste(self, 
        theTimeProfilingResults     =None,
        theContainerObject          =None, 
        theObjectsToPaste           =None,
        theIsMoveOperation          =False,
        theAdditionalParams         =None):
        """Delegated from the to-be container element of pasted elements, method pHandle_manage_pasteObjects, invoked by elements manage_pasteObjects.
        Cookes have already been decoded into objects to paste.
        Paste into an element the elements previously copied (references held in the clipboard internet browser cookie), and all its contents, reproducing between the copied elements the relations between the original elements.        
        This allows to transparently paste from usual plone action, but does not deliver a detailed report of the paste operation and any possible errors, or objects not pasted.
        """
        
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContainerObject)
        
        someMDDCopyTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theContainerObject)        
        somePloneCopyTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theContainerObject)        
        someMappingConfigs       =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(       theContainerObject)        
                
        unPasteReport = self.fModelDDvlPloneTool_Refactor( theContainerObject).fPaste( 
            theTimeProfilingResults        = theTimeProfilingResults,
            theModelDDvlPloneTool          = self,
            theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators = self.fModelDDvlPloneTool_Mutators( theContainerObject),
            theContainerObject             = theContainerObject, 
            theObjectsToPaste              = theObjectsToPaste,
            theIsMoveOperation             = theIsMoveOperation,
            theMDDCopyTypeConfigs          = someMDDCopyTypeConfigs, 
            thePloneCopyTypeConfigs        = somePloneCopyTypeConfigs, 
            theMappingConfigs              = someMappingConfigs, 
            theAdditionalParams            = theAdditionalParams
        )
        
        unosImpactedObjectsUIDs = unPasteReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theElement, unosImpactedObjectsUIDs)
            
        return unPasteReport
        

    
    
    

    
    
    
    
        