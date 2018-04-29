# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_EntriesAccess.py
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


from Products.PlacelessTranslationService.Negotiator import getLangPrefs




from ModelDDvlPloneTool_CacheConstants          import *

from MDDStringConversions                       import *




# #######################################################
# #######################################################








cRenderedTitle_HTML = """
<h1>%s</h1>
"""



    
class ModelDDvlPloneTool_Cache_EntriesAccess:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the access to entries in the cache support structures.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    


    
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
    
        
       
    
    
    
    
    
    
    
    
    security.declarePrivate( 'fCached_HTML')
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
            unRenderedTitle = cRenderedTitle_HTML % self.fCGIE( unTitle)
            unHTML = '%s\n%s\n' % ( unRenderedTitle, unHTML,)

        return unHTML
        
    
    
    
    
    
    
    
    
                
    
    
    
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
                
                
                

        unRootElementURL = unRootElement.absolute_url()
                    
        unParsedRootElementURL = self.fURLParse( theModelDDvlPloneTool, theContextualObject, unRootElementURL, )
        if ( not unParsedRootElementURL):
            return [ unaCachedEntry, unDirectory, unFilePath,]
                   
        if ( not unParsedRootElementURL[ 0]) or ( not unParsedRootElementURL[ 1]):
            return [ unaCachedEntry, unDirectory, unFilePath,]
        
        unSchemeHostAndDomain = '%s-%s' % ( unParsedRootElementURL[ 0], unParsedRootElementURL[ 1],)
        
        
        
        # ###########################################################
        """Determine if the user specific cache should be used. Determine the role kind to use to index the cache entry.
        
        """
        aCacheName       = cCacheName_ForElements
        aCacheKind       = cCacheKind_ForElements
        
        aRoleKindToIndex = cRoleKind_Anonymous
        
        aRoleKind, unMemberId, aRoleName = self.fGetMemberRoleKindAndUserId( theModelDDvlPloneTool, theContextualObject, theTemplateName)
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
        
                    someCachedTemplatesForRoot = someCachedTemplatesForLanguage.get( unRootElementUID, None)
                    if someCachedTemplatesForRoot:
                            
                        someCachedTemplatesForElement = someCachedTemplatesForRoot.get( unElementUID, None)
                        if someCachedTemplatesForElement:
                                
                            someCachedTemplatesForView = someCachedTemplatesForElement.get( aViewName, None)
                            if someCachedTemplatesForView:
                    
                                someCachedTemplateForRelationCursor = someCachedTemplatesForView.get( unRelationCursorName, None)
                                if someCachedTemplateForRelationCursor:
                                    
                                    someCachedTemplateForRelatedElement = someCachedTemplateForRelationCursor.get( unCurrentElementUID, None)
                                    if someCachedTemplateForRelatedElement:
                                        
                                        someCachedTemplateForSchemeHostAndDomain = someCachedTemplateForRelatedElement.get( unSchemeHostAndDomain, None)
                                        
                                        if someCachedTemplateForSchemeHostAndDomain:
                                            unaCachedEntry = someCachedTemplateForSchemeHostAndDomain.get( aRoleKindToIndex, None)
            
        finally:
            # #################
            """IF theEnforceThreadSafety MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if theEnforceThreadSafety:
                self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                

        return [ unaCachedEntry, unDirectory, unFilePath,]

    
    
         
    
    
    
    security.declarePrivate( 'fCountElementDependentCachedEntriesInProjectLanguageRoot')
    def fCountElementDependentCachedEntriesInProjectLanguageRoot(self, 
        theModelDDvlPloneTool  =None, 
        theContextualObject    =None, 
        theCacheName           =None, 
        theProjectName         =None, 
        theLanguage            =None,
        theRoot                =None,
        theEnforceThreadSafety =True):
        """Count the number the existing Cache Entries from a cache, optionally only those in for the specified project, optionally only those in for the specified language, optionally only those under for the specified root element.
        
        """    
        
        if theModelDDvlPloneTool == None:
            return 0

        if theContextualObject == None:
            return 0
        
        if not theCacheName:
            return 0
                    
        if cForbidCaches or not self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, theCacheName):
            return 0
                
                                
        someCachedEntriesForProject = self.fFindElementDependentCachedEntriesInProjectLanguageRoot( 
            theModelDDvlPloneTool  =theModelDDvlPloneTool, 
            theContextualObject    =theContextualObject, 
            theCacheName           =theCacheName, 
            theProjectName         =theProjectName, 
            theLanguage            =theLanguage,
            theRoot                =theRoot,
            theEnforceThreadSafety =theEnforceThreadSafety,
        )
        
        someCachedEntriesForProjectSet = set( someCachedEntriesForProject)
        
        aNumCachedEntries = len( someCachedEntriesForProjectSet)
        
        return aNumCachedEntries
    
    
    

       
    security.declarePrivate( 'fFindElementDependentCachedEntriesInProjectLanguageRoot')
    def fFindElementDependentCachedEntriesInProjectLanguageRoot(self, 
        theModelDDvlPloneTool  =None, 
        theContextualObject    =None, 
        theCacheName           =None, 
        theProjectName         =None, 
        theLanguage            =None,
        theRoot                =None,
        theEnforceThreadSafety =True):
        """Return the existing Cache Entries from a cache, optionally only those in for the specified project, optionally only those in for the specified language, optionally only those under for the specified root element.
        
        """
        
        someCachedEntries = [ ]

                
        if theModelDDvlPloneTool == None:
            return someCachedEntries

        if theContextualObject == None:
            return someCachedEntries
        
        if not theCacheName:
            return someCachedEntries
                    
        if cForbidCaches or not self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, theCacheName):
            return someCachedEntries
                        

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
            """Traverse cache control structures to access the cache entry corresponding to the parameters. 
            
            """
                
            someCachedTemplatesForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectName)                              
            if someCachedTemplatesForProject:
                
                someLanguages = [ ]
                if theLanguage:
                    someLanguages = [ theLanguage,]
                else:
                    someLanguages = someCachedTemplatesForProject.keys()
                            
                    
                for aLanguage in someLanguages:
                    
                    someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aLanguage, None)
                    if someCachedTemplatesForLanguage:
        
                        someRoots = [ ]
                        if theRoot:
                            someRoots = [ theRoot,]
                        else:
                            someRoots = someCachedTemplatesForLanguage.keys()
                 
                            
                        for aRoot in someRoots:
                            
                            someCachedTemplatesForRoot = someCachedTemplatesForLanguage.get( aRoot, None)
                            if someCachedTemplatesForRoot:
                    
                                someElementUIDs = someCachedTemplatesForRoot.keys()
                                
                                for unElementUID in someElementUIDs:
                                    
                                    someCachedTemplatesForElement = someCachedTemplatesForRoot.get( unElementUID, None)
                                    if someCachedTemplatesForElement:
                                            
                                        someViewNames = someCachedTemplatesForElement.keys()
                                        
                                        for aViewName in someViewNames:
                                                
                                            someCachedTemplatesForView = someCachedTemplatesForElement.get( aViewName, None)
                                            if someCachedTemplatesForView:
                                    
                                                someRelationCursorNames = someCachedTemplatesForView.keys()
                                                
                                                for unRelationCursorName in someRelationCursorNames:
                                                        
                                                    someCachedTemplatesForRelationCursor = someCachedTemplatesForView.get( unRelationCursorName, None)
                                                    if someCachedTemplatesForRelationCursor:
                                                        
                                                        someRelatedElementUIDs = someCachedTemplatesForRelationCursor.keys()
                                                        
                                                        for unCurrentElementUID in someRelatedElementUIDs:
                                                            
                                                            someCachedTemplatesForRelatedElement = someCachedTemplatesForRelationCursor.get( unCurrentElementUID, None)
                                                            if someCachedTemplatesForRelatedElement:
                                                                
                                                                someSchemeHostAndDomains = someCachedTemplatesForRelatedElement.keys()
                                                                
                                                                for unSchemeHostAndDomain in someSchemeHostAndDomains:
                                                                    
                                                                    someCachedTemplatesForSchemeHostAndDomain = someCachedTemplatesForRelatedElement.get( unSchemeHostAndDomain, None)
                                                                    
                                                                    if someCachedTemplatesForSchemeHostAndDomain:
                                                                        
                                                                        someRoleKinds = someCachedTemplatesForSchemeHostAndDomain.keys()
                                                                        
                                                                        for aRoleKind in someRoleKinds:
                                                                            
                                                                            unaCachedEntry = someCachedTemplatesForSchemeHostAndDomain.get( aRoleKind, None)
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
                

        return someCachedEntries

    
    
    
    
                