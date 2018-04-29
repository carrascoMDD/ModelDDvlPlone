# -*- coding: utf-8 -*-
#
# File: MDDTool_Globals.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Model Driven Development sl and Antonio Carrasco Valero
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
import sys
import traceback
import logging


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









# #######################################################
# #######################################################









class MDDTool_Globals:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """

    
    
    security = ClassSecurityInfo()
    
    
    
        
    
    # #######################################################
    """Accessors for globals held by ModelDDvlPloneTool_Globals on behalf of ModelDDvlPloneTool_Cache.
    
    """
    
    security.declarePrivate( 'fgCacheMutex')
    def fgCacheMutex(self, theContextualObject):
        return self.fModelDDvlPloneTool_Globals( theContextualObject).gCacheMutex
          
    
    
    
    security.declarePrivate( 'fgCacheStartupTime_Holder')
    def fgCacheStartupTime_Holder(self, theContextualObject, ):
        return self.fModelDDvlPloneTool_Globals( theContextualObject).gCacheStartupTime_Holder
    
    
     
    
    security.declarePrivate( 'fgCacheStore_UniqueIdCounter_Holder')
    def fgCacheStore_UniqueIdCounter_Holder(self, theContextualObject, ):
        return self.fModelDDvlPloneTool_Globals( theContextualObject).gCacheStore_UniqueIdCounter_Holder
    
    
        
    
    security.declarePrivate( 'fgCacheStore_EntriesByUniqueId')
    def fgCacheStore_EntriesByUniqueId(self, theContextualObject, ):
        return self.fModelDDvlPloneTool_Globals( theContextualObject).gCacheStore_EntriesByUniqueId
    
    
        
    
    security.declarePrivate( 'fgCacheStore_EntriesByElementUID')
    def fgCacheStore_EntriesByElementUID(self, theContextualObject, ):
        return self.fModelDDvlPloneTool_Globals( theContextualObject).gCacheStore_EntriesByElementUID
    
   
        
    
    security.declarePrivate( 'fgCacheStoreHolders')
    def fgCacheStoreHolders(self, theContextualObject, ):
        return self.fModelDDvlPloneTool_Globals( theContextualObject).gCacheStoreHolders
    
        
    
    security.declarePrivate( 'fgCacheStatisticsHolders')
    def fgCacheStatisticsHolders(self, theContextualObject, ):
        return self.fModelDDvlPloneTool_Globals( theContextualObject).gCacheStatisticsHolders
    
        