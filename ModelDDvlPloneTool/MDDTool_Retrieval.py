# -*- coding: utf-8 -*-
#
# File: MDDTool_Retrieval.py
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









class MDDTool_Retrieval:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """
    
    
    security = ClassSecurityInfo()

        
    
        
    
    # ######################################
    """Traversal configuration retrieval methods.
    
    """
    
    security.declareProtected( permissions.View, 'getAllTypeConfigs')
    def getAllTypeConfigs(self, theContextualObject):
        
        return self.fModelDDvlPloneTool_Retrieval( theContextualObject).getAllTypeConfigs( theContextualObject)
    
    
     
    
    
    
        
        
    
        
    
    # ######################################
    """Retrieve elements data by Traversal according to traversal configuration.
    
    """
    
    security.declareProtected( permissions.View, 'fRetrieveTypeConfig')
    def fRetrieveTypeConfig(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theParent                   =None,
        theParentTraversalName      ='',
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='', 
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):
        """Retrieval of an element result, for a given element.
        
        """

            
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theElement)
                
        unElementResult =  aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theElement                  =theElement, 
            theParent                   =theParent,
            theParentTraversalName      =theParentTraversalName,
            theTypeConfig               =theTypeConfig, 
            theAllTypeConfigs           =theAllTypeConfigs, 
            theViewName                 =theViewName, 
            theRetrievalExtents         =theRetrievalExtents,
            theWritePermissions         =theWritePermissions,
            theFeatureFilters           =theFeatureFilters, 
            theInstanceFilters          =theInstanceFilters,
            theTranslationsCaches       =theTranslationsCaches,
            theCheckedPermissionsCache  =theCheckedPermissionsCache,
            theAdditionalParams         =theAdditionalParams
        )
        
        if not unElementResult:
            return unElementResult
        
        aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)
        
        return unElementResult


    
    
    

    

    security.declareProtected( permissions.View, 'fRetrieveTypeConfigByUID')
    def fRetrieveTypeConfigByUID(self, 
        theTimeProfilingResults     =None,
        theContextualElement        =None, 
        theUID                      =None, 
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='', 
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):
        """Retrieval of element results, for an element given its UID (unique identifier in the scope of the Plone site).
        
        """
                
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContextualElement)
                
        unElementResult =  aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfigByUID( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theContextualElement        =theContextualElement, 
            theUID                      =theUID, 
            theTypeConfig               =theTypeConfig, 
            theAllTypeConfigs           =theAllTypeConfigs, 
            theViewName                 =theViewName, 
            theRetrievalExtents         =theRetrievalExtents,
            theWritePermissions         =theWritePermissions,
            theFeatureFilters           =theFeatureFilters, 
            theInstanceFilters          =theInstanceFilters,
            theTranslationsCaches       =theTranslationsCaches,
            theCheckedPermissionsCache  =theCheckedPermissionsCache,
            theAdditionalParams         =theAdditionalParams
        )

        if not unElementResult:
            return unElementResult
        
        aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)

        return unElementResult

    
    
  
    
    
    
    
    

    security.declareProtected( permissions.View, 'fNewResultForElement')
    def fNewResultForElement(self,  theElement=None, theResult=None):
        """Retrieve a result structure for an element, initialized with just the most important information and attributes.
        
        """
        
        return self.fModelDDvlPloneTool_Retrieval( theElement).fNewResultForElement( theElement, theResult)
    
    
    

    
    
    
    

    security.declareProtected( permissions.View, 'fRetrieveElementoBasicInfoAndTranslations')
    def fRetrieveElementoBasicInfoAndTranslations(self, 
        theTimeProfilingResults     =None,
        theContainerElement         =None, 
        thePloneSubItemsParameters  =None, 
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):
        """Retrieve a result structure for an element, initialized with just the most important information and attributes.
        
        """
        
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContainerElement)

        unElementResult =  aModelDDvlPloneTool_Retrieval.fRetrieveElementoBasicInfoAndTranslations( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theContainerElement         =theContainerElement, 
            thePloneSubItemsParameters  =thePloneSubItemsParameters, 
            theRetrievalExtents         =theRetrievalExtents,
            theWritePermissions         =theWritePermissions,
            theFeatureFilters           =theFeatureFilters, 
            theInstanceFilters          =theInstanceFilters,
            theTranslationsCaches       =theTranslationsCaches,
            theCheckedPermissionsCache  =theCheckedPermissionsCache,
            theAdditionalParams         =theAdditionalParams
        )
        if not unElementResult:
            return unElementResult
        
        aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)

        return unElementResult




    
    
    
    
    
    security.declareProtected( permissions.View, 'fRetrievePloneContent')
    def fRetrievePloneContent(self, 
        theTimeProfilingResults     =None,
        theContainerElement         =None, 
        thePloneSubItemsParameters  =None, 
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):
        """Retrieve a result structure for an element of a standard Plone archetype (ATLink, ATDocument, ATImage, ATNewsItem).
        
        """

        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContainerElement)

        unElementResult =  aModelDDvlPloneTool_Retrieval.fRetrievePloneContent( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theContainerElement         =theContainerElement, 
            thePloneSubItemsParameters  =thePloneSubItemsParameters, 
            theRetrievalExtents         =theRetrievalExtents,
            theWritePermissions         =theWritePermissions,
            theFeatureFilters           =theFeatureFilters, 
            theInstanceFilters          =theInstanceFilters,
            theTranslationsCaches       =theTranslationsCaches,
            theCheckedPermissionsCache  =theCheckedPermissionsCache,
            theAdditionalParams         =theAdditionalParams
        )
    
        if not unElementResult:
            return unElementResult
        
        aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)

        return unElementResult

    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fRetrieveElementsOfType')
    def fRetrieveElementsOfType(self, 
        theTimeProfilingResults     =None,
        theElement                  =None,
        theTypeNames                =None,
        theAllTypeConfigs           =None, 
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None, 
        theAdditionalParams         =None):
        """Retrieve result structures for all elements of a Type in a Plone site.
        
        """
        
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContextualObject)
        
        unTraversalResult = aModelDDvlPloneTool_Retrieval.fRetrieveElementsOfType( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theElement                  =theElement,
            theTypeNames                =theTypeNames,
            theAllTypeConfigs           =theAllTypeConfigs, 
            theTranslationsCaches       =theTranslationsCaches, 
            theCheckedPermissionsCache  =theCheckedPermissionsCache, 
            theWritePermissions         =theWritePermissions, 
            theAdditionalParams         =theAdditionalParams
        )
        
        if not unTraversalResult:
            return unTraversalResult
        
        unosElementsResults = unTraversalResult.get( 'elements', [])
        if not unosElementsResults:
            return unTraversalResult
         
        for unElementResult in unosElementsResults:
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)
            
        return unTraversalResult
    
        
        

   
    

    
    
    
    
                                
    security.declareProtected( permissions.View, 'fDefaultPloneSubItemsParameters')
    def fDefaultPloneSubItemsParameters(self, theContextualObject):
        return self.fModelDDvlPloneTool_Retrieval( theContextualObject).fDefaultPloneSubItemsParameters()
    
   
    
    
    
   
    security.declareProtected( permissions.View, 'fGetMemberInfoForUserId')
    def fGetMemberInfoForUserId(self, theContextualObject, theUserId):
        return self.fModelDDvlPloneTool_Retrieval( theContextualObject).fGetMemberInfoForUserId( theContextualObject, theUserId)
    
       
    

 
    
    
    


    
    # ######################################
    """Preferences Retrieval methods.
    Not yet implemented. Pending.
    
    """

    
    security.declareProtected( permissions.View, 'fRetrievePreferences')
    def fRetrievePreferences(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='', 
        thePreferencesExtents       =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):
        """Retrieval of presentation preferences for the user at the element. Temporary (in http cookie), or persisted in an element in the user folder. Defaulting to preferences in container elements, if any specified for the user, or for all users, and ultimately in the preferences of the model root element, for the user, or for all the users.
        
        """
        return {}
        #if (not thePreferencesExtents) or ( not thePreferencesExtents[ 0]):
            #return self.fGetAllPreferencesCopy( theContextualObject, thePreferencesExtents[ 0])

        #return self.fGetPreferencesCopy( theContextualObject, thePreferencesExtents[ 0])
    
    
        
        
        
            