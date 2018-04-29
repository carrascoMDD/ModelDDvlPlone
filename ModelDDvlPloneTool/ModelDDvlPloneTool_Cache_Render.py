# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_Render.py
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

from urlparse import urlparse


from AccessControl import ClassSecurityInfo



from Products.CMFCore import permissions


from Products.PlacelessTranslationService.Negotiator import getLangPrefs




from ModelDDvlPloneTool_CacheConstants          import *

from MDDStringConversions                       import *


from ModelDDvlPloneToolSupport                  import fMillisecondsNow, fMillisecondsToDateTime

from MDDRenderedTemplateCacheEntry_ElementIndependent import MDDRenderedTemplateCacheEntry_ElementIndependent
from MDDRenderedTemplateCacheEntry_ForElement         import MDDRenderedTemplateCacheEntry_ForElement

# #######################################################
# #######################################################








    
class ModelDDvlPloneTool_Cache_Render:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the configuration of cache operation parameters.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    



      
    
    
     
    
    # ###################################################################
    """Rendering service for templates that are Element Independent. Searching Cache entries NOT associated with any specific element. 
    
    """
    
    
       
    security.declarePrivate( '_fRenderError')
    def _fRenderError(self, theErrorCode, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=None,):
        """ Return HTML with an error message.
        
        """
        
        anErrorCode = theErrorCode
        if not anErrorCode:
            anErrorCode = cRenderError_UnknownError
            
        anErrorMsgId = '%s%s' % ( cRenderError_MsgIdPrefix, anErrorCode,)
        
        anTranslatedError = theModelDDvlPloneTool.fTranslateI18N( theContextualObject, 'ModelDDvlPlone', anErrorMsgId, anErrorMsgId, )
        
        anErrorHTML = cRenderError_HTML % self.fCGIE( anTranslatedError)        
        
        return anErrorHTML
    
    
         
    

    
    security.declarePrivate( 'fRenderTemplateOrCachedElementIndependent')
    def fRenderTemplateOrCachedElementIndependent(self, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        someRenderHandlers = self.fRenderHandlers_ElementIndependent(  theModelDDvlPloneTool, theContextualObject)
        return self.fRenderTemplateOrCached_withHandlers( someRenderHandlers, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=theAdditionalParams)
       
    
    
    
     
    security.declarePrivate( 'fRenderTemplateOrCachedForElement')
    def fRenderTemplateOrCachedForElement(self, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        someRenderHandlers = self.fRenderHandlers_ForElement(  theModelDDvlPloneTool, theContextualObject)
        return self.fRenderTemplateOrCached_withHandlers( someRenderHandlers, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=theAdditionalParams)
       
    
       
     
    security.declarePrivate( 'fRenderCallableOrCachedForElement')
    def fRenderCallableOrCachedForElement(self, theModelDDvlPloneTool, theContextualObject, theTemplateName, theCallable=None, theCallableCtxt=None, theCallableParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        someRenderHandlers = self.fRenderHandlers_ForElement(  theModelDDvlPloneTool, theContextualObject)
        
        someAdditionalParams = { }
        someAdditionalParams.update( {
            'callable':      theCallable,
            'callable_ctxt': theCallableCtxt,
            'callable_parms':theCallableParams,
        })
        
        return self.fRenderTemplateOrCached_withHandlers( someRenderHandlers, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=someAdditionalParams)
       
        
    
    security.declarePrivate( 'fRenderTemplateOrCached_withHandlers')
    def fRenderTemplateOrCached_withHandlers(self, theRenderHandlers, theModelDDvlPloneTool, theContextualObject, theTemplateName, theAdditionalParams=None):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        """
        
        # ###################################################################
        """Can not proceed without handlers.
        
        """
        if not theRenderHandlers:
            return self._fRenderError( cRenderError_MissingHandlers, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        aMemoryHandler = theRenderHandlers.get( 'memory', None)
        aDiscHandler   = theRenderHandlers.get( 'disc',   None)
        aRenderHandler = theRenderHandlers.get( 'render', None)
        aStoreHandler  = theRenderHandlers.get( 'store',  None)
        
        if not ( aMemoryHandler and aDiscHandler and aRenderHandler and  aStoreHandler):
            return self._fRenderError( cRenderError_MissingHandlers, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
            
        
        # ###################################################################
        """If caching not active, render now.
        
        """
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                return self._fRenderError( cRenderError_MissingParameters, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        
            unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            
            return unRenderedTemplate
        
        someVariables = { }
        
         
        # ###################################################################
        """Try to retrieve from memory the already rendered HTML.
        
        """
        aRenderResult_Phase_TryMemory = aMemoryHandler( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams, someVariables)
        if not aRenderResult_Phase_TryMemory:
            return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        
        
        aRenderStatus_Memory = aRenderResult_Phase_TryMemory.get( 'status',    '')
        if not aRenderStatus_Memory:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_UnknownError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
 
        
        if aRenderStatus_Memory == cRenderStatus_Completed:
            aRenderedHTML_Memory       = aRenderResult_Phase_TryMemory.get( 'rendered_html',        None)
            if not aRenderedHTML_Memory:
                self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
                return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
            return   aRenderedHTML_Memory
        
       
        if aRenderStatus_Memory == cRenderStatus_ForceRender:
            aRenderedHTML = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return aRenderedHTML

        
        if aRenderStatus_Memory == cRenderStatus_ShowError:
            aRenderError = aRenderResult_Phase_TryMemory.get( 'error',    '')
            if not aRenderError:
                aRenderError = cRenderError_UnknownError
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( aRenderError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
      

        if not ( aRenderStatus_Memory == cRenderStatus_Continue):
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_Discontinued, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
            

        
        
        
        
        # ###################################################################
        """Try to retrieve from disc the already rendered HTML.
        
        """        
        
        aRenderResult_Phase_TryDisk = aDiscHandler( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams, someVariables)
        if not aRenderResult_Phase_TryDisk:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        
        
        aRenderStatus_Disc = aRenderResult_Phase_TryDisk.get( 'status',    '')
        if not aRenderStatus_Disc:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_UnknownError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
 
        
        if aRenderStatus_Disc == cRenderStatus_Completed:
            aRenderedHTML_Disc       = aRenderResult_Phase_TryDisk.get( 'rendered_html',        None)
            if not aRenderedHTML_Disc:
                self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
                return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
            return   aRenderedHTML_Disc
        
       
        if aRenderStatus_Disc == cRenderStatus_ForceRender:
            aRenderedHTML = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            return aRenderedHTML

        
        if aRenderStatus_Disc == cRenderStatus_ShowError:
            aRenderError = aRenderResult_Phase_TryDisk.get( 'error',    '')
            if not aRenderError:
                aRenderError = cRenderError_UnknownError
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( aRenderError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
      

        if not ( aRenderStatus_Disc == cRenderStatus_Continue):
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_Discontinued, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        


        
        

                   
        # ###################################################################
        """Try to render HTML.
        
        """        
        aRenderResult_Phase_Render = aRenderHandler( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams, someVariables)
        if not aRenderResult_Phase_Render:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
        
        
        aRenderStatus_Render = aRenderResult_Phase_Render.get( 'status',    '')
        if not aRenderStatus_Render:
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( cRenderError_UnknownError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
 
        
        if aRenderStatus_Render == cRenderStatus_Completed:
            aRenderedHTML_Render       = aRenderResult_Phase_Render.get( 'rendered_html',        None)
            if not aRenderedHTML_Render:
                self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
                return self._fRenderError( cRenderError_NothingRendered, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)

            aResultPhase_StoreDisc = aStoreHandler( theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams, someVariables)

            return   aRenderedHTML_Render
        
       
        if aRenderStatus_Render == cRenderStatus_ForceRender:
            aRenderedHTML = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            return aRenderedHTML

        
        if aRenderStatus_Render == cRenderStatus_ShowError:
            aRenderError = aRenderResult_Phase_Render.get( 'error',    '')
            if not aRenderError:
                aRenderError = cRenderError_UnknownError
            self._pDestroyFailedPromise( theModelDDvlPloneTool, theContextualObject, aRenderResult_Phase_TryMemory)
            return self._fRenderError( aRenderError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)
      

        return self._fRenderError( cRenderError_UnknownError, theModelDDvlPloneTool,  theContextualObject, theTemplateName, theAdditionalParams,)

    
    
    
        
    
    
    

    
    

    
    
    security.declarePrivate( '_fTranslationsToRenderTemplate')
    def _fTranslationsToRenderTemplate(self, 
        theModelDDvlPloneTool =None, 
        theContextualObject   =None,
        theTranslations       =None,):
        """Retrieve localized strings for internationalized symbols (l10n4i18n).
            
        """
        
        someTranslations = theTranslations
        if theTranslations == None:
            someTranslations = { }
            
        if theModelDDvlPloneTool == None:
            return someTranslations
        
        if theContextualObject == None:
            return someTranslations
        
            
        someDomainsStringsAndDefaults = [
            [ 'ModelDDvlPlone', [    
                [ 'ModelDDvlPlone_Cached',                           'Cached-',], 
                [ 'ModelDDvlPlone_JustRendered',                     'Just Rendered-',],
                [ 'ModelDDvlPlone_DiskCached',                       'Disk Cached-',], 
                [ 'ModelDDvlPlone_JustCached',                       'Just Cached-',],
                [ 'ModelDDvlPlone_Time_label',                       'Date-',], 
                [ 'ModelDDvlPlone_Len_label',                        'Len-',], 
                [ 'ModelDDvlPlone_User_label',                       'User-',], 
                [ 'ModelDDvlPlone_Date_label',                       'Date-',], 
                [ 'ModelDDvlPlone_Project_label',                    'Project-',], 
                [ 'ModelDDvlPlone_Language_label',                   'Language-',], 
                [ 'ModelDDvlPlone_View_label',                       'View-',],
                [ 'ModelDDvlPlone_FilePath_label',                   'File-',],
                [ 'ModelDDvlPlone_RoleKind_label',                   'Role kind-',], 
                [ 'ModelDDvlPlone_Path_label',                       'Path-',], 
                [ 'ModelDDvlPlone_MetaType_label',                   'MetaType-',], 
                [ 'ModelDDvlPlone_PortalType_label',                 'PortalType-',], 
                [ 'ModelDDvlPlone_ArchetypeName_label',              'ArchetypeName-',], 
                [ 'ModelDDvlPlone_ElementId_label',                  'ElementId-',], 
                [ 'ModelDDvlPlone_UID_label',                        'UID-',], 
                [ 'ModelDDvlPlone_URL_label',                        'URL-',], 
                [ 'title_label',                                     'Title-',], 
                [ 'ModelDDvlPlone_Relation_label',                   'Relation-'],
                [ 'ModelDDvlPlone_ShowNoFromCacheLink_label',        'Show generated-',], 
                [ 'ModelDDvlPlone_FlushFromCacheLink_label',         'Flush from cache-',], 
                [ 'ModelDDvlPlone_FlushFromDiskCacheLink_label',     'Flush from diskcache-',], 
                [ 'ModelDDvlPlone_RelatedElement_label',             'Related Element-',],
                [ 'ModelDDvlPlone_SchemeHostAndDomain_label',        'Scheme, Host and Domain-',],
              
            ]],                                                      
        ]        
        
        theModelDDvlPloneTool.fTranslateI18NManyIntoDict( 
            theContextualObject, 
            someDomainsStringsAndDefaults, 
            someTranslations
        )

        return someTranslations
    
    
    

    
    security.declarePrivate( '_fRenderTemplateOrCachedElementIndependent_Phase_TryMemory')
    def _fRenderTemplateOrCachedElementIndependent_Phase_TryMemory(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """ Return theHTML, from cache or just rendered, for a project, for the specified view, and for the currently negotiared language.
        
        In-memory cache structure of dictionaries for views:
            
        Element Independent 
        
        'Project' : {
            'Language' : {
                'View' : {
                    'SchemeHostAndDomain' : object( ) # CacheEntry
                }
            }
        }        
        """
        
        aRenderResult = self._fNewVoidRenderResult_Phase_TryMemory()
        
        unosMillisBeforeMatch   = fMillisecondsNow()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if theModelDDvlPloneTool == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        if theContextualObject == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        if cForbidCaches or not self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent):
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        
        aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
        if aModelDDvlPloneTool_Retrieval == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
                
            
        if theVariables == None:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
           
        unCacheEntryUniqueId = ''
        unCachedTemplate = None
        
        aBeginMillis = fMillisecondsNow()
                
          
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
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        aNegotiatedLanguage = unosPreferredLanguages[ 0]   
        if not aNegotiatedLanguage:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
                
        aViewName = theTemplateName
        if not aViewName:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        if aViewName.find( '%s') >= 0:
            if not ( aProjectName == cDefaultNombreProyecto):
                aViewName = aViewName % aProjectName
            else:
                aViewName = aViewName.replace( '%s', '')
        if not aViewName:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
                    

        unRootElement = None
        try:
            unRootElement = theContextualObject.getRaiz()
        except:
            None
        if unRootElement == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
              
                        
        unRootElementURL = unRootElement.absolute_url()
              
        unParsedRootElementURL = self.fURLParse( theModelDDvlPloneTool, theContextualObject, unRootElementURL, )
        if ( not unParsedRootElementURL):
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
                   
        
        if ( not unParsedRootElementURL[ 0]) or ( not unParsedRootElementURL[ 1]):
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult    
        
        unSchemeHostAndDomain = '%s-%s' % ( unParsedRootElementURL[ 0], unParsedRootElementURL[ 1],)
        
        aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
        if aModelDDvlPloneTool_Retrieval == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
                
        unMemberId = aModelDDvlPloneTool_Retrieval.fGetMemberId(  theContextualObject)           
         
                    
            
        # ###################################################################
        """CRITICAL SECTION to access and modify cache control structure, for Cache entries associated with specific elements.
        
        """
        unExistingOrPromiseCacheEntry = None
        unCachedTemplate              = None
        unPromiseMade                 = None                      
        
        anActionToDo                  = None
        somePossibleActions           = [ 'UseFoundEntry', 'MakePromise', 'JustFallbackToRenderNow', ] # Just to document the options handled by logic below
        
        someFilesToDelete = [ ]
        
        someExistingCacheEntriesInWrongState = [ ]
        
        
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            # ###########################################################
            """Retrieve within thread safe section, to be used later, the configuration paameters specifying: whether to render a cache hit information collapsible section at the top or bottom of the view, or none at all, whether the disk caching is enabled, and the disk cache files base path.
            
            """
            aDisplayCacheHitInformation = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_DisplayCacheHitInformation)
            aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_CacheDiskEnabled)
            aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_CacheDiskPath)
            unExpireDiskAfterSeconds    = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_ExpireDiskAfterSeconds)

            
            # ###########################################################
            """All Cache Entries that have expired and are forced to expire shall be flushed, whether memory used is over the limit, or not.
            
            """  
            self._pFlushCacheEntriesForcedtoExpire(theModelDDvlPloneTool, theContextualObject, theFilesToDelete=someFilesToDelete)       
                        

            
            
            # ###########################################################
            """Traverse cache control structures to access the cache entry corresponding to the parameters. Elements found missing shall be created, to hook up the new cache entry.
            
            """
            someCachedTemplatesForProject = self.fGetOrInitCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, aProjectName)              

    
            someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aNegotiatedLanguage, None)
            if someCachedTemplatesForLanguage == None:
                someCachedTemplatesForLanguage = { }
                someCachedTemplatesForProject[ aNegotiatedLanguage] = someCachedTemplatesForLanguage
    
                
            someCachedTemplatesForView = someCachedTemplatesForLanguage.get( aViewName, None)
            if someCachedTemplatesForView == None:
                someCachedTemplatesForView = { }
                someCachedTemplatesForLanguage[ aViewName] = someCachedTemplatesForView
                    
                
            # ###########################################################
            """Obtain the Cache entry, if exists.
            
            """
            anExistingCacheEntry = someCachedTemplatesForView.get( unSchemeHostAndDomain, None)
            
            
            
            
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
                aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                aCacheEntryInWrongStateInfo.update( {
                    'cached_entry':        anExistingCacheEntry,
                    'cached_entry_holder': someCachedTemplatesForLanguage,
                    'cached_entry_key':    aViewName,            
                })                    
                someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)
                anActionToDo = 'MakePromise'
                
            elif not anExistingCacheEntry.vPromise:
                # ###########################################################
                """A null promise is a sign something went wrong with its resolution. A new entry shall be created, and shall replace the existing one in the cache control structure.
                
                """
                aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                aCacheEntryInWrongStateInfo.update( {
                    'cached_entry':        anExistingCacheEntry,
                    'cached_entry_holder': someCachedTemplatesForLanguage,
                    'cached_entry_key':    aViewName,            
                })                    
                someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)
                
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
                    aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                    aCacheEntryInWrongStateInfo.update( {
                        'cached_entry':        anExistingCacheEntry,
                        'cached_entry_holder': someCachedTemplatesForLanguage,
                        'cached_entry_key':    aViewName,            
                    })                    
                    someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)

                    anActionToDo = 'MakePromise'
                    
                else:
                    # ###########################################################
                    """Found cached template: Cache Hit. Update expiration time for the cache entry. Update cache hit statistics, and decide to use the HTML cached in the found entry.
                    
                    """
                    unMillisecondsNow = fMillisecondsNow()

                    anExistingCacheEntry.vHits += 1
                    anExistingCacheEntry.vLastHit  = unMillisecondsNow                         
                    anExistingCacheEntry.vLastUser = unMemberId                         
                    
                    unExistingCacheEntryChars = 0
                    if anExistingCacheEntry.vHTML:
                        unExistingCacheEntryChars = len( anExistingCacheEntry.vHTML)
    
                    unStatisticsUpdate = {
                        cCacheStatistics_TotalCacheHits:    1,
                        cCacheStatistics_TotalCharsSaved:   unExistingCacheEntryChars,
                        cCacheStatistics_TotalTimeSaved:    max( anExistingCacheEntry.vMilliseconds, 0),
                    }
                    self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                    
                
                    
                    # ###########################################################
                    """Renew the age of the cache entry in the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                    See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                    
                    """
                    
                    unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent)
                    if unListNewSentinel:
                        anExistingCacheEntry.pUnLink()   
                        unListNewSentinel.pLink( anExistingCacheEntry) 
                    
                    
                    
                    
                    # ###########################################################
                    """Determined the cache entry found, and an indication that no promise was made (so no rendering has to be produced to fullfill it), and there is no need to just fallback and render it now
                    
                    """
                    unExistingOrPromiseCacheEntry = anExistingCacheEntry
                    anActionToDo                  = 'UseFoundEntry'

                    
                    
            # ###########################################################
            """Remove cache entries that are in wrong state, more likely because of an error while trying to fulfill the promise to be rendered.
            
            """
            if someExistingCacheEntriesInWrongState:
                self._pRemoveCachedEntriesInWrongState( someExistingCacheEntriesInWrongState)
               
                    
                    
            if not ( anActionToDo == 'UseFoundEntry'):
                # ###########################################################
                """Not Found usable cached template: Cache Fault. Update cache fault statistics.
                
                """
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheFaults:    1,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                
                
                
            if anActionToDo == 'MakePromise':
                # ###########################################################
                """Create a new cache entry as a promise to be fullfilled after the CRITICAL SECTION, and hook it up in the cache control structure.
                
                """
                
                
                
            
                # ###########################################################
                """Allocate a new unique id for the cache entry, 
                
                """
                    
                unCacheEntryUniqueId  = self.fGetCacheStoreNewUniqueId(  theModelDDvlPloneTool, theContextualObject,) 
                unMillisecondsNow     = fMillisecondsNow()
                unExpireAfterSeconds  = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_ExpireAfterSeconds)
                unForceExpire         = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, cCacheName_ElementIndependent, cCacheConfigPpty_ForceExpire)

                unPromiseMade = unMillisecondsNow
                
                aNewCacheEntry = MDDRenderedTemplateCacheEntry_ElementIndependent(
                    theCacheName         =cCacheName_ElementIndependent,
                    theCacheKind         =cCacheKind_ElementIndependent,
                    theProjectName       =aProjectName,
                    theUniqueId          =unCacheEntryUniqueId,
                    theValid             =True,
                    thePromise           =unPromiseMade,
                    theUser              =unMemberId,
                    theDateMillis        =unMillisecondsNow,
                    theProject           =aProjectName,
                    theView              =aViewName,
                    theLanguage          =aNegotiatedLanguage,
                    theSchemeHostAndDomain=unSchemeHostAndDomain,
                    theHTML              =None,
                    theMilliseconds      =0,
                    theExpireAfterSeconds =unExpireAfterSeconds,
                    theForceExpire       =unForceExpire,
                )
                
                unExistingOrPromiseCacheEntry = aNewCacheEntry
                
                
                
                # ###########################################################
                """Hook up the new cache entry promise in the cache control structure, to be fullfilled after the CRITICAL SECTION.
                
                """
                someCachedTemplatesForView[ unSchemeHostAndDomain] = aNewCacheEntry

                aRenderResult.update( {
                    'cache_name':     cCacheName_ElementIndependent,
                    'promise_made':   unExistingOrPromiseCacheEntry,
                    'promise_holder': someCachedTemplatesForLanguage,
                    'promise_key':    aViewName,
                })
                
                                    
                
                # ###########################################################
                """Add unique id of cache entry to the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                
                """
                unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent)
                if unListNewSentinel:
                    unListNewSentinel.pLink( aNewCacheEntry) 
    
                

                
                # ###########################################################
                """Add the entry to the index by Cache Entry Unique Id.
                
                """
                self._pAddCacheEntryToUniqueIdIndex( theModelDDvlPloneTool, theContextualObject, aNewCacheEntry)
                

                
                # ###########################################################
                """Update cache statistics.
                
                """                    
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheEntries:    1,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                
                    
                
            
                
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            
        if someFilesToDelete:
            self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
            
            
            
        # ###########################################################
        """Act according to the analysis made of the Cache entry, and decide how to proceed: using it if retrieved, promissing to create a new one, or just fallback to render the template now and return it.
        
        """

        someTranslations = self._fTranslationsToRenderTemplate( theModelDDvlPloneTool, theContextualObject,)
        
        
        
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
                    u'<span>%(ModelDDvlPlone_Cached)s' % someTranslations,
                )   
    
                aEndMillis = fMillisecondsNow()
                aMilliseconds = aEndMillis - aBeginMillis
                
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn[:]
                if unExistingOrPromiseCacheEntry:
                    if unExistingOrPromiseCacheEntry.vUniqueId:
                        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                            cMagicReplacementString_UniqueId, 
                            str( unExistingOrPromiseCacheEntry.vUniqueId)
                        )

                        
                unDurationString = '%d ms' % aMilliseconds
                        
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                    u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                    u'%s</span>' % unDurationString
                )
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                   cMagicReplacementString_CacheCode, 
                   '%d' % aEndMillis
                )
                
                aRenderResult.update( {
                    'status':            cRenderStatus_Completed, 
                    'rendered_html':     unRenderedTemplateToReturnWithDuration,
                })                                    
                return aRenderResult
            
            
            
            
        
            
        if ( anActionToDo == 'UseFoundEntry') or ( anActionToDo == 'JustFallbackToRenderNow') or ( ( anActionToDo == 'MakePromise') and ( not unPromiseMade)) or not ( anActionToDo == 'MakePromise') or (unExistingOrPromiseCacheEntry == None):
            # ###########################################################
            """Entry was found, but something was wrong, or it has been decided that the action is to just render now, or a promise has been made but there is no promise code, or a the action is not the remaining possiblity of MakePromise , or no promise entry has been created. Fallback to render now.
            ACV OJO 20091219 Should remove the found entry: pages that fail usually leave the entry in a bad state, and are never cached again.
            
            """
            
            anActionToDo = 'JustFallbackToRenderNow'
            
            
            unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
           
            if aDisplayCacheHitInformation:
                if aDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                    unRenderedTemplateToReturn = unRenderedTemplate + ( u'\n<br/><br/><font size="1"><strong>%(ModelDDvlPlone_JustRendered)s</strong></font>' % someTranslations)
                elif aDisplayCacheHitInformation == cDisplayCacheHitInformation_Top:          
                    unRenderedTemplateToReturn = ( u'<br/><font size="1"><strong>%(ModelDDvlPlone_JustRendered)s</strong></font><br/>\n' % someTranslations) + unRenderedTemplate
                else:
                    unRenderedTemplateToReturn = unRenderedTemplate[:]
                    
            unosMillisAfterMatch   = fMillisecondsNow()
                    
            unosMilliseconds = unosMillisAfterMatch - unosMillisBeforeMatch
            unDurationString = '%d ms' % unosMilliseconds
            
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                u'%s</span>' % unDurationString
            )
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
               cMagicReplacementString_CacheCode, 
               '%d' % unosMillisAfterMatch
            )
           
            aRenderResult.update( {
                'status':            cRenderStatus_Completed, 
                'rendered_html':     unRenderedTemplateToReturnWithDuration,
            })                                    
            return aRenderResult
            
            
        theVariables.update( {
            'aBeginMillis':                  aBeginMillis,
            'anActionToDo':                  anActionToDo,
            'unExistingOrPromiseCacheEntry': unExistingOrPromiseCacheEntry,
            'unPromiseMade':                 unPromiseMade,
            'unCacheEntryUniqueId':          unCacheEntryUniqueId,
            'aProjectName':                  aProjectName,
            'aNegotiatedLanguage':           aNegotiatedLanguage,
            'unCacheId':                     unCacheEntryUniqueId,
            'aViewName':                     aViewName,
            'unMemberId':                    unMemberId,
            'unCachedTemplate':              unCachedTemplate,
            'someTranslations':              someTranslations,
            'aDisplayCacheHitInformation':   aDisplayCacheHitInformation,
            'aCacheDiskEnabled':             aCacheDiskEnabled,
            'aCacheDiskPath':                aCacheDiskPath,
            'unExpireDiskAfterSeconds':      unExpireDiskAfterSeconds,
            'unSchemeHostAndDomain':         unSchemeHostAndDomain,
        })
            
        aRenderResult.update( {
            'status':            cRenderStatus_Continue, 
        })                                    
        return aRenderResult

        
                

    
    
    
 
    
    security.declarePrivate( '_fRenderTemplateOrCachedElementIndependent_Phase_TryDisk')
    def _fRenderTemplateOrCachedElementIndependent_Phase_TryDisk(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """No usable cache entry has been found. Try to find the cached HTML on disc, for the project, for the currently negotiated language, and for the specified view.
        
        """
        
        aRenderResult = self._fNewVoidRenderResult_Phase_TryDisk()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if not theVariables:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        aViewName                     = theVariables[ 'aViewName']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        someTranslations              = theVariables[ 'someTranslations']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        unExpireDiskAfterSeconds      = theVariables[ 'unExpireDiskAfterSeconds']
        unSchemeHostAndDomain         = theVariables[ 'unSchemeHostAndDomain']
        
        if not aCacheDiskEnabled:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        

        if not aCacheDiskPath:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        # ###########################################################
        """Assemble the name of the disk file holding the cached HTML for the entry.
            
        """            
        
        aCacheContainerPath = self.fCacheContainerPath( theModelDDvlPloneTool, theContextualObject,)
        
        aProjectPath        = os.path.join( aCacheContainerPath, aCacheDiskPath, aProjectName)
        aLanguagePath       = os.path.join( aProjectPath, aNegotiatedLanguage)
        aFileName           = '%s-%s%s' % (  aViewName, unSchemeHostAndDomain, cCacheDiskFilePostfix)
        aFilePath           = os.path.join( aLanguagePath, aFileName)
        aDisplayPath        = os.path.join( aProjectName, aNegotiatedLanguage, aFileName)
        aDisplayPath        = aDisplayPath.replace( '/', '/ ')
        aDisplayPath           = aDisplayPath.replace( '\\', '/ ')

        theVariables[ 'aFilePath']         = aFilePath
        theVariables[ 'aDisplayPath']      = aDisplayPath

        
        
        # ###########################################################
        """Try to access the directory containing the element independent files with cached HTML.
            
        """            
        aCacheDiskPathExist = False
        try:
            aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
        except:
            None
        if not aCacheDiskPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        
        # ###########################################################
        """Try to access directories for project and language.
            
        """
        aProjectPathExist = False
        try:
            aProjectPathExist = os.path.exists( aProjectPath)
        except:
            None
        if not aProjectPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
            
        
        aLanguagePathExist = False
        try:
            aLanguagePathExist = os.path.exists( aLanguagePath)
        except:
            None
        if not aLanguagePathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult

        
        # ###########################################################
        """Try to retrieve the page from disk cache file.
            
        """
        aFilePathExist = False
        try:
            aFilePathExist = os.path.exists( aFilePath)
        except:
            None
        if not aFilePathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult

        anHTML = ''
        try:
            aViewFile = None
            try:
                aViewFile = open( aFilePath, cCacheDisk_ElementIndependent_FileOpenReadMode_View, cCacheDisk_ElementIndependent_FileOpenReadBuffering_View)
                anHTML = aViewFile.read()
            finally:
                if aViewFile:
                    aViewFile.close()
                
        except IOError:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
  
        if ( not anHTML) or ( len( anHTML) < cMinCached_HTMLFileLen):
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
            
        
        
        unosMillisAfterRead = fMillisecondsNow()
        unosMilliseconds   = unosMillisAfterRead - aBeginMillis


  

        # ###########################################################
        """Read the HTML timestamp, and determine if the file has expired.
            
        """
        if unExpireDiskAfterSeconds:
            
            aFirstLinesChunk = anHTML[:cHTMLFirstLinesChunkLen]
            unIndex = aFirstLinesChunk.find( cHTMLRenderingTimeComment_Keyword)
            if unIndex < 0:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                    
            unMillisecondsHTMLString = aFirstLinesChunk[ unIndex + len( cHTMLRenderingTimeComment_Keyword):]
            if not unMillisecondsHTMLString:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unLastIndex = unMillisecondsHTMLString.index( ' ')
            if unLastIndex < 0:
                unLastIndex = unMillisecondsHTMLString.index( '-')
                
            if unLastIndex >=0:
                unMillisecondsHTMLString = unMillisecondsHTMLString[:unLastIndex]
            if not unMillisecondsHTMLString:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                
                
            unMillisecondsHTML = 0
            try:
                unMillisecondsHTML = int( unMillisecondsHTMLString)
            except:
                None
            if not unMillisecondsHTML:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unTimePassed = int( ( unosMillisAfterRead - unMillisecondsHTML) / 1000)
           
            if unTimePassed >= unExpireDiskAfterSeconds:
                # ###########################################################
                """HTML has expired. Flush the file.
                    
                """
                self._pRemoveDiskCacheFiles( theModelDDvlPloneTool, theContextualObject, [ aFilePath,])
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                
                        

        
        # ###########################################################
        """CRITICAL SECTION to register in the in-memory cache entry the HTML result of reading the cached file content. 
        
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
              
            # ###########################################################
            """Check if somebody messed with the promised cache entry, so it is not being updated here.
            
            """
            if ( unPromiseMade == unExistingOrPromiseCacheEntry.vPromise):

                unMillisecondsNow = fMillisecondsNow()
                        
                unExistingOrPromiseCacheEntry.vHTML            = anHTML
                unExistingOrPromiseCacheEntry.vFilePath        = aFilePath
                unExistingOrPromiseCacheEntry.vDisplayPath     = aDisplayPath
                unExistingOrPromiseCacheEntry.vDateMillis      = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                unExistingOrPromiseCacheEntry.vLastHit         = unMillisecondsNow
                
                unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                
                unHTMLLen = len( unExistingOrPromiseCacheEntry.vHTML)
                
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheDiskHits:    1,
                    cCacheStatistics_TotalCharsCached:      unHTMLLen,
                    cCacheStatistics_TotalCharsSaved:       unHTMLLen,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                

                    
                         
            # ###########################################################
            """MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
            
            """
            self._pFlushCacheEntriesToReduceMemoryUsed( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent)
               
            
             
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                        
        
        theVariables[ 'unTemplateToCache'] = anHTML[:]

        

        # ###########################################################
        """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
        
        """
        
        unRenderedTemplateToReturn = anHTML.replace(    
            u'<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
            u'<span>%s' % someTranslations[ 'ModelDDvlPlone_DiskCached'],
        )   
        
        
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn[:]
        if unExistingOrPromiseCacheEntry:
            if unExistingOrPromiseCacheEntry.vUniqueId:
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                    cMagicReplacementString_UniqueId, 
                    str( unExistingOrPromiseCacheEntry.vUniqueId)
                )


        unDurationString = '%d ms' % unosMilliseconds
       
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
            u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
            u'%s</span>' % unDurationString
        )
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
           cMagicReplacementString_CacheCode, 
           '%d' % unosMillisAfterRead
        )

        
        theVariables[ 'unTemplateToReturn'] = unRenderedTemplateToReturnWithDuration
                    
            
        aRenderResult.update( {
            'status':            cRenderStatus_Completed, 
            'rendered_html':     unRenderedTemplateToReturnWithDuration,
        })                                    
        return aRenderResult
        
        
     
            
            
            

 
    
    security.declarePrivate( '_fRenderTemplateOrCachedElementIndependent_Phase_Render')
    def _fRenderTemplateOrCachedElementIndependent_Phase_Render(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """No usable cache entry has been found. Render the template, for the project, for the currently negotiated language, and for the specified view.
        
        """
                
        aRenderResult = self._fNewVoidRenderResult_Phase_Render()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if not theVariables:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        aViewName                     = theVariables[ 'aViewName']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        someTranslations              = theVariables[ 'someTranslations']
        aDisplayCacheHitInformation   = theVariables[ 'aDisplayCacheHitInformation']
        unSchemeHostAndDomain         = theVariables[ 'unSchemeHostAndDomain']
        aFilePath                     = theVariables.get( 'aFilePath', '')
        aDisplayPath                  = theVariables.get( 'aDisplayPath', '')
       

        if not aFilePath:
            # ACV OJO 20091219
            logging.getLogger( 'ModelDDvlPlone').error( 'No aFilePath var in _fRenderTemplateOrCachedElementIndependent_Phase_Render')
            
            

            
        aMillisecondsNow = theModelDDvlPloneTool.fMillisecondsNow()
        

        
       
        
        
        
        
        # ###########################################################
        """Render a caching information collapsible section to append to the rendered template HTML.
            
        """
        unRenderedCacheInfo = u''
        if aDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]:
            
            # ###########################################################
            """Prepare internationalized strings, and info values.
                
            """
            
            unPagina = ''
            if aViewName in [ 'Textual', 'Textual_NoHeaderNoFooter',]:
                unPagina = '/'
            elif aViewName in [ 'Tabular', 'Tabular_NoHeaderNoFooter',]:
                unPagina = '/Tabular/'
            elif aViewName.endswith( '_NoHeaderNoFooter'):
                unPagina = '/%s/' % aViewName[: 0 - len( '_NoHeaderNoFooter')]
            else:
                unPagina = '/%s/' % aViewName
            

            
        
        
        # ###########################################################
        """Render template, because it was not found (valid) in the cache. This may take some significant time. Status of cache may have changed since.
        
        """
        

        unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
            theModelDDvlPloneTool=theModelDDvlPloneTool, 
            theContextualObject  =theContextualObject, 
            theTemplateName      =theTemplateName, 
            theAdditionalParams =theAdditionalParams,
        )
        
        aEndMillis       = fMillisecondsNow()
        unosMilliseconds = aEndMillis - aBeginMillis
                
        unRenderedTemplateWithCacheInfo = unRenderedTemplate
        
        
    
        # ###########################################################
        """If so configured: Fill in the date in the caching information collapsible section appended to the rendered template HTML.
        
        """
        if not( aDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]):
            unRenderedTemplateWithCacheInfo = unRenderedTemplate[:]
        
        else:
            
            aCacheEntryValuesDict = someTranslations.copy()
            aCacheEntryValuesDict.update( {
                'unBaseURL':                                       theContextualObject.getRaiz().absolute_url(),
                'cMagicReplacementString_CacheCode':               cMagicReplacementString_CacheCode,
                'cMagicReplacementString_TimeToRetrieve':          cMagicReplacementString_TimeToRetrieve,
                'cMagicReplacementString_Milliseconds':            cMagicReplacementString_Milliseconds,
                'cMagicReplacementString_Len':                     cMagicReplacementString_Len,
                'cMagicReplacementString_Date':                    cMagicReplacementString_Date,
                'cMagicReplacementString_CollapsibleSectionTitle': cMagicReplacementString_CollapsibleSectionTitle,
                'cMagicReplacementString_UniqueId':                cMagicReplacementString_UniqueId,                    
                'aCacheName':                    cCacheName_ElementIndependent,
                'aCacheKind':                    cCacheName_ElementIndependent,
                'aProjectName':                  aProjectName,
                'unSchemeHostAndDomain':         unSchemeHostAndDomain,
                'aNegotiatedLanguage':           aNegotiatedLanguage,
                'unCacheId':                     unCacheEntryUniqueId,
                'aViewName':                     aViewName,
                'unMemberId':                    unMemberId,
                'unPagina':                      unPagina,
                'aFilePath':                     aFilePath,
                'aDisplayPath':                  aDisplayPath,
                'aMillisecondsNow':              aMillisecondsNow,
            })                   
                
            
            unRenderedCacheInfo = u"""
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
                        <form style="display: inline" action="%(unBaseURL)s%(unPagina)s" method="get" enctype="multipart/form-data">
                            <input type="hidden" name="theCacheView"  value="%(aViewName)s" />
                            <input type="hidden" name="theNoCache"   value="on" />
                            <input type="hidden" name="theNoCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="submit" value="%(ModelDDvlPlone_ShowNoFromCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDShowNoFromCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        &emsp;
                        <form style="display: inline"  action="%(unBaseURL)s%(unPagina)s/MDDFlushCachedTemplateByUniqueId/"
                            method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theCacheView"  value="%(aViewName)s" />
                            <input type="hidden" name="theCacheEntryUniqueId"   value="%(cMagicReplacementString_UniqueId)s" />
                            <input type="hidden" name="theFlushCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theCacheName" value="ElementIndependent" />
                            <input type="submit" value="%(ModelDDvlPlone_FlushFromCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDFlushCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        &emsp;
                        <form style="display: inline"  action="%(unBaseURL)s%(unPagina)s/MDDFlushCachedTemplateByUniqueId/"
                            method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theCacheView"  value="%(aViewName)s" />
                            <input type="hidden" name="theCacheEntryUniqueId"   value="%(cMagicReplacementString_UniqueId)s" />
                            <input type="hidden" name="theFlushCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theCacheName" value="ElementIndependent" />
                            <input type="hidden" name="theFlushDiskCache" value="on" />
                            <input type="submit" value="%(ModelDDvlPlone_FlushFromDiskCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDFlushDiskCacheCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
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
                                    <td align="left"><strong>CacheName</strong></td>
                                    <td align="left">%(aCacheName)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>CacheKind</strong></td>
                                    <td align="left">%(aCacheKind)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>Id</strong></td>
                                    <td align="left">%(cMagicReplacementString_UniqueId)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_FilePath_label)s</strong></td>
                                    <td align="left">%(aDisplayPath)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Time_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Milliseconds)s ms</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Len_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Len)s chars</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_User_label)s</strong></td>
                                    <td align="left">%(unMemberId)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Date_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Date)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_SchemeHostAndDomain_label)s</strong></td>
                                    <td align="left">%(unSchemeHostAndDomain)s</td>
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
            
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Milliseconds, fStrGrp( unosMilliseconds))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Len,          fStrGrp( len( unRenderedTemplate)))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Date,         fMillisecondsToDateTime( aEndMillis).rfc822())
               
            if aDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedTemplate, unRenderedCacheInfo,)
            else:
                unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedCacheInfo, unRenderedTemplate,)
            
        
                
                
                
         # ###########################################################
        """Add a comment with the rendering time at the top of the rendered HTML, to be used when reading from disk to determine if the HTML on disk has expired or can be reused.
        
        """
        unRenderingMillisecondsHTMLComment = """<!-- %s%s -->""" % ( cHTMLRenderingTimeComment_Keyword, aEndMillis, )
        unRenderedTemplateWithCacheInfo = '%s\n%s' % ( unRenderingMillisecondsHTMLComment, unRenderedTemplateWithCacheInfo,)
        
              
        
        
        
        # ###########################################################
        """CRITICAL SECTION to register in the promised cache entry the HTML result of rendering the template. 
        
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
              
            # ###########################################################
            """Check if somebody messed with the promised cache entry, so it is not being updated here.
            
            """
            if ( unPromiseMade == unExistingOrPromiseCacheEntry.vPromise):

                unMillisecondsNow   = fMillisecondsNow()
                
                unExistingOrPromiseCacheEntry.vHTML            = unRenderedTemplateWithCacheInfo
                unExistingOrPromiseCacheEntry.vDateMillis      = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                unExistingOrPromiseCacheEntry.vLastHit         = unMillisecondsNow
                
                unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                
                unStatisticsUpdate = {
                    cCacheStatistics_TotalRenderings:    1,
                    cCacheStatistics_TotalCharsCached: len( unExistingOrPromiseCacheEntry.vHTML),
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)
                
                
            # ###########################################################
            """MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
            
            """
            self._pFlushCacheEntriesToReduceMemoryUsed( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent)
               
            


            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
             
        theVariables[ 'unTemplateToCache'] = unRenderedTemplateWithCacheInfo[:]
        

        # ###########################################################
        """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
        
        """
        unRenderedTemplateToReturn = unRenderedTemplateWithCacheInfo.replace(    
            '<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
            '<span>%s' % someTranslations[ 'ModelDDvlPlone_JustCached'],
        )   
        

        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn[:]
        if unExistingOrPromiseCacheEntry:
            if unExistingOrPromiseCacheEntry.vUniqueId:
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                    cMagicReplacementString_UniqueId, 
                    str( unExistingOrPromiseCacheEntry.vUniqueId)
                )

        unDurationString = '%d ms' % unosMilliseconds
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
            u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
            u'%s</span>' % unDurationString
        )
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
           cMagicReplacementString_CacheCode, 
           '%d' % aEndMillis
        )

        theVariables[ 'unTemplateToReturn'] = unRenderedTemplateToReturnWithDuration
        
        aRenderResult.update( {
            'status':            cRenderStatus_Completed, 
            'rendered_html':     unRenderedTemplateToReturnWithDuration,
        })                                    
        return aRenderResult
        
        

            
            

 
    
    security.declarePrivate( '_fRenderTemplateOrCachedElementIndependent_Phase_StoreDisk')
    def _fRenderTemplateOrCachedElementIndependent_Phase_StoreDisk(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """Store the rendered HTML on disc, for the project, for the currently negotiated language, and for the specified view.
        
        """
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        if not theVariables:
            return False
        
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        aViewName                     = theVariables[ 'aViewName']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        someTranslations              = theVariables[ 'someTranslations']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        unTemplateToReturn            = theVariables[ 'unTemplateToReturn']
        unTemplateToCache             = theVariables[ 'unTemplateToCache']
        unSchemeHostAndDomain         = theVariables[ 'unSchemeHostAndDomain']
        
        
        if not aCacheDiskEnabled:
            return False
        
        if not unTemplateToCache:
            return False
        
        if not unExistingOrPromiseCacheEntry:
            return False
        
        
        # ###########################################################
        """Try to access the directory containing the element independent files with cached HTML.
            
        """
        if not aCacheDiskPath:
            return False

        aCacheDiskPathExist = False
        try:
            aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
        except:
            None
        if not aCacheDiskPathExist:
            try:
                os.makedirs(aCacheDiskPath)
            except:
                None
            try:
                aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
            except:
                None
            if not aCacheDiskPathExist:
                return False
        
        
        # ###########################################################
        """Access directories for project and language, creating them if the directories do not exist.
            
        """
        aProjectPath = os.path.join( aCacheDiskPath, aProjectName)
        aProjectPathExist = False
        try:
            aProjectPathExist = os.path.exists( aProjectPath)
        except:
            None
        if not aProjectPathExist:
            try:
                os.mkdir( aProjectPath, cCacheDisk_ElementIndependent_FolderCreateMode_Project)
            except:
                None
            try:
                aProjectPathExist = os.path.exists( aProjectPath)
            except:
                None
            if not aProjectPathExist:
                return False
        
        aLanguagePath = os.path.join( aProjectPath, aNegotiatedLanguage)
        aLanguagePathExist = False
        try:
            aLanguagePathExist = os.path.exists( aLanguagePath)
        except:
            None
        if not aLanguagePathExist:
            try:
                os.mkdir( aLanguagePath, cCacheDisk_ElementIndependent_FolderCreateMode_Language)
            except:
                None
            try:
                aLanguagePathExist = os.path.exists( aLanguagePath)
            except:
                None
            if not aLanguagePathExist:
                return False
        
            
            
        # ###########################################################
        """Write the page on disk cache file.
            
        """
        aViewFileName  = '%s-%s%s' % (  aViewName, unSchemeHostAndDomain, cCacheDiskFilePostfix)
        aViewPath      = os.path.join( aLanguagePath, aViewFileName)

        aWritten = False
        try:
            aViewFile  = None
            try:
                aViewFile = open( aViewPath, cCacheDisk_ElementIndependent_FileOpenWriteMode_View, cCacheDisk_ElementIndependent_FileOpenWriteBuffering_View)
                aViewFile.write( unTemplateToCache)
            finally:
                if aViewFile:
                    aViewFile.close()
            aWritten = True
        except IOError:
            return False
  
        if not aWritten:
            return False
        
        unExistingOrPromiseCacheEntry.vFilePath = aViewPath
        
        

        # ###########################################################
        """Update statistics of written file and chars.
            
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            unExistingOrPromiseCacheEntry.vFilePath        = aViewPath
                
            unStatisticsUpdate = {
                cCacheStatistics_TotalFilesWritten:   1,
                cCacheStatistics_TotalCharsWritten:   len( unTemplateToCache),
            }
            self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, cCacheName_ElementIndependent, unStatisticsUpdate)

        
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        return True

                        
            
            
            
            
            
       
    security.declarePrivate( 'fRenderHandlers_ElementIndependent')
    def fRenderHandlers_ElementIndependent(self, theModelDDvlPloneTool, theContextualObject,):
        """methods to handle the rendering phases for element independent cache entries.
        """
        someHandlers = {
            'memory':  self._fRenderTemplateOrCachedElementIndependent_Phase_TryMemory,
            'disc':    self._fRenderTemplateOrCachedElementIndependent_Phase_TryDisk,
            'render':  self._fRenderTemplateOrCachedElementIndependent_Phase_Render,
            'store':   self._fRenderTemplateOrCachedElementIndependent_Phase_StoreDisk,
        }
        return someHandlers
    
        
            
            
            
            
            
            
            
            
            
            
    
    # ###################################################################
    """Cache entries associated with specific elements.
    
    """

        
    

        
         

       
    security.declarePrivate( '_fRenderTemplateOrCachedForElement_Phase_TryMemory')
    def _fRenderTemplateOrCachedForElement_Phase_TryMemory(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None,
        theVariables={}):
        """ Return theHTML, from cache or just rendered, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        In-memory cache structure of dictionaries for views:
        
        Element Dependent 
        
        'Project' : {
            'Language' : {
                'Root' : {
                    'Element' : {
                        'View' : {
                            'Relation' : {
                                'Related' : {
                                    'SchemeHostAndDomain' : object( ) # CacheEntry
                                }
                            }
                        }
                    }
                }
            }
        }
        """
                
        aRenderResult = self._fNewVoidRenderResult_Phase_TryMemory()

        unosMillisBeforeMatch   = fMillisecondsNow()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if theModelDDvlPloneTool == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        if theContextualObject == None:
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        
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
                aCacheKind       = cCacheName_ForElements
                
        
        if not aRoleKindToIndex:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
            
        
        if cForbidCaches or not self.fGetCacheConfigParameter_CacheEnabled( theModelDDvlPloneTool, theContextualObject, aCacheName):
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
           
        if theVariables == None:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
           
        
        unCacheEntryUniqueId = ''
        unCachedTemplate = None
              
        aBeginMillis = fMillisecondsNow()
                
        # ###########################################################
        """Only cache objects that allow caching.
        
        """
        anIsCacheable = False
        try:
            anIsCacheable = theContextualObject.fIsCacheable()
        except:
            None
        if not anIsCacheable:    
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        
        
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
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        aNegotiatedLanguage = unosPreferredLanguages[ 0]   
        if not aNegotiatedLanguage:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        
        unElementId = ''
        try:
            unElementId = theContextualObject.getId()
        except:
            None
        if not unElementId:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
         
        
        unElementUID = ''
        try:
            unElementUID = theContextualObject.UID()
        except:
            None
        if not unElementUID:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
               
        unElementTitle = theContextualObject.Title()
        if not unElementTitle:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult

        unElementURL   = theContextualObject.absolute_url()
        if not unElementURL:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
           
        unElementPath = '/'.join( theContextualObject.getPhysicalPath())
        if not unElementPath:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult

        
        unElementMetaType = ''
        try:
            unElementMetaType =theContextualObject.meta_type
        except:
            None

        unElementArchetypeName = ''
        try:
            unElementArchetypeName =theContextualObject.archetype_name
        except:
            None
            
        unElementPortalType = ''
        try:
            unElementPortalType =theContextualObject.portal_type
        except:
            None
 
        unRootElementId   = ''
        unRootElementUID  = ''
        unRootElementPath = ''
        
        unRootElement = None
        try:
            unRootElement = theContextualObject.getRaiz()
        except:
            None
        if ( unRootElement == None):
            unRootElementId   = unElementId
            unRootElementUID  = unElementUID
            unRootElementPath = unElementPath
        else:
            unRootElementPath = '/'.join( unRootElement.getPhysicalPath())
            if not unRootElementPath:
                unRootElementPath = unElementPath

            try:
                unRootElementUID     = unRootElement.UID()
            except:
                None
            if not unRootElementUID:
                unRootElementUID  = unElementUID
                unRootElementPath = unElementPath
                
            try:
                unRootElementId     = unRootElement.getId()
            except:
                None          
            if not unRootElementId:
                unRootElementId   = unElementId
            
            
                
        aViewName = theTemplateName
        if not aViewName:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        if aViewName.find( '%s') >= 0:
            if not ( aProjectName == cDefaultNombreProyecto):
                aViewName = aViewName % aProjectName
            else:
                aViewName = aViewName.replace( '%s', '')
        if not aViewName:
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        

        
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
            
            
            
        unRootElementURL = unRootElement.absolute_url()
                    
        unParsedRootElementURL = self.fURLParse( theModelDDvlPloneTool, theContextualObject, unRootElementURL, )
        if ( not unParsedRootElementURL):
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
                   
        
        if ( not unParsedRootElementURL[ 0]) or ( not unParsedRootElementURL[ 1]):
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
        
        unSchemeHostAndDomain = '%s-%s' % ( unParsedRootElementURL[ 0], unParsedRootElementURL[ 1],)
        
            
        # ###################################################################
        """CRITICAL SECTION to access and modify cache control structure, for Cache entries associated with specific elements.
        
        """
        unExistingOrPromiseCacheEntry = None
        unCachedTemplate              = None
        unPromiseMade                 = None                      
        
        anActionToDo                  = None
        somePossibleActions           = [ 'UseFoundEntry', 'MakePromise', 'JustFallbackToRenderNow', ] # Just to document the options handled by logic below
        
        someFilesToDelete = [ ]
        
        someExistingCacheEntriesInWrongState = [ ]
        
        
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            # ###########################################################
            """Retrieve within thread safe section, to be used later, the configuration paameters specifying: whether to render a cache hit information collapsible section at the top or bottom of the view, or none at all, whether the disk caching is enabled, and the disk cache files base path.
            
            """
            aDisplayCacheHitInformation = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_DisplayCacheHitInformation)
            aCacheDiskEnabled           = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskEnabled)
            aCacheDiskPath              = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskPath)
            unExpireDiskAfterSeconds    = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_ExpireDiskAfterSeconds)
            

            # ###########################################################
            """All Cache Entries that have expired and are forced to expire shall be flushed, whether memory used is over the limit, or not.
            
            """  
            self._pFlushCacheEntriesForcedtoExpire(theModelDDvlPloneTool, theContextualObject, theFilesToDelete=someFilesToDelete)       
      
                    
                        
             
            # ###########################################################
            """Traverse cache control structures to access the cache entry corresponding to the parameters. Elements found missing shall be created, to hook up the new cache entry.
            
            """
            someCachedTemplatesForProject = self.fGetOrInitCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, aCacheName, aProjectName)                              
    
            someCachedTemplatesForLanguage = someCachedTemplatesForProject.get( aNegotiatedLanguage, None)
            if someCachedTemplatesForLanguage == None:
                someCachedTemplatesForLanguage = { }
                someCachedTemplatesForProject[ aNegotiatedLanguage] = someCachedTemplatesForLanguage
                
    
            someCachedTemplatesForRoot = someCachedTemplatesForLanguage.get( unRootElementUID, None)
            if someCachedTemplatesForRoot == None:
                someCachedTemplatesForRoot = { }
                someCachedTemplatesForLanguage[ unRootElementUID] = someCachedTemplatesForRoot
    
            someCachedTemplatesForElement = someCachedTemplatesForRoot.get( unElementUID, None)
            if someCachedTemplatesForElement == None:
                someCachedTemplatesForElement = { }
                someCachedTemplatesForRoot[ unElementUID] = someCachedTemplatesForElement
                    
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
    
            someCachedTemplateForSchemeHostAndDomain = someCachedTemplateForRelatedElement.get( unSchemeHostAndDomain, None)
            if someCachedTemplateForSchemeHostAndDomain == None:
                someCachedTemplateForSchemeHostAndDomain = { }
                someCachedTemplateForRelatedElement[ unSchemeHostAndDomain] = someCachedTemplateForSchemeHostAndDomain
    
                               
                
                
            # ###########################################################
            """Obtain the Cache entry, if exists.
            
            """
            # ACV 20110217 add host and domain to the cache entries store tree
            # anExistingCacheEntry = someCachedTemplateForRelatedElement.get( aRoleKindToIndex, None)
            anExistingCacheEntry = someCachedTemplateForSchemeHostAndDomain.get( aRoleKindToIndex, None)
            
            
            anExistingCacheEntryInWrongState = None
            
            
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
                aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                aCacheEntryInWrongStateInfo.update( {
                    'cached_entry':        anExistingCacheEntry,
                    'cached_entry_holder': someCachedTemplateForSchemeHostAndDomain,
                    'cached_entry_key':    aRoleKindToIndex,            
                })                    
                someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)
                
                anActionToDo = 'MakePromise'
                
            elif not anExistingCacheEntry.vPromise:
                # ###########################################################
                """A null promise is a sign something went wrong with its resolution. A new entry shall be created, and shall replace the existing one in the cache control structure.
                
                """
                aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                aCacheEntryInWrongStateInfo.update( {
                    'cached_entry':        anExistingCacheEntry,
                    'cached_entry_holder': someCachedTemplateForSchemeHostAndDomain,
                    'cached_entry_key':    aRoleKindToIndex,            
                })                    
                someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)

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
                    """A totally empty rendered template HTML means it is no longer useful (it shall always contain at least a smallish string or HTML element). A new entry shall be created, and shall replace the existing one in the cache control structure.
                    
                    """
                    aCacheEntryInWrongStateInfo = self._fNewVoidCachedEntryInWrongStateInfo()
                    aCacheEntryInWrongStateInfo.update( {
                        'cached_entry':        anExistingCacheEntry,
                        'cached_entry_holder': someCachedTemplateForSchemeHostAndDomain,
                        'cached_entry_key':    aRoleKindToIndex,            
                    })                    
                    someExistingCacheEntriesInWrongState.append( aCacheEntryInWrongStateInfo)
                    
                    anActionToDo = 'MakePromise'
                    
                else:
                    # ###########################################################
                    """Found cached template: Cache Hit. Update expiration time for the cache entry. Update cache hit statistics, and return the cached HTML
                    
                    """
                    unMillisecondsNow = fMillisecondsNow()

                    anExistingCacheEntry.vHits += 1
                    anExistingCacheEntry.vLastHit = unMillisecondsNow 
                    anExistingCacheEntry.vLastUser = unMemberId                         

                     
                    unExistingCacheEntryChars = 0
                    if anExistingCacheEntry.vHTML:
                        unExistingCacheEntryChars = len( anExistingCacheEntry.vHTML)
    
                    unStatisticsUpdate = {
                        cCacheStatistics_TotalCacheHits:    1,
                        cCacheStatistics_TotalCharsSaved:   unExistingCacheEntryChars,
                        cCacheStatistics_TotalTimeSaved:    max( anExistingCacheEntry.vMilliseconds, 0),
                    }
                    self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                    
                
                    
                    # ###########################################################
                    """Renew the age of the cache entry in the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                    See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                    
                    """
                    
                    unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, aCacheName)
                    if unListNewSentinel:
                        anExistingCacheEntry.pUnLink()   # if for some bad reason there is no list new sentinel, do not remove from the list, or it will never be flushed at any age.
                        unListNewSentinel.pLink( anExistingCacheEntry) 
                    
                    
                    
                    
                    # ###########################################################
                    """Returning the cache entry found, and an indication that no promise was made (so no rendering has to be produced to fullfill it), and there is no need to just fallback and render it now
                    
                    """
                    unExistingOrPromiseCacheEntry = anExistingCacheEntry
                    anActionToDo                  = 'UseFoundEntry'

                    
                  
                    
                    
                    
                    
            # ###########################################################
            """Remove cache entries that are in wrong state, more likely because of an error while trying to fulfill the promise to be rendered.
            
            """
            if someExistingCacheEntriesInWrongState:
                self._pRemoveCachedEntriesInWrongState( someExistingCacheEntriesInWrongState)
               
                    
                   
                    
                    
                    
            if not ( anActionToDo == 'UseFoundEntry'):
                # ###########################################################
                """Not Found usable cached template: Cache Fault. Update cache fault statistics.
                
                """
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheFaults:    1,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                
                
                
            if anActionToDo == 'MakePromise':
                # ###########################################################
                """Create a new cache entry as a promise to be fullfilled after the CRITICAL SECTION, and hook it up in the cache control structure.
                
                """

                
           
            
                # ###########################################################
                """Allocate a new unique id for the cache entry, 
                
                """
                    
                unCacheEntryUniqueId = self.fGetCacheStoreNewUniqueId( theModelDDvlPloneTool, theContextualObject,) 
                unMillisecondsNow = fMillisecondsNow()
                unExpireAfterSeconds      = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_ExpireAfterSeconds)
                unForceExpire             = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_ForceExpire)

                unPromiseMade = unMillisecondsNow
                
                aNewCacheEntry = MDDRenderedTemplateCacheEntry_ForElement(
                    theCacheName         =aCacheName,
                    theCacheKind         =aCacheKind,
                    theProjectName       =aProjectName,
                    theUniqueId          =unCacheEntryUniqueId,
                    theValid             =True,
                    thePromise           =unPromiseMade,
                    theUser              =unMemberId,
                    theDateMillis        =unMillisecondsNow,
                    theProject           =aProjectName,
                    theView              =aViewName,
                    theLanguage          =aNegotiatedLanguage,
                    theHTML              =None,
                    theMilliseconds      =0,
                    theExpireAfterSeconds=unExpireAfterSeconds,
                    theForceExpire       =unForceExpire,
                    theMetaType          =unElementMetaType,
                    thePortalType        =unElementPortalType,
                    theArchetypeName     =unElementArchetypeName,
                    theElementId         =unElementId,
                    theUID               =unElementUID,
                    theTitle             =unElementTitle,
                    theURL               =unElementURL,
                    theRootPath          =unRootElementPath,
                    theRootUID           =unRootElementUID,
                    theRootId            =unRootElementId,
                    thePath              =unElementPath,
                    theRoleKind          =aRoleKindToIndex,
                    theRelation          =unRelationCursorName,
                    theSchemeHostAndDomain=unSchemeHostAndDomain,
                    theCurrentUID        =unCurrentElementUID,
                )
                
                unExistingOrPromiseCacheEntry = aNewCacheEntry
                                    
                
                
                # ###########################################################
                """Hook up the new cache entry promise in the cache control structure. The promised cache entry shall be fullfilled after the CRITICAL SECTION, by reading the page HTML from disk cache, or rendering the page.
                
                """
                someCachedTemplateForSchemeHostAndDomain[ aRoleKindToIndex] = aNewCacheEntry

                
                aRenderResult.update( {
                    'cache_name':     aCacheName,
                    'promise_made':   unExistingOrPromiseCacheEntry,
                    'promise_holder': someCachedTemplatesForLanguage,
                    'promise_key':    aViewName,
                })
            
                
                 
                # ###########################################################
                """Add unique id of cache entry to the list ordered by their last usage time, that later allows to remove from cache the entries that have been used less recently, and recover its memory.
                See section above with comment starting with : MEMORY consumed maintenance: Release memory if exceed max ...
                
                """
                unListNewSentinel = self.fGetCacheStoreListSentinel_New( theModelDDvlPloneTool, theContextualObject, aCacheName)
                if unListNewSentinel:
                    unListNewSentinel.pLink( aNewCacheEntry) 
    
                
               
                
                # ###########################################################
                """Add the entry to the index by Cache Entry Unique Id.
                
                """
                self._pAddCacheEntryToUniqueIdIndex( theModelDDvlPloneTool, theContextualObject, aNewCacheEntry)
                

                
                # ###########################################################
                """Add the entry to the index by UID.
                
                """
                self._pAddCacheEntryToUIDIndex( theModelDDvlPloneTool, theContextualObject, aNewCacheEntry)
                
                

                
                # ###########################################################
                """Update cache statistics.
                
                """                    
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheEntries:    1,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                
                
                
                    
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            
        if someFilesToDelete:
            self._pRemoveDiskCacheFiles(  theModelDDvlPloneTool, theContextualObject, someFilesToDelete)
            
            
            
            
        # ###########################################################
        """Act according to the analysis made of the Cache entry, and decide how to proceed: using it if retrieved, promissing to create a new one, or just fallback to render the template now and return it.
        
        """
        
        

        someTranslations = self._fTranslationsToRenderTemplate( theModelDDvlPloneTool, theContextualObject,)
        
        
        if anActionToDo == 'UseFoundEntry':
            # ###########################################################
            """Found entry was good: sucessful cache hit.
            
            """
            if unCachedTemplate:
                # ###########################################################
                """The unCachedTemplate variable should hold HTML. 
                
                """
                unRenderedTemplateToReturn = unCachedTemplate.replace(    
                    u'<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
                    u'<span>%(ModelDDvlPlone_Cached)s' % someTranslations,
                )   
    
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn[:]
                if unExistingOrPromiseCacheEntry:
                    if unExistingOrPromiseCacheEntry.vUniqueId:
                        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                            cMagicReplacementString_UniqueId, 
                            str( unExistingOrPromiseCacheEntry.vUniqueId)
                        )
                
                aEndMillis = fMillisecondsNow()
                aMilliseconds = aEndMillis - aBeginMillis
                unDurationString = '%d ms' % aMilliseconds
                
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                    u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                    u'%s</span>' % unDurationString
                )
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                   cMagicReplacementString_CacheCode, 
                   '%d' % aEndMillis
                )

                
                
                aRenderResult.update( {
                    'status':            cRenderStatus_Completed, 
                    'rendered_html':     unRenderedTemplateToReturnWithDuration,
                })                                    
                return aRenderResult
            
            
        if ( anActionToDo == 'UseFoundEntry') or ( anActionToDo == 'JustFallbackToRenderNow') or ( ( anActionToDo == 'MakePromise') and ( not unPromiseMade)) or not ( anActionToDo == 'MakePromise') or (unExistingOrPromiseCacheEntry == None):
            # ###########################################################
            """Entry was found, but something was wrong, or it has been decided that the action is to just render now, or a promise has been made but there is no promise code, or a the action is not the remaining possiblity of MakePromise , or no promise entry has been created. Fallback to render now.
            
            """
            unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
                theModelDDvlPloneTool=theModelDDvlPloneTool, 
                theContextualObject  =theContextualObject, 
                theTemplateName      =theTemplateName, 
                theAdditionalParams =theAdditionalParams,
            )
            
            if aDisplayCacheHitInformation:
                if aDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                    unRenderedTemplateToReturn = unRenderedTemplate + ( u'\n<br/><br/><font size="1"><strong>%(ModelDDvlPlone_JustRendered)s</strong></font>' % someTranslations)
                elif aDisplayCacheHitInformation == cDisplayCacheHitInformation_Top:          
                    unRenderedTemplateToReturn = ( u'<br/><font size="1"><strong>%(ModelDDvlPlone_JustRendered)s</strong></font><br/>\n' % someTranslations) + unRenderedTemplate
                else:
                    unRenderedTemplateToReturn = unRenderedTemplate[:]
                    
            aEndMillis = fMillisecondsNow()
            unDurationString = '%d ms' % ( aEndMillis - aBeginMillis)
            
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn.replace( 
                u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
                u'%s</span>' % unDurationString
            )
            unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
               cMagicReplacementString_CacheCode, 
               '%d' % aEndMillis
            )
            
            aRenderResult.update( {
                'status':            cRenderStatus_Completed, 
                'rendered_html':     unRenderedTemplateToReturnWithDuration,
            })                                    
            return aRenderResult
            
            
            
        theVariables.update( {
            'aCacheName':                    aCacheName,
            'aCacheKind':                    aCacheKind,
            'aBeginMillis':                  aBeginMillis,
            'anActionToDo':                  anActionToDo,
            'unExistingOrPromiseCacheEntry': unExistingOrPromiseCacheEntry,
            'unPromiseMade':                 unPromiseMade,
            'unCacheEntryUniqueId':          unCacheEntryUniqueId,
            'unRelationCursorName':          unRelationCursorName,
            'unElementId':                   unElementId,
            'unCurrentElementUID':           unCurrentElementUID,
            'aProjectName':                  aProjectName,
            'aNegotiatedLanguage':           aNegotiatedLanguage,
            'unCacheId':                     unCacheEntryUniqueId,
            'unElementURL':                  unElementURL,
            'unElementUID':                  unElementUID,
            'unRootElementPath':             unRootElementPath,
            'unRootElementUID':              unRootElementUID,
            'unRootElementId':               unRootElementId,
            'unElementPath':                 unElementPath,
            'aViewName':                     aViewName,
            'unSchemeHostAndDomain':         unSchemeHostAndDomain,
            'aRoleKindToIndex':              aRoleKindToIndex,
            'unMemberId':                    unMemberId,
            'unCachedTemplate':              unCachedTemplate,
            'someTranslations':              someTranslations,
            'aDisplayCacheHitInformation':   aDisplayCacheHitInformation,
            'aCacheDiskEnabled':             aCacheDiskEnabled,
            'aCacheDiskPath':                aCacheDiskPath,
            'unExpireDiskAfterSeconds':      unExpireDiskAfterSeconds,
            'unElementId':                   unElementId,
            'unElementMetaType':             unElementMetaType,
            'unElementPortalType':           unElementPortalType,
            'unElementArchetypeName':        unElementArchetypeName,
        })
        
        aRenderResult.update( {
            'status':            cRenderStatus_Continue, 
        })                                    
        return aRenderResult
        

    
    
    
    
    
    

 
    
    security.declarePrivate( '_fRenderTemplateOrCachedForElement_Phase_TryDisk')
    def _fRenderTemplateOrCachedForElement_Phase_TryDisk(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """No usable cache entry has been found. Try to find the cached HTML on disc, for the project, the root UID, for the currently negotiated language, modulus of element UID, element uid, view, relation , current related UID, and role/user id.
        
        """
        
        aRenderResult = self._fNewVoidRenderResult_Phase_TryDisk()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if not theVariables:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
                
        
        aCacheName                    = theVariables[ 'aCacheName']
        aCacheKind                    = theVariables[ 'aCacheKind']
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unRelationCursorName          = theVariables[ 'unRelationCursorName'] 
        unCurrentElementUID           = theVariables[ 'unCurrentElementUID'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        unElementURL                  = theVariables[ 'unElementURL']
        unElementId                   = theVariables[ 'unElementId']
        unElementUID                  = theVariables[ 'unElementUID']
        unRootElementPath             = theVariables[ 'unRootElementPath']
        unRootElementUID              = theVariables[ 'unRootElementUID']
        unRootElementId               = theVariables[ 'unRootElementId']
        unElementPath                 = theVariables[ 'unElementPath']
        aViewName                     = theVariables[ 'aViewName']
        unSchemeHostAndDomain         = theVariables[ 'unSchemeHostAndDomain']
        aRoleKindToIndex              = theVariables[ 'aRoleKindToIndex']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        someTranslations              = theVariables[ 'someTranslations']
        aDisplayCacheHitInformation   = theVariables[ 'aDisplayCacheHitInformation']
        unExpireDiskAfterSeconds      = theVariables[ 'unExpireDiskAfterSeconds']
                 
        if not aCacheDiskEnabled:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        

        
        if not aCacheDiskPath:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult

        # ###########################################################
        """Assemble the name of the disk file holding the cached HTML for the entry.
            
        """            
        aCacheContainerPath = self.fCacheContainerPath( theModelDDvlPloneTool, theContextualObject,)
        
        aProjectPath           = os.path.join( aCacheContainerPath, aCacheDiskPath, aProjectName)
        aRootElementFolderName = '%s-%s' % ( unRootElementId, unRootElementUID,)
        aRootUIDPath           = os.path.join( aProjectPath, aRootElementFolderName)
        anElementUIDModulus    = self.fModulusUID( unElementUID, cCacheDisk_UIDModulus)
        aElementUIDModulusPath = os.path.join( aRootUIDPath, anElementUIDModulus)
        
        unElementIdShortened   = unElementId[:cMaxElementIdInDiscCachePath]
        unElementIdShortened   = unElementIdShortened.replace( ' ', '_').strip()
        anElementFolderName    = '%s-%s' % ( unElementIdShortened, unElementUID,)
        aElementUIDPath        = os.path.join( aElementUIDModulusPath, anElementFolderName)
        aLanguagePath          = os.path.join( aElementUIDPath, aNegotiatedLanguage)
        aFileName              = '%s-%s-%s-%s-%s%s' % ( aViewName, unRelationCursorName, unCurrentElementUID, unSchemeHostAndDomain, aRoleKindToIndex, cCacheDiskFilePostfix)
        aFilePath              = os.path.join( aLanguagePath, aFileName)
        aDisplayPath           = os.path.join( aProjectName, aRootElementFolderName, anElementUIDModulus, anElementFolderName, aNegotiatedLanguage, aFileName)
        aDisplayPath           = aDisplayPath.replace( '/', '/ ')
        aDisplayPath           = aDisplayPath.replace( '\\', '/ ')

        theVariables[ 'aFilePath']         = aFilePath
        theVariables[ 'aDisplayPath']      = aDisplayPath

        

        
        
        # ###########################################################
        """Try to access the directory containing the element independent files with cached HTML.
            
        """            
        aCacheDiskPathExist = False
        try:
            aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
        except:
            None
        if not aCacheDiskPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        
        # ###########################################################
        """Try to access directories for project, root UID, language, the modulus 100 of the checksum of element UID , element UID, view,  relation, relation current UID, and role/userId.
            
        """
        
        
        aProjectPathExist = False
        try:
            aProjectPathExist = os.path.exists( aProjectPath)
        except:
            None
        if not aProjectPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                    
        
        aRootUIDPathExist = False
        try:
            aRootUIDPathExist = os.path.exists( aRootUIDPath)
        except:
            None
        if not aRootUIDPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        
        aElementUIDModulusPathExist = False
        try:
            aElementUIDModulusPathExist = os.path.exists( aElementUIDModulusPath)
        except:
            None
        if not aElementUIDModulusPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                
        
        
        aElementUIDPathExist = False
        try:
            aElementUIDPathExist = os.path.exists( aElementUIDPath)
        except:
            None
        if not aElementUIDPathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                

        aLanguagePathExist = False
        try:
            aLanguagePathExist = os.path.exists( aLanguagePath)
        except:
            None
        if not aLanguagePathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                            
        
        # ###########################################################
        """Try to retrieve the page from disk cache file.
            
        """
        aFilePathExist = False
        try:
            aFilePathExist = os.path.exists( aFilePath)
        except:
            None
        if not aFilePathExist:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
        
        
        anHTML = ''
        try:
            aViewFile = None
            try:
                aViewFile = open( aFilePath, cCacheDisk_ForElements_FileOpenReadMode_View, cCacheDisk_ForElements_FileOpenReadBuffering_View)
                anHTML = aViewFile.read()
            finally:
                if aViewFile:
                    aViewFile.close()
                
        except IOError:
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
          
        if ( not anHTML) or ( len( anHTML) < cMinCached_HTMLFileLen):
            aRenderResult.update( {
                'status':           cRenderStatus_Continue, 
            })                                    
            return aRenderResult
                    
        
       
        
        unosMillisAfterRead = fMillisecondsNow()
        unosMilliseconds    = unosMillisAfterRead - aBeginMillis

        
        
        # ###########################################################
        """Read the HTML timestamp, and determine if the file has expired.
            
        """
        if unExpireDiskAfterSeconds:
            
            aFirstLinesChunk = anHTML[:cHTMLFirstLinesChunkLen]
            unIndex = aFirstLinesChunk.find( cHTMLRenderingTimeComment_Keyword)
            if unIndex < 0:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unMillisecondsHTMLString = aFirstLinesChunk[ unIndex + len( cHTMLRenderingTimeComment_Keyword):]
            if not unMillisecondsHTMLString:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unLastIndex = unMillisecondsHTMLString.index( ' ')
            if unLastIndex < 0:
                unLastIndex = unMillisecondsHTMLString.index( '-')
                
            if unLastIndex >=0:
                unMillisecondsHTMLString = unMillisecondsHTMLString[:unLastIndex]
            if not unMillisecondsHTMLString:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                
                
            unMillisecondsHTML = 0
            try:
                unMillisecondsHTML = int( unMillisecondsHTMLString)
            except:
                None
            if not unMillisecondsHTML:
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
            
            unTimePassed = int( ( unosMillisAfterRead - unMillisecondsHTML) / 1000)
            
            if unTimePassed >= unExpireDiskAfterSeconds:
                # ###########################################################
                """HTML has expired. Flush the file.
                    
                """
                self._pRemoveDiskCacheFiles( theModelDDvlPloneTool, theContextualObject, [ aFilePath,])
                aRenderResult.update( {
                    'status':           cRenderStatus_Continue, 
                })                                    
                return aRenderResult
                
            
        
        
        
        
        
        

        
        # ###########################################################
        """CRITICAL SECTION to register in the promised cache entry the HTML result of rendering the template. 
        
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
              
            # ###########################################################
            """Check if somebody messed with the promised cache entry, so it is not being updated here.
            
            """
            if ( unPromiseMade == unExistingOrPromiseCacheEntry.vPromise):

                unMillisecondsNow = fMillisecondsNow()
                        
                unExistingOrPromiseCacheEntry.vHTML            = anHTML
                unExistingOrPromiseCacheEntry.vFilePath        = aFilePath
                unExistingOrPromiseCacheEntry.vDisplayPath     = aDisplayPath
                unExistingOrPromiseCacheEntry.vDateMillis      = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                unExistingOrPromiseCacheEntry.vLastHit         = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vDirectory       = aLanguagePath

                
                unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                
                unHTMLLen = len( unExistingOrPromiseCacheEntry.vHTML)
                
                unStatisticsUpdate = {
                    cCacheStatistics_TotalCacheDiskHits:    1,
                    cCacheStatistics_TotalCharsCached:      unHTMLLen,
                    cCacheStatistics_TotalCharsSaved:       unHTMLLen,
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                
                
            # ###########################################################
            """MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
            
            """
            self._pFlushCacheEntriesToReduceMemoryUsed( theModelDDvlPloneTool, theContextualObject, aCacheName)
               
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                        
        theVariables[ 'unTemplateToCache'] = anHTML[:]

        
        
        someTranslations = self._fTranslationsToRenderTemplate( theModelDDvlPloneTool, theContextualObject,)

        
        
        # ###########################################################
        """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
        
        """
        
        unRenderedTemplateToReturn = anHTML.replace(    
            u'<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
            u'<span>%s' % someTranslations[ 'ModelDDvlPlone_DiskCached'],
        )   
        
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn[:]
        if unExistingOrPromiseCacheEntry:
            if unExistingOrPromiseCacheEntry.vUniqueId:
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                    cMagicReplacementString_UniqueId, 
                    str( unExistingOrPromiseCacheEntry.vUniqueId)
                )
                
        unDurationString = '%d ms' % unosMilliseconds
        
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
            u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
            u'%s</span>' % unDurationString
        )
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
           cMagicReplacementString_CacheCode, 
           '%d' % unosMillisAfterRead
        )

        
        theVariables[ 'unTemplateToReturn'] = unRenderedTemplateToReturnWithDuration
                    
        aRenderResult.update( {
            'status':            cRenderStatus_Completed, 
            'rendered_html':     unRenderedTemplateToReturnWithDuration,
        })                                    
        return aRenderResult
        
        
        
            
            
            
    
    
    
    
    
    
    
       

       
    security.declarePrivate( '_fRenderTemplateOrCachedForElement_Phase_Render')
    def _fRenderTemplateOrCachedForElement_Phase_Render(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """No usable cache entry has been found. Render the template, for the project, for the element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
             
        aRenderResult = self._fNewVoidRenderResult_Phase_Render()
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                    'status':           cRenderStatus_ShowError, 
                    'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ForceRender, 
            })                                    
            return aRenderResult
    
        
        if not theVariables:
            if not theModelDDvlPloneTool:
                aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
                })                                    
                return aRenderResult
            aRenderResult.update( {
                'status':           cRenderStatus_ShowError, 
                'error':            cRenderError_MissingParameters,
            })                                    
            return aRenderResult
        
        
        aCacheName                    = theVariables[ 'aCacheName']
        aCacheKind                    = theVariables[ 'aCacheKind']
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unRelationCursorName          = theVariables[ 'unRelationCursorName'] 
        unCurrentElementUID           = theVariables[ 'unCurrentElementUID'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        unElementURL                  = theVariables[ 'unElementURL']
        unElementUID                  = theVariables[ 'unElementUID']
        unRootElementPath             = theVariables[ 'unRootElementPath']
        unRootElementUID              = theVariables[ 'unRootElementUID']
        unRootElementId               = theVariables[ 'unRootElementId']
        unElementPath                 = theVariables[ 'unElementPath']
        aViewName                     = theVariables[ 'aViewName']
        unSchemeHostAndDomain         = theVariables[ 'unSchemeHostAndDomain']
        aRoleKindToIndex              = theVariables[ 'aRoleKindToIndex']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        someTranslations              = theVariables[ 'someTranslations']
        aDisplayCacheHitInformation   = theVariables[ 'aDisplayCacheHitInformation']
        aFilePath                     = theVariables[ 'aFilePath']
        aDisplayPath                  = theVariables[ 'aDisplayPath']
        unElementId                   = theVariables[ 'unElementId']
        unElementMetaType             = theVariables[ 'unElementMetaType']
        unElementPortalType           = theVariables[ 'unElementPortalType']
        unElementArchetypeName        = theVariables[ 'unElementArchetypeName']
        

        someTranslations = self._fTranslationsToRenderTemplate( theModelDDvlPloneTool, theContextualObject,)

    
        
        # ###########################################################
        """Render a caching information collapsible section to append to the rendered template HTML.
            
        """
        unRenderedCacheInfo = u''
        if aDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]:
            
            # ###########################################################
            """Prepare internationalized strings, and info values.
                
            """
            unaPaginaDefault = ''
            try:
                unaPaginaDefault = theContextualObject.fPaginaDefault()
            except:
                None
            if not unaPaginaDefault:
                unaPaginaDefault = 'Textual'
                
            unViewNameWONoHeaderNoFooter = aViewName[:]
            if aViewName.endswith( '_NoHeaderNoFooter'):
                unViewNameWONoHeaderNoFooter = aViewName[: 0 - len( '_NoHeaderNoFooter')]
                                                         
            unPagina = ''
            if unViewNameWONoHeaderNoFooter == unaPaginaDefault:
                unPagina = '/'
            else:
                unPagina = '/%s/' % unViewNameWONoHeaderNoFooter
            
                
            
        
        
        # ###########################################################
        """Render template or invoke callable with HTML result, because it was not found (valid) in the cache. This may take some significant time. Status of cache may have changed since.
        
        """
        unRenderedTemplate = self._fInvokeCallable_Or_RenderTemplate( 
            theModelDDvlPloneTool=theModelDDvlPloneTool, 
            theContextualObject  =theContextualObject, 
            theTemplateName      =theTemplateName, 
            theAdditionalParams =theAdditionalParams,
        )
        
        
        aEndMillis       = fMillisecondsNow()
        unosMilliseconds = aEndMillis - aBeginMillis
                
        unRenderedTemplateWithCacheInfo = unRenderedTemplate
        
  

         
        # ###########################################################
        """If so configured: Append a caching information collapsible section to the rendered template HTML.
        
        """
        if not( aDisplayCacheHitInformation in [ cDisplayCacheHitInformation_Top, cDisplayCacheHitInformation_Bottom,]):
            unRenderedTemplateWithCacheInfo = unRenderedTemplate[:]
        
        else:
            

            aCacheEntryValuesDict = someTranslations.copy()
            aCacheEntryValuesDict.update( {
                'cMagicReplacementString_CacheCode':               cMagicReplacementString_CacheCode,
                'cMagicReplacementString_TimeToRetrieve':          cMagicReplacementString_TimeToRetrieve,
                'cMagicReplacementString_Milliseconds':            cMagicReplacementString_Milliseconds,
                'cMagicReplacementString_Len':                     cMagicReplacementString_Len,
                'cMagicReplacementString_Date':                    cMagicReplacementString_Date,
                'cMagicReplacementString_CollapsibleSectionTitle': cMagicReplacementString_CollapsibleSectionTitle,
                'cMagicReplacementString_UniqueId':                cMagicReplacementString_UniqueId,   
                'aCacheName':                    aCacheName,
                'aCacheKind':                    aCacheKind,
                'aProjectName':                  aProjectName,
                'aNegotiatedLanguage':           aNegotiatedLanguage,
                'unTitle':                       theModelDDvlPloneTool.fAsUnicode( theContextualObject, theContextualObject.Title()),
                'unCacheId':                     unCacheEntryUniqueId,
                'unElementURL':                  unElementURL,
                'unElementDisplayURL':           unElementURL.replace( '/', '/ '),
                'unElementUID':                  unElementUID,
                'unElementPath':                 unElementPath,
                'unElementDisplayPath':          unElementPath.replace( '/', '/ '),
                'unSchemeHostAndDomain':         unSchemeHostAndDomain,
                'aViewName':                     aViewName,
                'aRoleKindToIndex':              aRoleKindToIndex,
                'unMemberId':                    unMemberId,
                'unPagina':                      unPagina,
                'aFilePath':                     aFilePath,
                'aDisplayPath':                  aDisplayPath,
                'unMetaType':                    unElementMetaType,
                'unPortalType':                  unElementPortalType,
                'unArchetypeName':               unElementArchetypeName,
                'unElementId':                   unElementId,
            })                   
                
                        
            
            unRenderedCacheInfo = u"""
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
                        <form style="display: inline" action="%(unElementURL)s%(unPagina)s" method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theCacheView"  value="%(aViewName)s" />
                            <input type="hidden" name="theNoCache"   value="on" />
                            <input type="hidden" name="theNoCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="submit" value="%(ModelDDvlPlone_ShowNoFromCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDShowNoFromCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        &emsp;
                        <form style="display: inline"  action="%(unElementURL)s%(unPagina)s" method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theCacheView"  value="%(aViewName)s" />
                            <input type="hidden" name="theNoCache"   value="on" />
                            <input type="hidden" name="theNoCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theFlushCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="submit" value="%(ModelDDvlPlone_FlushFromCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDFlushCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        &emsp;
                        <form  style="display: inline"  action="%(unElementURL)s%(unPagina)s" method="post" enctype="multipart/form-data">
                            <input type="hidden" name="theCacheView"  value="%(aViewName)s" />
                            <input type="hidden" name="theNoCache"   value="on" />
                            <input type="hidden" name="theNoCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theFlushCacheCode" value="%(cMagicReplacementString_CacheCode)s" />
                            <input type="hidden" name="theFlushDiskCache" value="1" />
                            <input type="submit" value="%(ModelDDvlPlone_FlushFromDiskCacheLink_label)s" 
                                name="theCacheControl" 
                                id="cid_MDDFlushDiskCacheCache_Button" 
                                style="color: Red; font-size: 8pt; font-style: italic; font-weight: 300" />
                        </form>
                        <br/>
                        <table class="listing" ">
                            <thead>
                                <tr>
                                    <th class="nosort"/>
                                    <th class="nosort"/>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="even">
                                    <td align="left"><strong>CacheName</strong></td>
                                    <td align="left">%(aCacheName)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>CacheKind</strong></td>
                                    <td align="left">%(aCacheKind)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>Id</strong></td>
                                    <td align="left">%(cMagicReplacementString_UniqueId)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_FilePath_label)s</strong></td>
                                    <td align="left">%(aDisplayPath)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Time_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Milliseconds)s ms</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Len_label)s</strong></td>
                                    <td align="left">%(cMagicReplacementString_Len)s chars</td>
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
                                    <td align="left"><strong>%(ModelDDvlPlone_SchemeHostAndDomain_label)s</strong></td>
                                    <td align="left">%(unSchemeHostAndDomain)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_Project_label)s</strong></td>
                                    <td align="left">%(aProjectName)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Language_label)s</strong></td>
                                    <td align="left">%(aNegotiatedLanguage)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(title_label)s</strong></td>
                                    <td align="left">%(unTitle)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_MetaType_label)s</strong></td>
                                    <td align="left">%(unMetaType)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_PortalType_label)s</strong></td>
                                    <td align="left">%(unPortalType)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_ArchetypeName_label)s</strong></td>
                                    <td align="left">%(unArchetypeName)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_ElementId_label)s</strong></td>
                                    <td align="left">%(unElementId)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_Path_label)s</strong></td>
                                    <td align="left">%(unElementDisplayPath)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_URL_label)s</strong></td>
                                    <td align="left">%(unElementDisplayURL)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_UID_label)s</strong></td>
                                    <td align="left">%(unElementUID)s</td>
                                </tr>
                                <tr class="odd">
                                    <td align="left"><strong>%(ModelDDvlPlone_View_label)s</strong></td>
                                    <td align="left">%(aViewName)s</td>
                                </tr>
                                <tr class="even">
                                    <td align="left"><strong>%(ModelDDvlPlone_RoleKind_label)s</strong></td>
                                    <td align="left">%(aRoleKindToIndex)s</td>
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
                    someTranslations[ 'ModelDDvlPlone_Relation_label'], 
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
                    someTranslations[  'ModelDDvlPlone_RelatedElement_label'],
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
            
            
                        
            
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Milliseconds, fStrGrp( unosMilliseconds))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Len,          fStrGrp( len( unRenderedTemplate)))
            unRenderedCacheInfo = unRenderedCacheInfo.replace( cMagicReplacementString_Date,         fMillisecondsToDateTime( aEndMillis).rfc822())
               
            if aDisplayCacheHitInformation == cDisplayCacheHitInformation_Bottom:          
                unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedTemplate, unRenderedCacheInfo,)
            else:
                unRenderedTemplateWithCacheInfo = u"%s\n<br/>\n%s" % ( unRenderedCacheInfo, unRenderedTemplate,)
            
        
                
                
                
         # ###########################################################
        """Add a comment with the rendering time at the top of the rendered HTML, to be used when reading from disk to determine if the HTML on disk has expired or can be reused.
        
        """
        unRenderingMillisecondsHTMLComment = """<!-- RenderMilliseconds=%s -->""" % aEndMillis
        unRenderedTemplateWithCacheInfo = '%s\n%s' % ( unRenderingMillisecondsHTMLComment, unRenderedTemplateWithCacheInfo,)
        
        
              
        
        # ###########################################################
        """CRITICAL SECTION to register in the promised cache entry the HTML result of rendering the template. 
        
        """
        someFilesToDelete = [ ]
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
                                    
              
            
            # ###########################################################
            """Check if somebody messed with the promised cache entry, so it is not being updated here.
            
            """
            if ( unPromiseMade == unExistingOrPromiseCacheEntry.vPromise):
                
                unMillisecondsNow   = fMillisecondsNow()

                unExistingOrPromiseCacheEntry.vHTML            = unRenderedTemplateWithCacheInfo
                unExistingOrPromiseCacheEntry.vDateMillis      = unMillisecondsNow
                unExistingOrPromiseCacheEntry.vMilliseconds    = unosMilliseconds
                unExistingOrPromiseCacheEntry.vLastHit         = unMillisecondsNow
                    
                unExistingOrPromiseCacheEntry.vPromise         = cCacheEntry_PromiseFulfilled_Sentinel
                                    
                unStatisticsUpdate = {
                    cCacheStatistics_TotalRenderings:  1,
                    cCacheStatistics_TotalCharsCached: len( unExistingOrPromiseCacheEntry.vHTML),
                }
                self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)
                
                # ###########################################################
                """MEMORY consumed maintenance: Release cached templates expired, and if memory used exceeds the maximum configured for cache, by flushing older cached entries until the amount of memory used is within the configured maximum parameter.
                
                """
                self._pFlushCacheEntriesToReduceMemoryUsed( theModelDDvlPloneTool, theContextualObject, aCacheName, )

            
            
            
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            


            
        theVariables[ 'unTemplateToCache'] = unRenderedTemplateWithCacheInfo[:]
            

        # ###########################################################
        """If the page was rendered with cache configuration parameter vDisplayCacheHitInformation set to non null value, Indicate to the user that this page has just been rendered, without causing side effects to the chached template rendering result.
        
        """
        unRenderedTemplateToReturn = unRenderedTemplateWithCacheInfo.replace(    
            '<span>%s' % cMagicReplacementString_CollapsibleSectionTitle,
            '<span>%s' % someTranslations[ 'ModelDDvlPlone_JustCached'],
        )   
        
        
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturn[:]
        if unExistingOrPromiseCacheEntry:
            if unExistingOrPromiseCacheEntry.vUniqueId:
                unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
                    cMagicReplacementString_UniqueId, 
                    str( unExistingOrPromiseCacheEntry.vUniqueId)
                )
        
        unDurationString = '%d ms' % unosMilliseconds
        
        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
            u'%s</span>' % cMagicReplacementString_TimeToRetrieve, 
            u'%s</span>' % unDurationString
        )

        unRenderedTemplateToReturnWithDuration = unRenderedTemplateToReturnWithDuration.replace( 
           cMagicReplacementString_CacheCode, 
           '%d' % aEndMillis
        )
        
        theVariables[ 'unTemplateToReturn'] = unRenderedTemplateToReturnWithDuration
        
        aRenderResult.update( {
            'status':            cRenderStatus_Completed, 
            'rendered_html':     unRenderedTemplateToReturnWithDuration,
        })                                    
        return aRenderResult
        
        
        
        
        
        
   
    security.declarePrivate( '_fInvokeCallable_Or_RenderTemplate')
    def _fInvokeCallable_Or_RenderTemplate(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None):
        """Invoke callable or Render template or returning the HTML result.
        
        """
        
        aCallable      = None
        aCallableParms = {}
        aCallableCtxt  = None
        if theAdditionalParams:
            aCallable = theAdditionalParams.get( 'callable', None)
            if aCallable:
                aCallableCtxt  = theAdditionalParams.get( 'callable_ctxt', {})
                aCallableParms = theAdditionalParams.get( 'callable_parms', {})
                
                
        unRenderedTemplate = u''
        if aCallable:
            unRenderedTemplate = aCallable( aCallableCtxt, aCallableParms)
        else:
            unRenderedTemplate = theModelDDvlPloneTool.fRenderTemplate( theContextualObject, theTemplateName)

        return unRenderedTemplate
    
    
            

 
    
    security.declarePrivate( '_fRenderTemplateOrCachedForElement_Phase_StoreDisk')
    def _fRenderTemplateOrCachedForElement_Phase_StoreDisk(self, 
        theModelDDvlPloneTool, 
        theContextualObject, 
        theTemplateName, 
        theAdditionalParams=None, 
        theVariables={}):
        """Store the rendered HTML on disc, for the project, the root UID, for the currently negotiated language, modulus of element UID, element uid, view, relation , current related UID, and role/user id.
        
        """
        
        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return False
        
        if not theVariables:
            return False
        
        aCacheName                    = theVariables[ 'aCacheName']
        aCacheKind                    = theVariables[ 'aCacheKind']
        aBeginMillis                  = theVariables[ 'aBeginMillis']
        anActionToDo                  = theVariables[ 'anActionToDo']
        unExistingOrPromiseCacheEntry = theVariables[ 'unExistingOrPromiseCacheEntry'] 
        unRelationCursorName          = theVariables[ 'unRelationCursorName'] 
        unCurrentElementUID           = theVariables[ 'unCurrentElementUID'] 
        unCacheEntryUniqueId          = theVariables[ 'unCacheEntryUniqueId']
        unPromiseMade                 = theVariables[ 'unPromiseMade'] 
        aProjectName                  = theVariables[ 'aProjectName']
        aNegotiatedLanguage           = theVariables[ 'aNegotiatedLanguage']
        unCacheId                     = theVariables[ 'unCacheId']
        unElementURL                  = theVariables[ 'unElementURL']
        unElementId                   = theVariables[ 'unElementId']
        unElementUID                  = theVariables[ 'unElementUID']
        unRootElementPath             = theVariables[ 'unRootElementPath']
        unRootElementUID              = theVariables[ 'unRootElementUID']
        unElementPath                 = theVariables[ 'unElementPath']
        unRootElementId               = theVariables[ 'unRootElementId']
        aViewName                     = theVariables[ 'aViewName']
        unSchemeHostAndDomain         = theVariables[ 'unSchemeHostAndDomain']    
        aRoleKindToIndex              = theVariables[ 'aRoleKindToIndex']
        unMemberId                    = theVariables[ 'unMemberId']
        unCachedTemplate              = theVariables[ 'unCachedTemplate']
        aCacheDiskEnabled             = theVariables[ 'aCacheDiskEnabled']
        aCacheDiskPath                = theVariables[ 'aCacheDiskPath']
        someTranslations              = theVariables[ 'someTranslations']
        aDisplayCacheHitInformation   = theVariables[ 'aDisplayCacheHitInformation']
        unTemplateToReturn            = theVariables[ 'unTemplateToReturn']
        unTemplateToCache             = theVariables[ 'unTemplateToCache']
         
        
        if not aCacheDiskEnabled:
            return False
        
        if not unTemplateToCache:
            return False
        
        if not unExistingOrPromiseCacheEntry:
            return False
        
        
  
        # ###########################################################
        """Try to access the directory containing the element independent files with cached HTML.
            
        """
        if not aCacheDiskPath:
            return False

        aCacheDiskPathExist = False
        try:
            aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
        except:
            None
        if not aCacheDiskPathExist:
            try:
                os.makedirs(aCacheDiskPath)
            except:
                None
            try:
                aCacheDiskPathExist = os.path.exists( aCacheDiskPath)
            except:
                None
            if not aCacheDiskPathExist:
                return False
        
        
        # ###########################################################
        """Access directories, or create as needed, for project, root UID, language, the modulus 100 of the checksum of element UID , element UID, view,  relation, relation current UID, and role/userId.
            
        """
        aProjectPath = os.path.join( aCacheDiskPath, aProjectName)
        aProjectPathExist = False
        try:
            aProjectPathExist = os.path.exists( aProjectPath)
        except:
            None
        if not aProjectPathExist:
            try:
                os.mkdir( aProjectPath, cCacheDisk_ForElements_FolderCreateMode_Project)
            except:
                None
            try:
                aProjectPathExist = os.path.exists( aProjectPath)
            except:
                None
            if not aProjectPathExist:
                return False
        
            
        aRootElementFolderName = '%s-%s' % ( unRootElementId, unRootElementUID,)
        aRootUIDPath = os.path.join( aProjectPath, aRootElementFolderName)
        aRootUIDPathExist = False
        try:
            aRootUIDPathExist = os.path.exists( aRootUIDPath)
        except:
            None
        if not aRootUIDPathExist:
            try:
                os.mkdir( aRootUIDPath, cCacheDisk_ForElements_FolderCreateMode_RootUID)
            except:
                None
            try:
                aRootUIDPathExist = os.path.exists( aRootUIDPath)
            except:
                None
            if not aRootUIDPathExist:
                return False
                        
            
            
            
        anElementUIDModulus = self.fModulusUID( unElementUID, cCacheDisk_UIDModulus)
            
        aElementUIDModulusPath = os.path.join( aRootUIDPath, anElementUIDModulus)
        aElementUIDModulusPathExist = False
        try:
            aElementUIDModulusPathExist = os.path.exists( aElementUIDModulusPath)
        except:
            None
        if not aElementUIDModulusPathExist:
            try:
                os.mkdir( aElementUIDModulusPath, cCacheDisk_ForElements_FolderCreateMode_ElementUIDModulus)
            except:
                None
            try:
                aElementUIDModulusPathExist = os.path.exists( aElementUIDModulusPath)
            except:
                None
            if not aElementUIDModulusPathExist:
                return False
        

            
        
        unElementIdShortened   = unElementId[:cMaxElementIdInDiscCachePath]
        unElementIdShortened   = unElementIdShortened.replace( ' ', '_')
        anElementFolderName = '%s-%s' % ( unElementIdShortened, unElementUID,)
        aElementUIDPath = os.path.join( aElementUIDModulusPath, anElementFolderName)
        aElementUIDPathExist = False
        try:
            aElementUIDPathExist = os.path.exists( aElementUIDPath)
        except:
            None
        if not aElementUIDPathExist:
            try:
                os.mkdir( aElementUIDPath, cCacheDisk_ForElements_FolderCreateMode_ElementUID)
            except:
                None
            try:
                aElementUIDPathExist = os.path.exists( aElementUIDPath)
            except:
                None
            if not aElementUIDPathExist:
                return False
        

           

        aLanguagePath = os.path.join( aElementUIDPath, aNegotiatedLanguage)
        aLanguagePathExist = False
        try:
            aLanguagePathExist = os.path.exists( aLanguagePath)
        except:
            None
        if not aLanguagePathExist:
            try:
                os.mkdir( aLanguagePath, cCacheDisk_ForElements_FolderCreateMode_Language)
            except:
                None
            try:
                aLanguagePathExist = os.path.exists( aLanguagePath)
            except:
                None
            if not aLanguagePathExist:
                return False
                        

            
            
        # ###########################################################
        """Write the page on disk cache file.
            
        """
        aViewFileName = '%s-%s-%s-%s-%s%s' % ( aViewName, unRelationCursorName, unCurrentElementUID, unSchemeHostAndDomain, aRoleKindToIndex, cCacheDiskFilePostfix)
        aViewPath = os.path.join( aLanguagePath, aViewFileName)

        aWritten = False
        try:
            aViewFile  = None
            try:
                aViewFile = open( aViewPath, cCacheDisk_ForElements_FileOpenWriteMode_View, cCacheDisk_ForElements_FileOpenWriteBuffering_View)
                aViewFile.write( unTemplateToCache)
            finally:
                if aViewFile:
                    aViewFile.close()
            aWritten = True
        except IOError:
            return False
  
        if not aWritten:
            return False
        
        


        # ###########################################################
        """Update statistics of written file and chars.
            
        """
        try:
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            unExistingOrPromiseCacheEntry.vFilePath        = aViewPath
            unExistingOrPromiseCacheEntry.vDirectory       = aLanguagePath
            
                
            unStatisticsUpdate = {
                cCacheStatistics_TotalFilesWritten:   1,
                cCacheStatistics_TotalCharsWritten:   len( unTemplateToCache),
            }
            self.pUpdateCacheStatistics( theModelDDvlPloneTool, theContextualObject, aCacheName, unStatisticsUpdate)

        
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        
        
        return True
    

        
        
        
        
        
        
       
    security.declarePrivate( 'fRenderHandlers_ForElement')
    def fRenderHandlers_ForElement(self, theModelDDvlPloneTool, theContextualObject,):
        """methods to handle the rendering phases for cache entries associated with specific element.
        """
        someHandlers = {
            'memory':  self._fRenderTemplateOrCachedForElement_Phase_TryMemory,
            'disc':    self._fRenderTemplateOrCachedForElement_Phase_TryDisk,
            'render':  self._fRenderTemplateOrCachedForElement_Phase_Render,
            'store':   self._fRenderTemplateOrCachedForElement_Phase_StoreDisk,
        }
        return someHandlers
    
        
                    
        
        
        
            
            

            
            
            


    security.declarePrivate( 'fIsPrivateCacheViewForNonAnonymousUsers')
    def fIsPrivateCacheViewForQualifiedUsers(self , theContextualObject, theTemplateName):
        """Shall return true when the template name is for a view sensitive to user permissions or roles ( modify portal content, delete, add folders, ) on rendered objects, in addition to the permissions required by Zope/Plone to deliver data to the requester (view, list folder contents, access content information,).
        
        """

        # ##############################################################
        """Assert whether the view is sensitive to users, for the aplication or for the framework.
        
        """
        try:
            unIsPrivateViewForQualifiedUsers = theContextualObject.fIsPrivateCacheViewForQualifiedUsers( theTemplateName)
            if unIsPrivateViewForQualifiedUsers:
                return unIsPrivateViewForQualifiedUsers
        except:
            None
            
        return  theTemplateName in  cPrivateCacheViewsForQualifiedUsers
        
    
        
    
    
        
    