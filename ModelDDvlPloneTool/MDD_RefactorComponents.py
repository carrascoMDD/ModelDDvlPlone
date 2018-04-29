# -*- coding: utf-8 -*-
#
# File: MDD_RefactorComponents.py
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



import sys
import traceback
import logging

import transaction

from StringIO  import StringIO
from cStringIO import StringIO   as clsFastStringIO




from AccessControl             import ClassSecurityInfo

from Acquisition               import aq_inner, aq_parent


from OFS.Image                 import Image
from OFS.Image                 import File


from Products.CMFCore          import permissions

from Products.CMFCore.utils    import getToolByName

from Products.Archetypes.utils import shasattr

from xml.dom.minidom           import Node as clsXMLNode


from Products.Relations.config                  import RELATIONS_LIBRARY
from Products.Relations                         import processor            as  gRelationsProcessor


#from ModelDDvlPloneTool                         import ModelDDvlPloneTool
#from ModelDDvlPloneTool_Retrieval               import ModelDDvlPloneTool_Retrieval
#from ModelDDvlPloneTool_Mutators                import ModelDDvlPloneTool_Mutators

from PloneElement_TraversalConfig               import cPloneTypes

from ModelDDvlPloneTool_Refactor_Constants      import *
from ModelDDvlPloneTool_ImportExport_Constants  import *

from PloneElement_TraversalConfig import cExportConfig_PloneElements_MetaTypes

cLogExceptions = True


gcMarker = object()



# ######################################################
# Generic refactoring
# ######################################################
    
    

