# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Permissions_Definitions.py
#
# Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
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



from Products.CMFCore       import permissions


cPermissionsAndRolesForNonFolderishTypes = [ 
    [ [ permissions.View, ],                [ 'Manager', 'Owner', 'Reviewer', ], True,], # last boolean is acquire
    [ [ permissions.ModifyPortalContent, ], [ 'Manager', 'Owner', ],             True],
    [ [ permissions.DeleteObjects, ],       [ 'Manager', 'Owner', ],             True],
]


cPermissionsAndRolesForFolderishTypes = cPermissionsAndRolesForNonFolderishTypes + [ 
    [ [ permissions.ListFolderContents, ],  [ 'Manager', 'Owner', 'Reviewer', ], True],
    [ [ permissions.AddPortalContent, ],    [ 'Manager', 'Owner', ],             True],
    [ [ permissions.AddPortalFolders, ],    [ 'Manager', 'Owner', ],             True],
]


cAnyType = '*'

cPermissionsAndRolesForTypes = {
    'ATDocument': cPermissionsAndRolesForNonFolderishTypes,
    'ATLink':     cPermissionsAndRolesForNonFolderishTypes,
    'ATFile':     cPermissionsAndRolesForNonFolderishTypes,
    'ATImage':    cPermissionsAndRolesForNonFolderishTypes,
    'ATNewsItem': cPermissionsAndRolesForNonFolderishTypes,
    cAnyType:     cPermissionsAndRolesForFolderishTypes
}

