# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool.py
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

import os
import sys
import traceback
import logging


# Zope
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo

from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation

from time import time

from DateTime import DateTime




from Products.CMFCore                    import permissions
from Products.CMFCore.utils              import getToolByName, UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase




from Acquisition  import aq_inner, aq_parent,aq_get





from MDDTool_Cache          import MDDTool_Cache               
from MDDTool_Dates          import MDDTool_Dates   
from MDDTool_Export         import MDDTool_Export
from MDDTool_Globals        import MDDTool_Globals             
from MDDTool_I18N           import MDDTool_I18N                
from MDDTool_Mutators       import MDDTool_Mutators            
from MDDTool_Plone          import MDDTool_Plone               
from MDDTool_Refactor       import MDDTool_Refactor              
from MDDTool_Render         import MDDTool_Render              
from MDDTool_Retrieval      import MDDTool_Retrieval           
from MDDTool_Translations   import MDDTool_Translations        
from MDDTool_Versions       import MDDTool_Versions            
from MDDTool_X              import MDDTool_X    






# ####################################################################
"""Tool permissions to be set upon instantiation of the tool,  not restricting the access of anonymous users.

"""         
cModelDDvlPloneToolPermissions = [                                                                                                                                     
    { 'permission': permissions.ManagePortal,         'acquire': True,  'roles': [              'Manager', ], },                             
    { 'permission': permissions.ManageProperties,     'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.DeleteObjects,        'acquire': True,  'roles': [              'Authenticated', ], }, 
    { 'permission': permissions.View,                 'acquire': True,  'roles': [ 'Anonymous', 'Authenticated', ], },  
    { 'permission': perm_AccessContentsInformation,   'acquire': True,  'roles': [ 'Anonymous', 'Authenticated', ], },  
]







# #######################################################
# #######################################################









class ModelDDvlPloneTool( UniqueObject, PropertyManager, SimpleItem.SimpleItem, ActionProviderBase, \
    MDDTool_Cache,    \
    MDDTool_Dates,    \
    MDDTool_Export,   \
    MDDTool_Globals,  \
    MDDTool_I18N,     \
    MDDTool_Mutators, \
    MDDTool_Plone,    \
    MDDTool_Refactor, \
    MDDTool_Render,   \
    MDDTool_Retrieval,\
    MDDTool_Translations, \
    MDDTool_Versions, \
    MDDTool_X,        \
    ):
    """Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """

              
    from ModelDDvlPloneToolLoadConstants import cModelDDvlPloneToolId
        
    
    "The ModelDDvlPloneTool"

    meta_type = 'ModelDDvlPloneTool'

    id = cModelDDvlPloneToolId

    manage_options = PropertyManager.manage_options + \
                     SimpleItem.SimpleItem.manage_options + (
    	{'label': 'View', 'action': 'index_html',},
    )

    _properties = (
        {'id':'title', 'type':'string', 'mode':'w'},
    )

    # Standard security settings
    security = ClassSecurityInfo()


    security.declareProtected('Manage properties', 'index_html')
    index_html = PageTemplateFile('skins/index_html', globals())

    


    

 

    # #######################################################
    """Globals
    
    """
     
    """Instance of MDDModulesManager in charge of importing modules, and resolve in the module symbols given their name.
    
    """
    gModulesManager       = None
    
    

    
    


    # #############################################################
    """Configuration methods.
    
    """        
        

    security.declarePublic('fLoadModulesSpecification')
    def fLoadModulesSpecification( self):

        from ModelDDvlPloneToolLoadConstants import cLoadModulesSpecification    
        
        return cLoadModulesSpecification
    
    
    
        
    
    

    
    
    # ######################################
    """Tool role classes resolution.
    
    """
    
    security.declarePrivate( 'fModelDDvlPloneTool_Globals')
    def fModelDDvlPloneTool_Globals( self, theContextualObject):
        return self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals')
       
    
    security.declarePrivate( 'fModelDDvlPloneTool_Retrieval')
    def fModelDDvlPloneTool_Retrieval( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval')
        if not aClass:
            return None
        return aClass()
    
    
       
    security.declarePrivate( 'fModelDDvlPloneTool_Inicializacion')
    def fModelDDvlPloneTool_Inicializacion( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion')
        if not aClass:
            return None
        return aClass()
    
       
    security.declarePrivate( 'fModelDDvlPloneTool_Bodies')
    def fModelDDvlPloneTool_Bodies( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Bodies')
        if not aClass:
            return None
        return aClass()
    

    security.declarePrivate( 'fModelDDvlPloneTool_Mutators')
    def fModelDDvlPloneTool_Mutators( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators')
        if not aClass:
            return None
        return aClass()
    
            
    security.declarePrivate( 'fModelDDvlPloneTool_Mutators_Plone')
    def fModelDDvlPloneTool_Mutators_Plone( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators_Plone')
        if not aClass:
            return None
        return aClass()
    
            
    security.declarePrivate( 'fModelDDvlPloneTool_Cache')
    def fModelDDvlPloneTool_Cache( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache')
        if not aClass:
            return None
        return aClass()
    
            
    security.declarePrivate( 'fModelDDvlPloneTool_Refactor')
    def fModelDDvlPloneTool_Refactor( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor')
        if not aClass:
            return None
        return aClass()
    
            
    security.declarePrivate( 'fModelDDvlPloneTool_Version')
    def fModelDDvlPloneTool_Version( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Version')
        if not aClass:
            return None
        return aClass()
    
    
    security.declarePrivate( 'fModelDDvlPloneTool_Transactions')
    def fModelDDvlPloneTool_Transactions( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Transactions')
        if not aClass:
            return None
        return aClass()    
    
    
    security.declarePrivate( 'fModelDDvlPloneTool_Translation')
    def fModelDDvlPloneTool_Translation( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Translation')
        if not aClass:
            return None
        return aClass()
    
      
    security.declarePrivate( 'fModelDDvlPloneTool_Import')
    def fModelDDvlPloneTool_Import( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Import')
        if not aClass:
            return None
        return aClass()
    
        
    security.declarePrivate( 'fModelDDvlPloneTool_Export')
    def fModelDDvlPloneTool_Export( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Export')
        if not aClass:
            return None
        return aClass()
    
        
    security.declarePrivate( 'fModelDDvlPloneTool_ToDicts')
    def fModelDDvlPloneTool_ToDicts( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_ToDicts')
        if not aClass:
            return None
        return aClass()
    

    security.declarePrivate( 'fModelDDvlPloneToolSupport')
    def fModelDDvlPloneToolSupport( self, theContextualObject):
        aClass = self.fImportedModuleResolvedSymbol( theContextualObject, 'Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport')
        if not aClass:
            return None
        return aClass()
    
            
                            
                       
 
    
    
    
    
    
        
    

    
    # #######################################################
    """Collaborations with other applications, i.e., ModelDDvlPloneConfiguration.
    
    """    
    
    security.declarePrivate( 'fModelDDvlPloneConfiguration')
    def fModelDDvlPloneConfiguration(self,):       
        """Retrieve or create an instance of ModelDDvlPloneConfiguration.
        
        """
        try:

            from Products.ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration import cModelDDvlPloneConfigurationId
            
            aModelDDvlPloneConfiguration = getToolByName( self, cModelDDvlPloneConfigurationId, None)
            
            if aModelDDvlPloneConfiguration == None:
                return None
            
            return aModelDDvlPloneConfiguration
            
            
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during tool access operation fModelDDvlPloneConfiguration\n' 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
     
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPloneTool').error( unInformeExcepcion)
    
            return None
             
            

    
    
    

    
    
    
    
    
    
    
    
    
    

        
        
        
    

    
    # #######################################################
    """Module and module component resolution
    
    """
    security.declarePrivate( 'fImportedModuleResolvedSymbol')
    def fImportedModuleResolvedSymbol( self, theContextualObject, theModuleName, theComponentName=''):
        
        if ( not ModelDDvlPloneTool.gModulesManager) or ( not ModelDDvlPloneTool.gModulesManager.fModulesAlreadyImported()):
            
            from MDDModulesManager                import MDDModulesManager
            from ModelDDvlPloneToolLoadConstants  import cLoadModulesSpecification
            
            ModelDDvlPloneTool.gModulesManager = MDDModulesManager(
                self,
                cLoadModulesSpecification,
            )
        
            if not ModelDDvlPloneTool.gModulesManager:
                return None    
            

        anImportedModuleResolvedSymbol = ModelDDvlPloneTool.gModulesManager.fImportedModuleResolvedSymbol( 
            theContextualObject =theContextualObject, 
            theModuleName       =theModuleName, 
            theComponentName    =theComponentName,
        )

        return anImportedModuleResolvedSymbol
        
    
        
        
        

    
    
    
    
    
    
    

    
    # ##########################################################
    """Initialization methods for the tool singleton.
    
    """

    security.declarePublic('manage_afterAdd')
    def manage_afterAdd(self,item,container):
        """Lazy Initialization of the tool.
        
        """        
        self.pSetPermissions()
                
        return self
    
    
    
    
    

    
    security.declarePrivate( 'pSetPermissions')
    def pSetPermissions(self):
        """Set tool permissions upon instantiation of the tool, according to a specification ( usually not restricting the access of anonymous users).
        
        """         
        
        for unaPermissionSpec in cModelDDvlPloneToolPermissions:
            unaPermission = unaPermissionSpec[ 'permission']
            unAcquire     = unaPermissionSpec[ 'acquire'] 
            unosRoles     = unaPermissionSpec[ 'roles']
            
            if unaPermission:
                self.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
        
        return self
        
         
    
    
    
    

    
    

# ####################################################
"""Constructor methods, only used when adding class to objectManager.

"""

def manage_addAction(self, REQUEST=None):
    "Add tool instance to parent ObjectManager"
    id = ModelDDvlPloneTool.id
    self._setObject(id, ModelDDvlPloneTool())
    if REQUEST is not None:
        return self.manage_main(self, REQUEST)

constructors = (manage_addAction,)



