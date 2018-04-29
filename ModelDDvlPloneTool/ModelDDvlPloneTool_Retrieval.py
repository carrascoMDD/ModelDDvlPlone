# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'



import sys
import traceback

import logging

from AccessControl          import ClassSecurityInfo
from Products.CMFCore       import permissions
from Products.CMFCore.utils import getToolByName


from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Profiling                    import ModelDDvlPloneTool_Profiling
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Permissions        import ModelDDvlPloneTool_Retrieval_Permissions
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Utils              import ModelDDvlPloneTool_Retrieval_Utils
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Candidates         import ModelDDvlPloneTool_Retrieval_Candidates
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Derivation         import ModelDDvlPloneTool_Retrieval_Derivation
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_I18N               import ModelDDvlPloneTool_Retrieval_I18N
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_TraversalConfigs   import ModelDDvlPloneTool_Retrieval_TraversalConfigs
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Impact             import ModelDDvlPloneTool_Retrieval_Impact
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_PloneContent       import ModelDDvlPloneTool_Retrieval_PloneContent


cKnownWritePermissionTargets = [ 'object', 'add', 'add_collection', 'delete', 'attrs', 'aggregations', 'relations', 'plone', 'delete_plone', ]
cKnownFeatureFilterKeys      = [ 'types', 'attrs', 'aggregations', 'relations', 'relations_without_element_details', 'candidates_for_relations', 'do_not_recurse_collections']
cKnownInstanceFilterKeys     = [ 'UIDs', ]
cKnownRetrievalExtents       = [ 'traversals', 'tree',  'owner', 'cursor', 'relation_cursors', 'dynamic_vocabularies',]
cKnownAdditionalParams       = [ 'Do_Not_Translate', 'Retrieve_Minimal_Related_Results', ]



