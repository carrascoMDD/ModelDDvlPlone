# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_Status.py
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


from ModelDDvlPloneToolSupport                  import fEvalString, fReprAsString, fMillisecondsNow, fMillisecondsToDateTime





# #######################################################
# #######################################################








    
class ModelDDvlPloneTool_Cache_Status:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the configuration of cache operation parameters.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    


    
        
    
    security.declarePrivate( 'fRetrieveCacheStatusReport')
    def fRetrieveCacheStatusReport(self, theModelDDvlPloneTool, theContextualObject, theRepresentation=''):
        """Retrieve a report with the status of the templates cache, containing the number of entries, the amount of memory occupied, and statistics of cache hits and faults.
        
        """
        
        unCacheStatusReport = self.fNewVoidCacheStatusReport()
            
        if theContextualObject == None:
            return unCacheStatusReport
        
        aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
        if aModelDDvlPloneTool_Retrieval == None:
            return unCacheStatusReport

        aCacheConfig_ElementIndependent     = theModelDDvlPloneTool.fGetCacheConfigCopy( theContextualObject, cCacheName_ElementIndependent)
        aCacheStatistics_ElementIndependent = self.fGetCacheStatisticsCopy( theModelDDvlPloneTool, theContextualObject,cCacheName_ElementIndependent)

        aCacheConfig_ForElements            = theModelDDvlPloneTool.fGetCacheConfigCopy( theContextualObject, cCacheName_ForElements)        
        aCacheStatistics_ForElements        = self.fGetCacheStatisticsCopy( theModelDDvlPloneTool, theContextualObject, cCacheName_ForElements)
        
        
        anAllCachesConfig = theModelDDvlPloneTool.fGetAllCachesConfigCopy( theContextualObject, )
        
        
        
        unAhoraMillis = fMillisecondsNow()
        unAhora       = fMillisecondsToDateTime( unAhoraMillis)
        
        someCacheReports = unCacheStatusReport[ 'reports']
        unCacheStatusReport.update( {
            'StatusReportTime':              unAhora,

            'CanActivateOrDeactivate':       False,
            'CanReset':                      False,
            'CanConfigure':                  False,
            'CanFlush':                      False,
            'CanEnableOrDisable':            False,
            
            'CacheStartupTime':              fMillisecondsToDateTime( theModelDDvlPloneTool.fgCacheStartupTime_Holder( theContextualObject)[ 0].millis()),
                          
            'IsCachingActive':               anAllCachesConfig[ cAllCachesConfigPpty_IsCachingActive],                    
            'PeersToNotify':                 anAllCachesConfig[ cAllCachesConfigPpty_PeersToNotify],                    
            'IdentificationStringForPeers':  anAllCachesConfig[ cAllCachesConfigPpty_IdentificationStringForPeers],                    
            'AuthenticationStringForPeers':  anAllCachesConfig[ cAllCachesConfigPpty_AuthenticationStringForPeers],                    
            'AuthenticationStringFromPeers': anAllCachesConfig[ cAllCachesConfigPpty_AuthenticationStringFromPeers], 
        })
        
        
        
        someCacheNames = self.fGetCacheStoreNames( theModelDDvlPloneTool, theContextualObject, )
        
        for aCacheName in someCacheNames:
            
            aCacheConfig               = theModelDDvlPloneTool.fGetCacheConfigCopy( theContextualObject, aCacheName)
            aCacheStatistics           = self.fGetCacheStatisticsCopy( theModelDDvlPloneTool, theContextualObject, aCacheName)
            aCacheStatusReportMetaInfo = self.fCacheConfigurationMetaInfo( theModelDDvlPloneTool, theContextualObject, aCacheName)        
            
            unCacheReport = self.fNewVoidCacheReport()
            unCacheReport.update( {
                'meta_info':                                      aCacheStatusReportMetaInfo,
                'CacheName':                                      aCacheName,
                'CacheKind':                                      self.fCacheStoreKind( theModelDDvlPloneTool, theContextualObject, aCacheName),
                cCacheConfigPpty_CacheEnabled:                    aCacheConfig[ cCacheConfigPpty_CacheEnabled] == True,
                cCacheConfigPpty_MaxCharsCached:                  aCacheConfig[ cCacheConfigPpty_MaxCharsCached], 
                cCacheConfigPpty_MinThresholdCharsToRelease:      aCacheConfig[ cCacheConfigPpty_MinThresholdCharsToRelease], 
                cCacheConfigPpty_DisplayCacheHitInformation:      aCacheConfig[ cCacheConfigPpty_DisplayCacheHitInformation], 
                cCacheConfigPpty_ExpireAfterSeconds:              aCacheConfig[ cCacheConfigPpty_ExpireAfterSeconds], 
                cCacheConfigPpty_ForceExpire:                     aCacheConfig[ cCacheConfigPpty_ForceExpire]  == True, 

                cCacheConfigPpty_CacheDiskEnabled:                aCacheConfig[ cCacheConfigPpty_CacheDiskEnabled] == True,
                cCacheConfigPpty_CacheDiskPath:                   aCacheConfig[ cCacheConfigPpty_CacheDiskPath] or '',
                cCacheConfigPpty_ExpireDiskAfterSeconds:          aCacheConfig[ cCacheConfigPpty_ExpireDiskAfterSeconds], 
    
                'MaxCharsCached_str':                             fStrGrp( aCacheConfig[ cCacheConfigPpty_MaxCharsCached]), 
                'MinThresholdCharsToRelease_str':                 fStrGrp( aCacheConfig[ cCacheConfigPpty_MinThresholdCharsToRelease]), 
                'ExpireAfterSeconds_str':                         fStrGrp( aCacheConfig[ cCacheConfigPpty_ExpireAfterSeconds]), 
                'ExpireAfterSeconds_wstr':                        fStrTime( aCacheConfig[ cCacheConfigPpty_ExpireAfterSeconds]), 
                
                'ExpireDiskAfterSeconds_str':                     fStrGrp( aCacheConfig[ cCacheConfigPpty_ExpireDiskAfterSeconds]), 
                'ExpireDiskAfterSeconds_wstr':                    fStrTime( aCacheConfig[ cCacheConfigPpty_ExpireDiskAfterSeconds]), 
                
                
                cCacheStatistics_LastFlushDate:                   aCacheStatistics[ cCacheStatistics_LastFlushDate],
                cCacheStatistics_LastFlushingUser:                aCacheStatistics[ cCacheStatistics_LastFlushingUser],
                                                                  
                cCacheStatistics_TotalCacheEntries:               aCacheStatistics[ cCacheStatistics_TotalCacheEntries],
                cCacheStatistics_TotalCharsCached:                aCacheStatistics[ cCacheStatistics_TotalCharsCached],
                cCacheStatistics_TotalCacheHits:                  aCacheStatistics[ cCacheStatistics_TotalCacheHits],
                cCacheStatistics_TotalCacheFaults:                aCacheStatistics[ cCacheStatistics_TotalCacheFaults],
                cCacheStatistics_TotalCacheDiskHits:              aCacheStatistics[ cCacheStatistics_TotalCacheDiskHits],
                cCacheStatistics_TotalRenderings:                 aCacheStatistics[ cCacheStatistics_TotalRenderings],
                cCacheStatistics_TotalCharsSaved:                 aCacheStatistics[ cCacheStatistics_TotalCharsSaved],
                cCacheStatistics_TotalTimeSaved:                  int( aCacheStatistics[ cCacheStatistics_TotalTimeSaved] / 1000),
                
                cCacheStatistics_TotalEntriesFlushed:             aCacheStatistics[ cCacheStatistics_TotalEntriesFlushed], 
                cCacheStatistics_TotalCharsFlushed:               aCacheStatistics[ cCacheStatistics_TotalCharsFlushed],    
                cCacheStatistics_TotalFilesWritten:               aCacheStatistics[ cCacheStatistics_TotalFilesWritten],   
                cCacheStatistics_TotalCharsWritten:               aCacheStatistics[ cCacheStatistics_TotalCharsWritten],    
                cCacheStatistics_TotalFilesCleared:               aCacheStatistics[ cCacheStatistics_TotalFilesCleared],    
                cCacheStatistics_TotalCharsDiskFreed:             aCacheStatistics[ cCacheStatistics_TotalCharsDiskFreed],      
                
                                                                  
                'TotalCacheEntries_str':                          fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCacheEntries]),
                'TotalCharsCached_str':                           fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsCached]),
                'TotalCacheHits_str':                             fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCacheHits]),
                'TotalCacheFaults_str':                           fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCacheFaults]),
                'TotalCacheDiskHits_str':                         fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCacheDiskHits]),
                'TotalRenderings_str':                            fStrGrp( aCacheStatistics[ cCacheStatistics_TotalRenderings]),
                'TotalCharsSaved_str':                            fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsSaved]),
                'TotalTimeSaved_str':                             fStrGrp( int( aCacheStatistics[ cCacheStatistics_TotalTimeSaved] / 1000)),
                
                cCacheStatistics_TotalEntriesFlushed + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalEntriesFlushed]), 
                cCacheStatistics_TotalCharsFlushed   + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsFlushed]),    
                cCacheStatistics_TotalFilesWritten   + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalFilesWritten]),   
                cCacheStatistics_TotalCharsWritten   + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsWritten]),    
                cCacheStatistics_TotalFilesCleared   + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalFilesCleared]),    
                cCacheStatistics_TotalCharsDiskFreed + '_str':    fStrGrp( aCacheStatistics[ cCacheStatistics_TotalCharsDiskFreed]),      
                
                'ReportTime':                                     unAhoraMillis,
                'ReportTime_str':                                 str( fMillisecondsToDateTime( unAhoraMillis)),
            })
            
            unCacheReport.update( {
                'meta_info':      aCacheStatusReportMetaInfo,
            })
            
            someCacheReports.append(  unCacheReport)

            
        unCacheReportRepresentation = fReprAsString( someCacheReports)
        if unCacheReportRepresentation:
            unCacheStatusReport[ 'reports_repr'] = unCacheReportRepresentation
            
            
            
        unosPreviousStatusReports = None
        if theRepresentation:
            aRepresentationValue = fEvalString( theRepresentation)
            if aRepresentationValue:
                if isinstance( aRepresentationValue, list) or isinstance( aRepresentationValue, tuple):
                    unosPreviousStatusReports = aRepresentationValue
        
        
        if unosPreviousStatusReports:   
            self.pDeltaStatusReports( theModelDDvlPloneTool, unosPreviousStatusReports, someCacheReports)
            
            
            
        
        unElementoRaiz = None
        try:
            unElementoRaiz = theContextualObject.getRaiz()
        except:
            None
        if unElementoRaiz == None:
            return unCacheStatusReport
            
        unHasManagePortalPermission = aModelDDvlPloneTool_Retrieval.fCheckElementPermission( unElementoRaiz, permissions.ManagePortal, None )
        unHasManagerRole            = aModelDDvlPloneTool_Retrieval.fRoleQuery_IsAnyRol(     'Manager', unElementoRaiz, )

        if not cForbidCaches:
            
            unCanActivateOrDeactivate = unHasManagePortalPermission or unHasManagerRole
            if not unCanActivateOrDeactivate:
                unPortalObject = aModelDDvlPloneTool_Retrieval.fPortalRoot( theContextualObject)
                if not(  unPortalObject == None):
            
                    unHasManagePortalPermission = unHasManagePortalPermission or aModelDDvlPloneTool_Retrieval.fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
                    unHasManagerRole            = unHasManagerRole            or aModelDDvlPloneTool_Retrieval.fRoleQuery_IsAnyRol(     'Manager', unPortalObject, )
                      
                    unCanActivateOrDeactivate = unHasManagePortalPermission or unHasManagerRole
            
            unCacheStatusReport.update( {
                'CanActivateOrDeactivate':                        unCanActivateOrDeactivate,
            })
        
            
            unCanDiagnose = unHasManagePortalPermission or unHasManagerRole
            if not unCanDiagnose:
                unPortalObject = aModelDDvlPloneTool_Retrieval.fPortalRoot( theContextualObject)
                if not(  unPortalObject == None):
            
                    unHasManagePortalPermission = unHasManagePortalPermission or aModelDDvlPloneTool_Retrieval.fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
                    unHasManagerRole            = unHasManagerRole            or aModelDDvlPloneTool_Retrieval.fRoleQuery_IsAnyRol(     'Manager', unPortalObject, )
                      
                    unCanDiagnose = unHasManagePortalPermission or unHasManagerRole
            
            unCacheStatusReport.update( {
                'CanDiagnose':                        unCanDiagnose,
            })
            
            
            unCanInspect = unHasManagePortalPermission or unHasManagerRole
            if not unCanInspect:
                unPortalObject = aModelDDvlPloneTool_Retrieval.fPortalRoot( theContextualObject)
                if not(  unPortalObject == None):
            
                    unHasManagePortalPermission = unHasManagePortalPermission or aModelDDvlPloneTool_Retrieval.fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
                    unHasManagerRole            = unHasManagerRole            or aModelDDvlPloneTool_Retrieval.fRoleQuery_IsAnyRol(     'Manager', unPortalObject, )
                      
                    unCanInspect = unHasManagePortalPermission or unHasManagerRole
            
            unCacheStatusReport.update( {
                'CanInspect':                        unCanInspect,
            })
            
                    
            if anAllCachesConfig[ cAllCachesConfigPpty_IsCachingActive]:
                unCanConfigure =  unHasManagePortalPermission or unHasManagerRole
                
                if not unCanConfigure:
                    unPortalObject = aModelDDvlPloneTool_Retrieval.fPortalRoot( theContextualObject)
                    if not( unPortalObject == None):
                
                        unHasManagePortalPermission = unHasManagePortalPermission or aModelDDvlPloneTool_Retrieval.fCheckElementPermission( unPortalObject, permissions.ManagePortal, None )
                        unHasManagerRole            = unHasManagerRole            or aModelDDvlPloneTool_Retrieval.fRoleQuery_IsAnyRol(     'Manager', unPortalObject, )
                          
                        unCanConfigure = unHasManagePortalPermission or unHasManagerRole
                
                unCacheStatusReport.update( {
                    'CanConfigure':            unCanConfigure,
                    'CanReset':                unCanConfigure,
                    'CanFlush':                unCanConfigure,
                    'CanEnableOrDisable':      unCanConfigure,
                })
                    
        return unCacheStatusReport
    


    
    

    security.declarePrivate( 'pDeltaStatusReports')
    def pDeltaStatusReports(self, theModelDDvlPloneTool, thePreviousStatusReports, theNewStatusReports):
        
        for unNewStatusReport in theNewStatusReports:
            
            unNewCacheName = unNewStatusReport.get( 'CacheName', '')
            if unNewCacheName:
                unPreviousStatusReport = None
                for unStatusReport in thePreviousStatusReports:
                    if unStatusReport:
                        unCacheName = unStatusReport.get( 'CacheName', '')
                        if unCacheName and ( unCacheName == unNewCacheName):
                            unPreviousStatusReport = unStatusReport
                            break

            if unPreviousStatusReport:
         
                unNewStatusReport.update( {
                                                                  
                    'TotalCacheEntries_Delta':       unNewStatusReport[ cCacheStatistics_TotalCacheEntries]                     - unPreviousStatusReport.get( cCacheStatistics_TotalCacheEntries, 0),
                    'TotalCharsCached_Delta':        unNewStatusReport[ cCacheStatistics_TotalCharsCached]                      - unPreviousStatusReport.get( cCacheStatistics_TotalCharsCached, 0),                      
                    'TotalCacheHits_Delta':          unNewStatusReport[ cCacheStatistics_TotalCacheHits]                        - unPreviousStatusReport.get( cCacheStatistics_TotalCacheHits, 0),                        
                    'TotalCacheFaults_Delta':        unNewStatusReport[ cCacheStatistics_TotalCacheFaults]                      - unPreviousStatusReport.get( cCacheStatistics_TotalCacheFaults, 0),                      
                    'TotalCacheDiskHits_Delta':      unNewStatusReport[ cCacheStatistics_TotalCacheDiskHits]                    - unPreviousStatusReport.get( cCacheStatistics_TotalCacheDiskHits, 0),                    
                    'TotalRenderings_Delta':         unNewStatusReport[ cCacheStatistics_TotalRenderings]                       - unPreviousStatusReport.get( cCacheStatistics_TotalRenderings, 0),                       
                                                                                                                                                                                                   
                    'TotalCharsSaved_Delta':         unNewStatusReport[ cCacheStatistics_TotalCharsSaved]                       - unPreviousStatusReport.get( cCacheStatistics_TotalCharsSaved, 0),                       
                    'TotalTimeSaved_Delta':          int( unNewStatusReport[ cCacheStatistics_TotalTimeSaved] / 1000)           - int( unPreviousStatusReport.get( cCacheStatistics_TotalTimeSaved, 0) / 1000),           
                        
                    cCacheStatistics_TotalEntriesFlushed + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalEntriesFlushed]- unPreviousStatusReport.get( cCacheStatistics_TotalEntriesFlushed, 0),
                    cCacheStatistics_TotalCharsFlushed   + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalCharsFlushed]  - unPreviousStatusReport.get( cCacheStatistics_TotalCharsFlushed, 0),
                    cCacheStatistics_TotalFilesWritten   + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalFilesWritten]  - unPreviousStatusReport.get( cCacheStatistics_TotalFilesWritten, 0),
                    cCacheStatistics_TotalCharsWritten   + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalCharsWritten]  - unPreviousStatusReport.get( cCacheStatistics_TotalCharsWritten, 0),
                    cCacheStatistics_TotalFilesCleared   + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalFilesCleared]  - unPreviousStatusReport.get( cCacheStatistics_TotalFilesCleared, 0),
                    cCacheStatistics_TotalCharsDiskFreed + '_Delta':    unNewStatusReport[ cCacheStatistics_TotalCharsDiskFreed]- unPreviousStatusReport.get( cCacheStatistics_TotalCharsDiskFreed, 0),

                                        
                    'TotalCacheEntries_Delta_str':   fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCacheEntries]           - unPreviousStatusReport.get( cCacheStatistics_TotalCacheEntries, 0)),           
                    'TotalCharsCached_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsCached]            - unPreviousStatusReport.get( cCacheStatistics_TotalCharsCached, 0)),            
                    'TotalCacheHits_Delta_str':      fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCacheHits]              - unPreviousStatusReport.get( cCacheStatistics_TotalCacheHits, 0)),              
                    'TotalCacheFaults_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCacheFaults]            - unPreviousStatusReport.get( cCacheStatistics_TotalCacheFaults, 0)),            
                    'TotalCacheDiskHits_Delta_str':  fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCacheDiskHits]          - unPreviousStatusReport.get( cCacheStatistics_TotalCacheDiskHits, 0)),          
                    'TotalRenderings_Delta_str':     fStrGrp( unNewStatusReport[ cCacheStatistics_TotalRenderings]             - unPreviousStatusReport.get( cCacheStatistics_TotalRenderings, 0)),             
                    'TotalCharsSaved_Delta_str':     fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsSaved]             - unPreviousStatusReport.get( cCacheStatistics_TotalCharsSaved, 0)),             
                    'TotalTimeSaved_Delta_str':      fStrGrp( int( unNewStatusReport[ cCacheStatistics_TotalTimeSaved] / 1000) - int( unPreviousStatusReport.get( cCacheStatistics_TotalTimeSaved, 0) / 1000)), 
                    
                    
                    cCacheStatistics_TotalEntriesFlushed + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalEntriesFlushed]- unPreviousStatusReport.get( cCacheStatistics_TotalEntriesFlushed, 0)),
                    cCacheStatistics_TotalCharsFlushed   + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsFlushed]  - unPreviousStatusReport.get( cCacheStatistics_TotalCharsFlushed, 0)),
                    cCacheStatistics_TotalFilesWritten   + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalFilesWritten]  - unPreviousStatusReport.get( cCacheStatistics_TotalFilesWritten, 0)),
                    cCacheStatistics_TotalCharsWritten   + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsWritten]  - unPreviousStatusReport.get( cCacheStatistics_TotalCharsWritten, 0)),
                    cCacheStatistics_TotalFilesCleared   + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalFilesCleared]  - unPreviousStatusReport.get( cCacheStatistics_TotalFilesCleared, 0)),
                    cCacheStatistics_TotalCharsDiskFreed + '_Delta_str':    fStrGrp( unNewStatusReport[ cCacheStatistics_TotalCharsDiskFreed]- unPreviousStatusReport.get( cCacheStatistics_TotalCharsDiskFreed, 0)),

                    
                    'PreviousReportTime':            unPreviousStatusReport.get( 'ReportTime', 0),
                    'PreviousReportTime_str':        str( fMillisecondsToDateTime( unPreviousStatusReport.get( 'ReportTime', 0))),
                    
                    'ReportTime_Delta':              int( unNewStatusReport[ 'ReportTime'] / 1000)                             -  int( unPreviousStatusReport.get( 'ReportTime', 0) / 1000),                                                             
                    'ReportTime_Delta_str':          fStrGrp( int( unNewStatusReport[ 'ReportTime'] / 1000)                    -  int( unPreviousStatusReport.get( 'ReportTime', 0) / 1000)),                                                             
                    'ReportTime_Delta_wstr':         fStrTime( int( unNewStatusReport[ 'ReportTime'] / 1000)                    -  int( unPreviousStatusReport.get( 'ReportTime', 0) / 1000)),                                                             
                })
              
                
        return self
    
        
        
        
        