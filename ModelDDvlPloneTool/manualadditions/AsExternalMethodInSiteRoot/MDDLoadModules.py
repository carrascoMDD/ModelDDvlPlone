# -*- coding: utf-8 -*-
#
# File: MDDLoadModules.py
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




# #######################################################
"""Configuration constants.

"""


cMDDLogLoadModulesErrors = True








# #######################################################
"""Modules Manager module and class names.

"""


cModulesManager_ModuleName    = 'Products.ModelDDvlPloneTool.MDDModulesManager'
cModulesManager_ClassName     = 'MDDModulesManager'








# #######################################################
# #######################################################




def _fNewVoidModulesListReport():
    aReport = {
        'success':                       False,
        'error_reports':                 [ ],
        
        'theLoadModulesSpecification':   { },
        
        'theLoadConstants_ModuleName':   '',
        'theLoadConstants_ConstantName': '',
        
        'theModulesAlreadyImported':     False,
        'theAllModulesImported':         False,
        
        'theImportedModules':            [ ],
        'theImportErrors':               [ ],
    }
    return aReport






def _fNewVoidLoadModulesReport():
    aReport = {
        'success':                       False,
        'error_reports':                 [ ],
        
        'theLoadModulesSpecification':   { },
        'theExtraModulesSpecifications': [ ],
        
        'theLoadConstants_ModuleName':   '',
        'theLoadConstants_ConstantName': '',
        'theReloadModules':              False,
        'theClearGlobals':               False,
        'theClearPersistent':            False,
        
        
        'theModulesBefore':              [ ],
        
        'theModulesToReload':            [ ],
        'theModulesToImport':            [ ],
        
        
        'theModulesReloaded_1':          [ ],
        'theModulesGlobalsRead_1':       [ ],
        'theModulesGlobalsRetained_1':   [ ],
        'theModulesSingletonsDeleted_1': [ ],
        'theModulesSingletonsReCreated_1':[ ],
        'theModulesPersistentRead_1':    [ ],
        'theModulesPersistentRetained_1':[ ],
        
        'theModulesWithReloadError_1':   [ ],
        
        
        'theModulesReloaded_2':          [ ],
        'theModulesGlobalsRead_2':       [ ],
        'theModulesGlobalsRetained_2':   [ ],
        'theModulesSingletonsDeleted_2': [ ],
        'theModulesSingletonsReCreated_2':[ ],
        'theModulesPersistentRead_2':    [ ],
        'theModulesPersistentRetained_2':[ ],

        'theModulesWithReloadError_2':   [ ],

        
        'theModulesImported':            [ ],
        'theModulesWithLoadError':       [ ],
        
        'theModulesWithGlobalsError':    [ ],
        'theModulesWithPersistentError': [ ],
        'theModulesWithSingletonsError': [ ],
    }
    return aReport





def _fNewVoidLoadModuleResult():
    aResult = {
        'success':                       False,
        'error_reports':                 [ ],
        'theModuleName':                 '',
        'theModule':                     None,
    }
    return aResult




def _fNewVoidReloadModuleResult():
    aResult = {
        'success':                       False,
        'error_reports':                 [ ],
        'theModuleName':                 '',
        'theModuleImplName':             '',
        'theModuleSpecification':        {},
        'theClearGlobals':               False,
        'theClearPersistent':            False,
        'theModule':                     None,
        
        'theModuleReloaded':             False,
        'theGlobalsRead':                False,
        'theGlobalsRetained':            False,
        'theSingletonDeleted':           False,        
        'theSingletonRecreated':         False,        
        'thePersistentRead':             False,
        'thePersistentRetained':         False,
    }
    return aResult





def _fNewVoidResolveSymbolResult():
    aResult = {
        'success':                       False,
        'error_reports':                 [ ],
        'theModule':                     None,
        'theSymbolName':                 '',
        'theSymbolValue':                None,
    }
    return aResult





def _fNewVoidLoadConstantsResult():
    aResult = _fNewVoidLoadModuleResult()
    aResult.update( _fNewVoidResolveSymbolResult())

    return aResult










# ###################################################
# ###################################################







def MDDModulesList( 
    theContextualElement          =None, 
    theLoadModulesSpecification   =None,
    theLoadConstants_ModuleName   =None,
    theLoadConstants_ConstantName =None,):
    """Exposed as an ExternalMethod invoked from template  http://localhost/modeldd/bpds/gvsig-i18n-manual-imported/MDDModules
   
    """
    
    aModulesListReport = _fNewVoidModulesListReport()
    
    if theContextualElement == None:
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList: No ContextualElement supplied')
        return aModulesListReport

    if not _fCheckHasRole( theContextualElement, 'Manager'):
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList: Can not List Modules if the user does not have Manager role on the current element')
        return aModulesListReport
        
    aModulesListReport.update({
        'theLoadModulesSpecification':    theLoadModulesSpecification,
        'theLoadConstants_ModuleName':    theLoadConstants_ModuleName,
        'theLoadConstants_ConstantName':  theLoadConstants_ConstantName,
    })
    

    

    
    aLoadModulesSpecification = theLoadModulesSpecification
    
    
    
    # #################################
    """When no load modules specification is supplied, one must be obtained by retrieving a constant from a module, whose names can be received as parameters, or forced or defaulted to values expressed in this external method, if configuration cosntants in this external methods allows. 
    
    """
    if not aLoadModulesSpecification:
        
        if not ( theLoadConstants_ModuleName and theLoadConstants_ConstantName):
            aModulesListReport[ 'error_reports'].append( 'MDDModulesList: No Load Modules Specification supplied, and are missing any of theLoadConstants_ModuleName or theLoadConstants_ConstantName')
            return aModulesListReport
            
            
        aLoadConstantsResult = _fLoadConstants(
            theContextualElement             =theContextualElement, 
            theLoadConstants_ModuleName      =theLoadConstants_ModuleName,
            theLoadConstants_ConstantName    =theLoadConstants_ConstantName,   
        )
        
        if ( not aLoadConstantsResult) or ( not aLoadConstantsResult.get( 'success', False)):
            aModulesListReport[ 'error_reports'].append( 'MDDModulesList: No Load Modules Specification obtained from module %s and constant name %s' % ( aLoadConstants_ModuleName, aLoadConstants_ConstantName,))
            return aModulesListReport
            
        aConstantValue = aLoadConstantsResult.get( 'theSymbolValue', None)
        if not aConstantValue:
            aModulesListReport[ 'error_reports'].append( 'MDDModulesList: No Load Modules Specification obtained from module %s and constant name %s' % ( aLoadConstants_ModuleName, aLoadConstants_ConstantName,))
            return aModulesListReport
        
        aLoadModulesSpecification = aConstantValue
        aModulesListReport.update({
            'theLoadModulesSpecification':    aLoadModulesSpecification,
        })

 
    if not aLoadModulesSpecification:
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList: No Load Modules Specification supplied, not could be obtained from ModelDDvlPloneToolLoadConstants')
        return aModulesListReport
    



    
    # #################################################
    """Get information supplied for the master module, with the class holding the globals for loaded modules .
    
    """      
    aMasterModuleSpecification = aLoadModulesSpecification.get( 'master_module', {})
    if not aMasterModuleSpecification:
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList: No Master Module Specification supplied')
        return aModulesListReport
    
     
    aMasterModuleName              = aMasterModuleSpecification.get( 'module_name', '')
    aMasterClassName               = aMasterModuleSpecification.get( 'class_name', '')
    aGlobalName_ModulesManager     = aMasterModuleSpecification.get( 'modules_manager_global', '')
    
    if not ( aMasterModuleName and aMasterModuleName):
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList: Missing Master Module name or Master Class name in Load Modules Specification')
        return aModulesListReport
 

    if not aGlobalName_ModulesManager:
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList: Missing Global name Modules Manager  in Load Modules Specification')
        return aModulesListReport
 
    
    
    # #################################################
    """Retrieve the Master class holding the globals with the dictionary of loaded modules.
    
    """                
    aMasterClass = _fMasterClass(
        theContextualElement   =theContextualElement,
        theMasterModule        =None,
        theMasterModuleName    =aMasterModuleName,
        theMasterClassName     =aMasterClassName,
    )
    if not aMasterClass:
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList: Master Class named %s not found in module %s' % ( aMasterClassName, aMasterModuleName,))
        return aModulesListReport
    
    
    
    
    
    
    # #################################################
    """Retrieve the Modules Manager from the Master Class global, and from the Modules Manager retrieve the dictionary of loaded modules, stored as a global of the Master class.
    
    """                               
    anModulesManagerGlobalRead = False
    try:
        aModulesManager = getattr( aMasterClass, aGlobalName_ModulesManager)
        anModulesManagerGlobalRead = True
    except:
        None
    if not anModulesManagerGlobalRead:  
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList: Could not read Global for Modules Manager named "%s" in Master Class named "%s" in module "%s"' % ( aGlobalName_ModulesManager, aMasterClassName, aMasterModuleName,))
        return aModulesListReport
    
    if not aModulesManager:
        aModulesListReport[ 'error_reports'].append( 'MDDModulesList:Empty Global for Modules Manager named "%s" in Master Class named "%s" in module "%s"' % ( aGlobalName_ModulesManager, aMasterClassName, aMasterModuleName,))
        return aModulesListReport
        

    someImportedModules    = aModulesManager.fImportedModules(    theContextualElement)
    if not someImportedModules:
        someImportedModules = {}
    someImportedModules  = someImportedModules.copy()   
    
    
    someImportErrorReports = aModulesManager.fImportErrorReports( theContextualElement)
    if not someImportErrorReports:
        someImportErrorReports = []
    someImportErrorReports  = someImportErrorReports[:]  
     
    
    aModulesListReport.update( {
        'success':             True,
        'theImportedModules':  sorted( someImportedModules.keys()),
        'theImportErrors':     someImportErrorReports,
    })

        
    return aModulesListReport

    



