# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_CacheConstants.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

import os

import sys
import traceback
import logging




from App.config import getConfiguration

from AccessControl import ClassSecurityInfo


from Products.CMFCore import permissions



from MDDLinkedList                              import MDDLinkedList, MDDLinkedNode

from MDDStringConversions import *


cMaxLenCacheEntryTitleDisplay = 48
cViewPostfix_NoHeaderNoFooter = '_NoHeaderNoFooter'


# #######################################################
"""Configuration of views that require private caches for qualified users.

"""
cPrivateCacheViewsForQualifiedUsers = [ 'Tabular', 'Tabular' + cViewPostfix_NoHeaderNoFooter,]





# #######################################################
"""Configuration of class behavior during development or quality assurance.

"""

cInDevelopment  = True

cLogExceptions  = True

        
cForbidCaches     = False
cForbidDiskCaches = False




cMinCached_HTMLFileLen  = 1



# #######################################################
"""Enumeration values for the type of the DisplayCacheHitInformation configuration property.

"""
cDisplayCacheHitInformation_None    = 'None'
cDisplayCacheHitInformation_Top     = 'Top'
cDisplayCacheHitInformation_Bottom  = 'Bottom'
cDisplayCacheHitInformation_Vocabulary = [ cDisplayCacheHitInformation_None, cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]





  
# #######################################################
"""Configuration of default and boundary values to control cache magnitude boundaries.

"""
 
cExpireAfterSeconds_MinValue                = 1 
cExpireDiskAfterSeconds_MinValue            = 1


cHTMLRenderingTimeComment_Keyword = """RenderMilliseconds="""

cHTMLFirstLinesChunkLen = 1024 # Surely, the rendering time comment fits here

cCacheDisk_UIDModulus = 100

cCacheDiskFilePostfix = '.html'

cCacheDisk_ElementIndependent_FolderCreateMode_Project   = 0777
cCacheDisk_ElementIndependent_FolderCreateMode_Language  = 0777
cCacheDisk_ElementIndependent_FileOpenReadMode_View      = 'rb'
cCacheDisk_ElementIndependent_FileOpenReadBuffering_View = 0
cCacheDisk_ElementIndependent_FileOpenWriteMode_View     = 'wb'
cCacheDisk_ElementIndependent_FileOpenWriteBuffering_View= 0
cCacheDisk_ElementIndependent_FileOpenTruncateMode_View     = 'wb'
cCacheDisk_ElementIndependent_FileOpenTruncateBuffering_View= 0


cCacheDisk_ForElements_FolderCreateMode_Project   = 0777
cCacheDisk_ForElements_FolderCreateMode_Language  = 0777
cCacheDisk_ForElements_FolderCreateMode_RootUID   = 077
cCacheDisk_ForElements_FolderCreateMode_ElementUIDModulus = 0777
cCacheDisk_ForElements_FolderCreateMode_ElementUID = 0777
cCacheDisk_ForElements_FileOpenReadMode_View      = 'rb'
cCacheDisk_ForElements_FileOpenReadBuffering_View = 0
cCacheDisk_ForElements_FileOpenWriteMode_View     = 'wb'
cCacheDisk_ForElements_FileOpenWriteBuffering_View= 0




cCacheDiskPath_Base_Default                 = os.path.join( getConfiguration().clienthome, 'mddcache')

cCacheEnabled_ElementIndependent_Default               = not cForbidCaches
cMinThresholdCharsToRelease_ElementIndependent_Default = 50 * 1000
cMaxCharsCached_ElementIndependent_Default             = 1000 * 1000
cMaxCharsCached_ElementIndependent_MinValue            = 1000
cMaxCharsCached_ElementIndependent_MaxValue            = 50 * 1000 * 1000
cDisplayCacheHitInformation_ElementIndependent_Default = ( cInDevelopment and cDisplayCacheHitInformation_Top) or cDisplayCacheHitInformation_None 
cExpireAfterSeconds_ElementIndependent_Default          = 30 * 24 * 3600 
cForceExpire_ElementIndependent_Default                = False
cCacheDiskEnabled_ElementIndependent_Default           = not cForbidDiskCaches
cCacheDiskPath_ElementIndependent_Default              = os.path.join( cCacheDiskPath_Base_Default, 'elein')   
cExpireDiskAfterSeconds_ElementIndependent_Default     = 365 * 24 * 3600 



