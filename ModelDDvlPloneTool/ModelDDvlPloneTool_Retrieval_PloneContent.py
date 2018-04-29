# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval_PloneContent.py
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



import logging

from AccessControl          import ClassSecurityInfo
from Products.CMFCore       import permissions
from Products.CMFCore.utils import getToolByName

from PloneElement_TraversalConfig            import cPloneTypes
from PloneElement_TraversalConfig            import cPloneSubItemsParameters





class ModelDDvlPloneTool_Retrieval_PloneContent:
    """
    """
    security = ClassSecurityInfo()



    
    security.declarePrivate('fNewVoidElementResult_PloneContent')
    def fNewVoidElementResult_PloneContent(self):
        unResult = { 
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
            'traversals_by_name':       { },                                  
            'traversals':               [ ],                                  
            'cursor':                   None,                                 
            'owner_element':            None,                               
            'container_element':        None, 
            'read_permission':          False,                                
            'write_permission':         False,
            'add_permission':           False,
            'delete_permission':        False,
        }
        return unResult   
    

     
    
    
    
    
    security.declarePrivate('fNewVoidTraversalResult_PloneContent')
    def fNewVoidTraversalResult_PloneContent(self):
        unResult = { 
            'traversal_kind' :          'aggregation-plone_content', 
            'traversal_name' :          '', 
            'contains_collections' :    False, 
            'has_grandchildren':        False,
            'is_multivalued' :          True, 
            'relationship':             'objectValues',
            'inverse_relationship':     'contenedor',
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
            'candidates':               [],
            'elements_by_UID':          {},
            'elements_by_id':           {},
        }
        return unResult   
   

    
    
    security.declarePrivate('fPlonePortalTypeForMetaType')
    def fPlonePortalTypeForMetaType(self, theMetaType):
        if not theMetaType:
            return ''
        
        aPlonePortalTypeSpec = cPloneTypes.get( theMetaType, {})
        if not aPlonePortalTypeSpec:
            return theMetaType
        
        unPortalType = aPlonePortalTypeSpec.get( 'portal_type', '')
        
        return unPortalType
        
   
    
    
        
    
    
    security.declarePrivate('fDefaultPloneSubItemsParameters')
    def fDefaultPloneSubItemsParameters(self):
        return cPloneSubItemsParameters
    
    
    security.declarePrivate('fDefaultPloneSubItemsTypes')
    def fDefaultPloneSubItemsTypes(self, theContextualElement):
    
        somePloneTypes = [ ]
            
        somePloneSubItemsParameters =self.fDefaultPloneSubItemsParameters()
        if not somePloneSubItemsParameters:
            return somePloneTypes      
        
        for aPloneSubItemsParameter in somePloneSubItemsParameters:
            someAllowedTypes = aPloneSubItemsParameter[ 'allowed_types']
            if someAllowedTypes:
                for unAllowedType in someAllowedTypes:
                    unMetaType = unAllowedType.get( 'meta_type', '')
                    if unMetaType and not ( unMetaType in somePloneTypes):
                        somePloneTypes.append( unMetaType)

        return somePloneTypes
    
    
                
    
    security.declarePrivate('fRetrievePloneObjects')
    def fRetrievePloneObjects(self, 
        theTimeProfilingResults     =None, 
        theElement                  =None, 
        theTypeNames                =None,
        theCanReturnValues          =None, 
        theCheckedPermissionsCache  =None, 
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theAdditionalParams         =None):
        """Return elements of standard Plone archetypes (ATLink, ATDocument, ATImage, ATNewsItem).
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrievePloneObjects', theTimeProfilingResults)
                      
        try:
            
            somePloneElements = [ ]
            
            
            if ( theElement == None) :
                return somePloneElements
            
            if not theCanReturnValues:
                return somePloneElements
            
            somePloneTypes = self.fDefaultPloneSubItemsTypes( theElement)
            if not somePloneTypes:
                return somePloneElements   
            
            someContentTypes = []
            
            if theFeatureFilters and theFeatureFilters.get( 'types', []):
                unLimitToTypes = theFeatureFilters[ 'types']   
                for unType in unLimitToTypes:
                    if ( unType in somePloneTypes) and not ( unType in someContentTypes):
                        someContentTypes.append( unType)
            else:
                someContentTypes = somePloneTypes
            
            if not someContentTypes:
                return somePloneElements          
 
                        
            if theInstanceFilters and theInstanceFilters.get( 'UIDs', []):
                someLimitToUIDs = theInstanceFilters[ 'UIDs']   
                for anElementUID in someLimitToUIDs:
                    anElementByUID = self.fElementoPorUID( anElementUID, theContainerElement)
                    if anElementByUID:
                        anElementById = self.fElementoContenidoPorId( theContainerElement, anElementByUID.getId()) 
                        if anElementById and ( ( not someContentTypes) or ( anElementById.meta_type in someContentTypes)) and not ( anElementById in somePloneElements):
                            somePloneElements.append( anElementById)   
            else:                        
                someElements = theElement.objectValues( someContentTypes)
                if someElements:
                    somePloneElements.extend( someElements)
                
            return somePloneElements

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrievePloneObjects', theTimeProfilingResults)
    
 
                  
  
    
    security.declarePrivate('fRetrievePloneContent')
    def fRetrievePloneContent(self, 
        theTimeProfilingResults     =None,
        theContainerElement         =None, 
        thePloneSubItemsParameters  =None, 
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):
        """Retrieve a result structure for an element of a standard Plone archetype (ATLink, ATDocument, ATImage, ATNewsItem).
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrievePloneContent', theTimeProfilingResults)
                      
        try:
            if ( theContainerElement == None) :
                return None

            unPloneSubItemsParameters = thePloneSubItemsParameters
            if not unPloneSubItemsParameters:
                unPloneSubItemsParameters = self.fDefaultPloneSubItemsParameters()
                if not unPloneSubItemsParameters:
                    return None             
                                
            unTranslationsCaches        = theTranslationsCaches
            if not unTranslationsCaches:
                unTranslationsCaches = self.fCreateTranslationsCaches()
                
            unCheckedPermissionsCache   = theCheckedPermissionsCache
            if not unCheckedPermissionsCache:
                unCheckedPermissionsCache = self.fCreateCheckedPermissionsCache()
                
                
            unResult = self.fRetrieveTypeConfig(
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theContainerElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =theRetrievalExtents,
                theWritePermissions         =theWritePermissions,
                theFeatureFilters           ={ 'attrs': [ 'title', 'description'], 'aggregations': [], 'relations': [], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =unTranslationsCaches,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams
                )                
            if not unResult:
                return None             
                
            unCanReturnValues       = unResult[ 'read_permission']
            unCanReturnTraversals   = unCanReturnValues and unResult[ 'traverse_permission']
             
            if theRetrievalExtents and ( ( 'traversals' in theRetrievalExtents) or ( 'tree' in theRetrievalExtents)):
                unosRetrievalExtents = theRetrievalExtents[:]
                if ( 'traversals' in unosRetrievalExtents):
                    unosRetrievalExtents.remove( 'traversals')

                for aPloneSubItemsParameter in unPloneSubItemsParameters:
                    unTraversalName = aPloneSubItemsParameter[ 'traversal_name']
                    if ( not theFeatureFilters) or  ( not theFeatureFilters.get( 'aggregations', {})) or ( unTraversalName in theFeatureFilters[ 'aggregations']):
                        self.pRetrievePloneSubItems( 
                            theTimeProfilingResults     =theTimeProfilingResults,
                            theResult                   =unResult,
                            theContainerElement         =theContainerElement, 
                            thePloneSubItemsParameter   =aPloneSubItemsParameter, 
                            theCanReturnValues          =unCanReturnTraversals,
                            theRetrievalExtents         =unosRetrievalExtents,
                            theWritePermissions         =theWritePermissions,
                            theFeatureFilters           =theFeatureFilters, 
                            theInstanceFilters          =theInstanceFilters,
                            theTranslationsCaches       =unTranslationsCaches,
                            theCheckedPermissionsCache  =unCheckedPermissionsCache,
                            theAdditionalParams         =theAdditionalParams)                        
                      
            return unResult

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrievePloneContent', theTimeProfilingResults)
    
 
                
                
    security.declarePrivate('pRetrievePloneSubItems')
    def pRetrievePloneSubItems(self, 
        theTimeProfilingResults     =None,
        theResult                   =None,
        theContainerElement         =None, 
        thePloneSubItemsParameter   =None, 
        theCanReturnValues          =True,
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'pRetrievePloneSubItems', theTimeProfilingResults)

        try:
            
            if ( theContainerElement == None)  or not thePloneSubItemsParameter or not theResult:
                return self                                    
             
            unTraversalResult = self.fNewVoidTraversalResult_PloneContent()
            
            unTraversalName = thePloneSubItemsParameter[ 'traversal_name']
            unTraversalResult[ 'traversal_name']    = unTraversalName
            
            unCanReturnValues = theCanReturnValues
            unCanChangeValues = unCanReturnValues and theResult[ 'write_permission']
            if unCanReturnValues:
                unPloneReadPermission = thePloneSubItemsParameter[ 'plone_read_permission']
                if unPloneReadPermission and not self.fCheckElementPermission( theContainerElement, [ unPloneReadPermission,], theCheckedPermissionsCache):
                    unCanReturnValues   = False
                    unCanChangeValues   = False
                
                if  unCanReturnValues and unCanChangeValues and theWritePermissions and ( 'aggregations' in theWritePermissions):
                    unPloneWritePermission = thePloneSubItemsParameter[ 'plone_write_permission']
                    if unPloneReadPermission and not self.fCheckElementPermission( theContainerElement, [ unPloneWritePermission,], theCheckedPermissionsCache):
                        unCanChangeValues = False
                    
            
            unTraversalResult[ 'read_permission']   = unCanReturnValues
            unTraversalResult[ 'write_permission']  = unCanChangeValues
            
            unaTraversalLabelMsgId       = thePloneSubItemsParameter[ 'label_msgid']
            unaTraversalDescriptionMsgId = thePloneSubItemsParameter[ 'description_msgid']

            unTraversalTranslation   = self.getAttributeTranslationResultFromDomainAndMsgids( 'ModelDDvlPlone', unaTraversalLabelMsgId,   unaTraversalLabelMsgId, unaTraversalDescriptionMsgId, unaTraversalDescriptionMsgId , theContainerElement)
            unTraversalResult[ 'traversal_translations'] = unTraversalTranslation
            
            someAllowedTypesParameters = thePloneSubItemsParameter.get( 'allowed_types', [])
            for unAllowedTypeParameter in someAllowedTypesParameters:
                unTypeTranslation = self.getPloneTypeTranslationResultFromMsgIdMetatypeAndArchetype( unAllowedTypeParameter[ 'i18n_msgid'], unAllowedTypeParameter[ 'meta_type'], unAllowedTypeParameter[ 'archetype_name'], theContainerElement)
                if unTypeTranslation:
                    unTraversalResult[ 'factories'].append( {
                        'meta_type':         unAllowedTypeParameter[ 'meta_type'], 
                        'type_translations': unTypeTranslation, 
                        'content_icon':      unAllowedTypeParameter[ 'content_icon'],
                        'archetype_name':    unAllowedTypeParameter[ 'archetype_name'], 
                    })
                  
            unosDefaultAttributesTranslations = self.getTranslationsForDefaultAttributes( theContainerElement)
            unTitleColumnTranslation = unosDefaultAttributesTranslations.get( 'title', {})
            unDescriptionColumnTranslation = unosDefaultAttributesTranslations.get( 'description', {})
            unDetailsColumnTranslation = self.getAttributeTranslationResultFromDomainAndMsgids( 'ModelDDvlPlone', 'ModelDDvlPlone_PloneContent_attr_details_label', 'Detalles', 'ModelDDvlPlone_PloneContent_attr_details_label', 'Detalles',  theContainerElement)

            unosElementResults = [ ]        
            unTraversalResult.update( { 
                'traversal_kind' :          'aggregation-plone', 
                'traversal_config':         None, 
                'elements':                 unosElementResults, 
                'column_names':             [ 'title', 'description', 'details', ],
                'column_translations':      { 'title': unTitleColumnTranslation,  'description': unDescriptionColumnTranslation,  'details': unDetailsColumnTranslation, }
            })
             
            somePloneTypes = [ unTypeParameter[ 'meta_type'] for unTypeParameter in someAllowedTypesParameters]
            
            unLimitToTypes = []
            if theFeatureFilters and theFeatureFilters.get( 'types', []):
                unLimitToTypes = theFeatureFilters[ 'types']   
             
            someContentTypes = []
            if not unLimitToTypes:
                someContentTypes = somePloneTypes
            else:
                for unType in unLimitToTypes:
                    if unType in somePloneTypes:
                        someContentTypes.append( unType)
                        
            
            someLimitToUIDs = []
            if unCanReturnValues:
                if theInstanceFilters and theInstanceFilters.get( 'UIDs', []):
                    someLimitToUIDs = theInstanceFilters[ 'UIDs']   
                            
                if someLimitToUIDs:
                    someElements =  []
                    for anElementUID in someLimitToUIDs:
                        anElementByUID = self.fElementoPorUID( anElementUID, theContainerElement)
                        if anElementByUID:
                            anElementById = self.fElementoContenidoPorId( theContainerElement, anElementByUID.getId()) 
                            if anElementById and ( ( not someContentTypes) or ( anElementById.meta_type in someContentTypes)) and not ( anElementById in someElements):
                                someElements.append( anElementById)   
                else:                        
                    someElements = theContainerElement.objectValues( someContentTypes)

                for unElemento in someElements:
                    unElementResult = self.fRetrievePloneElement( 
                        theTimeProfilingResults     =theTimeProfilingResults,
                        theElement                  =unElemento,
                        thePloneSubItemsParameter   =thePloneSubItemsParameter, 
                        theCanChangeValues          =unCanChangeValues,
                        theRetrievalExtents         =theRetrievalExtents,
                        theWritePermissions         =theWritePermissions,
                        theFeatureFilters           =theFeatureFilters, 
                        theInstanceFilters          =theInstanceFilters,
                        theTranslationsCaches       =theTranslationsCaches,
                        theCheckedPermissionsCache  =theCheckedPermissionsCache,
                        theAdditionalParams         =theAdditionalParams
                    )

                    if unElementResult and unElementResult[ 'read_permission']:
                        unosElementResults.append( unElementResult)
                        # ACV 20090901 Removed to avoid producing huge traversal result dumps
                        # because each element result is included 3 times (in the ordered collection, and the two dicts)
                        # which is compounded when traversing a tree
                        #unTraversalResult[ 'elements_by_UID'][ unElementResult[ 'UID']] = unElementResult
                        #unTraversalResult[ 'elements_by_id' ][ unElementResult[ 'id' ]] = unElementResult
                        
                
            unTraversalResult[ 'num_elements'] = len( unosElementResults) 
            
            if ( not someLimitToUIDs) or len( unosElementResults):  
# ACV OJO  
# Esto funcionaba para  porque si no hay unosElementResults, tanto da que hubiera una traversal vacia, como que no,
# pues no se va a presentar el resultado, solo se usa para verificar si existe y se puede eliminar el elemento Plone
# No tenia Ni idea como funciona el fEliminarElementoPlone si no se añade el traversal result, cuando se busca por una UID ... ?????               
# ???? someLimitToUIDs used when checking before deletion one Plone element, 
                theResult[ 'traversals'].append( unTraversalResult)
                theResult[ 'traversals_by_name'][ unTraversalName] = unTraversalResult
                theResult[ 'traversal_names'].append( unTraversalName)

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pRetrievePloneSubItems', theTimeProfilingResults)
    
   

                
                
                
    security.declarePrivate('fRetrievePloneElement')
    def fRetrievePloneElement(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        thePloneSubItemsParameter   =None, 
        theCanChangeValues          =None,
        theRetrievalExtents         =None,
        theWritePermissions         =None,
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None):

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrievePloneElement', theTimeProfilingResults)

        try:
            if ( theElement == None):
                return None
                
            unTranslationsCaches        = theTranslationsCaches
            if not unTranslationsCaches:
                unTranslationsCaches = self.fCreateTranslationsCaches()
                
            unCheckedPermissionsCache   = theCheckedPermissionsCache
            if not unCheckedPermissionsCache:
                unCheckedPermissionsCache = self.fCreateCheckedPermissionsCache()
            
            unResult = self.fNewVoidElementResult_PloneContent()
            self.fNewResultForElement( theElement, unResult)
            
            unElementoMetaType = theElement.meta_type
            unTypeMsgId             = ''
            unContentIcon           = ''
            unPloneReadPermission   = ''
            unPloneWritePermission  = ''
            
            unHasFoundTypeParameter=False
            if thePloneSubItemsParameter and thePloneSubItemsParameter.get( 'allowed_types', []):  
                someAllowedTypesParameter = thePloneSubItemsParameter[ 'allowed_types']
                for unTypeParameter in someAllowedTypesParameter:
                    if unTypeParameter[ 'meta_type'] == unElementoMetaType:
                        unPloneReadPermission   = unTypeParameter[ 'plone_read_permission']
                        unPloneWritePermission  = unTypeParameter[ 'plone_write_permission']
                        unTypeMsgId             = unTypeParameter[ 'i18n_msgid']
                        unContentIcon           = unTypeParameter[ 'content_icon']
                        unHasFoundTypeParameter = True
                        break
            
            
            unArchetypeName = ''
            try:
                unArchetypeName = theElement.archetype_name
            except:
                None
            
            if not unHasFoundTypeParameter:
                     
                if not unTypeMsgId:
                    unTypeMsgId = unArchetypeName
                if not unTypeMsgId:
                    unTypeMsgId = unElementoMetaType
                    
                try:
                    unContentIcon = theElement.content_icon   
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
                unResult[ 'content_icon'] = unContentIcon                
             
            unTypeTranslations = self.getPloneTypeTranslationResultFromMsgIdMetatypeAndArchetype( unTypeMsgId, unElementoMetaType, unArchetypeName, theElement)
            if unTypeTranslations:
                unResult[ 'type_translations'] = unTypeTranslations
    
    
            unReadPermission = self.fCheckElementPermission( theElement, [ permissions.View, ], unCheckedPermissionsCache) == True
            if unReadPermission and unPloneReadPermission:
                unReadPermission = self.fCheckElementPermission( theElement, [ unPloneReadPermission, ], unCheckedPermissionsCache) == True
            unResult[ 'read_permission']  =  unReadPermission

            if theCanChangeValues:
                if theWritePermissions and ( 'plone' in theWritePermissions):
                    unWritePermission = self.fCheckElementPermission( theElement, [ permissions.ModifyPortalContent, ], unCheckedPermissionsCache) == True
                    if unWritePermission and unPloneWritePermission:
                        unWritePermission = self.fCheckElementPermission( theElement, [ unPloneWritePermission, ], unCheckedPermissionsCache) == True                        
                    unResult[ 'write_permission']  =  unWritePermission  
                    
                if theWritePermissions and ( 'delete_plone' in theWritePermissions):
                    unDeletePermission = self.fCheckElementPermission( theElement, [ permissions.DeleteObjects, ], unCheckedPermissionsCache) == True
                    unResult[ 'delete_permission']  =  unDeletePermission   
                
            unosDefaultAttributesTranslations = self.getTranslationsForDefaultAttributes( theElement)
            unContentUrlAttributeTranslation  = self.getAttributeTranslationResultFromDomainAndMsgids( 'ModelDDvlPlone', 'ModelDDvlPlone_PloneContent_attr_content_url_label',  'ModelDDvlPlone_PloneContent_attr_content_url_label', 'ModelDDvlPlone_PloneContent_attr_content_url_label',  'ModelDDvlPlone_PloneContent_attr_content_url_label', theElement)
            unImageUrlAttributeTranslation  = self.getAttributeTranslationResultFromDomainAndMsgids( 'ModelDDvlPlone', 'ModelDDvlPlone_PloneContent_attr_image_url_label',  'ModelDDvlPlone_PloneContent_attr_image_url_label', 'ModelDDvlPlone_PloneContent_attr_image_url_label',  'ModelDDvlPlone_PloneContent_attr_image_url_label', theElement)
            unContentWidthAttributeTranslation  = self.getAttributeTranslationResultFromDomainAndMsgids( 'ModelDDvlPlone', 'ModelDDvlPlone_PloneContent_attr_content_width_label',  'ModelDDvlPlone_PloneContent_attr_content_width_label', 'ModelDDvlPlone_PloneContent_attr_content_width_label',  'ModelDDvlPlone_PloneContent_attr_content_width_label', theElement)
            unContentHeightAttributeTranslation  = self.getAttributeTranslationResultFromDomainAndMsgids( 'ModelDDvlPlone', 'ModelDDvlPlone_PloneContent_attr_content_height_label',  'ModelDDvlPlone_PloneContent_attr_content_height_label', 'ModelDDvlPlone_PloneContent_attr_content_height_label',  'ModelDDvlPlone_PloneContent_attr_content_height_label', theElement)
             
            unAttributeName = 'title'
            unValueResult = self.fNewVoidValueResult()
            unResult[ 'values'].append(     unValueResult)    
            # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
            #
            # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
            unResult[ 'field_names'].append( unAttributeName)
            unResult[ 'non_text_field_names'].append( unAttributeName)
            unValue = theElement.Title()
            unUnicodeValue = self.fAsUnicode( unValue, theElement  ) 
            unValueResult.update({
                'attribute_name':           unAttributeName,
                'type':                     'String',
                'raw_value':                unValue,
                'value':                    unValue,
                'uvalue':                   unValue,
                'attribute_translations':   unosDefaultAttributesTranslations.get( unAttributeName, None),                    
            })
 
            unAttributeName = 'description'
            unValueResult = self.fNewVoidValueResult()
            unResult[ 'values'].append(     unValueResult)    
            # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
            #
            # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
            unResult[ 'field_names'].append( unAttributeName)
            unResult[ 'text_field_names'].append( unAttributeName)
            unValue = theElement.Description()
            unUnicodeValue = self.fAsUnicode( unValue, theElement  ) 
            unValueResult.update({
                'attribute_name':           unAttributeName,
                'type':                     'Text',
                'raw_value':                unValue,
                'value':                    unValue,
                'uvalue':                   unUnicodeValue,
                'attribute_translations':   unosDefaultAttributesTranslations.get( unAttributeName, None),                    
            })
           
            if theElement.meta_type == 'ATImage':
                unAttributeName             = 'content_url'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unValue = theElement.absolute_url()                
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'String',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unContentUrlAttributeTranslation,                    
                })

                unAttributeName             = 'width'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unValue = theElement.getWidth()                
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'int',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unContentWidthAttributeTranslation,                    
                })

                unAttributeName             = 'height'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unValue = theElement.getHeight()                
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'int',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unContentHeightAttributeTranslation,                    
                })
                
                
            elif theElement.meta_type == 'ATLink':
                unAttributeName             = 'content_url'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unValue = theElement.getRemoteUrl()
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'String',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unContentUrlAttributeTranslation,                    
                })


            elif theElement.meta_type == 'ATDocument':
                unAttributeName             = 'text'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'text_field_names'].append( unAttributeName)
                unValue = theElement.getText()
                unUnicodeValue = self.fAsUnicode( unValue, theElement  )                 
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'Text',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unUnicodeValue,
                    'attribute_translations':   unosDefaultAttributesTranslations.get( 'text', None),                    
                })
                
                
            elif theElement.meta_type == 'ATNewsItem':
                unAttributeName             = 'content_url'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unValue = theElement.absolute_url()
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'String',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unContentUrlAttributeTranslation,                    
                })

                unAttributeName             = 'image_url'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unValue = ''
                unaImage = theElement.getImage()
                if unaImage:
                    unValue = unaImage.absolute_url()
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'String',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unImageUrlAttributeTranslation,                    
                })
                
                unAttributeName                     = 'text'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'text_field_names'].append( unAttributeName)
                unValue = theElement.getText()
                unUnicodeValue = self.fAsUnicode( unValue, theElement  )                 
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'Text',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unUnicodeValue,
                    'attribute_translations':   unosDefaultAttributesTranslations.get( 'text', None),                    
                })
                
                unAttributeName             = 'width'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unaImage = theElement.getImage()
                unValue = 0
                if unaImage:
                    unValue = unaImage.width                
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'int',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unContentWidthAttributeTranslation,                    
                })

                unAttributeName             = 'height'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unaImage = theElement.getImage()
                unValue = 0
                if unaImage:
                    unValue = unaImage.height                
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'int',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unContentHeightAttributeTranslation,                    
                })

                
            elif theElement.meta_type == 'ATFile':                
                unAttributeName             = 'content_url'
                unValueResult = self.fNewVoidValueResult()
                unResult[ 'values'].append(     unValueResult)    
                # ACV 20090901 Dict population is postponed until completion of retrieval by services layer
                #
                # unResult[ 'values_by_name'][     unAttributeName] = unValueResult 
                unResult[ 'field_names'].append( unAttributeName)
                unResult[ 'non_text_field_names'].append( unAttributeName)
                unValue = theElement.getFilename()
                unValueResult.update({
                    'attribute_name':           unAttributeName,
                    'type':                     'String',
                    'raw_value':                unValue,
                    'value':                    unValue,
                    'uvalue':                   unValue,
                    'attribute_translations':   unContentUrlAttributeTranslation,                    
                })

            return unResult
            
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrievePloneElement', theTimeProfilingResults)
    

                   