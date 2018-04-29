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



cMinimumTimeSlice_Minimum     = 10
cMinimumTimeSlice_Maximum     = 5000
cYieldMilliseconds_Minimum    = 10
cYieldMilliseconds_Maximum    = 5000

cExportForcedRootId = 'modeldd'


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
cExportStatus_Error_Export_NotAllowedInElement                          = 'ExportStatus_Error_Export_NotAllowedInElement'

cImportStatus_Error_MissingParameter_ContainerObject                    = 'ImportStatus_Error_MissingParameter_ContainerObject'
cImportStatus_Error_MissingParameter_MDDImportTypeConfigs               = 'ImportStatus_Error_MissingParameter_MDDImportTypeConfigs'
cImportStatus_Error_MissingParameter_UploadedFile                       = 'ImportStatus_Error_MissingParameter_UploadedFile'
cImportStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval            = 'ImportStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval'
cImportStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators             = 'ImportStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators'
cImportStatus_Error_Internal_MissingTool_translation_service            = 'ImportStatus_Error_Internal_MissingTool_translation_service'
cImportStatus_Error_Parameter_UploadedFile_NotAZip                      = 'ImportStatus_Error_Parameter_UploadedFile_NotAZip'
cImportStatus_Error_Parameter_UploadedFile_NotAZipNotAXML               = 'ImportStatus_Error_Parameter_UploadedFile_NotAZipNotAXML'
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
cImportStatus_Error_NoXMLEncoding                                       = 'ImportStatus_Error_NoXMLEncoding'
cImportStatus_Error_XMLEncodingUnknown                                  = 'ImportStatus_Error_XMLEncodingUnknown'

cNewVersionStatus_Error_Failure_Retrieving_AllVersions                  = 'NewVersionStatus_Error_Failure_Retrieving_AllVersions'
cNewVersionStatus_Error_MissingParameter_OriginalObject                 = 'NewVersionStatus_Error_MissingParameter_OriginalObject'
cNewVersionStatus_Error_ContainerReport_Missing                         = 'NewVersionStatus_Error_ContainerReport_Missing'
cNewVersionStatus_Error_ContainerReport_NotAllowed                      = 'NewVersionStatus_Error_ContainerReport_NotAllowed'
cNewVersionStatus_Error_Container_NotFound                              = 'NewVersionStatus_Error_Container_NotFound'
cNewVersionStatus_Error_Title_AlreadyExists                             = 'NewVersionStatus_Error_Title_AlreadyExists'
cNewVersionStatus_Error_Id_AlreadyExists                                = 'NewVersionStatus_Error_Id_AlreadyExists'
cNewVersionStatus_Error_VersionName_AlreadyExists                       = 'NewVersionStatus_Error_VersionName_AlreadyExists'
cNewVersionStatus_Error_MissingParameter_ContainerKind                  = 'NewVersionStatus_Error_MissingParameter_ContainerKind'
cNewVersionStatus_Error_MissingParameter_VersionName                    = 'NewVersionStatus_Error_MissingParameter_VersionName'
cNewVersionStatus_Error_MissingParameter_MDDImportTypeConfigs           = 'NewVersionStatus_Error_MissingParameter_MDDImportTypeConfigs'
cNewVersionStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval        = 'NewVersionStatus_Error_MissingTool_ModelDDvlPloneTool_Retrieval'
cNewVersionStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators         = 'NewVersionStatus_Error_MissingTool_ModelDDvlPloneTool_Mutators'
cNewVersionStatus_Error_Exception                                       = 'NewVersionStatus_Error_Exception'
cNewVersionStatus_Error_Internal_NoOriginalParentRetrieved              = 'NewVersionStatus_Error_Internal_NoOriginalParentRetrieved'
cNewVersionStatus_Error_NewVersion_NotAllowedInElement                  = 'NewVersionStatus_Error_NewVersion_NotAllowedInElement'
cNewVersionStatus_Error_Original_NotReadable                            = 'NewVersionStatus_Error_Original_NotReadable'
cNewVersionStatus_Error_Container_NotWritable                           = 'NewVersionStatus_Error_Container_NotWritable'
cNewVersionStatus_Error_Internal_Refactor_NotInitialized                = 'NewVersionStatus_Error_Internal_Refactor_NotInitialized'
cNewVersionStatus_Error_Internal_Refactor_Failed                        = 'NewVersionStatus_Error_Internal_Refactor_Failed'
cNewVersionStatus_Error_Internal_NoOriginalRetrieved                    = 'NewVersionStatus_Error_Internal_NoOriginalRetrieved'
cNewVersionStatus_Error_ObjectNotCreated                                = 'NewVersionStatus_Error_ObjectNotCreated'
cNewVersionStatus_Error_CreatedObjectNotFound                           = 'NewVersionStatus_Error_CreatedObjectNotFound'
cNewVersionStatus_Error_CreatedObjectResultFaulure                      = 'NewVersionStatus_Error_CreatedObjectResultFaulure'
cNewVersionStatus_Error_Internal_MissingTool_translation_service        = 'NewVersionStatus_Error_Internal_MissingTool_translation_service'
cNewVersionStatus_Error_Internal_NoMutator_version_field_storage        = 'NewVersionStatus_Error_Internal_NoMutator_version_field_storage'
cNewVersionStatus_Error_Internal_NoMutator_version_comment_field_storage= 'NewVersionStatus_Error_Internal_NoMutator_vversion_comment_field_storage'


