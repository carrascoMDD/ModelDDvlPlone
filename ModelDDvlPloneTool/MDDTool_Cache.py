# -*- coding: utf-8 -*-
#
# File: MDDTool_Cache.py
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









class MDDTool_Cache:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """

    
    security = ClassSecurityInfo()
    
    
    


    
    

    
    # #############################################################
    """Cache configuration editing and status reporting.
    
    """


     
    
    security.declareProtected( permissions.View, 'fRetrieveCacheStatusReport')
    def fRetrieveCacheStatusReport(self, theContextualObject, theRepresentation=''):
        """Retrieve a report with the status of the templates cache, containing the number of entries, the amount of memory occupied, and statistics of cache hits and faults.
        
        """
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fRetrieveCacheStatusReport( self, theContextualObject,theRepresentation=theRepresentation)


        
    
    
    security.declareProtected( permissions.ManagePortal, 'fActivateCaching')
    def fActivateCaching(self, theContextualObject, theCacheName,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fActivateCaching( self, theContextualObject)
        

        
    
        
    
    security.declareProtected( permissions.ManagePortal, 'fDeactivateCaching')
    def fDeactivateCaching(self, theContextualObject,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fDeactivateCaching( self, theContextualObject)
        


             
    
    
        
    
    security.declareProtected( permissions.ManagePortal, 'fConfigureTemplatesCache')
    def fConfigureTemplatesCache(self, theContextualObject, theEditedCacheParameters, theCacheName):
        """Set parameters controlling the maximum amount of memory available to store cached templates, and other controls on the behavior of the cache.
        
        """
      
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fConfigureTemplatesCache( self, theContextualObject, theEditedCacheParameters, theCacheName)
        

            
        
        
    
    security.declareProtected( permissions.ManagePortal, 'fEnableTemplatesCache')
    def fEnableTemplatesCache(self, theContextualObject, theCacheName,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fEnableTemplatesCache( self, theContextualObject, theCacheName)
        
         
        
    
    security.declareProtected( permissions.ManagePortal, 'fDectivateTemplatesCache')
    def fDectivateTemplatesCache(self, theContextualObject, theCacheName,):
        """Allow to store in memory the result of rendering templates, and save the effort of rendering in future request.
        
        """
      
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fDectivateTemplatesCache( self, theContextualObject, theCacheName)
        
        
   
    
    
    
    
 
    
    # #############################################################
    """Cache entry and disk flushing.
    
    """


        
    

    security.declareProtected( permissions.ManagePortal, 'pInvalidateToCreatePlone')
    def pInvalidateToCreatePlone(self, theContainerElement):
        """Flush templates that would be affected if a Plone element were created in the container.
        
        """
        
        unosImpactedObjectsUIDs = self.fModelDDvlPloneTool_Mutators( theContainerElement).fImpactCreatePloneUIDs( theContainerElement)

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theContainerElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return self
       
      
    
    

    
     
    

    security.declareProtected( permissions.ManagePortal, 'fFlushAllCachedTemplates')
    def fFlushAllCachedTemplates(self, theContextualObject, theCacheName, theFlushDiskCache=False):
        """Invoked by authorized users requesting to remove all cached rendered templates, recording who and when requested the flush.
        
        """
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fFlushAllCachedTemplates( self, theContextualObject, theCacheName, theFlushDiskCache=theFlushDiskCache)

       

    
    
    
    security.declareProtected( permissions.ManagePortal, 'fFlushSomeCachedTemplates')
    def fFlushSomeCachedTemplates(self, theContextualObject, theCacheName, theProjectNames, theFlushDiskCache=False):
        """Invoked by authorized users requesting to remove some cached rendered templates, from some projects (or all if none specified), and some languages (or all if none specified) .
        
        """
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fFlushSomeCachedTemplates( self, theContextualObject, theCacheName, theProjectNames,theFlushDiskCache=theFlushDiskCache)

    
    
    
    

    security.declareProtected( permissions.ManagePortal, 'fFlushCachedTemplateByUniqueId')
    def fFlushCachedTemplateByUniqueId(self, theContextualObject, theCacheEntryUniqueId, theFlushDiskCache=False):
        """Invoked by authorized users requesting invalidation of the cache entry given an id unique among all cache entries in all caches.
        
        """
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fFlushCachedTemplateByUniqueId( self, theContextualObject, theCacheEntryUniqueId, theFlushDiskCache=theFlushDiskCache)

    


    

    security.declareProtected( permissions.ManagePortal, 'fFlushCachedTemplateForElement')
    def fFlushCachedTemplateForElement(self, theContextualObject, theFlushCacheCode,  theTemplateName, theFlushDiskCache=False):
        """Invoked by authorized users requesting invalidation of the cache entry for the element given the view name.
        
        """
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fFlushCachedTemplateForElement( self, theFlushCacheCode, theContextualObject, theTemplateName, theFlushDiskCache=theFlushDiskCache)

    
    
    
    
    
    security.declarePrivate( 'pFlushCachedTemplatesForImpactedElementsUIDs')
    def pFlushCachedTemplatesForImpactedElementsUIDs(self, theContextualObject, theFlushedElementsUIDs, theViewsToFlush=[]):
        """Invoked from an element intercepting drag&drop reordering and impacting its changes.
        
        """
        return self.fModelDDvlPloneTool_Cache( theContextualObject).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContextualObject, theFlushedElementsUIDs, theViewsToFlush=theViewsToFlush)
  
    
    
        
    
    
    
    security.declareProtected( permissions.ManagePortal, 'pReceiveNotification_FlushCachedTemplatesForElementsUIDs')
    def pReceiveNotification_FlushCachedTemplatesForElementsUIDs(self, theContextualObject, theFlushedElementsUIDs, thePeerIdentificationString, thePeerAuthenticationString, theViewsToFlush=[]):
        """Invoked from service exposed to receive notifications from other ZEO clients authenticated with the supplied string, to flush cache entries for elements of the specified Ids.
        
        """
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).pProcessNotification_FlushCachedTemplatesForElementsUIDs( self, theContextualObject, theFlushedElementsUIDs, thePeerIdentificationString, thePeerAuthenticationString, theViewsToFlush=theViewsToFlush)

    

    
    
    
    
 
    
    # #############################################################
    """Cache mediated Rendering - may not render, but rather retrieve the HTML from memory or disk.
    
    """


            
    
    security.declareProtected( permissions.View, 'fRenderTemplateOrCachedElementIndependent')
    def fRenderTemplateOrCachedElementIndependent(self, theContextualObject, theTemplateName, theAdditionalParams=None):
        """Retrieve a previously rendered template for a project, independent of the here element, for the currently negotiared language and return the rendered HTML.
        
        """
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fRenderTemplateOrCachedElementIndependent( self, theContextualObject, theTemplateName, theAdditionalParams)
    
    
    
    


    security.declareProtected( permissions.View, 'fRenderTemplateOrCachedForElement')
    def fRenderTemplateOrCachedForElement(self, theContextualObject, theTemplateName, theAdditionalParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fRenderTemplateOrCachedForElement( self, theContextualObject, theTemplateName, theAdditionalParams)


    
    
    

    security.declareProtected( permissions.View, 'fRenderCallableOrCachedForElement')
    def fRenderCallableOrCachedForElement(self, theContextualObject, theTemplateName, theCallable, theCallableCtxt=None, theCallableParms=None):
        """ Return theHTML, from cache or just rendered, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fRenderCallableOrCachedForElement( self, theContextualObject, theTemplateName, theCallable, theCallableCtxt, theCallableParms)
    
    
    
    
        
        
    
    
    
    

        
    security.declarePrivate( 'fGetCacheConfigCopy')
    def fGetCacheConfigCopy(self, theContextualObject, theCacheName):
        
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fGetCacheConfigCopy( self, theContextualObject, theCacheName)
    
          

    
        
    security.declarePrivate( 'fGetCacheConfigParameterValue')
    def fGetCacheConfigParameterValue(self, theContextualObject, theCacheName, thePropertyName):
        
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fGetCacheConfigParameterValue( self, theContextualObject, theCacheName, thePropertyName)

  
    
        
    security.declarePrivate( 'fSetCacheConfigParameterValue')
    def fSetCacheConfigParameterValue(self, theContextualObject, theCacheName, thePropertyName, thePropertyValue):
        
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fSetCacheConfigParameterValue( self, theContextualObject, theCacheName, thePropertyName, thePropertyValue)

    
    
    
               
        
               
        
    security.declarePrivate( 'fUpdateCacheConfig')
    def fUpdateCacheConfig(self, theContextualObject, theCacheName, theConfigChanges):
        """Must be invoked from ModelDDvlPloneTool_Cache within a thread-safe protected critical section, in the same critical section where current configuration values where retrived with fGetCacheConfigCopy to compare with and known wheter if any parameter was changed by the user and the config needs updating.
        
        """
         
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fUpdateCacheConfig(  self, theContextualObject, theCacheName, theConfigChanges)

        
               
        
    security.declarePrivate( 'fGetAllCachesConfigCopy')
    def fGetAllCachesConfigCopy(self, theContextualObject, ):
        
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fGetAllCachesConfigCopy( self, theContextualObject,)
    
    

    
        
    security.declarePrivate( 'fGetAllCachesConfigParameterValue')
    def fGetAllCachesConfigParameterValue(self, theContextualObject, thePropertyName):
          
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fGetAllCachesConfigParameterValue( self, theContextualObject, thePropertyName)

    
    
        
    security.declarePrivate( 'fSetAllCachesConfigParameterValue')
    def fSetAllCachesConfigParameterValue(self, theContextualObject, thePropertyName, thePropertyValue):
            
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fSetAllCachesConfigParameterValue( self, theContextualObject, thePropertyName, thePropertyValue)

        
    
    
    
    
    
              
    security.declarePrivate( 'fUpdateAllCachesConfig')
    def fUpdateAllCachesConfig(self, theContextualObject, theConfigChanges):
        """Must be invoked from ModelDDvlPloneTool_Cache within a thread-safe protected critical section, in the same critical section where current configuration values where retrived with fGetCacheConfigCopy to compare with and known wheter if any parameter was changed by the user and the config needs updating.
        
        """
              
        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return None
        return aModelDDvlPloneToolConfiguration.fUpdateAllCachesConfig( self, theContextualObject, theConfigChanges)

                                                  
    
    
    
    

    
        
    security.declareProtected( permissions.View, 'fCached_HTML')
    def fCached_HTML( self, theContextualObject, theCacheEntryUniqueId, theAdditionalParams={}):
        
        aDumpResult = self.fModelDDvlPloneTool_Cache( theContextualObject).fCached_HTML( self, 
            theContextualObject, 
            theCacheEntryUniqueId, 
            theAdditionalParams=theAdditionalParams
        )
        return aDumpResult
    
     
    
    
    
    security.declareProtected( permissions.ManagePortal, 'fCachesDiagnostics')
    def fCachesDiagnostics( self, theContextualObject, theCacheNames=None, theAdditionalParams={}):
        
        someDiagnostics = self.fModelDDvlPloneTool_Cache( theContextualObject).fCachesDiagnostics( self, 
            theContextualObject, 
            theCacheNames       =theCacheNames, 
            theAdditionalParams =theAdditionalParams
        )
        return someDiagnostics
    
     
    
    
    
        
        