class MDDRefactor:
    """Manage the refactoring when pasting a source information structure.
        
    Roles:

    Source Info Manager, with uses Source MetaInfo Manager.

    Target Info Manager, with uses Target MetaInfo Manager.
    
    Refactoring Walker, with a Refactoring Stack, with Refactoring Stack Frames.
    
    
    Responsibilities:
    
    To know the target "root".
    
    To known the source "roots".
    
    To know the "container" target instance under which to create new instances from corresponding some source instances.
    Initially is the target "root". Will be switched to new instances aggregated under the target root, recursively.
    
    To know the source instances from which to create new instances under the "container" target instance.
    Initially are the source "roots". Will be switched to new instances aggregated or related to the source root, recursively.
    
    To know the type of new instance to create under the "container" target corresponding to the source instances.
    
    To create under target root a new instance of the specified type, corresponding to the source root.
    
    To know the "current" target instance to populate with values, from a corresponding source instance.
    Will become "container" for a new recursion of the refactoring.
    
    To know the source instance from which to populate target instance values, aggregations and relations.
    
    (recording the above) To know the source instance from which a given target was created.
    
    To populate attribute values in new instances under "current" target , with values (or computations of values) of corresponding attributes of source element .
    
    To know the "current" target instance to populate.
    
    
    
    To know with source aggregation (or expression on aggregations/relations to retrieve and flatten) to traverse to obtain source instances from which to aggregate new target instances under a target instance of a type.
    
    To know the type of the new instance to create under the target, corresponding to the instance aggregated under the source.
    
    To aggregate under new target instances, additional instances of the specified type corresponding to instances aggregated to the source instance.
    
    To know which source relation (or expression on aggregations/relations to retrieve and flatten) to traverse to populate a relation of a target instance, to obtain the source instances whose copied target (or themselves) must be related to the target through the target relation.
    
    To know which source instances have participated in the refactoring.
    
    To know the target instance created from each source instance.
    
    To create relationships between new target instances, corresponding to relationships between source instances.
    
    To create relationships from new target instances to instances not included in the refactoring (neither as source or target), corresponding to relationships from source instances to instances not included in the sources of the refactoring.
    
    
    
    NOTE:
    In the first recursion level, when refactoring the initial source "roots" under the initial target "root",
    we have not traversed any source aggregation/relation, therefore we do not know under which target aggregation to add new instances.
    Fortunately, the underlying technology is Plone, that does not requiere specific aggregations, and only enforces a set of types that can be aggregated under certain type.
    On the other side, we have the traversal specs, so for each source instance, we can search the traversal spec for an aggregation of the target instance type that allows content of the source instance type.
    
    When recursing (therefore we intend to add to known target aggregations) and the source and target aggregations have not the same name, we could search as above:
    
    To populate aggregations: 
    First: target driven: for each target aggregation, create target instances from source instances obtained by traversal of source aggregation of same name (or a configured mapped aggregation name, or a derivation expression)


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
                
                
                """Enforce all role members required.
                
                """        
                if ( self.vSourceInfoMgr == None)   or ( self.vSourceMetaInfoMgr == None)  or \
                   ( self.vTargetInfoMgr == None)   or ( self.vTargetMetaInfoMgr == None)  or \
                   ( self.vMapperInfoMgr == None)   or ( self.vMapperMetaInfoMgr == None)  or \
                   ( self.vTraceabilityMgr == None) or ( self.vWalker == None):
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
    
    
    
    def fGetContextParam( self, theKey):
        if not theKey:
            return None
        unValue = self.vContext.get( theKey, None)   
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
    
            
            
    
 
    
    
    
    
    
    
    
    
    
    
    
# ######################################################
# PASTE refactoring
# ######################################################
    
    

    
            
class MDDRefactor_Paste ( MDDRefactor):
    """Agent to perform a paste refactoring.
    
    """
    def __init__( self, 
        theModelDDvlPloneTool,
        theModelDDvlPloneTool_Retrieval,
        theModelDDvlPloneTool_Mutators,
        theIsMoveOperation,
        theSourceElementResults, 
        theTargetRoot, 
        theTargetRootResult, 
        theTargetAllTypeConfigs, 
        theMappingConfigs,
        theAllowMappings,
        theExceptionToRaise,
        theAllowPartialCopies,
        theIgnorePartialLinksForMultiplicityOrDifferentOwner,
        ):
        

        
        unInitialContextParms = {
            'is_move_operation':        ( theIsMoveOperation and True) or False,
            'source_element_results':   theSourceElementResults,
            'target_root':              theTargetRoot,
            'target_root_result':       theTargetRootResult,
            'target_all_type_configs':  theTargetAllTypeConfigs,
            'mapping_configs':          theMappingConfigs,
        }
        
        MDDRefactor.__init__(
            self,
            theModelDDvlPloneTool,
            theModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators,
            unInitialContextParms,
            MDDRefactor_Paste_SourceInfoMgr_TraversalResult(), 
            MDDRefactor_Paste_SourceMetaInfoMgr_TraversalResult(), 
            MDDRefactor_Paste_TargetInfoMgr_MDDElement(), 
            MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement(), 
            MDDRefactor_Paste_MapperInfoMgr(), 
            MDDRefactor_Paste_MapperMetaInfoMgr_ConvertTypes(), 
            MDDRefactor_Paste_TraceabilityMgr(), 
            MDDRefactor_Paste_Walker(), 
            theAllowMappings,
            theExceptionToRaise,
            theAllowPartialCopies,
            theIgnorePartialLinksForMultiplicityOrDifferentOwner,
        )
    
        
        
        

class MDDRefactor_Paste_SourceInfoMgr_TraversalResult ( MDDRefactor_Role_SourceInfoMgr):
    """
    
    """
    
    
    
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_SourceInfoMgr.fInitInRefactor( self, theRefactor,):
            return False
        
        unosSourceElementResults = self.vRefactor.fGetContextParam( 'source_element_results',) 
        
        if not unosSourceElementResults: 
            return False
        
        for unSourceElementResult in unosSourceElementResults:
            if ( unSourceElementResult.get( 'object', None) == None):
                return False
        return True
    
    
    
    
    def fGetSourceRoots( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        unosSourceElementResults = self.vRefactor.fGetContextParam( 'source_element_results',) 
        return unosSourceElementResults
    
    
    
 
    
    def fIsSourceReadable( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        if not self.fIsSourceOk( theSource):
            return False
    
        aIsReadable = theSource.get( 'read_permission', False)
        return aIsReadable
    
    
    
    def fIsSourceOk( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSourceElementResult or ( theSourceElementResult.get( 'object', None) == None):
            return False

        return True
    
    
    def fGetId( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unaId = theSourceElementResult.get( 'id', '')
        return unaId
    
    
    
    def fGetUID( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unaUID = theSourceElementResult.get( 'UID', '')
        return unaUID
    
    
    
    def fGetPath( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unPath = theSourceElementResult.get( 'path', '')
        return unPath
        
    
    def fGetTitle( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not self.fIsSourceOk( theSourceElementResult):
            return ''

        unTitle = theSourceElementResult.get( 'title', '')
        return unTitle
    
    


       
    
    def fOwnerPath( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unOwnerPath = theSourceElementResult.get( 'owner_path', '')
        return unOwnerPath
    
    
    
    def fRootPath( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unRootPath = theSourceElementResult.get( 'root_path', '')
        return unRootPath
    
    

    def fElementIdentificationForErrorMsg( self, theSource):
        
        if theSource == None:
            return str( None)
        
        unTitle = self.fGetTitle( theSource)
        unaId   = self.fGetId(    theSource)
        unPath  = self.fGetPath(  theSource)
        unaId   = self.fGetUID(   theSource)
        
        unaIdentification = 'Title=%s; id=%s; path=%s UID=%s' % ( repr( unTitle), repr( unaId), repr( unPath), repr( unaUID),)

        return unaIdentification
    

        
    def fElementIdentificationForErrorMsg_Unicode( self, theSource):        
      
        unaIdentification = self.fElementIdentificationForErrorMsg( theSource)
        unaIdentificationUnicode = self.vRefactor.vModelDDvlPloneTool.fAsUnicode( self.vRefactor.fGetContextParam( 'target_root'), unaIdentification)
        
        return unaIdentificationUnicode

        
    
    
        
    def fGetAttributeValue( self, theSourceElementResult, theAttributeName, theAttributeType):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
    
        if ( not theAttributeName) or ( not theAttributeType):
            return None
        
        if theAttributeName.lower() == 'title':
            return self.fGetTitle( theSource)
        elif theAttributeName.lower() == 'id':
            return self.fGetId( theSource)
        elif theAttributeName.lower() == 'path':
            return self.fGetPath( theSource)
        elif theAttributeName.lower() == 'uid':
            return self.fGetUID( theSource)
         
        
        unosValueResults = theSourceElementResult.get( 'values', [])
        if not unosValueResults:
            return None
        
        for unValueResult in unosValueResults:
            unAttrName = unValueResult.get( 'attribute_name', '')
            if unAttrName and ( unAttrName == theAttributeName):
                unAttrValue = unValueResult.get( 'raw_value', None)
                return unAttrValue
            
        return None
            
    
    
    def fGetTraversalValues( self, theSourceElementResult, theTraversalName, theAcceptedSourceTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not self.fIsSourceOk( theSourceElementResult) or ( not theTraversalName):
            return []
        
        unosTraversalResults = theSourceElementResult.get( 'traversals', [])
        if not unosTraversalResults:
            return []
        
        for unTraversalResult in unosTraversalResults:
            unTraversalName = unTraversalResult.get( 'traversal_name', '')
            if unTraversalName == theTraversalName:
                
                unosRetrievedSources = unTraversalResult.get( 'elements', [])
                if not unosRetrievedSources:
                    return []
                
                unosAcceptedSources = [ ]
                
                for unRetrievedSource in unosRetrievedSources:
                    if self.fIsSourceOk( unRetrievedSource):
                        if ( not theAcceptedSourceTypes) or ( self.vRefactor.vSourceMetaInfoMgr.fTypeName( unRetrievedSource) in theAcceptedSourceTypes):
                            unosAcceptedSources.append( unRetrievedSource)
                
                return unosAcceptedSources
            
        return []
    
    
    
    
    
    
    def fDeleteSource( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not self.fIsSourceOk( theSourceElementResult):
            return False
        
        unDeletePermission = theSourceElementResult.get( 'delete_permission', None)
        if not unDeletePermission:
            return False
        
        unSourceObject = theSourceElementResult.get( 'object', None)
        if ( unSourceObject == None):
            return False
        
        unSourceId = theSourceElementResult.get( 'id', '')
        if not unSourceId:
            return False
        
        unContenedorSource = aq_parent( aq_inner( unSourceObject))
        if unContenedorSource == None:
            return False
        
        # self.vRefactor.vModelDDvlPloneTool_Mutators().pSetAudit_Modification( unContenedor)       

        unContenedorSource.manage_delObjects( [ unSourceId, ])
        
        return True
        
    
    
    
        
    
class MDDRefactor_Paste_SourceMetaInfoMgr_TraversalResult ( MDDRefactor_Role_SourceMetaInfoMgr):
    """
    
    """
    

    def fTypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        
        unTypeName = theSource.get( 'meta_type', '')
        return unTypeName
    
    
    def fGetArchetypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        
        unArchetypeName = theSource.get( 'archetype_name', '')
        return unArchetypeName
    
         

    def fPloneTypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( thePloneElement == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        
        unMetaType = ''
        try:
            unMetaType = thePloneElement.meta_type
        except:
            None
            
        return unMetaType
    
    
    def fPloneArchetypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( thePloneElement == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        unArchetype = ''
        try:
            unArchetype = thePloneElement.archetype_name
        except:
            None
            
        return unArchetype
    
    
    

 
        
    
    
    def fTypeConfig( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        
        unTypeConfig = theSource.get( 'type_config', {})
        return unTypeConfig

    
    
    def fAggregationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasAggregationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and not ( unAggregationName in unasAggregationNames):
                unasAggregationNames.append( unAggregationName)
                
        return unasAggregationNames
    
    
    
    
    def fHasAggregationNamed( self, theSource, theAggregationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theAggregationName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_AggregationName
        
         
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theAggregationName):
                return True
                
        return False
    
    
    
    def fHasRelationNamed( self, theSource, theRelationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theRelationName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_RelationName
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theRelationName):
                return True
                
        return False

    
       
    def fHasTraversalNamed( self, theSource, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalName
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theTraversalName):
                return True
            
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theTraversalName):
                return True
                
        return False

    

    def fHasAggregationNamed( self, theSource, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalName
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theTraversalName):
                return True
        return False

    
    

    def fHasRelationNamed( self, theSource, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalName
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theTraversalName):
                return True
                
        return False

        
    
    
    def fRelationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasRelationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if not unRelationName:
                raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Spec_NoRelationName               
            else:
                if not ( unRelationName in unasRelationNames):
                    unasRelationNames.append( unRelationName)
                
        return unasRelationNames
    
    
    
    
    def fAttributeTypeInSource( self, theSource, theAttributeName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theAttributeName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_AttributeName            

        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return ''
       
        unosAttributeConfigs = unTypeConfig.get( 'attrs', [])
        if not unosAttributeConfigs:
            return ''
     
        for unAttributeConfig in unosAttributeConfigs:
            
            # ACV 20091110 Changed key.  'attribute_name' appears in  results, not configs
            # Don't know how this was working without it - indeed, because it was ignored, or fallbacks applied.
            # unAttributeName = unAttributeConfig.get( 'attribute_name', '')
            unAttributeName = unAttributeConfig.get( 'name', '')
            if not unAttributeName:
                raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Spec_NoAttributeName
            else:
                if unAttributeName == theAttributeName:
                    
                    unAttributeType = unAttributeConfig.get( 'type', '')
                    return unAttributeType
            
        return ''
                
                
                

class MDDRefactor_Paste_TargetInfoMgr_MDDElement ( MDDRefactor_Role_TargetInfoMgr):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_TargetInfoMgr.fInitInRefactor( self, theRefactor,):
            return False
        
        unTargetRoot = self.vRefactor.fGetContextParam( 'target_root',) 
        if not unTargetRoot:
            return False
        
        if not unTargetRoot.UID():
            """Shall raise an exception if not a Zope/Plone element or somehow operable object.
            
            """
            return False
 
        unTargetRootResult = self.vRefactor.fGetContextParam( 'target_root_result',) 
        if not unTargetRootResult:
            return False
        
        
        return True
      


    def fElementIdentificationForErrorMsg( self, theTarget):
        
        if theTarget == None:
            return str( None)
        
        unTitle = self.fGetTitle( theTarget)
        unaId   = self.fGetId(    theTarget)
        unPath  = self.fGetPath(  theTarget)
        unaUID   = self.fGetUID(   theTarget)
        
        unaIdentification = 'Title=%s; id=%s; path=%s UID=%s' % ( repr( unTitle), repr( unaId), repr( unPath), repr( unaUID),)

        return unaIdentification
    

        
    def fElementIdentificationForErrorMsg_Unicode( self, theTarget):        
      
        unaIdentification = self.fElementIdentificationForErrorMsg( theTarget)
        unaIdentificationUnicode = self.vRefactor.vModelDDvlPloneTool.fAsUnicode( self.vRefactor.fGetContextParam( 'target_root'), unaIdentification)
        
        return unaIdentificationUnicode

     
    
    def fGetTitle( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unTitle = theTarget.Title() 
        return unTitle
    


     
    def fGetId( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unId = theTarget.getId() 
        return unId
    

   

    def fGetPath( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target

        unPath = '/'.join( theTarget.getPhysicalPath())
        return unPath    
     
    
    
    
    def fGetPloneUID( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unaUID = ''
        try:
            unaUID = thePloneElement.UID()
        except:
            None
            
        return unaUID
    

    
    def fGetTargetRoot( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        unTargetRoot = self.vRefactor.fGetContextParam( 'target_root',) 
        return unTargetRoot
    
    
    def fGetTargetRootResult( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        unTargetRootResult = self.vRefactor.fGetContextParam( 'target_root_result',) 
        return unTargetRootResult
     
    
    
    
    
    def fCreateAggregatedElement( self, theSource, theTarget, theMetaTypeToCreate, ):
        
        unHasBeenCreated = False
        unErrorReason = ''
        unInException = False
        
        try:
            
            try:
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return None
        
                if ( theTarget == None) or not theMetaTypeToCreate or ( theSource == None):
                    unErrorReason = cRefactorStatus_Missing_Parameters
                    return None
                
                unPortalTypeToCreate = self.vRefactor.vTargetMetaInfoMgr.fPlonePortalTypeForMetaType(  theMetaTypeToCreate)
                if not unPortalTypeToCreate:
                    unErrorReason = cRefactorStatus_Error_NoPortalTypeToCreate
                    return None
        
                unSourceId    = self.vRefactor.vSourceInfoMgr.fGetId( theSource)
                if not unSourceId:
                    unErrorReason = cRefactorStatus_Error_NoSourceId
                    return None
                
                unSourceTitle = self.vRefactor.vSourceInfoMgr.fGetTitle( theSource)
                if not unSourceTitle:
                    unErrorReason = cRefactorStatus_Error_NoSourceTitle
                    return None
                
                unosExistingAggregatedElements = theTarget.objectValues()
                
                unosExistingIds    = [ unElement.getId() for unElement in unosExistingAggregatedElements]
                unosExistingTitles = [ unElement.Title() for unElement in unosExistingAggregatedElements]
                
                aPloneToolForNormalizeString = None
                if not ( theMetaTypeToCreate in cExportConfig_PloneElements_MetaTypes):
                    aPloneToolForNormalizeString = getToolByName( theTarget, 'plone_utils', None)
                    if aPloneToolForNormalizeString  and  not shasattr( aPloneToolForNormalizeString, 'normalizeString'):
                        aPloneToolForNormalizeString = None
                else:
                    pass # breakpoint placeholder
                
                unNewTargetId,unNewTargetTitle    = self.fUniqueStringsWithSameCounter( unSourceId, unosExistingIds, unSourceTitle, unosExistingTitles, aPloneToolForNormalizeString)
                if ( not unNewTargetId) or not unNewTargetTitle:
                    unErrorReason = cRefactorStatus_Error_NoNewUniqueIdOrTitle
                    return None
                
                 
                anAttrsDict = {  'title': unNewTargetTitle, }
                
                unCreatedId = None
                try:
                    self.vRefactor.vAnyWritesAttempted = True
                    unCreatedId = theTarget.invokeFactory( unPortalTypeToCreate, unNewTargetId, **anAttrsDict)
                except:
                    return None
                if not unCreatedId:
                    return None
                
                self.vRefactor.vAnyWritesDone = True
                
                unosExistingAggregatedElementsAfterCreation = theTarget.objectValues()
                unCreatedElement = None
                for unElement in unosExistingAggregatedElementsAfterCreation:
                    unId = unElement.getId()
                    if unId == unCreatedId:
                        unCreatedElement = unElement
                        break
                    
                if ( unCreatedElement == None):
                    return None
                
                unCreatedElement.manage_fixupOwnershipAfterAdd()
                
                self.vRefactor.vModelDDvlPloneTool_Mutators.pSetElementPermissions( unCreatedElement)
                
                self.vRefactor.vNumElementsPasted += 1
                self.vRefactor.vNumMDDElementsPasted += 1
                
                unHasBeenCreated = True
                
                return unCreatedElement
            
            except:
                unInException = True
                raise
        
        finally:
            if not unInException:
                if not unHasBeenCreated:
                    
                    self.vRefactor.vNumElementsFailed += 1
                    self.vRefactor.vNumMDDElementsFailed += 1
                    
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fCreateAggregatedElement', 
                        'status': cRefactorStatus_AggregatedElement_NotCreated,
                        'reason': unErrorReason,
                        'params': { 
                            'theTarget': self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTarget), 
                            'theMetaTypeToCreate': unicode( theMetaTypeToCreate),
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
            else:    
                self.vRefactor.vNumElementsFailed += 1
                self.vRefactor.vNumMDDElementsFailed += 1
    
            
        
    def fUniqueAggregatedTitle(self, theTarget, theTitle):
        if ( not theTitle):
            return ''
        
        if theTarget == None:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        
        unosExistingAggregatedElements = theTarget.objectValues()
        
        unosExistingTitles = [ unElement.Title() for unElement in unosExistingAggregatedElements]
        unNewTitle = self.fUniqueStringWithCounter( theTitle, unosExistingTitles)
        
        return unNewTitle
                 
    
    
    
    
    def fUniqueStringsWithSameCounter( self, theInitialStringOne, theExistingStringsOne, theInitialStringTwo, theExistingStringsTwo, thePloneToolForNormalizeString=None):
        if ( not theInitialStringOne) or not theInitialStringTwo:
            return theInitialStringOne, theInitialStringTwo
    
        unInitialStringOne = theInitialStringOne
        if thePloneToolForNormalizeString:
            unInitialStringOne = thePloneToolForNormalizeString.normalizeString( unInitialStringOne)
        
        unInitialStringTwo = theInitialStringTwo
        
        if ( not theExistingStringsOne) and not theExistingStringsTwo:
            return unInitialStringOne, unInitialStringTwo
        
        
        if not ( unInitialStringOne in theExistingStringsOne) and not ( unInitialStringTwo in theExistingStringsTwo):
            return unInitialStringOne, unInitialStringTwo
        
        
        unaStringWONumbersOne = unInitialStringOne
        unaLastChar = unaStringWONumbersOne[-1:]
        while ( unaLastChar >= '0' and unaLastChar <= '9'):
            unaStringWONumbersOne = unaStringWONumbersOne[:-1]
            unaLastChar = unaStringWONumbersOne[-1:]
        while ( unaLastChar in [ '-', '_',]):
            unaStringWONumbersOne = unaStringWONumbersOne[:-1]
            unaLastChar = unaStringWONumbersOne[-1:]        
        
        unaStringWONumbersTwo = unInitialStringTwo
        unaLastChar = unaStringWONumbersTwo[-1:]
        while ( unaLastChar >= '0' and unaLastChar <= '9'):
            unaStringWONumbersTwo = unaStringWONumbersTwo[:-1]
            unaLastChar = unaStringWONumbersTwo[-1:]
        while ( unaLastChar in [ '-', '_',]):
            unaStringWONumbersTwo = unaStringWONumbersTwo[:-1]
            unaLastChar = unaStringWONumbersTwo[-1:]        
        

        unCounter = 1
        
        unNewTargetStringOne = '%s-%d' % ( unaStringWONumbersOne, unCounter, )
        if thePloneToolForNormalizeString:
            unNewTargetStringOne = thePloneToolForNormalizeString.normalizeString( unNewTargetStringOne)
            
        unNewTargetStringTwo = '%s-%d' % ( unaStringWONumbersTwo, unCounter, )
        
        
        while ( unNewTargetStringOne in theExistingStringsOne) or ( unNewTargetStringTwo in theExistingStringsTwo):
            unCounter += 1
            
            unNewTargetStringOne = '%s-%d' % ( unaStringWONumbersOne, unCounter, )
            if thePloneToolForNormalizeString:
                unNewTargetStringOne = thePloneToolForNormalizeString.normalizeString( unNewTargetStringOne)
        
            unNewTargetStringTwo = '%s-%d' % ( unaStringWONumbersTwo, unCounter, )
                  
            
        return unNewTargetStringOne, unNewTargetStringTwo
            
            
    
    
            
    
    def fUniqueStringWithCounter( self, theInitialString, theExistingStrings, thePloneToolForNormalizeString=None):
        if not theInitialString:
            return ''
        
        unInitialString = theInitialString
        
        if thePloneToolForNormalizeString:
            unInitialString = thePloneToolForNormalizeString.normalizeString( unInitialString)
            
        if not theExistingStrings:
            return unInitialString
        
        if not ( unInitialString in theExistingStrings):
            return unInitialString
        
        unaStringWONumbers = unInitialString
        unaLastChar = unaStringWONumbers[-1:]
        
        while ( unaLastChar >= '0' and unaLastChar <= '9'):
            unaStringWONumbers = unaStringWONumbers[:-1]
            unaLastChar = unaStringWONumbers[-1:]
        while ( unaLastChar in [ '-', '_',]):
            unaStringWONumbers = unaStringWONumbers[:-1]
            unaLastChar = unaStringWONumbers[-1:]
        
        unCounter = 1
        unNewTargetString = '%s-%d' % ( unaStringWONumbers, unCounter, )
        if thePloneToolForNormalizeString:
            unNewTargetString = thePloneToolForNormalizeString.normalizeString( unNewTargetString)
        
        while unNewTargetString in theExistingStrings:
            unCounter += 1
            unNewTargetString = '%s-%d' % ( unaStringWONumbers, unCounter, )
            if thePloneToolForNormalizeString:
                unNewTargetString = thePloneToolForNormalizeString.normalizeString( unNewTargetString)
                
        return  unNewTargetString 
    
    
    
    
    
    
    def fPopulateElementAttributes( self, theSource, theTarget, theTargetTypeConfig, theMapping, theMustReindexTarget):
        
        unosAttributesNotProcessed = [ ]
        unErrorReason = ''
        unInException = False
        
        unCompleted = False
        try:
            try:
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                if ( not self.vRefactor.vSourceInfoMgr.fIsSourceOk( theSource )):
                    unErrorReason = cRefactorStatus_Source_Not_OK
                    return False
                

                if  theTarget == None:
                    unErrorReason = cRefactorStatus_Missing_Parameter_Target
                    return False
                
                if not theTargetTypeConfig:
                    unErrorReason = cRefactorStatus_Missing_Parameter_TypeConfig
                    return False
                                
                
                unosTargetAttributesNameTypesAndAttrConfig = self.vRefactor.vTargetMetaInfoMgr.fAttributesNamesTypeAndAttrConfigFromTypeConfig( theTargetTypeConfig)
                if not unosTargetAttributesNameTypesAndAttrConfig:
                    unCompleted = True
                    return True
                
                unNumAttributesToSet = len( unosTargetAttributesNameTypesAndAttrConfig)
                
                for unTargetAttributeNameTypeAndAttrConfig in unosTargetAttributesNameTypesAndAttrConfig:
                    unAttributeProcessed = False
                    
                    unTargetAttributeName   = unTargetAttributeNameTypeAndAttrConfig[ 0]
                    unTargetAttributeType   = unTargetAttributeNameTypeAndAttrConfig[ 1]
                    unTargetAttributeConfig = unTargetAttributeNameTypeAndAttrConfig[ 2]
                    
                    if unTargetAttributeName.lower() in [ 'title', 'id',]:
                        unAttributeProcessed = True
                    
                    elif unTargetAttributeType:
                        
                        unSourceNameAndType = self.vRefactor.vMapperMetaInfoMgr.fSourceAttributeNameAndTypeForTargetNameAndType( theSource, unTargetAttributeNameTypeAndAttrConfig, theMapping)
                        if not unSourceNameAndType:
                            continue
                            
                        unSourceAttributeName = unSourceNameAndType[ 0]
                        unSourceAttributeType = unSourceNameAndType[ 1]
                        
                        if unSourceAttributeName and unSourceAttributeType:
                            
                            unSourceValue = self.vRefactor.vSourceInfoMgr.fGetAttributeValue( theSource, unSourceAttributeName, unSourceAttributeType)
                                
                            unValueToSet = self.vRefactor.vMapperInfoMgr.fMapValue( unSourceValue, unSourceAttributeType, unTargetAttributeType)
                            unHasBeenSet = self.fSetAttributeValue( theTarget, unTargetAttributeName, unValueToSet, unTargetAttributeConfig,)
                            
                            unAttributeProcessed = True

                            if unHasBeenSet:
                                unAnythingChanged = True
                    
                    if not unAttributeProcessed:
                        unosAttributesNotProcessed.append( unTargetAttributeName or 'unknownAttributeName')
                        
                if unAnythingChanged:
                    self.vRefactor.vModelDDvlPloneTool_Mutators.pSetAudit_Modification( theTarget)
                    
                if unAnythingChanged or theMustReindexTarget:
                    theTarget.reindexObject()

                
                unCompleted = True
                
                return True
            
            
            except:
                unInException = True
                raise
    
        finally:
            if not unInException:
                if ( not unCompleted) or unosAttributesNotProcessed:
                    
                    if unosAttributesNotProcessed: 
                        unErrorReason = cRefactorStatus_Not_AllAttributes_Set
                        
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': u'fPopulateElementAttributes', 
                        'status': unicode( cRefactorStatus_Not_AllAttributes_Set),
                        'reason': unicode( unErrorReason),
                        'params': { 
                            'theTarget':         self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTarget), 
                            'numAttrsToSet':     unicode( str( unNumAttributesToSet)),
                            'attrsNotProcessed': unicode( repr( unosAttributesNotProcessed)),
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)


                
                
    
    def fSetAttributeValue( self, theTarget, theAttrName, theValueToSet, theAttributeConfig=None):
        
        unAttributeHasBeenSet = False
        unCanBypassAttribute  = False
        unInException = False
        unErrorReason = ''
        
        try:
            try:
                    
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                if ( theTarget == None) :
                    unErrorReason = cRefactorStatus_Missing_Parameter_Target
                    return False
                
                if not theAttrName:
                    unErrorReason = cRefactorStatus_Missing_Parameters
                    return False
                
                if not theAttributeConfig:
                    unErrorReason = cRefactorStatus_Missing_Parameters
                    return False
    
                
                unValueToSet = theValueToSet
                    
                    
                # #######################################
                """If copying, not moving, then bypass attributes specified no to be copied.
                
                """      
                unIsMoveOperation =  self.vRefactor.fGetContextParam( 'is_move_operation')
                if not unIsMoveOperation:
                    unDoNotCopy = self.vRefactor.vTargetMetaInfoMgr.fGetDoNotCopyFromAttributeConfig( theAttributeConfig)
                    if unDoNotCopy:
                        unCanBypassAttribute = True
                        return False
                
                # #######################################
                """Intercept setting sources counters field for special merge treatment of value to be set with existign value.
                The sources counters field holds a string representation of a dictionary:
                    whose keys are UIDs of source elements from which this one was originated either as a previous version, as original translation, as base element, or as used element,
                    whose values are the change counters in the soruce elements at the time the source element was read.
                
                """       
                unSourcesCountersFieldName = ''
                try:
                    unSourcesCountersFieldName = theTarget.sources_counters_field
                except:
                    None
                if unSourcesCountersFieldName and ( theAttrName == unSourcesCountersFieldName) and unValueToSet:
                    
                    unTargetSchema = None
                    try:
                        unTargetSchema = theTarget.schema
                    except:
                        None
                    if unTargetSchema and unTargetSchema.has_key( unSourcesCountersFieldName):
                        unSourcesCountersField = unTargetSchema[ unSourcesCountersFieldName]
                        if unSourcesCountersField:
    
                            unTargetSourcesCounters = { }
                
                            unTargetAccessor = unSourcesCountersField.getAccessor( theTarget)
                            unTargetSourcesCountersString = unTargetAccessor()
                            if unTargetSourcesCountersString:   
                                try:
                                    unTargetSourcesCounters = eval( unTargetSourcesCountersString)
                                except:
                                    None
                                if not unTargetSourcesCounters:
                                    unTargetSourcesCounters = { }
                                    if not ( unTargetSourcesCounters.__class__.__name__ == 'dict'):
                                        unTargetSourcesCounters = { }
    
                                        
                            unSourceSourcesCounters = { }
                            try:
                                unSourceSourcesCounters = eval( unValueToSet)
                            except:
                                None
                            if not unSourceSourcesCounters:
                                unSourceSourcesCounters = { }
                                if not ( unSourceSourcesCounters.__class__.__name__ == 'dict'):
                                    unSourceSourcesCounters = { }
                                        
                            unNewSourcesCounters = unTargetSourcesCounters.copy()
                            unNewSourcesCounters.update( unSourceSourcesCounters)
                            
                            unValueToSet = repr( unNewSourcesCounters)
                
                
                
                unAttrMutatorAccessorName = theAttributeConfig.get( 'mutator_accessor', '')     
                unAttributeName    = theAttributeConfig.get( 'attribute', '')     
                unAttrMutatorName  = theAttributeConfig.get( 'mutator', '')  
             
                
                unObject = theTarget
                
                # #######################################
                """Handle special attributes on standard Plone elements.
                
                """      
                if ( theTarget.__class__.__name__ == 'ATDocument') and ( theAttrName == 'content_type'):
                    unSchema = theTarget.schema
                    if not unSchema.has_key( 'text'):
                        unErrorReason = cRefactorStatus_Field_Not_in_Schema
                        return False
                    
                    unField  = unSchema[ 'text']
                    if not unField:
                        unErrorReason = cRefactorStatus_Field_Not_in_Schema
                        return False
                    
                    self.vRefactor.vAnyWritesAttempted = True
                    
                    unSet = False
                    try:
                        unField.setContentType( theTarget, unValueToSet)
                        unSet = True
                    except:
                        None
                    if not unSet:
                        unErrorReason = cRefactorStatus_Attribute_Not_Set
                        return False
                        
                        
                    self.vRefactor.vAnyWritesDone = True
                    unAttributeHasBeenSet = True
                    self.vRefactor.vNumAttributesPasted += 1
                    
                    return True
                
                
                
                # #######################################
                """Handle setting attributes that specify explicit accessor and mutators.
                unAttrMutatorAccessorName allows to set the new value in an object derived from theTarget
                unAttributeName allows to set an object attribute (with setattribute or setattr), not a schema field
                unAttrMutatorName allows to set the value by invoking a mutator rather than setting an attribute
                
                """      
                if unAttrMutatorAccessorName or unAttributeName or unAttrMutatorName:
                    
                    if unAttrMutatorAccessorName:
                        
                        unAccessor = None
                        try:
                            unAccessor = unObject[ unAttrMutatorAccessorName]    
                        except:
                            None
                        if not unAccessor:
                            unErrorReason = cRefactorStatus_AttrMutatorAccessor_NotFound
                            return False
                        
                        unRawValue = gcMarker
                        try:
                            unRawValue = unAccessor()                            
                        except:
                            None
                        if ( unRawValue == gcMarker):
                            unErrorReason = cRefactorStatus_AttrMutatorAccessor_Failed
                            return False
                        
                        unObject = unRawValue
                             
                            
                    if unAttributeName:
                        if ( unObject == None):
                            return False
    
                        self.vRefactor.vAnyWritesAttempted = True
                        
                        unSet = False
                        try:
                            unObject.__setattribute__( unAttributeName, unValueToSet)
                            unSet = True
                        except:
                            None
                            
                        if not unSet:
                            try:
                                unObject.__setattr__( unAttributeName, unValueToSet)
                                unSet = True
                            except:
                                None
                            
                        if not unSet:
                            unErrorReason = cRefactorStatus_AttrMutatorAccessor_Failed
                            return False
                            
                        self.vRefactor.vAnyWritesDone = True
                        self.vRefactor.vNumAttributesPasted += 1
                        unAttributeHasBeenSet = True
    
                        return True 
                    
                     
                    if unAttrMutatorName:
                        if ( unObject == None):
                            unErrorReason = cRefactorStatus_NoObjectFor_AttrMutator
                            return False
                        
                        unMutator = unObject[ unAttrMutatorName]    
                        if not unMutator:
                            unErrorReason = cRefactorStatus_AttrMutator_NotFound
                            return False
    
                        self.vRefactor.vAnyWritesAttempted = True
                        
                        unSet = False
                        try:
                            unMutator( unValueToSet)
                            unSet = True
                        except:
                            None
                            
                        if not unSet:
                            unErrorReason = cRefactorStatus_Attribute_Not_Set
                            return False
     
                        self.vRefactor.vAnyWritesDone = True
                        self.vRefactor.vNumAttributesPasted += 1
                        unAttributeHasBeenSet = True
    
                        return True
                        
                else:
                    # #######################################
                    """Handle setting attributes as schema fields
                    
                    """      
                    unSchema = None
                    try:
                        unSchema = theTarget.schema
                    except:
                        None
                    if not unSchema:
                        return False
                    
                    if not unSchema.has_key( theAttrName):
                        return False
                    
                    unField  = unSchema[ theAttrName]
                    if not unField:
                        return False
                    
                    unMutator = unField.getMutator( theTarget)
                    if not unMutator:
                        return False
                    
    
                    self.vRefactor.vAnyWritesAttempted = True
                    
                    unMutator( unValueToSet)
    
                    self.vRefactor.vAnyWritesDone = True
                    self.vRefactor.vNumAttributesPasted += 1
                    unAttributeHasBeenSet = True
                
                    return True

            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not unAttributeHasBeenSet and not unCanBypassAttribute:  
                    self.vRefactor.vNumAttributesFailed += 1
                    
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fSetAttributeValue', 
                        'status': cRefactorStatus_Attribute_Not_Set,
                        'reason': unErrorReason,
                        'params': { 
                            'theTarget': self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTarget), 
                            'theAttrName': unicode( theAttrName),
                            'theValueToSet': self.vRefactor.vModelDDvlPloneTool.fAsUnicode( self.vRefactor.fGetContextParam( 'target_root'), repr( theValueToSet),)
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
            else:
                self.vRefactor.vNumAttributesFailed += 1



    
    
    def fGetUID( self, theElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theElement == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Element
        
        if theElement.meta_type in cPloneSiteMetaTypes:
            return cFakeUIDForPloneSite
        
        unaUID = ''
        try:
            unaUID = theElement.UID()
        except:
            None
            
        return unaUID
    
      
    
    def fIsTargetResultOk( self, theTargetElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTargetElementResult or ( theTargetElementResult.get( 'object', None) == None):
            return False
        return True
    
    
       
    def fGetPermissionFromElementResult( self, theElementResult, thePermission):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsTargetResultOk( theElementResult):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_TargetResult_Not_OK
    
        if not ( thePermission in [ 'read_permission', 'traverse_permission', 'write_permission', 'add_permission', 'add_collection_permission', 'delete_permission', ]):
            return False
        
        aPermissionPermitted = theElementResult.get( thePermission, False)
        return aPermissionPermitted
    
    
    
    def fGetPermissionFromTraversalResult( self, theTraversalResult, thePermission):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not theTraversalResult:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalResult
    
        if not ( thePermission in [ 'read_permission', 'write_permission', ]):
            return False
        
        aPermissionPermitted = theTraversalResult.get( thePermission, False)
        return aPermissionPermitted
        
    
    
    def fTraversalResultNamed( self, theElementResult, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsTargetResultOk( theElementResult):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_TargetResult_Not_OK
    
        if not theTraversalName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalName
        
        unosTraversalResults = theElementResult.get( 'traversals', [])
        if not unosTraversalResults:
            return {}
        
        for unTraversalResult in unosTraversalResults:
            unTraversalName = unTraversalResult.get( 'traversal_name', '')
            if unTraversalName == theTraversalName:
                return unTraversalResult

            
        return {}
    
    
    
    
    
    def fRootPath( self, theElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if theElement == None:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Element
        
        unRaiz = theElement.getRaiz()
        if unRaiz == None:
            return ''
        
        unRootPath = ''    
        try:
            unRootPath         = unRaiz.fPhysicalPathString()
        except:
            None
        if not unRootPath:
            try:
                unRootPath     = '/'.join( unRaiz.getPhysicalPath())
            except:
                None
        return unRootPath
      
    
        
    
    def fOwnerPath( self, theElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theElement == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Element
    
        unOwner = theElement.getContenedor()
        if not unOwner:
            return ''
        
        unOwnerEsColeccion = False
        try:
            unOwnerEsColeccion =  unOwner.getEsColeccion()
        except:
            None
        if unOwnerEsColeccion:    
            unOwner = unOwner.getContenedor()
            
        unOwnerPath = ''    
        try:
            unOwnerPath         = unOwner.fPhysicalPathString()
        except:
            None
        if not unOwnerPath:
            try:
                unOwnerPath     = '/'.join( unOwner.getPhysicalPath())
            except:
                None
        return unOwnerPath
    
    
    
    
    
    def fPhysicalPathString( self, theElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theElement == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Element
    
        unPathString = ''
        try:
            unPathString = theElement.fPhysicalPathString()
        except:
            None
        return unPathString
    
    
    

    
    def fLink_Relation( self, theTargetFrom, theTargetsTo, theFieldName):
        """
        
        """
        unMethodName = 'fLink_Relation'
        unCompleted     = False
        unHasBeenLinked = False
        unInException   = False
        unLinkBypassed  = False
        unErrorReason   = ''
        
        try:
            try:
                    
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                if ( theTargetFrom == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_TargetFrom
                    return False
                
                if ( theTargetsTo == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_TargetTo
                    return False

                if not theFieldName:
                    unErrorReason = cRefactorStatus_Missing_Parameter_AttributeName
                    return False
                
                unFromSchema = theTargetFrom.schema
                if not unFromSchema.has_key( theFieldName):
                    unErrorReason = cRefactorStatus_Field_Not_in_Schema
                    return False
                 
                unFromField             = unFromSchema[ theFieldName]
                unFromFieldClassName    = unFromField.__class__.__name__
                
                if not ( unFromFieldClassName in [ 'RelationField', 'ReferenceField']):
                    unErrorReason = cRefactorStatus_Field_NotRelationOrReference
                    return False
                    
                    
                if unFromField.__class__.__name__ == 'RelationField':
                    
                    
                    unIsMultivaluedFrom = False
                    try:
                        unIsMultivaluedFrom = unFromField.multiValued
                    except:
                        None
                                                                            
                    if not unIsMultivaluedFrom:
                        unFromAccessor = unFromField.getAccessor( theTargetFrom)
                        if not unFromAccessor:
                            unErrorReason = cRefactorStatus_Field_No_Accessor
                            return False
                        
                        unCurrentlyLinkedFrom = unFromAccessor()
                        if unCurrentlyLinkedFrom:
                            if theTargetsTo and not ( unCurrentlyLinkedFrom == theTargetsTo[ 0]):
                                unErrorReason = cRefactorStatus_Relation_AlreadyLinked_NoMultivalued
                                if not ( self.vRefactor.vAllowPartialCopies or self.vRefactor.vIgnorePartialLinksForMultiplicityOrDifferentOwner):
                                    return False
                                else:
                                    anErrorReport = { 
                                        'theclass': self.__class__.__name__, 
                                        'method': unMethodName, 
                                        'status': unicode( unErrorReason),
                                    }
                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                    
                                    unCompleted = True
                                    unLinkBypassed = True
                                    self.vRefactor.vNumLinksBypassed += 1
                                    return True
                                     
                    else:
                        unMultiplicityHigherFrom = -1                                            
                        try:
                            unMultiplicityHigherFrom = unFromField.multiplicity_higher
                        except:
                            None     
                        if unMultiplicityHigherFrom > 0:
                            
                            unFromAccessor = unFromField.getAccessor( theTargetFrom)
                            if not unFromAccessor:
                                unErrorReason = cRefactorStatus_Field_No_Accessor
                                return False
                            
                            unCurrentlyLinkedFrom = unFromAccessor()
                            
                            if len( unCurrentlyLinkedFrom) > unMultiplicityHigherFrom:
                                unErrorReason = cRefactorStatus_Relation_MaxmultiplicityReached
                                if not ( self.vRefactor.vAllowPartialCopies or self.vRefactor.vIgnorePartialLinksForMultiplicityOrDifferentOwner):
                                    return False
                                else:
                                    anErrorReport = { 
                                        'theclass': self.__class__.__name__, 
                                        'method': unMethodName, 
                                        'status': unicode( unErrorReason),
                                    }
                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                    
                                    unCompleted = True
                                    unLinkBypassed = True
                                    
                                    return False
                    
                            
                    unRelationName = ''
                    try:
                        unRelationName = unFromField.relationship
                    except:
                        None
                    if not unRelationName:   
                        unErrorReason = cRefactorStatus_Field_NoRelationName
                        return False
                    
                    
                    unInverseRelationFieldName = ''
                    try:
                        unInverseRelationFieldName = unFromField.inverse_relation_field_name
                    except:
                        None
                    if not unInverseRelationFieldName:   
                        unErrorReason = cRefactorStatus_Field_NoInverseRelationFieldName
                        return False
                            
                    
                    aRelationsLibrary = getToolByName( theTargetFrom, RELATIONS_LIBRARY)        
                    if not aRelationsLibrary:
                        unErrorReason = cRefactorStatus_NoRelationsLibrary
                        return False
                        
                    unTargetUID = self.fGetUID( theTargetFrom)
                    if not unTargetUID:
                        unErrorReason = cRefactorStatus_NoTargetUID
                        return False
                
                    unAnyNotLinked = False
                    for unTargetToBeRelated in theTargetsTo:
                        
                        unTargetToBeRelatedUID = self.vRefactor.vTargetInfoMgr.fGetUID( unTargetToBeRelated)
                        if not unTargetToBeRelatedUID:
                            unAnyNotLinked = True
                        else:
                            
                            unToSchema = unTargetToBeRelated.schema
                            if not unToSchema.has_key( unInverseRelationFieldName):
                                unErrorReason = cRefactorStatus_Field_Not_in_Schema
                                return False
                             
                            unToField             = unToSchema[ unInverseRelationFieldName]
                            unToFieldClassName    = unToField.__class__.__name__
                            
                            if not ( unToFieldClassName =='RelationField'):
                                unErrorReason = cRefactorStatus_Field_InverseNotRelation
                                return False
                                 
                            
                            unIsMultivaluedTo = False
                            try:
                                unIsMultivaluedTo = unToField.multiValued
                            except:
                                None
                                                                                    
                            if not unIsMultivaluedTo:
                                unToAccessor = unToField.getAccessor( unTargetToBeRelated)
                                if not unToAccessor:
                                    unErrorReason = cRefactorStatus_Field_No_Accessor
                                    return False
                                
                                unCurrentlyLinkedTo = unToAccessor()
                                if unCurrentlyLinkedTo:
                                    if not ( unCurrentlyLinkedTo == theTargetFrom):
                                        unErrorReason = cRefactorStatus_Relation_AlreadyLinked_NoMultivalued
                                        return False
                            else:
                                unMultiplicityHigherTo = -1                                            
                                try:
                                    unMultiplicityHigherTo = unToField.multiplicity_higher
                                except:
                                    None     
                                if unMultiplicityHigherTo > 0:
                                    
                                    unToAccessor = unToField.getAccessor( unTargetToBeRelated)
                                    if not unToAccessor:
                                        unErrorReason = cRefactorStatus_Field_No_Accessor
                                        return False
                                    
                                    unCurrentlyLinkedTo = unToAccessor()
                                    if len( unCurrentlyLinkedTo) > unMultiplicityHigherTo:
                                        unErrorReason = cRefactorStatus_Relation_MaxmultiplicityReached
                                        return False
                            
                            gRelationsProcessor.process( aRelationsLibrary, connect=[( unTargetUID, unTargetToBeRelatedUID, unRelationName ), ], disconnect=[])
                            self.vRefactor.vNumLinksPasted += 1
                            unHasBeenLinked = True
                    
                    if unAnyNotLinked:
                        unErrorReason = cRefactorStatus_NotAllLinked
                        return False
                    
                    unCompleted = True
                    return True
                
                elif unField.__class__.__name__ == 'ReferenceField':
                    
                    unMutator = unField.getMutator( theTargetFrom)
                    if not unMutator:
                        unErrorReason = cRefactorStatus_Field_No_Mutator
                        return False
                        
                    unIsMultivalued = False
                    try:
                        unIsMultivalued = unField.multiValued
                    except:
                        None
                        
                    if unIsMultivalued:      
                        unMutator( theTargetsTo)
                        unHasBeenLinked = True
                            
                    else:
                        unTargetTo = theTargetsTo[ 0]
                        unMutator( unTargetTo)
                        unHasBeenLinked = True
                        
                
                    self.vRefactor.vNumLinksPasted += 1
                    unCompleted = True
                    return True
                    
                unCompleted = True
                return True

            except:
                unInException = True
                raise
        
        finally:
            if not unInException:
                if (not unCompleted) or ( ( not unHasBeenLinked) and not unLinkBypassed):
                    self.vRefactor.vNumLinksFailed += 1
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fLinkRelation', 
                        'status': cRefactorStatus_Element_NotLinked,
                        'reason': unErrorReason,
                        'params': { 
                            'theTargetFrom': self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTargetFrom), 
                            'theFieldName': unicode( theFieldName),
                            'theTargetsTo': u';'.join( [ self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( unTarget) for unTarget in ( theTargetsTo or [])]),
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
            else:
                self.vRefactor.vNumLinksFailed += 1
                
 
    
    
    
    def fCollectionToMergeWith( self, theTargetElement, theTypeToCreate, theSourceResult):
        """Return First Sub Element of Type, With Title Or Default Title. Also return whether to Override its Title, and to Override its Id
        
        """
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        unSourceId            = self.vRefactor.vSourceInfoMgr.fGetId( theSourceResult)
        unSourceTitle         = self.vRefactor.vSourceInfoMgr.fGetTitle( theSourceResult)
        unSourceArchetypeName = self.vRefactor.vSourceMetaInfoMgr.fGetArchetypeName( theSourceResult)
        
        unSourceHasDefaultTitle = unSourceTitle == unSourceArchetypeName
        
        someTargetSubElements =  theTargetElement.objectValues( theTypeToCreate)
        if not someTargetSubElements:
            return ( None, False, False)
        
        unosSubElementsMatching = [ ]
        
        for unTargetSubElement in someTargetSubElements:
            
            unTargetSubElementHasChildren = len( unTargetSubElement.objectValues()) > 0
            
            unTargetSubElementId    = unTargetSubElement.getId()
            unTargetSubElementTitle = unTargetSubElement.Title()
            
            if unTargetSubElementId == unSourceId:
                return ( unTargetSubElement, not ( unTargetSubElementTitle == unSourceTitle), False)

            if unTargetSubElementTitle == unSourceTitle:
                return ( unTargetSubElement, False, not unTargetSubElementHasChildren)
                
            unTargetSubElementArchetypeName = ''
            try:
                unTargetSubElementArchetypeName = unTargetSubElement.archetype_name
            except:
                None
            if unTargetSubElementTitle == unTargetSubElementArchetypeName:
                return ( unTargetSubElement, True, not unTargetSubElementHasChildren)
                 
        if unSourceHasDefaultTitle:
            return ( someTargetSubElements[ 0], False, not ( len( someTargetSubElements[ 0].objectValues()) > 0)) 
                
        return ( None, False, False,)
    
    
    
    
class MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement ( MDDRefactor_Role_TargetMetaInfoMgr):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_TargetMetaInfoMgr.fInitInRefactor( self, theRefactor,):
            return False
        
        unTargetAllTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',) 
        if not unTargetAllTypeConfigs:
            return False
        
        return True
     

    
    def fTypeName( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
    
        unTypeName = ''
        try:
            unTypeName = theTarget.meta_type
        except:
            None
        
        return unTypeName
    

    
    
    def fPlonePortalTypeForMetaType(self, theMetaType):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theMetaType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_MetaType
        
        aPlonePortalTypeSpec = cPloneTypes.get( theMetaType, {})
        if not aPlonePortalTypeSpec:
            return theMetaType
        
        unPortalType = aPlonePortalTypeSpec.get( 'portal_type', '')
        
        return unPortalType
        
    
    def fTypeConfig( self, theTarget, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTarget:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target

        unTargetType = self.fTypeName( theTarget)
        if not unTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoTarget_Type
        
        unTypeConfig = self.fTypeConfigForType( unTargetType, theTypeConfigName)
        return unTypeConfig
    
    
        
    
    def fTypeConfigForType( self, theTargetType, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TargetType

        unTargetAllTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',) 
        if not unTargetAllTypeConfigs:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_ContextParam_target_all_type_configs
        
        unasTypeConfigs = unTargetAllTypeConfigs.get( theTargetType, {})
        if not unasTypeConfigs:
            return {}
        
        unTypeConfigName = theTypeConfigName
        if ( not unTypeConfigName) or ( unTypeConfigName == 'Default'):
            unTypeConfigName = sorted( unasTypeConfigs.keys())[ 0]
        
        unaTypeConfig = unasTypeConfigs.get( unTypeConfigName, {})
        if not unaTypeConfig:
            return {}
        
        return unaTypeConfig
    
    
    
    
    
    def fAggregationConfigsWithType( self, theTargetType, theSourceType):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TargetType

        if not theSourceType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_SourceType

        unaTypeConfig = self.fTypeConfigForType( theTargetType)
        if not unaTypeConfig:
            return []
        
        unasTraversalConfigs = unaTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        someAggregationConfigs = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName:
                unosSubItems = unaTraversalConfig.get( 'subitems', [])
                for unSubItem in unosSubItems:
                    unosTypes = unSubItem.get( 'portal_types', [])
                    if theSourceType in unosTypes:
                        someAggregationConfigs.append( unaTraversalConfig)
                
        return someAggregationConfigs        
        
        
        
    
    def fTypeConfigForTypeFromAggregationTraversalConfig( self, theTargetType, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TargetType

        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig

        if not self.fIsTraversalConfigAggregation( theTraversalConfig):
            return {}
        
        unosSubItemsTypeConfigs = theTraversalConfig.get( 'subitems', [])
        for unSubItemTypeConfig in unosSubItemsTypeConfigs:
            unosTypes = unSubItemTypeConfig.get( 'portal_types', [])
            if theTargetType in unosTypes:
                
                unReuseTypeConfigNamed = unSubItemTypeConfig.get( 'reuse_config', '')
                if not unReuseTypeConfigNamed:
                    return unSubItemTypeConfig
                
                unTypeConfig = self.fTypeConfigForType( theTargetType, unReuseTypeConfigNamed)
                return unTypeConfig
                
        return {}
        
            
    
    
     
    def fAggregatedTypes( self, theTargetType):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TargetType

        unaTypeConfig = self.fTypeConfigForType( theTargetType)
        
        unasTraversalConfigs = unaTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unosAggregatedTypes = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName:
                unosSubItems = unaTraversalConfig.get( 'subitems', [])
                for unSubItem in unosSubItems:
                    unosTypes = unSubItem.get( 'portal_types', [])
                    for unType in unosTypes:
                        if not ( unType in unosAggregatedTypes):
                            unosAggregatedTypes.append( unType)
                
        return unosAggregatedTypes
    
    
    
    
    def fIsTraversalConfigAggregation( self, theTraversalConfig):
        
        return ( self.fAggregationNameFromTraversalConfig( theTraversalConfig) and True) or False
     
    
    
    
    def fGetAggregationConfigContainsCollections( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig
 
        if not self.fIsTraversalConfigAggregation( theTraversalConfig):
            return False
        
        unContainsCollection = theTraversalConfig.get( 'contains_collections', False) == True
        return unContainsCollection
        
    
    
    
    

    def fAggregationNameFromTraversalConfig( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig
        
        unAggregationName = theTraversalConfig.get( 'aggregation_name', '')
        return unAggregationName
        
     
    def fAggregatedTypesFromTraversalConfig( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig
        
        unAggregationName = theTraversalConfig.get( 'aggregation_name', '')
        if not unAggregationName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Spec_NoAggregationName

        unosAggregatedTypes = [ ]
        unosSubItems = theTraversalConfig.get( 'subitems', [])
        for unSubItem in unosSubItems:
            unosTypes = unSubItem.get( 'portal_types', [])
            for unType in unosTypes:
                if not ( unType in unosAggregatedTypes):
                    unosAggregatedTypes.append( unType)

        return unosAggregatedTypes
    
    
    
    def fRelatedTypesFromTraversalConfig( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig
        
        unRelationName = theTraversalConfig.get( 'relation_name', '')
        if not unRelationName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Spec_NoRelationName

        unosRelatedTypes = [ ]
        unosRelatedItems = theTraversalConfig.get( 'related_types', [])
        for unRelatedItem in unosRelatedItems:
            unosTypes = unRelatedItem.get( 'portal_types', [])
            for unType in unosTypes:
                if not ( unType in unosRelatedTypes):
                    unosRelatedTypes.append( unType)

        return unosRelatedTypes
        
    

    def fCandidatesScopeFromRelationTraversalConfig( self, theTraversalConfig):
        """"Shall return 'owner' or nothing
        
        """
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig
        
        unRelationName = theTraversalConfig.get( 'relation_name', '')
        if not unRelationName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Spec_NoRelationName
        
        unCandidatesScope = theTraversalConfig.get( 'candidates_scope','').lower()
        return unCandidatesScope

    
    
    
    def fAggregationTraversalConfigsFromTypeConfig( self, theTypeConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTypeConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TypeConfig
        
        unasTraversalConfigs = theTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasAggregationsTraversalConfigs = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName:
                unosSubItems = unaTraversalConfig.get( 'subitems', [])
                for unSubItem in unosSubItems:
                    unosTypes = unSubItem.get( 'portal_types', [])
                    if unosTypes:  
                        unasAggregationsTraversalConfigs.append( unaTraversalConfig)
                        break
                
        return unasAggregationsTraversalConfigs
    
    
    
    
    def fRelationNameFromTraversalConfig( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig
        
        unRelationName = theTraversalConfig.get( 'relation_name', '')
        if not unRelationName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Spec_NoRelationName
         
        return unRelationName
        
    
    
    
    
    def fGetDoNotCopyFromAttributeConfig( self, theAttributeConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theAttributeConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_AttributeConfig
        
        unDoNotCopy = theAttributeConfig.get( 'do_not_copy', False)
        return unDoNotCopy
    
    
    
    
    def fGetDoNotCopyFromTraversalConfig( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig
        
        unDoNotCopy = theTraversalConfig.get( 'do_not_copy', False)
        return unDoNotCopy
        
    
    def fGetIsAcrossRootsFromTraversalConfig( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TraversalConfig
        
        unIsAcrossRoots = theTraversalConfig.get( 'is_across_roots', False)
        return unIsAcrossRoots
        
        
    
     
    def fRelationTraversalConfigsFromTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTarget:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unTypeConfig = self.fTypeConfig( theTarget)
        if not unTypeConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_No_TypeConfig
        
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasRelationsTraversalConfigs = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName:
                unosRelatedConfigs = unaTraversalConfig.get( 'related_types', [])
                for unRelatedConfig in unosRelatedConfigs:
                    unosTypes = unRelatedConfig.get( 'portal_types', [])
                    if unosTypes:  
                        unasRelationsTraversalConfigs.append( unaTraversalConfig)
                        break
                
        return unasRelationsTraversalConfigs
    
    

    
    

        
    
    def fAttributesNamesTypeAndAttrConfigFromTypeConfig( self, theTypeConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theTypeConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TypeConfig

        unosAttrConfigs = theTypeConfig.get( 'attrs', [])
        if not unosAttrConfigs:
            return []
        
        unosAttributeNamesAndTypes = [ ]
        
        for unAttrConfig in unosAttrConfigs:
            unAttrName = unAttrConfig.get( 'name', '')
            if not unAttrName:
                raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Spec_NoAttributeName
            else:
                unAttrType = unAttrConfig.get( 'type', '')
                if unAttrType:
                    unosAttributeNamesAndTypes.append( [ unAttrName, unAttrType, unAttrConfig,])
                    
                
        return unosAttributeNamesAndTypes
        

    

    
    
class MDDRefactor_Paste_TraceabilityMgr ( MDDRefactor_Role_TraceabilityMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_TraceabilityMgr.__init__( self)
        

        
        
    
    def fEstablishTraceabilityLinks( self, theSource, theTarget):
        return True
    
    
            

            
    
class MDDRefactor_Paste_MapperInfoMgr ( MDDRefactor_Role_MapperInfoMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_MapperInfoMgr.__init__( self)
        
        self.vSourcesForTargetsMap = { }
        self.vTargetsForSourcesMap = { }
        self.vMappingsForTargets   = { }
        
        

        
    
    def fMapValue( self, theSourceValue, theSourceType, theTargetType):
        
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSourceType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_SourceType
        
        if not theTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TargetType

        if theTargetType.lower() == theSourceType.lower():
            return theSourceValue
        
        return theSourceValue
    
    
    
    
    
    def fRegisterSourceToTargetCorrespondence( self, theSource, theTarget, theMapping):

        unCompleted   = False
        unInException = False
        unErrorReason = ''
        
        try:
            try:
        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                if ( theSource == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Source
                    return False
                
                if ( theTarget == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Target
                    return False
        
                unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
                if not unSourceUID:
                    unErrorReason = cRefactorStatus_NoSourceUID
                    return False
                
                unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
                if not unTargetUID:
                    unErrorReason = cRefactorStatus_NoTargetUID
                    return False
                
                unosTargetForSource = self.vTargetsForSourcesMap.get( unSourceUID, None)
                if unosTargetForSource == None:
                    unosTargetForSource = [ set(), [], ]
                    self.vTargetsForSourcesMap[ unSourceUID] = unosTargetForSource
                    
                unosTargetUIDs = unosTargetForSource[ 0]
                if not ( unTargetUID in unosTargetUIDs):
                    unosTargetUIDs.add( unTargetUID)
                    unosTargetForSource[ 1].append( theTarget)
                
                unosSourceForTarget = self.vSourcesForTargetsMap.get( unTargetUID, None)
                if unosSourceForTarget == None:
                    unosSourceForTarget = [ set(), [], ]
                    self.vSourcesForTargetsMap[ unTargetUID] = unosSourceForTarget
                    
                unosSourceUIDs = unosSourceForTarget[ 0]
                if not ( unSourceUID in unosSourceUIDs):
                    unosSourceUIDs.add( unSourceUID)
                    unosSourceForTarget[ 1].append( theSource)
                    
                self.vMappingsForTargets[ unTargetUID] = theMapping
                
                         
                unCompleted = True
                
                return True
        
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not unCompleted:
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fRegisterSourceToTargetCorrespondence', 
                        'status': cRefactorStatus_SourceToTargetCorrespondence_Not_Set,
                        'params': { 
                            'theSource': self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg_Unicode( theSource), 
                            'theTarget': self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTarget), 
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
                    
    
    
    
    

    
    
    def fGetMappingForTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        if not self.vMappingsForTargets:
            return {}

        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
        if not unTargetUID:
            return {}
        
        unMapping = self.vMappingsForTargets.get( unTargetUID, {})
        
        return unMapping
        
    
        
    def fGetTargets( self, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        todosUIDsAndTargets = self.vTargetsForSourcesMap.values()
        if not todosUIDsAndTargets:
            return []
        
        todosTargets = []
        for unosUIDsAndTargets in todosUIDsAndTargets:
            unosTargets = unosUIDsAndTargets[ 1]
            if unosTargets:
                todosTargets += unosTargets
                
        return todosTargets
    
    
    
    
    def fGetSourcesForTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
        if not unTargetUID:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unosUIDsAndSources = self.vSourcesForTargetsMap.get( unTargetUID, None)
        if not unosUIDsAndSources:
            return None
        
        unosSources = unosUIDsAndSources[ 1]
        return unosSources
    
    
    
        
    def fGetTargetsForSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
        if not unSourceUID:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_NoSourceUID
        
        unosUIDsAndTargets = self.vTargetsForSourcesMap.get( unSourceUID, None)
        if not unosUIDsAndTargets:
            return None
        
        unosTargets = unosUIDsAndTargets[ 1]
        return unosTargets
    
        
    
  


    def pRegisterPloneSourceToTargetCorrespondence( self, theSource, theTarget,):
        
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
     
        unSourceUID = self.vRefactor.vSourceInfoMgr.fGetPloneUID( theSource)
        if not unSourceUID:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_NoSourceUID
        
        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetPloneUID( theTarget)
        if not unTargetUID:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_NoTargetUID
        
        unosTargetForSource = self.vTargetsForSourcesMap.get( unSourceUID, None)
        if unosTargetForSource == None:
            unosTargetForSource = [ set(), [], ]
            self.vTargetsForSourcesMap[ unSourceUID] = unosTargetForSource
            
        unosTargetUIDs = unosTargetForSource[ 0]
        if not ( unTargetUID in unosTargetUIDs):
            unosTargetUIDs.add( unTargetUID)
            unosTargetForSource[ 1].append( theTarget)
        
        unosSourceForTarget = self.vSourcesForTargetsMap.get( unTargetUID, None)
        if unosSourceForTarget == None:
            unosSourceForTarget = [ set(), [], ]
            self.vSourcesForTargetsMap[ unTargetUID] = unosSourceForTarget
            
        unosSourceUIDs = unosSourceForTarget[ 0]
        if not ( unSourceUID in unosSourceUIDs):
            unosSourceUIDs.add( unSourceUID)
            unosSourceForTarget[ 1].append( theSource)
            
        self.vMappingsForTargets[ unTargetUID] = None
        
        return self
    
    
    
    
    
class MDDRefactor_Paste_MapperMetaInfoMgr_ConvertTypes ( MDDRefactor_Role_MapperMetaInfoMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_MapperMetaInfoMgr.__init__( self)
        
        self.vMappingsByTargetTypeMap = { }
        
        
        
        
        
                
                
    def fFirstMappedTypeFromSourceTypeToTargetType( self, theSourceType, theTargetType, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSourceType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_SourceType
        
        if not theTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_TargetType
        
        someMappingConfigs = self.vRefactor.fGetContextParam( 'mapping_configs')
        if not someMappingConfigs:
            return ''
        
        for aMappingConfig in someMappingConfigs:
            if aMappingConfig:
                somePortalTypes = aMappingConfig.get( 'portal_types', [])
                aIsAbstract = aMappingConfig.get( 'abstract', False)
                if somePortalTypes and ( not aIsAbstract) and ( theSourceType in somePortalTypes) and  ( theTargetType in somePortalTypes):
                    for aMappedType in somePortalTypes:
                        if not ( aMappedType == theSourceType):
                            return aMappedType
        return ''
        
                 
                
    def fCompileMappingFromSourceTypeToMappedType( self, theSourceType, theMappedType, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSourceType or not theMappedType:
            return {}
        
        someMappingConfigs = self.vRefactor.fGetContextParam( 'mapping_configs')
        if not someMappingConfigs:
            return {}
        
        aAtLeastOneNonAbstractFound = False
        
        allSameFeatures   = [ ]
        allMappedFeatures = { }
        
        aMapping = { 
            'source_type':      theSourceType,
            'mapped_type':      theMappedType,
            'same_features':    allSameFeatures,
            'mapped_features':  allMappedFeatures,
        }
        
        for aMappingConfig in someMappingConfigs:
            if aMappingConfig:
                somePortalTypes = aMappingConfig.get( 'portal_types', [])
                if somePortalTypes and ( theSourceType in somePortalTypes) and ( theMappedType in somePortalTypes):
                    
                    aSourceIndex = somePortalTypes.index( theSourceType)
                    aMappedIndex = somePortalTypes.index( theMappedType)
                        
                    aIsAbstract = aMappingConfig.get( 'abstract', False)
                    if not aIsAbstract:
                        aAtLeastOneNonAbstractFound = True
                        
                    someSameFeatures = aMappingConfig.get( 'same_features', [])
                    if someSameFeatures:
                        for aFeatureName in someSameFeatures:
                            if not ( aFeatureName in allSameFeatures):
                                allSameFeatures.append( aFeatureName)
                                
                    someFeatureMappings = aMappingConfig.get( 'mapped_features', [])
                    if someFeatureMappings:
                        
                        for aFeatureMapping in someFeatureMappings:
                            if aFeatureMapping:
                                
                                aSourceFeatureName = aFeatureMapping[ aSourceIndex]
                                aMappedFeatureName = aFeatureMapping[ aMappedIndex]
                                                                    
                                allMappedFeatures[ aMappedFeatureName] = aSourceFeatureName
                                        
        return aMapping
        
        
        
            
       
    
    
    
    def fTargetAggregationConfigAndTypeToAggregateSourceIn( self, theSource, theTarget, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theTarget:
            return []
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            return []
        
        unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
        if not unTargetType:
            return []
        
        """StraightCopy : same type, if allowed.
        
        """
        unasAggregationsWithType = self.vRefactor.vTargetMetaInfoMgr.fAggregationConfigsWithType( unTargetType, unSourceType)
        if not unasAggregationsWithType:
            return []
        
        return [ unasAggregationsWithType[ 0], unSourceType, ]
    
    
    
    
    def fMappingAndTargetAggregationConfigAndTypeToAggregateSourceIn( self, theSource, theTarget, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theTarget:
            return []
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            return []
        
        unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
        if not unTargetType:
            return []
        
        unosAggregatedTypes = self.vRefactor.vTargetMetaInfoMgr.fAggregatedTypes( unTargetType)
        
        if unSourceType in unosAggregatedTypes:
            unasAggregationsWithType = self.vRefactor.vTargetMetaInfoMgr.fAggregationConfigsWithType( unTargetType, unSourceType)
            if unasAggregationsWithType:
                return [ None, unasAggregationsWithType[ 0], unSourceType, ]
            
            
        for unAggregatedType in unosAggregatedTypes:
            unMappedType = self.fFirstMappedTypeFromSourceTypeToTargetType( unSourceType, unAggregatedType)
            if unMappedType:
                
                unMapping = self.fCompileMappingFromSourceTypeToMappedType( unSourceType, unMappedType, )
                if unMapping:

                    unasAggregationsWithType = self.vRefactor.vTargetMetaInfoMgr.fAggregationConfigsWithType( unTargetType, unAggregatedType)
                    if unasAggregationsWithType:
                        return [ unMapping, unasAggregationsWithType[ 0], unAggregatedType, ]
        
        return []
    
    
    
        
    
    
    
    
  
       
    def fSourceAttributeNameAndTypeForTargetNameAndType( self, theSource, theNameAndTypeToPopulate, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not theSource or not theNameAndTypeToPopulate:
            return []

        if not theMapping:
            """StraightCopy : same attribute.
            
            """
            return theNameAndTypeToPopulate[:] 
        
        anAttributeName = theNameAndTypeToPopulate[ 0]
        if not anAttributeName:
            return []
                
        someSameFeatures = theMapping.get( 'same_features', [])
        if someSameFeatures and ( anAttributeName in someSameFeatures):
            return theNameAndTypeToPopulate[:] + [ anAttributeName,]
        
        someMappedFeatures = theMapping.get( 'mapped_features', [])
        unMappedFeature = someMappedFeatures.get( anAttributeName, None)
        if not unMappedFeature:
            return []
        
        unMappedFeatureType = self.vRefactor.vSourceMetaInfoMgr.fAttributeTypeInSource( theSource, unMappedFeature)
        if not unMappedFeatureType:
            return []
            
        return  [ unMappedFeature, unMappedFeatureType] 
    
    
       
    
    
    
    def fMappedTraversalNameFromSourceForTargetAggregationName( self, theSource, theAggregationName, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not theSource or not theAggregationName:
            return None
        
        if not theMapping:
            """StraightCopy : expression is same aggregation name, if source has it
            
            """
            if self.vRefactor.vSourceMetaInfoMgr.fHasAggregationNamed( theSource, theAggregationName):
                return theAggregationName
            return ''
       
        someSameFeatures = theMapping.get( 'same_features', [])
        if someSameFeatures and ( theAggregationName in someSameFeatures):
            return theAggregationName
        
        someMappedFeatures = theMapping.get( 'mapped_features', [])
        unMappedFeature = someMappedFeatures.get( theAggregationName, None)
        if not unMappedFeature:
            return ''
        
        if self.vRefactor.vSourceMetaInfoMgr.fHasAggregationNamed( theSource, unMappedFeature):
            return unMappedFeature
        
        return ''

    

    
    def fMappedTraversalNameFromSourceForTargetRelationName( self, theSource, theRelationName, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not theSource or not theRelationName:
            return None
        
        if not theMapping:
            """StraightCopy : expression is same aggregation name, if source has it
            
            """
            if self.vRefactor.vSourceMetaInfoMgr.fHasRelationNamed( theSource, theRelationName):
                return theRelationName
            return ''
       
        someSameFeatures = theMapping.get( 'same_features', [])
        if someSameFeatures and ( theRelationName in someSameFeatures):
            return theRelationName
        
        someMappedFeatures = theMapping.get( 'mapped_features', [])
        unMappedFeature = someMappedFeatures.get( theRelationName, None)
        if not unMappedFeature:
            return ''
        
        if self.vRefactor.vSourceMetaInfoMgr.fHasRelationNamed( theSource, unMappedFeature):
            return unMappedFeature
        
        return ''

    
    
    def fMappingAndTargetTypeFromSourceAndAllowedTypes( self, theSource, theAllowedTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not theSource or not theAllowedTypes:
            return []
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            return []

        if unSourceType in theAllowedTypes:
            """StraightCopy : same type, if allowed.
            
            """
            return [ None, unSourceType, ]
        
        for unAllowedType in theAllowedTypes:
            unMappedType = self.fFirstMappedTypeFromSourceTypeToTargetType( unSourceType, unAllowedType)
            if unMappedType:
                unMapping = self.fCompileMappingFromSourceTypeToMappedType( unSourceType, unAllowedType, )
                
                if unMapping:
                    return [ unMapping,  unAllowedType]
        
        return []
    
            
    
    def fTargetTypeFromSourceForTargetAggregationTraversalConfig( self, theSource, theTraversalConfig,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not theSource or not theTraversalConfig:
            return ''
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            return ''
        
        unosAgregatedTypes = self.vRefactor.vTargetMetaInfoMgr.fAggregatedTypesFromTraversalConfig( theTraversalConfig)
        if not unosAgregatedTypes:
            return ''
        
        """StraightCopy : same type, if allowed.
        
        """
        if unSourceType in unosAgregatedTypes:
            return unSourceType
        
        return ''
    
    
    
    def fTargetTypeFromSourceForTargetRelationTraversalConfig( self, theSource, theTraversalConfig,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not theSource or not theTraversalConfig:
            return ''
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            return ''
        
        unosAggregatedTypes = self.vRefactor.vTargetMetaInfoMgr.fRelatedTypesFromTraversalConfig( theTraversalConfig)
        if not unosAggregatedTypes:
            return ''
        
        """StraightCopy : same type, if allowed.
        
        """
        if unSourceType in unosAggregatedTypes:
            return unSourceType
        
        return ''
        
                       
    def fTraversalNameFromSourceForTargetRelationConfig( self, theSource, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not theSource or not theTraversalConfig:
            return None
        
        """StraightCopy : expression is same aggregation name, if source has it
        
        """
        unTargetRelationName = self.vRefactor.vTargetMetaInfoMgr.fRelationNameFromTraversalConfig( theTraversalConfig)
        someSourceRelationNames = self.vRefactor.vSourceMetaInfoMgr.fRelationNamesFromSource( theSource)
        
        if unTargetRelationName in someSourceRelationNames:
            return unTargetRelationName
        
        return ''
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# ######################################################
# IMPORT refactoring
# ######################################################
    


            
class MDDRefactor_Import ( MDDRefactor):
    """Agent to perform a paste refactoring.
    
    """
    def __init__( self, 
        theModelDDvlPloneTool,
        theModelDDvlPloneTool_Retrieval,
        theModelDDvlPloneTool_Mutators,
        theZIPFile, 
        theFileNames, 
        theXMLDocument,
        theXMLEncoding,
        theXMLRootElements,
        theTargetRoot, 
        theTargetRootResult, 
        theTargetMDDTypeConfigs, 
        theTargetPloneTypeConfigs, 
        theTargetAllTypeConfigs, 
        theMappingConfigs,
        theExceptionToRaise,
        theAllowPartialCopies,
        theIgnorePartialLinksForMultiplicityOrDifferentOwner):
        
        
        unInitialContextParms = {
            'zip_file':                 theZIPFile,
            'file_names':               theFileNames,
            'xml_document':             theXMLDocument,
            'xml_encoding':             theXMLEncoding,            
            'xml_root_elements':        theXMLRootElements,
            'target_root':              theTargetRoot,
            'target_root_result':       theTargetRootResult,
            'target_mdd_type_configs':  theTargetMDDTypeConfigs,
            'target_plone_type_configs':theTargetPloneTypeConfigs,
            'target_all_type_configs':  theTargetAllTypeConfigs,
            'mapping_configs':          theMappingConfigs,
        }
        
        MDDRefactor.__init__(
            self,
            theModelDDvlPloneTool,
            theModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators,
            unInitialContextParms,
            MDDRefactor_Import_SourceInfoMgr_XMLElements(), 
            MDDRefactor_Import_SourceMetaInfoMgr_XMLElements(), 
            MDDRefactor_Paste_TargetInfoMgr_MDDElement(), 
            MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement(), 
            MDDRefactor_Paste_MapperInfoMgr(), 
            MDDRefactor_Paste_MapperMetaInfoMgr_ConvertTypes(), 
            MDDRefactor_Import_TraceabilityMgr(), 
            MDDRefactor_Paste_Walker(), 
            True, # theAllowMappings
            theExceptionToRaise,
            theAllowPartialCopies,
            theIgnorePartialLinksForMultiplicityOrDifferentOwner
        )
    
        


         

class MDDRefactor_Import_SourceInfoMgr_XMLElements( MDDRefactor_Role_SourceInfoMgr):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_SourceInfoMgr.fInitInRefactor( self, theRefactor,):
            return False
        
        # ACV 20091112 May upload directly an xml not in a .zip archive. Removed.
        #if not self.vRefactor.fGetContextParam( 'zip_file',):
            #return False
        
        if not self.vRefactor.fGetContextParam( 'xml_document',):
            return False
        
        if not self.vRefactor.fGetContextParam( 'xml_root_elements',):
            return False

        unTargetRoot = self.vRefactor.fGetContextParam( 'target_root',)
        if ( unTargetRoot == None):
            return False
        
        aPloneUtilsTool = getToolByName( unTargetRoot, 'plone_utils', None)
        if ( aPloneUtilsTool == None):
            return False
        
        aSiteEncoding = aPloneUtilsTool.getSiteEncoding()
        if not aSiteEncoding:
            aSiteEncoding = cEncodingUTF8
        
        self.vRefactor.pSetContextParam( 'site_encoding', aSiteEncoding)
        
        return True
    
        
       

    def fElementIdentificationForErrorMsg( self, theSource):
        
        if theSource == None:
            return str( None)
        
        unTitle = self.fGetTitle( theSource)
        unaId   = self.fGetId(    theSource)
        unPath  = self.fGetPath(  theSource)
        unaId   = self.fGetUID(   theSource)
        
        unaIdentification = 'Title=%s; id=%s; path=%s UID=%s' % ( repr( unTitle), repr( unaId), repr( unPath), repr( unaUID),)

        return unaIdentification
    

        
    def fElementIdentificationForErrorMsg_Unicode( self, theSource):        
      
        unaIdentification = self.fElementIdentificationForErrorMsg( theSource)
        unaIdentificationUnicode = ModelDDvlPloneTool().fAsUnicode( self.vRefactor.fGetContextParam( 'target_root'), unaIdentification)
        
        return unaIdentificationUnicode

    
    
    def fGetSiteEncoding( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        aSiteEncoding = self.vRefactor.fGetContextParam( 'site_encoding',)
        return aSiteEncoding
    
    
    
    
    def fGetSourceRoots( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        unosSourceElements = self.vRefactor.fGetContextParam( 'xml_root_elements',) 
        
        unosPloneTypeNames = cPloneTypes.keys()
        
        unosNonPloneElements = [ ]
        
        for unSourceElement in unosSourceElements:
            unTypeName = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unSourceElement)
            if not ( unTypeName in unosPloneTypeNames):
                unosNonPloneElements.append( unSourceElement)
                
        return unosNonPloneElements

    

    
    
    
    def fIsSourceReadable( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            return False
    
        return True
    
    
    
    
    def fIsSourceOk( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameters
        
        allTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',)
        if not allTypeConfigs:
            return False
        
        unSourceType = theSource.nodeName
        
        if unSourceType.endswith( cXMLRelatedMetaTypePostfix):
            unSourceType = unSourceType[:0 - len( cXMLRelatedMetaTypePostfix)]
            
        if not allTypeConfigs.has_key( unSourceType):
            return False
        
        return True
    
    

     
     
    
    def fFromUnicodeToSystemEncoding( self, theXMLString,):
        
        if not theXMLString:
            return ''
        
        if isinstance( theXMLString, unicode):
            unStringUnicode = theXMLString
            
        else:
            
            unStringUnicode = None
            try:
                unStringUnicode = theXMLString.decode( cEncodingUTF8, errors=cEncodingErrorHandleMode_Strict)
            except UnicodeDecodeError:
                None
        
            if not unStringUnicode:
                return None
 
        unSiteEncoding = self.fGetSiteEncoding()
        if not unSiteEncoding:
            unSiteEncoding = cEncodingUTF8
        
        unStringEncoded  = None
        try:
            unStringEncoded = unStringUnicode.encode( unSiteEncoding, cEncodingErrorHandleMode_Strict)      
        except UnicodeEncodeError:
            None
                
        if not unStringEncoded:
            return None
        
        return unStringEncoded
    
    
    
    
    
    def fGetId( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        
        unaId = theSource.getAttribute( cXMLAttributeName_PloneId)
        if unaId:
            unEncoded = self.fFromUnicodeToSystemEncoding( unaId, )
            return unEncoded
        
        unPath = self.fGetPath( theSource)
        if not unPath:
            return ''
        
        unosPathSteps = unPath.split( '/')
        if not unosPathSteps:
            return ''
        
        unaId = unosPathSteps[-1:][ 0]
        
        unEncoded = self.fFromUnicodeToSystemEncoding( unaId, )
        return unEncoded
        
    
    
    def fGetUID( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        
        unaUID = theSource.getAttribute( cXMLAttributeName_PloneUID)
        unEncoded = self.fFromUnicodeToSystemEncoding( unaUID, )
        return unEncoded    
    
    
    
    def fGetPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        
        unPath = theSource.getAttribute( cXMLAttributeName_PlonePath)
        unEncoded = self.fFromUnicodeToSystemEncoding( unPath, )
        return unEncoded    
     
    
    def fGetTitle( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        
        unTitle = theSource.getAttribute( cXMLAttributeName_PloneTitle)
        unEncoded = self.fFromUnicodeToSystemEncoding( unTitle, )
        return unEncoded    
    
    
    
    
    def fOwnerPath( self, theSource):
        #if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            #return ''        
        return ''
    
    
    
    def fRootPath( self, theSource):
        #if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            #return ''
        
        return ''
    
    
    
    def fGetAttributeValue( self, theSource, theAttributeName, theAttributeType):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return None
    
        if ( not theAttributeName) or ( not theAttributeType):
            return None
        
        if theAttributeName.lower() == 'title':
            return self.fGetTitle( theSource)
        elif theAttributeName.lower() == 'id':
            return self.fGetId( theSource)
        elif theAttributeName.lower() == 'path':
            return self.fGetPath( theSource)
        elif theAttributeName.lower() == 'uid':
            return self.fGetUID( theSource)
            
        unosChildNodes = theSource.childNodes
        if not unosChildNodes:
            return None
        
        for unChildNode in unosChildNodes:
            
            unAttrValue = ''
            
            unNodeName = unChildNode.nodeName
            if unNodeName and not ( unNodeName == cXMLElementName_CommentText):
                                
                if unNodeName == theAttributeName:
                    
                    unosAttrChildNodes = unChildNode.childNodes
                    if unosAttrChildNodes:
                        
                        unPloneContentType = unChildNode.getAttribute( cXMLAttributeName_ContentType)
                        
                        if unPloneContentType.startswith( 'text'):
                                                        
                            for unAttrChildNode in unosAttrChildNodes:
                                
                                if unAttrChildNode.nodeType == clsXMLNode.CDATA_SECTION_NODE:
                                    
                                    unAttrValue = unAttrChildNode.nodeValue
                                    if unAttrValue:
                                        unAttrValue = unAttrValue.strip()
                                    break
                        else:
                        
                            for unAttrChildNode in unosAttrChildNodes:
                                    
                                unChildNodeType = unAttrChildNode.nodeType
                        
                                if unChildNodeType == clsXMLNode.TEXT_NODE:
                                    
                                    unAttrValue = unAttrChildNode.nodeValue
                                    if unAttrValue:
                                        unAttrValue = unAttrValue.strip()
                                    break
                                    
                                elif unChildNodeType == clsXMLNode.CDATA_SECTION_NODE:
                                    
                                    unAttrValue = unAttrChildNode.nodeValue
                                    if unAttrValue:
                                        unAttrValue = unAttrValue.strip()
                                    break
                            
                    if not unAttrValue:
                        return None
                    
                    unAttributeType = theAttributeType.lower()
                    
                    if unAttributeType in [ 'string', 'selection',]:
                        unAttrValue = unAttrValue.replace( '\t',' ')
                        unAttrValue = unAttrValue.replace( '\r',' ')
                        unAttrValue = unAttrValue.replace( '\n',' ')
                        unAttrValue = unAttrValue.strip()
                        unAttrValue = self.fFromUnicodeToSystemEncoding( unAttrValue, )
                    
                    elif unAttributeType in [ 'text', ]:
                        unAttrValue = unAttrValue.replace( '\r\n','\n')
                        unAttrValue = unAttrValue.replace( '\r','\n')
                        unAttrValue = unAttrValue.strip()
                        unAttrValue = self.fFromUnicodeToSystemEncoding( unAttrValue, )
                        
                    
                    elif unAttributeType == 'selection':
                        unAttrValue = self.fFromUnicodeToSystemEncoding( unAttrValue, )
                        
                    
                    
                    elif unAttributeType == 'boolean':
                        if unAttrValue.lower() == str( True).lower():
                            unAttrValue = True
                        else:
                            unAttrValue = False
                        
                    elif unAttributeType in [ 'integer' ]:
                        unNumber = None
                        try:
                            unNumber = int( unAttrValue)                                               
                        except:
                            None
                        if not ( unNumber == None):
                            unAttrValue =  unNumber
                        else:
                            unAttrValue = 0
                        
                    elif unAttributeType in [ 'float', 'fixedpoint', ]:
                        unNumber = None
                        try:
                            unNumber = float( unAttrValue)                                               
                        except:
                            None
                        if not ( unNumber == None):
                            unAttrValue =  unNumber
                        else:
                            unAttrValue = 0.0

                        
                    elif unAttributeType in [ 'datetime', 'date', ]:
                        unDate = None
                        try:
                            unDate = DateTime( unAttrValue)                                               
                        except:
                            None
                        if unDate:
                            unAttrValue =  unDate
                        else:
                            unAttrValue = None

                        
                    elif unAttributeType == 'file':
                        unFilePath = unAttrValue
                        unAttrValue = None
                        if unFilePath:
                            unosFileNames  = self.vRefactor.fGetContextParam( 'file_names',) 
                            if unosFileNames and ( unFilePath in unosFileNames):
                                unZipFile  = self.vRefactor.fGetContextParam( 'zip_file',) 
                                if unZipFile:
                                    unFileData = None
                                    try:
                                        unFileData =self.fZipFileElementContent( unZipFile, unFilePath)
                                    except:
                                        None
                                    if unFileData:
                                        unFileId = unChildNode.getAttribute( cXMLAttributeName_PloneId)
                                        if not unFileId:
                                            unFileId = 'file'
                                        unFileTitle = unChildNode.getAttribute( cXMLAttributeName_PloneTitle)
                                        if not unFileTitle:
                                            unFileTitle= unFileId
                                        unFileContentType = unChildNode.getAttribute( cXMLAttributeName_ContentType)
                                        if unFileContentType:
                                            unaFile = File( unFileId, unFileTitle, clsFastStringIO( unFileData), content_type=unFileContentType)
                                        else:
                                            unaFile = File( unFileId, unFileTitle, clsFastStringIO( unFileData),)
                                            
                                        unAttrValue = unaFile
                                
                    elif unAttributeType == 'image':
                        unFilePath = unAttrValue
                        unAttrValue = None
                        if unFilePath:
                            unosFileNames  = self.vRefactor.fGetContextParam( 'file_names',) 
                            if unosFileNames and ( unFilePath in unosFileNames):
                                unZipFile  = self.vRefactor.fGetContextParam( 'zip_file',) 
                                if unZipFile:
                                    unImageData = None
                                    try:
                                        unImageData = self.fZipFileElementContent( unZipFile, unFilePath)
                                    except:
                                        None
                                    
                                    if unImageData:
                                        unImageId = unChildNode.getAttribute( cXMLAttributeName_PloneId)
                                        if not unImageId:
                                            unImageId = 'image'
                                        unImageTitle = unChildNode.getAttribute( cXMLAttributeName_PloneTitle)
                                        if not unImageTitle:
                                            unImageTitle = unImageId
                                        unImageContentType = unChildNode.getAttribute( cXMLAttributeName_ContentType)
                                        if unImageContentType:
                                            unaImage = Image( unImageId, unImageTitle, clsFastStringIO( unImageData), content_type=unImageContentType)
                                        else:
                                            unaImage = Image( unImageId, unImageTitle, clsFastStringIO( unImageData), )
                                            
                                        unAttrValue = unaImage
                                    
                    return unAttrValue
            
        return None
            
    

     
    def fZipFileElementContent( self, theZipFile, theFileName):
  
        if not theZipFile or not theFileName:
            return None
        
        unContent = None
        try:
            unContent = theZipFile.read( theFileName)
        except:
            return None
        return unContent
            
    
    
    
    
    def fGetTraversalValues( self, theSource, theTraversalName, theAcceptedSourceTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource) or ( not theTraversalName):
            return []
        
        unosChildNodes = theSource.childNodes
        if not unosChildNodes:
            return []
        
        someAcceptedSourceTypes = theAcceptedSourceTypes
        
        if someAcceptedSourceTypes and self.vRefactor.vSourceMetaInfoMgr.fHasRelationNamed( theSource, theTraversalName):
            for anAcceptedSourceType in someAcceptedSourceTypes:
                someAcceptedSourceTypes.append( anAcceptedSourceType + cXMLRelatedMetaTypePostfix)
            
        for unChildNode in unosChildNodes:
            unNodeName = unChildNode.nodeName
            if unNodeName and not ( unNodeName == cXMLElementName_CommentText):
                                
                if unNodeName == theTraversalName:
                    
                    unosRetrievedElements = [ ]
                    
                    unosSubChildNodes = unChildNode.childNodes
                    if unosSubChildNodes:
                        
                        for unSubChildNode in unosSubChildNodes:
                            
                            unSubChildNodeName = unSubChildNode.nodeName
                            
                            if not ( unSubChildNodeName == cXMLElementName_CommentText):
                                if unSubChildNode.nodeType == clsXMLNode.ELEMENT_NODE:
                                    if ( not someAcceptedSourceTypes) or ( unSubChildNodeName in someAcceptedSourceTypes):
                                        unosRetrievedElements.append( unSubChildNode)
                            
                    return unosRetrievedElements
            
        return []
        

    
    

    
        
    
class MDDRefactor_Import_SourceMetaInfoMgr_XMLElements( MDDRefactor_Role_SourceMetaInfoMgr):
    """
    
    """
    


    def fTypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unTypeName = theSource.nodeName

        if unTypeName.endswith( cXMLRelatedMetaTypePostfix):
            unTypeName = unTypeName[:0 - len( cXMLRelatedMetaTypePostfix)]
        
        unUnicodeTypeName = self.vRefactor.vSourceInfoMgr.fFromUnicodeToSystemEncoding( unTypeName) 
            
        return unUnicodeTypeName
    
    
    
    
    def fGetArchetypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unArchetypeName = theSource.nodeName
        
        if unArchetypeName.endswith( cXMLRelatedMetaTypePostfix):
            unArchetypeName = unArchetypeName[:0 - len( cXMLRelatedMetaTypePostfix)]
        
        unUnicodeArchetypeName = self.vRefactor.vSourceInfoMgr.fFromUnicodeToSystemEncoding( unArchetypeName) 
            
        return unUnicodeArchetypeName
    
    

    
    def fPloneTypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if ( thePloneElement == None):
            return ''
        
        unTypeName  = thePloneElement.nodeName
        
        unUnicodeTypeName = self.vRefactor.vSourceInfoMgr.fFromUnicodeToSystemEncoding( unTypeName) 
            
        return unUnicodeTypeName
    
    
    
    def fPloneArchetypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if ( thePloneElement == None):
            return ''
        
        unPloneTypeName = self.fPloneTypeName( thePloneElement)
        if not unPloneTypeName:
            return ''
        
        unPloneNames = cPloneTypes.get( unPloneTypeName, {})
        if not unPloneNames:
            return ''
        
        unArchetypeName = unPloneNames.get( 'archetype_name', '')
        return unArchetypeName
    
    
    def fPlonePortalType( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if ( thePloneElement == None):
            return ''
        
        unPloneTypeName = self.fPloneTypeName( thePloneElement)
        if not unPloneTypeName:
            return ''
        
        unPloneNames = cPloneTypes.get( unPloneTypeName, {})
        if not unPloneNames:
            return ''
        
        unPortalType = unPloneNames.get( 'portal_type', '')
        return unPortalType
    
    

        
    
    def fTypeConfig( self, theSource, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theSource:
            return {}
        
        unTypeName = self.fTypeName( theSource)
        if not unTypeName:
            return {}
        
        unTypeConfig = self.fTypeConfigForType( unTypeName, theTypeConfigName)
        return unTypeConfig
    
    
        
    
    def fTypeConfigForType( self, theSourceType, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theSourceType:
            return {}

        unTargetAllTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',) 
        if not unTargetAllTypeConfigs:
            return {}
        
        unasTypeConfigs = unTargetAllTypeConfigs.get( theSourceType, {})
        if not unasTypeConfigs:
            return {}
        
        unTypeConfigName = theTypeConfigName
        if ( not unTypeConfigName) or ( unTypeConfigName == 'Default'):
            unTypeConfigName = sorted( unasTypeConfigs.keys())[ 0]
        
        unaTypeConfig = unasTypeConfigs.get( unTypeConfigName, {})
        if not unaTypeConfig:
            return {}
        
        return unaTypeConfig
    
    
    
    def fAggregationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
        if not theSource:
            return []
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasAggregationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and not ( unAggregationName in unasAggregationNames):
                unasAggregationNames.append( unAggregationName)
                
        return unasAggregationNames
    
    
    
    
    def fHasAggregationNamed( self, theSource, theAggregationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        
        if not theSource or not theAggregationName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theAggregationName):
                return True
                
        return False
    
    
    
    def fHasRelationNamed( self, theSource, theRelationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        
        if not theSource or not theRelationName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theRelationName):
                return True
                
        return False

    
       
    def fHasTraversalNamed( self, theSource, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        
        if not theSource or not theTraversalName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theTraversalName):
                return True
            
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theTraversalName):
                return True
                
        return False

    
     
    
    
    def fRelationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
        if not theSource:
            return []
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasRelationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and not ( unRelationName in unasRelationNames):
                unasRelationNames.append( unRelationName)
                
        return unasRelationNames
    
    
    
    
    def fAttributeTypeInSource( self, theSource, theAttributeName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource or not theAttributeName:
            return ''
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return ''
       
        unosAttributeConfigs = unTypeConfig.get( 'attrs', [])
        if not unosAttributeConfigs:
            return ''
     
        for unAttributeConfig in unosAttributeConfigs:
            
            # ACV 20091110 Changed key.  'attribute_name' appears in  results, not configs
            # Don't know how this was working without it - indeed, because it was ignored, or fallbacks applied.
            # unAttributeName = unAttributeConfig.get( 'attribute_name', '')
            unAttributeName = unAttributeConfig.get( 'name', '')
            if unAttributeName and ( unAttributeName == theAttributeName):
                
                unAttributeType = unAttributeConfig.get( 'type', '')
                return unAttributeType
            
        return ''
                
                

    
    
    

    
                        
    
class MDDRefactor_Import_TraceabilityMgr( MDDRefactor_Role_TraceabilityMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_TraceabilityMgr.__init__( self)
        

        

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_TraceabilityMgr.fInitInRefactor( self, theRefactor,):
            return False
        
                            
        return True
    
                    

    
    def fEstablishTraceabilityLinks( self, theSource, theTarget):
        return True
    
    

    
            
    
    
        
    
    
    
    
    
    
    
    
    

        
    
class MDDRefactor_Paste_Walker ( MDDRefactor_Role_Walker):
    """
    
    """
    
    
    
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_Walker.fInitInRefactor( self, theRefactor,):
            return False
        
        unRefactorStack = MDDRefactor_Paste_Walker_Stack()        
        
        self.vRefactor.pSetContextParam( 'stack', unRefactorStack)        
        
        return True
    
    
    
    
    
    
    def fRefactor( self,):

        unCompleted   = False
        unInException = False
        unErrorReason = ''
        unMethodName  = u'fRefactor'
        
        try:
            try:
                
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
        
                unosSourceRoots             = self.vRefactor.vSourceInfoMgr.fGetSourceRoots()
                
                if not unosSourceRoots:
                    unErrorReason = cRefactorStatus_Missing_Parameter_SourceRoots
                    return  False
                
                unTargetRoot = self.vRefactor.vTargetInfoMgr.fGetTargetRoot()
                if ( unTargetRoot == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_SourceRoots
                    return  False
                
                unTargetRootResult = self.vRefactor.vTargetInfoMgr.fGetTargetRootResult()
                if ( unTargetRootResult == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_TargetRoot
                    return False
                
                if not self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'read_permission'):
                    unErrorReason = cRefactorStatus_TargetRoot_Not_Readable
                    return  False
                
                if not self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'write_permission'):
                    unErrorReason = cRefactorStatus_TargetRoot_Not_Writable
                    return  False
                
                transaction.savepoint(optimistic=True)
                
                aIntoRootResult = self.fRefactor_IntoRoot( unosSourceRoots, unTargetRoot)

                if aIntoRootResult or self.vRefactor.vAllowPartialCopies:
                    transaction.savepoint(optimistic=True)
                else:
                    unErrorReason = cRefactorStatus_IntoRoot_NotCompleted
                    return  False
        
                
                
                unIsMoveOperation =  self.vRefactor.fGetContextParam( 'is_move_operation')
                if unIsMoveOperation:
                    
                    aMovesResult = self.fRefactor_Moves()

                    if aMovesResult:
                        transaction.savepoint(optimistic=True)
                    else:
                        unErrorReason = cRefactorStatus_Moves_NotCompleted
                        return  False
                        
        
                        
                aRelationsResult = self.fRefactor_Relations( )
                if aRelationsResult  or self.vRefactor.vAllowPartialCopies:
                    transaction.savepoint(optimistic=True)
                else:
                    unErrorReason = cRefactorStatus_Relations_NotCompleted
                    return  False
        
                unCompleted = True
                
                return True
           
            except:
                unInException = True
                raise

        finally:
            if not unInException:
                if not unCompleted:
                    
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': unMethodName, 
                        'status': unicode( cRefactorStatus_Not_Completed),
                        'reason': unicode( unErrorReason),
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
            
    
    
    

    
    
    def fRefactor_IntoRoot( self, theSourceRoots, theTargetRoot):
        
        unCompleted   = False
        unInException = False
        unErrorReason = ''
        unMethodName  = u'fRefactor_IntoRoot'
        
        try:
            try:
                        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
            
                if not theSourceRoots:
                    unErrorReason = cRefactorStatus_Missing_Parameter_SourceRoots
                    return False
                
                if theTargetRoot == None:
                    unErrorReason = cRefactorStatus_Missing_Parameter_TargetRoot
                    return False
                
                unTargetRootType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTargetRoot)
                if not unTargetRootType:
                    unErrorReason = cRefactorStatus_Error_NoTarget_Type
                    return False
        
                unTargetRootTitle = self.vRefactor.vTargetInfoMgr.fGetTitle( theTargetRoot)
                if not unTargetRootTitle:
                    unErrorReason = cRefactorStatus_Error_NoTarget_Title
                    return False
                
                unTargetRootResult = self.vRefactor.vTargetInfoMgr.fGetTargetRootResult() 
                if not unTargetRootResult:
                    unErrorReason = cRefactorStatus_NoTargetResult
                    return False
                
                unTargetRootTypeConfig =  self.vRefactor.vTargetMetaInfoMgr.fTypeConfig( theTargetRoot)     
                if not unTargetRootTypeConfig:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_No_TypeConfig
                    return False
                
                unRefactorStack = self.vRefactor.fGetContextParam( 'stack')  
                if not unRefactorStack:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_No_Stack
                    return False
                
                someSourcesMappedToSameTypeAsTargetRoot     = [ ]
                someSourcesMappedToAggregationsInTargetRoot = [ ]
                
                for unSourceRoot in theSourceRoots:
                    if not self.vRefactor.vSourceInfoMgr.fIsSourceOk( unSourceRoot):
                        unErrorReason = cRefactorStatus_SourceRoot_Not_OK
                        if not self.vRefactor.vAllowPartialCopies:
                            return False
                        else:
                            anErrorReport = { 
                                'theclass': self.__class__.__name__, 
                                'method': unMethodName, 
                                'status': unicode( unErrorReason),
                            }
                            self.vRefactor.pAppendErrorReport( anErrorReport)
                            
                    else:
                        
                        if not self.vRefactor.vSourceInfoMgr.fIsSourceReadable( unSourceRoot):
                            unErrorReason = cRefactorStatus_SourceRoot_Not_Readable
                            if not self.vRefactor.vAllowPartialCopies:
                                return False
                            else:
                                anErrorReport = { 
                                    'theclass': self.__class__.__name__, 
                                    'method': unMethodName, 
                                    'status': unicode( unErrorReason),
                                }
                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                
                                
                        else:
                            
                            unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unSourceRoot)
                            if not unSourceType:
                                unErrorReason = cRefactorStatus_Error_NoSourceType
                                if not self.vRefactor.vAllowPartialCopies:
                                    return False
                                else:
                                    anErrorReport = { 
                                        'theclass': self.__class__.__name__, 
                                        'method': unMethodName, 
                                        'status': unicode( unErrorReason),
                                    }
                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                    
                            else:
                                
                                if ( unSourceType == unTargetRootType):
                                    someSourcesMappedToSameTypeAsTargetRoot.append( unSourceRoot)
                                    continue
                                
                                if not self.vRefactor.vAllowMappings:
                                    unMappedType = unSourceType
                                else:
                                    unMappedType = self.vRefactor.vMapperMetaInfoMgr.fFirstMappedTypeFromSourceTypeToTargetType( unSourceType, unTargetRootType)
                                    
                                if unMappedType:
                                    if unMappedType == unTargetRootType:
                                        someSourcesMappedToSameTypeAsTargetRoot.append( unSourceRoot)
                                        continue
                                
                                unMappingTargetAggregationConfigAndType = self.vRefactor.vMapperMetaInfoMgr.fMappingAndTargetAggregationConfigAndTypeToAggregateSourceIn( unSourceRoot, theTargetRoot)
                                if not ( unMappingTargetAggregationConfigAndType and len( unMappingTargetAggregationConfigAndType) > 2):
                                    unErrorReason = cRefactorStatus_Error_Paste_No_MappingTargetAggregationConfigAndType
                                    if not self.vRefactor.vAllowPartialCopies:
                                        return False
                                    else:
                                        anErrorReport = { 
                                            'theclass': self.__class__.__name__, 
                                            'method': unMethodName, 
                                            'status': unicode( unErrorReason),
                                        }
                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                    
                                else:
                                    unaTargetAggregationConfig = unMappingTargetAggregationConfigAndType[ 1]
                                    unTypeToCreate             = unMappingTargetAggregationConfigAndType[ 2]
                                    
                                    if not(  unaTargetAggregationConfig and unTypeToCreate):
                                        unErrorReason = cRefactorStatus_Error_Paste_No_TargetAggregationConfigAndTypeToCreate
                                        if not self.vRefactor.vAllowPartialCopies:
                                            return False
                                        else:
                                            anErrorReport = { 
                                                'theclass': self.__class__.__name__, 
                                                'method': unMethodName, 
                                                'status': unicode( unErrorReason),
                                            }
                                            self.vRefactor.pAppendErrorReport( anErrorReport)
                                        
                                    else:
                                        someSourcesMappedToAggregationsInTargetRoot.append( unSourceRoot)
                                        continue
                                    
                    
                
                if ( someSourcesMappedToAggregationsInTargetRoot):
                    
                    unRefactorRootAggregationsResult = self.fRefactor_RootAggregations( someSourcesMappedToAggregationsInTargetRoot, theTargetRoot)
                    if not unRefactorRootAggregationsResult:
                        unErrorReason = cRefactorStatus_RootAggregations_NotCompleted
                        if not self.vRefactor.vAllowPartialCopies:
                            return False
                        else:
                            anErrorReport = { 
                                'theclass': self.__class__.__name__, 
                                'method': unMethodName, 
                                'status': unicode( unErrorReason),
                            }
                            self.vRefactor.pAppendErrorReport( anErrorReport)
                            
                            
                            
                if ( someSourcesMappedToSameTypeAsTargetRoot):
                    
                    unRefactorSameRootTypesResult = self.fRefactor_SameRootTypes( someSourcesMappedToSameTypeAsTargetRoot, theTargetRoot)
                    if not unRefactorSameRootTypesResult:
                        unErrorReason = cRefactorStatus_RootAggregations_NotCompleted
                        if not self.vRefactor.vAllowPartialCopies:
                            return False
                        else:
                            anErrorReport = { 
                                'theclass': self.__class__.__name__, 
                                'method': unMethodName, 
                                'status': unicode( unErrorReason),
                            }
                            self.vRefactor.pAppendErrorReport( anErrorReport)
                
                                      
                unCompleted = True
                return True

            except:
                unInException = True
                raise
        
        finally:
            
            if not unInException:
                if not unCompleted:
                    
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': unMethodName, 
                        'status': unicode( cRefactorStatus_Not_Completed),
                        'reason': unicode( unErrorReason),
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
    
    
                
                
                
                
                
                
                 
                

    
    def fRefactor_SameRootTypes( self, theSourceRoots, theTargetRoot):
        
        unCompleted   = False
        unInException = False
        unErrorReason = ''
        unMethodName  = u'fRefactor_SameRootTypes'
        
        try:
            try:
                        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
            
                if not theSourceRoots:
                    unErrorReason = cRefactorStatus_Missing_Parameter_SourceRoots
                    return False
                
                if theTargetRoot == None:
                    unErrorReason = cRefactorStatus_Missing_Parameter_TargetRoot
                    return False
                                
                
                unTargetRootType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTargetRoot)
                if not unTargetRootType:
                    unErrorReason = cRefactorStatus_Error_NoTarget_Type
                    return False

                unTargetRootTitle = self.vRefactor.vTargetInfoMgr.fGetTitle( theTargetRoot)
                if not unTargetRootTitle:
                    unErrorReason = cRefactorStatus_Error_NoTarget_Title
                    return False                    
                 
                
                unTargetRootTypeConfig =  self.vRefactor.vTargetMetaInfoMgr.fTypeConfig( theTargetRoot)     
                if not unTargetRootTypeConfig:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_No_TypeConfig
                    return False
                                
                
                unRefactorStack = self.vRefactor.fGetContextParam( 'stack')  
                if not unRefactorStack:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_No_Stack
                    return False
                
                # ###################################
                """Unless partial copies area already prohibited (set in refactor context by caller): 
                Because the targets will be copied on instances of same type, the copies shall be complete, except for relations not multiple or whose max multiplicity is reached, or for links outside of same owner.
                
                """
                if self.vRefactor.vAllowPartialCopies:
                    self.vRefactor.vAllowPartialCopies = False
                    self.vRefactor.vIgnorePartialLinksForMultiplicityOrDifferentOwner = True
                    
                
                unTargetRootParent =  aq_parent( aq_inner( theTargetRoot))
                unosExistingRootSiblings = unTargetRootParent.objectValues()
                
                unosExistingRootSiblingsTitles = [ ]
                
                for anExistingRootSibling in unosExistingRootSiblings:                
                    unTitle = ''
                    try:
                        unTitle = anExistingRootSibling.Title()
                    except:
                        None
                    if unTitle:
                        unosExistingRootSiblingsTitles.append( unTitle)
                
                        
                        
                for unSourceRoot in theSourceRoots:
                
                    unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unSourceRoot)
                    if not unSourceType:
                        unErrorReason = cRefactorStatus_Error_NoSourceType
                        if not self.vRefactor.vAllowPartialCopies:
                            return False
                        else:
                            anErrorReport = { 
                                'theclass': self.__class__.__name__, 
                                'method': unMethodName, 
                                'status': unicode( unErrorReason),
                            }
                            self.vRefactor.pAppendErrorReport( anErrorReport)
                            
                    else:
                        
                        if ( not self.vRefactor.vAllowMappings) or ( unSourceType == unTargetRootType):
                            unMapping = []
                        else:
                            unMapping = self.vRefactor.vMapperMetaInfoMgr.fCompileMappingFromSourceTypeToMappedType( unSourceType, unTargetRootType, )
                        
                            
                        unMustReindexTarget = False

                        unSourceRootTitle = self.vRefactor.vSourceInfoMgr.fGetTitle( unSourceRoot)
                        
                        if not ( unTargetRootTitle == unSourceRootTitle):
                            unNewTargetRootTitle = self.vRefactor.vTargetInfoMgr.fUniqueStringWithCounter( unSourceRootTitle, unosExistingRootSiblingsTitles)
                            if unNewTargetRootTitle:
                                theTargetRoot.setTitle( unNewTargetRootTitle)
                                unMustReindexTarget = True
                        
                        #unSourceRootDescription = self.vRefactor.vSourceInfoMgr.fGetAttributeValue( unSourceRoot, 'description', 'text',)
                        #unTargetRootDescription = self.vRefactor.vSourceInfoMgr.fGetAttributeValue( unSourceRoot, 'description', 'text',)
                        
                        #if not ( unTargetRootDescription == unSourceRootDescription):
                            #theTargetRoot.setDescription( unTargetRootDescription)
                            #unMustReindexTarget = True
                         
                        if unMustReindexTarget:
                            theTargetRoot.reindexObject()
                            
                        unRegisterCorrespondenceResult = self.vRefactor.vMapperInfoMgr.fRegisterSourceToTargetCorrespondence( unSourceRoot, theTargetRoot, unMapping)
                        if not unRegisterCorrespondenceResult:
                            unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                            if not self.vRefactor.vAllowPartialCopies:
                                return False
                            else:
                                anErrorReport = { 
                                    'theclass': self.__class__.__name__, 
                                    'method': unMethodName, 
                                    'status': unicode( unErrorReason),
                                }
                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                
                            
                                
                        unEstablishTraceabilityLinksResult = self.vRefactor.vTraceabilityMgr.fEstablishTraceabilityLinks( unSourceRoot, theTargetRoot,)
                        if not unEstablishTraceabilityLinksResult:
                            unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                            if not self.vRefactor.vAllowPartialCopies:
                                return False
                            else:
                                anErrorReport = { 
                                    'theclass': self.__class__.__name__, 
                                    'method': unMethodName, 
                                    'status': unicode( unErrorReason),
                                }
                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                                               
                                
                
                        unRefactorFrame = unRefactorStack.fAddRootStackFrame( self, unSourceRoot, theTargetRoot, unTargetRootTypeConfig, unMapping)
                        if not unRefactorFrame:
                            unErrorReason = cRefactorStatus_Error_NoNewRootStackFrame
                            if not self.vRefactor.vAllowPartialCopies:
                                return False
                            else:
                                anErrorReport = { 
                                    'theclass': self.__class__.__name__, 
                                    'method': unMethodName, 
                                    'status': unicode( unErrorReason),
                                }
                                self.vRefactor.pAppendErrorReport( anErrorReport)
                        
                        else:
                            
                            #if unMustReindexTarget:
                                #unRefactorFrame.vMustReindexTarget = True
                                
                            try:
                                unRefactorFrameResult = self.fRefactor_Frame( unRefactorFrame)
                                
                                if not unRefactorFrameResult:
                                    unErrorReason = cRefactorStatus_Error_RefactoringFrame
                                    if not self.vRefactor.vAllowPartialCopies:
                                        return False
                                    else:
                                        anErrorReport = { 
                                            'theclass': self.__class__.__name__, 
                                            'method': unMethodName, 
                                            'status': unicode( unErrorReason),
                                        }
                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                    
                            finally:
                                unRefactorStack.fPopStackFrame()
                                      
                unCompleted = True
                
                
                return self

            except:
                unInException = True
                raise
        
        finally:
            
            if not unInException:
                if not unCompleted:
                    
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': unMethodName, 
                        'status': unicode( cRefactorStatus_Not_Completed),
                        'reason': unicode( unErrorReason),
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
    
                    
                
                
                
                
                
                
                
                
                
                
                
                
                
    def fRefactor_RootAggregations( self, theSourceRoots, theTargetRoot):
        
        unCompleted   = False
        unInException = False
        unErrorReason = u''
        unMethodName  = u'fRefactor_RootAggregations'
        unaTargetAggregationName = u''
        
        try:
            try:
                        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
            
                if not theSourceRoots:
                    unErrorReason = cRefactorStatus_Missing_Parameter_SourceRoots
                    return False
                
                if theTargetRoot == None:
                    unErrorReason = cRefactorStatus_Missing_Parameter_TargetRoot
                    return False
                                
                
                unTargetRootResult = self.vRefactor.vTargetInfoMgr.fGetTargetRootResult() 
                if not unTargetRootResult:
                    unErrorReason = cRefactorStatus_NoTargetResult
                    return False
                
                if not self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'traverse_permission'):
                    unErrorReason = cRefactorStatus_NoTraversePermission
                    return False
        
                unRefactorStack = self.vRefactor.fGetContextParam( 'stack')  
                if not unRefactorStack:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_No_Stack
                    return False
                
                unAnythingAdded = False
                
                for unSourceRoot in theSourceRoots:
                    if not self.vRefactor.vSourceInfoMgr.fIsSourceOk( unSourceRoot):
                        unErrorReason = cRefactorStatus_SourceRoot_Not_OK
                        if not self.vRefactor.vAllowPartialCopies:
                            return False
                        else:
                            anErrorReport = { 
                                'theclass': self.__class__.__name__, 
                                'method': unMethodName, 
                                'status': unicode( unErrorReason),
                            }
                            self.vRefactor.pAppendErrorReport( anErrorReport)
                            
                    else:    
                        
                        if not self.vRefactor.vSourceInfoMgr.fIsSourceReadable( unSourceRoot):
                            unErrorReason = cRefactorStatus_SourceRoot_Not_Readable
                            if not self.vRefactor.vAllowPartialCopies:
                                return False
                            else:
                                anErrorReport = { 
                                    'theclass': self.__class__.__name__, 
                                    'method': unMethodName, 
                                    'status': unicode( unErrorReason),
                                }
                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                
                                
                        else:
                             
                            unMappingTargetAggregationConfigAndType = self.vRefactor.vMapperMetaInfoMgr.fMappingAndTargetAggregationConfigAndTypeToAggregateSourceIn( unSourceRoot, theTargetRoot)
                            if not( unMappingTargetAggregationConfigAndType and len( unMappingTargetAggregationConfigAndType) > 2):
                                
                                unErrorReason = cRefactorStatus_Error_Paste_No_MappingTargetAggregationConfigAndType
                                if not self.vRefactor.vAllowPartialCopies:
                                    return False
                                else:
                                    anErrorReport = { 
                                        'theclass': self.__class__.__name__, 
                                        'method': unMethodName, 
                                        'status': unicode( unErrorReason),
                                    }
                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                    
                            else:

                                unMapping                  = unMappingTargetAggregationConfigAndType[ 0]
                                unaTargetAggregationConfig = unMappingTargetAggregationConfigAndType[ 1]
                                unTypeToCreate             = unMappingTargetAggregationConfigAndType[ 2]
                                
                                if not( unaTargetAggregationConfig and unTypeToCreate):
                                    unErrorReason = cRefactorStatus_Error_Paste_No_TargetAggregationConfigAndTypeToCreate
                                    if not self.vRefactor.vAllowPartialCopies:
                                        return False
                                    else:
                                        anErrorReport = { 
                                            'theclass': self.__class__.__name__, 
                                            'method': unMethodName, 
                                            'status': unicode( unErrorReason),
                                        }
                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                    
                                else:    
                                    unContainsCollections = self.vRefactor.vTargetMetaInfoMgr.fGetAggregationConfigContainsCollections( unaTargetAggregationConfig)
                                            
        
                                    if unContainsCollections:
                                        
                                        unaCollectionToMergeWith, aOverrideTitle, aOverrideId = self.vRefactor.vTargetInfoMgr.fCollectionToMergeWith( theTargetRoot, unTypeToCreate, unSourceRoot)
                                        
                                        if unaCollectionToMergeWith:
                                            
                                            unMustReindexTargetCollection = False

                                            if aOverrideId:
                                                unSourceRootId = self.vRefactor.vSourceInfoMgr.fGetId( unSourceRoot)
                                                unaCollectionToMergeWith.setId( unSourceRootId)
                                                                
                                            if aOverrideTitle:
                                                unSourceRootTitle = self.vRefactor.vSourceInfoMgr.fGetTitle( unSourceRoot)
                                                
                                                unNewTargetTitle = self.vRefactor.vTargetInfoMgr.fUniqueAggregatedTitle( theTargetRoot, unSourceRootTitle)
                                                if unNewTargetTitle:
                                                    unaCollectionToMergeWith.setTitle( unNewTargetTitle)
                                                    unMustReindexTargetCollection = True

                                                    
                                            #unSourceCollectionDescription = self.vRefactor.vSourceInfoMgr.fGetAttributeValue( unSourceRoot, 'description', 'text',)
                                            #unTargetCollectionDescription = self.vRefactor.vSourceInfoMgr.fGetAttributeValue( unaCollectionToMergeWith, 'description', 'text',)
                                            
                                            #if not ( unTargetCollectionDescription == unSourceCollectionDescription):
                                                #unaCollectionToMergeWith.setDescription( unSourceCollectionDescription)
                                                #unMustReindexTargetCollection = True
                                                    
                                            if unMustReindexTargetCollection:
                                                unaCollectionToMergeWith.reindexObject()
                                                
                                                    
                                            unaCollectionType       = self.vRefactor.vTargetMetaInfoMgr.fTypeName( unaCollectionToMergeWith)
                                            unaCollectionTypeConfig = self.vRefactor.vTargetMetaInfoMgr.fTypeConfigForType( unaCollectionType)
                                            
                                             
                                            unRegisterCorrespondenceResult = self.vRefactor.vMapperInfoMgr.fRegisterSourceToTargetCorrespondence( unSourceRoot, unaCollectionToMergeWith, unMapping)
                                            if not unRegisterCorrespondenceResult:
                                                unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                                                if not self.vRefactor.vAllowPartialCopies:
                                                    return False
                                                else:
                                                    anErrorReport = { 
                                                        'theclass': self.__class__.__name__, 
                                                        'method': unMethodName, 
                                                        'status': unicode( unErrorReason),
                                                    }
                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                    
                                            else:    
                                                    
                                                unEstablishTraceabilityLinksResult = self.vRefactor.vTraceabilityMgr.fEstablishTraceabilityLinks( unSourceRoot, unaCollectionToMergeWith,)
                                                if not unEstablishTraceabilityLinksResult:
                                                    unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                                                    if not self.vRefactor.vAllowPartialCopies:
                                                        return False
                                                    else:
                                                        anErrorReport = { 
                                                            'theclass': self.__class__.__name__, 
                                                            'method': unMethodName, 
                                                            'status': unicode( unErrorReason),
                                                        }
                                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                                        
                                                else:
                                            
                                                    unRefactorFrame = unRefactorStack.fAddRootStackFrame( self, unSourceRoot, unaCollectionToMergeWith, unaCollectionTypeConfig, unMapping)
                                                    if not unRefactorFrame:
                                                        unErrorReason = cRefactorStatus_Error_NoNewRootStackFrame
                                                        if not self.vRefactor.vAllowPartialCopies:
                                                            return False
                                                        else:
                                                            anErrorReport = { 
                                                                'theclass': self.__class__.__name__, 
                                                                'method': unMethodName, 
                                                                'status': unicode( unErrorReason),
                                                            }
                                                            self.vRefactor.pAppendErrorReport( anErrorReport)
                                                    
                                                    else:
                                                        try:
                                                            unRefactorFrameResult = self.fRefactor_Frame( unRefactorFrame)
                                                            if not unRefactorFrameResult:
                                                                unErrorReason = cRefactorStatus_Error_RefactoringFrame
                                                                if not self.vRefactor.vAllowPartialCopies:
                                                                    return False
                                                                else:
                                                                    anErrorReport = { 
                                                                        'theclass': self.__class__.__name__, 
                                                                        'method': unMethodName, 
                                                                        'status': unicode( unErrorReason),
                                                                    }
                                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                        finally:
                                                            unRefactorStack.fPopStackFrame()
                                            continue

                                    
                                    unAddingPermitted = False
                                    if unContainsCollections:
                                        
                                        if self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'add_collection_permission'):
                                            unAddingPermitted = True
                                    else:
                                        if self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'add_permission'):
                                            unAddingPermitted = True
                                            
                                    if not unAddingPermitted:
                                        
                                        unErrorReason = cRefactorStatus_Error_AddingNotPermitted
                                        if not self.vRefactor.vAllowPartialCopies:
                                            return False
                                        else:
                                            anErrorReport = { 
                                                'theclass': self.__class__.__name__, 
                                                'method': unMethodName, 
                                                'status': unicode( unErrorReason),
                                            }
                                            self.vRefactor.pAppendErrorReport( anErrorReport)
                                        
                                    else:   
                                        
                                        unaTargetAggregationName = self.vRefactor.vTargetMetaInfoMgr.fAggregationNameFromTraversalConfig( unaTargetAggregationConfig)
                                        if not unaTargetAggregationName:
                                            unErrorReason = cRefactorStatus_Error_NoAggregationName
                                            if not self.vRefactor.vAllowPartialCopies:
                                                return False
                                            else:
                                                anErrorReport = { 
                                                    'theclass': self.__class__.__name__, 
                                                    'method': unMethodName, 
                                                    'status': unicode( unErrorReason),
                                                }
                                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                            
                                        else:   
                                            
                                            unRootAggregationResult  = self.vRefactor.vTargetInfoMgr.fTraversalResultNamed( unTargetRootResult, unaTargetAggregationName)
                                            if not unRootAggregationResult:
                                                unErrorReason = cRefactorStatus_Error_NoAggregationResult
                                                if not self.vRefactor.vAllowPartialCopies:
                                                    return False
                                                else:
                                                    anErrorReport = { 
                                                        'theclass': self.__class__.__name__, 
                                                        'method': unMethodName, 
                                                        'status': unicode( unErrorReason),
                                                        'reason': unicode( unaTargetAggregationName),
                                                    }
                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                
                                            else:   
                                                
                                                if not( self.vRefactor.vTargetInfoMgr.fGetPermissionFromTraversalResult( unRootAggregationResult, 'read_permission') and \
                                                   self.vRefactor.vTargetInfoMgr.fGetPermissionFromTraversalResult( unRootAggregationResult, 'write_permission')):
                                                    unErrorReason = cRefactorStatus_Error_AggregationNotReadableOrWritable
                                                    if not self.vRefactor.vAllowPartialCopies:
                                                        return False
                                                    else:
                                                        anErrorReport = { 
                                                            'theclass': self.__class__.__name__, 
                                                            'method': unMethodName, 
                                                            'status': unicode( unErrorReason),
                                                            'reason': unicode( unaTargetAggregationName),
                                                        }
                                                        self.vRefactor.pAppendErrorReport( anErrorReport)

                                                else:   
                                                    
                                                    unCreatedElement = self.vRefactor.vTargetInfoMgr.fCreateAggregatedElement( unSourceRoot, theTargetRoot, unTypeToCreate, )
                                                    if ( unCreatedElement == None):
                                                        unErrorReason = cRefactorStatus_AggregatedElement_NotCreated
                                                        if not self.vRefactor.vAllowPartialCopies:
                                                            return False
                                                        else:
                                                            anErrorReport = { 
                                                                'theclass': self.__class__.__name__, 
                                                                'method': unMethodName, 
                                                                'status': unicode( unErrorReason),
                                                                'reason': unicode( unaTargetAggregationName),
                                                            }
                                                            self.vRefactor.pAppendErrorReport( anErrorReport)
                                                    else:
                                                        
                                                        
                                                        unAnythingAdded = True
        
                                                        unRegisterCorrespondenceResult = self.vRefactor.vMapperInfoMgr.fRegisterSourceToTargetCorrespondence( unSourceRoot, unCreatedElement, unMapping)
                                                        if not unRegisterCorrespondenceResult:
                                                            unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                                                            if not self.vRefactor.vAllowPartialCopies:
                                                                return False
                                                            else:
                                                                anErrorReport = { 
                                                                    'theclass': self.__class__.__name__, 
                                                                    'method': unMethodName, 
                                                                    'status': unicode( unErrorReason),
                                                                    'reason': unicode( unaTargetAggregationName),
                                                                }
                                                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                        else:    

                                                            unCreatedElementTypeConfig = self.vRefactor.vTargetMetaInfoMgr.fTypeConfigForType( unTypeToCreate)
                                                            if not unCreatedElementTypeConfig:
                                                                unErrorReason = cRefactorStatus_Error_Paste_Internal_No_TypeConfig
                                                                if not self.vRefactor.vAllowPartialCopies:
                                                                    return False
                                                                else:
                                                                    anErrorReport = { 
                                                                        'theclass': self.__class__.__name__, 
                                                                        'method': unMethodName, 
                                                                        'status': unicode( unErrorReason),
                                                                        'reason': unicode( unaTargetAggregationName),
                                                                    }
                                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                            else:
                                                                unRefactorFrame = unRefactorStack.fAddRootStackFrame( self, unSourceRoot, unCreatedElement, unCreatedElementTypeConfig, unMapping)
                                                                if not unRefactorFrame:
                                                                    unErrorReason = cRefactorStatus_Error_NoNewRootStackFrame
                                                                    if not self.vRefactor.vAllowPartialCopies:
                                                                        return False
                                                                    else:
                                                                        anErrorReport = { 
                                                                            'theclass': self.__class__.__name__, 
                                                                            'method': unMethodName, 
                                                                            'status': unicode( unErrorReason),
                                                                            'reason': unicode( unaTargetAggregationName),
                                                                        }
                                                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                                else:
                                                                    try:
                                                                        unRefactorFrameResult = self.fRefactor_Frame( unRefactorFrame)
                                                                        if not unRefactorFrameResult:
                                                                            unErrorReason = cRefactorStatus_Error_RefactoringFrame
                                                                            if not self.vRefactor.vAllowPartialCopies:
                                                                                return False
                                                                            else:
                                                                                anErrorReport = { 
                                                                                    'theclass': self.__class__.__name__, 
                                                                                    'method': unMethodName, 
                                                                                    'status': unicode( unErrorReason),
                                                                                    'reason': unicode( unaTargetAggregationName),
                                                                                }
                                                                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                            
                                                                    finally:
                                                                        unRefactorStack.fPopStackFrame()
                                                                    
                                                                
                if unAnythingAdded:
                    self.vRefactor.vModelDDvlPloneTool_Mutators.pSetAudit_Modification( theTargetRoot)
                    
                unCompleted = True
                
                
                return True

            except:
                unInException = True
                raise
        
        finally:
            
            if not unInException:
                if not unCompleted:
                    
                    if unaTargetAggregationName:
                        unErrorReason = '%s; aggregation %s' % ( unErrorReason, unaTargetAggregationName,)
                        
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': unMethodName, 
                        'status': unicode( cRefactorStatus_Not_Completed),
                        'reason': unicode( unErrorReason),
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
    
                    
                    
                    
                    
                
                
                
                    
                    
    def fRefactor_Frame( self, theRefactorFrame):
        
        unCompleted   = False
        unInException = False
        unErrorReason = ''
        unMethodName  = u'fRefactor_Frame'
        
        try:
            try:
                        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
            
                if not theRefactorFrame:
                    unErrorReason = cRefactorStatus_Missing_Parameter_RefactorFrame
                    return False
                
                if  not theRefactorFrame.fIsFrameOk():
                    unErrorReason = cRefactorStatus_Error_BadStackFrame
                    return False
          
                unPopulateAttributesResult = self.vRefactor.vTargetInfoMgr.fPopulateElementAttributes( theRefactorFrame.vSource, theRefactorFrame.vTarget, theRefactorFrame.vTargetTypeConfig, theRefactorFrame.vMapping, theRefactorFrame.vMustReindexTarget)
                
                if unPopulateAttributesResult:
                    transaction.savepoint( optimistic=True)
                else:
                    unErrorReason = cRefactorStatus_Error_PopulateAttributes_Not_Completed
                    if not self.vRefactor.vAllowPartialCopies:
                        return False
                    else:
                        anErrorReport = { 
                            'theclass': self.__class__.__name__, 
                            'method': unMethodName, 
                            'status': unicode( unErrorReason),
                        }
                        self.vRefactor.pAppendErrorReport( anErrorReport)
                    
                        
                unRefactorFrameAggregationsResult = self.fRefactor_Frame_Aggregations( theRefactorFrame)
                
                if unRefactorFrameAggregationsResult:
                    transaction.savepoint( optimistic=True)
                else:
                    unErrorReason = cRefactorStatus_Error_RefactorFrameAggregations_Not_Completed
                    if not self.vRefactor.vAllowPartialCopies:
                        return False
                    else:
                        anErrorReport = { 
                            'theclass': self.__class__.__name__, 
                            'method': unMethodName, 
                            'status': unicode( unErrorReason),
                        }
                        self.vRefactor.pAppendErrorReport( anErrorReport)
        
                        
                #self.fRefactor_Frame_PloneContent( theRefactorFrame)
        
                unCompleted = True
                return True

            except:
                unInException = True
                raise
        
        finally:
            
            if not unInException:
                if not unCompleted:
                    
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': unMethodName, 
                        'status': unicode( cRefactorStatus_Not_Completed),
                        'reason': unicode( unErrorReason),
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
    
                   
    
    
    
    
    
    def fRefactor_Frame_Aggregations( self, theRefactorFrame):
        
        unCompleted   = False
        unInException = False
        unErrorReason = u''
        unMethodName  = u'fRefactor_Frame_Aggregations'
        unAggregationName = u''
        
        try:
            try:
                        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
        
                if not theRefactorFrame:
                    unErrorReason = cRefactorStatus_Missing_Parameter_RefactorFrame
                    return False
                
                if  not theRefactorFrame.fIsFrameOk():
                    unErrorReason = cRefactorStatus_Error_BadStackFrame
                    return False
        
                unRefactorStack = self.vRefactor.fGetContextParam( 'stack')  
                if not unRefactorStack:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_No_Stack
                    return False
        
                someAggregationTraversalConfigs = self.vRefactor.vTargetMetaInfoMgr.fAggregationTraversalConfigsFromTypeConfig( theRefactorFrame.vTargetTypeConfig)
                if not someAggregationTraversalConfigs:
                    unCompleted = True
                    return True
                
        
                unAnythingAdded = False
                                                    
                for anAggregationTraversalConfig in someAggregationTraversalConfigs:
                    
                    unAggregationName = self.vRefactor.vTargetMetaInfoMgr.fAggregationNameFromTraversalConfig( anAggregationTraversalConfig)
                    if not unAggregationName:
                        unErrorReason = cRefactorStatus_Error_NoAggregationName
                        if not self.vRefactor.vAllowPartialCopies:
                            return False
                        else:
                            anErrorReport = { 
                                'theclass': self.__class__.__name__, 
                                'method': unMethodName, 
                                'status': unicode( unErrorReason),
                            }
                            self.vRefactor.pAppendErrorReport( anErrorReport)
                        
                    else:   
           
                        someAggregatedTypes = self.vRefactor.vTargetMetaInfoMgr.fAggregatedTypesFromTraversalConfig( anAggregationTraversalConfig)
                        if someAggregatedTypes:
        
                            unSourceTraversalNameToRetrieve = self.vRefactor.vMapperMetaInfoMgr.fMappedTraversalNameFromSourceForTargetAggregationName( theRefactorFrame.vSource, unAggregationName, theRefactorFrame.vMapping)
                            if not unSourceTraversalNameToRetrieve:
                                
                                if theRefactorFrame.vMapping:
                                    continue
                                
                                unErrorReason = cRefactorStatus_Error_NoSourceTraversalNameToRetrieve
                                if not self.vRefactor.vAllowPartialCopies:
                                    return False
                                else:
                                    anErrorReport = { 
                                        'theclass': self.__class__.__name__, 
                                        'method': unMethodName, 
                                        'status': unicode( unErrorReason),
                                        'reason': unicode( unAggregationName),
                                    }
                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                
                            else:   
                                
        
                                unosAggregatedSources = self.vRefactor.vSourceInfoMgr.fGetTraversalValues( theRefactorFrame.vSource, unSourceTraversalNameToRetrieve, [])
                                if unosAggregatedSources:
                                    
                                    for unAggregatedSource in unosAggregatedSources:
                                        
                                        if not self.vRefactor.vSourceInfoMgr.fIsSourceOk( unAggregatedSource):
                                            unErrorReason = cRefactorStatus_AggregatedSource_Not_OK
                                            if not self.vRefactor.vAllowPartialCopies:
                                                return False
                                            else:
                                                anErrorReport = { 
                                                    'theclass': self.__class__.__name__, 
                                                    'method': unMethodName, 
                                                    'status': unicode( unErrorReason),
                                                    'reason': unicode( unAggregationName),
                                                }
                                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                        else:    
                                                                                    
                                            unMappingAndType = self.vRefactor.vMapperMetaInfoMgr.fMappingAndTargetTypeFromSourceAndAllowedTypes( unAggregatedSource, someAggregatedTypes)
                                            if not unMappingAndType:
                                                unErrorReason = cRefactorStatus_Error_Paste_No_MappingAndTypeToCreate
                                                if not self.vRefactor.vAllowPartialCopies:
                                                    return False
                                                else:
                                                    anErrorReport = { 
                                                        'theclass': self.__class__.__name__, 
                                                        'method': unMethodName, 
                                                        'status': unicode( unErrorReason),
                                                        'reason': unicode( unAggregationName),
                                                    }
                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                            else:
                                                
                                                unMapping      = unMappingAndType[ 0]
                                                unTypeToCreate = unMappingAndType[ 1]
                                                
                                                if not unTypeToCreate:
                                                    
                                                    if not unMapping:
                                                        continue
                                                    
                                                    
                                                    unErrorReason = cRefactorStatus_NoTypeToCreate
                                                    if not self.vRefactor.vAllowPartialCopies:
                                                        return False
                                                    else:
                                                        anErrorReport = { 
                                                            'theclass': self.__class__.__name__, 
                                                            'method': unMethodName, 
                                                            'status': unicode( unErrorReason),
                                                            'reason': unicode( unAggregationName),
                                                        }
                                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                                else:    
                                                
                                                    unContainsCollections = self.vRefactor.vTargetMetaInfoMgr.fGetAggregationConfigContainsCollections( anAggregationTraversalConfig)
        
                                                    if unContainsCollections:
                                                        
                                                        unaCollectionToMergeWith, aOverrideTitle, aOverrideId = self.vRefactor.vTargetInfoMgr.fCollectionToMergeWith( theRefactorFrame.vTarget, unTypeToCreate, unAggregatedSource)
                                                        
                                                        if unaCollectionToMergeWith:
                                                            
                                                            unMustReindexTargetCollection = False                                                            
                                                            
                                                            if aOverrideId:
                                                                unAggregatedSourceId = self.vRefactor.vSourceInfoMgr.fGetId( unAggregatedSource)
                                                                unaCollectionToMergeWith.setId( unAggregatedSourceId)

                                                            if aOverrideTitle:
                                                                unAggregatedSourceTitle = self.vRefactor.vSourceInfoMgr.fGetTitle( unAggregatedSource)
                                                                
                                                                unNewTargetTitle = self.vRefactor.vTargetInfoMgr.fUniqueAggregatedTitle( theRefactorFrame.vTarget, unAggregatedSourceTitle)
                                                                if unNewTargetTitle:
                                                                    unaCollectionToMergeWith.setTitle( unNewTargetTitle)
                                                                    unMustReindexTargetCollection = True
                                            
                                                            #unSourceCollectionDescription = self.vRefactor.vSourceInfoMgr.fGetAttributeValue( unAggregatedSource,       'description', 'text',)
                                                            #unTargetCollectionDescription = self.vRefactor.vSourceInfoMgr.fGetAttributeValue( unaCollectionToMergeWith, 'description', 'text',)
                                                            
                                                            #if not ( unTargetCollectionDescription == unSourceCollectionDescription):
                                                                #unaCollectionToMergeWith.setDescription( unSourceCollectionDescription)
                                                                #unMustReindexTargetCollection = True
        
                                                            if unMustReindexTargetCollection:
                                                                unaCollectionToMergeWith.reindexObject()
                                                                                      
                                            
                                                            unaCollectionType       = self.vRefactor.vTargetMetaInfoMgr.fTypeName( unaCollectionToMergeWith)
                                                            unaCollectionTypeConfig = self.vRefactor.vTargetMetaInfoMgr.fTypeConfigForType( unaCollectionType)
                                                            
                                                            unRegisterCorrespondenceResult = self.vRefactor.vMapperInfoMgr.fRegisterSourceToTargetCorrespondence( unAggregatedSource, unaCollectionToMergeWith, unMapping)
                                                            if not unRegisterCorrespondenceResult:
                                                                unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                                                                if not self.vRefactor.vAllowPartialCopies:
                                                                    return False
                                                                else:
                                                                    anErrorReport = { 
                                                                        'theclass': self.__class__.__name__, 
                                                                        'method': unMethodName, 
                                                                        'status': unicode( unErrorReason),
                                                                        'reason': unicode( unAggregationName),
                                                                    }
                                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                    
                                                            else:    
                                                            
                                                                unEstablishTraceabilityLinksResult = self.vRefactor.vTraceabilityMgr.fEstablishTraceabilityLinks( unAggregatedSource, unaCollectionToMergeWith,)
                                                                if not unEstablishTraceabilityLinksResult:
                                                                    unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                                                                    if not self.vRefactor.vAllowPartialCopies:
                                                                        return False
                                                                    else:
                                                                        anErrorReport = { 
                                                                            'theclass': self.__class__.__name__, 
                                                                            'method': unMethodName, 
                                                                            'status': unicode( unErrorReason),
                                                                            'reason': unicode( unAggregationName),
                                                                        }
                                                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                                else:
                                                                
                                                                    unRefactorFrame = unRefactorStack.fPushStackFrame( self, unAggregatedSource, unaCollectionToMergeWith, unaCollectionTypeConfig, unMapping)
                                                                    if not unRefactorFrame:
                                                                        unErrorReason = cRefactorStatus_Error_NoNewStackFrame
                                                                        if not self.vRefactor.vAllowPartialCopies:
                                                                            return False
                                                                        else:
                                                                            anErrorReport = { 
                                                                                'theclass': self.__class__.__name__, 
                                                                                'method': unMethodName, 
                                                                                'status': unicode( unErrorReason),
                                                                                'reason': unicode( unAggregationName),
                                                                            }
                                                                            self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                    
                                                                    else:
                                                                        try:
                                                                            unRefactorFrameResult = self.fRefactor_Frame( unRefactorFrame)
                                                                            if not unRefactorFrameResult:
                                                                                unErrorReason = cRefactorStatus_Error_RefactoringFrame
                                                                                if not self.vRefactor.vAllowPartialCopies:
                                                                                    return False
                                                                                else:
                                                                                    anErrorReport = { 
                                                                                        'theclass': self.__class__.__name__, 
                                                                                        'method': unMethodName, 
                                                                                        'status': unicode( unErrorReason),
                                                                                        'reason': unicode( unAggregationName),
                                                                                    }
                                                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                                
                                                                        finally:
                                                                            unRefactorStack.fPopStackFrame()
                                                                             
                                                                        continue
                                                            
                                                            
                                                    unCreatedElementTypeConfig = self.vRefactor.vTargetMetaInfoMgr.fTypeConfigForTypeFromAggregationTraversalConfig( unTypeToCreate, anAggregationTraversalConfig, )
                                                    if not unCreatedElementTypeConfig:
                                                        unErrorReason = cRefactorStatus_Error_Paste_Internal_No_TypeConfig
                                                        if not self.vRefactor.vAllowPartialCopies:
                                                            return False
                                                        else:
                                                            anErrorReport = { 
                                                                'theclass': self.__class__.__name__, 
                                                                'method': unMethodName, 
                                                                'status': unicode( unErrorReason),
                                                                'reason': unicode( unAggregationName),
                                                            }
                                                            self.vRefactor.pAppendErrorReport( anErrorReport)
                                                        
                                                    else:
                                                        
                                                        unCreatedAggregatedElement = self.vRefactor.vTargetInfoMgr.fCreateAggregatedElement( unAggregatedSource, theRefactorFrame.vTarget, unTypeToCreate, )
                                                        if ( unCreatedAggregatedElement == None):
                                                            unErrorReason = cRefactorStatus_AggregatedElement_NotCreated
                                                            if not self.vRefactor.vAllowPartialCopies:
                                                                return False
                                                            else:
                                                                anErrorReport = { 
                                                                    'theclass': self.__class__.__name__, 
                                                                    'method': unMethodName, 
                                                                    'status': unicode( unErrorReason),
                                                                    'reason': unicode( unAggregationName),
                                                                }
                                                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                                        else:
                                                            
                                                            unAnythingAdded = True

                                                            transaction.savepoint( optimistic=True)
        
                                                            unRegisterCorrespondenceResult = self.vRefactor.vMapperInfoMgr.fRegisterSourceToTargetCorrespondence( unAggregatedSource, unCreatedAggregatedElement, unMapping)
                                                            if not unRegisterCorrespondenceResult:
                                                                unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                                                                if not self.vRefactor.vAllowPartialCopies:
                                                                    return False
                                                                else:
                                                                    anErrorReport = { 
                                                                        'theclass': self.__class__.__name__, 
                                                                        'method': unMethodName, 
                                                                        'status': unicode( unErrorReason),
                                                                        'reason': unicode( unAggregationName),
                                                                    }
                                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                    
                                                            else:    
                                                                               
                                                                
                                                                unEstablishTraceabilityLinksResult = self.vRefactor.vTraceabilityMgr.fEstablishTraceabilityLinks( unAggregatedSource, unCreatedAggregatedElement,)
                                                                if not unEstablishTraceabilityLinksResult:
                                                                    unErrorReason = cRefactorStatus_Error_TraceabilityLinksNotSet
                                                                    if not self.vRefactor.vAllowPartialCopies:
                                                                        return False
                                                                    else:
                                                                        anErrorReport = { 
                                                                            'theclass': self.__class__.__name__, 
                                                                            'method': unMethodName, 
                                                                            'status': unicode( unErrorReason),
                                                                            'reason': unicode( unAggregationName),
                                                                        }
                                                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                                else:
                                                                                                                                    
                                                                    unSubRefactorFrame = unRefactorStack.fPushStackFrame( self, unAggregatedSource, unCreatedAggregatedElement, unCreatedElementTypeConfig, unMapping)
                                                                    if not unSubRefactorFrame:
                                                                        unErrorReason = cRefactorStatus_Error_NoNewStackFrame
                                                                        if not self.vRefactor.vAllowPartialCopies:
                                                                            return False
                                                                        else:
                                                                            anErrorReport = { 
                                                                                'theclass': self.__class__.__name__, 
                                                                                'method': unMethodName, 
                                                                                'status': unicode( unErrorReason),
                                                                                'reason': unicode( unAggregationName),
                                                                            }
                                                                            self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                    
                                                                    else:
                                                                        try:
                                                                            unSubRefactorFrameResult = self.fRefactor_Frame( unSubRefactorFrame)
                                                                            if not unSubRefactorFrameResult:
                                                                                unErrorReason = cRefactorStatus_Error_RefactoringFrame
                                                                                if not self.vRefactor.vAllowPartialCopies:
                                                                                    return False
                                                                                else:
                                                                                    anErrorReport = { 
                                                                                        'theclass': self.__class__.__name__, 
                                                                                        'method': unMethodName, 
                                                                                        'status': unicode( unErrorReason),
                                                                                        'reason': unicode( unAggregationName),
                                                                                    }
                                                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                                
                                                                        finally:
                                                                            unRefactorStack.fPopStackFrame()
                                                                        
                                                
                if unAnythingAdded:
                    self.vRefactor.vModelDDvlPloneTool_Mutators.pSetAudit_Modification( theRefactorFrame.vTarget)
                        
                unCompleted = True
                return True

            except:
                unInException = True
                raise
        
        finally:
            
            if not unInException:
                if not unCompleted:
                    
                    if unAggregationName:
                        unErrorReason = '%s; aggregation %s' % ( unErrorReason, unAggregationName,)
                        
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': unMethodName, 
                        'status': unicode( cRefactorStatus_Not_Completed),
                        'reason': unicode( unErrorReason),
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
    
                   
        
    
    
    
    
                        
    def fRefactor_Moves( self, ):
        """Delete source objects that have been copied and have the same root path as the target.
        If target root is same as source root or is under source root, then move is not possible (removing the source would remove the copies, too, loosing information).
        if source root is under target root, then move is possible.
        If there is no parent-child relationship between elements, then move is possible.
        
        """
        
        unCompleted   = False
        unInException = False
        unErrorReason = ''
        unMethodName  = u'fRefactor_Moves'
        
        try:
            try:
                        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                unIsMoveOperation =  self.vRefactor.fGetContextParam( 'is_move_operation')
                if not unIsMoveOperation:
                    unCompleted = True
                    return True
                
                unTargetRoot = self.vRefactor.vTargetInfoMgr.fGetTargetRoot()
                if ( unTargetRoot == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_TargetRoot
                    return False
        
                unTargetRootPath = self.vRefactor.vTargetInfoMgr.fRootPath( unTargetRoot)
                        
                unosTargets = self.vRefactor.vMapperInfoMgr.fGetTargets()
                if not unosTargets:
                    unCompleted = True
                    return True
                
                for unTarget in unosTargets:
                    
                    unosSources = self.vRefactor.vMapperInfoMgr.fGetSourcesForTarget( unTarget)
                    
                    for unSource in unosSources:
                        
                        if not unSource in unosTargets:
                            
                            unSourcePath = self.vRefactor.vSourceInfoMgr.fGetPath( unSource)
                            
                            if not self.fPathIsSameOrParentPathOf( unSourcePath, unTargetRootPath):
                                
                                self.vRefactor.vSourceInfoMgr.fDeleteSource( unSource)
                            
                         
                unCompleted = True
                return True

            except:
                unInException = True
                raise
        
        finally:
            
            if not unInException:
                if not unCompleted:
                    
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': unMethodName, 
                        'status': unicode( cRefactorStatus_Not_Completed),
                        'reason': unicode( unErrorReason),
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
    
                       
    
    
        
    
    def fPathIsSameOrParentPathOf( self, theParentPath, theChildPath):
        if theParentPath == theChildPath:
            return True
        
        unosParentPathSteps = theParentPath.split( '/')
        unosChildPathSteps = theChildPath.split( '/')
        
        unNumParentPathSteps = len( unosParentPathSteps)
        
        if unNumParentPathSteps > len( unosChildPathSteps):
            return False
        
        for unPathIndex in range( unNumParentPathSteps):
            
            unParentStep = unosParentPathSteps[ unPathIndex]
            unChildStep  = unosChildPathSteps[ unPathIndex]
        
            if not ( unParentStep == unChildStep):
                return False
            
        return True
    
    
    
    
    

    
                        
    def fRefactor_Relations( self, ):
        """
        
        """
        unCompleted   = False
        unInException = False
        unErrorReason = ''
        unMethodName  = u'fRefactor_Relations'
        
        try:
            try:
                        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                 
                unTargetRoot = self.vRefactor.vTargetInfoMgr.fGetTargetRoot()
                if ( unTargetRoot == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_TargetRoot
                    return False
        
        
                unTargetRootPath = self.vRefactor.vTargetInfoMgr.fRootPath( unTargetRoot)
                
                unosTargets = self.vRefactor.vMapperInfoMgr.fGetTargets()
                if not unosTargets:
                    unCompleted = True
                    return True
                
                unIsMoveOperation = self.vRefactor.fGetContextParam( 'is_move_operation')
                
                for unTarget in unosTargets:
                    
                    unTargetLinked = False
                    
                    unMapping = self.vRefactor.vMapperInfoMgr.fGetMappingForTarget( unTarget)
                    
                    unasTargetRelationTraversalConfigs = self.vRefactor.vTargetMetaInfoMgr.fRelationTraversalConfigsFromTarget( unTarget)
                    if unasTargetRelationTraversalConfigs:
                
                        unosSources = self.vRefactor.vMapperInfoMgr.fGetSourcesForTarget( unTarget)
                        
                        for unaTargetRelationTraversalConfig in unasTargetRelationTraversalConfigs:
                            
                            if not unIsMoveOperation:
                                unDoNotCopy = self.vRefactor.vTargetMetaInfoMgr.fGetDoNotCopyFromTraversalConfig( unaTargetRelationTraversalConfig)
                                if unDoNotCopy:
                                    continue
                                
                            
                            unRelationFieldName = self.vRefactor.vTargetMetaInfoMgr.fRelationNameFromTraversalConfig( unaTargetRelationTraversalConfig)
                            if not unRelationFieldName:
                                unErrorReason = cRefactorStatus_Field_NoRelationFieldName
                                if not self.vRefactor.vAllowPartialCopies:
                                    return False
                                else:
                                    anErrorReport = { 
                                        'theclass': self.__class__.__name__, 
                                        'method': unMethodName, 
                                        'status': unicode( unErrorReason),
                                    }
                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                
                            else:
                                
                                unTargetOwnerPath = ''
                                unRelationCandidatesScope = self.vRefactor.vTargetMetaInfoMgr.fCandidatesScopeFromRelationTraversalConfig( unaTargetRelationTraversalConfig)
                                if unRelationCandidatesScope.lower() == 'owner':
                                    unTargetOwnerPath = self.vRefactor.vTargetInfoMgr.fOwnerPath( unTarget)
                                    
        
                                someRelatedTypes = self.vRefactor.vTargetMetaInfoMgr.fRelatedTypesFromTraversalConfig( unaTargetRelationTraversalConfig)
                                if someRelatedTypes:
                                
                                    allRelatedSources    = [ ]
                                    allRelatedSourceUIDs = set()
                                    
                                    for unSource in unosSources:
                                        if not self.vRefactor.vSourceInfoMgr.fIsSourceOk( unSource):
                                            unErrorReason = cRefactorStatus_AggregatedSource_Not_OK
                                            if not self.vRefactor.vAllowPartialCopies:
                                                return False
                                            else:
                                                anErrorReport = { 
                                                    'theclass': self.__class__.__name__, 
                                                    'method': unMethodName, 
                                                    'status': unicode( unErrorReason),
                                                }
                                                self.vRefactor.pAppendErrorReport( anErrorReport)
                                        else:    
                                            
                                            unSourceTraversalNameToRetrieve = self.vRefactor.vMapperMetaInfoMgr.fMappedTraversalNameFromSourceForTargetRelationName( unSource, unRelationFieldName, unMapping)
                                            if not unSourceTraversalNameToRetrieve:
                                                
                                                if unMapping:
                                                    continue
                                                
                                                unErrorReason = cRefactorStatus_Error_NoSourceTraversalNameToRetrieve
                                                if not self.vRefactor.vAllowPartialCopies:
                                                    return False
                                                else:
                                                    anErrorReport = { 
                                                        'theclass': self.__class__.__name__, 
                                                        'method': unMethodName, 
                                                        'status': '%s relationFieldName=%s source=%s' % ( unicode( unErrorReason), unicode( unRelationFieldName), self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg( unSource)),
                                                    }
                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                
                                            else:   
                                            
                                                    unosRelatedSources = self.vRefactor.vSourceInfoMgr.fGetTraversalValues( unSource, unSourceTraversalNameToRetrieve, [])
                                                    if unosRelatedSources:
                                                        for unRelatedSource in unosRelatedSources:
                                                            if not self.vRefactor.vSourceInfoMgr.fIsSourceOk( unRelatedSource):
                                                                unErrorReason = cRefactorStatus_RelatedSource_Not_OK
                                                                if not self.vRefactor.vAllowPartialCopies:
                                                                    return False
                                                                else:
                                                                    anErrorReport = { 
                                                                        'theclass': self.__class__.__name__, 
                                                                        'method': unMethodName, 
                                                                        'status': '%s traversalName=%s source=%s' % ( unicode( unErrorReason), unicode( unSourceTraversalNameToRetrieve), self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg( unSource)),
                                                                    }
                                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                            else:
                                                                
                                                                unRelatedSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( unRelatedSource)
                                                                if not unRelatedSourceUID:
                                                                    unErrorReason = cRefactorStatus_NoSourceUID
                                                                    if not self.vRefactor.vAllowPartialCopies:
                                                                        return False
                                                                    else:
                                                                        anErrorReport = { 
                                                                            'theclass': self.__class__.__name__, 
                                                                            'method': unMethodName, 
                                                                            'status': '%s traversalName=%s source=%s' % ( unicode( unErrorReason), unicode( unSourceTraversalNameToRetrieve), self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg( unSource)),
                                                                        }
                                                                        self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                                else:    
                                                                    if not ( unRelatedSourceUID in allRelatedSourceUIDs):
                                                                        allRelatedSources.append( unRelatedSource)
                                                                        allRelatedSourceUIDs.add( unRelatedSourceUID)
                                                            
                                                            
                                                            
                                    if allRelatedSources:
                                                   
                                        for unRelatedSource in unosRelatedSources:
                                
                                            unosTargetsToBeRelated = self.vRefactor.vMapperInfoMgr.fGetTargetsForSource( unRelatedSource)
                                            
                                            if unosTargetsToBeRelated:
                                                """Because the Source related elements have been copied, link to the copies
                                                
                                                """
                                                unosTargetsToBeRelatedOfRightType = [ ]
                                                
                                                for unTargetToBeRelated in unosTargetsToBeRelated:
                                                    
                                                    unTargetToBeRelatedType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( unTargetToBeRelated)
                                                    if ( unTargetToBeRelatedType in someRelatedTypes):                 
                                                        unosTargetsToBeRelatedOfRightType.append( unTargetToBeRelated)
                                                        
                                                if unosTargetsToBeRelatedOfRightType:
                                                    unLinkResult = self.vRefactor.vTargetInfoMgr.fLink_Relation( unTarget, unosTargetsToBeRelatedOfRightType, unRelationFieldName)
                                                    if not unLinkResult:
                                                        unErrorReason = cRefactorStatus_Error_LinkRelation_Not_Completed
                                                        if not self.vRefactor.vAllowPartialCopies:
                                                            return False
                                                        else:
                                                            anErrorReport = { 
                                                                'theclass': self.__class__.__name__, 
                                                                'method': unMethodName, 
                                                                'status': unicode( unErrorReason),
                                                            }
                                                            self.vRefactor.pAppendErrorReport( anErrorReport)
                                                        
                                                    else:
                                                        unTargetLinked = True
                                            
                                            else:
                                                """UNLESS the relation is accross roots, in which case the relation shall be created:
                                                
                                                Because the related source has not been refactored, the target is linked to the original related source.
                                                
                                                Note that the mapping of types from source to copies may produce a copy of different type than the source.
                                                As here the related source has not been refactored into any target,
                                                we link the target to the original source which may be of a different type, 
                                                therefore we must verify again if the type of the original related source can be related with the target.
        
                                                If the source and target are not under same root (or traversal config candidates_scope == 'owner', i.e. steps in a business process),
                                                then the process shall not create relations from new copied elements to non-copied sources.
                                                """
                                                
                                                unSourceToBeRelatedType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unRelatedSource)
                                                if ( unSourceToBeRelatedType in someRelatedTypes):
                                                    
                                                    unCanLink = False
        
                                                    unIsAcrossRoots = self.vRefactor.vTargetMetaInfoMgr.fGetIsAcrossRootsFromTraversalConfig( unaTargetRelationTraversalConfig)
        
                                                    if unIsAcrossRoots:
                                                        unCanLink = True
                                                        
                                                    else:
                                                    
                                                        if unRelationCandidatesScope.lower() == 'owner':
                                                            if unTargetOwnerPath:
                                                                
                                                                unSourceOwnerPath = self.vRefactor.vSourceInfoMgr.fOwnerPath( unRelatedSource)
                                                                if unSourceOwnerPath == unTargetOwnerPath:
                                                                    unCanLink = True
                                                            
                                                        else:
                                                            if unTargetRootPath:
                                                                
                                                                unSourceRootPath = self.vRefactor.vSourceInfoMgr.fRootPath( unRelatedSource)
                                                                if unSourceRootPath == unTargetRootPath:
                                                                    unCanLink = True
                                                                
                                                    if unCanLink:    
                                                        
                                                        unRelatedSourceObject = unRelatedSource.get( 'object', None)
                                                        if not ( unRelatedSourceObject == None):
        
                                                            unLinkResult = self.vRefactor.vTargetInfoMgr.fLink_Relation( unTarget, [ unRelatedSourceObject, ], unRelationFieldName)
                                                            if not unLinkResult:
                                                                unErrorReason = cRefactorStatus_Error_LinkRelation_Not_Completed
                                                                if not self.vRefactor.vAllowPartialCopies:
                                                                    return False
                                                                else:
                                                                    anErrorReport = { 
                                                                        'theclass': self.__class__.__name__, 
                                                                        'method': unMethodName, 
                                                                        'status': unicode( unErrorReason),
                                                                    }
                                                                    self.vRefactor.pAppendErrorReport( anErrorReport)
                                                                
                                                            else:
                                                                unTargetLinked = True

        
                    if unTargetLinked:
                        self.vRefactor.vModelDDvlPloneTool_Mutators.pSetAudit_Modification( unTarget)
     
                         
                         
                unCompleted = True
                return True

            except:
                unInException = True
                raise
        
        finally:
            
            if not unInException:
                if not unCompleted:
                    
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': unMethodName, 
                        'status': unicode( cRefactorStatus_Not_Completed),
                        'reason': unicode( unErrorReason),
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
    
                           
            
    
    
    
    
    
    
    
        
                        
        
class MDDRefactor_Paste_Walker_Stack:
    """
    
    """
    def __init__( self, ):
        self.vRootFrames    = [ ]
        self.vStack         = [ ]

    
    
    def fAddRootStackFrame( self, theWalker, theSourceRoot, theCreatedElement, theCreatedElementTypeConfig, theMapping):
        if ( not theWalker) or ( not theSourceRoot) or ( not theCreatedElement) or ( not theCreatedElementTypeConfig):
            return None
        
        unStackFrame = MDDRefactor_Paste_Walker_Stack_Frame()
        unStackFrame.vWalker           = theWalker 
        unStackFrame.vSource           = theSourceRoot 
        unStackFrame.vTarget           = theCreatedElement
        unStackFrame.vTargetTypeConfig = theCreatedElementTypeConfig
        unStackFrame.vMapping          = theMapping
        
        self.vRootFrames.append( unStackFrame)
        self.vStack.append(      unStackFrame)
        
        return unStackFrame
    
    
    
    def fPushStackFrame( self, theWalker, theSourceRoot, theCreatedElement, theCreatedElementTypeConfig, theMapping):
        if ( not theWalker) or ( not theSourceRoot) or ( not theCreatedElement) or ( not theCreatedElementTypeConfig):
            return None
        
        if not self.vStack:
            return None
        
        unLastFrame = self.vStack[-1:][ 0]
        if not unLastFrame:
            return None
        
        unStackFrame = MDDRefactor_Paste_Walker_Stack_Frame()
        unStackFrame.vWalker           = theWalker 
        unStackFrame.vSource           = theSourceRoot 
        unStackFrame.vTarget           = theCreatedElement
        unStackFrame.vTargetTypeConfig = theCreatedElementTypeConfig
        unStackFrame.vMapping          = theMapping
        
        unLastFrame.pAddChildFrame( unStackFrame)
        
        self.vStack.append( unStackFrame)
        
        return unStackFrame
    
    
    
    
    def fPopStackFrame( self,):
        
        if not self.vStack:
            return None
    
        unLastFrame = self.vStack[-1:][ 0]
        if not unLastFrame:
            return None
        
        self.vStack.pop()
        
        return unLastFrame
    
    
    
       
class MDDRefactor_Paste_Walker_Stack_Frame:
    """
    
    """
    def __init__( self, ):
        self.vWalker            = None
        self.vSource            = None
        self.vTarget            = None
        self.vTargetTypeConfig  = None
        self.vMapping           = None
        
        self.vChildrenFrames    = [ ]
        
        self.vCurrentChildFrameIndex = -1

        self.vMustReindexTarget = False
        
        

    def fIsFrameOk( self, ):
    
        if ( self.vWalker == None) or ( self.vSource == None) or ( self.vTarget == None) or not ( self.vTargetTypeConfig):
            return False
        
        if not self.vWalker.vRefactor.vSourceInfoMgr.fIsSourceOk( self.vSource):
            return False

        return True
    
    
    
    
    
    def pAddChildFrame( self, theStackFrame):
    
        if not theStackFrame:
            return self
            
        self.vChildrenFrames.append( theStackFrame)
        return self
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
# ######################################################
# NEW VERSION refactoring
# ######################################################
    


            
class MDDRefactor_NewVersion ( MDDRefactor):
    """Agent to perform a new version refactoring.
    
    """


    def __init__( self, 
        theModelDDvlPloneTool,
        theModelDDvlPloneTool_Retrieval,
        theModelDDvlPloneTool_Mutators,
        theOriginalRoot, 
        theNewVersionRoot,
        theNewVersionRootResult,
        theNewVersionName,
        theNewVersionComment,
        theTargetMDDTypeConfigs, 
        theTargetPloneTypeConfigs, 
        theTargetAllTypeConfigs,
        theExceptionToRaise,
        ):
        
        
        unInitialContextParms = {
            'original_root':            theOriginalRoot,
            'target_root':              theNewVersionRoot,
            'target_root_result':       theNewVersionRootResult,
            'new_version_name':         theNewVersionName,
            'new_version_comment':      theNewVersionComment,
            'target_mdd_type_configs':  theTargetMDDTypeConfigs,
            'target_plone_type_configs':theTargetPloneTypeConfigs,
            'target_all_type_configs':  theTargetAllTypeConfigs,
        }
        
        MDDRefactor.__init__(
            self,
            theModelDDvlPloneTool,
            theModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators,
            unInitialContextParms,
            MDDRefactor_NewVersion_SourceInfoMgr_MDDElements(), 
            MDDRefactor_NewVersion_SourceMetaInfoMgr_MDDElements(), 
            MDDRefactor_Paste_TargetInfoMgr_MDDElement(), 
            MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement(), 
            MDDRefactor_NewVersion_MapperInfoMgr_NoConversion(), 
            MDDRefactor_NewVersion_MapperMetaInfoMgr_NoConversion(), 
            MDDRefactor_NewVersion_TraceabilityMgr(), 
            MDDRefactor_Paste_Walker(), 
            False, # theAllowMappings
            theExceptionToRaise,
            False, # theAllowPartialCopies,
            True, # theIgnorePartialLinksForMultiplicityOrDifferentOwner,
        )
    
        
        
    
class MDDRefactor_NewVersion_SourceMetaInfoMgr_MDDElements ( MDDRefactor_Role_SourceMetaInfoMgr):
    """
    
    """
    

    def fTypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource:
            return ''
        
        unTypeName = theSource.meta_type
        return unTypeName
    
    
    def fGetArchetypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource:
            return ''
        
        unArchetypeName = theSource.archetype_name
        return unArchetypeName
    
         

    def fPloneTypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( thePloneElement == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        unMetaType = ''
        try:
            unMetaType = thePloneElement.meta_type
        except:
            None
            
        return unMetaType
    
    
    def fPloneArchetypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( thePloneElement == None):
            return ''
        
        unArchetype = ''
        try:
            unArchetype = thePloneElement.archetype_name
        except:
            None
            
        return unArchetype
    
    
    

 
        
    
    
    def fTypeConfig( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        
        if not theSource:
            return {}
        
        unTypeName = self.fTypeName( theSource)
        if not unTypeName:
            return {}
        
        unTypeConfig = self.fTypeConfigForType( unTypeName)
        return unTypeConfig
    
    

    def fTypeConfigForType( self, theSourceType, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theSourceType:
            return {}

        unTargetAllTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',) 
        if not unTargetAllTypeConfigs:
            return {}
        
        unasTypeConfigs = unTargetAllTypeConfigs.get( theSourceType, {})
        if not unasTypeConfigs:
            return {}
        
        unTypeConfigName = theTypeConfigName
        if ( not unTypeConfigName) or ( unTypeConfigName == 'Default'):
            unTypeConfigName = sorted( unasTypeConfigs.keys())[ 0]
        
        unaTypeConfig = unasTypeConfigs.get( unTypeConfigName, {})
        if not unaTypeConfig:
            return {}
        
        return unaTypeConfig
        
    
    
    
    def fAggregationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource:
            return []
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasAggregationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and not ( unAggregationName in unasAggregationNames):
                unasAggregationNames.append( unAggregationName)
                
        return unasAggregationNames
    
    
    
    
    def fHasAggregationNamed( self, theSource, theAggregationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theAggregationName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theAggregationName):
                return True
                
        return False
    
    
    
    def fHasRelationNamed( self, theSource, theRelationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theRelationName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theRelationName):
                return True
                
        return False

    
       
    def fHasTraversalNamed( self, theSource, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theTraversalName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theTraversalName):
                return True
            
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theTraversalName):
                return True
                
        return False

    
    
    
    
    def fRelationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource:
            return []
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasRelationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and not ( unRelationName in unasRelationNames):
                unasRelationNames.append( unRelationName)
                
        return unasRelationNames
    
    
    
    
    def fAttributeTypeInSource( self, theSource, theAttributeName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theAttributeName:
            return ''
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return ''
       
        unAttributeConfig = self.fAttributeConfigInSource(  theSource, theAttributeName)
        if not unAttributeConfig:
            return ''
    
        unAttributeType = unAttributeConfig.get( 'type', '')
        
        return unAttributeType
           
        
    
    


    def fAttributeConfigInSource( self, theSource, theAttributeName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theAttributeName:
            return {}
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return {}
       
        unosAttributeConfigs = unTypeConfig.get( 'attrs', [])
        if not unosAttributeConfigs:
            return {}
     
        for unAttributeConfig in unosAttributeConfigs:
            
            # ACV 20091110 Changed key.  'attribute_name' appears in  results, not configs
            # Don't know how this was working without it - indeed, because it was ignored, or fallbacks applied.
            # unAttributeName = unAttributeConfig.get( 'attribute_name', '')
            unAttributeName = unAttributeConfig.get( 'name', '')
            if unAttributeName and ( unAttributeName == theAttributeName):
                
                return unAttributeConfig
            
        return {}
                         
    
    
    
class MDDRefactor_NewVersion_SourceInfoMgr_MDDElements( MDDRefactor_Role_SourceInfoMgr):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_SourceInfoMgr.fInitInRefactor( self, theRefactor,):
            return False
        
        if not self.vRefactor.fGetContextParam( 'original_root',):
            return False

        # ACV 20091003 Should not be necessary. Copied from the XML flavor.
        #aSiteEncoding = aPloneUtilsTool.getSiteEncoding()
        #if not aSiteEncoding:
            #aSiteEncoding = cEncodingUTF8
        
        #self.vRefactor.pSetContextParam( 'site_encoding', aSiteEncoding)

         
        return True
    
      
    # ACV 20091003 Should not be necessary. Copied from the XML flavor.
    #def fGetSiteEncoding( self,):
        #if not self.vInitialized or not self.vRefactor.vInitialized:
            #return None
        
        #aSiteEncoding = self.vRefactor.fGetContextParam( 'site_encoding',)
        #return aSiteEncoding
    
    
    

    def fElementIdentificationForErrorMsg( self, theSource):
        
        if theSource == None:
            return str( None)
        
        unTitle = self.fGetTitle( theSource)
        unaId   = self.fGetId(    theSource)
        unPath  = self.fGetPath(  theSource)
        unaId   = self.fGetUID(   theSource)
        
        unaIdentification = 'Title=%s; id=%s; path=%s UID=%s' % ( repr( unTitle), repr( unaId), repr( unPath), repr( unaUID),)

        return unaIdentification
    

        
    def fElementIdentificationForErrorMsg_Unicode( self, theSource):        
      
        unaIdentification = self.fElementIdentificationForErrorMsg( theSource)
        unaIdentificationUnicode = ModelDDvlPloneTool().fAsUnicode( self.vRefactor.fGetContextParam( 'target_root'), unaIdentification)
        
        return unaIdentificationUnicode

        
    
    
    
    
    def fGetSourceRoots( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        unOriginalElement = self.vRefactor.fGetContextParam( 'original_root',) 
        if not unOriginalElement:
            return None
        
        unosSourceElements = [ unOriginalElement,]
        
        unosPloneTypeNames = cPloneTypes.keys()
        
        unosNonPloneElements = [ ]
        
        for unSourceElement in unosSourceElements:
            unTypeName = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unSourceElement)
            if not ( unTypeName in unosPloneTypeNames):
                unosNonPloneElements.append( unSourceElement)
                
        return unosNonPloneElements

    

    
    
    
    def fIsSourceReadable( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            return False
    
        return True
    
    
    
    
    def fIsSourceOk( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        allTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',)
        if not allTypeConfigs:
            return False
        
        
        unSourceType = None
        try:
            unSourceType = theSource.meta_type
        except:
            None
            
        if not unSourceType:
            return False
        
        if not allTypeConfigs.has_key( unSourceType):
            return False
        
        return True
    
    

     
     
    

    
    
    
    
    def fGetId( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        unaId = theSource.getId()
        return unaId
        
    
    
    def fGetUID( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        if theSource.meta_type in cPloneSiteMetaTypes:
            return cFakeUIDForPloneSite
        
        unaUID = theSource.UID()
        return unaUID    
    
    
    
    def fGetPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        unPath = '/'.join( theSource.getPhysicalPath())
        return unPath    
     
    
    def fGetTitle( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK
        
        unTitle = theSource.Title()
        return unTitle    
    
    
    
    
    def fOwnerPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        unPropietario = None
        try:
            unPropietario = theSource.getPropietario()
        except:
            None
        if not unPropietario:
            return ''
        
        unPropietarioPath = '/'.join( unPropietario.getRaiz().getPhysicalPath())
        return unPropietarioPath
    
    
    
    def fRootPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK
        
        unRootPath = '/'.join( theSource.getRaiz().getPhysicalPath())
        return unRootPath
    
    
    
    def fGetAttributeValue( self, theSource, theAttributeName, theAttributeType):

        unCompleted   = False
        unInException = False
        unErrorReason = ''
        
        try:
            try:
                
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
                if not self.fIsSourceOk( theSource):
                    raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK
        
                if not theAttributeName:
                    unErrorReason = cRefactorStatus_Missing_Parameter_AttributeName
                    return None
                
                if theAttributeName.lower() == 'title':
                    unCompleted = True                   
                    return self.fGetTitle( theSource)
                elif theAttributeName.lower() == 'id':
                    unCompleted = True                   
                    return self.fGetId( theSource)
                elif theAttributeName.lower() == 'path':
                    unCompleted = True                   
                    return self.fGetPath( theSource)
                elif theAttributeName.lower() == 'uid':
                    unCompleted = True                   
                    return self.fGetUID( theSource)

                
                # ACV 20091110 Not usef theAttributeType at this time, but keeping the check to enforce contract for future use
                if not theAttributeType:
                    unErrorReason = cRefactorStatus_Missing_Parameter_AttributeType
                    return None
                
                
                unAttrConfig = self.vRefactor.vSourceMetaInfoMgr.fAttributeConfigInSource( theSource, theAttributeName)
                if not unAttrConfig:
                    unErrorReason = cRefactorStatus_Error_NoAttributeConfig
                    return None
                    

               
                unRawValue = None

                unAttrAccessorName = unAttrConfig.get( 'accessor',  '')     
                unAttributeName    = unAttrConfig.get( 'attribute', '')    
                

                if unAttrAccessorName or unAttributeName:
                    
                    # ##############################################################################
                    """Non schema retrieval: Specifiying in the attribute config an accessor, o an attribute name, or both.
                    
                    """
                    if unAttrAccessorName:
                        unAccessor = None
                        try:
                            unAccessor = theSource[ unAttrAccessorName]    
                        except:
                            None
                        if not unAccessor:
                            unErrorReason = cRefactorStatus_Attr_No_Accessor
                            return None
                         
                        unRawValue = unAccessor()
   
                                
                    if unAttributeName:
                        
                        unAttributeOwner = theSource
                        if unAttrAccessorName:
                            unAttributeOwner = unRawValue
                            
                        if ( unAttributeOwner == None):
                            unErrorReason = cRefactorStatus_Attr_No_AttributeOwner
                            return None
                        
                        unRawValue = unAttributeOwner.__getattribute__( unAttributeName)
                        if unRawValue.__class__.__name__ == "ComputedAttribute":
                            
                            unComputedAttribute = unRawValue
                            unRawValue = unComputedAttribute.__get__( unAttributeOwner)
                     
                    unCompleted = True
                    
                    return unRawValue
                            
                else:
                    
                    # ##############################################################################
                    """Retrieve value through the element's schema field.
                    
                    """
                    unObjectSchema = theSource.schema
                    if not unObjectSchema:
                        unErrorReason = cExportStatus_Error_Internal_ObjectHasNoSchema,

                    
                    if not unObjectSchema.has_key( theAttributeName):
                        unErrorReason = cRefactorStatus_Field_Not_in_Schema
                        return None
                    
                    unObjectAttributeField   = unObjectSchema[ theAttributeName]

                    unRawValue = unObjectAttributeField.getRaw( theSource)
                    
                    unCompleted = True
                    
                    return unRawValue
            
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not unCompleted:
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fGetAttributeValue', 
                        'status': cRefactorStatus_SourceToTargetCorrespondence_Not_Set,
                        'condition': unErrorReason,
                        'params': { 
                            'theSource':        self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg_Unicode( theSource), 
                            'theAttribute':     theAttributeName, 
                            'theAttributeType': theAttributeType, 
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
                    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def fGetTraversalValues( self, theSource, theTraversalName, theAcceptedSourceTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        

        unSchema = None
        try:
            unSchema = theSource.schema
        except:
            None
        if not unSchema:
            return None
        
        if not unSchema.has_key( theTraversalName):
            return None
        
        unField  = unSchema[ theTraversalName]
        if not unField:
            return None
        
        unAccessor = unField.getAccessor( theSource)
        if not unAccessor:
            return None
        
        unosRetrievedElements = None
        try:
            unosRetrievedElements = unAccessor()
        except:
            None
        
        unIsMultiValued = False
        try:
            unIsMultiValued = unField.multiValued
        except:
            None
        if not unIsMultiValued:
            if not unosRetrievedElements:
                unosRetrievedElements = []
            else:
                unosRetrievedElements = [ unosRetrievedElements,]
        else:
            if unosRetrievedElements == None:
                unosRetrievedElements = []
  
        return unosRetrievedElements

        

    
    
           

class MDDRefactor_NewVersion_TargetInfoMgr_MDDElement ( MDDRefactor_Paste_TargetInfoMgr_MDDElement):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Paste_TargetInfoMgr_MDDElement.fInitInRefactor( self, theRefactor,):
            return False
        
        unNewVersionName = self.vRefactor.fGetContextParam( 'new_version_name',) 
        if not unNewVersionName:
            return False
        
        return True
      
    
    

    
    
                        
    
class MDDRefactor_NewVersion_TraceabilityMgr( MDDRefactor_Role_TraceabilityMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_TraceabilityMgr.__init__( self)
        


                 
    
    def fEstablishTraceabilityLinks( self, theSource, theTarget):

        unCompleted   = False
        unInException = False
        unErrorReason = ''
        
        try:
            try:
        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                if ( theSource == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Source
                    return False
                
                if ( theTarget == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Target
                    return False
        
                unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
                if not unSourceUID:
                    unErrorReason = cRefactorStatus_NoSourceUID
                    return False
                
                unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
                if not unTargetUID:
                    unErrorReason = cRefactorStatus_NoTargetUID
                    return False
                

                
                # #######################################
                """ Link new version with its previous, with the application-managed relationship for application managed arhectypes, and with the generic references relation for non-application archetypes.
                
                """     
                
                unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
                unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
                
                unPreviousVersionsRelationName = self.vRefactor.fGetContextParam( 'previous_relation')        

                if not (( unSourceType in cPloneTypes) or ( unTargetType in cPloneTypes)):
                    
                    if unPreviousVersionsRelationName:
                        aRelationsLibrary = self.vRefactor.fGetContextParam( 'relations_library')        
                        if not aRelationsLibrary:
                            unErrorReason = cRefactorStatus_NoRelationsLibrary
                            return False
                            
                        gRelationsProcessor.process( aRelationsLibrary, connect=[( unTargetUID, unSourceUID, unPreviousVersionsRelationName ), ], disconnect=[])
                
                else:
                    theSource.addReference( theTarget, 'PloneAT_' + unPreviousVersionsRelationName)
                
                
                        
                    
                # #######################################
                """ Set new version to the same inter version uid as the original.
                
                """
                unInterVersionFieldsCache = self.vRefactor.fGetContextParam( 'inter_version_uid_fields_cache',)  
                
                unTypeName = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
                
                unInterVersionField = unInterVersionFieldsCache.get( unTypeName, None)
                if not unInterVersionField:
                    unInterVersionFieldName = ''
                    try:
                        unInterVersionFieldName = theSource.inter_version_field
                    except:
                        None
                    if unInterVersionFieldName:
                        unSchema = theSource.schema
                        if unSchema and unSchema.has_key( unInterVersionFieldName):
                            unInterVersionField = unSchema[ unInterVersionFieldName]
                            if unInterVersionField:
                                unInterVersionFieldsCache[ unTypeName] = unInterVersionField
                                
                if unInterVersionField:
                    unSourceAccessor = unInterVersionField.getAccessor( theSource)
                    unSourceInterVersionUID = unSourceAccessor()
                    if not unSourceInterVersionUID:
                        unSourceInterVersionUID = theSource.UID()
                   
                    unTargetMutator = unInterVersionField.getMutator( theTarget)
                    if not unTargetMutator:
                        unErrorReason = cRefactorStatus_Field_No_Mutator
                        return self
                    unTargetMutator( unSourceInterVersionUID)
                    
                    
                    
                   
                # #######################################
                """ Record in the new version the source change counter.
                
                """
                unSourceChangeCounter = 0
                
                unChangeCounterFieldsCache = self.vRefactor.fGetContextParam( 'change_counter_fields_cache',)  
                unChangeCounterField = unChangeCounterFieldsCache.get( unTypeName, None)
                if not unChangeCounterField:
                    unChangeCounterFieldName = ''
                    try:
                        unChangeCounterFieldName = theSource.change_counter_field
                    except:
                        None
                    if unChangeCounterFieldName:
                        unSchema = theSource.schema
                        if unSchema and unSchema.has_key( unChangeCounterFieldName):
                            unChangeCounterField = unSchema[ unChangeCounterFieldName]
                            if unChangeCounterField:
                                unChangeCounterFieldsCache[ unTypeName] = unChangeCounterField
                                
                if unChangeCounterField:
                    unSourceAccessor = unChangeCounterField.getAccessor( theSource)
                    if not unSourceAccessor:
                        unErrorReason = cRefactorStatus_Field_No_Accessor
                        return self
                    unSourceChangeCounter = unSourceAccessor()
                    if not unSourceChangeCounter:
                        unSourceChangeCounter = 0
                    
                unTargetSourcesCounters = { }
                        
                unSourcesCountersFieldsCache = self.vRefactor.fGetContextParam( 'sources_counters_fields_cache',)  
                unSourcesCountersField = unSourcesCountersFieldsCache.get( unTypeName, None)
                if not unSourcesCountersField:
                    unSourcesCountersFieldName = ''
                    try:
                        unSourcesCountersFieldName = theSource.sources_counters_field
                    except:
                        None
                    if unSourcesCountersFieldName:
                        unSchema = theSource.schema
                            
                        if unSchema and unSchema.has_key( unSourcesCountersFieldName):
                            unSourcesCountersField = unSchema[ unSourcesCountersFieldName]
                            if unSourcesCountersField:
                                unSourcesCountersFieldsCache[ unTypeName] = unSourcesCountersField
                                
                if unSourcesCountersField:
                    unTargetAccessor = unSourcesCountersField.getAccessor( theTarget)
                    unTargetSourcesCountersString = unTargetAccessor()
                    if unTargetSourcesCountersString:   
                        try:
                            unTargetSourcesCounters = eval( unTargetSourcesCountersString)
                        except:
                            None
                        if not unTargetSourcesCounters:
                            unTargetSourcesCounters = { }
                            if not ( unTargetSourcesCounters.__class__.__name__ == 'dict'):
                                unTargetSourcesCounters = { }
                    
                    unTargetSourcesCounters[ unSourceUID] = unSourceChangeCounter
                
                    unNewTargetSourcesCountersString = repr( unTargetSourcesCounters)    
                    unTargetMutator = unSourcesCountersField.getMutator( theTarget)
                    
                    if not unTargetMutator:
                        unErrorReason = cRefactorStatus_Field_No_Mutator
                        return self
                    
                    unTargetMutator( unNewTargetSourcesCountersString)
                    
                        
                unCompleted = True
                
                return True
        
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not unCompleted:
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fEstablishTraceabilityLinks', 
                        'status': cRefactorStatus_SourceToTargetCorrespondence_Not_Set,
                        'condition': unErrorReason,
                        'params': { 
                            'theSource': self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg_Unicode( theSource), 
                            'theTarget': self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTarget), 
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
                    
    
    
                    
                
                
                
                
                
                
                
                
                
                
                
                    
    
    
    
                        
    
class MDDRefactor_NewVersion_MapperInfoMgr_NoConversion ( MDDRefactor_Role_MapperInfoMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_MapperInfoMgr.__init__( self)
        
        self.vSourcesForTargetsMap = { }
        self.vTargetsForSourcesMap = { }
        
        
        

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_MapperInfoMgr.fInitInRefactor( self, theRefactor,):
            return False

        unOriginalRoot = theRefactor.fGetContextParam( 'original_root')
        if not unOriginalRoot:
            return False
        
        unosLinkFields = None
        try:
            unosLinkFields = unOriginalRoot.versioning_link_fields
        except:
            None
        if ( not unosLinkFields) or ( len( unosLinkFields) < 2):
            return False
        
        unPreviousVersionsFieldName = unosLinkFields[ 0]
        unNextVersionsFieldName     = unosLinkFields[ 1]
        
        if not unPreviousVersionsFieldName or not unNextVersionsFieldName:
            return False
        
        unSchema = unOriginalRoot.schema
        
        if not unSchema.has_key( unPreviousVersionsFieldName) or not unSchema.has_key( unNextVersionsFieldName):
            return False

        unPreviousVersionsField = unSchema[ unPreviousVersionsFieldName]
        if ( not unPreviousVersionsField) or not ( unPreviousVersionsField.__class__.__name__ == 'RelationField'):
            return False
        
        unNextVersionsField = unSchema[ unNextVersionsFieldName]
        if ( not unNextVersionsField) or not ( unNextVersionsField.__class__.__name__ == 'RelationField'):
            return False
        
        unPreviousVersionsRelationName = ''
        try:
            unPreviousVersionsRelationName = unPreviousVersionsField.relationship
        except:
            None
        if not unPreviousVersionsRelationName:
            return False
        theRefactor.pSetContextParam( 'previous_relation', unPreviousVersionsRelationName)        
        
        unNextVersionsRelationName = ''
        try:
            unNextVersionsRelationName = unNextVersionsField.relationship
        except:
            None
        if not unNextVersionsRelationName:
            return False
        theRefactor.pSetContextParam( 'next_relation', unNextVersionsRelationName)        
        
        aRelationsLibrary = getToolByName( unOriginalRoot, RELATIONS_LIBRARY)        
        if not aRelationsLibrary:
            return False
        
        theRefactor.pSetContextParam( 'relations_library', aRelationsLibrary)      
        
        theRefactor.pSetContextParam( 'inter_version_uid_fields_cache', { })        

        theRefactor.pSetContextParam( 'change_counter_fields_cache', { })        

        theRefactor.pSetContextParam( 'sources_counters_fields_cache', { })        
                            
        return True
    
                
    
    def fMapValue( self, theSourceValue, theSourceType, theTargetType):
        
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
      
        return theSourceValue
    
    
    

     
    
    def fRegisterSourceToTargetCorrespondence( self, theSource, theTarget, theMapping):

        unCompleted   = False
        unInException = False
        unErrorReason = ''
        
        try:
            try:
        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                if ( theSource == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Source
                    return False
                
                if ( theTarget == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Target
                    return False
        
                unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
                if not unSourceUID:
                    unErrorReason = cRefactorStatus_NoSourceUID
                    return False
                
                unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
                if not unTargetUID:
                    unErrorReason = cRefactorStatus_NoTargetUID
                    return False
                
                unosTargetForSource = self.vTargetsForSourcesMap.get( unSourceUID, None)
                if unosTargetForSource == None:
                    unosTargetForSource = [ set(), [], ]
                    self.vTargetsForSourcesMap[ unSourceUID] = unosTargetForSource
                    
                unosTargetUIDs = unosTargetForSource[ 0]
                if not ( unTargetUID in unosTargetUIDs):
                    unosTargetUIDs.add( unTargetUID)
                    unosTargetForSource[ 1].append( theTarget)
                
                unosSourceForTarget = self.vSourcesForTargetsMap.get( unTargetUID, None)
                if unosSourceForTarget == None:
                    unosSourceForTarget = [ set(), [], ]
                    self.vSourcesForTargetsMap[ unTargetUID] = unosSourceForTarget
                    
                unosSourceUIDs = unosSourceForTarget[ 0]
                if not ( unSourceUID in unosSourceUIDs):
                    unosSourceUIDs.add( unSourceUID)
                    unosSourceForTarget[ 1].append( theSource)
                         
                unCompleted = True
                
                return True
        
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not unCompleted:
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fRegisterSourceToTargetCorrespondence', 
                        'status': cRefactorStatus_SourceToTargetCorrespondence_Not_Set,
                        'params': { 
                            'theSource': self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg_Unicode( theSource), 
                            'theTarget': self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTarget), 
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
                    
    
    
                
                
                
                
                
                
                
    
    
    def fGetMappingForTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        return {}
    
    
    
        
        
    def fGetTargets( self, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        todosUIDsAndTargets = self.vTargetsForSourcesMap.values()
        if not todosUIDsAndTargets:
            return []
        
        todosTargets = []
        for unosUIDsAndTargets in todosUIDsAndTargets:
            unosTargets = unosUIDsAndTargets[ 1]
            if unosTargets:
                todosTargets += unosTargets
                
        return todosTargets
    
    
    
    
    def fGetSourcesForTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
        if not unTargetUID:
            return None
        
        unosUIDsAndSources = self.vSourcesForTargetsMap.get( unTargetUID, None)
        if not unosUIDsAndSources:
            return None
        
        unosSources = unosUIDsAndSources[ 1]
        return unosSources
    
    
    
        
    def fGetTargetsForSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.vRefactor.vSourceInfoMgr.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        
        unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
        if not unSourceUID:
            return None
        
        unosUIDsAndTargets = self.vTargetsForSourcesMap.get( unSourceUID, None)
        if not unosUIDsAndTargets:
            return None
        
        unosTargets = unosUIDsAndTargets[ 1]
        return unosTargets
    
        
    
  


    def pRegisterPloneSourceToTargetCorrespondence( self, theSource, theTarget,):
        
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( not theSource) or ( not theTarget):
            return self
     
        unSourceUID = self.vRefactor.vSourceInfoMgr.fGetPloneUID( theSource)
        if not unSourceUID:
            return self
        
        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetPloneUID( theTarget)
        if not unTargetUID:
            return self
        
        unosTargetForSource = self.vTargetsForSourcesMap.get( unSourceUID, None)
        if unosTargetForSource == None:
            unosTargetForSource = [ set(), [], ]
            self.vTargetsForSourcesMap[ unSourceUID] = unosTargetForSource
            
        unosTargetUIDs = unosTargetForSource[ 0]
        if not ( unTargetUID in unosTargetUIDs):
            unosTargetUIDs.add( unTargetUID)
            unosTargetForSource[ 1].append( theTarget)
        
        unosSourceForTarget = self.vSourcesForTargetsMap.get( unTargetUID, None)
        if unosSourceForTarget == None:
            unosSourceForTarget = [ set(), [], ]
            self.vSourcesForTargetsMap[ unTargetUID] = unosSourceForTarget
            
        unosSourceUIDs = unosSourceForTarget[ 0]
        if not ( unSourceUID in unosSourceUIDs):
            unosSourceUIDs.add( unSourceUID)
            unosSourceForTarget[ 1].append( theSource)
            
        
        return self
    
    
    
    
    
    
    

    

    
    
    
    
    
class MDDRefactor_NewVersion_MapperMetaInfoMgr_NoConversion ( MDDRefactor_Role_MapperMetaInfoMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_MapperMetaInfoMgr.__init__( self)
        
        self.vMappingsByTargetTypeMap = { }
        
        
    
        
        
                
                
    def fFirstMappedTypeFromSourceTypeToTargetType( self, theSourceType, theTargetType, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSourceType or not theTargetType:
            return ''
        
        return theSourceType
    
    
    
                 
                
    def fCompileMappingFromSourceTypeToMappedType( self, theSourceType, theMappedType, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        return {}
        

    
    def fTargetAggregationConfigAndTypeToAggregateSourceIn( self, theSource, theTarget, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoSource_Type
        
        unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
        if not unTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoTarget_Type
        
        unasAggregationsWithType = self.vRefactor.vTargetMetaInfoMgr.fAggregationConfigsWithType( unTargetType, unSourceType)
        if not unasAggregationsWithType:
            return []
        
        return [ unasAggregationsWithType[ 0], unSourceType, ]
    
    
    
    
    def fMappingAndTargetAggregationConfigAndTypeToAggregateSourceIn( self, theSource, theTarget, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoSource_Type
        
        unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
        if not unTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoTarget_Type
        
        unosAggregatedTypes = self.vRefactor.vTargetMetaInfoMgr.fAggregatedTypes( unTargetType)
        
        if unSourceType in unosAggregatedTypes:
            unasAggregationsWithType = self.vRefactor.vTargetMetaInfoMgr.fAggregationConfigsWithType( unTargetType, unSourceType)
            if unasAggregationsWithType:
                return [ None, unasAggregationsWithType[ 0], unSourceType, ]
            
        return []
    
    
    
   
       
    def fSourceAttributeNameAndTypeForTargetNameAndType( self, theSource, theNameAndTypeToPopulate, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        return theNameAndTypeToPopulate
        

    
    
    def fMappedTraversalNameFromSourceForTargetAggregationName( self, theSource, theAggregationName, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        return theAggregationName

   
    def fMappedTraversalNameFromSourceForTargetRelationName( self, theSource, theRelationName, theMapping,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        return theRelationName


    
    
    def fMappingAndTargetTypeFromSourceAndAllowedTypes( self, theSource, theAllowedTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theAllowedTypes:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_AllowedTypes
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:    
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoSource_Type

        return [ None, unSourceType, ]

    
    
            
    
    def fTargetTypeFromSourceForTargetAggregationTraversalConfig( self, theSource, theTraversalConfig,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_No_TraversalConfig
                
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        return unSourceType
        
    
    
    
    
    def fTargetTypeFromSourceForTargetRelationTraversalConfig( self, theSource, theTraversalConfig,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_No_TraversalConfig
                
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoSource_Type
        
        unosRelatedTypes = self.vRefactor.vTargetMetaInfoMgr.fRelatedTypesFromTraversalConfig( theTraversalConfig)
        if not unosRelatedTypes:
            return ''
        
        if unSourceType in unosAggregatedTypes:
            return unSourceType
        
        return ''
        
                     
    
    
    
    def fTraversalNameFromSourceForTargetRelationConfig( self, theSource, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_No_TraversalConfig
                
        
        """StraightCopy : expression is same aggregation name, if source has it
        
        """
        unTargetRelationName = self.vRefactor.vTargetMetaInfoMgr.fRelationNameFromTraversalConfig( theTraversalConfig)
        if not unTargetRelationName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Field_NoRelationFieldName
        
        someSourceRelationNames = self.vRefactor.vSourceMetaInfoMgr.fRelationNamesFromSource( theSource)
        
        if unTargetRelationName in someSourceRelationNames:
            return unTargetRelationName
        
        return ''
       
    
    
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


    
# ######################################################
# NEW TRANSLATION refactoring
# ######################################################
    


            
class MDDRefactor_NewTranslation ( MDDRefactor):
    """Agent to perform a new translation refactoring.
    
    """


    def __init__( self, 
        theModelDDvlPloneTool,
        theModelDDvlPloneTool_Retrieval,
        theModelDDvlPloneTool_Mutators,
        theOriginalRoot, 
        theNewTranslationRoot,
        theNewTranslationRootResult,
        theNewLanguage,
        theFallbackStrategy,
        theTargetMDDTypeConfigs, 
        theTargetPloneTypeConfigs, 
        theTargetAllTypeConfigs,
        theExceptionToRaise,
        ):
        
        
        unInitialContextParms = {
            'original_root':            theOriginalRoot,
            'new_language':            theNewLanguage,
            'fallback_strategy':            theFallbackStrategy,
            'target_root':              theNewTranslationRoot,
            'target_root_result':       theNewTranslationRootResult,
            'new_translation_name':         theNewLanguage,
            'new_translation_comment':      theFallbackStrategy,
            'target_mdd_type_configs':  theTargetMDDTypeConfigs,
            'target_plone_type_configs':theTargetPloneTypeConfigs,
            'target_all_type_configs':  theTargetAllTypeConfigs,
        }
        
        MDDRefactor.__init__(
            self,
            theModelDDvlPloneTool,
            theModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators,
            unInitialContextParms,
            MDDRefactor_NewTranslation_SourceInfoMgr_MDDElements(), 
            MDDRefactor_NewTranslation_SourceMetaInfoMgr_MDDElements(), 
            MDDRefactor_Paste_TargetInfoMgr_MDDElement(), 
            MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement(), 
            MDDRefactor_NewTranslation_MapperInfoMgr_NoConversion(), 
            MDDRefactor_NewTranslation_MapperMetaInfoMgr_NoConversion(), 
            MDDRefactor_NewTranslation_TraceabilityMgr(), 
            MDDRefactor_Paste_Walker(), 
            False, # theAllowMappings
            theExceptionToRaise,
            False, # theAllowPartialCopies,
            True, # theIgnorePartialLinksForMultiplicityOrDifferentOwner,
        )
    
        
        
    
class MDDRefactor_NewTranslation_SourceMetaInfoMgr_MDDElements ( MDDRefactor_Role_SourceMetaInfoMgr):
    """
    
    """
    

    def fTypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource:
            return ''
        
        unTypeName = theSource.meta_type
        return unTypeName
    
    
    def fGetArchetypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource:
            return ''
        
        unArchetypeName = theSource.archetype_name
        return unArchetypeName
    
         

    def fPloneTypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( thePloneElement == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        unMetaType = ''
        try:
            unMetaType = thePloneElement.meta_type
        except:
            None
            
        return unMetaType
    
    
    def fPloneArchetypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( thePloneElement == None):
            return ''
        
        unArchetype = ''
        try:
            unArchetype = thePloneElement.archetype_name
        except:
            None
            
        return unArchetype
    
    
    

 
        
    
    
    def fTypeConfig( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        
        if not theSource:
            return {}
        
        unTypeName = self.fTypeName( theSource)
        if not unTypeName:
            return {}
        
        unTypeConfig = self.fTypeConfigForType( unTypeName)
        return unTypeConfig
    
    

    def fTypeConfigForType( self, theSourceType, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theSourceType:
            return {}

        unTargetAllTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',) 
        if not unTargetAllTypeConfigs:
            return {}
        
        unasTypeConfigs = unTargetAllTypeConfigs.get( theSourceType, {})
        if not unasTypeConfigs:
            return {}
        
        unTypeConfigName = theTypeConfigName
        if ( not unTypeConfigName) or ( unTypeConfigName == 'Default'):
            unTypeConfigName = sorted( unasTypeConfigs.keys())[ 0]
        
        unaTypeConfig = unasTypeConfigs.get( unTypeConfigName, {})
        if not unaTypeConfig:
            return {}
        
        return unaTypeConfig
        
    
    
    
    def fAggregationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource:
            return []
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasAggregationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and not ( unAggregationName in unasAggregationNames):
                unasAggregationNames.append( unAggregationName)
                
        return unasAggregationNames
    
    
    
    
    def fHasAggregationNamed( self, theSource, theAggregationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theAggregationName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theAggregationName):
                return True
                
        return False
    
    
    
    def fHasRelationNamed( self, theSource, theRelationName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theRelationName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theRelationName):
                return True
                
        return False

    
       
    def fHasTraversalNamed( self, theSource, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theTraversalName:
            return False
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return False
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return False
                
        for unaTraversalConfig in unasTraversalConfigs:
            unAggregationName = unaTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and ( unAggregationName == theTraversalName):
                return True
            
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and ( unRelationName == theTraversalName):
                return True
                
        return False

    
    
    
    
    def fRelationNamesFromSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource:
            return []
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return []
       
        unasTraversalConfigs = unTypeConfig.get( 'traversals', [])
        if not unasTraversalConfigs:
            return []
        
        unasRelationNames = [ ]
        
        for unaTraversalConfig in unasTraversalConfigs:
            unRelationName = unaTraversalConfig.get( 'relation_name', '')
            if unRelationName and not ( unRelationName in unasRelationNames):
                unasRelationNames.append( unRelationName)
                
        return unasRelationNames
    
    
    
    
    def fAttributeTypeInSource( self, theSource, theAttributeName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theAttributeName:
            return ''
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return ''
       
        unAttributeConfig = self.fAttributeConfigInSource(  theSource, theAttributeName)
        if not unAttributeConfig:
            return ''
    
        unAttributeType = unAttributeConfig.get( 'type', '')
        
        return unAttributeType
           
        
    
    


    def fAttributeConfigInSource( self, theSource, theAttributeName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSource or not theAttributeName:
            return {}
        
        unTypeConfig = self.fTypeConfig( theSource)
        if not unTypeConfig:
            return {}
       
        unosAttributeConfigs = unTypeConfig.get( 'attrs', [])
        if not unosAttributeConfigs:
            return {}
     
        for unAttributeConfig in unosAttributeConfigs:
            
            # ACV 20091110 Changed key.  'attribute_name' appears in  results, not configs
            # Don't know how this was working without it - indeed, because it was ignored, or fallbacks applied.
            # unAttributeName = unAttributeConfig.get( 'attribute_name', '')
            unAttributeName = unAttributeConfig.get( 'name', '')
            if unAttributeName and ( unAttributeName == theAttributeName):
                
                return unAttributeConfig
            
        return {}
                         
    
    
    
class MDDRefactor_NewTranslation_SourceInfoMgr_MDDElements( MDDRefactor_Role_SourceInfoMgr):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_SourceInfoMgr.fInitInRefactor( self, theRefactor,):
            return False
        
        if not self.vRefactor.fGetContextParam( 'original_root',):
            return False

        # ACV 20091003 Should not be necessary. Copied from the XML flavor.
        #aSiteEncoding = aPloneUtilsTool.getSiteEncoding()
        #if not aSiteEncoding:
            #aSiteEncoding = cEncodingUTF8
        
        #self.vRefactor.pSetContextParam( 'site_encoding', aSiteEncoding)

         
        return True
    
      
    # ACV 20091003 Should not be necessary. Copied from the XML flavor.
    #def fGetSiteEncoding( self,):
        #if not self.vInitialized or not self.vRefactor.vInitialized:
            #return None
        
        #aSiteEncoding = self.vRefactor.fGetContextParam( 'site_encoding',)
        #return aSiteEncoding
    
    
    

    def fElementIdentificationForErrorMsg( self, theSource):
        
        if theSource == None:
            return str( None)
        
        unTitle = self.fGetTitle( theSource)
        unaId   = self.fGetId(    theSource)
        unPath  = self.fGetPath(  theSource)
        unaId   = self.fGetUID(   theSource)
        
        unaIdentification = 'Title=%s; id=%s; path=%s UID=%s' % ( repr( unTitle), repr( unaId), repr( unPath), repr( unaUID),)

        return unaIdentification
    

        
    def fElementIdentificationForErrorMsg_Unicode( self, theSource):        
      
        unaIdentification = self.fElementIdentificationForErrorMsg( theSource)
        unaIdentificationUnicode = ModelDDvlPloneTool().fAsUnicode( self.vRefactor.fGetContextParam( 'target_root'), unaIdentification)
        
        return unaIdentificationUnicode

        
    
    
    
    
    def fGetSourceRoots( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        unOriginalElement = self.vRefactor.fGetContextParam( 'original_root',) 
        if not unOriginalElement:
            return None
        
        unosSourceElements = [ unOriginalElement,]
        
        unosPloneTypeNames = cPloneTypes.keys()
        
        unosNonPloneElements = [ ]
        
        for unSourceElement in unosSourceElements:
            unTypeName = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unSourceElement)
            if not ( unTypeName in unosPloneTypeNames):
                unosNonPloneElements.append( unSourceElement)
                
        return unosNonPloneElements

    

    
    
    
    def fIsSourceReadable( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            return False
    
        return True
    
    
    
    
    def fIsSourceOk( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        allTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',)
        if not allTypeConfigs:
            return False
        
        
        unSourceType = None
        try:
            unSourceType = theSource.meta_type
        except:
            None
            
        if not unSourceType:
            return False
        
        if not allTypeConfigs.has_key( unSourceType):
            return False
        
        return True
    
    

     
     
    

    
    
    
    
    def fGetId( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        unaId = theSource.getId()
        return unaId
        
    
    
    def fGetUID( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        if theSource.meta_type in cPloneSiteMetaTypes:
            return cFakeUIDForPloneSite
        
        unaUID = theSource.UID()
        return unaUID    
    
    
    
    def fGetPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        unPath = '/'.join( theSource.getPhysicalPath())
        return unPath    
     
    
    def fGetTitle( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK
        
        unTitle = theSource.Title()
        return unTitle    
    
    
    
    
    def fOwnerPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        unPropietario = None
        try:
            unPropietario = theSource.getPropietario()
        except:
            None
        if not unPropietario:
            return ''
        
        unPropietarioPath = '/'.join( unPropietario.getRaiz().getPhysicalPath())
        return unPropietarioPath
    
    
    
    def fRootPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK
        
        unRootPath = '/'.join( theSource.getRaiz().getPhysicalPath())
        return unRootPath
    
    
    
    def fGetAttributeValue( self, theSource, theAttributeName, theAttributeType):

        unCompleted   = False
        unInException = False
        unErrorReason = ''
        
        try:
            try:
                
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
                if not self.fIsSourceOk( theSource):
                    raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK
        
                if not theAttributeName:
                    unErrorReason = cRefactorStatus_Missing_Parameter_AttributeName
                    return None
                
                if theAttributeName.lower() == 'title':
                    unCompleted = True                   
                    return self.fGetTitle( theSource)
                elif theAttributeName.lower() == 'id':
                    unCompleted = True                   
                    return self.fGetId( theSource)
                elif theAttributeName.lower() == 'path':
                    unCompleted = True                   
                    return self.fGetPath( theSource)
                elif theAttributeName.lower() == 'uid':
                    unCompleted = True                   
                    return self.fGetUID( theSource)

                
                # ACV 20091110 Not usef theAttributeType at this time, but keeping the check to enforce contract for future use
                if not theAttributeType:
                    unErrorReason = cRefactorStatus_Missing_Parameter_AttributeType
                    return None
                
                
                unAttrConfig = self.vRefactor.vSourceMetaInfoMgr.fAttributeConfigInSource( theSource, theAttributeName)
                if not unAttrConfig:
                    unErrorReason = cRefactorStatus_Error_NoAttributeConfig
                    return None
                    

               
                unRawValue = None

                unAttrAccessorName = unAttrConfig.get( 'accessor',  '')     
                unAttributeName    = unAttrConfig.get( 'attribute', '')    
                

                if unAttrAccessorName or unAttributeName:
                    
                    # ##############################################################################
                    """Non schema retrieval: Specifiying in the attribute config an accessor, o an attribute name, or both.
                    
                    """
                    if unAttrAccessorName:
                        unAccessor = None
                        try:
                            unAccessor = theSource[ unAttrAccessorName]    
                        except:
                            None
                        if not unAccessor:
                            unErrorReason = cRefactorStatus_Attr_No_Accessor
                            return None
                         
                        unRawValue = unAccessor()
   
                                
                    if unAttributeName:
                        
                        unAttributeOwner = theSource
                        if unAttrAccessorName:
                            unAttributeOwner = unRawValue
                            
                        if ( unAttributeOwner == None):
                            unErrorReason = cRefactorStatus_Attr_No_AttributeOwner
                            return None
                        
                        unRawValue = unAttributeOwner.__getattribute__( unAttributeName)
                        if unRawValue.__class__.__name__ == "ComputedAttribute":
                            
                            unComputedAttribute = unRawValue
                            unRawValue = unComputedAttribute.__get__( unAttributeOwner)
                     
                    unCompleted = True
                    
                    return unRawValue
                            
                else:
                    
                    # ##############################################################################
                    """Retrieve value through the element's schema field.
                    
                    """
                    unObjectSchema = theSource.schema
                    if not unObjectSchema:
                        unErrorReason = cExportStatus_Error_Internal_ObjectHasNoSchema,

                    
                    if not unObjectSchema.has_key( theAttributeName):
                        unErrorReason = cRefactorStatus_Field_Not_in_Schema
                        return None
                    
                    unObjectAttributeField   = unObjectSchema[ theAttributeName]

                    unRawValue = unObjectAttributeField.getRaw( theSource)
                    
                    unCompleted = True
                    
                    return unRawValue
            
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not unCompleted:
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fGetAttributeValue', 
                        'status': cRefactorStatus_SourceToTargetCorrespondence_Not_Set,
                        'condition': unErrorReason,
                        'params': { 
                            'theSource':        self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg_Unicode( theSource), 
                            'theAttribute':     theAttributeName, 
                            'theAttributeType': theAttributeType, 
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
                    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def fGetTraversalValues( self, theSource, theTraversalName, theAcceptedSourceTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        

        unSchema = None
        try:
            unSchema = theSource.schema
        except:
            None
        if not unSchema:
            return None
        
        if not unSchema.has_key( theTraversalName):
            return None
        
        unField  = unSchema[ theTraversalName]
        if not unField:
            return None
        
        unAccessor = unField.getAccessor( theSource)
        if not unAccessor:
            return None
        
        unosRetrievedElements = None
        try:
            unosRetrievedElements = unAccessor()
        except:
            None
        
        unIsMultiValued = False
        try:
            unIsMultiValued = unField.multiValued
        except:
            None
        if not unIsMultiValued:
            if unosRetrievedElements == None:
                unosRetrievedElements = []
            else:
                unosRetrievedElements = [ unosRetrievedElements,]
        else:
            if unosRetrievedElements == None:
                unosRetrievedElements = []
  
        return unosRetrievedElements

        

    
    
           

class MDDRefactor_NewTranslation_TargetInfoMgr_MDDElement ( MDDRefactor_Paste_TargetInfoMgr_MDDElement):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Paste_TargetInfoMgr_MDDElement.fInitInRefactor( self, theRefactor,):
            return False
        
        unNewTranslationName = self.vRefactor.fGetContextParam( 'new_translation_name',) 
        if not unNewTranslationName:
            return False
        
        return True
      
    
    

    
    
                        
    
class MDDRefactor_NewTranslation_TraceabilityMgr( MDDRefactor_Role_TraceabilityMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_TraceabilityMgr.__init__( self)
        


                 
    
    def fEstablishTraceabilityLinks( self, theSource, theTarget):

        unCompleted   = False
        unInException = False
        unErrorReason = ''
        
        try:
            try:
        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                if ( theSource == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Source
                    return False
                
                if ( theTarget == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Target
                    return False
        
                unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
                if not unSourceUID:
                    unErrorReason = cRefactorStatus_NoSourceUID
                    return False
                
                unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
                if not unTargetUID:
                    unErrorReason = cRefactorStatus_NoTargetUID
                    return False
                

                
                # #######################################
                """ Link new translation with its previous, with the application-managed relationship for application managed arhectypes, and with the generic references relation for non-application archetypes.
                
                """     
                
                unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
                unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
                
                unPreviousTranslationsRelationName = self.vRefactor.fGetContextParam( 'previous_relation')        

                if not (( unSourceType in cPloneTypes) or ( unTargetType in cPloneTypes)):
                    
                    if unPreviousTranslationsRelationName:
                        aRelationsLibrary = self.vRefactor.fGetContextParam( 'relations_library')        
                        if not aRelationsLibrary:
                            unErrorReason = cRefactorStatus_NoRelationsLibrary
                            return False
                            
                        gRelationsProcessor.process( aRelationsLibrary, connect=[( unTargetUID, unSourceUID, unPreviousTranslationsRelationName ), ], disconnect=[])
                
                else:
                    theSource.addReference( theTarget, 'PloneAT_' + unPreviousTranslationsRelationName)
                
                
                        
                    
                # #######################################
                """ Set new translation to the same inter translation uid as the original.
                
                """
                unInterTranslationFieldsCache = self.vRefactor.fGetContextParam( 'inter_translation_uid_fields_cache',)  
                
                unTypeName = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
                
                unInterTranslationField = unInterTranslationFieldsCache.get( unTypeName, None)
                if not unInterTranslationField:
                    unInterTranslationFieldName = ''
                    try:
                        unInterTranslationFieldName = theSource.inter_translation_field
                    except:
                        None
                    if unInterTranslationFieldName:
                        unSchema = theSource.schema
                        if unSchema and unSchema.has_key( unInterTranslationFieldName):
                            unInterTranslationField = unSchema[ unInterTranslationFieldName]
                            if unInterTranslationField:
                                unInterTranslationFieldsCache[ unTypeName] = unInterTranslationField
                                
                if unInterTranslationField:
                    unSourceAccessor = unInterTranslationField.getAccessor( theSource)
                    unSourceInterTranslationUID = unSourceAccessor()
                    if not unSourceInterTranslationUID:
                        unSourceInterTranslationUID = theSource.UID()
                   
                    unTargetMutator = unInterTranslationField.getMutator( theTarget)
                    if not unTargetMutator:
                        unErrorReason = cRefactorStatus_Field_No_Mutator
                        return self
                    unTargetMutator( unSourceInterTranslationUID)
                    
                    
                    
                   
                # #######################################
                """ Record in the new translation the source change counter.
                
                """
                unSourceChangeCounter = 0
                
                unChangeCounterFieldsCache = self.vRefactor.fGetContextParam( 'change_counter_fields_cache',)  
                unChangeCounterField = unChangeCounterFieldsCache.get( unTypeName, None)
                if not unChangeCounterField:
                    unChangeCounterFieldName = ''
                    try:
                        unChangeCounterFieldName = theSource.change_counter_field
                    except:
                        None
                    if unChangeCounterFieldName:
                        unSchema = theSource.schema
                        if unSchema and unSchema.has_key( unChangeCounterFieldName):
                            unChangeCounterField = unSchema[ unChangeCounterFieldName]
                            if unChangeCounterField:
                                unChangeCounterFieldsCache[ unTypeName] = unChangeCounterField
                                
                if unChangeCounterField:
                    unSourceAccessor = unChangeCounterField.getAccessor( theSource)
                    if not unSourceAccessor:
                        unErrorReason = cRefactorStatus_Field_No_Accessor
                        return self
                    unSourceChangeCounter = unSourceAccessor()
                    if not unSourceChangeCounter:
                        unSourceChangeCounter = 0
                    
                unTargetSourcesCounters = { }
                        
                unSourcesCountersFieldsCache = self.vRefactor.fGetContextParam( 'sources_counters_fields_cache',)  
                unSourcesCountersField = unSourcesCountersFieldsCache.get( unTypeName, None)
                if not unSourcesCountersField:
                    unSourcesCountersFieldName = ''
                    try:
                        unSourcesCountersFieldName = theSource.sources_counters_field
                    except:
                        None
                    if unSourcesCountersFieldName:
                        unSchema = theSource.schema
                            
                        if unSchema and unSchema.has_key( unSourcesCountersFieldName):
                            unSourcesCountersField = unSchema[ unSourcesCountersFieldName]
                            if unSourcesCountersField:
                                unSourcesCountersFieldsCache[ unTypeName] = unSourcesCountersField
                                
                if unSourcesCountersField:
                    unTargetAccessor = unSourcesCountersField.getAccessor( theTarget)
                    unTargetSourcesCountersString = unTargetAccessor()
                    if unTargetSourcesCountersString:   
                        try:
                            unTargetSourcesCounters = eval( unTargetSourcesCountersString)
                        except:
                            None
                        if not unTargetSourcesCounters:
                            unTargetSourcesCounters = { }
                            if not ( unTargetSourcesCounters.__class__.__name__ == 'dict'):
                                unTargetSourcesCounters = { }
                    
                    unTargetSourcesCounters[ unSourceUID] = unSourceChangeCounter
                
                    unNewTargetSourcesCountersString = repr( unTargetSourcesCounters)    
                    unTargetMutator = unSourcesCountersField.getMutator( theTarget)
                    
                    if not unTargetMutator:
                        unErrorReason = cRefactorStatus_Field_No_Mutator
                        return self
                    
                    unTargetMutator( unNewTargetSourcesCountersString)
                    
                        
                unCompleted = True
                
                return True
        
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not unCompleted:
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fEstablishTraceabilityLinks', 
                        'status': cRefactorStatus_SourceToTargetCorrespondence_Not_Set,
                        'condition': unErrorReason,
                        'params': { 
                            'theSource': self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg_Unicode( theSource), 
                            'theTarget': self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTarget), 
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
                    
    
    
                    
                
                
                
                
                
                
                
                
                
                
                
                    
    
    
    
                        
    
class MDDRefactor_NewTranslation_MapperInfoMgr_NoConversion ( MDDRefactor_Role_MapperInfoMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_MapperInfoMgr.__init__( self)
        
        self.vSourcesForTargetsMap = { }
        self.vTargetsForSourcesMap = { }
        
        
        

    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_MapperInfoMgr.fInitInRefactor( self, theRefactor,):
            return False

        unOriginalRoot = theRefactor.fGetContextParam( 'original_root')
        if not unOriginalRoot:
            return False
        
        unosLinkFields = None
        try:
            unosLinkFields = unOriginalRoot.translationing_link_fields
        except:
            None
        if ( not unosLinkFields) or ( len( unosLinkFields) < 2):
            return False
        
        unPreviousTranslationsFieldName = unosLinkFields[ 0]
        unNextTranslationsFieldName     = unosLinkFields[ 1]
        
        if not unPreviousTranslationsFieldName or not unNextTranslationsFieldName:
            return False
        
        unSchema = unOriginalRoot.schema
        
        if not unSchema.has_key( unPreviousTranslationsFieldName) or not unSchema.has_key( unNextTranslationsFieldName):
            return False

        unPreviousTranslationsField = unSchema[ unPreviousTranslationsFieldName]
        if ( not unPreviousTranslationsField) or not ( unPreviousTranslationsField.__class__.__name__ == 'RelationField'):
            return False
        
        unNextTranslationsField = unSchema[ unNextTranslationsFieldName]
        if ( not unNextTranslationsField) or not ( unNextTranslationsField.__class__.__name__ == 'RelationField'):
            return False
        
        unPreviousTranslationsRelationName = ''
        try:
            unPreviousTranslationsRelationName = unPreviousTranslationsField.relationship
        except:
            None
        if not unPreviousTranslationsRelationName:
            return False
        theRefactor.pSetContextParam( 'previous_relation', unPreviousTranslationsRelationName)        
        
        unNextTranslationsRelationName = ''
        try:
            unNextTranslationsRelationName = unNextTranslationsField.relationship
        except:
            None
        if not unNextTranslationsRelationName:
            return False
        theRefactor.pSetContextParam( 'next_relation', unNextTranslationsRelationName)        
        
        aRelationsLibrary = getToolByName( unOriginalRoot, RELATIONS_LIBRARY)        
        if not aRelationsLibrary:
            return False
        
        theRefactor.pSetContextParam( 'relations_library', aRelationsLibrary)      
        
        theRefactor.pSetContextParam( 'inter_translation_uid_fields_cache', { })        

        theRefactor.pSetContextParam( 'change_counter_fields_cache', { })        

        theRefactor.pSetContextParam( 'sources_counters_fields_cache', { })        
                            
        return True
    
                
    
    def fMapValue( self, theSourceValue, theSourceType, theTargetType):
        
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
      
        return theSourceValue
    
    
    

     
    
    def fRegisterSourceToTargetCorrespondence( self, theSource, theTarget, theMapping):

        unCompleted   = False
        unInException = False
        unErrorReason = ''
        
        try:
            try:
        
                if not self.vInitialized or not self.vRefactor.vInitialized:
                    unErrorReason = cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
                    return False
                
                if ( theSource == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Source
                    return False
                
                if ( theTarget == None):
                    unErrorReason = cRefactorStatus_Missing_Parameter_Target
                    return False
        
                unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
                if not unSourceUID:
                    unErrorReason = cRefactorStatus_NoSourceUID
                    return False
                
                unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
                if not unTargetUID:
                    unErrorReason = cRefactorStatus_NoTargetUID
                    return False
                
                unosTargetForSource = self.vTargetsForSourcesMap.get( unSourceUID, None)
                if unosTargetForSource == None:
                    unosTargetForSource = [ set(), [], ]
                    self.vTargetsForSourcesMap[ unSourceUID] = unosTargetForSource
                    
                unosTargetUIDs = unosTargetForSource[ 0]
                if not ( unTargetUID in unosTargetUIDs):
                    unosTargetUIDs.add( unTargetUID)
                    unosTargetForSource[ 1].append( theTarget)
                
                unosSourceForTarget = self.vSourcesForTargetsMap.get( unTargetUID, None)
                if unosSourceForTarget == None:
                    unosSourceForTarget = [ set(), [], ]
                    self.vSourcesForTargetsMap[ unTargetUID] = unosSourceForTarget
                    
                unosSourceUIDs = unosSourceForTarget[ 0]
                if not ( unSourceUID in unosSourceUIDs):
                    unosSourceUIDs.add( unSourceUID)
                    unosSourceForTarget[ 1].append( theSource)
                                   
                         
                unCompleted = True
                
                return True
        
            
            except:
                unInException = True
                raise
            
        finally:
            if not unInException:
                if not unCompleted:
                    anErrorReport = { 
                        'theclass': self.__class__.__name__, 
                        'method': 'fRegisterSourceToTargetCorrespondence', 
                        'status': cRefactorStatus_SourceToTargetCorrespondence_Not_Set,
                        'params': { 
                            'theSource': self.vRefactor.vSourceInfoMgr.fElementIdentificationForErrorMsg_Unicode( theSource), 
                            'theTarget': self.vRefactor.vTargetInfoMgr.fElementIdentificationForErrorMsg_Unicode( theTarget), 
                        }, 
                    }
                    self.vRefactor.pAppendErrorReport( anErrorReport)
                    if not self.vRefactor.vAllowPartialCopies:
                        raise self.vRefactor.vExceptionToRaise, repr( anErrorReport)
                    
    
    
                
                
                
                
                
                
                
    
    
    def fGetMappingForTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        return {}
    
    
    
        
    def fGetTargets( self, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        todosUIDsAndTargets = self.vTargetsForSourcesMap.values()
        if not todosUIDsAndTargets:
            return []
        
        todosTargets = []
        for unosUIDsAndTargets in todosUIDsAndTargets:
            unosTargets = unosUIDsAndTargets[ 1]
            if unosTargets:
                todosTargets += unosTargets
                
        return todosTargets
    
    
    
    
    def fGetSourcesForTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
        if not unTargetUID:
            return None
        
        unosUIDsAndSources = self.vSourcesForTargetsMap.get( unTargetUID, None)
        if not unosUIDsAndSources:
            return None
        
        unosSources = unosUIDsAndSources[ 1]
        return unosSources
    
    
    
        
    def fGetTargetsForSource( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if not self.vRefactor.vSourceInfoMgr.fIsSourceOk( theSource):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Source_Not_OK

        
        unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
        if not unSourceUID:
            return None
        
        unosUIDsAndTargets = self.vTargetsForSourcesMap.get( unSourceUID, None)
        if not unosUIDsAndTargets:
            return None
        
        unosTargets = unosUIDsAndTargets[ 1]
        return unosTargets
    
        
    
  


    def pRegisterPloneSourceToTargetCorrespondence( self, theSource, theTarget,):
        
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( not theSource) or ( not theTarget):
            return self
     
        unSourceUID = self.vRefactor.vSourceInfoMgr.fGetPloneUID( theSource)
        if not unSourceUID:
            return self
        
        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetPloneUID( theTarget)
        if not unTargetUID:
            return self
        
        unosTargetForSource = self.vTargetsForSourcesMap.get( unSourceUID, None)
        if unosTargetForSource == None:
            unosTargetForSource = [ set(), [], ]
            self.vTargetsForSourcesMap[ unSourceUID] = unosTargetForSource
            
        unosTargetUIDs = unosTargetForSource[ 0]
        if not ( unTargetUID in unosTargetUIDs):
            unosTargetUIDs.add( unTargetUID)
            unosTargetForSource[ 1].append( theTarget)
        
        unosSourceForTarget = self.vSourcesForTargetsMap.get( unTargetUID, None)
        if unosSourceForTarget == None:
            unosSourceForTarget = [ set(), [], ]
            self.vSourcesForTargetsMap[ unTargetUID] = unosSourceForTarget
            
        unosSourceUIDs = unosSourceForTarget[ 0]
        if not ( unSourceUID in unosSourceUIDs):
            unosSourceUIDs.add( unSourceUID)
            unosSourceForTarget[ 1].append( theSource)
            
        
        return self
    
    
    
    
    

    
    

    
    
    
    
    
class MDDRefactor_NewTranslation_MapperMetaInfoMgr_NoConversion ( MDDRefactor_Role_MapperMetaInfoMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_MapperMetaInfoMgr.__init__( self)
        
        self.vMappingsByTargetTypeMap = { }
        
        
    
        
        
                
                
    def fFirstMappedTypeFromSourceTypeToTargetType( self, theSourceType, theTargetType, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if not theSourceType or not theTargetType:
            return ''
        
        return theSourceType
    
    
    
                 
                
    def fCompileMappingFromSourceTypeToMappedType( self, theSourceType, theMappedType, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        return {}
        

    
    def fTargetAggregationConfigAndTypeToAggregateSourceIn( self, theSource, theTarget, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoSource_Type
        
        unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
        if not unTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoTarget_Type
        
        unasAggregationsWithType = self.vRefactor.vTargetMetaInfoMgr.fAggregationConfigsWithType( unTargetType, unSourceType)
        if not unasAggregationsWithType:
            return []
        
        return [ unasAggregationsWithType[ 0], unSourceType, ]
    
    
    
    
    def fMappingAndTargetAggregationConfigAndTypeToAggregateSourceIn( self, theSource, theTarget, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized
        
        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if ( theTarget == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Target
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoSource_Type
        
        unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
        if not unTargetType:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoTarget_Type
        
        unosAggregatedTypes = self.vRefactor.vTargetMetaInfoMgr.fAggregatedTypes( unTargetType)
        
        if unSourceType in unosAggregatedTypes:
            unasAggregationsWithType = self.vRefactor.vTargetMetaInfoMgr.fAggregationConfigsWithType( unTargetType, unSourceType)
            if unasAggregationsWithType:
                return [ None, unasAggregationsWithType[ 0], unSourceType, ]
            
        return []
    
    
    
   
       
    def fSourceAttributeNameAndTypeForTargetNameAndType( self, theSource, theNameAndTypeToPopulate, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        return theNameAndTypeToPopulate
        

    
    
    def fMappedTraversalNameFromSourceForTargetAggregationName( self, theSource, theAggregationName, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        return theAggregationName

   
    def fMappedTraversalNameFromSourceForTargetRelationName( self, theSource, theRelationName, theMapping,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        return theRelationName


    
    
    def fMappingAndTargetTypeFromSourceAndAllowedTypes( self, theSource, theAllowedTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theAllowedTypes:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_AllowedTypes
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:    
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoSource_Type

        return [ None, unSourceType, ]

    
    
            
    
    def fTargetTypeFromSourceForTargetAggregationTraversalConfig( self, theSource, theTraversalConfig,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_No_TraversalConfig
                
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        return unSourceType
        
    
    
    
    
    def fTargetTypeFromSourceForTargetRelationTraversalConfig( self, theSource, theTraversalConfig,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_No_TraversalConfig
                
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_NoSource_Type
        
        unosRelatedTypes = self.vRefactor.vTargetMetaInfoMgr.fRelatedTypesFromTraversalConfig( theTraversalConfig)
        if not unosRelatedTypes:
            return ''
        
        if unSourceType in unosAggregatedTypes:
            return unSourceType
        
        return ''
        
                     
    
    
    
    def fTraversalNameFromSourceForTargetRelationConfig( self, theSource, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized

        if ( theSource == None):
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Missing_Parameter_Source
        
        if not theTraversalConfig:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Error_Paste_Internal_No_TraversalConfig
                
        
        """StraightCopy : expression is same aggregation name, if source has it
        
        """
        unTargetRelationName = self.vRefactor.vTargetMetaInfoMgr.fRelationNameFromTraversalConfig( theTraversalConfig)
        if not unTargetRelationName:
            raise self.vRefactor.vExceptionToRaise, cRefactorStatus_Field_NoRelationFieldName
        
        someSourceRelationNames = self.vRefactor.vSourceMetaInfoMgr.fRelationNamesFromSource( theSource)
        
        if unTargetRelationName in someSourceRelationNames:
            return unTargetRelationName
        
        return ''
       
    
    
       
    
    
    
    
    
    
    