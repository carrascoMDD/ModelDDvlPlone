# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneToolLoadConstants.py
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







# ####################################################################
"""Id of the tool in its install container.

"""
cModelDDvlPloneToolId = 'MDDModelDDvlPlone_tool'






# ####################################################################
"""Specifications of modules to load, and globals and singletons to save. Used by ModelDDvlPloneTool_Initialization class and ExternalMethod MDDLoadModules.

"""


cLoadModulesSpecification = {
    'install_tools_on_portal_root': False,
    'install_tools_path':           [ 'portal_skins', 'custom',],
    'master_module': {
        'module_name':                   'Products.ModelDDvlPloneTool.ModelDDvlPloneTool',
        'class_name':                    'ModelDDvlPloneTool',
        'singleton_id':                  cModelDDvlPloneToolId,
        'modules_manager_global':        'gModulesManager',
    },
    'modules':  [
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDModulesManager',                             'global_spec': {}, 'singleton_spec': {}, },

        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneToolLoadConstants',               'global_spec': {}, 'singleton_spec': {}, },

        { 'module_name': 'Products.ModelDDvlPloneTool.MDDLinkedList',                                 'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDNestedContext',                              'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDStringConversions',                          'global_spec': {}, 'singleton_spec': {}, },

        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Cache',                                 'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Dates',                                 'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Export',                                'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Globals',                               'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_I18N',                                  'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Mutators',                              'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Plone',                                 'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Render',                                'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Refactor',                              'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Retrieval',                             'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Translations',                          'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_Versions',                              'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDTool_X',                                     'global_spec': {}, 'singleton_spec': {}, },

        { 'module_name': 'Products.ModelDDvlPloneTool.PloneElement_TraversalConfig',                  'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion_Constants',   'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor_Constants',         'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_ImportExport_Constants',     'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_ToDicts_Constants',          'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants',             'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators_Constants',         'global_spec': {}, 'singleton_spec': {}, },
        
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport',                     'global_spec': {}, 'singleton_spec': {}, },

        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Transactions',               'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Profiling',                  'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Candidates',       'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_I18N',             'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Impact',           'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Permissions',      'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_PloneContent',     'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_TraversalConfigs', 'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Utils',            'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval',                  'global_spec': {}, 'singleton_spec': {}, },
        
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDRefactor',                                   'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDRefactor_Paste',                             'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDRefactor_Import',                            'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDRefactor_NewTranslation',                    'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.MDDRefactor_NewVersion',                        'global_spec': {}, 'singleton_spec': {}, },
        
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_ToDicts',                    'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Export',                     'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Import',                     'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Bodies',                     'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators_Plone',             'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Permissions_Definitions',    'global_spec': {}, 'singleton_spec': {}, },    
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators',                   'global_spec': {}, 'singleton_spec': {}, },   
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor',                   'global_spec': {}, 'singleton_spec': {}, }, 
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Version',                    'global_spec': {}, 'singleton_spec': {}, },   
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Translation',                'global_spec': {}, 'singleton_spec': {}, },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals',                    
            'global_spec': {
                'class_name':       'ModelDDvlPloneTool_Globals', 
                'globals_accessor': 'fgGlobalsAccessor', 
                'globals_mutator':  'pgGlobalsMutator',
            }, 
            'singleton_spec': {}, 
        },   
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache',                      'global_spec': {}, 'singleton_spec': {}, },  
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool',                            
            'global_spec': {}, 
            'singleton_spec': {
                'class_name':                    'ModelDDvlPloneTool',           
                'singleton_id':                  cModelDDvlPloneToolId, 
                'persistent_data_accessor_name': None,
                'persistent_data_mutator_name':  None,
            }, 
        },
        { 'module_name': 'Products.ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration',          
            'global_spec': {}, 
            'singleton_spec': {
                'class_name':                    'ModelDDvlPloneConfiguration',           
                'singleton_id':                  'MDDModelDDvlPlone_configuration', 
                'persistent_data_accessor_name': 'fPersistentFieldsAccessor',
                'persistent_data_mutator_name':  'pPersistentFieldsMutator',
            }, 
        },
        { 'module_name': 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion',             'global_spec': {}, 'singleton_spec': {}, },
    ]
}






    

