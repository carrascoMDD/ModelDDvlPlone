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
import sys
import traceback

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


from Products.ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration import ModelDDvlPloneConfiguration, cModelDDvlPloneConfigurationId


import ModelDDvlPloneToolSupport

import ModelDDvlPloneTool_Inicializacion_Constants



from ModelDDvlPloneTool_Inicializacion_Constants import cLazyCreateModelDDvlPloneConfiguration







# ##################################
# Must be synchronized with the constants of same names in ExternalMethod module MDDLoadModules
#


cModelDDvlPloneToolId = 'ModelDDvlPlone_tool'

cInstall_Tools_On_PortalSkinsCustom = True

cInstallPath_PortalSkinsCustom = [ 'portal_skins', 'custom',]





cModuleNamesToImport = [
    'Products.ModelDDvlPloneTool.MDDLinkedList',
    'Products.ModelDDvlPloneTool.MDDNestedContext',
    'Products.ModelDDvlPloneTool.MDDStringConversions',
    'Products.ModelDDvlPloneTool.PloneElement_TraversalConfig',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor_Constants',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_ImportExport_Constants',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Transactions',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Profiling',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Candidates',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_I18N',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Impact',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Permissions',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_PloneContent',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_TraversalConfigs',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Utils',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval',
    'Products.ModelDDvlPloneTool.MDD_RefactorComponents',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Export',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Import',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Bodies',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators_Plone',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Permissions_Definitions',    
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators',   
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor', 
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Version',   
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Translation',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals',   
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache',  
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool',
    'Products.ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration',
]



"""Tool permissions to be set upon instantiation of the tool,  not restricting the access of anonymous users.

"""         
cModelDDvlPloneToolPermissions = [                                                                                                                                     
    { 'permission': permissions.ManagePortal,         'acquire': True,  'roles': [              'Authenticated', ], },                             
    { 'permission': permissions.ManageProperties,     'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.AddPortalContent,     'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.DeleteObjects,        'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.ModifyPortalContent,  'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.View,                 'acquire': True,  'roles': [ 'Anonymous', 'Authenticated', ], },  
    { 'permission': perm_AccessContentsInformation,   'acquire': True,  'roles': [ 'Anonymous', 'Authenticated', ], },  
]








# #######################################################
# #######################################################

   










