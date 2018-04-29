# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Version.py
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

from Products.CMFCore.utils      import getToolByName

from Products.Archetypes.utils   import shasattr



from ModelDDvlPloneTool_ImportExport_Constants import *

from ModelDDvlPloneTool_Transactions           import ModelDDvlPloneTool_Transactions
from ModelDDvlPloneTool_Retrieval              import ModelDDvlPloneTool_Retrieval
from ModelDDvlPloneTool_Profiling              import ModelDDvlPloneTool_Profiling
from MDD_RefactorComponents                    import MDDRefactor_NewVersion

from ModelDDvlPloneToolSupport               import fPrettyPrint



cLogExceptions = True

cLogVersionResults = True




cVersionName_UnVersioned = '-Not versioned-'
cVersionName_MissingVersionName = '-Version Name Missing-'


cAcceptedVersionContainerMetaTypes = cPloneSiteMetaTypes + [ 'ATFolder', 'ATBTreeFolder',]
               
cPermissionsOnVersionContainers = [ 
    permissions.View,
    perm_AccessContentsInformation,
    permissions.ListFolderContents,
    permissions.AddPortalContent,  
    permissions.AddPortalFolders,
    permissions.ModifyPortalContent,
]




class MDDRefactor_Version_Exception( Exception): pass




