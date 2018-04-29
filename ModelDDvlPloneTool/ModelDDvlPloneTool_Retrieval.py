# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval.py
#
# Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
#
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
#
# Authors: 
# Model Driven Development sl  Valencia (Spain) www.ModelDD.org 
# Antonio Carrasco Valero                       carrasco@ModelDD.org
#

__author__ = """Model Driven Development sl <ModelDDvlPlone@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'



import sys
import traceback

import logging


from marshal import loads,    dumps
from urllib  import quote,    unquote
from zlib    import compress, decompress


from time     import time
from DateTime import DateTime


from OFS     import Moniker        


from AccessControl          import ClassSecurityInfo

from Acquisition            import aq_inner, aq_parent


from Products.CMFCore       import permissions
from Products.CMFCore.utils import getToolByName




from PloneElement_TraversalConfig                    import cPloneTypes

from ModelDDvlPloneTool_Profiling                    import ModelDDvlPloneTool_Profiling
from ModelDDvlPloneTool_Retrieval_Permissions        import ModelDDvlPloneTool_Retrieval_Permissions
from ModelDDvlPloneTool_Retrieval_Utils              import ModelDDvlPloneTool_Retrieval_Utils
from ModelDDvlPloneTool_Retrieval_Candidates         import ModelDDvlPloneTool_Retrieval_Candidates
from ModelDDvlPloneTool_Retrieval_I18N               import ModelDDvlPloneTool_Retrieval_I18N
from ModelDDvlPloneTool_Retrieval_TraversalConfigs   import ModelDDvlPloneTool_Retrieval_TraversalConfigs
from ModelDDvlPloneTool_Retrieval_Impact             import ModelDDvlPloneTool_Retrieval_Impact
from ModelDDvlPloneTool_Retrieval_PloneContent       import ModelDDvlPloneTool_Retrieval_PloneContent

from ModelDDvlPloneToolSupport import fSecondsNow



cKnownWritePermissionTargets = [ 'object', 'add', 'add_collection', 'delete', 'attrs', 'aggregations', 'relations', 'plone', 'delete_plone', ]
cKnownFeatureFilterKeys      = [ 'objectValues', 'types', 'attrs', 'aggregations', 'relations', 'relations_without_element_details', 'candidates_for_relations', 'do_not_recurse_collections']
                               #  objectValues retrieves all objectValues in a traversalResult with a predefined traversal spec
cKnownInstanceFilterKeys     = [ 'UIDs', ]
cKnownRetrievalExtents       = [ 'traversals', 'tree',  'owner', 'cursor', 'relation_cursors', 'dynamic_vocabularies', 'audit', 'audit_all', 'change_entries', 'change_entries_summaries', 'change_entries_summaries_fields_values', 'extra_links', 'num_contained',] # ACV 20090920 Removed 'plone_objects',
cKnownAdditionalParams       = [ 'Do_Not_Translate', 'Retrieve_Minimal_Related_Results', 'ChangesAfter', 'DoNotForbidDeletionFor_Aggregations_ReadOnly']

cAuditFieldKeys = [
    'creation_date',      
    'creation_user',      
    'modification_date',  
    'modification_user',  
    'deletion_date',      
    'deletion_user',      
    'is_inactive',          
    'change_counter',     
]

cChangeLogFieldKey  = 'change_log'
cChangeLogFieldNameField = 'change_log_field'

cBasicInfoAttributeConfigs = [
    { 'name': 'title',             'type': 'String',     'kind': 'Data',  }, 
    { 'name': 'description',       'type': 'Text',       'kind': 'Data', 'optional':  True, }, 
]







class ModelDDvlPloneTool_Retrieval(
    ModelDDvlPloneTool_Profiling,
    ModelDDvlPloneTool_Retrieval_Permissions, 
    ModelDDvlPloneTool_Retrieval_Utils, 
    ModelDDvlPloneTool_Retrieval_Candidates, 
#    ModelDDvlPloneTool_Retrieval_Derivation,
    ModelDDvlPloneTool_Retrieval_I18N, 
    ModelDDvlPloneTool_Retrieval_TraversalConfigs,
    ModelDDvlPloneTool_Retrieval_Impact,
    ModelDDvlPloneTool_Retrieval_PloneContent):
    """
    """
    security = ClassSecurityInfo()

    
    security.declarePrivate('fNewVoidElementResult')
    def fNewVoidElementResult(self):
        """Inter-layer contract: Element retrieval Result structure.
        
        """
        unResult = { 
            # ACV 200906110258 added portal_url to have all icons and images to reference same url to allow effective caching
            'is_supported':             False,
            'portal_url':               '',
            'portal_object':            '',
            'object':                   None,                           
            'meta_type':                '',     
            'portal_type':              '',
            'archetype_name':           '',
            'UID':                      '',    
            'url':                      '',                 
            'title':                    '',                   
            'path':                     '',    
            'root_url':                 '',
            'root_path':                '',
            'root_title':               '',
            'is_root_supported':        '',
            'owner_url':                '',
            'owner_path':               '',
            'owner_title':              '',
            'is_collection':            False,          
            'is_root':                  False, 
            'content_icon':             '',
            'type_config':              None,                                 
            'type_translations':        None,                                 
            'non_text_field_names':     [ ],                                  
            'text_field_names':         [ ],                                  
            'field_names':              [ ],                                  
            'values_by_name':           { },                                  
            'values':                   [ ],                                  
            'traversal_names':          [ ],                                  
            'traversals_by_name':       { },                                  
            'traversals':               [ ],                                  
            'cursor':                   None,                                 
            'owner_element':            None,                               
            'container_element':        None, 
            'read_permission':          False,                                
            'traverse_permission':      False,
            'write_permission':         False,
            'add_permission':           False,
            'add_collection_permission': False,
            'delete_permission':        False,
            'factory_methods':          None,
            
            # Dynamic factory enablers
            'factory_enablers':         None,

            # Dynamic actions allowed
            'is_copyable':              False,
            'allow_paste':              True,
            'allow_import':             True,
            'allow_export':             True,
            'allow_read':               None,
            'allow_write':              None,
            'allow_edit_id':            None,
            'allow_version':            None,
            'allow_translation':        None,
            
            # Audit field names
            'creation_date_field':      '',
            'creation_user_field':      '',
            'modification_date_field':  '',
            'modification_user_field':  '',
            'deletion_date_field':      '',
            'deletion_user_field':      '',
            'is_inactive_field':          '',
            'change_counter_field':     '',
            'change_log_field':         '',

            # Audit fields values
            'creation_date':            None,
            'creation_user':            '',
            'modification_date':        None,
            'modification_user':        '',
            'deletion_date':            None,
            'deletion_user':            '',
            'is_inactive':              False,
            'change_counter':           0,
            'change_entries':           None,
            'change_entries_summaries':     None,
            'change_entries_after':         None,
            'change_entries_after_summaries': '',
            
            # Versioning and Translation field namess
            'inter_version_field':      '',
            'version_field':            '',
            'version_storage_field':    '',
            'version_comment_field':    '',
            'version_comment_storage_field':'',
            'language_field':           '',
            'fields_pending_translation_field': '',
            'fields_pending_revision_field':'',
            
            # Traceability field names
            'inter_translation_field':  '',
            'versioning_link_fields':   '',
            'translation_link_fields':  '',
            'usage_link_fields':        '',
            'derivation_link_fields':   '',
            'propagate_delete_impact_to':'',
            
            # Presentation dynamics and customizaton
            'extra_links':              '',
            
            
            
            
            
# ACV 20090921 Removed
#           'plone_objects':            [ ],
        }
        return unResult   
    

    
    
    
    
    security.declarePrivate('fNewVoidValueResult')
    def fNewVoidValueResult(self):
        """Inter-layer contract: Attribute retrieval Result structure.
        
        """
        unResult = { 
            'attribute_name':           '', 
            'type':                     '', 
            'computed':                 False,
            'attribute_config':         None,
            'attribute_translations':   { },
            'vocabulary':               None,
            'raw_value':                None, 
            'value':                    None, 
            'uvalue':                   None, 
            'translated_value':         None,
            'vocabulary_translations':  None,
            'attribute_config':         None,
            'read_permission':          False,
            'write_permission':         False,
            'sub_values':               [ ],
            'sub_values_by_name':       { },            
            'computed':              False,
        }
        return unResult   
   
    
    
    
    security.declarePrivate('fNewVoidTraversalResult')
    def fNewVoidTraversalResult(self):
        """Inter-layer contract: Traversal retrieval Result structure.
        
        """
        unResult = { 
            'traversal_kind' :          '', 
            'traversal_name' :          '', 
            'contains_collections' :    False, 
            'has_grandchildren':        False,
            'num_grandchildren':        0,
            'is_multivalued' :          False, 
            'relationship':             '',
            'inverse_relationship':     '',
            'traversal_config':         None, 
            'num_elements':             0,
            'dependency_supplier':      False,
            'elements':                 [ ], 
            'traversal_translations' :  { },
            'factories' :               [ ],
            'column_names':             [ ],
            'column_translations':      { },
            'read_permission':          False,
            'write_permission':         False,
            'max_multiplicity_reached': False,
            'multiplicity_higher':      -1,
            'candidates':               [ ],
            'elements_by_UID':          { },
            'elements_by_id':           { },
            'factory_views':            None,
            'computed':                 False,
            'related_types_and_icons':  [ ],
        }
        return unResult   
   
    

    

    
    security.declarePrivate('fNewVoidCursorResult')
    def fNewVoidCursorResult(self):
        """Inter-layer contract: Cursor retrieval Result structure, with entries for first, last, previous, next results of sibling elements.
        
        """
        unResult = {
            'object':               None,
            'meta_type':            '',
            'owner_element':        None,
            'elements_count':       0,
            'element_index':        -1,
            'first_element':        None,
            'last_element':         None,
            'previous_element':     None,
            'next_element':         None,
            'traversal_name':       '',
            'traversal_result':     None,
            'siblings':             [ ],
        }
        return unResult   
    


    security.declarePrivate('fNewVoidFactoryResult')
    def fNewVoidFactoryResult(self):
        """Inter-layer contract: Factory specification Result structure for aggregation traversal results.
        
        """
        unResult = { 
            'meta_type':            '', 
            'type_translations':    [], 
            'content_icon':         '',
            'archetype_name':       '',
            'portal_type':          '',
            'factory_view':         '',
        }                
        return unResult
    
    
    
    
    security.declarePrivate('fPortalRoot')
    def fPortalRoot(self, theContextualObject=None):
        
        unContextualObject = theContextualObject
        if unContextualObject == None:
            unContextualObject = self
             
        aPortalTool = getToolByName( unContextualObject, 'portal_url', None)
        if aPortalTool == None:
            return None
        
        unPortal = aPortalTool.getPortalObject()
        return unPortal       
        

    
    
    security.declarePrivate('fPortalURL')
    def fPortalURL(self, theContextualObject=None):
        
        unContextualObject = theContextualObject
        if unContextualObject == None:
            unContextualObject = self

        unPortalURLTool = getToolByName( unContextualObject, 'portal_url', None)
        if not unPortalURLTool:
            return ''
        
        unPortalURL = ''
        try:
            unPortalURL = unPortalURLTool()
        except: 
            None
        if not unPortalURL:
            return ''
        
        return unPortalURL
    
   
    
    
    security.declarePrivate(   'fUniqueStringWithCounter')
    def fUniqueStringWithCounter( self, theInitialString, theExistingStrings, thePloneToolForNormalizeString=None):
        if not theInitialString:
            return ''
        
        unInitialString = theInitialString
        
        if thePloneToolForNormalizeString:
            unInitialString = thePloneToolForNormalizeString.normalizeString( unInitialString)
            
        if not theExistingStrings:
            return unInitialString
        
        if not ( unInitialString in theExistingStrings):
            return unInitialString
        
        unaStringWONumbers = unInitialString
        unaLastChar = unaStringWONumbers[-1:]
        
        while ( unaLastChar >= '0' and unaLastChar <= '9'):
            unaStringWONumbers = unaStringWONumbers[:-1]
            unaLastChar = unaStringWONumbers[-1:]
        while ( unaLastChar in [ '-', '_',]):
            unaStringWONumbers = unaStringWONumbers[:-1]
            unaLastChar = unaStringWONumbers[-1:]
        
        unCounter = 1
        unNewTargetString = '%s-%d' % ( unaStringWONumbers, unCounter, )
        if thePloneToolForNormalizeString:
            unNewTargetString = thePloneToolForNormalizeString.normalizeString( unNewTargetString)
        
        while unNewTargetString in theExistingStrings:
            unCounter += 1
            unNewTargetString = '%s-%d' % ( unaStringWONumbers, unCounter, )
            if thePloneToolForNormalizeString:
                unNewTargetString = thePloneToolForNormalizeString.normalizeString( unNewTargetString)
                
        return  unNewTargetString 
            

        
    
    security.declarePrivate( 'fClipboardCookieElements')
    def fClipboardCookieElements( self, theRequest, theContextualElement):
        
        if not theRequest:
            return []
        
        if not theRequest.has_key('__cp'):
            return []

        aClipboardContents = theRequest['__cp']
        
        unaOperation     = None
        unosMonikerDatas = None
        try:
            unaOperation, unosMonikerDatas = loads( decompress( unquote( aClipboardContents))) # _cb_decode(cp)
        except:
            None
            
        unosElementos = [ ]
    
        unaApplication = theContextualElement.getPhysicalRoot()
        
        for unMonikerData in unosMonikerDatas:
            unMoniker = Moniker.loadMoniker( unMonikerData)
            unElement = None
            try:
                unElement = unMoniker.bind( unaApplication)
            except:
                None
            if not ( unElement == None):
                unosElementos.append( unElement)
        # End of code copied from class CopyContainer
                    
        return unosElementos
        
    
###############   
###############   T   Y  P   E
###############       
    
    
   

    
    security.declarePrivate('fRetrieveTypeConfigByUID')
    def fRetrieveTypeConfigByUID(self, 
        theTimeProfilingResults     =None,
        theContextualElement        =None, 
        theUID                      =None, 
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='', 
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):
        """Retrieval of element results, for an element given its UID (unique identifier in the scope of the Plone site).
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveTypeConfigByUID', theTimeProfilingResults)
                      
        try:
            unElemento = self.fElementoPorUID( theUID, theContextualElement)
            if ( unElemento == None):
                return None
            
            unResult = self.fRetrieveTypeConfig(
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =unElemento, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =theTypeConfig, 
                theAllTypeConfigs           =theAllTypeConfigs, 
                theViewName                 =theViewName, 
                theRetrievalExtents         =theRetrievalExtents,
                theWritePermissions         =theWritePermissions,
                theFeatureFilters           =theFeatureFilters, 
                theInstanceFilters          =theInstanceFilters,
                theTranslationsCaches       =theTranslationsCaches,
                theCheckedPermissionsCache  =theCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams
            )
            return unResult
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveTypeConfigByUID', theTimeProfilingResults)
            
    

            

    
    security.declarePrivate('fRetrieveTypeConfig')
    def fRetrieveTypeConfig(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theParent                   =None,
        theParentTraversalName      ='',
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='', 
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):
        """Retrieval of an element result, for a given element.
        
        """


        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveTypeConfig', theTimeProfilingResults)
                      
        try:
            if ( theElement == None):
                return None

            unTranslationsCaches        = theTranslationsCaches
            if not unTranslationsCaches:
                unTranslationsCaches = self.fCreateTranslationsCaches()
                
            unCheckedPermissionsCache   = theCheckedPermissionsCache
            if ( unCheckedPermissionsCache == None):
                unCheckedPermissionsCache = self.fCreateCheckedPermissionsCache()
                
                
            unResult = self.fNewResultForElement( theElement)
            
            unWritePermissions = []
            if theWritePermissions:
                for aWritePermission in theWritePermissions:
                    if aWritePermission in self.fKnownWritePermissionTargets():
                        unWritePermissions.append( aWritePermission)    

            unFeatureFilters = {}
            if theFeatureFilters:
                for aFeatureFilterKey in theFeatureFilters.keys():
                    if aFeatureFilterKey in self.fKnownFeatureFilterKeys():
                        unFeatureFilters[ aFeatureFilterKey] =  theFeatureFilters[ aFeatureFilterKey]  
                        
            unInstanceFilters = {}
            if theInstanceFilters:
                for aInstanceFilterKey in theInstanceFilters.keys():
                    if aInstanceFilterKey in self.fKnownInstanceFilterKeys():
                        unInstanceFilters[ aInstanceFilterKey] =  theInstanceFilters[ aInstanceFilterKey]  
                        
            unRetrievalExtents = []
            if theRetrievalExtents:
                for aRetrievalExtent in theRetrievalExtents:
                    if aRetrievalExtent in self.fKnownRetrievalExtents():
                        unRetrievalExtents.append( aRetrievalExtent)    
                        
            unNoLogRetrievalExtents = unRetrievalExtents[:]
            if 'change_entries' in unNoLogRetrievalExtents:
                unNoLogRetrievalExtents.remove( 'change_entries')
            if 'change_entries_summaries' in unNoLogRetrievalExtents:
                unNoLogRetrievalExtents.remove( 'change_entries_summaries')
            if 'change_entries_summaries_fields_values' in unNoLogRetrievalExtents:
                unNoLogRetrievalExtents.remove( 'change_entries_summaries_fields_values')
            if ( 'audit' in unNoLogRetrievalExtents) and not ( ( 'audit_all' in unNoLogRetrievalExtents)):
                unNoLogRetrievalExtents.remove( 'audit')
               
                                        
            unAllTypeConfigs = theAllTypeConfigs
            if not unAllTypeConfigs:
                unAllTypeConfigs = self.getAllTypeConfigs( theElement)
                if not (theAllTypeConfigs == None):
                    theAllTypeConfigs.update( unAllTypeConfigs)  

    
            if ( 'owner' in unRetrievalExtents) or ( 'cursor' in unRetrievalExtents):
                if theElement.getEsRaiz():
                    unResult[ 'owner_element']      = unResult
                    unResult[ 'container_element']  = unResult
                
                else:
                    otroWritePermissions = unWritePermissions[:]
                    if not ('object' in otroWritePermissions):
                        otroWritePermissions.append( 'object')
                     

                        
                    unPropietario = theElement.getPropietario()
                    if not ( unPropietario == None):
                        unPropietarioResult = self.fRetrieveElementoBasicInfoAndTranslations( 
                            theTimeProfilingResults     =theTimeProfilingResults,
                            theElement                  =unPropietario,      
                            theRetrievalExtents         =unNoLogRetrievalExtents,
                            theTranslationsCaches       =unTranslationsCaches,       
                            theCheckedPermissionsCache  =unCheckedPermissionsCache,
                            theResult                   =None,
                            theParentTraversalResult    =None,
                            theWritePermissions         =otroWritePermissions,     
                            theAdditionalParams         =theAdditionalParams     
                        )    
                        if unPropietarioResult:
                            unResult[ 'owner_element'] = unPropietarioResult
        
                    unContenedor = theElement.getContenedor()
                    if not ( unContenedor == None):
                        if ( not( unPropietario == None)) and ( unContenedor == unPropietario):
                            unContenedorResult = unPropietarioResult
                        else:
                            unContenedorResult = self.fRetrieveElementoBasicInfoAndTranslations( 
                                theTimeProfilingResults     =theTimeProfilingResults,
                                theElement                  =unContenedor,             
                                theRetrievalExtents         =unNoLogRetrievalExtents,
                                theTranslationsCaches       =unTranslationsCaches,       
                                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                                theResult                   =None,
                                theParentTraversalResult    =None,
                                theWritePermissions         =otroWritePermissions,
                                theAdditionalParams         =theAdditionalParams     
                            )    
                        if unContenedorResult:
                            unResult[ 'container_element'] = unContenedorResult
    
           
            if  'cursor' in unRetrievalExtents:
                unCursorResult = self.fRetrieveAggregationCursorInfoAndTranslations( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =theElement,
                    theViewName                 =theViewName,
                    theAllTypeConfigs           =unAllTypeConfigs,
                    theTranslationsCaches       =unTranslationsCaches,
                    theCheckedPermissionsCache  =unCheckedPermissionsCache,
                    theWritePermissions         =unWritePermissions,
                    theAdditionalParams         =theAdditionalParams,
                )
                if unCursorResult:
                    unResult[ 'cursor'] = unCursorResult
                    
            
            otroRetrievalExtents = unRetrievalExtents[:]
            if  'owner' in otroRetrievalExtents:
                otroRetrievalExtents.remove( 'owner')            
            if  'cursor' in otroRetrievalExtents:
                otroRetrievalExtents.remove( 'cursor')
                
    
            unResult = self.fRetrieveTypeConfig_recursive( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theResult                   =unResult, 
                theElement                  =theElement, 
                theParent                   =theParent,
                theParentTraversalName      =theParentTraversalName,
                theCanReturnValues          =True, 
                theViewName                 =theViewName,
                theRetrievalExtents         =otroRetrievalExtents, 
                theTypeConfig               =theTypeConfig, 
                theAllTypeConfigs           =unAllTypeConfigs, 
                theParentTraversalResult    =None, 
                theTranslationsCaches       =unTranslationsCaches, 
                theCheckedPermissionsCache  =unCheckedPermissionsCache, 
                theWritePermissions         =unWritePermissions, 
                theFeatureFilters           =unFeatureFilters,
                theInstanceFilters          =unInstanceFilters,
                theAdditionalParams         =theAdditionalParams 
            )
            
            return unResult
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveTypeConfig', theTimeProfilingResults)
            
    
    
    


    
    



