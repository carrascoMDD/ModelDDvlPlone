# -*- coding: utf-8 -*-
#
# File: MDDTool_Translations.py
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









class MDDTool_Translations:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """
    
    

    security = ClassSecurityInfo()
    
   
    
    
    
    
        
    # #############################################################
    """Translation retrieval and management methods.
    
    """


    security.declareProtected( permissions.View, 'fNewTranslation')
    def fNewTranslation(self, 
        theTimeProfilingResults     =None,
        theOriginalObject           =None, 
        theNewTranslationContainerKind  =None,
        theNewLanguage           =None,
        theFallbackStrategy        =None,
        theNewTitle                 =None,
        theNewId                    =None,
        theAdditionalParams         =None):
        """Create a new translation of the original object which shall be a root, with the new translation name as given as parameter, as a whole object network copy of the source root object and its contents."
        
        """
                
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theOriginalObject)

        someMDDNewTranslationTypeConfigs   =  aModelDDvlPloneTool_Retrieval.getMDDTypeCopyConfigs(   theOriginalObject)        
        somePloneNewTranslationTypeConfigs =  aModelDDvlPloneTool_Retrieval.getPloneTypeCopyConfigs( theOriginalObject)        
                
        return self.fModelDDvlPloneTool_Translation( theOriginalObject).fNewTranslation( 
            theTimeProfilingResults          =theTimeProfilingResults,
            theModelDDvlPloneTool            =self,
            theModelDDvlPloneTool_Retrieval  =aModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators   =self.fModelDDvlPloneTool_Mutators( theOriginalObject),
            theOriginalObject                =theOriginalObject, 
            theNewTranslationContainerKind   =theNewTranslationContainerKind,
            theNewLanguage                   =theNewLanguage,
            theFallbackStrategy              =theFallbackStrategy,
            theNewTitle                      =theNewTitle,
            theNewId                         =theNewId,
            theMDDNewTranslationTypeConfigs  =someMDDNewTranslationTypeConfigs, 
            thePloneNewTranslationTypeConfigs=somePloneNewTranslationTypeConfigs, 
            theAdditionalParams              =theAdditionalParams
        )


   

   

    

    
        
