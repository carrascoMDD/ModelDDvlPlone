# -*- coding: utf-8 -*-
#
# File: MDDLoadModules.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'


import transaction

from Acquisition                         import aq_get

from Products.CMFCore.utils              import getToolByName



from Products.ModelDDvlPloneTool.ModelDDvlPloneTool import ModelDDvlPloneTool


cMethodName_pgSetImportedModules    = 'pgSetImportedModules'





cModuleNamesWithGlobals = { 
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals' : [ 'ModelDDvlPloneTool_Globals', 'fgGlobalsAccessor', 'pgGlobalsMutator',],  
}


cModuleName_ModelDDvlPloneTool  = 'Products.ModelDDvlPloneTool.ModelDDvlPloneTool'
cClassName_ModelDDvlPloneTool   = 'ModelDDvlPloneTool'
cGlobalName_ImportedModules     = 'gImportedModules'
cSingletonId_ModelDDvlPloneTool = 'ModelDDvlPlone_tool'


cModuleName_ModelDDvlPloneConfiguration  = 'Products.ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration'
cClassName_ModelDDvlPloneConfiguration   = 'ModelDDvlPloneConfiguration'
cSingletonId_ModelDDvlPloneConfiguration = 'ModelDDvlPlone_configuration'


cModuleNamesWithTool = { 
    cModuleName_ModelDDvlPloneTool :          [ cClassName_ModelDDvlPloneTool,           cSingletonId_ModelDDvlPloneTool,          None,                        None,],  
    cModuleName_ModelDDvlPloneConfiguration : [ cClassName_ModelDDvlPloneConfiguration,  cSingletonId_ModelDDvlPloneConfiguration, 'fPersistentFieldsAccessor', 'pPersistentFieldsMutator',],  
}






# ##################################
# Must be synchronized with the constants of same names in Products.ModelDDvlPloneTool.ModelDDvlPloneTool
#


cModelDDvlPloneToolId = 'ModelDDvlPlone_tool'

cInstall_Tools_On_PortalSkinsCustom = True

cInstallPath_PortalSkinsCustom = [ 'portal_skins', 'custom',]


cModuleNamesToImport = [
    'Products.ModelDDvlPloneTool.MDDLinkedList',
    'Products.ModelDDvlPloneTool.MDDNestedContext',
    'Products.ModelDDvlPloneTool.MDDStringConversions',
    'Products.ModelDDvlPloneTool.PloneElement_TraversalConfig',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor_Constants',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_ImportExport_Constants',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Transactions',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Profiling',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Candidates',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_I18N',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Impact',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Permissions',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_PloneContent',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_TraversalConfigs',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval_Utils',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval',
    'Products.ModelDDvlPloneTool.MDD_RefactorComponents',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Export',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Import',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Bodies',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators_Plone',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Permissions_Definitions',    
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators',   
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Refactor', 
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Version',   
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Translation',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants',
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Globals',   
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache',  
    'Products.ModelDDvlPloneTool.ModelDDvlPloneTool',
    'Products.ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration',
]






def MDDLoadModules( 
    theContextualElement   =None, 
    theExtraModules        =[], 
    theReloadModules       =False, 
    theClearGlobals        =False,
    theClearPersistent     =False):
    """Exposed as an ExternalMethod.
    
    """
    return _fLoadModules( 
        theContextualElement   =theContextualElement,
        theExtraModules        =theExtraModules, 
        theReloadModules       =theReloadModules, 
        theClearGlobals        =theClearGlobals,
        theClearPersistent     =theClearPersistent,
    )
    
    
    


def fInstallContainer_Tools( theContextualElement):
    
    aPortalTool = getToolByName( theContextualElement, 'portal_url')
    if aPortalTool == None:
        return None
    
    unPortalRoot = aPortalTool.getPortalObject()                
    if unPortalRoot == None:
        return None
    
    if not cInstall_Tools_On_PortalSkinsCustom:
        return unPortalRoot
    
    if not cInstallPath_PortalSkinsCustom:
        return unPortalRoot
        
    
    aTraversedObject = unPortalRoot
    for aTraversal in cInstallPath_PortalSkinsCustom:
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



def fNewVoidLoadModulesReport():
    aReport = {
        'success':                       False,
        'theExtraModules':               [ ],
        'theReloadModules':              False,
        'theClearGlobals':               False,
        'theClearPersistent':            False,
        'theModulesBefore':              [ ],
        'theModulesToReload':            [ ],
        'theModulesToImport':            [ ],
        'theModulesImported':            [ ],
        'theModulesReloaded_1':          [ ],
        'theModulesGlobalsRetained_1':   [ ],
        'theModulesPersistentRetained_1':[ ],
        'theModulesSingletonsReCreated_1':[ ],
        'theModulesReloaded_2':          [ ],
        'theModulesGlobalsRetained_2':   [ ],
        'theModulesPersistentRetained_2':[ ],
        'theModulesSingletonsReCreated_2':[ ],
    }
    return aReport