def MDDLoadModules( 
    theContextualElement          =None, 
    theLoadModulesSpecification   =None,
    theExtraModulesSpecifications =None, 
    theLoadConstants_ModuleName   =None,
    theLoadConstants_ConstantName =None,
    theReloadModules              =False, 
    theClearGlobals               =False,
    theClearPersistent            =False):
    """Exposed as an ExternalMethod invoked from template  http://localhost/modeldd/bpds/gvsig-i18n-manual-imported/MDDReload/?theClearGlobals=on&theClearPersistent=on
   
    """
    
    aLoadModulesReport = _fNewVoidLoadModulesReport()
    
    if theContextualElement == None:
        aLoadModulesReport[ 'error_reports'].append( 'MDDLoadModules: No ContextualElement supplied')
        return aLoadModulesReport

    if not _fCheckHasRole( theContextualElement, 'Manager'):
        aLoadModulesReport[ 'error_reports'].append( 'MDDLoadModules: Can not ReLoad Modules if the user does not have Manager role on the current element')
        return aLoadModulesReport
        
    aLoadModulesReport.update({
        'theLoadModulesSpecification':    theLoadModulesSpecification,
        'theExtraModulesSpecifications':  theExtraModulesSpecifications,
        'theLoadConstants_ModuleName':    theLoadConstants_ModuleName,
        'theLoadConstants_ConstantName':  theLoadConstants_ConstantName,
        'theReloadModules':               theReloadModules,
        'theClearGlobals':                theClearGlobals,
        'theClearPersistent':             theClearPersistent,
    })
    
    
        

    
    aLoadModulesSpecification = theLoadModulesSpecification
    
    
    
    # #################################
    """When no load modules specification is supplied, one must be obtained by retrieving a constant from a module, whose names can be received as parameters, or forced or defaulted to values expressed in this external method, if configuration cosntants in this external methods allows. 
    
    """
    if not aLoadModulesSpecification:
        
        if not ( theLoadConstants_ModuleName and theLoadConstants_ConstantName):
            aLoadModulesReport[ 'error_reports'].append( 'MDDLoadModules: No Load Modules Specification supplied, and are missing any of theLoadConstants_ModuleName or theLoadConstants_ConstantName')
            return aLoadModulesReport
            
        aLoadConstantsResult = _fLoadConstants(
            theContextualElement             =theContextualElement, 
            theLoadConstants_ModuleName      =theLoadConstants_ModuleName,
            theLoadConstants_ConstantName    =theLoadConstants_ConstantName,   
        )
        
        if ( not aLoadConstantsResult) or ( not aLoadConstantsResult.get( 'success', False)):
            aLoadModulesReport[ 'error_reports'].append( 'MDDLoadModules: No Load Modules Specification obtained from module %s and constant name %s' % ( aLoadConstants_ModuleName, aLoadConstants_ConstantName,))
            return aLoadModulesReport
            
        aLoadModulesSpecification = aLoadConstantsResult.get( 'theSymbolValue', None)
        if not aLoadModulesSpecification:
            aLoadModulesReport[ 'error_reports'].append( 'MDDLoadModules: No Load Modules Specification obtained from module %s and constant name %s' % ( aLoadConstants_ModuleName, aLoadConstants_ConstantName,))
            return aLoadModulesReport
        
        aLoadModulesReport.update({
            'theLoadModulesSpecification':    aLoadModulesSpecification,
        })

 
    if not aLoadModulesSpecification:
        aLoadModulesReport[ 'error_reports'].append( 'MDDLoadModules: No Load Modules Specification supplied, not could be obtained from ModelDDvlPloneToolLoadConstants')
        return aLoadModulesReport
    


    _fLoadModules( 
        theContextualElement          =theContextualElement,
        theLoadModulesSpecification   =aLoadModulesSpecification,
        theExtraModulesSpecifications =theExtraModulesSpecifications, 
        theReloadModules              =theReloadModules, 
        theClearGlobals               =theClearGlobals,
        theClearPersistent            =theClearPersistent,
        theLoadModulesReport          =aLoadModulesReport,
    )
    
    return aLoadModulesReport

    





 