class ModelDDvlPloneTool_Version( ModelDDvlPloneTool_Profiling):
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
    
        
    
    security.declarePrivate( 'fNewVoidNewVersionContext')    
    def fNewVoidNewVersionContext( self,):
        unContext = {
            'original_object':               None,
            'original_object_result':        None,
            'container_object':              None,
            'version_name':                  None,
            'ModelDDvlPloneTool_Retrieval':  None,
            'ModelDDvlPloneTool_Mutators':   None,
            'checked_permissions_cache':     None,
            'mdd_type_configs':              {},
            'plone_type_configs':            {},
            'all_copy_type_configs':         {},
            'additional_params':             self.fTraversalSourcesAdditionalParams(),
            'report':                        self.fNewVoidNewVersionReport(),
            'translation_service':           None,
        }
        return unContext
    
      
    
    
    
    
    security.declarePrivate( 'fNewVoidVersioningInfo')    
    def fNewVoidVersioningInfo( self,):
        aReport = {
            'success':                             False,
            'element':                             None,
            'title':                               '',
            'id':                                  '',
            'url':                                 '',
            'UID':                                 '',
            'description':                         '',
            'path':                                '',
            'inter_version_uid':                   '',
            'version':                             '',
            'version_comment':                     '',
            'previous_versioning_infos':           [ ],
            'previous_initialized':                False,
            'next_versioning_infos':               [ ],
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
    
    

    security.declarePrivate( 'fNewVoidAllVersionsReport')    
    def fNewVoidAllVersionsReport( self,):
        aReport = {
            'success':                             False,
            'versioned_element':                   None,
            'versioned_element_result':            None,
            'original_version_info':               None,
            'all_versions_by_name':                {},
            'allow_version':                       False,
            'column_names':                        [],
            'column_translations':                 {},
            'parent_container_report':             None,
            'clipboard_container_report':          None,
            'site_container_report':              None,
        }
        return aReport
    
    
 
    security.declarePrivate( 'fNewVoidNewVersionReport')    
    def fNewVoidNewVersionReport( self,):
        unInforme = {
            'success':                  False,
            'status':                   '',
            'condition':                None,
            'exception':                '',
            'new_version_element':      None,
            'new_version_element_result': None,            
            'num_elements_versioned':      0,
            'num_mdd_elements_versioned':  0,
            'num_plone_elements_versioned': 0,
            'error_reports':            [ ],
        }
        return unInforme
    
    
    
    
    
    
    
    
    
    

    security.declarePrivate( 'fRetrieveVersioningInfo')
    def fRetrieveVersioningInfo( self,
        theTimeProfilingResults             =None,
        theModelDDvlPloneTool_Retrieval     =None,
        theRetrievePreviousVersions         =False,
        theRetrieveNextVersions             =False,
        theRecurse                          =False,
        theVersionedElement                 =None, 
        theAllVersionsByName                =None,
        theInterVersionUIDFieldsCache       =None,
        theVersionNameFieldsCache           =None,
        theVersionCommentFieldsCache        =None,
        thePreviousVersionsLinkFieldsCache  =None,
        theNextVersionsLinkFieldsCache      =None,
        theAdditionalParams                 =None):
        """Retrieve the version number and the immediate previous and next versions, recursing if so requested."
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveVersioningInfo', theTimeProfilingResults)
                      
        try:
            unVersioningInfo = { 'success': False, }
            try:
                
                unVersioningInfo = self.fNewVoidVersioningInfo()
                if ( theVersionedElement== None):
                    return unVersioningInfo
                
                unVersioningInfo[ 'element'] = theVersionedElement
                
                unAlreadyVisited = { }
                
                self.pRetrieveVersionInfo_Inner(
                    theTimeProfilingResults             =theTimeProfilingResults,
                    theModelDDvlPloneTool_Retrieval     =theModelDDvlPloneTool_Retrieval,
                    theRetrievePreviousVersions         =theRetrievePreviousVersions,
                    theRetrieveNextVersions             =theRetrieveNextVersions,
                    theRecurse                          =theRecurse,
                    theAlreadyVisited                   =unAlreadyVisited,
                    theVersioningInfo                   =unVersioningInfo, 
                    theAllVersionsByName                =theAllVersionsByName,
                    theInterVersionUIDFieldsCache       =theInterVersionUIDFieldsCache,
                    theVersionNameFieldsCache           =theVersionNameFieldsCache,
                    theVersionCommentFieldsCache        =theVersionCommentFieldsCache,
                    thePreviousVersionsLinkFieldsCache  =thePreviousVersionsLinkFieldsCache,
                    theNextVersionsLinkFieldsCache      =theNextVersionsLinkFieldsCache,
                    theAdditionalParams                 =theAdditionalParams,
                )
                
                return unVersioningInfo
                
                
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fRetrieveVersioningInfo\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unVersioningInfo:
                    unVersioningInfo = { }
                    
                unVersioningInfo.update( { 
                    'success':      False,
                    'status':       cMDDNewVersionStatus_Error_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unVersioningInfo
                        
            return unVersioningInfo        
        
         
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveVersioningInfo', theTimeProfilingResults)
                            
           
                                
                

    security.declarePrivate( 'pRetrieveVersionInfo_Inner')
    def pRetrieveVersionInfo_Inner( self,
        theTimeProfilingResults             =None,
        theModelDDvlPloneTool_Retrieval     =None,
        theRetrievePreviousVersions         =False,
        theRetrieveNextVersions             =False,
        theRecurse                          =False,
        theAlreadyVisited                   =None,
        theVersioningInfo                   =None, 
        theAllVersionsByName                =None,
        theInterVersionUIDFieldsCache       =None,
        theVersionNameFieldsCache           =None,
        theVersionCommentFieldsCache        =None,
        thePreviousVersionsLinkFieldsCache  =None,
        theNextVersionsLinkFieldsCache      =None,
        theAdditionalParams                 =None):
        """Initialize the version number and the immediate previous and next versions, recursing if so requested."
        
        """
        
        if not theVersioningInfo:
            return self

        unVersionedElement = theVersioningInfo.get( 'element', None)
        if ( unVersionedElement == None):
            return self
        
        
        
        unAlreadyVisited = theAlreadyVisited
        if unAlreadyVisited == None:
            unAlreadyVisited = { }
            
        
        unModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool_Retrieval
        if not unModelDDvlPloneTool_Retrieval:
            unModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        
        
        unInterVersionUIDFieldsCache = theInterVersionUIDFieldsCache
        if ( unInterVersionUIDFieldsCache == None):
            unInterVersionUIDFieldsCache = { }
        
        unVersionNameFieldsCache = theVersionNameFieldsCache
        if ( unVersionNameFieldsCache == None):
            unVersionNameFieldsCache = { }
        
        unVersionCommentFieldsCache = theVersionCommentFieldsCache
        if ( unVersionCommentFieldsCache == None):
            unVersionCommentFieldsCache = { }
        
        unPreviousVersionsLinkFieldsCache = thePreviousVersionsLinkFieldsCache
        if ( unPreviousVersionsLinkFieldsCache == None):
            unPreviousVersionsLinkFieldsCache = { }
        
        unNextVersionsLinkFieldsCache = theNextVersionsLinkFieldsCache
        if ( unNextVersionsLinkFieldsCache == None):
            unNextVersionsLinkFieldsCache = { }
        
            

            
        unVersionedElementMetaType = unVersionedElement.meta_type
            
        
        
        
        unId        = unVersionedElement.getId()
        theVersioningInfo[ 'id']       = unModelDDvlPloneTool_Retrieval.fAsUnicode( unId, unVersionedElement)
        
        unaURL = unVersionedElement.absolute_url()
        if not ( unaURL[-1:] == '/'):
            unaURL = '%s/' % unaURL                
        theVersioningInfo[ 'url'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unaURL, unVersionedElement)
         
        unaUID = unVersionedElement.UID()
        theVersioningInfo[ 'UID'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unaUID, unVersionedElement)
         
        unTitle        = unVersionedElement.Title()
        theVersioningInfo[ 'title']       = unModelDDvlPloneTool_Retrieval.fAsUnicode( unTitle, unVersionedElement)
        
        unaDescription = unVersionedElement.Description()
        theVersioningInfo[ 'description'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unaDescription, unVersionedElement)
        
        unPath        = '/'.join( unVersionedElement.getPhysicalPath())
        theVersioningInfo[ 'path']       = unModelDDvlPloneTool_Retrieval.fAsUnicode( unPath, unVersionedElement)
        
        unInterVersionUID    = None
        unVersionName        = None
        unVersionComment     = None
        unasPreviousVersions = None
        unasNextVersions     = None
        
        
        unSchema = None
        try:
            unSchema = unVersionedElement.schema
        except:
            None
        if not unSchema:
            return self


        unInterVersionField = unInterVersionUIDFieldsCache.get( unVersionedElementMetaType, None)
        if not unInterVersionField:
            
            unInterVersionFieldName = None
            try:
                unInterVersionFieldName = unVersionedElement.inter_version_field
            except:
                None
            if unInterVersionFieldName:
            
                unInterVersionField = unSchema.get( unInterVersionFieldName, None)
                if unInterVersionField:            
                    unInterVersionUIDFieldsCache[ unVersionedElementMetaType] = unInterVersionField
        
        
        if unInterVersionField:    
            unInterVersionAccessor = unInterVersionField.getAccessor( unVersionedElement)
            if not unInterVersionAccessor:
                return self
            unInterVersionUID = None
            try:
                unInterVersionUID = unInterVersionAccessor()
            except:
                None
            if not ( unInterVersionUID == None):
                theVersioningInfo[ 'inter_version_uid'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unInterVersionUID, unVersionedElement)
            
                    
        
        unVersionField = unVersionNameFieldsCache.get( unVersionedElementMetaType, None)
        if not unVersionField:
            
            unVersionFieldName = None
            try:
                unVersionFieldName = unVersionedElement.version_field
            except:
                None
            if not unVersionFieldName:
                return self
            
            unVersionField = unSchema.get( unVersionFieldName, None)
            if not unVersionField:
                return self
            
            unVersionNameFieldsCache[ unVersionedElementMetaType] = unVersionField
        
        
        unVersionName = None
        if unVersionField:    
            unVersionAccessor = unVersionField.getAccessor( unVersionedElement)
            if not unVersionAccessor:
                return self
            try:
                unVersionName = unVersionAccessor()
            except:
                None
            if not ( unVersionName == None):
                theVersioningInfo[ 'version'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unVersionName, unVersionedElement)
                if not ( theAllVersionsByName == None):
                    if theAllVersionsByName.has_key( unVersionName):
                        raise "Duplicate_Version_Name"
                    theAllVersionsByName[ unVersionName] = theVersioningInfo
                
  
        unVersionCommentField = unVersionCommentFieldsCache.get( unVersionedElementMetaType, None)
        if not unVersionCommentField:
            
            unVersionCommentFieldName = None
            try:
                unVersionCommentFieldName = unVersionedElement.version_comment_field
            except:
                None
            if unVersionCommentFieldName:
            
                unVersionCommentField = unSchema.get( unVersionCommentFieldName, None)
                if unVersionCommentField:
                    unVersionCommentFieldsCache[ unVersionedElementMetaType] = unVersionCommentField
        
        if unVersionCommentField:   
            unVersionCommentAccessor = unVersionCommentField.getAccessor( unVersionedElement)
            if not unVersionCommentAccessor:
                return self
            unVersionComment = None
            try:
                unVersionComment = unVersionCommentAccessor()
            except:
                None
            if not ( unVersionComment == None):
                theVersioningInfo[ 'version_comment'] = unModelDDvlPloneTool_Retrieval.fAsUnicode( unVersionComment, unVersionedElement)
        
        
            

            
            
        if ( not theRetrievePreviousVersions) and ( not theRetrieveNextVersions):
            return self
        
        unPreviousVersionsField = unPreviousVersionsLinkFieldsCache.get( unVersionedElementMetaType, None)
        unNextVersionsField     = unNextVersionsLinkFieldsCache.get( unVersionedElementMetaType, None)
        
        
        if not unPreviousVersionsField or not unNextVersionsField:
            try:
                unVersioningLinksFieldNames = unVersionedElement.versioning_link_fields
            except:
                None
            if not unVersioningLinksFieldNames:
                return self
        
            unPreviousVersionsLinkFieldName = unVersioningLinksFieldNames[ 0]
            unNextVersionsLinkFieldName     = unVersioningLinksFieldNames[ 1]
            
            if not unPreviousVersionsLinkFieldName or not unNextVersionsLinkFieldName:
                return self

            if not unPreviousVersionsField:
                unPreviousVersionsField = unSchema.get( unPreviousVersionsLinkFieldName, None)
                if not unPreviousVersionsField:
                    return self
                unPreviousVersionsLinkFieldsCache[ unVersionedElementMetaType] = unPreviousVersionsField
                
            if not unNextVersionsField:
                unNextVersionsField = unSchema.get( unNextVersionsLinkFieldName, None)
                if not unNextVersionsField:
                    return self
                unNextVersionsLinkFieldsCache[ unVersionedElementMetaType] = unNextVersionsField
            
            
        
      
        if theRetrievePreviousVersions:

            unPreviousVersionsAccessor = unPreviousVersionsField.getAccessor( unVersionedElement)
            if unPreviousVersionsAccessor:
                unasPreviousVersions = None
                try:
                    unasPreviousVersions = unPreviousVersionsAccessor()
                except:
                    None
                
            if not ( unasPreviousVersions == None):
                
                for unaPreviousVersion in unasPreviousVersions:
                    
                    unaPreviousVersionUID = unaPreviousVersion.UID()
                    if unaPreviousVersionUID:
                
                        unExistingPreviousVersioningInfo = unAlreadyVisited.get( unaPreviousVersionUID, None)
                        if unExistingPreviousVersioningInfo:
                            unReusedVersioningInfo = unExistingPreviousVersioningInfo.copy()
                            unReusedVersioningInfo[ 'reused'] = unExistingPreviousVersioningInfo
                            unReusedVersioningInfo[ 'previous_versioning_infos'] = None
                            unReusedVersioningInfo[ 'previous_initialized'] = False
                            unReusedVersioningInfo[ 'next_versioning_infos'] = None
                            unReusedVersioningInfo[ 'next_initialized'] = False
                            
                            theVersioningInfo[ 'previous_versioning_infos'].append( unReusedVersioningInfo)  
                      
                        else:
                        
                            unAlreadyVisited[ unaPreviousVersionUID] = unaPreviousVersion
                            
                            
                            unPreviousVersioningInfo = self.fNewVoidVersioningInfo()
                            unPreviousVersioningInfo.update( {
                                'element':    unaPreviousVersion,
                            })
                            
                            theVersioningInfo[ 'previous_versioning_infos'].append( unPreviousVersioningInfo)  
                            
                            self.pRetrieveVersionInfo_Inner( 
                                theTimeProfilingResults             =theTimeProfilingResults,
                                theModelDDvlPloneTool_Retrieval     =unModelDDvlPloneTool_Retrieval,
                                theRetrievePreviousVersions         =theRecurse,
                                theRetrieveNextVersions             =False,
                                theRecurse                          =theRecurse,
                                theAlreadyVisited                   =unAlreadyVisited,
                                theVersioningInfo                   =unPreviousVersioningInfo, 
                                theVersionNameFieldsCache           =theVersionNameFieldsCache,
                                thePreviousVersionsLinkFieldsCache  =thePreviousVersionsLinkFieldsCache,
                                theNextVersionsLinkFieldsCache      =theNextVersionsLinkFieldsCache,
                                theAdditionalParams                 =theAdditionalParams,
                            )
                        
            theVersioningInfo[ 'previous_initialized'] = True
            
            

        if theRetrieveNextVersions:

            unNextVersionsAccessor = unNextVersionsField.getAccessor( unVersionedElement)
            if unNextVersionsAccessor:
                unasNextVersions = None
                try:
                    unasNextVersions = unNextVersionsAccessor()
                except:
                    None
                
            if not ( unasNextVersions == None):
                
                for unaNextVersion in unasNextVersions:
                    
                    unaNextVersionUID = unaNextVersion.UID()
                    if unaNextVersionUID:
                
                        unExistingNextVersioningInfo = unAlreadyVisited.get( unaNextVersionUID, None)
                        if unExistingNextVersioningInfo:
                            unReusedVersioningInfo = unExistingNextVersioningInfo.copy()
                            unReusedVersioningInfo[ 'reused'] = unExistingNextVersioningInfo
                            unReusedVersioningInfo[ 'next_versioning_infos'] = None
                            unReusedVersioningInfo[ 'next_initialized'] = False
                            unReusedVersioningInfo[ 'next_versioning_infos'] = None
                            unReusedVersioningInfo[ 'next_initialized'] = False
                                                        
                            theVersioningInfo[ 'next_versioning_infos'].append( unExistingNextVersioningInfo)  
                        
                        else:
                        
                            unAlreadyVisited[ unaNextVersionUID] = unaNextVersion
                            
                            
                            unNextVersioningInfo = self.fNewVoidVersioningInfo()
                            unNextVersioningInfo.update( {
                                'element':    unaNextVersion,
                            })
                            
                            theVersioningInfo[ 'next_versioning_infos'].append( unNextVersioningInfo)  
                            
                            self.pRetrieveVersionInfo_Inner( 
                                theTimeProfilingResults             =theTimeProfilingResults,
                                theModelDDvlPloneTool_Retrieval     =unModelDDvlPloneTool_Retrieval,
                                theRetrievePreviousVersions         =False,
                                theRetrieveNextVersions             =theRecurse,
                                theRecurse                          =theRecurse,
                                theAlreadyVisited                   =unAlreadyVisited,
                                theVersioningInfo                   =unNextVersioningInfo, 
                                theVersionNameFieldsCache           =theVersionNameFieldsCache,
                                thePreviousVersionsLinkFieldsCache  =thePreviousVersionsLinkFieldsCache,
                                theNextVersionsLinkFieldsCache      =theNextVersionsLinkFieldsCache,
                                theAdditionalParams                 =theAdditionalParams,
                            )
                        
            theVersioningInfo[ 'next_initialized'] = True
            
        if not unVersionName:
            if ( not unasPreviousVersions) and ( not unasNextVersions):
                theVersioningInfo[ 'version'] = cVersionName_UnVersioned
            else:
                theVersioningInfo[ 'version'] = cVersionName_MissingVersionName
                
            
        theVersioningInfo[ 'success'] = True

        return self
    
    
    
    
    
                
    
    security.declarePrivate( 'fRetrieveAllVersionsWithContainerPloneSiteAndClipboard')
    def fRetrieveAllVersionsWithContainerPloneSiteAndClipboard( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool_Retrieval=None,
        theVersionedElement             =None, 
        theAdditionalParams            =None):
        """Create a new version of the original object which shall be a root, with the new version name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveAllVersionsWithContainerPloneSiteAndClipboard', theTimeProfilingResults)
                      
        try:
            unAllVersionsReport = { 'success': False, }  
            try:
                
                # ##############################################################
                """Prepare result structure.
                
                """
                unAllVersionsReport = self.fNewVoidAllVersionsReport()
                

                # ##############################################################
                """Check for element to create a new version from.
                
                """
                if ( theVersionedElement == None):
                    return unAllVersionsReport
                unAllVersionsReport[ 'versioned_element'] = theVersionedElement
                
                
                
                
                # ##############################################################
                """Assert whether the element can be versioned.
                
                """
                unVersionPermission = False
                try:
                    unVersionPermission = theVersionedElement.fAllowVersion()
                except:
                    None
                unAllVersionsReport[ 'allow_version'] = unVersionPermission  
                
                if not unVersionPermission:
                    return unAllVersionsReport

                
                
                # ##############################################################
                """Check for necessary parameters.
                
                """
                if not theModelDDvlPloneTool_Retrieval:
                    return unAllVersionsReport
                    
                
                unVoid = self.fRetrieveAllVersions( 
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theModelDDvlPloneTool_Retrieval=theModelDDvlPloneTool_Retrieval,
                    theVersionedElement            =theVersionedElement, 
                    theAllVersionsReport           =unAllVersionsReport,
                    theAdditionalParams            =theAdditionalParams,
                )
                
                if not unAllVersionsReport or not unAllVersionsReport.get( 'success', False):
                    return unAllVersionsReport
                
                
                unCheckedPermissionsCache = theModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                
                                    
                # ##############################################################
                """Retrieve the parent of current version and check if it may be a candidate to contain the new version.
                
                """
                unParentElement = aq_parent( aq_inner( theVersionedElement))
                if not ( unParentElement == None):
                    unParentCandidateContainerReport = self.fRetrieveCandidateVersionContainerReport( theModelDDvlPloneTool_Retrieval, theVersionedElement, unParentElement, theVersionedElement.getId(), theVersionedElement.Title(), unCheckedPermissionsCache,)
                    if unParentCandidateContainerReport.get( 'allowed', False):
                        unAllVersionsReport[ 'parent_container_report'] = unParentCandidateContainerReport
                            
                                 
                
                        
                        
                # ##############################################################
                """Retrieve first element from CLIPBOARD and check if it may be a candidate to contain the new version.
                
                """
                
                unosElementosFromClipboard = theModelDDvlPloneTool_Retrieval.fClipboardCookieElements( theVersionedElement.REQUEST, theVersionedElement)
                if unosElementosFromClipboard:
                    
                    for unElementoFromClipboard in unosElementosFromClipboard:
                        if not ( unElementoFromClipboard == None):
                            
                            if unAllVersionsReport[ 'parent_container_report'] and ( unElementoFromClipboard == unAllVersionsReport[ 'parent_container_report'].get( 'element', None)):
                                unAllVersionsReport[ 'clipboard_container_report'] = unAllVersionsReport[ 'parent_container_report']
                                break
                            
                            else:
                                unClipboardCandidateContainerReport = self.fRetrieveCandidateVersionContainerReport( theModelDDvlPloneTool_Retrieval, theVersionedElement, unElementoFromClipboard, theVersionedElement.getId(), theVersionedElement.Title(), unCheckedPermissionsCache,)
                                if unClipboardCandidateContainerReport.get( 'allowed', False):
                                    unAllVersionsReport[ 'clipboard_container_report'] = unClipboardCandidateContainerReport
                                    break
                                    
                # ##############################################################
                """Retrieve Plone Site and check if it may be a candidate to contain the new version.
                
                """
                       
                unSite = theModelDDvlPloneTool_Retrieval.fPortalRoot( theVersionedElement)
                if not ( unSite == None):
                    if unAllVersionsReport[ 'parent_container_report'] and ( unSite == unAllVersionsReport[ 'parent_container_report'].get( 'element', None)):
                        unAllVersionsReport[ 'site_container_report'] = unAllVersionsReport[ 'parent_container_report']
                    elif unAllVersionsReport[ 'clipboard_container_report'] and ( unSite == unAllVersionsReport[ 'clipboard_container_report'].get( 'element', None)):
                        unAllVersionsReport[ 'site_container_report'] = unAllVersionsReport[ 'clipboard_container_report']
                    else:
                        unSiteCandidateContainerReport = self.fRetrieveCandidateVersionContainerReport( theModelDDvlPloneTool_Retrieval, theVersionedElement, unSite, theVersionedElement.getId(), theVersionedElement.Title(), unCheckedPermissionsCache)
                        if unSiteCandidateContainerReport.get( 'allowed', False):
                            unAllVersionsReport[ 'site_container_report'] = unSiteCandidateContainerReport
                        
                    
                unAllVersionsReport[ 'success'] = True
                
                return unAllVersionsReport
                          
                
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fRetrieveAllVersionsWithContainerPloneSiteAndClipboard\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unAllVersionsReport:
                    unAllVersionsReport = { }

                unAllVersionsReport.update( { 
                    'success':      False,
                    'status':       'Exception',
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unAllVersionsReport
                        
            return  unAllVersionsReport     
        
         
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveAllVersionsWithContainerPloneSiteAndClipboard', theTimeProfilingResults)
            
    
               
    
        
                
    
    
                
    
    security.declarePrivate( 'fRetrieveAllVersions')
    def fRetrieveAllVersions( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool_Retrieval=None,
        theVersionedElement             =None, 
        theAllVersionsReport           =None,
        theAdditionalParams            =None):
        """Create a new version of the original object which shall be a root, with the new version name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveAllVersions', theTimeProfilingResults)
                      
        try:
            # ##############################################################
            """Prepare result structure.
            
            """
            unAllVersionsReport = theAllVersionsReport
            if not unAllVersionsReport:
                unAllVersionsReport = self.fNewVoidAllVersionsReport()
                
            unAllVersionsReport.update( { 'success': False, })
            
            try:
                
                # ##############################################################
                """Check for element to create a new version from.
                
                """
                if ( theVersionedElement == None):
                    return unAllVersionsReport
                unAllVersionsReport[ 'versioned_element'] = theVersionedElement
                
                
                
                
                # ##############################################################
                """Assert whether the element can be versioned.
                
                """
                unVersionPermission = False
                try:
                    unVersionPermission = theVersionedElement.fAllowVersion()
                except:
                    None
                unAllVersionsReport[ 'allow_version'] = unVersionPermission  

                
                
                # ##############################################################
                """Check for necessary parameters.
                
                """
                if not theModelDDvlPloneTool_Retrieval:
                    return unAllVersionsReport
                    
                
               # ##############################################################
                """Retrieve traversal results for versioned element 
                
                """
                unTranslationsCaches      = theModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()
                unCheckedPermissionsCache = theModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                someAllTypeConfigs        = { }
                
                someDefaultColumnNames        = [ 'title', 'description', ]
                
                unOriginalResult = theModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                    theTimeProfilingResults     = theTimeProfilingResults,
                    theElement                  = theVersionedElement, 
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
                if not unOriginalResult or not( unOriginalResult.get( 'object', None) == theVersionedElement):
                    return unAllVersionsReport
                 
                unAllVersionsReport[ 'versioned_element_result'] = unOriginalResult      
                
                
          
                    
                    
                    
                # ##############################################################
                """Retrieve translations for attributes in columns in version tables (current, previous, next).
                
                """
                unAllVersionsReport[ 'column_names'].extend( someDefaultColumnNames)
                unAllVersionsReport[ 'column_names'].extend( [ 'version', 'version_comment', 'id', 'path',])
                someDefaultColumnTranslations = theModelDDvlPloneTool_Retrieval.getTranslationsForDefaultAttributes( theVersionedElement)
                theModelDDvlPloneTool_Retrieval.pUpdateTranslationsForObjectAttribute( theModelDDvlPloneTool_Retrieval, someDefaultColumnTranslations, theVersionedElement, 'version')
                theModelDDvlPloneTool_Retrieval.pUpdateTranslationsForObjectAttribute( theModelDDvlPloneTool_Retrieval, someDefaultColumnTranslations, theVersionedElement, 'version_comment')
                # ACV 20091002 Now is retrieved with the translations for Default attributes. Removed.
                #
                #theModelDDvlPloneTool_Retrieval.pUpdateTranslationsForObjectAttribute( theModelDDvlPloneTool_Retrieval, someDefaultColumnTranslations, theVersionedElement, 'path')
                unAllVersionsReport[ 'column_translations'] = someDefaultColumnTranslations
                    
                
                # ##############################################################
                """Retrieve current version info, and version infos for all previous and next versions, as a tree.
                
                """
                someAllVersionsByName = unAllVersionsReport[ 'all_versions_by_name'] 

                unInterVersionUIDFieldsCache      = { }
                unVersionNameFieldsCache          = { }
                unVersionCommentFieldsCache       = { }
                unPreviousVersionsLinkFieldsCache = { }
                unNextVersionsLinkFieldsCache     = { }
                
                unOriginalVersioningInfo = self.fRetrieveVersioningInfo( 
                    theTimeProfilingResults          = theTimeProfilingResults,
                    theModelDDvlPloneTool_Retrieval  = theModelDDvlPloneTool_Retrieval,
                    theRetrievePreviousVersions      = True,
                    theRetrieveNextVersions          = True,
                    theRecurse                       = True,
                    theVersionedElement              = theVersionedElement, 
                    theInterVersionUIDFieldsCache    = unInterVersionUIDFieldsCache,
                    theVersionNameFieldsCache        = unVersionNameFieldsCache,
                    theAllVersionsByName             = someAllVersionsByName,
                    theVersionCommentFieldsCache     = unVersionCommentFieldsCache,
                    thePreviousVersionsLinkFieldsCache=unPreviousVersionsLinkFieldsCache,
                    theNextVersionsLinkFieldsCache   = unNextVersionsLinkFieldsCache,
                    theAdditionalParams              = theAdditionalParams,
                )
                unAllVersionsReport[ 'original_version_info'] = unOriginalVersioningInfo
       
                unAllVersionsReport[ 'success'] = True
                
                return unAllVersionsReport
                          
                
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fRetrieveAllVersions\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unAllVersionsReport:
                    unAllVersionsReport = { }

                unAllVersionsReport.update( { 
                    'success':      False,
                    'status':       'Exception',
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unAllVersionsReport
                        
            return  unAllVersionsReport     
        
         
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveAllVersions', theTimeProfilingResults)
            
    
               
    
                        
                
                
                
                

    security.declarePrivate( 'fRetrieveCandidateVersionContainerReport')
    def fRetrieveCandidateVersionContainerReport( self, 
        theModelDDvlPloneTool_Retrieval,
        theVersionedElement,
        theCandidateContainer,
        theOriginalId,
        theOriginalTitle,
        theCheckedPermissionsCache,):
                 
                                    
        # ##############################################################
        """Retrieve the parent of current version and check if it may be a candidate to contain the new version.
        
        """
        unCandidateContainerReport = self.fNewVoidCandidateContainerReport()
        
        if ( theCandidateContainer == None):
            return unCandidateContainerReport
        

        unMetaType = theCandidateContainer.meta_type
            
        if not unMetaType in cAcceptedVersionContainerMetaTypes:
            return unCandidateContainerReport
                    
        if not theModelDDvlPloneTool_Retrieval.fCheckElementPermission( theCandidateContainer, cPermissionsOnVersionContainers, theCheckedPermissionsCache ):
            return unCandidateContainerReport
        
                    
        unaUID = ''
        if unMetaType in cPloneSiteMetaTypes:
            unaUID = cFakeUIDForPloneSite
        else:
            unaUID = theCandidateContainer.UID()
            
        unCandidateContainerReport.update( {
            'allowed':                   True,
            'element':                   theCandidateContainer,
            'title':                     theModelDDvlPloneTool_Retrieval.fAsUnicode( theCandidateContainer.Title(),       theVersionedElement),
            'description':               theModelDDvlPloneTool_Retrieval.fAsUnicode( theCandidateContainer.Description(), theVersionedElement),
            'id':                        theModelDDvlPloneTool_Retrieval.fAsUnicode( theCandidateContainer.getId(),       theVersionedElement),
            'path':                      theModelDDvlPloneTool_Retrieval.fAsUnicode( '/'.join( theCandidateContainer.getPhysicalPath()),       theVersionedElement),
            'UID':                       theModelDDvlPloneTool_Retrieval.fAsUnicode( unaUID,                        theVersionedElement),
            'children_titles':           [],
            'children_ids':              [],
        })
        
        

        # ##############################################################
        """Retrieve the titles and ids of child elements of the container for the new version. These will be siblings of the new version, and the new version can not have same title or id than one of these pre-existing children of the new version container.
        
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
            unTitle = theModelDDvlPloneTool_Retrieval.fAsUnicode( unTitle, theVersionedElement)
            if unTitle:
                if not ( unTitle in unosContainerChildrenTitles):
                    unosContainerChildrenTitles.append( unTitle)
                
            unId = ''
            try:
                unId = unChild.getId()
            except:
                None
            unId = theModelDDvlPloneTool_Retrieval.fAsUnicode( unId, theVersionedElement)                
            if unId:
                if not ( unId in unosContainerChildrenIds):
                    unosContainerChildrenIds.append( unId)
                
        unCandidateContainerReport[ 'children_titles'] = sorted( unosContainerChildrenTitles)
        unCandidateContainerReport[ 'children_ids']    = sorted( unosContainerChildrenIds)
       
        
        
        # ##############################################################
        """Calculate a Title and an Id for the new version, derived from the title and version of the element to create the new version from, but not duplicating any title or id in the container of the new version.
        
        """
        unOriginalTitle = theVersionedElement.Title()
        unOriginalId    = theVersionedElement.getId()
       
        aPloneToolForNormalizeString = getToolByName( theVersionedElement, 'plone_utils', None)
        if aPloneToolForNormalizeString  and  not shasattr( aPloneToolForNormalizeString, 'normalizeString'):
            aPloneToolForNormalizeString = None
        
        unNewVersionId    = theModelDDvlPloneTool_Retrieval.fUniqueStringWithCounter( unOriginalId,    unosContainerChildrenIds, aPloneToolForNormalizeString)
        if not unNewVersionId:
            unNewVersionId = unOriginalId + '-version'
        unNewVersionId = theModelDDvlPloneTool_Retrieval.fAsUnicode( unNewVersionId, theVersionedElement)
        
        unCandidateContainerReport[ 'new_id'] = unNewVersionId
        
        
        unNewVersionTitle = theModelDDvlPloneTool_Retrieval.fUniqueStringWithCounter( unOriginalTitle, unosContainerChildrenTitles)
        if not unNewVersionTitle:
            unNewVersionTitle = unOriginalTitle + '-Version'
        unNewVersionTitle = theModelDDvlPloneTool_Retrieval.fAsUnicode( unNewVersionTitle, theVersionedElement)

        unCandidateContainerReport[ 'new_title'] = unNewVersionTitle
                            
        return unCandidateContainerReport
                    

                                
                        
        

    security.declarePrivate( 'fNewVersion')
    def fNewVersion( self,
        theTimeProfilingResults        =None,
        theModelDDvlPloneTool          =None,
        theModelDDvlPloneTool_Retrieval=None,
        theModelDDvlPloneTool_Mutators =None,
        theOriginalObject              =None, 
        theNewVersionContainerKind     =None,
        theNewVersionName              =None,
        theNewVersionComment           =None,
        theNewTitle                    =None,
        theNewId                       =None,
        theMDDNewVersionTypeConfigs    =None, 
        thePloneNewVersionTypeConfigs  =None, 
        theAdditionalParams            =None):
        """Create a new version of the original object which shall be a root, with the new version name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fNewVersion', theTimeProfilingResults)
                      
        try:
            unNewVersionReport = None
            try:
                
                # ##############################################################################
                """Transaction Save point before import to get a clean view on the existing object network.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                
                unNewTitle          = theNewTitle.strip()
                unNewId             = theNewId.strip()
                unNewVersionName    = theNewVersionName.strip()
                unNewVersionComment = theNewVersionComment.strip()
                
                unNewVersionContext   = self.fNewVoidNewVersionContext()
                unNewVersionReport    = unNewVersionContext.get( 'report', {})
                unosNewVersionErrors  = unNewVersionContext.get( 'newversion_errors', {})
                
                
                
                # ##############################################################################
                """Check parameter with original version to copy from.
                
                """      
                if ( theOriginalObject == None):
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_MissingParameter_OriginalObject,
                    })
                    return unNewVersionReport
                unNewVersionContext[ 'original_object'] = theOriginalObject

                
                
                # ##############################################################################
                """Check critical parameters.
                
                """      
                if not theModelDDvlPloneTool_Retrieval:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval,
                    })
                    return unNewVersionReport
                unNewVersionContext[ 'ModelDDvlPloneTool_Retrieval'] = theModelDDvlPloneTool_Retrieval
                
                if not theModelDDvlPloneTool_Mutators:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators,
                    })
                    return unNewVersionReport
                unNewVersionContext[ 'ModelDDvlPloneTool_Mutators'] = theModelDDvlPloneTool_Mutators

                
                
                
                # ##############################################################################
                """Incorporate additional params into context.
                
                """ 
                if theAdditionalParams:
                    unNewVersionContext[ 'additional_params'].update( theAdditionalParams)
                
                                    
                    
                
                # ##############################################################################
                """Check permissions on original version element.
                
                """ 
                
                unCheckedPermissionsCache = theModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                unNewVersionContext[ 'checked_permissions_cache'] = unCheckedPermissionsCache
                
                if not theModelDDvlPloneTool_Retrieval.fCheckElementPermission( theOriginalObject, permissions.View , unCheckedPermissionsCache):
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Original_NotReadable,
                    })
                    return unNewVersionReport
                
                
                # ##############################################################################
                """Chek versioning allowed in the original object.
                
                """      
                unAllowNewVersion = False
                try:
                    unAllowNewVersion = theOriginalObject.fAllowVersion()
                except:
                    None
                    
                if not unAllowNewVersion:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_NewVersion_NotAllowedInElement,
                    })
                    return unNewVersionReport
                           
                
                # ##############################################################################
                """Chek version name parameter.
                
                """      
                if not unNewVersionName:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_MissingParameter_VersionName,
                    })
                    return unNewVersionReport
                unNewVersionContext[ 'version_name'] = theOriginalObject
                
                                
                
                # ##############################################################################
                """Check auxiliary parameters.
                
                """      
                if not theMDDNewVersionTypeConfigs:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_MissingParameter_MDDNewVersionTypeConfigs,
                    })
                    return unNewVersionReport
                unNewVersionContext[ 'mdd_type_configs'] = theMDDNewVersionTypeConfigs
                        
                
                
                
                # ##############################################################################
                """Retrieve translation_service tool to handle the input encoding.
                
                """
                aTranslationService = getToolByName( theOriginalObject, 'translation_service', None)      
                if not aTranslationService:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Internal_MissingTool_translation_service,
                    })
                    return unNewVersionReport
                unNewVersionContext[ 'translation_service'] = aTranslationService
                
                
                
                # ##############################################################################
                """Retrieve all the versioning information, from the original element and all its previous and next versions.
                
                """      
                unAllVersionsReport = self.fRetrieveAllVersionsWithContainerPloneSiteAndClipboard(
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theModelDDvlPloneTool_Retrieval=theModelDDvlPloneTool_Retrieval,
                    theVersionedElement            =theOriginalObject, 
                    theAdditionalParams            =theAdditionalParams,
                )
                if ( not unAllVersionsReport) or not unAllVersionsReport.get( 'success', False):
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Failure_Retrieving_AllVersions,
                    })
                    return unNewVersionReport
                
                
                
                # ##############################################################################
                """Obtain the element to become the parent of the new version: where the new duplicate shall be created. One of the Parent of the current version, or one of the elements in the clipboard, or the root of the Plone site.
                
                """      
                if not ( theNewVersionContainerKind in [ 'Parent', 'Clipboard', 'Site', ]):
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_MissingParameter_ContainerKind,
                    })
                    return unNewVersionReport
                
                
                
                unContainerReport = None
                if theNewVersionContainerKind   == 'Parent':
                    unContainerReport = unAllVersionsReport.get( 'parent_container_report', {})
                elif theNewVersionContainerKind == 'Clipboard':
                    unContainerReport = unAllVersionsReport.get( 'clipboard_container_report', {})
                elif theNewVersionContainerKind   == 'Site':
                    unContainerReport = unAllVersionsReport.get( 'site_container_report', {})
                    
                if not unContainerReport:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_ContainerReport_Missing,
                    })
                    return unNewVersionReport
                
                if not unContainerReport.get( 'allowed', False):
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_ContainerReport_NotAllowed,
                    })
                    return unNewVersionReport
                
                unContainer = unContainerReport.get( 'element', None)
                if unContainer == None:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Container_NotFound,
                    })
                    return unNewVersionReport
                
                unNewVersionContext[ 'container_object'] = unContainer

                
                
                # ##############################################################################
                """Check permissions on new version container.
                
                """      
                if not theModelDDvlPloneTool_Retrieval.fCheckElementPermission( unContainer, cPermissionsOnVersionContainers, unCheckedPermissionsCache):
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Container_NotWritable,
                    })
                    return unNewVersionReport
                
                
                
                # ##############################################################################
                """Check uniqueness of title and id for new version.
                
                """      
                unosTitlesToAvoid = unContainerReport.get( 'children_titles', [])
                if unNewTitle in unosTitlesToAvoid:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Title_AlreadyExists,
                    })
                    return unNewVersionReport
                    
                unasIdsToAvoid = unContainerReport.get( 'children_ids', [])
                if theNewId in unasIdsToAvoid:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Id_AlreadyExists,
                    })
                    return unNewVersionReport
                    
                
                
                    
                 
                # ##############################################################################
                """Check uniqueness of name for the new version.
                
                """      
                unasExistingVersionNames = unContainerReport.get( 'all_versions_by_name', {}).keys()
                if unNewVersionName in unasExistingVersionNames:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_VersionName_AlreadyExists,
                    })
                    return unNewVersionReport
                                

                
                
                
                
                   
                # ##############################################################################
                """Retrieve original object result not needed because the refactor shall use directly the values in the original elements.
                
                """      
                
     

                # ##############################################################################
                """Create new version root by duplicating the original object as target of the copy, to be populated later with attributes, aggregates and relations.
                
                """      
                if aTranslationService:
                    unNewTitle          = aTranslationService.encode( unNewTitle)
                    unNewId             = aTranslationService.encode( unNewId)
                    unNewVersionName    = aTranslationService.encode( unNewVersionName)
                    unNewVersionComment = aTranslationService.encode( unNewVersionComment)
                
                unTypeToCreate = theOriginalObject.meta_type
                anAttrsDict = {
                    'title':          unNewTitle,
                    'versionInterna':    unNewVersionName,
                    'comentarioVersionInterna': unNewVersionComment,
                }
                
                unCreatedId = None
                try:
                    unCreatedVersionId = unContainer.invokeFactory( unTypeToCreate, unNewId, **anAttrsDict)
                except:
                    return None
                if not unCreatedVersionId:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_ObjectNotCreated,
                    })
                    return unNewVersionReport
        
   
                unosElementsAfterCreation = unContainer.objectValues()
                unNewVersionElement = None
                for unElement in unosElementsAfterCreation:
                    unId = unElement.getId()
                    if unId == unCreatedVersionId:
                        unNewVersionElement = unElement
                        break
                if ( unNewVersionElement == None):
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_CreatedObjectNotFound,
                    })
                    return unNewVersionReport
                
                unNewVersionElement.manage_fixupOwnershipAfterAdd()
                
                theModelDDvlPloneTool_Mutators.pSetElementPermissions( unNewVersionElement)
                 
                theModelDDvlPloneTool_Mutators.pSetAudit_Creation( unNewVersionElement)
                
                unNewVersionReport[ 'new_version_element'] = unNewVersionElement
                
                
                # ##############################################################################
                """Transaction Save point before import to get a clean view on the existing object network.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                
                # ##############################################################################
                """Retrieve results for new version element just created. Required by the copy machinery.
                
                """      
                somePloneNewVersionTypeConfigs = thePloneNewVersionTypeConfigs
                if not somePloneNewVersionTypeConfigs:
                    somePloneNewVersionTypeConfigs = {}
                unNewVersionContext[ 'plone_type_configs'] = somePloneNewVersionTypeConfigs
                
                
                allNewVersionTypeConfigs = somePloneNewVersionTypeConfigs.copy()
                allNewVersionTypeConfigs.update( theMDDNewVersionTypeConfigs)
                unNewVersionContext[ 'all_copy_type_configs'] = allNewVersionTypeConfigs
                
                
                unNewVersionElementResult = self.fRetrieveJustCreatedVersionResult( 
                    theTimeProfilingResults        =theTimeProfilingResults,
                    theNewVersionContext           =unNewVersionContext,
                    theNewVersionElement            =unNewVersionElement, 
                    theAdditionalParams            =theAdditionalParams,
                )
                if ( not unNewVersionElementResult) or unNewVersionElementResult.get( 'object', None) == None:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_CreatedObjectResultFaulure,
                    })
                    return unNewVersionReport
                
                # ACV 20091110. Unused. Creates a very big log entry. Removed
                # unNewVersionReport[ 'new_version_element_result'] = unNewVersionElementResult
                
                
                
                 
                
                # ##############################################################################
                """Traverse source elements network and create copy linked with new version traceability links.
                
                """      
        


                unRefactor = MDDRefactor_NewVersion( 
                    theModelDDvlPloneTool,
                    theModelDDvlPloneTool_Retrieval,
                    theModelDDvlPloneTool_Mutators,
                    theOriginalObject, 
                    unNewVersionElement, 
                    unNewVersionElementResult,
                    unNewVersionName,
                    unNewVersionComment,
                    theMDDNewVersionTypeConfigs,
                    somePloneNewVersionTypeConfigs,
                    allNewVersionTypeConfigs, 
                    MDDRefactor_Version_Exception
                )  
                if ( not unRefactor) or not unRefactor.vInitialized:
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Internal_Refactor_NotInitialized,
                    })
                    return unNewVersionReport
                    
                
                unHuboRefactorException  = False
                unHuboException  = False
                unRefactorResult = False
                try:
                    
                    try:
                        unRefactorResult = unRefactor.fRefactor()
                        
                        unNewVersionElement.setTitle( unNewTitle)
                        unNewVersionElement.reindexObject()
                        
                        unNewVersionElementSchema = None
                        try:
                            unNewVersionElementSchema = unNewVersionElement.schema
                        except:
                            None
                        if unNewVersionElementSchema:
                            
                            unVersionFieldName = None
                            try:
                                unVersionFieldName = unNewVersionElement.version_field_storage
                            except:
                                None
                            if unVersionFieldName:
                                if unNewVersionElementSchema.has_key( unVersionFieldName):
                                    unVersionField = unNewVersionElementSchema[ unVersionFieldName]
                                    if unVersionField:
                                        unVersionMutator = unVersionField.getMutator( unNewVersionElement)
                                        if unVersionMutator:
                                            
                                            unVersionMutator( unNewVersionName)
                                            
                                        else:
                                            unNewVersionReport.update( { 
                                                'success':      False,
                                                'status':       cMDDNewVersionStatus_Error_Internal_NoMutator_version_field_storage,
                                            })
                                            return unNewVersionReport
                                        
                            unVersionCommentFieldName = None
                            try:
                                unVersionCommentFieldName = unNewVersionElement.version_comment_field_storage
                            except:
                                None
                            if unVersionCommentFieldName:
                                if unNewVersionElementSchema.has_key( unVersionCommentFieldName):
                                    unVersionCommentField = unNewVersionElementSchema[ unVersionCommentFieldName]
                                    if unVersionCommentField:
                                        unVersionCommentMutator = unVersionCommentField.getMutator( unNewVersionElement)
                                        if unVersionCommentMutator:
                                            
                                            unVersionCommentMutator( unNewVersionComment)
                                            
                                        else:
                                            unNewVersionReport.update( { 
                                                'success':      False,
                                                'status':       cMDDNewVersionStatus_Error_Internal_NoMutator_version_comment_field_storage,
                                            })
                                            return unNewVersionReport
                                        
                                            
                    
                                        
                    except MDDRefactor_Version_Exception:
                        
                        unHuboRefactorException = True
                        
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                        
                        unInformeExcepcion = ''
                        if unRefactor and unRefactor.vErrorReports:
                            unInformeExcepcion = '%s\n' % '\n'.join( [ str( unErrorReport) for unErrorReport in unRefactor.vErrorReports])
                        
                        unInformeExcepcion += 'Exception during ModelDDvlPloneTool_Refactor::fNewVersion invoking MDDRefactor_NewVersion::fRefactor\n' 
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        unNewVersionReport[ 'exception'] = unInformeExcepcion
                                 
                        if cLogExceptions:
                            logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                        
                except:
                    unHuboException = True
                    raise
                    
                
                unNewVersionReport.update( {
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
                unNewVersionReport[ 'error_reports'].extend( unRefactor.vErrorReports )
                            
                if ( not unHuboException) and ( not unHuboRefactorException) and unRefactorResult:
                    
                    ModelDDvlPloneTool_Transactions().fTransaction_Commit()
    
                    unNewVersionReport.update( { 
                         'success':      True,
                    })
                    
                    if cLogVersionResults:
                        unStringErrorReports = ''
                        if unRefactor and unRefactor.vErrorReports:
                            unInformeExcepcion = '%s\n' % '\n'.join( [ str( unErrorReport) for unErrorReport in unRefactor.vErrorReports])
                        logging.getLogger( 'ModelDDvlPlone').info( 'COMMIT: %s::fNewVersion\n%s\n%s\n' % ( self.__class__.__name__, fPrettyPrint( [ unNewVersionReport, ]), unStringErrorReports))
                    
                else:
                    ModelDDvlPloneTool_Transactions().fTransaction_Abort()
                                    
                    
                    unNewVersionReport.update( { 
                        'success':      False,
                        'status':       cMDDNewVersionStatus_Error_Internal_Refactor_Failed,
                    })

                    unStringErrorReports = ''
                    if unRefactor and unRefactor.vErrorReports:
                        unInformeExcepcion = '%s\n' % '\n'.join( [ str( unErrorReport) for unErrorReport in unRefactor.vErrorReports])
                
                    if cLogVersionResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'ABORT: %s::fNewVersion\n%s%s\n' % ( self.__class__.__name__, fPrettyPrint( [ unNewVersionReport, ]), unStringErrorReports))
                    
                return unNewVersionReport                
                
                
                
          
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fNewVersion\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unNewVersionReport:
                    unNewVersionReport = { }
                    
                unNewVersionReport.update( { 
                    'success':      False,
                    'status':       cMDDNewVersionStatus_Error_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unNewVersionReport
                        
            return { 'success': False, }
         
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fNewVersion', theTimeProfilingResults)
            
    
               

    
        

    security.declarePrivate( 'fRetrieveJustCreatedVersionResult')
    def fRetrieveJustCreatedVersionResult( self,
        theTimeProfilingResults        =None,
        theNewVersionContext           =None,
        theNewVersionElement           =None, 
        theAdditionalParams            =None):
        """
        
        """
        
        try:
            if not theNewVersionContext:
                return None
           
            if not theNewVersionElement:
                return None
           
            allCopyTypeConfigs = theNewVersionContext.get( 'all_copy_type_configs', {})
            if not allCopyTypeConfigs:
                return None
                            
            someAdditionalParams = theNewVersionContext.get(  'additional_params', None)
            
            aModelDDvlPloneTool_Retrieval = theNewVersionContext.get( 'ModelDDvlPloneTool_Retrieval', None)
            
            unCheckedPermissionsCache = theNewVersionContext.get( 'checked_permissions_cache', None)
            
            unElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     = theTimeProfilingResults,
                theElement                  = theNewVersionElement, 
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
            if not unElementResult or not( unElementResult.get( 'object', None) == theNewVersionElement):
                return None
                        
        
            return unElementResult
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during fImport fRetrieveContainer\n' 
            unInformeExcepcion += 'source object %s\n' % str( theNewVersionElement) 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            return None
                    
        return None    
    

     