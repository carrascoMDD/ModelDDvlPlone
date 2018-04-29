# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

import os

import sys
import traceback
import logging

import threading

import transaction

# Zope
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo


from time import time

from DateTime import DateTime

from StringIO import StringIO



# cmf
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName, UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase

#from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService

#from Products.PlacelessTranslationService.Negotiator import Negotiator
from Products.PlacelessTranslationService.Negotiator import getLangPrefs

from Acquisition  import aq_inner, aq_parent


from ModelDDvlPloneTool_Retrieval   import ModelDDvlPloneTool_Retrieval



cInDevelopment  = True


cLogExceptions  = True


cUnsecureCacheFlushAcknowledgedAuthenticationString = 'UnsecureCacheFlushAcknowledgedAuthenticationString'


cMinThresholdCharsToRelease         = 50 * 1000
cMaxCharsCachedForElements_MinValue = cMinThresholdCharsToRelease * 2
cMaxCharsCachedForElements_MaxValue = 1000 * 1000 * 1000


cLockOnceOrTwice_Once   = 'Once'
cLockOnceOrTwice_Twice  = 'Twice'
cLockOnceOrTwice_Vocabulary = [ cLockOnceOrTwice_Once, cLockOnceOrTwice_Twice,]


cDisplayCacheHitInformation_None    = 'None'
cDisplayCacheHitInformation_Top     = 'Top'
cDisplayCacheHitInformation_Bottom  = 'Bottom'
cDisplayCacheHitInformation_Vocabulary = [ cDisplayCacheHitInformation_None, cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]


cMaxCharsCachedForElements_Default  = max( 8 * 1000 * 1000, cMinThresholdCharsToRelease)
cCacheEnabled_Default               = True
cLockOnceOrTwice_Default            = cLockOnceOrTwice_Twice
cDisplayCacheHitInformation_Default = ( cInDevelopment and cDisplayCacheHitInformation_Top) or cDisplayCacheHitInformation_Bottom 






cModelDDvlPloneToolName = 'ModelDDvlPlone_tool'

cDefaultNombreProyecto  = 'a_ModelDDvlPlone_driven_ProjectName'

cMagicReplacementString_UniqueId     = '!!! UNI !!! !!! HERE!!!'
cMagicReplacementString_Len          = '!!! LEN !!! !!! HERE!!!'
cMagicReplacementString_Milliseconds = '!!! MIL !!! !!! HERE!!!'
cMagicReplacementString_Date         = '!!! DAT !!! !!! HERE!!!'
cMagicReplacementString_TimeToRetrieve = '!!! TIME !!! !!! HERE!!!'
 
cMagicReplacementString_CollapsibleSectionTitle = '!!! CST !!! !!! HERE!!!'

cZopeRole_Anonymous     = 'Anonymous'
cZopeRole_Authenticated = 'Authenticated'
cZopeRole_Member        = 'Member'
cZopeRole_Reviewer      = 'Reviewer'
cZopeRole_Owner         = 'Owner'
cZopeRole_Manager       = 'Manager'

cRoleKind_Anonymous     = 'Anonymous'
cRoleKind_Authenticated = 'Authenticated'
cRoleKind_Member        = 'Member'
cRoleKind_Owner         = 'Owner'
cRoleKind_Manager       = 'Manager'


cNoRelationCursorName = '-NoRelationCursorName-'
cNoCurrentElementUID  = '-NoCurrentElementUID-'


cCacheEntry_PromiseFulfilled_Sentinel = object()






class MDDRenderedTemplateCacheEntry_Element:
    
    def __init__( self):
        
        pass
    
        
        
    def fIsForElement( self):
        return False
    
    def fIsSentinel(self, ):
        return False
        
    def fIsSentinel_Old(self, ):
        return False
          
    def fIsSentinel_New(self, ):
        return False
          
        
    
    
class MDDRenderedTemplateCacheEntry_WithPrevious( MDDRenderedTemplateCacheEntry_Element):
    
    def __init__( self):
        
        MDDRenderedTemplateCacheEntry_Element.__init__( self)
        
        self.vPrevious    = None
        

        
        
    
class MDDRenderedTemplateCacheEntry_WithNext( MDDRenderedTemplateCacheEntry_Element):
    
    def __init__( self):
        
        MDDRenderedTemplateCacheEntry_Element.__init__( self)
        
        self.vNext    = None
        

        
        
    
class MDDRenderedTemplateCacheEntry_WithPreviousAndNext( MDDRenderedTemplateCacheEntry_WithPrevious, MDDRenderedTemplateCacheEntry_WithNext):
    
    def __init__( self):
        
        MDDRenderedTemplateCacheEntry_WithPrevious.__init__( self)
        MDDRenderedTemplateCacheEntry_WithNext.__init__( self)
        

        

        

class MDDRenderedTemplateCacheEntry_ListSentinel:
    
    def __init__(self, ):
        
        pass

    def fIsSentinel(self, ):
        return True
        
         
        

class MDDRenderedTemplateCacheEntry_ListSentinel_Old( MDDRenderedTemplateCacheEntry_ListSentinel, MDDRenderedTemplateCacheEntry_WithNext):
    
    def __init__( self, ):
        
        MDDRenderedTemplateCacheEntry_ListSentinel.__init__(  self)
        MDDRenderedTemplateCacheEntry_WithNext.__init__( self)

        
         

    def pLink( theNode):
        """TheNode must not be linked anywhere in the list. Use Unlink first to move.
        
        """
        theNode.vPrevious    = self
        theNode.vNext        = self.vNext
        
        self.vNext.vPrevious = theNode
        self.vNext           = theNode
        
        return self
    
    
    
    def fIsSentinel_Old(self, ):
        return True
          

        
        
class MDDRenderedTemplateCacheEntry_ListSentinel_New( MDDRenderedTemplateCacheEntry_ListSentinel, MDDRenderedTemplateCacheEntry_WithPrevious):
    
    def __init__( self, theOldSentinel):
        
        MDDRenderedTemplateCacheEntry_ListSentinel.__init__( self)
        MDDRenderedTemplateCacheEntry_WithPrevious.__init__( self)

        self.vPrevious       = theOldSentinel
        theOldSentinel.vNext = self
         
 

    
    
    
    def pLink( self, theNode):
        """TheNode must not be linked anywhere in the list. Use Unlink first to move.
        
        """
        theNode.vNext        = self
        theNode.vPrevious    = self.vPrevious
        
        self.vPrevious.vNext = theNode
        self.vPrevious       = theNode
        
        return self
    
       
    
    def fIsSentinel_New(self, ):
        return True
          
              
    
    
    
class MDDRenderedTemplateCacheEntry_Node( MDDRenderedTemplateCacheEntry_WithPreviousAndNext):
        
        
    def __init__( self, theUniqueId=None,):
       
        MDDRenderedTemplateCacheEntry_WithPreviousAndNext.__init__( self)

        self.vUniqueId  = theUniqueId

        
        
        
        
    
    def pUnLink( self, ):

        if  self.vPrevious:
            self.vPrevious.vNext = self.vNext
            
        if self.vNext:
            self.vNext.vPrevious = self.vPrevious
        
        self.vPrevious       = None
        self.vNext           = None
        
        return self
        
    
    
    
    
    

class MDDRenderedTemplateCacheEntry_ElementIndependent( MDDRenderedTemplateCacheEntry_Node):
    
    def __init__( self, 
        theUniqueId     =None,
        theValid        =False, 
        thePromise      =0,
        theUser         ='', 
        theDate         ='', 
        theProject      ='', 
        theView         ='', 
        theLanguage     ='', 
        theHTML         ='', 
        theMilliseconds =0,
        theExpireAfter  =None,):
        
        MDDRenderedTemplateCacheEntry_Node.__init__( self, theUniqueId=theUniqueId)
        
        self.vValid       = theValid
        self.vPromise     = thePromise
        self.vUser        = theUser
        self.vDate        = theDate
        self.vProject     = theProject
        self.vLanguage    = theLanguage
        self.vView        = theView
        self.vHTML        = theHTML
        self.vMilliseconds= theMilliseconds
        self.vExpireAfter = theExpireAfter
        
        self.vLastHit  = theDate
        self.vHits     = 0
        
        

    
    
    
    
    
     
class MDDRenderedTemplateCacheEntry_ForElement( MDDRenderedTemplateCacheEntry_ElementIndependent):
    
    def __init__( self, 
        theUniqueId     =None,
        theValid        =False, 
        thePromise      =0,
        theUser         ='', 
        theDate         ='', 
        theProject      ='', 
        theView         ='', 
        theLanguage     ='', 
        theHTML         ='', 
        theMilliseconds =0, 
        theExpireAfter  =None,
        theUID          ='', 
        theTitle        ='', 
        theURL          ='', 
        thePath         = '', 
        theRoleKind     ='', 
        theRelation     ='', 
        theCurrentUID   =''):
        
        MDDRenderedTemplateCacheEntry_ElementIndependent.__init__( self, 
            theUniqueId     =theUniqueId,
            theValid        =theValid, 
            thePromise      =thePromise,
            theUser         =theUser, 
            theDate         =theDate, 
            theProject      =theProject, 
            theView         =theView, 
            theLanguage     =theLanguage, 
            theHTML         =theHTML, 
            theMilliseconds =theMilliseconds,
            theExpireAfter  =theExpireAfter,
        )
         
        self.vUID        = theUID
        self.vTitle      = theTitle
        self.vURL        = theURL
        self.vPath       = thePath
        self.vRoleKind   = theRoleKind
        self.vRelation   = theRelation
        self.vCurrentUID = theCurrentUID
        

       
        
         
    def fIsForElement( self):
        return True
    
    
    
    
    


