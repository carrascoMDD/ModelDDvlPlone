# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_EntriesFlush.py
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

from ModelDDvlPloneToolSupport                  import fMillisecondsNow





# #######################################################
# #######################################################




    
class ModelDDvlPloneTool_Cache_EntriesFlush:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the configuration of cache operation parameters.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    



      
    
    
        
        
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
        
        aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
        if aModelDDvlPloneTool_Retrieval == None:
            return False
        
        unMemberId    = aModelDDvlPloneTool_Retrieval.fGetMemberId(  theContextualObject)
     
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
        

     
 
        
        
        
    # ACV 20110222 Unused. Removed        
    #security.declarePrivate( 'fFlushSomeCachedTemplates')
    #def fFlushSomeCachedTemplates(self, theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectNames, theFlushDiskCache=False):
        #"""Initiated by a User with ManagePortal permission, or Manager Role, in the root model element, or the portal root, Remove all cached rendered templates, recording who and when requested the flush.
        
        #"""
        
        #if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            #return False
        
        #if not theCacheName:
            #return False
        
        #if theModelDDvlPloneTool == None:
            #return False
        
        #if theContextualObject == None:
            #return False
        
        #aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
        #if aModelDDvlPloneTool_Retrieval == None:
            #return False

        
        #unMemberId    = aModelDDvlPloneTool_Retrieval.fGetMemberId(  theContextualObject)
        
        #someFilesToDelete = [ ]
     
        ## ###########################################################
        #"""Remove all existing cached templates, from within a thread-safe protected critical section.
        
        #"""

        #try:
            
            ## #################
            #"""MUTEX LOCK. 
            
            #"""
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            #aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskEnabled)
            #aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, theCacheName, cCacheConfigPpty_CacheDiskPath)
            
            #someCacheEntries, someFilePaths = self.fFindSomeCachedEntriesAndFilePaths( theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectNames,)
            
            #if someFilePaths:
                #someFilesToDelete.extend( someFilePaths)
                
            #if someCacheEntries:
                #self._pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, someCacheEntries, someFilesToDelete)
            
        #finally:
            ## #################
            #"""MUTEX UNLOCK. 
            
            #"""
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
        #if theFlushDiskCache:
            #if aCacheDiskEnabled:
                #someFilesToDelete = [ ]
                #self._pAllFilePathsInto( aCacheDiskPath, someFilesToDelete)
                #if someFilesToDelete:
                    #self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
            
             
        #return True
        

         
    
    
          
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

    
    
    
    
    
    
    

        
    
    security.declarePrivate( 'fFlushCachedTemplatesSelected')
    def fFlushCachedTemplatesSelected(self, theModelDDvlPloneTool, theContextualObject, theCacheName, theProjectName, theLanguage, theRoot, theFlushDiskCache=False):
        """Invoked by authorized users requesting invalidation of the cache entry given a ProjectName, and optionally a Language and a Root UID.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return 0
        
        
        if theModelDDvlPloneTool == None:
            return 0
        
        if not theProjectName:
            return 0
        
        
        someCachedEntries = self.fFindElementDependentCachedEntriesInProjectLanguageRoot( 
            theModelDDvlPloneTool  =theModelDDvlPloneTool, 
            theContextualObject    =theContextualObject, 
            theCacheName           =theCacheName, 
            theProjectName         =theProjectName, 
            theLanguage            =theLanguage,
            theRoot                =theRoot,
            theEnforceThreadSafety =True,
        )
                
        if not someCachedEntries:
            return 0
        
        someCachedEntries = set( someCachedEntries)
        
        
        
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


            self._pFlushCacheEntries( theModelDDvlPloneTool, theContextualObject, someCachedEntries, theFilesToDelete=someFilesToDelete)                             
                                                    
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

        return len( someCachedEntries)        

    
    
    
    
    
        
            
            
            
    
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
        
        aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
        if aModelDDvlPloneTool_Retrieval == None:
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
                            Root UID
                                Element UID
                                    View Name
                                        -when applicable - Relation name
                                            -when applicable - Current related element UID
                                                - scheme, host and domain name
                                                    - role kind or user id : the Entry
                """
            
                aCacheName   = unaCacheEntryToFlush.vCacheName
                aProjectName = unaCacheEntryToFlush.vProject
                aLanguage    = unaCacheEntryToFlush.vLanguage
                aRootUID     = unaCacheEntryToFlush.vRootUID
                anElementUID = unaCacheEntryToFlush.vUID
                aViewName    = unaCacheEntryToFlush.vView
                aRelationName= unaCacheEntryToFlush.vRelation 
                aCurrentUID  = unaCacheEntryToFlush.vCurrentUID
                aSchemeHostAndDomain=unaCacheEntryToFlush.vSchemeHostAndDomain
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
                
                    someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aLanguage, None)
                    if someCachedTemplatesForLanguage:
                            
                        someCachedTemplatesForRoot = someCachedTemplatesForLanguage.get( aRootUID, None)
                        if someCachedTemplatesForRoot:
                            
                            someCachedTemplatesForElement = someCachedTemplatesForRoot.get( anElementUID, None)
                            if someCachedTemplatesForElement:
                                
                                someCachedTemplatesForView = someCachedTemplatesForElement.get( aViewName, None)
                                if someCachedTemplatesForView:
                                    
                                    someCachedTemplatesForRelation = someCachedTemplatesForView.get( aRelationName, None)
                                    if someCachedTemplatesForRelation:
                                        
                                        someCachedTemplatesForCurrentUID = someCachedTemplatesForRelation.get( aCurrentUID, None)
                                        if someCachedTemplatesForCurrentUID:
                                    
                                            someCachedTemplatesForSchemeHostAndDomain = someCachedTemplatesForCurrentUID.get( aSchemeHostAndDomain, None)
                                            if someCachedTemplatesForSchemeHostAndDomain:
                                            
                                                unaFoundCacheEntry = someCachedTemplatesForSchemeHostAndDomain.get( aRoleKind, None)
                                                
                                                if unaFoundCacheEntry and ( unaFoundCacheEntry == unaCacheEntryToFlush):
                                                                                                            
                                                    try:
                                                        someCachedTemplatesForSchemeHostAndDomain.pop( aRoleKind)
                                                    except:
                                                        None
                                            
      
                                                if not someCachedTemplatesForSchemeHostAndDomain:
                                                    someCachedTemplatesForCurrentUID.pop( aSchemeHostAndDomain)
                                                    unosObjectsToDelete.append( someCachedTemplatesForSchemeHostAndDomain)
        
          
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
                                    someCachedTemplatesForRoot.pop( anElementUID)
                                    unosObjectsToDelete.append( someCachedTemplatesForElement)
                
                            if not someCachedTemplatesForRoot:
                                someCachedTemplatesForLanguage.pop( aRootUID)
                                unosObjectsToDelete.append( someCachedTemplatesForRoot)
                                
                        if not someCachedTemplatesForLanguage:
                            someCachedTemplatesForProject.pop( aLanguage)
                            unosObjectsToDelete.append( someCachedTemplatesForLanguage)
                                
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
                aSchemeHostAndDomain=unaCacheEntryToFlush.vSchemeHostAndDomain

                                           
                if not ( aProjectName and aLanguage and aViewName and aSchemeHostAndDomain):
                    unasEntriesToRemove.append( unaCacheEntryToFlush)
                    continue

                
                unasEntriesToRemove.append( unaCacheEntryToFlush)
                
                someCachedTemplatesForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)              
                if someCachedTemplatesForProject:
                
                
                    someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aLanguage, None)
                    if someCachedTemplatesForLanguage:
                            
                        someCachedTemplateForView = someCachedTemplatesForLanguage.get( aViewName, None)
                        if someCachedTemplateForView:
                                
                            unaFoundCacheEntry = someCachedTemplateForView.get( aSchemeHostAndDomain, None)
                            
                            if unaFoundCacheEntry and ( unaFoundCacheEntry == unaCacheEntryToFlush):
                                                                                        
                                try:
                                    someCachedTemplateForView.pop( aSchemeHostAndDomain)
                                except:
                                    None
                                        
                            if not someCachedTemplateForView:
                                someCachedTemplatesForLanguage.pop( aViewName)
                                unosObjectsToDelete.append( someCachedTemplateForView)
                                
                        if not someCachedTemplatesForLanguage:
                            someCachedTemplatesForProject.pop( aLanguage)
                            unosObjectsToDelete.append( someCachedTemplatesForLanguage)
                                
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
    
    
    
    
    

    
    


    security.declarePrivate( 'fVerifyInvalidationRequesterIdentificationAndAutentication')
    def fVerifyRequesterPeerIdentificationAndAutentication(self, theContextualObject, thePeerIdentificationString, thePeerAuthenticationString):
             
        if thePeerAuthenticationString == cUnsecureCacheFlushAcknowledgedAuthenticationString:
            return True
        
        return False
    
            
    
    