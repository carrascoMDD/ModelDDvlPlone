# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Mutators_Constants.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Model Driven Development sl and Antonio Carrasco Valero
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




# #############################################
"""Configuraton value should be in ModelDDvlPloneTool Preferences.

"""
cMaxChangeMillisDifference_ForSameEntries = 60 * 1000 # ACV OJO in debug. For runtime make it 100 ms





# #############################################
"""Token symbols for change entries representation on plone elements, abbreviated and long.

"""
cModificationKind_DeletePloneSubElement = 'DeletePloneSubElement'
cModificationKind_MovePloneSubObject    = 'MovePloneSubObject'

cModificationKind_DeletePloneSubElement_abbr = 'dpl'
cModificationKind_MovePloneSubObject_abbr    = 'mvp'




# #############################################
"""Token symbols for change entries representation, abbreviated and long.

"""

cModificationKind_ChangeValues         = 'Change Values'
cModificationKind_MoveSubObject        = 'Move Sub Object'
cModificationKind_MoveReferencedObject = 'Move Referenced Object'
cModificationKind_Link                 = 'Link'
cModificationKind_Unlink               = 'Unlink'
cModificationKind_DeleteSubElement     = 'Delete SubElement'
cModificationKind_Delete               = 'Delete'
cModificationKind_CreateSubElement     = 'Create SubElement'
cModificationKind_Create               = 'Create'
cModificationKind_Process              = 'Process'

cModificationKinds = [
    cModificationKind_ChangeValues,
    cModificationKind_MoveSubObject,
    cModificationKind_MoveReferencedObject,
    cModificationKind_Link,
    cModificationKind_Unlink,
    cModificationKind_DeleteSubElement,
    cModificationKind_Delete,
    cModificationKind_CreateSubElement,
    cModificationKind_Create,
    cModificationKind_DeletePloneSubElement,
    cModificationKind_Process,
]



cModificationKind_ChangeValues_abbr         = 'chg'
cModificationKind_MoveSubObject_abbr        = 'mvs'
cModificationKind_MoveReferencedObject_abbr = 'mvr'
cModificationKind_Link_abbr                 = 'lnk'
cModificationKind_Unlink_abbr               = 'uln'
cModificationKind_DeleteSubElement_abbr     = 'des'
cModificationKind_Delete_abbr               = 'del'
cModificationKind_CreateSubElement_abbr     = 'crs'
cModificationKind_Create_abbr               = 'cre'
cModificationKind_MovePloneSubObject_abbr   = 'mvp'
cModificationKind_Process_abbr              = 'pro'

cModificationKinds_Abbreviated = [
    cModificationKind_ChangeValues_abbr,
    cModificationKind_MoveSubObject_abbr,
    cModificationKind_MoveReferencedObject_abbr,
    cModificationKind_Link_abbr,
    cModificationKind_Unlink_abbr,
    cModificationKind_DeleteSubElement_abbr,
    cModificationKind_Delete_abbr,
    cModificationKind_CreateSubElement_abbr,
    cModificationKind_Create_abbr,
    cModificationKind_MovePloneSubObject_abbr,
    cModificationKind_Process_abbr,
]



cModificationKinds_AbbreviationsByName = {
    cModificationKind_ChangeValues:            cModificationKind_ChangeValues_abbr,
    cModificationKind_MoveSubObject:           cModificationKind_MoveSubObject_abbr,
    cModificationKind_MoveReferencedObject:    cModificationKind_MoveReferencedObject_abbr,
    cModificationKind_Link:                    cModificationKind_Link_abbr,
    cModificationKind_Unlink:                  cModificationKind_Unlink_abbr,
    cModificationKind_DeleteSubElement:        cModificationKind_DeleteSubElement_abbr,
    cModificationKind_Delete:                  cModificationKind_Delete_abbr,
    cModificationKind_CreateSubElement:        cModificationKind_CreateSubElement_abbr,
    cModificationKind_Create:                  cModificationKind_Create_abbr,
    cModificationKind_DeletePloneSubElement:   cModificationKind_DeletePloneSubElement_abbr,
    cModificationKind_MovePloneSubObject:      cModificationKind_MovePloneSubObject_abbr,
    cModificationKind_Process:                 cModificationKind_Process_abbr,
    
}