cFakeUIDForPloneSite = '-P-l-o-n-e-S-i-t-e-'

cPloneSiteMetaTypes = [ 'Portal Site', 'Plone Site', ]



cXMLElementName_CommentText = '#text'

cXMLAttributeName_PloneId   = 'ploneid'
cXMLAttributeName_PloneTitle = 'plonetitle'
cXMLAttributeName_PloneUID   = 'ploneuid'
cXMLAttributeName_PlonePath  = 'plonepath'
cXMLAttributeName_ContentType= 'contenttype'
cXMLAttributeName_IsReference  = 'isreference'

cXMLAttributeValue_IsReference_True = 'True'
                
cXMLAttributeName_IsCollection  = 'iscollection'
cXMLAttributeValue_IsCollection_True = 'True'

cXMLAttributeName_IsAggregation  = 'isaggregation'
cXMLAttributeValue_IsAggregation_True = 'True'

cXMLAttributeName_IsRelation  = 'isrelation'
cXMLAttributeValue_IsRelation_True = 'True'


cXMLPloneContentTypeValue_Text     = 'text/plain'
cXMLPloneContentTypeValue_TextRest = 'text/x-rst'


cXMLFilePostfix = 'xml'
cZIPFilePostfix = '.zip'


cXMLRelatedMetaTypePostfix = '_RelRef'








cEncodingASCII= 'ascii'
cEncodingUTF8   = 'utf-8'
cEncodingUTF16  = 'utf-16'
cEncodingLatin  = 'ISO-8859-1'

cEncodingUnicodeEscape   = 'unicode_escape'


cDefaultEncodingForXMLImport = cEncodingUTF8

cEncodingErrorHandleMode_Strict = 'strict'



cUTFEncodingsForAllLanguages = [ 
    [ cEncodingUnicodeEscape, cEncodingUnicodeEscape, []], 
    [ cEncodingUTF8, cEncodingUTF8, []], 
    [ u'utf_7', u'U7,unicode-1-1-utf-7', []], 
     [ u'utf_8_sig', u'utf_8_sig', []], 
    [ cEncodingUTF16, cEncodingUTF16, []],
    [ u'utf_16_be', u'UTF-16BE', [ u'(BMP only)']], 
    [ u'utf_16_le', u'UTF-16LE', [ u'(BMP only)']], 
    [ u'utf_32_be', u'UTF-32BE', [ u'(BMP only)']], 
    [ u'utf_32_le', u'UTF-32LE', [ u'(BMP only)']], 
]


