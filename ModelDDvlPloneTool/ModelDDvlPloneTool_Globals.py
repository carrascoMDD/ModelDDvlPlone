# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Globals.py
#
# Copyright (c) 2008, 2009, 2010 by Model Driven Development sl and Antonio Carrasco Valero
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

import sys
import traceback
import logging

import threading

from DateTime import DateTime


from AccessControl import ClassSecurityInfo


from Products.CMFCore import permissions




from ModelDDvlPloneTool_CacheConstants    import *








# ######################################
"""Initial values for globals.

"""


def fgInitial_CacheMutex():
    return threading.Lock()


def fgInitial_CacheStartupTime_Holder():
    return [ DateTime(), ]


def fgInitial_UniqueIdCounter_Holder():
    return [ 0,]


def fgInitial_EntriesByUniqueId():
    return { }


def fgInitial_EntriesByElementUID():
    return { }


def fgInitial_CacheStoreHolders():
    return dict( [ [ aCacheName, fNewCacheStore(      aCacheName, aCacheKind),] for aCacheName, aCacheKind in cCacheNamesAndKindsToCreate])


def fgInitial_CacheStatisticsHolders():
    return dict( [ [ aCacheName, fNewCacheStatistics( aCacheName, aCacheKind),] for aCacheName, aCacheKind in cCacheNamesAndKindsToCreate])
    



def fgInitial_AllCacheGlobals():
    someGlobals = { 
        'gCacheMutex':                             fgInitial_CacheMutex(),
        'gCacheStartupTime_Holder':                fgInitial_CacheStartupTime_Holder(),
        'gCacheStore_UniqueIdCounter_Holder':      fgInitial_UniqueIdCounter_Holder(),
        'gCacheStore_EntriesByUniqueId':           fgInitial_EntriesByUniqueId(),
        'gCacheStore_EntriesByElementUID':         fgInitial_EntriesByElementUID(),
        'gCacheStoreHolders':                      fgInitial_CacheStoreHolders(),
        'gCacheStatisticsHolders':                 fgInitial_CacheStatisticsHolders(),
    }
    return someGlobals
   



def fgInitial_AllGlobals():
    someGlobals = fgInitial_AllCacheGlobals()
    someGlobals = someGlobals.copy()
    return someGlobals
   

    
    



