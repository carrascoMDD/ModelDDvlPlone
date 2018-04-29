# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneToolPreferences.py
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



from AccessControl import ClassSecurityInfo

from Products.CMFCore import permissions

from Products.CMFCore.utils import getToolByName

from ModelDDvlPloneTool_CacheConstants  import *

from ModelDDvlPloneToolSupport          import fEvalString, fReprAsString


cKnownPreferencesExtents       = [ 'presentation',] 
  


cCacheName_ElementIndependent = 'ElementIndependent' 
cCacheName_ForElements        = 'ForElements'    
cCacheName_ForUsers           = 'ForUsers'    

cCacheNamesAndKindsToCreate = [ 
    [ cCacheName_ElementIndependent, cCacheKind_ElementIndependent,],
    [ cCacheName_ForElements,        cCacheKind_ForElements,],
    [ cCacheName_ForUsers,           cCacheKind_ForUsers,],
]










# #######################################################
"""Names for the cache configuration properties.

"""
cPreferenceProperty_Presentation_SecondsToDelete              = 'SecondsToDelete'
cPreferenceProperty_Presentation_SecondsToEdit                = 'SecondsToEdit'
cPreferenceProperty_Presentation_SecondsToLink                = 'SecondsToLink'
cPreferenceProperty_Presentation_DisplayActionLabels          = 'DisplayActionLabels'
cPreferenceProperty_Presentation_DisplayCabeceraNavigationLabels = 'DisplayActionLabels'
cPreferenceProperties_PresentationNames = [
    cPreferenceProperty_Presentation_SecondsToDelete,              
    cPreferenceProperty_Presentation_SecondsToEdit,                
    cPreferenceProperty_Presentation_SecondsToLink, 
    cPreferenceProperty_Presentation_DisplayActionLabels, 
    cPreferenceProperty_Presentation_DisplayCabeceraNavigationLabels,
]


cPreferenceProperty_Name                       = 'Name'
cPreferenceProperty_Kind                       = 'Kind'

cPreferencePropertyNames = [
]








# #######################################################
"""Names for the cache storage structure.

"""
cPreferences_Name                   = 'Name'
cPreferences_Kind                   = 'Kind'
cPreferences_CachedTemplates        = 'CachedTemplates'