class ModelDDvlPloneTool_Cache:
    """Manager for Caching of rendered templates
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    
    # #######################################################
    """Cache and cache control globals
    
    """
    
    gCacheStartupTime                  = DateTime()
    
    gCachedTemplatesElementIndependent  = { }
    gCachedTemplatesForElements         = { }
    
    gTotalCacheEntriesElementIndependent= 0
    gTotalCacheEntriesForElements       = 0
    
    gTotalCharsCachedElementIndependent = 0
    gTotalCharsCachedForElements        = 0
    
    gTotalCacheHitsElementIndependent   = 0
    gTotalCacheHitsForElements          = 0
    gTotalCacheFaultsElementIndependent = 0
    gTotalCacheFaultsForElements        = 0

    gTotalCharsSavedElementIndependent  = 0
    gTotalCharsSavedForElements         = 0
    gTotalTimeSavedElementIndependent   = 0
    gTotalTimeSavedForElements          = 0
    
    gCacheEntriesPromised = [ ]
    
    
    
       
    # #######################################################
    """To locate cache entries to invalidate, and to choose the oldest, least used ones
    
    """
    gCachedEntriesByElementUID          = { }
    

    
    
    # #######################################################
    """Counter for unique Cache Entry identifiers. 
    
    """
    gCacheEntryUniqueIdCounter          = 1  
    
    # ACV 20091118 Unused, but may become useful
    # gCacheEntriesByUniqueId             = { }
    
    
    
    
    # #######################################################
    """Dynamic list of active entries ordered by the time they were last accessed, the last at the bottom
    
    """
    
    gCacheEntriesList_Old_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_Old( )
    gCacheEntriesList_New_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_New( gCacheEntriesList_Old_Sentinel)
    
    
    # #######################################################
    """To enforce Exclusive access to Cache
    
    """
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    gTemplatesCacheMutex = threading.Lock()
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 
    
    
    
    # #######################################################
    """To know who is flushing (in case some authorized user gets funny.
    
    """
    gLastFlushingUser                   = ''      
    gLastFlushDate                      = None
    


    
    # #############################################################
    """Utility to render list.
    
    """
   
    security.declarePrivate( 'fListDump_OLD')
    def fListDump_OLD(self,):
        unSentinel = ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel
        if not unSentinel:
            return '[]'
        
        unStream = StringIO()
        
        unStream.write( "[ 'Old'")
        
        unAlreadyVisited = set()
        unNumIterations  = 0

        unCurrent = unSentinel.vNext
        
        while unCurrent and ( unNumIterations < 10000) :
            
            if ( unCurrent in unAlreadyVisited):
                unStream.write( " , '... ... ...' ]")
                break
            
            unAlreadyVisited.add( unCurrent)
            unNumIterations += 1
            

            if unCurrent.fIsSentinel():
                
                if unCurrent.fIsSentinel_New: 
                    unStream.write( " , 'New' ]")
                
                elif unCurrent.fIsSentinel_Old()(): 
                    unStream.write( " , '!!!Old!!!'")  
                
                else:
                    unStream.write( " , '???Sentinel???'")
                
                break

            unStream.write( " , '%s'" % unCurrent.vUniqueId)
            unCurrent = unCurrent.vNext
    
        unString = unStream.getvalue()
        
        return unString
    
    
    
   
    security.declarePrivate( 'fListDump_NEW')
    def fListDump_NEW(self,):
        unSentinel = ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel
        if not unSentinel:
            return '[]'
        
        unStream = StringIO()
        
        unStream.write( "[ 'New'")
        
        
        unAlreadyVisited = set()
        unNumIterations  = 0
        
        unCurrent = unSentinel.vPrevious
        
        while unCurrent and ( unNumIterations < 10000) :
            
            if ( unCurrent in unAlreadyVisited):
                unStream.write( " , '... ... ...' ]")
                break
            
            unAlreadyVisited.add( unCurrent)
            unNumIterations += 1

            if unCurrent.fIsSentinel():
                
                if unCurrent.fIsSentinel_Old(): 
                    unStream.write( " , 'Old' ]")
                
                elif unCurrent.fIsSentinel_New(): 
                    unStream.write( ", '!!!New!!!'")  
                
                else:
                    unStream.write( ", '???Sentinel???'")
                
                break

            unStream.write( unCurrent.vUniqueId)
            unCurrent = unCurrent.vPrevious
    
        unString = unStream.getvalue()
        
        return unString
    
    
        
    # #############################################################
    """Rendered Templates Retrieval from Caches and Caches management methods.
    
    """

    
    security.declarePrivate( 'fStrGrp')
    def fStrGrp(self, theInteger):
        
        aString = str( theInteger)

        someFragments = [ ]

        while aString:
            aFragment = aString[-3:]
            someFragments.append( aFragment)
            aString = aString[ :-3]
            
        someReversedFragments = someFragments.reverse()
        aGroupedString = '.'.join( someFragments)
        return aGroupedString
    
        
    
    
    
    
        
    
    security.declarePrivate( 'fRetrieveCachedTemplatesStatusReport')
    def fRetrieveCachedTemplatesStatusReport(self, theModelDDvlPloneTool, theContextualObject):
        """Retrieve a report with the status of the templates cache, containing the number of entries, the amount of memory occupied, and statistics of cache hits and faults.
        
        """
        
        unCacheStatusReport = {
            'CanConfigure':                        False,
            'CanFlush':                            False,
            'CanEnableOrDisable':                  False,
            
            'CacheEnabled':                        ( theModelDDvlPloneTool and theModelDDvlPloneTool.vCacheEnabled) or False,
            
            'CacheStartupTime':                    ModelDDvlPloneTool_Cache.gCacheStartupTime,
            'LastFlushingUser':                    ModelDDvlPloneTool_Cache.gLastFlushingUser,
            'LastFlushDate':                       ModelDDvlPloneTool_Cache.gLastFlushDate,
            
            'MaxCharsCachedForElements':           ( theModelDDvlPloneTool and theModelDDvlPloneTool.vMaxCharsCachedForElements) or 0, 
            'LockOnceOrTwice':                     ( theModelDDvlPloneTool and theModelDDvlPloneTool.vLockOnceOrTwice) or cLockOnceOrTwice_Default, 
            'DisplayCacheHitInformation':          ( theModelDDvlPloneTool and theModelDDvlPloneTool.vDisplayCacheHitInformation) or cDisplayCacheHitInformation_Default, 
        
            'TotalCacheEntriesElementIndependent': ModelDDvlPloneTool_Cache.gTotalCacheEntriesElementIndependent,
            'TotalCharsCachedElementIndependent':  ModelDDvlPloneTool_Cache.gTotalCharsCachedElementIndependent,
            'TotalCacheHitsElementIndependent':    ModelDDvlPloneTool_Cache.gTotalCacheHitsElementIndependent,
            'TotalCacheFaultsElementIndependent':  ModelDDvlPloneTool_Cache.gTotalCacheFaultsElementIndependent,
            'TotalCharsSavedElementIndependent':   ModelDDvlPloneTool_Cache.gTotalCharsSavedElementIndependent,
            'TotalTimeSavedElementIndependent':    ModelDDvlPloneTool_Cache.gTotalTimeSavedElementIndependent,

            'TotalCacheEntriesForElements':        ModelDDvlPloneTool_Cache.gTotalCacheEntriesForElements,
            'TotalCharsCachedForElements':         ModelDDvlPloneTool_Cache.gTotalCharsCachedForElements,
            'TotalCacheHitsForElements':           ModelDDvlPloneTool_Cache.gTotalCacheHitsForElements,
            'TotalCacheFaultsForElements':         ModelDDvlPloneTool_Cache.gTotalCacheFaultsForElements,
            'TotalCharsSavedForElements':          ModelDDvlPloneTool_Cache.gTotalCharsSavedForElements,
            'TotalTimeSavedForElements':           ModelDDvlPloneTool_Cache.gTotalTimeSavedForElements,

            'MaxCharsCachedForElements_str':           self.fStrGrp( ( theModelDDvlPloneTool and theModelDDvlPloneTool.vMaxCharsCachedForElements) or 0), 
        
            'TotalCacheEntriesElementIndependent_str': self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCacheEntriesElementIndependent),
            'TotalCharsCachedElementIndependent_str':  self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCharsCachedElementIndependent),
            'TotalCacheHitsElementIndependent_str':    self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCacheHitsElementIndependent),
            'TotalCacheFaultsElementIndependent_str':  self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCacheFaultsElementIndependent),
            'TotalCharsSavedElementIndependent_str':   self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCharsSavedElementIndependent),
            'TotalTimeSavedElementIndependent_str':    self.fStrGrp( int( ModelDDvlPloneTool_Cache.gTotalTimeSavedElementIndependent) / 1000),

            'TotalCacheEntriesForElements_str':        self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCacheEntriesForElements),
            'TotalCharsCachedForElements_str':         self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCharsCachedForElements),
            'TotalCacheHitsForElements_str':           self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCacheHitsForElements),
            'TotalCacheFaultsForElements_str':         self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCacheFaultsForElements),
            'TotalCharsSavedForElements_str':          self.fStrGrp( ModelDDvlPloneTool_Cache.gTotalCharsSavedForElements),
            'TotalTimeSavedForElements_str':           self.fStrGrp( int( ModelDDvlPloneTool_Cache.gTotalTimeSavedForElements) / 1000),        
        }
        
        
        
        if theContextualObject == None:
            return unCacheStatusReport
        
        unElementoRaiz = None
        try:
            unElementoRaiz = theContextualObject.getRaiz()
        except:
            None
        if unElementoRaiz == None:
            return unCacheStatusReport
            
        unPortalObject = ModelDDvlPloneTool_Retrieval().fPortalRoot( theContextualObject)
        if unPortalObject == None:
            return unCacheStatusReport
        
        unHasManagePortalPermission = ModelDDvlPloneTool_Retrieval().fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
        unHasManagerRole            = ModelDDvlPloneTool_Retrieval().fRoleQuery_IsAnyRol( 'Manager', unPortalObject, )
              
        unCanConfigure = unHasManagePortalPermission or unHasManagerRole
        
        unCacheStatusReport.update( {
            'CanConfigure':                        unCanConfigure,
            'CanFlush':                            unCanConfigure,
            'CanEnableOrDisable':                  unCanConfigure,
        })
                        
        
        return unCacheStatusReport
    


    
    
    
    
    security.declarePrivate( 'fConfigureTemplatesCache')
    def fConfigureTemplatesCache(self, theModelDDvlPloneTool, theContextualObject, theTemplateCacheParameters):
        """Initiated by a User with ManagePortal persmission, Set parameters controlling the maximum amount of memory available to store cached templates, and other controls on the behavior of the cache.
        
        """
        if theContextualObject == None:
            return False
        
        if theModelDDvlPloneTool == None:
            return False
        
        if not theTemplateCacheParameters:
            return False
        
        unSentinel = object()
        
        unAnyParameterChanged = False
        

        # ###########################################################
        """Change cache configuration parameters, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX  LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if theTemplateCacheParameters.has_key( 'theMaxCharsCachedForElements'):
                unParameterValueString = theTemplateCacheParameters.get( 'theMaxCharsCachedForElements', unSentinel)
                if not ( unParameterValueString == unSentinel):
                    unParameterValue = unSentinel
                    try:
                        unParameterValue = int( unParameterValueString)
                    except:
                        None
                    if not ( unParameterValue == unSentinel):
                        if ( unParameterValue >= cMaxCharsCachedForElements_MinValue) and ( unParameterValue <= cMaxCharsCachedForElements_MaxValue):
                            theModelDDvlPloneTool.vMaxCharsCachedForElements = unParameterValue
                            unAnyParameterChanged = True
            
                            
                            
            # ACV 20091118 As it works perfectly under load Lockin Twice, and is a parameter that it may not appear immediately clear to administrators, the parameter is left fixed in the configuration initialization upon instantiation of the ModelDDvlPlone_tool.
            if False and theTemplateCacheParameters.has_key( 'theLockOnceOrTwice'):
                unParameterValueString = theTemplateCacheParameters.get( 'theLockOnceOrTwice', unSentinel)
                if not ( unParameterValueString == unSentinel):
                    if unParameterValueString in cLockOnceOrTwice_Vocabulary:
                        theModelDDvlPloneTool.vLockOnceOrTwice = unParameterValueString
                        unAnyParameterChanged = True
            
                        
                        
            if theTemplateCacheParameters.has_key( 'theDisplayCacheHitInformation'):
                unParameterValueString = theTemplateCacheParameters.get( 'theDisplayCacheHitInformation', unSentinel)
                if not ( unParameterValueString == unSentinel):
                    if unParameterValueString in cDisplayCacheHitInformation_Vocabulary:
                        theModelDDvlPloneTool.vDisplayCacheHitInformation = unParameterValueString
                        unAnyParameterChanged = True

            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        if unAnyParameterChanged:
            transaction.commit()
                    
        return unAnyParameterChanged
    
    
    
        
    
    security.declarePrivate( 'fEnableTemplatesCache')
    def fEnableTemplatesCache(self, theModelDDvlPloneTool, theContextualObject):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
        if theContextualObject == None:
            return False
        
        if theModelDDvlPloneTool == None:
            return False

        # ###########################################################
        """Enable caching of template redering result, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX  LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            theModelDDvlPloneTool.vCacheEnabled = True
                 
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return True
        

         
    
    
    
   
        
    
    security.declarePrivate( 'fDisableTemplatesCache')
    def fDisableTemplatesCache(self, theModelDDvlPloneTool, theContextualObject):
        """Do not Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
        if theContextualObject == None:
            return False
        
        if theModelDDvlPloneTool == None:
            return False

        # ###########################################################
        """Disable caching of template redering result, from within a thread-safe protected critical section.
        
        """
        try:
            
            # #################
            """MUTEX  LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            theModelDDvlPloneTool.vCacheEnabled = False
                 
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return True
        

            
    
        
        
    security.declarePrivate( 'fFlushCachedTemplates')
    def fFlushCachedTemplates(self, theModelDDvlPloneTool, theContextualObject):
        """Initiated by a User with ManagePortal persmission, Remove all cached rendered templates, recording who and when requested the flush.
        
        """
        if theModelDDvlPloneTool == None:
            return False
        
        if theContextualObject == None:
            return False
        

        unMemberId    = ModelDDvlPloneTool_Retrieval().fGetMemberId(  theContextualObject)
        unFlushDate   = DateTime()
     
        # ###########################################################
        """Remove all existing cached teimplates, from within a thread-safe protected critical section.
        
        """

        try:
            
            # #################
            """MUTEX  LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            ModelDDvlPloneTool_Cache.gCachedTemplatesElementIndependent = { }
            ModelDDvlPloneTool_Cache.gTotalCacheEntriesElementIndependent= 0
            ModelDDvlPloneTool_Cache.gTotalCharsCachedElementIndependent = 0

            
            ModelDDvlPloneTool_Cache.gCachedTemplatesForElements         = { }    
            ModelDDvlPloneTool_Cache.gTotalCacheEntriesForElements       = 0
            ModelDDvlPloneTool_Cache.gTotalCharsCachedForElements        = 0
            
            
            ModelDDvlPloneTool_Cache.gTotalCacheHitsElementIndependent    = 0
            ModelDDvlPloneTool_Cache.gTotalCacheFaultsElementIndependent  = 0
            ModelDDvlPloneTool_Cache.gTotalCharsSavedElementIndependent   = 0
            ModelDDvlPloneTool_Cache.gTotalTimeSavedElementIndependent    = 0

            ModelDDvlPloneTool_Cache.gTotalCacheHitsForElements           = 0
            ModelDDvlPloneTool_Cache.gTotalCacheFaultsForElements         = 0
            ModelDDvlPloneTool_Cache.gTotalCharsSavedForElements          = 0
            ModelDDvlPloneTool_Cache.gTotalTimeSavedForElements           = 0

            
            ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID        = { }
            
            ModelDDvlPloneTool_Cache.gLastFlushingUser = unMemberId
            ModelDDvlPloneTool_Cache.gLastFlushDate    = unFlushDate
            
            
            unCurrent = ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel.vNext
            
            ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel.vNext     = None
            ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel.vPrevious = None
            
            while unCurrent and ( not unCurrent.fIsSentinel()):
                
                unNext     = unCurrent.vNext
                unToDelete = unCurrent
                unCurrent = unNext
                    
                del unToDelete
                
            del ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel
            del ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel
                
            ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_Old( )
            ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_New( ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel)
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return True
        

     
          
    security.declareProtected( permissions.ManagePortal, 'fInvalidateCachedTemplatesForElements')
    def fInvalidateCachedTemplatesForElements( theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs, theAuthenticationString):
        """Invoked from service exposed to receive notifications from other ZEO clients authenticated with the supplied string, to flush cache entries for elements of the specified Ids.
        
        """
        if theModelDDvlPloneTool == None:
            return str( False)
        
        if theContextualObject == None:
            return str( False)
        
        if not theFlushedElementsUIDs:
            return str( False)
        
        if not theAuthenticationString:
            return str( False)
        
        if not theModelDDvlPloneTool.vCacheEnabled:
            return str( False)
        
        
        anAcknowledgedAuthenticationString = theModelDDvlPloneTool.fCacheFlushAcknowledgedAuthenticationString()
        if not anAcknowledgedAuthenticationString:
            return str( False)
        
        if not ( theAuthenticationString == anAcknowledgedAuthenticationString):
            return str( False)
        
        
        someUIDs = theFlushedElementsUIDs
        if not ( isinstance( someUIDs, list) or isinstance( someUIDs, tuple)):
            someUIDs = [ someUIDs, ]
            
    
        self.pFlushCachedTemplatesForElements( theModelDDvlPloneTool, theContextualObject, someUIDs)
        
            
        return str( True)
        
    
    
    
    
    security.declarePrivate( 'pSendNotification_FlushCachedTemplatesForElements')
    def pSendNotification_FlushCachedTemplatesForElements(self, theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs):
        """Try to send notification to flush the elements to all other client ZOPEs hitting the same ZODB server.
        
        """
        pass
    
    
        
    
    security.declarePrivate( 'pFlushCachedTemplatesForElements')
    def pFlushCachedTemplatesForElements(self, theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs):
        """Invoked by the public tool singleton, may be initiated by the element intercepting side-effect of drag&drop reorder, or by receivin an external notification sent from other instance with the method above after verifying the originator: After modification of an elements values, contained elements or relations, Remove the cached rendered templates for the elements with specified UIDs.
        
        """
        if theModelDDvlPloneTool == None:
            return self
        
        if not theFlushedElementsUIDs:
            return self
        
        
        # ###########################################################
        """Try to send notification to flush the elements to all other client ZOPEs hitting the same ZODB server.
        
        """
        self.pSendNotification_FlushCachedTemplatesForElements( theModelDDvlPloneTool, theContextualObject, theFlushedElementsUIDs)
        
        
        # ###########################################################
        """Try to flush cached content, from within a thread-safe protected critical section.
        
        """

        try:
            # #################
            """MUTEX  LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if not ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID:
                return self
        
            unTotalCacheEntriesFlushed = 0
            unTotalCharsFlushed        = 0
            unosObjectsToDelete        = [ ]
            
            for aFlushedElementUID in theFlushedElementsUIDs:
                
                unasCachedEntriesForElementUID =  ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID.get( aFlushedElementUID, [])
                
                if unasCachedEntriesForElementUID:
                    
                    self.pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, unasCachedEntriesForElementUID)
                                
                    ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID.pop( aFlushedElementUID)                               
                                                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        return self
        

    
        
        
    
    
    
    security.declarePrivate( 'pFlushCacheEntries')
    def pFlushCacheEntries(self, theModelDDvlPloneTool, theContextualObject, theCacheEntriesToFlush):
        """Invoked from this class, within a CRITICAL SECTION To release memory before caching more templates, or after modification of an elements values, contained elements or relations, Remove the cached rendered templates for the elements with specified UIDs.
        
        """
        
        if theModelDDvlPloneTool == None:
            return self
        

        if not theCacheEntriesToFlush:
            return self
        
        
        # ###########################################################
        """Release cache entries. This shall be invoked from within a thread-safe protected critical section.
        
        """
            
        
        unTotalCacheEntriesFlushed = 0
        unTotalCharsFlushed        = 0
        unosObjectsToDelete        = [ ]
        
        for unaCacheEntryToFlush in theCacheEntriesToFlush:

            if not unaCacheEntryToFlush.fIsForElement():
                continue
            
            if not unaCacheEntryToFlush.vValid:
                continue
            
            aProjectName = unaCacheEntryToFlush.vProject
            aLanguage    = unaCacheEntryToFlush.vLanguage
            anElementUID = unaCacheEntryToFlush.vUID
            aViewName    = unaCacheEntryToFlush.vView
            aRelationName= unaCacheEntryToFlush.vRelation 
            aCurrentUID  = unaCacheEntryToFlush.vCurrentUID
            aRoleKind    = unaCacheEntryToFlush.vRoleKind
            
            if not ( aProjectName and aLanguage and anElementUID and aViewName and aRelationName and aCurrentUID and aRoleKind):
                continue
                
            if ModelDDvlPloneTool_Cache.gCachedTemplatesForElements:
                
                someCachedTemplatesForProject = ModelDDvlPloneTool_Cache.gCachedTemplatesForElements.get( aProjectName, None)
                if someCachedTemplatesForProject:
                
                
                    someCachedTemplateForLanguage = someCachedTemplatesForProject.get( aLanguage, None)
                    if someCachedTemplateForLanguage:
                            
                        someCachedTemplatesForElement = someCachedTemplateForLanguage.get( anElementUID, None)
                        if someCachedTemplatesForElement:
                            
                            for aScannedViewName in someCachedTemplatesForElement.keys()[:]:
                                
                                someScannedCachedTemplatesForView = someCachedTemplatesForElement.get( aScannedViewName, None)

                                for aScannedRelationName in someScannedCachedTemplatesForView.keys()[:]:
                                
                                    someScannedCachedTemplateForRelationCursor = someScannedCachedTemplatesForView.get( aScannedRelationName, None)
                                
                                    for aScannedCurrentUID in someScannedCachedTemplateForRelationCursor.keys()[:]:
                                    
                                        someScannedCachedTemplateForCurrentUID = someScannedCachedTemplateForRelationCursor.get( aScannedCurrentUID, None)
                                    
                                        for aScannedRoleKind in someScannedCachedTemplateForCurrentUID.keys()[:]:
                                            
                                            unaScannedCacheEntry = someScannedCachedTemplateForCurrentUID.get( aScannedRoleKind, None)
                                            
                                            if unaScannedCacheEntry and ( unaScannedCacheEntry == unaCacheEntryToFlush):
                                                                                                        
                                                if unaScannedCacheEntry.vValid:
                                                                                                                        
                                                    if ( not unaScannedCacheEntry.vPromise) or ( unaScannedCacheEntry.vPromise and ( unaScannedCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel)):
                                                        
                                                        someScannedCachedTemplateForCurrentUID.pop( aScannedRoleKind)
                                                        
                                                        unaScannedCacheEntry.vValid = False
                                                    
                                                        unTotalCacheEntriesFlushed += 1
                                                        
                                                        unaCachedTemplate = unaScannedCacheEntry.vHTML
                                                        if unaCachedTemplate:
                                                            unTotalCharsFlushed += len( unaCachedTemplate)
                                                                                                        
                                                        # ###########################################################
                                                        """Remove from registry by element UID.
                                                        
                                                        """
                                                        unasCachedEntriesForElementUID = ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID.get( anElementUID, [])
                                                        if unasCachedEntriesForElementUID:   # ACV 20091117 Better just to try and catch. Removed.  ( unaCacheEntryToFlush in unasCachedEntriesForElementUID):
                                                            try:
                                                                unasCachedEntriesForElementUID.remove( unaCacheEntryToFlush)
                                                            except:
                                                                None
                                                                
                                                        # ###########################################################
                                                        """Remove from registry by element UID.
                                                        
                                                        """
                                                        unasCachedEntriesForElementUID = ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID.get( anElementUID, [])
                                                        if unasCachedEntriesForElementUID:   # ACV 20091117 Better just to try and catch. Removed.  ( unaCacheEntryToFlush in unasCachedEntriesForElementUID):
                                                            try:
                                                                unasCachedEntriesForElementUID.remove( unaCacheEntryToFlush)
                                                            except:
                                                                None
                                                            
                                                                
                                                        # ###########################################################
                                                        """Just in case it is hold there, Try to remove from list of promised cache entries pending to accumulate totals of its size and time.
                                                        
                                                        """
                                                        try:
                                                            gCacheEntriesPromised.remove( unaCacheEntryToFlush)
                                                        except:
                                                            None
                                                        
                                                        
                                                        
                                                        # ###########################################################
                                                        """Remove from list of cache entries ordered by last time accessed.
                                                        
                                                        """
                                                        unaCacheEntryToFlush.pUnLink()
                                                           
                                                        
                                                        # ###########################################################
                                                        """Shall be destroyed at the end, along with intermediate dictionaries that ae left empty.
                                                        
                                                        """
                                                        unosObjectsToDelete.append( unaScannedCacheEntry)


                                        someScannedCachedTemplateForRelationCursor.pop( aScannedCurrentUID)
                                        unosObjectsToDelete.append( someScannedCachedTemplateForCurrentUID)

                                    someScannedCachedTemplatesForView.pop( aScannedRelationName)
                                    unosObjectsToDelete.append( someScannedCachedTemplateForRelationCursor)
                                        
                                someCachedTemplatesForElement.pop( aScannedViewName)
                                unosObjectsToDelete.append( someScannedCachedTemplatesForView)
        
                            if not someCachedTemplatesForElement:
                                someCachedTemplateForLanguage.pop( anElementUID)
                                unosObjectsToDelete.append( someCachedTemplatesForElement)
            
                        if not someCachedTemplateForLanguage:
                            someCachedTemplatesForProject.pop( aLanguage)
                            unosObjectsToDelete.append( someCachedTemplateForLanguage)
                                
                    if not someCachedTemplatesForProject:
                        ModelDDvlPloneTool_Cache.gCachedTemplatesForElements.pop( aProjectName)
                        
                        
                                                        
                    
            
                    
        # ###########################################################
        """Decrease total of number of entries and memory used.
        
        """
        ModelDDvlPloneTool_Cache.gTotalCacheEntriesForElements -= unTotalCacheEntriesFlushed

        ModelDDvlPloneTool_Cache.gTotalCharsCachedForElements  -= unTotalCharsFlushed
        
        del unosObjectsToDelete
            
        return self
        

    
        
      
    
    
    
    
    
    
    # ###################################################################
    """Cache entries NOT associated with any specific element. TWO CRITICAL SECTIONS. 
    
    """

    
  
    
    
    
    security.declarePrivate( 'fRenderTemplateOrCachedForProjectInLanguage')
    def fRenderTemplateOrCachedForProjectInLanguage(self, theModelDDvlPloneTool, theContextualObject, theTemplateName):
        """Retrieve a previously rendered template for a project, independent of the here element, for the currently negotiared language and return the rendered HTML.
        
        """
        if theModelDDvlPloneTool == None:
            return ModelDDvlPloneTool().fRenderTemplate( theContextualObject, theTemplateName)
        
        if not theModelDDvlPloneTool.vCacheEnabled:
            return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
        
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
            return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
        
        aNegotiatedLanguage = unosPreferredLanguages[ 0]   
        if not aNegotiatedLanguage:
            return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
        

        aViewName = theTemplateName
        if not aViewName:
            return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
        
        if aViewName.find( '%s') >= 0:
            if not ( aProjectName == cDefaultNombreProyecto):
                aViewName = aViewName % aProjectName
            else:
                aViewName = aViewName.replace( '%s', '')
                
         
        
        unCachedTemplate = u''
        
        
        # ###########################################################
        """MUTEX. Try to retrieve cached content.
        
        """
        try:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
            unCacheEntry = self.fCacheEntryForProjectInLanguage( aProjectName, aNegotiatedLanguage, aViewName, )
            
            if unCacheEntry and unCacheEntry.vValid:
                    
                unCachedTemplate = unCacheEntry.vHTML 
                if unCachedTemplate: 
                    
                    # ###########################################################
                    """Found cached template: Update cache hit statistics, and return the cached HTML
                    
                    """
                    ModelDDvlPloneTool_Cache.gTotalCacheHitsElementIndependent  += 1
                    
                    ModelDDvlPloneTool_Cache.gTotalCharsSavedElementIndependent += len( unCacheEntry.vHTML)
                    ModelDDvlPloneTool_Cache.gTotalTimeSavedElementIndependent  += max( unCacheEntry.vMilliseconds, 0)
                    
                    # ###########################################################
                    """Renew the age of the cache entry in the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                    See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                    
                    """
                    
                    if ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel) or ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel):
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_Old( )
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_New( gCacheEntriesList_Old_Sentinel)
                    
                    unCacheEntry.pUnLink()
                    
                    ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel.pLink( unCacheEntry) 
                 
                    return unCachedTemplate
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            
            
            
            
            
        # ###########################################################
        """Prepare as much as possible before the thread-safe section below.
            
        """

        unMemberId = ModelDDvlPloneTool_Retrieval().fGetMemberId(       theContextualObject)
        
        aCacheEntryValuesDict = {
            'ModelDDvlPlone_Cached':         theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Cached', 'Cached-'), 
            'ModelDDvlPlone_Time_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Time_label', 'Date-'), 
            'ModelDDvlPlone_Len_label':      theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Len_label', 'Len-'), 
            'ModelDDvlPlone_User_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_User_label', 'User-'), 
            'ModelDDvlPlone_Date_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Date_label', 'Date-'), 
            'ModelDDvlPlone_Project_label':  theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Project_label', 'Project-'), 
            'ModelDDvlPlone_Language_label': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Language_label', 'Language-'), 
            'aNegotiatedLanguage':           aNegotiatedLanguage,
            'ModelDDvlPlone_View_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_View_label', 'View-'), 
            'cMagicReplacementString_Milliseconds': cMagicReplacementString_Milliseconds,
            'cMagicReplacementString_Len':   cMagicReplacementString_Len,
            'cMagicReplacementString_Date':  cMagicReplacementString_Date,
            'cMagicReplacementString_UniqueId': cMagicReplacementString_UniqueId,
            'unMemberId':                    unMemberId,
            'aProjectName':                  aProjectName,
            'aViewName':                     aViewName,

            
        }                    
            
        
        
        
        
        # ###########################################################
        """Render a caching information collapsible section to append to the rendered template HTML.
            
        """
        unRenderedCacheInfo = """
            <br/>
            <!-- ######### Start collapsible  section ######### --> 
            <dl id="cid_MDDCachedElementView" class="collapsible inline collapsedInlineCollapsible" >
                <dt class="collapsibleHeader">
                    <span>%(ModelDDvlPlone_Cached)s</span>                        
                </dt>
                <dd class="collapsibleContent">
                    <br/>
                    <table class="listing">
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
                            <tr class="even">
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

        
                    
             
            
            
        # ###########################################################
        """Render template, as it was not found in cache.
        
        """
        unDateBeforeRender = DateTime()
        
        unRenderedTemplate = theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
        
        unDateAfterRender = DateTime()
        
        
        unRenderedTemplateToReturn      = unRenderedTemplate
        unRenderedTemplateWithCacheInfo = unRenderedTemplate
        
        
        
        
        
        # ###########################################################
        """Critical section, with the thread-safe, mutex protected code where the cache support structure is updated.        
        
        """
        try:
            # #################
            """MUTEX  LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
            
            # ###########################################################
            """Try to retrieve cached content again, just in case some other request rendered and cached it while this was doing it in the sentence before.
            
            """
            unCacheEntry = self.fCacheEntryForProjectInLanguage( aProjectName, aNegotiatedLanguage, aViewName, )
            
            if unCacheEntry and unCacheEntry.vValid:
                    
                unCachedTemplate = unCacheEntry.vHTML 
                if unCachedTemplate: 
                    
                    # ###########################################################
                    """Found cached template: Update cache hit statistics, and return the cached HTML
                    
                    """
                    ModelDDvlPloneTool_Cache.gTotalCacheHitsElementIndependent  += 1
                    
                    ModelDDvlPloneTool_Cache.gTotalCharsSavedElementIndependent += len( unCacheEntry.vHTML)
                    ModelDDvlPloneTool_Cache.gTotalTimeSavedElementIndependent  += max( unCacheEntry.vMilliseconds, 0)
                    
                    # ###########################################################
                    """Renew the age of the cache entry in the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                    See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                    
                    """
                    
                    if ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel) or ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel):
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_Old( )
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_New( gCacheEntriesList_Old_Sentinel)
                    
                    unCacheEntry.pUnLink()
                    
                    ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel.pLink( unCacheEntry) 
                 
                    return unCachedTemplate
           
            
            
            # ###########################################################
            """Allocate a new unique id for the new cache entry to create, 
            
            """
            if not ModelDDvlPloneTool_Cache.gCacheEntryUniqueIdCounter:
                ModelDDvlPloneTool_Cache.gCacheEntryUniqueIdCounter = 1
                
            ModelDDvlPloneTool_Cache.gCacheEntryUniqueIdCounter += 1  
                    
            unCacheEntryUniqueId = ModelDDvlPloneTool_Cache.gCacheEntryUniqueIdCounter
            
                
                
            # ###########################################################
            """Append a caching information collapsible section to the rendered template HTML.
            
            """
            unosMilliseconds = unDateAfterRender.millis() - unDateBeforeRender.millis()
            unHTMLLen        = len( unRenderedTemplateToReturn)
            
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_UniqueId,     str( unCacheEntryUniqueId))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Milliseconds, str( unosMilliseconds))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Len,          str( unHTMLLen))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Date,         unDateAfterRender.rfc822())
                 
            unRenderedTemplateWithCacheInfo = "%s\n<br/>%s" % ( unRenderedTemplate, unRenderedCacheInfo,)
            
            
            
            
            # ###########################################################
            """Cache just rendered template and Update cache structures.
            
            """
            if not ModelDDvlPloneTool_Cache.gCachedTemplatesElementIndependent:
                ModelDDvlPloneTool_Cache.gCachedTemplatesElementIndependent = { }
                
            someCachedTemplatesForProject = ModelDDvlPloneTool_Cache.gCachedTemplatesElementIndependent.get( aProjectName, {})
            if not someCachedTemplatesForProject:
                someCachedTemplatesForProject = { }
                ModelDDvlPloneTool_Cache.gCachedTemplatesElementIndependent[ aProjectName] = someCachedTemplatesForProject
                
            someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aNegotiatedLanguage, {})
            if not someCachedTemplatesForLanguage:
                someCachedTemplatesForLanguage = { }
                someCachedTemplatesForProject[ aNegotiatedLanguage] = someCachedTemplatesForLanguage

            unDateAfterRender = DateTime()
            
                           
            aCacheEntry = MDDRenderedTemplateCacheEntry_ElementIndependent(
                theUniqueId          =unCacheEntryUniqueId,
                theValid             =True,
                thePromise           =0,
                theUser              =unMemberId,
                theDate              =unDateAfterRender,
                theProject           =aProjectName,
                theView              =aViewName,
                theLanguage          =aNegotiatedLanguage,
                theHTML              =unRenderedTemplateWithCacheInfo,
                theMilliseconds      =unosMilliseconds,
                theExpireAfter       =None,
            )
            

            someCachedTemplatesForLanguage[ aViewName] = aCacheEntry
            
            # ###########################################################
            """Update cache statistics.
            
            """
            ModelDDvlPloneTool_Cache.gTotalCacheEntriesElementIndependent += 1
            
            ModelDDvlPloneTool_Cache.gTotalCacheFaultsElementIndependent  += 1
            
            ModelDDvlPloneTool_Cache.gTotalCharsCachedElementIndependent  += len( unRenderedTemplateWithCacheInfo)
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
        
        unRenderedTemplateToReturn = unRenderedTemplateWithCacheInfo.replace(    
            '<span>%(ModelDDvlPlone_Cached)s' % aCacheEntryValuesDict,
            '<span>%s' % theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_JustRendered', 'Just Rendered-'),
        )   
        
        return unRenderedTemplateToReturn
    
    
    



    
    security.declarePrivate( 'fCacheEntryForProjectInLanguage')
    def fCacheEntryForProjectInLanguage( self, theProjectName='', theLanguage='',  theViewName='', ):
    
        if ( not theProjectName) or ( not theLanguage) or ( not theViewName):
            return None
            
        if not ModelDDvlPloneTool_Cache.gCachedTemplatesElementIndependent:
            return None
            
        someCachedTemplatesForProject = ModelDDvlPloneTool_Cache.gCachedTemplatesElementIndependent.get( theProjectName, {})
        if not someCachedTemplatesForProject:
            return None
            
        someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( theLanguage, {})
        if not someCachedTemplatesForLanguage:
            return None
            
        aCachedEntryForView = someCachedTemplatesForLanguage.get( theViewName, {})
        if not aCachedEntryForView:
            return None
            
        unCachedTemplate = aCachedEntryForView.vHTML
        if not unCachedTemplate:
            return None
            
        return aCachedEntryForView    

    
    
    
    
    

    
    # ###################################################################
    """ONLY ONE CRITICAL SECTION. Cache entries associated with specific elements.
    
    """

       
    security.declarePrivate( 'fRenderTemplateOrCachedForElementInLanguage')
    def fRenderTemplateOrCachedForElementInLanguage(self, theModelDDvlPloneTool, theContextualObject, theTemplateName):
        """ Return theHTML, from cache or just rendered, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
    
        if theModelDDvlPloneTool == None:
            return ModelDDvlPloneTool().fRenderTemplate( theContextualObject, theTemplateName)
        
        if not theModelDDvlPloneTool.vCacheEnabled:
            return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
        
        if theContextualObject == None:
            return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
        
        
        aBeginTime = int( time() * 1000)
        try:
                
            # ###########################################################
            """Only cache objects that allow caching.
            
            """
            anIsCacheable = False
            try:
                anIsCacheable = theContextualObject.fIsCacheable()
            except:
                None
            if not anIsCacheable:    
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
            
            
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
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
            aNegotiatedLanguage = unosPreferredLanguages[ 0]   
            if not aNegotiatedLanguage:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
            
            
            unElementUID = theContextualObject.UID()
            if not unElementUID:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
                   
            unElementTitle = theContextualObject.Title()
            if not unElementTitle:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
    
            unElementURL   = theContextualObject.absolute_url()
            if not unElementURL:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
               
            unElementPath = '/'.join( theContextualObject.getPhysicalPath())
            if not unElementPath:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
    
            
                    
            aViewName = theTemplateName
            if not aViewName:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            if aViewName.find( '%s') >= 0:
                if not ( aProjectName == cDefaultNombreProyecto):
                    aViewName = aViewName % aProjectName
                else:
                    aViewName = aViewName.replace( '%s', '')
            if not aViewName:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
                    
            unMemberId = ModelDDvlPloneTool_Retrieval().fGetMemberId(  theContextualObject)
            if not unMemberId:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
            
            
            unRoleKind = self.fGetMemberRoleKind( theContextualObject, theTemplateName)
            if not unRoleKind:
                return theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
            
            
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
                
                        
                        
                        
                
            unExistingOrPromiseCacheEntry = None
            unCachedTemplate              = None
            unPromiseMade                 = None                      
            
            anActionToDo                  = None
            somePossibleActions           = [ 'UseFoundEntry', 'MakePromise', 'JustFallbackToRenderNow', ] # Just to document the options handled by logic below
            
            # ###################################################################
            """CRITICAL SECTION to access and modify cache control structure, for Cache entries associated with specific elements.
            
            """
            try:
                # #################
                """MUTEX  LOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                    
                
                
                
                # ###########################################################
                """MEMORY consumed maintenance: Accumulate into the chars used total the length of the HTML of promissed cache entries that have been fulfilled lately, bud did not update totals because no critical section was permitted after rendering (ONE SYNCH MODE).
                
                """
                
                if ModelDDvlPloneTool_Cache.gCacheEntriesPromised:
                    unasCacheEntriesRemainingToFullfill = [ ]
                    for unPromisedCacheEntry in ModelDDvlPloneTool_Cache.gCacheEntriesPromised:
                        
                        if not unPromisedCacheEntry.vValid:
                            continue
                        
                        if not( unPromisedCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel):
                            unasCacheEntriesRemainingToFullfill.append( unPromisedCacheEntry)
                            continue
                            
                        unCachedTemplate = unPromisedCacheEntry.vHTML
                        if unCachedTemplate:
                            ModelDDvlPloneTool_Cache.gTotalCharsCachedForElements += len( unCachedTemplate)
                                
                    ModelDDvlPloneTool_Cache.gCacheEntriesPromised = unasCacheEntriesRemainingToFullfill
                    
                   
                
                # ###########################################################
                """MEMORY consumed maintenance: Release memory if exceed maximum configured for cache, by flushing cached entries until the amount of memory used is within the configured maximum parameter.
                
                """
                if ModelDDvlPloneTool_Cache.gTotalCharsCachedForElements >= ( theModelDDvlPloneTool.vMaxCharsCachedForElements + cMinThresholdCharsToRelease):
                    """Hysteresis : Delay a bit over the set limit the clean up of memory used, such that no all request produce a clean up of used memory. 
                    
                    """
                    someCacheEntriesToRelease = []
                    someCharsToRelease        = 0
                    
                    if ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel) or ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel):
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_Old( )
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_New( gCacheEntriesList_Old_Sentinel)
                    
                    
                    unCacheEntryCandidateToFlush = ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel.vNext
                    
                    while unCacheEntryCandidateToFlush and ( not unCacheEntryCandidateToFlush.fIsSentinel()) and \
                        ( ModelDDvlPloneTool_Cache.gTotalCharsCachedForElements - someCharsToRelease) < ( theModelDDvlPloneTool.vMaxCharsCachedForElements - cMinThresholdCharsToRelease):
                        """Hysteresis : Clean up a bit more memory than the maximum configured, and do not clean up immediately on hitting the limit, such that no all request produce a clean up of used memory.
                        
                        """  
                        if aCacheEntry.vValid:
                            
                            if ( not aCacheEntry.vPromise) or ( aCacheEntry.vPromise  and ( aCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel)):
                                unCachedTemplate = aCacheEntry.vHTML
                                if unCachedTemplate:
            
                                    unCharsTemplate    = len( unCachedTemplate)
                                    someCharsToRelease += unCharsTemplate
                                    
                                    someCacheEntriesToRelease.append( aCacheEntry)
                            
                        unCacheEntryCandidateToFlush = unCacheEntryCandidateToFlush.vNext
                                
                    if someCacheEntriesToRelease:
                        self.pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, someCacheEntriesToRelease)
                
                        
                        
                            
                 
                # ###########################################################
                """Traverse cache control structures to access the cache entry corresponding to the parameters. Elements found missing shall be created, to hook up the new cache entry.
                
                """
                if ModelDDvlPloneTool_Cache.gCachedTemplatesForElements == None:
                    ModelDDvlPloneTool_Cache.gCachedTemplatesForElements = { }
                    
                someCachedTemplatesForProject = ModelDDvlPloneTool_Cache.gCachedTemplatesForElements.get( aProjectName, None)
                if someCachedTemplatesForProject  == None:
                    someCachedTemplatesForProject = { }
                    ModelDDvlPloneTool_Cache.gCachedTemplatesForElements[ aProjectName] = someCachedTemplatesForProject
        
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
                anExistingCacheEntry = someCachedTemplateForRelatedElement.get( unRoleKind, None)
                
                
                
                
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
                    anActionToDo = 'MakePromise'
                    
                elif not anExistingCacheEntry.vPromise:
                    # ###########################################################
                    """A null promise is a sign something went wrong with its resolution. A new entry shall be created, and shall replace the existing one in the cache control structure.
                    
                    """
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
                        anActionToDo = 'MakePromise'
                        
                    else:
                        # ###########################################################
                        """Found cached template: Cache Hit. Update cache hit statistics, and return the cached HTML
                        
                        """
                        anExistingCacheEntry.vHits += 1
        
                        ModelDDvlPloneTool_Cache.gTotalCacheHitsForElements  += 1
                        
                        ModelDDvlPloneTool_Cache.gTotalCharsSavedForElements += len( anExistingCacheEntry.vHTML)
                        ModelDDvlPloneTool_Cache.gTotalTimeSavedForElements  += max( anExistingCacheEntry.vMilliseconds, 0)
                        
                    
                        
                        # ###########################################################
                        """Renew the age of the cache entry in the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                        See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                        
                        """
                        
                        if ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel) or ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel):
                            ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_Old( )
                            ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_New( gCacheEntriesList_Old_Sentinel)
                        
                        anExistingCacheEntry.pUnLink()
                        
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel.pLink( anExistingCacheEntry) 
                        
                        
                        
                        
                        # ###########################################################
                        """Returning the cache entry found, and an indication that no promise was made (so no rendering has to be produced to fullfill it), and there is no need to just fallback and render it now
                        
                        """
                        unExistingOrPromiseCacheEntry = anExistingCacheEntry
                        anActionToDo                  = 'UseFoundEntry'
    
                        
                        
                        
                if not ( anActionToDo == 'UseFoundEntry'):
                    # ###########################################################
                    """Not Found usable cached template: Cache Fault. Update cache fault statistics.
                    
                    """
                    ModelDDvlPloneTool_Cache.gTotalCacheFaultsForElements   += 1
                    
                    
                    
                if anActionToDo == 'MakePromise':
                    # ###########################################################
                    """Create a new cache entry as a promise to be fullfilled after the CRITICAL SECTION, and hook it up in the cache control structure.
                    
                    """
                    
                    # ###########################################################
                    """Allocate a new unique id for the cache entry, 
                    
                    """
                    if not ModelDDvlPloneTool_Cache.gCacheEntryUniqueIdCounter:
                        ModelDDvlPloneTool_Cache.gCacheEntryUniqueIdCounter = 1
                        
                    ModelDDvlPloneTool_Cache.gCacheEntryUniqueIdCounter += 1  
                    
                    unCacheEntryUniqueId = ModelDDvlPloneTool_Cache.gCacheEntryUniqueIdCounter
    
                    unPromiseMade = int( time() * 1000)
                    
                    aNewCacheEntry = MDDRenderedTemplateCacheEntry_ForElement(
                        theUniqueId          =unCacheEntryUniqueId,
                        theValid             =True,
                        thePromise           =unPromiseMade,
                        theUser              =unMemberId,
                        theDate              =None,
                        theProject           =aProjectName,
                        theView              =aViewName,
                        theLanguage          =aNegotiatedLanguage,
                        theHTML              =None,
                        theMilliseconds      =0,
                        theUID               =unElementUID,
                        theTitle             =unElementTitle,
                        theURL               =unElementURL,
                        thePath              =unElementPath,
                        theRoleKind          =unRoleKind,
                        theRelation          =unRelationCursorName,
                        theCurrentUID        =unCurrentElementUID,
                    )
                    
                    unExistingOrPromiseCacheEntry = aNewCacheEntry
                    
                    
                    
                    
                    # ###########################################################
                    """Add unique id of cache entry to the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                    See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                    
                    """
                    if ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel) or ( not ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel):
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_Old_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_Old( )
                        ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel = MDDRenderedTemplateCacheEntry_ListSentinel_New( gCacheEntriesList_Old_Sentinel)
                    
                    ModelDDvlPloneTool_Cache.gCacheEntriesList_New_Sentinel.pLink( aNewCacheEntry)
        
                    
                    
                    # ###########################################################
                    """Hook up the new cache entry promise in the cache control structure, to be fullfilled after the CRITICAL SECTION.
                    
                    """
                    someCachedTemplateForRelatedElement[ unRoleKind] = aNewCacheEntry
                    
                    if ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID == None:
                        ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID = { }
                    
                    unasCachedEntriesForElementUID = ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID.get( unElementUID, None)
                    if unasCachedEntriesForElementUID == None:
                        unasCachedEntriesForElementUID = []
                        ModelDDvlPloneTool_Cache.gCachedEntriesByElementUID[ unElementUID] = unasCachedEntriesForElementUID 
            
                    unasCachedEntriesForElementUID.append( aNewCacheEntry)
                    
                    
                    # ###########################################################
                    """Register cache entry as pending to accumulate its length into the used chars total, to be set when the promise is fullfilled after the CRITICAL SECTION, and accumulated in the next HTTP request accessing the cache.
                    See section above with comment starting with :
                        MEMORY consumed maintenance: Accumulate into the chars use...
                    
                    """
                    if ModelDDvlPloneTool_Cache.gCacheEntriesPromised == None:
                        ModelDDvlPloneTool_Cache.gCacheEntriesPromised = [ ]
                    ModelDDvlPloneTool_Cache.gCacheEntriesPromised.append( aNewCacheEntry)  
                    
                    

                    
                    # ###########################################################
                    """Update cache statistics.
                    
                    """
                    ModelDDvlPloneTool_Cache.gTotalCacheEntriesForElements  += 1
                    
                    
                        
            finally:
                # #################
                """MUTEX UNLOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                
                
                
                
            # ###########################################################
            """Act according to the analysis made of the Cache entry, if retrieved, and decide how to proceed: using it, promissing to create a new one, or just fallback to render the template now and return it.
            
            """
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
                        u'<span>%s' % theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Cached', 'Cached-'),
                    )   
        
                    aEndTime = int( time() * 1000)
                    unDurationString = '%d ms' % ( aEndTime - aBeginTime)
                    
                    unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                        '%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                        '%s</span>' % unDurationString
                    )
                    
                    return unRenderedTemplateToReturnWithDuration
                
                
            if ( anActionToDo == 'UseFoundEntry') or ( anActionToDo == 'JustFallbackToRenderNow') or ( ( anActionToDo == 'MakePromise') and ( not unPromiseMade)) or not ( anActionToDo == 'MakePromise') or (unExistingOrPromiseCacheEntry == None):
                # ###########################################################
                """Entry was found, but something was wrong, or it has been decided that the action is to just render now, or a promise has been made but there is no promise code, or a the action is not the remaining possiblity of MakePromise , or no promise entry has been created. Fallback to render now.
                
                """
                unRenderedTemplate = theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
                
                if theModelDDvlPloneTool.vDisplayCacheHitInformation:
                    if theModelDDvlPloneTool.vDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                        unRenderedTemplateToReturn = u'%s\n<br/><br/><font size="1"><strong>%s</strong></font>' % ( unRenderedTemplate, theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_JustRendered', 'Just Rendered-'),)
                    elif theModelDDvlPloneTool.vDisplayCacheHitInformation == cDisplayCacheHitInformation_Top:          
                        unRenderedTemplateToReturn = u'<br/><font size="1"><strong>%s</strong></font><br/>\n%s' % ( theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_JustRendered', 'Just Rendered-'), unRenderedTemplate)
                    else:
                        unRenderedTemplateToReturn = unRenderedTemplate[:]
                        
                aEndTime = int( time() * 1000)
                unDurationString = '%d ms' % ( aEndTime - aBeginTime)
                
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                    '%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                    '%s</span>' % unDurationString
                )
                
                return unRenderedTemplateToReturnWithDuration
                
                
    
        
 

        
            unRenderedCacheInfo = u''
            
            # ###########################################################
            """Render a caching information collapsible section to append to the rendered template HTML.
                
            """
            if theModelDDvlPloneTool.vDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]:
                
                # ###########################################################
                """Prepare internationalized strings, and info values.
                    
                """
                aCacheEntryValuesDict = {
                    'ElementURL':                    '',
                    'ModelDDvlPlone_ShowNoFromCacheLink_label':theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_ShowGeneratedNoFromCacheLink_label', 'Show generated (not from cache)-'), 
                    'ModelDDvlPlone_FlushFromCacheLink_label':theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_FlushFromCacheLink_label', 'Flush from cache-'), 
                    'cMagicReplacementString_TimeToRetrieve':          cMagicReplacementString_TimeToRetrieve,
                    'cMagicReplacementString_Milliseconds':            cMagicReplacementString_Milliseconds,
                    'cMagicReplacementString_Len':                     cMagicReplacementString_Len,
                    'cMagicReplacementString_Date':                    cMagicReplacementString_Date,
                    'cMagicReplacementString_CollapsibleSectionTitle': cMagicReplacementString_CollapsibleSectionTitle,
                    'cMagicReplacementString_UniqueId':                cMagicReplacementString_UniqueId,
                    'ModelDDvlPlone_Cached':         theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Cached', 'Cached-'), 
                    'ModelDDvlPlone_JustCached':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_JustRendered', 'Just Rendered-'), 
                    'ModelDDvlPlone_JustRendered':   theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_JustRendered', 'Just Cached-'), 
                    'ModelDDvlPlone_Time_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Time_label', 'Time (ms)-'), 
                    'ModelDDvlPlone_Len_label':      theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Len_label', 'Len-'), 
                    'ModelDDvlPlone_User_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_User_label', 'User-'), 
                    'ModelDDvlPlone_RoleKind_label': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_RoleKind_label', 'Role kind-'), 
                    'ModelDDvlPlone_Date_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Date_label', 'Date-'), 
                    'ModelDDvlPlone_Project_label':  theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Project_label', 'Project-'), 
                    'ModelDDvlPlone_Language_label': theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Language_label', 'Language-'), 
                    'ModelDDvlPlone_Path_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Path_label', 'Path-'), 
                    'ModelDDvlPlone_UID_label':      theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_UID_label', 'UID-'), 
                    'ModelDDvlPlone_URL_label':      theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_URL_label', 'URL-'), 
                    'ModelDDvlPlone_View_label':     theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_View_label', 'View-'), 
                    'ModelDDvlPlone_Len_label':      theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Len_label', 'Len-'), 
                    'title_label':                   theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_titulo_label', 'Title-'), 
                    
                    'aProjectName':                  aProjectName,
                    'aNegotiatedLanguage':           aNegotiatedLanguage,
                    'unTitle':                       theModelDDvlPloneTool.fAsUnicode( theContextualObject, theContextualObject.Title()),
                    'unElementURL':                  unElementURL,
                    'unElementUID':                  unElementUID,
                    'unElementPath':                 unElementPath,
                    'aViewName':                     aViewName,
                    'unRoleKind':                    unRoleKind,
                    'unMemberId':                    unMemberId,
                    'unPagina':                      (( aViewName in [ 'Textual', 'Textual_NoHeaderNoFooter',]) and '/') or (( aViewName in [ 'Tabular', 'Tabular_NoHeaderNoFooter',]) and '/Tabular/') or ( '/%s/' % aViewName)
                }                    
                    
                
                
                
                
                unRenderedCacheInfo = u"""
                    <br/>
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
                            <a href="%(unElementURL)s%(unPagina)s?theNoCache=1" id="cid_MDDtheNoCache" >
                                %(ModelDDvlPlone_ShowNoFromCacheLink_label)s
                            </a>
                            &emsp;
                            &emsp;
                            <a href="%(unElementURL)s%(unPagina)s?theFlushCache=1&theNoCache=1" id="cid_MDDtheFlushCache" >
                                %(ModelDDvlPlone_FlushFromCacheLink_label)s
                            </a>
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
                                        <td align="left"><strong>%(title_label)s</strong></td>
                                        <td align="left">%(unTitle)s</td>
                                    </tr>
                                    <tr class="odd">
                                        <td align="left"><strong>%(ModelDDvlPlone_URL_label)s</strong></td>
                                        <td align="left">%(unElementURL)s</td>
                                    </tr>
                                    <tr class="odd">
                                        <td align="left"><strong>%(ModelDDvlPlone_Path_label)s</strong></td>
                                        <td align="left">%(unElementPath)s</td>
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
                                        <td align="left">%(unRoleKind)s</td>
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
                        theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_Relation_label', 'Relation-'), 
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
                        theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_RelatedElement_label', 'Related Element-'), 
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
                
                
                
            
            
            # ###########################################################
            """Render template, because it was not found (valid) in the cache. This may take some significant time. Status of cache may have changed since.
            
            """
            
            unDateBeforeRender = DateTime()
            
            unRenderedTemplate = theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
            unDateAfterRender = DateTime()
            
            unosMilliseconds = unDateAfterRender.millis() - unDateBeforeRender.millis()
                    
            unRenderedTemplateWithCacheInfo = unRenderedTemplate
            
      
            
             # ###########################################################
            """If so condfigured: Append a caching information collapsible section to the rendered template HTML.
            
            """
            if not( theModelDDvlPloneTool.vDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]):
                unRenderedTemplateWithCacheInfo = unRenderedTemplate[:]
            
            else:
                unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_UniqueId,     str( unCacheEntryUniqueId))
                unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Milliseconds, str( unosMilliseconds))
                unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Len,          str( len( unRenderedTemplate)))
                unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Date,         unDateAfterRender.rfc822())
                   
                if theModelDDvlPloneTool.vDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                    unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedTemplate, unRenderedCacheInfo,)
                else:
                    unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedCacheInfo, unRenderedTemplate,)
                
            
            
                  
            
            # ###########################################################
            """If so configured : CRITICAL SECTION to register in the promised cache entry the HTML result of rendering the template. 
            
            """
            unWasSynch = False
            try:
                # #################
                """If so configured : MUTEX  LOCK. 
                
                """
                if theModelDDvlPloneTool.vLockOnceOrTwice == cLockOnceOrTwice_Twice:
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    unWasSynch = True
                    ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.acquire()
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                unExistingOrPromiseCacheEntryPromise = unExistingOrPromiseCacheEntry.vPromise
                
                if ( unPromiseMade == unExistingOrPromiseCacheEntryPromise):
                    # ###########################################################
                    """If somebody messed with the promised cache entry, so it is not being updated here.
                    
                    """
                    unExistingOrPromiseCacheEntry.vHTML            = unRenderedTemplateWithCacheInfo
                    unExistingOrPromiseCacheEntry.vDate            = DateTime()
                    unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                    unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                
                
            finally:
                # #################
                """MUTEX UNLOCK. 
                
                """
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if unWasSynch:
                    ModelDDvlPloneTool_Cache.gTemplatesCacheMutex.release()
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                
                 
    
            # ###########################################################
            """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
            
            """
            unRenderedTemplateToReturn = unRenderedTemplateWithCacheInfo.replace(    
                '<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
                '<span>%s' % theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_JustCached', 'JustCached-'),
            )   
            
            aEndTime = int( time() * 1000)
            unDurationString = '%d ms' % ( aEndTime - aBeginTime)
            
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                '%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                '%s</span>' % unDurationString
            )
            
            return unRenderedTemplateToReturnWithDuration
        
        except:
            raise
            #unaExceptionInfo = sys.exc_info()
            #unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
            
            #unInformeExcepcion = 'Exception during access to a page from cache of rendered templates' 
            #unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            #unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            #unInformeExcepcion += unaExceptionFormattedTraceback   
            
            #if cLogExceptions:
                #logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            #unRenderedTemplate = theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)
            
            #unRenderedTemplateToReturn = u'%s\n<br/><br/><font size="1"><strong>%s</strong></font>' % ( unRenderedTemplate, theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', 'ModelDDvlPlone_ExceptionRetrievingPageFromCachedRenderedTemplate', 'Exception rendering page-'), unExceptionReport)
        
            #aEndTime = int( time() * 1000)
            #unRenderedTemplateToReturn = '%s\n<br/>%d ms<br/>' % ( unRenderedTemplateToReturn, aEndTime - aBeginTime,)

            #return unRenderedTemplateToReturn
                
       
        
    security.declarePrivate( 'fIsPrivateCacheViewForNonAnonymousUsers')
    def fIsPrivateCacheViewForNonAnonymousUsers(self , theContextualObject, theTemplateName):
        return  theTemplateName == 'Tabular'
        
    
        
    


    # #############################################################
    """User Role access methods. Roles are classified into a reduced number of role kinds: Anonymous, Authenticated, Owner, Manager
    
    """

         
    security.declarePrivate( 'fGetMemberRoleKind')
    def fGetMemberRoleKind(self , theContextualObject, theTemplateName):
    
        aMembershipTool = getToolByName( theContextualObject, 'portal_membership', None)
        if not aMembershipTool:
            return ''
        
        unMember = aMembershipTool.getAuthenticatedMember()   
        if not unMember:
            return ''
        
        if unMember.getUserName() == 'Anonymous User':
            return cRoleKind_Anonymous
        
        unElementoGetRoles = theContextualObject
        unElementoRaiz = None
        try:
            unElementoRaiz = theContextualObject.getRaiz()
        except:
            None
        if not ( unElementoRaiz == None):
            unElementoGetRoles = unElementoRaiz
        
            
        someRoles = ModelDDvlPloneTool_Retrieval().fGetRequestingUserRoles( unElementoGetRoles)
        if not someRoles:
            return cRoleKind_Anonymous
        
        
        # ##############################################################
        """Cached entries of elements with private caches for the specified view, shall be associated with the User Id (and thus private to the user), except for: Non Anonymous users, that do not hold a Member, Reviewer, Owner or Manager Role in the model root (or this object, if no model root), shall obtain cached pages as an Authenticated role kind.
        
        """
        if self.fIsPrivateCacheViewForNonAnonymousUsers( theContextualObject, theTemplateName): 
            
            if not set( [ cZopeRole_Member, cZopeRole_Reviewer, cZopeRole_Owner, cZopeRole_Manager,]).intersection( set( someRoles)):
                return cRoleKind_Authenticated
                
            unMemberId = unMember.getMemberId()
            if unMemberId:
                return unMemberId
        
            
        if cZopeRole_Manager in someRoles:
            return cRoleKind_Manager
        
        if cZopeRole_Owner in someRoles:
            return cRoleKind_Owner

        if set( [ cZopeRole_Reviewer, cZopeRole_Member, ]).intersection( set( someRoles)):
            return cRoleKind_Member
        
        if cZopeRole_Authenticated in someRoles:
            return cRoleKind_Authenticated
        
        # ACV 20091118 Edundant with the last sentence. Removed. 
        #
        #if cZopeRole_Anonymous in someRoles:
            #return cRoleKind_Anonymous
        
        return cRoleKind_Anonymous
                
    
    
    


    

    
    
    
    
    
        
    