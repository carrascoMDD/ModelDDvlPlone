# -*- coding: utf-8 -*-
#
# File: MDDTool_Render.py
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


from time import time

try:
    import simplejson as json
except:
    json=None
    

# Zope
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo

from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation

from DateTime import DateTime




from Products.CMFCore                    import permissions
from Products.CMFCore.utils              import getToolByName, UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase




from Acquisition  import aq_inner, aq_parent,aq_get









# #######################################################
# #######################################################









class MDDTool_Render:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """
    
    
    security = ClassSecurityInfo()
    

    
    # ####################################################
    """Rest (ReStructuredText) rendering of elements contents.
    
    """

    
    
    
    
    security.declarePublic( 'fCookedBodyForElement')
    def fCookedBodyForElement(self, 
        theTimeProfilingResults =None,
        theElement              =None, 
        stx_level               =None, 
        setlevel                =0,
        theAdditionalParams     =None):
        """Retrieve an HTML presentation of an element's content as a Textual view.
        
        """
        
        return self.fModelDDvlPloneTool_Bodies( theElement).fCookedBodyForElement( 
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement, 
            stx_level               =stx_level, 
            setlevel                =setlevel,
            theAdditionalParams     =theAdditionalParams)
    

    
    
    
    
    
    
    security.declarePublic( 'fEditableBodyForElement')
    def fEditableBodyForElement(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a REST presentation of an element's content as a Textual view.
        
        """
        
        return self.fModelDDvlPloneTool_Bodies( theElement).fEditableBodyForElement( 
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement,
            theAdditionalParams     =theAdditionalParams
        )
    

    

    
    
    
    security.declarePublic( 'fEditableBodyBlock_MetaTypeIcons')
    def fEditableBodyBlock_MetaTypeIcons(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a REST presentation of an element's content as a Textual view.
        
        """
        
        return self.fModelDDvlPloneTool_Bodies( theElement).fEditableBodyBlock_MetaTypeIcons( 
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement,
            theAdditionalParams     =theAdditionalParams
        )
    
        

    
    
    
    
    

    
    
    # #############################################################
    """Template invocation methods.
    
    """

    
    
    
    security.declareProtected( permissions.View, 'fNoCacheIdAllowsRender')
    def fNoCacheIdAllowsRender(self, theContextualObject, theNoCacheCode, theTemplateName, ):
        
        return self.fModelDDvlPloneTool_Cache( theContextualObject).fNoCacheIdAllowsRender( self, theContextualObject, theNoCacheCode, theTemplateName)
        
    
    
    


    security.declareProtected( permissions.View, 'fRenderTemplate')
    def fRenderTemplate(self, theContextualObject, theTemplateName):
        """Execute a template in the current context and return the rendered HTML.
        
        """
        if not theTemplateName:
            return ''
             
        aViewTemplateInContext  = self.fTemplateCallable( theContextualObject, theTemplateName)
        
        if not aViewTemplateInContext:
            return ''
        
        aRenderedView = aViewTemplateInContext()       
                   
        return aRenderedView
    
    

    
    
    

    security.declareProtected( permissions.View, 'fTemplateCallable')
    def fTemplateCallable(self, theContextualObject, theTemplateName):
        """Execute a template in the current context and return the rendered HTML.
        
        """
        if not theTemplateName:
            return None
                        
        aViewName = theTemplateName
        if aViewName.find( '%s') >= 0:
            aProjectName = ''
            try:
                aProjectName = theContextualObject.getNombreProyecto()
            except:
                None
            if aProjectName:    
                aViewName = aViewName % aProjectName
            else:
                aViewName = aViewName % ''
            
        if not aViewName:
            return None
        
        aViewTemplate    = self.unrestrictedTraverse( aViewName)

        aContext                = aq_inner( theContextualObject)               
        aViewTemplateInContext  = aViewTemplate.__of__(aContext)

        return aViewTemplateInContext
    
    
    
    
    
        
    
    
    
    

    
        
    # ######################################
    """Pretty print methods.
    
    """

    
    security.declareProtected( permissions.View,  'fPrettyPrintHTML')
    def fPrettyPrintHTML( self, theContextualObject, theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):
        """Render as HTML a presentation of a list with rich inner structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return self.fModelDDvlPloneTool_Retrieval( theContextualObject).fPrettyPrintHTML( theList, theDictKeysToExclude, theDictKeysOrder, theFindAlreadyPrinted)


    
    
    
    
    
    security.declareProtected( permissions.View,  'fPrettyPrint')
    def fPrettyPrint( self, theContextualObject, theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):
        """Render a text presentation of a list with rich inner structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return self.fModelDDvlPloneTool_Retrieval( theContextualObject).fPrettyPrint( theList, theDictKeysToExclude, theDictKeysOrder, theFindAlreadyPrinted)


    
    
    
    
    
    security.declareProtected( permissions.View,  'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResultHTML( self, theContextualObject, theProfilingResult):
        """Render as HTML a presentation of an execution profiling result structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return self.fModelDDvlPloneToolSupport( theContextualObject).fPrettyPrintProfilingResultHTML( theProfilingResult)

    

    
    
    
    security.declareProtected( permissions.View,  'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResult( self, theContextualObject, theProfilingResult):
        """Render a text presentation of an execution profiling result structure, where items appear in consecutive lines, and nested items appear indented under their containers, and alineated with their siblings.
        
        """
        return self.fModelDDvlPloneToolSupport( theContextualObject).fPrettyPrintProfilingResult( theProfilingResult)

    
    
    
    
    
    security.declareProtected( permissions.View,  'fPreferredResultDictKeysOrder')
    def fPreferredResultDictKeysOrder( self, theContextualObject,):
        """The prefered keys order to render dictionary values as a text presentation.
        
        """
        return self.fModelDDvlPloneToolSupport( theContextualObject).fPreferredResultDictKeysOrder()

    
    
    
    
    
    
    
    
    
        
        
    # ######################################
    """JSON interchange methods.
    
    """        
       
  
 
    security.declareProtected( permissions.View,  'fJSONdumps')
    def fJSONdumps(self, theObject):
        if not json:
            return ""
        
        aJSON=json.dumps(theObject)
        return aJSON
    

    
         
    
 
    security.declareProtected( permissions.View,  'fJSONloads')
    def fJSONloads(self, theString):
        if not json:
            return None
        anObject=json.loads(theString)
        return anObject
    
