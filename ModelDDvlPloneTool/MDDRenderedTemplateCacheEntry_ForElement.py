# -*- coding: utf-8 -*-
#
# File: MDDRenderedTemplateCacheEntry_ForElement.py
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


from MDDRenderedTemplateCacheEntry_ElementIndependent import MDDRenderedTemplateCacheEntry_ElementIndependent



# #######################################################
"""Cache entry clases as nodes to be linked in a list ordered by the last time the entry was used.

"""
    
    
     
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
        theRootId       = '', 
        thePath         = '', 
        theRoleKind     ='', 
        theRelation     ='', 
        theSchemeHostAndDomain='', 
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
            theSchemeHostAndDomain=theSchemeHostAndDomain,
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
        self.vRootId     = theRootId
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
    


    
    
    
    
    
    
    
    



