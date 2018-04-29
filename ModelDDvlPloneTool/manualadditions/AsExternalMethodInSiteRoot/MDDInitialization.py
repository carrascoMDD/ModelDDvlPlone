# -*- coding: utf-8 -*-
#
# File: MDDInitialization.py
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

import sys
import traceback
import logging


import transaction

from Acquisition                         import aq_get

from Products.CMFCore.utils              import getToolByName








def MDDInitialization( 
    theContextualElement     =None, 
    theAllowInitialization   =False,):
    """Exposed as an ExternalMethod.
    
    """
    

    from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion import ModelDDvlPloneTool_Inicializacion

    from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion_Constants import cMDDInitializationDefinitions

    aModelDDvlPloneTool_Inicializacion = ModelDDvlPloneTool_Inicializacion()
    
    if aModelDDvlPloneTool_Inicializacion == None:
        return None

    if theContextualElement == None:
        aInformeVerifyOrInit = aModelDDvlPloneTool_Inicializacion.fNewVoidInformeVerifyOrInit()
        aInformeVerifyOrInit[ 'condition'] = 'No Contextual element supplied to MDDInitialization ExternalMethod'
        return aInformeVerifyOrInit

    if not _fCheckHasRole( theContextualElement, 'Manager'):
        aInformeVerifyOrInit = aModelDDvlPloneTool_Inicializacion.fNewVoidInformeVerifyOrInit()
        aInformeVerifyOrInit[ 'condition'] = 'Can not MDDInitialization if the user does not have Manager role on the current element'
        return aInformeVerifyOrInit

    aInformeVerifyOrInit = aModelDDvlPloneTool_Inicializacion.fVerifyOrInitialize( 
        theInitializationSpecification =cMDDInitializationDefinitions, 
        theContextualElement           =theContextualElement, 
        theAllowInitialization         =theAllowInitialization )
    

    return aInformeVerifyOrInit

    
    



def _fCheckHasRole( theContextualElement=None, theRole=''):
    if ( theContextualElement == None):
        return False
    
    if not theRole:
        return False
       
    unaRequest = theContextualElement.REQUEST
    if not unaRequest:
        return None
    
    unUserObject = unaRequest.get("AUTHENTICATED_USER", None)
    
    unosRoles = unUserObject.getRolesInContext( theContextualElement)
    if not unosRoles:
        return False
    
    aHasRole = theRole in unosRoles
    
    return aHasRole