###############   
###############   T   Y  P   E         R   E   C   U   R   S   I   V   E
###############   
       
    
    security.declarePrivate('fRetrieveTypeConfig_recursive')
    def fRetrieveTypeConfig_recursive(self,
        theTimeProfilingResults     =None,
        theResult                   =None, 
        theElement                  =None, 
        theParent                   =None,
        theParentTraversalName      =None,
        theCanReturnValues          =True, 
        theViewName                 ='',
        theRetrievalExtents         =None, 
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theParentTraversalResult    =None, 
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None, 
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theAdditionalParams         =None):
        """Retrieval of an element result, for a given element, and recursively its contained elements.
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveTypeConfig_recursive', theTimeProfilingResults)

        try:

            if ( theElement == None):
                return None
         
            unResult = theResult
            if not unResult:
                unResult = self.fNewResultForElement( theElement)
                        
            unDummy = self.fRetrieveElementoBasicInfoAndTranslations( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theElement, 
                theRetrievalExtents         =theRetrievalExtents,
                theTranslationsCaches       =theTranslationsCaches, 
                theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                theResult                   =unResult,
                theParentTraversalResult    =theParentTraversalResult,
                theWritePermissions         =theWritePermissions,
                theAdditionalParams         =theAdditionalParams,
            )
    
            unNoLogRetrievalExtents = theRetrievalExtents[:]
            if 'change_entries' in unNoLogRetrievalExtents:
                unNoLogRetrievalExtents.remove( 'change_entries')
            if 'change_entries_summaries' in unNoLogRetrievalExtents:
                unNoLogRetrievalExtents.remove( 'change_entries_summaries')
            if 'change_entries_summaries_fields_values' in unNoLogRetrievalExtents:
                unNoLogRetrievalExtents.remove( 'change_entries_summaries_fields_values')
                
                
            if ( 'audit' in unNoLogRetrievalExtents) and not ( ( 'audit_all' in unNoLogRetrievalExtents)):
                unNoLogRetrievalExtents.remove( 'audit')

            unCanReturnValues       = unResult[ 'read_permission']
            unCanReturnTraversals   = unCanReturnValues and unResult[ 'traverse_permission']
             
            unTypeConfig = theTypeConfig
            if unTypeConfig:
                if unTypeConfig.has_key( 'reuse_config'):
                    unConfigName = unTypeConfig.get( 'reuse_config', '')
                    unTypeConfig =      self.getTypeConfig( theElement, theElement.meta_type, theAllTypeConfigs, unConfigName)
                    if not unTypeConfig:
                        unTypeConfig =  self.getTypeConfig( theElement, theElement.meta_type, theAllTypeConfigs)
            else:
                unTypeConfig =          self.getTypeConfig( theElement, theElement.meta_type, theAllTypeConfigs)                    
            if not unTypeConfig:
                return None
            unResult[ 'type_config']  =  unTypeConfig 
            
                                
    
            if unTypeConfig.has_key( 'attrs'):
                someAttributeConfigs =  unTypeConfig.get( 'attrs', [])
                if someAttributeConfigs:
                    self.pRetrieveAttributeConfigs( 
                        theTimeProfilingResults     =theTimeProfilingResults,
                        theElement                  =theElement, 
                        theCanReturnValues          =unCanReturnValues,
                        theViewName                 =theViewName,
                        theRetrievalExtents         =unNoLogRetrievalExtents,
                        theTypeConfig               =unTypeConfig, 
                        theAllTypeConfigs           =theAllTypeConfigs, 
                        theAttributeConfigs         =someAttributeConfigs, 
                        theTranslationsCaches       =theTranslationsCaches, 
                        theResult                   =unResult, 
                        theParentTraversalResult    =theParentTraversalResult, 
                        theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                        theWritePermissions         =theWritePermissions,
                        theFeatureFilters           =theFeatureFilters,
                        theInstanceFilters          =theInstanceFilters,
                        theAdditionalParams         =theAdditionalParams
                   ) 
            
                    
            if theFeatureFilters.get( 'objectValues', False):
                
                if unResult.has_key( 'traversals'):
                    someTraversalResults = unResult[ 'traversals']
                else:
                    someTraversalResults = [ ]
                    unResult[ 'traversals'] = someTraversalResults
                
                unTraversalResult= self.fRetrieveTraversalConfig_ObjectValues( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theTraversedObjectResult    =unResult,
                    theElement                  =theElement, 
                    theCanReturnValues          =unCanReturnValues,
                    theViewName                 =theViewName,
                    theRetrievalExtents         =unNoLogRetrievalExtents,
                    theTypeConfig               =unTypeConfig, 
                    theAllTypeConfigs           =theAllTypeConfigs, 
                    theTranslationsCaches       =theTranslationsCaches, 
                    theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                    theWritePermissions         =theWritePermissions, 
                    theFeatureFilters           =theFeatureFilters, 
                    theInstanceFilters          =theInstanceFilters,
                    theAdditionalParams         =theAdditionalParams
                )
                
                if unTraversalResult:
                    someTraversalResults.append( unTraversalResult)
                    
                    if ('delete' in theWritePermissions) and theResult.get( 'delete_permission', False):
                        unosElementResults = unTraversalResult.get( 'elements', [])
                        for unElementResult in unosElementResults:
                            if unElementResult and ( not unElementResult.get( 'object', None) == None):
                                if not unElementResult.get( 'delete_permission', False): 
                                    theResult[ 'delete_permission']  =  False   
                                    break
                    
                    
            if unNoLogRetrievalExtents and ( ( 'traversals' in unNoLogRetrievalExtents) or ( 'tree' in unNoLogRetrievalExtents)):
                
                     
                    
                    
                if unTypeConfig.has_key( 'traversals'):
                    someTraversalConfigs =  unTypeConfig.get( 'traversals', [])
                    if someTraversalConfigs:
                        if theRetrievalExtents:
                            unosRetrievalExtents = unNoLogRetrievalExtents[:]
                        else:
                            unosRetrievalExtents = []
                        if ( 'traversals' in unosRetrievalExtents):
                            unosRetrievalExtents.remove( 'traversals')
                            
                        self.pRetrieveTraversalConfigs( 
                            theTimeProfilingResults     =theTimeProfilingResults, 
                            theElement                  =theElement, 
                            theCanReturnValues          =unCanReturnTraversals, 
                            theViewName                 =theViewName,
                            theRetrievalExtents         =unosRetrievalExtents,
                            theTypeConfig               =unTypeConfig, 
                            theAllTypeConfigs           =theAllTypeConfigs, 
                            theTraversalConfigs         =someTraversalConfigs, 
                            theTranslationsCaches       =theTranslationsCaches, 
                            theResult                   =unResult,
                            theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                            theWritePermissions         =theWritePermissions, 
                            theFeatureFilters           =theFeatureFilters, 
                            theInstanceFilters          =theInstanceFilters,
                            theAdditionalParams         =theAdditionalParams
                        )
                    
                        
            #if theRetrievalExtents and ( 'plone_objects' in theRetrievalExtents):

                #unosResultPloneObjects = unResult.get( 'plone_objects', None)
                #if unosResultPloneObjects == None:
                    #unosResultPloneObjects = [ ]
                    #unResult[ 'plone_objects'] = unosResultPloneObjects
                
                #somePloneObjects = self.fRetrievePloneObjects( 
                    #theTimeProfilingResults     =theTimeProfilingResults, 
                    #theElement                  =theElement, 
                    #theTypeNames                =None,
                    #theCanReturnValues          =unCanReturnValues, 
                    #theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                    #theFeatureFilters           =theFeatureFilters, 
                    #theInstanceFilters          =theInstanceFilters,
                    #theAdditionalParams         =theAdditionalParams
                #)
                
                #if somePloneObjects:
                    #unosResultPloneObjects.extend( somePloneObjects)
                    
            return unResult

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveTypeConfig_recursive', theTimeProfilingResults)
    
    
    
    
    



###############   
###############   A   T   T   R   I   B   U   T   E   S
###############   
 
    
    security.declarePrivate('pRetrieveAttributeConfigs')
    def pRetrieveAttributeConfigs(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theCanReturnValues          =True,
        theViewName                 ='',
        theRetrievalExtents         =None,
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theAttributeConfigs         =None, 
        theTranslationsCaches       =None, 
        theResult                   =None, 
        theParentTraversalResult    =None, 
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None,
        theFeatureFilters           =None,
        theInstanceFilters          =None,
        theAdditionalParams         =None):
        """Retrieval of the attribute results for an element.
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'pRetrieveAttributeConfigs', theTimeProfilingResults)

        try:

            if ( theElement == None) or not theAttributeConfigs or (theResult == None):
                return self
    
            if theResult.has_key( 'text_field_names'):
                someResultTextFieldNames = theResult[ 'text_field_names']
            else:
                someResultTextFieldNames = [ ]
                theResult[ 'text_field_names'] = someResultTextFieldNames
     
            if theResult.has_key( 'non_text_field_names'):
                someResultNonTextFieldNames = theResult[ 'non_text_field_names']
            else:
                someResultNonTextFieldNames = [ ]
                theResult[ 'non_text_field_names'] = someResultNonTextFieldNames
     
            if theResult.has_key( 'field_names'):
                someResultFieldNames = theResult[ 'field_names']
            else:
                someResultFieldNames = [ ]
                theResult[ 'field_names'] = someResultFieldNames
    
               
            if theResult.has_key( 'values'):
                someResultValues = theResult[ 'values']
            else:
                someResultValues = [ ]
                theResult[ 'values'] = someResultValues
                
            someAlreadyRetrievedAttributeNames = set()
            for aResultValue in someResultValues:
                anAttributeName = aResultValue.get( 'attribute_name', '')
                if anAttributeName:
                    someAlreadyRetrievedAttributeNames.add( anAttributeName)
                
    
            # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
            #if theResult.has_key( 'values_by_name'):
                #aResultValuesByNameDict = theResult[ 'values_by_name']
            #else:
                #aResultValuesByNameDict = { }
                #theResult[ 'values_by_name'] = aResultValuesByNameDict
                            
            someFilteredAttributeNames = [ anAttributeConfig[ 'name'] for anAttributeConfig in theAttributeConfigs]
            if theFeatureFilters and theFeatureFilters.has_key( 'attrs'):
                unosFiltrosNombresAttributes = theFeatureFilters.get( 'attrs', None)        
                if not ( unosFiltrosNombresAttributes == None):
                    someFilteredAttributeNames = [ anAttributeName for anAttributeName in someFilteredAttributeNames if anAttributeName in unosFiltrosNombresAttributes]
            
            if not theViewName:
                someNotExcludedFieldNames = someFilteredAttributeNames
            else:    
                someNotExcludedFieldNames =  []
                for unAttributeConfig in theAttributeConfigs:
                    unAttributeName     = unAttributeConfig[ 'name']
                    if ( unAttributeName in someFilteredAttributeNames) :
                        unExcludeFromViews  = unAttributeConfig.get( 'exclude_from_views', [])
                        if( not unExcludeFromViews or not ( theViewName in unExcludeFromViews)):               
                            someNotExcludedFieldNames.append( unAttributeName)
    
            someFieldsAndConfigsToRetrieve = [ ]
            someFieldNames       = [ ]
            for unAttributeConfig in theAttributeConfigs:
                unAttributeName     = unAttributeConfig[ 'name']
                if unAttributeName in someNotExcludedFieldNames:
                    # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                    # was:
                    # if not aResultValuesByNameDict.has_key( unAttributeName) and not ( unAttributeName in someFieldNames):
                    if not ( unAttributeName in someFieldNames) and not ( unAttributeName in someAlreadyRetrievedAttributeNames):
                        unKind          = ''
                        if unAttributeConfig.has_key(  'kind'):
                            unKind = unAttributeConfig[ 'kind']
                        if (not unKind) or (unKind == 'Data'):
                            someFieldsAndConfigsToRetrieve.append( [ unAttributeName, unAttributeConfig, ])
                            someFieldNames.append( unAttributeName)
                                
            # ACV 20090901 Code below was obsolete, but never executed because the dict had description and title
            # now Dict population is postponed until completion of retrieval by services layer
            #if (not aResultValuesByNameDict.has_key( 'description')) and not ( 'description' in someFieldNames):
                #someFieldsToRetrieve= [ [ 'description', None, ], ] + someFieldsToRetrieve
            #if (not aResultValuesByNameDict.has_key( 'title'))       and not ( 'title'       in someFieldNames):
                #someFieldsToRetrieve= [ [ 'title', None, ], ]       + someFieldsToRetrieve
                            
            someValuesResults  = self.fRetrieveValoresYTraduccionesAtributos( 
                theTimeProfilingResults         =theTimeProfilingResults,
                theElement                      =theElement, 
                theCanReturnValues              =theCanReturnValues, 
                theViewName                     =theViewName,
                theRetrievalExtents             =theRetrievalExtents,
                theNamesAndConfigsToRetrieve    =someFieldsAndConfigsToRetrieve, 
                theTranslationsCaches           =theTranslationsCaches, 
                theCheckedPermissionsCache      =theCheckedPermissionsCache, 
                theWritePermissions             =theWritePermissions,
                theFeatureFilters               =theFeatureFilters,
                theInstanceFilters              =theInstanceFilters,
                theAdditionalParams             =theAdditionalParams
            )
             
            for unValueResult in someValuesResults:
                unAttributeName = unValueResult.get('attribute_name', '')
                if unAttributeName:
                    if unValueResult[ 'type'].lower() == 'text':
                        someResultTextFieldNames.append( unAttributeName)
                    else:
                        someResultNonTextFieldNames.append( unAttributeName)
    
                    someResultFieldNames.append( unAttributeName)
                    someResultValues.append( unValueResult)    
    
                    # ACV 20090901 Avoid adding redundant results to dictionaries during service layer processing
                    # the dictionaries will be compiled at the completion of the retrieval
                    # in method pBuildDictResults_Element
                    #
                    # aResultValuesByNameDict[ unAttributeName] = unValueResult 
                                     
            return self
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pRetrieveAttributeConfigs', theTimeProfilingResults)
    


                
                
                
                