cModificationKinds_ByAbbreviation = dict( [ ( anAbbr, aKind) for aKind, anAbbr in cModificationKinds_AbbreviationsByName.items()])


    
cChangeDetails_ChangeKind              = 'kind'
cChangeDetails_UserId                  = 'user'
cChangeDetails_ChangeDate              = 'ms'
cChangeDetails_Details                 = 'dets'
cChangeDetails_ChangeCounter           = 'ctr'
cChangeDetails_NewFieldValue           = 'newv'
cChangeDetails_FieldChanges            = 'flds'
cChangeDetails_Relation                = 'rel'
cChangeDetails_TargetPath              = 'tpath'
cChangeDetails_TargetUID               = 'tuid'
cChangeDetails_TargetTitle             = 'ttit'
cChangeDetails_NewElementTitle         = 'ntit'
cChangeDetails_NewElementId            = 'nid'
cChangeDetails_NewElementUID           = 'nuid'
cChangeDetails_NewElementMetaType      = 'nmt'
cChangeDetails_NewElementArchetypeName = 'nar'
cChangeDetails_DeletedElementTitle     = 'dtit'
cChangeDetails_DeletedElementId        = 'did'
cChangeDetails_DeletedElementPath      = 'dph'
cChangeDetails_DeletedElementUID       = 'duid'
cChangeDetails_DeletedElementMetaType  = 'dty'
cChangeDetails_DeletedElementArchetypeName='dar'
cChangeDetails_MovedElementTitle       = 'mtit'
cChangeDetails_MovedElementId          = 'mid'
cChangeDetails_MovedElementPath        = 'mph'
cChangeDetails_MovedElementUID         = 'muid'
cChangeDetails_MovedElementMetaType    = 'mty'
cChangeDetails_MovedElementArchetypeName='mar'
cChangeDetails_IncludedDeleted         = 'dele'
cChangeDetails_Position                = 'pos'
cChangeDetails_Delta                   = 'delta'
cChangeDetails_TraversalName           = 'trav'
cChangeDetails_ProcessName             = 'proc'
cChangeDetails_ProcessParameters       = 'parms'


cChangeDetails_keys = [
    cChangeDetails_ChangeKind,
    cChangeDetails_UserId,
    cChangeDetails_ChangeDate,
    cChangeDetails_Details,
    cChangeDetails_ChangeCounter,
    cChangeDetails_NewFieldValue, 
    cChangeDetails_FieldChanges,  
    cChangeDetails_Relation,      
    cChangeDetails_TargetPath,    
    cChangeDetails_TargetTitle,     
    cChangeDetails_TargetUID,     
    cChangeDetails_NewElementTitle,   
    cChangeDetails_NewElementId,   
    cChangeDetails_NewElementUID,
    cChangeDetails_NewElementMetaType,
    cChangeDetails_NewElementArchetypeName,
    cChangeDetails_DeletedElementTitle,        
    cChangeDetails_DeletedElementId,        
    cChangeDetails_DeletedElementPath,      
    cChangeDetails_DeletedElementUID,       
    cChangeDetails_DeletedElementMetaType,  
    cChangeDetails_DeletedElementArchetypeName,   
    cChangeDetails_MovedElementTitle,        
    cChangeDetails_MovedElementId,        
    cChangeDetails_MovedElementPath,      
    cChangeDetails_MovedElementUID,       
    cChangeDetails_MovedElementMetaType,  
    cChangeDetails_MovedElementArchetypeName,   
    cChangeDetails_IncludedDeleted,
    cChangeDetails_Position,
    cChangeDetails_Delta,
    cChangeDetails_TraversalName,
    cChangeDetails_ProcessName,
    cChangeDetails_ProcessParameters,
]


