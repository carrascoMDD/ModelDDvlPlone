# -*- coding: utf-8 -*-
#
# File: PloneElement_TraversalConfig.py
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



from AccessControl      import ClassSecurityInfo
from Acquisition        import aq_inner, aq_parent

from Products.CMFCore import permissions


cPloneElement_ColumnName_Details = 'details'
cPloneImage_DetailsHeight        = 64
cPloneDocument_DetailsLen        = 128


cPloneTypes = {
    'ATImage':     { 'meta_type': 'ATImage',       'archetype_name': 'Image',       'portal_type': 'Image',      'i18n_msgid': 'Image',      'content_icon': 'image_icon.gif',   },                                 
    'ATFile':      { 'meta_type': 'ATFile',        'archetype_name': 'File',        'portal_type': 'File',       'i18n_msgid': 'File',       'content_icon': 'file_icon.gif',    },                                 
    'ATDocument':  { 'meta_type': 'ATDocument',    'archetype_name': 'Page',        'portal_type': 'Document',   'i18n_msgid': 'Page',       'content_icon': 'document_icon.gif',},                                 
    'ATNewsItem':  { 'meta_type': 'ATNewsItem',    'archetype_name': 'News Item',   'portal_type': 'News Item',  'i18n_msgid': 'News Item',  'content_icon': 'newsitem_icon.gif',},                                 
    'ATLink':      { 'meta_type': 'ATLink',        'archetype_name': 'Link' ,       'portal_type': 'Link' ,      'i18n_msgid': 'Link',       'content_icon': 'link_icon.gif',    },                                  
}



cPloneSubItemsParameters = [
    {   'traversal_name':           'adjuntos', 
        'label_msgid':              'ModelDDvlPlone_documentos_adjuntos_label', 
        'description_msgid':        'ModelDDvlPlone_documentos_adjuntos_description', 
        'plone_read_permission':     None, # already checked in container for permissions.ListFolderContents,
        'plone_write_permission':    None, # already checked in container for permissions.AddPortalContent,
        'allowed_types':        [ 
# could check additional write permissions than the standard  the AT content types add permissions like ATContentTypes: Add Image , ATContentTypes: Add Document , etc            
            { 'meta_type': 'ATImage',       'archetype_name': 'Image',      'i18n_msgid': 'Image',      'content_icon': 'image_icon.gif',   'plone_read_permission':     None, 'plone_write_permission':     None,}, 
            { 'meta_type': 'ATFile',        'archetype_name': 'File',       'i18n_msgid': 'File',       'content_icon': 'file_icon.gif',    'plone_read_permission':     None, 'plone_write_permission':     None,}, 
            { 'meta_type': 'ATDocument',    'archetype_name': 'Document',   'i18n_msgid': 'Page',       'content_icon': 'document_icon.gif','plone_read_permission':     None, 'plone_write_permission':     None,}, 
            { 'meta_type': 'ATNewsItem',    'archetype_name': 'News Item',  'i18n_msgid': 'News Item',  'content_icon': 'newsitem_icon.gif','plone_read_permission':     None, 'plone_write_permission':     None,}, 
        ]
    },
    {   'traversal_name':           'enlaces',  
        'label_msgid':              'ModelDDvlPlone_hiper_enlaces_label', 
        'description_msgid':        'ModelDDvlPlone_hiper_enlaces_description' , 
        'plone_read_permission':     permissions.View,
        'plone_write_permission':    permissions.AddPortalContent,
        'allowed_types':        [ 
            { 'meta_type': 'ATLink',        'archetype_name': 'Link' ,      'i18n_msgid': 'Link',        'content_icon': 'link_icon.gif',   'plone_read_permission':     None, 'plone_write_permission':     None,}, 
        ]
    }
]
   


cExportConfig_PloneElements = [
    {   'portal_types': [ 'ATLink', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {
                'name': 'url',
                'type': 'String',
                'accessor': 'getRemoteUrl',
                'mutator':  'setRemoteUrl',
            },
             
        ],
    },
    {   'portal_types': [ 'ATDocument', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'content_type',
                'type': 'String',
                'accessor': 'getContentType',
                'mutator':  'setContentType',
            },
        ],
    },
    {   'portal_types': [ 'ATFile', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {
                'name': 'file',
                'type': 'File',
            },
            {   'name': 'content_type',
                'type': 'String',
                'accessor': 'getContentType',
                'mutator':  'setContentType',
            },
            {   'name': 'filename',
                'type': 'String',
                'accessor': 'getFilename',
                'mutator':  'setFilename',
            },
        ],
    },
    {   'portal_types': [ 'ATImage', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'image',
                'type': 'Image',
            },
            {   'name': 'content_type',
                'type': 'String',
                'accessor': 'getContentType',
                'mutator':  'setContentType',
            },
            {   'name': 'filename',
                'type': 'String',
                'accessor': 'getFilename',
                'mutator':  'setFilename',
            },
        ],
    },
    {   'portal_types': [ 'ATNewsItem', ],
        'attrs':        [
            {   'name': 'title',
                'type': 'String',
            },
            {   'name': 'description',
                'type': 'Text',
            },
            {   'name': 'text',
                'type': 'Text',
            },
            {   'name': 'content_type',
                'type': 'String',
                'accessor': 'getContentType',
                'mutator':  'setContentType',
            },
            {   'name': 'image',
                'type': 'Image',
            },
            {   'name': 'imageCaption',
                'type': 'String',
            },
            {   'name': 'image_content_type',
                'type': 'String',
                'accessor': 'getImage',
                'attribute': 'content_type',
                'mutator_accessor': 'getImage',
            },
            #{   'name': 'filename',
                #'type': 'String',
                #'accessor': 'getImage',
                #'attribute': 'filename',
                #'mutator_accessor': 'getImage',
            #},
            {   'name': 'filename',
                'type': 'String',
                'accessor': 'getImage',
                'attribute': 'filename',
                'mutator_accessor': 'getImage',
            },
        ],
    },
]    
 

cExportConfig_PloneElements_MetaTypes = [ ]
for aTypeConfig in cExportConfig_PloneElements:
    someTypes = aTypeConfig.get( 'portal_types', [])
    for aType in someTypes:
        if not ( aType in cExportConfig_PloneElements_MetaTypes):
            cExportConfig_PloneElements_MetaTypes.append( aType)
            