###############    
###############   T   R   A   V   E   R   S   A   L   S
###############   


    security.declarePrivate('pRetrieveTraversalConfigs')
    def pRetrieveTraversalConfigs(self,
        theTimeProfilingResults     =None, 
        theElement                  =None, 
        theCanReturnValues          =True, 
        theViewName                 ='',
        theRetrievalExtents         =None,
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theTraversalConfigs         =None, 
        theTranslationsCaches       =None, 
        theResult                   =None,
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None, 
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theAdditionalParams         =None):
        """Retrieval of the traversal results for an element.
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'pRetrieveTraversalConfigs', theTimeProfilingResults)

        try:

            if ( theElement == None) or not theTraversalConfigs or (theResult == None):
                return self
            
            if theResult.has_key( 'traversals'):
                someTraversalResults = theResult[ 'traversals']
            else:
                someTraversalResults = [ ]
                theResult[ 'traversals'] = someTraversalResults
            
            if not theTraversalConfigs:
                return self
            
            
           
            if theResult.has_key( 'traversals_by_name'):
                aResultTraversalsByNameDict = theResult[ 'traversals_by_name']
            else:
                aResultTraversalsByNameDict = { }
                theResult[ 'traversals_by_name'] = aResultTraversalsByNameDict
    
            if theResult.has_key( 'traversal_names'):
                someResultTraversalNames = theResult[ 'traversal_names']
            else:
                someResultTraversalNames = [ ]
                theResult[ 'traversal_names'] = someResultTraversalNames
    
            unosFiltrosNombresAggregations = None
            unosFiltrosNombresRelations    = None
            
            if theFeatureFilters:
                unosFiltrosNombresAggregations = theFeatureFilters.get( 'aggregations', None)
                unosFiltrosNombresRelations    = theFeatureFilters.get( 'relations',    None)
                 
            for unaTraversalConfig in theTraversalConfigs:        
    
                if theViewName:
                    if unaTraversalConfig.has_key( 'exclude_from_views'):
                        unasExcludeFromViews = unaTraversalConfig[ 'exclude_from_views']
                        if unasExcludeFromViews and (theViewName in unasExcludeFromViews):
                            continue
    
                if unaTraversalConfig.has_key( 'aggregation_name'):
                    unaAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
                    
                        
                    if unaAggregationName and (( unosFiltrosNombresAggregations == None) or ( unaAggregationName in unosFiltrosNombresAggregations)):
                        unTraversalResult= self.fRetrieveTraversalConfig_Aggregation( 
                            theTimeProfilingResults     =theTimeProfilingResults,
                            theTraversedObjectResult    =theResult,
                            theElement                  =theElement, 
                            theCanReturnValues          =theCanReturnValues,
                            theViewName                 =theViewName,
                            theRetrievalExtents         =theRetrievalExtents,
                            theTypeConfig               =theTypeConfig, 
                            theAllTypeConfigs           =theAllTypeConfigs, 
                            theTraversalConfig          =unaTraversalConfig, 
                            theTranslationsCaches       =theTranslationsCaches, 
                            theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                            theWritePermissions         =theWritePermissions, 
                            theFeatureFilters           =theFeatureFilters, 
                            theInstanceFilters          =theInstanceFilters,
                            theAdditionalParams         =theAdditionalParams
                        )
                        
                        if unTraversalResult:
                            someTraversalResults.append( unTraversalResult)
                            
                            if ('delete' in theWritePermissions) and theResult.get( 'delete_permission', False):
                                unosElementResults = unTraversalResult.get( 'elements', [])
                                for unElementResult in unosElementResults:
                                    if unElementResult and ( not unElementResult.get( 'object', None) == None):
                                        if not unElementResult.get( 'delete_permission', False): 
                                            theResult[ 'delete_permission']  =  False   
                     
                elif unaTraversalConfig.has_key( 'relation_name'):
                    unaRelationName = unaTraversalConfig.get( 'relation_name', '')
                    if unaRelationName  and (( unosFiltrosNombresRelations == None) or ( unaRelationName in unosFiltrosNombresRelations)):
                        unTraversalResult = self.fRetrieveTraversalConfig_Relation(     
                            theTimeProfilingResults     =theTimeProfilingResults,
                            theTraversedObjectResult    =theResult,
                            theElement                  =theElement, 
                            theCanReturnValues          =theCanReturnValues, 
                            theViewName                 =theViewName,
                            theRetrievalExtents         =theRetrievalExtents,
                            theTypeConfig               =theTypeConfig, 
                            theAllTypeConfigs           =theAllTypeConfigs, 
                            theTraversalConfig          =unaTraversalConfig, 
                            theTranslationsCaches       =theTranslationsCaches, 
                            theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                            theWritePermissions         =theWritePermissions, 
                            theFeatureFilters           =theFeatureFilters, 
                            theInstanceFilters          =theInstanceFilters,
                            theAdditionalParams         =theAdditionalParams
                        )
                        if unTraversalResult:
                            someTraversalResults.append( unTraversalResult)
           
            for unTraversalResult in someTraversalResults:
                unTraversalName = unTraversalResult.get('traversal_name', '')
                if unTraversalName:
                    # ACV 20090901 Avoid adding redundant results to dictionaries during service layer processing
                    # the dictionaries will be compiled at the completion of the retrieval
                    # in method pBuildDictResults_Element
                    #
                    # aResultTraversalsByNameDict[ unTraversalName] = unTraversalResult  
                    
                    if not ( unTraversalName in someResultTraversalNames):
                        someResultTraversalNames.append( unTraversalName)
                   
            return self

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pRetrieveTraversalConfigs', theTimeProfilingResults)
 
 
 
 
 
 
 
 
 
 
###############    
###############   A   G   G   R   E   G   A   T   I  O  N    
###############   

  
   
    security.declarePrivate('fRetrieveTraversalConfig_Aggregation')
    def fRetrieveTraversalConfig_Aggregation(self, 
        theTimeProfilingResults     =None,
        theTraversedObjectResult    =None,
        theElement                  =None, 
        theCanReturnValues          =True,
        theViewName                 ='',
        theRetrievalExtents         =None,
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theTraversalConfig          =None, 
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None, 
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theAdditionalParams         =None):
        """Retrieval of the traversal results for an aggregation in an element.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveTraversalConfig_Aggregation', theTimeProfilingResults)

        try:

            if not theTraversalConfig:
                return {}
            
            
            aFieldName         = theTraversalConfig.get( 'aggregation_name', '') or ''
            if not aFieldName:
                return {}
                
            unContainsCollections = theTraversalConfig.get( 'contains_collections', None)
            if unContainsCollections == None:
                unContainsCollections = True
            else:
                unContainsCollections = ( unContainsCollections == True)
                
    
            unasElementResults = [ ]        
            unTraversalResult = self.fNewVoidTraversalResult()
            unTraversalResult.update( { 
                'traversal_kind' :          'aggregation', 
                'traversal_name' :          aFieldName, 
                'contains_collections' :    unContainsCollections, 
                'is_multivalued' :          True, 
                'traversal_config':         theTraversalConfig, 
                'elements':                 unasElementResults, 
                'max_multiplicity_reached': False,
                'multiplicity_higher':      -1,
            })
                
            unCanReturnValues = theCanReturnValues
            if unCanReturnValues:
                unReadPermission = self.fCheckFieldReadPermission( theElement, aFieldName, [ permissions.View], theCheckedPermissionsCache) == True
                unTraversalResult[ 'read_permission'] = unReadPermission
                unCanReturnValues = unReadPermission
    
                if unCanReturnValues and theTraversedObjectResult[ 'traverse_permission'] and theTraversedObjectResult[ 'write_permission'] and theWritePermissions and ( 'aggregations' in theWritePermissions):
                    unWritePermission = True
                    if theTraversalConfig.get( 'read_only', False) == True:
                        unWritePermission = False   
                    else:
                        unWritePermission = self.fCheckFieldWritePermission( theElement, aFieldName, [ permissions.ModifyPortalContent, ], theCheckedPermissionsCache) == True
                        if unWritePermission:
                            unTraversalResult[ 'write_permission'] = True  
                                
                
                        
            aDummy = self.fAttributeTranslationsFromCache( 
                theElement            = theElement,
                theFieldName          = aFieldName, 
                theTranslationsCaches = theTranslationsCaches,
                theResultDict         = unTraversalResult, 
                theResultKey          = 'traversal_translations',
                theAdditionalParams   = theAdditionalParams,
            )                                         
    
            someSubitems   = theTraversalConfig.get( 'subitems', []) or []
            if not someSubitems:
                return unTraversalResult        
    
            unSchema = theElement.schema
            if not unSchema.has_key( aFieldName):
                return None
                
            unField  = unSchema[ aFieldName]
                
            unosComputedTypes = [ ]                                            
            try:
                unosComputedTypes = unField.computed_types
            except:
                None                                                
            if not unosComputedTypes:
                unosComputedTypes = [ ] 
     
            unMultiplicityHigher = -1                                            
            try:
                unMultiplicityHigher = unField.multiplicity_higher
            except:
                None     
            if unMultiplicityHigher > 0:
                unTraversalResult[ 'multiplicity_higher'] = unMultiplicityHigher     
                
                
            unEsComputed =  unField.type == 'computed'
            unTraversalResult[ 'computed'] = unEsComputed
            
 
            # ACV 20090905 If no columns specified in traversal config, then do not restrict attributes to retrieve
            someColumnNames = theTraversalConfig.get( 'columns', None)     
            unosFeatureFilters = {}
            if not someColumnNames:
                unTraversalResult[ 'column_names'] = []
            else:           
                unTraversalResult[ 'column_names'] = someColumnNames
                if theFeatureFilters:
                    unosFeatureFilters = theFeatureFilters.copy()
                else:
                    unosFeatureFilters = {}
                unosAttrsFilters = unosFeatureFilters.get( 'attrs', None)
                if not unosAttrsFilters:
                    unosFeatureFilters[ 'attrs'] = someColumnNames[:]
                else:
                    for unColumnName in someColumnNames:
                        if not ( unColumnName in unosAttrsFilters):
                            unosAttrsFilters.append( unColumnName)
     
            someElementFactoryNames = []
            
            unosTodosTiposAceptados = []
        
            unNumGrandChildren = 0
            
            unasTodosSubAggregationsTranslations = []
            
            if theRetrievalExtents:
                unRetrievalExtents = theRetrievalExtents[:]
                if 'relation_cursors' in unRetrievalExtents:
                    unRetrievalExtents.remove( 'relation_cursors')
            else:
                unRetrievalExtents = []
                
            unEsColeccion = False
            try:
                unEsColeccion = theElement.getEsColeccion()   
            except:
                None
