# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache.py
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

from urlparse import urlparse

from StringIO import StringIO


from App.config import getConfiguration

from AccessControl import ClassSecurityInfo



from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName


from Products.PlacelessTranslationService.Negotiator import getLangPrefs



from ModelDDvlPloneTool_Cache_Configuration           import ModelDDvlPloneTool_Cache_Configuration
from ModelDDvlPloneTool_Cache_Diagnostics             import ModelDDvlPloneTool_Cache_Diagnostics
from ModelDDvlPloneTool_Cache_Disc                    import ModelDDvlPloneTool_Cache_Disc
from ModelDDvlPloneTool_Cache_EntriesAccess           import ModelDDvlPloneTool_Cache_EntriesAccess
from ModelDDvlPloneTool_Cache_EntriesFlush            import ModelDDvlPloneTool_Cache_EntriesFlush
from ModelDDvlPloneTool_Cache_GenericAccessors        import ModelDDvlPloneTool_Cache_GenericAccessors
from ModelDDvlPloneTool_Cache_Render                  import ModelDDvlPloneTool_Cache_Render
from ModelDDvlPloneTool_Cache_Statistics              import ModelDDvlPloneTool_Cache_Statistics
from ModelDDvlPloneTool_Cache_Status                  import ModelDDvlPloneTool_Cache_Status
from ModelDDvlPloneTool_Cache_VoidResults             import ModelDDvlPloneTool_Cache_VoidResults



from ModelDDvlPloneTool_CacheConstants          import *

from MDDStringConversions                       import *

from MDDLinkedList                              import MDDLinkedList, MDDLinkedNode

from ModelDDvlPloneToolSupport                  import fEvalString, fReprAsString, fMillisecondsNow, fMillisecondsToDateTime, fDateTimeNow








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
# #######################################################

# #######################################################
# #######################################################

# #######################################################
# #######################################################










    
class ModelDDvlPloneTool_Cache( \
    ModelDDvlPloneTool_Cache_Configuration, \
    ModelDDvlPloneTool_Cache_Diagnostics, \
    ModelDDvlPloneTool_Cache_Disc, \
    ModelDDvlPloneTool_Cache_EntriesAccess, \
    ModelDDvlPloneTool_Cache_EntriesFlush, \
    ModelDDvlPloneTool_Cache_GenericAccessors, \
    ModelDDvlPloneTool_Cache_Render, \
    ModelDDvlPloneTool_Cache_Statistics, \
    ModelDDvlPloneTool_Cache_Status, \
    ModelDDvlPloneTool_Cache_VoidResults):
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
    



    
   

    # #######################################################################
    """ Utility to escape strings written as HTML.
    
    """
    def fCGIE( self, theString, quote=1):
        if not theString:
            return theString
        return cgi.escape( theString, quote=quote)
        
        
    
    
 
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
    # #######################################################
    
    # #######################################################
    # #######################################################




    
    
    
    
    def fURLParse( self, theModelDDvlPloneTool, theContextualObject, theURL):
        """Parse the URL in its 6 components
        <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
        Note that we don't break the components up in smaller bits
        (e.g. netloc is a single string) and we don't expand % escapes.
        """
        
        if not theURL:
            return ()
        
        aParsedURL = urlparse( theURL)
        
        return aParsedURL
    
    
    
    


    # #############################################################
    """User Role access methods. Roles are classified into a reduced number of role kinds: Anonymous, Authenticated, Owner, Manager
    
    """

         
    security.declarePrivate( 'fGetMemberRoleKindAndUserId')
    def fGetMemberRoleKindAndUserId(self , theModelDDvlPloneTool, theContextualObject, theTemplateName):
    
        if theModelDDvlPloneTool == None:
            return None
        
        aMembershipTool = getToolByName( theContextualObject, 'portal_membership', None)
        if aMembershipTool == None:
            return None
        
        unMember = aMembershipTool.getAuthenticatedMember()   
        if not unMember:
            return None
        
        aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
        if aModelDDvlPloneTool_Retrieval == None:
            return None
        
        
        unMemberUserName = unMember.getUserName()
        if unMemberUserName == 'Anonymous User':
            return [ cRoleKind_Anonymous, 'Anonymous User', cZopeRole_Anonymous]
        
        unMemberId = unMember.getMemberId()
        
        unElementoGetRoles = theContextualObject

        
        aUserRolesSet = set( aModelDDvlPloneTool_Retrieval.fGetRequestingUserRoles( unElementoGetRoles))
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
    
    
    
            
            
            

            
            

    
    

    