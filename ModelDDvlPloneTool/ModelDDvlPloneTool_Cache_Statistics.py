# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_Statistics.py
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


from ModelDDvlPloneToolSupport                  import fDateTimeNow





# #######################################################
# #######################################################








    
class ModelDDvlPloneTool_Cache_Statistics:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the configuration of cache operation parameters.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    


        
    

            
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
    
        
    
    

        