def _fLoadModules( 
    theContextualElement          =None, 
    theLoadModulesSpecification   =None,
    theExtraModulesSpecifications =None, 
    theReloadModules              =False, 
    theClearGlobals               =False,
    theClearPersistent            =False,
    theLoadModulesReport          =None,):
    """Import specified and extra modules. 
    If not the first invocation, shall previously Reload all currently loaded framework modules, import all modules and the extra modules, and reload again all modules including the extra, saving or optionally discarding values of interesting globals, and re-creating or leaving the persistent singletons of classes in reloaded modules.
    
    """

    
    # #################################################
    """Get information supplied for the master module, with the class holding the globals for loaded modules .
    
    """      
    aMasterModuleSpecification = theLoadModulesSpecification.get( 'master_module', {})
    if not aMasterModuleSpecification:
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: No Master Module Specification supplied')
        return None
    
    aMasterModuleName              = aMasterModuleSpecification.get( 'module_name', '')
    aMasterClassName               = aMasterModuleSpecification.get( 'class_name', '')
    aMasterSingletonId             = aMasterModuleSpecification.get( 'singleton_id', '')
    aGlobalName_ModulesManager     = aMasterModuleSpecification.get( 'modules_manager_global', '')
    

    
    # #################################################
    """Predefined Modules specifications programmed into the tool product source code.
    
    """
    someModulesSpecifications       = theLoadModulesSpecification.get( 'modules', [])
    someSpecifiedModuleNames        =         [ aModuleSpec.get( 'module_name', '')                 for aModuleSpec in someModulesSpecifications if aModuleSpec.get( 'module_name', '')]
    someModulesSpecificationsByName = dict( [ [ aModuleSpec.get( 'module_name', '') , aModuleSpec,] for aModuleSpec in someModulesSpecifications if aModuleSpec.get( 'module_name', '')])
    

    
    # #################################################
    """Extra Modules specifications supplied specifically in this request, override the predefined specifications
    
    """
     
    someExtraModuleNames = [ ]   
    if theExtraModulesSpecifications:
        someExtraModuleNames                 =         [ aModuleSpec.get( 'module_name', '')                 for aModuleSpec in theExtraModulesSpecifications if aModuleSpec.get( 'module_name', '')]
        someExtraModulesSpecificationsByName = dict( [ [ aModuleSpec.get( 'module_name', '') , aModuleSpec,] for aModuleSpec in theExtraModulesSpecifications if aModuleSpec.get( 'module_name', '')])
        
        someModulesSpecificationsByName.update( someExtraModulesSpecificationsByName)        
        
        
        
    someCurrentModules = None
   
        
    # #################################################
    """Retrieve the Master class holding the globals with the dictionary of loaded modules.
    
    """                
    aMasterClass = _fMasterClass(
        theContextualElement   =theContextualElement,
        theMasterModule        =None,
        theMasterModuleName    =aMasterModuleName,
        theMasterClassName     =aMasterClassName,
    )
    if not aMasterClass:
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Master Class named %s not found in module %s' % ( aMasterClassName, aMasterModuleName,))
        return theLoadModulesReport
    
        
        
     
    
    # #################################################
    """Retrieve the Modules Manager from the Master Class global, and from the Modules Manager retrieve the dictionary of loaded modules, stored as a global of the Master class.
    
    """                               
    anModulesManagerGlobalRead = False
    try:
        aModulesManager = getattr( aMasterClass, aGlobalName_ModulesManager)
        anModulesManagerGlobalRead = True
    except:
        None
    if not anModulesManagerGlobalRead:  
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Could not read Global for Modules Manager named "%s" in Master Class named "%s" in module "%s"' % ( aGlobalName_ModulesManager, aMasterClassName, aMasterModuleName,))
        return theLoadModulesReport

    if not aModulesManager:
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Empty Global for Modules Manager named "%s" in Master Class named "%s" in module "%s"' % ( aGlobalName_ModulesManager, aMasterClassName, aMasterModuleName,))
        return theLoadModulesReport
        
    
    someCurrentModules    = aModulesManager.fImportedModules(    theContextualElement)
    if not someCurrentModules:
        someCurrentModules = {}
    someCurrentModules  = someCurrentModules.copy()   
    
            
    theLoadModulesReport[ 'theModulesBefore'] = sorted( someCurrentModules.keys())
    
    
    
    
    someModuleNamesToImport = [ ]
    someModuleNamesToReload = [ ]
    someModulesToReload     = [ ]
    
    someReloadedModules     = [ ]
    someImportedModules     = [ ]


    
    
    
    # #################################################
    """Gather currently known modules.
    
    """
    for aModuleName in someSpecifiedModuleNames:
        if someCurrentModules.has_key( aModuleName):
            if theReloadModules:
                aModuleAndImpl = someCurrentModules.get( aModuleName, None)
                if aModuleAndImpl:
                    aModule = aModuleAndImpl[ 0]
                    if aModule:
                        someModuleNamesToReload.append( aModuleName)
                        someModulesToReload.append( [ aModuleName, aModule, ])
                        theLoadModulesReport[ 'theModulesToReload'].append( aModuleName)
        else:
            someModuleNamesToImport.append( aModuleName)
            theLoadModulesReport[ 'theModulesToImport'].append( aModuleName)
        
            
            
            
            
            
    # #################################################
    """Gather extra modules, that may be already known, or new to import.
    
    """
    for aModuleName in someExtraModuleNames:
        if aModuleName in someSpecifiedModuleNames:
            if theReloadModules:
                aModuleAndImpl = someCurrentModules.get( aModuleName, None)
                if aModuleAndImpl:
                    aModule = aModuleAndImpl[ 0]
                    if aModule and not( aModuleName in someModuleNamesToReload):
                        someModuleNamesToReload.append( aModuleName)
                        someModulesToReload.append( [ aModuleName, aModule, ])
                        theLoadModulesReport[ 'theModulesToReload'].append( aModuleName)
        else:
            someModuleNamesToImport.append( aModuleName)
            theLoadModulesReport[ 'theModulesToImport'].append( aModuleName)
       
                
                
                
                
                
            

    # #################################################
    """Reload all currently loaded modules, preserving tool singleton, and preserving class globals and persistent data in singletons, unless otherwise specified .
    
    """        
                    
    for aModuleNameToReload, aModuleToReload in someModulesToReload:
        
        
        aModuleSpecification = someModulesSpecificationsByName.get( aModuleNameToReload, None)
        if aModuleSpecification:
 
            aReloadModuleResult = _fReloadModule( 
                theContextualElement         =theContextualElement, 
                theLoadModulesSpecification  =theLoadModulesSpecification,
                theModuleSpecification       =aModuleSpecification,
                theModule                    =aModuleToReload, 
                theClearGlobals              =theClearGlobals, 
                theClearPersistent           =theClearPersistent,
            )
            if not aReloadModuleResult:
                theLoadModulesReport[ 'theModulesWithReloadError_1'].append( aModuleNameToReload)        
                continue

            theLoadModulesReport[ 'error_reports'].extend( aReloadModuleResult.get( 'error_reports', []))
            
            if not aReloadModuleResult.get( 'success', False):
                theLoadModulesReport[ 'theModulesWithReloadError_1'].append( aModuleNameToReload)               
                continue
            
            aModule = aReloadModuleResult.get( 'theModule', False)
            if not aModule:
                theLoadModulesReport[ 'theModulesWithReloadError_1'].append( aModuleNameToReload)               
                continue
            
            
            someReloadedModules.append( [ aModuleNameToReload, aModule, ])

            
            if aReloadModuleResult.get( 'theModuleReloaded', False):
                theLoadModulesReport[ 'theModulesReloaded_1'].append( aModuleNameToReload)
                
            if aReloadModuleResult.get( 'theGlobalsRead', False):
                theLoadModulesReport[ 'theModulesGlobalsRead_1'].append( aModuleNameToReload)
                
            if aReloadModuleResult.get( 'theGlobalsRetained', False):
                theLoadModulesReport[ 'theModulesGlobalsRetained_1'].append( aModuleNameToReload)

            if aReloadModuleResult.get( 'theSingletonDeleted', False):
                theLoadModulesReport[ 'theModulesSingletonsDeleted_1'].append( aModuleNameToReload)
                
            if aReloadModuleResult.get( 'theSingletonRecreated', False):
                theLoadModulesReport[ 'theModulesSingletonsReCreated_1'].append( aModuleNameToReload)

            if aReloadModuleResult.get( 'thePersistentRead', False):
                theLoadModulesReport[ 'theModulesPersistentRead_1'].append( aModuleNameToReload)

            if aReloadModuleResult.get( 'thePersistentRetained', False):
                theLoadModulesReport[ 'theModulesPersistentRetained_1'].append( aModuleNameToReload)
                

                
               
                
                
        
    # #################################################
    """Import the modules that where not already registered as loaded in the master class global. BEcause they were not loaded, no measures are taken to preserve class globals, singletons or persistent data in singletons.
    
    """        
        
    for aModuleNameToImport in someModuleNamesToImport:
        
        aModuleSpecification = someModulesSpecificationsByName.get( aModuleNameToImport, None)
        
        aModule = None
        aLoadModuleResult = _fLoadModule( 
            theContextualElement    =theContextualElement, 
            theModuleName           =aModuleNameToImport,
            theModuleSpecification  =aModuleSpecification,
            theResult               =None,)
        
        if not aLoadModuleResult:
            theLoadModulesReport[ 'theModulesWithLoadError'].append( aModuleNameToImport)               
            continue
        
        theLoadModulesReport[ 'error_reports'].extend( aLoadModuleResult.get( 'error_reports', []))
 
        if not aLoadModuleResult.get( 'success', False):
            theLoadModulesReport[ 'theModulesWithLoadError'].append( aModuleNameToImport)               
            continue
        
        aModule = aLoadModuleResult.get( 'theModule', False)
        if not aModule:
            theLoadModulesReport[ 'theModulesWithLoadError'].append( aModuleNameToImport)               
            continue
        
        
        someImportedModules.append( [ aModuleNameToImport,  aModule, ])
        
        
        theLoadModulesReport[ 'theModulesImported'].append( aModuleNameToImport)
            
            
 
        
        
        
        
        
        

        
    allModules = { }
        
    
    # #################################################
    """Reload all currently loaded modules, preserving tool singleton, and preserving class globals and persistent data in singletons, unless otherwise specified .
    
    """
    
    
    someSortedModulesAndNames = _fSortedModulesAndNames( 
        theImportedModules      =someImportedModules, 
        theReloadedModules      =someReloadedModules, 
        theSpecifiedModuleNames =someSpecifiedModuleNames, 
        theExtraModuleNames     =someExtraModuleNames,
    )

    for aModuleNameToReload, aModuleToReload in someSortedModulesAndNames:
        if aModuleToReload:
            
            aModuleSpecification = someModulesSpecificationsByName.get( aModuleNameToReload, None)
            if aModuleSpecification:

                aReloadModuleResult = _fReloadModule( 
                    theContextualElement         =theContextualElement, 
                    theLoadModulesSpecification  =theLoadModulesSpecification,
                    theModuleSpecification       =aModuleSpecification,
                    theModule                    =aModuleToReload, 
                    theClearGlobals              =theClearGlobals, 
                    theClearPersistent           =theClearPersistent,
                )
                if not ( aReloadModuleResult):
                    theLoadModulesReport[ 'theModulesWithReloadError_2'].append( aModuleNameToReload)        
                    continue
    
                theLoadModulesReport[ 'error_reports'].extend( aReloadModuleResult.get( 'error_reports', []))
                
                if not aReloadModuleResult.get( 'success', False):
                    theLoadModulesReport[ 'theModulesWithReloadError_2'].append( aModuleNameToReload)               
                    continue
                
                aModule = aReloadModuleResult.get( 'theModule', False)
                if not aModule:
                    theLoadModulesReport[ 'theModulesWithReloadError_2'].append( aModuleNameToReload)               
                    continue
    
                aModuleImplName = aReloadModuleResult.get ( 'theModuleImplName', '')
                
                allModules[ aModuleNameToReload] = [ aModule, aModuleImplName,]
                    
                
                if aReloadModuleResult.get( 'theModuleReloaded', False):
                    theLoadModulesReport[ 'theModulesReloaded_2'].append( aModuleNameToReload)
                    
                if aReloadModuleResult.get( 'theGlobalsRead', False):
                    theLoadModulesReport[ 'theModulesGlobalsRead_2'].append( aModuleNameToReload)
                    
                if aReloadModuleResult.get( 'theGlobalsRetained', False):
                    theLoadModulesReport[ 'theModulesGlobalsRetained_2'].append( aModuleNameToReload)
    
                if aReloadModuleResult.get( 'theSingletonDeleted', False):
                    theLoadModulesReport[ 'theModulesSingletonsDeleted_2'].append( aModuleNameToReload)
                    
                if aReloadModuleResult.get( 'theSingletonRecreated', False):
                    theLoadModulesReport[ 'theModulesSingletonsReCreated_2'].append( aModuleNameToReload)
    
                if aReloadModuleResult.get( 'thePersistentRead', False):
                    theLoadModulesReport[ 'theModulesPersistentRead_2'].append( aModuleNameToReload)
    
                if aReloadModuleResult.get( 'thePersistentRetained', False):
                    theLoadModulesReport[ 'theModulesPersistentRetained_2'].append( aModuleNameToReload)
                                    
                
             
                        
                        
                        
    # #################################################
    """FINAL AND MOST IMPORTANT SIDE EFFECT: To store the new dictionary of loaded modules, and the list of load errors, creating an  instance of Modules Manager to hold imported modules, and be stored as a global of the master class that has just been created when reloading the master module.
    
    """       
    
    from Products.ModelDDvlPloneTool.MDDModulesManager import MDDModulesManager as aModulesManagerClass
    #if not unModulesManagerModule:
        ## #################################################
        #"""Fail if no Modules Manager module found.
        
        #"""
        #theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Modules Manager Module named %s not found. Can not create instance to hold imported modules and be stored as a global of the master class' % cModulesManager_ModuleName,)
        #return None
    

    #aModulesManagerClass = _fResolveClass( 
        #theContextualElement   =theContextualElement,
        #theMasterModule        =unMasterModule,
        #theMasterModuleName    =None,
        #theMasterClassName     =cModulesManager_ClassName,
    #)
    #if not aModulesManagerClass:
        ## #################################################
        #"""Fail if no Modules Manager class found.
        
        #"""
        #theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Modules Manager Class named %s not found in loaded Modules Manager module %s' % ( cModulesManager_ClassName, cModulesManager_ModuleName,))
        #return None
    

        
    # #################################################
    """Retrieve Master Module and Class, To store as a global a new instance of Modules Manager, with the new dictionary of loaded modules, and the list of load errors, creating an  instance of Modules Manager to hold imported modules, and be stored as a global of the master class that has just been created when reloading the master module.
    
    """       
    unMasterModuleAndImpl = allModules.get( aMasterModuleName, None)
    if not unMasterModuleAndImpl:
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Master Module named %s not found to store imported modules global' % aMasterModuleName,)
        return None
    
    unMasterModule = unMasterModuleAndImpl[ 0]
    if not unMasterModule:
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Empty Master Module named %s' % aMasterModuleName,)
        return None
 
        
    aMasterClass = _fMasterClass( 
        theContextualElement   =theContextualElement,
        theMasterModule        =unMasterModule,
        theMasterModuleName    =None,
        theMasterClassName     =aMasterClassName,
    )
    if not aMasterClass:
        # #################################################
        """Fail if no Master class found to store the loaded modules in a global.
        
        """
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Master Class named %s not found in loaded Master module %s' % ( aMasterClassName, aMasterModuleName,))
        return None
        
    
        
    # #################################################
    """Join modules specification from the load specification and the extra modules speficied.
    
    """    
    aNewLoadModulesSpecification =  theLoadModulesSpecification.copy()
    aNewLoadModulesSpecification[ 'modules'] = aNewLoadModulesSpecification.get( 'modules', [])[:]
    if theExtraModulesSpecifications:
        aNewLoadModulesSpecification[ 'modules'] += theExtraModulesSpecifications
        
        
        
    # #################################################
    """Create a Modules Manager instance to hold the new dictionary of loaded modules and the list of load errors, to be stored into the global of the Master class.
    
    """    
    aModulesManager = aModulesManagerClass( 
        theMasterClass              =aMasterClass, 
        theLoadModulesSpecification =aNewLoadModulesSpecification, 
        theImportedModules          =allModules, 
        theImportErrorReports       =theLoadModulesReport[ 'error_reports'][:],
    )
    if not aModulesManager:
        # #################################################
        """Fail if no Modules Manager instance could be created to store the loaded modules in a global of the Master Class.
        
        """
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Could not create Modules Manager instance to store in Master Class named %s in loaded Master module %s' % ( aMasterClassName, aMasterModuleName,))
        return None

    
    
                        
    # #################################################
    """FINAL AND MOST IMPORTANT SIDE EFFECT: To store as a global of the Master Class the new instance of Model Manager with the dictionary of loaded modules, and the list of load errors.
    
    """      


    aModulesManagerGlobalWritten = False
    try:
        setattr( aMasterClass, aGlobalName_ModulesManager, aModulesManager)
        anImportedModulesGlobalWritten = True
    except:
        None
    if not anImportedModulesGlobalWritten:
        # #################################################
        """Fail if could not store  the loaded modules in a global in the Master class.
        
        """
        theLoadModulesReport[ 'error_reports'].append( '_fLoadModules: Could not write Global for Imported Modules named %s in Master Class named %s in module %s' % ( aGlobalName_ModulesManager, aMasterClassName, aMasterModuleName,))
        return None
            

    theLoadModulesReport[ 'success'] = True
                                    
    return None



    
