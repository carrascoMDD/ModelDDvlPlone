# -*- coding: utf-8 -*-
#
# File: MDDTool_Plone.py
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









# #######################################################
# #######################################################









class MDDTool_Plone:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """
    
    
    security = ClassSecurityInfo()


        
    # #############################################################
    """Clipboard methods.
    
    """    
    
    security.declareProtected( permissions.View, 'pClearClipboard')
    def pClearClipboard(self, 
        theTimeProfilingResults     =None,
        theContextualElement        =None, 
        theAdditionalParams         =None):
              
        self.fModelDDvlPloneTool_Refactor( theContextualElement).pClearClipboard( 
            theModelDDvlPloneTool            = self,
            theTimeProfilingResults          = theTimeProfilingResults,
            theContextualElement             = theContextualElement,
            theAdditionalParams              = theAdditionalParams
        )
    
            

    
        
        
        
        
        
        
    security.declareProtected( permissions.View, 'fClipboardResult')
    def fClipboardResult(self, 
        theTimeProfilingResults     =None,
        theContextualElement        =None, 
        theAdditionalParams         =None):
      
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContextualElement)
        
    
        aClipboardResult = self.fModelDDvlPloneTool_Refactor( theContextualElement).fClipboardResult( 
            theModelDDvlPloneTool           = self,
            theModelDDvlPloneTool_Retrieval = aModelDDvlPloneTool_Retrieval,
            theTimeProfilingResults         = theTimeProfilingResults,
            theContextualElement            = theContextualElement,
            theAdditionalParams             = theAdditionalParams
        )
        if not aClipboardResult:
            return aClipboardResult
            
        someElementsByRoots = aClipboardResult.get( 'elements_by_roots', [])
        for unResultForOneRoot in someElementsByRoots:
            someElementsResults = unResultForOneRoot[ 'elements']
            for unElementResult in someElementsResults:
                aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)

        return aClipboardResult


    
    
    
    
    
    
    
    

    
    # ######################################
    """Portal accessors, not worth to delegate on specific role classes."    
    
    """    
    
          
    security.declarePrivate('fPortalRoot')
    def fPortalRoot(self):
        aPortalTool = getToolByName( self, 'portal_url')
        unPortal = aPortalTool.getPortalObject()
        return unPortal       
    
    
    
    
    security.declarePublic('fPortalURL')
    def fPortalURL(self, ):

        unPortalURLTool = getToolByName( self, 'portal_url', None)
        if not unPortalURLTool:
            return ''
        
        unPortalURL = ''
        try:
            unPortalURL = unPortalURLTool()
        except: 
            None
        if not unPortalURL:
            return ''
        
        return unPortalURL
        
    
    
    
    
    
    
    
    
    
    


    # #############################################################
    """Retrieval of information about relevant Plone Products installed.
    
    """        
    
    
    
  
    
    security.declareProtected( permissions.View, 'fProductsInfo')
    def fProductsInfo(self, 
        theContextualObject         =None,
        theProductNames             =None, 
        theProductNamesNotInQuickInstaller=None,
        theAdditionalParams         =None):
        """Retrieve from Plone Quick Installer the information for the named products.
        
        """
        return self.fProductsInfo_Fake( 
            theContextualObject         =theContextualObject,
            theProductNames             =theProductNames, 
            theProductNamesNotInQuickInstaller=theProductNamesNotInQuickInstaller,
            theAdditionalParams         =theAdditionalParams)
    
    
    
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fProductsInfo_Fake')
    def fProductsInfo_Fake(self, 
        theContextualObject         =None,
        theProductNames             =None, 
        theProductNamesNotInQuickInstaller=None,
        theAdditionalParams         =None):
        """Faked to avoid accessing the portal_quick_intaller, because it makes it dirty and join the Transaction and causing a write operation on the store. Bad also for performance, although this is accessed only once per language (is used only in an element independent cacheable view).
        
        """
    
        someProductsInfo = []
        
        if ( theContextualObject == None):
            return someProductsInfo
        
        if not ( theProductNames or theProductNamesNotInQuickInstaller):
            return someProductsInfo
        
        for aProductName in theProductNames:
            aProductInfo = {
                'id':        aProductName, 
                'status':    True,
                'hasError':  False,
                'installed': True,
                'installedVersion': 'x.x',
            }
            someProductsInfo.append( aProductInfo)
                    
                    
        for aProductName in theProductNamesNotInQuickInstaller:
            aProductInfo = {
                'id':        aProductName, 
                'status':    True,
                'hasError':  False,
                'installed': True,
                'installedVersion': 'x.x',
           }
            someProductsInfo.append( aProductInfo)
                
                        
        return someProductsInfo
    
    
    
    
    
    
    
    security.declareProtected( permissions.View, 'fProductsInfo_Accessing')
    def fProductsInfo_Accessing(self, 
        theContextualObject         =None,
        theProductNames             =None, 
        theProductNamesNotInQuickInstaller=None,
        theAdditionalParams         =None):
        """Retrieve from Plone Quick Installer the information for the named products.
        
        """
    
        someProductsInfo = []
        
        if ( theContextualObject == None):
            return someProductsInfo
        
        if not ( theProductNames or theProductNamesNotInQuickInstaller):
            return someProductsInfo
        
        
        
        #aPortalQuickInstaller = getToolByName( theContextualObject, 'ACV OJO 20091203 seems to get dirty the current Transaction in any read only  portal_quickinstaller', None)
        aPortalQuickInstaller = getToolByName( theContextualObject, 'portal_quickinstaller', None)
        if ( aPortalQuickInstaller == None):
            return someProductsInfo
        
        anInstanceHome  = aPortalQuickInstaller.getInstanceHome()
        aProductsFolder = os.path.join( anInstanceHome, 'Products')
        
    
        
        someInstallableProducts = aPortalQuickInstaller.listInstallableProducts()
        """entries like {'id':r, 
                        'status':p.getStatus(),
                        'hasError':p.hasError()}
        """
        someInstallableProductsById = dict( [ [aProduct.get('id', ''), aProduct,] for  aProduct in someInstallableProducts])
        
        someInstalledProducts = aPortalQuickInstaller.listInstalledProducts()
        """entries like {'id':r, 'status':p.getStatus(),
                        'hasError':p.hasError(),
                        'isLocked':p.isLocked(),
                        'isHidden':p.isHidden(),
                        'installedVersion':p.getInstalledVersion()}
        """
        someInstalledProductsById = dict( [ [ aProduct.get('id', ''), aProduct,] for  aProduct in someInstalledProducts])
    
        
        for aProductName in theProductNames:
            aInstallableProduct = someInstallableProductsById.get( aProductName, {})
            if aInstallableProduct:
                aProductInfo = aInstallableProduct.copy()
                aProductInfo[ 'installed'] = False
                someProductsInfo.append( aProductInfo)
            else:
                aInstalledProduct = someInstalledProductsById.get( aProductName, {})
                if aInstalledProduct:
                    aProductInfo = aInstalledProduct.copy()
                    aProductInfo[ 'installed'] = True
                    someProductsInfo.append( aProductInfo)
                else:
                    aProductInfo = {
                        'id':        aProductName, 
                        'status':    False,
                        'hasError':  True,
                        'installed': False,
                    }
                    someProductsInfo.append( aProductInfo)
                    
                    
        for aProductName in theProductNamesNotInQuickInstaller:
            aFound = False

            aProductPath =os.path.join( aProductsFolder, aProductName)
            someFiles = []
            try:
                someFiles = os.listdir( aProductPath)
            except OSError:
                None
            for aFile in someFiles:
                if aFile.lower() == 'version.txt':
                    aVersion = open( os.path.join( aProductPath, aFile)).read().strip()
                    if aVersion:
                        aProductInfo = {
                            'id':        aProductName, 
                            'status':    True,
                            'hasError':  False,
                            'installed': True,
                            'installedVersion': aVersion,
                        }
                        someProductsInfo.append( aProductInfo)
                        aFound = True
                        break
            if not aFound:
                aProductInfo = {
                    'id':        aProductName, 
                    'status':    False,
                    'hasError':  False,
                    'installed': False,
                }
                someProductsInfo.append( aProductInfo)
                
                        
        return someProductsInfo
        
                
        
        
            
    
    
    


                

    # ####################################################
    """Display view maintenance methods.
    
    """

               
                   

    security.declareProtected( permissions.View,  'pSetDefaultDisplayView')
    def pSetDefaultDisplayView(self, theElement):  
        """Set to its default the view that will be presented for an element, when no view is specified. Usually one of Textual or Tabular.
        
        """
    
        if not self.fModelDDvlPloneTool_Retrieval( theElement).fCheckElementPermission( theElement, [ permissions.ModifyPortalContent ], None):
            return self
            
        unaDefaultView = ''
        try:
            unaDefaultView = theElement.default_view
        except:
            None
        
        if unaDefaultView:
            self.pSetAsDisplayView( theElement, unaDefaultView)
            
        return self
        

    
    
    


    security.declareProtected( permissions.View, 'pSetAsDisplayView')
    # security.declareProtected( permissions.ModifyPortalContent,  'pSetAsDisplayView')
    def pSetAsDisplayView(self, theElement, theViewName):            
        """Set the view that will be presented for an element, when no view is specified. Usually one of Textual or Tabular.
        
        """
                
        unaPortalInterfaceTool = getToolByName( theElement, 'portal_interface')   
        if unaPortalInterfaceTool.objectImplements( theElement, 'Products.CMFPlone.interfaces.BrowserDefault.ISelectableBrowserDefault'):
            if not theElement.getLayout() == theViewName:
                theElement.setLayout( theViewName)                 
        return self
                   
        
    
