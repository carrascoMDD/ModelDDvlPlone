# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_ToDicts_Constants.py
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



# ############################################################
"""Configuration constants.

"""

cMDDLogToDictsErrors = True




# ############################################################
"""Key to store indexes.

"""
cMDDModelDict_theIndexes = 'theIndexes'





# ############################################################
"""Interface constants: dictionary keys and values.

"""

cMDDDictAttributeName_DictKind             = 'dict_kind'
cMDDDictAttributeName_DictKind_Element     = 'element'
cMDDDictAttributeName_DictKind_Attribute   = 'attribute'
cMDDDictAttributeName_DictKind_Aggregation = 'aggregation'
cMDDDictAttributeName_DictKind_Relation    = 'relation'
cMDDDictAttributeName_DictKind_Reference   = 'reference'
cMDDDictAttributeName_DictKind_ElementRef  = 'element_ref'

cMDDDictAttributeName_DictKinds = [
    cMDDDictAttributeName_DictKind_Element,     
    cMDDDictAttributeName_DictKind_Attribute,   
    cMDDDictAttributeName_DictKind_Aggregation, 
    cMDDDictAttributeName_DictKind_Relation,    
    cMDDDictAttributeName_DictKind_Reference,   
    cMDDDictAttributeName_DictKind_ElementRef,     
    
]



cMDDDictAttributeName_DictId               = 'dict_id'

cMDDDictAttributeName_ParentDictId         = 'parent_dict_id'
cMDDDictAttributeName_ReferencedDictId     = 'referenced_dict_id'

cMDDDictAttributeName_Element              = 'element'
cMDDDictAttributeName_IsRoot               = 'is_root'

cMDDDictAttributeName_PloneMetaType        = 'meta_type'

cMDDDictAttributeName_PloneId              = 'plone_id'
cMDDDictAttributeName_PloneTitle           = 'plone_title'
cMDDDictAttributeName_PloneURL             = 'plone_url'
cMDDDictAttributeName_PloneUID             = 'plone_uid'
cMDDDictAttributeName_PlonePath            = 'plone_path'
cMDDDictAttributeName_PhysicalPath         = 'physical_path'

cMDDDictAttributeName_IsCollection         = 'is_collection'
cMDDDictAttributeName_ContainsCollections  = 'contains_collections'
cMDDDictAttributeName_MultiplicityHigher   = 'multiplicity_higher'

cMDDDictAttributeName_Features             = 'features'
cMDDDictAttributeName_FeatureName          = 'feature_name'
cMDDDictAttributeName_Elements             = 'elements'
cMDDDictAttributeName_ElementRefs          = 'element_refs'



cMDDDictAttributeName_AttributeType        = 'attribute_type'
cMDDDictAttributeName_AttributeValue       = 'attribute_value'

cMDDDictAttributeName_ContentType          = 'content_type'

cMDDDictAttributeName_ImageId              = 'image_id'
cMDDDictAttributeName_ImageTitle           = 'image_title'
cMDDDictAttributeName_ImageFilename        = 'image_filename'

cMDDDictAttributeName_FileId               = 'file_id'
cMDDDictAttributeName_FileTitle            = 'file_title'
cMDDDictAttributeName_FileFilename         = 'file_filename'



cMDDDictPloneContentTypeValue_Text     = 'text/plain'
cMDDDictPloneContentTypeValue_TextRest = 'text/x-rst'



cMDDDictIndexableAttributeNames = [
    cMDDDictAttributeName_DictId,
    cMDDDictAttributeName_ParentDictId,
    cMDDDictAttributeName_ReferencedDictId,
    cMDDDictAttributeName_PloneMetaType,
    cMDDDictAttributeName_PloneId,
    cMDDDictAttributeName_PloneTitle,
    cMDDDictAttributeName_PloneUID,
    cMDDDictAttributeName_PlonePath,
    cMDDDictAttributeName_PhysicalPath,
]






cMDDDictIndexableDictKinds = [
    cMDDDictAttributeName_DictKind_Element,     
    cMDDDictAttributeName_DictKind_ElementRef,  
]



# ############################################################
"""Interface constants: errors.

"""

