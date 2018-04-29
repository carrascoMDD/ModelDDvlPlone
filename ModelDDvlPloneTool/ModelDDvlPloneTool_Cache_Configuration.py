# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_Configuration.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Model Driven Development sl and Antonio Carrasco Valero
#
# GNU General Public License (GPL)
#anElementUIDModulus
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


import cgi 

import sys
import traceback

import logging


from AccessControl import ClassSecurityInfo



from Products.CMFCore import permissions


from ModelDDvlPloneTool_CacheConstants          import *

from MDDStringConversions                       import *







# #######################################################
# #######################################################



    
class ModelDDvlPloneTool_Cache_Configuration:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the configuration of cache operation parameters.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    




    
    
    # #############################################################
    """Metainformation about Cache configuration parameters.
    
    """

    security.declarePrivate( 'fCacheConfigurationMetaInfo')
    def fCacheConfigurationMetaInfo(self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        

        
        aMetaInfo = None
        if theCacheName == cCacheName_ElementIndependent:                
            aMetaInfo = {
                'MaxCharsCached': {
                    'minimum':      fStrGrp( cMaxCharsCached_ElementIndependent_MinValue),
                    'maximum':      fStrGrp( cMaxCharsCached_ElementIndependent_MaxValue),
                    'default':      fStrGrp( cMaxCharsCached_ElementIndependent_Default),
                },
                'ExpireAfterSeconds': {
                    'minimum':      fStrGrp(  cExpireAfterSeconds_MinValue),
                    'minimum_w':    fStrTime( cExpireAfterSeconds_MinValue),
                    'default':      fStrGrp(  cExpireAfterSeconds_ElementIndependent_Default),
                    'default_w':    fStrTime( cExpireAfterSeconds_ElementIndependent_Default),
                },
                'MinThresholdCharsToRelease': {
                    'default':      fStrGrp( cMinThresholdCharsToRelease_ElementIndependent_Default),
                },
                'DisplayCacheHitInformation': {
                    'default':      cDisplayCacheHitInformation_ElementIndependent_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_InspectCache_DisplayCacheHitInformation_%s' % cDisplayCacheHitInformation_ElementIndependent_Default, cDisplayCacheHitInformation_ElementIndependent_Default),
                },
                'ForceExpire': {
                    'default':             cForceExpire_ElementIndependent_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_%s' % str ( cForceExpire_ElementIndependent_Default == True), str( cForceExpire_ElementIndependent_Default)),
                },
                'CacheDiskEnabled': {
                    'default':             cCacheDiskEnabled_ElementIndependent_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_%s' % str ( cCacheDiskEnabled_ElementIndependent_Default == True), str( cCacheDiskEnabled_ElementIndependent_Default)),
                },
                'CacheDiskPath': {
                    'default':             cCacheDiskPath_ElementIndependent_Default,
                },
                'ExpireDiskAfterSeconds': {
                    'minimum':      fStrGrp(  cExpireDiskAfterSeconds_MinValue),
                    'minimum_w':    fStrTime( cExpireDiskAfterSeconds_MinValue),
                    'default':      fStrGrp(  cExpireDiskAfterSeconds_ElementIndependent_Default),
                    'default_w':    fStrTime( cExpireDiskAfterSeconds_ElementIndependent_Default),
                },
            }
        elif theCacheName == cCacheName_ForElements:                
            aMetaInfo = {
                'MaxCharsCached': {
                    'minimum':      fStrGrp( cMaxCharsCached_ForElements_MinValue),
                    'maximum':      fStrGrp( cMaxCharsCached_ForElements_MaxValue),
                    'default':      fStrGrp( cMaxCharsCached_ForElements_Default),
                },
                'ExpireAfterSeconds': {
                    'minimum':      fStrGrp(  cExpireAfterSeconds_MinValue),
                    'minimum_w':    fStrTime( cExpireAfterSeconds_MinValue),
                    'default':      fStrGrp(  cExpireAfterSeconds_ForElements_Default),
                    'default_w':    fStrTime( cExpireAfterSeconds_ForElements_Default),
                },
                'MinThresholdCharsToRelease': {
                    'default':      fStrGrp( cMinThresholdCharsToRelease_ForElements_Default),
                },
                'DisplayCacheHitInformation': {
                    'default':      cDisplayCacheHitInformation_ForElements_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_InspectCache_DisplayCacheHitInformation_%s' % cDisplayCacheHitInformation_ForElements_Default, cDisplayCacheHitInformation_ForElements_Default),
                },
                'ForceExpire': {
                    'default':             cForceExpire_ForElements_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_%s' % str ( cForceExpire_ForElements_Default == True), str( cForceExpire_ForElements_Default)),
                },
                'CacheDiskEnabled': {
                    'default':             cCacheDiskEnabled_ForElements_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_%s' % str ( cCacheDiskEnabled_ForElements_Default == True), str( cCacheDiskEnabled_ForElements_Default)),
                },
                'CacheDiskPath': {
                    'default':             cCacheDiskPath_ForElements_Default,
                },
                'ExpireDiskAfterSeconds': {
                    'minimum':      fStrGrp(  cExpireDiskAfterSeconds_MinValue),
                    'minimum_w':    fStrTime( cExpireDiskAfterSeconds_MinValue),
                    'default':      fStrGrp(  cExpireDiskAfterSeconds_ForElements_Default),
                    'default_w':    fStrTime( cExpireDiskAfterSeconds_ForElements_Default),
                },
            }
        elif theCacheName == cCacheName_ForUsers:                
            aMetaInfo = {
                'MaxCharsCached': {
                    'minimum':      fStrGrp( cMaxCharsCached_ForUsers_MinValue),
                    'maximum':      fStrGrp( cMaxCharsCached_ForUsers_MaxValue),
                    'default':      fStrGrp( cMaxCharsCached_ForUsers_Default),
                },
                'ExpireAfterSeconds': {
                    'minimum':      fStrGrp(  cExpireAfterSeconds_MinValue),
                    'minimum_w':    fStrTime( cExpireAfterSeconds_MinValue),
                    'default':      fStrGrp(  cExpireAfterSeconds_ForUsers_Default),
                    'default_w':    fStrTime( cExpireAfterSeconds_ForUsers_Default),
                },
                'MinThresholdCharsToRelease': {
                    'default':      fStrGrp( cMinThresholdCharsToRelease_ForUsers_Default),
                },
                'DisplayCacheHitInformation': {
                    'default':      cDisplayCacheHitInformation_ForUsers_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_InspectCache_DisplayCacheHitInformation_%s' % cDisplayCacheHitInformation_ForUsers_Default, cDisplayCacheHitInformation_ForUsers_Default),
                },
                'ForceExpire': {
                    'default':             cForceExpire_ForUsers_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_%s' % str ( cForceExpire_ForUsers_Default == True), str( cForceExpire_ForUsers_Default)),
                },
                'CacheDiskEnabled': {
                    'default':             cCacheDiskEnabled_ForUsers_Default,
                    'default_translation': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_%s' % str ( cCacheDiskEnabled_ForUsers_Default == True), str( cCacheDiskEnabled_ForUsers_Default)),
                },
                'CacheDiskPath': {
                    'default':             cCacheDiskPath_ForUsers_Default,
                },
                'ExpireDiskAfterSeconds': {
                    'minimum':      fStrGrp(  cExpireDiskAfterSeconds_MinValue),
                    'minimum_w':    fStrTime( cExpireDiskAfterSeconds_MinValue),
                    'default':      fStrGrp(  cExpireDiskAfterSeconds_ForUsers_Default),
                    'default_w':    fStrTime( cExpireDiskAfterSeconds_ForUsers_Default),
                },
            }
        return aMetaInfo.copy()
        
        
        
        


    # #############################################################
    """To supply to ModelDDvlPloneTool the cache configs for initialization of a new tool instance.
    
    """

    
     

    security.declarePrivate( 'fInitialCacheConfigs')
    def fInitialCacheConfigs(self, ):
        """Used by instances of MDDModelDDvlPlone_tool to initialize the CacheConfigsHolder.
        
        """

        someCacheConfigs = [ ]
        
        someCacheConfigs.append( {
            cCacheConfigPpty_Name:                         cCacheName_ElementIndependent,
            cCacheConfigPpty_Kind:                         cCacheKind_ElementIndependent,
            cCacheConfigPpty_CacheEnabled:                 cCacheEnabled_ElementIndependent_Default,
            cCacheConfigPpty_MaxCharsCached:               cMaxCharsCached_ElementIndependent_Default,
            cCacheConfigPpty_MinThresholdCharsToRelease:   cMinThresholdCharsToRelease_ElementIndependent_Default,
            cCacheConfigPpty_DisplayCacheHitInformation:   cDisplayCacheHitInformation_ElementIndependent_Default,
            cCacheConfigPpty_ExpireAfterSeconds:           cExpireAfterSeconds_ElementIndependent_Default,
            cCacheConfigPpty_ForceExpire:                  cForceExpire_ElementIndependent_Default,
            cCacheConfigPpty_CacheDiskEnabled:             cCacheDiskEnabled_ElementIndependent_Default,
            cCacheConfigPpty_CacheDiskPath:                cCacheDiskPath_ElementIndependent_Default,
            cCacheConfigPpty_ExpireDiskAfterSeconds:       cExpireDiskAfterSeconds_ElementIndependent_Default,
        })
        
        someCacheConfigs.append( {
            cCacheConfigPpty_Name:                         cCacheName_ForElements,
            cCacheConfigPpty_Kind:                         cCacheKind_ForElements,
            cCacheConfigPpty_CacheEnabled:                 cCacheEnabled_ForElements_Default,
            cCacheConfigPpty_MaxCharsCached:               cMaxCharsCached_ForElements_Default,
            cCacheConfigPpty_MinThresholdCharsToRelease:   cMinThresholdCharsToRelease_ForElements_Default,
            cCacheConfigPpty_DisplayCacheHitInformation:   cDisplayCacheHitInformation_ForElements_Default,            
            cCacheConfigPpty_ExpireAfterSeconds:           cExpireAfterSeconds_ForElements_Default,
            cCacheConfigPpty_ForceExpire:                  cForceExpire_ForElements_Default,
            cCacheConfigPpty_CacheDiskEnabled:             cCacheDiskEnabled_ForElements_Default,
            cCacheConfigPpty_CacheDiskPath:                cCacheDiskPath_ForElements_Default,
            cCacheConfigPpty_ExpireDiskAfterSeconds:       cExpireDiskAfterSeconds_ForElements_Default,
        })
        
        someCacheConfigs.append( {
            cCacheConfigPpty_Name:                         cCacheName_ForUsers,
            cCacheConfigPpty_Kind:                         cCacheKind_ForUsers,
            cCacheConfigPpty_CacheEnabled:                 cCacheEnabled_ForUsers_Default,
            cCacheConfigPpty_MaxCharsCached:               cMaxCharsCached_ForUsers_Default,
            cCacheConfigPpty_MinThresholdCharsToRelease:   cMinThresholdCharsToRelease_ForUsers_Default,
            cCacheConfigPpty_DisplayCacheHitInformation:   cDisplayCacheHitInformation_ForUsers_Default,            
            cCacheConfigPpty_ExpireAfterSeconds:           cExpireAfterSeconds_ForUsers_Default,
            cCacheConfigPpty_ForceExpire:                  cForceExpire_ForUsers_Default,
            cCacheConfigPpty_CacheDiskEnabled:             cCacheDiskEnabled_ForUsers_Default,
            cCacheConfigPpty_CacheDiskPath:                cCacheDiskPath_ForUsers_Default,
            cCacheConfigPpty_ExpireDiskAfterSeconds:       cExpireDiskAfterSeconds_ForUsers_Default,
        })
        return someCacheConfigs
    
    
    
    
    


 

    
    
    
    
    
    
    # #############################################################
    """Access to the configuration parameters held by ModelDDvlPloneTool persistent singleton.
    
    """
    
    
        
    security.declarePrivate( 'fGetCacheConfigCopy')
    def fGetCacheConfigCopy(self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        
        if not theCacheName:
            return False
        
        if not theModelDDvlPloneTool:
            return None
        
        aCacheConfigCopy = theModelDDvlPloneTool.fGetCacheConfigCopy( theContextualObject, theCacheName)
        if not aCacheConfigCopy:
            return None

        return aCacheConfig
    
     
        
    

    
    
    def fGetAllCachesConfigParameter_IsCachingActive( self, theModelDDvlPloneTool, theContextualObject,):
        if not theModelDDvlPloneTool:
            return False
        
        return theModelDDvlPloneTool.fGetAllCachesConfigParameterValue( theContextualObject, cAllCachesConfigPpty_IsCachingActive)
    
    
    def fSetAllCachesConfigparameter_IsCachingActive( self, theModelDDvlPloneTool, theContextualObject, theCachingIsActive):
        if not theModelDDvlPloneTool:
            return False
        
        return theModelDDvlPloneTool.fSetAllCachesConfigParameterValue( theContextualObject, cAllCachesConfigPpty_IsCachingActive, theCachingIsActive)
        
    
    
    
    def fGetCacheConfigKind( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        if not theModelDDvlPloneTool:
            return False
        
        return theModelDDvlPloneTool.fGetCacheConfigParameterValue( theContextualObject, theCacheName, cCacheConfigPpty_Kind)
    
    
       
    def fGetCacheConfigParameter_CacheEnabled( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        if not theModelDDvlPloneTool:
            return False
        
        return theModelDDvlPloneTool.fGetCacheConfigParameterValue( theContextualObject, theCacheName, cCacheConfigPpty_CacheEnabled)
    
       
    
    def fGetCacheConfigParameter_CacheDiskPath( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        if not theModelDDvlPloneTool:
            return False
        
        return theModelDDvlPloneTool.fGetCacheConfigParameterValue( theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskPath)
    
        
    
    def fSetCacheConfigParameter_CacheEnabled( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theCacheEnabled):
        if not theModelDDvlPloneTool:
            return False
        
        return theModelDDvlPloneTool.fSetCacheConfigParameterValue( theContextualObject, theCacheName, cCacheConfigPpty_CacheEnabled, theCacheEnabled)
    
    
    
    def fGetCacheConfigParameter_ForceExpire( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        if not theModelDDvlPloneTool:
            return False
        
        return theModelDDvlPloneTool.fGetCacheConfigParameterValue( theContextualObject, theCacheName, cCacheConfigPpty_ForceExpire)
    
         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

            
        

    
    
    security.declarePrivate( 'fEditCacheParameters')
    def fEditCacheParameters(self, theModelDDvlPloneTool, theContextualObject, theEditedCacheParameters, theCacheName):
        """Initiated by a User with ManagePortal persmission, Set parameters controlling the maximum amount of memory available to store cached templates, and other controls on the behavior of the cache.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
                
        if theContextualObject == None:
            return [ False, 'Edit', theCacheName,]
        
        if theModelDDvlPloneTool == None:
            return [ False, 'Edit', theCacheName,]
        
        if not theEditedCacheParameters:
            return [ False, 'Edit', theCacheName,]
        
        unSentinel = object()
        
        aCacheConfigHasChanged = False
 
        # ###########################################################
        """Change cache configuration parameters, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if not theCacheName:
                # ###########################################################
                """Configuration parameters affecting all the caches.
                
                """
                
                aCurrentAllCachesConfigCopy = theModelDDvlPloneTool.fGetAllCachesConfigCopy( theContextualObject)
                if not aCurrentAllCachesConfigCopy:
                    return [ False, 'Edit', theCacheName,]
                
                unosConfigChanges = { }
             
                if theEditedCacheParameters.has_key( 'thePeersToNotify'):
                    unParameterValue = theEditedCacheParameters.get( 'thePeersToNotify', unSentinel)
                    if not ( unParameterValue == unSentinel):
                        
                        if not isinstance( unParameterValue, str) and not isinstance( unParameterValue, unicode):
                            unParameterValue = str( unParameterValue)
                            
                        aCurrentParameterValue = aCurrentAllCachesConfigCopy.get( cAllCachesConfigPpty_PeersToNotify, unSentinel)
 
                        if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                            unosConfigChanges[ cAllCachesConfigPpty_PeersToNotify] = unParameterValue
                                    
                
                if theEditedCacheParameters.has_key( 'theIdentificationStringForPeers'):
                    unParameterValue = theEditedCacheParameters.get( 'theIdentificationStringForPeers', unSentinel)
                    if not ( unParameterValue == unSentinel):
                                
                        if not isinstance( unParameterValue, str) and not isinstance( unParameterValue, unicode):
                            unParameterValue = str( unParameterValue)
                            
                        aCurrentParameterValue = aCurrentAllCachesConfigCopy.get( cAllCachesConfigPpty_IdentificationStringForPeers, unSentinel)
 
                        if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                            unosConfigChanges[ cAllCachesConfigPpty_IdentificationStringForPeers] = unParameterValue
                                    
                
                
                if theEditedCacheParameters.has_key( 'theAuthenticationStringForPeers'):
                    unParameterValue = theEditedCacheParameters.get( 'theAuthenticationStringForPeers', unSentinel)
                    if not ( unParameterValue == unSentinel):
                                
                        if not isinstance( unParameterValue, str) and not isinstance( unParameterValue, unicode):
                            unParameterValue = str( unParameterValue)
                            
                        aCurrentParameterValue = aCurrentAllCachesConfigCopy.get( cAllCachesConfigPpty_AuthenticationStringForPeers, unSentinel)
 
                        if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                            unosConfigChanges[ cAllCachesConfigPpty_AuthenticationStringForPeers] = unParameterValue
                                    
                
                if theEditedCacheParameters.has_key( 'theAuthenticationStringFromPeers'):
                    unParameterValue = theEditedCacheParameters.get( 'theAuthenticationStringFromPeers', unSentinel)
                    if not ( unParameterValue == unSentinel):
                                
                        if not isinstance( unParameterValue, str) and not isinstance( unParameterValue, unicode):
                            unParameterValue = str( unParameterValue)
                            
                        aCurrentParameterValue = aCurrentAllCachesConfigCopy.get( cAllCachesConfigPpty_AuthenticationStringFromPeers, unSentinel)
 
                        if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                            unosConfigChanges[ cAllCachesConfigPpty_AuthenticationStringFromPeers] = unParameterValue
                                        
                if not unosConfigChanges:
                    return [ False, 'Edit', theCacheName,]
                
                aCacheConfigHasChanged = theModelDDvlPloneTool.fUpdateAllCachesConfig( theContextualObject, unosConfigChanges)
                return [ aCacheConfigHasChanged, 'Edit', theCacheName,]
                
            else:
            
                aCurrentCacheConfigCopy = theModelDDvlPloneTool.fGetCacheConfigCopy( theContextualObject, theCacheName)
                if not aCurrentCacheConfigCopy:
                    return [ False, 'Edit', theCacheName,]
                
                unosConfigChanges = { }
                
                if theEditedCacheParameters.has_key( 'theMaxCharsCached'):
                    unParameterValueString = theEditedCacheParameters.get( 'theMaxCharsCached', unSentinel)
                    if not ( unParameterValueString == unSentinel):
                        unParameterValue = unSentinel
                        try:
                            unParameterValue = int( unParameterValueString)
                        except:
                            None
                        if not ( unParameterValue == unSentinel):
                            if ( unParameterValue >= cMaxCharsCached_ForElements_MinValue) and ( unParameterValue <= cMaxCharsCached_ForElements_MaxValue):
                                
                                aCurrentParameterValue = aCurrentCacheConfigCopy.get( cCacheConfigPpty_MaxCharsCached, unSentinel)
                                if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                                    unosConfigChanges[ cCacheConfigPpty_MaxCharsCached] = unParameterValue
                                    
                                    
                if theEditedCacheParameters.has_key( 'theMinThresholdCharsToRelease'):
                    unParameterValueString = theEditedCacheParameters.get( 'theMinThresholdCharsToRelease', unSentinel)
                    if not ( unParameterValueString == unSentinel):
                        unParameterValue = unSentinel
                        try:
                            unParameterValue = int( unParameterValueString)
                        except:
                            None
                        if not ( unParameterValue == unSentinel):
                            aCurrentParameterValue = aCurrentCacheConfigCopy.get( cCacheConfigPpty_MinThresholdCharsToRelease, unSentinel)
                            if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                                unosConfigChanges[ cCacheConfigPpty_MinThresholdCharsToRelease] = unParameterValue
                
                                
                                    
                if theEditedCacheParameters.has_key( 'theExpireAfterSeconds'):
                    unParameterValueString = theEditedCacheParameters.get( 'theExpireAfterSeconds', unSentinel)
                    if not ( unParameterValueString == unSentinel):
                        unParameterValue = unSentinel
                        try:
                            unParameterValue = int( unParameterValueString)
                        except:
                            None
                        if not ( unParameterValue == unSentinel):
                            if ( unParameterValue >= cExpireAfterSeconds_MinValue):
                                
                                aCurrentParameterValue = aCurrentCacheConfigCopy.get( cCacheConfigPpty_ExpireAfterSeconds, unSentinel)
                                if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                                    unosConfigChanges[ cCacheConfigPpty_ExpireAfterSeconds] = unParameterValue
                                
                                    
                                    
                if theEditedCacheParameters.has_key( 'theForceExpire'):
                    unParameterValueString = theEditedCacheParameters.get( 'theForceExpire', unSentinel)
                    if not ( unParameterValueString == unSentinel):
                            
                        unParameterValue = unParameterValueString.lower() == str( True).lower()
                        
                        unMustSet = False
                        aCurrentParameterValue = aCurrentCacheConfigCopy.get( cCacheConfigPpty_ForceExpire, unSentinel)
                        if ( aCurrentParameterValue == unSentinel):
                            unMustSet = True
                        else:                            
                            if not ( unParameterValue == aCurrentParameterValue):
                                unMustSet = True
                        
                        if unMustSet:
                            unosConfigChanges[ cCacheConfigPpty_ForceExpire] = unParameterValue
                            
                                 
                if theEditedCacheParameters.has_key( 'theDisplayCacheHitInformation'):
                    unParameterValueString = theEditedCacheParameters.get( 'theDisplayCacheHitInformation', unSentinel)
                    if not ( unParameterValueString == unSentinel):
                        
                        if unParameterValueString in cDisplayCacheHitInformation_Vocabulary:
                            
                            aCurrentParameterValueString = aCurrentCacheConfigCopy.get( cCacheConfigPpty_DisplayCacheHitInformation, unSentinel)
                            if ( aCurrentParameterValueString == unSentinel) or not ( unParameterValueString == aCurrentParameterValueString):
                                unosConfigChanges[ cCacheConfigPpty_DisplayCacheHitInformation] = unParameterValueString
                 
                                
                                
                                    
                                    
                if theEditedCacheParameters.has_key( 'theCacheDiskEnabled'):
                    unParameterValueString = theEditedCacheParameters.get( 'theCacheDiskEnabled', unSentinel)
                    if not ( unParameterValueString == unSentinel):
                            
                        unParameterValue = unParameterValueString.lower() == str( True).lower()
                        
                        unMustSet = False
                        aCurrentParameterValue = aCurrentCacheConfigCopy.get( cCacheConfigPpty_CacheDiskEnabled, unSentinel)
                        if ( aCurrentParameterValue == unSentinel):
                            unMustSet = True
                        else:                            
                            if not ( unParameterValue == aCurrentParameterValue):
                                unMustSet = True
                        
                        if unMustSet:
                            unosConfigChanges[ cCacheConfigPpty_CacheDiskEnabled] = unParameterValue
                            
                                    
                                
                                    
                                    
                if theEditedCacheParameters.has_key( 'theCacheDiskPath'):
                    unParameterValue = theEditedCacheParameters.get( 'theCacheDiskPath', unSentinel)
                    if not ( unParameterValue == unSentinel):
                                
                        if not isinstance( unParameterValue, str) and not isinstance( unParameterValue, unicode):
                            unParameterValue = str( unParameterValue)
                            
                        aCurrentParameterValue = aCurrentCacheConfigCopy.get( cCacheConfigPpty_CacheDiskPath, unSentinel)
 
                        if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                            unosConfigChanges[ cCacheConfigPpty_CacheDiskPath] = unParameterValue
                                    
                                
                                
                                    
                if theEditedCacheParameters.has_key( 'theExpireDiskAfterSeconds'):
                    unParameterValueString = theEditedCacheParameters.get( 'theExpireDiskAfterSeconds', unSentinel)
                    if not ( unParameterValueString == unSentinel):
                        unParameterValue = unSentinel
                        try:
                            unParameterValue = int( unParameterValueString)
                        except:
                            None
                        if not ( unParameterValue == unSentinel):
                            if ( unParameterValue >= cExpireDiskAfterSeconds_MinValue):
                                
                                aCurrentParameterValue = aCurrentCacheConfigCopy.get( cCacheConfigPpty_ExpireDiskAfterSeconds, unSentinel)
                                if ( aCurrentParameterValue == unSentinel) or not ( unParameterValue == aCurrentParameterValue):
                                    unosConfigChanges[ cCacheConfigPpty_ExpireDiskAfterSeconds] = unParameterValue
                                
                                    
                                
                                
                if not unosConfigChanges:
                    return [ False, 'Edit', theCacheName,]
                
                aCacheConfigHasChanged = theModelDDvlPloneTool.fUpdateCacheConfig( theContextualObject, theCacheName, unosConfigChanges)
                return [ aCacheConfigHasChanged, 'Edit', theCacheName,]
            
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if aCacheConfigHasChanged:
                
                aModelDDvlPloneTool_Transactions = theModelDDvlPloneTool.fModelDDvlPloneTool_Transactions( theContextualObject)
                if not ( aModelDDvlPloneTool_Transactions == None):
                    aModelDDvlPloneTool_Transactions.fTransaction_Commit()
   
        return [ False, 'Edit', theCacheName,]
    
    
    
        
    
    
    
    
    
    

        
        
        
    
    
    security.declarePrivate( 'fConfigureTemplatesCache')
    def fConfigureTemplatesCache(self, theModelDDvlPloneTool, theContextualObject, theEditedCacheParameters, theCacheName):
        """Initiated by a User with ManagePortal persmission, Set parameters controlling the maximum amount of memory available to store cached templates, and other controls on the behavior of the cache.
        
        """
        
        unSentinel = object()

        unResetCacheParameter = theEditedCacheParameters.get( 'theResetCache', unSentinel)
        if not ( unResetCacheParameter == unSentinel):
            if unResetCacheParameter == 'on':
                return [ self.fResetCache(    theModelDDvlPloneTool, theContextualObject,), 'Reset', 'All',]
                
            
        unDeactivateCacheParameter = theEditedCacheParameters.get( 'theDeactivateCaching', unSentinel)
        if not ( unDeactivateCacheParameter == unSentinel):
            if unDeactivateCacheParameter == 'on':
                return [ self.fDeactivateCaching(    theModelDDvlPloneTool, theContextualObject,), 'Deactivate', 'All',]
            
                
        unActivateCacheParameter = theEditedCacheParameters.get( 'theActivateCaching', unSentinel)
        if not ( unActivateCacheParameter == unSentinel):
            if unActivateCacheParameter == 'on':
                return [ self.fActivateCaching(     theModelDDvlPloneTool, theContextualObject,), 'Activate',  'All',]
            
        
            
            
        if self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):

            unFlushCacheParameter = theEditedCacheParameters.get( 'theFlushCache', unSentinel)
            if not ( unFlushCacheParameter == unSentinel):
                if unFlushCacheParameter == 'on':
                    
                    unFlushDiskCacheParameter = theEditedCacheParameters.get( 'theFlushDiskCache', unSentinel)
                    unFlushDiskCache = ( not ( unFlushDiskCacheParameter == unSentinel)) and ( unFlushDiskCacheParameter == 'on')

                    return [ self.fFlushAllCachedTemplates(  theModelDDvlPloneTool, theContextualObject, theCacheName, theFlushDiskCache=unFlushDiskCache), ( unFlushDiskCache and 'Flush Disc') or 'Flush',  theCacheName,]
                

                    
            unDisableCacheParameter = theEditedCacheParameters.get( 'theDisableCache', unSentinel)
            if not ( unDisableCacheParameter == unSentinel):
                if unDisableCacheParameter == 'on':
                    return [ self.fDisableTemplatesCache(    theModelDDvlPloneTool, theContextualObject, theCacheName), 'Disable', theCacheName,]
                
                    
                    
            unEnableCacheParameter = theEditedCacheParameters.get( 'theEnableCache', unSentinel)
            if not ( unEnableCacheParameter == unSentinel):
                if unEnableCacheParameter == 'on':
                    return [ self.fEnableTemplatesCache(     theModelDDvlPloneTool, theContextualObject, theCacheName), 'Enable',  theCacheName,]
            
                
        return self.fEditCacheParameters( theModelDDvlPloneTool, theContextualObject, theEditedCacheParameters, theCacheName)
                
            
    
    
    
        
    
    
    

    
    
    
    # #######################################################
    # #######################################################
    
    # #######################################################
    # #######################################################
    
        



    
    
        
    
    security.declarePrivate( 'fIsCachingActive')
    def fIsCachingActive(self, theModelDDvlPloneTool, theContextualObject):
        if cForbidCaches:
            return False
        
        if not theModelDDvlPloneTool:
            return False
        
 
        # ###########################################################
        """Change cache configuration parameters, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock_Unconditionally( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            unIsCachingActive = theModelDDvlPloneTool.fGetAllCachesConfigParameterValue( theContextualObject, cAllCachesConfigPpty_IsCachingActive)
            return unIsCachingActive
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock_Unconditionally( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return False
    
            
        
    
    
    
    
    
    security.declarePrivate( 'fIsCachingActive_NotThreadSafe')
    def fIsCachingActive_NotThreadSafe(self, theModelDDvlPloneTool, theContextualObject):
        if cForbidCaches:
            return False
        
        if not theModelDDvlPloneTool:
            return False
        
        unIsCachingActive = theModelDDvlPloneTool.fGetAllCachesConfigParameterValue( theContextualObject, cAllCachesConfigPpty_IsCachingActive)
        return unIsCachingActive
        
    
  
 
    
    security.declarePrivate( 'fResetCache')
    def fResetCache(self, theModelDDvlPloneTool, theContextualObject):
        """Initalize memory structures holding and controlling cache entries.
        
        """

        if theContextualObject == None:
            return False
        
        if theModelDDvlPloneTool == None:
            return False

        aLock  = None
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            aLock = theModelDDvlPloneTool.fgCacheMutex( theContextualObject)
            if aLock:
                aLock.acquire()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            from ModelDDvlPloneTool_Globals import ModelDDvlPloneTool_Globals, fgInitial_AllCacheGlobals
            
            allCacheGlobals = fgInitial_AllCacheGlobals()
            ModelDDvlPloneTool_Globals().pgGlobalsMutator( allCacheGlobals)
            
            aReseted = True
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if aLock:
                aLock.release()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return aReseted
        

    
        
    
    security.declarePrivate( 'fActivateCaching')
    def fActivateCaching(self, theModelDDvlPloneTool, theContextualObject):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future requests.
        
        """
        if theContextualObject == None:
            return False
        
        if theModelDDvlPloneTool == None:
            return False

        # ###########################################################
        """Activate caching of template redering result, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock_Unconditionally( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            aCurrentCacheActivated = self.fGetAllCachesConfigParameter_IsCachingActive( theModelDDvlPloneTool, theContextualObject,)
            if aCurrentCacheActivated:
                return False
            
            aCacheActivatedChanged = self.fSetAllCachesConfigparameter_IsCachingActive( theModelDDvlPloneTool, theContextualObject, True)
                 
                 
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock_Unconditionally( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return aCacheActivatedChanged
        

         
    
    
    
 
    
    security.declarePrivate( 'fDeactivateCaching')
    def fDeactivateCaching(self, theModelDDvlPloneTool, theContextualObject):
        """Do not Allow to store in memory the result of rendering templates, and save the effort of rendering in future requests.
        
        """

        if theContextualObject == None:
            return False
        
        if theModelDDvlPloneTool == None:
            return False

        # ###########################################################
        """Deactivate caching of template redering result, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock_Unconditionally( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            aCurrentCacheActivated = self.fGetAllCachesConfigParameter_IsCachingActive( theModelDDvlPloneTool, theContextualObject,)
            if not aCurrentCacheActivated:
                return False
            
            aCacheActivatedChanged = self.fSetAllCachesConfigparameter_IsCachingActive( theModelDDvlPloneTool, theContextualObject, False)
                 
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock_Unconditionally( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return aCacheActivatedChanged
        

    
    
            

    security.declarePrivate( 'fEnableTemplatesCache')
    def fEnableTemplatesCache(self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future requests.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        if not theCacheName:
            return False
        
        if theContextualObject == None:
            return False
        
        if theModelDDvlPloneTool == None:
            return False

        # ###########################################################
        """Enable caching of template redering result, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            aCurrentCacheEnabled = self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, theCacheName)
            if aCurrentCacheEnabled:
                return False
            
            aCacheEnabledChanged = self.fSetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, theCacheName, True)
                 
                 
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return aCacheEnabledChanged
        

         
    
           
        
    
    security.declarePrivate( 'fDisableTemplatesCache')
    def fDisableTemplatesCache(self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        """Do not Allow to store in memory the result of rendering templates, and save the effort of rendering in future requests.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        if not theCacheName:
            return False
        
        if theContextualObject == None:
            return False
        
        if theModelDDvlPloneTool == None:
            return False

        # ###########################################################
        """Disable caching of template redering result, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            aCurrentCacheEnabled = self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, theCacheName)
            if not aCurrentCacheEnabled:
                return False
            
            aCacheEnabledChanged = self.fSetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, theCacheName, False)
                 
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return aCacheEnabledChanged
        

    
    
                