cCacheEnabled_ForElements_Default                      = not cForbidCaches
cMinThresholdCharsToRelease_ForElements_Default        = 200 * 1000
cMaxCharsCached_ForElements_Default                    = 100 * 1000 * 1000
cMaxCharsCached_ForElements_MinValue                   = 1000
cMaxCharsCached_ForElements_MaxValue                   = 2 * 1000 * 1000 * 1000
cDisplayCacheHitInformation_ForElements_Default        = ( cInDevelopment and cDisplayCacheHitInformation_Top) or cDisplayCacheHitInformation_None 
cExpireAfterSeconds_ForElements_Default                = 1 * 24 * 3600 
cForceExpire_ForElements_Default                       = False
cCacheDiskEnabled_ForElements_Default                  = not cForbidDiskCaches
cCacheDiskPath_ForElements_Default                     = os.path.join( cCacheDiskPath_Base_Default, 'felem')   
cExpireDiskAfterSeconds_ForElements_Default            = 3 * 30 * 24 * 3600 



cCacheEnabled_ForUsers_Default                         = not cForbidCaches
cMinThresholdCharsToRelease_ForUsers_Default           = 200 * 1000
cMaxCharsCached_ForUsers_Default                       = 10 * 1000 * 1000
cMaxCharsCached_ForUsers_MinValue                      = 1000
cMaxCharsCached_ForUsers_MaxValue                      = 500 * 1000 * 1000
cDisplayCacheHitInformation_ForUsers_Default           = ( cInDevelopment and cDisplayCacheHitInformation_Top) or cDisplayCacheHitInformation_None 
cExpireAfterSeconds_ForUsers_Default                   = 4 * 3600
cForceExpire_ForUsers_Default                          = True
cCacheDiskEnabled_ForUsers_Default                     = not cForbidDiskCaches
cCacheDiskPath_ForUsers_Default                        = os.path.join( cCacheDiskPath_Base_Default, 'fuser')   
cExpireDiskAfterSeconds_ForUsers_Default               = 7 * 24 * 3600 









# #######################################################
"""Naive hack to simulate some kind or authentication upon reception from other ZEO clientes (or a networked broker), of a request to invalidate cache entries, given their corresponding element UID.

"""

cUnsecureCacheFlushAcknowledgedAuthenticationString = 'UnsecureCacheFlushAcknowledgedAuthenticationString'








# #######################################################
"""Names for the cache control structures: names, kinds and properties. A hack that could rather be implemented as classes. Implemented in this free-way because the approach shall eventually become fully meta-driven, and light control structures are easier to manufacture by the meta-layers for the runtime interpretation engine to consume.

"""




# #######################################################
"""Kinds of caches supported. Only two kinds: independent of any element, and bound to an element. Dispatches different cache hit algorithms, and constructs different control structures. Hard-coded, can not be open-ended by declaration of new cache kinds.

"""

cCacheKind_ElementIndependent = 'ElementIndependent' 
cCacheKind_ForElements        = 'ForElements'        
cCacheKind_ForUsers           = 'ForUsers'        

cCacheKindsSupported = [ 
    cCacheKind_ElementIndependent, 
    cCacheKind_ForElements, 
    cCacheKind_ForUsers, 
]


# #######################################################
"""Names of chaches to create upon startup. Caches of names different of these can be created afterwards (of one of the fixed list of kinds above).

"""

cCacheName_ElementIndependent = 'ElementIndependent' 
cCacheName_ForElements        = 'ForElements'    
cCacheName_ForUsers           = 'ForUsers'    

