# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_Diagnostics.py
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
from Products.CMFCore.utils import getToolByName


from Products.PlacelessTranslationService.Negotiator import getLangPrefs




from ModelDDvlPloneTool_CacheConstants          import *

from MDDStringConversions                       import *






# #######################################################
# #######################################################








    
class ModelDDvlPloneTool_Cache_Diagnostics:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the diagnostics of cache support structures.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    

    
    
    
       
    security.declarePrivate('fCachesDiagnostics')
    def fCachesDiagnostics(self, theModelDDvlPloneTool, theContextualObject, theCacheNames=None, theAdditionalParams=None):
    
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            
            return self.fCachesDiagnostics_WithinCriticalSection( theModelDDvlPloneTool, theContextualObject, theCacheNames=theCacheNames, theAdditionalParams=theAdditionalParams)
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                            
                                                       
            
    
                
       
    security.declarePrivate( 'fCachesDiagnostics_WithinCriticalSection')
    def fCachesDiagnostics_WithinCriticalSection(self, theModelDDvlPloneTool, theContextualObject, theCacheNames=None, theAdditionalParams=None):
    
        
        
        someCacheNames = theCacheNames
        if not someCacheNames:
            someCacheNames = cCacheNamesAll[:]
        else:
            if not ( isinstance( someCacheNames, list) or isinstance( someCacheNames, tuple) or isinstance( someCacheNames, set)):
                someCacheNames = list( someCacheNames)
            someCacheNames = set( someCacheNames).intersection( set( cCacheNamesAll))


             
        # ###########################################################
        """Verify cache control structures to access the cache entries
        
        """
        someUIDsElementsToRetrieve = set()
        
        allDiagnostics = self.fNewVoidAllCachesDiagnostics()
        allCacheEntriesInStructure_AllCaches = allDiagnostics[ 'allcacheEntriesInStructures']
        allEntriesWithProblems_AllCaches     = allDiagnostics[ 'allEntriesWithProblems']

        
        # ###########################################################
        """Iterate over Caches
        
        """
        
        
        for aCacheName in someCacheNames:
                
            aDiagnostics = self.fNewVoidCacheDiagnostic()
            aDiagnostics[ 'cache_name'] = aCacheName
            aCacheKind = ''
            for aCName, aCKind in cCacheNamesAndKindsToCreate:
                if aCName == aCacheName:
                    aCacheKind = aCKind
                    break
            if aCacheKind:
                aDiagnostics[ 'cache_kind'] = aCacheKind
               
            allDiagnostics[ 'caches_diagnostics'][ aCacheName] = aDiagnostics
            
            someCacheEntriesInStructure = aDiagnostics[ 'cacheEntriesInStructure']
            someEntriesWithProblems     = aDiagnostics[ 'entriesWithProblems']

            
            
            if aCacheKind in [ cCacheKind_ForElements, cCacheKind_ForUsers,]:
            
                # ###########################################################
                """Iterate over Projects
                
                """
                someProjectNames = sorted( self.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, aCacheName,))
                for aProjectName in someProjectNames:
                    someTemplatesByLanguageForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)                              
                   
                    if not someTemplatesByLanguageForProject:
                        aDiagnostics[ 'structure_voids'].append( [ aProjectName,])
                        
                        
                        
                    # ###########################################################
                    """Iterate over Languages
                    
                    """
                    someLanguages =  sorted( ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or [])
                    for aLanguage  in someLanguages:
                        someTemplatesByRootForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
                        
                   
                        if not someTemplatesByRootForLanguage:
                            aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage])
                            
                            
                        # ###########################################################
                        """Iterate over Roots
                        
                        """
                        someRoots =  sorted( ( someTemplatesByRootForLanguage and someTemplatesByRootForLanguage.keys()) or [])
                        for aRoot  in someRoots:
                            someTemplatesByUIDForRoot = someTemplatesByRootForLanguage.get( aRoot, {})
                            
                       
                            if not someTemplatesByUIDForRoot:
                                aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, aRoot,])
                                
                                                          
                            # ###########################################################
                            """Gather UIDs and Iterate over Elements UIDs
                            
                            """                    
                            someUIDs = sorted( (someTemplatesByUIDForRoot and someTemplatesByUIDForRoot.keys()) or [])
                            
                            someUIDsElementsToRetrieve.update( someUIDs)
                            
                            for anUID in someUIDs:
                                someTemplatesByViewForUID = someTemplatesByUIDForRoot.get( anUID, {})
                                
                                if not someTemplatesByViewForUID:
                                    aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, aRoot, anUID, ])
                                    
                                    
                                    
                                # ###########################################################
                                """Iterate over Views
                                
                                """                        
                                someViewNames = sorted( ( someTemplatesByViewForUID and someTemplatesByViewForUID.keys()) or [])
                                for aViewName in someViewNames:
                                    someTemplatesByRelationForView = someTemplatesByViewForUID.get( aViewName, {})
                                    
                       
                                    if not someTemplatesByRelationForView:
                                        aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, aRoot, anUID, aViewName, ])
                                        
                                        
                                        
                                    # ###########################################################
                                    """Iterate over Relations
                                    
                                    """
                                    someRelations = sorted( ( someTemplatesByRelationForView and someTemplatesByRelationForView.keys()) or [])
                                    for aRelationName in someRelations:
                                        someTemplatesByRelatedUIDForRelation = someTemplatesByRelationForView.get( aRelationName, {})
                                        
                       
                                        if not someTemplatesByRelatedUIDForRelation:
                                            aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, aRoot, anUID, aViewName, aRelationName, ])
                                            
                                            
                                            
                                        # ###########################################################
                                        """Gather and Iterate over Related Element UIDs
                                        
                                        """                                
                                        someRelatedUIDs = sorted( ( someTemplatesByRelatedUIDForRelation and someTemplatesByRelatedUIDForRelation.keys()) or [])
                                        for aRelatedUID in someRelatedUIDs:
                                            if not ( aRelatedUID == cNoCurrentElementUID):
                                                someUIDsElementsToRetrieve.add( aRelatedUID)
                        
                                            someTemplatesBySchemeHostAndDomainForRelatedUID = someTemplatesByRelatedUIDForRelation.get( aRelatedUID, {})
                                              
                                            if not someTemplatesBySchemeHostAndDomainForRelatedUID:
                                                aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, aRoot, anUID, aViewName, aRelationName, aRelatedUID, ])
                                            
                                                
                                                
                                            # ###########################################################
                                            """Iterate over SchemeHostAndDomains
                                            
                                            """
                                            someSchemeHostAndDomains = sorted( ( someTemplatesBySchemeHostAndDomainForRelatedUID and someTemplatesBySchemeHostAndDomainForRelatedUID.keys()) or [])
                                            for aSchemeHostAndDomain in someSchemeHostAndDomains:
                                            
                                                someTemplatesByRoleOrUserForSchemeHostAndDomain = someTemplatesBySchemeHostAndDomainForRelatedUID.get( aSchemeHostAndDomain, {})
                                                
                                                if not someTemplatesByRoleOrUserForSchemeHostAndDomain:
                                                    aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, aRoot, anUID, aViewName, aRelationName, aRelatedUID, aSchemeHostAndDomain, ])
                                            
                                                  
                                                
                                                    
                                                # ###########################################################
                                                """Iterate over RoleOrUsers
                                                
                                                """
                                                someRoleOrUsers = sorted( ( someTemplatesByRoleOrUserForSchemeHostAndDomain and someTemplatesByRoleOrUserForSchemeHostAndDomain.keys()) or [])
                                                for aRoleOrUserName in someRoleOrUsers:
                                                
                                                    
                                                    
                                                    # ########################
                                                    """Access CacheEntry
                                                    
                                                    """
                                                    aCacheEntry = someTemplatesByRoleOrUserForSchemeHostAndDomain.get( aRoleOrUserName, None)
                                                
                                                    if not aCacheEntry:
                                                        # ########################
                                                        """Report cache entry as missing
                                                        
                                                        """
                                                        aDiagnostics[ 'structure_missing_entries'].append( [ aProjectName, aLanguage, aRoot, anUID, aViewName, aRelationName, aRelatedUID, aRoleOrUserName, ])
                                                        
                                                        
                                                    else:
                                                        
                                                        if aCacheEntry in someCacheEntriesInStructure:
                                                            aDiagnostics[ 'structure_entries_found_more_than_once'].add( aCacheEntry)
                                                        
                                                        else:                                                
                                                            someCacheEntriesInStructure.add( aCacheEntry)
                                                        
                                                        if not aCacheEntry.vValid:
                                                            aDiagnostics[ 'invalid_entries_in_list'].add( aCacheEntry)
                                                            self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'Invalid',])
                                                            
                                                        aCacheEntryPromise = aCacheEntry.vPromise
                                                        if aCacheEntryPromise and not ( aCacheEntryPromise == cCacheEntry_PromiseFulfilled_Sentinel):
                                                            aDiagnostics[ 'promised_entries_in_list'].add( aCacheEntry)
                        
                                                        if not aCacheEntryPromise:
                                                            aDiagnostics[ 'broken_promise_entries_in_list'].add( aCacheEntry)
                                                            self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'BrokenPromise',])
                                            
                                                            
                                                        # ########################
                                                        """Verify CacheEntry information consistent with the tree indexing data used to reach it, and report inconsistencies
                                                        
                                                        """
                                                        someEntryInconsistenciesInTree = [ ]
                                                        if ( not aCacheEntry.vProjectName) or not ( aCacheEntry.vProjectName == aProjectName):
                                                            someEntryInconsistenciesInTree.append( [ 'vProjectName', aCacheEntry.vProjectName, aProjectName,])
                                                        if ( not aCacheEntry.vLanguage)    or not ( aCacheEntry.vLanguage == aLanguage):
                                                            someEntryInconsistenciesInTree.append( [ 'vLanguage',    aCacheEntry.vLanguage,    aLanguage,])
                                                        if ( not aCacheEntry.vUID )        or not ( aCacheEntry.vUID == anUID):
                                                            someEntryInconsistenciesInTree.append( [ 'vUID',         aCacheEntry.vUID,         anUID,])
                                                        if ( not aCacheEntry.vView )       or not (aCacheEntry.vView == aViewName):
                                                            someEntryInconsistenciesInTree.append( [ 'vView',        aCacheEntry.vView,        aViewName,])
                                                        if ( not aCacheEntry.vRelation)    or not ( aCacheEntry.vRelation == aRelationName):
                                                            someEntryInconsistenciesInTree.append( [ 'vRelation',    aCacheEntry.vRelation,    aRelationName,])
                                                        if ( not aCacheEntry.vRelation)    or not ( aCacheEntry.vCurrentUID == aRelatedUID): 
                                                            someEntryInconsistenciesInTree.append( [ 'vCurrentUID',  aCacheEntry.vCurrentUID,  aRelatedUID,])
                                                        if ( not aCacheEntry.vRoleKind )   or not ( aCacheEntry.vRoleKind == aRoleOrUserName):
                                                            someEntryInconsistenciesInTree.append( [ 'vRoleKind',    aCacheEntry.vRoleKind,    aRoleOrUserName,])
                                                        if someEntryInconsistenciesInTree:
                                                            aDiagnostics[ 'structure_inconsistent_entries'].append( [ aCacheEntry,              someEntryInconsistenciesInTree,])
                                                             
                                                            self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'inconsistencies_in_tree', someEntryInconsistenciesInTree,])
                                                            
                                                        # ########################
                                                        """Verify CacheEntry properly registered by its unique id
                                                        
                                                        """
                                                        unEntryByUniqueId = self._fGetCachedEntryById( theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUniqueId)
                                                        if not unEntryByUniqueId or not ( unEntryByUniqueId == aCacheEntry):
                                                            aDiagnostics[ 'structure_entries_not_in_uniqueid_registry'].add( aCacheEntry)
                                                            
                                                            self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'not_in_uniqueid_registry',])
                                                              
                                                        
                                                        # ########################
                                                        """Verify CacheEntry properly registered by the element UID
                                                        
                                                        """
                                                        if not aCacheEntry.vUID:                                                  
                                                            aDiagnostics[ 'structure_entries_without_UID'].add( aCacheEntry)
                                                            self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'structure_entries_without_UID',])
                                                            
                                                        else:
                                                            unasEntriesByUID = self._fGetCachedEntriesByUID(  theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUID)
                                                            if not ( aCacheEntry in unasEntriesByUID):
                                                                aDiagnostics[ 'structure_entries_not_in_UID_registry'].add( aCacheEntry)
                                                                
                                                                self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'not_in_UID_registry',])

                                                
                                                
            elif aCacheKind == cCacheKind_ElementIndependent:
            
                # ###########################################################
                """Iterate over Projects
                
                """
                someProjectNames = self.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, aCacheName,)
                for aProjectName in someProjectNames:
                    someTemplatesByLanguageForProject = self.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)                              
                   
                    if not someTemplatesByLanguageForProject:
                        aDiagnostics[ 'structure_voids'].append( [ aProjectName,])
                        
                        
                        
                    # ###########################################################
                    """Iterate over Languages
                    
                    """
                    someLanguages =  ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or []
                    for aLanguage  in someLanguages:
                        someTemplatesByViewForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
                        
                   
                        if not someTemplatesByViewForLanguage:
                            aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage])
                            
                            
                        # ###########################################################
                        """Iterate over Views
                        
                        """                        
                        someViewNames = ( someTemplatesByViewForLanguage and someTemplatesByViewForLanguage.keys()) or []
                        for aViewName in someViewNames:
                            
                            
                            someTemplatesBySchemeHostAndDomainForView = someTemplatesByViewForLanguage.get( aViewName, {})
                              
                            if not someTemplatesBySchemeHostAndDomainForView:
                                aDiagnostics[ 'structure_voids'].append( [ aProjectName, aLanguage, aViewName, ])
                                                
                            
                            # ###########################################################
                            """Iterate over SchemeHostAndDomains
                            
                            """
                            someSchemeHostAndDomains = sorted( ( someTemplatesBySchemeHostAndDomainForView and someTemplatesBySchemeHostAndDomainForView.keys()) or [])
                            for aSchemeHostAndDomain in someSchemeHostAndDomains:
                            

                                         
                                # ########################
                                """Access CacheEntry
                                
                                """
                                aCacheEntry = someTemplatesBySchemeHostAndDomainForView.get( aSchemeHostAndDomain, None)
                            
                                if not aCacheEntry:
                                    # ########################
                                    """Report cache entry as missing
                                    
                                    """
                                    aDiagnostics[ 'structure_missing_entries'].append( [ aProjectName, aLanguage, aViewName, aSchemeHostAndDomain,])
                                    
                                    
                                else:
                                    
                                    if aCacheEntry in someCacheEntriesInStructure:
                                        aDiagnostics[ 'structure_entries_found_more_than_once'].add( aCacheEntry)
                                        self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'structure_entries_found_more_than_once',])
                                    
                                    else:                                                
                                        someCacheEntriesInStructure.add( aCacheEntry)
                                    
                                    if not aCacheEntry.vValid:
                                        aDiagnostics[ 'invalid_entries_in_list'].add( aCacheEntry)
                                        self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'Invalid',])
                                        
                                    aCacheEntryPromise = aCacheEntry.vPromise
                                    if aCacheEntryPromise and not ( aCacheEntryPromise == cCacheEntry_PromiseFulfilled_Sentinel):
                                        aDiagnostics[ 'promised_entries_in_list'].add( aCacheEntry)
    
                                    if not aCacheEntryPromise:
                                        aDiagnostics[ 'broken_promise_entries_in_list'].add( aCacheEntry)
                                        self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'BrokenPromise',])
                                        
                                        
                                        
                                    # ########################
                                    """Verify CacheEntry information consistent with the tree indexing data used to reach it, and report inconsistencies
                                    
                                    """
                                    someEntryInconsistenciesInTree = [ ]
                                    if ( not aCacheEntry.vProjectName) or not ( aCacheEntry.vProjectName == aProjectName):
                                        someEntryInconsistenciesInTree.append( [ 'vProjectName', aCacheEntry.vProjectName, aProjectName,])
                                    if ( not aCacheEntry.vLanguage)    or not ( aCacheEntry.vLanguage == aLanguage):
                                        someEntryInconsistenciesInTree.append( [ 'vLanguage',    aCacheEntry.vLanguage,    aLanguage,])
                                    if ( not aCacheEntry.vView )       or not (aCacheEntry.vView == aViewName):
                                        someEntryInconsistenciesInTree.append( [ 'vView',        aCacheEntry.vView,        aViewName,])
                                    if someEntryInconsistenciesInTree:
                                        aDiagnostics[ 'structure_inconsistent_entries'].append( [ aCacheEntry,              someEntryInconsistenciesInTree,])
                                         
                                        self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'inconsistencies_in_tree', someEntryInconsistenciesInTree,])
                                        
                                    # ########################
                                    """Verify CacheEntry properly registered by its unique id
                                    
                                    """
                                    unEntryByUniqueId = self._fGetCachedEntryById( theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUniqueId)
                                    if not unEntryByUniqueId or not ( unEntryByUniqueId == aCacheEntry):
                                        aDiagnostics[ 'structure_entries_not_in_uniqueid_registry'].add( aCacheEntry)
                                        
                                        self._pAppendEntryDefect( someEntriesWithProblems, aCacheEntry, [ 'not_in_uniqueid_registry',])
                                          
                                                                                           

                        
            # ########################
            """Verify that the list of entries ordered by last access time contains all entries reached by traversal, and no others
            
            """
            anUnwindHack = True
            while anUnwindHack:
                anUnwindHack = False
                    
                # ########################
                """Verify list sentinels
                
                """
                unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, aCacheName)
                if not unListNewSentinel:
                    aDiagnostics[ 'list_errors'].add( 'no_list_new_sentinel')
                    
                unListOldSentinel = self.fGetCacheStoreListSentinel_Old( theModelDDvlPloneTool, theContextualObject, aCacheName)
                if not unListOldSentinel:
                    aDiagnostics[ 'list_errors'].add( 'no_list_old_sentinel')
                    
                if ( unListNewSentinel and unListOldSentinel) and ( unListNewSentinel == unListOldSentinel):
                    aDiagnostics[ 'list_errors'].add( 'same_new_and_old_sentinels')
                    
                    
                    
                # ########################
                """Verify firsts and lasts links
                
                """
                anOldestEntry = unListOldSentinel.vNext
                if not anOldestEntry:
                    aDiagnostics[ 'list_errors'].add( 'old_sentinel_without_next')
                    
                aNewestEntry = unListNewSentinel.vPrevious
                if not aNewestEntry:
                    aDiagnostics[ 'list_errors'].add( 'new_sentinel_without_previous')
                    
                # ########################
                """Allow empty list
                
                """
                if ( anOldestEntry == unListNewSentinel) and ( aNewestEntry == unListOldSentinel):
                    break
                    
                    
                    
                # ########################
                """Traverse from old to new, stop if discontinued or found repeated entries
                
                """
                someEntriesFoundFromOldToNew = set()
                aCanCheckCointinuityOldToNew = False
                if anOldestEntry:
                    aCurrentEntry = anOldestEntry
                    
                    while aCurrentEntry:
                        if aCurrentEntry in someEntriesFoundFromOldToNew:
                            aDiagnostics[ 'found_fromOldToNew_moreThanOnce'].add( aCurrentEntry)
                            aDiagnostics[ 'list_errors'].add( 'scan_fromOldToNew_stopped_entryfoundMoreThanOnce')
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'fromOldToNew_moreThanOnce',])

                             
                            break
                        else:
                            someEntriesFoundFromOldToNew.add( aCurrentEntry)
                            aNextEntry = aCurrentEntry.vNext
                            if not aNextEntry:
                                aDiagnostics[ 'entries_WithtoutNext'].add( aCurrentEntry)
                                aDiagnostics[ 'list_errors'].add( 'scan_fromOldToNew_stopped_entryWithoutNext')
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'fromOldToNew_entryWithoutNext',])
                                
                                break
                              
                            else:
                                if aNextEntry == unListNewSentinel:
                                    aCanCheckCointinuityOldToNew = True
                                    break
                                aCurrentEntry = aNextEntry
                                                                                                    
                     
                                
                # ########################
                """Traverse from new to old, stop if discontinued or found repeated entries
                
                """
                someEntriesFoundFromNewToOld = set()
                aCanCheckCointinuityNewToOld = False
                if aNewestEntry:
                    aCurrentEntry = aNewestEntry
                               
                    while aCurrentEntry:
                        if aCurrentEntry in someEntriesFoundFromNewToOld:
                            aDiagnostics[ 'found_fromNewToOld_moreThanOnce'].add( aCurrentEntry)
                            aDiagnostics[ 'list_errors'].add( 'scan_fromNewToOld_stopped_entryfoundMoreThanOnce')
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'fromNewToOld_moreThanOnce',])
                            
                            break
                        else:
                            someEntriesFoundFromNewToOld.add( aCurrentEntry)
                            aPreviousEntry = aCurrentEntry.vPrevious
                            if not aPreviousEntry:
                                aDiagnostics[ 'entries_WithoutPrevious'].add( aCurrentEntry)
                                aDiagnostics[ 'list_errors'].add( 'scan_fromNewToOld_stopped_entryWithoutPrevious')
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'fromNewToOld_entryWithoutPrevious',])

                                break
                            
                            else:
                                if aPreviousEntry == unListOldSentinel:
                                    aCanCheckCointinuityNewToOld = True
                                    break
                                aCurrentEntry = aPreviousEntry
                             
                                
                                
                                
                                
                # ########################
                """Verify that the same entries are reached by traversing the list in both directions
                
                """
                someEntriesNotReachedInBothDirections = someEntriesFoundFromNewToOld.symmetric_difference( someEntriesFoundFromOldToNew)
                if someEntriesNotReachedInBothDirections:
                    aDiagnostics[ 'list_errors'].add( 'some_entries_not_reached_in_both_directions')
                    
                aDiagnostics[ 'linkedlist_size'] = max( len( someEntriesFoundFromNewToOld), len( someEntriesFoundFromOldToNew))

                aDiagnostics[ 'linkedlist_size_direction_difference'] = abs( len( someEntriesFoundFromNewToOld) - len( someEntriesFoundFromOldToNew))
                
                
                    
            
                
                
                # ########################
                """Traverse from old to new, check bidirectional entry links
                
                """
                if anOldestEntry and aCanCheckCointinuityOldToNew:
                    aCurrentEntry = anOldestEntry
                    
                    while aCurrentEntry:
                        
                        # ###################
                        """Check continuity with previous entry.
                        
                        """
                        aPreviousEntry = aCurrentEntry.vPrevious
                        if aPreviousEntry:
                            aPreviousEntryNext = aPreviousEntry.vNext
                            if not aPreviousEntryNext:
                                aDiagnostics[ 'entries_WithPrevious_NoNext'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_NoNext',])

                            elif not ( aPreviousEntryNext == aCurrentEntry):
                                aDiagnostics[ 'entries_WithPrevious_WrongNext'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])

                        else:
                            # ####################
                            """Should have been reported above, and this pass never executed.
                            
                            """
                            aDiagnostics[ 'entries_WithoutPrevious'].add( aCurrentEntry)
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithoutPrevious',])
                            break 

                        
                        # ###################
                        """Check continuity with next entry.
                        
                        """
                        aNextEntry = aCurrentEntry.vNext
                        if aNextEntry:
                            aNextEntryPrevious = aNextEntry.vPrevious
                            if not aNextEntryPrevious:
                                aDiagnostics[ 'entries_WithNext_NoPrevious'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithNext_NoPrevious',])
                                
                            elif not ( aNextEntryPrevious == aCurrentEntry):
                                aDiagnostics[ 'entries_WithNext_WrongPrevious'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithNext_WrongPrevious',])

                        else:
                            # ####################
                            """Should have been reported above, and this pass never executed.
                            
                            """
                            aDiagnostics[ 'entries_WithoutNext'].add( aCurrentEntry)
                            break 

                        # ###################
                        """Detect end reached ok
                        
                        """
                        if aNextEntry == unListNewSentinel:
                            break
                        aCurrentEntry = aNextEntry
               
                        
                        
             
                                
                # ########################
                """Traverse from new to old, check bidirectional entry links
                
                """
                if aNewestEntry and aCanCheckCointinuityNewToOld:
                    aCurrentEntry = aNewestEntry
                    
                    while aCurrentEntry:
                        
                        # ###################
                        """Check continuity with previous entry.
                        
                        """
                        aPreviousEntry = aCurrentEntry.vPrevious
                        if aPreviousEntry:
                            aPreviousEntryNext = aPreviousEntry.vNext
                            if not aPreviousEntryNext:
                                aDiagnostics[ 'entries_WithPrevious_NoNext'].add( aCurrentEntry)
                                
                                someEntryProblems = someProblematicEntriesAndDefects.get( aCurrentEntry, None)
                                if someEntryProblems == None:
                                    someEntryProblems = [ ]
                                    someProblematicEntriesAndDefects[ aCurrentEntry] = someEntryProblems
                                someEntryProblems.append( [ 'WithPrevious_NoNext',])
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])

                            elif not ( aPreviousEntryNext == aCurrentEntry):
                                aDiagnostics[ 'entries_WithPrevious_WrongNext'].add( aCurrentEntry)
                                
                                someEntryProblems = someProblematicEntriesAndDefects.get( aCurrentEntry, None)
                                if someEntryProblems == None:
                                    someEntryProblems = [ ]
                                    someProblematicEntriesAndDefects[ aCurrentEntry] = someEntryProblems
                                someEntryProblems.append( [ 'WithPrevious_WrongNext',])
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])
                                
                        else:
                            # ####################
                            """Should have been reported above, and this pass never executed.
                            
                            """
                            aDiagnostics[ 'entries_WithoutPrevious'].add( aCurrentEntry)
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithtoutPrevious',])
                            break 

                        
                        # ###################
                        """Check continuity with next entry.
                        
                        """
                        aNextEntry = aCurrentEntry.vNext
                        if aNextEntry:
                            aNextEntryPrevious = aNextEntry.vPrevious
                            if not aNextEntryPrevious:
                                aDiagnostics[ 'entries_WithNext_NoPrevious'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])
                            elif not ( aNextEntryPrevious == aCurrentEntry):
                                aDiagnostics[ 'entries_WithNext_WrongPrevious'].add( aCurrentEntry)
                                self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithPrevious_WrongNext',])

                        else:
                            # ####################
                            """Should have been reported above, and this pass never executed.
                            
                            """
                            aDiagnostics[ 'entries_WithtoutNext'].add( aCurrentEntry)
                            self._pAppendEntryDefect( someEntriesWithProblems, aCurrentEntry, [ 'WithtoutNext',])
                            break 

                        # ###################
                        """Detect end reached ok
                        
                        """
                        if aPreviousEntry == unListOldSentinel:
                            break
                        aCurrentEntry = aPreviousEntry
               
                        
            aLinkedListAndStructureSizeDifference = abs( len( aDiagnostics[ 'cacheEntriesInStructure']) - aDiagnostics[ 'linkedlist_size'])
            aDiagnostics[ 'structure_and_linkedlist_size_difference'] = aLinkedListAndStructureSizeDifference
                
                       
            aSuccess = ( not len( aDiagnostics[ 'entriesWithProblems'])) and \
                ( not len( aDiagnostics[ 'structure_missing_entries'])) and \
                ( not len( aDiagnostics[ 'structure_voids'])) and \
                ( not len( aDiagnostics[ 'structure_inconsistent_entries'])) and \
                ( not len( aDiagnostics[ 'structure_entries_found_more_than_once'])) and \
                ( not len( aDiagnostics[ 'structure_entries_without_UID'])) and \
                ( not len( aDiagnostics[ 'structure_entries_not_in_uniqueid_registry'])) and \
                ( not len( aDiagnostics[ 'structure_entries_not_in_UID_registry'])) and \
                ( not      aDiagnostics[ 'structure_and_linkedlist_size_difference']) and \
                ( not len( aDiagnostics[ 'list_errors'])) and \
                ( not len( aDiagnostics[ 'invalid_entries_in_list'])) and \
                ( not len( aDiagnostics[ 'broken_promise_entries_in_list'])) and \
                ( not      aDiagnostics[ 'linkedlist_size_direction_difference']) and \
                ( not len( aDiagnostics[ 'found_fromOldToNew_moreThanOnce'])) and \
                ( not len( aDiagnostics[ 'found_fromNewToOld_moreThanOnce'])) and \
                ( not len( aDiagnostics[ 'entries_WithNext_NoPrevious'])) and \
                ( not len( aDiagnostics[ 'entries_WithNext_WrongPrevious'])) and \
                ( not len( aDiagnostics[ 'entries_WithoutNext'])) and \
                ( not len( aDiagnostics[ 'entries_WithPrevious_NoNext'])) and \
                ( not len( aDiagnostics[ 'entries_WithPrevious_WrongNext'])) and \
                ( not len( aDiagnostics[ 'entries_WithoutPrevious'])) 
                
            aDiagnostics[ 'success'] = aSuccess
                        
            # ########################
            """Cache-specific verifications completed
            
            """                            
            allCacheEntriesInStructure_AllCaches.update( someCacheEntriesInStructure)
            
            allEntriesWithProblems_AllCaches.update( someEntriesWithProblems)                                    
            
            
        aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
        if not( aModelDDvlPloneTool_Retrieval == None):
                 
            # ########################
            """Retrieve elements name and type info from the UID catalog and check elements have been found for all entries UIDs
            
            """
            someElementsNamesByUID = {}
            if someUIDsElementsToRetrieve:
                someElementsNamesByUID =  aModelDDvlPloneTool_Retrieval.fElementsNamesByUID( someUIDsElementsToRetrieve, theContextualObject)
                
                for anUID in someUIDsElementsToRetrieve:
                    anElementNames = someElementsNamesByUID.get( anUID, None)
                    if not anElementNames:
                        allDiagnostics[ 'structures_UIDs_withoutElement'].add( anUID)
                    
               
                    
        
            

                         
        # ########################
        """Check consistency of data in the entries with elements name and type info retrieved from the UID catalog
        
        """
        for aCacheEntry in allCacheEntriesInStructure_AllCaches:
            
            aCacheName = aCacheEntry.vCacheName
            if aCacheName in someCacheNames:
                
                if aCacheEntry.fIsForElement():
                
                    anUID = aCacheEntry.vUID
                    if not anUID:
                        """Must have been already reported when scanning entries in the structures
                        
                        """
                        pass
    
                    else:
                        anElementNames = someElementsNamesByUID.get( anUID, None)
                        if not anElementNames:
                            allDiagnostics[ 'structures_UIDs_withoutElement'].add( anUID)
                            self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'WithoutElement_by_UID',])
                        
                        else:
                            someEntryInconsistenciesWithElement = [ ]   
                            
                            aTitle = anElementNames.get( 'Title', '')
                            if not ( aCacheEntry.vTitle == aTitle):
                                someEntryInconsistenciesWithElement.append( [ 'vTitle',            aCacheEntry.vTitle, aTitle,])
                                
                            aType = anElementNames.get( 'Type', '')
                            if not ( aCacheEntry.vArchetypeName == aType):
                                someEntryInconsistenciesWithElement.append( [ 'vArchetypeName',     aCacheEntry.vArchetypeName, aType,])
                                
                            aPortalType = anElementNames.get( 'portal_type', '')
                            if not ( aCacheEntry.vPortalType == aPortalType):   
                                someEntryInconsistenciesWithElement.append( [ 'vPortalType',        aCacheEntry.vPortalType, aPortalType,])
                                
                            anElementId = anElementNames.get( 'id', '')
                            if not ( aCacheEntry.vElementId == anElementId):   
                                someEntryInconsistenciesWithElement.append( [ 'vElementId',        aCacheEntry.vElementId, anElementId ,])
                                
                            if someEntryInconsistenciesWithElement:
                                allDiagnostics[ 'elementnames_inconsistent_entries'].append( [ aCacheEntry, someEntryInconsistenciesWithElement,])
                                self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'inconsistent_with_element', someEntryInconsistenciesWithElement])
                                            
                        
                        
                

                             
        # ########################
        """Verify that the registry of entries by Unique entry Id does not contain entries for the considered caches, that have not been reached through structure traversal
        
        """
        aCachedEntriesByUniqueId = self._fGetCachedEntriesById_Copy( theModelDDvlPloneTool, theContextualObject,)
        
        someUniqueIds = aCachedEntriesByUniqueId.keys()
        allDiagnostics[ 'uniqueIDs_registry_size'] = len( someUniqueIds)
        
        for aUniqueId in someUniqueIds:
            
            aCacheEntry = aCachedEntriesByUniqueId.get( aUniqueId, None)
            if aCacheEntry:
                
                aCacheName = aCacheEntry.vCacheName
                if aCacheName in someCacheNames:
                    if not ( aCacheEntry in allCacheEntriesInStructure_AllCaches):
                        allDiagnostics[ 'entriesByUniqueId_Not_in_structure'].add( aCacheEntry)
                        self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'EntryInUniqueIdsRegistry_NotInStructure',])
                    
                if not aCacheEntry.vValid:
                    allDiagnostics[ 'invalid_entries_in_UniqueId_registry'].add( aCacheEntry)
                    self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'Invalid',])
                    
                aCacheEntryPromise = aCacheEntry.vPromise
                if not aCacheEntryPromise:
                    allDiagnostics[ 'broken_promise_entries_in_UniqueId_registry'].add( aCacheEntry)
                    self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'BrokenPromise',])
                        
                    
                         
        # ########################
        """Count number of UIDs and number of entries in the UID registry
        
        """
        aCachedEntriesByUID = self._fGetCachedEntriesByUID_Copy( theModelDDvlPloneTool, theContextualObject,)
        
        someUIDs= aCachedEntriesByUID.keys()
        allDiagnostics[ 'UIDs_registry_size'] = len( someUIDs)
        
        aNumEntriesInUIDRegistry = 0
        for aUID in someUIDs:
            aNumEntriesInUIDRegistry += len( aCachedEntriesByUID.get( aUID, []))
        
        allDiagnostics[ 'numentries_in_UIDs_registry'] = aNumEntriesInUIDRegistry
            
        # ########################
        """Only if all caches have been scanned, Verify that the registry of entries by UID does not contain entries for the considered caches, that have not been reached through structure traversal
        
        """
        if ( set( someCacheNames).intersection( set( cCacheNamesForElementsOrUsers))) == set( cCacheNamesForElementsOrUsers):
            for aUID in someUIDs:
                
                someCachedEntries = aCachedEntriesByUID.get( aUID, [])
                for aCacheEntry in someCachedEntries:
                    if aCacheEntry:
                        if not ( aCacheEntry in allCacheEntriesInStructure_AllCaches):
                            allDiagnostics[ 'entriesByUID_Not_in_structure'].add( aCacheEntry)
                            self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'EntryInUIDsRegistry_NotInStructure',])
                            
                        if not aCacheEntry.vValid:
                            allDiagnostics[ 'invalid_entries_in_UID_registry'].add( aCacheEntry)
                            self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'Invalid',])
                            
                        aCacheEntryPromise = aCacheEntry.vPromise
                        if not aCacheEntryPromise:
                            allDiagnostics[ 'broken_promise_entries_in_UID_registry'].add( aCacheEntry)
                            self._pAppendEntryDefect( allEntriesWithProblems_AllCaches, aCacheEntry, [ 'BrokenPromise',])
                            

        aSuccess = True
        for aCacheDiagnostics in allDiagnostics[ 'caches_diagnostics'].values():
            if not aCacheDiagnostics[ 'success']:
                aSuccess = False
                break
            
        aSuccess = aSuccess and ( not len( allDiagnostics[ 'allEntriesWithProblems'])) and \
            ( not len( allDiagnostics[ 'structures_UIDs_withoutElement'])) and \
            ( not len( allDiagnostics[ 'entriesByUniqueId_Not_in_structure'])) and \
            ( not len( allDiagnostics[ 'entriesByUID_Not_in_structure'])) and \
            ( not len( allDiagnostics[ 'elementnames_inconsistent_entries'])) and \
            ( not len( allDiagnostics[ 'invalid_entries_in_UID_registry'])) and \
            ( not len( allDiagnostics[ 'invalid_entries_in_UniqueId_registry'])) and \
            ( not len( allDiagnostics[ 'broken_promise_entries_in_UniqueId_registry'])) and \
            ( not len( allDiagnostics[ 'broken_promise_entries_in_UID_registry'])) 
        
        

        
            
        allDiagnostics[ 'success'] = aSuccess
        
        return allDiagnostics
    
    
    
    
    
    
    security.declarePrivate( '_pAppendEntryDefect')
    def _pAppendEntryDefect(self, theDefectsRegistry, theCacheEntry, theDefect):
     
        if theDefectsRegistry == None:
            return self
        
        if not theCacheEntry:
            return self
        
        if not theDefect:
            return self
        
        someEntryDefects = theDefectsRegistry.get( theCacheEntry, None)
        if someEntryDefects == None:
            someEntryDefects = [ ]
            theDefectsRegistry[ theCacheEntry] = someEntryDefects
            
        someEntryDefects.append( theDefect)
        
        return self
    