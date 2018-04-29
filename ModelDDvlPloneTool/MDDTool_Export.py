# -*- coding: utf-8 -*-
#
# File: MDDTool_Export.py
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









# #######################################################
# #######################################################









class MDDTool_Export:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """
    
    
    security = ClassSecurityInfo()

        
    
        
    
    
      
    # #############################################################
    """Export methods.
    
    """

    
    security.declareProtected( permissions.View, 'fExport')
    def fExport(self, 
        theTimeProfilingResults     =None,
        theObject                   =None, 
        theAllExportTypeConfigs     =None,
        theOutputEncoding           =None,
        theReturnXML                =False,
        theAdditionalParams         =None):
        """Export an element as a zipped archive with XML file, and including binary content with the attached files and images."
        
        """
        
        return self.fModelDDvlPloneTool_Export( theObject).fExport( 
            theModelDDvlPloneTool       =self,
            theTimeProfilingResults     =theTimeProfilingResults,
            theObject                   =theObject, 
            theAllExportTypeConfigs     =theAllExportTypeConfigs, 
            theOutputEncoding           =theOutputEncoding,
            theReturnXML                =theReturnXML,
            theAdditionalParams         =theAdditionalParams
        )


    
        
    
    
    
    
        
    # #############################################################
    """Retrieval as dictionary of dictionaries methods.
    
    """
    
    security.declareProtected( permissions.View, 'fToDicts')
    def fToDicts(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theAdditionalParams         =None):
        """Export an element as a zipped archive with XML file, and including binary content with the attached files and images."
        
        """
        
        someAllExportTypeConfigs =  self.fModelDDvlPloneTool_Retrieval( theElement).getAllTypeExportConfigs( theElement)        
            
        return self.fModelDDvlPloneTool_ToDicts( theElement).fToDicts( 
            theModelDDvlPloneTool       =self,
            theElement                  =theElement, 
            theAllToDictsTypeConfigs    =someAllExportTypeConfigs, 
            theAdditionalParams         =theAdditionalParams
        )


    
    
    
    security.declarePrivate( 'fIndexToDicts')
    def fIndexToDicts( self,
        theContextualElement = None,
        theDicts             =None, 
        theIndexNames        =None):
        """Create specified indexes with information from the dictionaries in the tree.
        
        """    
        return self.fModelDDvlPloneTool_ToDicts( theContextualElement).fIndexToDicts( 
            theModelDDvlPloneTool =self,
            theContextualElement  =theContextualElement,
            theDicts              =theDicts, 
            theIndexNames         =theIndexNames,
        )
    
    
    
    
    
    security.declarePrivate( 'fResolveByIndex_Callable')
    def fResolveByIndex_Callable( self,
        theContextualElement = None,):
        """Obtain a callable element able to resolve model element from their identity.
        
        """
        return self.fModelDDvlPloneTool_ToDicts( theContextualElement).fResolveByIndex_Callable( 
            theModelDDvlPloneTool =self,
            theContextualElement  =theContextualElement,
        )
            
        
    
    
    
    
    security.declarePublic( 'fDownloadObjectPythonRepresentation')
    def fDownloadObjectPythonRepresentation(self, 
        theTimeProfilingResults =None,
        theContextualElement    =None,
        theObject               =None, 
        theTitle                =None,
        theAdditionalParams     =None,):
        """Download utility.
        
        """    
          
        return self.fModelDDvlPloneTool_ToDicts( theObject).fDownloadObjectPythonRepresentation( 
            theContextualElement       =theContextualElement,
            theObject                  =theObject, 
            theTitle                   =theTitle, 
            theAdditionalParams        =theAdditionalParams
        )

    
    
					
					
    
    
    
           
    

            