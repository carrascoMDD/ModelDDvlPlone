# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Inicializacion.py
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


from AccessControl import ClassSecurityInfo

##code-section module-header #fill in your manual code here


import sys
import traceback


from StringIO                       import StringIO


import logging

import transaction

from Acquisition                    import aq_get



from Products.ExternalMethod.ExternalMethod import ExternalMethod




    

from Products.CMFCore               import permissions
from Products.CMFCore.utils         import getToolByName



from ModelDDvlPloneToolSupport import fMillisecondsNow, cIndent

from ModelDDvlPloneTool_Inicializacion_Constants import *




from ModelDDvlPloneTool              import ModelDDvlPloneTool

from Products.ModelDDvlPloneConfiguration.ModelDDvlPloneConfiguration import ModelDDvlPloneConfiguration, cModelDDvlPloneConfigurationId


##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here


cLogExceptions          = True

cLogInformeVerifyOrInit     = True




##/code-section after-schema

class ModelDDvlPloneTool_Inicializacion:
    """
    """
    security = ClassSecurityInfo()



    security.declarePrivate('fPortalRoot')
    def fPortalRoot( self, theContextualElement=None):
        
        if theContextualElement == None:
            return None
        
        aPortalTool = getToolByName( theContextualElement, 'portal_url')
        if aPortalTool == None:
            return None
        
        unPortalRoot = aPortalTool.getPortalObject()                
        if unPortalRoot == None:
            return None
        
        return unPortalRoot
        
    

    def fInstallContainer_Traversal( self, thePortalRoot=None, theTraversalPath=None):

        if thePortalRoot == None:
            return None
        
        if not theTraversalPath:
            return thePortalRoot
        
        aTraversedObject = thePortalRoot
        for aTraversal in theTraversalPath:
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
            
            
    
  
    


    def fPackageClass_Traversal( self, thePackageName=None, theClassName=None):
        if not thePackageName or not theClassName:
            return None
        

        someModuleNameSteps = thePackageName.split( '.')
        if someModuleNameSteps:
            
            try:
                aRootModule = __import__( thePackageName, globals(), locals())
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
    
        
    
    
    
    
    def fNewVoidInformeVerifyOrInit( self):
        unInforme = { 
            'title':             '',
            'type':              'external_methods_and_tool_singletons',
            'allow_initialization':    False,
            'success':           False,
            'condition':         '',
            'exception':         '',
            'external_methods':  self.fNewVoidInformeVerifyOrInitTodosExternalMethods(),
            'tool_singletons':   self.fNewVoidInformeVerifyOrInitTodosToolSingletons(),
        }
        return unInforme
    
    

   
    def fNewVoidInformeVerifyOrInitTodosExternalMethods( self):
        unInforme = {
            'type':         'external_methods',
            'success':      False,
            'methods':      [],
        }
        return unInforme    
    
    
    
    
    
    def fNewVoidInformeVerifyOrInitExternalMethod( self):
        unInforme = { 
            'type':                      'external_method',   
            'success':                   False,
            'status':                    '',           
            'committed':                 False,
            'install_path':              None,
            'ext_method_module':         '',
            'ext_method_id':             '',
            'ext_method_title':          '',
            'ext_method_function':       '',
            'required':                  False,
         }
        return unInforme

    
        
    
   
    def fNewVoidInformeVerifyOrInitTodosToolSingletons( self):
        unInforme = {
            'type':         'tool_singletons',
            'success':      False,
            'tools':        [],
        }
        return unInforme    
    
        

    def fNewVoidInformeVerifyOrInitToolSingleton( self):
        unInforme = { 
            'type':                     'tool',   
            'success':                  False,
            'status':                   '',           
            'committed':                False,
            'install_path':             '',
            'singleton_id':             '',
            'tool_module':             '',
            'tool_class':               '',
            'required':                 False,
       }
        return unInforme

        
    
    
    
    
    
    def fVerifyOrInitialize_ModelDDvlPloneFramework( self, theContextualElement=None, theAllowInitialization=False, ):
        """Verify or Initialize, and report,  tool singletons and external methods of the ModelDDvlPlone framework.
        
        """
        return self.fVerifyOrInitialize( theInitializationSpecification=cMDDInitializationDefinitions, theContextualElement=theContextualElement, theAllowInitialization=theAllowInitialization, )
      

    
    
    
    
     
    def fVerifyOrInitialize( self, 
        theInitializationSpecification =None, 
        theContextualElement           =None, 
        theAllowInitialization         =False, ):
        """Verify or Initialize, and report, all specified tool singletons and external methods.
        
        """
        
        if not theInitializationSpecification:
            return None

        if theContextualElement == None:
            return None
        
        unInforme = self.fNewVoidInformeVerifyOrInit()
        
        try:
            
            unInforme.update( {
                'allow_initialization':        ( theAllowInitialization and True) or False,
                'title':                       theInitializationSpecification.get( 'title', ''),
            })

            if theAllowInitialization:
                if not self.fCheckInitializationPermissions( theContextualElement):
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'user_can_NOT_initialize %s' % theInitializationSpecification.get( 'title', '')
                    return unInforme
                
            unPortalRoot = self.fPortalRoot( theContextualElement)
            if unPortalRoot == None:
                unInforme[ 'success']   =  False
                unInforme[ 'condition'] = 'No_Portal_Root'
                return unInforme
                


            
            
            # #######################################################
            """Verify or Initialize, and report, all specified external methods.
            
            """
            anAllExternalMethodReports = unInforme.get( 'external_methods', None)
            someExternalMethodReports = anAllExternalMethodReports.get( 'methods', None)
            if someExternalMethodReports == None:
                someExternalMethodReports = [ ]
                anAllExternalMethodReports[ 'methods'] = someExternalMethodReports
            
            aAllExternalMethodsSuccess = True      
            
            someExternalMethodSpecifications = theInitializationSpecification.get( 'external_methods', [])
            if someExternalMethodSpecifications:
                for aExternalMethodSpecification in someExternalMethodSpecifications:
    
                    aExternalMethodReport = self.fVerifyOrInitialize_ExternalMethod( theInitializationSpecification=aExternalMethodSpecification, theContextualElement=theContextualElement, theAllowInitialization=theAllowInitialization, thePortalRoot=unPortalRoot)
    
                    if not aExternalMethodReport:
                        if theInitializationSpecification.get( 'required', False):
                            aAllExternalMethodsSuccess = False
                    else:
                        if not aExternalMethodReport.get( 'success', False):
                            if aExternalMethodSpecification.get( 'required', False):
                                aAllExternalMethodsSuccess = False
                        
                        someExternalMethodReports.append( aExternalMethodReport)
                        
            anAllExternalMethodReports[ 'success'] = aAllExternalMethodsSuccess      
            

                      
            
            # #######################################################
            """Verify or Initialize, and report, all specified tool singletons.
            
            """
            anAllToolSingletonReports = unInforme.get( 'tool_singletons', None)
            someToolSingletonReports = anAllToolSingletonReports.get( 'tools', None)
            if someToolSingletonReports == None:
                someToolSingletonReports = [ ]
                anAllToolSingletonReports[ 'tools'] = someToolSingletonReports
 
            aAllToolSingletonsSuccess = True  
            
            someToolSingletonSpecifications = theInitializationSpecification.get( 'tool_singletons', [])
            if someToolSingletonSpecifications:
                for aToolSingletonSpecification in someToolSingletonSpecifications:
    
                    aToolSingletonReport = self.fVerifyOrInitialize_ToolSingleton( theInitializationSpecification=aToolSingletonSpecification, theContextualElement=theContextualElement, theAllowInitialization=theAllowInitialization, thePortalRoot=unPortalRoot)
    
                    if not aToolSingletonReport:
                        if theInitializationSpecification.get( 'required', False):
                            aAllToolSingletonsSuccess = False
                    else:
                        if not aToolSingletonReport.get( 'success', False):
                            if aToolSingletonSpecification.get( 'required', False):
                                aAllToolSingletonsSuccess = False
                        
                        someToolSingletonReports.append( aToolSingletonReport)
                        
            anAllToolSingletonReports[ 'success'] = aAllToolSingletonsSuccess   
            
            
            
            unInforme[ 'success'] = anAllExternalMethodReports.get( 'success', False) and anAllToolSingletonReports.get( 'success', False) 
         
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during ModelDDvlPloneTool Verification or Initialization operation fVerifyOrInitialize theAllowInitialization=%s\n' % str( theAllowInitialization) 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            unInforme[ 'success'] = False
            unInforme[ 'condition'] = 'exception'
            unInforme[ 'exception'] = unInformeExcepcion

            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPloneTool').error( unInformeExcepcion)
            
        return unInforme
    
         

 
 
 
    def fCheckInitializationPermissions( self,  theContextualElement=None, ):
       
        if theContextualElement== None:
            return False
        
        aPortalMembershipTool = getToolByName( theContextualElement, 'portal_membership')
        if not aPortalMembershipTool:
            return False
                
        aPermitted = aPortalMembershipTool.checkPermission( cMDDInitializationPermission, theContextualElement)

        return aPermitted
    

    
    
    
 
    def fCheckInitializationPermissions_ExternalMethod( self,  theContextualElement=None, ):
     
        return self.fCheckInitializationPermissions( theContextualElement)
    
    
    
    
                
    
 
    def fCheckInitializationPermissions_ToolSingleton( self,  theContextualElement=None, ):
     
        return self.fCheckInitializationPermissions( theContextualElement)
    
    
    
    
                
                    
                
                
                
         
    def fVerifyOrInitialize_ExternalMethod( self, 
        theInitializationSpecification=None, 
        theContextualElement          =None, 
        theAllowInitialization        =False, 
        thePortalRoot                 =None):
       
        if not theInitializationSpecification:
            return None

        if theContextualElement == None:
            return None
        
        if thePortalRoot == None:
            return None
        
        unInforme = self.fNewVoidInformeVerifyOrInitExternalMethod( )
        
        aExtMethodModule   = theInitializationSpecification.get( 'ext_method_module', '')
        aExtMethodFunction = theInitializationSpecification.get( 'ext_method_function', '')
        aExtMethodId       = theInitializationSpecification.get( 'ext_method_id', '')
        aExtMethodTitle    = theInitializationSpecification.get( 'ext_method_title', '')
        anInstallPath      = theInitializationSpecification.get( 'install_path', '')
        aRequired          = theInitializationSpecification.get( 'required', '')
      
        try:
            unInforme.update( {
                'ext_method_module':         aExtMethodModule,
                'ext_method_function':       aExtMethodFunction,
                'ext_method_id':             aExtMethodId,
                'ext_method_title':          aExtMethodTitle,
                'install_path':              anInstallPath,
                'required':                  aRequired,
            })
            

            if not aExtMethodModule or not aExtMethodFunction or not aExtMethodId or not aExtMethodTitle:
                unInforme[ 'success']   =  False
                unInforme[ 'condition'] = 'MISSING_parameters'
                return unInforme
            
            if theAllowInitialization:
                if not self.fCheckInitializationPermissions_ExternalMethod( theContextualElement):
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'user_can_NOT_initialize ExternalMethod %s' % str( theInitializationSpecification)
                    return unInforme
                

            unInstallContainer = thePortalRoot
            
            if anInstallPath:
                unInstallContainer = self.fInstallContainer_Traversal( thePortalRoot, anInstallPath)
                
                
            if unInstallContainer == None:
                unInforme.update({
                    'success':   False,
                    'condition': 'No_InstallContainer',
                })
                return unInforme
            
            
            unExternalMethod = None
            try:
                unExternalMethod = aq_get( unInstallContainer, aExtMethodId, None, 1)
            except:
                None  
            if unExternalMethod:
                unInforme[ 'success'] = True
                unInforme[ 'status']  = 'exists'
                return unInforme
            
            if not ( theAllowInitialization and cLazyCreateExternalMethods):
                unInforme[ 'success'] = False
                unInforme[ 'status'] = 'missing'         
                return unInforme
            
            unNewExternalMethod = None
            try:
                unNewExternalMethod = ExternalMethod(
                    aExtMethodId,
                    aExtMethodTitle,
                    aExtMethodModule,
                    aExtMethodFunction,
                )
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during ExternalMethod compilation in operation fVerifyOrInitialize_ExternalMethod for %s\n' % str( theInitializationSpecification)
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion
                

                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPloneTool').error( unInformeExcepcion)
                
                return unInforme
            
            if not unNewExternalMethod:
                unInforme[ 'success'] = False
                unInforme[ 'status']  = 'creation_failed'
                return unInforme
                
            unInstallContainer._setObject( aExtMethodId,  unNewExternalMethod)
            unExternalMethod = None
            try:
                unExternalMethod = aq_get( unInstallContainer, aExtMethodId, None, 1)
            except:
                None  
            if not unExternalMethod:
                unInforme[ 'success'] = False
                unInforme[ 'status']  = 'creation_failed'
                return unInforme
                           
            unInforme[ 'success'] = True
            unInforme[ 'status']  = 'created'

            transaction.commit()
            unInforme[ 'committed'] = True
            
            return unInforme

        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during Lazy Initialization operation fVerifyOrInitialize_ExternalMethod %s\n' % str( theInitializationSpecification) 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            unInforme[ 'success'] = False
            unInforme[ 'condition'] = 'exception'
            unInforme[ 'exception'] = unInformeExcepcion
            

            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPloneTool').error( unInformeExcepcion)

            return unInforme

            
        
        
        
        


     
                
         
    def fVerifyOrInitialize_ToolSingleton( self, 
        theInitializationSpecification=None, 
        theContextualElement          =None, 
        theAllowInitialization        =False, 
        thePortalRoot                 =None):
       
        if not theInitializationSpecification:
            return None

        if theContextualElement == None:
            return None
        
        if thePortalRoot == None:
            return None
        
        unInforme = self.fNewVoidInformeVerifyOrInitToolSingleton( )
        
        aSingletonId   = theInitializationSpecification.get( 'singleton_id', '')
        aToolModule   = theInitializationSpecification.get( 'tool_module', '')
        aToolClassName = theInitializationSpecification.get( 'tool_class', '')
        anInstallPath  = theInitializationSpecification.get( 'install_path', '')
        aRequired      = theInitializationSpecification.get( 'required', '')
      
        try:
            unInforme.update( {
                'singleton_id':         aSingletonId,
                'tool_module':         aToolModule,
                'tool_class':           aToolClassName,
                'install_path':         anInstallPath,
                'required':             aRequired,
            })
            

            if not aSingletonId or not aToolModule or not aToolClassName:
                unInforme[ 'success']   =  False
                unInforme[ 'condition'] = 'MISSING_parameters'
                return unInforme
            
            if theAllowInitialization:
                if not self.fCheckInitializationPermissions_ToolSingleton( theContextualElement):
                    unInforme[ 'success']   =  False
                    unInforme[ 'condition'] = 'user_can_NOT_initialize ToolSingleton %s' % str( theInitializationSpecification)
                    return unInforme
                

            unInstallContainer = thePortalRoot
            
            if anInstallPath:
                unInstallContainer = self.fInstallContainer_Traversal( thePortalRoot, anInstallPath)
                
                
            if unInstallContainer == None:
                unInforme.update({
                    'success':   False,
                    'condition': 'No_InstallContainer',
                })
                return unInforme
            
            
            unToolSingleton = None
            try:
                unToolSingleton = aq_get( unInstallContainer, aSingletonId, None, 1)
            except:
                None  
            if unToolSingleton:
                unInforme[ 'success'] = True
                unInforme[ 'status']  = 'exists'
                return unInforme
            
            if not ( theAllowInitialization and cLazyCreateToolSingletons):
                unInforme[ 'success'] = False
                unInforme[ 'status'] = 'missing'         
                return unInforme
            
            
            unToolClass = self.fPackageClass_Traversal( aToolModule, aToolClassName)
            if not unToolClass:
                unInforme[ 'success'] = False
                unInforme[ 'status'] = 'ClassNotFound'         
                return unInforme
                
                
            unNewToolSingleton = None
            try:
                unNewToolSingleton = unToolClass()
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during Singleton instantiation in operation fVerifyOrInitialize_ToolSingleton for %s\n' % str( theInitializationSpecification)
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                unInforme[ 'success'] = False
                unInforme[ 'condition'] = 'exception'
                unInforme[ 'exception'] = unInformeExcepcion
                
                unExecutionRecord and unExecutionRecord.pRecordException( unInformeExcepcion)

                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPloneTool').error( unInformeExcepcion)
                
                return unInforme
            
            if unNewToolSingleton == None:
                unInforme[ 'success'] = False
                unInforme[ 'status']  = 'creation_failed'
                return unInforme
                
            unInstallContainer._setObject( aSingletonId,  unNewToolSingleton)
            unToolSingleton = None
            try:
                unToolSingleton = aq_get( unInstallContainer, aSingletonId, None, 1)
            except:
                None  
            if not unToolSingleton:
                unInforme[ 'success'] = False
                unInforme[ 'status']  = 'creation_failed'
                return unInforme
                           
            unInforme[ 'success'] = True
            unInforme[ 'status']  = 'created'

            transaction.commit()
            unInforme[ 'committed'] = True
            
            return unInforme

        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during Lazy Initialization operation fVerifyOrInitialize_ToolSingleton %s\n' % str( theInitializationSpecification) 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            unInforme[ 'success'] = False
            unInforme[ 'condition'] = 'exception'
            unInforme[ 'exception'] = unInformeExcepcion
            

            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPloneTool').error( unInformeExcepcion)

            return unInforme

            
        


        
        
        
        
        
        
        
        
        
        
            
    

    # ##################################################################
    # Rendering of Lazy creation results 
    #        

    security.declarePrivate( 'pWriteLine')
    def pWriteLine( self, theOutput, theString, theIndentLevel):
        if not theOutput or not theOutput:
            return self
        unIndentLevel = theIndentLevel
        if unIndentLevel < 0:
            unIndentLevel = 0
        theOutput.write( '%s%s\n' % ( cIndent * unIndentLevel, theString))   
        return self
    
    
    
    
    security.declarePrivate( 'fPrettyPrintLazyCreationResult')
    def fPrettyPrintLazyCreationResult( self, theInforme):
        
        if not theInforme:
            return ''
    
        try:
            
            anOutput= StringIO()
            anIndent = 0
            
            if not theInforme:
                self.pWriteLine( anOutput,  'No Report', 0)
                return anOutput.getvalue()
            
 
            self.pWriteLine( anOutput,  '\n\n%s\n\n' % ( ( theInforme.get( 'allow_creation', False) and 'Initializing ModelDDvlPloneTool artefacts, if necessary') or 'Verifying ModelDDvlPloneTool artefacts, if initialization'), 0)     
 
            self.pWriteLine( anOutput,  'ModelDDvlPloneTool title: %s' % theInforme.get( 'title', ''), 0)     
            self.pWriteLine( anOutput,  'ModelDDvlPloneTool path:  %s\n'  % theInforme.get( 'path', ''), 0)  
            
            if theInforme.get( 'success', False):
                self.pWriteLine( anOutput,  'success\n', 0)
            else:
                self.pWriteLine( anOutput,  'failure: %s\n' % theInforme.get( 'condition', ''), 0)
                if theInforme.get( 'exception', ''):
                    self.pWriteLine( anOutput,  'exception:\n%s\n\n' % theInforme.get( 'exception', ''), 0)
                    
            self.pWriteLine( anOutput,  '\n', 0)
                        
                
                       
                
                
            unResultadoModelDDvlPloneTool = theInforme.get( 'ModelDDvlPloneTool', {})        
            if not unResultadoModelDDvlPloneTool:
                self.pWriteLine( anOutput,  'no ModelDDvlPloneTool initialization\n\n', 1)
            else:
                if unResultadoModelDDvlPloneTool.get( 'success', False):
                    self.pWriteLine( anOutput,  'success ModelDDvlPloneTool status: %s' % unResultadoModelDDvlPloneTool.get( 'status', ''), 1)    
                else:
                    self.pWriteLine( anOutput,  'FAILURE ModelDDvlPloneTool status: %s' % unResultadoModelDDvlPloneTool.get( 'status', ''), 1)    
                    if unResultadoModelDDvlPloneTool.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % unResultadoModelDDvlPloneTool.get( 'exception', ''), 1)

                self.pWriteLine( anOutput,  '\n', 1)
                
                
                
                
            unResultadoModelDDvlPloneConfiguration = theInforme.get( 'ModelDDvlPloneConfiguration', {})        
            if not unResultadoModelDDvlPloneConfiguration:
                self.pWriteLine( anOutput,  'no ModelDDvlPloneConfiguration initialization\n\n', 1)
            else:
                if unResultadoModelDDvlPloneConfiguration.get( 'success', False):
                    self.pWriteLine( anOutput,  'success ModelDDvlPloneConfiguration status: %s' % unResultadoModelDDvlPloneConfiguration.get( 'status', ''), 1)    
                else:
                    self.pWriteLine( anOutput,  'FAILURE ModelDDvlPloneConfiguration status: %s' % unResultadoModelDDvlPloneConfiguration.get( 'status', ''), 1)    
                    if unResultadoModelDDvlPloneConfiguration.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % unResultadoModelDDvlPloneConfiguration.get( 'exception', ''), 1)

                self.pWriteLine( anOutput,  '\n', 1)
                                
               
            unResultadoExtMethods = theInforme.get( 'external_methods', {})        
            if not unResultadoExtMethods:
                self.pWriteLine( anOutput,  'NO external_methods initializations\n\n', 1)
            else:
                if unResultadoExtMethods.get( 'success', False):
                    self.pWriteLine( anOutput,  'success external_methods', 1)    
                else:
                    self.pWriteLine( anOutput,  'FAILURE external_methods', 1)    
                    self.pWriteLine( anOutput,  'status % s' % unResultadoExtMethods.get( 'status', ''), 1)  
                    if unResultadoExtMethods.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % unResultadoExtMethods.get( 'exception', ''), 1)
                    
                self.pWriteLine( anOutput,  'external_methods initialization:', 1)
          
                for aExtMethodResult in unResultadoExtMethods.get( 'methods', []):
                    self.pWriteLine( anOutput,  'id: %s     title: %s     module: %s      function: %s' % (   aExtMethodResult.get( 'ext_method_id', ''), aExtMethodResult.get( 'ext_method_title', ''), aExtMethodResult.get( 'ext_method_module', ''), aExtMethodResult.get( 'ext_method_function', ''), ), 2)    
                    self.pWriteLine( anOutput,  'committed: %s status %s ' % (  aExtMethodResult.get( 'committed', False), aExtMethodResult.get( 'status', ''), ), 3)    
                    if aExtMethodResult.get( 'exception', ''):
                        self.pWriteLine( anOutput,  'exception:\n%s\n\n' % aExtMethodResult.get( 'exception', ''), 2)
            
                self.pWriteLine( anOutput,  '\n', 1)
                                                                                             

            
             
            aResult = anOutput.getvalue()
           
            return aResult
        except:
            unaExceptionInfo = sys.exc_info()
            unInformeExcepcion = 'Exception during printing of LazyCreation\n'  
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += ''.join(traceback.format_exception( *unaExceptionInfo))   
            
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPloneTool').error( unInformeExcepcion)
                 
            return 'Error printing lazy creation result\nPartial print and exception traceback follows:\n%s\n%s\n' % ( anOutput.getvalue(), unInformeExcepcion, )
    
     
    
    
    

    
    
            
    
    


##/code-section module-footer



