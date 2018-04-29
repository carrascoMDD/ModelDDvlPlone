# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache.py
#
# Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
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

from StringIO import StringIO


from App.config import getConfiguration

from AccessControl import ClassSecurityInfo



from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName


from Products.PlacelessTranslationService.Negotiator import getLangPrefs




from ModelDDvlPloneTool_CacheConstants          import *

from MDDStringConversions                       import *

from MDDLinkedList                              import MDDLinkedList, MDDLinkedNode

from ModelDDvlPloneTool_Retrieval               import ModelDDvlPloneTool_Retrieval
from ModelDDvlPloneTool_Transactions            import ModelDDvlPloneTool_Transactions
from ModelDDvlPloneToolSupport                  import fEvalString, fReprAsString, fMillisecondsNow, fMillisecondsToDateTime, fDateTimeNow




cRenderedTitle_HTML = """
<h1>%s</h1>
"""



# #######################################################################
""" Utility to escape strings written as HTML.

"""
def fCGIE( theString, quote=1):
    if not theString:
        return theString
    return cgi.escape( theString, quote=quote)
    




# #######################################################
"""
Cache services:

Cache configuration initialization.
  Invoked when: Instantiating ModelDDvlPloneTool singleton. Once every product installation ( intervals of weeks or months).
  Feature:  To know which cache configurations to create and with which initial values.
            Supported by method: ###

Initialize caches
  Invoked when: starting up instance. Once every instance or server restart (intervals of days or weeks).
  Feature:  To know which caches to create, their names  and kinds.

Flush all caches, or some of the caches. 
  Invoked when: By manager user demand. Reponses can be even many minute-long (not that it should take that long to flush).
  Feature:  To know which caches exists, the cache entries held, how to remove these from global registries (those that include entries from more than one cache, if any - we'll see in features below).

Flush cached entries in any cache for elements given their UID, changed in this ZEO client.
  Invoked when: an element changes (its attributes, or change any relevant attributes of its contents, or container, or owner, or siblings or related elements).
  Request frequency: By users authorized to change elements, engaged in authoring: so not so many as readers, by are active and expect the system to be agile and responsive).  
  Feature:  Index by their element UID all cache entries in all element dependent caches.

Flush cached entries for elements given their UID.
  Invoked when: Notified from other ZEO clients.
  Request frequency: As above, in any other ZEO client, so frquency is multiplied by number of ZEO clients.
  Feature:  Same as above.

Flush cached entry for specific rendered template.
  Invoked when: By manager user demand.
  Seldom, but could be a per request frequency. Response times shall be as simply rendering a page from scratch.
  Feature:  Index by their UniqueId all cache entries in all caches.

Render or retrieve cached rendered template, independent of element (and user).
  Invoked when: per all users requests, per project, for any element => for most requests in the project: lots.
  Feature:  Maintain a cache entry structure by 
            Project
                Language 
                    View name.

Render or retrieve cached rendered template, for element, user independent.
  Invoked when: per all users requests, per project, for specific element => whenever the element is accessed: average frequency.
  Feature:  Maintain a cache entry structure by:
            Project
                Language 
                    Element UID
                        View name
                            (optionally) Relation Name
                                (optionally) Current Related UID
                                    Role Kind 
                            

Render or retrieve cached rendered template, for element and user, when the view is user specific, and user with role worth uniquely identiying the user.
  Invoked when: per request, per project, per element and user: as often as teh suers requests, but the users is so likely engaged that the user requires responsiveness.
  Feature:  Same as above, using the User Id instead of the Role Kind  

Report configuration for a cache, or all caches.

Report statistics for a cache, or all caches.

Flush entries forced to expire in any cache, when expired :
     An entry is expired when the current time is equal of later than : 
        - the last time the entry was hit (or created) plus the time to expire for entries in the cache
            the time to expire is configured differently by default for caches with:
                element specific user specific entries, and 
                element specific  non-user specific entries, and for non element specific entries
            So there are cache configurations for caches that are specific to users, or for all users.
            All caches of each kind share one of the configurations.
  Feature:  To know which cache entries have an expiration time earlier or equal to the current time.
  Supported by: Having a single collection for all entries in all caches, that are forced to expire at their time (entries not forced to expire do not need to be in this collection).
    Ordered by the time to expire, earliest values first.
    Whenever a cache entry is hit, the entry is relocated in the collecttion.



    
Flush cache entries from a cache when memory usage for the cache exceeds maximum.
  Flush expired cache entries that have passed more time from expiration time, as needed.
  If more flushing is needed, flush not expired cache entries with less time remaining to expire, .

Configure parameters for a kind of cache (element independent, element dependent user independent, element and user dependent).  
  

# #######################################################


One cache (store) kind=element independent, with a config with max memory and time to expire,  and a linked list ordered by expiration time, which is the same as last access time because of same time to expire configuration value 
other cache (store) kind=for users, for all roles (role is the last key in the structure),  with a config with max memory and time to expire, and a linked list ordered by expiration time, which is the same as last access time because of same time to expire configuration value 
another cache (store) kind=for users (users worth considering apart) (entries are element dependent) (user id is the last key in the structure), and a memory used accumulator for informative purposes,
all user dependent caches sharing one config with max memory and time to expire, and all sharing a memory storage structure, and all sharing one memory used accumulator to trigger when exceeded the flushing of oldest entries in any of the sharing caches
all user dependent caches sharing one linked list ordered by expiration time, which is the same ordering as the last time accessed, because all share the same time to expire configuration value
(no need to calculate expiration time and update it on the cache entries at every hit)

One index by element UID

One index by cache entry unique Id

All entries in a cache are either forced or not forced to flush at their expire time, according to their configuration parameter (that for user specific, is shared by all user specific caches).
Those caches that have a configuration with a force expired parameter True, shall be visited at every request to flush expired entries.
Because all entries are either forced or not forced, when visiting to flush expired entries, all the entries with times earlier than the calculated one shall be flushed: there is no walking the list visiting entries that do not contribute recovered memory so they are worth visiting.
Those with the force expired configuration parameter False, only flush their older entries, when the cache exceeds its configured maximum memory usage.


To recover memory: 

At every request ( or just those that create new entries):
Flush All the expired entroes in all the caches forced to expire 

When creating a new entry in a cache, that then exceeds configured maximum memory,
or if the cache is a user dependent and therefore shares its memory with other caches of its kind, when the sum of memory used by all the caches of the kind exceeds the configured maximum, 

1) As many already expired in the cache (or all the user caches if the cache is user specific) (no matter if the cache forces or not) as needed to recover memory enough to fall under the maximum minus threshold.

and if the above does not bring the memory used in the cache under the maximum minus threshold:

2) As many of the oldest in the cache (or all the user caches if the cache is user specific)  not expired (no expired remains after step 1) as needed to recover memory enough to fall under the maximum minus threshold.

"""






# #######################################################
"""Cache entry clases as nodes to be linked in a list ordered by the last time the entry was used.

"""
    
    

class MDDRenderedTemplateCacheEntry_ElementIndependent( MDDLinkedNode):
    """"Cache entry class incorporating the list nodes facility above, and the cache entry specific features like an unique id. The unique id is not used in any algorithm, but is set upon cache entry instantiation to facilitate the identification of individual cache entries in quality assurance procedures.
    
    """
    
    def __init__( self, 
        theCacheName    ='',
        theCacheKind    ='',
        theProjectName  = '',
        theUniqueId     =None,
        theValid        =False, 
        thePromise      =0,
        theUser         ='', 
        theDateMillis   ='', 
        theProject      ='', 
        theView         ='', 
        theLanguage     ='', 
        theHTML         ='', 
        theMilliseconds =0,
        theExpireAfterSeconds  =0,
        theForceExpire  =False):
        
        MDDLinkedNode.__init__( self, theUniqueId=theUniqueId)
        
        self.vCacheName   = theCacheName
        self.vCacheKind   = theCacheKind
        self.vProjectName = theProjectName
        self.vValid       = theValid
        self.vPromise     = thePromise
        self.vUser        = theUser
        self.vDateMillis  = theDateMillis
        self.vProject     = theProject
        self.vLanguage    = theLanguage
        self.vView        = theView
        self.vHTML        = theHTML
        self.vMilliseconds= theMilliseconds
        # ##############
        """ExpireAfter is the configured interval since last for expiration, hit copied from config at the time of creation, 
           not absolute time, which would require update at each hit, and be redundant with the last hit time recorded below.
        """
        self.vExpireAfterSeconds = theExpireAfterSeconds
        self.vForceExpire = theForceExpire 
        
        self.vLastHit  = theDateMillis
        self.vLastUser = theUser
        self.vHits     = 0
        
        self.vFilePath = ''
        
        
        
        
    def fIsForElement( self):
        return False
    
       
        
        
    def pBeGone( self,):
        
        try:
            MDDLinkedNode.pBeGone( self)
        except:
            None
        
        
        self.vCacheName   = None
        self.vCacheKind   = None
        self.vProjectName = None
        self.vValid       = None
        self.vPromise     = None
        self.vUser        = None
        self.vDateMillis  = None
        self.vProject     = None
        self.vLanguage    = None
        self.vView        = None
        self.vHTML        = None
        self.vMilliseconds= None
        self.vExpireAfterSeconds = None
        self.vForceExpire = None 
        self.vLastHit  = None
        self.vLastUser = None
        self.vHits     = None
        self.vFilePath = None
    
        return self
    
    
    
    
     
class MDDRenderedTemplateCacheEntry_ForElement( MDDRenderedTemplateCacheEntry_ElementIndependent):
    """Cache entry class specific to individual elements.
    
    """
    def __init__( self, 
        theCacheName    ='',
        theCacheKind    ='',
        theProjectName  = '',
        theUniqueId     =None,
        theValid        =False, 
        thePromise      =0,
        theUser         ='', 
        theDateMillis   ='', 
        theProject      ='', 
        theView         ='', 
        theLanguage     ='', 
        theHTML         ='', 
        theMilliseconds =0, 
        theExpireAfterSeconds  =None,
        theForceExpire  =False,
        theMetaType     ='',
        thePortalType   ='',
        theArchetypeName='',
        theElementId    ='', 
        theUID          ='', 
        theTitle        ='', 
        theURL          ='', 
        theRootPath     = '', 
        theRootUID      = '', 
        thePath         = '', 
        theRoleKind     ='', 
        theRelation     ='', 
        theCurrentUID   =''):
        
        MDDRenderedTemplateCacheEntry_ElementIndependent.__init__( self, 
            theCacheName    =theCacheName,
            theCacheKind    =theCacheKind,
            theProjectName  =theProjectName,
            theUniqueId     =theUniqueId,
            theValid        =theValid, 
            thePromise      =thePromise,
            theUser         =theUser, 
            theDateMillis   =theDateMillis, 
            theProject      =theProject, 
            theView         =theView, 
            theLanguage     =theLanguage, 
            theHTML         =theHTML, 
            theMilliseconds =theMilliseconds,
            theExpireAfterSeconds  =theExpireAfterSeconds,
            theForceExpire  =theForceExpire,
        )
         
        self.vMetaType      = theMetaType
        self.vPortalType    = thePortalType
        self.vArchetypeName = theArchetypeName
        self.vElementId  = theElementId
        self.vUID        = theUID
        self.vTitle      = theTitle
        self.vURL        = theURL
        self.vRootUID    = theRootUID
        self.vRootPath   = thePath
        self.vPath       = theRootPath
        self.vRoleKind   = theRoleKind
        self.vRelation   = theRelation
        self.vCurrentUID = theCurrentUID
        
        self.vDirectory  = ''
        

       
        
        
    def pBeGone( self,):
        
        try:
            MDDRenderedTemplateCacheEntry_ElementIndependent.pBeGone( self)
        except:
            None
        
        
        self.vMetaType      = None
        self.vPortalType    = None
        self.vArchetypeName = None
        self.vElementId  = None
        self.vUID        = None
        self.vTitle      = None
        self.vURL        = None
        self.vRootUID    = None
        self.vRootPath   = None
        self.vPath       = None
        self.vRoleKind   = None
        self.vRelation   = None
        self.vCurrentUID = None
        
        self.vDirectory  = None
        
        return self
        
       
         
    def fIsForElement( self):
        return True
    


    
    
    
    
    
    
    
    








# #######################################################
# #######################################################

# #######################################################
# #######################################################