cCacheNamesForElementsOrUsers = [ cCacheName_ForElements, cCacheName_ForUsers,]
cCacheNamesAll                = [ cCacheName_ElementIndependent, cCacheName_ForElements, cCacheName_ForUsers,]

cCacheNamesAndKindsToCreate = [ 
    [ cCacheName_ElementIndependent, cCacheKind_ElementIndependent,],
    [ cCacheName_ForElements,        cCacheKind_ForElements,],
    [ cCacheName_ForUsers,           cCacheKind_ForUsers,],
]










# #######################################################
"""Names for the cache configuration properties.

"""
cAllCachesConfigPpty_IsCachingActive              = 'IsCachingActive'
cAllCachesConfigPpty_PeersToNotify                = 'PeersToNotify'
cAllCachesConfigPpty_IdentificationStringForPeers = 'IdentificationStringForPeers'
cAllCachesConfigPpty_AuthenticationStringForPeers = 'AuthenticationStringForPeers'
cAllCachesConfigPpty_AuthenticationStringFromPeers= 'AuthenticationStringFromPeers'
cAllCachesConfigPptyNames = [
    cAllCachesConfigPpty_IsCachingActive,              
    cAllCachesConfigPpty_PeersToNotify,                
    cAllCachesConfigPpty_IdentificationStringForPeers, 
    cAllCachesConfigPpty_AuthenticationStringForPeers, 
    cAllCachesConfigPpty_AuthenticationStringFromPeers,
]


cCacheConfigPpty_Name                       = 'Name'
cCacheConfigPpty_Kind                       = 'Kind'
cCacheConfigPpty_CacheEnabled               = 'CacheEnabled'
cCacheConfigPpty_MaxCharsCached             = 'MaxCharsCached'
cCacheConfigPpty_MinThresholdCharsToRelease = 'MinThresholdCharsToRelease'
cCacheConfigPpty_DisplayCacheHitInformation = 'DisplayCacheHitInformation'
cCacheConfigPpty_ExpireAfterSeconds         = 'ExpireAfterSeconds'
cCacheConfigPpty_ForceExpire                = 'ForceExpire'
cCacheConfigPpty_CacheDiskEnabled           = 'CacheDiskEnabled'
cCacheConfigPpty_CacheDiskPath              = 'CacheDiskPath'
cCacheConfigPpty_ExpireDiskAfterSeconds     = 'ExpireDiskAfterSeconds'

cCacheConfigPptyNames = [
    cCacheConfigPpty_Name,
    cCacheConfigPpty_Kind,
    cCacheConfigPpty_CacheEnabled,
    cCacheConfigPpty_MaxCharsCached,
    cCacheConfigPpty_MinThresholdCharsToRelease,
    cCacheConfigPpty_DisplayCacheHitInformation,
    cCacheConfigPpty_ExpireAfterSeconds,
    cCacheConfigPpty_ForceExpire,
    cCacheConfigPpty_CacheDiskEnabled,
    cCacheConfigPpty_CacheDiskPath,
    cCacheConfigPpty_ExpireDiskAfterSeconds,
]








# #######################################################
"""Names for the cache storage structure.

"""
cCacheStore_Name                   = 'Name'
cCacheStore_Kind                   = 'Kind'
cCacheStore_CachedTemplates        = 'CachedTemplates'
cCacheStore_EntryUniqueIdCounter   = 'EntryUniqueIdCounter '

cCacheStore_ForElements_EntriesPromised          = 'EntriesPromised '
cCacheStore_EntriesList_Old_Sentinel = 'EntriesList_Old_Sentinel '
cCacheStore_EntriesList_New_Sentinel = 'EntriesList_New_Sentinel '