def _fgModelDDvlPloneToolClass( theModelDDvlPloneToolModule=None):
    
    aModule = theModelDDvlPloneToolModule
    
    if not aModule:
        
        someModuleNameSteps = cModuleName_ModelDDvlPloneTool.split( '.')
        if someModuleNameSteps:
            
            try:
                aRootModule = __import__( cModuleName_ModelDDvlPloneTool, globals(), locals())
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
    
    aModelDDvlPloneToolClass = None
    try:
        aModelDDvlPloneToolClass = getattr( aModule, cClassName_ModelDDvlPloneTool)
    except:
        None
        
    return aModelDDvlPloneToolClass
    
    
       
 

def _fLoadModules( 
    theContextualElement  =None, 
    theExtraModules       =[], 
    theReloadModules      =False, 
    theClearGlobals       =False,
    theClearPersistent    =False):
    """Import extra modules. If not the first invocation, Reload all currently loaded framework modules, import all modules and the extra modules, and reload again all modules including the extra, saving or optionally discarding values of interesting globals, and re-creating or leaving the persistent singletons of classes in reloaded modules.
    http://localhost/modeldd/bpds/gvsig-i18n-manual-imported/MDDReload/?theInitGlobals=on
    
    """
    someModulesToReload     = []
    someModuleNamesToImport = []
    
    aLoadModulesReport = fNewVoidLoadModulesReport()
    aLoadModulesReport.update({
        'theExtraModules':       theExtraModules,
        'theReloadModules':      theReloadModules,
        'theClearGlobals':       theClearGlobals,
        'theClearPersistent':    theClearPersistent,
    })
    
    
    
    # #################################################
    """Retrieve the dictionary of loaded modules, stored as a global of the ModelDDvlPloneTool class.
    
    """                
    aModelDDvlPloneToolClass = _fgModelDDvlPloneToolClass()
    if not aModelDDvlPloneToolClass:
        return aLoadModulesReport
    
    someCurrentModules = None
    try:
        someCurrentModules = getattr( aModelDDvlPloneToolClass, cGlobalName_ImportedModules)
    except:
        None

    
    if not someCurrentModules:
        someCurrentModules = { }
    
    aLoadModulesReport[ 'theModulesBefore'] = someCurrentModules.keys()
    
    someImportedModules = someCurrentModules.copy()
    someCurrentModules  = someCurrentModules.copy()    
    
    
    # #################################################
    """Gather currently known modules.
    
    """
    for aModuleName in cModuleNamesToImport:
        if someCurrentModules.has_key( aModuleName):
            if theReloadModules:
                aModule = someCurrentModules.get( aModuleName, None)
                if aModule:
                    someModulesToReload.append( [ aModuleName, aModule, ])
        else:
            someModuleNamesToImport.append( aModuleName)
        
            
    # #################################################
    """Gather extra modules, that may be already known , or new to import.
    
    """
    for aModuleName in theExtraModules:
        if aModuleName in cModuleNamesToImport:
            if theReloadModules:
                aModule = someCurrentModules.get( aModuleName, None)
                if aModule and not( aModule in someModulesToReload):
                    someModulesToReload.append( [ aModuleName, aModule, ])
        else:
            someModuleNamesToImport.append( aModuleName)
            
       
            

    # #################################################
    """Reload all currently loaded modules, before import the extra modules.
    
    """        
                    
    for aModuleNameToReload, aModuleToReload in someModulesToReload:
        aLoadModulesReport[ 'theModulesToReload'].append( aModuleNameToReload)
        
        aReloaded, aGlobalsRetained, aPersistentRetained, aSingletonRecreated = _fReloadModule( 
            theContextualElement, 
            aModuleNameToReload, 
            aModuleToReload, 
            theClearGlobals, 
            theClearPersistent
        )
        if aReloaded:
            aLoadModulesReport[ 'theModulesReloaded_1'].append( aModuleNameToReload)
            if aGlobalsRetained:
                aLoadModulesReport[ 'theModulesGlobalsRetained_1'].append( aModuleNameToReload)
            if aPersistentRetained:
                aLoadModulesReport[ 'theModulesPersistentRetained_1'].append( aModuleNameToReload)
            if aSingletonRecreated:
                aLoadModulesReport[ 'theModulesSingletonsReCreated_1'].append( aModuleNameToReload)
            
        
        
        
    # #################################################
    """Import the modules.
    
    """        
    aLoadModulesReport[ 'theModulesToImport'] = [ aModuleNameToImport for aModuleNameToImport in someModuleNamesToImport]
        
    for aModuleNameToImport in someModuleNamesToImport:
        
        someModuleNameSteps = aModuleNameToImport.split( '.')
        if someModuleNameSteps:
            
            try:
                aRootModule = __import__( aModuleNameToImport, globals(), locals())
            except:
                None
            
            if aRootModule:                                
                aModule = aRootModule
                
                if len( someModuleNameSteps) > 1:
                    
                    someRemainingSteps = someModuleNameSteps[1:]
                    for aModuleNameStep in someRemainingSteps:                        
                        aModule = getattr( aModule, aModuleNameStep)
                        if not aModule:
                            break
            
                if aModule:
                    someImportedModules[ aModuleNameToImport] = aModule
                    aLoadModulesReport[ 'theModulesImported'].append( aModuleNameToImport)
                
                    
            
            
            
 
        
    
    # #################################################
    """Reload first the well known modules  in the order specified, and after reload all other modules - for which no load order was specified.
    
    """
    someSortedModulesAndNames = _fSortedModulesDict( someImportedModules)

    for aModuleNameToReload, aModuleToReload in someSortedModulesAndNames:
        if aModuleToReload:
            aReloaded, aGlobalsRetained, aPersistentRetained, aSingletonRecreated = _fReloadModule( 
                theContextualElement, 
                aModuleNameToReload, 
                aModuleToReload, 
                theClearGlobals, 
                theClearPersistent
            )
            if aReloaded:
                aLoadModulesReport[ 'theModulesReloaded_2'].append( aModuleNameToReload)
                if aGlobalsRetained:
                    aLoadModulesReport[ 'theModulesGlobalsRetained_2'].append( aModuleNameToReload)
                if aPersistentRetained:
                    aLoadModulesReport[ 'theModulesPersistentRetained_2'].append( aModuleNameToReload)
                if aSingletonRecreated:
                    aLoadModulesReport[ 'theModulesSingletonsReCreated_2'].append( aModuleNameToReload)
                
             
                        
                        
                        
                        
    # #################################################
    """Store the new dictionary of loaded modules in the global of the previous class, and in the class that has just been created when reloading its module.
    
    """           
    unModelDDvlPloneClassModule = someImportedModules.get( cModuleName_ModelDDvlPloneTool, None)
    if unModelDDvlPloneClassModule:
        
        aModelDDvlPloneToolClass = _fgModelDDvlPloneToolClass( unModelDDvlPloneClassModule)
        if aModelDDvlPloneToolClass:

            setattr( aModelDDvlPloneToolClass, cGlobalName_ImportedModules, someCurrentModules)

        

    aLoadModulesReport[ 'success'] = True
                                    
    return aLoadModulesReport





