# -*- coding: utf-8 -*-
#
# File: MDDTool_Versions.py
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









class MDDTool_Versions:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """
    

    security = ClassSecurityInfo()
    
    
        
    # #############################################################
    """Version retrieval and management methods.
    
    """

        
    
    
    
    security.declareProtected( permissions.View, 'fRetrieveAllVersions')
    def fRetrieveAllVersions(self, 
        theTimeProfilingResults     =None,
        theVersionedElement          =None, 
        theAdditionalParams         =None):
        """Retrieve all versions of a model root, classified as the direct previous and next versions, and all others recursively previous and next versions."
        
        """
   
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theVersionedElement)
        aModelDDvlPloneTool_Version   = self.fModelDDvlPloneTool_Version( theVersionedElement)
        
                
        unAllVersionsReport =  aModelDDvlPloneTool_Version.fRetrieveAllVersions( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool_Retrieval=aModelDDvlPloneTool_Retrieval,
            theVersionedElement            =theVersionedElement,
            theAllVersionsReport           =None,
            theAdditionalParams            =theAdditionalParams
        )


        if not unAllVersionsReport:
            return {}
        
        unVersionedElementResult = unAllVersionsReport.get( 'versioned_element_result', None)
        if unVersionedElementResult:
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unVersionedElementResult)
        
        return unAllVersionsReport

    
    
    
    
    

   
    security.declareProtected( permissions.View, 'fRetrieveAllVersionsWithContainerPloneSiteAndClipboard')
    def fRetrieveAllVersionsWithContainerPloneSiteAndClipboard(self, 
        theTimeProfilingResults     =None,
        theVersionedElement          =None, 
        theAdditionalParams         =None):
        """Retrieve all versions of a model root, classified as the direct previous and next versions, and all others recursively previous and next versions."
        
        """
   
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theVersionedElement)
        aModelDDvlPloneTool_Version   = self.fModelDDvlPloneTool_Version(   theVersionedElement)
        
                
        unAllVersionsReport =  aModelDDvlPloneTool_Version.fRetrieveAllVersionsWithContainerPloneSiteAndClipboard( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool_Retrieval=aModelDDvlPloneTool_Retrieval,
            theVersionedElement            =theVersionedElement, 
            theAdditionalParams            =theAdditionalParams
        )


        if not unAllVersionsReport:
            return {}
        
        unVersionedElementResult = unAllVersionsReport.get( 'versioned_element_result', None)
        if unVersionedElementResult:
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unVersionedElementResult)
        
        return unAllVersionsReport

        
    
    
    
    
    
    security.declareProtected( permissions.View, 'fNewVersion')
    def fNewVersion(self, 
        theTimeProfilingResults     =None,
        theOriginalObject           =None, 
        theNewVersionContainerKind  =None,
        theNewVersionName           =None,
        theNewVersionComment        =None,
        theNewTitle                 =None,
        theNewId                    =None,
        theAdditionalParams         =None):
        """Create a new version of the original object which shall be a root, with the new version name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """
                
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theOriginalObject)

        someMDDNewVersionTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theOriginalObject)        
        somePloneNewVersionTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theOriginalObject)        
                
        return self.fModelDDvlPloneTool_Version( theOriginalObject).fNewVersion( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool          =self,
            theModelDDvlPloneTool_Retrieval=aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators =self.fModelDDvlPloneTool_Mutators( theOriginalObject),
            theOriginalObject              =theOriginalObject, 
            theNewVersionContainerKind     =theNewVersionContainerKind,
            theNewVersionName              =theNewVersionName,
            theNewVersionComment           =theNewVersionComment,
            theNewTitle                    =theNewTitle,
            theNewId                       =theNewId,
            theMDDNewVersionTypeConfigs    =someMDDNewVersionTypeConfigs, 
            thePloneNewVersionTypeConfigs  =somePloneNewVersionTypeConfigs, 
            theAdditionalParams            =theAdditionalParams
        )


   

    

        