# #######################################################
"""Names for the cache statistics.

"""    
cCacheStatistics_Name              = 'Name'
cCacheStatistics_Kind              = 'Kind'
cCacheStatistics_LastFlushingUser  = 'LastFlushingUser'
cCacheStatistics_LastFlushDate     = 'LastFlushDate'
cCacheStatistics_TotalCacheEntries = 'TotalCacheEntries'
cCacheStatistics_TotalCharsCached  = 'TotalCharsCached'
cCacheStatistics_TotalCacheHits    = 'TotalCacheHits'
cCacheStatistics_TotalCacheFaults  = 'TotalCacheFaults'
cCacheStatistics_TotalCacheDiskHits= 'TotalCacheDiskHits'
cCacheStatistics_TotalRenderings   = 'TotalRenderings'
cCacheStatistics_TotalCharsSaved   = 'TotalCharsSaved'
cCacheStatistics_TotalTimeSaved    = 'TotalTimeSaved'
cCacheStatistics_TotalEntriesFlushed='TotalEntriesFlushed'
cCacheStatistics_TotalCharsFlushed = 'TotalCharsFlushed'
cCacheStatistics_TotalFilesWritten = 'TotalFilesWritten'
cCacheStatistics_TotalCharsWritten = 'TotalCharsWritten'
cCacheStatistics_TotalFilesCleared = 'TotalFilesCleared'
cCacheStatistics_TotalCharsDiskFreed='TotalCharsDiskFreed'





cCacheStatisticsSupported = [
    cCacheStatistics_LastFlushingUser,
    cCacheStatistics_LastFlushDate,
    cCacheStatistics_TotalCacheEntries,
    cCacheStatistics_TotalCharsCached,
    cCacheStatistics_TotalCacheHits,
    cCacheStatistics_TotalCacheFaults,
    cCacheStatistics_TotalCacheDiskHits,
    cCacheStatistics_TotalRenderings,
    cCacheStatistics_TotalCharsSaved,
    cCacheStatistics_TotalTimeSaved,   
    cCacheStatistics_TotalEntriesFlushed,   
    cCacheStatistics_TotalCharsFlushed,     
    cCacheStatistics_TotalFilesWritten,   
    cCacheStatistics_TotalCharsWritten,     
    cCacheStatistics_TotalFilesCleared,     
    cCacheStatistics_TotalCharsDiskFreed,       
]








# #######################################################
"""Different magic strings to include in the HTML of the cache hit information of generated and cached pages, to be later substituted before presentation, by the actual rendering or cache hit retrieval values.

"""
cDefaultNombreProyecto  = 'a_ModelDDvlPlone_driven_ProjectName'

cMagicReplacementString_UniqueId     = '!!! UNI !!! !!! HERE!!!'
cMagicReplacementString_Len          = '!!! LEN !!! !!! HERE!!!'
cMagicReplacementString_Milliseconds = '!!! MIL !!! !!! HERE!!!'
cMagicReplacementString_Date         = '!!! DAT !!! !!! HERE!!!'
cMagicReplacementString_TimeToRetrieve = '!!! TIME !!! !!! HERE!!!'
cMagicReplacementString_CacheCode    = '!!! CACODE !!! !!! HERE!!!'

 
cMagicReplacementString_CollapsibleSectionTitle = '!!! CST !!! !!! HERE!!!'





# #######################################################
"""Names of roles in Zope/Plone, and the names of the reduced set of role kinds into which the cache folds the variety of role combinations that a user may hold. 
The Cache does not maintain different cached pages for each possible combination of roles that a user may hold, at the various elements that incoporate information into a page 
(the main element, its container, owner, siblings, contained and related elements),
because that would reduce largely the possiblity of reusing rendered and cached pages in future cache hits.
Rather, from all the relevant roles that a user may hold at the Plone site, 
or at the root of the model, or at the target element,
the application classifies users as pertaining to one of a few (5 jut now, see below)
broad groups of role holders.

"""
cZopeRole_Anonymous     = 'Anonymous'
cZopeRole_Authenticated = 'Authenticated'
cZopeRole_Member        = 'Member'
cZopeRole_Reviewer      = 'Reviewer'
cZopeRole_Owner         = 'Owner'
cZopeRole_Manager       = 'Manager'