class ModelDDvlPloneToolPreferences:
    """Handles the persistent configuration of the ModelDDvlPlone framework. Currently, mostly Caching configuration, and UI.
    
    """
    
    # Standard security settings
    security = ClassSecurityInfo()
    
    
    def __init__( self):
        """Instantiation and initialization.
        
        """
        
        
        
        
        
     
        
        # #######################################################
        """Cache control properties holder. Shall be persistent between server restarts. Acccess exclusively by ModelDDvlPloneTool_Cache within thread-safe protected critical sections.
        
        """
        self.vPreferencesHolder = fReprAsString( dict( [ [ aCacheConfig.get( cPreferenceProperty_Name, ''), aCacheConfig,] for aCacheConfig in ModelDDvlPloneTool_Cache().fInitialCacheConfigs() if aCacheConfig.get( cPreferenceProperty_Name, '')]))

        
        
        ## #######################################################
        #"""User Interface Dialog control properties
        
        #"""        
        #self.vSecondsToDelete   = cSecondsToDelete_Default
    
                
        
 
        
        
        

    



        
 
        
                
    

    # #############################################################
    """Access to Preferences.
    
    """

        

    
                                                 
    security.declarePrivate( '_fGetPreferencesHolder')
    def _fGetPreferencesHolder(self, theContextualObject, thePreferencesName):
        
        if not thePreferencesName:
            return None
        
        if not self.vPreferencesHolder:
            return {}
        
        somePreferencesHolder = fEvalString( self.vPreferencesHolder)
        
        unPreferencesHolder = somePreferencesHolder.get( thePreferencesName, None)
        if unPreferencesHolder == None:
            return None

        return unPreferencesHolder
    
    
            
    security.declarePrivate( '_pPutPreferencesHolder')
    def _pPutPreferencesHolder(self, theContextualObject, thePreferencesName, thePreferencesHolder):
        
        if not thePreferencesName:
            return self
        
        if not thePreferencesHolder:
            return self
        
        if not self.vPreferencesHolder:
            return {}
        
        somePreferencesHolder = fEvalString( self.vPreferencesHolder)
            
        somePreferencesHolder[ thePreferencesName] = thePreferencesHolder
        
        somePreferencesHolderString = fReprAsString( somePreferencesHolder)
        
        self.vPreferencesHolder = somePreferencesHolderString
        
        return self
            
                 
        
    security.declarePrivate( 'fGetPreferencesCopy')
    def fGetPreferencesCopy(self, theContextualObject, thePreferencesName):
        
        if not thePreferencesName:
            return None
        
        unPreferencesHolder = self._fGetPreferencesHolder( theContextualObject, thePreferencesName)
        if unPreferencesHolder == None:
            return None
        
        unPreferencesCopy = unPreferencesHolder.copy()
        return unPreferencesCopy
    
          

    
        
    security.declarePrivate( 'fGetPreferenceValue')
    def fGetPreferenceValue(self, theContextualObject, thePreferencesName, thePropertyName):
        
        if ( not thePreferencesName) or ( not thePropertyName):
            return None

        #if not ( thePropertyName in cPreferenceNames):
            #return None

        unPreferencesHolder = self._fGetPreferencesHolder( theContextualObject, thePreferencesName)
        if unPreferencesHolder == None:
            return None
        
        unSentinel = object()
        unPropertyValue = unPreferencesHolder.get( thePropertyName, unSentinel)
        if unPropertyValue == unSentinel:
            return None
        
        return unPropertyValue
  
  
    
        
    security.declarePrivate( 'fSetPreferenceValue')
    def fSetPreferenceValue(self, theContextualObject, thePreferencesName, thePropertyName, thePropertyValue):
        
        if ( not thePreferencesName) or ( not thePropertyName):
            return False
        
        #if not ( thePropertyName in cPreferenceNames):
            #return None
        
        unPreferencesHolder = self._fGetPreferencesHolder( theContextualObject, thePreferencesName)
        if unPreferencesHolder == None:
            return False
        
        unSentinel = object()
        unCurrentPropertyValue = unPreferencesHolder.get( thePropertyName, unSentinel)
        if unCurrentPropertyValue == unSentinel:
            return False
        
        if unCurrentPropertyValue == thePropertyValue:
            return False
        
        unPreferencesHolder[ thePropertyName] = thePropertyValue
        
        self._pPutPreferencesHolder( theContextualObject, thePreferencesName, unPreferencesHolder, )
        
        return True
    
    
    
               
        
               
        
    security.declarePrivate( 'fUpdatePreferences')
    def fUpdatePreferences(self, theContextualObject, thePreferencesName, thePreferencesChanges):
        """Must be invoked from  within a thread-safe protected critical section, in the same critical section where current preference values where retrived with fGetPreferencesCopy to compare with and known whether if any parameter was changed by the user and the preferences needs updating.
        
        """
        if not thePreferencesName:
            return False
        
        if not thePreferencesChanges:
            return False
        
        unPreferencesHolder = self._fGetPreferencesHolder( theContextualObject, thePreferencesName)
        if unPreferencesHolder == None:
            return False
        
        aThereIsChange = False
        
        aSentinel = object()
        
        for aKey in thePreferencesChanges.keys():

            aValue = thePreferencesChanges.get( aKey, aSentinel)
            if not ( aValue == aSentinel):
                aCurrentValue = unPreferencesHolder.get( aKey, aSentinel)
                if ( aCurrentValue == aSentinel) or not ( aValue == aCurrentValue):
                    unPreferencesHolder[ aKey] = aValue
                    aThereIsChange = True
                    
        if aThereIsChange:
            self._pPutPreferencesHolder( theContextualObject, thePreferencesName, unPreferencesHolder, )
        
        return aThereIsChange
                                                  
               
        
               
        
    security.declarePrivate( 'fGetAllPreferencesCopy')
    def fGetAllPreferencesCopy(self, theContextualObject, ):
        
        unAllPreferencesCopy = {
            #cAllPreferencesPpty_IsCachingActive:               self.vIsCachingActive == True,
            #cAllPreferencesPpty_PeersToNotify:                 ( self.vPeersToNotify                 or '')[:],
            #cAllPreferencesPpty_IdentificationStringForPeers:  ( self.vIdentificationStringForPeers  or '')[:],
            #cAllPreferencesPpty_AuthenticationStringForPeers:  ( self.vAuthenticationStringForPeers  or '')[:],
            #cAllPreferencesPpty_AuthenticationStringFromPeers: ( self.vAuthenticationStringFromPeers or '')[:],
        }
        return unAllPreferencesCopy
    
    

    
        
    security.declarePrivate( 'fGetAllPreferencesParameterValue')
    def fGetAllPreferencesParameterValue(self, theContextualObject, thePropertyName):
        
        if not thePropertyName:
            return None

        if not ( thePropertyName in cAllPreferencesPptyNames):
            return None

        #if thePropertyName == cAllPreferencesPpty_IsCachingActive:
            #return self.vIsCachingActive == True
            
        #if thePropertyName == cAllPreferencesPpty_PeersToNotify:
            #return self.vPeersToNotify
            
        #if thePropertyName == cAllPreferencesPpty_IdentificationStringForPeers:
            #return self.vIdentificationStringForPeers
            
        #if thePropertyName == cAllPreferencesPpty_AuthenticationStringForPeers:
            #return self.vAuthenticationStringForPeers
            
        #if thePropertyName == cAllPreferencesPpty_AuthenticationStringFromPeers:
            #return self.vAuthenticationStringFromPeers
         
        return None
  
    
    
        
    security.declarePrivate( 'fSetAllPreferencesParameterValue')
    def fSetAllPreferencesParameterValue(self, theContextualObject, thePropertyName, thePropertyValue):
        
        if not thePropertyName:
            return False
        
        if not ( thePropertyName in cAllPreferencesPptyNames):
            return False
        
        #if thePropertyName == cAllPreferencesPpty_IsCachingActive:
            #if not ( thePropertyValue == self.vIsCachingActive):
                #self.vIsCachingActive = thePropertyValue
                #return True
                
        #if thePropertyName == cAllPreferencesPpty_PeersToNotify:
            #if not ( thePropertyValue == self.vPeersToNotify):
                #self.vPeersToNotify = thePropertyValue
                #return True
                
        #if thePropertyName == cAllPreferencesPpty_IdentificationStringForPeers:
            #if not ( thePropertyValue == self.vIdentificationStringForPeers):
                #self.vIdentificationStringForPeers = thePropertyValue
                #return True
                
        #if thePropertyName == cAllPreferencesPpty_AuthenticationStringForPeers:
            #if not ( thePropertyValue == self.vAuthenticationStringForPeers):
                #self.vAuthenticationStringForPeers = thePropertyValue
                #return True
                
        #if thePropertyName == cAllPreferencesPpty_AuthenticationStringFromPeers:
            #if not ( thePropertyValue == self.vAuthenticationStringFromPeers):
                #self.vAuthenticationStringFromPeers = thePropertyValue
                #return True
                    
        return False
    
        
    
    
    
    
    
              
    security.declarePrivate( 'fUpdateAllPreferences')
    def fUpdateAllPreferences(self, theContextualObject, thePreferencesChanges):
        """Must be invoked from within a thread-safe protected critical section, in the same critical section where current configuration values where retrived with fGetPreferencesCopy to compare with and known wheter if any parameter was changed by the user and the config needs updating.
        
        """
        if not thePreferencesChanges:
            return False
        
        aSentinel = object()
        
        aThereIsChange = False
        
        for aKey in thePreferencesChanges.keys():
            pass
            #if aKey == cAllPreferencesPpty_IsCachingActive:
                #aValue = thePreferencesChanges.get( aKey, aSentinel)
                #if not ( aValue == aSentinel):
                    #if not ( aValue == self.vIsCachingActive):
                        #self.vPeersToNotify = aValue
                        #aThereIsChange = True
                    
            #if aKey == cAllPreferencesPpty_PeersToNotify:
                #aValue = thePreferencesChanges.get( aKey, aSentinel)
                #if not ( aValue == aSentinel):
                    #if not ( aValue == self.vPeersToNotify):
                        #self.vPeersToNotify = aValue
                        #aThereIsChange = True
                    
            #if aKey == cAllPreferencesPpty_IdentificationStringForPeers:
                #aValue = thePreferencesChanges.get( aKey, aSentinel)
                #if not ( aValue == aSentinel):
                    #if not ( aValue == self.vIdentificationStringForPeers):
                        #self.vIdentificationStringForPeers = aValue
                        #aThereIsChange = True
                    
            #if aKey == cAllPreferencesPpty_AuthenticationStringForPeers:
                #aValue = thePreferencesChanges.get( aKey, aSentinel)
                #if not ( aValue == aSentinel):
                    #if not ( aValue == self.vAuthenticationStringForPeers):
                        #self.vAuthenticationStringForPeers = aValue
                        #aThereIsChange = True
                    
            #if aKey == cAllPreferencesPpty_AuthenticationStringFromPeers:
                #aValue = thePreferencesChanges.get( aKey, aSentinel)
                #if not ( aValue == aSentinel):
                    #if not ( aValue == self.vAuthenticationStringFromPeers):
                        #self.vAuthenticationStringFromPeers = aValue
                        #aThereIsChange = True

        return aThereIsChange
                                                  

        
    
    
    
      
    


    
    