def _fReloadModule( 
    theContextualElement         =None, 
    theLoadModulesSpecification  =None,
    theModuleSpecification       =None,
    theModule                    =None, 
    theClearGlobals              =False, 
    theClearPersistent           =False):
    
    aResult = _fNewVoidReloadModuleResult()
    aResult.update( {
        'theModule':              theModule,
        'theModuleSpecification': theModuleSpecification,
        'theClearGlobals':        theClearGlobals,
        'theClearPersistent':     theClearPersistent,
    })
    
    
   
    if theContextualElement == None:
        aResult[ 'error_reports'].append( '_fReloadModule: No ContextualElement supplied')
        return aResult
    
    if not theLoadModulesSpecification:
        aResult[ 'error_reports'].append( '_fReloadModule: No theLoadModulesSpecification supplied')
        return aResult

    if not theModuleSpecification:
        aResult[ 'error_reports'].append( '_fReloadModule: No theModuleSpecification supplied')
        return aResult
    
    aModuleName = theModuleSpecification.get ( 'module_name', '')
    if not aModuleName:
        aResult[ 'error_reports'].append( '_fReloadModule: Module Name is empty')
        return aResult
    
    
    aResult.update( {
        'theModuleName':          aModuleName,
    })    
    
    
    
    
    aModuleNameToLoad = aModuleName
    
    aModuleImplName = theModuleSpecification.get ( 'module_impl', '')
    if aModuleImplName:
        aModuleNameToLoad = aModuleImplName
    else:
        aModuleImplName = aModuleNameToLoad
    
    
    aResult.update( {
        'theModuleNameToLoad':    aModuleNameToLoad,
        'theModuleImplName':      aModuleImplName,
    })
    
    
    someModuleNameSteps = aModuleNameToLoad.split( '.')
    if not someModuleNameSteps:    
        aResult[ 'error_reports'].append( '_fReloadModule: Module Name without any root module name or module steps')
        return aResult
            
    if not theModule:
        aResult[ 'error_reports'].append( '_fReloadModule: No theModule supplied')
        return aResult
        
    
  
    
    aGlobalsClassName    = None
    aGlobalsAccessorName = None
    aGlobalsMutatorName  = None
    
    
    aSingletonClassName         = None
    aPersistentDataMutatorName  = None
    aPersistentDataAccessorName = None
    aSingletonId                = None
    
    unInstallContainer              = None
    unInstallContainerTitleAndPath  = ''

    
    aModuleWithGlobalsSpec = theModuleSpecification.get ( 'global_spec', None)
    if aModuleWithGlobalsSpec:
        aGlobalsClassName    = aModuleWithGlobalsSpec.get( 'class_name', None)
        aGlobalsAccessorName = aModuleWithGlobalsSpec.get( 'globals_accessor', None)
        aGlobalsMutatorName  = aModuleWithGlobalsSpec.get( 'globals_mutator', None)    
    
    
    
    aModuleWithSingletonSpec = theModuleSpecification.get ( 'singleton_spec', None)
    if aModuleWithSingletonSpec:
        aSingletonClassName         = aModuleWithSingletonSpec.get( 'class_name',   None)
        aSingletonId                = aModuleWithSingletonSpec.get( 'singleton_id', None)
        aPersistentDataAccessorName = aModuleWithSingletonSpec.get( 'persistent_data_accessor_name', None)
        aPersistentDataMutatorName  = aModuleWithSingletonSpec.get( 'persistent_data_mutator_name',  None)
    
        
    if aSingletonClassName and aSingletonId:
        unInstallContainer = _fInstallContainer_Tools( theContextualElement, theLoadModulesSpecification, )
        if unInstallContainer == None:
            aResult[ 'error_reports'].append( '_fReloadModule: No _fInstallContainer_Tools')
            return aResult
        
        unInstallContainerTitleAndPath = ''
        try:
            unInstallContainerTitleAndPath += unInstallContainer.Title()
        except:
            None
        try:
            unInstallContainerTitleAndPath += ' at %s' % '/'.join( unInstallContainer.getPhysicalPath())
        except:
            None
        
        
        
        
    someGlobals       = None
    aSingleton        = None
    aSingletonData    = None
        
    
    # ################################################
    """Get a copy of the interesting globals of the module, if any, unless it has been requested to clear the global values, in which case it is not neccessary to save the globals values.
    
    """
    if ( not theClearGlobals) and aGlobalsClassName and aGlobalsAccessorName and aGlobalsMutatorName:
            
        aClass = None
        try:
            aClass = getattr( theModule, aGlobalsClassName)
        except:
            None
         
        if not aClass:
            aResult[ 'error_reports'].append( '_fReloadModule: Failure in module %s getattr globals class named %s to Get a copy' % ( aModuleNameToLoad, aGlobalsClassName, ))
            
        else:
            
            anInstance = None
            try:
                anInstance = aClass()
            except:
                None
                
            if not anInstance:
                aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s instantiating globals class named %s to Get a copy' % ( aModuleNameToLoad, aGlobalsClassName, ))
                
            else:
                
                aGlobalsAccessor = None
                try:
                    aGlobalsAccessor = getattr( anInstance, aGlobalsAccessorName)
                except:
                    None
                    
                if not aGlobalsAccessor:
                    aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s retrieving from instance of globals class named %s the globals accessor method named %s' % ( aModuleNameToLoad, aGlobalsClassName, aGlobalsAccessorName))
                
                else:
                    
                    aGlobalsRead = False 
                    try:
                        someGlobals = aGlobalsAccessor()
                        aGlobalsRead = True
                    except:
                        None

                    if not aGlobalsRead:
                        aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s invoking on instance of globals class named %s the globals accessor method named %s' % ( aModuleNameToLoad, aGlobalsClassName, aGlobalsAccessorName))
                    
                    else:
                        aResult[ 'theGlobalsRead'] = True
                        if someGlobals:
                            someGlobals = someGlobals.copy()
                      
                        
                        
                            
    # ################################################
    """Get a copy of the interesting persistent information in the module singleton instance, if any,  unless it has been requested to clear the persistent data values, in which case it is not neccessary to save the persistent data values.
    
    """
    if ( not theClearPersistent) and  aSingletonClassName and aSingletonId and aPersistentDataAccessorName and aPersistentDataMutatorName:
            
        try:
            aSingleton = aq_get( unInstallContainer, aSingletonId, None, 1)
        except:
            None

        if aSingleton == None:
            aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s retrieving a singleton with id %s  from container  %s' % ( aModuleNameToLoad, aSingletonId, unInstallContainerTitleAndPath,))
            
            
        else:
            anAccessor = None
            try:
                anAccessor = getattr( aSingleton, aPersistentDataAccessorName)
            except:
                None
                
            if not anAccessor:
                aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s retrieving from singleton with id %s the persistent accessor method named %s' % ( aModuleNameToLoad, aSingletonId, aPersistentDataAccessorName))
                
            else:
                aPersistentRead = False
                try:
                    aSingletonData = anAccessor( )
                    aPersistentRead = True
                except:
                    None
    
                if not aPersistentRead:
                    aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s invoking on instance with id %s the persistent accessor method named %s' % ( aModuleNameToLoad, aSingletonId, aPersistentDataAccessorName))
                else:
                    aResult[ 'thePersistentRead'] = True
                    if aSingletonData:
                        aSingletonData = aSingletonData.copy()
                                
                                
                                
                                
    # ###############################################
    """Delete singleton now, otherwise the system won't be able to pickle the object after reloading the module (is a class object different from the class of the existing singleton).
    
    """
    if aSingletonClassName and aSingletonId:
        aSingletonDeleted = False
        try:
            unInstallContainer.manage_delObjects( [ aSingletonId,])
            aSingletonDeleted = True
        except:
            None
            
        if not aSingletonDeleted:
            aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s Deleting singleton with id %s from container %s' % ( aModuleNameToLoad, aSingletonId, unInstallContainerTitleAndPath))
        else:
            transaction.commit()
            aResult[ 'theSingletonDeleted'] = True
            aSingleton = None                                                

               
                        
                    
        
        
    # ################################################
    """Actual reload of the module from source or compiled code.
    
    """
    aModuleReloaded = False
    try:
        reload( theModule)
        aModuleReloaded = True
    except:
        unaExceptionInfo = sys.exc_info()
        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
        unInformeExcepcion = 'Exception during fReloadModule reload module\n' 
        try:
            unInformeExcepcion += 'theModule=%s\n' % aModuleNameToLoad
        except:
            None
        try:
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
        except:
            None
        try:
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
        except:
            None
        unInformeExcepcion += unaExceptionFormattedTraceback   
        
        aResult[ 'error_reports'].append( unInformeExcepcion)
        
        if cMDDLogLoadModulesErrors:
            aLogger = logging.getLogger( 'ModelDDvlPloneTool')
            aLogger.error( unInformeExcepcion) 
                 
    
    
    if not aModuleReloaded:
        aResult[ 'error_reports'].append( '_fReloadModule: Failure reloading  module %s' %  aModuleNameToLoad)
        return aResult
    else:
        aResult[ 'theModuleReloaded'] = True
    
    
        
        
    
    
    # ################################################
    """Restore into the newly reloaded module the copy of the interesting globals of the module, if any.
    
    """
    if ( not theClearGlobals) and aGlobalsClassName and aGlobalsAccessorName and aGlobalsMutatorName and ( not ( someGlobals == None)):
        
        aClass = None
        try:
            aClass = getattr( theModule, aGlobalsClassName)
        except:
            None
         
        if not aClass:
            aResult[ 'error_reports'].append( '_fReloadModule: Failure in module %s getattr globals class named %s' % ( aModuleNameToLoad, aGlobalsClassName, ))
            
        else:
            
            anInstance = None
            try:
                anInstance = aClass()
            except:
                None
                
            if not anInstance:
                aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s instantiating globals class named %s' % ( aModuleNameToLoad, aGlobalsClassName, ))
                
            else:
                aGlobalsMutator = None
                try:
                    aGlobalsMutator = getattr( anInstance, aGlobalsMutatorName)
                except:
                    None
         
                if not aGlobalsMutator:
                    aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s retrieving from instance of globals class named %s the globals mutator method named %s' % ( aModuleNameToLoad, aGlobalsClassName, aGlobalsMutatorName))
                else:
                    
                    aGlobalsMutated = False 
                    try:
                        aGlobalsMutator( someGlobals)
                        aGlobalsMutated = True
                    except:
                        None
                        
                    if not aGlobalsMutated:
                        aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s invoking on instance of globals class named %s the globals mutator method named %s' % ( aModuleNameToLoad, aGlobalsClassName, aGlobalsMutatorName))
                    
                    else: 
                        aResult[ 'theGlobalsRetained'] = True
                            
                        
                            
                            
    # ################################################
    """Create a new singleton instance of the module.
    
    """
        
    if aSingletonClassName and aSingletonId:

        unNuevoSingleton = None
        
        aSingletonClass = None
        try:
            aSingletonClass = getattr( theModule, aSingletonClassName)
        except:
            None
     
        if not aSingletonClass:
            aResult[ 'error_reports'].append( '_fReloadModule: Failure in module %s getattr singleton class named %s' % ( aModuleNameToLoad, aSingletonClassName, ))
            
            
        else:
            
            unNuevoSingleton = None
            try:
                unNuevoSingleton = aSingletonClass( ) 
            except:
                None
                
            if unNuevoSingleton == None:
                
                aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s instantiating singleton class named %s' % ( aModuleNameToLoad, aSingletonClassName, ))

            else:
                
                aSingletonAddedToContainer = False
                try:
                    unInstallContainer._setObject( aSingletonId,  unNuevoSingleton)
                    transaction.commit()
                    aSingletonAddedToContainer = True
                except:
                    None
                    
                if not aSingletonAddedToContainer:
                    aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s adding to container instantiated singleton of class named %s in container %s' % ( aModuleNameToLoad, aSingletonClassName, unInstallContainerTitleAndPath,))
                    
                else:
                    aSingleton = unNuevoSingleton
                    aResult[ 'theSingletonRecreated'] = True
                        
                        
                
    # ################################################
    """Restore on the singleton the interesting persistent information saved above, if any.
    
    """
    if ( not theClearPersistent) and  aSingletonClassName and aSingletonId and aPersistentDataAccessorName and aPersistentDataMutatorName and ( not ( aSingleton == None)) and ( not ( aSingletonData == None)):

        aSingletonMutator = None
        try:
            aSingletonMutator = getattr( aSingleton, aPersistentDataMutatorName)
        except:
            None
 
        if not aSingletonMutator:
            aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s retrieving from instance with id %s of singleton class named %s the singleton mutator method named %s' % ( aModuleNameToLoad, aSingletonId, aSingletonClassName, aPersistentDataMutatorName))
            
        else:
            aSingletonMutated = False
            try:
                aSingletonMutator( aSingletonData)
                aSingletonMutated = True
            except:
                None
                
            if not aSingletonMutated:
                aResult[ 'error_reports'].append( '_fReloadModule: Failure in  module %s invoking on instance with id %s of singleton class named %s the globals mutator method named %s' % ( aModuleNameToLoad, aSingletonId, aSingletonClassName, aPersistentDataMutatorName))
            else:
                transaction.commit()
                aResult[ 'thePersistentRetained'] = True
                
                
                
    aResult.update( {
        'success': True,
    })
    
        
    return aResult

        