class ModelDDvlPloneTool( UniqueObject, PropertyManager, SimpleItem.SimpleItem, ActionProviderBase):
    """Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. Holds and persists configurations for caches and presentation. Holds transient globals for caches, on behalf of the ModelDDvlPloneTool_Cache manager role.
    
    """

              
        
    
    "The ModelDDvlPloneTool"

    meta_type = 'ModelDDvlPloneTool'

    id = cModelDDvlPloneToolId

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

    


    

 

    # #######################################################
    # #######################################################
    """Globals
    
    """
    # #######################################################
    
       
    
    
    
    
    # #######################################################
    """Dictionary holding imported modules by name. Methods used when reloading modules from the MDDLoadModules external method.
    
    """
    gImportedModules   = None
    
    def fgImportedModules(self,):
        return ModelDDvlPloneTool.gImportedModules
    
    
    
    def pgSetImportedModules(self, theImportedModules):
        ModelDDvlPloneTool.gImportedModules = theImportedModules
           
    
    
    
        
        
        
        
        
        
    
    # #######################################################
    """Module and module component resolution
    
    """
    
     
    security.declarePrivate( '_fIMC')
    def _fIMC( self, theContextualObject, theModuleName, theComponentName=''):
        
        if not theModuleName:
            return None
        
        aComponentName = theComponentName
        if not aComponentName:
            aModuleNameSteps = theModuleName.split( '.')
            if aModuleNameSteps:
                aComponentName = aModuleNameSteps[-1:][ 0]

        if not aComponentName:
            return None
        
        aModule = self._fImportedModule( theContextualObject, theModuleName)
        if not aModule:
            return None
        
        if aComponentName:
            aComponent = None
            try:
                aComponent = getattr( aModule, aComponentName)
            except:
                None
            
        return aComponent
    
    

            
    
    

    security.declarePrivate( '_fImportedModule')
    def _fImportedModule( self, theContextualObject, theModuleName):
        
        someImportedModules = self.fgImportedModules()
        if not someImportedModules:
            
            self.pImportModules( theContextualObject)
             
            someImportedModules = self.fgImportedModules()
            
            if not someImportedModules:
                return None
        
        aModule = someImportedModules.get( theModuleName, None)
        
        if not aModule:
            self.pImportModules( theContextualObject)
            
            someImportedModules = self.fgImportedModules()
            
            aModule = someImportedModules.get( theModuleName, None)
            
        return aModule
    
    
    
    
    
    
    def pImportModules( self, theContextualObject=None):
        
        # #################################################
        """Retrieve the dictionary of loaded modules, stored as a global of the ModelDDvlPloneTool class.
        
        """                

        someImportedModules = self.fgImportedModules()
        if not someImportedModules:
            someImportedModules = { }

        
        # #################################################
        """Determine module names to import.
        
        """
        someModuleNamesToImport = [ ]
        for aModuleName in cModuleNamesToImport:
            if not someImportedModules.has_key( aModuleName):
                someModuleNamesToImport.append( aModuleName)
            
           
            
        # #################################################
        """Import  modules.
        
        """                        
        for aModuleNameToImport in someModuleNamesToImport:
            
            someModuleNameSteps = aModuleNameToImport.split( '.')
            if someModuleNameSteps:
                       
                aRootModule = None
                try:
                    aRootModule = __import__( aModuleNameToImport, globals(), locals())
                except:
                    None
                
                if aRootModule:
                    aModule = aRootModule
                    
                    if len( someModuleNameSteps) > 1:
                        
                        someRemainingSteps = someModuleNameSteps[1:]
                        for aModuleNameStep in someRemainingSteps:                        
                            aModule = getattr( aModule, aModuleNameStep)
                            if not aModule:
                                break
                
                    if aModule:
                        someImportedModules[ aModuleNameToImport] = aModule
                        
                        
                        
        #for aModuleNameToImport in someModuleNamesToImport:
            
            #someModuleNameSteps = aModuleNameToImport.split( '.')
            #if someModuleNameSteps:
                
                #aRootModuleName = someModuleNameSteps[ 0]
                #aRootModule = someImportedRootModules.get( aRootModuleName, None)
                
                #if not aRootModule:
                    #try:
                        #aRootModule = __import__( aRootModuleName, globals(), locals())
                    #except:
                        #None
                    #if aRootModule:
                        #someImportedRootModules[ aRootModuleName] = aRootModule
                
                #if aRootModule:
                    #aModule = aRootModule
                    
                    #if len( someModuleNameSteps) > 1:
                        
                        #someRemainingSteps = someModuleNameSteps[1:]
                        #for aModuleNameStep in someRemainingSteps:                        
                            #aModule = getattr( aModule, aModuleNameStep)
                            #if not aModule:
                                #break
                
                    #if aModule:
                        #someImportedModules[ aModuleNameToImport] = aModule
                    
        self.pgSetImportedModules( someImportedModules)
        return self

     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    

    security.declarePublic( 'fTestAddedMethod')
    def fTestAddedMethod( self, ):
        return """<p>The fTestAddedMethod has been added</p>"""

 
        
                   

  

    #security.declarePublic( 'fTestAddedMethod2')
    #def fTestAddedMethod2( self, ):
        #return """<p>The fTestAddedMethod 2 has been added</p>"""

    
    # #######################################################
    # #######################################################
            


    

        
        


    security.declareProtected( permissions.View, 'fSecondsNow')
    def fSecondsNow(self):   
    
        return ModelDDvlPloneToolSupport.fSecondsNow()
    
    
        
    security.declareProtected( permissions.View, 'fMillisecondsNow')
    def fMillisecondsNow(self):   
        return ModelDDvlPloneToolSupport.fMillisecondsNow()
    
    
    
    security.declareProtected( permissions.View, 'fDateTimeNow')
    def fDateTimeNow(self):   
        return ModelDDvlPloneToolSupport.fDateTimeNow()
    
    
    
    
    security.declareProtected( permissions.View, 'fDateTimeAfterSeconds')
    def fDateTimeAfterSeconds( self, theDateTime, theSeconds):
        return ModelDDvlPloneToolSupport.fDateTimeAfterSeconds( theDateTime, theSeconds)
   
    
             
        
    security.declarePublic( 'fMillisecondsToDateTime')
    def fMillisecondsToDateTime( self, theMilliseconds):
        return ModelDDvlPloneToolSupport.fMillisecondsToDateTime( theMilliseconds)
        
        
         


    # #######################################################
    # #######################################################

        
    
    # #######################################################
    """Accessors for globals held by ModelDDvlPloneTool_Globals on behalf of ModelDDvlPloneTool_Cache.
    
    """
    
    security.declarePrivate( 'fgCacheMutex')
    def fgCacheMutex(self, theContextualObject):
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals').gCacheMutex
       
    
    
    
    security.declarePrivate( 'fgCacheStartupTime_Holder')
    def fgCacheStartupTime_Holder(self, theContextualObject, ):
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals').gCacheStartupTime_Holder
    
    
     
    
    security.declarePrivate( 'fgCacheStore_UniqueIdCounter_Holder')
    def fgCacheStore_UniqueIdCounter_Holder(self, theContextualObject, ):
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals').gCacheStore_UniqueIdCounter_Holder
    
    
        
    
    security.declarePrivate( 'fgCacheStore_EntriesByUniqueId')
    def fgCacheStore_EntriesByUniqueId(self, theContextualObject, ):
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals').gCacheStore_EntriesByUniqueId
    
    
        
    
    security.declarePrivate( 'fgCacheStore_EntriesByElementUID')
    def fgCacheStore_EntriesByElementUID(self, theContextualObject, ):
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals').gCacheStore_EntriesByElementUID
    
   
        
    
    security.declarePrivate( 'fgCacheStoreHolders')
    def fgCacheStoreHolders(self, theContextualObject, ):
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals').gCacheStoreHolders
    
        
    
    security.declarePrivate( 'fModelDDvlPloneTool_Retrieval')
    def fgCacheStatisticsHolders(self, theContextualObject, ):
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals').gCacheStatisticsHolders
    
    
    
    
    
       
    
    # #######################################################
    # #######################################################
    
        
 
        


    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """Lazy Initialization of the tool.
        
        """        
        self.pSetPermissions()
                
        return self
    

    
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
    """Managers.
    
    """
    
       
    security.declarePrivate( 'fModelDDvlPloneTool_Retrieval')
    def fModelDDvlPloneTool_Retrieval( self, theContextualObject):
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
    
    
    
    
          
    security.declarePrivate('fPortalRoot')
    def fPortalRoot(self):
        aPortalTool = getToolByName( self, 'portal_url')
        unPortal = aPortalTool.getPortalObject()
        return unPortal       
    
    
    
    
    security.declarePrivate('fPortalURL')
    def fPortalURL(self, ):

        unPortalURLTool = getToolByName( self, 'portal_url', None)
        if not unPortalURLTool:
            return ''
        
        unPortalURL = ''
        try:
            unPortalURL = unPortalURLTool()
        except: 
            None
        if not unPortalURL:
            return ''
        
        return unPortalURL
        
    
    
    
    
    
    
    # ######################################
    """Preferences Retrieval methods.
    TODO
    
    """

    
    security.declareProtected( permissions.View, 'fRetrieveTypeConfig')
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
    
    
    
    
    
        
        
    
    
    # ######################################
    """Retrieval methods.
    
    """
    

    
    security.declareProtected( permissions.View, 'getAllTypeConfigs')
    def getAllTypeConfigs(self, theContextualObject):
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().getAllTypeConfigs( theContextualObject)
    
    
     
    
    
    

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

            
        aModelDDvlPloneTool_Retrieval = self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
                
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
                
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContextualElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
                
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
        
        return self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().fNewResultForElement( theElement, theResult)
    
    
    

    
    
    
    

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
        
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()

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

        aModelDDvlPloneTool_Retrieval = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()

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
        
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
        
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
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().fDefaultPloneSubItemsParameters()
    
   
   
    
    
    


    security.declareProtected( permissions.View, 'fDeleteImpactReport')
    def fDeleteImpactReport(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a report of the impact of deleting an element, including all elements that will be related (contained elements) and elements that will be affected (related elements).
        
        """
        
        aModelDDvlPloneTool_Retrieval = self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
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
        
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
        
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
        
        return self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Bodies')().fCookedBodyForElement( 
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
        
        return self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Bodies')().fEditableBodyForElement( 
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
        
        return self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Bodies')().fEditableBodyBlock_MetaTypeIcons( 
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
        
        aCreationReport = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fCrearElementoDeTipo( 
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
        
        if not aCreationReport:
            return aCreationReport
        
        unosImpactedObjectsUIDs = aCreationReport.get( 'impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
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
        
        aCreationReport = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fCrearElementoDeTipo( 
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
        
        if not aCreationReport:
            return aCreationReport
        
        unNewElementResult = aCreationReport.get( 'new_object_result', None)
        if not unNewElementResult:
            return aCreationReport
        
        if not aCreationReport:
            return aCreationReport
        
        unosImpactedObjectsUIDs = aCreationReport.get( 'impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return aCreationReport
       
        
        
                    
    
    
    
    
        
    security.declareProtected(  permissions.ModifyPortalContent, 'fChangeValues')
    def fChangeValues(self, 
        theTimeProfilingResults =None,
        theElement              =None, 
        theNewValuesDict        =None,
        theAdditionalParams     =None):        
        """Apply changes to an element's attributes values.
        
        """
        
        unChangeReport = self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fChangeValues(  
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement, 
            theNewValuesDict        =theNewValuesDict,
            theAdditionalParams     =theAdditionalParams
        )
        if not unChangeReport:
            return unChangeReport
        
        unosImpactedObjectsUIDs = unChangeReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theElement, unosImpactedObjectsUIDs)
            
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
        
        unMoveReport = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fMoveSubObject( 
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
            self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
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
        
        unMoveReport = self._fIMC( theSourceElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fMoveReferencedObject(
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
            self._fIMC( theSourceElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theSourceElement, unosImpactedObjectsUIDs)
            
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
        
        unLinkReport = self._fIMC( theSourceElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fLinkToUIDReferenceFieldNamed( 
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
            self._fIMC( theSourceElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theSourceElement, unosImpactedObjectsUIDs)
            
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

        unUnlinkReport = self._fIMC( theSourceElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fUnlinkFromUIDReferenceFieldNamed( 
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
            self._fIMC( theSourceElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theSourceElement, unosImpactedObjectsUIDs)
            
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

        unDeleteReport = self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fEliminarElemento( 
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
            self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theElement, unosImpactedObjectsUIDs)
            
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

        someDeleteManyReports = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fEliminarVariosElementos( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement,            
            theIdsToDelete          =theIdsToDelete, 
            theUIDsToDelete         =theUIDsToDelete, 
            theRequestSeconds       =theRequestSeconds, 
            theAdditionalParams     =theAdditionalParams
        )
        if not someDeleteManyReports:
            return someDeleteManyReports
        
        unasUIDsAlreadyFlushed = set( )
        
        for unDeleteReport in someDeleteManyReports:
        
            if unDeleteReport and ( unDeleteReport.get( 'effect', '') == 'deleted'):
                unImpactReport = unDeleteReport.get( 'impact_report', {})
                unosImpactedObjectsUIDs = unDeleteReport.get('impacted_objects_UIDs', [])
                unasUIDsNoFlushed = [ unaUID for unaUID in unosImpactedObjectsUIDs if not ( unaUID in unasUIDsAlreadyFlushed)]
    
                if unasUIDsNoFlushed:
                    self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unasUIDsNoFlushed)
                    unasUIDsAlreadyFlushed.update( unasUIDsNoFlushed)
            
        return someDeleteManyReports
    
                
    
        
    
    
    
    
    
    
    
    
    
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

        unDeleteReport = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fEliminarElementoPlone( 
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
            self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
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

        unMoveReport = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fMoveSubObjectPlone( 
            theTimeProfilingResults =theTimeProfilingResults,            
            theContainerElement     =theContainerElement,  
            theTraversalName        =theTraversalName, 
            theMovedObjectUID       =theMovedObjectUID, 
            theMoveDirection        =theMoveDirection, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unMoveReport:
            return unMoveReport
        
        unosImpactedObjectsUIDs = unMoveReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return unMoveReport
                  
    
    
    
    
    
                

    # ####################################################
    """Display view maintenance methods.
    
    """

               
                   

    security.declareProtected( permissions.View,  'pSetDefaultDisplayView')
    def pSetDefaultDisplayView(self, theElement):  
        """Set to its default the view that will be presented for an element, when no view is specified. Usually one of Textual or Tabular.
        
        """
    
        if not self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().fCheckElementPermission( theElement, [ permissions.ModifyPortalContent ], None):
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
        
        return self._fIMC( theContextElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().fTranslateI18N( theI18NDomain, theString, theDefault, theContextElement)


    
    


    security.declarePublic( 'fTranslateI18NManyIntoDict')
    def fTranslateI18NManyIntoDict( self, 
        theContextElement,
        theI18NDomainsStringsAndDefaults, 
        theResultDict                   =None):
        """Internationalization: build or update a dictionaty with the translations of all requested strings from the specified domain into the language preferred by the connected user, or return the supplied default.
        
        """
        
        return self._fIMC( theContextElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().fTranslateI18NManyIntoDict( theContextElement, theI18NDomainsStringsAndDefaults, theResultDict)
        
    
    
    
    
    
    

    security.declarePublic( 'fTranslationsBundle_ForChanges')
    def fTranslationsBundle_ForChanges( self, theContextElement,):
        """The translations of change kinds, and property names of changes and change details, to be used in the presentation of changes.
        
        """
        
        return self._fIMC( theContextElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fTranslationsBundle_ForChanges( theContextElement,)
        
    
    
    
    
    

    security.declareProtected( permissions.View,  'fAsUnicode')
    def fAsUnicode( self, theContextElement,  theString):
        """Decode a string from the system encoding into a unicode in-memory representation.
        
        """
        return self._fIMC( theContextElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().fAsUnicode(theString, theContextElement)

    

    
    
    
    
    
        
    # ######################################
    """Pretty print methods.
    
    """

    
    security.declareProtected( permissions.View,  'fPrettyPrintHTML')
    def fPrettyPrintHTML( self, theContextualObject, theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):
        """Render as HTML a presentation of a list with rich inner structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().fPrettyPrintHTML( theList, theDictKeysToExclude, theDictKeysOrder, theFindAlreadyPrinted)


    
    
    
    
    
    security.declareProtected( permissions.View,  'fPrettyPrint')
    def fPrettyPrint( self, theContextualObject, theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):
        """Render a text presentation of a list with rich inner structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return self._fIMC( theContextualObject, 'ModelDDvlPloneToolSupport')().fPrettyPrint( theList, theDictKeysToExclude, theDictKeysOrder, theFindAlreadyPrinted)


    
    
    
    
    
    security.declareProtected( permissions.View,  'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResultHTML( self, theContextualObject, theProfilingResult):
        """Render as HTML a presentation of an execution profiling result structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return self._fIMC( theContextualObject, 'ModelDDvlPloneToolSupport')().fPrettyPrintProfilingResultHTML( theProfilingResult)

    
    
    
    
    
    security.declareProtected( permissions.View,  'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResult( self, theContextualObject, theProfilingResult):
        """Render a text presentation of an execution profiling result structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return self._fIMC( theContextualObject, 'ModelDDvlPloneToolSupport')().fPrettyPrintProfilingResult( theProfilingResult)

    
    
    
    
    
    security.declareProtected( permissions.View,  'fPreferredResultDictKeysOrder')
    def fPreferredResultDictKeysOrder( self, theContextualObject,):
        """The prefered keys order to render dictionary values as a text presentation.
        
        """
        return self._fIMC( theContextualObject, 'ModelDDvlPloneToolSupport')().fPreferredResultDictKeysOrder()

    
    
    
    
    
    
    
    
    # #############################################################
    """Template invocation methods.
    
    """

    
    
    
    security.declareProtected( permissions.View, 'fNoCacheIdAllowsRender')
    def fNoCacheIdAllowsRender(self, theContextualObject, theNoCacheCode, theTemplateName, ):
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fNoCacheIdAllowsRender( self, theContextualObject, theNoCacheCode, theTemplateName)
        
    
    
    


    security.declareProtected( permissions.View, 'fRenderTemplate')
    def fRenderTemplate(self, theContextualObject, theTemplateName):
        """Execute a template in the current context and return the rendered HTML.
        
        """
        if not theTemplateName:
            return ''
             
        aViewTemplateInContext  = self.fTemplateCallable( theContextualObject, theTemplateName)
        
        if not aViewTemplateInContext:
            return ''
        
        aRenderedView = aViewTemplateInContext()       
                   
        return aRenderedView
    
    

    
    
    

    security.declareProtected( permissions.View, 'fTemplateCallable')
    def fTemplateCallable(self, theContextualObject, theTemplateName):
        """Execute a template in the current context and return the rendered HTML.
        
        """
        if not theTemplateName:
            return None
                        
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
            return None
        
        aViewTemplate    = self.unrestrictedTraverse( aViewName)

        aContext                = aq_inner( theContextualObject)               
        aViewTemplateInContext  = aViewTemplate.__of__(aContext)

        return aViewTemplateInContext
    
    
    
    
    
    

    
    # #############################################################
    """Cache configuration editing and status reporting.
    
    """


     
    
    security.declareProtected( permissions.View, 'fRetrieveCacheStatusReport')
    def fRetrieveCacheStatusReport(self, theContextualObject, theRepresentation=''):
        """Retrieve a report with the status of the templates cache, containing the number of entries, the amount of memory occupied, and statistics of cache hits and faults.
        
        """
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fRetrieveCacheStatusReport( self, theContextualObject,theRepresentation=theRepresentation)


        
    
    
    security.declareProtected( permissions.ManagePortal, 'fActivateCaching')
    def fActivateCaching(self, theContextualObject, theCacheName,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fActivateCaching( self, theContextualObject)
        

        
    
        
    
    security.declareProtected( permissions.ManagePortal, 'fDeactivateCaching')
    def fDeactivateCaching(self, theContextualObject,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fDeactivateCaching( self, theContextualObject)
        


             
    
    
        
    
    security.declareProtected( permissions.ManagePortal, 'fConfigureTemplatesCache')
    def fConfigureTemplatesCache(self, theContextualObject, theEditedCacheParameters, theCacheName):
        """Set parameters controlling the maximum amount of memory available to store cached templates, and other controls on the behavior of the cache.
        
        """
      
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fConfigureTemplatesCache( self, theContextualObject, theEditedCacheParameters, theCacheName)
        

            
        
        
    
    security.declareProtected( permissions.ManagePortal, 'fEnableTemplatesCache')
    def fEnableTemplatesCache(self, theContextualObject, theCacheName,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fEnableTemplatesCache( self, theContextualObject, theCacheName)
        
         
        
    
    security.declareProtected( permissions.ManagePortal, 'fDectivateTemplatesCache')
    def fDectivateTemplatesCache(self, theContextualObject, theCacheName,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fDectivateTemplatesCache( self, theContextualObject, theCacheName)
        
        
   
    
    
    
    
 
    
    # #############################################################
    """Cache entry and disk flushing.
    
    """


        
    

    security.declareProtected( permissions.ManagePortal, 'pInvalidateToCreatePlone')
    def pInvalidateToCreatePlone(self, theContainerElement):
        """Flush templates that would be affected if a Plone element were created in the container.
        
        """
        
        unosImpactedObjectsUIDs = self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().fImpactCreatePloneUIDs( theContainerElement)

        if unosImpactedObjectsUIDs:
            self._fIMC( theContainerElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return self
       
      
    
    

    
     
    

    security.declareProtected( permissions.ManagePortal, 'fFlushAllCachedTemplates')
    def fFlushAllCachedTemplates(self, theContextualObject, theCacheName, theFlushDiskCache=False):
        """Invoked by authorized users requesting to remove all cached rendered templates, recording who and when requested the flush.
        
        """
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fFlushAllCachedTemplates( self, theContextualObject, theCacheName, theFlushDiskCache=theFlushDiskCache)

       

    
    
    
    security.declareProtected( permissions.ManagePortal, 'fFlushSomeCachedTemplates')
    def fFlushSomeCachedTemplates(self, theContextualObject, theCacheName, theProjectNames, theFlushDiskCache=False):
        """Invoked by authorized users requesting to remove some cached rendered templates, from some projects (or all if none specified), and some languages (or all if none specified) .
        
        """
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fFlushSomeCachedTemplates( self, theContextualObject, theCacheName, theProjectNames,theFlushDiskCache=theFlushDiskCache)

    
    
    
    

    security.declareProtected( permissions.ManagePortal, 'fFlushCachedTemplateByUniqueId')
    def fFlushCachedTemplateByUniqueId(self, theContextualObject, theCacheEntryUniqueId, theFlushDiskCache=False):
        """Invoked by authorized users requesting invalidation of the cache entry given an id unique among all cache entries in all caches.
        
        """
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fFlushCachedTemplateByUniqueId( self, theContextualObject, theCacheEntryUniqueId, theFlushDiskCache=theFlushDiskCache)

    


    

    security.declareProtected( permissions.ManagePortal, 'fFlushCachedTemplateForElement')
    def fFlushCachedTemplateForElement(self, theContextualObject, theFlushCacheCode,  theTemplateName, theFlushDiskCache=False):
        """Invoked by authorized users requesting invalidation of the cache entry for the element given the view name.
        
        """
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fFlushCachedTemplateForElement( self, theFlushCacheCode, theContextualObject, theTemplateName, theFlushDiskCache=theFlushDiskCache)

    
    
    
    
    
    security.declarePrivate( 'pFlushCachedTemplatesForImpactedElementsUIDs')
    def pFlushCachedTemplatesForImpactedElementsUIDs(self, theContextualObject, theFlushedElementsUIDs, theViewsToFlush=[]):
        """Invoked from an element intercepting drag&drop reordering and impacting its changes.
        
        """
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContextualObject, theFlushedElementsUIDs, theViewsToFlush=theViewsToFlush)
  
    
    
        
    
    
    
    security.declareProtected( permissions.ManagePortal, 'pReceiveNotification_FlushCachedTemplatesForElementsUIDs')
    def pReceiveNotification_FlushCachedTemplatesForElementsUIDs(self, theContextualObject, theFlushedElementsUIDs, thePeerIdentificationString, thePeerAuthenticationString, theViewsToFlush=[]):
        """Invoked from service exposed to receive notifications from other ZEO clients authenticated with the supplied string, to flush cache entries for elements of the specified Ids.
        
        """
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pProcessNotification_FlushCachedTemplatesForElementsUIDs( self, theContextualObject, theFlushedElementsUIDs, thePeerIdentificationString, thePeerAuthenticationString, theViewsToFlush=theViewsToFlush)

    

    
    
    
    
 
    
    # #############################################################
    """Cache mediated Rendering - may not render, but rather retrieve the HTML from memory or disk.
    
    """


            
    
    security.declareProtected( permissions.View, 'fRenderTemplateOrCachedElementIndependent')
    def fRenderTemplateOrCachedElementIndependent(self, theContextualObject, theTemplateName, theAdditionalParams=None):
        """Retrieve a previously rendered template for a project, independent of the here element, for the currently negotiared language and return the rendered HTML.
        
        """
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fRenderTemplateOrCachedElementIndependent( self, theContextualObject, theTemplateName, theAdditionalParams)
    
    
    
    


    security.declareProtected( permissions.View, 'fRenderTemplateOrCachedForElement')
    def fRenderTemplateOrCachedForElement(self, theContextualObject, theTemplateName, theAdditionalParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
        return self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fRenderTemplateOrCachedForElement( self, theContextualObject, theTemplateName, theAdditionalParams)


    
    
    
    
    
    
    
    
    
      
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
        
        someAllExportTypeConfigs =  self._fIMC( theObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')().getAllTypeExportConfigs( theObject)        
            
        
        
        return self._fIMC( theObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Export')().fExport( 
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
        
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()

        someMDDImportTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeImportConfigs(   theContainerObject)        
        somePloneImportTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeImportConfigs( theContainerObject)        
        someMappingConfigs         =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(         theContainerObject)        
                
        return self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Import')().fImport( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool          =self,
            theModelDDvlPloneTool_Retrieval=aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators =self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')(),
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
   
        aModelDDvlPloneTool_Retrieval = self._fIMC( theVersionedElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
        aModelDDvlPloneTool_Version   = self._fIMC( theVersionedElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Version')()
        
                
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
   
        aModelDDvlPloneTool_Retrieval = self._fIMC( theVersionedElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
        aModelDDvlPloneTool_Version   = self._fIMC( theVersionedElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Version')()
        
                
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
                
        aModelDDvlPloneTool_Retrieval = self._fIMC( theOriginalObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()

        someMDDNewVersionTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theOriginalObject)        
        somePloneNewVersionTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theOriginalObject)        
                
        return self._fIMC( theOriginalObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Version')().fNewVersion( 
            theTimeProfilingResults        =theTimeProfilingResults,
            theModelDDvlPloneTool          =self,
            theModelDDvlPloneTool_Retrieval=aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators =self._fIMC( theOriginalObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')(),
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
                
        aModelDDvlPloneTool_Retrieval = self._fIMC( theOriginalObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()

        someMDDNewTranslationTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theOriginalObject)        
        somePloneNewTranslationTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theOriginalObject)        
                
        return ModelDDvlPloneTool_Translation().fNewTranslation( 
            theTimeProfilingResults          =theTimeProfilingResults,
            theModelDDvlPloneTool            =self,
            theModelDDvlPloneTool_Retrieval  =aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators   =self._fIMC( theOriginalObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')(),
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


   

   

    

    
    
    
    
        
    # #############################################################
    """Actions applied to multiple elements selected in the same aggregation or collection or relations table.
    
    """


       
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
        
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()

        if theGroupAction == 'Cut':
            return self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor')().fGroupAction_CutOrCopy( 
                theTimeProfilingResults        = theTimeProfilingResults,
                theModelDDvlPloneTool          = self,
                theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
                theContainerObject             = theContainerObject, 
                theGroupUIDs                   = theGroupUIDs,
                theIsCut                       = True,
                theAdditionalParams            = theAdditionalParams
            )
           
            
        elif theGroupAction == 'Copy':
            return self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor')().fGroupAction_CutOrCopy( 
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
    """Clipboard methods.
    
    """    
    
    security.declareProtected( permissions.View, 'pClearClipboard')
    def pClearClipboard(self, 
        theTimeProfilingResults     =None,
        theContextualElement        =None, 
        theAdditionalParams         =None):
              
        self._fIMC( theContextualElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor')().pClearClipboard( 
            theModelDDvlPloneTool            = self,
            theTimeProfilingResults          = theTimeProfilingResults,
            theContextualElement             = theContextualElement,
            theAdditionalParams              = theAdditionalParams
        )
    
            

    
        
        
        
        
        
        
    security.declareProtected( permissions.View, 'fClipboardResult')
    def fClipboardResult(self, 
        theTimeProfilingResults     =None,
        theContextualElement        =None, 
        theAdditionalParams         =None):
      
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContextualElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
        
    
        aClipboardResult = self._fIMC( theContextualElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor')().fClipboardResult( 
            theModelDDvlPloneTool           = self,
            theModelDDvlPloneTool_Retrieval = aModelDDvlPloneTool_Retrieval,
            theTimeProfilingResults         = theTimeProfilingResults,
            theContextualElement            = theContextualElement,
            theAdditionalParams             = theAdditionalParams
        )
        if not aClipboardResult:
            return aClipboardResult
            
        someElementsByRoots = aClipboardResult.get( 'elements_by_roots', [])
        for unResultForOneRoot in someElementsByRoots:
            someElementsResults = unResultForOneRoot[ 'elements']
            for unElementResult in someElementsResults:
                aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)

        return aClipboardResult


        
        
        
        
        
        
        
        
        
        
        

    
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
        
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
        
        someMDDCopyTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theContainerObject)        
        somePloneCopyTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theContainerObject)        
        someMappingConfigs       =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(       theContainerObject)        
                
        unPasteReport = self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor')().fObjectPaste( 
            theTimeProfilingResults        = theTimeProfilingResults,
            theModelDDvlPloneTool          = self,
            theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators = self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')(),
            theContainerObject             = theContainerObject, 
            theMDDCopyTypeConfigs          = someMDDCopyTypeConfigs, 
            thePloneCopyTypeConfigs        = somePloneCopyTypeConfigs, 
            theMappingConfigs              = someMappingConfigs, 
            theAdditionalParams            = theAdditionalParams
        )
        
        unosImpactedObjectsUIDs = unPasteReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerObject, unosImpactedObjectsUIDs)
            
        return unPasteReport
        

    
    
    
    
    
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
        
        aModelDDvlPloneTool_Retrieval = self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')()
        
        someMDDCopyTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theContainerObject)        
        somePloneCopyTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theContainerObject)        
        someMappingConfigs       =  aModelDDvlPloneTool_Retrieval.getMappingConfigs(       theContainerObject)        
                
        unPasteReport = self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor')().fPaste( 
            theTimeProfilingResults        = theTimeProfilingResults,
            theModelDDvlPloneTool          = self,
            theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators = self._fIMC( theContainerObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')(),
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
            self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().pFlushCachedTemplatesForImpactedElementsUIDs( self, theElement, unosImpactedObjectsUIDs)
            
        return unPasteReport
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    # #############################################################
    """Configuration methods.
    
    """        
        
    
    

    security.declarePrivate('fInstallContainer_Tools')
    def fInstallContainer_Tools( self):
        
        unPortalRoot = self.fPortalRoot()
        
        if unPortalRoot == None:
            return None
        
        if not cInstall_Tools_On_PortalSkinsCustom:
            return unPortalRoot
        
        if not cInstallPath_PortalSkinsCustom:
            return unPortalRoot
            
        
        aTraversedObject = unPortalRoot
        for aTraversal in cInstallPath_PortalSkinsCustom:
            aNextObject = None
            try:                    
                aNextObject = aq_get( aTraversedObject,  aTraversal, None, 1)
            except:
                None
            if aNextObject == None:
                return None
            
            aTraversedObject = aNextObject
            
        if aTraversedObject == None:
            return None
        
        return aTraversedObject
    
    
    
    
    security.declarePrivate( 'fModelDDvlPloneConfiguration')
    def fModelDDvlPloneConfiguration(self, theAllowCreation=False):       
        """Retrieve or create an instance of ModelDDvlPloneConfiguration.
        
        """
        try:

            
            aModelDDvlPloneConfiguration = getToolByName( self, cModelDDvlPloneConfigurationId, None)
            
            if aModelDDvlPloneConfiguration:
                return aModelDDvlPloneConfiguration
            
            if not ( theAllowCreation and cLazyCreateModelDDvlPloneConfiguration):
                return None
     
            unInstallContainer = self.fInstallContainer_Tools()
            if not unInstallContainer:
                return None
             
            unaNuevaTool = ModelDDvlPloneConfiguration( ) 
            unInstallContainer._setObject( cModelDDvlPloneConfigurationId,  unaNuevaTool)
            aModelDDvlPloneConfiguration = None
            

                
            aModelDDvlPloneConfiguration = getToolByName( self, cModelDDvlPloneConfigurationId, None)
            if not aModelDDvlPloneConfiguration:
                return None
                        
            return aModelDDvlPloneConfiguration
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during Lazy Initialization operation fModelDDvlPloneConfiguration\n' 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
     
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPloneTool').error( unInformeExcepcion)
    
            return None
             
        
    

        
    security.declarePrivate( 'fGetCacheConfigCopy')
    def fGetCacheConfigCopy(self, theContextualObject, theCacheName):
        
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fGetCacheConfigCopy( self, theContextualObject, theCacheName)
    
          

    
        
    security.declarePrivate( 'fGetCacheConfigParameterValue')
    def fGetCacheConfigParameterValue(self, theContextualObject, theCacheName, thePropertyName):
        
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fGetCacheConfigParameterValue( self, theContextualObject, theCacheName, thePropertyName)

  
    
        
    security.declarePrivate( 'fSetCacheConfigParameterValue')
    def fSetCacheConfigParameterValue(self, theContextualObject, theCacheName, thePropertyName, thePropertyValue):
        
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fSetCacheConfigParameterValue( self, theContextualObject, theCacheName, thePropertyName, thePropertyValue)

    
    
    
               
        
               
        
    security.declarePrivate( 'fUpdateCacheConfig')
    def fUpdateCacheConfig(self, theContextualObject, theCacheName, theConfigChanges):
        """Must be invoked from ModelDDvlPloneTool_Cache within a thread-safe protected critical section, in the same critical section where current configuration values where retrived with fGetCacheConfigCopy to compare with and known wheter if any parameter was changed by the user and the config needs updating.
        
        """
         
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fUpdateCacheConfig(  self, theContextualObject, theCacheName, theConfigChanges)

        
               
        
    security.declarePrivate( 'fGetAllCachesConfigCopy')
    def fGetAllCachesConfigCopy(self, theContextualObject, ):
        
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fGetAllCachesConfigCopy( self, theContextualObject,)
    
    

    
        
    security.declarePrivate( 'fGetAllCachesConfigParameterValue')
    def fGetAllCachesConfigParameterValue(self, theContextualObject, thePropertyName):
          
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fGetAllCachesConfigParameterValue( self, theContextualObject, thePropertyName)

    
    
        
    security.declarePrivate( 'fSetAllCachesConfigParameterValue')
    def fSetAllCachesConfigParameterValue(self, theContextualObject, thePropertyName, thePropertyValue):
            
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fSetAllCachesConfigParameterValue( self, theContextualObject, thePropertyName, thePropertyValue)

        
    
    
    
    
    
              
    security.declarePrivate( 'fUpdateAllCachesConfig')
    def fUpdateAllCachesConfig(self, theContextualObject, theConfigChanges):
        """Must be invoked from ModelDDvlPloneTool_Cache within a thread-safe protected critical section, in the same critical section where current configuration values where retrived with fGetCacheConfigCopy to compare with and known wheter if any parameter was changed by the user and the config needs updating.
        
        """
              
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fUpdateAllCachesConfig( self, theContextualObject, theConfigChanges)

                                                  

                   


    security.declareProtected( permissions.View, 'fSecondsToReviewAndDelete')
    def fSecondsToReviewAndDelete(self, theContextualObject,):

        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return 30 * 60
        return aModelDDvlPloneToolConfiguration.fSecondsToReviewAndDelete( self, theContextualObject,)

        
    
    


    security.declareProtected( permissions.View, 'fSecondsToReviewAndUnlink')
    def fSecondsToReviewAndUnlink(self, theContextualObject,):

        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration( True)
        if not aModelDDvlPloneToolConfiguration:
            return 30 * 60
        return aModelDDvlPloneToolConfiguration.fSecondsToReviewAndUnlink( self, theContextualObject,)

        

    
     
    
        
    security.declareProtected( permissions.View, 'fCached_HTML')
    def fCached_HTML( self, theContextualObject, theCacheEntryUniqueId, theAdditionalParams={}):
        
        aDumpResult = self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fCached_HTML( self, 
            theContextualObject, 
            theCacheEntryUniqueId, 
            theAdditionalParams=theAdditionalParams
        )
        return aDumpResult
    
     
    
    
    
    security.declareProtected( permissions.ManagePortal, 'fCachesDiagnostics')
    def fCachesDiagnostics( self, theContextualObject, theCacheNames=None, theAdditionalParams={}):
        
        someDiagnostics = self._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')().fCachesDiagnostics( self, 
            theContextualObject, 
            theCacheNames       =theCacheNames, 
            theAdditionalParams =theAdditionalParams
        )
        return someDiagnostics
    
     
    
    
    
        
    
    
    

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
        return self.fProductsInfo_Fake( 
            theContextualObject         =theContextualObject,
            theProductNames             =theProductNames, 
            theProductNamesNotInQuickInstaller=theProductNamesNotInQuickInstaller,
            theAdditionalParams         =theAdditionalParams)
    
    
    
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fProductsInfo_Fake')
    def fProductsInfo_Fake(self, 
        theContextualObject         =None,
        theProductNames             =None, 
        theProductNamesNotInQuickInstaller=None,
        theAdditionalParams         =None):
        """Faked to avoid accessing the portal_quick_intaller, because it makes it dirty and join the Transaction and causing a write operation on the store. Bad also for performance, although this is accessed only once per language (is used only in an element independent cacheable view).
        
        """
    
        someProductsInfo = []
        
        if ( theContextualObject == None):
            return someProductsInfo
        
        if not ( theProductNames or theProductNamesNotInQuickInstaller):
            return someProductsInfo
        
        for aProductName in theProductNames:
            aProductInfo = {
                'id':        aProductName, 
                'status':    True,
                'hasError':  False,
                'installed': True,
                'installedVersion': 'x.x',
            }
            someProductsInfo.append( aProductInfo)
                    
                    
        for aProductName in theProductNamesNotInQuickInstaller:
            aProductInfo = {
                'id':        aProductName, 
                'status':    True,
                'hasError':  False,
                'installed': True,
                'installedVersion': 'x.x',
           }
            someProductsInfo.append( aProductInfo)
                
                        
        return someProductsInfo
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fProductsInfo_Accessing')
    def fProductsInfo_Accessing(self, 
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
        
        
        
        #aPortalQuickInstaller = getToolByName( theContextualObject, 'ACV OJO 20091203 seems to get dirty the current Transaction in any read only  portal_quickinstaller', None)
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
        
    
    
    
    
    
    
    
    security.declarePrivate('_pSetAudit_Modification')
    def _pSetAudit_Modification(self, theElement, theChangeKind, theChangeReport, theReverseRelation=False):     
        """Invoked from an element intercepting drag&drop reordering and logging its changes.
        
        """
        self._fIMC( theElement, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')().pSetAudit_Modification( theElement, theChangeKind, theChangeReport, theReverseRelation)
        return self
    
    
    
    

    
         
    
    

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



