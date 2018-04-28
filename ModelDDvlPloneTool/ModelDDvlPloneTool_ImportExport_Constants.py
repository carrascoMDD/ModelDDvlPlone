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






cExportStatus_Error_MissingParameter_Element                            = 'Error_MissingParameter_Element'
cExportStatus_Error_MissingParameter_ExportTypeConfigs                  = 'Error_MissingParameter_ExportTypeConfigs'
cExportStatus_Error_Internal_MissingParameters                          = 'Error_Internal_MissingParameters'
cExportStatus_Error_Internal_EncodingErrors                             = 'Error_Internal_EncodingErrors'
cExportStatus_Error_Internal_CanNotCreateZipFile                        = 'Error_Internal_CanNotCreateZipFile'
cExportStatus_Error_Internal_NoXMLStack                                 = 'Error_Internal_NoXMLStack'
cExportStatus_Error_Internal_NoXMLDocument                              = 'Error_Internal_NoXMLDocument'
cExportStatus_Error_Internal_EncodingError_ElementMetaTypeName          = 'Error_Internal_EncodingError_ElementMetaTypeName'
cExportStatus_Error_Internal_EmptyEncodingResult_ElementMetaTypeName    = 'Error_Internal_EmptyEncodingResult_ElementMetaTypeName'
cExportStatus_Error_Internal_EncodingError_AttrName                     = 'Error_Internal_EncodingError_AttrName'
cExportStatus_Error_Internal_EmptyEncodingResult_AttrName               = 'Error_Internal_EmptyEncodingResult_AttrName'
cExportStatus_Error_Internal_EncodedNameMissing_ElementMetaTypeName     = 'Error_Internal_EncodedNameMissing_ElementMetaTypeName'
cExportStatus_Error_Internal_ObjectHasNoSchema                          = 'Error_Internal_ObjectHasNoSchema'
cExportStatus_Error_Internal_EncodingError_AggregationName              = 'Error_Internal_EncodingError_AggregationName'
cExportStatus_Error_Internal_EmptyEncodingResult_AggregationName        = 'Error_Internal_EmptyEncodingResult_AggregationName'
cExportStatus_Error_Internal_EncodingError_RelationName                 = 'Error_Internal_EncodingError_RelationName'
cExportStatus_Error_Internal_EmptyEncodingResult_RelationName           = 'Error_Internal_EmptyEncodingResult_RelationName'
cExportStatus_Error_Internal_AttributeValueAccessException              = 'Error_Internal_AttributeValueAccessException'
cExportStatus_Error_Internal_AttributeAccessorNotFound                  = 'Error_Internal_AttributeAccessorNotFound'
cExportStatus_Error_Internal_MissingZipFile                             = 'Error_Internal_MissingZipFile'


cImportStatus_Error_MissingParameter_Element                            = 'Error_MissingParameter_Element'
cImportStatus_Error_MissingParameter_ImportTypeConfigs                  = 'Error_MissingParameter_ImportTypeConfigs'
cImportStatus_Error_MissingParameter_UploadedFile                       = 'Error_MissingParameter_UploadedFile'
cImportStatus_Error_Parameter_UploadedFile_NotAZip                      = 'Error_Parameter_UploadedFile_NotAZip'
cImportStatus_Error_Parameter_UploadedFile_ZipWithoutXMLFile            = 'Error_Parameter_UploadedFile_ZipWithoutXMLFile'
cImportStatus_Error_EmptyXMLFile                                        = 'Error_EmptyXMLFile'
cImportStatus_Error_DecodingXMLFileContents                             = 'Error_DecodingXMLFileContentst'
cImportStatus_Error_BadXMLFile                                          = 'Error_BadXMLFile'
cImportStatus_Error_NoRootXMLElements                                   = 'Error_NoRootXMLElements'




cXMLAttributeName_PloneTitle = 'plonetitle'
cXMLAttributeName_PloneUID   = 'ploneuid'
cXMLAttributeName_PlonePath  = 'plonepath'
cXMLAttributeName_ContentType= 'plonecontenttype'
                
             
cXMLFilePostfix = 'xml'
cZIPFilePostfix = '.zip'

cXMLEncodingUTF8  = 'utf-8'