def _fInstallContainer_Tools( theContextualElement, theLoadModulesSpecification, ):
    
    if theContextualElement == None:
        return None

    
    aPortalTool = getToolByName( theContextualElement, 'portal_url')
    if aPortalTool == None:
        return None
    
    unPortalRoot = aPortalTool.getPortalObject()                
    if unPortalRoot == None:
        return None
    
    if not theLoadModulesSpecification:
        return unPortalRoot
    
    if theLoadModulesSpecification.get( 'install_tools_on_portal_root', False):
        return unPortalRoot
        
    anInstallPath = theLoadModulesSpecification.get( 'install_tools_path', False)
    if not anInstallPath:
        return unPortalRoot
    
    
    aTraversedObject = unPortalRoot
    for aTraversal in anInstallPath:
        aNextObject = None
        try:
            aNextObject = aTraversedObject[ aTraversal]
        except ValueError, AttributeError:
            None
        if aNextObject == None:
            return None
        
        aTraversedObject = aNextObject
        
    if aTraversedObject == None:
        return None
    
    return aTraversedObject







def _fMasterClass( 
    theContextualElement   =None,
    theMasterModule        =None,
    theMasterModuleName    =None,
    theMasterClassName     =None,):
 
    if theContextualElement == None:
        return None
    
    if not theMasterClassName:
        return None
   
    if ( not theMasterModule) and ( not theMasterModuleName):
        return None
    
    
    aModule = theMasterModule
    
    if not aModule:

        someModuleNameSteps = theMasterModuleName.split( '.')
        if someModuleNameSteps:
            
            aRootModule = None
            try:
                aRootModule = __import__( theMasterModuleName, globals(), locals())
            except:
                None
            
            if not aRootModule:                                
                return None
            
            aModule = aRootModule
            
            if len( someModuleNameSteps) > 1:
                
                someRemainingSteps = someModuleNameSteps[1:]
                for aModuleNameStep in someRemainingSteps:  
                    aNextModule = None
                    try:
                        aNextModule = getattr( aModule, aModuleNameStep)
                    except:
                        None
                    if not aNextModule:
                        return None
                    aModule = aNextModule   
        
    if not aModule:
        return None
    
    aMasterClass = None
    try:
        aMasterClass = getattr( aModule, theMasterClassName)
    except:
        None
        
    return aMasterClass
    
    







