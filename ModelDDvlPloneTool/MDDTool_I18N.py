# -*- coding: utf-8 -*-
#
# File: MDDTool_I18N.py
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









class MDDTool_I18N:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """
    
    
    security = ClassSecurityInfo()
    

    
        
    # #####################################
    """Internationalisation methods.
    
    """

    
    security.declareProtected( permissions.View,  'fTranslateI18N')
    def fTranslateI18N( self, theContextualElement, theI18NDomain, theString, theDefault):
        """Localize a string from a domain into the language negotiated for the current request, or return a default.
        
        """
        
        return self.fModelDDvlPloneTool_Retrieval( theContextualElement).fTranslateI18N( theI18NDomain, theString, theDefault, theContextualElement)


    
    


    security.declarePublic( 'fTranslateI18NManyIntoDict')
    def fTranslateI18NManyIntoDict( self, 
        theContextualElement,
        theI18NDomainsStringsAndDefaults, 
        theResultDict                   =None):
        """Internationalization: build or update a dictionaty with the translations of all requested strings from the specified domain into the language preferred by the connected user, or return the supplied default.
        
        """
        
        return self.fModelDDvlPloneTool_Retrieval( theContextualElement).fTranslateI18NManyIntoDict( theContextualElement, theI18NDomainsStringsAndDefaults, theResultDict)
        
    
    
    
    
    
    

    security.declarePublic( 'fTranslationsBundle_ForChanges')
    def fTranslationsBundle_ForChanges( self, theContextualElement,):
        """The translations of change kinds, and property names of changes and change details, to be used in the presentation of changes.
        
        """
        
        return self.fModelDDvlPloneTool_Mutators( theContextualElement).fTranslationsBundle_ForChanges( theContextualElement,)
        
    
    
    
    
    

    security.declareProtected( permissions.View,  'fAsUnicode')
    def fAsUnicode( self, theContextualElement,  theString):
        """Decode a string from the system encoding into a unicode in-memory representation.
        
        """
        return self.fModelDDvlPloneTool_Retrieval( theContextualElement).fAsUnicode(theString, theContextualElement)

    

    
        