# ACV OJOJOJOJOJO 200811240748
# Avoid retrieving sibling collection contents when retrieving parent for cursor 
# WAS            unRetrieveTraversals =  (not unEsColeccion) and not ( theTraversalConfig.has_key('contains_collections') and ( theTraversalConfig[ 'contains_collections'] == False)) 
            unRetrieveTraversals =  (not unEsColeccion) and not ( theTraversalConfig.has_key('contains_collections') and ( theTraversalConfig[ 'contains_collections'] == False)) \
                and not(  unContainsCollections and theFeatureFilters.get( 'do_not_recurse_collections', False))
            if unRetrieveTraversals:
                if not ( 'traversals' in unRetrievalExtents):
                    unRetrievalExtents.append( 'traversals')
            else:
                if 'traversals' in unRetrievalExtents:
                    unRetrievalExtents.remove( 'traversals')
                 
                            
            for aSubItems in someSubitems:
    
                unSubitemsTypeConfig = aSubItems
                
                somePortalTypes = aSubItems.get( 'portal_types', []) or []
                
                someAcceptedPortalTypes = somePortalTypes[:]
                if unosComputedTypes:
                    someAcceptedPortalTypes = [ unTypeName for unTypeName in unosComputedTypes if unTypeName in somePortalTypes]
                 
                for unPortalTypeName in someAcceptedPortalTypes:
                    if not unTypeName in unosTodosTiposAceptados:
                        unosTodosTiposAceptados.append( unPortalTypeName)
                            
                someEnabledPortalTypes = [ ]
                
                unosFactoryEnablers = theTraversedObjectResult.get( 'factory_enablers', {})
                if not unosFactoryEnablers:
                    someEnabledPortalTypes = someAcceptedPortalTypes[:]
                    
                else:
                    unosAlreadyCheckedEnablerMethods = { }
                    
                    for unPortalTypeName in someAcceptedPortalTypes:
                        
                        unTypeIsEnabled = True
                        
                        unFactoryEnablerMethodName = ''
                        unFactoryEnablerParameter  = None
                        
                        unFactoryEnablerSpecification = unosFactoryEnablers.get( unPortalTypeName, '')
                        if unFactoryEnablerSpecification:
                            if unFactoryEnablerSpecification.__class__.__name__ in [ 'list', 'tuple', ]:
                                unFactoryEnablerMethodName = unFactoryEnablerSpecification[ 0]
                                unFactoryEnablerParameter  = unFactoryEnablerSpecification[ 1]
                            else:
                                unFactoryEnablerMethodName = unFactoryEnablerSpecification
                                
                        if unFactoryEnablerMethodName:
                            if unosAlreadyCheckedEnablerMethods.has_key( unFactoryEnablerMethodName):
                                unTypeIsEnabled = unosAlreadyCheckedEnablerMethods.get( unFactoryEnablerMethodName, True)
                            
                            else:
                                unFactoryEnablerMethod = None
                                try:
                                    unFactoryEnablerMethod = theElement[ unFactoryEnablerMethodName]
                                except:
                                    None
                                if unFactoryEnablerMethod:

                                    if not ( unFactoryEnablerParameter == None):
                                        try:
                                            unTypeIsEnabled = unFactoryEnablerMethod( unPortalTypeName, unFactoryEnablerParameter)
                                        except:
                                            None
                                    else:
                                        try:
                                            unTypeIsEnabled = unFactoryEnablerMethod( unPortalTypeName)
                                        except:
                                            None
                                    unosAlreadyCheckedEnablerMethods[ unFactoryEnablerMethodName] = unTypeIsEnabled
                                    
                        if unTypeIsEnabled:
                            someEnabledPortalTypes.append( unPortalTypeName)    
                        
                    
                    
                for unPortalTypeName in someEnabledPortalTypes:
                    if not ( unPortalTypeName in someElementFactoryNames): 
                        someElementFactoryNames.append( unPortalTypeName)
                  
                if unSubitemsTypeConfig and someAcceptedPortalTypes:
                    if unCanReturnValues:
                        someElements = theElement.objectValues( someAcceptedPortalTypes)
    
                        if someElements:
                            for unElemento in someElements:
                                unElementResult = self.fRetrieveTypeConfig_recursive( 
                                    theTimeProfilingResults     =theTimeProfilingResults,
                                    theResult                   =None, 
                                    theElement                  =unElemento, 
                                    theParent                   =theElement,
                                    theParentTraversalName      =aFieldName,
                                    theCanReturnValues          =unCanReturnValues, 
                                    theViewName                 =theViewName,
                                    theRetrievalExtents         =unRetrievalExtents, 
                                    theTypeConfig               =unSubitemsTypeConfig, 
                                    theAllTypeConfigs           =theAllTypeConfigs, 
                                    theParentTraversalResult    =unTraversalResult, 
                                    theTranslationsCaches       =theTranslationsCaches, 
                                    theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                                    theWritePermissions         =theWritePermissions, 
                                    theFeatureFilters           =unosFeatureFilters, 
                                    theInstanceFilters          =theInstanceFilters,
                                    theAdditionalParams         =theAdditionalParams
                                )
                                if unElementResult and unElementResult[ 'read_permission']:
                                    unasElementResults.append( unElementResult)
                                    # ACV 20090901 Removed to avoid producing huge traversal result dumps
                                    # because each element result is included 3 times (in the ordered collection, and the two dicts)
                                    # which is compounded when traversing a tree
                                    # ACV 20090901 Avoid adding redundant results to dictionaries during service layer processing
                                    # the dictionaries will be compiled at the completion of the retrieval
                                    # in method pBuildDictResults_Element
                                    #
                                    #unTraversalResult[ 'elements_by_UID'][ unElementResult[ 'UID']] = unElementResult
                                    #unTraversalResult[ 'elements_by_id' ][ unElementResult[ 'id' ]] = unElementResult
                                    
                                    if unContainsCollections:
                                        someAggegationSubTraversals = []
                                        for unTraversalRes in unElementResult[ 'traversals']:
                                            if unTraversalRes[ 'traversal_kind'] == 'aggregation' and unTraversalRes[ 'num_elements'] > 0:
                                                someAggegationSubTraversals.append( unTraversalRes)
                                                unNumGrandChildren += unTraversalRes[ 'num_elements']
                                                
                                        for unTraversalRes in someAggegationSubTraversals:
                                            unTranslatedSubAggregationName = unTraversalRes.get( 'traversal_translations', {}).get( 'translated_label', '')
                                            if unTranslatedSubAggregationName and not ( unTranslatedSubAggregationName in unasTodosSubAggregationsTranslations):
                                                unasTodosSubAggregationsTranslations.append( unTranslatedSubAggregationName)
                    
                    self.pFactoryNamesAndTranslations_into( 
                        theContextElement      = theElement, 
                        theTypeNames           = someElementFactoryNames, 
                        theTranslationsCaches  = theTranslationsCaches, 
                        theResult              = unTraversalResult,
                        theAdditionalParams    = theAdditionalParams,
                    )   
                    if theTraversalConfig.has_key( 'factory_views') and theTraversalConfig[ 'factory_views']:
                        unTraversalResult[ 'factory_views'] = theTraversalConfig[ 'factory_views'].copy()
    
            self.pCompleteColumnTranslations( 
                theTimeProfilingResults= theTimeProfilingResults,
                theContextualElement   = theElement, 
                theTraversalResult     = unTraversalResult, 
                theTypeNames           = unosTodosTiposAceptados, 
                theTranslationsCaches  = theTranslationsCaches,
                theAdditionalParams    = theAdditionalParams,
            )
            
            unTraversalResult[ 'num_elements'] = len( unasElementResults)
            
            if ( unMultiplicityHigher > 0) and ( len( unasElementResults) >= unMultiplicityHigher): 
                unTraversalResult[ 'max_multiplicity_reached'] = True
            else:
                unTraversalResult[ 'max_multiplicity_reached'] = False

            
            if unContainsCollections:
                unTraversalResult[ 'num_grandchildren'] = unNumGrandChildren
                unTraversalResult[ 'has_grandchildren'] = unNumGrandChildren > 0
                
                unTraversalResult[ 'grandchildren_plural_type_translations'] = unasTodosSubAggregationsTranslations
            return unTraversalResult
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveTraversalConfig_Aggregation', theTimeProfilingResults)

 
    
    
    
    
    

  
   
    security.declarePrivate('fRetrieveTraversalConfig_ObjectValues')
    def fRetrieveTraversalConfig_ObjectValues(self, 
        theTimeProfilingResults     =None,
        theTraversedObjectResult    =None,
        theElement                  =None, 
        theCanReturnValues          =True,
        theViewName                 ='',
        theRetrievalExtents         =None,
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None, 
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theAdditionalParams         =None):
        """Retrieval of the traversal results for an aggregation in an element.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveTraversalConfig_ObjectValues', theTimeProfilingResults)

        try:

            unasElementResults = [ ]        
            unTraversalResult = self.fNewVoidTraversalResult()
            unTraversalResult.update( { 
                'traversal_kind' :          'aggregation', 
                'traversal_name' :          'objectValues', 
                'contains_collections' :    False, 
                'is_multivalued' :          True, 
                'elements':                 unasElementResults, 
                'max_multiplicity_reached': False,
                'multiplicity_higher':      -1,
            })

            aTraversalConfig          =self.objectValuesTraversalConfig()
            if not aTraversalConfig:
                return unTraversalResult
            unTraversalResult[ 'traversal_config'] =  aTraversalConfig
            
            if not theCanReturnValues:
                return unTraversalResult
            unTraversalResult[ 'read_permission'] = True
    
            anObjectValuesAttributeTranslationsResult = self.getTranslationsForObjectAttributeFromMsgIds(  
                theElement, 
                'ModelDDvlPlone', 
                'ModelDDvlPlone_objectValues_Label', 
                'Aggregated Elements-', 
                'ModelDDvlPlone_objectValues_Help', 
                'Contents: Elements Aggregated into the current element. When the current element is deleted, these elements, and their contents, recursively, are also deleted.-',
            )
            if not( anObjectValuesAttributeTranslationsResult == None):
                unTraversalResult[ 'traversal_translations'] = anObjectValuesAttributeTranslationsResult
                
            #aDummy = self.fAttributeTranslationsFromCache( 
                #theElement            = theElement,
                #theFieldName          = 'objectValues', 
                #theTranslationsCaches = theTranslationsCaches,
                #theResultDict         = unTraversalResult, 
                #theResultKey          = 'traversal_translations',
                #theAdditionalParams   = theAdditionalParams,
            #)                                         
    
      
             # ACV 20090905 If no columns specified in traversal config, then do not restrict attributes to retrieve
            someColumnNames = aTraversalConfig.get( 'columns', None)     
            unosFeatureFilters = {}
            if not someColumnNames:
                unTraversalResult[ 'column_names'] = []
            else:           
                unTraversalResult[ 'column_names'] = someColumnNames
                if theFeatureFilters:
                    unosFeatureFilters = theFeatureFilters.copy()
                else:
                    unosFeatureFilters = {}
                unosAttrsFilters = unosFeatureFilters.get( 'attrs', None)
                if not unosAttrsFilters:
                    unosFeatureFilters[ 'attrs'] = someColumnNames[:]
                else:
                    for unColumnName in someColumnNames:
                        if not ( unColumnName in unosAttrsFilters):
                            unosAttrsFilters.append( unColumnName)
     
            someElementFactoryNames = []
            
            unasTodosSubAggregationsTranslations = []
            
            unRetrievalExtents = []
            if theRetrievalExtents:
                unRetrievalExtents = theRetrievalExtents[:]
            if 'relation_cursors' in unRetrievalExtents:
                unRetrievalExtents.remove( 'relation_cursors')
            if 'traversals' in unRetrievalExtents:
                unRetrievalExtents.remove( 'traversals')
                
            unEsColeccion = False
            unContainsCollections = False
                 
            unosSubitemsTypeConfigs = aTraversalConfig.get( 'subitems', [])
            if not unosSubitemsTypeConfigs:
                return unTraversalResult
            
            unSubitemsTypeConfig  = unosSubitemsTypeConfigs[ 0]         
            
            someElements = theElement.objectValues( )

            unSetTodosTiposAceptados = set()
            
            if someElements:
                for unElemento in someElements:
                    
                    unElementResult = self.fNewResultForElement( unElemento)
                                
                    unDummy = self.fRetrieveElementoBasicInfoAndTranslations( 
                        theTimeProfilingResults     =theTimeProfilingResults,
                        theElement                  =unElemento, 
                        theRetrievalExtents         =unRetrievalExtents,
                        theTranslationsCaches       =theTranslationsCaches, 
                        theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                        theResult                   =unElementResult,
                        theParentTraversalResult    =unTraversalResult,
                        theWritePermissions         =theWritePermissions,
                        theAdditionalParams         =theAdditionalParams,
                    )
                    if unElementResult and unElementResult[ 'read_permission']:
                        unasElementResults.append( unElementResult)
                        
                        unElementoMetaType = unElemento.meta_type
                        if unElementoMetaType:
                            unSetTodosTiposAceptados.add( unElementoMetaType)
                            
                        if not unElementResult.get( 'type_translations', {}):
                                           
                            unTypeMsgId = ''
                            unArchetypeName = ''
                            unContentIcon = None
                            
                            unTypeParameter = cPloneTypes.get(  unElementoMetaType, {})
                            if unTypeParameter:
                                unTypeMsgId             = unTypeParameter[ 'i18n_msgid']
                                unArchetypeName         = unTypeParameter[ 'archetype_name']
                                unContentIcon           = unTypeParameter[ 'content_icon']
                             
                            if not unArchetypeName:
                                try:
                                    unArchetypeName = unElemento.archetype_name
                                except:
                                    None
                            
                            if not unTypeMsgId:
                                unTypeMsgId = unArchetypeName
                            if not unTypeMsgId:
                                unTypeMsgId = unElementoMetaType
                                
                            if not unContentIcon:
                                try:
                                    unContentIcon = unElemento.content_icon   
                                except:
                                    None
                                if not unContentIcon:
                                    if unArchetypeName:
                                        unContentIcon = '%s_icon.gif' % unArchetypeName.lower()
                                    else:
                                        unIconName = unElementoMetaType
                                        if unIconName.startswith( 'AT'):
                                            unIconName = unIconName[ 2:] 
                                        unContentIcon = '%s_icon.gif' % unIconName.lower()
                            if unContentIcon:
                                unElementResult[ 'content_icon'] = unContentIcon                
                             
                            unTypeTranslations = self.getPloneTypeTranslationResultFromMsgIdMetatypeAndArchetype( unTypeMsgId, unElementoMetaType, unArchetypeName, unElemento)
                            if unTypeTranslations:
                                unElementResult[ 'type_translations'] = unTypeTranslations
                    
                            
            unosTodosTiposAceptados = list ( unSetTodosTiposAceptados)
            self.pCompleteColumnTranslations( 
                theTimeProfilingResults= theTimeProfilingResults,
                theContextualElement   = theElement, 
                theTraversalResult     = unTraversalResult, 
                theTypeNames           = unosTodosTiposAceptados, 
                theTranslationsCaches  = theTranslationsCaches,
                theAdditionalParams    = theAdditionalParams,
            )
            
            unTraversalResult[ 'num_elements'] = len( unasElementResults)
            
            return unTraversalResult
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveTraversalConfig_ObjectValues', theTimeProfilingResults)

 
    
        
    
    
    
###############       
###############   R   E   L   A   T   I  O  N    
###############   
    
    security.declarePrivate('fRetrieveTraversalConfig_Relation')
    def fRetrieveTraversalConfig_Relation(self, 
        theTimeProfilingResults     =None,
        theTraversedObjectResult    =None,
        theElement                  =None, 
        theCanReturnValues          =None, 
        theViewName                 ='',
        theRetrievalExtents         =None,
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theTraversalConfig          =None, 
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None, 
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theAdditionalParams         =None):
        """Retrieval of the traversal results for a relation from an element.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveTraversalConfig_Relation', theTimeProfilingResults)

        try:

            if not theTraversalConfig:
                return {}
            
            unRetrieveMinimalResult = theAdditionalParams and ( theAdditionalParams.get( 'Retrieve_Minimal_Related_Results', False) == True)
            
            aFieldName         = theTraversalConfig.get( 'relation_name', '') or ''
            if not aFieldName:
                return {}
                
            unosElementResults = [ ]        
            unTraversalResult = self.fNewVoidTraversalResult()
            unTraversalResult.update( { 
                'traversal_kind' :          'relation', 
                'traversal_name' :          aFieldName, 
                'is_multivalued' :          False, 
                'traversal_config':         theTraversalConfig, 
                'elements':                 unosElementResults, 
                'num_elements':             0,

            } )
            
    
            unCanReturnValues = theCanReturnValues
            if unCanReturnValues:
                unReadPermission = self.fCheckFieldReadPermission( theElement, aFieldName, [ permissions.View, ], theCheckedPermissionsCache) == True
                unTraversalResult[ 'read_permission'] = unReadPermission
                unCanReturnValues = unReadPermission
        
                if unCanReturnValues and theWritePermissions and  theTraversedObjectResult[ 'traverse_permission'] and theTraversedObjectResult[ 'write_permission'] and theWritePermissions and( 'relations' in theWritePermissions):
                    unWritePermission = True
                    if theTraversalConfig.get( 'read_only', False) == True:
                        unWritePermission = False            
                    if unWritePermission:
                        unWritePermission = self.fCheckFieldWritePermission( theElement, aFieldName, [ permissions.ModifyPortalContent, ], theCheckedPermissionsCache) == True
                    if unWritePermission:
                        unTraversalResult[ 'write_permission'] = unWritePermission     
                                                                           
            unSchema = theElement.schema
            if not unSchema.has_key( aFieldName):
                return {}
                
            unField             = unSchema[ aFieldName]
            if not unField:
                return {}
            
            unRelationship = ''
            try:
                unRelationship = unField.relationship 
            except:
                None
            if unRelationship:
                unTraversalResult[ 'relationship']= unRelationship
                
            unInverseRelationship = ''
            try:
                unInverseRelationship = unField.inverse_relationship 
            except:
                None
            if unInverseRelationship:
                unTraversalResult[ 'inverse_relationship']= unInverseRelationship


            unEsMultiValued = True
            try:
                unEsMultiValued = unField.multiValued 
            except:
                None
            unTraversalResult[ 'is_multivalued']= unEsMultiValued

            unMultiplicityHigher = -1                                            
            try:
                unMultiplicityHigher = unField.multiplicity_higher
            except:
                None     
            if unMultiplicityHigher > 0:
                unTraversalResult[ 'multiplicity_higher'] = unMultiplicityHigher                                           
            
            unEsDependencySupplier =  theTraversalConfig.get( 'dependency', '') == 'Supplier'
            if not unEsDependencySupplier:
                try:
                    unEsDependencySupplier = unField.dependency_supplier == True
                except:
                    None
            unTraversalResult[ 'dependency_supplier'] = unEsDependencySupplier
 
            
            unEsComputed =  unField.type == 'computed'
            unTraversalResult[ 'computed'] = unEsComputed

            
            someColumnNames = theTraversalConfig.get( 'columns', []) or []    
            unTraversalResult[ 'column_names'] = someColumnNames
                       
            if theFeatureFilters:
                unosFeatureFilters = theFeatureFilters.copy()
            else:
                unosFeatureFilters = {}
            unosFeatureFilters[ 'attrs'] = someColumnNames                       
            
            unAccessor      = unField.getAccessor( theElement)
            
            unosTiposElementos = self.getTiposCandidatosReferenceFieldNamed( theElement, aFieldName)
            

            
            
            for unTipoElemento in unosTiposElementos:
                
                unContentIcon = ''
                
                unArchetypeClass = theElement.fArchetypeClassByName( unTipoElemento)
                if unArchetypeClass:
                    
                    try:
                        unContentIcon = unArchetypeClass.content_icon
                    except:
                        None
                        
                unTraversalResult[ 'related_types_and_icons'].append( [ unTipoElemento, unContentIcon,])
                        
            
                
                
                                                        
            aDummy = self.fAttributeTranslationsFromCache( 
                theElement            = theElement,
                theFieldName          = aFieldName, 
                theTranslationsCaches = theTranslationsCaches,
                theResultDict         = unTraversalResult, 
                theResultKey          = 'traversal_translations',
                theAdditionalParams   = theAdditionalParams,
            )                                         
    
            someRelatedItems   = theTraversalConfig.get( 'related_types', []) or []
            if not someRelatedItems:
                return unTraversalResult        
    
            someElementAdditionalColumns = theTraversalConfig.get( 'additional_columns', []) or []               
    
            unosElementos         = [ ]
            unosElementosVisibles = [ ]
    
            unosTodosTiposAceptados = []
            
            if unCanReturnValues:
                unValue = None
                try:            
                    unValue  = unAccessor()    
                except  Exception, unaException:
                    aLogger = logging.getLogger( 'ModelDDvlPloneTool_Retrieval::fRetrieveTraversalConfig_Relation')
                    aLogger.info( 'Error accessing element relation: meta_type=%s title=%s attribute=%s\nException:%s\n' % ( theElement.meta_type, theElement.Title(), aFieldName , str( unaException) )) 
                
                if not unEsMultiValued:
                    if unValue: 
                        unosElementos = [ unValue, ]
                        unTraversalResult[ 'max_multiplicity_reached'] = True
                    else:
                        unosElementos = []
                        unTraversalResult[ 'max_multiplicity_reached'] = False
                else:
                    if ( unMultiplicityHigher > 0) and ( len( unValue) >= unMultiplicityHigher): 
                        unTraversalResult[ 'max_multiplicity_reached'] = True
                    else:
                        unTraversalResult[ 'max_multiplicity_reached'] = False
                    if unValue:
                        unosElementos = unValue
                    else:
                        unValue = []
            
                for unElemento in unosElementos:
                    if self.fCheckTypeReadPermission( unElemento, [ permissions.View ], theCheckedPermissionsCache):
                        unosElementosVisibles.append( unElemento)    
                        
            if theRetrievalExtents:
                unRetrievalExtents = theRetrievalExtents[:]
            else:
                unRetrievalExtents = []
                
            if 'relation_cursors' in unRetrievalExtents:
                unRetrievalExtents.remove( 'relation_cursors')
            if 'traversals' in unRetrievalExtents:
                unRetrievalExtents.remove( 'traversals')
            if 'tree' in unRetrievalExtents:
                unRetrievalExtents.remove( 'tree')
                        
        
            if unosElementosVisibles:
                for aRelatedItems in someRelatedItems:
                    
                    unRelatedItemsTypeConfig = aRelatedItems
         
                    somePortalTypes = aRelatedItems.get( 'portal_types', []) or []
                    someAcceptedPortalTypes = [ unTipoElemento for unTipoElemento in unosTiposElementos if unTipoElemento in somePortalTypes]
    
                    for unTypeName in someAcceptedPortalTypes:
                        if not unTypeName in unosTodosTiposAceptados:
                            unosTodosTiposAceptados.append( unTypeName)
                            
                    
                    if someAcceptedPortalTypes:

                        if unCanReturnValues:
                            someElements = [ unElemento for unElemento in unosElementosVisibles if unElemento.meta_type in someAcceptedPortalTypes]
        
                            if someElements:
                                unTraversalResult[ 'num_elements'] += len( someElements)
                                
                                if ( not theFeatureFilters) or not ( aFieldName in theFeatureFilters.get( 'relations_without_element_details', [])):
                                    aNumElements = len( someElements)
                                    for unIndexElemento in range( aNumElements):
                                        unElemento = someElements[ unIndexElemento]
                                        if unRetrieveMinimalResult:
                                            unElementResult = self.fNewResultForElement( unElemento)
                                            
                                            if unCanReturnValues:
                                                unReadPermission = self.fCheckTypeReadPermission( unElemento, [ permissions.View ], theCheckedPermissionsCache)
                                                unElementResult[ 'read_permission'] = unReadPermission

                                            
                                        else:
                                            unElementResult = self.fRetrieveTypeConfig_recursive( 
                                                theTimeProfilingResults     =theTimeProfilingResults,
                                                theResult                   =None, 
                                                theElement                  =unElemento, 
                                                theParent                   =theElement,
                                                theParentTraversalName      =aFieldName,
                                                theCanReturnValues          =unCanReturnValues, 
                                                theViewName                 =theViewName,
                                                theRetrievalExtents         =unRetrievalExtents, 
                                                theTypeConfig               =unRelatedItemsTypeConfig, 
                                                theAllTypeConfigs           =theAllTypeConfigs, 
                                                theParentTraversalResult    =unTraversalResult, 
                                                theTranslationsCaches       =theTranslationsCaches, 
                                                theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                                                theWritePermissions         =theWritePermissions, 
                                                theFeatureFilters           =unosFeatureFilters, 
                                                theInstanceFilters          =theInstanceFilters,
                                                theAdditionalParams         =theAdditionalParams
                                            )
                                        
                                        
                                        if unElementResult and unElementResult[ 'read_permission']:
                                            unosElementResults.append( unElementResult)
                                            # ACV 20090901 Removed to avoid producing huge traversal result dumps
                                            # because each element result is included 3 times (in the ordered collection, and the two dicts)
                                            # which is compounded when traversing a tree
                                            # ACV 20090901 Avoid adding redundant results to dictionaries during service layer processing
                                            # the dictionaries will be compiled at the completion of the retrieval
                                            # in method pBuildDictResults_Element
                                            #
                                            #unTraversalResult[ 'elements_by_UID'][ unElementResult[ 'UID']] = unElementResult
                                            #unTraversalResult[ 'elements_by_id' ][ unElementResult[ 'id' ]] = unElementResult
                                        
                                    if theRetrievalExtents and ( 'relation_cursors' in theRetrievalExtents):
                                        unNumResults = len( unosElementResults) 
                                        for unIndexResult in range( unNumResults):
                                            unElementResult = unosElementResults[ unIndexResult]

                                            unResultCursor = self.fNewVoidCursorResult()
                                            unResultCursor.update( {
                                                'object':               unElementResult[ 'object'],
                                                'meta_type':            unElementResult[ 'meta_type'],
                                            })                                            
                                            unResultCursor[ 'container_element'] = theTraversedObjectResult                                      
                                            unResultCursor[ 'elements_count']    = aNumElements
                                            unResultCursor[ 'element_index']     = unIndexResult + 1
                                            unResultCursor[ 'first_element']     = unosElementResults[ 0]
                                            unResultCursor[ 'last_element']      = unosElementResults[ unNumResults - 1]
                                            unResultCursor[ 'traversal_name']     = aFieldName

                                            unResultCursor[ 'traversal_result'] = unTraversalResult
 
                                            if unIndexResult:
                                                unResultCursor[ 'previous_element'] = unosElementResults[ unIndexResult - 1]
                                            if unIndexResult < ( unNumResults - 1):
                                                unResultCursor[ 'next_element']     = unosElementResults[ unIndexResult + 1]
                                            
                                            unElementResult[ 'cursor'] = unResultCursor
                                         
            else:
                for aRelatedItems in someRelatedItems:
                    
                    unRelatedItemsTypeConfig = aRelatedItems
         
                    somePortalTypes = aRelatedItems.get( 'portal_types', []) or []
                    someAcceptedPortalTypes = [ unTipoElemento for unTipoElemento in unosTiposElementos if unTipoElemento in somePortalTypes]
    
                    for unTypeName in someAcceptedPortalTypes:
                        if not unTypeName in unosTodosTiposAceptados:
                            unosTodosTiposAceptados.append( unTypeName)
                            
                                
            self.pCompleteColumnTranslations( 
                theTimeProfilingResults= theTimeProfilingResults,
                theContextualElement   = theElement, 
                theTraversalResult     = unTraversalResult, 
                theTypeNames           = unosTodosTiposAceptados, 
                theTranslationsCaches  = theTranslationsCaches,
                theAdditionalParams    = theAdditionalParams,
            )
                                    
                                    
            if theFeatureFilters and ( aFieldName in theFeatureFilters.get( 'candidates_for_relations', [])):
                unosResultadosCandidatos = self.fRetrieveCandidatesTraversalConfig(
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =theElement,
                    theCanReturnValues          =theCanReturnValues, 
                    theViewName                 =theViewName,
                    theTypeConfig               =theTypeConfig, 
                    theAllTypeConfigs           =theAllTypeConfigs, 
                    theTraversalConfig          =theTraversalConfig, 
                    theTranslationsCaches       =theTranslationsCaches, 
                    theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                    theWritePermissions         =theWritePermissions, 
                    theFeatureFilters           =theFeatureFilters,
                    theCurrentTraversalResult   =unTraversalResult,
                    theAdditionalParams         =theAdditionalParams
                )
                if unosResultadosCandidatos:
                    unTraversalResult[ 'candidates'] = unosResultadosCandidatos
                    
                    
    
            return unTraversalResult
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveTraversalConfig_Relation', theTimeProfilingResults)

    

    

    
  
    security.declarePrivate('fRetrieveValoresYTraduccionesAtributos')
    def fRetrieveValoresYTraduccionesAtributos(self, 
        theTimeProfilingResults         =None,
        theElement                      =None, 
        theCanReturnValues              =False, 
        theViewName                     ='',
        theRetrievalExtents             =None,
        theNamesAndConfigsToRetrieve    =None, 
        theTranslationsCaches           =None, 
        theCheckedPermissionsCache      =None, 
        theWritePermissions             =None,
        theFeatureFilters               =None,
        theInstanceFilters              =None,
        theAdditionalParams             =None): 
        """Retrieval of the attribute results and translations in an element.
        
        """
            
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveValoresYTraduccionesAtributos', theTimeProfilingResults)

        try:

            if ( theElement == None):
                return None
            
            someElementValues = []
             
            for aNameAndConfigToRetrieve in theNamesAndConfigsToRetrieve:
    
                unAttributeName   = aNameAndConfigToRetrieve[ 0]
                unAttributeConfig = aNameAndConfigToRetrieve[ 1]
                
                unValueResult = self.fNewVoidValueResult()
                unValueResult[ 'attribute_name']   = unAttributeName 
                unValueResult[ 'attribute_config'] = unAttributeConfig 
                
                someElementValues.append( unValueResult)
                
                unCanReturnValues = theCanReturnValues
                if unCanReturnValues:
                    unReadPermission = self.fCheckFieldReadPermission( theElement, unAttributeName, [ permissions.View ], theCheckedPermissionsCache) == True
                    unValueResult[ 'read_permission'] = unReadPermission
                    unCanReturnValues = unReadPermission
        
                    if unCanReturnValues and theWritePermissions and ( 'attrs' in theWritePermissions):
                        unWritePermission = True
                        if unAttributeConfig.get( 'read_only', False) == True:
                            unWritePermission = False            
                        if unWritePermission:
                            unWritePermission = self.fCheckFieldWritePermission( theElement, unAttributeName, [ permissions.ModifyPortalContent, ], theCheckedPermissionsCache)  == True
                        if unWritePermission:
                            unValueResult[ 'write_permission'] = unWritePermission   
    
                aDummy = self.fAttributeTranslationsFromCache( 
                    theElement            = theElement,
                    theFieldName          = unAttributeName, 
                    theTranslationsCaches = theTranslationsCaches,
                    theResultDict         = unValueResult, 
                    theResultKey          = 'attribute_translations',
                    theAdditionalParams   = theAdditionalParams,
                )                                         
                
                unElementFieldType = None
                
                unAttrAccessorName = unAttributeConfig.get( 'accessor', '')     
                if unAttrAccessorName:
                    unAccessor = None
                    try:
                        unAccessor = theElement[ unAttrAccessorName]    
                    except:
                        None
                    if unAccessor:
                        unElementFieldType = unAttributeConfig.get( 'type', '').lower()
                        try:
                            unRawValue = unAccessor()
                        except:
                            unaExceptionInfo = sys.exc_info()
                            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                            unInformeExcepcion = 'Exception during fRetrieveValoresYTraduccionesAtributos during accessor invocation\n' 
                            unInformeExcepcion += 'meta_type=%s title=%s attribute=%s\n' % ( theElement.meta_type, theElement.Title(), unAttrAccessorName ,)
                            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                            unInformeExcepcion += unaExceptionFormattedTraceback   
                            aLogger = logging.getLogger( 'ModelDDvlPlone')
                            aLogger.info( 'Exception:%s\n' % unInformeExcepcion) 
                
                unAttributeNameToGet = unAttributeConfig.get( 'attribute', '')     
                if unAttributeNameToGet:
                    unElementFieldType = unAttributeConfig.get( 'type', '').lower()
                    if unAttrAccessorName and unRawValue:
                        unAttributeOwner = unRawValue
                    else:
                        unAttributeOwner = theElement
                        
                    try:
                        unRawValue = unAttributeOwner.__getattribute__( unAttributeNameToGet)
                        if unRawValue.__class__.__name__ == "ComputedAttribute":
                            unComputedAttribute = unRawValue
                            unRawValue = unComputedAttribute.__get__( theElement)
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                        unInformeExcepcion = 'Exception during fRetrieveValoresYTraduccionesAtributos during access to element getattribute\n' 
                        unInformeExcepcion += 'meta_type=%s title=%s attribute=%s\n' % ( theElement.meta_type, theElement.Title(), unAttributeNameToGet ,)
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        aLogger = logging.getLogger( 'ModelDDvlPlone')
                        aLogger.info( 'Exception:%s\n' % unInformeExcepcion) 
                
                elif not unAttrAccessorName:
                    unElementSchema = theElement.schema
                    unFieldInSchema = False
                    try:
                        unFieldInSchema = unElementSchema.has_key( unAttributeName)
                    except:
                        None
                    if unFieldInSchema:
                        unElementField  = unElementSchema[ unAttributeName]
                        if unElementField:
                            
                            unElementFieldType      = unElementField.type
                            
                            unRawValue = None
                            if unCanReturnValues: 
                                try:
                                    unRawValue = unElementField.getRaw( theElement)
                                except  Exception, unaException:
                                    unaExceptionInfo = sys.exc_info()
                                    unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                                    unInformeExcepcion = 'Exception during fRetrieveValoresYTraduccionesAtributos elementattribute\n' 
                                    unInformeExcepcion += 'meta_type=%s title=%s attribute=%s\n' % ( theElement.meta_type, theElement.Title(), unAttributeName ,)
                                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                                    unInformeExcepcion += unaExceptionFormattedTraceback   
                                    aLogger = logging.getLogger( 'ModelDDvlPlone')
                                    aLogger.info( 'Exception:%s\n' % unInformeExcepcion) 
                                
                            
                            if unElementFieldType == 'computed':
                                unValueResult[ 'write_permission'] = False
                                unValueResult[ 'computed'] = True
                                unElementFieldType = unAttributeConfig.get( 'type', '').lower() 
                                if not unElementFieldType:
                                    unElementFieldType = 'string'
    
                            unWidget = unElementField.widget
                            if unWidget and (unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget') and unElementField.__dict__.has_key('vocabulary'):
                                unElementFieldType = 'selection'
                 
                if not unElementFieldType:
                    continue
                
                unValueResult[ 'type']  = unElementFieldType.lower()

                unValueResult[ 'raw_value']         = unRawValue
                unValueResult[ 'value']             = unRawValue
                unValueResult[ 'uvalue']            = unRawValue
                unValueResult[ 'translated_value']  = unRawValue
                
                if unElementFieldType == 'selection':
                                                                            
                    aDummy = self.fVocabularyOptionsAndValueTranslationFromCache_into(  
                        theElement             =theElement, 
                        theCanReturnValues     =unCanReturnValues, 
                        theValue               =unRawValue, 
                        theAttributeName       =unAttributeName, 
                        theRetrievalExtents    =theRetrievalExtents,
                        theTranslationsCaches  =theTranslationsCaches, 
                        theResultDict          =unValueResult,
                        theAdditionalParams    =theAdditionalParams,
                    )
                           
                elif unElementFieldType in[  'string', 'text']:
                    
                    unValueResult[ 'uvalue']            = self.fAsUnicode( unRawValue, theElement)
                    unValueResult[ 'translated_value']  = unValueResult[ 'uvalue']
                    
                elif unElementFieldType == 'boolean':
                    
                    aDummy = self.fBooleanOptionsAndValueTranslationFromCache_into(     
                           theElement, 
                           unCanReturnValues, 
                           unRawValue,
                           unAttributeName, 
                           theTranslationsCaches, 
                           unValueResult,
                           theAdditionalParams)
                    
                elif unElementFieldType == 'integer':
                    unValueResult[ 'uvalue']            = self.fAsUnicode( str( unRawValue), theElement)
                    unValueResult[ 'translated_value']  = unValueResult[ 'uvalue']
                    
                elif unElementFieldType == 'float':
                    unValueResult[ 'uvalue']            = self.fAsUnicode( str( unRawValue), theElement)
                    unValueResult[ 'translated_value']  = unValueResult[ 'uvalue']

                elif unElementFieldType == 'fixedpoint':
                    unValueResult[ 'uvalue']            = self.fAsUnicode( str( unRawValue), theElement)
                    unValueResult[ 'translated_value']  = unValueResult[ 'uvalue']

                elif unElementFieldType == 'datetime':
                    self.pDateSubValuesOptionsAndTranslations_into( 
                       theElement, 
                       unCanReturnValues, 
                       unRawValue,
                       unAttributeName, 
                       theTranslationsCaches, 
                       unValueResult)
                
            return someElementValues                            

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveValoresYTraduccionesAtributos', theTimeProfilingResults)




    
        
    security.declarePrivate('fRetrieveAggregationCursorInfoAndTranslations')
    def fRetrieveAggregationCursorInfoAndTranslations(self,         
        theTimeProfilingResults     =None,
        theElement                  =None,
        theViewName                 ='',
        theAllTypeConfigs           =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theWritePermissions         =None,
        theAdditionalParams         =None):
        """Retrieval of the cursor result for an element, including the first, last, previous and next sibling elements on the element's container.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveAggregationCursorInfoAndTranslations', theTimeProfilingResults)

        try:

            if ( theElement == None):
                return None
            
            unResultCursor = self.fNewVoidCursorResult()
            unResultCursor.update( {
                'object':               theElement,
                'meta_type':            theElement.meta_type,
            })
            
            unContenedor = theElement.getContenedor()
            unEsRaiz = theElement.getEsRaiz()
            
            if unEsRaiz or ( not unContenedor) or ( unContenedor == theElement):
                unResultCursor[ 'elements_count'] = 1
                unResultCursor[ 'element_index']          = 0
                unResultCursor[ 'first_element']          = None
                unResultCursor[ 'last_element']           = None
                unResultCursor[ 'container_element']      = None
                return unResultCursor
                        
            unResultadoContenedor = self.fRetrieveTypeConfig_recursive(
                theTimeProfilingResults     =theTimeProfilingResults,
                theResult                   =None, 
                theElement                  =unContenedor, 
                theParent                   =None,
                theParentTraversalName      =None,
                theCanReturnValues          =True, 
                theViewName                 =theViewName,
                theRetrievalExtents         =[ 'traversals'], 
                theTypeConfig               =None, 
                theAllTypeConfigs           =theAllTypeConfigs, 
                theParentTraversalResult    =None, 
                theTranslationsCaches       =theTranslationsCaches, 
                theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                theWritePermissions         =theWritePermissions, 
                theFeatureFilters           ={ 'attributes': [ 'title', 'description', ], 'relations': [], 'do_not_recurse_collections': True, }, 
                theInstanceFilters          =None,
                theAdditionalParams         =theAdditionalParams
            )            

            if not unResultadoContenedor:
                return unResultCursor
            
            unResultCursor[ 'container_element']     = unResultadoContenedor  
            
            unResultadoEncontrado = None
            unIndiceEncontrado = -1
            unResultadoColeccionEncontrado = None
            unIndiceColeccionEncontrado = -1
            
            for unaTraversalResult in unResultadoContenedor.get( 'traversals', []):
                unosElementsResults = unaTraversalResult.get( 'elements', [])  
                unNumElementsResults = len( unosElementsResults)
                for unElementIndex in range( unNumElementsResults):
                    unElementResult = unosElementsResults[ unElementIndex]
                    if theElement == unElementResult.get( 'object', None):
                        unResultadoEncontrado           = unElementResult  
                        unIndiceEncontrado              = unElementIndex
                        break
                
                if unResultadoEncontrado:
                    unResultCursor[ 'traversal_name']   = unaTraversalResult[ 'traversal_name']

                    unResultCursor[ 'traversal_result'] = unaTraversalResult
 
                    unResultCursor[ 'element_index']    = unIndiceEncontrado + 1
                    unResultCursor[ 'elements_count']   = unNumElementsResults
                    unResultCursor[ 'first_element']    = unosElementsResults[ 0]
                    unResultCursor[ 'last_element']     = unosElementsResults[ unNumElementsResults - 1]
                    
                    unResultCursor[ 'siblings']         = unaTraversalResult[ 'elements']
                    
                    
                    if unIndiceEncontrado > 0:
                        unResultCursor[ 'previous_element'] = unosElementsResults[ unIndiceEncontrado - 1]
                                
                    if unIndiceEncontrado < ( unNumElementsResults - 1):
                        unResultCursor[ 'next_element']     = unosElementsResults[ unIndiceEncontrado + 1]
                       
                    return unResultCursor
                        
            return unResultCursor   
    
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveAggregationCursorInfoAndTranslations', theTimeProfilingResults)


    

                
                
                
                
                
                

    security.declarePrivate('fNewResultForElement')
    def fNewResultForElement(self, theElement, theResult=None):
        """Create a result structure for an element, initializing it with the most relevant information, including identity, naming, path and owner attributes.
        
        """
        
        unResult = theResult
        if unResult == None:
            unResult = self.fNewVoidElementResult()
            
        unResult.update( { 
            'object':                   theElement,                           
            'meta_type':                theElement.meta_type,  
            'seconds_now':              fSecondsNow(),
        } )

        unTitle = ''    
        try:
            unTitle        = theElement.Title()
        except:
            None
        if unTitle:
            unResult[ 'title'] = unTitle

        unaId = ''    
        try:
            unaId        = theElement.getId()
        except:
            None
        if unaId:
            unResult[ 'id'] = unaId
            
        unaUrl = ''    
        try:
            unaUrl         = theElement.absolute_url()
        except:
            None
        if unaUrl:
            if not ( unaUrl[-1:] == '/'):
                unaUrl = '%s/' % unaUrl                
            unResult[ 'url'] = unaUrl 
            
        unaUID = ''    
        try:
            unaUID         = theElement.UID()
        except:
            None
        if unaUID:
            unResult[ 'UID'] = unaUID 
        
            
        unPath = ''    
        try:
            unPath         = theElement.fPhysicalPathString( theElement)
        except:
            unPath         = '/'.join( theElement.getPhysicalPath())
        if unPath:
            unResult[ 'path'] = unPath 
            
            
        unPortalObject = None
        unPortalURLTool = getToolByName( theElement, 'portal_url')
        if unPortalURLTool:
            unPortalURL = ''
            try:
                unPortalURL = unPortalURLTool()
            except: 
                None
            if unPortalURL:
                unResult[ 'portal_url'] = unPortalURL 
            try:
                unPortalObject = unPortalURLTool.getPortalObject()
            except: 
                None
            if not ( unPortalObject == None):
                unResult[ 'portal_object'] = unPortalObject 
                
            
            
        unRaiz = None
        try:
            unRaiz = theElement.getRaiz()
            unResult[ 'is_supported'] = True
        except:
            None
        if unRaiz == None:
            unCurrent = theElement
            # #########################################
            """If the element does not implement the getRaiz() method, 
            I.e. is not a ModelDDvlPlone supported application, 
            Recurse up the containment hierarchy until finding an element that does, or reaching the portal root.
            """
            while ( unRaiz == None):
                if unCurrent == unPortalObject:
                    unResult[ 'root_title']  = 'Portal %s' % unCurrent.Title()
                    unResult[ 'root_url']    = unCurrent.absolute_url()
                    break
                unCurrent = aq_parent( aq_inner( unCurrent))
                if unCurrent == None:
                    break
                try:
                    unRaiz = theElement.getRaiz()
                except:
                    None
                
        if unRaiz:
            try:
                unResult[ 'root_title']    = unRaiz.Title()
            except:
                None
            try:
                unResult[ 'root_url']    = unRaiz.absolute_url()
            except:
                None
                
            
            try:
                unRaiz.getRaiz()
                unResult[ 'is_root_supported'] = True
            except:
                None
            
            
             
        unRootPath = ''    
        if not ( unRaiz == None):
            try:
                unRootPath         = unRaiz.fPathDelRaiz()
            except:
                None
            if not unRootPath:
                try:
                    unRootPath     = unRaiz.fPhysicalPathString()
                except:
                    None
        else:
            try:
                unRootPath         = theElement.fPathDelRaiz()
            except:
                None
            if not unRootPath:
                try:
                    unRootPath     = theElement.getRaiz().fPhysicalPathString()
                except:
                    None
            
        if unRootPath:
            unResult[ 'root_path'] = unRootPath 
        else:
            unResult[ 'root_path'] = '/' 
            
             

            
        unPortalType = ''    
        try:
            unPortalType        = theElement.portal_type
        except:
            None
        if unPortalType:
            unResult[ 'portal_type'] = unPortalType 

        unArchetypeName = ''    
        try:
            unArchetypeName     = theElement.archetype_name
        except:
            None
        if unArchetypeName:
            unResult[ 'archetype_name'] = unArchetypeName

        unContentIcon = ''
        try:
            unContentIcon       = theElement.content_icon
        except:
            None
        if unContentIcon:
            unResult[ 'content_icon'] = unContentIcon

        unEsColeccion = False
        try:
            unEsColeccion       = theElement.getEsColeccion()
        except:
            None
        unResult[ 'is_collection'] = unEsColeccion
        
        unEsRaiz = False
        try:
            unEsRaiz            = theElement.getEsRaiz()
        except:
            None
        unResult[ 'is_root'] = unEsRaiz
            
            
        unOwner = None
        try:
            unOwner = theElement.getContenedor()
        except:
            None
        if unOwner:
            unOwnerEsColeccion = False
            try:
                unOwnerEsColeccion =  unOwner.getEsColeccion()
            except:
                None
            if unOwnerEsColeccion:    
                unOwner = unOwner.getContenedor()
            
            unOwnerPath = ''    
            try:
                unOwnerPath         = unOwner.fPhysicalPathString()
            except:
                unOwnerPath = '/'.join( unOwner.getPhysicalPath())
            if unOwnerPath:
                unResult[ 'owner_path'] = unOwnerPath 
                
            try:
                unResult[ 'owner_title'] = unOwner.Title()
            except:
                None
                
            try:
                unResult[ 'owner_url'] = unOwner.absoute_url()
            except:
                None
            

        unNombreProyecto = ''
        try:
            unNombreProyecto = theElement.getNombreProyecto()   
        except:
            None            
        if unNombreProyecto:
            unResult[ 'nombre_proyecto'] = unNombreProyecto
             
        unFactoryMethods = ''
        try:
            unFactoryMethods = theElement.factory_methods   
        except:
            None            
        if unFactoryMethods:
            unResult[ 'factory_methods'] = unFactoryMethods
            
            
        """Retrieve Dynamic factory enablers.
        
        """
 
        unFactoryEnablers = ''
        try:
            unFactoryEnablers = theElement.factory_enablers   
        except:
            None            
        if unFactoryEnablers:
            unResult[ 'factory_enablers'] = unFactoryEnablers

            
            
        """Retrieve Dynamic actions allowed, at this actual moment.
        
        """
            
        unAllowRead = None
        try:
            unAllowRead = theElement.fAllowRead()
        except:
            None   
        if not ( unAllowRead == None):
            unResult[ 'allow_read'] = unAllowRead

        unAllowWrite = None
        try:
            unAllowWrite = theElement.fAllowWrite()
        except:
            None            
        if not ( unAllowWrite == None):
            unResult[ 'allow_write'] = unAllowWrite

        unAllowEditId = None
        try:
            unAllowEditId = theElement.fAllowEditId()
        except:
            None            
        if not ( unAllowEditId == None):
            unResult[ 'allow_edit_id'] = unAllowEditId            
            
        unIsCopyable = True
        try:
            unIsCopyable = theElement.cb_isCopyable()
        except:
            None            
        unResult[ 'is_copyable'] = unIsCopyable
            
        unAllowPaste = True
        try:
            unAllowPaste = theElement.fAllowPaste()
        except:
            None            
        unResult[ 'allow_paste'] = unAllowPaste

        unAllowImport = True
        try:
            unAllowImport = theElement.fAllowImport()
        except:
            None            
        unResult[ 'allow_import'] = unAllowImport

        unAllowExport = True
        try:
            unAllowExport = theElement.fAllowExport()
        except:
            None            
        unResult[ 'allow_export'] = unAllowExport

        unAllowVersion = False
        try:
            unAllowVersion = theElement.fAllowVersion()
        except:
            None            
        unResult[ 'allow_version'] = unAllowVersion

        unAllowTranslation = False
        try:
            unAllowTranslation = theElement.unAllowTranslation()
        except:
            None            
        unResult[ 'allow_translation'] = unAllowTranslation
            
                  
        
        
        """Retrieve Audit field names.
        
        """
            
        try:
            unResult[ 'creation_date_field'] = theElement.creation_date_field
        except:
            None            
        try:
            unResult[ 'creation_user_field'] = theElement.creation_user_field
        except:
            None            
        try:
            unResult[ 'modification_date_field'] = theElement.modification_date_field
        except:
            None            
        try:
            unResult[ 'modification_user_field'] = theElement.modification_user_field
        except:
            None            
        try:
            unResult[ 'deletion_date_field'] = theElement.deletion_date_field
        except:
            None            
        try:
            unResult[ 'deletion_user_field'] = theElement.deletion_user_field
        except:
            None            
        try:
            unResult[ 'is_inactive_field'] = theElement.is_inactive_field
        except:
            None            
        try:
            unResult[ 'change_counter_field'] = theElement.change_counter_field
        except:
            None            
        try:
            unResult[ 'change_log_field'] = theElement.change_log_field
        except:
            None            
        
        """Retrieve Versioning and Translation fields names
        
        """
        try:
            unResult[ 'inter_version_field'] = theElement.inter_version_field
        except:
            None            
        try:
            unResult[ 'version_field'] = theElement.version_field
        except:
            None            
        try:
            unResult[ 'version_storage_field'] = theElement.version_storage_field
        except:
            None            
        try:
            unResult[ 'version_comment_field'] = theElement.version_comment_field
        except:
            None            
        try:
            unResult[ 'version_comment_storage_field'] = theElement.version_comment_storage_field
        except:
            None            
        try:
            unResult[ 'inter_translation_field'] = theElement.inter_translation_field
        except:
            None            
        try:
            unResult[ 'language_field'] = theElement.language_field
        except:
            None            
        try:
            unResult[ 'fields_pending_translation_field'] = theElement.fields_pending_translation_field
        except:
            None            
        try:
            unResult[ 'fields_pending_revision_field'] = theElement.fields_pending_revision_field
        except:
            None            
           
         
 
        try:
            unResult[ 'versioning_link_fields'] = theElement.versioning_link_fields
        except:
            None            
        try:
            unResult[ 'translation_link_fields'] = theElement.translation_link_fields
        except:
            None            
        try:
            unResult[ 'usage_link_fields'] = theElement.usage_link_fields
        except:
            None            
        try:
            unResult[ 'derivation_link_fields'] = theElement.derivation_link_fields
        except:
            None            
  
            
            
            
            
        try:
            unResult[ 'propagate_delete_impact_to'] = theElement.propagate_delete_impact_to
        except:
            None            
            
            
        return unResult   


                

                



    
    security.declarePrivate('fRetrieveElementoBasicInfoAndTranslations')
    def fRetrieveElementoBasicInfoAndTranslations(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theRetrievalExtents         =None,
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theResult                   =None,
        theParentTraversalResult    =None,
        theWritePermissions         =None,
        theAdditionalParams         =None):
        """Retrieve a result structure for an element, initialized with the most important information and attributes.
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveElementoBasicInfoAndTranslations', theTimeProfilingResults)

        try:
        
            if ( theElement == None):
                return None
            
            unResult = theResult
            if not unResult:    
                unResult = self.fNewResultForElement( theElement)
    
                
                
                
            aDummy = self.fMetaTypeNameTranslationsFromCache_into( 
                theMetaTypeName        =theElement.meta_type, 
                theTranslationsCaches  =theTranslationsCaches, 
                theResultDict          =unResult, 
                theContextualElement   =theElement,
                theAdditionalParams    =theAdditionalParams,
            )

            
            unReadPermission  = False
            unWritePermission = False

            unAllowRead = unResult.get( 'allow_read', None)
            if not ( unAllowRead == None):
                unReadPermission = unAllowRead and True
            else:
                unReadPermission = self.fCheckTypeReadPermission( theElement, [ permissions.View ], theCheckedPermissionsCache)
            
            unResult[ 'read_permission'] = unReadPermission
            unCanReturnValues = unReadPermission

            if unReadPermission:
                unTraversePermission = self.fCheckElementPermission( theElement, [ permissions.ListFolderContents ], theCheckedPermissionsCache)
                unResult[ 'traverse_permission'] = unTraversePermission

                
                if theWritePermissions:
                    
                    unAllowWrite = unResult.get( 'allow_write', None)
                    if unAllowWrite:
                    
                        if ( 'object' in theWritePermissions) or ( 'add' in theWritePermissions) or ( 'add_collection' in theWritePermissions) or ( 'delete' in theWritePermissions):
                            unWritePermission = self.fCheckTypeWritePermission( theElement, [ permissions.ModifyPortalContent, ], theCheckedPermissionsCache) == True
                            unResult[ 'write_permission']            =  unWritePermission   
        
                            if unWritePermission and ( 'add' in theWritePermissions):
                                unAddPortalContentPermission = self.fCheckElementPermission( theElement, [ permissions.AddPortalContent, ], theCheckedPermissionsCache) == True
                                unResult[ 'add_permission']     =  unAddPortalContentPermission  
            
                            if unWritePermission and ( 'add_collection' in theWritePermissions):
                                unAddPortalFoldersPermission = self.fCheckElementPermission( theElement, [ permissions.AddPortalFolders, ], theCheckedPermissionsCache) == True
                                unResult[ 'add_collection_permission']     =  unAddPortalFoldersPermission  
            
                            if unWritePermission and ('delete' in theWritePermissions):
                                unDeletePermission = self.fCheckElementPermission( theElement, [ permissions.DeleteObjects, ], theCheckedPermissionsCache) == True
                                unResult[ 'delete_permission']           =  unDeletePermission   
            
            self.pRetrieveAttributeConfigs( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theElement, 
                theCanReturnValues          =unCanReturnValues,
                theViewName                 ='',
                theRetrievalExtents         =None,
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theAttributeConfigs         =cBasicInfoAttributeConfigs, 
                theTranslationsCaches       =theTranslationsCaches, 
                theResult                   =unResult, 
                theParentTraversalResult    =theParentTraversalResult, 
                theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                theWritePermissions         =theWritePermissions,
                theFeatureFilters           =None,
                theInstanceFilters          =None,
                theAdditionalParams         =theAdditionalParams                
            ) 
            
            if 'audit' in theRetrievalExtents:
                self.fRetrieveAuditInfo(                
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =theElement, 
                    theRetrievalExtents         =None,
                    theTranslationsCaches       =theTranslationsCaches, 
                    theResult                   =unResult, 
                    theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                    theAdditionalParams         =theAdditionalParams                
                )
                                    
            if ( 'change_entries' in theRetrievalExtents) or ( 'change_entries_summaries' in theRetrievalExtents) or ( 'change_entries_summaries_fields_values' in theRetrievalExtents):
                from ModelDDvlPloneTool_Mutators import ModelDDvlPloneTool_Mutators
                ModelDDvlPloneTool_Mutators().fRetrieveChangeLog(                
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =theElement, 
                    theRetrievalExtents         =theRetrievalExtents,
                    theTranslationsCaches       =theTranslationsCaches, 
                    theResult                   =unResult, 
                    theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                    theAdditionalParams         =theAdditionalParams                
                )
 
                
            if 'extra_links' in theRetrievalExtents:
                unosExtraLinks = []
                try:
                    unosExtraLinks = theElement.fExtraLinks()
                except:
                    None
                if unosExtraLinks:
                    unResult[ 'extra_links'] = unosExtraLinks
               
                #self.fRetrieveExtraLinks(                
                    #theTimeProfilingResults     =theTimeProfilingResults,
                    #theElement                  =theElement, 
                    #theRetrievalExtents         =None,
                    #theTranslationsCaches       =theTranslationsCaches, 
                    #theResult                   =unResult, 
                    #theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                    #theAdditionalParams         =theAdditionalParams                
                #)
                
                
            if 'num_contained' in theRetrievalExtents:
                
                unPath = '/'.join( theElement.getPhysicalPath())
                
                unPortalCatalog = getToolByName( theElement, 'portal_catalog')
                unaBusqueda = { 
                    'path' :             unPath,
                }
     
                unosResultadosBusqueda = unPortalCatalog.searchResults( **unaBusqueda)
                unNumContained = max( 0, len( unosResultadosBusqueda) - 1)
                
                unResult[ 'num_contained'] = unNumContained
                
                
            return unResult
            
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveElementoBasicInfoAndTranslations', theTimeProfilingResults)
                   

                

    
    security.declarePrivate('fRetrieveAuditInfo')
    def fRetrieveAuditInfo(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theRetrievalExtents         =None,
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theResult                   =None,
        theAdditionalParams         =None):
        """Retrieve a result structure for an element, initialized with the audit information.
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveAuditInfo', theTimeProfilingResults)

        try:
        
            if ( theElement == None):
                return None
            
            unResult = theResult
            if not unResult:    
                unResult = self.fNewResultForElement( theElement)  
                
            unSchema = theElement.schema
            if not unSchema:
                return unResult
                
            for unFieldKey in cAuditFieldKeys:
                unFieldNameKey = '%s_field' % unFieldKey
                unFieldName = unResult.get( unFieldNameKey, '')
                if unFieldName:
                    
                    unField = unSchema.get( unFieldName, None)
                    if unField:
                        unAccessor = unField.getAccessor( theElement)
                        if unAccessor:
                            unValue = None
                            try:
                                unValue = unAccessor()
                            except:
                                None
                            unResult[ unFieldKey] = unValue
                           
            return unResult
            
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveAuditInfo', theTimeProfilingResults)
                  
                
                
                
  
    
    
                    
                
                
                
                
                
                
                
                
                
                
                
    security.declarePrivate( 'fRetrieveElementoTypeInfo')
    def fRetrieveElementoTypeInfo(self, theElement, theTranslationsCaches, theResult=None):
        """Retrieve translations for an element's type.
        
        """
        
        unResult = theResult
        if not unResult:
            unResult = self.fNewResultForElement( theElement)
        if not unResult:
            return None
    
        aDummy    = self.fMetaTypeNameTranslationsFromCache_into( 
            theMetaTypeName        =theElement.meta_type, 
            theTranslationsCaches  =theTranslationsCaches, 
            theResultDict          =unResult, 
            theContextualElement   =theElement,
            theAdditionalParams    =None,
        )
    
        return unResult
    
    
    
    
    

    
    
    
    
    
    
    security.declarePrivate( 'pFactoryNamesAndTranslations_into')
    def pFactoryNamesAndTranslations_into(self, 
        theContextElement      = None, 
        theTypeNames           = None, 
        theTranslationsCaches  = None, 
        theResult              = None,
        theAdditionalParams    = None):
        """Retrieve the factory specifications applicable to create elements inside a given element, including their translations.
        
        """
         
        if not theResult:
            return self
                
        someFactoryNamesAndTranslations = [ ]                                            
        for unMetaType in theTypeNames:
            
            unPortalTypeTranslations = self.fMetaTypeNameTranslationsFromCache_into( 
                theMetaTypeName        =unMetaType, 
                theTranslationsCaches  =theTranslationsCaches, 
                theResultDict          =None, 
                theContextualElement   =theContextElement,
                theAdditionalParams    =theAdditionalParams,
            )
            unContentIcon    = ''
            unArchetypeName  = unMetaType
            unPortalType     = unMetaType
            if unPortalTypeTranslations:
                unArchetypeName = unPortalTypeTranslations.get( 'archetype_name', '')
                unContentIcon = unPortalTypeTranslations.get( 'content_icon', '')
                
            unPlonePortalType = self.fPlonePortalTypeForMetaType( unMetaType)
            if unPlonePortalType:
                unPortalType = unPlonePortalType
               
            unFactoryResult = self.fNewVoidFactoryResult()
            unFactoryResult.update( { 
                'meta_type':            unMetaType, 
                'type_translations':    unPortalTypeTranslations, 
                'content_icon':         unContentIcon ,
                'archetype_name':       unArchetypeName,
                'portal_type':          unPortalType,
            } )                
            
            someFactoryNamesAndTranslations.append( unFactoryResult)
            
        someSortedFactoryNamesAndTranslations = sorted( someFactoryNamesAndTranslations, lambda unaF, otraF: cmp( unaF.get('type_translations',{}).get( 'translated_archetype_name', unaF['archetype_name']) , otraF.get('type_translations',{}).get( 'translated_archetype_name', unaF['archetype_name']) ) )
    
        theResult[ 'factories'] =  someSortedFactoryNamesAndTranslations
        
        return self
    
    
    
    



   
    
    security.declarePrivate('fKnownWritePermissionTargets')
    def fKnownWritePermissionTargets( self):
        return cKnownWritePermissionTargets
    
    
    security.declarePrivate('fKnownFeatureFilterKeys')
    def fKnownFeatureFilterKeys( self):
        return cKnownFeatureFilterKeys
    
    security.declarePrivate('fKnownInstanceFilterKeys')
    def fKnownInstanceFilterKeys( self):
        return cKnownInstanceFilterKeys
 
    
    security.declarePrivate('fKnownRetrievalExtents')
    def fKnownRetrievalExtents( self):
        return cKnownRetrievalExtents
    
     
    



    security.declarePrivate( 'fElementoPorUID')
    def fElementoPorUID( self, theUID, theContextualElement):
        """Element access by UID.
        
        """
        if not theUID or ( theContextualElement == None):
            return None
            
        unPortalCatalog = getToolByName( theContextualElement, 'uid_catalog')
        unaBusqueda = { 
            'UID' :            theUID, 
        }
        unosResultadosBusqueda = unPortalCatalog.searchResults( **unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return None
            
        unElemento = unosResultadosBusqueda[ 0].getObject() 
        if ( unElemento == None):
            return None

        return unElemento    





    security.declarePrivate( 'fElementosPorUIDs_Results')
    def fElementosPorUIDs_Results( self, theUIDs, theContextualElement):
        """Elements access by UIDs.
        
        """
        if not theUIDs or ( theContextualElement == None):
            return []
            
        unPortalCatalog = getToolByName( theContextualElement, 'uid_catalog')
        unaBusqueda = { 
            'UID' :            list( theUIDs), 
        }
        unosResultadosBusqueda = unPortalCatalog.searchResults( **unaBusqueda)
        if len( unosResultadosBusqueda) < 1:
            return []

        return unosResultadosBusqueda    



    security.declarePrivate( 'fElementosPorUIDs')
    def fElementosPorUIDs( self, theUIDs, theContextualElement):
        """Elements access by UIDs.
        
        """

        unosResultadosBusqueda = self.fElementosPorUIDs_Results( theUIDs, theContextualElement)
        if not unosResultadosBusqueda:
            return {}
            
        unosElementosPorUIDs =  {}
        for unResultado in unosResultadosBusqueda:
            
            unElemento =unResultado.getObject() 
            unaUID     = unResultado[ 'UID']
            if not ( unElemento == None):
                unosElementosPorUIDs[ unaUID] = unElemento

        return unosElementosPorUIDs    


    

    security.declarePrivate( 'fElementosPorUIDs')
    def fElementsNamesByUID( self, theUIDs, theContextualElement):
        """Elements access by UIDs.
        
        """

        unosResultadosBusqueda = self.fElementosPorUIDs_Results( theUIDs, theContextualElement)
        if not unosResultadosBusqueda:
            return {}
            
        unosElementosPorUIDs =  {}
        for unResultado in unosResultadosBusqueda:
            
            unaUID =  unResultado[ 'UID']
            unosElementosPorUIDs[ unaUID] = {
                'UID':           unaUID,
                'Title':         unResultado[ 'Title'],
                'Type':          unResultado[ 'Type'],
                'id':            unResultado[ 'id'],
                'portal_type':   unResultado[ 'portal_type'],
            }

        return unosElementosPorUIDs    


    
    
    
    
        
    # #############################################################
    # Initialize keyed indexes in result dictionaries, whose initialization was postponed during retrieval.
    # 

    security.declarePrivate('pBuildResultDicts')
    def pBuildResultDicts(self, theResult, theWhichDicts=None):
        """Initialize result dictionaries indexing feature results by name and id.
        
        """
        if not theResult:
            return self
        
        if ( theWhichDicts == None) or ( 'owner_element' in theWhichDicts):
            anOwnerResult = theResult.get( 'owner_element', None)
            if anOwnerResult:
                self.pBuildResultDicts_ElementValues( anOwnerResult)            
            
        if ( theWhichDicts == None) or ( 'container_element' in theWhichDicts):
            aContainerResult = theResult.get( 'container_element', None)
            if aContainerResult:
                self.pBuildResultDicts_ElementValues( aContainerResult)
                
        if ( theWhichDicts == None) or ( 'cursor' in theWhichDicts):
            aCursorResult = theResult.get( 'cursor', None)
            if aCursorResult:
                aFirstElementResult = aCursorResult.get( 'first_element', None)
                if aFirstElementResult:
                    self.pBuildResultDicts_ElementValues( aFirstElementResult)
                    
                aLastElementResult = aCursorResult.get( 'last_element', None)
                if aLastElementResult:
                    self.pBuildResultDicts_ElementValues( aLastElementResult)
    
                aPreviousElementResult = aCursorResult.get( 'previous_element', None)
                if aPreviousElementResult:
                    self.pBuildResultDicts_ElementValues( aPreviousElementResult)
    
                aNextElementResult = aCursorResult.get( 'next_element', None)
                if aNextElementResult:
                    self.pBuildResultDicts_ElementValues( aNextElementResult)
                    
                someSiblings = aCursorResult.get( 'siblings', None)
                for aSibling in someSiblings:
                    if aSibling:
                        self.pBuildResultDicts_ElementValues( aSibling)
                    
        if ( theWhichDicts == None) or ( 'values' in theWhichDicts):
            self.pBuildResultDicts_ElementValues(     theResult)
            
        if ( theWhichDicts == None) or ( 'traversals' in theWhichDicts):
            self.pBuildResultDicts_ElementTraversals( theResult)    
            
        return self
    
        
        
    
    security.declarePrivate('pBuildResultDicts_Element')
    def pBuildResultDicts_Element(self, theResult):
        if not theResult:
            return self
        
        self.pBuildResultDicts_ElementValues(     theResult)
        self.pBuildResultDicts_ElementTraversals( theResult)

        return self
    
    
    
    
    
    security.declarePrivate('pBuildResultDicts_ElementValues')
    def pBuildResultDicts_ElementValues(self, theResult):
        """Initialize result dictionaries indexing attribute results by name.
        
        """
        if not theResult:
            return self

        someValuesResults    = theResult.get( 'values',     None)
                 
        if someValuesResults:
            someValuesByName = theResult.get( 'values_by_name', None)
            if someValuesByName == None:
                someValuesByName = { }
                theResult[ 'values_by_name'] = someValuesByName

            for aValueResult in someValuesResults:
                anAttributeName = aValueResult.get( 'attribute_name', '')
                if anAttributeName:
                    someValuesByName[ anAttributeName] = aValueResult
                    
                    someSubValuesResults = aValueResult.get( 'sub_values', None)
                    if someSubValuesResults:
                        someSubValuesByName = aValueResult.get( 'sub_values_by_name', None)
                        if someSubValuesByName == None:
                            someSubValuesByName = { }
                            aValueResult[ 'sub_values_by_name'] = someSubValuesByName
                    
                        for aSubValueResult in someSubValuesResults:
                            aSubValueName = aSubValueResult.get( 'attribute_name', '')
                            if aSubValueName:
                                someSubValuesByName[ aSubValueName ] = aSubValueResult
            
        return self
    
    
    
    
    security.declarePrivate('pBuildResultDicts_ElementTraversals')
    def pBuildResultDicts_ElementTraversals(self, theResult):
        """Initialize result dictionaries indexing traversal results by name, and recursively the results of traversed elements.
        
        """
        if not theResult:
            return self

        someTraversalResults = theResult.get( 'traversals', None)
                 
        if someTraversalResults:
            someTraversalsByName = theResult.get( 'traversals_by_name', None)
            if someTraversalsByName == None:
                someTraversalsByName = { }
                theResult[ 'traversals_by_name'] = someTraversalsByName
            
            for aTraversalResult in someTraversalResults:
                aTraversalName = aTraversalResult.get( 'traversal_name', '')
                if aTraversalName:
                    someTraversalsByName[ aTraversalName] = aTraversalResult
    
                someElementsResults = aTraversalResult.get( 'elements', [])
                if someElementsResults:
                    
                    someElementsById = aTraversalResult.get( 'elements_by_id', [])  
                    if someElementsById == None:
                        someElementsById = { }
                        aTraversalResult[ 'elements_by_id'] = someElementsById
    
                    someElementsByUID = aTraversalResult.get( 'elements_by_UID', [])  
                    if someElementsByUID == None:
                        someElementsByUID = { }
                        aTraversalResult[ 'elements_by_UID'] = someElementsByUID
                        
                    for anElementResult in someElementsResults:
                        anElementId = anElementResult.get( 'id', '')
                        if anElementId:
                            someElementsById[ anElementId] = anElementResult
                        
                        anElementUID = anElementResult.get( 'UID', '')
                        if anElementUID:
                            someElementsByUID[ anElementUID] = anElementResult
                
                        self.pBuildResultDicts_Element( anElementResult)
                        
                aTraversalConfig = aTraversalResult.get( 'traversal_config', {})
                if aTraversalConfig:
                    aRelationName = aTraversalConfig.get( 'relation_name', '')
                    if aRelationName:
                        
                        aCandidatesTraversalResult = aTraversalResult.get( 'candidates', [])
                        if aCandidatesTraversalResult:
                            
                            someCandidateElementsResults = aCandidatesTraversalResult.get( 'elements', [])
                            if someCandidateElementsResults:
                                
                                for aCandidateElementResult in someCandidateElementsResults:                                        
                                    self.pBuildResultDicts_Element( aCandidateElementResult)
                                
        
        return self
    
        
    
        
    
    
# #############################################################
# Contained Element access by Id
# 
    security.declarePrivate( 'fElementoContenidoPorId')
    def fElementoContenidoPorId( self, theContainer, theID):
        if not theContainer or not theID:
            return None
            
        if not theID in theContainer.objectIds():
            return None
        
        unElemento = None    
        try:
            unElemento = theContainer.get( theID, None)
        except:
            None

        return unElemento    
    
    
    
    
    
    
    
    
    
# #############################################################
# Miscelaneus presentation utils
# 
    
        
    security.declarePrivate('fPreferredResultDictKeysOrder')
    def fPreferredResultDictKeysOrder( self):
        return  [ 
            'object', 
            'title',
            'id',
            'path',
            'url',
            'UID', 
            'meta_type', 
            'portal_type',
            'archetype_name',
            'content_icon',
            'is_root', 
            'is_collection', 
            'contains_collections',
            'has_grandchildren',
            'dependency_supplier', 
            'read_permission', 
            'write_permission', 
            'add_permission', 
            'delete_permission', 
            'element_index',
            'elements_count',
            'previous_element',
            'next_element',
            'first_element',
            'last_element',
            'traversal_kind',
            'inverse_relationship',
            'relationship', 
            'grandchildren_plural_type_translations',
            'num_elements',
            'traversal_name',  
            'attribute_name', 
            'type', 
            'non_text_field_names', 
            'text_field_names', 
            'field_names', 
            'traversal_names', 
            'column_names', 
            'factories', 
            'translated_value', 
            'translated_label_and_value', 
            'uvalue',
            'value', 
            'raw_value', 
            'vocabulary', 
            'values',  
            'traversals', 
            'elements', 
            'candidates',
            'values_by_name', 
            'traversals_by_name', 
            'cursor', 
            'owner_element', 
            'container_element', 
            'type_config', 
            'traversal_config', 
            'attribute_config',
            'type_translations',  
            'column_translations', 
            'attribute_translations', 
            'vocabulary_translations', 
            'traversal_translations', 
            'elements_by_UID',
            'elements_by_id',
        ]     
    
     