def _fResolveClass( 
    theContextualElement   =None,
    theModule              =None,
    theModuleName          =None,
    theClassName           =None,):
    
    if theContextualElement == None:
        return None
    
    if not theClassName:
        return None
   
    if ( not theModule) and ( not theModuleName):
        return None
    
    
    aModule = theModule
    
    if not aModule:

        someModuleNameSteps = theModuleName.split( '.')
        if someModuleNameSteps:
            
            aRootModule = None
            try:
                aRootModule = __import__( theModuleName, globals(), locals())
            except:
                None
            
            if not aRootModule:                                
                return None
            
            aModule = aRootModule
            
            if len( someModuleNameSteps) > 1:
                
                someRemainingSteps = someModuleNameSteps[1:]
                for aModuleNameStep in someRemainingSteps:  
                    aNextModule = None
                    try:
                        aNextModule = getattr( aModule, aModuleNameStep)
                    except:
                        None
                    if not aNextModule:
                        return None
                    aModule = aNextModule   
        
    if not aModule:
        return None
    
    aClass = None
    try:
        aClass = getattr( aModule, theClassName)
    except:
        None
        
    return aClass
    
    
       

def _fSortedModulesAndNames( 
    theImportedModules      =None, 
    theReloadedModules      =None, 
    theSpecifiedModuleNames =None, 
    theExtraModuleNames     =None,):
    """Return a list of module names and modules, in the order given by theSpecified and theExtra modules names.
    
    """
    
    someSpecifiedModuleNames = theSpecifiedModuleNames
    if not someSpecifiedModuleNames:
        someSpecifiedModuleNames = []
        
    someExtraModuleNames = theExtraModuleNames
    if not someExtraModuleNames:
        someExtraModuleNames = []
        
    allModuleNames = someSpecifiedModuleNames + someExtraModuleNames
    
    
    someImportedModules = theImportedModules
    if not someImportedModules:
        someImportedModules = []
        
    someReloadedModules = theReloadedModules
    if not someReloadedModules:
        someReloadedModules = []
        
    allModules = someReloadedModules + someImportedModules
    if not allModules:
        return []
    
    
    aHighestIndex = len( allModuleNames) + 2
    
    someIndexesAndModules = [  ]
    for aModuleName, aModule in allModules:
        
        if aModuleName and aModule:
            
            aModuleIndex = -1
            try:
                aModuleIndex = allModuleNames.index( aModuleName)
            except:
                None
                
            if aModuleIndex >= 0:
                someIndexesAndModules.append( [ aModuleIndex,  aModuleName, aModule,])
 
            else:                
                someIndexesAndModules.append( [ aHighestIndex, aModuleName, aModule,])
                aHighestIndex += 1
            
                
    someSortedIndexesAndModules = sorted ( someIndexesAndModules, lambda anA, otherA: cmp( anA[ 0], otherA[ 0]))
    someSortedModuleNamesAndModules = [ [ anEntry[ 1], anEntry[ 2],]  for anEntry in someSortedIndexesAndModules ]

    return someSortedModuleNamesAndModules







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











 