def _fSortedModulesDict( theModuleNamesAndModules):
    if not theModuleNamesAndModules:
        return theModuleNamesAndModules
    
    aHighestIndex = len( theModuleNamesAndModules) + 2
    
    someIndexesAndModules = [  ]
    for aModuleName in theModuleNamesAndModules.keys():
        aModule = theModuleNamesAndModules.get( aModuleName)
        if aModule:
            if aModuleName in cModuleNamesToImport:
                someIndexesAndModules.append( [ cModuleNamesToImport.index( aModuleName), aModuleName, aModule,])
                continue
            
            someIndexesAndModules.append( [ aHighestIndex, aModuleName, aModule,])
            aHighestIndex += 1
            
    someSortedIndexesAndModules = sorted ( someIndexesAndModules, lambda anA, otherA: cmp( anA[ 0], otherA[ 0]))
    someSortedModuleNamesAndModules = [ [ anEntry[ 1], anEntry[ 2],]  for anEntry in someSortedIndexesAndModules ]

    return someSortedModuleNamesAndModules






    
def _fReloadModule( theContextualElement, theModuleName, theModule, theClearGlobals=False, theClearPersistent=False):
    if ( not theModuleName) or ( not theModule):
        return [ False, False, False, False, ]

    someGlobals         = None
    aGlobalsClassName   = None
    aGlobalsMutatorName = None
    
    aGlobalsRetained    = False
    aPersistentRetained = False
    aSingletonRecreated = False

    
    aSingletonData        = None
    aSingletonClassName   = None
    aSingletonMutatorName = None
    aSingletonId          = None
    aSingleton            = None
    
    
    
    if not theClearGlobals:
        # ################################################
        """Get a copy of the interesting globals of the module, if any.
        
        """
        aClassAccesorAndMutatorNames = cModuleNamesWithGlobals.get ( theModuleName, None)
    
        if aClassAccesorAndMutatorNames:
            aGlobalsClassName, anAccessorName, aGlobalsMutatorName = aClassAccesorAndMutatorNames
            if aGlobalsClassName and anAccessorName and aGlobalsMutatorName:
                
                aClass = None
                try:
                    aClass = getattr( theModule, aGlobalsClassName)
                except:
                    None
                 
                if aClass:
                    
                    anInstance = None
                    try:
                        anInstance = aClass()
                    except:
                        None
                        
                    if anInstance:
                        anAccessor = None
                        try:
                            anAccessor = getattr( anInstance, anAccessorName)
                        except:
                            None
                            
                        if anAccessor:
                            try:
                                someGlobals = anAccessor()
                            except:
                                None

                            if someGlobals:
                                someGlobals = someGlobals.copy()
                                
                                

    if ( not theClearPersistent) and not ( theContextualElement == None):
        
        # ################################################
        """Get a copy of the interesting persistent information in the module singleton instance, if any.
        
        """
        aClassIdAccesorAndMutatorNames = cModuleNamesWithTool.get ( theModuleName, None)
    
        if aClassIdAccesorAndMutatorNames:
            aSingletonClassName, aSingletonId, anAccessorName, aSingletonMutatorName = aClassIdAccesorAndMutatorNames
            if aSingletonClassName and aSingletonId and theContextualElement:
                
                unInstallContainer = fInstallContainer_Tools( theContextualElement)
                if not( unInstallContainer == None):
                
                    try:
                        aSingleton = aq_get( unInstallContainer, aSingletonId, None, 1)
                    except:
                        None
            
                    if aSingleton:
                        
                        if anAccessorName:
                            
                            anAccessor = None
                            try:
                                anAccessor = getattr( aSingleton, anAccessorName)
                            except:
                                None
                                
                            if anAccessor:
                                try:
                                    aSingletonData = anAccessor( )
                                except:
                                    None

                                
    reload( theModule)
    
            
    if not theClearGlobals:
        # ################################################
        """Restore into the newly reloaded module the copy of the interesting globals of the module, if any.
        
        """
        if someGlobals and aGlobalsClassName and aGlobalsMutatorName:
        
            aClass = None
            try:
                aClass = getattr( theModule, aGlobalsClassName)
            except:
                None
             
            if aClass:
                
                anInstance = None
                try:
                    anInstance = aClass()
                except:
                    None
                    
                if anInstance:
                    aGlobalsMutator = None
                    try:
                        aGlobalsMutator = getattr( anInstance, aGlobalsMutatorName)
                    except:
                        None
             
                    if aGlobalsMutator:
                        try:
                            aGlobalsMutator( someGlobals)
                        except:
                            None
                            
                        aGlobalsRetained = True
                            
                        
                            
                            
    if ( not theClearPersistent) and not ( theContextualElement == None):
        # ################################################
        """Delete the current singleton instance of the module and create a new one, restoring the interesting persistent information, if any.
        
        """
            
        if aSingletonClassName and aSingletonId:

            unInstallContainer = fInstallContainer_Tools( theContextualElement)
            if not ( unInstallContainer == None):
                
                aSingletonClass = None
                try:
                    aSingletonClass = getattr( theModule, aSingletonClassName)
                except:
                    None
             
                if aSingletonClass:
                      
                    try:
                        unInstallContainer.manage_delObjects( [ aSingletonId,])
                    except:
                        None
            
                    transaction.commit()
                        
                    
                    try:
                        aSingleton = aq_get( unInstallContainer, aSingletonId, None, 1)
                    except:
                        None
            
                    if not aSingleton:                        
                
                         
                        unNuevoSingleton = None
                        try:
                            unNuevoSingleton = aSingletonClass( ) 
                        except:
                            None
                            
                        if unNuevoSingleton:
                            unInstallContainer._setObject( aSingletonId,  unNuevoSingleton)
                    
                            
                            if aSingletonMutatorName:
                                if aSingletonData:
                                
                                    aSingletonMutator = None
                                    try:
                                        aSingletonMutator = getattr( unNuevoSingleton, aSingletonMutatorName)
                                    except:
                                        None
                             
                                    if aSingletonMutator:
                                        try:
                                            aSingletonMutator( aSingletonData)
                                        except:
                                            None
                                            
                                        aPersistentRetained = True
                          
                            transaction.commit()
                            aSingletonRecreated = True
        
    return [ True, aGlobalsRetained, aPersistentRetained, aSingletonRecreated,]

        