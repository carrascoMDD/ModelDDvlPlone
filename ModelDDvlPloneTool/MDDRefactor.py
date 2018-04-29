# -*- coding: utf-8 -*-
#
# File: MDDRefactor.py
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



import sys
import traceback
import logging


import time





from AccessControl             import ClassSecurityInfo



from Products.CMFCore          import permissions




from ModelDDvlPloneTool_Refactor_Constants      import *
from ModelDDvlPloneTool_ImportExport_Constants  import *





# ######################################################
# Generic refactoring: abstract classes
# ######################################################
    
    

class MDDRefactor:
    """Manage the refactoring when pasting a source information structure.

    """ 
    
    
    def __init__( self, 
        theModelDDvlPloneTool,
        theModelDDvlPloneTool_Retrieval,
        theModelDDvlPloneTool_Mutators,
        theInitialContextParms =None,
        theSourceInfoMgr       =None, 
        theSourceMetaInfoMgr   =None, 
        theTargetInfoMgr       =None, 
        theTargetMetaInfoMgr   =None, 
        theMapperInfoMgr       =None,
        theMapperMetaInfoMgr   =None, 
        theTraceabilityMgr     =None,
        theTimeSliceMgr        =None,
        theWalker              =None, 
        theAllowMappings       =True,
        theExceptionToRaise    =None,
        theAllowPartialCopies  =True,
        theIgnorePartialLinksForMultiplicityOrDifferentOwner=True,
        ):
        
        unInException = False
        
        try:
            try:
                self.vContext           = { }
                if theInitialContextParms:
                    self.vContext.update( theInitialContextParms)
                    
                self.vResult            = None
                self.vStarted           = False
                self.vTerminated        = False
                self.vSuccess           = False
                self.vErrorReports      = [ ]
                
                self.vModelDDvlPloneTool           = theModelDDvlPloneTool
                self.vModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool_Retrieval
                self.vModelDDvlPloneTool_Mutators  = theModelDDvlPloneTool_Mutators
                    
                self.vSourceInfoMgr     = theSourceInfoMgr
                self.vSourceMetaInfoMgr = theSourceMetaInfoMgr
                self.vTargetInfoMgr     = theTargetInfoMgr
                self.vTargetMetaInfoMgr = theTargetMetaInfoMgr
                self.vMapperInfoMgr     = theMapperInfoMgr
                self.vMapperMetaInfoMgr = theMapperMetaInfoMgr
                self.vTraceabilityMgr   = theTraceabilityMgr
                self.vTimeSliceMgr      = theTimeSliceMgr
                self.vWalker            = theWalker
                
                self.vAllowMappings     = theAllowMappings
            
                self.vExceptionToRaise  = theExceptionToRaise
                
                self.vAllowPartialCopies= theAllowPartialCopies
                self.vIgnorePartialLinksForMultiplicityOrDifferentOwner = theIgnorePartialLinksForMultiplicityOrDifferentOwner
                
                self.vInitialized       = False
                self.vInitFailed        = False
                
                self.vAnyWritesAttempted= False
                self.vAnyWritesDone     = False
                
                self.vNumElementsExpected        = 0
                self.vNumMDDElementsExpected     = 0
                self.vNumPloneElementsExpected   = 0
                self.vNumAttributesExpected      = 0
                self.vNumLinksExpected           = 0
                
                self.vNumElementsPasted        = 0
                self.vNumMDDElementsPasted     = 0
                self.vNumPloneElementsPasted   = 0
                self.vNumAttributesPasted      = 0
                self.vNumLinksPasted           = 0
                
                self.vNumElementsCompleted        = 0
                self.vNumMDDElementsCompleted     = 0
                self.vNumPloneElementsCompleted   = 0
                self.vNumAttributesCompleted      = 0
                self.vNumLinksCompleted           = 0
                
                self.vNumElementsFailed        = 0
                self.vNumMDDElementsFailed     = 0
                self.vNumPloneElementsFailed   = 0
                self.vNumAttributesFailed      = 0
                self.vNumLinksFailed           = 0
                
                self.vNumElementsBypassed      = 0
                self.vNumMDDElementsBypassed   = 0
                self.vNumPloneElementsBypassed = 0
                self.vNumAttributesBypassed    = 0
                self.vNumLinksBypassed         = 0
                
                self.vCreatedElements          = set( )
                self.vChangedElements          = set( )
                
                self.vImpactedObjectUIDs       = [ ]
                
                self.vNumElementsPastedByType = { }
                
                
                """Enforce all role members required.
                
                """        
                if ( self.vSourceInfoMgr == None)   or ( self.vSourceMetaInfoMgr == None)  or \
                   ( self.vTargetInfoMgr == None)   or ( self.vTargetMetaInfoMgr == None)  or \
                   ( self.vMapperInfoMgr == None)   or ( self.vMapperMetaInfoMgr == None)  or \
                   ( self.vTraceabilityMgr == None) or ( self.vTimeSliceMgr == None)  or \
                   ( self.vWalker == None):
                    return self
    
    
                        
                if self.vSourceInfoMgr:
                    if not self.vSourceInfoMgr.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vSourceInfoMgr.vInitialized = True
    
                if self.vSourceMetaInfoMgr and not self.vInitFailed:
                    if not self.vSourceMetaInfoMgr.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vSourceMetaInfoMgr.vInitialized = True
                    
                if self.vTargetInfoMgr and not self.vInitFailed:
                    if not self.vTargetInfoMgr.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vTargetInfoMgr.vInitialized = True
                    
                if self.vTargetMetaInfoMgr and not self.vInitFailed:
                    if not self.vTargetMetaInfoMgr.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vTargetMetaInfoMgr.vInitialized = True
                    
                if self.vMapperInfoMgr and not self.vInitFailed:
                    if not self.vMapperInfoMgr.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vMapperInfoMgr.vInitialized = True
                    
                if self.vMapperMetaInfoMgr and not self.vInitFailed:
                    if not self.vMapperMetaInfoMgr.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vMapperMetaInfoMgr.vInitialized = True
                    
                if self.vTraceabilityMgr and not self.vInitFailed:
                    if not self.vTraceabilityMgr.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vTraceabilityMgr.vInitialized = True
                    
                if self.vTimeSliceMgr and not self.vInitFailed:
                    if not self.vTimeSliceMgr.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vTimeSliceMgr.vInitialized = True
                    
                if self.vWalker and not self.vInitFailed:
                    if not self.vWalker.fInitInRefactor( self):
                        self.vInitFailed = True
                    else:
                        self.vWalker.vInitialized = True
                    
                self.vInitialized       = True
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not self.vInitialized:
                    unaExceptionToRaise = theExceptionToRaise
                    if not unaExceptionToRaise:
                        unaExceptionToRaise = Exception
                        
                    raise unaExceptionToRaise, '%s instance creation and initialization failed' % self.__class__.__name
                 
                
 
                
                

    
    def pAppendErrorReport( self, theErrorReport):
        
        if not theErrorReport:
            return self
        
        if  ( self.vErrorReports == None) or not ( self.vErrorReports.__class__.__name__ == 'list' ):
            self.vErrorReports = [ ]
        
        self.vErrorReports.append( theErrorReport)
        return self
    
    
    
            
    def pSetContextParam( self, theKey, theValue):
        if theKey:
            self.vContext[ theKey] = theValue
            
        return self
    
    
    
    def fGetContextParam( self, theKey, theDefault=None):
        if not theKey:
            return None
        unValue = self.vContext.get( theKey, theDefault)   
        return unValue
    
    
            
    def fRefactor( self,):
        
        if not self.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        unInException = False
        try:
            try:
                if not self.vWalker:
                    return None
            
                self.vStarted = True
                
                aResult = self.vWalker.fRefactor()
    
                self.vResult  = aResult
                
                if self.vResult:
                    self.vSuccess = True
                
                self.vTerminated = True
                
                return self.vSuccess
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not self.vTerminated:
                    raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Refactor_Not_Completed
                
            
    
    
    

