# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_VoidResults.py
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








    
class ModelDDvlPloneTool_Cache_VoidResults:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the configuration of cache operation parameters.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    

    
    
        
    security.declarePrivate( 'fNewVoidCacheStatusReport')
    def fNewVoidCacheStatusReport(self, ):
        unReport = {
            'StatusReportTime':              None,

            'CanActivateOrDeactivate':       False,
            'CanReset':                      False,
            'CanConfigure':                  False,
            'CanFlush':                      False,
            'CanEnableOrDisable':            False,
            
            'CacheStartupTime':              0,
                          
            'IsCachingActive':               False,                    
            'PeersToNotify':                 '',                    
            'IdentificationStringForPeers':  '',
            'AuthenticationStringForPeers':  '',
            'AuthenticationStringFromPeers': '',
            
            'reports':                       [],
            
            'reports_repr':                  '',
        }
        return unReport
    
    
        
    
    
    
        
    security.declarePrivate( 'fNewVoidCacheReport')
    def fNewVoidCacheReport(self, ):
        unReport = {
            'meta_info':                                None,           
            'CacheName':                                '',             
            'CacheKind':                                '',             
            'CacheEnabled':                             False,          
            'MaxCharsCached':                           0,              
            'MinThresholdCharsToRelease':               0,              
            'DisplayCacheHitInformation':               '',             
            'ExpireAfterSeconds':                       0,              
            'ForceExpire':                              False,          
                                                                      
            'CacheDiskEnabled':                         False,          
            'CacheDiskPath':                            '',             
            'ExpireDiskAfterSeconds':                   0,              
                                                                      
            'MaxCharsCached_str':                       '0',            
            'MinThresholdCharsToRelease_str':           '0',            
            'ExpireAfterSeconds_str':                   '0',            
            'ExpireAfterSeconds_wstr':                  '0 s',          
                                                                      
            'ExpireDiskAfterSeconds_str':               '0',            
            'ExpireDiskAfterSeconds_wstr':              '0 s',          
                                                                      
                                                                      
            'LastFlushDate':                            '',             
            'LastFlushingUser':                         '',             
                                                                        
            'TotalCacheEntries':                        0,              
            'TotalCharsCached':                         0,              
            'TotalCacheHits':                           0,              
            'TotalCacheFaults':                         0,              
            'TotalCacheDiskHits':                       0,              
            'TotalRenderings':                          0,                
                                                                      
            'TotalCharsSaved':                          0,              
            'TotalTimeSaved':                           0,              
                                                                        
            'TotalCacheEntries_str':                    '0',            
            'TotalCharsCached_str':                     '0',            
            'TotalCacheHits_str':                       '0',            
            'TotalCacheFaults_str':                     '0',            
            'TotalCacheDiskHits_str':                   '0',            
            'TotalRenderings_str':                      '0',            
            'TotalCharsSaved_str':                      '0',            
            'TotalTimeSaved_str':                       '0',  
            
        }
        return unReport
    
    
    
    
    
    

    
    
    
    
       
    security.declarePrivate( 'fNewVoidAllCachesDiagnostics')
    def fNewVoidAllCachesDiagnostics(self, ):
        aDiagnostics = {
            'success':                                     False,
            'UIDs_registry_size':                          0,
            'numentries_in_UIDs_registry':                 0,
            'uniqueIDs_registry_size':                     0,
            'allcacheEntriesInStructures':                 set( ),
            'allEntriesWithProblems':                      { },
            'structures_UIDs_withoutElement':              set( ),
            'entriesByUniqueId_Not_in_structure':          set( ),
            'entriesByUID_Not_in_structure':               set( ),
            'UIDs_without_corresponding_elements':         set( ),
            'elementnames_inconsistent_entries':           [ ],
            'invalid_entries_in_UID_registry':             set( ),
            'invalid_entries_in_UniqueId_registry':        set( ),
            'broken_promise_entries_in_UniqueId_registry': set( ),
            'broken_promise_entries_in_UID_registry':      set( ),
            'caches_diagnostics':                          { },
        }
        return aDiagnostics
    
     
        
    
       
    security.declarePrivate( 'fNewVoidCacheDiagnostic')
    def fNewVoidCacheDiagnostic(self, ):
        aDiagnostics = {
            'cache_kind':                                  '',
            'cache_name':                                  '',
            'success':                                     False,
            'cacheEntriesInStructure':                     set( ),      #
            'entriesWithProblems':                         { },         #
            'structure_missing_entries':                   [ ],     #   #
            'structure_voids':                             [ ],     #   #
            'structure_inconsistent_entries':              [ ],     #   #
            'structure_entries_found_more_than_once':      set( ),  #   #
            'structure_entries_not_in_uniqueid_registry':  set( ),  #   #
            'structure_entries_without_UID':               set( ),  #   #
            'structure_entries_not_in_UID_registry':       set( ),  #   #
            'linkedlist_size':                             0,           #
            'structure_and_linkedlist_size_difference':    0,       #   #
            'list_errors':                                 [ ],     #   #
            'invalid_entries_in_list':                     set( ),  #   #
            'promised_entries_in_list':                    set( ),
            'broken_promise_entries_in_list':              set( ),  #   #
            'linkedlist_size_direction_difference':        0,       #   #
            'found_fromOldToNew_moreThanOnce':             set( ),  #   #
            'found_fromNewToOld_moreThanOnce':             set( ),  #   #        
            'entries_WithNext_NoPrevious':                 set( ),  #   #
            'entries_WithNext_WrongPrevious':              set( ),  #   #
            'entries_WithoutNext':                         set( ),  #   #
            'entries_WithPrevious_NoNext':                 set( ),  #   #
            'entries_WithPrevious_WrongNext':              set( ),  #   #
            'entries_WithoutPrevious':                     set( ),  #   #
            
        }
        return aDiagnostics

    
        
    
    
    
    
    
   
    

    
    
    security.declarePrivate( '_fNewVoidRenderResult_Phase_TryMemory')
    def _fNewVoidRenderResult_Phase_TryMemory(self, ):
        aResult = {
            'status':              cRenderStatus_NotExecuted,
            'error':               None,
            'rendered_html':       None,
            'cache_name':          None,
            'promise_made':        None,
            'promise_holder':      None,
            'promise_key':         None,
        }
        return aResult
        
        
    

     
    security.declarePrivate( '_fNewVoidRenderResult_Phase_TryDisk')
    def _fNewVoidRenderResult_Phase_TryDisk(self, ):
        aResult = {
            'status':              cRenderStatus_NotExecuted,
            'error':               None,
            'rendered_html':       None,
        }     
        
        return aResult
            
         
        

     
    security.declarePrivate( '_fNewVoidRenderResult_Phase_Render')
    def _fNewVoidRenderResult_Phase_Render(self, ):
        aResult = {
            'status':              cRenderStatus_NotExecuted,
            'error':               None,
            'rendered_html':       None,
        }     
        
        return aResult
            
         
       
    
    
    security.declarePrivate( '_fNewVoidCachedEntryInWrongStateInfo')
    def _fNewVoidCachedEntryInWrongStateInfo(self, ):
        aCachedEntryInWrongStateInfo = {
            'cached_entry':        None,
            'cached_entry_holder': None,
            'cached_entry_key':    None,            
        }
        return aCachedEntryInWrongStateInfo
   
    
             