class ModelDDvlPloneTool_Globals:
    """Holds globals on behalf of the other roles, whose classes can therefore be unloaded and reloadad without hassle.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    
    
    
    # #######################################################
    # #######################################################
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """Globals held on behalf of ModelDDvlPloneTool_Cache.
    
    """
    # #######################################################


 
    # #######################################################
    """To enforce Exclusive access to Cache
    
    """
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    gCacheMutex = fgInitial_CacheMutex()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 
    
    
    
    # #######################################################
    """Cache store, indexing, and control globals
    
    """
    gCacheStartupTime_Holder = fgInitial_CacheStartupTime_Holder()
    
    
    

    # #######################################################
    """Unique counter for all entries in all caches. Cached entries Element Independent in all caches Indexed by the Unique Id  of the cache entry.
    
    """
    gCacheStore_UniqueIdCounter_Holder = fgInitial_UniqueIdCounter_Holder()
     
    gCacheStore_EntriesByUniqueId      = fgInitial_EntriesByUniqueId()
    
    
    
    

    # #######################################################
    """Cached entries For Elements in all caches Indexed by the UID of the represented element.
    Used to invalidate entries for elements impacted by change operations, or to invalidate current cache entry, or by request from distributed peers.
    
    """
    gCacheStore_EntriesByElementUID = fgInitial_EntriesByElementUID()
        
  
    
    
    # #######################################################
    """Caches store global. The cache memory storage structure and all Cached pages are rooted here.
    Includes: Cached pages,a list of promised entries in process of resolution, 
    a Counter for unique Cache Entry identifiers.
    and a Dynamic list of active entries ordered by the time they were last accessed, the last at the bottom.
    """
    gCacheStoreHolders = fgInitial_CacheStoreHolders()
        
    
    
    
    # #######################################################
    """Caches statistics global. The statistics for all caches are rooted here.
    Record the date of last flush, and who did the flushing.
    Total of cache entries, and memory used.
    Number of Hits (pages served from cache), and savings.
    Number of Faults (pages not in cache had to be rendered).
    
    """
    gCacheStatisticsHolders = fgInitial_CacheStatisticsHolders()
    

    

    
    def fgGlobalsAccessor(self,):
        someGlobals = { 
            'gCacheMutex':                             ModelDDvlPloneTool_Globals.gCacheMutex,
            'gCacheStartupTime_Holder':                ModelDDvlPloneTool_Globals.gCacheStartupTime_Holder,
            'gCacheStore_UniqueIdCounter_Holder':      ModelDDvlPloneTool_Globals.gCacheStore_UniqueIdCounter_Holder,
            'gCacheStore_EntriesByUniqueId':           ModelDDvlPloneTool_Globals.gCacheStore_EntriesByUniqueId,
            'gCacheStore_EntriesByElementUID':         ModelDDvlPloneTool_Globals.gCacheStore_EntriesByElementUID,
            'gCacheStoreHolders':                      ModelDDvlPloneTool_Globals.gCacheStoreHolders,
            'gCacheStatisticsHolders':                 ModelDDvlPloneTool_Globals.gCacheStatisticsHolders,
        }
        return someGlobals
    
    
    
    
 
    
        
    
    
    def pgGlobalsMutator(self, theGlobals):
        if not theGlobals:
            return self
        
        aSentinel = object()
        
        aNewValue = theGlobals.get( 'gCacheMutex', aSentinel)
        if not ( aNewValue == aSentinel):
            ModelDDvlPloneTool_Globals.gCacheMutex = aNewValue
            
        aNewValue = theGlobals.get( 'gCacheStartupTime_Holder', aSentinel)
        if not ( aNewValue == aSentinel):
            ModelDDvlPloneTool_Globals.gCacheStartupTime_Holder = aNewValue
            
        aNewValue = theGlobals.get( 'gCacheStore_UniqueIdCounter_Holder', aSentinel)
        if not ( aNewValue == aSentinel):
            ModelDDvlPloneTool_Globals.gCacheStore_UniqueIdCounter_Holder = aNewValue
            
        aNewValue = theGlobals.get( 'gCacheStore_EntriesByUniqueId', aSentinel)
        if not ( aNewValue == aSentinel):
            ModelDDvlPloneTool_Globals.gCacheStore_EntriesByUniqueId = aNewValue
            
        aNewValue = theGlobals.get( 'gCacheStore_EntriesByElementUID', aSentinel)
        if not ( aNewValue == aSentinel):
            ModelDDvlPloneTool_Globals.gCacheStore_EntriesByElementUID = aNewValue
            
        aNewValue = theGlobals.get( 'gCacheStoreHolders', aSentinel)
        if not ( aNewValue == aSentinel):
            ModelDDvlPloneTool_Globals.gCacheStoreHolders = aNewValue
            
        aNewValue = theGlobals.get( 'gCacheStatisticsHolders', aSentinel)
        if not ( aNewValue == aSentinel):
            ModelDDvlPloneTool_Globals.gCacheStatisticsHolders = aNewValue
        
        return self
    
    
 
    
    

   

    
    
    
    
    

    # #######################################################
    # #######################################################
    

    # #######################################################
    # #######################################################


    # #######################################################
    # #######################################################

        
    
    # #######################################################
    """Accessors for globals held on behalf of ModelDDvlPloneTool_Cache. Globals also accessed trhough methods in the ModelDDvlPloneTool singleton.
    
    """
    
    def fgCacheMutex(self, ):
        return ModelDDvlPloneTool_Globals.gCacheMutex
       
    
    
    
    def fgCacheStartupTime_Holder(self, ):
        return ModelDDvlPloneTool_Globals.gCacheStartupTime_Holder
    
    
     
    
    def fgCacheStore_UniqueIdCounter_Holder(self, ):
        return ModelDDvlPloneTool_Globals.gCacheStore_UniqueIdCounter_Holder
    
    
        
    
    def fgCacheStore_EntriesByUniqueId(self, ):
        return ModelDDvlPloneTool_Globals.gCacheStore_EntriesByUniqueId
    
    
        
    
    def fgCacheStore_EntriesByElementUID(self, ):
        return ModelDDvlPloneTool_Globals.gCacheStore_EntriesByElementUID
    
   
        
    
    def fgCacheStoreHolders(self, ):
        return ModelDDvlPloneTool_Globals.gCacheStoreHolders
    
        
    
    def fgCacheStatisticsHolders(self, ):
        return ModelDDvlPloneTool_Globals.gCacheStatisticsHolders
    
    
       
    
    # #######################################################
    # #######################################################
    
    
    
    
    
    
    
    
    
    