class MDDRefactor_Role:
    """
    
    """    
    def __init__( self, ):
        self.vRefactor    = None
        self.vInitialized = False
        
        
    def fInitInRefactor( self, theRefactor):
        if not theRefactor:
            return False
        
        self.vRefactor = theRefactor
        
        return True
    

        
class MDDRefactor_Role_SourceInfoMgr ( MDDRefactor_Role):
    """
    
    """    
        
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    
     
    
class MDDRefactor_Role_SourceMetaInfoMgr ( MDDRefactor_Role):
    """
    
    """    
    
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    
     
        
class MDDRefactor_Role_TargetInfoMgr ( MDDRefactor_Role):
    """
    
    """    

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    

     
    
class MDDRefactor_Role_TargetMetaInfoMgr ( MDDRefactor_Role):
    """
    
    """    

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    
    
    
    
    
    
class MDDRefactor_Role_TimeSliceMgr ( MDDRefactor_Role):
    """
    
    """    

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    
    
        
    
    
    
class MDDRefactor_Role_TraceabilityMgr ( MDDRefactor_Role):
    """
    
    """    

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    
    
    
    
    
            
class MDDRefactor_Role_MapperInfoMgr ( MDDRefactor_Role):
    """
    
    """    

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    
        
    
    
class MDDRefactor_Role_MapperMetaInfoMgr ( MDDRefactor_Role):
    """
    
    """    

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    
    
    
        
class MDDRefactor_Role_Walker ( MDDRefactor_Role):
    """
    
    """    
        
    def fRefactor( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None

        return None
    
    
    
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role.fInitInRefactor( self, theRefactor,):
            return False
        
        return True
    
            
            
    
 
    
    
    
    
    
    
    
    
    
    