# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Translation.py
#
# Copyright (c) 2008, 2009, 2010 by Model Driven Development sl and Antonio Carrasco Valero
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


from AccessControl import ClassSecurityInfo

from Acquisition  import aq_inner, aq_parent

from Products.CMFCore            import permissions
from AccessControl.Permissions   import access_contents_information   as perm_AccessContentsInformation

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.utils import shasattr



from ModelDDvlPloneTool_Retrieval               import ModelDDvlPloneTool_Retrieval
from ModelDDvlPloneTool_Transactions            import ModelDDvlPloneTool_Transactions

from ModelDDvlPloneTool_Profiling               import ModelDDvlPloneTool_Profiling


from MDD_RefactorComponents                     import MDDRefactor_NewTranslation

from ModelDDvlPloneTool_ImportExport_Constants  import *




cLogExceptions = True

cLogTranslationResults = True




cNewLanguage_UnTranslated = '-u-n-v-e-r-s-i-o-n-e-d-'
cNewLanguage_MissingNewLanguage = '-v-e-r-s-i-o-n-n-a-m-e-m-i-s-s-i-n-g-'


cAcceptedTranslationContainerMetaTypes = cPloneSiteMetaTypes + [ 'ATFolder', 'ATBTreeFolder',]
               
cPermissionsOnTranslationContainers = [ 
    permissions.View,
    perm_AccessContentsInformation,
    permissions.ListFolderContents,
    permissions.AddPortalContent,  
    permissions.AddPortalFolders,
    permissions.ModifyPortalContent,
]




class MDDRefactor_Translation_Exception( Exception): pass




