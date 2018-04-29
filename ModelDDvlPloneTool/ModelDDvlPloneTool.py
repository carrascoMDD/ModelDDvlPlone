# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool.py
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

import threading

# Zope
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo


from time import time

from DateTime import DateTime




# cmf
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName, UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase

#from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService

#from Products.PlacelessTranslationService.Negotiator import Negotiator
from Products.PlacelessTranslationService.Negotiator import getLangPrefs

from Acquisition  import aq_inner, aq_parent


from ModelDDvlPloneTool_Export      import ModelDDvlPloneTool_Export
from ModelDDvlPloneTool_Import      import ModelDDvlPloneTool_Import
from ModelDDvlPloneTool_Retrieval   import ModelDDvlPloneTool_Retrieval
from ModelDDvlPloneTool_Bodies      import ModelDDvlPloneTool_Bodies                
from ModelDDvlPloneTool_Mutators    import ModelDDvlPloneTool_Mutators   
from ModelDDvlPloneTool_Refactor    import ModelDDvlPloneTool_Refactor
from ModelDDvlPloneTool_Version     import ModelDDvlPloneTool_Version
from ModelDDvlPloneTool_Cache       import ModelDDvlPloneTool_Cache

from ModelDDvlPloneTool_Cache       import cCacheEnabled_Default,              cLockOnceOrTwice_Default
from ModelDDvlPloneTool_Cache       import cMaxCharsCachedForElements_Default, cDisplayCacheHitInformation_Default
from ModelDDvlPloneTool_Cache       import cUnsecureCacheFlushAcknowledgedAuthenticationString





    
cSecondsToReviewAndDelete_Minumum = 10
cSecondsToReviewAndDelete_Default = max( 60, cSecondsToReviewAndDelete_Minumum)






cModelDDvlPloneToolName = 'ModelDDvlPlone_tool'

cDefaultNombreProyecto  = 'a_ModelDDvlPlone_driven_ProjectName'




cRoleKind_Anonymous     = 'Anonymous'
cRoleKind_Authenticated = 'Authenticated'
cRoleKind_Member        = 'Member'
cRoleKind_Owner         = 'Owner'
cRoleKind_Manager       = 'Manager'


cNoRelationCursorName = '-NoRelationCursorName-'
cNoCurrentElementUID  = '-NoCurrentElementUID-'


"""Tool permissions to be set upon instantiation of the tool,  not restricting the access of anonymous users.

"""         
cModelDDvlPloneToolPermissions = [                                                                                                                                     
    { 'permission': permissions.AddPortalContent,     'acquire': False,  'roles': [              'Authenticated',  ], },  
    { 'permission': permissions.DeleteObjects,        'acquire': False,  'roles': [              'Authenticated',  ], },  
    { 'permission': permissions.ModifyPortalContent,  'acquire': False,  'roles': [              'Authenticated',  ], },  
    { 'permission': permissions.View,                 'acquire': False,  'roles': [ 'Anonymous', 'Authenticated',  ], },  
]




