# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Inicializacion_Constants.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Model Driven Development sl and Antonio Carrasco Valero
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


##code-section module-header #fill in your manual code here

from AccessControl import ClassSecurityInfo

from Products.CMFCore               import permissions


##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here







cMDDInitializationPermission = permissions.ManagePortal



from ModelDDvlPloneToolLoadConstants import cModelDDvlPloneToolId

#cModelDDvlPloneToolId          = 'MDDModelDDvlPlone_tool'
cModelDDvlPloneConfigurationId = 'MDDModelDDvlPlone_configuration'



cInstallPath_PortalSkinsCustom = [ 'portal_skins', 'custom',]




cLazyCreateExternalMethods             = True
cLazyCreateToolSingletons              = True


# #############################################################
# UNSAFE External methods to create. Use during development, debugging, or under strict extreme development precesses. 
#


cMDDExtMethod_MDDInitialization                     = "MDDInitialization"

cMDDExtMethod_MDDLoadModules                        = "MDDLoadModules"
cMDDExtMethod_MDDModulesList                        = "MDDModulesList"


cMDDExtModule_MDDZipFileExpansionUtils              = 'MDDZipFileExpansionUtils'

cMDDExtMethod_MDDInformeContenidoZipFile            = "MDDInformeContenidoZipFile"
cMDDExtMethod_MDDDescomprimirContenidoZipFile       = "MDDDescomprimirContenidoZipFile"



# #############################################################
# External methods to create
#

cMDDExtMethod_MDDManageActions              = 'MDDManageActions'

cMDDExtMethod_MDDInteractionTabular         = "MDDInteractionTabular"

cMDDExtModule_MDDPresentationTabular        = 'MDDPresentationTabular'

cMDDExtMethod_MDDPresentationTabular        = 'MDDPresentationTabular'

cMDDExtMethod_MDDPresentationEmpty          = "MDDPresentationEmpty"

cMDDExtMethod_MDDPresentationClipboard      = "MDDPresentationClipboard"

cMDDExtMethod_MDDPresentationActionsResults = "MDDPresentationActionsResults"

cMDDExtMethod_MDDCacheDump                  = "MDDCacheDump"



cMDDExternalMetodDefinitions = [
    {
        'ext_method_module':         cMDDExtMethod_MDDManageActions,
        'ext_method_function':       cMDDExtMethod_MDDManageActions,
        'ext_method_id':             cMDDExtMethod_MDDManageActions,
        'ext_method_title':          cMDDExtMethod_MDDManageActions,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  True,
    },
    {
        'ext_method_module':         cMDDExtMethod_MDDInteractionTabular,
        'ext_method_function':       cMDDExtMethod_MDDInteractionTabular,
        'ext_method_id':             cMDDExtMethod_MDDInteractionTabular,
        'ext_method_title':          cMDDExtMethod_MDDInteractionTabular,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  True,
    },
    {
        'ext_method_module':         cMDDExtModule_MDDPresentationTabular,
        'ext_method_function':       cMDDExtMethod_MDDPresentationEmpty,
        'ext_method_id':             cMDDExtMethod_MDDPresentationEmpty,
        'ext_method_title':          cMDDExtMethod_MDDPresentationEmpty,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  True,
    },
    {
        'ext_method_module':         cMDDExtModule_MDDPresentationTabular,
        'ext_method_function':       cMDDExtMethod_MDDPresentationClipboard,
        'ext_method_id':             cMDDExtMethod_MDDPresentationClipboard,
        'ext_method_title':          cMDDExtMethod_MDDPresentationClipboard,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  True,
    },
    {
        'ext_method_module':         cMDDExtModule_MDDPresentationTabular,
        'ext_method_function':       cMDDExtMethod_MDDPresentationActionsResults,
        'ext_method_id':             cMDDExtMethod_MDDPresentationActionsResults,
        'ext_method_title':          cMDDExtMethod_MDDPresentationActionsResults,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  True,
    },
    {
        'ext_method_module':         cMDDExtModule_MDDPresentationTabular,
        'ext_method_function':       cMDDExtMethod_MDDPresentationTabular,
        'ext_method_id':             cMDDExtMethod_MDDPresentationTabular,
        'ext_method_title':          cMDDExtMethod_MDDPresentationTabular,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  True,
    },
    {
        'ext_method_module':         cMDDExtMethod_MDDCacheDump,
        'ext_method_function':       cMDDExtMethod_MDDCacheDump,
        'ext_method_id':             cMDDExtMethod_MDDCacheDump,
        'ext_method_title':          cMDDExtMethod_MDDCacheDump,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  True,
    },
    {
        'ext_method_module':         cMDDExtMethod_MDDLoadModules,
        'ext_method_function':       cMDDExtMethod_MDDLoadModules,
        'ext_method_id':             cMDDExtMethod_MDDLoadModules,
        'ext_method_title':          cMDDExtMethod_MDDLoadModules,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  False,
    },
    {
        'ext_method_module':         cMDDExtMethod_MDDLoadModules,
        'ext_method_function':       cMDDExtMethod_MDDModulesList,
        'ext_method_id':             cMDDExtMethod_MDDModulesList,
        'ext_method_title':          cMDDExtMethod_MDDModulesList,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  False,
    },
    {
        'ext_method_module':         cMDDExtMethod_MDDInitialization,
        'ext_method_function':       cMDDExtMethod_MDDInitialization,
        'ext_method_id':             cMDDExtMethod_MDDInitialization,
        'ext_method_title':          cMDDExtMethod_MDDInitialization,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  False,
    },
    {
        'ext_method_module':         cMDDExtModule_MDDZipFileExpansionUtils,
        'ext_method_function':       cMDDExtMethod_MDDInformeContenidoZipFile,
        'ext_method_id':             cMDDExtMethod_MDDInformeContenidoZipFile,
        'ext_method_title':          cMDDExtMethod_MDDInformeContenidoZipFile,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  False,
    },
    {
        'ext_method_module':         cMDDExtModule_MDDZipFileExpansionUtils,
        'ext_method_function':       cMDDExtMethod_MDDDescomprimirContenidoZipFile,
        'ext_method_id':             cMDDExtMethod_MDDDescomprimirContenidoZipFile,
        'ext_method_title':          cMDDExtMethod_MDDDescomprimirContenidoZipFile,
        'install_path':              cInstallPath_PortalSkinsCustom,
        'required':                  False,
    },   
]



cMDDToolSingletonDefinitions = [
    {
        'singleton_id': cModelDDvlPloneToolId, 
        'tool_module': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool', 
        'tool_class':   'ModelDDvlPloneTool', 
        'install_path': cInstallPath_PortalSkinsCustom, 
        'required':     True, 
    }, 
    {
        'singleton_id': cModelDDvlPloneConfigurationId, 
        'tool_module': 'Products.ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration', 
        'tool_class':   'ModelDDvlPloneConfiguration', 
        'install_path': cInstallPath_PortalSkinsCustom, 
        'required':     True, 
    },
]

             
cMDDInitializationDefinitions = {
    'title':             'framework ModelDDvlPlone',
    'external_methods':  cMDDExternalMetodDefinitions,
    'tool_singletons':   cMDDToolSingletonDefinitions,
}



##/code-section module-footer