cUserSpecificZopeRoles = [
    cZopeRole_Reviewer,
    cZopeRole_Owner,
    cZopeRole_Manager,
]


cRoleKind_Anonymous     = 'Anonymous'
cRoleKind_Authenticated = 'Authenticated'
cRoleKind_Member        = 'Member'
cRoleKind_UserSpecific  = 'UserSpecific'

cRoleKinds = [
    cRoleKind_Anonymous,
    cRoleKind_Authenticated,
    cRoleKind_Member,
    cRoleKind_UserSpecific,
]





# ##########################################################################
"""Classification of roles into a subset of role kinds, for the cache to figure out whther to serve a cached page generic for the role kind, or specific to the user.

"""
cZopeRolesAndRoleKinds = [
    [ [ cZopeRole_Manager,],         cRoleKind_UserSpecific],
    [ [ cZopeRole_Owner, ],          cRoleKind_UserSpecific],
    [ [ cZopeRole_Reviewer,],        cRoleKind_UserSpecific],
    [ [ cZopeRole_Member,],          cRoleKind_Member],
    [ [ cZopeRole_Authenticated,],   cRoleKind_Authenticated],
    [ [ cZopeRole_Anonymous,],       cRoleKind_Anonymous],
]




# #######################################################
"""Symbols for cache control structure nodes for entries that do not correspond to browsing elements related to an element.

"""
cNoRelationCursorName = '_'
cNoCurrentElementUID  = '_'





# #######################################################
"""Used to mark promised entries as fulfilled.

"""
cCacheEntry_PromiseFulfilled_Sentinel = '--Promise Fulfilled--'





# #######################################################
# #######################################################

# #######################################################
# #######################################################










# #######################################################
"""Factory methods for cache stores. These are not constants, yet they are built exclussively from constants, and are used in initialization of globals, so these are defined here, and not in a functional manager class, to avoid import dependency loops.

"""



def fNewCacheStore( theCacheName, theCacheKind):
    if not theCacheName:
        return None
    
    if not ( theCacheKind in cCacheKindsSupported):
        return None
    
    aLinkedList = MDDLinkedList()

    aCacheStore = {
        cCacheStore_Name:                          theCacheName,
        cCacheStore_Kind:                          theCacheKind,
        cCacheStore_CachedTemplates:      { },
        cCacheStore_EntryUniqueIdCounter: 0,
        cCacheStore_EntriesList_Old_Sentinel:      aLinkedList.vFirst,
        cCacheStore_EntriesList_New_Sentinel:      aLinkedList.vLast,
    }        
    return aCacheStore






# #######################################################
"""Factory methods for cache statistics.

"""
    
    
def fNewCacheStatistics( theCacheName, theCacheKind):
    if not theCacheName:
        return None
    
    aCacheStatistics = {
        cCacheStatistics_Name:                theCacheName,
        cCacheStatistics_Kind:                theCacheKind,
        cCacheStatistics_LastFlushingUser:    '',
        cCacheStatistics_LastFlushDate:       None,
        cCacheStatistics_TotalCacheEntries:   0,
        cCacheStatistics_TotalCharsCached:    0,
        cCacheStatistics_TotalCacheHits:      0,
        cCacheStatistics_TotalCacheFaults:    0,
        cCacheStatistics_TotalCacheDiskHits:  0,
        cCacheStatistics_TotalRenderings:     0,
        cCacheStatistics_TotalCharsSaved:     0,
        cCacheStatistics_TotalTimeSaved:      0,    
        cCacheStatistics_TotalEntriesFlushed: 0,   
        cCacheStatistics_TotalCharsFlushed:   0,     
        cCacheStatistics_TotalFilesWritten:   0,   
        cCacheStatistics_TotalCharsWritten:   0,     
        cCacheStatistics_TotalFilesCleared:   0,     
        cCacheStatistics_TotalCharsDiskFreed: 0,       
    }
    return aCacheStatistics


