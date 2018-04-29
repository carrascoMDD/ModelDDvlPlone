# -*- coding: utf-8 -*-
#
# File: MDDModulesManager.py
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


from AccessControl import ClassSecurityInfo

# #######################################################################
"""Configuration constants: to log exceptions.

"""


cMDDLogLoadModulesErrors = True



_cParamsAccess_KeyNotFound_Sentinel = object()



# #######################################################################
"""Load the modules that compose the application organized by the master class supplied, according to the supplied modules specification.

"""

class MDDModulesManager:
    
    security = ClassSecurityInfo()

    
    def __init__( self, 
        theMasterClass              =None, 
        theLoadModulesSpecification =None, 
        theImportedModules          =None, 
        theImportErrorReports       =None):
        
        self.vModulesAlreadyImported      = False
        self.vAllModulesImported          = False
        self.vMasterClass                 = theMasterClass
        self.vLoadModulesSpecification    = theLoadModulesSpecification

        
        """Dictionary holding imported modules by name.
        
        """
        self.vImportedModules      = { }
        if theImportedModules:
            self.vImportedModules        = theImportedModules
            self.vModulesAlreadyImported = True
            
        
        """List of errors while importing modules.
        
        """
        self.vImportErrorReports   = [ ]
        if theImportErrorReports:
            self.vImportErrorReports = theImportErrorReports
            
        

    
    
    # #######################################################
    """Accessors
    
    """
    security.declarePrivate( 'fModulesAlreadyImported')
    def fModulesAlreadyImported( self,
        theContextualObject =None, ):
        
        return self.vModulesAlreadyImported
        
    
    
    security.declarePrivate( 'fAllModulesImported')
    def fAllModulesImported( self,
        theContextualObject =None, ):
        
        return self.vAllModulesImported
        
    
        
    security.declarePrivate( 'fImportedModules')
    def fImportedModules( self,
        theContextualObject =None, ):
        
        return self.vImportedModules
        
    
    
        
    security.declarePrivate( 'fImportErrorReports')
    def fImportErrorReports( self,
        theContextualObject =None, ):
        
        return self.vImportErrorReports
        
    
    
    
    
    
    
            
    # #######################################################
    """Module and module component resolution
    
    """
    
     
    security.declarePrivate( 'fImportedModuleResolvedSymbol')
    def fImportedModuleResolvedSymbol( self, 
        theContextualObject =None, 
        theModuleName       ='', 
        theComponentName    =''):

        if theContextualObject == None:
            self._pRecordLoadModuleError( theContextualObject, 'Error fImportedModuleResolvedSymbol parameter missing theContextualObject; theModuleName %s, theComponentName %s' % ( theModuleName or '?', theComponentName or '?',))
            return None
        
        if not theModuleName:
            self._pRecordLoadModuleError( theContextualObject, 'Error fImportedModuleResolvedSymbol parameter missing theModuleName;  theComponentName' % ( theComponentName or '?'))
            return None
        

        aModuleAndImplName = self._fImportedModuleAndImplName( theContextualObject, theModuleName)
        if not ( aModuleAndImplName and aModuleAndImplName[ 0]):
            self._pRecordLoadModuleError( theContextualObject, 'Error fImportedModuleResolvedSymbol no result _fImportedModuleAndImplName; theModuleName %s, theComponentName %s' % ( theModuleName or '?', theComponentName or '?',))
            return None
        
        aModule    = aModuleAndImplName[ 0]
        anImplName = aModuleAndImplName[ 1]
        
        aComponentName = theComponentName
        if not aComponentName:
            aModuleNameSteps = anImplName.split( '.')
            if aModuleNameSteps:
                aComponentName = aModuleNameSteps[-1:][ 0]

        if not aComponentName:
            self._pRecordLoadModuleError( theContextualObject, 'Error fImportedModuleResolvedSymbol no component name; anImplName %s' % ( anImplName or '?'))
            return None

        aComponentResolved = False
        aComponent = None
        try:
            aComponent = getattr( aModule, aComponentName)
            aComponentResolved = True
        except:
            None
            
        if not aComponentResolved:
            self._pRecordLoadModuleError( theContextualObject, 'Error fImportedModuleResolvedSymbol component not resolved; theModuleName %s, aComponentName %s' % ( theModuleName or '?', aComponentName or '?',))
            return None
        
        return aComponent
    
    

            
    
    

    security.declarePrivate( '_fImportedModuleAndImplName')
    def _fImportedModuleAndImplName( self, 
        theContextualObject =None, 
        theModuleName       =''):
        
        if theContextualObject == None:
            self._pRecordLoadModuleError( theContextualObject, 'Error _fImportedModuleAndImplName parameter missing theContextualObject; theModuleName %s' % ( theModuleName or '?'))
            return None
        
        if not theModuleName:
            self._pRecordLoadModuleError( theContextualObject, 'Error _fImportedModuleAndImplName parameter missing theModuleName' )
            return [ None, None,]
        
        if not self.vModulesAlreadyImported:
            self._pImportModules( theContextualObject)
            
        someImportedModules = self.fImportedModules()
        if not someImportedModules:
            self._pRecordLoadModuleError( theContextualObject, 'Error _fImportedModuleAndImplName no self.fImportedModules();  theModuleName %s' % ( theModuleName or '?'))
            return [ None, None,]
             
            
        aModuleAndImplName = someImportedModules.get( theModuleName, None)
        if aModuleAndImplName and aModuleAndImplName[ 0]:
            return  aModuleAndImplName

        self._pRecordLoadModuleError( theContextualObject, 'Error _fImportedModuleAndImplName module not found;  theModuleName %s' % ( theModuleName or '?'))
        
    
        return None
    
    
    
    
    
    
    def _pImportModules( self, theContextualObject=None):
        
        if theContextualObject == None:
            self._pRecordLoadModuleError( theContextualObject, 'Error _pImportModules parameter missing theContextualObject')
            return self

        
        if self.vModulesAlreadyImported:
            return self

        if not self.vMasterClass:
            self._pRecordLoadModuleError( theContextualObject, 'Error _pImportModules no self.vMasterClass')
            return self

        if not self.vLoadModulesSpecification:
            self._pRecordLoadModuleError( theContextualObject, 'Error _pImportModules no self.vLoadModulesSpecification')
            return self
        

        someModulesSpecifications       = self.vLoadModulesSpecification.get( 'modules', [])
        
        someSpecifiedModuleNames        =         [ aModuleSpec.get( 'module_name', '')                 for aModuleSpec in someModulesSpecifications if aModuleSpec.get( 'module_name', '')]
        someModulesSpecificationsByName = dict( [ [ aModuleSpec.get( 'module_name', '') , aModuleSpec,] for aModuleSpec in someModulesSpecifications if aModuleSpec.get( 'module_name', '')])
        
        
        
        
        
        # #################################################
        """Retrieve the dictionary of loaded modules, stored as a global of the master class class.
        
        """                

        someImportedModules = self.fImportedModules()
        
        if not someImportedModules:
            someImportedModules = { }
        
        
        
        
        # #################################################
        """Determine module names to import.
        
        """
        someModuleNamesToImport = [ ]
        for aModuleName in someSpecifiedModuleNames:
            if not someImportedModules.has_key( aModuleName):
                someModuleNamesToImport.append( aModuleName)
            
           
            
                
        # #################################################
        """Import  modules.
        
        """        
        someImportedModules = { }

        for aModuleNameToImport in someModuleNamesToImport:

            
            aModuleSpecification = someModulesSpecificationsByName.get( aModuleNameToImport, None)
            if not aModuleSpecification:
                self._pRecordLoadModuleError( theContextualObject, 'Error _pImportModules no ModuleSpecification found for module named %s' % aModuleNameToImport)
                
            else:
            
                aModuleNameToLoad = aModuleNameToImport
                
                aModuleImplName   = aModuleSpecification.get( 'module_impl', None)
                if aModuleImplName:
                    aModuleNameToLoad = aModuleImplName
                    
                else:
                    aModuleImplName   = aModuleNameToLoad
                            
                    
                someModuleNameSteps = aModuleNameToLoad.split( '.')
                if not someModuleNameSteps:
                    self._pRecordLoadModuleError( theContextualObject, 'Error _pImportModules no steps in module to load named %s' % aModuleNameToLoad)
                    
                else:
                           
                    aRootModule = None
                    try:
                        aRootModule = __import__( aModuleNameToLoad, globals(), locals())
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                        unInformeExcepcion = 'Exception during _pImportModules __import__ root module\n' 
                        try:
                            unInformeExcepcion += 'aModuleNameToImport=%s\n' % aModuleNameToImport
                        except:
                            None
                        try:
                            unInformeExcepcion += 'aModuleNameToLoad=%s\n' % aModuleNameToLoad
                        except:
                            None
                        try:
                            unInformeExcepcion += 'aModuleImplName=%s\n' % aModuleImplName
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
                        
                        aRootModule = None
    
                        self._pRecordLoadModuleError( theContextualObject, unInformeExcepcion)
    
                    if not aRootModule:
                        self._pRecordLoadModuleError( theContextualObject, 'Error _pImportModules no RootModule %s loaded' % aModuleNameToLoad)
                        
                    else:
                        aModule = aRootModule
                        
                        if len( someModuleNameSteps) > 1:
                            
                            someRemainingSteps = someModuleNameSteps[1:]
                            for aModuleNameStep in someRemainingSteps: 
                                try:
                                    aModule = getattr( aModule, aModuleNameStep)
                                except:
                                    unaExceptionInfo = sys.exc_info()
                                    unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                                    unInformeExcepcion = 'Exception during _pImportModules getattr module name step\n' 
                                    try:
                                        unInformeExcepcion += 'aModuleNameToImport=%s,  aModuleNameToLoad=%s, aModuleImplName=%s, aModuleNameStep=%s\n' % ( aModuleNameToImport, aModuleNameToLoad, aModuleImplName, aModuleNameStep)
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

                                    self._pRecordLoadModuleError( theContextualObject, unInformeExcepcion)

                                    break
                                    
                                if not aModule:
                                    break
                    
                        if not aModule:
                            self._pRecordLoadModuleError( theContextualObject, 'Error _pImportModules no Module %s loaded and resolved' % aModuleNameToLoad)
                            
                        else:
                            someImportedModules[ aModuleNameToImport] = [ aModule, aModuleImplName,]
                            
                        
        self.vImportedModules = someImportedModules
                
        self.vModulesAlreadyImported = True    
        
        someImportedModules = self.fImportedModules()
        for aModuleName in someSpecifiedModuleNames:
            aImportedModuleAndImpl = someImportedModules.get( aModuleName, None)
            if ( not aImportedModuleAndImpl) or not ( aImportedModuleAndImpl[ 0]):
                self.vAllModulesImported = False
                return self
  
        self.vAllModulesImported = True
        
        return self

     
        
    
    
    
    
    
    
    def _pRecordLoadModuleError( self,
        theContextualElement = None,
        theErrorMessage      = '',):
        
        if theContextualElement == None:
            return self
        
        if not theErrorMessage:
            return self
        
        anErrorMessage = 'MDDModulesManager: %s' % theErrorMessage
        
        if self.vImportErrorReports:
            self._pRecordLoadModuleError( anErrorMessage)
        
        if cMDDLogLoadModulesErrors:
            aLogger = logging.getLogger( 'ModelDDvlPlone')
            aLogger.error( anErrorMessage) 
            
        return self
    
                
    
                