class ModelDDvlPloneTool_Retrieval(
    ModelDDvlPloneTool_Profiling,
    ModelDDvlPloneTool_Retrieval_Permissions, 
    ModelDDvlPloneTool_Retrieval_Utils, 
    ModelDDvlPloneTool_Retrieval_Candidates, 
    ModelDDvlPloneTool_Retrieval_Derivation,
    ModelDDvlPloneTool_Retrieval_I18N, 
    ModelDDvlPloneTool_Retrieval_TraversalConfigs,
    ModelDDvlPloneTool_Retrieval_Impact,
    ModelDDvlPloneTool_Retrieval_PloneContent):
    """
    """
    security = ClassSecurityInfo()

    
    security.declarePrivate('pBuildResultDicts')
    def pBuildResultDicts(self, theResult, theWhichDicts=None):
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
    
        
    
    
    security.declarePrivate('fNewVoidElementResult')
    def fNewVoidElementResult(self):
        unResult = { 
            # ACV 200906110258 added portal_url to have all icons and images to reference same url to allow effective caching
            'portal_url':               '',
            'object':                   None,                           
            'meta_type':                '',     
            'portal_type':              '',
            'archetype_name':           '',
            'UID':                      '',    
            'url':                      '',                 
            'title':                    '',                   
            'path':                     '',       
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
            'traversals_by_name':   { },                                  
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
            'factory_enablers':         None,
            'allow_paste':              True,
        }
        return unResult   
    

    
    
    
    
    security.declarePrivate('fNewVoidValueResult')
    def fNewVoidValueResult(self):
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
        }
        return unResult   
   
    
    
    
    security.declarePrivate('fNewVoidTraversalResult')
    def fNewVoidTraversalResult(self):
        unResult = { 
            'traversal_kind' :          '', 
            'traversal_name' :          '', 
            'contains_collections' :    False, 
            'has_grandchildren':        False,
            'is_multivalued' :          False, 
            'relationship':             '',
            'inverse_relationship':     '',
            'traversal_config':         None, 
            'num_elements':             0,
            'dependency_supplier':      False,
            'elements':                 [], 
            'traversal_translations' :  { },
            'factories' :               [],
            'column_names':             [ ],
            'column_translations':      { },
            'read_permission':          False,
            'write_permission':         False,
            'max_multiplicity_reached': False,
            'multiplicity_higher':      -1,
            'candidates':               [],
            'elements_by_UID':          {},
            'elements_by_id':           {},
            'factory_views':            None,
        }
        return unResult   
   
    

    

    
    security.declarePrivate('fNewVoidCursorResult')
    def fNewVoidCursorResult(self):
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
        }
        return unResult   
    


    security.declarePrivate('fNewVoidFactoryResult')
    def fNewVoidFactoryResult(self):
        unResult = { 
            'meta_type':            '', 
            'type_translations':    [], 
            'content_icon':         '',
            'archetype_name':       '',
            'factory_view':         '',
        }                
        return unResult
    
    
    
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
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveTypeConfigByUID', theTimeProfilingResults)
                      
        try:
            unElemento = self.fElementoPorUID( theUID, theContextualElement)
            if not unElemento:
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
                    if unPropietario:
                        unPropietarioResult = self.fRetrieveElementoBasicInfoAndTranslations( 
                            theTimeProfilingResults     =theTimeProfilingResults,
                            theElement                  =unPropietario,             
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
                    if unContenedor:
                        if unPropietario and ( unContenedor == unPropietario):
                            unContenedorResult = unPropietarioResult
                        else:
                            unContenedorResult = self.fRetrieveElementoBasicInfoAndTranslations( 
                                theTimeProfilingResults     =theTimeProfilingResults,
                                theElement                  =unContenedor,             
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
                theTranslationsCaches       =theTranslationsCaches, 
                theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                theResult                   =unResult,
                theParentTraversalResult    =theParentTraversalResult,
                theWritePermissions         =theWritePermissions,
                theAdditionalParams         =theAdditionalParams,
            )
    
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
            
                                
            # ACV OJO 20090901 It is already done in fRetrieveElementoBasicInfoAndTranslations above
            # aDummy    = self.fMetaTypeNameTranslationsFromCache_into( theElement.meta_type, theTranslationsCaches, unResult, theElement)
    
            if unTypeConfig.has_key( 'attrs'):
                someAttributeConfigs =  unTypeConfig.get( 'attrs', [])
                if someAttributeConfigs:
                    self.pRetrieveAttributeConfigs( 
                        theTimeProfilingResults     =theTimeProfilingResults,
                        theElement                  =theElement, 
                        theCanReturnValues          =unCanReturnValues,
                        theViewName                 =theViewName,
                        theRetrievalExtents         =theRetrievalExtents,
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
            
            if theRetrievalExtents and ( ( 'traversals' in theRetrievalExtents) or ( 'tree' in theRetrievalExtents)):
                if unTypeConfig.has_key( 'traversals'):
                    someTraversalConfigs =  unTypeConfig.get( 'traversals', [])
                    if someTraversalConfigs:
                        if theRetrievalExtents:
                            unosRetrievalExtents = theRetrievalExtents[:]
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
                    if unValueResult[ 'type'] == 'text':
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
                            continue;
    
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
                    if unWritePermission:
                        unWritePermission = self.fCheckFieldWritePermission( theElement, aFieldName, [ permissions.ModifyPortalContent, ], theCheckedPermissionsCache) == True
                    if unWritePermission:
                        unTraversalResult[ 'write_permission'] = unWritePermission     
                
                        
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
        
            unHasGrandChildren = False
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
                 
                someEnabledPortalTypes = [ ]
                
                unosFactoryEnablers = theTraversedObjectResult.get( 'factory_enablers', {})
                if not unosFactoryEnablers:
                    someEnabledPortalTypes = someAcceptedPortalTypes[:]
                    
                else:
                    for unPortalTypeName in someAcceptedPortalTypes:
                        unTypeIsEnabled = True
                        
                        unFactoryEnablerMethodName = unosFactoryEnablers.get( unPortalTypeName, '')
                        if unFactoryEnablerMethodName:
                            unFactoryEnablerMethod = None
                            try:
                                unFactoryEnablerMethod = theElement[ unFactoryEnablerMethodName]
                            except:
                                None
                            if unFactoryEnablerMethod:
                                unTypeIsEnabled = False
                                try:
                                    unTypeIsEnabled = unFactoryEnablerMethod( unPortalTypeName)
                                except:
                                    None
                                    
                        if unTypeIsEnabled:
                            someEnabledPortalTypes.append( unPortalTypeName)    
                        
                    
                    
                for unPortalTypeName in someEnabledPortalTypes:
                    if not ( unPortalTypeName in someElementFactoryNames): 
                        someElementFactoryNames.append( unPortalTypeName)
                  
                for unPortalTypeName in someEnabledPortalTypes:
                    if not unTypeName in unosTodosTiposAceptados:
                        unosTodosTiposAceptados.append( unPortalTypeName)
                            
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
                                        someAggegationSubTraversals = [ unTraversalRes for unTraversalRes in unElementResult[ 'traversals'] if unTraversalRes[ 'traversal_kind'] == 'aggregation' and unTraversalRes[ 'num_elements'] > 0]
                                        if not  unHasGrandChildren:
                                            unHasGrandChildren = len( someAggegationSubTraversals) > 0 
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
                unTraversalResult[ 'has_grandchildren'] = unHasGrandChildren
                unTraversalResult[ 'grandchildren_plural_type_translations'] = unasTodosSubAggregationsTranslations
            return unTraversalResult
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveTraversalConfig_Aggregation', theTimeProfilingResults)

 
    
    
    
    
    
    
    
    
    
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
            
            someColumnNames = theTraversalConfig.get( 'columns', []) or []    
            unTraversalResult[ 'column_names'] = someColumnNames
                       
            if theFeatureFilters:
                unosFeatureFilters = theFeatureFilters.copy()
            else:
                unosFeatureFilters = {}
            unosFeatureFilters[ 'attrs'] = someColumnNames                       
            
            unAccessor      = unField.getAccessor( theElement)
            
            unosTiposElementos = self.getTiposCandidatosReferenceFieldNamed( theElement, aFieldName)
            
                        
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
                
                unElementSchema = theElement.schema
                if unElementSchema.has_key( unAttributeName):
                    unElementField  = unElementSchema[ unAttributeName]
                    if unElementField:
                        unRawValue = None
                        if unCanReturnValues: 
                            try:
                                unRawValue = unElementField.getRaw( theElement)
                            except  Exception, unaException:
                                aLogger = logging.getLogger( 'ModelDDvlPloneTool_Retrieval::fRetrieveValoresYTraduccionesAtributos')
                                aLogger.info( 'Error accessing element attribute: meta_type=%s title=%s attribute=%s\nException:%s\n' % ( theElement.meta_type, theElement.Title(), unAttributeName , str( unaException) )) 
                            
                                        
                        unElementFieldType      = unElementField.type
                        
                        if unElementFieldType == 'computed':
                            unValueResult[ 'write_permission'] = False
                            unValueResult[ 'computed'] = True
                            unElementFieldType = unAttributeConfig.get( 'type', '') 

                        unWidget = unElementField.widget
                        if unWidget and (unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget') and unElementField.__dict__.has_key('vocabulary'):
                            unElementFieldType = 'selection'
                            
                        unValueResult[ 'type']  = unElementFieldType

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
        
        unResult = theResult
        if unResult == None:
            unResult = self.fNewVoidElementResult()
            
        unResult.update( { 
            'object':                   theElement,                           
            'meta_type':                theElement.meta_type,  
            'seconds_now':              self.getSecondsNow(),
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
            unResult[ 'url'] = unaUrl 
            
        unaUID = ''    
        try:
            unaUID         = theElement.UID()
        except:
            None
        if unaUID:
            unResult[ 'UID'] = unaUID 
        
            
        # ACV OJO 200906110306
        # When removing 2the use ofo an application specific index getPathDelRaiz.
        # we observed that the path we were constructing in concrete archetypes root type
        # as BPDElemento, EMOFElmento, ... do not match the paths used normally by plone ...
        # 
        # TO REVIEW
        unPath = ''    
        try:
            unPath         = theElement.fPhysicalPathString()
        except:
            unPath         = '/' + ('/'.join( theElement.getPhysicalPath()[2:]))
        if unPath:
            unResult[ 'path'] = unPath 
            
            
            
        # ACV 200906110258 added portal_url to have all icons and images to reference same url to allow effective caching
        unPortalURLTool = getToolByName( theElement, 'portal_url')
        if unPortalURLTool:
            unPortalURL = ''
            try:
                unPortalURL = unPortalURLTool()
            except: 
                None
            if unPortalURL:
                unResult[ 'portal_url'] = unPortalURL 

            
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
        if unEsColeccion:
            unResult[ 'is_collection'] = unEsColeccion
        
        unEsRaiz = False
        try:
            unEsRaiz            = theElement.getEsRaiz()
        except:
            None
        if unEsRaiz:
            unResult[ 'is_root'] = unEsRaiz

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
 
        unFactoryEnablers = ''
        try:
            unFactoryEnablers = theElement.factory_enablers   
        except:
            None            
        if unFactoryEnablers:
            unResult[ 'factory_enablers'] = unFactoryEnablers

        unAllowPaste = True
        try:
            unAllowPaste = theElement.fAllowPaste()
        except:
            None            
        if unAllowPaste:
            unResult[ 'allow_paste'] = True

        return unResult   


                

                



    
    security.declarePrivate('fRetrieveElementoBasicInfoAndTranslations')
    def fRetrieveElementoBasicInfoAndTranslations(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theResult                   =None,
        theParentTraversalResult    =None,
        theWritePermissions         =None,
        theAdditionalParams         =None):
        
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
                                    
            unReadPermission = self.fCheckTypeReadPermission( theElement, [ permissions.View ], theCheckedPermissionsCache)
            unResult[ 'read_permission'] = unReadPermission
            unCanReturnValues = unReadPermission

            if unReadPermission:
                unTraversePermission = self.fCheckElementPermission( theElement, [ permissions.ListFolderContents ], theCheckedPermissionsCache)
                unResult[ 'traverse_permission'] = unTraversePermission

                if theWritePermissions:
                    if ( 'object' in theWritePermissions) or ( 'add' in theWritePermissions) or ( 'add_collection' in theWritePermissions) or ( 'delete' in theWritePermissions):
                        unWritePermission = self.fCheckTypeWritePermission( theElement, [ permissions.ModifyPortalContent, ], theCheckedPermissionsCache) == True
                        unResult[ 'write_permission']   =  unWritePermission   
    
                        if unWritePermission and ( 'add' in theWritePermissions):
                            unAddPortalContentPermission = self.fCheckElementPermission( theElement, [ permissions.AddPortalContent, ], theCheckedPermissionsCache) == True
                            unResult[ 'add_permission']     =  unAddPortalContentPermission  
        
                        if unWritePermission and ( 'add_collection' in theWritePermissions):
                            unAddPortalFoldersPermission = self.fCheckElementPermission( theElement, [ permissions.AddPortalFolders, ], theCheckedPermissionsCache) == True
                            unResult[ 'add_collection_permission']     =  unAddPortalFoldersPermission  
        
                        if unWritePermission and ('delete' in theWritePermissions):
                            unDeletePermission = self.fCheckElementPermission( theElement, [ permissions.DeleteObjects, ], theCheckedPermissionsCache) == True
                            unResult[ 'delete_permission']  =  unDeletePermission   
            
            
            
            someAttributeConfigs = [
                { 'name': 'title',             'type': 'String',     'kind': 'Data',  }, 
                { 'name': 'description',       'type': 'Text',       'kind': 'Data', 'optional':  True, }, 
            ]
            
            self.pRetrieveAttributeConfigs( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theElement, 
                theCanReturnValues          =unCanReturnValues,
                theViewName                 ='',
                theRetrievalExtents         =None,
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theAttributeConfigs         =someAttributeConfigs, 
                theTranslationsCaches       =theTranslationsCaches, 
                theResult                   =unResult, 
                theParentTraversalResult    =theParentTraversalResult, 
                theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                theWritePermissions         =theWritePermissions,
                theFeatureFilters           =None,
                theInstanceFilters          =None,
                theAdditionalParams         =theAdditionalParams                
            )
                 
            return unResult
            
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveElementoBasicInfoAndTranslations', theTimeProfilingResults)
                   
    

   
    
    security.declarePrivate( 'fRetrieveElementoTypeInfo')
    def fRetrieveElementoTypeInfo(self, theElement, theTranslationsCaches, theResult=None):
        
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
        
        
        if not theResult:
            return self
                
        someFactoryNamesAndTranslations = [ ]                                            
        for unPortalTypeName in theTypeNames:
            
            unPortalTypeTranslations = self.fMetaTypeNameTranslationsFromCache_into( 
                theMetaTypeName        =unPortalTypeName, 
                theTranslationsCaches  =theTranslationsCaches, 
                theResultDict          =None, 
                theContextualElement   =theContextElement,
                theAdditionalParams    =theAdditionalParams,
            )
            unContentIcon    = ''
            unArchetypeName  = ''
            if unPortalTypeTranslations:
                unArchetypeName = unPortalTypeTranslations.get( 'archetype_name', '')
                unContentIcon = unPortalTypeTranslations.get( 'content_icon', '')
               
            unFactoryResult = self.fNewVoidFactoryResult()
            unFactoryResult.update( { 
                'meta_type':            unPortalTypeName, 
                'type_translations':    unPortalTypeTranslations, 
                'content_icon':         unContentIcon ,
                'archetype_name':       unArchetypeName,
            } )                
            
            someFactoryNamesAndTranslations.append( unFactoryResult)
    
        theResult[ 'factories'] =  someFactoryNamesAndTranslations
        
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
    
     
    


# #############################################################
# Element access by UID
# 
    security.declarePrivate( 'fElementoPorUID')
    def fElementoPorUID( self, theUID, theContextualElement):
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
        if not unElemento:
            return None

        return unElemento    




    
    
    
    
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
    
     