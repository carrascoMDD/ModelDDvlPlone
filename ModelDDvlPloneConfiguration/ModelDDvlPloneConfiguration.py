# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneConfiguration.py
#
# Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
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


# Zope
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo

from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation


from Products.CMFCore                    import permissions
from Products.CMFCore.utils              import UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase







    
cSecondsToReviewAndDelete_Minumum = 3
cSecondsToReviewAndDelete_Default = 60
cSecondsToReviewAndDelete_Maximum = 600



cSecondsToReviewAndUnlink_Minumum = 3
cSecondsToReviewAndUnlink_Default = 60
cSecondsToReviewAndUnlink_Maximum = 600


    
cModuleName_ModelDDvlPloneTool       = 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool'
cClassName_ModelDDvlPloneTool_Cache  = 'ModelDDvlPloneTool_Cache'
cMethodName_fInitialCacheConfigs     = 'fInitialCacheConfigs'


def fgInitial_CacheConfigsHolder():
    from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache      import ModelDDvlPloneTool_Cache as aModelDDvlPloneTool_Cache_Class
    aInitialCacheConfigs      = aModelDDvlPloneTool_Cache_Class().fInitialCacheConfigs()
    
    from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport      import fReprAsString
    return fReprAsString( dict( [ [ aCacheConfig.get( 'Name', ''), aCacheConfig,] for aCacheConfig in aInitialCacheConfigs if aCacheConfig.get( 'Name', '')]))


def fgInitial_IsCachingActive():
    from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants import cForbidCaches
    return not cForbidCaches


def fgInitial_PeersToNotify():
    return ''


def fgInitial_IdentificationStringForPeers():
    return ''
    
    
def fgInitial_AuthenticationStringForPeers():    
    return ''
    
    
def fgInitial_AuthenticationStringFromPeers():    
    return ''
    
    
def fgInitial_SecondsToReviewAndDelete():    
    return cSecondsToReviewAndDelete_Default

 
def fgInitial_SecondsToReviewAndUnlink():    
    return cSecondsToReviewAndUnlink_Default







cModelDDvlPloneConfigurationId = 'ModelDDvlPlone_configuration'




"""Tool permissions to be set upon instantiation of the tool,  not restricting the access of anonymous users.

"""         
cModelDDvlPloneConfigurationPermissions = [                                                                                                                                     
    { 'permission': permissions.ManagePortal,         'acquire': True,  'roles': [              'Authenticated', ], },                             
    { 'permission': permissions.ManageProperties,     'acquire': True,  'roles': [              'Authenticated', ], }, 
     # permission Not available for the configuration tool:  { 'permission': permissions.AddPortalContent,     'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.DeleteObjects,        'acquire': True,  'roles': [              'Authenticated', ], }, 
     # permission Not available for the configuration tool:  { 'permission': permissions.ModifyPortalContent,  'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.View,                 'acquire': True,  'roles': [ 'Anonymous', 'Authenticated', ], },  
    { 'permission': perm_AccessContentsInformation,   'acquire': True,  'roles': [ 'Anonymous', 'Authenticated', ], },  
]