# #######################################################
# #######################################################










    
class ModelDDvlPloneTool_Cache:
    """Manager for Caching of rendered templates
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    
    
    
    # #######################################################
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """Globals with cache information are held by the ModelDDvlPloneTool_Globals and accessed through the supplied instance of ModelDDvlPloneTool, which currently is a singleton, yet access is always to the supplied argument instance.
    
    """
    # #######################################################
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """gCacheMutex
    To enforce Exclusive access to Cache
    
    """
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # #######################################################
    """gCacheStartupTime_Holder
    Cache and cache control globals
    
    """
    # #######################################################
    """gCacheStore_UniqueIdCounter_Holder gCacheStore_EntriesByUniqueId 
    Unique counter for all entries in all caches. Cached entries Element Independent in all caches Indexed by the Unique Id  of the cache entry.
    
    """
    # #######################################################
    """gCacheStore_EntriesByElementUID
    Cached entries For Elements in all caches Indexed by the UID of the represented element.
    Used to invalidate entries for elements impacted by change operations, or to invalidate current cache entry, or by request from distributed peers.
    
    """
    # #######################################################
    """gCacheStoreHolders
    Caches store global. The cache memory storage structure and all Cached pages are rooted here.
    Includes: Cached pages,a list of promised entries in process of resolution, 
    a Counter for unique Cache Entry identifiers.
    and a Dynamic list of active entries ordered by the time they were last accessed, the last at the bottom.
    """
    # #######################################################
    """gCacheStatisticsHolders
    Caches statistics global. The statistics for all caches are rooted here.
    Record the date of last flush, and who did the flushing.
    Total of cache entries, and memory used.
    Number of Hits (pages served from cache), and savings.
    Number of Faults (pages not in cache had to be rendered).
    
    """
    



    
   
    
    
    
 
    # #######################################################
    """Reserve or release access to Cache and Cache control, by acquiring and releasing a lock on a mutual exclussion (mutex) semaphore, held here to protect critical sections and make them thread-safe.
    
    """
   
    def pAcquireCacheLock(self, theModelDDvlPloneTool, theContextualObject):
        
        if not self.fIsCachingActive_NotThreadSafe( theModelDDvlPloneTool, theContextualObject):
            return self
        

        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        theModelDDvlPloneTool.fgCacheMutex( theContextualObject).acquire()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    

    
    
    
    
    def pAcquireCacheLock_Unconditionally(self, theModelDDvlPloneTool, theContextualObject):
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        theModelDDvlPloneTool.fgCacheMutex( theContextualObject).acquire()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
        
    
    
    
    
    
    
    def pReleaseCacheLock(self, theModelDDvlPloneTool, theContextualObject):

        if not self.fIsCachingActive_NotThreadSafe( theModelDDvlPloneTool, theContextualObject):
            return self

        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        theModelDDvlPloneTool.fgCacheMutex( theContextualObject).release()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    


    def pReleaseCacheLock_Unconditionally(self, theModelDDvlPloneTool, theContextualObject):

        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        theModelDDvlPloneTool.fgCacheMutex( theContextualObject).release()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self
    

   

    
    

    
    
    
    # #######################################################
    """Access the Cache configuration parameters held by the ModelDDvlPloneTool singleton
    
    """
    
    
    
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
    
     
    
    # #######################################################
    """Access the Cache Entries index by Element UID.
    
    """
       
    
    def _fGetCachedEntriesByUID_Copy( self, theModelDDvlPloneTool, theContextualObject, ):

        aCacheStore_EntriesByElementUID = theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject)
        if aCacheStore_EntriesByElementUID == None:
            return {}

        return aCacheStore_EntriesByElementUID.copy()
    
    
        
    
    def _fGetCachedEntriesByUID( self, theModelDDvlPloneTool, theContextualObject, theUID, theViewsToFlush=[]):
        if not theUID:
            return []
        
        aCacheStore_EntriesByElementUID = theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject)
        if not aCacheStore_EntriesByElementUID:
            return [ ]
        
        someCacheEntries = aCacheStore_EntriesByElementUID.get( theUID, [])
        if not theViewsToFlush:
            return someCacheEntries
         

        
        someCacheEntriesOfView = []
        for aCacheEntry in someCacheEntries:
            if aCacheEntry.vView in theViewsToFlush:
                someCacheEntriesOfView.append( aCacheEntry)

        return someCacheEntriesOfView
    
    
    
    
    
    
    def _fGetCachedEntriesByManyUIDs( self , theModelDDvlPloneTool, theContextualObject, theUIDs, theViewsToFlush=[]):
        if not theUIDs:
            return []
        
        if not theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject):
            return [ ]
        
        todasCacheEntries = [ ]
        
        for aUID in theUIDs:
            someCacheEntries = theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject).get( aUID, [])
            if someCacheEntries:
                if not theViewsToFlush:
                    todasCacheEntries.extend( someCacheEntries)
                else:
                    for aCacheEntry in someCacheEntries:
                        if aCacheEntry.vView in theViewsToFlush:
                            todasCacheEntries.append( aCacheEntry)
                            
        return todasCacheEntries
    
    
        
    
    def _pRemoveCacheEntriesFromUIDIndex( self, theModelDDvlPloneTool, theContextualObject, theCacheEntriesToRemove):
        if not theCacheEntriesToRemove:
            return self
        
        if not theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject):
            return self
    
        for aCacheEntry in theCacheEntriesToRemove:
            if aCacheEntry.fIsForElement():
        
                aUID = aCacheEntry.vUID
                if aUID:
                    
                    someCacheEntries = theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject).get( aUID, [])
                    
                    if aCacheEntry in someCacheEntries:
                        someCacheEntries.remove( aCacheEntry)
                        if not someCacheEntries:
                            theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject).pop( aUID)
                            
                    
        return self
    
    
    
    def _pAddCacheEntryToUIDIndex( self, theModelDDvlPloneTool, theContextualObject, theCacheEntry):
        if not theCacheEntry:
            return self
        
        if not theCacheEntry.fIsForElement():
            return self
        
        if theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject) == None:
            return self
    
        aUID = theCacheEntry.vUID
        if not aUID:
            return self
        
            
        someCacheEntries = theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject).get( aUID, None)
        if someCacheEntries == None:
            someCacheEntries = [ ]
            theModelDDvlPloneTool.fgCacheStore_EntriesByElementUID( theContextualObject)[ aUID] = someCacheEntries
        else:
            if theCacheEntry in someCacheEntries:
                return self
        
        someCacheEntries.append( theCacheEntry)
        
        return self
    
         
    
    
    
    
    def _fGetCachedEntriesById_Copy( self , theModelDDvlPloneTool, theContextualObject,):

        aCacheStore_EntriesByUniqueId = theModelDDvlPloneTool.fgCacheStore_EntriesByUniqueId( theContextualObject)
        if aCacheStore_EntriesByUniqueId == None:
            return None
        
        return aCacheStore_EntriesByUniqueId.copy()
    
        
        
    
    def _fGetCachedEntryById( self , theModelDDvlPloneTool, theContextualObject, theCacheEntryId):
        if not theCacheEntryId:
            return None
        
        aCacheStore_EntriesByUniqueId = theModelDDvlPloneTool.fgCacheStore_EntriesByUniqueId( theContextualObject)
        if not aCacheStore_EntriesByUniqueId:
            return None
        
        aCacheEntry = aCacheStore_EntriesByUniqueId.get( theCacheEntryId, None)
        return aCacheEntry
    
        
    
    
    def _pAddCacheEntryToUniqueIdIndex( self, theModelDDvlPloneTool, theContextualObject, theCacheEntry):
        if not theCacheEntry:
            return self
        
        aCacheStore_EntriesByUniqueId = theModelDDvlPloneTool.fgCacheStore_EntriesByUniqueId( theContextualObject)
        if aCacheStore_EntriesByUniqueId == None:
            return self
    
        aUniqueId = theCacheEntry.vUniqueId
        if not aUniqueId:
            return self
            
        aCacheStore_EntriesByUniqueId[ aUniqueId] = theCacheEntry
        
        return self
            
        
    
    
    def _pRemoveCacheEntriesFromUniqueIdIndex( self, theModelDDvlPloneTool, theContextualObject, theCacheEntriesToRemove):
        if not theCacheEntriesToRemove:
            return self
        
        aCacheStore_EntriesByUniqueId = theModelDDvlPloneTool.fgCacheStore_EntriesByUniqueId( theContextualObject)
        if aCacheStore_EntriesByUniqueId == None:
            return self
    
   
        for aCacheEntry in theCacheEntriesToRemove:
            aUniqueId = aCacheEntry.vUniqueId
            if aUniqueId:
                
                try:
                    aCacheStore_EntriesByUniqueId.pop( aUniqueId)
                except:
                    None
        
        return self
    
    
    
    
    
    
    # #######################################################
    """Access to Caches store. The cache memory storage structure and all Cached pages are rooted here.
    
    """

    def fGetCacheStoreNames( self, theModelDDvlPloneTool, theContextualObject, ):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return False
            
        return theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).keys()
 
    
    
    
    
    
    def fHasCacheStoreNamed( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return False
        
        if not theCacheName:
            return False
            
        return theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).has_key( theCacheName)
    
    
    
    
    
    
    def fCacheStoreKind( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return ''
        
        if not theCacheName:
            return ''
        
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if not aCacheStoreHolder:
            return ''
        
        return aCacheStoreHolder.get( cCacheStore_Kind, '')
    
     
     
    
    
    
    def pRemoveRootProjectFromCacheStore( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectNameToRemove):
        return self.fRemoveKeysFromCacheStoreSlotDict( theModelDDvlPloneTool, theContextualObject, theCacheName, cCacheStore_CachedTemplates, [ theProjectNameToRemove,])
    
    
    
    
    def fGetCachedProjects( self, theModelDDvlPloneTool, theContextualObject, theCacheName,):
        someCachedTemplatesForProject = self.fGetCacheStoreSlotDictKeys( theModelDDvlPloneTool, theContextualObject, theCacheName, cCacheStore_CachedTemplates) 
        return someCachedTemplatesForProject

 
    
    

    def fGetCachedTemplatesForProject( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectName):
        someCachedTemplatesForProject = self.fGetCacheStoreSlotDictValueForKey( theModelDDvlPloneTool, theContextualObject, theCacheName, cCacheStore_CachedTemplates, theProjectName) 
        return someCachedTemplatesForProject

    
    
     

    def fGetOrInitCachedTemplatesForProject( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectName):
        someCachedTemplatesForProject = self.fGetCacheStoreSlotDictValueForKey( theModelDDvlPloneTool, theContextualObject, theCacheName, cCacheStore_CachedTemplates, theProjectName) 
        if not( someCachedTemplatesForProject == None):
            return someCachedTemplatesForProject
        
        someCachedTemplatesForProject = { }
        self.pRegisterCacheSlotDictValueWithKey( theModelDDvlPloneTool, theContextualObject, theCacheName, cCacheStore_CachedTemplates, theProjectName, someCachedTemplatesForProject)
        return someCachedTemplatesForProject

    
    
    
     
    
    def fGetCacheStoreNewUniqueId( self, theModelDDvlPloneTool, theContextualObject, ):
        theModelDDvlPloneTool.fgCacheStore_UniqueIdCounter_Holder( theContextualObject)[ 0] += 1
        return theModelDDvlPloneTool.fgCacheStore_UniqueIdCounter_Holder( theContextualObject)[ 0]
    
    
    
    
    def fGetCacheStoreListSentinel_New( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        return self.fGetCacheStoreSlotObject( theModelDDvlPloneTool, theContextualObject, theCacheName, cCacheStore_EntriesList_New_Sentinel)
    
    
    
    
    def fGetCacheStoreListSentinel_Old( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        return self.fGetCacheStoreSlotObject( theModelDDvlPloneTool, theContextualObject, theCacheName, cCacheStore_EntriesList_Old_Sentinel)
    
    
     
    
    
    
    
    # #######################################################
    # #######################################################



    
    
    

    # #######################################################
    """Generic accessors to Caches store. The cache memory storage structure and all Cached pages are rooted here.
    
    """
    
    
    def fGetCacheStoreSlotObject( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return None
        
        if ( not theCacheName) or ( not theSlotName):
            return None
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return None
        
        aCacheStoreSlot = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlot == None):
            return None
        
        return aCacheStoreSlot
            
    
    
    
    
    
    def fGetCacheStoreSlotNewCounter( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return 0
        
        if ( not theCacheName) or ( not theSlotName):
            return None
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return 0
        
        aCacheStoreSlotCounter = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlotCounter == None):
            return 0
        
        unNewCounter = aCacheStoreSlotCounter + 1
        
        aCacheStoreHolder[ theSlotName] = unNewCounter
        
        return unNewCounter
                
    
    
    
    


    def fGetCacheStoreNamesOfKind( self, theModelDDvlPloneTool, theContextualObject, theCacheKind):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return None
        
        if not theCacheKind:
            return None
        
        someCacheStoreNames = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).keys()
        
        someCacheStoreNamesOfKind = [ ]
        for aCacheName in someCacheStoreNames:
            
            aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( aCacheName, None)
            if aCacheStoreHolder:
                
                aCacheKind = aCacheStoreHolder.get( cCacheStore_Kind, '')
                if aCacheKind and ( aCacheKind == theCacheKind):
                    someCacheStoreNamesOfKind.append( aCacheKind)
                    
        return someCacheStoreNamesOfKind
    

    
    
    
    
    def fGetCacheStoreSlotDictValueForKey( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName, theKey):
        if not theKey:
            return None
        
        someValues = self.fGetCacheStoreSlotDictValuesForKeys( theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName, [ theKey,])
        if not someValues:
            return None

        unValue = someValues[ 0]
        return unValue

    
    
    
    
    
    def pRegisterCacheSlotDictValueWithKey( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName, theKey, theValue):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return self
        
        if ( not theCacheName) or ( not theSlotName) or ( not theKey):
            return self
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return self
        
        aCacheStoreSlotDict = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlotDict == None):
            return self
        
        aCacheStoreSlotDict[ theKey] = theValue
        
        return self

    
    
        
    
    
   
    def fGetCacheStoreSlotDictValuesForKeys( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName, theKeys):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return None
        
        if ( not theCacheName) or ( not theSlotName):
            return None
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return None
        
        aCacheStoreSlotDict = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlotDict == None):
            return None
        
        if not theKeys:
            return []
            
        someValues = [ ]
        
        aSentinel = object()
        
        for aKey in theKeys:
            aValue = aCacheStoreSlotDict.get( aKey, aSentinel)
            if not ( aValue == aSentinel):
                someValues.append( aValue)
                
        return someValues
            
    

   
    def fGetCacheStoreSlotDictKeys( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName,):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return None
        
        if ( not theCacheName) or ( not theSlotName):
            return None
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return None
        
        aCacheStoreSlotDict = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlotDict == None):
            return None
        
        someKeys = aCacheStoreSlotDict.keys()
        
        return someKeys
            
    
    
   
    def fRemoveKeysFromCacheStoreSlotDict( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName, theKeys):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return False
        
        if ( not theCacheName) or ( not theSlotName):
            return False
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return False
        
        aCacheStoreSlotDict = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlotDict == None):
            return False
        
        if not theKeys:
            return True
            
        someValues = [ ]
        
        aSentinel = object()
        
        for aKey in theKeys:
            if aCacheStoreSlotDict.has_key( aKey):
                aCacheStoreSlotDict.pop( aKey)
                
        return True
            
    
    
    
    
   
    def fRemoveObjectsFromCacheStoreSlotList( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName, theObjects):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return False
        
        if ( not theCacheName) or ( not theSlotName):
            return False
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return False
        
        aCacheStoreSlotList = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlotList == None):
            return False
        
        if not theObjects:
            return True
            
        someValues = [ ]
        
        aSentinel = object()
        
        for anObject in theObjects:
            if not ( anObject == None):                
                try:
                    aCacheStoreSlotList.remove( anObject)
                except:
                    None
                
        return True
            
     
    
    
   
    #def pAddObjectToCacheStoreSlotDictKeyList( self, theCacheName, theSlotName, theKey, theObject):
        #if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            #return self
        
        #if ( not theCacheName) or ( not theSlotName):
            #return self
            
        #if theObject == None:
            #return self

        #aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders.get( theCacheName, None)
        #if aCacheStoreHolder == None:
            #return self
        
        #aCacheStoreSlotDict = aCacheStoreHolder.get( theSlotName, None)
        #if ( aCacheStoreSlotDict == None):
            #return self
            
        #aSentinel = object()
        
        #aCacheStoreSlotDictList = aCacheStoreSlotDict.get( theKey, aSentinel)
        #if aCacheStoreSlotDictList == aSentinel:
            #aCacheStoreSlotDictList = [ ]
            #aCacheStoreSlotDict[ theKey] = aCacheStoreSlotDictList
            
        #if theObject in aCacheStoreSlotDictList:
            #return self
        
        #aCacheStoreSlotDictList.append( theObject)
                
        #return self            
      
    
    
    
   
    def fGetCacheStoreSlotListCopy( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return None
        
        if ( not theCacheName) or ( not theSlotName):
            return None
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return None
        
        aCacheStoreSlotList = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlotList == None):
            return None
        
        if not aCacheStoreSlotList:
            return []
        
        return aCacheStoreSlotList[:]
    

    
    
    
    def pReplaceCacheStoreSlotList( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName, theNewList):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return self
        
        if ( not theCacheName) or ( not theSlotName):
            return self
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return self
        
        if not aCacheStoreHolder.has_key( theSlotName):
            return self
        
        aCacheStoreHolder[ theSlotName] = theNewList
        
        return self
    
    
     

   
    def pAddObjectToCacheStoreSlotList( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theSlotName, theObject):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return self
        
        if ( not theCacheName) or ( not theSlotName):
            return self
            
        if theObject == None:
            return self

        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        if aCacheStoreHolder == None:
            return self
        
        aCacheStoreSlotList = aCacheStoreHolder.get( theSlotName, None)
        if ( aCacheStoreSlotList == None):
            return self
                        
        if theObject in aCacheStoreSlotList:
            return self
        
        aCacheStoreSlotList.append( theObject)
                
        return self            
      
    
    
    
         
    # #######################################################
    # #######################################################
    
    # #######################################################
    # #######################################################
        





    def fResetCacheStore( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        if theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject) == None:
            return False
        
        if not theCacheName:
            return False
            
        aCacheStoreHolder = theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject).get( theCacheName, None)
        aCacheKind = ''
        if aCacheStoreHolder:        
            aCacheKind = aCacheStoreHolder.get( cCacheStore_Kind, '')
        
        aNewCacheStoreHolder = fNewCacheStore( theCacheName, aCacheKind)
        if aNewCacheStoreHolder == None:
            return False
        
        theModelDDvlPloneTool.fgCacheStoreHolders( theContextualObject)[  theCacheName] = aNewCacheStoreHolder
        
        someObjectsToDelete = [ ]
        
        if aCacheStoreHolder:   
            
            anOld_Sentinel = aCacheStoreHolder.get( cCacheStore_EntriesList_Old_Sentinel, None)
            if anOld_Sentinel:
                
                someEntriesInList = [ ]
                
                unCurrent = anOld_Sentinel.vNext
                
                while unCurrent and ( not unCurrent.fIsSentinel()):
                    
                    someEntriesInList.append( unCurrent)
                    
                    someObjectsToDelete.append( unCurrent)
                    
                    unCurrent = unCurrent.vNext
                        

                self._pRemoveCacheEntriesFromUIDIndex( theModelDDvlPloneTool, theContextualObject, someEntriesInList)
                self._pRemoveCacheEntriesFromUniqueIdIndex( theModelDDvlPloneTool, theContextualObject, someEntriesInList)
                
                
            anObject = aCacheStoreHolder.get( cCacheStore_CachedTemplates, None)
            if not ( anObject == None):
                someObjectsToDelete.append( anObject)
                
            anObject = aCacheStoreHolder.get( cCacheStore_ForElements_EntriesPromised, None)
            if not ( anObject == None):
                someObjectsToDelete.append( anObject)
                
            anObject = aCacheStoreHolder.get( cCacheStore_EntriesList_Old_Sentinel, None)
            if not ( anObject == None):
                someObjectsToDelete.append( anObject)
            
            anObject = aCacheStoreHolder.get( cCacheStore_EntriesList_New_Sentinel, None)
            if not ( anObject == None):
                someObjectsToDelete.append( anObject)
            
            del someObjectsToDelete
        
        return True
    
        
    
    

        
    

            
    # #######################################################
    """Access to Caches statistics. The statistics for all caches are rooted here.

    """
    def fGetCacheStatisticsCopy( self, theModelDDvlPloneTool, theContextualObject, theCacheName):
        if not theCacheName:
            return None
        
        if theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject) ==None:
            return None
    
        aCacheStatisticsHolder = theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject).get( theCacheName, None)
        if aCacheStatisticsHolder == None:
            return None
        
        aCacheStatisticsCopy = aCacheStatisticsHolder.copy()
        return aCacheStatisticsCopy

    
    
    
    
    def fGetCacheStatisticValue( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theStatisticName):
        if not theCacheName:
            return None
        
        if not theStatisticName:
            return None

        if theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject) ==None:
            return None
    
        aCacheStatisticsHolder = theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject).get( theCacheName, None)
        if aCacheStatisticsHolder == None:
            return None
        
        aSentinel = object()
        
        aStatisticValue = aCacheStatisticsHolder.get( theStatisticName, aSentinel)
        if aStatisticValue == aSentinel:
            return None
        
        return aStatisticValue

    
     
    

    def pUpdateCacheStatistics( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theStatisticsUpdate):
        if not theCacheName:
            return self
        
        if not theStatisticsUpdate:
            return self
        
        if theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject) ==None:
            return self
    
        aCacheStatisticsHolder = theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject).get( theCacheName, None)
        if aCacheStatisticsHolder == None:
            return self
        
        
        for aStatisticsKey in theStatisticsUpdate.keys():
            if aStatisticsKey in cCacheStatisticsSupported: 

                aStatisticsValueDelta = theStatisticsUpdate.get( aStatisticsKey, None)
                if isinstance( aStatisticsValueDelta, int) or isinstance( aStatisticsValueDelta, long):
                    
                    aStatisticsCurrentValue = aCacheStatisticsHolder.get( aStatisticsKey, None)
                    if not ( aStatisticsCurrentValue == None):
                        
                        aCacheStatisticsHolder[ aStatisticsKey] = aStatisticsCurrentValue + aStatisticsValueDelta
        
        return self

    




    
    def fResetCacheStatistics( self, theModelDDvlPloneTool, theContextualObject, theCacheName, theUserId):
        if theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject) == None:
            return False
        
        if not theCacheName:
            return False
            
        aCurrentCacheStatisticsHolder = theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject).get( theCacheName, None)
        if not aCurrentCacheStatisticsHolder:
            return False
        
        aCacheKind = aCurrentCacheStatisticsHolder.get( cCacheStatistics_Kind, '')
        if not aCacheKind:
            return False
        
        aNewCacheStatisticsHolder = fNewCacheStatistics( theCacheName, aCacheKind)
        if aNewCacheStatisticsHolder == None:
            return False
        
        aNewCacheStatisticsHolder.update( {
            cCacheStatistics_LastFlushingUser: theUserId,
            cCacheStatistics_LastFlushDate:    fDateTimeNow(),
        })
        
        theModelDDvlPloneTool.fgCacheStatisticsHolders( theContextualObject)[  theCacheName] = aNewCacheStatisticsHolder
        
        del aCurrentCacheStatisticsHolder
        
        return True
    
        
    
    

    
    
    # #######################################################
    # #######################################################
    
    # #######################################################
    # #######################################################





    # #############################################################
    """Access to the configuration parameters held by ModelDDvlPloneTool persistent holders.
    
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
    
     
    
    
    


    security.declarePrivate( 'fVerifyInvalidationRequesterIdentificationAndAutentication')
    def fVerifyRequesterPeerIdentificationAndAutentication(self, theContextualObject, thePeerIdentificationString, thePeerAuthenticationString):
             
        if thePeerAuthenticationString == cUnsecureCacheFlushAcknowledgedAuthenticationString:
            return True
        
        return False
    
            
        
    
    


    # #############################################################
    """To supply to ModelDDvlPloneTool the cache configs for initialization of a new tool instance.
    
    """

    
     

    security.declarePrivate( 'fInitialCacheConfigs')
    def fInitialCacheConfigs(self, ):
        """Used by instances of ModelDDvlPlone_tool to initialize the CacheConfigsHolder.
        
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
    
    
    
    
    


 

    
    
    
    
    
    
      
    
    
    
    
    # #######################################################
    # #######################################################
    
    # #######################################################
    # #######################################################
    
        





    
    
    # #############################################################
    """Report Cache status.
    
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
        
    
    
    
    
        
    security.declarePrivate( 'fNewVoidCacheStatusReport')
    def fNewVoidCacheStatusReport(self, ):
        unReport = {
            'StatusReportTime':              None,

            'CanActivateOrDeactivate':       False,
            'CanReset':                      False,
            'CanConfigure':                  False,
            'CanFlush':                      False,
            'CanEnableOrDisable':            False,
            
            'CacheStartupTime':              0,
                          
            'IsCachingActive':               False,                    
            'PeersToNotify':                 '',                    
            'IdentificationStringForPeers':  '',
            'AuthenticationStringForPeers':  '',
            'AuthenticationStringFromPeers': '',
            
            'reports':                       [],
            
            'reports_repr':                  '',
        }
        return unReport
    
    
        
    
    
    
        
    security.declarePrivate( 'fNewVoidCacheReport')
    def fNewVoidCacheReport(self, ):
        unReport = {
            'meta_info':                                None,           
            'CacheName':                                '',             
            'CacheKind':                                '',             
            'CacheEnabled':                             False,          
            'MaxCharsCached':                           0,              
            'MinThresholdCharsToRelease':               0,              
            'DisplayCacheHitInformation':               '',             
            'ExpireAfterSeconds':                       0,              
            'ForceExpire':                              False,          
                                                                      
            'CacheDiskEnabled':                         False,          
            'CacheDiskPath':                            '',             
            'ExpireDiskAfterSeconds':                   0,              
                                                                      
            'MaxCharsCached_str':                       '0',            
            'MinThresholdCharsToRelease_str':           '0',            
            'ExpireAfterSeconds_str':                   '0',            
            'ExpireAfterSeconds_wstr':                  '0 s',          
                                                                      
            'ExpireDiskAfterSeconds_str':               '0',            
            'ExpireDiskAfterSeconds_wstr':              '0 s',          
                                                                      
                                                                      
            'LastFlushDate':                            '',             
            'LastFlushingUser':                         '',             
                                                                        
            'TotalCacheEntries':                        0,              
            'TotalCharsCached':                         0,              
            'TotalCacheHits':                           0,              
            'TotalCacheFaults':                         0,              
            'TotalCacheDiskHits':                       0,              
            'TotalRenderings':                          0,                
                                                                      
            'TotalCharsSaved':                          0,              
            'TotalTimeSaved':                           0,              
                                                                        
            'TotalCacheEntries_str':                    '0',            
            'TotalCharsCached_str':                     '0',            
            'TotalCacheHits_str':                       '0',            
            'TotalCacheFaults_str':                     '0',            
            'TotalCacheDiskHits_str':                   '0',            
            'TotalRenderings_str':                      '0',            
            'TotalCharsSaved_str':                      '0',            
            'TotalTimeSaved_str':                       '0',  
            
        }
        return unReport
    
    
    
    
    
        
    
    security.declarePrivate( 'fRetrieveCacheStatusReport')
    def fRetrieveCacheStatusReport(self, theModelDDvlPloneTool, theContextualObject, theRepresentation=''):
        """Retrieve a report with the status of the templates cache, containing the number of entries, the amount of memory occupied, and statistics of cache hits and faults.
        
        """
        
        unCacheStatusReport = self.fNewVoidCacheStatusReport()
            
        if theContextualObject == None:
            return unCacheStatusReport

        aCacheConfig_ElementIndependent     = theModelDDvlPloneTool.fGetCacheConfigCopy( theContextualObject, cCacheName_ElementIndependent)
        aCacheStatistics_ElementIndependent = self.fGetCacheStatisticsCopy( theModelDDvlPloneTool, theContextualObject,cCacheName_ElementIndependent)

        aCacheConfig_ForElements            = theModelDDvlPloneTool.fGetCacheConfigCopy( theContextualObject, cCacheName_ForElements)        
        aCacheStatistics_ForElements        = self.fGetCacheStatisticsCopy( theModelDDvlPloneTool, theContextualObject, cCacheName_ForElements)
        
        
        anAllCachesConfig = theModelDDvlPloneTool.fGetAllCachesConfigCopy( theContextualObject, )
        
        
        
        unAhoraMillis = fMillisecondsNow()
        unAhora       = fMillisecondsToDateTime( unAhoraMillis)
        
        someCacheReports = unCacheStatusReport[ 'reports']
        unCacheStatusReport.update( {
            'StatusReportTime':              unAhora,

            'CanActivateOrDeactivate':       False,
            'CanReset':                      False,
            'CanConfigure':                  False,
            'CanFlush':                      False,
            'CanEnableOrDisable':            False,
            
            'CacheStartupTime':              fMillisecondsToDateTime( theModelDDvlPloneTool.fgCacheStartupTime_Holder( theContextualObject)[ 0].millis()),
                          
            'IsCachingActive':               anAllCachesConfig[ cAllCachesConfigPpty_IsCachingActive],                    
            'PeersToNotify':                 anAllCachesConfig[ cAllCachesConfigPpty_PeersToNotify],                    
            'IdentificationStringForPeers':  anAllCachesConfig[ cAllCachesConfigPpty_IdentificationStringForPeers],                    
            'AuthenticationStringForPeers':  anAllCachesConfig[ cAllCachesConfigPpty_AuthenticationStringForPeers],                    
            'AuthenticationStringFromPeers': anAllCachesConfig[ cAllCachesConfigPpty_AuthenticationStringFromPeers], 
        })
        
        
        
        someCacheNames = self.fGetCacheStoreNames( theModelDDvlPloneTool, theContextualObject, )
        
        for aCacheName in someCacheNames:
            
            aCacheConfig               = theModelDDvlPloneTool.fGetCacheConfigCopy( theContextualObject, aCacheName)
            aCacheStatistics           = self.fGetCacheStatisticsCopy( theModelDDvlPloneTool, theContextualObject, aCacheName)
            aCacheStatusReportMetaInfo = self.fCacheConfigurationMetaInfo( theModelDDvlPloneTool, theContextualObject, aCacheName)        
            
            unCacheReport = self.fNewVoidCacheReport()
            unCacheReport.update( {
                'meta_info':                                      aCacheStatusReportMetaInfo,
                'CacheName':                                      aCacheName,
                'CacheKind':                                      self.fCacheStoreKind( theModelDDvlPloneTool, theContextualObject, aCacheName),
                cCacheConfigPpty_CacheEnabled:                    aCacheConfig[ cCacheConfigPpty_CacheEnabled] == True,
                cCacheConfigPpty_MaxCharsCached:                  aCacheConfig[ cCacheConfigPpty_MaxCharsCached], 
                cCacheConfigPpty_MinThresholdCharsToRelease:      aCacheConfig[ cCacheConfigPpty_MinThresholdCharsToRelease], 
                cCacheConfigPpty_DisplayCacheHitInformation:      aCacheConfig[ cCacheConfigPpty_DisplayCacheHitInformation], 
                cCacheConfigPpty_ExpireAfterSeconds:              aCacheConfig[ cCacheConfigPpty_ExpireAfterSeconds], 
                cCacheConfigPpty_ForceExpire:                     aCacheConfig[ cCacheConfigPpty_ForceExpire]  == True, 

                cCacheConfigPpty_CacheDiskEnabled:                aCacheConfig[ cCacheConfigPpty_CacheDiskEnabled] == True,
                cCacheConfigPpty_CacheDiskPath:                   aCacheConfig[ cCacheConfigPpty_CacheDiskPath] or '',
                cCacheConfigPpty_ExpireDiskAfterSeconds:          aCacheConfig[ cCacheConfigPpty_ExpireDiskAfterSeconds], 
    
                'MaxCharsCached_str':                             fStrGrp( aCacheConfig[ cCacheConfigPpty_MaxCharsCached]), 
                'MinThresholdCharsToRelease_str':                 fStrGrp( aCacheConfig[ cCacheConfigPpty_MinThresholdCharsToRelease]), 
                'ExpireAfterSeconds_str':                         fStrGrp( aCacheConfig[ cCacheConfigPpty_ExpireAfterSeconds]), 
                'ExpireAfterSeconds_wstr':                        fStrTime( aCacheConfig[ cCacheConfigPpty_ExpireAfterSeconds]), 
                
                'ExpireDiskAfterSeconds_str':                     fStrGrp( aCacheConfig[ cCacheConfigPpty_ExpireDiskAfterSeconds]), 
                'ExpireDiskAfterSeconds_wstr':                    fStrTime( aCacheConfig[ cCacheConfigPpty_ExpireDiskAfterSeconds]), 
                
                
                cCacheStatistics_LastFlushDate:                   aCacheStatistics[ cCacheStatistics_LastFlushDate],
                cCacheStatistics_LastFlushingUser:                aCacheStatistics[ cCacheStatistics_LastFlushingUser],
                                                                  
                cCacheStatistics_TotalCacheEntries:               aCacheStatistics[ cCacheStatistics_TotalCacheEntries],
                cCacheStatistics_TotalCharsCached:                aCacheStatistics[ cCacheStatistics_TotalCharsCached],
                cCacheStatistics_TotalCacheHits:                  aCacheStatistics[ cCacheStatistics_TotalCacheHits],
                cCacheStatistics_TotalCacheFaults:                aCacheStatistics[ cCacheStatistics_TotalCacheFaults],
                cCacheStatistics_TotalCacheDiskHits:              aCacheStatistics[ cCacheStatistics_TotalCacheDiskHits],
                cCacheStatistics_TotalRenderings:                 aCacheStatistics[ cCacheStatistics_TotalRenderings],
                cCacheStatistics_TotalCharsSaved:                 aCacheStatistics[ cCacheStatistics_TotalCharsSaved],
                cCacheStatistics_TotalTimeSaved:                  int( aCacheStatistics[ cCacheStatistics_TotalTimeSaved] / 1000),
                
                cCacheStatistics_TotalEntriesFlushed:             aCacheStatistics[ cCacheStatistics_TotalEntriesFlushed], 
                cCacheStatistics_TotalCharsFlushed:               aCacheStatistics[ cCacheStatistics_TotalCharsFlushed],    
                cCacheStatistics_TotalFilesWritten:               aCacheStatistics[ cCacheStatistics_TotalFilesWritten],   
                cCacheStatistics_TotalCharsWritten:               aCacheStatistics[ cCacheStatistics_TotalCharsWritten],    
                cCacheStatistics_TotalFilesCleared:               aCacheStatistics[ cCacheStatistics_TotalFilesCleared],    
                cCacheStatistics_TotalCharsDiskFreed:             aCacheStatistics[ cCacheStatistics_TotalCharsDiskFreed],      
                
                                                                  
                'TotalCacheEntries_str':                          fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCacheEntries]),
                'TotalCharsCached_str':                           fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsCached]),
                'TotalCacheHits_str':                             fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCacheHits]),
                'TotalCacheFaults_str':                           fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCacheFaults]),
                'TotalCacheDiskHits_str':                         fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCacheDiskHits]),
                'TotalRenderings_str':                            fStrGrp( aCacheStatistics[ cCacheStatistics_TotalRenderings]),
                'TotalCharsSaved_str':                            fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsSaved]),
                'TotalTimeSaved_str':                             fStrGrp( int( aCacheStatistics[ cCacheStatistics_TotalTimeSaved] / 1000)),
                
                cCacheStatistics_TotalEntriesFlushed + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalEntriesFlushed]), 
                cCacheStatistics_TotalCharsFlushed   + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsFlushed]),    
                cCacheStatistics_TotalFilesWritten   + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalFilesWritten]),   
                cCacheStatistics_TotalCharsWritten   + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsWritten]),    
                cCacheStatistics_TotalFilesCleared   + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalFilesCleared]),    
                cCacheStatistics_TotalCharsDiskFreed + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsDiskFreed]),      
                
                'ReportTime':                                     unAhoraMillis,
                'ReportTime_str':                                 str( fMillisecondsToDateTime( unAhoraMillis)),
            })
            
            unCacheReport.update( {
                'meta_info':      aCacheStatusReportMetaInfo,
            })
            
            someCacheReports.append(  unCacheReport)

            
        unCacheReportRepresentation = fReprAsString( someCacheReports)
        if unCacheReportRepresentation:
            unCacheStatusReport[ 'reports_repr'] = unCacheReportRepresentation
            
            
            
        unosPreviousStatusReports = None
        if theRepresentation:
            aRepresentationValue = fEvalString( theRepresentation)
            if aRepresentationValue:
                if isinstance( aRepresentationValue, list) or isinstance( aRepresentationValue, tuple):
                    unosPreviousStatusReports = aRepresentationValue
        
        
        if unosPreviousStatusReports:   
            self.pDeltaStatusReports( theModelDDvlPloneTool, unosPreviousStatusReports, someCacheReports)
            
            
            
        
        unElementoRaiz = None
        try:
            unElementoRaiz = theContextualObject.getRaiz()
        except:
            None
        if unElementoRaiz == None:
            return unCacheStatusReport
            
        unHasManagePortalPermission = ModelDDvlPloneTool_Retrieval().fCheckElementPermission( unElementoRaiz, permissions.ManagePortal, None )
        unHasManagerRole            = ModelDDvlPloneTool_Retrieval().fRoleQuery_IsAnyRol(     'Manager', unElementoRaiz, )

        if not cForbidCaches:
            
            unCanActivateOrDeactivate = unHasManagePortalPermission or unHasManagerRole
            if not unCanActivateOrDeactivate:
                unPortalObject = ModelDDvlPloneTool_Retrieval().fPortalRoot( theContextualObject)
                if not(  unPortalObject == None):
            
                    unHasManagePortalPermission = unHasManagePortalPermission or ModelDDvlPloneTool_Retrieval().fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
                    unHasManagerRole            = unHasManagerRole            or ModelDDvlPloneTool_Retrieval().fRoleQuery_IsAnyRol(     'Manager', unPortalObject, )
                      
                    unCanActivateOrDeactivate = unHasManagePortalPermission or unHasManagerRole
            
            unCacheStatusReport.update( {
                'CanActivateOrDeactivate':                        unCanActivateOrDeactivate,
            })
        
            
            unCanDiagnose = unHasManagePortalPermission or unHasManagerRole
            if not unCanDiagnose:
                unPortalObject = ModelDDvlPloneTool_Retrieval().fPortalRoot( theContextualObject)
                if not(  unPortalObject == None):
            
                    unHasManagePortalPermission = unHasManagePortalPermission or ModelDDvlPloneTool_Retrieval().fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
                    unHasManagerRole            = unHasManagerRole            or ModelDDvlPloneTool_Retrieval().fRoleQuery_IsAnyRol(     'Manager', unPortalObject, )
                      
                    unCanDiagnose = unHasManagePortalPermission or unHasManagerRole
            
            unCacheStatusReport.update( {
                'CanDiagnose':                        unCanDiagnose,
            })
            
            
            unCanInspect = unHasManagePortalPermission or unHasManagerRole
            if not unCanInspect:
                unPortalObject = ModelDDvlPloneTool_Retrieval().fPortalRoot( theContextualObject)
                if not(  unPortalObject == None):
            
                    unHasManagePortalPermission = unHasManagePortalPermission or ModelDDvlPloneTool_Retrieval().fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
                    unHasManagerRole            = unHasManagerRole            or ModelDDvlPloneTool_Retrieval().fRoleQuery_IsAnyRol(     'Manager', unPortalObject, )
                      
                    unCanInspect = unHasManagePortalPermission or unHasManagerRole
            
            unCacheStatusReport.update( {
                'CanInspect':                        unCanInspect,
            })
            
                    
            if anAllCachesConfig[ cAllCachesConfigPpty_IsCachingActive]:
                unCanConfigure =  unHasManagePortalPermission or unHasManagerRole
                
                if not unCanConfigure:
                    unPortalObject = ModelDDvlPloneTool_Retrieval().fPortalRoot( theContextualObject)
                    if not( unPortalObject == None):
                
                        unHasManagePortalPermission = unHasManagePortalPermission or ModelDDvlPloneTool_Retrieval().fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
                        unHasManagerRole            = unHasManagerRole            or ModelDDvlPloneTool_Retrieval().fRoleQuery_IsAnyRol(     'Manager', unPortalObject, )
                          
                        unCanConfigure = unHasManagePortalPermission or unHasManagerRole
                
                unCacheStatusReport.update( {
                    'CanConfigure':            unCanConfigure,
                    'CanReset':                unCanConfigure,
                    'CanFlush':                unCanConfigure,
                    'CanEnableOrDisable':      unCanConfigure,
                })
                    
        return unCacheStatusReport
    


    
    

    security.declarePrivate( 'pDeltaStatusReports')
    def pDeltaStatusReports(self, theModelDDvlPloneTool, thePreviousStatusReports, theNewStatusReports):
        
        for unNewStatusReport in theNewStatusReports:
            
            unNewCacheName = unNewStatusReport.get( 'CacheName', '')
            if unNewCacheName:
                unPreviousStatusReport = None
                for unStatusReport in thePreviousStatusReports:
                    if unStatusReport:
                        unCacheName = unStatusReport.get( 'CacheName', '')
                        if unCacheName and ( unCacheName == unNewCacheName):
                            unPreviousStatusReport = unStatusReport
                            break

            if unPreviousStatusReport:
         
                unNewStatusReport.update( {
                                                                  
                    'TotalCacheEntries_Delta':       unNewStatusReport[ cCacheStatistics_TotalCacheEntries]                     - unPreviousStatusReport.get( cCacheStatistics_TotalCacheEntries, 0),
                    'TotalCharsCached_Delta':        unNewStatusReport[ cCacheStatistics_TotalCharsCached]                      - unPreviousStatusReport.get( cCacheStatistics_TotalCharsCached, 0),                      
                    'TotalCacheHits_Delta':          unNewStatusReport[ cCacheStatistics_TotalCacheHits]                        - unPreviousStatusReport.get( cCacheStatistics_TotalCacheHits, 0),                        
                    'TotalCacheFaults_Delta':        unNewStatusReport[ cCacheStatistics_TotalCacheFaults]                      - unPreviousStatusReport.get( cCacheStatistics_TotalCacheFaults, 0),                      
                    'TotalCacheDiskHits_Delta':      unNewStatusReport[ cCacheStatistics_TotalCacheDiskHits]                    - unPreviousStatusReport.get( cCacheStatistics_TotalCacheDiskHits, 0),                    
                    'TotalRenderings_Delta':         unNewStatusReport[ cCacheStatistics_TotalRenderings]                       - unPreviousStatusReport.get( cCacheStatistics_TotalRenderings, 0),                       
                                                                                                                                                                                                   
                    'TotalCharsSaved_Delta':         unNewStatusReport[ cCacheStatistics_TotalCharsSaved]                       - unPreviousStatusReport.get( cCacheStatistics_TotalCharsSaved, 0),                       
                    'TotalTimeSaved_Delta':          int( unNewStatusReport[ cCacheStatistics_TotalTimeSaved] / 1000)           - int( unPreviousStatusReport.get( cCacheStatistics_TotalTimeSaved, 0) / 1000),           
                        
                    cCacheStatistics_TotalEntriesFlushed + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalEntriesFlushed]- unPreviousStatusReport.get( cCacheStatistics_TotalEntriesFlushed, 0),
                    cCacheStatistics_TotalCharsFlushed   + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalCharsFlushed]  - unPreviousStatusReport.get( cCacheStatistics_TotalCharsFlushed, 0),
                    cCacheStatistics_TotalFilesWritten   + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalFilesWritten]  - unPreviousStatusReport.get( cCacheStatistics_TotalFilesWritten, 0),
                    cCacheStatistics_TotalCharsWritten   + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalCharsWritten]  - unPreviousStatusReport.get( cCacheStatistics_TotalCharsWritten, 0),
                    cCacheStatistics_TotalFilesCleared   + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalFilesCleared]  - unPreviousStatusReport.get( cCacheStatistics_TotalFilesCleared, 0),
                    cCacheStatistics_TotalCharsDiskFreed + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalCharsDiskFreed]- unPreviousStatusReport.get( cCacheStatistics_TotalCharsDiskFreed, 0),

                                        
                    'TotalCacheEntries_Delta_str':   fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCacheEntries]           - unPreviousStatusReport.get( cCacheStatistics_TotalCacheEntries, 0)),           
                    'TotalCharsCached_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsCached]            - unPreviousStatusReport.get( cCacheStatistics_TotalCharsCached, 0)),            
                    'TotalCacheHits_Delta_str':      fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCacheHits]              - unPreviousStatusReport.get( cCacheStatistics_TotalCacheHits, 0)),              
                    'TotalCacheFaults_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCacheFaults]            - unPreviousStatusReport.get( cCacheStatistics_TotalCacheFaults, 0)),            
                    'TotalCacheDiskHits_Delta_str':  fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCacheDiskHits]          - unPreviousStatusReport.get( cCacheStatistics_TotalCacheDiskHits, 0)),          
                    'TotalRenderings_Delta_str':     fStrGrp( unNewStatusReport[ cCacheStatistics_TotalRenderings]             - unPreviousStatusReport.get( cCacheStatistics_TotalRenderings, 0)),             
                    'TotalCharsSaved_Delta_str':     fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsSaved]             - unPreviousStatusReport.get( cCacheStatistics_TotalCharsSaved, 0)),             
                    'TotalTimeSaved_Delta_str':      fStrGrp( int( unNewStatusReport[ cCacheStatistics_TotalTimeSaved] / 1000) - int( unPreviousStatusReport.get( cCacheStatistics_TotalTimeSaved, 0) / 1000)), 
                    
                    
                    cCacheStatistics_TotalEntriesFlushed + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalEntriesFlushed]- unPreviousStatusReport.get( cCacheStatistics_TotalEntriesFlushed, 0)),
                    cCacheStatistics_TotalCharsFlushed   + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsFlushed]  - unPreviousStatusReport.get( cCacheStatistics_TotalCharsFlushed, 0)),
                    cCacheStatistics_TotalFilesWritten   + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalFilesWritten]  - unPreviousStatusReport.get( cCacheStatistics_TotalFilesWritten, 0)),
                    cCacheStatistics_TotalCharsWritten   + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsWritten]  - unPreviousStatusReport.get( cCacheStatistics_TotalCharsWritten, 0)),
                    cCacheStatistics_TotalFilesCleared   + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalFilesCleared]  - unPreviousStatusReport.get( cCacheStatistics_TotalFilesCleared, 0)),
                    cCacheStatistics_TotalCharsDiskFreed + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsDiskFreed]- unPreviousStatusReport.get( cCacheStatistics_TotalCharsDiskFreed, 0)),

                    
                    'PreviousReportTime':            unPreviousStatusReport.get( 'ReportTime', 0),
                    'PreviousReportTime_str':        str( fMillisecondsToDateTime( unPreviousStatusReport.get( 'ReportTime', 0))),
                    
                    'ReportTime_Delta':              int( unNewStatusReport[ 'ReportTime'] / 1000)                             -  int( unPreviousStatusReport.get( 'ReportTime', 0) / 1000),                                                             
                    'ReportTime_Delta_str':          fStrGrp( int( unNewStatusReport[ 'ReportTime'] / 1000)                    -  int( unPreviousStatusReport.get( 'ReportTime', 0) / 1000)),                                                             
                    'ReportTime_Delta_wstr':         fStrTime( int( unNewStatusReport[ 'ReportTime'] / 1000)                    -  int( unPreviousStatusReport.get( 'ReportTime', 0) / 1000)),                                                             
                })
              
                
        return self
    
        
        
        
        
        
        
    
    
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
                ModelDDvlPloneTool_Transactions().fTransaction_Commit()
   
        return [ False, 'Edit', theCacheName,]
    
    
    
    
    
  
 
    
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
        

    
    
            
    
        
        
    security.declarePrivate( 'fFlushAllCachedTemplates')
    def fFlushAllCachedTemplates(self, theModelDDvlPloneTool, theContextualObject, theCacheName, theFlushDiskCache=False):
        """Initiated by a User with ManagePortal permission, or Manager Role, in the root model element, or the portal root, Remove all cached rendered templates, recording who and when requested the flush.
        
        """
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        if not theCacheName:
            return False
        
        if theModelDDvlPloneTool == None:
            return False
        
        if theContextualObject == None:
            return False
        

        
        unMemberId    = ModelDDvlPloneTool_Retrieval().fGetMemberId(  theContextualObject)
     
        # ###########################################################
        """Remove all existing cached teimplates, from within a thread-safe protected critical section.
        
        """

        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskEnabled)
            aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskPath)
            
            
            if not self.fHasCacheStoreNamed( theModelDDvlPloneTool, theContextualObject, theCacheName):
                return False
            
            aResult = self.fResetCacheStore(      theModelDDvlPloneTool, theContextualObject,theCacheName) and \
                      self.fResetCacheStatistics( theModelDDvlPloneTool, theContextualObject,theCacheName, unMemberId)
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
        if theFlushDiskCache:
            if aCacheDiskEnabled:
                someFilesToDelete = [ ]
                self._pAllFilePathsInto( aCacheDiskPath, someFilesToDelete)
                if someFilesToDelete:
                    self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
            
             
        return aResult
        

     
 
        
        
        
        
    security.declarePrivate( 'fFlushSomeCachedTemplates')
    def fFlushSomeCachedTemplates(self, theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectNames, theFlushDiskCache=False):
        """Initiated by a User with ManagePortal permission, or Manager Role, in the root model element, or the portal root, Remove all cached rendered templates, recording who and when requested the flush.
        
        """
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        if not theCacheName:
            return False
        
        if theModelDDvlPloneTool == None:
            return False
        
        if theContextualObject == None:
            return False
        

        
        unMemberId    = ModelDDvlPloneTool_Retrieval().fGetMemberId(  theContextualObject)
        
        someFilesToDelete = [ ]
     
        # ###########################################################
        """Remove all existing cached teimplates, from within a thread-safe protected critical section.
        
        """

        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskEnabled)
            aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskPath)
            
            someCacheEntries, someFilePaths = self.fFindSomeCachedEntriesAndFilePaths( theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectNames,)
            
            if someFilePaths:
                someFilesToDelete.extend( someFilePaths)
                
            if someCacheEntries:
                self._pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, someCacheEntries, someFilesToDelete)
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
        if theFlushDiskCache:
            if aCacheDiskEnabled:
                someFilesToDelete = [ ]
                self._pAllFilePathsInto( aCacheDiskPath, someFilesToDelete)
                if someFilesToDelete:
                    self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
            
             
        return True
        

         
    
    
          
    security.declarePrivate( 'pProcessNotification_FlushCachedTemplatesForElementsUIDs')
    def pProcessNotification_FlushCachedTemplatesForElementsUIDs( theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs, thePeerIdentificationString, thePeerAuthenticationString):
        """Invoked from service exposed to receive notifications from other ZEO clients authenticated with the supplied string, to flush cache entries for elements of the specified Ids.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return self
        
        if theModelDDvlPloneTool == None:
            return self
        
        if theContextualObject == None:
            return self
        
        if not theFlushedElementsUIDs:
            return self
        
        if not theAuthenticationString:
            return self
        
        if not theModelDDvlPloneTool.fVerifyRequesterPeerIdentificationAndAuthentication( thePeerIdentificationString, thePeerAuthenticationString):
            return self
        
        
        someUIDs = theFlushedElementsUIDs
        if not ( isinstance( someUIDs, list) or isinstance( someUIDs, tuple)):
            someUIDs = [ someUIDs, ]
            
    
        self.pFlushCachedTemplatesForImpactedElementsUIDs( theModelDDvlPloneTool, theContextualObject, someUIDs)
        
        return self
        
    
    
    
    
    
    
    
    security.declarePrivate( 'pSendNotification_FlushCachedTemplatesForElementsUIDs')
    def pSendNotification_FlushCachedTemplatesForElementsUIDs(self, theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs):
        """Try to send notification to flush the elements to all other client ZOPEs hitting the same ZODB server.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return self
        
        if not theModelDDvlPloneTool:
            return self
        
        someCachedStoreNames = self.fGetCacheStoreNamesOfKind( theModelDDvlPloneTool, theContextualObject, cCacheKind_ForElements)
        todosPeersToNotify = [ ]
        for aCacheName in someCachedStoreNames:
            aPeersToNotify = theModelDDvlPloneTool.fGetAllCachesConfigParameterValue( theContextualObject, cAllCachesConfigPpty_PeersToNotify)
            if aPeersToNotify:
                todosPeersToNotify.extend( aPeersToNotify)
                
        if todosPeersToNotify:
            """
            Construct and send to all Peers requests to invalidate cache entries with the flushed UIDs
            """
            pass
        
            
        return self
    
    
    
    security.declareProtected( permissions.View, 'fCached_HTML')
    def fCached_HTML(self, theModelDDvlPloneTool, theContextualObject, theCacheEntryUniqueId, theAdditionalParams=None):
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        
        if theModelDDvlPloneTool == None:
            return False

        aCacheEntryUniqueId = theCacheEntryUniqueId
        if isinstance( aCacheEntryUniqueId, str) or isinstance( aCacheEntryUniqueId, unicode):
            if not aCacheEntryUniqueId:
                return False
            aCacheEntryUniqueId = 0
            try:
                aCacheEntryUniqueId = int( theCacheEntryUniqueId)
            except:
                return False
            
        if not aCacheEntryUniqueId:
            return False

        unHTML  = ''
        unTitle = ''

        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            unaCacheEntry = self._fGetCachedEntryById( theModelDDvlPloneTool, theContextualObject, aCacheEntryUniqueId)
            if unaCacheEntry:
                unHTML = unaCacheEntry.vHTML
                if unaCacheEntry.fIsForElement():
                    unTitle = unaCacheEntry.vTitle
        
                                                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        if unTitle:
            unRenderedTitle = cRenderedTitle_HTML % fCGIE( unTitle)
            unHTML = '%s\n%s\n' % ( unRenderedTitle, unHTML,)

        return unHTML
    
    
        
    
    security.declarePrivate( 'fFlushCachedTemplateByUniqueId')
    def fFlushCachedTemplateByUniqueId(self, theModelDDvlPloneTool, theContextualObject, theCacheEntryUniqueId, theFlushDiskCache=False):
        """Invoked by authorized users requesting invalidation of the cache entry given an id unique among all cache entries in all caches.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        
        if theModelDDvlPloneTool == None:
            return False

        aCacheEntryUniqueId = theCacheEntryUniqueId
        if isinstance( aCacheEntryUniqueId, str) or isinstance( aCacheEntryUniqueId, unicode):
            if not aCacheEntryUniqueId:
                return False
            aCacheEntryUniqueId = 0
            try:
                aCacheEntryUniqueId = int( theCacheEntryUniqueId)
            except:
                return False
            
        if not aCacheEntryUniqueId:
            return False
        
        
        # ###########################################################
        """Try to flush cached content, from within a thread-safe protected critical section.
        
        """
        
        someFilesToDelete = [ ]

        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            unaCacheEntry = self._fGetCachedEntryById( theModelDDvlPloneTool, theContextualObject, aCacheEntryUniqueId)
            if not unaCacheEntry:
                return  False
        
            self._pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, [ unaCacheEntry,], theFilesToDelete=someFilesToDelete)                             
                                                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       
        if theFlushDiskCache:
            if someFilesToDelete:
                self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)

            
        return True        

    
    
    
    
    
    
    

    
    
        
            
            
            
    
    # ###################################################################
    """Flush Cache entries associated with specific elements.
    
    """

       
    security.declarePrivate( 'fFlushCachedTemplateForElement')
    def fFlushCachedTemplateForElement(self, theModelDDvlPloneTool, theFlushCacheCode, theContextualObject, theTemplateName, theFlushDiskCache=False):
        """If theFlushCacheCode is a recently issued cache entry flush authorization code, Flush the cache entry, and disk file, for an element, for the currently negotiared language, for the specified view.
        
        """
        if not theModelDDvlPloneTool:
            return False

        if ( theContextualObject == None):
            return False

        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        

        # ###########################################################
        """Try to flush cached content, from within a thread-safe protected critical section.
        
        """
        
        someFilesToDelete = [ ]
        aCacheEntry = None
        
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            aCacheEntry, aDirectory, aFilePath = self._fFindCachedEntryAndDirectoryAndFilePathForElement( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theEnforceThreadSafety=False)
    
            aCanFlushDiskCache = False
            someFilesToDelete = None
            if theFlushDiskCache:
                someFilesToDelete = [ ]
            
            if aCacheEntry: 
                aCanFlushMemoryCache, aCanFlushDiskCache = self.fCacheIdAllowsFlushMemoryAndDisk( theModelDDvlPloneTool, theContextualObject, theFlushCacheCode, theTemplateName, aCacheEntry)
                if aCanFlushMemoryCache:
                    self._pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, [ aCacheEntry,], theFilesToDelete=someFilesToDelete)                             
        
            
                                                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

       

        
            
        if theFlushDiskCache:
            if not aCacheEntry:
                aCanFlushDiskCache = self.fCacheIdAllowsFlushDisk( theModelDDvlPloneTool, theContextualObject, theFlushCacheCode, theTemplateName,)
                if aCanFlushDiskCache:
                    someFilesToDelete.append( aFilePath)
                    self._pAllFilePathsInto( aDirectory, someFilesToDelete)
                
        if theFlushDiskCache:
            if aCanFlushDiskCache:
                if someFilesToDelete:
                    self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
                
        return True
    
        
    
    

    
    security.declarePrivate( 'fCacheIdAllowsFlushMemoryAndDisk')
    def fCacheIdAllowsFlushMemoryAndDisk(self, theModelDDvlPloneTool, theContextualObject, theFlushCacheCode, theTemplateName, theCacheEntry):

        if not theFlushCacheCode:
            return [ False,  False,]

        return [ True, True,]
    

    
    security.declarePrivate( 'fCacheIdAllowsFlushDisk')
    def fCacheIdAllowsFlushDisk(self, theModelDDvlPloneTool, theContextualObject, theFlushCacheCode, theTemplateName, ):

        if not theFlushCacheCode:
            return False

        return True
        

    
    
    security.declarePrivate( 'fNoCacheIdAllowsRender')
    def fNoCacheIdAllowsRender(self, theModelDDvlPloneTool, theContextualObject, theNoCacheCode,  theTemplateName, ):

        if not theNoCacheCode:
            return False

        return True
        
    
    
    security.declarePrivate( 'fFlushAllCachedTemplatesForElement')
    def fFlushAllCachedTemplatesForElement(self, theModelDDvlPloneTool, theContextualObject, theFlushDiskCache=False):
        """Flush all the cache entries, and disk files, for an element.
        
        """
        if not theModelDDvlPloneTool:
            return False

        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        
        anElementUID = ''
        try:
            anElementUID = theContextualObject.UID()
        except:
            None
            
        if anElementUID:
            self.pFlushCachedTemplatesForImpactedElementsUIDs( theModelDDvlPloneTool, theContextualObject, [ anElementUID,],)

            
            
        someFilesToDelete = [ ]

        someDirectories= self.fDirectoriesForElement( theModelDDvlPloneTool, theContextualObject)
        for aDirectory in someDirectories:
            self._pAllFilePathsInto( aDirectory, someFilesToDelete)
                 
        if someFilesToDelete:
            self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
         
        return True
    
        
    

  
    
    
    
    
    
    
    
        
    security.declarePrivate( 'pFlushCachedTemplatesForImpactedElementsUIDs')
    def pFlushCachedTemplatesForImpactedElementsUIDs(self, theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs, theViewsToFlush=[]):
        """Invoked by the public tool singleton to remove cache entries for elements reported as invalidated by change operations effect reports. It may be also initiated by the element intercepting side-effect of drag&drop reorder. It may be also initiated by the tool receiving an external notification sent from other instance of elements given their UIDs whose cache entries have been invalidated by changes in the elements, their content, or related elements.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return self
        
        if theModelDDvlPloneTool == None:
            return self
        
        if not theFlushedElementsUIDs:
            return self
        # ###########################################################
        """Try to flush cached content, from within a thread-safe protected critical section.
        
        """
        
        someFilesToDelete = [ ]

        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            someCacheEntriesToFlush = self._fGetCachedEntriesByManyUIDs( theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs, theViewsToFlush=theViewsToFlush)
                
            if someCacheEntriesToFlush:
                self._pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, someCacheEntriesToFlush, theFilesToDelete=someFilesToDelete)                             
                                                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            
            
        # ###########################################################
        """Flush all disk cache files for the elements given their UIDs.
        
        """
            
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        
        for aFlushedElementUID in theFlushedElementsUIDs:
            
            anElementByUID = aModelDDvlPloneTool_Retrieval.fElementoPorUID( aFlushedElementUID, theContextualObject)
            
            if not ( anElementByUID == None):
            
                someDirectories= self.fDirectoriesForElement( theModelDDvlPloneTool, anElementByUID)
                for aDirectory in someDirectories:
                    self._pAllFilePathsInto( aDirectory, someFilesToDelete)
                     

        if someFilesToDelete:
            self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
        
       
        # ###########################################################
        """Try to send notification to flush the elements to all other client ZOPEs hitting the same ZODB server. Note that this method must have been invoked upon receiving a notification of this kind from other ZEO client, therefore the peer synchronization mechanism shall take care of notifying those peers except the one that sent the nofication.
        
        """
        self.pSendNotification_FlushCachedTemplatesForElementsUIDs( theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs)
        
        
        return self
        

    
    
    

    
    
    security.declarePrivate( '_pRemoveDiskCacheFiles')
    def _pRemoveDiskCacheFiles(self, theModelDDvlPloneTool, theContextualObject, theFilesToDelete=None):
        
        if not theFilesToDelete:
            return self
        
        
        
        someCache_NumFilesCleared    = { }
        someCache_NumCharsDiskFreed  = { }
        
        someCacheNames = self.fGetCacheStoreNames( theModelDDvlPloneTool, theContextualObject, )
        
        somePathsAndCacheNames = [ ]        
        for aCacheName in someCacheNames:
            aCacheDiskPath = self.fGetCacheConfigParameter_CacheDiskPath( theModelDDvlPloneTool, theContextualObject, aCacheName)
            if aCacheDiskPath:
                if not ( aCacheDiskPath[:-1] == os.path.sep):
                    aCacheDiskPath = '%s%s' % ( aCacheDiskPath, os.path.sep)
                somePathsAndCacheNames.append( [ aCacheDiskPath, aCacheName, ])
                

        for aFilePath in theFilesToDelete:
            if aFilePath:
                
                aFilePathExists = False
                try:
                    aFilePathExists = os.path.exists( aFilePath)
                except:
                    None
            
                if aFilePathExists:
                    
                    aFoundCacheName = ''
                    for aCachePath, aCacheName in somePathsAndCacheNames:
                        if aFilePath.startswith( aCachePath):
                            aFoundCacheName = aCacheName
                            break
                            
                    aFileSize = 0
                    try:
                        aFileSize  = os.path.getsize( aFilePath)
                    except:
                        None
                    if aFileSize:
                        if aFoundCacheName:
                            someCache_NumCharsDiskFreed[ aFoundCacheName] = someCache_NumCharsDiskFreed.get( aFoundCacheName, 0) + aFileSize
                        
                    aTruncated = False
                    try:
                        aFile  = None
                        try:
                            aFile = open( aFilePath, cCacheDisk_ElementIndependent_FileOpenTruncateMode_View, cCacheDisk_ElementIndependent_FileOpenTruncateBuffering_View)
                            aFile.truncate( 0)
                        finally:
                            if aFile:
                                aFile.close()
                        
                        aTruncated = True
                                
                        if aFoundCacheName:
                            someCache_NumFilesCleared[ aFoundCacheName] = someCache_NumFilesCleared.get( aFoundCacheName, 0) + 1
                    except IOError:
                        None
                        
                        
        # ###########################################################
        """Update statistics with the cleared files and sizes, within a protected section.
        
        """

        if someCache_NumFilesCleared or someCache_NumCharsDiskFreed:
            
            try:
                # #################
                """MUTEX LOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                for aCacheName in someCacheNames:
                    
                    aNumFilesCleared   = someCache_NumFilesCleared.get(   aCacheName, 0)
                    aNumCharsDiskFreed = someCache_NumCharsDiskFreed.get( aCacheName, 0)
                    
                    if aNumFilesCleared or aNumCharsDiskFreed:
                        unStatisticsUpdate = {
                            cCacheStatistics_TotalFilesCleared:   aNumFilesCleared,
                            cCacheStatistics_TotalCharsDiskFreed: aNumCharsDiskFreed,
                        }
                        self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
 
            
            finally:
                # #################
                """MUTEX UNLOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                  
                        
                        
        
        return self
    
    
        
        
    
   
    
    
    
    security.declarePrivate( '_pAllFilePathsInto')
    def _pAllFilePathsInto(self, theDirectory, theFilesToDelete):
        if not theDirectory:
            return self
        
        if ( theFilesToDelete == None):
            return self
        
                            
        unDirectoryExists = False
        try:
            unDirectoryExists = os.path.exists( theDirectory)
        except:
            None
        if not unDirectoryExists:
            return self
        
        aFilesToDeleteSet = set( theFilesToDelete)
        for unRoot, unosDirectories, unosFileNames in os.walk( theDirectory):
            
            for unFileName in unosFileNames:
                
                unFilePath = os.path.join( unRoot, unFileName)
                
                if not ( unFilePath in aFilesToDeleteSet):
                    
                    theFilesToDelete.append( unFilePath)
                    
                    aFilesToDeleteSet.add( unFilePath)
                
        return self
        
        
        
        
   
    security.declarePrivate( '_pAllFilePathsInto_Filtering')
    def _pAllFilePathsInto_Filtering(self, theDirectory, theSubDirectoryNames, theFilesToDelete):
        if not theDirectory:
            return self
        
        if ( theFilesToDelete == None):
            return self
        
                            
        unDirectoryExists = False
        try:
            unDirectoryExists = os.path.exists( theDirectory)
        except:
            None
        if not unDirectoryExists:
            return self
        
        aFilesToDeleteSet = set( theFilesToDelete)
        for unRoot, unosDirectories, unosFileNames in os.walk( theDirectory):
            
            for unFileName in unosFileNames:
                
                if ( not theSubDirectoryNames) or (  unFileName in theSubDirectoryNames):
                
                    unFilePath = os.path.join( unRoot, unFileName)
                    
                    if not ( unFilePath in aFilesToDeleteSet):
                        
                        theFilesToDelete.append( unFilePath)
                        
                        aFilesToDeleteSet.add( unFilePath)
                
        return self
        
            
    
    
    
    
    
    
    
    
    
    
                    
    
    security.declarePrivate( '_pFlushCacheEntries')
    def _pFlushCacheEntries(self, theModelDDvlPloneTool, theContextualObject, theCacheEntriesToFlush, theFilesToDelete=None):
        """Invoked from this class, within a CRITICAL SECTION To release memory before caching more templates, or after modification of an elements values, contained elements or relations, Remove the cached rendered templates for the elements with specified UIDs.
        TODO: ACV OJO 20091219 Only works with entries ForElements or ForUsers. Will raise exception if an ElementDependent entry is flushed here.
        
        """

        if theModelDDvlPloneTool == None:
            return self
        

        if not theCacheEntriesToFlush:
            return self
        
        
        # ###########################################################
        """Release cache entries. This shall be invoked from within a thread-safe protected critical section.
        
        """
            

        unasEntriesToRemove                 = [ ]
        unosObjectsToDelete                 = [ ]
        unosCachesAndProjectNamesToRemove   = [ ]
        
        unTotalCacheEntriesFlushed = 0
        unTotalCharsFlushed        = 0
        
        for unaCacheEntryToFlush in theCacheEntriesToFlush:
    
            if not unaCacheEntryToFlush.vValid:
                unasEntriesToRemove.append( unaCacheEntryToFlush)
                continue
            
            if not unaCacheEntryToFlush.vPromise:
                unasEntriesToRemove.append( unaCacheEntryToFlush)
                continue
            
            if not ( unaCacheEntryToFlush.vPromise == cCacheEntry_PromiseFulfilled_Sentinel):
                continue
            
            
            aFilePath    = unaCacheEntryToFlush.vFilePath
            if not( theFilesToDelete == None):
                if aFilePath:
                    theFilesToDelete.append( aFilePath)
             
            
            if unaCacheEntryToFlush.fIsForElement():
                # ###########################################################
                """Drill-down through the cache control structure, remove cached entry if found, and remove cache control structure elements that are left empty.
                The cache control structure is organized by:
                    Project
                        Language
                            Element UID
                                View Name
                                    -when applicable - Relation name
                                        -when applicable - Current related element UID
                                            - role kind or user id : the Entry
                """
            
                aCacheName   = unaCacheEntryToFlush.vCacheName
                aProjectName = unaCacheEntryToFlush.vProject
                aLanguage    = unaCacheEntryToFlush.vLanguage
                anElementUID = unaCacheEntryToFlush.vUID
                aViewName    = unaCacheEntryToFlush.vView
                aRelationName= unaCacheEntryToFlush.vRelation 
                aCurrentUID  = unaCacheEntryToFlush.vCurrentUID
                aRoleKind    = unaCacheEntryToFlush.vRoleKind
                aDirectory   = unaCacheEntryToFlush.vDirectory
                
                        
                if not( theFilesToDelete == None):
                    unDirectoryExists = False
                    try:
                        unDirectoryExists = os.path.exists( aDirectory)
                    except:
                        None
                    if unDirectoryExists:
                        self._pAllFilePathsInto( aDirectory, theFilesToDelete)
                                           
                if not ( aProjectName and aLanguage and anElementUID and aViewName and aRelationName and aCurrentUID and aRoleKind):
                    unasEntriesToRemove.append( unaCacheEntryToFlush)
                    continue

                
                unasEntriesToRemove.append( unaCacheEntryToFlush)
                
                someCachedTemplatesForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)              
                if someCachedTemplatesForProject:
                
                
                    someCachedTemplateForLanguage = someCachedTemplatesForProject.get( aLanguage, None)
                    if someCachedTemplateForLanguage:
                            
                        someCachedTemplatesForElement = someCachedTemplateForLanguage.get( anElementUID, None)
                        if someCachedTemplatesForElement:
                            
                            someCachedTemplatesForView = someCachedTemplatesForElement.get( aViewName, None)
                            if someCachedTemplatesForView:
                                
                                someCachedTemplatesForRelation = someCachedTemplatesForView.get( aRelationName, None)
                                if someCachedTemplatesForRelation:
                                    
                                    someCachedTemplatesForCurrentUID = someCachedTemplatesForRelation.get( aCurrentUID, None)
                                    if someCachedTemplatesForCurrentUID:
                                
                                        unaFoundCacheEntry = someCachedTemplatesForCurrentUID.get( aRoleKind, None)
                                        
                                        if unaFoundCacheEntry and ( unaFoundCacheEntry == unaCacheEntryToFlush):
                                                                                                    
                                            try:
                                                someCachedTemplatesForCurrentUID.pop( aRoleKind)
                                            except:
                                                None
                                    
                                                                      
  
                                        if not someCachedTemplatesForCurrentUID:
                                            someCachedTemplatesForRelation.pop( aCurrentUID)
                                            unosObjectsToDelete.append( someCachedTemplatesForCurrentUID)
    
                                            
                                    if not someCachedTemplatesForRelation:
                                        someCachedTemplatesForView.pop( aRelationName)
                                        unosObjectsToDelete.append( someCachedTemplatesForRelation)
                                        
                                if not someCachedTemplatesForView:
                                    someCachedTemplatesForElement.pop( aViewName)
                                    unosObjectsToDelete.append( someCachedTemplatesForView)
        
                            if not someCachedTemplatesForElement:
                                someCachedTemplateForLanguage.pop( anElementUID)
                                unosObjectsToDelete.append( someCachedTemplatesForElement)
            
                        if not someCachedTemplateForLanguage:
                            someCachedTemplatesForProject.pop( aLanguage)
                            unosObjectsToDelete.append( someCachedTemplateForLanguage)
                                
                    if not someCachedTemplatesForProject:
                        unosCachesAndProjectNamesToRemove.append( [ aCacheName, aProjectName,])
                                
            else:
                # ###########################################################
                """Drill-down through the cache control structure, remove cached entry if found, and remove cache control structure elements that are left empty.
                The cache control structure is organized by:
                    Project
                        Language
                            View Name : the Entry
                """
            
                aCacheName   = unaCacheEntryToFlush.vCacheName
                aProjectName = unaCacheEntryToFlush.vProject
                aLanguage    = unaCacheEntryToFlush.vLanguage
                aViewName    = unaCacheEntryToFlush.vView

                                           
                if not ( aProjectName and aLanguage and aViewName):
                    unasEntriesToRemove.append( unaCacheEntryToFlush)
                    continue

                
                unasEntriesToRemove.append( unaCacheEntryToFlush)
                
                someCachedTemplatesForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)              
                if someCachedTemplatesForProject:
                
                
                    someCachedTemplateForLanguage = someCachedTemplatesForProject.get( aLanguage, None)
                    if someCachedTemplateForLanguage:
                            
                        unaFoundCacheEntry = someCachedTemplateForLanguage.get( aViewName, None)
                        
                        if unaFoundCacheEntry and ( unaFoundCacheEntry == unaCacheEntryToFlush):
                                                                                    
                            try:
                                someCachedTemplateForLanguage.pop( aViewName)
                            except:
                                None
                                    
                        if not someCachedTemplateForLanguage:
                            someCachedTemplatesForProject.pop( aLanguage)
                            unosObjectsToDelete.append( someCachedTemplateForLanguage)
                                
                    if not someCachedTemplatesForProject:
                        unosCachesAndProjectNamesToRemove.append( [ aCacheName, aProjectName,])
                                
                        
        # ###########################################################
        """Decrease total of number of entries and memory used. 
        
        """
        
        if unasEntriesToRemove:
            
        
            unTotalCharsFlushed      = 0
            unNumEntriesFlushed      = 0
            
            for aCacheEntry in unasEntriesToRemove:

                aCacheEntry.pUnLink()
                
                unosObjectsToDelete.append( aCacheEntry)

                unNumEntriesFlushed += 1

                if aCacheEntry.vValid:
                        
                    unCachedHTML = aCacheEntry.vHTML
                    if unCachedHTML:
                        unTotalCharsFlushed += len( unCachedHTML)
                        unosObjectsToDelete.append( unCachedHTML)
                        
                                                                            
            unStatisticsUpdate = {
                cCacheStatistics_TotalEntriesFlushed: unNumEntriesFlushed,
                cCacheStatistics_TotalCharsFlushed:   unTotalCharsFlushed,
                cCacheStatistics_TotalCacheEntries:   0 - unNumEntriesFlushed,
                cCacheStatistics_TotalCharsCached:    0 - unTotalCharsFlushed,
            }
            self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
            
            
            
            
            # ###########################################################
            """Remove the entries from the linked list, the dict by UIs, the promised entries, and delete the entries from memory. 
            
            """
            
            
            self._pRemoveCacheEntriesFromUniqueIdIndex( theModelDDvlPloneTool, theContextualObject, unasEntriesToRemove)

            self._pRemoveCacheEntriesFromUIDIndex( theModelDDvlPloneTool, theContextualObject, unasEntriesToRemove)
                

                
            # ###########################################################
            """mark the entry as no longer valid for any purpose 
            
            """
            for aCacheEntry in unasEntriesToRemove:

                aCacheEntry.pBeGone()
            
            
        # ###########################################################
        """Remove the root structure object for a project name that has been emptied. 
        
        """
        for unCacheNameToRemove, unProjectNameToRemove in unosCachesAndProjectNamesToRemove: 
            if unCacheNameToRemove and unProjectNameToRemove:
                self.pRemoveRootProjectFromCacheStore( theModelDDvlPloneTool, theContextualObject, unCacheNameToRemove, unProjectNameToRemove)
            
            
            
            
        # ###########################################################
        """Delete from memory the structure objects holding the entries, that have been emptied. 
        
        """
        if unosObjectsToDelete:
            del unosObjectsToDelete
                    
        return self
        

    

    
    
            


    
    def _pFlushCacheEntriesForcedtoExpire( self, theModelDDvlPloneTool, theContextualObject, theFilesToDelete=None):
        """MEMORY consumed maintenance: Release cached templates expired, and forced to expire in any of the caches. 
        
        """
        
        someCacheNames = self.fGetCacheStoreNames( theModelDDvlPloneTool, theContextualObject, )
        
        
        aMillisecondsNow = fMillisecondsNow()
        
        
        for aCacheName in someCacheNames:
            
            if not self.fGetCacheConfigParameter_ForceExpire( theModelDDvlPloneTool, theContextualObject, aCacheName):
                continue
            
            anOld_Sentinel = self.fGetCacheStoreListSentinel_Old( theModelDDvlPloneTool, theContextualObject, aCacheName)
            
            if not anOld_Sentinel:
                continue
            
            someCacheEntriesToRelease = []
            
            unCurrentCacheEntry = anOld_Sentinel.vNext
            
            while unCurrentCacheEntry and ( not unCurrentCacheEntry.fIsSentinel()):
                
                if not unCurrentCacheEntry.vValid:
                    someCacheEntriesToRelease.append( unCurrentCacheEntry)
                    continue
                
                if ( not unCurrentCacheEntry.vPromise) or ( unCurrentCacheEntry.vPromise  and ( unCurrentCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel)):
                    
                    if ( unCurrentCacheEntry.vLastHit + ( unCurrentCacheEntry.vExpireAfterSeconds * 1000) ) <= aMillisecondsNow:
                        
                        someCacheEntriesToRelease.append( unCurrentCacheEntry)
                    
                    else:
                        break
                            
                unCurrentCacheEntry = unCurrentCacheEntry.vNext
                    
                        
            if someCacheEntriesToRelease:
                self._pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, someCacheEntriesToRelease, theFilesToDelete=theFilesToDelete)
        
        return self              
          
    
    
    
    
    
    def _pFlushCacheEntriesToReduceMemoryUsed( self, theModelDDvlPloneTool, theContextualObject, theCacheName, ):
        """Invoked from this class within a CRITICAL SECTION. MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
        
        """

        
        aTotalCharsCached          = self.fGetCacheStatisticValue( theModelDDvlPloneTool, theContextualObject, theCacheName, cCacheStatistics_TotalCharsCached)

        aMaxCharsCached_ConfigurationParameterValue             = theModelDDvlPloneTool.fGetCacheConfigParameterValue( theContextualObject, theCacheName, cCacheConfigPpty_MaxCharsCached)
        aMinThresholdCharsToRelease_ConfigurationParameterValue = theModelDDvlPloneTool.fGetCacheConfigParameterValue( theContextualObject, theCacheName, cCacheConfigPpty_MinThresholdCharsToRelease)
        
        aMillisecondsNow = fMillisecondsNow()
        
        someCacheEntriesToRelease = []
        someCharsToRelease        = 0

        
        anOld_Sentinel = self.fGetCacheStoreListSentinel_Old( theModelDDvlPloneTool, theContextualObject,theCacheName)
        if not anOld_Sentinel:
            return self

                
        if ( aTotalCharsCached - someCharsToRelease) >= ( aMaxCharsCached_ConfigurationParameterValue + aMinThresholdCharsToRelease_ConfigurationParameterValue):
            # ###########################################################
            """Cache Entries shall be flushed, as many as necessary to bring the memory used under the limit and threshold, but without deleting its disk cache file, if exist.
            Hysteresis : Clean up a bit more memory than the maximum configured, and do not clean up immediately on hitting the limit, such that no all request produce a clean up of used memory.
            
            """  
                        
            unCurrentCacheEntry = anOld_Sentinel.vNext
            
            while unCurrentCacheEntry and ( not unCurrentCacheEntry.fIsSentinel()) and \
                ( aTotalCharsCached - someCharsToRelease) > ( aMaxCharsCached_ConfigurationParameterValue - aMinThresholdCharsToRelease_ConfigurationParameterValue):
                
                if not unCurrentCacheEntry.vValid:
                    someCacheEntriesToRelease.append( unCurrentCacheEntry)
                    continue
                
                if ( not unCurrentCacheEntry.vPromise) or ( unCurrentCacheEntry.vPromise  and ( unCurrentCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel)):
                                            
                    someCacheEntriesToRelease.append( unCurrentCacheEntry)
                    
                    unCachedTemplate = unCurrentCacheEntry.vHTML
                    if unCachedTemplate:
                        
                        someCharsToRelease += len( unCachedTemplate)
            
                unCurrentCacheEntry = unCurrentCacheEntry.vNext
                    
            self._pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, someCacheEntriesToRelease, )
        
        return self              
    

    
    
    
    
    

            

    
    # ###################################################################
    """Directories associated with specific element.
    
    """
       
    security.declarePrivate( 'fDirectoriesForElement')
    def fDirectoriesForElement(self, theModelDDvlPloneTool, theContextualObject, ):
        """The Disk Cache Directory for an element, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
        someDirectories = [ ]
                
        if theModelDDvlPloneTool == None:
            return someDirectories

        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return someDirectories
          
        if theContextualObject == None:
            return someDirectories
        
        
        # ###########################################################
        """Only cache objects that allow caching.
        
        """
        anIsCacheable = False
        try:
            anIsCacheable = theContextualObject.fIsCacheable()
        except:
            None
        if not anIsCacheable:    
            return someDirectories
            
        
        
        
        
        # ###########################################################
        """Gather all information to look up the cache for a matching cached entry with a rendered template.
        
        """
        aProjectName = ''
        try:
            aProjectName = theContextualObject.getNombreProyecto()
        except:
            None
        if not aProjectName:    
            aProjectName = cDefaultNombreProyecto
              
        
        unElementUID = ''
        try:
            unElementUID = theContextualObject.UID()
        except:
            None
        if not unElementUID:
            return someDirectories
        
               
        unRootElementUID = ''
        
        unRootElement = None
        try:
            unRootElement = theContextualObject.getRaiz()
        except:
            None
        if ( unRootElement == None):
            unRootElementUID  = unElementUID
            unRootElementPath = unElementPath
        else:
            try:
                unRootElementUID     = unRootElement.UID()
            except:
                None
            if not unRootElementUID:
                unRootElementUID = unElementUID
                
                        
        someCacheDiskPaths = [ ]
        
        
        # ###################################################################
        """CRITICAL SECTION to access configuration information.
        
        """
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            # ###########################################################
            """Retrieve within thread safe section, to be used later, the configuration paameters specifying: whether to render a cache hit information collapsible section at the top or bottom of the view, or none at all, whether the disk caching is enabled, and the disk cache files base path.
            
            """
            for aCacheName in [ cCacheName_ForElements, cCacheName_ForUsers, ]:
                
                aCacheDiskEnabled        = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskEnabled)
                
                if aCacheDiskEnabled:
                    aCacheDiskPath       = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskPath)
                    
                    if aCacheDiskPath:
                        someCacheDiskPaths.append( aCacheDiskPath)
                        
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            


    
        # ###########################################################
        """Assemble the names of the directories )one per cache: for elements, and for users) holding all disk files with cached HTML for all entries on the element.
            
        """            
                
        for aCacheDiskPath in someCacheDiskPaths:
            aProjectPath           = os.path.join( aCacheDiskPath, aProjectName)
            aRootUIDPath           = os.path.join( aProjectPath, unRootElementUID)
            anElementUIDModulus    = self.fModulusUID( unElementUID, cCacheDisk_UIDModulus)
            aElementUIDModulusPath = os.path.join( aRootUIDPath, anElementUIDModulus)
            aElementUIDPath        = os.path.join( aElementUIDModulusPath, unElementUID)
    
            someDirectories.append(  aElementUIDPath)
        
        return someDirectories
    
    
                
                

    
    
                
    
    
    
    # ###################################################################
    """Find Cache entries associated with specific elements, or some projects and languages.
    
    """
    security.declarePrivate( 'fFindCachedEntryAndDirectoryAndFilePathForElement')
    def fFindCachedEntryAndDirectoryAndFilePathForElement(self, theModelDDvlPloneTool, theContextualObject, theTemplateName,):
        """ Return an existing CacheEntry from cache, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """

        if theModelDDvlPloneTool == None:
            return [ None, '', '',]

        if theContextualObject == None:
            return [ None, '', '',]

        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return [ None, '', '',]          
        
        return self._fFindCachedEntryAndDirectoryAndFilePathForElement( theModelDDvlPloneTool, theContextualObject, theTemplateName, theEnforceThreadSafety=True)

    
    
    
    
    
    
       
    security.declarePrivate( '_fFindCachedEntryAndDirectoryAndFilePathForElement')
    def _fFindCachedEntryAndDirectoryAndFilePathForElement(self, theModelDDvlPloneTool, theContextualObject, theTemplateName, theEnforceThreadSafety=True):
        """ Return an existing CacheEntry from cache, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
        unaCachedEntry = None
        unDirectory    = ''
        unFilePath     = ''
                
        if theModelDDvlPloneTool == None:
            return [ unaCachedEntry, unDirectory, unFilePath,]

        if theContextualObject == None:
            return [ unaCachedEntry, unDirectory, unFilePath,]
        
        
        # ###########################################################
        """Only cache objects that allow caching.
        
        """
        anIsCacheable = False
        try:
            anIsCacheable = theContextualObject.fIsCacheable()
        except:
            None
        if not anIsCacheable:    
            return [ unaCachedEntry, unDirectory, unFilePath,]
            
        
        
        
        
        # ###########################################################
        """Gather all information to look up the cache for a matching cached entry with a rendered template.
        
        """
        aProjectName = ''
        try:
            aProjectName = theContextualObject.getNombreProyecto()
        except:
            None
        if not aProjectName:    
            aProjectName = cDefaultNombreProyecto
              
        
        unElementUID = ''
        try:
            unElementUID = theContextualObject.UID()
        except:
            None
        if not unElementUID:
            return [ unaCachedEntry, unDirectory, unFilePath,]
        
               
        unRootElementUID = ''
        unRootElementPath = ''
        
        unRootElement = None
        try:
            unRootElement = theContextualObject.getRaiz()
        except:
            None
        if ( unRootElement == None):
            unRootElementUID  = unElementUID
            unRootElementPath = unElementPath
        else:
            unRootElementPath = '/'.join( unRootElement.getPhysicalPath())
            try:
                unRootElementUID     = unRootElement.UID()
            except:
                None
            if not unRootElementUID:
                unRootElementUID = unElementUID
                unRootElementPath = unElementPath
                
                
        
        # ###########################################################
        """Determine if the user specific cache should be used. Determine the role kind to use to index the cache entry.
        
        """
        aCacheName       = cCacheName_ForElements
        aCacheKind       = cCacheKind_ForElements
        
        aRoleKindToIndex = cRoleKind_Anonymous
        
        aRoleKind, unMemberId, aRoleName = self.fGetMemberRoleKindAndUserId( theContextualObject, theTemplateName)
        aRoleKindToIndex = aRoleKind

        if ( aRoleKind == cRoleKind_UserSpecific):
            if self.fIsPrivateCacheViewForQualifiedUsers( theContextualObject, theTemplateName): 
                aRoleKindToIndex = unMemberId
                aCacheName       = cCacheName_ForUsers
                aCacheKind       = cCacheKind_ForUsers
            else:
                aRoleKindToIndex = aRoleName
                aCacheName       = cCacheName_ForElements
                aCacheKind       = cCacheKind_ForElements
               
        
        if not aRoleKindToIndex:
            return [ unaCachedEntry, unDirectory, unFilePath,]
            
                        
                
        # ###################################################################
        """If theEnforceThreadSafety : CRITICAL SECTION to access configuration information.
        
        """
        try:
            
            # #################
            """If theEnforceThreadSafety MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if theEnforceThreadSafety:
                self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            # ###########################################################
            """Retrieve within thread safe section, to be used later, the configuration paameters specifying: whether to render a cache hit information collapsible section at the top or bottom of the view, or none at all, whether the disk caching is enabled, and the disk cache files base path.
            
            """
            aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskEnabled)
            aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskPath)

        finally:
            # #################
            """If theEnforceThreadSafety MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if theEnforceThreadSafety:
                self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            


                   
        if aCacheDiskEnabled:           
            # ###########################################################
            """Assemble the name of the directory holding all disk files with cached HTML for all entries on the element.
                
            """            
                    
            aProjectPath           = os.path.join( aCacheDiskPath, aProjectName)
            aRootUIDPath           = os.path.join( aProjectPath, unRootElementUID)
            anElementUIDModulus    = self.fModulusUID( unElementUID, cCacheDisk_UIDModulus)
            aElementUIDModulusPath = os.path.join( aRootUIDPath, anElementUIDModulus)
            aElementUIDPath        = os.path.join( aElementUIDModulusPath, unElementUID)

            unDirectory = aElementUIDPath
            
            
            
            
        # ###########################################################
        """Determine the language under which to register the cache entry.
        
        """
        unosPreferredLanguages = getLangPrefs( theContextualObject.REQUEST)
        if not unosPreferredLanguages:
            return [ unaCachedEntry, unDirectory, unFilePath,]
        
        aNegotiatedLanguage = unosPreferredLanguages[ 0]   
        if not aNegotiatedLanguage:
            return [ unaCachedEntry, unDirectory, unFilePath,]
            
            
                 
        # ###########################################################
        """Determine the view name.
        
        """
        aViewName = theTemplateName
        if not aViewName:
            return  False
        if aViewName.find( '%s') >= 0:
            if not ( aProjectName == cDefaultNombreProyecto):
                aViewName = aViewName % aProjectName
            else:
                aViewName = aViewName.replace( '%s', '')
        if not aViewName:
            return [ unaCachedEntry, unDirectory, unFilePath,]
        
        unRelationCursorName = ''
        unCurrentElementUID  = ''
        
        unaRequest = theContextualObject.REQUEST
        if unaRequest:
            unRelationCursorName = unaRequest.get( 'theRelationCursorName', '')
            unCurrentElementUID = unaRequest.get( 'theCurrentElementUID', '')
                
        if not unRelationCursorName:
            unRelationCursorName = cNoRelationCursorName
        if not unCurrentElementUID:
            unCurrentElementUID = cNoCurrentElementUID
                        

               
        if aCacheDiskEnabled:           
            # ###########################################################
            """Assemble the name of the directory holding all disk files with cached HTML for all entries on the element.
                
            """            
                    
            aLanguagePath          = os.path.join( aElementUIDPath, aNegotiatedLanguage)
            aFileName              = '%s-%s-%s-%s%s' % ( aViewName, unRelationCursorName, unCurrentElementUID, aRoleKindToIndex, cCacheDiskFilePostfix)
            
            unFilePath             = os.path.join( aLanguagePath, aFileName)
            
            
            
        if cForbidCaches or not self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, aCacheName):
            return [ unaCachedEntry, unDirectory, unFilePath,]
        

            
        # ###################################################################
        """IF theEnforceThreadSafety: CRITICAL SECTION to access and modify cache control structure, for Cache entries associated with specific elements.
        
        """
        try:
            
            # #################
            """IF theEnforceThreadSafety MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if theEnforceThreadSafety:
                self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
              
            # ###########################################################
            """Traverse cache control structures to access the cache entry corresponding to the parameters. 
            
            """
            someCachedTemplatesForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)                              
            if someCachedTemplatesForProject:
    
                someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aNegotiatedLanguage, None)
                if someCachedTemplatesForLanguage:
        
                    someCachedTemplatesForElement = someCachedTemplatesForLanguage.get( unElementUID, None)
                    if someCachedTemplatesForElement:
                            
                        someCachedTemplatesForView = someCachedTemplatesForElement.get( aViewName, None)
                        if someCachedTemplatesForView:
                
                            someCachedTemplateForRelationCursor = someCachedTemplatesForView.get( unRelationCursorName, None)
                            if someCachedTemplateForRelationCursor:
                                
                                someCachedTemplateForRelatedElement = someCachedTemplateForRelationCursor.get( unCurrentElementUID, None)
                                if someCachedTemplateForRelatedElement:
                                    
                                    unaCachedEntry = someCachedTemplateForRelatedElement.get( aRoleKindToIndex, None)
            
        finally:
            # #################
            """IF theEnforceThreadSafety MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if theEnforceThreadSafety:
                self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                

        return [ unaCachedEntry, unDirectory, unFilePath,]

    
    
         
    
    
    
    
    
    security.declarePrivate( 'fFindSomeCachedEntriesAndFilePaths')
    def fFindSomeCachedEntriesAndFilePaths(self, theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectNames, ):
        """ Return an existing CacheEntry from cache, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
              
        if theModelDDvlPloneTool == None:
            return [ [] , [],]

        if theContextualObject == None:
            return [ [] , [],]
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return [ [] , [],]
          
            
        return self._fFindSomeCachedEntriesAndFilePaths( theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectNames, theEnforceThreadSafety=True)
    
    
    
    
    

       
    security.declarePrivate( '_fFindSomeCachedEntriesAndFilePaths')
    def _fFindSomeCachedEntriesAndFilePaths(self, theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectNames, theEnforceThreadSafety=True):
        """ Return an existing CacheEntry from cache, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
        someCachedEntries = [ ]
        someFilePaths     = [ ]

                
        if theModelDDvlPloneTool == None:
            return [ someCachedEntries, someFilePaths,]

        if theContextualObject == None:
            return [ someCachedEntries, someFilePaths,]
        
            
        if cForbidCaches or not self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, theCacheName):
            return [ someCachedEntries, someFilePaths,]
        

            
        # ###################################################################
        """IF theEnforceThreadSafety CRITICAL SECTION to access and modify cache control structure, for Cache entries associated with specific elements.
        
        """
        try:
            
            # #################
            """IF theEnforceThreadSafety MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if theEnforceThreadSafety:
                self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            # ###########################################################
            """Retrieve within thread safe section, to be used later, the configuration paameters specifying: whether to render a cache hit information collapsible section at the top or bottom of the view, or none at all, whether the disk caching is enabled, and the disk cache files base path.
            
            """
            aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskEnabled)
            aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskPath)
            
            # ###########################################################
            """Traverse cache control structures to access the cache entry corresponding to the parameters. 
            
            """
            allCachedTemplatesForLanguages = [ ]

            someProjectsNames     = [ ]
            if not theProjectNames:
                someProjectsNames = self.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject,)
                
            for aProjectName in someProjectsNames:
                    
                if aCacheDiskEnabled:           
                    # ###########################################################
                    """Assemble the names disk files with cached HTML for entries to be flushed.
                        
                    """            
                    aProjectPath = os.path.join( aCacheDiskPath, aProjectName)   
                    self._pAllFilePathsInto( aProjectPath, someFilePaths)
                        
                    
                
                someCachedTemplatesForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, aProjectName)                              
                if someCachedTemplatesForProject:
                    
                    someLanguages = [ ]
                    if not theLanguages:
                        someLanguages = someCachedTemplatesForProject.keys()
                            
            if allCachedTemplatesForLanguages:
                
                for someCachedTemplatesForLanguage in allCachedTemplatesForLanguages:
                    
                    if someCachedTemplatesForLanguage:
                        someElementUIDs = someCachedTemplatesForLanguage.keys()
                        for unElementUID in someElementUIDs:                    
                            
                            someCachedTemplatesForElement = someCachedTemplatesForLanguage.get( unElementUID, None)

                            if someCachedTemplatesForElement:
                                someViewNames = someCachedTemplatesForElement.keys()
                                for aViewName in someViewNames:
                                    
                                    someCachedTemplatesForView = someCachedTemplatesForElement.get( aViewName, None)
                                    
                                    if someCachedTemplatesForView:
                                        someRelationCursorNames = someCachedTemplatesForView.keys()
                                        for unRelationCursorName in someRelationCursorNames:
                         
                                            someCachedTemplateForRelationCursor = someCachedTemplatesForView.get( unRelationCursorName, None)
                                            if someCachedTemplateForRelationCursor:
                                                
                                                someCurrentElementUIDs = someCachedTemplateForRelationCursor.keys()
                                                for unCurrentElementUID in someCurrentElementUIDs:
                                                
                                                    someCachedTemplateForRelatedElement = someCachedTemplateForRelationCursor.get( unCurrentElementUID, None)
                                                    if someCachedTemplateForRelatedElement:
                                                        
                                                        someRoleKindsToIndex = someCachedTemplateForRelatedElement.keys()
                                                        for aRoleKindToIndex in someRoleKindsToIndex:
                                                            unaCachedEntry = someCachedTemplateForRelatedElement.get( aRoleKindToIndex, None)
                                                            if unaCachedEntry:
                                                                someCachedEntries.append( unaCachedEntry)
                                                                
                                                                
            
        finally:
            # #################
            """IF theEnforceThreadSafety MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if theEnforceThreadSafety:
                self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                

        return [ someCachedEntries, someFilePaths,]

    
    
    
    
            
    
    security.declarePrivate( '_pDestroyFailedPromise')
    def _pDestroyFailedPromise(self, theModelDDvlPloneTool, theContextualObject, theRenderPhaseResult):
        
        if not theRenderPhaseResult:
            return self
        
        aPromiseMade = theRenderPhaseResult.get( 'promise_made', None)
        if not aPromiseMade:
            return self
        
            
        someObjectsToDelete = set()
        someObjectsToDelete.add( aPromiseMade)
        
            
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        

            try:
                aPromiseHolder = theRenderPhaseResult.get( 'promise_holder', None)
                if aPromiseHolder:        
                    aPromiseKey = theRenderPhaseResult.get( 'promise_key', None)
                    if aPromiseKey:
                        aPromiseInHolder = aPromiseHolder.get( aPromiseKey, None)
                        if aPromiseInHolder == aPromiseMade:
                            aPromiseHolder.pop( aPromiseKey)        
            except:
                None
                
                
            try:
                aPromiseMade.pUnLink()      
            except:
                None
                
            
            unCachedHTML = aPromiseMade.vHTML
            if unCachedHTML:            
                someObjectsToDelete.add( unCachedHTML)
                
            try:
                self._pRemoveCacheEntriesFromUniqueIdIndex( theModelDDvlPloneTool, theContextualObject, [ aPromiseMade,])
            except:
                None                

            if aPromiseMade.fIsForElement():
                try:
                    self._pRemoveCacheEntriesFromUIDIndex( theModelDDvlPloneTool, theContextualObject, [ aPromiseMade,])
                except:
                    None       
                    
            try:
                aPromiseMade.pBeGone()      
            except:
                None                
           
                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
            
        if someObjectsToDelete:
            del someObjectsToDelete
                                            
        return self
    
    
    
     
    
    # ###################################################################
    """Rendering service for templates that are Element Independent. Searching Cache entries NOT associated with any specific element. 
    
    """
    
    
       
    security.declarePrivate( '_fRenderError')
    def _fRenderError(self, theErrorCode, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=None,):
        """ Return HTML with an error message.
        
        """
        
        anErrorCode = theErrorCode
        if not anErrorCode:
            anErrorCode = cRenderError_UnknownError
            
        anErrorMsgId = '%s%s' % ( cRenderError_MsgIdPrefix, anErrorCode,)
        
        anTranslatedError = theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', anErrorMsgId, anErrorMsgId, )
        
        anErrorHTML = cRenderError_HTML % fCGIE( anTranslatedError)        
        
        return anErrorHTML
    
    
         
    

    
    security.declarePrivate( 'fRenderTemplateOrCachedElementIndependent')
    def fRenderTemplateOrCachedElementIndependent(self, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        someRenderHandlers = self.fRenderHandlers_ElementIndependent(  theModelDDvlPloneTool, theContextualObject)
        return self.fRenderTemplateOrCached_withHandlers( someRenderHandlers, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=theAdditionalParams)
       
    
    
    
     
    security.declarePrivate( 'fRenderTemplateOrCachedForElement')
    def fRenderTemplateOrCachedForElement(self, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        someRenderHandlers = self.fRenderHandlers_ForElement(  theModelDDvlPloneTool, theContextualObject)
        return self.fRenderTemplateOrCached_withHandlers( someRenderHandlers, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=theAdditionalParams)
       
    
       
     
    security.declarePrivate( 'fRenderCallableOrCachedForElement')
    def fRenderCallableOrCachedForElement(self, theModelDDvlPloneTool, theContextualObject, theTemplateName, theCallable=None, theCallableCtxt=None, theCallableParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        someRenderHandlers = self.fRenderHandlers_ForElement(  theModelDDvlPloneTool, theContextualObject)
        
        someAdditionalParams = { }
        someAdditionalParams.update( {
            'callable':      theCallable,
            'callable_ctxt': theCallableCtxt,
            'callable_parms':theCallableParams,
        })
        
        return self.fRenderTemplateOrCached_withHandlers( someRenderHandlers, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=someAdditionalParams)
       
        
    
    security.declarePrivate( 'fRenderTemplateOrCached_withHandlers')
    def fRenderTemplateOrCached_withHandlers(self, theRenderHandlers, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        # ###################################################################
        """Can not proceed without handlers.
        
        """
        if not theRenderHandlers:
            return self._fRenderError( cRenderError_MissingHandlers, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        aMemoryHandler = theRenderHandlers.get( 'memory', None)
        aDiscHandler   = theRenderHandlers.get( 'disc',   None)
        aRenderHandler = theRenderHandlers.get( 'render', None)
        aStoreHandler  = theRenderHandlers.get( 'store',  None)
        
        if not ( aMemoryHandler and aDiscHandler and aRenderHandler and  aStoreHandler):
            return self._fRenderError( cRenderError_MissingHandlers, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
            
        
        # ###################################################################
        """If caching not active, render now.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                return self._fRenderError( cRenderError_MissingParameters, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        
            unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            
            return unRenderedTemplate
        
        someVariables = { }
        
         
        # ###################################################################
        """Try to retrieve from memory the already rendered HTML.
        
        """
        aRenderResult_Phase_TryMemory = aMemoryHandler( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams, someVariables)
        if not aRenderResult_Phase_TryMemory:
            return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        
        
        aRenderStatus_Memory = aRenderResult_Phase_TryMemory.get( 'status',    '')
        if not aRenderStatus_Memory:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_UnknownError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
 
        
        if aRenderStatus_Memory == cRenderStatus_Completed:
            aRenderedHTML_Memory       = aRenderResult_Phase_TryMemory.get( 'rendered_html',        None)
            if not aRenderedHTML_Memory:
                self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
                return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
            return   aRenderedHTML_Memory
        
       
        if aRenderStatus_Memory == cRenderStatus_ForceRender:
            aRenderedHTML = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return aRenderedHTML

        
        if aRenderStatus_Memory == cRenderStatus_ShowError:
            aRenderError = aRenderResult_Phase_TryMemory.get( 'error',    '')
            if not aRenderError:
                aRenderError = cRenderError_UnknownError
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( aRenderError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
      

        if not ( aRenderStatus_Memory == cRenderStatus_Continue):
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_Discontinued, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
            

        
        
        
        
        # ###################################################################
        """Try to retrieve from disc the already rendered HTML.
        
        """        
        
        aRenderResult_Phase_TryDisk = aDiscHandler( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams, someVariables)
        if not aRenderResult_Phase_TryDisk:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        
        
        aRenderStatus_Disc = aRenderResult_Phase_TryDisk.get( 'status',    '')
        if not aRenderStatus_Disc:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_UnknownError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
 
        
        if aRenderStatus_Disc == cRenderStatus_Completed:
            aRenderedHTML_Disc       = aRenderResult_Phase_TryDisk.get( 'rendered_html',        None)
            if not aRenderedHTML_Disc:
                self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
                return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
            return   aRenderedHTML_Disc
        
       
        if aRenderStatus_Disc == cRenderStatus_ForceRender:
            aRenderedHTML = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            return aRenderedHTML

        
        if aRenderStatus_Disc == cRenderStatus_ShowError:
            aRenderError = aRenderResult_Phase_TryDisk.get( 'error',    '')
            if not aRenderError:
                aRenderError = cRenderError_UnknownError
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( aRenderError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
      

        if not ( aRenderStatus_Disc == cRenderStatus_Continue):
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_Discontinued, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        


        
        

                   
        # ###################################################################
        """Try to render HTML.
        
        """        
        aRenderResult_Phase_Render = aRenderHandler( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams, someVariables)
        if not aRenderResult_Phase_Render:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        
        
        aRenderStatus_Render = aRenderResult_Phase_Render.get( 'status',    '')
        if not aRenderStatus_Render:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_UnknownError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
 
        
        if aRenderStatus_Render == cRenderStatus_Completed:
            aRenderedHTML_Render       = aRenderResult_Phase_Render.get( 'rendered_html',        None)
            if not aRenderedHTML_Render:
                self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
                return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)

            aResultPhase_StoreDisc = aStoreHandler( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams, someVariables)

            return   aRenderedHTML_Render
        
       
        if aRenderStatus_Render == cRenderStatus_ForceRender:
            aRenderedHTML = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            return aRenderedHTML

        
        if aRenderStatus_Render == cRenderStatus_ShowError:
            aRenderError = aRenderResult_Phase_Render.get( 'error',    '')
            if not aRenderError:
                aRenderError = cRenderError_UnknownError
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( aRenderError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
      

        return self._fRenderError( cRenderError_UnknownError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)

    
    
    
        
    
    
    
    

    
    
    security.declarePrivate( '_fNewVoidRenderResult_Phase_TryMemory')
    def _fNewVoidRenderResult_Phase_TryMemory(self, ):
        aResult = {
            'status':              cRenderStatus_NotExecuted,
            'error':               None,
            'rendered_html':       None,
            'cache_name':          None,
            'promise_made':        None,
            'promise_holder':      None,
            'promise_key':         None,
        }
        return aResult
        
        
    

     
    security.declarePrivate( '_fNewVoidRenderResult_Phase_TryDisk')
    def _fNewVoidRenderResult_Phase_TryDisk(self, ):
        aResult = {
            'status':              cRenderStatus_NotExecuted,
            'error':               None,
            'rendered_html':       None,
        }     
        
        return aResult
            
         
        

     
    security.declarePrivate( '_fNewVoidRenderResult_Phase_Render')
    def _fNewVoidRenderResult_Phase_Render(self, ):
        aResult = {
            'status':              cRenderStatus_NotExecuted,
            'error':               None,
            'rendered_html':       None,
        }     
        
        return aResult
            
         
       
    
    
    security.declarePrivate( '_fNewVoidCachedEntryInWrongStateInfo')
    def _fNewVoidCachedEntryInWrongStateInfo(self, ):
        aCachedEntryInWrongStateInfo = {
            'cached_entry':        None,
            'cached_entry_holder': None,
            'cached_entry_key':    None,            
        }
        return aCachedEntryInWrongStateInfo
   
    
         

     
    security.declarePrivate( '_pRemoveCachedEntriesInWrongState')
    def _pRemoveCachedEntriesInWrongState(self, theCachedEntriesInWrongStateInfos):
        """Invoked from within thread-safe critical section. Remove cache entries that are in wrong state, more likely because of an error while trying to fulfill the promise to be rendered.
        
        """
        if not theCachedEntriesInWrongStateInfos:
            return self
        
        unosObjectsToDelete = set()
                           
        for aCachedEntryInWrongStateInfo in theCachedEntriesInWrongStateInfos:
            
            
            if aCachedEntryInWrongStateInfo: 
                aCachedEntry         = aCachedEntryInWrongStateInfo.get( 'cached_entry', None)
                aCachedEntryHolder   = aCachedEntryInWrongStateInfo.get( 'cached_entry_holder', None)
                aCachedEntryKey      = aCachedEntryInWrongStateInfo.get( 'cached_entry_key', None)
                
                if aCachedEntry and aCachedEntryHolder and aCachedEntryKey:
                    """Remove the cache entry from all structures
                    
                    """
                    try:
                        
                        try:
                            aCachedEntryHolder.pop( aCachedEntryKey)
                        except:
                            None
                        
                        unNumEntriesFlushed = 0
                        unTotalCharsFlushed = 0
                        
                        aFilePath    = aCachedEntry.vFilePath
                        if aFilePath:
                            someFilesToDelete.append( aFilePath)
                        
                        aCachedEntry.pUnLink()
                        
                        unosObjectsToDelete.append( aCachedEntry)
        
                        unNumEntriesFlushed += 1
                        
                        if anExistingCacheEntryInWrongState.vValid:
                                
                            unCachedHTML = anExistingCacheEntryInWrongState.vHTML
                            if unCachedHTML:
                                unTotalCharsFlushed += len( unCachedHTML)
                                unosObjectsToDelete.append( unCachedHTML)
        
                        unStatisticsUpdate = {
                            cCacheStatistics_TotalEntriesFlushed: unNumEntriesFlushed,
                            cCacheStatistics_TotalCharsFlushed:   unTotalCharsFlushed,
                            cCacheStatistics_TotalCacheEntries:   0 - unNumEntriesFlushed,
                            cCacheStatistics_TotalCharsCached:    0 - unTotalCharsFlushed,
                        }
                        self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                
                            
                        self._pRemoveCacheEntriesFromUniqueIdIndex( theModelDDvlPloneTool, theContextualObject, [ anExistingCacheEntryInWrongState,])
            
                        # not for element independent self._pRemoveCacheEntriesFromUIDIndex( theModelDDvlPloneTool, theContextualObject, [anExistingCacheEntryInWrongState,])
                    
                        anExistingCacheEntryInWrongState.pBeGone()
                    except:
                        None
                                
               
        if unosObjectsToDelete:
            try:
                del unosObjectsToDelete
            except:
                None
                
        
            
        return self
    
    
    
    
    

    
    security.declarePrivate( '_fRenderTemplateOrCachedElementIndependent_Phase_TryMemory')
    def _fRenderTemplateOrCachedElementIndependent_Phase_TryMemory(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        aRenderResult = self._fNewVoidRenderResult_Phase_TryMemory()
        
        unosMillisBeforeMatch   = fMillisecondsNow()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if theModelDDvlPloneTool == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        if theContextualObject == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        if cForbidCaches or not self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent):
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        unMemberId = ModelDDvlPloneTool_Retrieval().fGetMemberId(  theContextualObject)
        
            
        if theVariables == None:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
           
        unCacheEntryUniqueId = ''
        unCachedTemplate = None
        
        aBeginMillis = fMillisecondsNow()
                
          
        # ###########################################################
        """Gather all information to look up the cache for a matching cached entry with a rendered template. Fall back to non-cached template rendering if any information can not be obtained.
        
        """
        aProjectName = ''
        try:
            aProjectName = theContextualObject.getNombreProyecto()
        except:
            None
        if not aProjectName:    
            aProjectName = cDefaultNombreProyecto
          
            
            
        unosPreferredLanguages = getLangPrefs( theContextualObject.REQUEST)
        if not unosPreferredLanguages:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        aNegotiatedLanguage = unosPreferredLanguages[ 0]   
        if not aNegotiatedLanguage:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
                
        aViewName = theTemplateName
        if not aViewName:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        if aViewName.find( '%s') >= 0:
            if not ( aProjectName == cDefaultNombreProyecto):
                aViewName = aViewName % aProjectName
            else:
                aViewName = aViewName.replace( '%s', '')
        if not aViewName:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
                
        unMemberId = ModelDDvlPloneTool_Retrieval().fGetMemberId(  theContextualObject)           
         
                    
            
        # ###################################################################
        """CRITICAL SECTION to access and modify cache control structure, for Cache entries associated with specific elements.
        
        """
        unExistingOrPromiseCacheEntry = None
        unCachedTemplate              = None
        unPromiseMade                 = None                      
        
        anActionToDo                  = None
        somePossibleActions           = [ 'UseFoundEntry', 'MakePromise', 'JustFallbackToRenderNow', ] # Just to document the options handled by logic below
        
        someFilesToDelete = [ ]
        
        someExistingCacheEntriesInWrongState = [ ]
        
        
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # ###########################################################
            """Retrieve within thread safe section, to be used later, the configuration paameters specifying: whether to render a cache hit information collapsible section at the top or bottom of the view, or none at all, whether the disk caching is enabled, and the disk cache files base path.
            
            """
            aDisplayCacheHitInformation = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_DisplayCacheHitInformation)
            aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_CacheDiskEnabled)
            aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_CacheDiskPath)
            unExpireDiskAfterSeconds    = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_ExpireDiskAfterSeconds)

            
            # ###########################################################
            """All Cache Entries that have expired and are forced to expire shall be flushed, whether memory used is over the limit, or not.
            
            """  
            self._pFlushCacheEntriesForcedtoExpire(theModelDDvlPloneTool, theContextualObject, theFilesToDelete=someFilesToDelete)       
                        

            
            
            # ###########################################################
            """Traverse cache control structures to access the cache entry corresponding to the parameters. Elements found missing shall be created, to hook up the new cache entry.
            
            """
            someCachedTemplatesForProject = self.fGetOrInitCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, aProjectName)              

    
            someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aNegotiatedLanguage, None)
            if someCachedTemplatesForLanguage == None:
                someCachedTemplatesForLanguage = { }
                someCachedTemplatesForProject[ aNegotiatedLanguage] = someCachedTemplatesForLanguage
    
                
                
            # ###########################################################
            """Obtain the Cache entry, if exists.
            
            """
            anExistingCacheEntry = someCachedTemplatesForLanguage.get( aViewName, None)
            
            
            
            
            # ###########################################################
            """Analyze the Cache entry, if retrieved, and decide how to proceed: using it, promissing to create a new one, or just fallback to render the template now and return it.
            
            """
            
            
            if not anExistingCacheEntry:
                # ###########################################################
                """If not found, it shall be created, and be hooked up into the cache control structure.
                
                """
                anActionToDo = 'MakePromise'
                
            elif not anExistingCacheEntry.vValid:
                # ###########################################################
                """If found invalid, it shall be created, and shall replace the existing one in the cache control structure.
                
                """
                aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                aCacheEntryInWrongStateInfo.update( {
                    'cached_entry':        anExistingCacheEntry,
                    'cached_entry_holder': someCachedTemplatesForLanguage,
                    'cached_entry_key':    aViewName,            
                })                    
                someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)
                anActionToDo = 'MakePromise'
                
            elif not anExistingCacheEntry.vPromise:
                # ###########################################################
                """A null promise is a sign something went wrong with its resolution. A new entry shall be created, and shall replace the existing one in the cache control structure.
                
                """
                aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                aCacheEntryInWrongStateInfo.update( {
                    'cached_entry':        anExistingCacheEntry,
                    'cached_entry_holder': someCachedTemplatesForLanguage,
                    'cached_entry_key':    aViewName,            
                })                    
                someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)
                
                anActionToDo = 'MakePromise'
                
            elif not ( anExistingCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel):
                # ###########################################################
                """If a promisse made, but promissed not fulfilled, somebody else is trying to complete the rendering. Just fallback to render it now.
                
                """
                anActionToDo = 'JustFallbackToRenderNow'
            
            else:
                # ###########################################################
                """This is a proper entry, if its cached rendered template result HTML is something.
                
                """
            
                unCachedTemplate = anExistingCacheEntry.vHTML
                
                if not unCachedTemplate: 
                    # ###########################################################
                    """A totally empty rendered template HTML is a sign something went wrong with its resolution (it shall always return a smallish string or HTML element. A new entry shall be created, and shall replace the existing one in the cache control structure.
                    
                    """
                    aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                    aCacheEntryInWrongStateInfo.update( {
                        'cached_entry':        anExistingCacheEntry,
                        'cached_entry_holder': someCachedTemplatesForLanguage,
                        'cached_entry_key':    aViewName,            
                    })                    
                    someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)

                    anActionToDo = 'MakePromise'
                    
                else:
                    # ###########################################################
                    """Found cached template: Cache Hit. Update expiration time for the cache entry. Update cache hit statistics, and decide to use the HTML cached in the found entry.
                    
                    """
                    unMillisecondsNow = fMillisecondsNow()

                    anExistingCacheEntry.vHits += 1
                    anExistingCacheEntry.vLastHit  = unMillisecondsNow                         
                    anExistingCacheEntry.vLastUser = unMemberId                         
                    
                    unExistingCacheEntryChars = 0
                    if anExistingCacheEntry.vHTML:
                        unExistingCacheEntryChars = len( anExistingCacheEntry.vHTML)
    
                    unStatisticsUpdate = {
                        cCacheStatistics_TotalCacheHits:    1,
                        cCacheStatistics_TotalCharsSaved:   unExistingCacheEntryChars,
                        cCacheStatistics_TotalTimeSaved:    max( anExistingCacheEntry.vMilliseconds, 0),
                    }
                    self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                    
                
                    
                    # ###########################################################
                    """Renew the age of the cache entry in the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                    See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                    
                    """
                    
                    unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent)
                    if unListNewSentinel:
                        anExistingCacheEntry.pUnLink()   
                        unListNewSentinel.pLink( anExistingCacheEntry) 
                    
                    
                    
                    
                    # ###########################################################
                    """Determined the cache entry found, and an indication that no promise was made (so no rendering has to be produced to fullfill it), and there is no need to just fallback and render it now
                    
                    """
                    unExistingOrPromiseCacheEntry = anExistingCacheEntry
                    anActionToDo                  = 'UseFoundEntry'

                    
                    
            # ###########################################################
            """Remove cache entries that are in wrong state, more likely because of an error while trying to fulfill the promise to be rendered.
            
            """
            if someExistingCacheEntriesInWrongState:
                self._pRemoveCachedEntriesInWrongState( someExistingCacheEntriesInWrongState)
               
                    
                    
            if not ( anActionToDo == 'UseFoundEntry'):
                # ###########################################################
                """Not Found usable cached template: Cache Fault. Update cache fault statistics.
                
                """
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheFaults:    1,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                
                
                
            if anActionToDo == 'MakePromise':
                # ###########################################################
                """Create a new cache entry as a promise to be fullfilled after the CRITICAL SECTION, and hook it up in the cache control structure.
                
                """
                
                
                
            
                # ###########################################################
                """Allocate a new unique id for the cache entry, 
                
                """
                    
                unCacheEntryUniqueId  = self.fGetCacheStoreNewUniqueId(  theModelDDvlPloneTool, theContextualObject,) 
                unMillisecondsNow     = fMillisecondsNow()
                unExpireAfterSeconds  = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_ExpireAfterSeconds)
                unForceExpire         = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_ForceExpire)

                unPromiseMade = unMillisecondsNow
                
                aNewCacheEntry = MDDRenderedTemplateCacheEntry_ElementIndependent(
                    theCacheName         =cCacheName_ElementIndependent,
                    theCacheKind         =cCacheKind_ElementIndependent,
                    theProjectName       =aProjectName,
                    theUniqueId          =unCacheEntryUniqueId,
                    theValid             =True,
                    thePromise           =unPromiseMade,
                    theUser              =unMemberId,
                    theDateMillis        =unMillisecondsNow,
                    theProject           =aProjectName,
                    theView              =aViewName,
                    theLanguage          =aNegotiatedLanguage,
                    theHTML              =None,
                    theMilliseconds      =0,
                    theExpireAfterSeconds =unExpireAfterSeconds,
                    theForceExpire       =unForceExpire,
                )
                
                unExistingOrPromiseCacheEntry = aNewCacheEntry
                
                
                
                # ###########################################################
                """Hook up the new cache entry promise in the cache control structure, to be fullfilled after the CRITICAL SECTION.
                
                """
                someCachedTemplatesForLanguage[ aViewName] = aNewCacheEntry
                
                aRenderResult.update( {
                    'cache_name':     cCacheName_ElementIndependent,
                    'promise_made':   unExistingOrPromiseCacheEntry,
                    'promise_holder': someCachedTemplatesForLanguage,
                    'promise_key':    aViewName,
                })
                
                                    
                
                # ###########################################################
                """Add unique id of cache entry to the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                
                """
                unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent)
                if unListNewSentinel:
                    unListNewSentinel.pLink( aNewCacheEntry) 
    
                

                
                # ###########################################################
                """Add the entry to the index by Cache Entry Unique Id.
                
                """
                self._pAddCacheEntryToUniqueIdIndex( theModelDDvlPloneTool, theContextualObject, aNewCacheEntry)
                

                
                # ###########################################################
                """Update cache statistics.
                
                """                    
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheEntries:    1,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                
                    
                
            
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            
        if someFilesToDelete:
            self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
            
            
            
        # ###########################################################
        """Act according to the analysis made of the Cache entry, and decide how to proceed: using it if retrieved, promissing to create a new one, or just fallback to render the template now and return it.
        
        """

        someTranslations = { }
        someDomainsStringsAndDefaults = [
            [ 'ModelDDvlPlone', [    
                [ 'ModelDDvlPlone_Cached',                           'Cached-',], 
                [ 'ModelDDvlPlone_JustRendered',                     'Just Rendered-',],
            ]],                                                      
        ]        
        theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someDomainsStringsAndDefaults, someTranslations)
                
        
        
        if anActionToDo == 'UseFoundEntry':
            # ###########################################################
            """Found entry was good: sucessful cache hit.
            
            """
            if unCachedTemplate:
                # ###########################################################
                """If no HTML (in cache entry to use, something is wrong in the logic of the entry search and analysis. The unCachedTemplate variable should hold HTML. Falling back in the code following to render now.
                
                """
                unRenderedTemplateToReturn = unCachedTemplate.replace(    
                    u'<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
                    u'<span>%(ModelDDvlPlone_Cached)s' % someTranslations,
                )   
    
                aEndMillis = fMillisecondsNow()
                aMilliseconds = aEndMillis - aBeginMillis
                unDurationString = '%d ms' % aMilliseconds
                
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                    u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                    u'%s</span>' % unDurationString
                )
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                   cMagicReplacementString_CacheCode, 
                   '%d' % aEndMillis
                )
                
                aRenderResult.update( {
                    'status':            cRenderStatus_Completed, 
                    'rendered_html':     unRenderedTemplateToReturnWithDuration,
                })                                    
                return aRenderResult
            
            
            
            
        
            
        if ( anActionToDo == 'UseFoundEntry') or ( anActionToDo == 'JustFallbackToRenderNow') or ( ( anActionToDo == 'MakePromise') and ( not unPromiseMade)) or not ( anActionToDo == 'MakePromise') or (unExistingOrPromiseCacheEntry == None):
            # ###########################################################
            """Entry was found, but something was wrong, or it has been decided that the action is to just render now, or a promise has been made but there is no promise code, or a the action is not the remaining possiblity of MakePromise , or no promise entry has been created. Fallback to render now.
            ACV OJO 20091219 Should remove the found entry: pages that fail usually leave the entry in a bad state, and are never cached again.
            
            """
            
            anActionToDo = 'JustFallbackToRenderNow'
            
            
            unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
           
            if aDisplayCacheHitInformation:
                if aDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                    unRenderedTemplateToReturn = unRenderedTemplate + ( u'\n<br/><br/><font size="1"><strong>%(ModelDDvlPlone_JustRendered)s</strong></font>' % someTranslations)
                elif aDisplayCacheHitInformation == cDisplayCacheHitInformation_Top:          
                    unRenderedTemplateToReturn = ( u'<br/><font size="1"><strong>%(ModelDDvlPlone_JustRendered)s</strong></font><br/>\n' % someTranslations) + unRenderedTemplate
                else:
                    unRenderedTemplateToReturn = unRenderedTemplate[:]
                    
            unosMillisAfterMatch   = fMillisecondsNow()
                    
            unosMilliseconds = unosMillisAfterMatch - unosMillisBeforeMatch
            unDurationString = '%d ms' % unosMilliseconds
            
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                u'%s</span>' % unDurationString
            )
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
               cMagicReplacementString_CacheCode, 
               '%d' % unosMillisAfterMatch
            )
           
            aRenderResult.update( {
                'status':            cRenderStatus_Completed, 
                'rendered_html':     unRenderedTemplateToReturnWithDuration,
            })                                    
            return aRenderResult
            
            
        theVariables.update( {
            'aBeginMillis':                  aBeginMillis,
            'anActionToDo':                  anActionToDo,
            'unExistingOrPromiseCacheEntry': unExistingOrPromiseCacheEntry,
            'unPromiseMade':                 unPromiseMade,
            'unCacheEntryUniqueId':          unCacheEntryUniqueId,
            'aProjectName':                  aProjectName,
            'aNegotiatedLanguage':           aNegotiatedLanguage,
            'unCacheId':                     unCacheEntryUniqueId,
            'aViewName':                     aViewName,
            'unMemberId':                    unMemberId,
            'unCachedTemplate':              unCachedTemplate,
            'someTranslations':              someTranslations,
            'aDisplayCacheHitInformation':   aDisplayCacheHitInformation,
            'aCacheDiskEnabled':             aCacheDiskEnabled,
            'aCacheDiskPath':                aCacheDiskPath,
            'unExpireDiskAfterSeconds':      unExpireDiskAfterSeconds,
        })
            
        aRenderResult.update( {
            'status':            cRenderStatus_Continue, 
        })                                    
        return aRenderResult

        
                
       
    
                
 
    
    security.declarePrivate( '_fRenderTemplateOrCachedElementIndependent_Phase_TryDisk')
    def _fRenderTemplateOrCachedElementIndependent_Phase_TryDisk(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """No usable cache entry has been found. Try to find the cached HTML on disc, for the project, for the currently negotiated language, and for the specified view.
        
        """
        
        aRenderResult = self._fNewVoidRenderResult_Phase_TryDisk()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if not theVariables:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        aViewName                     = theVariables[ 'aViewName']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        someTranslations              = theVariables[ 'someTranslations']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        unExpireDiskAfterSeconds      = theVariables[ 'unExpireDiskAfterSeconds']
        
        if not aCacheDiskEnabled:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        

        if not aCacheDiskPath:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        # ###########################################################
        """Assemble the name of the disk file holding the cached HTML for the entry.
            
        """            
        aProjectPath  = os.path.join( aCacheDiskPath, aProjectName)
        aLanguagePath = os.path.join( aProjectPath, aNegotiatedLanguage)
        aFileName     = '%s%s' % (  aViewName, cCacheDiskFilePostfix)
        aFilePath     = os.path.join( aLanguagePath, aFileName)

        theVariables[ 'aFilePath']         = aFilePath

        
        
        # ###########################################################
        """Try to access the directory containing the element independent files with cached HTML.
            
        """            
        aCacheDiskPathExist = False
        try:
            aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
        except:
            None
        if not aCacheDiskPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        
        # ###########################################################
        """Try to access directories for project and language.
            
        """
        aProjectPathExist = False
        try:
            aProjectPathExist = os.path.exists( aProjectPath)
        except:
            None
        if not aProjectPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
            
        
        aLanguagePathExist = False
        try:
            aLanguagePathExist = os.path.exists( aLanguagePath)
        except:
            None
        if not aLanguagePathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult

        
        # ###########################################################
        """Try to retrieve the page from disk cache file.
            
        """
        aFilePathExist = False
        try:
            aFilePathExist = os.path.exists( aFilePath)
        except:
            None
        if not aFilePathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult

        anHTML = ''
        try:
            aViewFile = None
            try:
                aViewFile = open( aFilePath, cCacheDisk_ElementIndependent_FileOpenReadMode_View, cCacheDisk_ElementIndependent_FileOpenReadBuffering_View)
                anHTML = aViewFile.read()
            finally:
                if aViewFile:
                    aViewFile.close()
                
        except IOError:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
  
        if ( not anHTML) or ( len( anHTML) < cMinCached_HTMLFileLen):
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
            
        
        
        unosMillisAfterRead = fMillisecondsNow()
        unosMilliseconds   = unosMillisAfterRead - aBeginMillis


  

        # ###########################################################
        """Read the HTML timestamp, and determine if the file has expired.
            
        """
        if unExpireDiskAfterSeconds:
            
            aFirstLinesChunk = anHTML[:cHTMLFirstLinesChunkLen]
            unIndex = aFirstLinesChunk.find( cHTMLRenderingTimeComment_Keyword)
            if unIndex < 0:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                    
            unMillisecondsHTMLString = aFirstLinesChunk[ unIndex + len( cHTMLRenderingTimeComment_Keyword):]
            if not unMillisecondsHTMLString:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unLastIndex = unMillisecondsHTMLString.index( ' ')
            if unLastIndex < 0:
                unLastIndex = unMillisecondsHTMLString.index( '-')
                
            if unLastIndex >=0:
                unMillisecondsHTMLString = unMillisecondsHTMLString[:unLastIndex]
            if not unMillisecondsHTMLString:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                
                
            unMillisecondsHTML = 0
            try:
                unMillisecondsHTML = int( unMillisecondsHTMLString)
            except:
                None
            if not unMillisecondsHTML:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unTimePassed = int( ( unosMillisAfterRead - unMillisecondsHTML) / 1000)
           
            if unTimePassed >= unExpireDiskAfterSeconds:
                # ###########################################################
                """HTML has expired. Flush the file.
                    
                """
                self._pRemoveDiskCacheFiles( theModelDDvlPloneTool, theContextualObject, [ aFilePath,])
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                
                        

        
        # ###########################################################
        """CRITICAL SECTION to register in the promised cache entry the HTML result of rendering the template. 
        
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
              
            # ###########################################################
            """Check if somebody messed with the promised cache entry, so it is not being updated here.
            
            """
            if ( unPromiseMade == unExistingOrPromiseCacheEntry.vPromise):

                unMillisecondsNow = fMillisecondsNow()
                        
                unExistingOrPromiseCacheEntry.vHTML            = anHTML
                unExistingOrPromiseCacheEntry.vFilePath        = aFilePath
                unExistingOrPromiseCacheEntry.vDateMillis      = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                unExistingOrPromiseCacheEntry.vLastHit         = unMillisecondsNow
                
                unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                
                unHTMLLen = len( unExistingOrPromiseCacheEntry.vHTML)
                
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheDiskHits:    1,
                    cCacheStatistics_TotalCharsCached:      unHTMLLen,
                    cCacheStatistics_TotalCharsSaved:       unHTMLLen,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                

                    
                         
            # ###########################################################
            """MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
            
            """
            self._pFlushCacheEntriesToReduceMemoryUsed( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent)
               
            
             
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                        
        
        theVariables[ 'unTemplateToCache'] = anHTML[:]

        # ###########################################################
        """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
        
        """
        someDomainsStringsAndDefaults = [
            [ 'ModelDDvlPlone', [    
                [ 'ModelDDvlPlone_DiskCached',                     'Disk Cached-',], 
            ]],                                                      
        ]        
        theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someDomainsStringsAndDefaults, someTranslations)
        
        unRenderedTemplateToReturn = anHTML.replace(    
            u'<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
            u'<span>%s' % someTranslations[ 'ModelDDvlPlone_DiskCached'],
        )   
        
        unDurationString = '%d ms' % unosMilliseconds
        
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
            u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
            u'%s</span>' % unDurationString
        )
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
           cMagicReplacementString_CacheCode, 
           '%d' % unosMillisAfterRead
        )

        
        theVariables[ 'unTemplateToReturn'] = unRenderedTemplateToReturnWithDuration
                    
            
        aRenderResult.update( {
            'status':            cRenderStatus_Completed, 
            'rendered_html':     unRenderedTemplateToReturnWithDuration,
        })                                    
        return aRenderResult
        
        
     
            
            
            

 
    
    security.declarePrivate( '_fRenderTemplateOrCachedElementIndependent_Phase_Render')
    def _fRenderTemplateOrCachedElementIndependent_Phase_Render(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """No usable cache entry has been found. Render the template, for the project, for the currently negotiated language, and for the specified view.
        
        """
                
        aRenderResult = self._fNewVoidRenderResult_Phase_Render()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if not theVariables:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        aViewName                     = theVariables[ 'aViewName']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        someTranslations              = theVariables[ 'someTranslations']
        aDisplayCacheHitInformation   = theVariables[ 'aDisplayCacheHitInformation']
        aFilePath                     = theVariables.get( 'aFilePath', '')
        if not aFilePath:
            # ACV OJO 20091219
            logging.getLogger( 'ModelDDvlPlone').error( 'No aFilePath var in _fRenderTemplateOrCachedElementIndependent_Phase_Render')
            
            
            
        aMillisecondsNow = theModelDDvlPloneTool.fMillisecondsNow()
        

        
        # ###########################################################
        """Retrieve localized strings for internationalized symbols (l10n4i18n).
            
        """
        moreDomainsStringsAndDefaults = [
            [ 'ModelDDvlPlone', [    
                [ 'ModelDDvlPlone_JustCached',                       'Just Cached-',],
                [ 'ModelDDvlPlone_Time_label',                       'Date-',], 
                [ 'ModelDDvlPlone_Len_label',                        'Len-',], 
                [ 'ModelDDvlPlone_User_label',                       'User-',], 
                [ 'ModelDDvlPlone_Date_label',                       'Date-',], 
                [ 'ModelDDvlPlone_Project_label',                    'Project-',], 
                [ 'ModelDDvlPlone_Language_label',                   'Language-',], 
                [ 'ModelDDvlPlone_View_label',                       'View-',],
                [ 'ModelDDvlPlone_FilePath_label',                   'File-',],
                [ 'ModelDDvlPlone_RoleKind_label',                   'Role kind-',], 
                [ 'ModelDDvlPlone_Path_label',                       'Path-',], 
                [ 'ModelDDvlPlone_UID_label',                        'UID-',], 
                [ 'ModelDDvlPlone_URL_label',                        'URL-',], 
                [ 'ModelDDvlPlone_Len_label',                        'Len-',], 
                [ 'title_label',                                     'Title-',], 
                [ 'ModelDDvlPlone_Relation_label',                   'Relation-'],
                [ 'ModelDDvlPlone_ShowNoFromCacheLink_label',        'Show generated-',], 
                [ 'ModelDDvlPlone_FlushFromCacheLink_label',         'Flush from cache-',], 
                [ 'ModelDDvlPlone_FlushFromDiskCacheLink_label',     'Flush from diskcache-',], 
                [ 'ModelDDvlPlone_RelatedElement_label',             'Related Element-',],
            ]],                                                      
        ]        
        theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, moreDomainsStringsAndDefaults, someTranslations)
        
        
        
        
        
        # ###########################################################
        """Render a caching information collapsible section to append to the rendered template HTML.
            
        """
        unRenderedCacheInfo = u''
        if aDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]:
            
            # ###########################################################
            """Prepare internationalized strings, and info values.
                
            """
            
            unPagina = ''
            if aViewName in [ 'Textual', 'Textual_NoHeaderNoFooter',]:
                unPagina = '/'
            elif aViewName in [ 'Tabular', 'Tabular_NoHeaderNoFooter',]:
                unPagina = '/Tabular/'
            elif aViewName.endswith( '_NoHeaderNoFooter'):
                unPagina = '/%s/' % aViewName[: 0 - len( '_NoHeaderNoFooter')]
            else:
                unPagina = '/%s/' % aViewName
            

            
        
        
        # ###########################################################
        """Render template, because it was not found (valid) in the cache. This may take some significant time. Status of cache may have changed since.
        
        """
        

        unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
            theModelDDvlPloneTool=theModelDDvlPloneTool, 
            theContextualObject  =theContextualObject, 
            theTemplateName      =theTemplateName, 
            theAdditionalParams =theAdditionalParams,
        )
        
        aEndMillis       = fMillisecondsNow()
        unosMilliseconds = aEndMillis - aBeginMillis
                
        unRenderedTemplateWithCacheInfo = unRenderedTemplate
        
        
    
        # ###########################################################
        """If so configured: Fill in the date in the caching information collapsible section appended to the rendered template HTML.
        
        """
        if not( aDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]):
            unRenderedTemplateWithCacheInfo = unRenderedTemplate[:]
        
        else:
            
            aCacheEntryValuesDict = someTranslations.copy()
            aCacheEntryValuesDict.update( {
                'unBaseURL':                                       theContextualObject.getRaiz().absolute_url(),
                'cMagicReplacementString_CacheCode':               cMagicReplacementString_CacheCode,
                'cMagicReplacementString_TimeToRetrieve':          cMagicReplacementString_TimeToRetrieve,
                'cMagicReplacementString_Milliseconds':            cMagicReplacementString_Milliseconds,
                'cMagicReplacementString_Len':                     cMagicReplacementString_Len,
                'cMagicReplacementString_Date':                    cMagicReplacementString_Date,
                'cMagicReplacementString_CollapsibleSectionTitle': cMagicReplacementString_CollapsibleSectionTitle,
                'cMagicReplacementString_UniqueId':                cMagicReplacementString_UniqueId,                    
                'aProjectName':                  aProjectName,
                'aNegotiatedLanguage':           aNegotiatedLanguage,
                'unCacheId':                     unCacheEntryUniqueId,
                'aViewName':                     aViewName,
                'unMemberId':                    unMemberId,
                'unPagina':                      unPagina,
                'aFilePath':                     aFilePath,
                'aMillisecondsNow':              aMillisecondsNow,
            })                   
                
            
            unRenderedCacheInfo = u"""
                <!-- ######### Start collapsible  section ######### 
                    # ##################################################################################################
                    With placeholder for the title of the section (to be later set as Just Rendered, Just Cached, Cached 
                --> 
                <dl id="cid_MDDCachedElementView" class="collapsible inline collapsedInlineCollapsible" >
                    <dt class="collapsibleHeader">
                        <span>%(cMagicReplacementString_CollapsibleSectionTitle)s %(cMagicReplacementString_TimeToRetrieve)s</span>                        
                    </dt>
                    <dd class="collapsibleContent">
                        <br/>
                        <form style="display: inline" action="%(unBaseURL)s%(unPagina)s" method="get" enctype="multipart/form-data">
                            <input type="hidden" name="theNoCache"   value="on" />
                            <input type="hidden" name="theNoCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="submit" value="%(ModelDDvlPlone_ShowNoFromCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDShowNoFromCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        &emsp;
                        <form style="display: inline"  action="%(unBaseURL)s/MDDFlushCachedTemplateByUniqueId/"
                            method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theCacheEntryUniqueId"   value="%(cMagicReplacementString_UniqueId)s" />
                            <input type="hidden" name="theFlushCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theCacheName" value="ElementIndependent" />
                            <input type="submit" value="%(ModelDDvlPlone_FlushFromCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDFlushCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        &emsp;
                        <form style="display: inline"  action="%(unBaseURL)s/MDDFlushCachedTemplateByUniqueId/"
                            method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theCacheEntryUniqueId"   value="%(cMagicReplacementString_UniqueId)s" />
                            <input type="hidden" name="theFlushCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theCacheName" value="ElementIndependent" />
                            <input type="hidden" name="theFlushDiskCache" value="on" />
                            <input type="submit" value="%(ModelDDvlPlone_FlushFromDiskCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDFlushDiskCacheCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        <br/>
                        <table class="listing" ">
                            <thead>
                                <tr>
                                    <th class="nosort"/>
                                    <th class="nosort"/>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="odd">
                                    <td align="left"><strong>Id</strong></td>
                                    <td align="right">%(cMagicReplacementString_UniqueId)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_FilePath_label)s</strong></td>
                                    <td align="left">%(aFilePath)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Time_label)s</strong></td>
                                    <td align="right">%(cMagicReplacementString_Milliseconds)s ms</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Len_label)s</strong></td>
                                    <td align="right">%(cMagicReplacementString_Len)s chars</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_User_label)s</strong></td>
                                    <td align="left">%(unMemberId)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Date_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Date)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Project_label)s</strong></td>
                                    <td align="left">%(aProjectName)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Language_label)s</strong></td>
                                    <td align="left">%(aNegotiatedLanguage)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_View_label)s</strong></td>
                                    <td align="left">%(aViewName)s</td>
                                </tr>
                            </tbody>
                        </table>
                        <br/>   
                    </dd>
                </dl>
                <!-- ######### End collapsible  section ######### --> 
            """  % aCacheEntryValuesDict
            
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_UniqueId,     str( unCacheEntryUniqueId))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Milliseconds, fStrGrp( unosMilliseconds))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Len,          fStrGrp( len( unRenderedTemplate)))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Date,         fMillisecondsToDateTime( aEndMillis).rfc822())
               
            if aDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedTemplate, unRenderedCacheInfo,)
            else:
                unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedCacheInfo, unRenderedTemplate,)
            
        
                
                
                
         # ###########################################################
        """Add a comment with the rendering time at the top of the rendered HTML, to be used when reading from disk to determine if the HTML on disk has expired or can be reused.
        
        """
        unRenderingMillisecondsHTMLComment = """<!-- %s%s -->""" % ( cHTMLRenderingTimeComment_Keyword, aEndMillis, )
        unRenderedTemplateWithCacheInfo = '%s\n%s' % ( unRenderingMillisecondsHTMLComment, unRenderedTemplateWithCacheInfo,)
        
              
        
        
        
        # ###########################################################
        """CRITICAL SECTION to register in the promised cache entry the HTML result of rendering the template. 
        
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
              
            # ###########################################################
            """Check if somebody messed with the promised cache entry, so it is not being updated here.
            
            """
            if ( unPromiseMade == unExistingOrPromiseCacheEntry.vPromise):

                unMillisecondsNow   = fMillisecondsNow()
                
                unExistingOrPromiseCacheEntry.vHTML            = unRenderedTemplateWithCacheInfo
                unExistingOrPromiseCacheEntry.vDateMillis      = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                unExistingOrPromiseCacheEntry.vLastHit         = unMillisecondsNow
                
                unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                
                unStatisticsUpdate = {
                    cCacheStatistics_TotalRenderings:    1,
                    cCacheStatistics_TotalCharsCached: len( unExistingOrPromiseCacheEntry.vHTML),
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                
                
            # ###########################################################
            """MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
            
            """
            self._pFlushCacheEntriesToReduceMemoryUsed( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent)
               
            


            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
             
        theVariables[ 'unTemplateToCache'] = unRenderedTemplateWithCacheInfo[:]
        

        # ###########################################################
        """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
        
        """
        unRenderedTemplateToReturn = unRenderedTemplateWithCacheInfo.replace(    
            '<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
            '<span>%s' % someTranslations[ 'ModelDDvlPlone_JustCached'],
        )   
        
        unDurationString = '%d ms' % unosMilliseconds

        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
            u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
            u'%s</span>' % unDurationString
        )
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
           cMagicReplacementString_CacheCode, 
           '%d' % aEndMillis
        )

        theVariables[ 'unTemplateToReturn'] = unRenderedTemplateToReturnWithDuration
        
        aRenderResult.update( {
            'status':            cRenderStatus_Completed, 
            'rendered_html':     unRenderedTemplateToReturnWithDuration,
        })                                    
        return aRenderResult
        
        

            
            

 
    
    security.declarePrivate( '_fRenderTemplateOrCachedElementIndependent_Phase_StoreDisk')
    def _fRenderTemplateOrCachedElementIndependent_Phase_StoreDisk(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """Store the rendered HTML on disc, for the project, for the currently negotiated language, and for the specified view.
        
        """
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        if not theVariables:
            return False
        
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        aViewName                     = theVariables[ 'aViewName']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        someTranslations              = theVariables[ 'someTranslations']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        unTemplateToReturn            = theVariables[ 'unTemplateToReturn']
        unTemplateToCache             = theVariables[ 'unTemplateToCache']
        
        
        if not aCacheDiskEnabled:
            return False
        
        if not unTemplateToCache:
            return False
        
        if not unExistingOrPromiseCacheEntry:
            return False
        
        
        # ###########################################################
        """Try to access the directory containing the element independent files with cached HTML.
            
        """
        if not aCacheDiskPath:
            return False

        aCacheDiskPathExist = False
        try:
            aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
        except:
            None
        if not aCacheDiskPathExist:
            try:
                os.makedirs(aCacheDiskPath)
            except:
                None
            try:
                aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
            except:
                None
            if not aCacheDiskPathExist:
                return False
        
        
        # ###########################################################
        """Access directories for project and language, creating them if the directories do not exist.
            
        """
        aProjectPath = os.path.join( aCacheDiskPath, aProjectName)
        aProjectPathExist = False
        try:
            aProjectPathExist = os.path.exists( aProjectPath)
        except:
            None
        if not aProjectPathExist:
            try:
                os.mkdir( aProjectPath, cCacheDisk_ElementIndependent_FolderCreateMode_Project)
            except:
                None
            try:
                aProjectPathExist = os.path.exists( aProjectPath)
            except:
                None
            if not aProjectPathExist:
                return False
        
        aLanguagePath = os.path.join( aProjectPath, aNegotiatedLanguage)
        aLanguagePathExist = False
        try:
            aLanguagePathExist = os.path.exists( aLanguagePath)
        except:
            None
        if not aLanguagePathExist:
            try:
                os.mkdir( aLanguagePath, cCacheDisk_ElementIndependent_FolderCreateMode_Language)
            except:
                None
            try:
                aLanguagePathExist = os.path.exists( aLanguagePath)
            except:
                None
            if not aLanguagePathExist:
                return False
        
            
            
        # ###########################################################
        """Write the page on disk cache file.
            
        """
        aViewFileName  = '%s%s' % (  aViewName, cCacheDiskFilePostfix)
        aViewPath      = os.path.join( aLanguagePath, aViewFileName)

        aWritten = False
        try:
            aViewFile  = None
            try:
                aViewFile = open( aViewPath, cCacheDisk_ElementIndependent_FileOpenWriteMode_View, cCacheDisk_ElementIndependent_FileOpenWriteBuffering_View)
                aViewFile.write( unTemplateToCache)
            finally:
                if aViewFile:
                    aViewFile.close()
            aWritten = True
        except IOError:
            return False
  
        if not aWritten:
            return False
        
        unExistingOrPromiseCacheEntry.vFilePath = aViewPath
        
        

        # ###########################################################
        """Update statistics of written file and chars.
            
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            unExistingOrPromiseCacheEntry.vFilePath        = aViewPath
                
            unStatisticsUpdate = {
                cCacheStatistics_TotalFilesWritten:   1,
                cCacheStatistics_TotalCharsWritten:   len( unTemplateToCache),
            }
            self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)

        
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return True

                        
            
            
            
            
            
       
    security.declarePrivate( 'fRenderHandlers_ElementIndependent')
    def fRenderHandlers_ElementIndependent(self, theModelDDvlPloneTool, theContextualObject,):
        """methods to handle the rendering phases for element independent cache entries.
        """
        someHandlers = {
            'memory':  self._fRenderTemplateOrCachedElementIndependent_Phase_TryMemory,
            'disc':    self._fRenderTemplateOrCachedElementIndependent_Phase_TryDisk,
            'render':  self._fRenderTemplateOrCachedElementIndependent_Phase_Render,
            'store':   self._fRenderTemplateOrCachedElementIndependent_Phase_StoreDisk,
        }
        return someHandlers
    
        
            
            
            
            
            
            
            
            
            
            
    
    # ###################################################################
    """Cache entries associated with specific elements.
    
    """

        
    

        
         

       
    security.declarePrivate( '_fRenderTemplateOrCachedForElement_Phase_TryMemory')
    def _fRenderTemplateOrCachedForElement_Phase_TryMemory(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None,
        theVariables={}):
        """ Return theHTML, from cache or just rendered, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
                
        aRenderResult = self._fNewVoidRenderResult_Phase_TryMemory()

        unosMillisBeforeMatch   = fMillisecondsNow()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if theModelDDvlPloneTool == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        if theContextualObject == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        
        # ###########################################################
        """Determine if the user specific cache should be used. Determine the role kind to use to index the cache entry.
        
        """
        aCacheName       = cCacheName_ForElements
        aCacheKind       = cCacheKind_ForElements
        
        aRoleKindToIndex = cRoleKind_Anonymous
        
        aRoleKind, unMemberId, aRoleName = self.fGetMemberRoleKindAndUserId( theContextualObject, theTemplateName)
        aRoleKindToIndex = aRoleKind

        if ( aRoleKind == cRoleKind_UserSpecific):
            if self.fIsPrivateCacheViewForQualifiedUsers( theContextualObject, theTemplateName): 
                aRoleKindToIndex = unMemberId
                aCacheName       = cCacheName_ForUsers
                aCacheKind       = cCacheKind_ForUsers
            else:
                aRoleKindToIndex = aRoleName
                aCacheName       = cCacheName_ForElements
                aCacheKind       = cCacheName_ForElements
                
        
        if not aRoleKindToIndex:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
            
        
        if cForbidCaches or not self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, aCacheName):
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
           
        if theVariables == None:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
           
        
        unCacheEntryUniqueId = ''
        unCachedTemplate = None
              
        aBeginMillis = fMillisecondsNow()
                
        # ###########################################################
        """Only cache objects that allow caching.
        
        """
        anIsCacheable = False
        try:
            anIsCacheable = theContextualObject.fIsCacheable()
        except:
            None
        if not anIsCacheable:    
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        
        
        # ###########################################################
        """Gather all information to look up the cache for a matching cached entry with a rendered template. Fall back to non-cached template rendering if any information can not be obtained.
        
        """
        aProjectName = ''
        try:
            aProjectName = theContextualObject.getNombreProyecto()
        except:
            None
        if not aProjectName:    
            aProjectName = cDefaultNombreProyecto
          
            
            
        unosPreferredLanguages = getLangPrefs( theContextualObject.REQUEST)
        if not unosPreferredLanguages:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        aNegotiatedLanguage = unosPreferredLanguages[ 0]   
        if not aNegotiatedLanguage:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        
        unElementId = theContextualObject.getId()
         
        unElementUID = ''
        try:
            unElementUID = theContextualObject.UID()
        except:
            None
        if not unElementUID:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
               
        unElementTitle = theContextualObject.Title()
        if not unElementTitle:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult

        unElementURL   = theContextualObject.absolute_url()
        if not unElementURL:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
           
        unElementPath = '/'.join( theContextualObject.getPhysicalPath())
        if not unElementPath:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult

        
        unElementMetaType = ''
        try:
            unElementMetaType =theContextualObject.meta_type
        except:
            None

        unElementArchetypeName = ''
        try:
            unElementArchetypeName =theContextualObject.archetype_name
        except:
            None
            
        unElementPortalType = ''
        try:
            unElementPortalType =theContextualObject.portal_type
        except:
            None
 
        unRootElementUID = ''
        unRootElementPath = ''
        
        unRootElement = None
        try:
            unRootElement = theContextualObject.getRaiz()
        except:
            None
        if ( unRootElement == None):
            unRootElementUID  = unElementUID
            unRootElementPath = unElementPath
        else:
            unRootElementPath = '/'.join( unRootElement.getPhysicalPath())
            try:
                unRootElementUID     = unRootElement.UID()
            except:
                None
            if not unRootElementUID:
                unRootElementUID = unElementUID
                unRootElementPath = unElementPath
                
            
            
            
        
                
        aViewName = theTemplateName
        if not aViewName:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        if aViewName.find( '%s') >= 0:
            if not ( aProjectName == cDefaultNombreProyecto):
                aViewName = aViewName % aProjectName
            else:
                aViewName = aViewName.replace( '%s', '')
        if not aViewName:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        

        
        unRelationCursorName = ''
        unCurrentElementUID  = ''
        
        unaRequest = theContextualObject.REQUEST
        if unaRequest:
            unRelationCursorName = unaRequest.get( 'theRelationCursorName', '')
            unCurrentElementUID = unaRequest.get( 'theCurrentElementUID', '')
                
        if not unRelationCursorName:
            unRelationCursorName = cNoRelationCursorName
        if not unCurrentElementUID:
            unCurrentElementUID = cNoCurrentElementUID
            
                    
                    
                    
            
        # ###################################################################
        """CRITICAL SECTION to access and modify cache control structure, for Cache entries associated with specific elements.
        
        """
        unExistingOrPromiseCacheEntry = None
        unCachedTemplate              = None
        unPromiseMade                 = None                      
        
        anActionToDo                  = None
        somePossibleActions           = [ 'UseFoundEntry', 'MakePromise', 'JustFallbackToRenderNow', ] # Just to document the options handled by logic below
        
        someFilesToDelete = [ ]
        
        someExistingCacheEntriesInWrongState = [ ]
        
        
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            # ###########################################################
            """Retrieve within thread safe section, to be used later, the configuration paameters specifying: whether to render a cache hit information collapsible section at the top or bottom of the view, or none at all, whether the disk caching is enabled, and the disk cache files base path.
            
            """
            aDisplayCacheHitInformation = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_DisplayCacheHitInformation)
            aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskEnabled)
            aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskPath)
            unExpireDiskAfterSeconds    = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_ExpireDiskAfterSeconds)
            

            # ###########################################################
            """All Cache Entries that have expired and are forced to expire shall be flushed, whether memory used is over the limit, or not.
            
            """  
            self._pFlushCacheEntriesForcedtoExpire(theModelDDvlPloneTool, theContextualObject, theFilesToDelete=someFilesToDelete)       
      
                    
                        
             
            # ###########################################################
            """Traverse cache control structures to access the cache entry corresponding to the parameters. Elements found missing shall be created, to hook up the new cache entry.
            
            """
            someCachedTemplatesForProject = self.fGetOrInitCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)                              
    
            someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aNegotiatedLanguage, None)
            if someCachedTemplatesForLanguage == None:
                someCachedTemplatesForLanguage = { }
                someCachedTemplatesForProject[ aNegotiatedLanguage] = someCachedTemplatesForLanguage
    
            someCachedTemplatesForElement = someCachedTemplatesForLanguage.get( unElementUID, None)
            if someCachedTemplatesForElement == None:
                someCachedTemplatesForElement = { }
                someCachedTemplatesForLanguage[ unElementUID] = someCachedTemplatesForElement
                    
            someCachedTemplatesForView = someCachedTemplatesForElement.get( aViewName, None)
            if someCachedTemplatesForView == None:
                someCachedTemplatesForView = { }
                someCachedTemplatesForElement[ aViewName] = someCachedTemplatesForView
    
            someCachedTemplateForRelationCursor = someCachedTemplatesForView.get( unRelationCursorName, None)
            if someCachedTemplateForRelationCursor  == None:
                someCachedTemplateForRelationCursor = { }
                someCachedTemplatesForView[ unRelationCursorName] = someCachedTemplateForRelationCursor
                
            someCachedTemplateForRelatedElement = someCachedTemplateForRelationCursor.get( unCurrentElementUID, None)
            if someCachedTemplateForRelatedElement == None:
                someCachedTemplateForRelatedElement = { }
                someCachedTemplateForRelationCursor[ unCurrentElementUID] = someCachedTemplateForRelatedElement
    
                
                
                
            # ###########################################################
            """Obtain the Cache entry, if exists.
            
            """
            anExistingCacheEntry = someCachedTemplateForRelatedElement.get( aRoleKindToIndex, None)
            
            anExistingCacheEntryInWrongState = None
            
            
            # ###########################################################
            """Analyze the Cache entry, if retrieved, and decide how to proceed: using it, promissing to create a new one, or just fallback to render the template now and return it.
            
            """
            
            if not anExistingCacheEntry:
                # ###########################################################
                """If not found, it shall be created, and be hooked up into the cache control structure.
                
                """
                anActionToDo = 'MakePromise'
                
            elif not anExistingCacheEntry.vValid:
                # ###########################################################
                """If found invalid, it shall be created, and shall replace the existing one in the cache control structure.
                
                """
                aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                aCacheEntryInWrongStateInfo.update( {
                    'cached_entry':        anExistingCacheEntry,
                    'cached_entry_holder': someCachedTemplateForRelatedElement,
                    'cached_entry_key':    aRoleKindToIndex,            
                })                    
                someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)
                
                anActionToDo = 'MakePromise'
                
            elif not anExistingCacheEntry.vPromise:
                # ###########################################################
                """A null promise is a sign something went wrong with its resolution. A new entry shall be created, and shall replace the existing one in the cache control structure.
                
                """
                aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                aCacheEntryInWrongStateInfo.update( {
                    'cached_entry':        anExistingCacheEntry,
                    'cached_entry_holder': someCachedTemplateForRelatedElement,
                    'cached_entry_key':    aRoleKindToIndex,            
                })                    
                someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)

                anActionToDo = 'MakePromise'
                
            elif not ( anExistingCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel):
                # ###########################################################
                """If a promisse made, but promissed not fulfilled, somebody else is trying to complete the rendering. Just fallback to render it now.
                
                """
                anActionToDo = 'JustFallbackToRenderNow'
            
            else:
                # ###########################################################
                """This is a proper entry, if its cached rendered template result HTML is something.
                
                """
            
                unCachedTemplate = anExistingCacheEntry.vHTML
                
                if not unCachedTemplate: 
                    # ###########################################################
                    """A totally empty rendered template HTML means it is no longer useful (it shall always contain at least a smallish string or HTML element). A new entry shall be created, and shall replace the existing one in the cache control structure.
                    
                    """
                    aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                    aCacheEntryInWrongStateInfo.update( {
                        'cached_entry':        anExistingCacheEntry,
                        'cached_entry_holder': someCachedTemplateForRelatedElement,
                        'cached_entry_key':    aRoleKindToIndex,            
                    })                    
                    someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)
                    
                    anActionToDo = 'MakePromise'
                    
                else:
                    # ###########################################################
                    """Found cached template: Cache Hit. Update expiration time for the cache entry. Update cache hit statistics, and return the cached HTML
                    
                    """
                    unMillisecondsNow = fMillisecondsNow()

                    anExistingCacheEntry.vHits += 1
                    anExistingCacheEntry.vLastHit = unMillisecondsNow 
                    anExistingCacheEntry.vLastUser = unMemberId                         

                     
                    unExistingCacheEntryChars = 0
                    if anExistingCacheEntry.vHTML:
                        unExistingCacheEntryChars = len( anExistingCacheEntry.vHTML)
    
                    unStatisticsUpdate = {
                        cCacheStatistics_TotalCacheHits:    1,
                        cCacheStatistics_TotalCharsSaved:   unExistingCacheEntryChars,
                        cCacheStatistics_TotalTimeSaved:    max( anExistingCacheEntry.vMilliseconds, 0),
                    }
                    self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                    
                
                    
                    # ###########################################################
                    """Renew the age of the cache entry in the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                    See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                    
                    """
                    
                    unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, aCacheName)
                    if unListNewSentinel:
                        anExistingCacheEntry.pUnLink()   # if for some bad reason there is no list new sentinel, do not remove from the list, or it will never be flushed at any age.
                        unListNewSentinel.pLink( anExistingCacheEntry) 
                    
                    
                    
                    
                    # ###########################################################
                    """Returning the cache entry found, and an indication that no promise was made (so no rendering has to be produced to fullfill it), and there is no need to just fallback and render it now
                    
                    """
                    unExistingOrPromiseCacheEntry = anExistingCacheEntry
                    anActionToDo                  = 'UseFoundEntry'

                    
                  
                    
                    
                    
                    
            # ###########################################################
            """Remove cache entries that are in wrong state, more likely because of an error while trying to fulfill the promise to be rendered.
            
            """
            if someExistingCacheEntriesInWrongState:
                self._pRemoveCachedEntriesInWrongState( someExistingCacheEntriesInWrongState)
               
                    
                   
                    
                    
                    
            if not ( anActionToDo == 'UseFoundEntry'):
                # ###########################################################
                """Not Found usable cached template: Cache Fault. Update cache fault statistics.
                
                """
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheFaults:    1,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                
                
                
            if anActionToDo == 'MakePromise':
                # ###########################################################
                """Create a new cache entry as a promise to be fullfilled after the CRITICAL SECTION, and hook it up in the cache control structure.
                
                """

                
           
            
                # ###########################################################
                """Allocate a new unique id for the cache entry, 
                
                """
                    
                unCacheEntryUniqueId = self.fGetCacheStoreNewUniqueId( theModelDDvlPloneTool, theContextualObject,) 
                unMillisecondsNow = fMillisecondsNow()
                unExpireAfterSeconds      = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_ExpireAfterSeconds)
                unForceExpire             = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_ForceExpire)

                unPromiseMade = unMillisecondsNow
                
                aNewCacheEntry = MDDRenderedTemplateCacheEntry_ForElement(
                    theCacheName         =aCacheName,
                    theCacheKind         =aCacheKind,
                    theProjectName       =aProjectName,
                    theUniqueId          =unCacheEntryUniqueId,
                    theValid             =True,
                    thePromise           =unPromiseMade,
                    theUser              =unMemberId,
                    theDateMillis        =unMillisecondsNow,
                    theProject           =aProjectName,
                    theView              =aViewName,
                    theLanguage          =aNegotiatedLanguage,
                    theHTML              =None,
                    theMilliseconds      =0,
                    theExpireAfterSeconds =unExpireAfterSeconds,
                    theForceExpire       =unForceExpire,
                    theMetaType          =unElementMetaType,
                    thePortalType        =unElementPortalType,
                    theArchetypeName     =unElementArchetypeName,
                    theElementId         =unElementId,
                    theUID               =unElementUID,
                    theTitle             =unElementTitle,
                    theURL               =unElementURL,
                    theRootPath          =unRootElementPath,
                    theRootUID           =unRootElementUID,
                    thePath              =unElementPath,
                    theRoleKind          =aRoleKindToIndex,
                    theRelation          =unRelationCursorName,
                    theCurrentUID        =unCurrentElementUID,
                )
                
                unExistingOrPromiseCacheEntry = aNewCacheEntry
                                    
                
                
                # ###########################################################
                """Hook up the new cache entry promise in the cache control structure. The promised cache entry shall be fullfilled after the CRITICAL SECTION, by reading the page HTML from disk cache, or rendering the page.
                
                """
                someCachedTemplateForRelatedElement[ aRoleKindToIndex] = aNewCacheEntry

                
                aRenderResult.update( {
                    'cache_name':     aCacheName,
                    'promise_made':   unExistingOrPromiseCacheEntry,
                    'promise_holder': someCachedTemplatesForLanguage,
                    'promise_key':    aViewName,
                })
            
                
                 
                # ###########################################################
                """Add unique id of cache entry to the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                
                """
                unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, aCacheName)
                if unListNewSentinel:
                    unListNewSentinel.pLink( aNewCacheEntry) 
    
                
               
                
                # ###########################################################
                """Add the entry to the index by Cache Entry Unique Id.
                
                """
                self._pAddCacheEntryToUniqueIdIndex( theModelDDvlPloneTool, theContextualObject, aNewCacheEntry)
                

                
                # ###########################################################
                """Add the entry to the index by UID.
                
                """
                self._pAddCacheEntryToUIDIndex( theModelDDvlPloneTool, theContextualObject, aNewCacheEntry)
                
                

                
                # ###########################################################
                """Update cache statistics.
                
                """                    
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheEntries:    1,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                
                
                
                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            
        if someFilesToDelete:
            self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
            
            
            
            
        # ###########################################################
        """Act according to the analysis made of the Cache entry, and decide how to proceed: using it if retrieved, promissing to create a new one, or just fallback to render the template now and return it.
        
        """
        
        

        someTranslations = { }
        someDomainsStringsAndDefaults = [
            [ 'ModelDDvlPlone', [    
                [ 'ModelDDvlPlone_Cached',                           'Cached-',], 
                [ 'ModelDDvlPlone_JustRendered',                     'Just Rendered-',],
            ]],                                                      
        ]        
        theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someDomainsStringsAndDefaults, someTranslations)
        
        if anActionToDo == 'UseFoundEntry':
            # ###########################################################
            """Found entry was good: sucessful cache hit.
            
            """
            if unCachedTemplate:
                # ###########################################################
                """The unCachedTemplate variable should hold HTML. 
                
                """
                unRenderedTemplateToReturn = unCachedTemplate.replace(    
                    u'<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
                    u'<span>%(ModelDDvlPlone_Cached)s' % someTranslations,
                )   
    
                aEndMillis = fMillisecondsNow()
                aMilliseconds = aEndMillis - aBeginMillis
                unDurationString = '%d ms' % aMilliseconds
                
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                    u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                    u'%s</span>' % unDurationString
                )
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                   cMagicReplacementString_CacheCode, 
                   '%d' % aEndMillis
                )

                aRenderResult.update( {
                    'status':            cRenderStatus_Completed, 
                    'rendered_html':     unRenderedTemplateToReturnWithDuration,
                })                                    
                return aRenderResult
            
            
        if ( anActionToDo == 'UseFoundEntry') or ( anActionToDo == 'JustFallbackToRenderNow') or ( ( anActionToDo == 'MakePromise') and ( not unPromiseMade)) or not ( anActionToDo == 'MakePromise') or (unExistingOrPromiseCacheEntry == None):
            # ###########################################################
            """Entry was found, but something was wrong, or it has been decided that the action is to just render now, or a promise has been made but there is no promise code, or a the action is not the remaining possiblity of MakePromise , or no promise entry has been created. Fallback to render now.
            
            """
            unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            
            if aDisplayCacheHitInformation:
                if aDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                    unRenderedTemplateToReturn = unRenderedTemplate + ( u'\n<br/><br/><font size="1"><strong>%(ModelDDvlPlone_JustRendered)s</strong></font>' % someTranslations)
                elif aDisplayCacheHitInformation == cDisplayCacheHitInformation_Top:          
                    unRenderedTemplateToReturn = ( u'<br/><font size="1"><strong>%(ModelDDvlPlone_JustRendered)s</strong></font><br/>\n' % someTranslations) + unRenderedTemplate
                else:
                    unRenderedTemplateToReturn = unRenderedTemplate[:]
                    
            aEndMillis = fMillisecondsNow()
            unDurationString = '%d ms' % ( aEndMillis - aBeginMillis)
            
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                u'%s</span>' % unDurationString
            )
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
               cMagicReplacementString_CacheCode, 
               '%d' % aEndMillis
            )
            
            aRenderResult.update( {
                'status':            cRenderStatus_Completed, 
                'rendered_html':     unRenderedTemplateToReturnWithDuration,
            })                                    
            return aRenderResult
            
            
            
        theVariables.update( {
            'aCacheName':                    aCacheName,
            'aCacheKind':                    aCacheKind,
            'aBeginMillis':                  aBeginMillis,
            'anActionToDo':                  anActionToDo,
            'unExistingOrPromiseCacheEntry': unExistingOrPromiseCacheEntry,
            'unPromiseMade':                 unPromiseMade,
            'unCacheEntryUniqueId':          unCacheEntryUniqueId,
            'unRelationCursorName':          unRelationCursorName,
            'unCurrentElementUID':           unCurrentElementUID,
            'aProjectName':                  aProjectName,
            'aNegotiatedLanguage':           aNegotiatedLanguage,
            'unCacheId':                     unCacheEntryUniqueId,
            'unElementURL':                  unElementURL,
            'unElementUID':                  unElementUID,
            'unRootElementPath':             unRootElementPath,
            'unRootElementUID':              unRootElementUID,
            'unElementPath':                 unElementPath,
            'aViewName':                     aViewName,
            'aRoleKindToIndex':              aRoleKindToIndex,
            'unMemberId':                    unMemberId,
            'unCachedTemplate':              unCachedTemplate,
            'someTranslations':              someTranslations,
            'aDisplayCacheHitInformation':   aDisplayCacheHitInformation,
            'aCacheDiskEnabled':             aCacheDiskEnabled,
            'aCacheDiskPath':                aCacheDiskPath,
            'unExpireDiskAfterSeconds':      unExpireDiskAfterSeconds,
            'unElementId':                   unElementId,
            'unElementMetaType':             unElementMetaType,
            'unElementPortalType':           unElementPortalType,
            'unElementArchetypeName':        unElementArchetypeName,
        })
        
        aRenderResult.update( {
            'status':            cRenderStatus_Continue, 
        })                                    
        return aRenderResult
        

    
    
    
    
    
    

 
    
    security.declarePrivate( '_fRenderTemplateOrCachedForElement_Phase_TryDisk')
    def _fRenderTemplateOrCachedForElement_Phase_TryDisk(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """No usable cache entry has been found. Try to find the cached HTML on disc, for the project, the root UID, for the currently negotiated language, modulus of element UID, element uid, view, relation , current related UID, and role/user id.
        
        """
        
        aRenderResult = self._fNewVoidRenderResult_Phase_TryDisk()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if not theVariables:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
                
        
        aCacheName                    = theVariables[ 'aCacheName']
        aCacheKind                    = theVariables[ 'aCacheKind']
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unRelationCursorName          = theVariables[ 'unRelationCursorName'] 
        unCurrentElementUID           = theVariables[ 'unCurrentElementUID'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        unElementURL                  = theVariables[ 'unElementURL']
        unElementUID                  = theVariables[ 'unElementUID']
        unRootElementPath             = theVariables[ 'unRootElementPath']
        unRootElementUID              = theVariables[ 'unRootElementUID']
        unElementPath                 = theVariables[ 'unElementPath']
        aViewName                     = theVariables[ 'aViewName']
        aRoleKindToIndex              = theVariables[ 'aRoleKindToIndex']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        someTranslations              = theVariables[ 'someTranslations']
        aDisplayCacheHitInformation   = theVariables[ 'aDisplayCacheHitInformation']
        unExpireDiskAfterSeconds      = theVariables[ 'unExpireDiskAfterSeconds']
                 
        if not aCacheDiskEnabled:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        

        
        if not aCacheDiskPath:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult

        # ###########################################################
        """Assemble the name of the disk file holding the cached HTML for the entry.
            
        """            
        aProjectPath           = os.path.join( aCacheDiskPath, aProjectName)
        aRootUIDPath           = os.path.join( aProjectPath, unRootElementUID)
        anElementUIDModulus    = self.fModulusUID( unElementUID, cCacheDisk_UIDModulus)
        aElementUIDModulusPath = os.path.join( aRootUIDPath, anElementUIDModulus)
        aElementUIDPath        = os.path.join( aElementUIDModulusPath, unElementUID)
        aLanguagePath          = os.path.join( aElementUIDPath, aNegotiatedLanguage)
        aFileName              = '%s-%s-%s-%s%s' % ( aViewName, unRelationCursorName, unCurrentElementUID, aRoleKindToIndex, cCacheDiskFilePostfix)
        aFilePath              = os.path.join( aLanguagePath, aFileName)
        
        theVariables[ 'aFilePath']         = aFilePath
        theVariables[ 'aDirectory']        = aElementUIDPath
        
        
        
        # ###########################################################
        """Try to access the directory containing the element independent files with cached HTML.
            
        """            
        aCacheDiskPathExist = False
        try:
            aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
        except:
            None
        if not aCacheDiskPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        
        # ###########################################################
        """Try to access directories for project, root UID, language, the modulus 100 of the checksum of element UID , element UID, view,  relation, relation current UID, and role/userId.
            
        """
        
        
        aProjectPathExist = False
        try:
            aProjectPathExist = os.path.exists( aProjectPath)
        except:
            None
        if not aProjectPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                    
        
        aRootUIDPathExist = False
        try:
            aRootUIDPathExist = os.path.exists( aRootUIDPath)
        except:
            None
        if not aRootUIDPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        
        aElementUIDModulusPathExist = False
        try:
            aElementUIDModulusPathExist = os.path.exists( aElementUIDModulusPath)
        except:
            None
        if not aElementUIDModulusPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                
        
        
        aElementUIDPathExist = False
        try:
            aElementUIDPathExist = os.path.exists( aElementUIDPath)
        except:
            None
        if not aElementUIDPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                

        aLanguagePathExist = False
        try:
            aLanguagePathExist = os.path.exists( aLanguagePath)
        except:
            None
        if not aLanguagePathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                            
        
        # ###########################################################
        """Try to retrieve the page from disk cache file.
            
        """
        aFilePathExist = False
        try:
            aFilePathExist = os.path.exists( aFilePath)
        except:
            None
        if not aFilePathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        
        anHTML = ''
        try:
            aViewFile = None
            try:
                aViewFile = open( aFilePath, cCacheDisk_ForElements_FileOpenReadMode_View, cCacheDisk_ForElements_FileOpenReadBuffering_View)
                anHTML = aViewFile.read()
            finally:
                if aViewFile:
                    aViewFile.close()
                
        except IOError:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
          
        if ( not anHTML) or ( len( anHTML) < cMinCached_HTMLFileLen):
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                    
        
       
        
        unosMillisAfterRead = fMillisecondsNow()
        unosMilliseconds    = unosMillisAfterRead - aBeginMillis

        
        
        # ###########################################################
        """Read the HTML timestamp, and determine if the file has expired.
            
        """
        if unExpireDiskAfterSeconds:
            
            aFirstLinesChunk = anHTML[:cHTMLFirstLinesChunkLen]
            unIndex = aFirstLinesChunk.find( cHTMLRenderingTimeComment_Keyword)
            if unIndex < 0:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unMillisecondsHTMLString = aFirstLinesChunk[ unIndex + len( cHTMLRenderingTimeComment_Keyword):]
            if not unMillisecondsHTMLString:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unLastIndex = unMillisecondsHTMLString.index( ' ')
            if unLastIndex < 0:
                unLastIndex = unMillisecondsHTMLString.index( '-')
                
            if unLastIndex >=0:
                unMillisecondsHTMLString = unMillisecondsHTMLString[:unLastIndex]
            if not unMillisecondsHTMLString:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                
                
            unMillisecondsHTML = 0
            try:
                unMillisecondsHTML = int( unMillisecondsHTMLString)
            except:
                None
            if not unMillisecondsHTML:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unTimePassed = int( ( unosMillisAfterRead - unMillisecondsHTML) / 1000)
            
            if unTimePassed >= unExpireDiskAfterSeconds:
                # ###########################################################
                """HTML has expired. Flush the file.
                    
                """
                self._pRemoveDiskCacheFiles( theModelDDvlPloneTool, theContextualObject, [ aFilePath,])
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                
            
        
        
        
        
        
        

        
        # ###########################################################
        """CRITICAL SECTION to register in the promised cache entry the HTML result of rendering the template. 
        
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
              
            # ###########################################################
            """Check if somebody messed with the promised cache entry, so it is not being updated here.
            
            """
            if ( unPromiseMade == unExistingOrPromiseCacheEntry.vPromise):

                unMillisecondsNow = fMillisecondsNow()
                        
                unExistingOrPromiseCacheEntry.vHTML            = anHTML
                unExistingOrPromiseCacheEntry.vFilePath        = aFilePath
                unExistingOrPromiseCacheEntry.vDateMillis      = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                unExistingOrPromiseCacheEntry.vLastHit         = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vDirectory       = aElementUIDPath

                
                unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                
                unHTMLLen = len( unExistingOrPromiseCacheEntry.vHTML)
                
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheDiskHits:    1,
                    cCacheStatistics_TotalCharsCached:      unHTMLLen,
                    cCacheStatistics_TotalCharsSaved:       unHTMLLen,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                
                
            # ###########################################################
            """MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
            
            """
            self._pFlushCacheEntriesToReduceMemoryUsed( theModelDDvlPloneTool, theContextualObject, aCacheName)
               
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                        
        theVariables[ 'unTemplateToCache'] = anHTML[:]

        # ###########################################################
        """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
        
        """
        someDomainsStringsAndDefaults = [
            [ 'ModelDDvlPlone', [    
                [ 'ModelDDvlPlone_DiskCached',                     'Disk Cached-',], 
            ]],                                                      
        ]        
        theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someDomainsStringsAndDefaults, someTranslations)
        
        unRenderedTemplateToReturn = anHTML.replace(    
            u'<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
            u'<span>%s' % someTranslations[ 'ModelDDvlPlone_DiskCached'],
        )   
        
        unDurationString = '%d ms' % unosMilliseconds
        
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
            u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
            u'%s</span>' % unDurationString
        )
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
           cMagicReplacementString_CacheCode, 
           '%d' % unosMillisAfterRead
        )

        
        theVariables[ 'unTemplateToReturn'] = unRenderedTemplateToReturnWithDuration
                    
        aRenderResult.update( {
            'status':            cRenderStatus_Completed, 
            'rendered_html':     unRenderedTemplateToReturnWithDuration,
        })                                    
        return aRenderResult
        
        
        
            
            
            
    
    
    
    
    
    
    
       

       
    security.declarePrivate( '_fRenderTemplateOrCachedForElement_Phase_Render')
    def _fRenderTemplateOrCachedForElement_Phase_Render(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """No usable cache entry has been found. Render the template, for the project, for the element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
             
        aRenderResult = self._fNewVoidRenderResult_Phase_Render()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if not theVariables:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        
        aCacheName                    = theVariables[ 'aCacheName']
        aCacheKind                    = theVariables[ 'aCacheKind']
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unRelationCursorName          = theVariables[ 'unRelationCursorName'] 
        unCurrentElementUID           = theVariables[ 'unCurrentElementUID'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        unElementURL                  = theVariables[ 'unElementURL']
        unElementUID                  = theVariables[ 'unElementUID']
        unRootElementPath             = theVariables[ 'unRootElementPath']
        unRootElementUID              = theVariables[ 'unRootElementUID']
        unElementPath                 = theVariables[ 'unElementPath']
        aViewName                     = theVariables[ 'aViewName']
        aRoleKindToIndex              = theVariables[ 'aRoleKindToIndex']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        someTranslations              = theVariables[ 'someTranslations']
        aDisplayCacheHitInformation   = theVariables[ 'aDisplayCacheHitInformation']
        aFilePath                     = theVariables[ 'aFilePath']
        unElementId                   = theVariables[ 'unElementId']
        unElementMetaType             = theVariables[ 'unElementMetaType']
        unElementPortalType           = theVariables[ 'unElementPortalType']
        unElementArchetypeName        = theVariables[ 'unElementArchetypeName']
        


                
        someTranslations = { }
        someDomainsStringsAndDefaults = [
            [ 'ModelDDvlPlone', [    
                [ 'ModelDDvlPlone_JustCached',                       'Just Cached-',],
                [ 'ModelDDvlPlone_Time_label',                       'Date-',], 
                [ 'ModelDDvlPlone_Len_label',                        'Len-',], 
                [ 'ModelDDvlPlone_User_label',                       'User-',], 
                [ 'ModelDDvlPlone_Date_label',                       'Date-',], 
                [ 'ModelDDvlPlone_Project_label',                    'Project-',], 
                [ 'ModelDDvlPlone_Language_label',                   'Language-',], 
                [ 'ModelDDvlPlone_View_label',                       'View-',], 
                [ 'ModelDDvlPlone_RoleKind_label',                   'Role kind-',], 
                [ 'ModelDDvlPlone_FilePath_label',                   'File-',], 
                [ 'ModelDDvlPlone_Path_label',                       'Path-',], 
                [ 'ModelDDvlPlone_MetaType_label',                   'MetaType-',], 
                [ 'ModelDDvlPlone_PortalType_label',                 'PortalType-',], 
                [ 'ModelDDvlPlone_ArchetypeName_label',              'ArchetypeName-',], 
                [ 'ModelDDvlPlone_ElementId_label',                  'ElementId-',], 
                [ 'ModelDDvlPlone_UID_label',                        'UID-',], 
                [ 'ModelDDvlPlone_URL_label',                        'URL-',], 
                [ 'ModelDDvlPlone_Len_label',                        'Len-',], 
                [ 'title_label',                                     'Title-',], 
                [ 'ModelDDvlPlone_Relation_label',                   'Relation-'],
                [ 'ModelDDvlPlone_ShowNoFromCacheLink_label',        'Show generated-',], 
                [ 'ModelDDvlPlone_FlushFromCacheLink_label',         'Flush from cache-',], 
                [ 'ModelDDvlPlone_FlushFromDiskCacheLink_label',     'Flush from diskcache-',], 
                [ 'ModelDDvlPlone_RelatedElement_label',             'Related Element-',],
            ]],                                                      
        ]        
        theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someDomainsStringsAndDefaults, someTranslations)
                

    
        
        # ###########################################################
        """Render a caching information collapsible section to append to the rendered template HTML.
            
        """
        unRenderedCacheInfo = u''
        if aDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]:
            
            # ###########################################################
            """Prepare internationalized strings, and info values.
                
            """
            unPagina = ''
            if aViewName in [ 'Textual', 'Textual_NoHeaderNoFooter',]:
                unPagina = '/'
            elif aViewName in [ 'Tabular', 'Tabular_NoHeaderNoFooter',]:
                unPagina = '/Tabular/'
            elif aViewName.endswith( '_NoHeaderNoFooter'):
                unPagina = '/%s/' % aViewName[: 0 - len( '_NoHeaderNoFooter')]
            else:
                unPagina = '/%s/' % aViewName

            
        
        
        # ###########################################################
        """Render template or invoke callable with HTML result, because it was not found (valid) in the cache. This may take some significant time. Status of cache may have changed since.
        
        """
        unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
            theModelDDvlPloneTool=theModelDDvlPloneTool, 
            theContextualObject  =theContextualObject, 
            theTemplateName      =theTemplateName, 
            theAdditionalParams =theAdditionalParams,
        )
        
        
        aEndMillis       = fMillisecondsNow()
        unosMilliseconds = aEndMillis - aBeginMillis
                
        unRenderedTemplateWithCacheInfo = unRenderedTemplate
        
  

         
        # ###########################################################
        """If so configured: Append a caching information collapsible section to the rendered template HTML.
        
        """
        if not( aDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]):
            unRenderedTemplateWithCacheInfo = unRenderedTemplate[:]
        
        else:
            

            aCacheEntryValuesDict = someTranslations.copy()
            aCacheEntryValuesDict.update( {
                'cMagicReplacementString_CacheCode':               cMagicReplacementString_CacheCode,
                'cMagicReplacementString_TimeToRetrieve':          cMagicReplacementString_TimeToRetrieve,
                'cMagicReplacementString_Milliseconds':            cMagicReplacementString_Milliseconds,
                'cMagicReplacementString_Len':                     cMagicReplacementString_Len,
                'cMagicReplacementString_Date':                    cMagicReplacementString_Date,
                'cMagicReplacementString_CollapsibleSectionTitle': cMagicReplacementString_CollapsibleSectionTitle,
                'cMagicReplacementString_UniqueId':                cMagicReplacementString_UniqueId,                    
                'aProjectName':                  aProjectName,
                'aNegotiatedLanguage':           aNegotiatedLanguage,
                'unTitle':                       theModelDDvlPloneTool.fAsUnicode( theContextualObject, theContextualObject.Title()),
                'unCacheId':                     unCacheEntryUniqueId,
                'unElementURL':                  unElementURL,
                'unElementUID':                  unElementUID,
                'unElementPath':                 unElementPath,
                'aViewName':                     aViewName,
                'aRoleKindToIndex':              aRoleKindToIndex,
                'unMemberId':                    unMemberId,
                'unPagina':                      unPagina,
                'aFilePath':                     aFilePath,
                'unMetaType':                    unElementMetaType,
                'unPortalType':                  unElementPortalType,
                'unArchetypeName':               unElementArchetypeName,
                'unElementId':                   unElementId,
            })                   
                
                        
            
            unRenderedCacheInfo = u"""
                <!-- ######### Start collapsible  section ######### 
                    # ##################################################################################################
                    With placeholder for the title of the section (to be later set as Just Rendered, Just Cached, Cached 
                --> 
                <dl id="cid_MDDCachedElementView" class="collapsible inline collapsedInlineCollapsible" >
                    <dt class="collapsibleHeader">
                        <span>%(cMagicReplacementString_CollapsibleSectionTitle)s %(cMagicReplacementString_TimeToRetrieve)s</span>                        
                    </dt>
                    <dd class="collapsibleContent">
                        <br/>
                        <form style="display: inline" action="%(unElementURL)s%(unPagina)s" method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theNoCache"   value="on" />
                            <input type="hidden" name="theNoCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="submit" value="%(ModelDDvlPlone_ShowNoFromCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDShowNoFromCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        &emsp;
                        <form style="display: inline"  action="%(unElementURL)s%(unPagina)s" method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theNoCache"   value="on" />
                            <input type="hidden" name="theNoCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theFlushCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="submit" value="%(ModelDDvlPlone_FlushFromCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDFlushCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        &emsp;
                        <form  style="display: inline"  action="%(unElementURL)s%(unPagina)s" method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theNoCache"   value="on" />
                            <input type="hidden" name="theNoCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theFlushCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theFlushDiskCache" value="1" />
                            <input type="submit" value="%(ModelDDvlPlone_FlushFromDiskCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDFlushDiskCacheCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        <br/>
                        <table class="listing" ">
                            <thead>
                                <tr>
                                    <th class="nosort"/>
                                    <th class="nosort"/>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="odd">
                                    <td align="left"><strong>Id</strong></td>
                                    <td align="left">%(cMagicReplacementString_UniqueId)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_FilePath_label)s</strong></td>
                                    <td align="left">%(aFilePath)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Time_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Milliseconds)s ms</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Len_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Len)s chars</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_User_label)s</strong></td>
                                    <td align="left">%(unMemberId)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Date_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Date)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Project_label)s</strong></td>
                                    <td align="left">%(aProjectName)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Language_label)s</strong></td>
                                    <td align="left">%(aNegotiatedLanguage)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(title_label)s</strong></td>
                                    <td align="left">%(unTitle)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_MetaType_label)s</strong></td>
                                    <td align="left">%(unMetaType)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_PortalType_label)s</strong></td>
                                    <td align="left">%(unPortalType)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_ArchetypeName_label)s</strong></td>
                                    <td align="left">%(unArchetypeName)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_ElementId_label)s</strong></td>
                                    <td align="left">%(unElementId)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Path_label)s</strong></td>
                                    <td align="left">%(unElementPath)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_URL_label)s</strong></td>
                                    <td align="left">%(unElementURL)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_UID_label)s</strong></td>
                                    <td align="left">%(unElementUID)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_View_label)s</strong></td>
                                    <td align="left">%(aViewName)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_RoleKind_label)s</strong></td>
                                    <td align="left">%(aRoleKindToIndex)s</td>
                                </tr>
            """ % aCacheEntryValuesDict
                
                       
            if unRelationCursorName and not ( unRelationCursorName == cNoRelationCursorName):
                unRenderedCacheInfo = u"""
                                %s
                                <tr class="even">
                                    <td align="left"><strong>%s</strong></td>
                                    <td align="left">%s</td>
                                </tr>
                """ % ( 
                    unRenderedCacheInfo,
                    someTranslations[ 'ModelDDvlPlone_Relation_label'], 
                    unRelationCursorName,
                )
                
            if unCurrentElementUID and not ( unCurrentElementUID == cNoCurrentElementUID):
                unRenderedCacheInfo = u"""
                                %s
                                <tr class="%s">
                                    <td align="left"><strong>%s</strong></td>
                                    <td align="left">%s</td>
                                </tr>
                """ % ( 
                    unRenderedCacheInfo,
                    (( unRelationCursorName and not ( unRelationCursorName == cNoRelationCursorName)) and 'odd') or 'even',
                    someTranslations[  'ModelDDvlPlone_RelatedElement_label'],
                    unCurrentElementUID,
                )
                
            unRenderedCacheInfo = u"""
                                %s
                            </tbody>
                        </table>
                        <br/>   
                    </dd>
                </dl>
                <!-- ######### End collapsible  section ######### --> 
            """  % unRenderedCacheInfo
            
            
                        
            
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_UniqueId,     str( unCacheEntryUniqueId))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Milliseconds, fStrGrp( unosMilliseconds))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Len,          fStrGrp( len( unRenderedTemplate)))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Date,         fMillisecondsToDateTime( aEndMillis).rfc822())
               
            if aDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedTemplate, unRenderedCacheInfo,)
            else:
                unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedCacheInfo, unRenderedTemplate,)
            
        
                
                
                
         # ###########################################################
        """Add a comment with the rendering time at the top of the rendered HTML, to be used when reading from disk to determine if the HTML on disk has expired or can be reused.
        
        """
        unRenderingMillisecondsHTMLComment = """<!-- RenderMilliseconds=%s -->""" % aEndMillis
        unRenderedTemplateWithCacheInfo = '%s\n%s' % ( unRenderingMillisecondsHTMLComment, unRenderedTemplateWithCacheInfo,)
        
        
              
        
        # ###########################################################
        """CRITICAL SECTION to register in the promised cache entry the HTML result of rendering the template. 
        
        """
        someFilesToDelete = [ ]
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                                    
              
            
            # ###########################################################
            """Check if somebody messed with the promised cache entry, so it is not being updated here.
            
            """
            if ( unPromiseMade == unExistingOrPromiseCacheEntry.vPromise):
                
                unMillisecondsNow   = fMillisecondsNow()

                unExistingOrPromiseCacheEntry.vHTML            = unRenderedTemplateWithCacheInfo
                unExistingOrPromiseCacheEntry.vDateMillis      = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                unExistingOrPromiseCacheEntry.vLastHit         = unMillisecondsNow
                    
                unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                                    
                unStatisticsUpdate = {
                    cCacheStatistics_TotalRenderings:  1,
                    cCacheStatistics_TotalCharsCached: len( unExistingOrPromiseCacheEntry.vHTML),
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                
                # ###########################################################
                """MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
                
                """
                self._pFlushCacheEntriesToReduceMemoryUsed( theModelDDvlPloneTool, theContextualObject, aCacheName, )

            
            
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            


            
        theVariables[ 'unTemplateToCache'] = unRenderedTemplateWithCacheInfo[:]
            

        # ###########################################################
        """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
        
        """
        unRenderedTemplateToReturn = unRenderedTemplateWithCacheInfo.replace(    
            '<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
            '<span>%s' % someTranslations[ 'ModelDDvlPlone_JustCached'],
        )   
        
        unDurationString = '%d ms' % unosMilliseconds
        
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
            u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
            u'%s</span>' % unDurationString
        )

        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
           cMagicReplacementString_CacheCode, 
           '%d' % aEndMillis
        )
        
        theVariables[ 'unTemplateToReturn'] = unRenderedTemplateToReturnWithDuration
        
        aRenderResult.update( {
            'status':            cRenderStatus_Completed, 
            'rendered_html':     unRenderedTemplateToReturnWithDuration,
        })                                    
        return aRenderResult
        
        
        
        
        
        
   
    security.declarePrivate( '_fInvokeCallable_Or_RenderTemplate')
    def _fInvokeCallable_Or_RenderTemplate(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None):
        """Invoke callable or Render template or returning the HTML result.
        
        """
        
        aCallable      = None
        aCallableParms = {}
        aCallableCtxt  = None
        if theAdditionalParams:
            aCallable = theAdditionalParams.get( 'callable', None)
            if aCallable:
                aCallableCtxt  = theAdditionalParams.get( 'callable_ctxt', {})
                aCallableParms = theAdditionalParams.get( 'callable_parms', {})
                
                
        unRenderedTemplate = u''
        if aCallable:
            unRenderedTemplate = aCallable( aCallableCtxt, aCallableParms)
        else:
            unRenderedTemplate = theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)

        return unRenderedTemplate
    
    
            

 
    
    security.declarePrivate( '_fRenderTemplateOrCachedForElement_Phase_StoreDisk')
    def _fRenderTemplateOrCachedForElement_Phase_StoreDisk(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """Store the rendered HTML on disc, for the project, the root UID, for the currently negotiated language, modulus of element UID, element uid, view, relation , current related UID, and role/user id.
        
        """
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        if not theVariables:
            return False
        
        aCacheName                    = theVariables[ 'aCacheName']
        aCacheKind                    = theVariables[ 'aCacheKind']
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unRelationCursorName          = theVariables[ 'unRelationCursorName'] 
        unCurrentElementUID           = theVariables[ 'unCurrentElementUID'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        unElementURL                  = theVariables[ 'unElementURL']
        unElementUID                  = theVariables[ 'unElementUID']
        unRootElementPath             = theVariables[ 'unRootElementPath']
        unRootElementUID              = theVariables[ 'unRootElementUID']
        unElementPath                 = theVariables[ 'unElementPath']
        aViewName                     = theVariables[ 'aViewName']
        aRoleKindToIndex              = theVariables[ 'aRoleKindToIndex']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        someTranslations              = theVariables[ 'someTranslations']
        aDisplayCacheHitInformation   = theVariables[ 'aDisplayCacheHitInformation']
        unTemplateToReturn            = theVariables[ 'unTemplateToReturn']
        unTemplateToCache             = theVariables[ 'unTemplateToCache']
         
        
        if not aCacheDiskEnabled:
            return False
        
        if not unTemplateToCache:
            return False
        
        if not unExistingOrPromiseCacheEntry:
            return False
        
        
  
        # ###########################################################
        """Try to access the directory containing the element independent files with cached HTML.
            
        """
        if not aCacheDiskPath:
            return False

        aCacheDiskPathExist = False
        try:
            aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
        except:
            None
        if not aCacheDiskPathExist:
            try:
                os.makedirs(aCacheDiskPath)
            except:
                None
            try:
                aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
            except:
                None
            if not aCacheDiskPathExist:
                return False
        
        
        # ###########################################################
        """Access directories, or create as needed, for project, root UID, language, the modulus 100 of the checksum of element UID , element UID, view,  relation, relation current UID, and role/userId.
            
        """
        aProjectPath = os.path.join( aCacheDiskPath, aProjectName)
        aProjectPathExist = False
        try:
            aProjectPathExist = os.path.exists( aProjectPath)
        except:
            None
        if not aProjectPathExist:
            try:
                os.mkdir( aProjectPath, cCacheDisk_ForElements_FolderCreateMode_Project)
            except:
                None
            try:
                aProjectPathExist = os.path.exists( aProjectPath)
            except:
                None
            if not aProjectPathExist:
                return False
        
            
            
        aRootUIDPath = os.path.join( aProjectPath, unRootElementUID)
        aRootUIDPathExist = False
        try:
            aRootUIDPathExist = os.path.exists( aRootUIDPath)
        except:
            None
        if not aRootUIDPathExist:
            try:
                os.mkdir( aRootUIDPath, cCacheDisk_ForElements_FolderCreateMode_RootUID)
            except:
                None
            try:
                aRootUIDPathExist = os.path.exists( aRootUIDPath)
            except:
                None
            if not aRootUIDPathExist:
                return False
                        
            
            
            
        anElementUIDModulus = self.fModulusUID( unElementUID, cCacheDisk_UIDModulus)
            
        aElementUIDModulusPath = os.path.join( aRootUIDPath, anElementUIDModulus)
        aElementUIDModulusPathExist = False
        try:
            aElementUIDModulusPathExist = os.path.exists( aElementUIDModulusPath)
        except:
            None
        if not aElementUIDModulusPathExist:
            try:
                os.mkdir( aElementUIDModulusPath, cCacheDisk_ForElements_FolderCreateMode_ElementUIDModulus)
            except:
                None
            try:
                aElementUIDModulusPathExist = os.path.exists( aElementUIDModulusPath)
            except:
                None
            if not aElementUIDModulusPathExist:
                return False
        

            
            
        aElementUIDPath = os.path.join( aElementUIDModulusPath, unElementUID)
        aElementUIDPathExist = False
        try:
            aElementUIDPathExist = os.path.exists( aElementUIDPath)
        except:
            None
        if not aElementUIDPathExist:
            try:
                os.mkdir( aElementUIDPath, cCacheDisk_ForElements_FolderCreateMode_ElementUID)
            except:
                None
            try:
                aElementUIDPathExist = os.path.exists( aElementUIDPath)
            except:
                None
            if not aElementUIDPathExist:
                return False
        

           

        aLanguagePath = os.path.join( aElementUIDPath, aNegotiatedLanguage)
        aLanguagePathExist = False
        try:
            aLanguagePathExist = os.path.exists( aLanguagePath)
        except:
            None
        if not aLanguagePathExist:
            try:
                os.mkdir( aLanguagePath, cCacheDisk_ForElements_FolderCreateMode_Language)
            except:
                None
            try:
                aLanguagePathExist = os.path.exists( aLanguagePath)
            except:
                None
            if not aLanguagePathExist:
                return False
                        
             
         
        # ###########################################################
        """Write the page on disk cache file.
            
        """
        aViewFileName = '%s-%s-%s-%s%s' % ( aViewName, unRelationCursorName, unCurrentElementUID, aRoleKindToIndex, cCacheDiskFilePostfix)
        aViewPath = os.path.join( aLanguagePath, aViewFileName)

        aWritten = False
        try:
            aViewFile  = None
            try:
                aViewFile = open( aViewPath, cCacheDisk_ForElements_FileOpenWriteMode_View, cCacheDisk_ForElements_FileOpenWriteBuffering_View)
                aViewFile.write( unTemplateToCache)
            finally:
                if aViewFile:
                    aViewFile.close()
            aWritten = True
        except IOError:
            return False
  
        if not aWritten:
            return False
        
        


        # ###########################################################
        """Update statistics of written file and chars.
            
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            unExistingOrPromiseCacheEntry.vFilePath        = aViewPath
            unExistingOrPromiseCacheEntry.vDirectory       = aElementUIDPath
            
                
            unStatisticsUpdate = {
                cCacheStatistics_TotalFilesWritten:   1,
                cCacheStatistics_TotalCharsWritten:   len( unTemplateToCache),
            }
            self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)

        
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        
        
        return True
    

        
        
        
        
        
        
       
    security.declarePrivate( 'fRenderHandlers_ForElement')
    def fRenderHandlers_ForElement(self, theModelDDvlPloneTool, theContextualObject,):
        """methods to handle the rendering phases for cache entries associated with specific element.
        """
        someHandlers = {
            'memory':  self._fRenderTemplateOrCachedForElement_Phase_TryMemory,
            'disc':    self._fRenderTemplateOrCachedForElement_Phase_TryDisk,
            'render':  self._fRenderTemplateOrCachedForElement_Phase_Render,
            'store':   self._fRenderTemplateOrCachedForElement_Phase_StoreDisk,
        }
        return someHandlers
    
        
                    
        
        
        
            
            

            
            
            


    security.declarePrivate( 'fIsPrivateCacheViewForNonAnonymousUsers')
    def fIsPrivateCacheViewForQualifiedUsers(self , theContextualObject, theTemplateName):
        """Shall return true when the template name is for a view sensitive to user permissions or roles ( modify portal content, delete, add folders, ) on rendered objects, in addition to the permissions required by Zope/Plone to deliver data to the requester (view, list folder contents, access content information,).
        
        """

        # ##############################################################
        """Assert whether the view is sensitive to users, for the aplication or for the framework.
        
        """
        try:
            unIsPrivateViewForQualifiedUsers = theContextualObject.fIsPrivateCacheViewForQualifiedUsers( theTemplateName)
            if unIsPrivateViewForQualifiedUsers:
                return unIsPrivateViewForQualifiedUsers
        except:
            None
            
        return  theTemplateName in  cPrivateCacheViewsForQualifiedUsers
        
    
        
    
    
    


    # #############################################################
    """User Role access methods. Roles are classified into a reduced number of role kinds: Anonymous, Authenticated, Owner, Manager
    
    """

         
    security.declarePrivate( 'fGetMemberRoleKindAndUserId')
    def fGetMemberRoleKindAndUserId(self , theContextualObject, theTemplateName):
    
        aMembershipTool = getToolByName( theContextualObject, 'portal_membership', None)
        if not aMembershipTool:
            return None
        
        unMember = aMembershipTool.getAuthenticatedMember()   
        if not unMember:
            return None
        
        unMemberUserName = unMember.getUserName()
        if unMemberUserName == 'Anonymous User':
            return [ cRoleKind_Anonymous, 'Anonymous User', cZopeRole_Anonymous]
        
        unMemberId = unMember.getMemberId()
        
        unElementoGetRoles = theContextualObject
        # ###############
        """ACV 20091217 Roles from the contextual element, hopefully the element for which the view is requested
        
        """
        #unElementoRaiz = None
        #try:
            #unElementoRaiz = theContextualObject.getRaiz()
        #except:
            #None
        #if not ( unElementoRaiz == None):
            #unElementoGetRoles = unElementoRaiz
        
        aUserRolesSet = set( ModelDDvlPloneTool_Retrieval().fGetRequestingUserRoles( unElementoGetRoles))
        if not aUserRolesSet:
            return [ cRoleKind_Anonymous, unMemberId, cZopeRole_Anonymous]
        
                            


        # ##############################################################
        """Retrieve the specification of mapping from roles to role kinds, from the appplication element (if supported), and the generic Zope roles known by the ModelDDvlPlone framework.
        
        """
        someApplicationRolesAndRoleKinds = None
        try:
            someApplicationRolesAndRoleKinds = theContextualObject.fApplicationRolesAndRoleKinds( )
        except:
            None
            
        someRolesAndRoleKinds = []
        if someApplicationRolesAndRoleKinds:
            someRolesAndRoleKinds.extend( someApplicationRolesAndRoleKinds)
        if cZopeRolesAndRoleKinds:
            someRolesAndRoleKinds.extend( cZopeRolesAndRoleKinds)
            
    
            
        # ##############################################################
        """Cached entries of elements with private caches for the specified view, shall be associated with the User Id (and thus private to the user), except for: Non Anonymous users, that do not hold a Member, Reviewer, Owner or Manager Role in the model root (or this object, if no model root), shall obtain cached pages as an Authenticated role kind.
        
        """
        aRoleKind = cRoleKind_Anonymous
        aRole     = cZopeRole_Anonymous
        for aZopeRolesAndRoleKind in someRolesAndRoleKinds:
            
            aRolesOfAKindSet = set( aZopeRolesAndRoleKind[ 0])
            someMatchingRoles = aUserRolesSet.intersection( aRolesOfAKindSet)
            if someMatchingRoles:

                aRoleKind = aZopeRolesAndRoleKind[ 1]
                break
        
        return [ aRoleKind, unMemberId, aZopeRolesAndRoleKind[ 0][ 0]]

    


    

    
    


    # #############################################################
    """Utility methods
    
    """

         
    security.declarePrivate( 'fModulusUID')
    def fModulusUID(self , theUID, theModulus):
        """Compute a sum of characters in theUID and return its modulus.
        
        """
        
        aModulus = 0
        if theUID and theModulus:
            aSum = 0
            for aChar in theUID:
                aSum += ord( aChar)
                
            aModulus = aSum % theModulus
        
        aNumCharsToReturn = len( str( theModulus))
        
        aStringToReturn = '%s%d' % ( '0' * aNumCharsToReturn, aModulus)
        aStringToReturn = aStringToReturn[ 0 - aNumCharsToReturn:]
        return aStringToReturn
    
    
    
            
            
            

            
            

    
    
    
    
    
    
       
    security.declarePrivate( 'fNewVoidAllCachesDiagnostics')
    def fNewVoidAllCachesDiagnostics(self, ):
        aDiagnostics = {
            'success':                                     False,
            'UIDs_registry_size':                          0,
            'numentries_in_UIDs_registry':                 0,
            'uniqueIDs_registry_size':                     0,
            'allcacheEntriesInStructures':                 set( ),
            'allEntriesWithProblems':                      { },
            'structures_UIDs_withoutElement':              set( ),
            'entriesByUniqueId_Not_in_structure':          set( ),
            'entriesByUID_Not_in_structure':               set( ),
            'UIDs_without_corresponding_elements':         set( ),
            'elementnames_inconsistent_entries':           [ ],
            'invalid_entries_in_UID_registry':             set( ),
            'invalid_entries_in_UniqueId_registry':        set( ),
            'broken_promise_entries_in_UniqueId_registry': set( ),
            'broken_promise_entries_in_UID_registry':      set( ),
            'caches_diagnostics':                          { },
        }
        return aDiagnostics
    
     
        
    
       
    security.declarePrivate( 'fNewVoidCacheDiagnostic')
    def fNewVoidCacheDiagnostic(self, ):
        aDiagnostics = {
            'cache_kind':                                  '',
            'cache_name':                                  '',
            'success':                                     False,
            'cacheEntriesInStructure':                     set( ),      #
            'entriesWithProblems':                         { },         #
            'structure_missing_entries':                   [ ],     #   #
            'structure_voids':                             [ ],     #   #
            'structure_inconsistent_entries':              [ ],     #   #
            'structure_entries_found_more_than_once':      set( ),  #   #
            'structure_entries_not_in_uniqueid_registry':  set( ),  #   #
            'structure_entries_without_UID':               set( ),  #   #
            'structure_entries_not_in_UID_registry':       set( ),  #   #
            'linkedlist_size':                             0,           #
            'structure_and_linkedlist_size_difference':    0,       #   #
            'list_errors':                                 [ ],     #   #
            'invalid_entries_in_list':                     set( ),  #   #
            'promised_entries_in_list':                    set( ),
            'broken_promise_entries_in_list':              set( ),  #   #
            'linkedlist_size_direction_difference':        0,       #   #
            'found_fromOldToNew_moreThanOnce':             set( ),  #   #
            'found_fromNewToOld_moreThanOnce':             set( ),  #   #        
            'entries_WithNext_NoPrevious':                 set( ),  #   #
            'entries_WithNext_WrongPrevious':              set( ),  #   #
            'entries_WithoutNext':                         set( ),  #   #
            'entries_WithPrevious_NoNext':                 set( ),  #   #
            'entries_WithPrevious_WrongNext':              set( ),  #   #
            'entries_WithoutPrevious':                     set( ),  #   #
            
        }
        return aDiagnostics

    
    
    
    
       
    security.declareProtected( permissions.ManagePortal, 'fCachesDiagnostics')
    def fCachesDiagnostics(self, theModelDDvlPloneTool, theContextualObject, theCacheNames=None, theAdditionalParams=None):
    
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            return self.fCachesDiagnostics_WithinCriticalSection( theModelDDvlPloneTool, theContextualObject, theCacheNames=theCacheNames, theAdditionalParams=theAdditionalParams)
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                            
                                                       
            
    
                
       
    security.declareProtected( permissions.ManagePortal, 'fCachesDiagnostics_WithinCriticalSection')
    def fCachesDiagnostics_WithinCriticalSection(self, theModelDDvlPloneTool, theContextualObject, theCacheNames=None, theAdditionalParams=None):
    
        
        
        someCacheNames = theCacheNames
        if not someCacheNames:
            someCacheNames = cCacheNamesAll[:]
        else:
            if not ( isinstance( someCacheNames, list) or isinstance( someCacheNames, tuple) or isinstance( someCacheNames, set)):
                someCacheNames = list( someCacheNames)
            someCacheNames = set( someCacheNames).intersection( set( cCacheNamesAll))


             
        # ###########################################################
        """Verify cache control structures to access the cache entries
        
        """
        someUIDsElementsToRetrieve = set()
        
        allDiagnostics = self.fNewVoidAllCachesDiagnostics()
        allCacheEntriesInStructure_AllCaches = allDiagnostics[ 'allcacheEntriesInStructures']
        allEntriesWithProblems_AllCaches     = allDiagnostics[ 'allEntriesWithProblems']

        
        # ###########################################################
        """Iterate over Caches
        
        """
        
        
        for aCacheName in someCacheNames:
                
            aDiagnostics = self.fNewVoidCacheDiagnostic()
            aDiagnostics[ 'cache_name'] = aCacheName
            aCacheKind = ''
            for aCName, aCKind in cCacheNamesAndKindsToCreate:
                if aCName == aCacheName:
                    aCacheKind = aCKind
                    break
            if aCacheKind:
                aDiagnostics[ 'cache_kind'] = aCacheKind
               
            allDiagnostics[ 'caches_diagnostics'][ aCacheName] = aDiagnostics
            
            someCacheEntriesInStructure = aDiagnostics[ 'cacheEntriesInStructure']
            someEntriesWithProblems     = aDiagnostics[ 'entriesWithProblems']

            
            
            if aCacheKind in [ cCacheKind_ForElements, cCacheKind_ForUsers,]:
            
                # ###########################################################
                """Iterate over Projects
                
                """
                someProjectNames = self.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, aCacheName,)
                for aProjectName in someProjectNames:
                    someTemplatesByLanguageForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)                              
                   
                    if not someTemplatesByLanguageForProject:
                        aDiagnostics[ 'structure_voids'].append( [ aProjectName,])
                        
                        
                        
                    # ###########################################################
                    """Iterate over Languages
                    
                    """
                    someLanguages =  ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or []
                    for aLanguage  in someLanguages:
                        someTemplatesByUIDForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
                        
                   
                        if not someTemplatesByUIDForLanguage:
                            aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage])
                            
                            
                            
                        # ###########################################################
                        """Gather UIDs and Iterate over Elements UIDs
                        
                        """                    
                        someUIDs = (someTemplatesByUIDForLanguage and someTemplatesByUIDForLanguage.keys()) or [] 
                        
                        someUIDsElementsToRetrieve.update( someUIDs)
                        
                        for anUID in someUIDs:
                            someTemplatesByViewForUID = someTemplatesByUIDForLanguage.get( anUID, {})
                            
                            if not someTemplatesByViewForUID:
                                aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, anUID, ])
                                
                                
                                
                            # ###########################################################
                            """Iterate over Views
                            
                            """                        
                            someViewNames = ( someTemplatesByViewForUID and someTemplatesByViewForUID.keys()) or []
                            for aViewName in someViewNames:
                                someTemplatesByRelationForView = someTemplatesByViewForUID.get( aViewName, {})
                                
                   
                                if not someTemplatesByRelationForView:
                                    aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, anUID, aViewName, ])
                                    
                                    
                                    
                                # ###########################################################
                                """Iterate over Relations
                                
                                """
                                someRelations = ( someTemplatesByRelationForView and someTemplatesByRelationForView.keys()) or []
                                for aRelationName in someRelations:
                                    someTemplatesByRelatedUIDForRelation = someTemplatesByRelationForView.get( aRelationName, {})
                                    
                   
                                    if not someTemplatesByRelatedUIDForRelation:
                                        aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, anUID, aViewName, aRelationName, ])
                                        
                                        
                                        
                                    # ###########################################################
                                    """Gather and Iterate over Related Element UIDs
                                    
                                    """                                
                                    someRelatedUIDs = ( someTemplatesByRelatedUIDForRelation and someTemplatesByRelatedUIDForRelation.keys()) or []
                                    for aRelatedUID in someRelatedUIDs:
                                        if not ( aRelatedUID == cNoCurrentElementUID):
                                            someUIDsElementsToRetrieve.add( aRelatedUID)
                    
                                        someTemplatesByRoleOrUserForRelatedUID = someTemplatesByRelatedUIDForRelation.get( aRelatedUID, {})
                                          
                   
                                        if not someTemplatesByRoleOrUserForRelatedUID:
                                            aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, anUID, aViewName, aRelationName, aRelatedUID, ])
                                        
                                            
                                            
                                        # ###########################################################
                                        """Iterate over RoleOrUsers
                                        
                                        """
                                        someRoleOrUsers = sorted( ( someTemplatesByRoleOrUserForRelatedUID and someTemplatesByRoleOrUserForRelatedUID.keys()) or [])
                                        for aRoleOrUserName in someRoleOrUsers:
                                        
                                            
                                            
                                            # ########################
                                            """Access CacheEntry
                                            
                                            """
                                            aCacheEntry = someTemplatesByRoleOrUserForRelatedUID.get( aRoleOrUserName, None)
                                        
                                            if not aCacheEntry:
                                                # ########################
                                                """Report cache entry as missing
                                                
                                                """
                                                aDiagnostics[ 'structure_missing_entries'].append( [ aProjectName, aLanguage, anUID, aViewName, aRelationName, aRelatedUID, aRoleOrUserName, ])
                                                
                                                
                                            else:
                                                
                                                if aCacheEntry in someCacheEntriesInStructure:
                                                    aDiagnostics[ 'structure_entries_found_more_than_once'].add( aCacheEntry)
                                                
                                                else:                                                
                                                    someCacheEntriesInStructure.add( aCacheEntry)
                                                
                                                if not aCacheEntry.vValid:
                                                    aDiagnostics[ 'invalid_entries_in_list'].add( aCacheEntry)
                                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'Invalid',])
                                                    
                                                aCacheEntryPromise = aCacheEntry.vPromise
                                                if aCacheEntryPromise and not ( aCacheEntryPromise == cCacheEntry_PromiseFulfilled_Sentinel):
                                                    aDiagnostics[ 'promised_entries_in_list'].add( aCacheEntry)
                
                                                if not aCacheEntryPromise:
                                                    aDiagnostics[ 'broken_promise_entries_in_list'].add( aCacheEntry)
                                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'BrokenPromise',])
                                    
                                                    
                                                # ########################
                                                """Verify CacheEntry information consistent with the tree indexing data used to reach it, and report inconsistencies
                                                
                                                """
                                                someEntryInconsistenciesInTree = [ ]
                                                if ( not aCacheEntry.vProjectName) or not ( aCacheEntry.vProjectName == aProjectName):
                                                    someEntryInconsistenciesInTree.append( [ 'vProjectName', aCacheEntry.vProjectName, aProjectName,])
                                                if ( not aCacheEntry.vLanguage)    or not ( aCacheEntry.vLanguage == aLanguage):
                                                    someEntryInconsistenciesInTree.append( [ 'vLanguage',    aCacheEntry.vLanguage,    aLanguage,])
                                                if ( not aCacheEntry.vUID )        or not ( aCacheEntry.vUID == anUID):
                                                    someEntryInconsistenciesInTree.append( [ 'vUID',         aCacheEntry.vUID,         anUID,])
                                                if ( not aCacheEntry.vView )       or not (aCacheEntry.vView == aViewName):
                                                    someEntryInconsistenciesInTree.append( [ 'vView',        aCacheEntry.vView,        aViewName,])
                                                if ( not aCacheEntry.vRelation)    or not ( aCacheEntry.vRelation == aRelationName):
                                                    someEntryInconsistenciesInTree.append( [ 'vRelation',    aCacheEntry.vRelation,    aRelationName,])
                                                if ( not aCacheEntry.vRelation)    or not ( aCacheEntry.vCurrentUID == aRelatedUID): 
                                                    someEntryInconsistenciesInTree.append( [ 'vCurrentUID',  aCacheEntry.vCurrentUID,  aRelatedUID,])
                                                if ( not aCacheEntry.vRoleKind )   or not ( aCacheEntry.vRoleKind == aRoleOrUserName):
                                                    someEntryInconsistenciesInTree.append( [ 'vRoleKind',    aCacheEntry.vRoleKind,    aRoleOrUserName,])
                                                if someEntryInconsistenciesInTree:
                                                    aDiagnostics[ 'structure_inconsistent_entries'].append( [ aCacheEntry,              someEntryInconsistenciesInTree,])
                                                     
                                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'inconsistencies_in_tree', someEntryInconsistenciesInTree,])
                                                    
                                                # ########################
                                                """Verify CacheEntry properly registered by its unique id
                                                
                                                """
                                                unEntryByUniqueId = self._fGetCachedEntryById( theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUniqueId)
                                                if not unEntryByUniqueId or not ( unEntryByUniqueId == aCacheEntry):
                                                    aDiagnostics[ 'structure_entries_not_in_uniqueid_registry'].add( aCacheEntry)
                                                    
                                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'not_in_uniqueid_registry',])
                                                      
                                                
                                                # ########################
                                                """Verify CacheEntry properly registered by the element UID
                                                
                                                """
                                                if not aCacheEntry.vUID:                                                  
                                                    aDiagnostics[ 'structure_entries_without_UID'].add( aCacheEntry)
                                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'structure_entries_without_UID',])
                                                    
                                                else:
                                                    unasEntriesByUID = self._fGetCachedEntriesByUID(  theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUID)
                                                    if not ( aCacheEntry in unasEntriesByUID):
                                                        aDiagnostics[ 'structure_entries_not_in_UID_registry'].add( aCacheEntry)
                                                        
                                                        self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'not_in_UID_registry',])

                                                
                                                
            if aCacheKind == cCacheKind_ElementIndependent:
            
                # ###########################################################
                """Iterate over Projects
                
                """
                someProjectNames = self.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, aCacheName,)
                for aProjectName in someProjectNames:
                    someTemplatesByLanguageForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)                              
                   
                    if not someTemplatesByLanguageForProject:
                        aDiagnostics[ 'structure_voids'].append( [ aProjectName,])
                        
                        
                        
                    # ###########################################################
                    """Iterate over Languages
                    
                    """
                    someLanguages =  ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or []
                    for aLanguage  in someLanguages:
                        someTemplatesByViewForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
                        
                   
                        if not someTemplatesByViewForLanguage:
                            aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage])
                            
                            
                        # ###########################################################
                        """Iterate over Views
                        
                        """                        
                        someViewNames = ( someTemplatesByViewForLanguage and someTemplatesByViewForLanguage.keys()) or []
                        for aViewName in someViewNames:
                            
                                         
                            # ########################
                            """Access CacheEntry
                            
                            """
                            aCacheEntry = someTemplatesByViewForLanguage.get( aViewName, None)
                        
                            if not aCacheEntry:
                                # ########################
                                """Report cache entry as missing
                                
                                """
                                aDiagnostics[ 'structure_missing_entries'].append( [ aProjectName, aLanguage, aViewName,])
                                
                                
                            else:
                                
                                if aCacheEntry in someCacheEntriesInStructure:
                                    aDiagnostics[ 'structure_entries_found_more_than_once'].add( aCacheEntry)
                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'structure_entries_found_more_than_once',])
                                
                                else:                                                
                                    someCacheEntriesInStructure.add( aCacheEntry)
                                
                                if not aCacheEntry.vValid:
                                    aDiagnostics[ 'invalid_entries_in_list'].add( aCacheEntry)
                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'Invalid',])
                                    
                                aCacheEntryPromise = aCacheEntry.vPromise
                                if aCacheEntryPromise and not ( aCacheEntryPromise == cCacheEntry_PromiseFulfilled_Sentinel):
                                    aDiagnostics[ 'promised_entries_in_list'].add( aCacheEntry)

                                if not aCacheEntryPromise:
                                    aDiagnostics[ 'broken_promise_entries_in_list'].add( aCacheEntry)
                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'BrokenPromise',])
                                    
                                    
                                    
                                # ########################
                                """Verify CacheEntry information consistent with the tree indexing data used to reach it, and report inconsistencies
                                
                                """
                                someEntryInconsistenciesInTree = [ ]
                                if ( not aCacheEntry.vProjectName) or not ( aCacheEntry.vProjectName == aProjectName):
                                    someEntryInconsistenciesInTree.append( [ 'vProjectName', aCacheEntry.vProjectName, aProjectName,])
                                if ( not aCacheEntry.vLanguage)    or not ( aCacheEntry.vLanguage == aLanguage):
                                    someEntryInconsistenciesInTree.append( [ 'vLanguage',    aCacheEntry.vLanguage,    aLanguage,])
                                if ( not aCacheEntry.vView )       or not (aCacheEntry.vView == aViewName):
                                    someEntryInconsistenciesInTree.append( [ 'vView',        aCacheEntry.vView,        aViewName,])
                                if someEntryInconsistenciesInTree:
                                    aDiagnostics[ 'structure_inconsistent_entries'].append( [ aCacheEntry,              someEntryInconsistenciesInTree,])
                                     
                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'inconsistencies_in_tree', someEntryInconsistenciesInTree,])
                                    
                                # ########################
                                """Verify CacheEntry properly registered by its unique id
                                
                                """
                                unEntryByUniqueId = self._fGetCachedEntryById( theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUniqueId)
                                if not unEntryByUniqueId or not ( unEntryByUniqueId == aCacheEntry):
                                    aDiagnostics[ 'structure_entries_not_in_uniqueid_registry'].add( aCacheEntry)
                                    
                                    self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'not_in_uniqueid_registry',])
                                      
                                                                                           

                        
            # ########################
            """Verify that the list of entries ordered by last access time contains all entries reached by traversal, and no others
            
            """
            anUnwindHack = True
            while anUnwindHack:
                anUnwindHack = False
                    
                # ########################
                """Verify list sentinels
                
                """
                unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, aCacheName)
                if not unListNewSentinel:
                    aDiagnostics[ 'list_errors'].add( 'no_list_new_sentinel')
                    
                unListOldSentinel = self.fGetCacheStoreListSentinel_Old( theModelDDvlPloneTool, theContextualObject, aCacheName)
                if not unListOldSentinel:
                    aDiagnostics[ 'list_errors'].add( 'no_list_old_sentinel')
                    
                if ( unListNewSentinel and unListOldSentinel) and ( unListNewSentinel == unListOldSentinel):
                    aDiagnostics[ 'list_errors'].add( 'same_new_and_old_sentinels')
                    
                    
                    
                # ########################
                """Verify firsts and lasts links
                
                """
                anOldestEntry = unListOldSentinel.vNext
                if not anOldestEntry:
                    aDiagnostics[ 'list_errors'].add( 'old_sentinel_without_next')
                    
                aNewestEntry = unListNewSentinel.vPrevious
                if not aNewestEntry:
                    aDiagnostics[ 'list_errors'].add( 'new_sentinel_without_previous')
                    
                # ########################
                """Allow empty list
                
                """
                if ( anOldestEntry == unListNewSentinel) and ( aNewestEntry == unListOldSentinel):
                    break
                    
                    
                    
                # ########################
                """Traverse from old to new, stop if discontinued or found repeated entries
                
                """
                someEntriesFoundFromOldToNew = set()
                aCanCheckCointinuityOldToNew = False
                if anOldestEntry:
                    aCurrentEntry = anOldestEntry
                    
                    while aCurrentEntry:
                        if aCurrentEntry in someEntriesFoundFromOldToNew:
                            aDiagnostics[ 'found_fromOldToNew_moreThanOnce'].add( aCurrentEntry)
                            aDiagnostics[ 'list_errors'].add( 'scan_fromOldToNew_stopped_entryfoundMoreThanOnce')
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'fromOldToNew_moreThanOnce',])

                             
                            break
                        else:
                            someEntriesFoundFromOldToNew.add( aCurrentEntry)
                            aNextEntry = aCurrentEntry.vNext
                            if not aNextEntry:
                                aDiagnostics[ 'entries_WithtoutNext'].add( aCurrentEntry)
                                aDiagnostics[ 'list_errors'].add( 'scan_fromOldToNew_stopped_entryWithoutNext')
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'fromOldToNew_entryWithoutNext',])
                                
                                break
                              
                            else:
                                if aNextEntry == unListNewSentinel:
                                    aCanCheckCointinuityOldToNew = True
                                    break
                                aCurrentEntry = aNextEntry
                                                                                                    
                     
                                
                # ########################
                """Traverse from new to old, stop if discontinued or found repeated entries
                
                """
                someEntriesFoundFromNewToOld = set()
                aCanCheckCointinuityNewToOld = False
                if aNewestEntry:
                    aCurrentEntry = aNewestEntry
                               
                    while aCurrentEntry:
                        if aCurrentEntry in someEntriesFoundFromNewToOld:
                            aDiagnostics[ 'found_fromNewToOld_moreThanOnce'].add( aCurrentEntry)
                            aDiagnostics[ 'list_errors'].add( 'scan_fromNewToOld_stopped_entryfoundMoreThanOnce')
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'fromNewToOld_moreThanOnce',])
                            
                            break
                        else:
                            someEntriesFoundFromNewToOld.add( aCurrentEntry)
                            aPreviousEntry = aCurrentEntry.vPrevious
                            if not aPreviousEntry:
                                aDiagnostics[ 'entries_WithoutPrevious'].add( aCurrentEntry)
                                aDiagnostics[ 'list_errors'].add( 'scan_fromNewToOld_stopped_entryWithoutPrevious')
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'fromNewToOld_entryWithoutPrevious',])

                                break
                            
                            else:
                                if aPreviousEntry == unListOldSentinel:
                                    aCanCheckCointinuityNewToOld = True
                                    break
                                aCurrentEntry = aPreviousEntry
                             
                                
                                
                                
                                
                # ########################
                """Verify that the same entries are reached by traversing the list in both directions
                
                """
                someEntriesNotReachedInBothDirections = someEntriesFoundFromNewToOld.symmetric_difference( someEntriesFoundFromOldToNew)
                if someEntriesNotReachedInBothDirections:
                    aDiagnostics[ 'list_errors'].add( 'some_entries_not_reached_in_both_directions')
                    
                aDiagnostics[ 'linkedlist_size'] = max( len( someEntriesFoundFromNewToOld), len( someEntriesFoundFromOldToNew))

                aDiagnostics[ 'linkedlist_size_direction_difference'] = abs( len( someEntriesFoundFromNewToOld) - len( someEntriesFoundFromOldToNew))
                
                
                    
            
                
                
                # ########################
                """Traverse from old to new, check bidirectional entry links
                
                """
                if anOldestEntry and aCanCheckCointinuityOldToNew:
                    aCurrentEntry = anOldestEntry
                    
                    while aCurrentEntry:
                        
                        # ###################
                        """Check continuity with previous entry.
                        
                        """
                        aPreviousEntry = aCurrentEntry.vPrevious
                        if aPreviousEntry:
                            aPreviousEntryNext = aPreviousEntry.vNext
                            if not aPreviousEntryNext:
                                aDiagnostics[ 'entries_WithPrevious_NoNext'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_NoNext',])

                            elif not ( aPreviousEntryNext == aCurrentEntry):
                                aDiagnostics[ 'entries_WithPrevious_WrongNext'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])

                        else:
                            # ####################
                            """Should have been reported above, and this pass never executed.
                            
                            """
                            aDiagnostics[ 'entries_WithoutPrevious'].add( aCurrentEntry)
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithoutPrevious',])
                            break 

                        
                        # ###################
                        """Check continuity with next entry.
                        
                        """
                        aNextEntry = aCurrentEntry.vNext
                        if aNextEntry:
                            aNextEntryPrevious = aNextEntry.vPrevious
                            if not aNextEntryPrevious:
                                aDiagnostics[ 'entries_WithNext_NoPrevious'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithNext_NoPrevious',])
                                
                            elif not ( aNextEntryPrevious == aCurrentEntry):
                                aDiagnostics[ 'entries_WithNext_WrongPrevious'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithNext_WrongPrevious',])

                        else:
                            # ####################
                            """Should have been reported above, and this pass never executed.
                            
                            """
                            aDiagnostics[ 'entries_WithoutNext'].add( aCurrentEntry)
                            break 

                        # ###################
                        """Detect end reached ok
                        
                        """
                        if aNextEntry == unListNewSentinel:
                            break
                        aCurrentEntry = aNextEntry
               
                        
                        
             
                                
                # ########################
                """Traverse from new to old, check bidirectional entry links
                
                """
                if aNewestEntry and aCanCheckCointinuityNewToOld:
                    aCurrentEntry = aNewestEntry
                    
                    while aCurrentEntry:
                        
                        # ###################
                        """Check continuity with previous entry.
                        
                        """
                        aPreviousEntry = aCurrentEntry.vPrevious
                        if aPreviousEntry:
                            aPreviousEntryNext = aPreviousEntry.vNext
                            if not aPreviousEntryNext:
                                aDiagnostics[ 'entries_WithPrevious_NoNext'].add( aCurrentEntry)
                                
                                someEntryProblems = someProblematicEntriesAndDefects.get( aCurrentEntry, None)
                                if someEntryProblems == None:
                                    someEntryProblems = [ ]
                                    someProblematicEntriesAndDefects[ aCurrentEntry] = someEntryProblems
                                someEntryProblems.append( [ 'WithPrevious_NoNext',])
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])

                            elif not ( aPreviousEntryNext == aCurrentEntry):
                                aDiagnostics[ 'entries_WithPrevious_WrongNext'].add( aCurrentEntry)
                                
                                someEntryProblems = someProblematicEntriesAndDefects.get( aCurrentEntry, None)
                                if someEntryProblems == None:
                                    someEntryProblems = [ ]
                                    someProblematicEntriesAndDefects[ aCurrentEntry] = someEntryProblems
                                someEntryProblems.append( [ 'WithPrevious_WrongNext',])
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])
                                
                        else:
                            # ####################
                            """Should have been reported above, and this pass never executed.
                            
                            """
                            aDiagnostics[ 'entries_WithoutPrevious'].add( aCurrentEntry)
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithtoutPrevious',])
                            break 

                        
                        # ###################
                        """Check continuity with next entry.
                        
                        """
                        aNextEntry = aCurrentEntry.vNext
                        if aNextEntry:
                            aNextEntryPrevious = aNextEntry.vPrevious
                            if not aNextEntryPrevious:
                                aDiagnostics[ 'entries_WithNext_NoPrevious'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])
                            elif not ( aNextEntryPrevious == aCurrentEntry):
                                aDiagnostics[ 'entries_WithNext_WrongPrevious'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])

                        else:
                            # ####################
                            """Should have been reported above, and this pass never executed.
                            
                            """
                            aDiagnostics[ 'entries_WithtoutNext'].add( aCurrentEntry)
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithtoutNext',])
                            break 

                        # ###################
                        """Detect end reached ok
                        
                        """
                        if aPreviousEntry == unListOldSentinel:
                            break
                        aCurrentEntry = aPreviousEntry
               
                        
            aLinkedListAndStructureSizeDifference = abs( len( aDiagnostics[ 'cacheEntriesInStructure']) - aDiagnostics[ 'linkedlist_size'])
            aDiagnostics[ 'structure_and_linkedlist_size_difference'] = aLinkedListAndStructureSizeDifference
            if aLinkedListAndStructureSizeDifference:
                self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'StrucutreandLinkedListSizeDifference',])
                
                       
            aSuccess = ( not len( aDiagnostics[ 'entriesWithProblems'])) and \
                ( not len( aDiagnostics[ 'structure_missing_entries'])) and \
                ( not len( aDiagnostics[ 'structure_voids'])) and \
                ( not len( aDiagnostics[ 'structure_inconsistent_entries'])) and \
                ( not len( aDiagnostics[ 'structure_entries_found_more_than_once'])) and \
                ( not len( aDiagnostics[ 'structure_entries_without_UID'])) and \
                ( not len( aDiagnostics[ 'structure_entries_not_in_uniqueid_registry'])) and \
                ( not len( aDiagnostics[ 'structure_entries_not_in_UID_registry'])) and \
                ( not      aDiagnostics[ 'structure_and_linkedlist_size_difference']) and \
                ( not len( aDiagnostics[ 'list_errors'])) and \
                ( not len( aDiagnostics[ 'invalid_entries_in_list'])) and \
                ( not len( aDiagnostics[ 'broken_promise_entries_in_list'])) and \
                ( not      aDiagnostics[ 'linkedlist_size_direction_difference']) and \
                ( not len( aDiagnostics[ 'found_fromOldToNew_moreThanOnce'])) and \
                ( not len( aDiagnostics[ 'found_fromNewToOld_moreThanOnce'])) and \
                ( not len( aDiagnostics[ 'entries_WithNext_NoPrevious'])) and \
                ( not len( aDiagnostics[ 'entries_WithNext_WrongPrevious'])) and \
                ( not len( aDiagnostics[ 'entries_WithoutNext'])) and \
                ( not len( aDiagnostics[ 'entries_WithPrevious_NoNext'])) and \
                ( not len( aDiagnostics[ 'entries_WithPrevious_WrongNext'])) and \
                ( not len( aDiagnostics[ 'entries_WithoutPrevious'])) 
                
            aDiagnostics[ 'success'] = aSuccess
                        
            # ########################
            """Cache-specific verifications completed
            
            """                            
            allCacheEntriesInStructure_AllCaches.update( someCacheEntriesInStructure)
            
            allEntriesWithProblems_AllCaches.update( someEntriesWithProblems)                                    
            
                 
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            
        # ########################
        """Retrieve elements name and type info from the UID catalog and check elements have been found for all entries UIDs
        
        """
        someElementsNamesByUID = {}
        if someUIDsElementsToRetrieve:
            someElementsNamesByUID =  aModelDDvlPloneTool_Retrieval.fElementsNamesByUID( someUIDsElementsToRetrieve, theContextualObject)
            
            for anUID in someUIDsElementsToRetrieve:
                anElementNames = someElementsNamesByUID.get( anUID, None)
                if not anElementNames:
                    allDiagnostics[ 'structures_UIDs_withoutElement'].add( anUID)
                    
               
                    
        
            

                         
        # ########################
        """Check consistency of data in the entries with elements name and type info retrieved from the UID catalog
        
        """
        for aCacheEntry in allCacheEntriesInStructure_AllCaches:
            
            aCacheName = aCacheEntry.vCacheName
            if aCacheName in someCacheNames:
                
                if aCacheEntry.fIsForElement():
                
                    anUID = aCacheEntry.vUID
                    if not anUID:
                        """Must have been already reported when scanning entries in the structures
                        
                        """
                        pass
    
                    else:
                        anElementNames = someElementsNamesByUID.get( anUID, None)
                        if not anElementNames:
                            allDiagnostics[ 'structures_UIDs_withoutElement'].add( anUID)
                            self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'WithoutElement_by_UID',])
                        
                        else:
                            someEntryInconsistenciesWithElement = [ ]   
                            
                            aTitle = anElementNames.get( 'Title', '')
                            if not ( aCacheEntry.vTitle == aTitle):
                                someEntryInconsistenciesWithElement.append( [ 'vTitle',            aCacheEntry.vTitle, aTitle,])
                                
                            aType = anElementNames.get( 'Type', '')
                            if not ( aCacheEntry.vArchetypeName == aType):
                                someEntryInconsistenciesWithElement.append( [ 'vArchetypeName',     aCacheEntry.vArchetypeName, aType,])
                                
                            aPortalType = anElementNames.get( 'portal_type', '')
                            if not ( aCacheEntry.vPortalType == aPortalType):   
                                someEntryInconsistenciesWithElement.append( [ 'vPortalType',        aCacheEntry.vPortalType, aPortalType,])
                                
                            anElementId = anElementNames.get( 'id', '')
                            if not ( aCacheEntry.vElementId == anElementId):   
                                someEntryInconsistenciesWithElement.append( [ 'vElementId',        aCacheEntry.vElementId, anElementId ,])
                                
                            if someEntryInconsistenciesWithElement:
                                allDiagnostics[ 'elementnames_inconsistent_entries'].append( [ aCacheEntry, someEntryInconsistenciesWithElement,])
                                self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'inconsistent_with_element', someEntryInconsistenciesWithElement])
                                            
                        
                        
                

                             
        # ########################
        """Verify that the registry of entries by Unique entry Id does not contain entries for the considered caches, that have not been reached through structure traversal
        
        """
        aCachedEntriesByUniqueId = self._fGetCachedEntriesById_Copy( theModelDDvlPloneTool, theContextualObject,)
        
        someUniqueIds = aCachedEntriesByUniqueId.keys()
        allDiagnostics[ 'uniqueIDs_registry_size'] = len( someUniqueIds)
        
        for aUniqueId in someUniqueIds:
            
            aCacheEntry = aCachedEntriesByUniqueId.get( aUniqueId, None)
            if aCacheEntry:
                
                aCacheName = aCacheEntry.vCacheName
                if aCacheName in someCacheNames:
                    if not ( aCacheEntry in allCacheEntriesInStructure_AllCaches):
                        allDiagnostics[ 'entriesByUniqueId_Not_in_structure'].add( aCacheEntry)
                        self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'EntryInUniqueIdsRegistry_NotInStructure',])
                    
                if not aCacheEntry.vValid:
                    allDiagnostics[ 'invalid_entries_in_UniqueId_registry'].add( aCacheEntry)
                    self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'Invalid',])
                    
                aCacheEntryPromise = aCacheEntry.vPromise
                if not aCacheEntryPromise:
                    allDiagnostics[ 'broken_promise_entries_in_UniqueId_registry'].add( aCacheEntry)
                    self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'BrokenPromise',])
                        
                    
                         
        # ########################
        """Count number of UIDs and number of entries in the UID registry
        
        """
        aCachedEntriesByUID = self._fGetCachedEntriesByUID_Copy( theModelDDvlPloneTool, theContextualObject,)
        
        someUIDs= aCachedEntriesByUID.keys()
        allDiagnostics[ 'UIDs_registry_size'] = len( someUIDs)
        
        aNumEntriesInUIDRegistry = 0
        for aUID in someUIDs:
            aNumEntriesInUIDRegistry += len( aCachedEntriesByUID.get( aUID, []))
        
        allDiagnostics[ 'numentries_in_UIDs_registry'] = aNumEntriesInUIDRegistry
            
        # ########################
        """Only if all caches have been scanned, Verify that the registry of entries by UID does not contain entries for the considered caches, that have not been reached through structure traversal
        
        """
        if ( set( someCacheNames).intersection( set( cCacheNamesForElementsOrUsers))) == set( cCacheNamesForElementsOrUsers):
            for aUID in someUIDs:
                
                someCachedEntries = aCachedEntriesByUID.get( aUID, [])
                for aCacheEntry in someCachedEntries:
                    if aCacheEntry:
                        if not ( aCacheEntry in allCacheEntriesInStructure_AllCaches):
                            allDiagnostics[ 'entriesByUID_Not_in_structure'].add( aCacheEntry)
                            self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'EntryInUIDsRegistry_NotInStructure',])
                            
                        if not aCacheEntry.vValid:
                            allDiagnostics[ 'invalid_entries_in_UID_registry'].add( aCacheEntry)
                            self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'Invalid',])
                            
                        aCacheEntryPromise = aCacheEntry.vPromise
                        if not aCacheEntryPromise:
                            allDiagnostics[ 'broken_promise_entries_in_UID_registry'].add( aCacheEntry)
                            self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'BrokenPromise',])
                            

        aSuccess = True
        for aCacheDiagnostics in allDiagnostics[ 'caches_diagnostics'].values():
            if not aCacheDiagnostics[ 'success']:
                aSuccess = False
                break
            
        aSuccess = aSuccess and ( not len( allDiagnostics[ 'allEntriesWithProblems'])) and \
            ( not len( allDiagnostics[ 'structures_UIDs_withoutElement'])) and \
            ( not len( allDiagnostics[ 'entriesByUniqueId_Not_in_structure'])) and \
            ( not len( allDiagnostics[ 'entriesByUID_Not_in_structure'])) and \
            ( not len( allDiagnostics[ 'elementnames_inconsistent_entries'])) and \
            ( not len( allDiagnostics[ 'invalid_entries_in_UID_registry'])) and \
            ( not len( allDiagnostics[ 'invalid_entries_in_UniqueId_registry'])) and \
            ( not len( allDiagnostics[ 'broken_promise_entries_in_UniqueId_registry'])) and \
            ( not len( allDiagnostics[ 'broken_promise_entries_in_UID_registry'])) 
        
        

        
            
        allDiagnostics[ 'success'] = aSuccess
        
        return allDiagnostics
    
    
    
    
    
    
    security.declarePrivate( '_pAppendEntryDefect')
    def _pAppendEntryDefect(self, theDefectsRegistry, theCacheEntry, theDefect):
     
        if theDefectsRegistry == None:
            return self
        
        if not theCacheEntry:
            return self
        
        if not theDefect:
            return self
        
        someEntryDefects = theDefectsRegistry.get( theCacheEntry, None)
        if someEntryDefects == None:
            someEntryDefects = [ ]
            theDefectsRegistry[ theCacheEntry] = someEntryDefects
            
        someEntryDefects.append( theDefect)
        
        return self
    
    

    