cMDDToDictsStatus_Error_MissingParameter_Element                            = 'ToDictsStatus_Error_MissingParameter_Element'
cMDDToDictsStatus_Error_MissingParameter_ToDictsTypeConfigs                 = 'ToDictsStatus_Error_MissingParameter_ToDictsTypeConfigs'
cMDDToDictsStatus_Error_MissingParameter_AttributeConfigs                   = 'ToDictsStatus_Error_MissingParameter_AttributeConfigs'
cMDDToDictsStatus_Error_MissingParameter_AttributeConfig                    = 'ToDictsStatus_Error_MissingParameter_AttributeConfig'
cMDDToDictsStatus_Error_MissingParameter_TraversalConfigs                   = 'ToDictsStatus_Error_MissingParameter_TraversalConfigs'
cMDDToDictsStatus_Error_MissingParameter_TraversalConfig                    = 'ToDictsStatus_Error_MissingParameter_TraversalConfig'
cMDDToDictsStatus_Error_MissingParameter_Context                            = 'ToDictsStatus_Error_MissingParameter_Context'
cMDDToDictsStatus_Error_Internal_MissingParameters                          = 'ToDictsStatus_Error_Internal_MissingParameters'
cMDDToDictsStatus_Error_Internal_NoCurrentElement                           = 'ToDictsStatus_Error_Internal_NoCurrentElement'
cMDDToDictsStatus_Error_Internal_NoToDictsStack                             = 'ToDictsStatus_Error_Internal_NoToDictsStack'
cMDDToDictsStatus_Error_Internal_NoToDictsReport                            = 'ToDictsStatus_Error_Internal_NoToDictsReport'
cMDDToDictsStatus_Error_Internal_NoToDictsErrors                            = 'ToDictsStatus_Error_Internal_NoToDictsErrors'
cMDDToDictsStatus_Error_Internal_NoDictsRoot                                = 'ToDictsStatus_Error_Internal_NoDictsRoot'
cMDDToDictsStatus_Error_Internal_NoObjectSchema                             = 'ToDictsStatus_Error_Internal_ObjectHasNoSchema'
cMDDToDictsStatus_Error_Internal_NoFieldInSchema                            = 'ToDictsStatus_Error_Internal_NoFieldInSchema'
cMDDToDictsStatus_Error_Internal_NoAttributeName                            = 'ToDictsStatus_Error_Internal_NoAttributeName'
cMDDToDictsStatus_Error_Internal_NoAggregationName                          = 'ToDictsStatus_Error_Internal_NoAggregationName'
cMDDToDictsStatus_Error_Internal_NoRelationName                             = 'ToDictsStatus_Error_Internal_NoRelationName'
cMDDToDictsStatus_Error_ToDictsRecursive_Failed                             = 'ToDictsStatus_Error_ToDictsRecursive_Failed'
cMDDToDictsStatus_Error_ToDicts_Attributes_Failed                           = 'ToDictsStatus_Error_ToDicts_Attributes_Failed'
cMDDToDictsStatus_Error_ToDicts_Attribute_Failed                            = 'ToDictsStatus_Error_ToDicts_Attribute_Failed'
cMDDToDictsStatus_Error_ToDicts_Traversals_Failed                           = 'ToDictsStatus_Error_ToDicts_Traversals_Failed'
cMDDToDictsStatus_Error_ToDicts_Aggregation_Failed                          = 'ToDictsStatus_Error_ToDicts_Aggregation_Failed'
cMDDToDictsStatus_Error_ToDicts_Relation_Failed                             = 'ToDictsStatus_Error_ToDicts_Relation_Failed'
cMDDToDictsStatus_Error_ToDictsRecursive_ErrorsOccurred                     = 'ToDictsStatus_Error_ToDictsRecursive_ErrorsOccurred'
cMDDToDictsStatus_Error_Internal_ObjectHasNoSchema                          = 'ToDictsStatus_Error_Internal_ObjectHasNoSchema'
cMDDToDictsStatus_Error_Internal_AttributeValueAccessException              = 'ToDictsStatus_Error_Internal_AttributeValueAccessException'
cMDDToDictsStatus_Error_Internal_AttributeAccessorNotFound                  = 'ToDictsStatus_Error_Internal_AttributeAccessorNotFound'
cMDDToDictsStatus_Error_ToDicts_NotAllowedInElement                         = 'ToDictsStatus_Error_ToDicts_NotAllowedInElement'
cMDDToDictsStatus_Error_Failed_Factory_ForElement                           = 'ToDictsStatus_Error_Failed_Factory_ForElement'
cMDDToDictsStatus_Error_Failed_Factory_ForAttribute                         = 'ToDictsStatus_Error_Failed_Factory_ForAttribute'
cMDDToDictsStatus_Error_Failed_Factory_ForAggregation                       = 'ToDictsStatus_Error_Failed_Factory_ForAggregation'
cMDDToDictsStatus_Error_Failed_Factory_ForRelation                          = 'ToDictsStatus_Error_Failed_Factory_ForRelation'
cMDDToDictsStatus_Error_Failed_Factory_ForReference                         = 'ToDictsStatus_Error_Failed_Factory_ForReference'
cMDDToDictsStatus_Error_Failed_Factory_ForElementRef                        = 'ToDictsStatus_Error_Failed_Factory_ForElementRef'

cMDDToDictsStatus_Error_Failed_Attribute_UnknownAttributeType               = 'ToDictsStatus_Error_Failed_Attribute_UnknownAttributeType'






            
                         