class ModelDDvlPloneTool(UniqueObject, PropertyManager, SimpleItem.SimpleItem, ActionProviderBase):
    """Facade object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations.
    
    """
    
    "The ModelDDvlPloneTool"

    meta_type = 'ModelDDvlPloneTool'

    id = cModelDDvlPloneToolName

    manage_options = PropertyManager.manage_options + \
                     SimpleItem.SimpleItem.manage_options + (
    	{'label': 'View', 'action': 'index_html',},
    )

    _properties = (
        {'id':'title', 'type':'string', 'mode':'w'},
    )

    # Standard security settings
    security = ClassSecurityInfo()


    security.declareProtected('Manage properties', 'index_html')
    index_html = PageTemplateFile('skins/index_html', globals())

    
    def __init__( self):
        """Instantiation and initialization.
        
        """
        
        # #######################################################
        """Cache and cache control
        
        """
        self.vCacheEnabled               = cCacheEnabled_Default
        self.vMaxCharsCachedForElements  = cMaxCharsCachedForElements_Default
        self.vLockOnceOrTwice            = cLockOnceOrTwice_Default
        self.vDisplayCacheHitInformation = cDisplayCacheHitInformation_Default
        self.vSecondsToReviewAndDelete   = cSecondsToReviewAndDelete_Default
    
            
 
        

    security.declarePrivate( 'fSecondsToReviewAndDelete')
    def fSecondsToReviewAndDelete( self, theContextualElement):
        
        if self.vSecondsToReviewAndDelete > cSecondsToReviewAndDelete_Minumum:
            return self.vSecondsToReviewAndDelete
            
        return cSecondsToReviewAndDelete_Default
    
        
        
    security.declarePrivate( 'fCacheFlushAcknowledgedAuthenticationString')
    def fCacheFlushAcknowledgedAuthenticationString(self,):
        return cUnsecureCacheFlushAcknowledgedAuthenticationString
        
        
        
    #"""Trying to find wich superclasses instance intialiation methods to delegate into.
    
    #"""
    
    #"""
    #UniqueObject: __init__ method in object supertype (which just pass)
    #PropertyManager: __init__ method in ExtensionClass supertype (which just pass)
    
    #Can not find up the inheritance chain any __init__ method worth to delegate to
    
    
    #x: __init__ method in itself or its superclasses
    
        #"""

        


    # ACV 20090325 Learned from tools generation by ArchGenXML
    #    # tool-constructors have no id argument, the id is fixed
    #    def __init__(self, id=None):
    #        BaseContent.__init__(self,'TRAtool_gvSIGtraducciones')
    #        self.setTitle('Catalogo de Traducciones')
    #        
    #        ##code-section constructor-footer #fill in your manual code here
    #        ##/code-section constructor-footer
    
    
    # ACV 20090325 Learned from tools generation by ArchGenXML
    #    # tool should not appear in portal_catalog
    #    def at_post_edit_script(self):
    #        self.unindexObject()
    #        
    #        ##code-section post-edit-method-footer #fill in your manual code here
    #        ##/code-section post-edit-method-footer




    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """Lazy Initialization of the tool.
        
        """        
        self.pSetPermissions()
                
        return self
    


    


    # #############################################################
    """Security configuration utility 
    
    """

    
    security.declarePrivate( 'pSetPermissions')
    def pSetPermissions(self):
        """Set tool permissions upon instantiation of the tool, according to a specification ( usually not restricting the access of anonymous users).
        
        """         
        for unaPermissionSpec in cModelDDvlPloneToolPermissions:
            unaPermission = unaPermissionSpec[ 'permission']
            unAcquire     = unaPermissionSpec[ 'acquire'] 
            unosRoles     = unaPermissionSpec[ 'roles']
            
            if unaPermission:
                self.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
        
        return self
    

 
    # ######################################
    """Time methods.
    
    """

   
    security.declareProtected( permissions.View, 'fSecondsNow')
    def fSecondsNow(self):   

        return int( time())
    
   
        
    security.declareProtected( permissions.View, 'fMillisecondsNow')
    def fMillisecondsNow(self):   

        return int( time() * 1000)
   
    
    
    security.declareProtected( permissions.View, 'fDateTimeNow')
    def fDateTimeNow(self):   
        return DateTime()
    
    
    
    
        
      
    
    
    # ######################################
    """Retrieval methods.
    
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
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
                
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
                
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
                
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
        """Retrieve a result structure for an element, initialized with the most important information and attributes.
        
        """
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()

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

        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()

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
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        
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
    def fDefaultPloneSubItemsParameters(self):
        return ModelDDvlPloneTool_Retrieval().fDefaultPloneSubItemsParameters()
    
   
   
    
    


    security.declareProtected( permissions.View, 'fDeleteImpactReport')
    def fDeleteImpactReport(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a report of the impact of deleting an element, including all elements that will be related (contained elements) and elements that will be affected (related elements).
        
        """
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        unDeleteImpactReport =  aModelDDvlPloneTool_Retrieval.fDeleteImpactReport( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement,
            theAdditionalParams     =theAdditionalParams 
        )
        
        if not unDeleteImpactReport:
            return unDeleteImpactReport
        
        self.pBuildResultDictsForImpactReport( aModelDDvlPloneTool_Retrieval, unDeleteImpactReport)
                 
        return unDeleteImpactReport
        
        
    


    security.declareProtected( permissions.View, 'fDeleteImpactReport')
    def fDeleteManyImpactReports(self, 
        theTimeProfilingResults =None,
        theContainerElement     =None,
        theGroupUIDs            =[],
        theAdditionalParams     =None):
        """Retrieve a report of the impact of deleting an element, including all elements that will be related (contained elements) and elements that will be affected (related elements).
        
        """
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        
        unDeleteManyImpactReports =  aModelDDvlPloneTool_Retrieval.fDeleteManyImpactReports( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement,
            theGroupUIDs            =theGroupUIDs,
            theAdditionalParams     =theAdditionalParams 
        )
        
        if not unDeleteManyImpactReports:
            return unDeleteManyImpactReports
        
        unContainerElementResult = unDeleteManyImpactReports.get( 'container_result', None)
        if unContainerElementResult:
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unContainerElementResult)
            
        someImpactReports = unDeleteManyImpactReports[ 'impact_reports']
        for anImpactReport in someImpactReports:
            self.pBuildResultDictsForImpactReport( aModelDDvlPloneTool_Retrieval, anImpactReport)
                 
        return unDeleteManyImpactReports
        
    
    
            
    def pBuildResultDictsForImpactReport( self, theModelDDvlPloneTool_Retrieval, theImpactReport):
        if not theImpactReport:
            return self
        
        unElementResult =  theImpactReport.get( 'here', {})
        if unElementResult:        
            theModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)
        
        unosPloneImpactResults = theImpactReport.get( 'plone', [])
        for unPloneImpactResult in unosPloneImpactResults:
            unPloneResult = unPloneImpactResult.get( 'here', {}) 
            if unPloneResult:
                theModelDDvlPloneTool_Retrieval.pBuildResultDicts( unPloneResult)
 
        unosRelatedResults = theImpactReport.get( 'related', [])
        for unRelatedResult in unosRelatedResults:
            theModelDDvlPloneTool_Retrieval.pBuildResultDicts( unRelatedResult)
                
        unosIncludedImpactReports = theImpactReport.get( 'included', [])
        for unIncludedImpactReport in unosIncludedImpactReports:
            self.pBuildResultDictsForImpactReport( theModelDDvlPloneTool_Retrieval, unIncludedImpactReport)

        return self
    
    
        
    
    
    
    
    
    
    # ####################################################
    """Rest (ReStructuredText) reporting methods.
    
    """

    
    
    
    security.declarePublic( 'fCookedBodyForElement')
    def fCookedBodyForElement(self, 
        theTimeProfilingResults =None,
        theElement              =None, 
        stx_level               =None, 
        setlevel                =0,
        theAdditionalParams     =None):
        """Retrieve an HTML presentation of an element's content as a Textual view.
        
        """
        
        return ModelDDvlPloneTool_Bodies().fCookedBodyForElement( 
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement, 
            stx_level               =stx_level, 
            setlevel                =setlevel,
            theAdditionalParams     =theAdditionalParams)
    

    
    
    
    
    security.declarePublic( 'fEditableBodyForElement')
    def fEditableBodyForElement(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a REST presentation of an element's content as a Textual view.
        
        """
        
        return ModelDDvlPloneTool_Bodies().fEditableBodyForElement( 
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement,
            theAdditionalParams     =theAdditionalParams
        )
    

    

    
    security.declarePublic( 'fEditableBodyBlock_MetaTypeIcons')
    def fEditableBodyBlock_MetaTypeIcons(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a REST presentation of an element's content as a Textual view.
        
        """
        
        return ModelDDvlPloneTool_Bodies().fEditableBodyBlock_MetaTypeIcons( 
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement,
            theAdditionalParams     =theAdditionalParams
        )
    
    
    
    
    
    
    
    
    
    
    # ####################################################
    """Change element methods.
    
    """
                
    
    
    
    security.declareProtected( permissions.AddPortalContent,  'fCrearElementoDeTipo')
    def fCrearElementoDeTipo(self, 
        theTimeProfilingResults =None,
        theContainerElement      =None, 
        theTypeName             ='', 
        theId                   =None,
        theTitle                ='', 
        theDescription          ='',
        theAdditionalParams     =None,
        theAllowFactoryMethods  =False,):           
        """Create a new contained element of a type.
        
        """
        
        aCreationReport = ModelDDvlPloneTool_Mutators().fCrearElementoDeTipo( 
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement, 
            theTypeName             =theTypeName, 
            theId                   =theId,
            theTitle                =theTitle, 
            theDescription          =theDescription,
            theAdditionalParams     =theAdditionalParams,
            theAllowFactoryMethods  =theAllowFactoryMethods,
        )
        if not aCreationReport:
            return aCreationReport
        
        unNewElementResult = aCreationReport.get( 'new_object_result', None)
        if not unNewElementResult:
            return aCreationReport
        
        unNewElementUID = unNewElementResult.get( 'UID', '')
        if not unNewElementUID:
            return aCreationReport
        
        ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theContainerElement, [ unNewElementUID],)
            
        return aCreationReport
            
        
        
        
    
    
    
   
    # ACV OJO 20090917 Seems unused
    security.declareProtected( permissions.AddPortalContent,  'fCrearElementoDeTipoEspecial')
    def fCrearElementoDeTipoEspecial(self, 
        theTimeProfilingResults =None,
        theContainerElement     =None, 
        theId                   =None,
        theTypeName             ='', 
        theTitle                ='', 
        theDescription          ='',
        theAdditionalParams     =None):           
        """Create a new contained element of an special type type.
        
        """
        
        aCreationReport = ModelDDvlPloneTool_Mutators().fCrearElementoDeTipo( 
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement, 
            theTypeName             =theTypeName, 
            theId                   =theId,
            theTitle                =theTitle, 
            theDescription          =theDescription,
            theAdditionalParams     =theAdditionalParams
        )
        if not aCreationReport:
            return aCreationReport
        
        unNewElementResult = aCreationReport.get( 'new_object_result', None)
        if not unNewElementResult:
            return aCreationReport
        
        unNewElementUID = unNewElementResult.get( 'UID', '')
        if not unNewElementUID:
            return aCreationReport
        
        ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theContainerElement, [ unNewElementUID],)
            
        return aCreationReport
            
        
        
                    
    
    
        
    security.declareProtected(  permissions.ModifyPortalContent, 'fChangeValues')
    def fChangeValues(self, 
        theTimeProfilingResults =None,
        theElement              =None, 
        theNewValuesDict        =None,
        theAdditionalParams     =None):        
        """Apply changes to an element's attributes values.
        
        """
        
        unChangeReport = ModelDDvlPloneTool_Mutators().fChangeValues(  
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement, 
            theNewValuesDict        =theNewValuesDict,
            theAdditionalParams     =theAdditionalParams
        )
        if not unChangeReport:
            return unChangeReport
        
        unosImpactedObjectsUIDs = unChangeReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theElement, unosImpactedObjectsUIDs)
            
        return unChangeReport
        
        
    
    
    security.declareProtected( permissions.ModifyPortalContent, 'fMoveSubObject')
    def fMoveSubObject(self, 
        theTimeProfilingResults =None,
        theContainerElement      =None,  
        theTraversalName        =None, 
        theMovedObjectId        =None, 
        theMoveDirection        =None, 
        theAdditionalParams     =None):        
        """Change the order index of an element in the collection of elements aggregated in its container.
        
        """
        
        unMoveReport = ModelDDvlPloneTool_Mutators().fMoveSubObject( 
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement      =theContainerElement,  
            theTraversalName        =theTraversalName, 
            theMovedObjectId        =theMovedObjectId, 
            theMoveDirection        =theMoveDirection, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unMoveReport:
            return unMoveReport
        
        unosImpactedObjectsUIDs = unMoveReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return unMoveReport
                
        
        
    
           
    security.declareProtected( permissions.ModifyPortalContent, 'fMoveReferencedObject')
    def fMoveReferencedObject(self,
        theTimeProfilingResults =None,
        theSourceElement        =None,  
        theReferenceFieldName   =None, 
        theMovedReferenceUID    =None, 
        theMoveDirection        =None,
        theAdditionalParams     =None):        
        """Change the order index of an element in the collection of related elements.
        
        """
        
        unMoveReport = ModelDDvlPloneTool_Mutators().fMoveReferencedObject(
            theTimeProfilingResults =theTimeProfilingResults,
            theSourceElement        =theSourceElement,  
            theReferenceFieldName   =theReferenceFieldName, 
            theMovedReferenceUID    =theMovedReferenceUID, 
            theMoveDirection        =theMoveDirection, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unMoveReport:
            return unMoveReport
        
        unosImpactedObjectsUIDs = unMoveReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theSourceElement, unosImpactedObjectsUIDs)
            
        return unMoveReport
                  
    
    
 
    
    
     
    security.declareProtected(  permissions.ModifyPortalContent, 'fLinkToUIDReferenceFieldNamed')
    def fLinkToUIDReferenceFieldNamed(self, 
        theTimeProfilingResults =None,
        theSourceElement        =None, 
        theReferenceFieldName   =None, 
        theTargetUID            =None,
        theAdditionalParams     =None):        
        """Link an element as related to another element.
        
        """
        
        unLinkReport = ModelDDvlPloneTool_Mutators().fLinkToUIDReferenceFieldNamed( 
            theTimeProfilingResults =theTimeProfilingResults,            
            theSourceElement        =theSourceElement, 
            theReferenceFieldName   =theReferenceFieldName, 
            theTargetUID            =theTargetUID, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unLinkReport:
            return unLinkReport
        
        unosImpactedObjectsUIDs = unLinkReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theSourceElement, unosImpactedObjectsUIDs)
            
        return unLinkReport
        
       
    
        
    
    security.declareProtected(  permissions.ModifyPortalContent, 'fUnlinkFromUIDReferenceFieldNamed')
    def fUnlinkFromUIDReferenceFieldNamed(self, 
        theTimeProfilingResults =None,
        theSourceElement        =None, 
        theReferenceFieldName   =None, 
        theTargetUID            =None,
        theAdditionalParams     =None):        
        """Unink an element from another related element.
        
        """

        unUnlinkReport = ModelDDvlPloneTool_Mutators().fUnlinkFromUIDReferenceFieldNamed( 
            theTimeProfilingResults =theTimeProfilingResults,            
            theSourceElement        =theSourceElement, 
            theReferenceFieldName   =theReferenceFieldName, 
            theTargetUID            =theTargetUID, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unUnlinkReport:
            return unUnlinkReport
        
        unosImpactedObjectsUIDs = unUnlinkReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theSourceElement, unosImpactedObjectsUIDs)
            
        return unUnlinkReport
        
        
        
    
    
    
    security.declareProtected( permissions.DeleteObjects,  'fEliminarElemento')
    def fEliminarElemento(self, 
        theTimeProfilingResults =None,                          
        theElement              =None, 
        theIdToDelete           =None, 
        theUIDToDelete          =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete an element and all its contents.
        
        """

        unDeleteReport = ModelDDvlPloneTool_Mutators().fEliminarElemento( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement,            
            theIdToDelete           =theIdToDelete, 
            theUIDToDelete          =theUIDToDelete, 
            theRequestSeconds       =theRequestSeconds, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unDeleteReport:
            return unDeleteReport
        
        unosImpactedObjectsUIDs = unDeleteReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theElement, unosImpactedObjectsUIDs)
            
        return unDeleteReport
        
    
              

    
    security.declareProtected( permissions.DeleteObjects,  'fEliminarVariosElementos')
    def fEliminarVariosElementos(self, 
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,                          
        theContainerElement     =None, 
        theIdsToDelete          =None, 
        theUIDsToDelete         =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete an element and all its contents.
        
        """

        unDeleteManyReport = ModelDDvlPloneTool_Mutators().fEliminarVariosElementos( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement,            
            theIdsToDelete          =theIdsToDelete, 
            theUIDsToDelete         =theUIDsToDelete, 
            theRequestSeconds       =theRequestSeconds, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unDeleteManyReport:
            return unDeleteManyReport
        
        unosImpactedObjectsUIDs = unDeleteManyReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theElement, unosImpactedObjectsUIDs)
            
        return unDeleteReport
    
                
    
        
    
    
    
    
    
    
    
    # ####################################################
    """Change Plone methods.
    
    """
                
                
    
    
    security.declareProtected( permissions.DeleteObjects,  'fEliminarElementoPlone')
    def fEliminarElementoPlone(self, 
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,                          
        theContainerElement     =None, 
        theUIDToDelete          =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete an element of an standard Plone archetype (ATLink, ATDocument, ATImage, ATNewsItem).
        
        """

        unDeleteReport = ModelDDvlPloneTool_Mutators().fEliminarElementoPlone( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults, 
            theContainerElement     =theContainerElement,
            theUIDToDelete          =theUIDToDelete, 
            theRequestSeconds       =theRequestSeconds, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unDeleteReport:
            return unDeleteReport
        
        unosImpactedObjectsUIDs = unDeleteReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theElement, unosImpactedObjectsUIDs)
            
        return unDeleteReport

            
    
    
    
    security.declareProtected( permissions.ModifyPortalContent, 'fMoveSubObjectPlone')
    def fMoveSubObjectPlone(self, 
        theTimeProfilingResults =None,                          
        theContainerElement     =None,  
        theTraversalName        ='', 
        theMovedObjectUID       =None, 
        theMoveDirection        ='', 
        theAdditionalParams     =None):        
        """Change the order index of an element of an standard Plone archetype (ATLink, ATDocument, ATImage, ATNewsItem) in the collection of elements aggregated in its container.
        
        """

        unMoveReport = ModelDDvlPloneTool_Mutators().fMoveSubObjectPlone( 
            theTimeProfilingResults =theTimeProfilingResults,            
            theContainerElement      =theContainerElement,  
            theTraversalName        =theTraversalName, 
            theMovedObjectUID       =theMovedObjectUID, 
            theMoveDirection        =theMoveDirection, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unMoveReport:
            return unMoveReport
        
        unosImpactedObjectsUIDs = unMoveReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theSourceElement, unosImpactedObjectsUIDs)
            
        return unMoveReport
                  
    
    
    
    
    
                

    # ####################################################
    """Display view maintenance methods.
    
    """

               
                   

    security.declareProtected( permissions.View,  'pSetDefaultDisplayView')
    def pSetDefaultDisplayView(self, theElement):  
        """Set to its default the view that will be presented for an element, when no view is specified. Usually one of Textual or Tabular.
        
        """
    
        if not ModelDDvlPloneTool_Retrieval().fCheckElementPermission( theElement, [ permissions.ModifyPortalContent ], None):
            return self
            
        unaDefaultView = ''
        try:
            unaDefaultView = theElement.default_view
        except:
            None
        
        if unaDefaultView:
            self.pSetAsDisplayView( theElement, unaDefaultView)
            
        return self
        



    security.declareProtected( permissions.ModifyPortalContent,  'pSetAsDisplayView')
    def pSetAsDisplayView(self, theElement, theViewName):            
        """Set the view that will be presented for an element, when no view is specified. Usually one of Textual or Tabular.
        
        """
                
        unaPortalInterfaceTool = getToolByName( theElement, 'portal_interface')   
        if unaPortalInterfaceTool.objectImplements( theElement, 'Products.CMFPlone.interfaces.BrowserDefault.ISelectableBrowserDefault'):
            if not theElement.getLayout() == theViewName:
                theElement.setLayout( theViewName)                 
        return self
                   
    
    
    
    
    
    
    
        
    # #####################################
    """Internationalisation methods.
    
    """

    
    security.declareProtected( permissions.View,  'fTranslateI18N')
    def fTranslateI18N( self, theContextElement, theI18NDomain, theString, theDefault):
        """Localize a string from a domain into the language negotiated for the current request, or return a default.
        
        """
        
        return ModelDDvlPloneTool_Retrieval().fTranslateI18N( theI18NDomain, theString, theDefault, theContextElement)


    
    


    security.declarePublic( 'fTranslateI18NManyIntoDict')
    def fTranslateI18NManyIntoDict( self, 
        theContextElement,
        theI18NDomainsStringsAndDefaults, 
        theResultDict                   =None):
        """Internationalization: build or update a dictionaty with the translations of all requested strings from the specified domain into the language preferred by the connected user, or return the supplied default.
        
        """
        
        return ModelDDvlPloneTool_Retrieval().fTranslateI18NManyIntoDict( theContextElement, theI18NDomainsStringsAndDefaults, theResultDict)
        
    
    

    security.declareProtected( permissions.View,  'fAsUnicode')
    def fAsUnicode( self, theContextElement,  theString):
        """Decode a string from the system encoding into a unicode in-memory representation.
        
        """
        return ModelDDvlPloneTool_Retrieval().fAsUnicode(theString, theContextElement)

    

    
    
    
    
    
        
    # ######################################
    """Pretty print methods.
    
    """

    
    security.declareProtected( permissions.View,  'fPrettyPrintHTML')
    def fPrettyPrintHTML( self, theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):
        """Render as HTML a presentation of a list with rich inner structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return ModelDDvlPloneTool_Retrieval().fPrettyPrintHTML( theList, theDictKeysToExclude, theDictKeysOrder, theFindAlreadyPrinted)


    security.declareProtected( permissions.View,  'fPrettyPrint')
    def fPrettyPrint( self, theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):
        """Render a text presentation of a list with rich inner structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return ModelDDvlPloneTool_Retrieval().fPrettyPrint( theList, theDictKeysToExclude, theDictKeysOrder, theFindAlreadyPrinted)


    security.declareProtected( permissions.View,  'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResultHTML( self, theProfilingResult):
        """Render as HTML a presentation of an execution profiling result structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return ModelDDvlPloneTool_Retrieval().fPrettyPrintProfilingResultHTML( theProfilingResult)

    security.declareProtected( permissions.View,  'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResult( self, theProfilingResult):
        """Render a text presentation of an execution profiling result structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return ModelDDvlPloneTool_Retrieval().fPrettyPrintProfilingResult( theProfilingResult)

    security.declareProtected( permissions.View,  'fPreferredResultDictKeysOrder')
    def fPreferredResultDictKeysOrder( self):
        """The prefered keys order to render dictionary values as a text presentation.
        
        """
        return ModelDDvlPloneTool_Retrieval().fPreferredResultDictKeysOrder()

    
    
    
    
    
    
    
    
    # #############################################################
    """Template invocation methods.
    
    """



    security.declareProtected( permissions.View, 'fRenderTemplate')
    def fRenderTemplate(self, theContextualObject, theTemplateName):
        """Execute a template in the current context and return the rendered HTML.
        
        """
        if not theTemplateName:
            return ''
                        
        aViewName = theTemplateName
        if aViewName.find( '%s') >= 0:
            aProjectName = ''
            try:
                aProjectName = theContextualObject.getNombreProyecto()
            except:
                None
            if aProjectName:    
                aViewName = aViewName % aProjectName
            else:
                aViewName = aViewName % ''
            
        if not aViewName:
            return ''
        
        aViewTemplate    = self.unrestrictedTraverse( aViewName)

        aContext                = aq_inner( theContextualObject)               
        aViewTemplateInContext  = aViewTemplate.__of__(aContext)
        
        aRenderedView = aViewTemplateInContext()       
                   
        return aRenderedView
    
    
    

    
    
    
    
    
    
    # #############################################################
    """Rendered Templates Retrieval from Caches and Caches management methods.
    
    """

    
    
    security.declareProtected( permissions.View, 'fRetrieveCachedTemplatesStatusReport')
    def fRetrieveCachedTemplatesStatusReport(self, theContextualObject,):
        """Retrieve a report with the status of the templates cache, containing the number of entries, the amount of memory occupied, and statistics of cache hits and faults.
        
        """
        
        return ModelDDvlPloneTool_Cache().fRetrieveCachedTemplatesStatusReport( self, theContextualObject)

    
    
        
    
    security.declareProtected( permissions.ManagePortal, 'fConfigureTemplatesCache')
    def fConfigureTemplatesCache(self, theContextualObject, theTemplateCacheParameters):
        """Set parameters controlling the maximum amount of memory available to store cached templates, and other controls on the behavior of the cache.
        
        """
      
        return ModelDDvlPloneTool_Cache().fConfigureTemplatesCache( self, theContextualObject, theTemplateCacheParameters)
        

            
        
        
    
    security.declareProtected( permissions.ManagePortal, 'fEnableTemplatesCache')
    def fEnableTemplatesCache(self, theContextualObject,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return ModelDDvlPloneTool_Cache().fEnableTemplatesCache( self, theContextualObject)
        

        
    
        
    
    security.declareProtected( permissions.ManagePortal, 'fDisableTemplatesCache')
    def fDisableTemplatesCache(self, theContextualObject,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return ModelDDvlPloneTool_Cache().fDisableTemplatesCache( self, theContextualObject)
        

        
    

      
    

    security.declareProtected( permissions.ManagePortal, 'fFlushCachedTemplates')
    def fFlushCachedTemplates(self, theContextualObject):
        """Remove all cached rendered templates, recording who and when requested the flush.
        
        """
        
        return ModelDDvlPloneTool_Cache().fFlushCachedTemplates( self, theContextualObject)

    

    
    security.declareProtected( permissions.ManagePortal, 'fInvalidateCachedTemplatesForElements')
    def fInvalidateCachedTemplatesForElements(self, theContextualObject, theFlushedElementsUIDs, theAuthenticationString):
        """Invoked from service exposed to receive notifications from other ZEO clients authenticated with the supplied string, to flush cache entries for elements of the specified Ids.
        
        """
        
        return ModelDDvlPloneTool_Cache().fInvalidateCachedTemplatesForElements( self, theContextualObject, theFlushedElementsUIDs, theAuthenticationString)

    

    
    security.declarePrivate( 'pFlushCachedTemplatesForElements')
    def pFlushCachedTemplatesForElements(self, theContextualObject, theFlushedElementsUIDs):
        """Invoked from an element intercepting drag&drop reordering and impacting its changes.
        
        """
        return ModelDDvlPloneTool_Cache().pFlushCachedTemplatesForElements( self, theContextualObject, theFlushedElementsUIDs)
  
    
    
    security.declareProtected( permissions.View, 'fRenderTemplateOrCachedForProjectInLanguage')
    def fRenderTemplateOrCachedForProjectInLanguage(self, theContextualObject, theTemplateName):
        """Retrieve a previously rendered template for a project, independent of the here element, for the currently negotiared language and return the rendered HTML.
        
        """
        return ModelDDvlPloneTool_Cache().fRenderTemplateOrCachedForProjectInLanguage( self, theContextualObject, theTemplateName)
    
    


    security.declareProtected( permissions.View, 'fRenderTemplateOrCachedForElementInLanguage')
    def fRenderTemplateOrCachedForElementInLanguage(self, theContextualObject, theTemplateName):
        """ Return theHTML, from cache or just rendered, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
        return ModelDDvlPloneTool_Cache().fRenderTemplateOrCachedForElementInLanguage( self, theContextualObject, theTemplateName)


    
    
    
    
    
    
    
    
    
      
    # #############################################################
    """Import and export methods.
    
    """

        
    
    
    security.declareProtected( permissions.View, 'fExport')
    def fExport(self, 
        theTimeProfilingResults     =None,
        theObject                   =None, 
        theOutputEncoding           =None,
        theAdditionalParams         =None):
        """Export an element as a zipped archive with XML file, and including binary content with the attached files and images."
        
        """
        
        someAllExportTypeConfigs =  ModelDDvlPloneTool_Retrieval().getAllTypeExportConfigs( theObject)        
                
        return ModelDDvlPloneTool_Export().fExport( 
            theTimeProfilingResults     =theTimeProfilingResults,
            theObject                   =theObject, 
            theAllExportTypeConfigs     =someAllExportTypeConfigs, 
            theOutputEncoding           =theOutputEncoding,
            theAdditionalParams         =theAdditionalParams
        )


    
    
   
    
    security.declareProtected( permissions.View, 'fImport')
    def fImport(self, 
        theTimeProfilingResults     =None,
        theContainerObject          =None, 
        theUploadedFile             =None,
        theAdditionalParams         =None):
        """Import into an element a zipped archive with XML file, and any included binary content the attached files and images."
        
        """
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()

        someMDDImportTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeImportConfigs(   theContainerObject)        
        somePloneImportTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeImportConfigs( theContainerObject)        
        someMappingConfigs         =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(         theContainerObject)        
                
        return ModelDDvlPloneTool_Import().fImport( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool          =self,
            theModelDDvlPloneTool_Retrieval=aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators =ModelDDvlPloneTool_Mutators(),
            theContainerObject             =theContainerObject, 
            theUploadedFile                =theUploadedFile,
            theMDDImportTypeConfigs        =someMDDImportTypeConfigs, 
            thePloneImportTypeConfigs      =somePloneImportTypeConfigs, 
            theMappingConfigs              =someMappingConfigs,
            theAdditionalParams            =theAdditionalParams
        )

      
    
 
 
    
    
    
    
        
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
   
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        aModelDDvlPloneTool_Version   = ModelDDvlPloneTool_Version()
        
                
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
   
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        aModelDDvlPloneTool_Version   = ModelDDvlPloneTool_Version()
        
                
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
                
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()

        someMDDNewVersionTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theOriginalObject)        
        somePloneNewVersionTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theOriginalObject)        
                
        return ModelDDvlPloneTool_Version().fNewVersion( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool          =self,
            theModelDDvlPloneTool_Retrieval=aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators =ModelDDvlPloneTool_Mutators(),
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


   

    

    
    
    
    
        
    # #############################################################
    """Translation retrieval and management methods.
    
    """


    security.declareProtected( permissions.View, 'fNewTranslation')
    def fNewTranslation(self, 
        theTimeProfilingResults     =None,
        theOriginalObject           =None, 
        theNewTranslationContainerKind  =None,
        theNewLanguage           =None,
        theFallbackStrategy        =None,
        theNewTitle                 =None,
        theNewId                    =None,
        theAdditionalParams         =None):
        """Create a new translation of the original object which shall be a root, with the new translation name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """
                
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()

        someMDDNewTranslationTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theOriginalObject)        
        somePloneNewTranslationTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theOriginalObject)        
                
        return ModelDDvlPloneTool_Translation().fNewTranslation( 
            theTimeProfilingResults          =theTimeProfilingResults,
            theModelDDvlPloneTool            =self,
            theModelDDvlPloneTool_Retrieval  =aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators   =ModelDDvlPloneTool_Mutators(),
            theOriginalObject                =theOriginalObject, 
            theNewTranslationContainerKind   =theNewTranslationContainerKind,
            theNewLanguage                   =theNewLanguage,
            theFallbackStrategy              =theFallbackStrategy,
            theNewTitle                      =theNewTitle,
            theNewId                         =theNewId,
            theMDDNewTranslationTypeConfigs  =someMDDNewTranslationTypeConfigs, 
            thePloneNewTranslationTypeConfigs=somePloneNewTranslationTypeConfigs, 
            theAdditionalParams              =theAdditionalParams
        )


   

        
       
    security.declareProtected( permissions.View, 'fGroupAction')
    def fGroupAction(self, 
        theTimeProfilingResults     =None,
        theContainerObject          =None, 
        theGroupAction              =None,
        theGroupUIDs                =None,
        theAdditionalParams         =None):
        """Process a request for an action affecting multiple elements, given their UIDs. Actions may be Delete objects, or Prepare to Cut (move) or Prepare to Copy objects. 
        Cut and Copy are prepared by setting a cookie in the HTTP request response including references ( monikers) for the selected elements.        
        
        """
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()

        if theGroupAction == 'Cut':
            return ModelDDvlPloneTool_Refactor().fGroupAction_CutOrCopy( 
                theTimeProfilingResults        = theTimeProfilingResults,
                theModelDDvlPloneTool          = self,
                theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
                theContainerObject             = theContainerObject, 
                theGroupUIDs                   = theGroupUIDs,
                theIsCut                       = True,
                theAdditionalParams            = theAdditionalParams
            )
           
            
        elif theGroupAction == 'Copy':
            return ModelDDvlPloneTool_Refactor().fGroupAction_CutOrCopy( 
                theTimeProfilingResults        = theTimeProfilingResults,
                theModelDDvlPloneTool          = self,
                theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
                theContainerObject             = theContainerObject, 
                theGroupUIDs                   = theGroupUIDs,
                theIsCut                       = False,
                theAdditionalParams            = theAdditionalParams
            )
            
        # ACV 20090930 Handled by the standard Plone manage_paste, implemented in all non-abstract types
        #elif theGroupAction == 'Paste':
            #return self.fPaste( 
                #theTimeProfilingResults        = theTimeProfilingResults,
                #theContainerObject             = theContainerObject, 
                #theGroupUIDs                   = theGroupUIDs,
                #theAdditionalParams            = theAdditionalParams
            #)
            
            
        elif theGroupAction == 'Delete':
            # ACV 20090930 Handled by a specific view MDDEliminarVarios
            pass
        
   
        return None
    
        
        
        
    
    
    

        
    # #############################################################
    """Clipboard paste methods.
    
    """    
    
    
    security.declareProtected( permissions.AddPortalContent, 'fObjectPaste')
    def fObjectPaste(self, 
        theTimeProfilingResults     =None,
        theContainerObject          =None, 
        theAdditionalParams         =None):
        
        """Invoked from template MDDPaste, used as an alias to the object_paste action.
        Paste into an element the elements previously copied (references held in the clipboard internet browser cookie), and all its contents, reproducing between the copied elements the relations between the original elements.        
        Cookies have not yet been decoded into objects to paste.
        Preferred to the alternative of fPaste below ( transparently paste from usual plone action), to deliver a detailed report of the paste operation and any possible errors. or objects not pasted.
        
        """
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        
        someMDDCopyTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theContainerObject)        
        somePloneCopyTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theContainerObject)        
        someMappingConfigs       =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(       theContainerObject)        
                
        return ModelDDvlPloneTool_Refactor().fObjectPaste( 
            theTimeProfilingResults        = theTimeProfilingResults,
            theModelDDvlPloneTool          = self,
            theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators(),
            theContainerObject             = theContainerObject, 
            theMDDCopyTypeConfigs          = someMDDCopyTypeConfigs, 
            thePloneCopyTypeConfigs        = somePloneCopyTypeConfigs, 
            theMappingConfigs              = someMappingConfigs, 
            theAdditionalParams            = theAdditionalParams
        )
        

    
    
    
    
    
    security.declareProtected( permissions.AddPortalContent, 'fPaste')
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
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        
        someMDDCopyTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theContainerObject)        
        somePloneCopyTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theContainerObject)        
        someMappingConfigs       =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(       theContainerObject)        
                
        return ModelDDvlPloneTool_Refactor().fPaste( 
            theTimeProfilingResults        = theTimeProfilingResults,
            theModelDDvlPloneTool          = self,
            theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators = ModelDDvlPloneTool_Mutators(),
            theContainerObject             = theContainerObject, 
            theObjectsToPaste              = theObjectsToPaste,
            theIsMoveOperation             = theIsMoveOperation,
            theMDDCopyTypeConfigs          = someMDDCopyTypeConfigs, 
            thePloneCopyTypeConfigs        = somePloneCopyTypeConfigs, 
            theMappingConfigs              = someMappingConfigs, 
            theAdditionalParams            = theAdditionalParams
        )

    
    
     
    
    
    
    
    

    # #############################################################
    """Retrieval of information about relevant Plone Products installed.
    
    """        
    
    
    security.declareProtected( permissions.View, 'fProductsInfo')
    def fProductsInfo(self, 
        theContextualObject         =None,
        theProductNames             =None, 
        theProductNamesNotInQuickInstaller=None,
        theAdditionalParams         =None):
        """Retrieve from Plone Quick Installer the information for the named products.
        
        """
    
        someProductsInfo = []
        
        if ( theContextualObject == None):
            return someProductsInfo
        
        if not ( theProductNames or theProductNamesNotInQuickInstaller):
            return someProductsInfo
        
        
        
        aPortalQuickInstaller = getToolByName( theContextualObject, 'portal_quickinstaller', None)
        if ( aPortalQuickInstaller == None):
            return someProductsInfo
        
        anInstanceHome  = aPortalQuickInstaller.getInstanceHome()
        aProductsFolder = os.path.join( anInstanceHome, 'Products')
        
    
        
        someInstallableProducts = aPortalQuickInstaller.listInstallableProducts()
        """entries like {'id':r, 
                        'status':p.getStatus(),
                        'hasError':p.hasError()}
        """
        someInstallableProductsById = dict( [ [aProduct.get('id', ''), aProduct,] for  aProduct in someInstallableProducts])
        
        someInstalledProducts = aPortalQuickInstaller.listInstalledProducts()
        """entries like {'id':r, 'status':p.getStatus(),
                        'hasError':p.hasError(),
                        'isLocked':p.isLocked(),
                        'isHidden':p.isHidden(),
                        'installedVersion':p.getInstalledVersion()}
        """
        someInstalledProductsById = dict( [ [ aProduct.get('id', ''), aProduct,] for  aProduct in someInstalledProducts])
    
        
        for aProductName in theProductNames:
            aInstallableProduct = someInstallableProductsById.get( aProductName, {})
            if aInstallableProduct:
                aProductInfo = aInstallableProduct.copy()
                aProductInfo[ 'installed'] = False
                someProductsInfo.append( aProductInfo)
            else:
                aInstalledProduct = someInstalledProductsById.get( aProductName, {})
                if aInstalledProduct:
                    aProductInfo = aInstalledProduct.copy()
                    aProductInfo[ 'installed'] = True
                    someProductsInfo.append( aProductInfo)
                else:
                    aProductInfo = {
                        'id':        aProductName, 
                        'status':    False,
                        'hasError':  True,
                        'installed': False,
                    }
                    someProductsInfo.append( aProductInfo)
                    
                    
        for aProductName in theProductNamesNotInQuickInstaller:
            aFound = False

            aProductPath =os.path.join( aProductsFolder, aProductName)
            someFiles = []
            try:
                someFiles = os.listdir( aProductPath)
            except OSError:
                None
            for aFile in someFiles:
                if aFile.lower() == 'version.txt':
                    aVersion = open( os.path.join( aProductPath, aFile)).read().strip()
                    if aVersion:
                        aProductInfo = {
                            'id':        aProductName, 
                            'status':    True,
                            'hasError':  False,
                            'installed': True,
                            'installedVersion': aVersion,
                        }
                        someProductsInfo.append( aProductInfo)
                        aFound = True
                        break
            if not aFound:
                aProductInfo = {
                    'id':        aProductName, 
                    'status':    False,
                    'hasError':  False,
                    'installed': False,
                }
                someProductsInfo.append( aProductInfo)
                
                        
        return someProductsInfo
    
    

    
    
     
    
    
    

# ####################################################
"""Constructor methods, only used when adding class to objectManager.

"""

def manage_addAction(self, REQUEST=None):
    "Add tool instance to parent ObjectManager"
    id = ModelDDvlPloneTool.id
    self._setObject(id, ModelDDvlPloneTool())
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

constructors = (manage_addAction,)



