# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_GenericAccessors.py
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





    
class ModelDDvlPloneTool_Cache_GenericAccessors:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with generic access to cache configuration and control structures.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    

    
    
    

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
      
    
        