cDefaultEncodingsSourceMap = [
    [ u'ascii', u'646,us-ascii', u'English', u'',],
    [ u'big5', u'big5-tw,csbig5', u'Traditional Chinese', u'zh',],
    [ u'big5hkscs', u'big5-hkscs,hkscs', u'Traditional Chinese', u'zh',],
    [ u'cp037', u'IBM037,IBM039', u'English', u'',],
    [ u'cp424', u'EBCDIC-CP-HE,IBM424', u'Hebrew', u'he',],
    [ u'cp437', u'437,IBM437', u'English', u'',],
    [ u'cp500', u'EBCDIC-CP-BE,EBCDIC-CP-CH,IBM500', u'Western Europe', u'',],
    [ u'cp737', u'', u'Greek', u'el',],
    [ u'cp775', u'IBM775', u'Baltic languages', u'lv,lt',],
    [ u'cp850', u'850,IBM850', u'Western Europe', u'',],
    [ u'cp852', u'852,IBM852', u'Central and Eastern Europe', u'',],
    [ u'cp855', u'855,IBM855', u'Bulgarian,Byelorussian,Macedonian,Russian,Serbian', u'bg,be,mk,ru,sr',],
    [ u'cp856', u'cp856', u'Hebrew', u'he',],
    [ u'cp857', u'857,IBM857', u'Turkish', u'tr',],
    [ u'cp860', u'860,IBM860', u'Portuguese', u'pt',],
    [ u'cp861', u'861,CP-IS,IBM861', u'Icelandic', u'is',],
    [ u'cp862', u'862,IBM862', u'Hebrew', u'he',],
    [ u'cp863', u'863,IBM863', u'Canadian', u'en-ca',],
    [ u'cp864', u'IBM864', u'Arabic', u'ar',],
    [ u'cp865', u'865,IBM865', u'Danish,Norwegian', u'da,no,nn',],
    [ u'cp866', u'866,IBM866', u'Russian', u'ru',],
    [ u'cp869', u'869,CP-GR,IBM869', u'Greek', u'el',],
    [ u'cp874', u'cp874', u'Thai', u'th',],
    [ u'cp875', u'cp875', u'Greek', u'el',],
    [ u'cp932', u'932,ms932,mskanji,ms-kanji', u'Japanese', u'ja',],
    [ u'cp949', u'949,ms949,uhc', u'Korean', u'ko',],
    [ u'cp950', u'950,ms950', u'Traditional Chinese', u'zh',],
    [ u'cp1006', u'cp1006', u'Urdu', u'ur',],
    [ u'cp1026', u'ibm1026', u'Turkish', u'',],
    [ u'cp1140', u'ibm1140', u'Western Europe', u'',],
    [ u'cp1250', u'windows-1250', u'Central and Eastern Europe', u'',],
    [ u'cp1251', u'windows-1251', u'Bulgarian,Byelorussian,Macedonian,Russian,Serbian', u'bg,be,mk,ru,sr',],
    [ u'cp1252', u'windows-1252', u'Western Europe', u'',],
    [ u'cp1253', u'windows-1253', u'Greek', u'el',],
    [ u'cp1254', u'windows-1254', u'Turkish', u'tr',],
    [ u'cp1255', u'windows-1255', u'Hebrew', u'he',],
    [ u'cp1256', 'windows1256',   'Arabic', u'ar',],
    [ u'cp1257', u'windows-1257', u'Baltic languages', u'lv,lt',],
    [ u'cp1258', u'windows-1258', u'Vietnamese', u'vi',],
    [ u'euc_jp', u'eucjp,ujis,u-jis', u'Japanese', u'ja',],
    [ u'euc_jis_2004', u'jisx0213,eucjis2004', u'Japanese', u'ja',],
    [ u'euc_jisx0213', u'eucjisx0213', u'Japanese', u'ja',],
    [ u'euc_kr', u'euckr,korean,ksc5601,ks_c-5601,ks_c-5601-1987,ksx1001,ks_x-1001', u'Korean', u'ko',],
    [ u'gb2312', u'chinese,csiso58gb231280,euc-cn,euccn,eucgb2312-cn,gb2312-1980,gb2312-80,iso-ir-58', u'Simplified Chinese', u'zh',],
    [ u'gbk', u'936,cp936,ms936', u'Unified Chinese', u'zh',],
    [ u'gb18030', u'gb18030-2000', u'Unified Chinese', u'zh',],
    [ u'hz', u'hzgb,hz-gb,hz-gb-2312', u'Simplified Chinese', u'zh',],
    [ u'iso2022_jp', u'csiso2022jp,iso2022jp,iso-2022-jp', u'Japanese', u'ja',],
    [ u'iso2022_jp_1', u'iso2022jp-1,iso-2022-jp-1', u'Japanese', u'ja',],
    [ u'iso2022_jp_2', u'iso2022jp-2,iso-2022-jp-2', u'Japanese,Korean,Simplified Chinese,Western Europe,Greek', u'ja,ko,zh,el,en',],
    [ u'iso2022_jp_2004', u'iso2022jp-2004,iso-2022-jp-2004', u'Japanese', u'ja',],
    [ u'iso2022_jp_3', u'iso2022jp-3,iso-2022-jp-3', u'Japanese', u'ja',],
    [ u'iso2022_jp_ext', u'iso2022jp-ext,iso-2022-jp-ext', u'Japanese', u'ja',],
    [ u'iso2022_kr', u'csiso2022kr,iso2022kr,iso-2022-kr', u'Korean', u'ko',],
    [ u'latin_1', u'iso-8859-1,iso8859-1,8859,cp819,latin,latin1,L1', u'West Europe', u'',],
    [ u'iso8859_2', u'iso-8859-2,latin2,L2', u'Central and Eastern Europe', u'',],
    [ u'iso8859_3', u'iso-8859-3,latin3,L3', u'Esperanto,Maltese', u'eo,mt',],
    [ u'iso8859_4', u'iso-8859-4,latin4,L4', u'Baltic languages', u'lv,lt',],
    [ u'iso8859_5', u'iso-8859-5,cyrillic', u'Bulgarian,Byelorussian,Macedonian,Russian,Serbian', u'bg,be,mk,ru,sr',],
    [ u'iso8859_6', u'iso-8859-6,arabic', u'Arabic', u'ar',],
    [ u'iso8859_7', u'iso-8859-7,greek,greek8', u'Greek', u'el',],
    [ u'iso8859_8', u'iso-8859-8,hebrew', u'Hebrew', u'he',],
    [ u'iso8859_9', u'iso-8859-9,latin5,L5', u'Turkish', u'th',],
    [ u'iso8859_10', u'iso-8859-10,latin6,L6', u'Nordic languages', u'da,sv,no,nn,is,sv',],
    [ u'iso8859_13', u'iso-8859-13', u'Baltic languages', u'lv,lt',],
    [ u'iso8859_14', u'iso-8859-14,latin8,L8', u'Celtic languages', u'ga,gd,cy,br ',],
    [ u'iso8859_15', u'iso-8859-15', u'Western Europe', u'',],
    [ u'johab', u'cp1361,ms1361', u'Korean', u'ko',],
    [ u'koi8_r', u'koi8_r', u'Russian', u'ru',],
    [ u'koi8_u', u'koi8_u', u'Ukrainian', u'uk',],
    [ u'mac_cyrillic', u'maccyrillic', u'Bulgarian,Byelorussian,Macedonian,Russian,Serbian', u'bg,be,mk,ru,sr',],
    [ u'mac_greek', u'macgreek', u'Greek', u'el',],
    [ u'mac_iceland', u'maciceland', u'Icelandic', u'is',],
    [ u'mac_latin2', u'maclatin2,maccentraleurope', u'Central and Eastern Europe', u'',],
    [ u'mac_roman', u'macroman', u'Western Europe', u'',],
    [ u'mac_turkish', u'macturkish', u'Turkish', u'tr',],
    [ u'ptcp154', u'csptcp154,pt154,cp154,cyrillic-asian', u'Kazakh', u'kk',],
    [ u'shift_jis', u'csshiftjis,shiftjis,sjis,s_jis', u'Japanese', u'ja',],
    [ u'shift_jis_2004', u'shiftjis2004,sjis_2004,sjis2004', u'Japanese', u'ja',],
    [ u'shift_jisx0213', u'shiftjisx0213,sjisx0213,s_jisx0213', u'Japanese', u'ja',],
 ]


cAllEncodingNames = reduce( lambda todosEncodings, someEncodings: todosEncodings + someEncodings, [ [ unEncodingSpec[ 0], ] + unEncodingSpec[ 1].split( ',') for unEncodingSpec in cUTFEncodingsForAllLanguages + cDefaultEncodingsSourceMap], [])