class ModelDDvlPloneConfiguration( UniqueObject, PropertyManager, SimpleItem.SimpleItem, ActionProviderBase):
    """Class of ModelDDvlPlone_configuration Persistent singleton plone tool object storing the configuration of ModelDDvlPlone supported applications.
    
    """


    "The ModelDDvlPloneConfiguration"

    meta_type = 'ModelDDvlPloneConfiguration'

    id = cModelDDvlPloneConfigurationId

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
    
    # #######################################################
    # #######################################################
    

            
    
    def __init__( self):
        """Instantiation and initialization.
        
        """

           
        # #######################################################
        """Cache control properties holder. Shall be persistent between server restarts. Acccess exclusively by ModelDDvlPloneTool_Cache within thread-safe protected critical sections.
        
        """
        self.vCacheConfigsHolder = fgInitial_CacheConfigsHolder()

        

        
        
        # #######################################################
        """To notify other ZEO clients of UIDs of elements whose entries have been invalidated by changes in this ZEO client.
        
        """
        self.vIsCachingActive               = fgInitial_IsCachingActive()
        self.vPeersToNotify                 = fgInitial_PeersToNotify()
        self.vIdentificationStringForPeers  = fgInitial_IdentificationStringForPeers()
        self.vAuthenticationStringForPeers  = fgInitial_AuthenticationStringForPeers()

        self.vAuthenticationStringFromPeers = fgInitial_AuthenticationStringFromPeers()
        
        
        
        # #######################################################
        """User Interface Dialog control properties
        
        """        
        self.vSecondsToReviewAndDelete   =  fgInitial_SecondsToReviewAndDelete()
        self.vSecondsToReviewAndUnlink   =  fgInitial_SecondsToReviewAndUnlink()

    
                
        
        

    # #############################################################
    """Configuration access 
    
    """            

    
    
    def fPersistentFieldsAccessor(self,):
        somePersistentFields =  {
            'vCacheConfigsHolder':              self.vCacheConfigsHolder,
            'vIsCachingActive':                 self.vIsCachingActive,
            'vPeersToNotify':                   self.vPeersToNotify,
            'vIdentificationStringForPeers':    self.vIdentificationStringForPeers,
            'vAuthenticationStringForPeers':    self.vAuthenticationStringForPeers,
            'vAuthenticationStringFromPeers':   self.vAuthenticationStringFromPeers,
            'vSecondsToReviewAndDelete':        self.vSecondsToReviewAndDelete,
        }
        return somePersistentFields
    
        
    
    
    def pPersistentFieldsMutator(self, thePersistentFieldsAndValues):
        if not thePersistentFieldsAndValues:
            return self
        
        aSentinel = object()
        
        aNewValue = thePersistentFieldsAndValues.get( 'vCacheConfigsHolder', aSentinel)
        if not ( aNewValue == aSentinel):
            self.vCacheConfigsHolder = aNewValue
            
        aNewValue = thePersistentFieldsAndValues.get( 'vIsCachingActive', aSentinel)
        if not ( aNewValue == aSentinel):
            self.vIsCachingActive = aNewValue
            
        aNewValue = thePersistentFieldsAndValues.get( 'vPeersToNotify', aSentinel)
        if not ( aNewValue == aSentinel):
            self.vPeersToNotify = aNewValue
            
        aNewValue = thePersistentFieldsAndValues.get( 'vIdentificationStringForPeers', aSentinel)
        if not ( aNewValue == aSentinel):
            self.vIdentificationStringForPeers = aNewValue
            
        aNewValue = thePersistentFieldsAndValues.get( 'vAuthenticationStringForPeers', aSentinel)
        if not ( aNewValue == aSentinel):
            self.vAuthenticationStringForPeers = aNewValue
            
        aNewValue = thePersistentFieldsAndValues.get( 'vAuthenticationStringFromPeers', aSentinel)
        if not ( aNewValue == aSentinel):
            self.vAuthenticationStringFromPeers = aNewValue
            
        aNewValue = thePersistentFieldsAndValues.get( 'vSecondsToReviewAndDelete', aSentinel)
        if not ( aNewValue == aSentinel):
            self.vSecondsToReviewAndDelete = aNewValue
            
        return self
    

    
    
                  
        
        

    # #############################################################
    """Configuration access 
    
    """    

    security.declareProtected( permissions.View, 'fSecondsToReviewAndDelete')
    def fSecondsToReviewAndDelete( self, theModelDDvlPloneTool, theContextualElement):
        
        if self.vSecondsToReviewAndDelete > cSecondsToReviewAndDelete_Minumum:
            return self.vSecondsToReviewAndDelete
            
        return cSecondsToReviewAndDelete_Default
    
    
    
 
    security.declareProtected( permissions.View, 'fSecondsToReviewAndUnlink')
    def fSecondsToReviewAndUnlink( self, theModelDDvlPloneTool, theContextualElement):
        
        if self.vSecondsToReviewAndUnlink > cSecondsToReviewAndUnlink_Minumum:
            return self.vSecondsToReviewAndUnlink
            
        return cSecondsToReviewAndUnlink_Default
           

    

    # #############################################################
    """Private Configuration access 
    
    """    
                                                 
    security.declarePrivate( '_fGetCacheConfigHolder')
    def _fGetCacheConfigHolder(self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        
        if not theCacheName:
            return None
        
        if not self.vCacheConfigsHolder:
            return {}
        
        someCacheConfigsHolder = theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport', 'fEvalString')( self.vCacheConfigsHolder)
        
        unCacheConfigHolder = someCacheConfigsHolder.get( theCacheName, None)
        if unCacheConfigHolder == None:
            return None

        return unCacheConfigHolder
    
    
            
    security.declarePrivate( '_pPutCacheConfigHolder')
    def _pPutCacheConfigHolder(self, theModelDDvlPloneTool, theContextualObject, theCacheName, theCacheConfigHolder):
        
        if not theCacheName:
            return self
        
        if not theCacheConfigHolder:
            return self
        
        if not self.vCacheConfigsHolder:
            return {}
        
        someCacheConfigsHolder       = theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport', 'fEvalString')(   self.vCacheConfigsHolder)
            
        someCacheConfigsHolder[ theCacheName] = theCacheConfigHolder
        
        someCacheConfigsHolderString = theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport', 'fReprAsString')( someCacheConfigsHolder)
        
        self.vCacheConfigsHolder = someCacheConfigsHolderString
        
        return self
            
          
    
         

    # #############################################################
    """Generic Configuration access 
    
    """    
                                                 
    
        
    security.declarePrivate( 'fGetCacheConfigCopy')
    def fGetCacheConfigCopy(self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        
        if not theCacheName:
            return None
        
        unCacheConfigHolder = self._fGetCacheConfigHolder( theModelDDvlPloneTool, theContextualObject, theCacheName)
        if unCacheConfigHolder == None:
            return None
        
        unCacheConfigCopy = unCacheConfigHolder.copy()
        return unCacheConfigCopy
    
          

    
        
    security.declarePrivate( 'fGetCacheConfigParameterValue')
    def fGetCacheConfigParameterValue(self, theModelDDvlPloneTool, theContextualObject, theCacheName, thePropertyName):
        
        if ( not theCacheName) or ( not thePropertyName):
            return None

        if not ( thePropertyName in theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cCacheConfigPptyNames')):
            return None

        unCacheConfigHolder = self._fGetCacheConfigHolder( theModelDDvlPloneTool, theContextualObject, theCacheName)
        if unCacheConfigHolder == None:
            return None
        
        unSentinel = object()
        unPropertyValue = unCacheConfigHolder.get( thePropertyName, unSentinel)
        if unPropertyValue == unSentinel:
            return None
        
        return unPropertyValue
  
  
    
        
    security.declarePrivate( 'fSetCacheConfigParameterValue')
    def fSetCacheConfigParameterValue(self, theModelDDvlPloneTool, theContextualObject, theCacheName, thePropertyName, thePropertyValue):
        
        if ( not theCacheName) or ( not thePropertyName):
            return False
        
        if not ( thePropertyName in cCacheConfigPptyNames):
            return None
        
        unCacheConfigHolder = self._fGetCacheConfigHolder( theModelDDvlPloneTool, theContextualObject, theCacheName)
        if unCacheConfigHolder == None:
            return False
        
        unSentinel = object()
        unCurrentPropertyValue = unCacheConfigHolder.get( thePropertyName, unSentinel)
        if unCurrentPropertyValue == unSentinel:
            return False
        
        if unCurrentPropertyValue == thePropertyValue:
            return False
        
        unCacheConfigHolder[ thePropertyName] = thePropertyValue
        
        self._pPutCacheConfigHolder( theModelDDvlPloneTool, theContextualObject, theCacheName, unCacheConfigHolder, )
        
        return True
    
    
    
               
        
               
        
    security.declarePrivate( 'fUpdateCacheConfig')
    def fUpdateCacheConfig(self, theModelDDvlPloneTool, theContextualObject, theCacheName, theConfigChanges):
        """Must be invoked from ModelDDvlPloneTool_Cache within a thread-safe protected critical section, in the same critical section where current configuration values where retrived with fGetCacheConfigCopy to compare with and known wheter if any parameter was changed by the user and the config needs updating.
        
        """
        if not theCacheName:
            return False
        
        if not theConfigChanges:
            return False
        
        unCacheConfigHolder = self._fGetCacheConfigHolder( theModelDDvlPloneTool, theContextualObject, theCacheName)
        if unCacheConfigHolder == None:
            return False
        
        aThereIsChange = False
        
        aSentinel = object()
        
        for aKey in theConfigChanges.keys():

            aValue = theConfigChanges.get( aKey, aSentinel)
            if not ( aValue == aSentinel):
                aCurrentValue = unCacheConfigHolder.get( aKey, aSentinel)
                if ( aCurrentValue == aSentinel) or not ( aValue == aCurrentValue):
                    unCacheConfigHolder[ aKey] = aValue
                    aThereIsChange = True
                    
        if aThereIsChange:
            self._pPutCacheConfigHolder( theModelDDvlPloneTool, theContextualObject, theCacheName, unCacheConfigHolder, )
        
        return aThereIsChange
                                                  
               
        
               
        
    security.declarePrivate( 'fGetAllCachesConfigCopy')
    def fGetAllCachesConfigCopy(self, theModelDDvlPloneTool, theContextualObject, ):
        
        unAllCachesConfigCopy = {
            theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_IsCachingActive'):               self.vIsCachingActive == True,
            theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_PeersToNotify'):                 ( self.vPeersToNotify                 or '')[:],
            theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_IdentificationStringForPeers'):  ( self.vIdentificationStringForPeers  or '')[:],
            theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_AuthenticationStringForPeers'):  ( self.vAuthenticationStringForPeers  or '')[:],
            theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_AuthenticationStringFromPeers') :( self.vAuthenticationStringFromPeers or '')[:],
        }
        return unAllCachesConfigCopy
    
    

    
        
    security.declarePrivate( 'fGetAllCachesConfigParameterValue')
    def fGetAllCachesConfigParameterValue(self, theModelDDvlPloneTool, theContextualObject, thePropertyName):
        
        if not thePropertyName:
            return None

        if not ( thePropertyName in theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPptyNames')):
            return None

        if thePropertyName == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_IsCachingActive'):
            return self.vIsCachingActive == True
            
        if thePropertyName == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_PeersToNotify'):
            return self.vPeersToNotify
            
        if thePropertyName == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_IdentificationStringForPeers'):
            return self.vIdentificationStringForPeers
            
        if thePropertyName == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_AuthenticationStringForPeers'):
            return self.vAuthenticationStringForPeers
            
        if thePropertyName == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_AuthenticationStringFromPeers'):
            return self.vAuthenticationStringFromPeers
         
        return None
  
    
    
        
    security.declarePrivate( 'fSetAllCachesConfigParameterValue')
    def fSetAllCachesConfigParameterValue(self, theModelDDvlPloneTool, theContextualObject, thePropertyName, thePropertyValue):
        
        if not thePropertyName:
            return False
        
        if not ( thePropertyName in cAllCachesConfigPptyNames):
            return False
        
        if thePropertyName ==  theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_IsCachingActive'):
            if not ( thePropertyValue == self.vIsCachingActive):
                self.vIsCachingActive = thePropertyValue
                return True
                
        if thePropertyName ==  theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_PeersToNotify'):
            if not ( thePropertyValue == self.vPeersToNotify):
                self.vPeersToNotify = thePropertyValue
                return True
                
        if thePropertyName ==  theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_IdentificationStringForPeers'):
            if not ( thePropertyValue == self.vIdentificationStringForPeers):
                self.vIdentificationStringForPeers = thePropertyValue
                return True
                
        if thePropertyName ==  theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_AuthenticationStringForPeers'):
            if not ( thePropertyValue == self.vAuthenticationStringForPeers):
                self.vAuthenticationStringForPeers = thePropertyValue
                return True
                
        if thePropertyName ==  theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_AuthenticationStringFromPeers'):
            if not ( thePropertyValue == self.vAuthenticationStringFromPeers):
                self.vAuthenticationStringFromPeers = thePropertyValue
                return True
                    
        return False
    
        
    
    
    
    
    
              
    security.declarePrivate( 'fUpdateAllCachesConfig')
    def fUpdateAllCachesConfig(self, theModelDDvlPloneTool, theContextualObject, theConfigChanges):
        """Must be invoked from ModelDDvlPloneTool_Cache within a thread-safe protected critical section, in the same critical section where current configuration values where retrived with fGetCacheConfigCopy to compare with and known wheter if any parameter was changed by the user and the config needs updating.
        
        """
        if not theConfigChanges:
            return False
        
        aSentinel = object()
        
        aThereIsChange = False
        
        for aKey in theConfigChanges.keys():

            if aKey == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_IsCachingActive'):
                aValue = theConfigChanges.get( aKey, aSentinel)
                if not ( aValue == aSentinel):
                    if not ( aValue == self.vIsCachingActive):
                        self.vPeersToNotify = aValue
                        aThereIsChange = True
                    
            if aKey == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_PeersToNotify'):
                aValue = theConfigChanges.get( aKey, aSentinel)
                if not ( aValue == aSentinel):
                    if not ( aValue == self.vPeersToNotify):
                        self.vPeersToNotify = aValue
                        aThereIsChange = True
                    
            if aKey == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_IdentificationStringForPeers'):
                aValue = theConfigChanges.get( aKey, aSentinel)
                if not ( aValue == aSentinel):
                    if not ( aValue == self.vIdentificationStringForPeers):
                        self.vIdentificationStringForPeers = aValue
                        aThereIsChange = True
                    
            if aKey == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_AuthenticationStringForPeers'):
                aValue = theConfigChanges.get( aKey, aSentinel)
                if not ( aValue == aSentinel):
                    if not ( aValue == self.vAuthenticationStringForPeers):
                        self.vAuthenticationStringForPeers = aValue
                        aThereIsChange = True
                    
            if aKey == theModelDDvlPloneTool._fIMC( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants', 'cAllCachesConfigPpty_AuthenticationStringFromPeers'):
                aValue = theConfigChanges.get( aKey, aSentinel)
                if not ( aValue == aSentinel):
                    if not ( aValue == self.vAuthenticationStringFromPeers):
                        self.vAuthenticationStringFromPeers = aValue
                        aThereIsChange = True

        return aThereIsChange
                                                  

                   



    
    
    
    
    

            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
        for unaPermissionSpec in cModelDDvlPloneConfigurationPermissions:
            unaPermission = unaPermissionSpec[ 'permission']
            unAcquire     = unaPermissionSpec[ 'acquire'] 
            unosRoles     = unaPermissionSpec[ 'roles']
            
            if unaPermission:
                self.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
        
        return self
        
         
    
    

# ####################################################
"""Constructor methods, only used when adding class to objectManager.

"""

def manage_addAction(self, REQUEST=None):
    "Add tool instance to parent ObjectManager"
    id = ModelDDvlPloneConfiguration.id
    self._setObject(id, ModelDDvlPloneConfiguration())
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

constructors = (manage_addAction,)



