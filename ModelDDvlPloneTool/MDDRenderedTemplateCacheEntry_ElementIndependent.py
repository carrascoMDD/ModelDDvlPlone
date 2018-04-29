# -*- coding: utf-8 -*-
#
# File: MDDRenderedTemplateCacheEntry_ElementIndependent.py
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

from MDDLinkedList                              import MDDLinkedNode






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
        theSchemeHostAndDomain='',
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
        self.vView        = theView
        self.vLanguage    = theLanguage
        self.vSchemeHostAndDomain=theSchemeHostAndDomain
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
        
        self.vFilePath    = ''
        self.vDisplayPath = ''
        
        
        
        
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
        self.vView        = None
        self.vLanguage    = None
        self.vSchemeHostAndDomain=None
        self.vHTML        = None
        self.vMilliseconds= None
        self.vExpireAfterSeconds = None
        self.vForceExpire = None 
        self.vLastHit     = None
        self.vLastUser    = None
        self.vHits        = None
        self.vFilePath    = None
        self.vDisplayPath =None
        
        return self
    
    
    