def _fLoadConstants( 
    theContextualElement             =None, 
    theLoadConstants_ModuleName      =None,
    theLoadConstants_ConstantName    =None,):
    """Obtain the LoadConstants specification to load the modules of the tool application, and resolve the symbol with the specification, returning its value.
    
    """
    aLoadConstantsResult = _fNewVoidLoadConstantsResult()
    aLoadConstantsResult.update({
        'theModuleName':       theLoadConstants_ModuleName,
        'theSymbolName':       theLoadConstants_ConstantName,
    })
    
    if ( not theLoadConstants_ModuleName) or ( not theLoadConstants_ConstantName):
        return aLoadConstantsResult
        
    aModuleSpecification = { 'module_name': theLoadConstants_ModuleName,  'global_spec': {}, 'singleton_spec': {}, }

    _fLoadModule(
        theContextualElement   =theContextualElement,
        theModuleName          =theLoadConstants_ModuleName,
        theModuleSpecification =aModuleSpecification,
        theResult              =aLoadConstantsResult,
    )
    if not aLoadConstantsResult.get( 'success', False):
        return aLoadConstantsResult
    
    aModule = aLoadConstantsResult.get( 'theModule', None)
    if not aModule:
        return aLoadConstantsResult
    
    
    _fResolveSymbol( 
        theContextualElement  =theContextualElement, 
        theModule             =aModule,
        theSymbolName         =theLoadConstants_ConstantName,
        theResult             =aLoadConstantsResult,
    )  
    if not aLoadConstantsResult.get( 'success', False):
        return aLoadConstantsResult
    
    return aLoadConstantsResult