class ModelDDvlPloneTool_Translation( ModelDDvlPloneTool_Profiling):
    """
    """
    security = ClassSecurityInfo()

    
    # ACV 20091001 Unused. Removed.
    #security.declarePrivate( 'fTraversalTargetAdditionalParams')    
    #def fTraversalTargetAdditionalParams( self,):
        #unosParams = {
            #'Do_Not_Translate' : True,
            #'Retrieve_Minimal_Related_Results': True,
        #}
        #return unosParams
    
    
 
     
    security.declarePrivate( 'fTraversalSourcesAdditionalParams')    
    def fTraversalSourcesAdditionalParams( self,):
        unosParams = {
            'Do_Not_Translate' : True,
            'Retrieve_Minimal_Related_Results': True,
        }
        return unosParams
    
        
    
    security.declarePrivate( 'fNewVoidNewTranslationContext')    
    def fNewVoidNewTranslationContext( self,):
        unContext = {
            'original_object':               None,
            'original_object_result':        None,
            'container_object':              None,
            'translation_name':                  None,
            'ModelDDvlPloneTool_Retrieval':  None,
            'ModelDDvlPloneTool_Mutators':   None,
            'checked_permissions_cache':     None,
            'mdd_type_configs':              {},
            'plone_type_configs':            {},
            'all_copy_type_configs':         {},
            'additional_params':             self.fTraversalSourcesAdditionalParams(),
            'report':                        self.fNewVoidNewTranslationReport(),
            'translation_service':           None,
        }
        return unContext
    
      
    
    
    
    
    security.declarePrivate( 'fNewVoidTranslatingInfo')    
    def fNewVoidTranslatingInfo( self,):
        aReport = {
            'success':                             False,
            'element':                             None,
            'title':                               '',
            'id':                                  '',
            'url':                                 '',
            'UID':                                 '',
            'description':                         '',
            'path':                                '',
            'inter_translation_uid':                   '',
            'translation':                             '',
            'translation_comment':                     '',
            'previous_translationing_infos':           [ ],
            'previous_initialized':                False,
            'next_translationing_infos':               [ ],
            'next_initialized':                    False,
            'reused':                              None,
        }
        return aReport
        
    
    
    security.declarePrivate( 'fNewVoidCandidateContainerReport')    
    def fNewVoidCandidateContainerReport( self,):
        aReport = {
            'allowed':                   False,
            'element':                   None,
            'title':                     '',
            'description':               '',
            'id':                        '',
            'path':                      '',
            'UID':                       '',
            'children_titles':           [],
            'children_ids':              [],
            'new_title':                 '',
            'new_id':                    '',
        }
        return aReport
    
    

    security.declarePrivate( 'fNewVoidAllTranslationsReport')    
    def fNewVoidAllTranslationsReport( self,):
        aReport = {
            'success':                             False,
            'translationed_element':                   None,
            'translationed_element_result':            None,
            'original_translation_info':               None,
            'all_translations_by_name':                {},
            'allow_translation':                       False,
            'column_names':                        [],
            'column_translations':                 {},
            'parent_container_report':             None,
            'clipboard_container_report':          None,
            'site_container_report':              None,
        }
        return aReport
    
    
 
    security.declarePrivate( 'fNewVoidNewTranslationReport')    
    def fNewVoidNewTranslationReport( self,):
        unInforme = {
            'success':                  False,
            'status':                   '',
            'condition':                None,
            'exception':                '',
            'new_translation_element':      None,
            'new_translation_element_result': None,            
            'num_elements_translationed':      0,
            'num_mdd_elements_translationed':  0,
            'num_plone_elements_translationed': 0,
            'error_reports':            [ ],
        }
        return unInforme
    
    
    
    
    
    
    
    
    
    

    security.declarePrivate( 'fRetrieveTranslatingInfo')
    def fRetrieveTranslatingInfo( self,
        theTimeProfilingResults             =None,
        theModelDDvlPloneTool_Retrieval     =None,
        theRetrievePreviousTranslations         =False,
        theRetrieveNextTranslations             =False,
        theRecurse                          =False,
        theTranslationedElement                 =None, 
        theAllTranslationsByName                =None,
        theInterTranslationUIDFieldsCache       =None,
        theNewLanguageFieldsCache           =None,
        theFallbackStrategyFieldsCache        =None,
        thePreviousTranslationsLinkFieldsCache  =None,
        theNextTranslationsLinkFieldsCache      =None,
        theAdditionalParams                 =None):
        """Retrieve the translation language and the immediate previous and next translations, recursing if so requested."
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveTranslatingInfo', theTimeProfilingResults)
                      
        try:
            unTranslatingInfo = { 'success': False, }
            try:
                
                unTranslatingInfo = self.fNewVoidTranslatingInfo()
                if ( theTranslationedElement== None):
                    return unTranslatingInfo
                
                unTranslatingInfo[ 'element'] = theTranslationedElement
                
                unAlreadyVisited = { }
                
                self.pRetrieveTranslationInfo_Inner(
                    theTimeProfilingResults             =theTimeProfilingResults,
                    theModelDDvlPloneTool_Retrieval     =theModelDDvlPloneTool_Retrieval,
                    theRetrievePreviousTranslations         =theRetrievePreviousTranslations,
                    theRetrieveNextTranslations             =theRetrieveNextTranslations,
                    theRecurse                          =theRecurse,
                    theAlreadyVisited                   =unAlreadyVisited,
                    theTranslatingInfo                   =unTranslatingInfo, 
                    theAllTranslationsByName                =theAllTranslationsByName,
                    theInterTranslationUIDFieldsCache       =theInterTranslationUIDFieldsCache,
                    theNewLanguageFieldsCache           =theNewLanguageFieldsCache,
                    theFallbackStrategyFieldsCache        =theFallbackStrategyFieldsCache,
                    thePreviousTranslationsLinkFieldsCache  =thePreviousTranslationsLinkFieldsCache,
                    theNextTranslationsLinkFieldsCache      =theNextTranslationsLinkFieldsCache,
                    theAdditionalParams                 =theAdditionalParams,
                )
                
                return unTranslatingInfo
                
                
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fRetrieveTranslatingInfo\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unTranslatingInfo:
                    unTranslatingInfo = { }
                    
                unTranslatingInfo.update( { 
                    'success':      False,
                    'status':       cNewTranslationStatus_Error_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unTranslatingInfo
                        
            return unTranslatingInfo        
        
         
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveTranslatingInfo', theTimeProfilingResults)
                            
           
                                
                

    security.declarePrivate( 'pRetrieveTranslationInfo_Inner')
    def pRetrieveTranslationInfo_Inner( self,
        theTimeProfilingResults             =None,
        theModelDDvlPloneTool_Retrieval     =None,
        theRetrievePreviousTranslations         =False,
        theRetrieveNextTranslations             =False,
        theRecurse                          =False,
        theAlreadyVisited                   =None,
        theTranslatingInfo                   =None, 
        theAllTranslationsByName                =None,
        theInterTranslationUIDFieldsCache       =None,
        theNewLanguageFieldsCache           =None,
        theFallbackStrategyFieldsCache        =None,
        thePreviousTranslationsLinkFieldsCache  =None,
        theNextTranslationsLinkFieldsCache      =None,
        theAdditionalParams                 =None):
        """Initialize the translation language, the base and derived translations into other languages, and their immediate previous and next translations, recursing if so requested."
        
        """
        
        if not theTranslatingInfo:
            return self

        unTranslationedElement = theTranslatingInfo.get( 'element', None)
        if ( unTranslationedElement == None):
            return self
        
        
        
        unAlreadyVisited = theAlreadyVisited
        if unAlreadyVisited == None:
            unAlreadyVisited = { }
            
        
        unModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool_Retrieval
        if not unModelDDvlPloneTool_Retrieval:
            unModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        
        
        unInterTranslationUIDFieldsCache = theInterTranslationUIDFieldsCache
        if ( unInterTranslationUIDFieldsCache == None):
            unInterTranslationUIDFieldsCache = { }
        
        unNewLanguageFieldsCache = theNewLanguageFieldsCache
        if ( unNewLanguageFieldsCache == None):
            unNewLanguageFieldsCache = { }
        
        unFallbackStrategyFieldsCache = theFallbackStrategyFieldsCache
        if ( unFallbackStrategyFieldsCache == None):
            unFallbackStrategyFieldsCache = { }
        
        unPreviousTranslationsLinkFieldsCache = thePreviousTranslationsLinkFieldsCache
        if ( unPreviousTranslationsLinkFieldsCache == None):
            unPreviousTranslationsLinkFieldsCache = { }
        
        unNextTranslationsLinkFieldsCache = theNextTranslationsLinkFieldsCache
        if ( unNextTranslationsLinkFieldsCache == None):
            unNextTranslationsLinkFieldsCache = { }
        
            

            
        unTranslationedElementMetaType = unTranslationedElement.meta_type
            
        
        
        
        unId        = unTranslationedElement.getId()
        theTranslatingInfo[ 'id']       = unModelDDvlPloneTool_Retrieval.fAsUnicode( unId, unTranslationedElement)
        
        unaURL = unTranslationedElement.absolute_url()
        if not ( unaURL[-1:] == '/'):
            unaURL = '%s/' % unaURL                
        theTranslatingInfo[ 'url'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unaURL, unTranslationedElement)
         
        unaUID = unTranslationedElement.UID()
        theTranslatingInfo[ 'UID'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unaUID, unTranslationedElement)
         
        unTitle        = unTranslationedElement.Title()
        theTranslatingInfo[ 'title']       = unModelDDvlPloneTool_Retrieval.fAsUnicode( unTitle, unTranslationedElement)
        
        unaDescription = unTranslationedElement.Description()
        theTranslatingInfo[ 'description'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unaDescription, unTranslationedElement)
        
        unPath        = '/'.join( unTranslationedElement.getPhysicalPath())
        theTranslatingInfo[ 'path']       = unModelDDvlPloneTool_Retrieval.fAsUnicode( unPath, unTranslationedElement)
        
        unInterTranslationUID    = None
        unNewLanguage        = None
        unFallbackStrategy     = None
        unasPreviousTranslations = None
        unasNextTranslations     = None
        
        
        unSchema = None
        try:
            unSchema = unTranslationedElement.schema
        except:
            None
        if not unSchema:
            return self


        unInterTranslationField = unInterTranslationUIDFieldsCache.get( unTranslationedElementMetaType, None)
        if not unInterTranslationField:
            
            unInterTranslationFieldName = None
            try:
                unInterTranslationFieldName = unTranslationedElement.inter_translation_field
            except:
                None
            if unInterTranslationFieldName:
            
                unInterTranslationField = unSchema.get( unInterTranslationFieldName, None)
                if unInterTranslationField:            
                    unInterTranslationUIDFieldsCache[ unTranslationedElementMetaType] = unInterTranslationField
        
        
        if unInterTranslationField:    
            unInterTranslationAccessor = unInterTranslationField.getAccessor( unTranslationedElement)
            if not unInterTranslationAccessor:
                return self
            unInterTranslationUID = None
            try:
                unInterTranslationUID = unInterTranslationAccessor()
            except:
                None
            if not ( unInterTranslationUID == None):
                theTranslatingInfo[ 'inter_translation_uid'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unInterTranslationUID, unTranslationedElement)
            
                    
        
        unTranslationField = unNewLanguageFieldsCache.get( unTranslationedElementMetaType, None)
        if not unTranslationField:
            
            unTranslationFieldName = None
            try:
                unTranslationFieldName = unTranslationedElement.translation_field
            except:
                None
            if not unTranslationFieldName:
                return self
            
            unTranslationField = unSchema.get( unTranslationFieldName, None)
            if not unTranslationField:
                return self
            
            unNewLanguageFieldsCache[ unTranslationedElementMetaType] = unTranslationField
        
        
        unNewLanguage = None
        if unTranslationField:    
            unTranslationAccessor = unTranslationField.getAccessor( unTranslationedElement)
            if not unTranslationAccessor:
                return self
            try:
                unNewLanguage = unTranslationAccessor()
            except:
                None
            if not ( unNewLanguage == None):
                theTranslatingInfo[ 'translation'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unNewLanguage, unTranslationedElement)
                if not ( theAllTranslationsByName == None):
                    if theAllTranslationsByName.has_key( unNewLanguage):
                        raise "Duplicate_Translation_Name"
                    theAllTranslationsByName[ unNewLanguage] = theTranslatingInfo
                
  
        unFallbackStrategyField = unFallbackStrategyFieldsCache.get( unTranslationedElementMetaType, None)
        if not unFallbackStrategyField:
            
            unFallbackStrategyFieldName = None
            try:
                unFallbackStrategyFieldName = unTranslationedElement.translation_comment_field
            except:
                None
            if unFallbackStrategyFieldName:
            
                unFallbackStrategyField = unSchema.get( unFallbackStrategyFieldName, None)
                if unFallbackStrategyField:
                    unFallbackStrategyFieldsCache[ unTranslationedElementMetaType] = unFallbackStrategyField
        
        if unFallbackStrategyField:   
            unFallbackStrategyAccessor = unFallbackStrategyField.getAccessor( unTranslationedElement)
            if not unFallbackStrategyAccessor:
                return self
            unFallbackStrategy = None
            try:
                unFallbackStrategy = unFallbackStrategyAccessor()
            except:
                None
            if not ( unFallbackStrategy == None):
                theTranslatingInfo[ 'translation_comment'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unFallbackStrategy, unTranslationedElement)
        
        
            

            
            
        if ( not theRetrievePreviousTranslations) and ( not theRetrieveNextTranslations):
            return self
        
        unPreviousTranslationsField = unPreviousTranslationsLinkFieldsCache.get( unTranslationedElementMetaType, None)
        unNextTranslationsField     = unNextTranslationsLinkFieldsCache.get( unTranslationedElementMetaType, None)
        
        
        if not unPreviousTranslationsField or not unNextTranslationsField:
            try:
                unTranslatingLinksFieldNames = unTranslationedElement.translationing_link_fields
            except:
                None
            if not unTranslatingLinksFieldNames:
                return self
        
            unPreviousTranslationsLinkFieldName = unTranslatingLinksFieldNames[ 0]
            unNextTranslationsLinkFieldName     = unTranslatingLinksFieldNames[ 1]
            
            if not unPreviousTranslationsLinkFieldName or not unNextTranslationsLinkFieldName:
                return self

            if not unPreviousTranslationsField:
                unPreviousTranslationsField = unSchema.get( unPreviousTranslationsLinkFieldName, None)
                if not unPreviousTranslationsField:
                    return self
                unPreviousTranslationsLinkFieldsCache[ unTranslationedElementMetaType] = unPreviousTranslationsField
                
            if not unNextTranslationsField:
                unNextTranslationsField = unSchema.get( unNextTranslationsLinkFieldName, None)
                if not unNextTranslationsField:
                    return self
                unNextTranslationsLinkFieldsCache[ unTranslationedElementMetaType] = unNextTranslationsField
            
            
        
      
        if theRetrievePreviousTranslations:

            unPreviousTranslationsAccessor = unPreviousTranslationsField.getAccessor( unTranslationedElement)
            if unPreviousTranslationsAccessor:
                unasPreviousTranslations = None
                try:
                    unasPreviousTranslations = unPreviousTranslationsAccessor()
                except:
                    None
                
            if not ( unasPreviousTranslations == None):
                
                for unaPreviousTranslation in unasPreviousTranslations:
                    
                    unaPreviousTranslationUID = unaPreviousTranslation.UID()
                    if unaPreviousTranslationUID:
                
                        unExistingPreviousTranslatingInfo = unAlreadyVisited.get( unaPreviousTranslationUID, None)
                        if unExistingPreviousTranslatingInfo:
                            unReusedTranslatingInfo = unExistingPreviousTranslatingInfo.copy()
                            unReusedTranslatingInfo[ 'reused'] = unExistingPreviousTranslatingInfo
                            unReusedTranslatingInfo[ 'previous_translationing_infos'] = None
                            unReusedTranslatingInfo[ 'previous_initialized'] = False
                            unReusedTranslatingInfo[ 'next_translationing_infos'] = None
                            unReusedTranslatingInfo[ 'next_initialized'] = False
                            
                            theTranslatingInfo[ 'previous_translationing_infos'].append( unReusedTranslatingInfo)  
                      
                        else:
                        
                            unAlreadyVisited[ unaPreviousTranslationUID] = unaPreviousTranslation
                            
                            
                            unPreviousTranslatingInfo = self.fNewVoidTranslatingInfo()
                            unPreviousTranslatingInfo.update( {
                                'element':    unaPreviousTranslation,
                            })
                            
                            theTranslatingInfo[ 'previous_translationing_infos'].append( unPreviousTranslatingInfo)  
                            
                            self.pRetrieveTranslationInfo_Inner( 
                                theTimeProfilingResults             =theTimeProfilingResults,
                                theModelDDvlPloneTool_Retrieval     =unModelDDvlPloneTool_Retrieval,
                                theRetrievePreviousTranslations         =theRecurse,
                                theRetrieveNextTranslations             =False,
                                theRecurse                          =theRecurse,
                                theAlreadyVisited                   =unAlreadyVisited,
                                theTranslatingInfo                   =unPreviousTranslatingInfo, 
                                theNewLanguageFieldsCache           =theNewLanguageFieldsCache,
                                thePreviousTranslationsLinkFieldsCache  =thePreviousTranslationsLinkFieldsCache,
                                theNextTranslationsLinkFieldsCache      =theNextTranslationsLinkFieldsCache,
                                theAdditionalParams                 =theAdditionalParams,
                            )
                        
            theTranslatingInfo[ 'previous_initialized'] = True
            
            

        if theRetrieveNextTranslations:

            unNextTranslationsAccessor = unNextTranslationsField.getAccessor( unTranslationedElement)
            if unNextTranslationsAccessor:
                unasNextTranslations = None
                try:
                    unasNextTranslations = unNextTranslationsAccessor()
                except:
                    None
                
            if not ( unasNextTranslations == None):
                
                for unaNextTranslation in unasNextTranslations:
                    
                    unaNextTranslationUID = unaNextTranslation.UID()
                    if unaNextTranslationUID:
                
                        unExistingNextTranslatingInfo = unAlreadyVisited.get( unaNextTranslationUID, None)
                        if unExistingNextTranslatingInfo:
                            unReusedTranslatingInfo = unExistingNextTranslatingInfo.copy()
                            unReusedTranslatingInfo[ 'reused'] = unExistingNextTranslatingInfo
                            unReusedTranslatingInfo[ 'next_translationing_infos'] = None
                            unReusedTranslatingInfo[ 'next_initialized'] = False
                            unReusedTranslatingInfo[ 'next_translationing_infos'] = None
                            unReusedTranslatingInfo[ 'next_initialized'] = False
                                                        
                            theTranslatingInfo[ 'next_translationing_infos'].append( unExistingNextTranslatingInfo)  
                        
                        else:
                        
                            unAlreadyVisited[ unaNextTranslationUID] = unaNextTranslation
                            
                            
                            unNextTranslatingInfo = self.fNewVoidTranslatingInfo()
                            unNextTranslatingInfo.update( {
                                'element':    unaNextTranslation,
                            })
                            
                            theTranslatingInfo[ 'next_translationing_infos'].append( unNextTranslatingInfo)  
                            
                            self.pRetrieveTranslationInfo_Inner( 
                                theTimeProfilingResults             =theTimeProfilingResults,
                                theModelDDvlPloneTool_Retrieval     =unModelDDvlPloneTool_Retrieval,
                                theRetrievePreviousTranslations         =False,
                                theRetrieveNextTranslations             =theRecurse,
                                theRecurse                          =theRecurse,
                                theAlreadyVisited                   =unAlreadyVisited,
                                theTranslatingInfo                   =unNextTranslatingInfo, 
                                theNewLanguageFieldsCache           =theNewLanguageFieldsCache,
                                thePreviousTranslationsLinkFieldsCache  =thePreviousTranslationsLinkFieldsCache,
                                theNextTranslationsLinkFieldsCache      =theNextTranslationsLinkFieldsCache,
                                theAdditionalParams                 =theAdditionalParams,
                            )
                        
            theTranslatingInfo[ 'next_initialized'] = True
            
        if not unNewLanguage:
            if ( not unasPreviousTranslations) and ( not unasNextTranslations):
                theTranslatingInfo[ 'translation'] = cNewLanguage_UnTranslated
            else:
                theTranslatingInfo[ 'translation'] = cNewLanguage_MissingNewLanguage
                
            
        theTranslatingInfo[ 'success'] = True

        return self
    
    
    
    
    
                
    
    security.declarePrivate( 'fRetrieveAllTranslationsWithContainerPloneSiteAndClipboard')
    def fRetrieveAllTranslationsWithContainerPloneSiteAndClipboard( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool_Retrieval=None,
        theTranslationedElement             =None, 
        theAdditionalParams            =None):
        """Create a new translation of the original object which shall be a root, with the new translation name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveAllTranslationsWithContainerPloneSiteAndClipboard', theTimeProfilingResults)
                      
        try:
            unAllTranslationsReport = { 'success': False, }  
            try:
                
                # ##############################################################
                """Prepare result structure.
                
                """
                unAllTranslationsReport = self.fNewVoidAllTranslationsReport()
                

                # ##############################################################
                """Check for element to create a new translation from.
                
                """
                if ( theTranslationedElement == None):
                    return unAllTranslationsReport
                unAllTranslationsReport[ 'translationed_element'] = theTranslationedElement
                
                
                
                
                # ##############################################################
                """Assert whether the element can be translationed.
                
                """
                unTranslationPermission = False
                try:
                    unTranslationPermission = theTranslationedElement.fAllowTranslation()
                except:
                    None
                unAllTranslationsReport[ 'allow_translation'] = unTranslationPermission  
                
                if not unTranslationPermission:
                    return unAllTranslationsReport

                
                
                # ##############################################################
                """Check for necessary parameters.
                
                """
                if not theModelDDvlPloneTool_Retrieval:
                    return unAllTranslationsReport
                    
                
                unVoid = self.fRetrieveAllTranslations( 
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theModelDDvlPloneTool_Retrieval=theModelDDvlPloneTool_Retrieval,
                    theTranslationedElement            =theTranslationedElement, 
                    theAllTranslationsReport           =unAllTranslationsReport,
                    theAdditionalParams            =theAdditionalParams,
                )
                
                if not unAllTranslationsReport or not unAllTranslationsReport.get( 'success', False):
                    return unAllTranslationsReport
                
                
                unCheckedPermissionsCache = theModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                
                                    
                # ##############################################################
                """Retrieve the parent of current translation and check if it may be a candidate to contain the new translation.
                
                """
                unParentElement = aq_parent( aq_inner( theTranslationedElement))
                if not ( unParentElement == None):
                    unParentCandidateContainerReport = self.fRetrieveCandidateTranslationContainerReport( theModelDDvlPloneTool_Retrieval, theTranslationedElement, unParentElement, theTranslationedElement.getId(), theTranslationedElement.Title(), unCheckedPermissionsCache,)
                    if unParentCandidateContainerReport.get( 'allowed', False):
                        unAllTranslationsReport[ 'parent_container_report'] = unParentCandidateContainerReport
                            
                                 
                
                        
                        
                # ##############################################################
                """Retrieve first element from CLIPBOARD and check if it may be a candidate to contain the new translation.
                
                """
                
                unosElementosFromClipboard = theModelDDvlPloneTool_Retrieval.fClipboardCookieElements( theTranslationedElement.REQUEST, theTranslationedElement)
                if unosElementosFromClipboard:
                    
                    for unElementoFromClipboard in unosElementosFromClipboard:
                        if not ( unElementoFromClipboard == None):
                            
                            if unAllTranslationsReport[ 'parent_container_report'] and ( unElementoFromClipboard == unAllTranslationsReport[ 'parent_container_report'].get( 'element', None)):
                                unAllTranslationsReport[ 'clipboard_container_report'] = unAllTranslationsReport[ 'parent_container_report']
                                break
                            
                            else:
                                unClipboardCandidateContainerReport = self.fRetrieveCandidateTranslationContainerReport( theModelDDvlPloneTool_Retrieval, theTranslationedElement, unElementoFromClipboard, theTranslationedElement.getId(), theTranslationedElement.Title(), unCheckedPermissionsCache,)
                                if unClipboardCandidateContainerReport.get( 'allowed', False):
                                    unAllTranslationsReport[ 'clipboard_container_report'] = unClipboardCandidateContainerReport
                                    break
                                    
                # ##############################################################
                """Retrieve Plone Site and check if it may be a candidate to contain the new translation.
                
                """
                       
                unSite = theModelDDvlPloneTool_Retrieval.fPortalRoot( theTranslationedElement)
                if not ( unSite == None):
                    if unAllTranslationsReport[ 'parent_container_report'] and ( unSite == unAllTranslationsReport[ 'parent_container_report'].get( 'element', None)):
                        unAllTranslationsReport[ 'site_container_report'] = unAllTranslationsReport[ 'parent_container_report']
                    elif unAllTranslationsReport[ 'clipboard_container_report'] and ( unSite == unAllTranslationsReport[ 'clipboard_container_report'].get( 'element', None)):
                        unAllTranslationsReport[ 'site_container_report'] = unAllTranslationsReport[ 'clipboard_container_report']
                    else:
                        unSiteCandidateContainerReport = self.fRetrieveCandidateTranslationContainerReport( theModelDDvlPloneTool_Retrieval, theTranslationedElement, unSite, theTranslationedElement.getId(), theTranslationedElement.Title(), unCheckedPermissionsCache)
                        if unSiteCandidateContainerReport.get( 'allowed', False):
                            unAllTranslationsReport[ 'site_container_report'] = unSiteCandidateContainerReport
                        
                    
                unAllTranslationsReport[ 'success'] = True
                
                return unAllTranslationsReport
                          
                
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fRetrieveAllTranslationsWithContainerPloneSiteAndClipboard\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unAllTranslationsReport:
                    unAllTranslationsReport = { }

                unAllTranslationsReport.update( { 
                    'success':      False,
                    'status':       'Exception',
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unAllTranslationsReport
                        
            return  unAllTranslationsReport     
        
         
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveAllTranslationsWithContainerPloneSiteAndClipboard', theTimeProfilingResults)
            
    
               
    
        
                
    
    
                
    
    security.declarePrivate( 'fRetrieveAllTranslations')
    def fRetrieveAllTranslations( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool_Retrieval=None,
        theTranslationedElement             =None, 
        theAllTranslationsReport           =None,
        theAdditionalParams            =None):
        """Create a new translation of the original object which shall be a root, with the new translation name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveAllTranslations', theTimeProfilingResults)
                      
        try:
            # ##############################################################
            """Prepare result structure.
            
            """
            unAllTranslationsReport = theAllTranslationsReport
            if not unAllTranslationsReport:
                unAllTranslationsReport = self.fNewVoidAllTranslationsReport()
                
            unAllTranslationsReport.update( { 'success': False, })
            
            try:
                
                # ##############################################################
                """Check for element to create a new translation from.
                
                """
                if ( theTranslationedElement == None):
                    return unAllTranslationsReport
                unAllTranslationsReport[ 'translationed_element'] = theTranslationedElement
                
                
                
                
                # ##############################################################
                """Assert whether the element can be translationed.
                
                """
                unTranslationPermission = False
                try:
                    unTranslationPermission = theTranslationedElement.fAllowTranslation()
                except:
                    None
                unAllTranslationsReport[ 'allow_translation'] = unTranslationPermission  

                
                
                # ##############################################################
                """Check for necessary parameters.
                
                """
                if not theModelDDvlPloneTool_Retrieval:
                    return unAllTranslationsReport
                    
                
               # ##############################################################
                """Retrieve traversal results for translationed element 
                
                """
                unTranslationsCaches      = theModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()
                unCheckedPermissionsCache = theModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                someAllTypeConfigs        = { }
                
                someDefaultColumnNames        = [ 'title', 'description', ]
                
                unOriginalResult = theModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                    theTimeProfilingResults     = theTimeProfilingResults,
                    theElement                  = theTranslationedElement, 
                    theParent                   = None,
                    theParentTraversalName      = '',
                    theTypeConfig               = None, 
                    theAllTypeConfigs           = someAllTypeConfigs, 
                    theViewName                 = '', 
                    theRetrievalExtents         = [ 'owner', 'traversals', ],
                    theWritePermissions         =None,
                    theFeatureFilters           ={'attrs': someDefaultColumnNames, 'aggregations':[], 'relations':[],},
                    theInstanceFilters          =None,
                    theTranslationsCaches       =unTranslationsCaches,
                    theCheckedPermissionsCache  =unCheckedPermissionsCache,
                    theAdditionalParams         =theAdditionalParams
                )
                if not unOriginalResult or not( unOriginalResult.get( 'object', None) == theTranslationedElement):
                    return unAllTranslationsReport
                 
                unAllTranslationsReport[ 'translationed_element_result'] = unOriginalResult      
                
                
          
                    
                    
                    
                # ##############################################################
                """Retrieve translations for attributes in columns in translation tables (current, previous, next).
                
                """
                unAllTranslationsReport[ 'column_names'].extend( someDefaultColumnNames)
                unAllTranslationsReport[ 'column_names'].extend( [ 'translation', 'translation_comment', 'id', 'path',])
                someDefaultColumnTranslations = theModelDDvlPloneTool_Retrieval.getTranslationsForDefaultAttributes( theTranslationedElement)
                theModelDDvlPloneTool_Retrieval.pUpdateTranslationsForObjectAttribute( theModelDDvlPloneTool_Retrieval, someDefaultColumnTranslations, theTranslationedElement, 'translation')
                theModelDDvlPloneTool_Retrieval.pUpdateTranslationsForObjectAttribute( theModelDDvlPloneTool_Retrieval, someDefaultColumnTranslations, theTranslationedElement, 'translation_comment')
                # ACV 20091002 Now is retrieved with the translations for Default attributes. Removed.
                #
                #theModelDDvlPloneTool_Retrieval.pUpdateTranslationsForObjectAttribute( theModelDDvlPloneTool_Retrieval, someDefaultColumnTranslations, theTranslationedElement, 'path')
                unAllTranslationsReport[ 'column_translations'] = someDefaultColumnTranslations
                    
                
                # ##############################################################
                """Retrieve current translation info, and translation infos for all previous and next translations, as a tree.
                
                """
                someAllTranslationsByName = unAllTranslationsReport[ 'all_translations_by_name'] 

                unInterTranslationUIDFieldsCache      = { }
                unNewLanguageFieldsCache          = { }
                unFallbackStrategyFieldsCache       = { }
                unPreviousTranslationsLinkFieldsCache = { }
                unNextTranslationsLinkFieldsCache     = { }
                
                unOriginalTranslatingInfo = self.fRetrieveTranslatingInfo( 
                    theTimeProfilingResults          = theTimeProfilingResults,
                    theModelDDvlPloneTool_Retrieval  = theModelDDvlPloneTool_Retrieval,
                    theRetrievePreviousTranslations      = True,
                    theRetrieveNextTranslations          = True,
                    theRecurse                       = True,
                    theTranslationedElement              = theTranslationedElement, 
                    theInterTranslationUIDFieldsCache    = unInterTranslationUIDFieldsCache,
                    theNewLanguageFieldsCache        = unNewLanguageFieldsCache,
                    theAllTranslationsByName             = someAllTranslationsByName,
                    theFallbackStrategyFieldsCache     = unFallbackStrategyFieldsCache,
                    thePreviousTranslationsLinkFieldsCache=unPreviousTranslationsLinkFieldsCache,
                    theNextTranslationsLinkFieldsCache   = unNextTranslationsLinkFieldsCache,
                    theAdditionalParams              = theAdditionalParams,
                )
                unAllTranslationsReport[ 'original_translation_info'] = unOriginalTranslatingInfo
       
                unAllTranslationsReport[ 'success'] = True
                
                return unAllTranslationsReport
                          
                
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fRetrieveAllTranslations\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unAllTranslationsReport:
                    unAllTranslationsReport = { }

                unAllTranslationsReport.update( { 
                    'success':      False,
                    'status':       'Exception',
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unAllTranslationsReport
                        
            return  unAllTranslationsReport     
        
         
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveAllTranslations', theTimeProfilingResults)
            
    
               
    
                        
                
                
                
                

    security.declarePrivate( 'fRetrieveCandidateTranslationContainerReport')
    def fRetrieveCandidateTranslationContainerReport( self, 
        theModelDDvlPloneTool_Retrieval,
        theTranslationedElement,
        theCandidateContainer,
        theOriginalId,
        theOriginalTitle,
        theCheckedPermissionsCache,):
                 
                                    
        # ##############################################################
        """Retrieve the parent of current translation and check if it may be a candidate to contain the new translation.
        
        """
        unCandidateContainerReport = self.fNewVoidCandidateContainerReport()
        
        if ( theCandidateContainer == None):
            return unCandidateContainerReport
        

        unMetaType = theCandidateContainer.meta_type
            
        if not unMetaType in cAcceptedTranslationContainerMetaTypes:
            return unCandidateContainerReport
                    
        if not theModelDDvlPloneTool_Retrieval.fCheckElementPermission( theCandidateContainer, cPermissionsOnTranslationContainers, theCheckedPermissionsCache ):
            return unCandidateContainerReport
        
                    
        unaUID = ''
        if unMetaType in cPloneSiteMetaTypes:
            unaUID = cFakeUIDForPloneSite
        else:
            unaUID = theCandidateContainer.UID()
            
        unCandidateContainerReport.update( {
            'allowed':                   True,
            'element':                   theCandidateContainer,
            'title':                     theModelDDvlPloneTool_Retrieval.fAsUnicode( theCandidateContainer.Title(),       theTranslationedElement),
            'description':               theModelDDvlPloneTool_Retrieval.fAsUnicode( theCandidateContainer.Description(), theTranslationedElement),
            'id':                        theModelDDvlPloneTool_Retrieval.fAsUnicode( theCandidateContainer.getId(),       theTranslationedElement),
            'path':                      theModelDDvlPloneTool_Retrieval.fAsUnicode( '/'.join( theCandidateContainer.getPhysicalPath()),       theTranslationedElement),
            'UID':                       theModelDDvlPloneTool_Retrieval.fAsUnicode( unaUID,                        theTranslationedElement),
            'children_titles':           [],
            'children_ids':              [],
        })
        
        

        # ##############################################################
        """Retrieve the titles and ids of child elements of the container for the new translation. These will be siblings of the new translation, and the new translation can not have same title or id than one of these pre-existing children of the new translation container.
        
        """
        
        unosContainerChildren = theCandidateContainer.objectValues()
        
        unosContainerChildrenTitles       = [ ]
        unosContainerChildrenIds          = [ ]
        
        for unChild in unosContainerChildren:
            unTitle = ''
            try:
                unTitle = unChild.Title()
            except:
                None
            unTitle = theModelDDvlPloneTool_Retrieval.fAsUnicode( unTitle, theTranslationedElement)
            if unTitle:
                if not ( unTitle in unosContainerChildrenTitles):
                    unosContainerChildrenTitles.append( unTitle)
                
            unId = ''
            try:
                unId = unChild.getId()
            except:
                None
            unId = theModelDDvlPloneTool_Retrieval.fAsUnicode( unId, theTranslationedElement)                
            if unId:
                if not ( unId in unosContainerChildrenIds):
                    unosContainerChildrenIds.append( unId)
                
        unCandidateContainerReport[ 'children_titles'] = sorted( unosContainerChildrenTitles)
        unCandidateContainerReport[ 'children_ids']    = sorted( unosContainerChildrenIds)
       
        
        
        # ##############################################################
        """Calculate a Title and an Id for the new translation, derived from the title and translation of the element to create the new translation from, but not duplicating any title or id in the container of the new translation.
        
        """
        unOriginalTitle = theTranslationedElement.Title()
        unOriginalId    = theTranslationedElement.getId()
       
        aPloneToolForNormalizeString = getToolByName( theTranslationedElement, 'plone_utils', None)
        if aPloneToolForNormalizeString  and  not shasattr( aPloneToolForNormalizeString, 'normalizeString'):
            aPloneToolForNormalizeString = None
        
        unNewTranslationId    = theModelDDvlPloneTool_Retrieval.fUniqueStringWithCounter( unOriginalId,    unosContainerChildrenIds, aPloneToolForNormalizeString)
        if not unNewTranslationId:
            unNewTranslationId = unOriginalId + '-translation'
        unNewTranslationId = theModelDDvlPloneTool_Retrieval.fAsUnicode( unNewTranslationId, theTranslationedElement)
        
        unCandidateContainerReport[ 'new_id'] = unNewTranslationId
        
        
        unNewTranslationTitle = theModelDDvlPloneTool_Retrieval.fUniqueStringWithCounter( unOriginalTitle, unosContainerChildrenTitles)
        if not unNewTranslationTitle:
            unNewTranslationTitle = unOriginalTitle + '-Translation'
        unNewTranslationTitle = theModelDDvlPloneTool_Retrieval.fAsUnicode( unNewTranslationTitle, theTranslationedElement)

        unCandidateContainerReport[ 'new_title'] = unNewTranslationTitle
                            
        return unCandidateContainerReport
                    

                                
                        
        

    security.declarePrivate( 'fNewTranslation')
    def fNewTranslation( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool          =None,
        theModelDDvlPloneTool_Retrieval=None,
        theModelDDvlPloneTool_Mutators =None,
        theOriginalObject              =None, 
        theNewTranslationContainerKind     =None,
        theNewNewLanguage              =None,
        theNewFallbackStrategy           =None,
        theNewTitle                    =None,
        theNewId                       =None,
        theMDDNewTranslationTypeConfigs    =None, 
        thePloneNewTranslationTypeConfigs  =None, 
        theAdditionalParams            =None):
        """Create a new translation of the original object which shall be a root, with the new translation name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fNewTranslation', theTimeProfilingResults)
                      
        try:
            unNewTranslationReport = None
            try:
                
                # ##############################################################################
                """Transaction Save point before import to get a clean view on the existing object network.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                
                unNewTitle          = theNewTitle.strip()
                unNewId             = theNewId.strip()
                unNewNewLanguage    = theNewNewLanguage.strip()
                unNewFallbackStrategy = theNewFallbackStrategy.strip()
                
                unNewTranslationContext   = self.fNewVoidNewTranslationContext()
                unNewTranslationReport    = unNewTranslationContext.get( 'report', {})
                unosNewTranslationErrors  = unNewTranslationContext.get( 'newtranslation_errors', {})
                
                # ##############################################################################
                """Check parameter with original translation to copy from.
                
                """      
                if ( theOriginalObject == None):
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_MissingParameter_OriginalObject,
                    })
                    return unNewTranslationReport
                unNewTranslationContext[ 'original_object'] = theOriginalObject

                
                
                # ##############################################################################
                """Check critical parameters.
                
                """      
                if not theModelDDvlPloneTool_Retrieval:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval,
                    })
                    return unNewTranslationReport
                unNewTranslationContext[ 'ModelDDvlPloneTool_Retrieval'] = theModelDDvlPloneTool_Retrieval
                
                if not theModelDDvlPloneTool_Mutators:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators,
                    })
                    return unNewTranslationReport
                unNewTranslationContext[ 'ModelDDvlPloneTool_Mutators'] = theModelDDvlPloneTool_Mutators

                
                
                
                # ##############################################################################
                """Incorporate additional params into context.
                
                """ 
                if theAdditionalParams:
                    unNewTranslationContext[ 'additional_params'].update( theAdditionalParams)
                
                                    
                    
                
                # ##############################################################################
                """Check permissions on original translation element.
                
                """ 
                
                unCheckedPermissionsCache = theModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                unNewTranslationContext[ 'checked_permissions_cache'] = unCheckedPermissionsCache
                
                if not theModelDDvlPloneTool_Retrieval.fCheckElementPermission( theOriginalObject, permissions.View , unCheckedPermissionsCache):
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Original_NotReadable,
                    })
                    return unNewTranslationReport
                
                
                # ##############################################################################
                """Chek translationing allowed in the original object.
                
                """      
                unAllowNewTranslation = False
                try:
                    unAllowNewTranslation = theOriginalObject.fAllowTranslation()
                except:
                    None
                    
                if not unAllowNewTranslation:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_NewTranslation_NotAllowedInElement,
                    })
                    return unNewTranslationReport
                           
                
                # ##############################################################################
                """Chek translation name parameter.
                
                """      
                if not unNewNewLanguage:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_MissingParameter_NewLanguage,
                    })
                    return unNewTranslationReport
                unNewTranslationContext[ 'translation_name'] = theOriginalObject
                
                                
                
                # ##############################################################################
                """Check auxiliary parameters.
                
                """      
                if not theMDDNewTranslationTypeConfigs:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_MissingParameter_MDDNewTranslationTypeConfigs,
                    })
                    return unNewTranslationReport
                unNewTranslationContext[ 'mdd_type_configs'] = theMDDNewTranslationTypeConfigs
                        
                
                
                
                # ##############################################################################
                """Retrieve translation_service tool to handle the input encoding.
                
                """
                aTranslationService = getToolByName( theOriginalObject, 'translation_service', None)      
                if not aTranslationService:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Internal_MissingTool_translation_service,
                    })
                    return unNewTranslationReport
                unNewTranslationContext[ 'translation_service'] = aTranslationService
                
                
                
                # ##############################################################################
                """Retrieve all the translationing information, from the original element and all its previous and next translations.
                
                """      
                unAllTranslationsReport = self.fRetrieveAllTranslationsWithContainerPloneSiteAndClipboard(
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theModelDDvlPloneTool_Retrieval=theModelDDvlPloneTool_Retrieval,
                    theTranslationedElement            =theOriginalObject, 
                    theAdditionalParams            =theAdditionalParams,
                )
                if ( not unAllTranslationsReport) or not unAllTranslationsReport.get( 'success', False):
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Failure_Retrieving_AllTranslations,
                    })
                    return unNewTranslationReport
                
                
                
                # ##############################################################################
                """Obtain the element to become the parent of the new translation: where the new duplicate shall be created. One of the Parent of the current translation, or one of the elements in the clipboard, or the root of the Plone site.
                
                """      
                if not ( theNewTranslationContainerKind in [ 'Parent', 'Clipboard', 'Site', ]):
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_MissingParameter_ContainerKind,
                    })
                    return unNewTranslationReport
                
                
                
                unContainerReport = None
                if theNewTranslationContainerKind   == 'Parent':
                    unContainerReport = unAllTranslationsReport.get( 'parent_container_report', {})
                elif theNewTranslationContainerKind == 'Clipboard':
                    unContainerReport = unAllTranslationsReport.get( 'clipboard_container_report', {})
                elif theNewTranslationContainerKind   == 'Site':
                    unContainerReport = unAllTranslationsReport.get( 'site_container_report', {})
                    
                if not unContainerReport:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_ContainerReport_Missing,
                    })
                    return unNewTranslationReport
                
                if not unContainerReport.get( 'allowed', False):
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_ContainerReport_NotAllowed,
                    })
                    return unNewTranslationReport
                
                unContainer = unContainerReport.get( 'element', None)
                if unContainer == None:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Container_NotFound,
                    })
                    return unNewTranslationReport
                
                unNewTranslationContext[ 'container_object'] = unContainer

                
                
                # ##############################################################################
                """Check permissions on new translation container.
                
                """      
                if not theModelDDvlPloneTool_Retrieval.fCheckElementPermission( unContainer, cPermissionsOnTranslationContainers, unCheckedPermissionsCache):
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Container_NotWritable,
                    })
                    return unNewTranslationReport
                
                
                
                # ##############################################################################
                """Check uniqueness of title and id for new translation.
                
                """      
                unosTitlesToAvoid = unContainerReport.get( 'children_titles', [])
                if unNewTitle in unosTitlesToAvoid:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Title_AlreadyExists,
                    })
                    return unNewTranslationReport
                    
                unasIdsToAvoid = unContainerReport.get( 'children_ids', [])
                if theNewId in unasIdsToAvoid:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Id_AlreadyExists,
                    })
                    return unNewTranslationReport
                    
                
                
                    
                 
                # ##############################################################################
                """Check uniqueness of name for the new translation.
                
                """      
                unasExistingNewLanguages = unContainerReport.get( 'all_translations_by_name', {}).keys()
                if unNewNewLanguage in unasExistingNewLanguages:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_NewLanguage_AlreadyExists,
                    })
                    return unNewTranslationReport
                                

                
                
                
                
                   
                # ##############################################################################
                """Retrieve original object result not needed because the refactor shall use directly the values in the original elements.
                
                """      
                
     

                # ##############################################################################
                """Create new translation root by duplicating the original object as target of the copy, to be populated later with attributes, aggregates and relations.
                
                """      
                if aTranslationService:
                    unNewTitle          = aTranslationService.encode( unNewTitle)
                    unNewId             = aTranslationService.encode( unNewId)
                    unNewNewLanguage    = aTranslationService.encode( unNewNewLanguage)
                    unNewFallbackStrategy = aTranslationService.encode( unNewFallbackStrategy)
                
                unTypeToCreate = theOriginalObject.meta_type
                anAttrsDict = {
                    'title':          unNewTitle,
                    'translationInterna':    unNewNewLanguage,
                    'comentarioTranslationInterna': unNewFallbackStrategy,
                }
                
                unCreatedId = None
                try:
                    unCreatedTranslationId = unContainer.invokeFactory( unTypeToCreate, unNewId, **anAttrsDict)
                except:
                    return None
                if not unCreatedTranslationId:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_ObjectNotCreated,
                    })
                    return unNewTranslationReport
        
   
                unosElementsAfterCreation = unContainer.objectValues()
                unNewTranslationElement = None
                for unElement in unosElementsAfterCreation:
                    unId = unElement.getId()
                    if unId == unCreatedTranslationId:
                        unNewTranslationElement = unElement
                        break
                if ( unNewTranslationElement == None):
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_CreatedObjectNotFound,
                    })
                    return unNewTranslationReport
                
                unNewTranslationElement.manage_fixupOwnershipAfterAdd()
                
                theModelDDvlPloneTool_Mutators.pSetElementPermissions( unNewTranslationElement)
                 
                theModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNewTranslationElement)
                
                unNewTranslationReport[ 'new_translation_element'] = unNewTranslationElement
                
                
                # ##############################################################################
                """Transaction Save point.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                
                # ##############################################################################
                """Retrieve results for new translation element just created. Required by the copy machinery.
                
                """      
                somePloneNewTranslationTypeConfigs = thePloneNewTranslationTypeConfigs
                if not somePloneNewTranslationTypeConfigs:
                    somePloneNewTranslationTypeConfigs = {}
                unNewTranslationContext[ 'plone_type_configs'] = somePloneNewTranslationTypeConfigs
                
                
                allNewTranslationTypeConfigs = somePloneNewTranslationTypeConfigs.copy()
                allNewTranslationTypeConfigs.update( theMDDNewTranslationTypeConfigs)
                unNewTranslationContext[ 'all_copy_type_configs'] = allNewTranslationTypeConfigs
                
                
                unNewTranslationElementResult = self.fRetrieveJustCreatedTranslationResult( 
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theNewTranslationContext           =unNewTranslationContext,
                    theNewTranslationElement            =unNewTranslationElement, 
                    theAdditionalParams            =theAdditionalParams,
                )
                if ( not unNewTranslationElementResult) or unNewTranslationElementResult.get( 'object', None) == None:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_CreatedObjectResultFaulure,
                    })
                    return unNewTranslationReport
                
                unNewTranslationReport[ 'new_translation_element_result'] = unNewTranslationElementResult
                
                
                
                 
                
                # ##############################################################################
                """Traverse source elements network and create copy linked with new translation traceability links.
                
                """      
        


                unRefactor = MDDRefactor_NewTranslation( 
                    theModelDDvlPloneTool,
                    theModelDDvlPloneTool_Retrieval,
                    theModelDDvlPloneTool_Mutators,
                    theOriginalObject, 
                    unNewTranslationElement, 
                    unNewTranslationElementResult,
                    unNewNewLanguage,
                    unNewFallbackStrategy,
                    theMDDNewTranslationTypeConfigs,
                    somePloneNewTranslationTypeConfigs,
                    allNewTranslationTypeConfigs, 
                    MDDRefactor_Translation_Exception
                )  
                if ( not unRefactor) or not unRefactor.vInitialized:
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Internal_Refactor_NotInitialized,
                    })
                    return unNewTranslationReport
                    
                
                unHuboRefactorException  = False
                unHuboException  = False
                unRefactorResult = False
                try:
                    
                    try:
                        unRefactorResult = unRefactor.fRefactor()
                        
                        unNewTranslationElement.setTitle( unNewTitle)
                        unNewTranslationElement.reindexObject()
                        
                        unNewTranslationElementSchema = None
                        try:
                            unNewTranslationElementSchema = unNewTranslationElement.schema
                        except:
                            None
                        if unNewTranslationElementSchema:
                            
                            unTranslationFieldName = None
                            try:
                                unTranslationFieldName = unNewTranslationElement.translation_field
                            except:
                                None
                            if unTranslationFieldName:
                                if unNewTranslationElementSchema.has_key( unTranslationFieldName):
                                    unTranslationField = unNewTranslationElementSchema[ unTranslationFieldName]
                                    if unTranslationField:
                                        unTranslationMutator = unTranslationField.getMutator( unNewTranslationElement)
                                        unTranslationMutator( unNewNewLanguage)
                                        
                            unFallbackStrategyFieldName = None
                            try:
                                unFallbackStrategyFieldName = unNewTranslationElement.translation_comment_field
                            except:
                                None
                            if unFallbackStrategyFieldName:
                                if unNewTranslationElementSchema.has_key( unFallbackStrategyFieldName):
                                    unFallbackStrategyField = unNewTranslationElementSchema[ unFallbackStrategyFieldName]
                                    if unFallbackStrategyField:
                                        unFallbackStrategyMutator = unFallbackStrategyField.getMutator( unNewTranslationElement)
                                        unFallbackStrategyMutator( unNewFallbackStrategy)
                        
                    
                                        
                    except MDDRefactor_Translation_Exception:
                        
                        unHuboRefactorException = True
                        
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                        
                        unInformeExcepcion = 'Exception during ModelDDvlPloneTool_Refactor::fNewTranslation invoking MDDRefactor_NewTranslation::fRefactor\n' 
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        unNewTranslationReport[ 'exception'] = unInformeExcepcion
                                 
                        if cLogExceptions:
                            logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                        
                except:
                    unHuboException = True
                    raise
                    
                
                unNewTranslationReport.update( {
                    'num_elements_pasted':         unRefactor.vNumElementsPasted,
                    'num_mdd_elements_pasted':     unRefactor.vNumMDDElementsPasted,
                    'num_plone_elements_pasted':   unRefactor.vNumPloneElementsPasted,
                    'num_attributes_pasted':       unRefactor.vNumAttributesPasted,
                    'num_links_pasted':            unRefactor.vNumLinksPasted,
                    'num_elements_failed':         unRefactor.vNumElementsFailed,
                    'num_mdd_elements_failed':     unRefactor.vNumMDDElementsFailed,
                    'num_plone_elements_failed':   unRefactor.vNumPloneElementsFailed,
                    'num_attributes_failed':       unRefactor.vNumAttributesFailed,
                    'num_links_failed':            unRefactor.vNumLinksFailed,
                    'num_elements_bypassed':       unRefactor.vNumElementsBypassed,
                    'num_mdd_elements_bypassed':   unRefactor.vNumMDDElementsBypassed,
                    'num_plone_elements_bypassed': unRefactor.vNumPloneElementsBypassed,
                    'num_attributes_bypassed':     unRefactor.vNumAttributesBypassed,
                    'num_links_bypassed':          unRefactor.vNumLinksBypassed,
                })
                unNewTranslationReport[ 'error_reports'].extend( unRefactor.vErrorReports )
                            
                if ( not unHuboException) and ( not unHuboRefactorException) and unRefactorResult:
                    ModelDDvlPloneTool_Transactions().fTransaction_Commit()
    
                    unNewTranslationReport.update( { 
                         'success':      True,
                    })
                    
                    if cLogTranslationResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'COMMIT: %s::fNewTranslation\n%s' % ( self.__class__.__name__, theModelDDvlPloneTool.fPrettyPrint( [ unNewTranslationReport, ])))
                    
                else:
                    ModelDDvlPloneTool_Transactions().fTransaction_Abort()
                    
                    unNewTranslationReport.update( { 
                        'success':      False,
                        'status':       cNewTranslationStatus_Error_Internal_Refactor_Failed,
                    })
                    
                    if cLogTranslationResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'ABORT: %s::fNewTranslation\n%s' % ( self.__class__.__name__, theModelDDvlPloneTool.fPrettyPrint( [ unNewTranslationReport, ])))
                    
                return unNewTranslationReport                
                
                
                
          
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fNewTranslation\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unNewTranslationReport:
                    unNewTranslationReport = { }
                    
                unNewTranslationReport.update( { 
                    'success':      False,
                    'status':       cNewTranslationStatus_Error_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unNewTranslationReport
                        
            return { 'success': False, }
         
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fNewTranslation', theTimeProfilingResults)
            
    
               

    
        

    security.declarePrivate( 'fRetrieveJustCreatedTranslationResult')
    def fRetrieveJustCreatedTranslationResult( self,
        theTimeProfilingResults        =None,
        theNewTranslationContext           =None,
        theNewTranslationElement           =None, 
        theAdditionalParams            =None):
        """
        
        """
        
        try:
            if not theNewTranslationContext:
                return None
           
            if not theNewTranslationElement:
                return None
           
            allCopyTypeConfigs = theNewTranslationContext.get( 'all_copy_type_configs', {})
            if not allCopyTypeConfigs:
                return None
                            
            someAdditionalParams = theNewTranslationContext.get(  'additional_params', None)
            
            aModelDDvlPloneTool_Retrieval = theNewTranslationContext.get( 'ModelDDvlPloneTool_Retrieval', None)
            
            unCheckedPermissionsCache = theNewTranslationContext.get( 'checked_permissions_cache', None)
            
            unElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     = theTimeProfilingResults,
                theElement                  = theNewTranslationElement, 
                theParent                   = None,
                theParentTraversalName      = '',
                theTypeConfig               = None, 
                theAllTypeConfigs           = allCopyTypeConfigs, 
                theViewName                 = '', 
                theRetrievalExtents         = [ 'traversals', ],
                theWritePermissions         =[ 'object', 'add', 'add_collection', 'aggregations', ],
                theFeatureFilters           =None, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =someAdditionalParams
            )
            if not unElementResult or not( unElementResult.get( 'object', None) == theNewTranslationElement):
                return None
                        
        
            return unElementResult
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during fImport fRetrieveContainer\n' 
            unInformeExcepcion += 'source object %s\n' % str( theNewTranslationElement) 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            return None
                    
        return None    
    

     