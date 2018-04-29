# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_ImportExport_Constants.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'






cExportStatus_Error_MissingParameter_Element                            = 'ExportStatus_Error_MissingParameter_Element'
cExportStatus_Error_MissingParameter_ExportTypeConfigs                  = 'ExportStatus_Error_MissingParameter_ExportTypeConfigs'
cExportStatus_Error_Internal_MissingParameters                          = 'ExportStatus_Error_Internal_MissingParameters'
cExportStatus_Error_Internal_EncodingErrors                             = 'ExportStatus_Error_Internal_EncodingErrors'
cExportStatus_Error_Internal_CanNotCreateZipFile                        = 'ExportStatus_Error_Internal_CanNotCreateZipFile'
cExportStatus_Error_Internal_NoXMLStack                                 = 'ExportStatus_Error_Internal_NoXMLStack'
cExportStatus_Error_Internal_NoXMLDocument                              = 'ExportStatus_Error_Internal_NoXMLDocument'
cExportStatus_Error_Internal_EncodingError_ElementMetaTypeName          = 'ExportStatus_Error_Internal_EncodingError_ElementMetaTypeName'
cExportStatus_Error_Internal_EmptyEncodingResult_ElementMetaTypeName    = 'ExportStatus_Error_Internal_EmptyEncodingResult_ElementMetaTypeName'
cExportStatus_Error_Internal_EncodingError_AttrName                     = 'ExportStatus_Error_Internal_EncodingError_AttrName'
cExportStatus_Error_Internal_EmptyEncodingResult_AttrName               = 'ExportStatus_Error_Internal_EmptyEncodingResult_AttrName'
cExportStatus_Error_Internal_EncodedNameMissing_ElementMetaTypeName     = 'ExportStatus_Error_Internal_EncodedNameMissing_ElementMetaTypeName'
cExportStatus_Error_Internal_ObjectHasNoSchema                          = 'ExportStatus_Error_Internal_ObjectHasNoSchema'
cExportStatus_Error_Internal_EncodingError_AggregationName              = 'ExportStatus_Error_Internal_EncodingError_AggregationName'
cExportStatus_Error_Internal_EmptyEncodingResult_AggregationName        = 'ExportStatus_Error_Internal_EmptyEncodingResult_AggregationName'
cExportStatus_Error_Internal_EncodingError_RelationName                 = 'ExportStatus_Error_Internal_EncodingError_RelationName'
cExportStatus_Error_Internal_EmptyEncodingResult_RelationName           = 'ExportStatus_Error_Internal_EmptyEncodingResult_RelationName'
cExportStatus_Error_Internal_AttributeValueAccessException              = 'ExportStatus_Error_Internal_AttributeValueAccessException'
cExportStatus_Error_Internal_AttributeAccessorNotFound                  = 'ExportStatus_Error_Internal_AttributeAccessorNotFound'
cExportStatus_Error_Internal_MissingZipFile                             = 'ExportStatus_Error_Internal_MissingZipFile'


cImportStatus_Error_MissingParameter_ContainerObject                    = 'ImportStatus_Error_MissingParameter_ContainerObject'
cImportStatus_Error_MissingParameter_MDDImportTypeConfigs               = 'ImportStatus_Error_MissingParameter_MDDImportTypeConfigs'
cImportStatus_Error_MissingParameter_UploadedFile                       = 'ImportStatus_Error_MissingParameter_UploadedFile'
cImportStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval            = 'ImportStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval'
cImportStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators             = 'ImportStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators'
cImportStatus_Error_Internal_MissingTool_translation_service            = 'ImportStatus_Error_Internal_MissingTool_translation_service'
cImportStatus_Error_Parameter_UploadedFile_NotAZip                      = 'ImportStatus_Error_Parameter_UploadedFile_NotAZip'
cImportStatus_Error_Parameter_UploadedFile_ZipWithoutXMLFile            = 'ImportStatus_Error_Parameter_UploadedFile_ZipWithoutXMLFile'
cImportStatus_Error_EmptyXMLFile                                        = 'ImportStatus_Error_EmptyXMLFile'
cImportStatus_Error_DecodingXMLFileContents                             = 'ImportStatus_Error_DecodingXMLFileContentst'
cImportStatus_Error_BadXMLFile                                          = 'ImportStatus_Error_BadXMLFile'
cImportStatus_Error_NoRootXMLElements                                   = 'ImportStatus_Error_NoRootXMLElements'
cImportStatus_Error_Internal_NoContainerRetrieved                       = 'ImportStatus_Error_Internal_NoContainerRetrieved'
cImportStatus_Error_Internal_Refactor_NotInitialized                    = 'ImportStatus_Error_Internal_Refactor_NotInitialized'
cImportStatus_Error_Internal_Refactor_Failed                            = 'ImportStatus_Error_Internal_Refactor_Failed'
cImportStatus_Error_Exception                                           = 'ImportStatus_Error_Exception'
cImportStatus_Error_Container_NotReadable                               = 'ImportStatus_Error_Container_NotReadable'
cImportStatus_Error_Container_NotWritable                               = 'ImportStatus_Error_Container_NotWritable'
cImportStatus_Error_Import_NotAllowedInElement                          = 'ImportStatus_Error_Import_NotAllowedInElement'


cXMLElementName_CommentText = '#text'

cXMLAttributeName_PloneId   = 'ploneid'
cXMLAttributeName_PloneTitle = 'plonetitle'
cXMLAttributeName_PloneUID   = 'ploneuid'
cXMLAttributeName_PlonePath  = 'plonepath'
cXMLAttributeName_ContentType= 'contenttype'
# cXMLAttributeName_Filename   = 'filename'
                
cXMLPloneContentTypeValue_Text     = 'text/plain'
cXMLPloneContentTypeValue_TextRest = 'text/x-rst'


cXMLFilePostfix = 'xml'
cZIPFilePostfix = '.zip'

cXMLEncodingUTF8  = 'utf-8'