def _fLoadModule( 
    theContextualElement  =None, 
    theModuleName         =None,
    theModuleSpecification=None,
    theResult             =None,):
    """Load the module.
    
    """

    aResult = theResult
    if aResult == None:
        aResult = _fNewVoidLoadModuleResult()
        
    aResult.update({
        'theModuleName':       theModuleName,
    })
        
    if theContextualElement == None:
        aResult[ 'error_reports'].append( '_fLoadModule: No ContextualElement supplied')
        return aResult
    
    if not theModuleName:
        aResult[ 'error_reports'].append( '_fLoadModule: No Module Name supplied')
        return aResult
    
    
    aModuleNameToLoad = theModuleName
 
    if theModuleSpecification:
        aModuleImplName = theModuleSpecification.get ( 'module_impl', '')
        if aModuleImplName:
            aModuleNameToLoad = aModuleImplName
    
    
    aResult.update( {
        'theModuleNameToLoad':    aModuleNameToLoad,
    })
                   
            
    someModuleNameSteps = aModuleNameToLoad.split( '.')
    if not someModuleNameSteps:    
        aResult[ 'error_reports'].append( '_fLoadModule: Module Name without any root module name or module steps')
        return aResult
    
    
    

    # #################################################
    """Import the root module.
    
    """        

    aRootModule = None
    
    try:
        aRootModule = __import__( aModuleNameToLoad, globals(), locals())
    except:
        unaExceptionInfo = sys.exc_info()
        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
        unInformeExcepcion = 'Exception during _fLoadModule __import__ root module\n' 
        try:
            unInformeExcepcion += 'theModuleName=%s\n' % aModuleNameToLoad
        except:
            None
        try:
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
        except:
            None
        try:
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
        except:
            None
        unInformeExcepcion += unaExceptionFormattedTraceback   
        
        aResult[ 'error_reports'].append( unInformeExcepcion)                
        
        if cMDDLogLoadModulesErrors:
            aLogger = logging.getLogger( 'MDDLoadModules')
            aLogger.error( unInformeExcepcion) 
        
        return aResult
    
    
    if not aRootModule:
        aResult[ 'error_reports'].append( '_fLoadModule: Root Module was not __import__ ed')
        return aResult
        
        
    if len( someModuleNameSteps) == 1:
        aResult.update( {
            'success':   True,
            'theModule': aRootModule,
        })
        return aResult
    
    
   
 

    # #################################################
    """Traverse module steps from the root module.
    
    """        
        
    aModule = aRootModule
    
    someStepsAfterRoot = someModuleNameSteps[1:]
    for aModuleNameStep in someStepsAfterRoot:                        
        try:
            aModule = getattr( aModule, aModuleNameStep)
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            unInformeExcepcion = 'Exception during _fLoadModule getattr module name step\n' 
            try:
                unInformeExcepcion += 'theModuleName=%s  , aModuleNameStep=%s\n' % ( aModuleNameToLoad, aModuleNameStep)
            except:
                None
            try:
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            except:
                None
            try:
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            except:
                None
            unInformeExcepcion += unaExceptionFormattedTraceback   
            
            aModule = None
            
            aResult[ 'error_reports'].append( unInformeExcepcion)                
            
            if cMDDLogLoadModulesErrors:
                aLogger = logging.getLogger( 'MDDLoadModules')
                aLogger.error( unInformeExcepcion) 
                
            return aResult

            
        if not aModule:
            aResult[ 'error_reports'].append( '_fLoadModule: Load Module %s step %s failed getattr' % ( aModuleNameToLoad, aModuleNameStep,))
            return aResult
        
        

    if not aModule:
        aResult[ 'error_reports'].append( '_fLoadModule: Module %s Not Loaded' % aModuleNameToLoad)
        return aResult
        
    aResult.update( {
        'success':   True,
        'theModule': aModule,
    })
    return aResult
            









def _fResolveSymbol( 
    theContextualElement  =None, 
    theModule             =None,
    theSymbolName         =None,
    theResult             =None,):
    """Obtain the value of a symbol in the module.
    
    """

    aResult = theResult
    if aResult == None:
        aResult = _fNewVoidResolveSymbolResult()
    aResult.update({
        'theSymbolName':       theSymbolName,
    })
        
    
    if not theSymbolName:
        aResult[ 'error_reports'].append( '_fResolveSymbol: No Symbol Name supplied')
        return aResult
    
    if not theModule:
        aResult[ 'error_reports'].append( '_fResolveSymbol: No Module supplied')
        return aResult
        
    
    

    # #################################################
    """Resolve the symbol in the module.
    
    """        

    aSymbolValue         = None
    aSymbolValueResolved = False   
    
    try:
        aSymbolValue = getattr( theModule, theSymbolName)
        aSymbolValueResolved = True
    except:
        unaExceptionInfo = sys.exc_info()
        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
        unInformeExcepcion = 'Exception during _fResolveSymbol getattr symbol name\n' 
        try:
            unInformeExcepcion += 'theModuleName=%s ' %  theModule.__name__
        except:
            None
        try:
            unInformeExcepcion += 'theSymbolName=%s\n' % theSymbolName
        except:
            None
        try:
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
        except:
            None
        try:
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
        except:
            None
        unInformeExcepcion += unaExceptionFormattedTraceback   
        
        
        if cMDDLogLoadModulesErrors:
            aLogger = logging.getLogger( 'MDDLoadModules')
            aLogger.error( unInformeExcepcion) 


        

    if not aSymbolValueResolved:
        aResult[ 'error_reports'].append( '_fResolveSymbol: Symbol %s Not Resolved' % theSymbolName)
        return aResult

    
    
    aResult.update( {
        'success':         True,
        'theSymbolValue':  aSymbolValue,
    })
    return aResult
            