cChangeDetails_ChangeKind_long                        = 'Kind'
cChangeDetails_UserId_long                            = 'User Id'
cChangeDetails_ChangeDate_long                        = 'Date'
cChangeDetails_Details_long                           = 'Details'
cChangeDetails_ChangeCounter_long                     = 'Counter'
cChangeDetails_NewFieldValue_long                     = 'New Field Value' 
cChangeDetails_FieldChanges_long                      = 'Field Changes'  
cChangeDetails_Relation_long                          = 'Relation'      
cChangeDetails_TargetPath_long                        = 'Target Path'    
cChangeDetails_TargetTitle_long                       = 'Target Title'     
cChangeDetails_TargetUID_long                         = 'Target UID'     
cChangeDetails_NewElementTitle_long                   = 'New Element Title'   
cChangeDetails_NewElementId_long                      = 'New Element Id'   
cChangeDetails_NewElementUID_long                     = 'New Element UID'
cChangeDetails_NewElementMetaType_long                = 'New Element MetaType'
cChangeDetails_NewElementArchetypeName_long           = 'New Element ArchetypeName'
cChangeDetails_DeletedElementTitle_long               = 'Deleted Element Title'        
cChangeDetails_DeletedElementId_long                  = 'Deleted Element Id'        
cChangeDetails_DeletedElementPath_long                = 'Deleted Element Path'      
cChangeDetails_DeletedElementUID_long                 = 'Deleted Element UID'       
cChangeDetails_DeletedElementMetaType_long            = 'Deleted Element MetaType'  
cChangeDetails_DeletedElementArchetypeName_long       = 'Deleted Element ArchetypeName'   
cChangeDetails_MovedElementTitle_long                 = 'Moved Element Title'        
cChangeDetails_MovedElementId_long                    = 'Moved Element Id'        
cChangeDetails_MovedElementPath_long                  = 'Moved Element Path'      
cChangeDetails_MovedElementUID_long                   = 'Moved Element UID'       
cChangeDetails_MovedElementMetaType_long              = 'Moved Element MetaType'  
cChangeDetails_MovedElementArchetypeName_long         = 'Moved Element ArchetypeName'   
cChangeDetails_IncludedDeleted_long                   = 'Included Deleted'
cChangeDetails_Position_long                          = 'Position'
cChangeDetails_Delta_long                             = 'Delta'
cChangeDetails_TraversalName_long                     = 'Traversal Name'
cChangeDetails_ProcessName_long                       = 'Process Name'
cChangeDetails_ProcessParameters_long                 = 'Process Parameters'
    
    

cChangeDetails_long_byAbbreviation = {    
    cChangeDetails_ChangeKind:                      cChangeDetails_ChangeKind_long,                  
    cChangeDetails_UserId:                          cChangeDetails_UserId_long,                      
    cChangeDetails_ChangeDate:                      cChangeDetails_ChangeDate_long,                  
    cChangeDetails_Details:                         cChangeDetails_Details_long,                     
    cChangeDetails_ChangeCounter:                   cChangeDetails_ChangeCounter_long,               
    cChangeDetails_NewFieldValue:                   cChangeDetails_NewFieldValue_long,               
    cChangeDetails_FieldChanges:                    cChangeDetails_FieldChanges_long,                
    cChangeDetails_Relation:                        cChangeDetails_Relation_long,                    
    cChangeDetails_TargetPath:                      cChangeDetails_TargetPath_long,                  
    cChangeDetails_TargetTitle:                     cChangeDetails_TargetTitle_long,                   
    cChangeDetails_TargetUID:                       cChangeDetails_TargetUID_long,                   
    cChangeDetails_NewElementTitle:                 cChangeDetails_NewElementTitle_long,                
    cChangeDetails_NewElementId:                    cChangeDetails_NewElementId_long,                
    cChangeDetails_NewElementUID:                   cChangeDetails_NewElementUID_long,               
    cChangeDetails_NewElementMetaType:              cChangeDetails_NewElementMetaType_long,          
    cChangeDetails_NewElementArchetypeName:         cChangeDetails_NewElementArchetypeName_long,     
    cChangeDetails_DeletedElementTitle:             cChangeDetails_DeletedElementTitle_long,            
    cChangeDetails_DeletedElementId:                cChangeDetails_DeletedElementId_long,            
    cChangeDetails_DeletedElementPath:              cChangeDetails_DeletedElementPath_long,          
    cChangeDetails_DeletedElementUID:               cChangeDetails_DeletedElementUID_long,           
    cChangeDetails_DeletedElementMetaType:          cChangeDetails_DeletedElementMetaType_long,      
    cChangeDetails_DeletedElementArchetypeName:     cChangeDetails_DeletedElementArchetypeName_long, 
    cChangeDetails_MovedElementTitle:               cChangeDetails_MovedElementTitle_long,              
    cChangeDetails_MovedElementId:                  cChangeDetails_MovedElementId_long,              
    cChangeDetails_MovedElementPath:                cChangeDetails_MovedElementPath_long,            
    cChangeDetails_MovedElementUID:                 cChangeDetails_MovedElementUID_long,             
    cChangeDetails_MovedElementMetaType:            cChangeDetails_MovedElementMetaType_long,        
    cChangeDetails_MovedElementArchetypeName:       cChangeDetails_MovedElementArchetypeName_long,   
    cChangeDetails_IncludedDeleted:                 cChangeDetails_IncludedDeleted_long,             
    cChangeDetails_Position:                        cChangeDetails_Position_long,                    
    cChangeDetails_Delta:                           cChangeDetails_Delta_long,                       
    cChangeDetails_TraversalName:                   cChangeDetails_TraversalName_long,    
    cChangeDetails_ProcessName:                     cChangeDetails_ProcessName_long,
    cChangeDetails_ProcessParameters:               cChangeDetails_ProcessParameters_long,
}    
        
    







