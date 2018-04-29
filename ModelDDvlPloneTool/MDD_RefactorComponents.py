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



from ModelDDvlPloneTool_Retrieval               import ModelDDvlPloneTool_Retrieval
from ModelDDvlPloneTool_Mutators                import ModelDDvlPloneTool_Mutators

from PloneElement_TraversalConfig               import cPloneTypes

from ModelDDvlPloneTool_Refactor_Constants      import *
from ModelDDvlPloneTool_ImportExport_Constants  import *



cLogExceptions = True





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
        theInitialContextParms =None,
        theSourceInfoMgr       =None, 
        theSourceMetaInfoMgr   =None, 
        theTargetInfoMgr       =None, 
        theTargetMetaInfoMgr   =None, 
        theMapperInfoMgr       =None,
        theMapperMetaInfoMgr   =None, 
        theWalker              =None, 
        ):
        
        self.vContext           = { }
        if theInitialContextParms:
            self.vContext.update( theInitialContextParms)
            
        self.vResult            = None
        self.vStarted           = False
        self.vTerminated        = False
        self.vSuccess           = False
        self.vErrorReports      = [ ]
            
        self.vSourceInfoMgr     = theSourceInfoMgr
        self.vSourceMetaInfoMgr = theSourceMetaInfoMgr
        self.vTargetInfoMgr     = theTargetInfoMgr
        self.vTargetMetaInfoMgr = theTargetMetaInfoMgr
        self.vMapperInfoMgr     = theMapperInfoMgr
        self.vMapperMetaInfoMgr = theMapperMetaInfoMgr
        self.vWalker            = theWalker
    
        self.vInitialized       = False
        self.vInitFailed        = False
        
        """Enforce all role members required.
        
        """        
        if ( self.vSourceInfoMgr == None)   or ( self.vSourceMetaInfoMgr == None)  or \
           ( self.vTargetInfoMgr == None)   or ( self.vTargetMetaInfoMgr == None)  or \
           ( self.vMapperInfoMgr == None)   or ( self.vMapperMetaInfoMgr == None)  or ( self.vWalker == None):
            return self

        try:
                    
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
                
            if self.vWalker and not self.vInitFailed:
                if not self.vWalker.fInitInRefactor( self):
                    self.vInitFailed = True
                else:
                    self.vWalker.vInitialized = True
                
            self.vInitialized       = True
            
        except:
            
            self.vInitFailed = True
            
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during %s __init__\n' % self.__class__.__name__
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            self.vErrorReports.append( unInformeExcepcion)

            
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            

    
            
            
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
            return None
        
        if not self.vWalker:
            return None
        
        try:
            self.vStarted = True
            
            try:
                
                aResult = self.vWalker.fRefactor()

                self.vResult  = aResult
                
                if self.vResult and ( self.vResult.get( 'success', False) == True):
                    self.vSuccess = True
                
                return self.vResult
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during %s fRefactor\n' % self.__class__.__name__
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                self.vErrorReports.append( unInformeExcepcion)
    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return { 'success': False, }
        finally:
            self.vTerminated = True
            
        return self
    
    
    

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
        theIsMoveOperation,
        theSourceElementResults, 
        theTargetRoot, 
        theTargetRootResult, 
        theTargetAllTypeConfigs, 
        theMappingConfigs):
        
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
            unInitialContextParms,
            MDDRefactor_Paste_SourceInfoMgr_TraversalResult(), 
            MDDRefactor_Paste_SourceMetaInfoMgr_TraversalResult(), 
            MDDRefactor_Paste_TargetInfoMgr_MDDElement(), 
            MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement(), 
            MDDRefactor_Paste_MapperInfoMgr(), 
            MDDRefactor_Paste_MapperMetaInfoMgr_ConvertTypes(), 
            MDDRefactor_Paste_Walker(), 
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
            return None
        unosSourceElementResults = self.vRefactor.fGetContextParam( 'source_element_results',) 
        return unosSourceElementResults
    
    
    
 
    
    
    def fIsSourceReadable( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        if not self.fIsSourceOk( theSource):
            return False
    
        aIsReadable = theSource.get( 'read_permission', False)
        return aIsReadable
    
    
    
    def fIsSourceOk( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not theSourceElementResult or ( theSourceElementResult.get( 'object', None) == None):
            return False
        
        return True
    
    
    def fGetId( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unaId = theSourceElementResult.get( 'id', '')
        return unaId
    
    
    
    def fGetUID( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unaUID = theSourceElementResult.get( 'UID', '')
        return unaUID
    
    
    
    def fGetPath( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unPath = theSourceElementResult.get( 'path', '')
        return unPath
        
    
    def fGetTitle( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unTitle = theSourceElementResult.get( 'title', '')
        return unTitle
    
    


       
    
    def fOwnerPath( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unOwnerPath = theSourceElementResult.get( 'owner_path', '')
        return unOwnerPath
    
    
    
    def fRootPath( self, theSourceElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
            return ''
        
        unRootPath = theSourceElementResult.get( 'root_path', '')
        return unRootPath
    
    
    
    
    
        
    def fGetAttributeValue( self, theSourceElementResult, theAttributeName, theAttributeType):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
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
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult) or ( not theTraversalName):
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
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSourceElementResult):
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
        
        # ModelDDvlPloneTool_Mutators().pSetAudit_Modification( unContenedor)       

        unContenedorSource.manage_delObjects( [ unSourceId, ])
        
        return True
        
    
    
    
        
    
class MDDRefactor_Paste_SourceMetaInfoMgr_TraversalResult ( MDDRefactor_Role_SourceMetaInfoMgr):
    """
    
    """
    

    def fTypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unTypeName = theSource.get( 'meta_type', '')
        return unTypeName
    
    
    def fGetArchetypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unArchetypeName = theSource.get( 'archetype_name', '')
        return unArchetypeName
    
         

    def fPloneTypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if ( thePloneElement == None):
            return ''
        
        unMetaType = ''
        try:
            unMetaType = thePloneElement.meta_type
        except:
            None
            
        return unMetaType
    
    
    def fPloneArchetypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
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
            return ''
        
        if not theSource:
            return ''
        
        unTypeConfig = theSource.get( 'type_config', {})
        return unTypeConfig

    
    
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
            
            unAttributeName = unAttributeConfig.get( 'attribute_name', '')
            if unAttributeName and ( unAttributeName == theAttributeName):
                
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
      

 
    
    def fGetTitle( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theTarget:
            return ''
        
        unTitle = theTarget.Title() 
        return unTitle
    


    
    
    def fGetPloneUID( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized or ( thePloneElement == None):
            return ''
        
        unaUID = ''
        try:
            unaUID = thePloneElement.UID()
        except:
            None
            
        return unaUID
    

    
    def fGetTargetRoot( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        unTargetRoot = self.vRefactor.fGetContextParam( 'target_root',) 
        return unTargetRoot
    
    
    def fGetTargetRootResult( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        unTargetRootResult = self.vRefactor.fGetContextParam( 'target_root_result',) 
        return unTargetRootResult
     
    
    
    def fCreateAggregatedElement( self, theSource, theTarget, theMetaTypeToCreate, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None

        if not theTarget or not theMetaTypeToCreate or not theSource:
            return None
        
        unPortalTypeToCreate = self.vRefactor.vTargetMetaInfoMgr.fPlonePortalTypeForMetaType(  theMetaTypeToCreate)
        if not unPortalTypeToCreate:
            return None

        unSourceId    = self.vRefactor.vSourceInfoMgr.fGetId( theSource)
        if not unSourceId:
            return None
        
        unSourceTitle = self.vRefactor.vSourceInfoMgr.fGetTitle( theSource)
        if not unSourceTitle:
            return None
        
        unosExistingAggregatedElements = theTarget.objectValues()
        
        unosExistingIds    = [ unElement.getId() for unElement in unosExistingAggregatedElements]
        unosExistingTitles = [ unElement.Title() for unElement in unosExistingAggregatedElements]
        
        
        aPloneToolForNormalizeString = getToolByName( theTarget, 'plone_utils', None)
        if aPloneToolForNormalizeString  and  not shasattr( aPloneToolForNormalizeString, 'normalizeString'):
            aPloneToolForNormalizeString = None
        
        unNewTargetId    = self.fUniqueStringWithCounter( unSourceId,    unosExistingIds, aPloneToolForNormalizeString)
        if not unNewTargetId:
            return None
        unNewTargetTitle = self.fUniqueStringWithCounter( unSourceTitle, unosExistingTitles)
        if not unNewTargetTitle:
            return None
        
        
        anAttrsDict = {  'title': unNewTargetTitle, }
        
        unCreatedId = None
        try:
            unCreatedId = theTarget.invokeFactory( unPortalTypeToCreate, unNewTargetId, **anAttrsDict)
        except:
            return None
        if not unCreatedId:
            return None
        
        # ACV 20090917 Raises exception  when invoking on the element method manage_permission from pSetElementPermissions
        #              Raises ValueError, ( "The permission <em>%s</em> is invalid." % escape(permission_to_manage))
        #
        #unCreatedElement = None
        #try:
            #unCreatedElement = theTarget._getOb( unCreatedId)
        #except:
            #None
            
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
        
        ModelDDvlPloneTool_Mutators().pSetElementPermissions( unCreatedElement)
                
        return unCreatedElement
    
    
    
        
    def fUniqueAggregatedTitle(self, theTarget, theTitle):
        if ( not theTitle) or ( theTarget == None):
            return ''
        
        unosExistingAggregatedElements = theTarget.objectValues()
        
        unosExistingTitles = [ unElement.Title() for unElement in unosExistingAggregatedElements]
        unNewTitle = self.fUniqueStringWithCounter( theTitle, unosExistingTitles)
        
        return unNewTitle
                 
    
    
    
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
    
    
    
    
    
    
    def pPopulateElementAttributes( self, theSource, theTarget, theTargetTypeConfig, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return self
        
        if ( not theSource) or ( not theTarget) or ( not theTargetTypeConfig):
            return self
        
        
        unosTargetAttributesNameTypesAndAttrConfig = self.vRefactor.vTargetMetaInfoMgr.fAttributesNamesTypeAndAttrConfigFromTypeConfig( theTargetTypeConfig)
        if not unosTargetAttributesNameTypesAndAttrConfig:
            return self
        
        for unTargetAttributeNameTypeAndAttrConfig in unosTargetAttributesNameTypesAndAttrConfig:
            
            unTargetAttributeName   = unTargetAttributeNameTypeAndAttrConfig[ 0]
            unTargetAttributeType   = unTargetAttributeNameTypeAndAttrConfig[ 1]
            unTargetAttributeConfig = unTargetAttributeNameTypeAndAttrConfig[ 2]
            
            if not ( unTargetAttributeName.lower() in [ 'title', 'id',]) and unTargetAttributeType:
                
                unSourceNameAndType = self.vRefactor.vMapperMetaInfoMgr.fSourceAttributeNameAndTypeForTargetNameAndType( theSource, unTargetAttributeNameTypeAndAttrConfig, theMapping)
                if unSourceNameAndType:
                    
                    unSourceAttributeName = unSourceNameAndType[ 0]
                    unSourceAttributeType = unSourceNameAndType[ 1]
                    
                    if unSourceAttributeName and unSourceAttributeType:
                        
                        unSourceValue = self.vRefactor.vSourceInfoMgr.fGetAttributeValue( theSource, unSourceAttributeName, unSourceAttributeType)
                        if unSourceValue:
                            
                            unValueToSet = self.vRefactor.vMapperInfoMgr.fMapValue( unSourceValue, unSourceAttributeType, unTargetAttributeType)
                            if unValueToSet:
                                unVoidHasBeenSet = self.fSetAttributeValue( theTarget, unTargetAttributeName, unValueToSet, unTargetAttributeConfig,)
            
        return self
    
    

    
    def fSetAttributeValue( self, theTarget, theAttrName, theValueToSet, theAttributeConfig=None):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        
        if ( theTarget == None) or ( not theAttrName):
            return False
        
        try:
                
            if theAttributeConfig:
                unAttrMutatorAccessorName = theAttributeConfig.get( 'mutator_accessor', '')     
                unAttributeName    = theAttributeConfig.get( 'attribute', '')     
                unAttrMutatorName  = theAttributeConfig.get( 'mutator', '')  
             
                
                unObject = theTarget
                
                if ( theTarget.__class__.__name__ == 'ATDocument') and ( theAttrName == 'content_type'):
                    unSchema = None
                    try:
                        unSchema = theTarget.schema
                    except:
                        None
                    if not unSchema:
                        return False
                    
                    if not unSchema.has_key( 'text'):
                        return False
                    
                    unField  = unSchema[ 'text']
                    if not unField:
                        return False
                    
                    unField.setContentType( theTarget, theValueToSet)
                    return True
                
                if unAttrMutatorAccessorName or unAttributeName or unAttrMutatorName:
                    
                    if unAttrMutatorAccessorName:
                        
                        unAccessor = unObject[ unAttrMutatorAccessorName]    
                        if not unAccessor:
                            return False
                        
                        unRawValue = unAccessor()                            
                        if ( unRawValue == None):
                            return False
                        unObject = unRawValue
                             
                            
                    if unAttributeName:
                        if ( unObject == None):
                            return False
                        
                        try: 
                            unObject.__setattribute__( unAttributeName, theValueToSet)
                        except:
                            unObject.__setattr__( unAttributeName, theValueToSet)

                            
                        return True 
                    
                     
                    if unAttrMutatorName:
                        if ( unObject == None):
                            return False
                        
                        unMutator = unObject[ unAttrMutatorName]    
                        if not unMutator:
                            return False

                        unMutator( theValueToSet)
                        return True
                        
                else:
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
                    
                    try:
                        unMutator( theValueToSet)
                    except:
                        return False
                
        except:
            
            if not unObject:
                unObject = theTarget
                
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            unInformeExcepcion = 'Exception during %s fSetAttributeValue \n'  % self.__class__.__name__
            unInformeExcepcion += 'meta_type=%s path=%s attribute=%s \n' % ( unObject.meta_type, '/'.join( unObject.getPhysicalPath()), str( theAttrName),)
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
            
            aLogger = logging.getLogger( 'ModelDDvlPloneTool')
            aLogger.info( unInformeExcepcion) 
            return False
    
        return True
    

    
    
    def fGetUID( self, theElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        if ( theElement == None):
            return ''
        
        unaUID = ''
        try:
            unaUID = theElement.UID()
        except:
            None
            
        return unaUID
    
      
    
    def fIsTargetResultOk( self, theTargetElementResult):
        if not self.vInitialized or not self.vRefactor.vInitialized or not theTargetElementResult or ( theTargetElementResult.get( 'object', None) == None):
            return False
        
        return True
    
    
       
    def fGetPermissionFromElementResult( self, theElementResult, thePermission):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        if not self.fIsTargetResultOk( theElementResult):
            return False
    
        if not ( thePermission in [ 'read_permission', 'traverse_permission', 'write_permission', 'add_permission', 'add_collection_permission', 'delete_permission', ]):
            return False
        
        aPermissionPermitted = theElementResult.get( thePermission, False)
        return aPermissionPermitted
    
    
    def fGetPermissionFromTraversalResult( self, theTraversalResult, thePermission):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return False
        if not theTraversalResult:
            return False
    
        if not ( thePermission in [ 'read_permission', 'write_permission', ]):
            return False
        
        aPermissionPermitted = theTraversalResult.get( thePermission, False)
        return aPermissionPermitted
        
    
    
    def fTraversalResultNamed( self, theElementResult, theTraversalName):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        if not self.fIsTargetResultOk( theElementResult):
            return {}
    
        if not theTraversalName:
            return {}
        
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
            return ''
        
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
            return ''
        if ( theElement == None):
            return ''
    
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
            return None
        if ( theElement == None):
            return None
    
        unPathString = ''
        try:
            unPathString = theElement.fPhysicalPathString()
        except:
            None
        return unPathString
    
    
    

    
    def fLink_Relation( self, theTargetFrom, theTargetsTo, theFieldName):
        """
        
        """
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        
        if ( theTargetFrom == None) or not theTargetsTo or not theFieldName:
            return None
        
        unSchema = theTargetFrom.schema
        if not unSchema.has_key( theFieldName):
            return None
         
        unField             = unSchema[ theFieldName]
        unFieldClassName    = unField.__class__.__name__
        
        if not ( unFieldClassName in [ 'RelationField', 'ReferenceField']):
            return None
            
            
        if unField.__class__.__name__ == 'RelationField':
            
            unRelationName = ''
            try:
                unRelationName = unField.relationship
            except:
                None
            if not unRelationName:         
                return None
            
            aRelationsLibrary = getToolByName( theTargetFrom, RELATIONS_LIBRARY)        
            if not aRelationsLibrary:
                return None
                
            unTargetUID = self.fGetUID( theTargetFrom)
            if not unTargetUID:
                return None
        
            for unTargetToBeRelated in theTargetsTo:
                
                unTargetToBeRelatedUID = self.vRefactor.vTargetInfoMgr.fGetUID( unTargetToBeRelated)
                if unTargetToBeRelatedUID:
                    try:
                        gRelationsProcessor.process( aRelationsLibrary, connect=[( unTargetUID, unTargetToBeRelatedUID, unRelationName ), ], disconnect=[])
                    except:
                        None
            
            return theTargetFrom
        
        elif unField.__class__.__name__ == 'ReferenceField':
            
            unMutator = unField.getMutator( theTargetFrom)
            if unMutator:
                unIsMultivalued = False
                try:
                    unIsMultivalued = unField.multiValued
                except:
                    None
                if unIsMultivalued:      
                    try:
                        unMutator( theTargetsTo)
                    except:
                        None
                else:
                    unTargetTo = theTargetsTo[ 0]
                    try:
                        unMutator( unTargetTo)
                    except:
                        None
            
            return theTargetFrom
            
        return None
            
 
    
    
    
    def fCollectionToMergeWith( self, theTargetElement, theTypeToCreate, theSourceResult):
        """Return First Sub Element Of Type, With Title Or Default Title. Also return whether to Override its Title .
        
        """
        unSourceTitle         = self.vRefactor.vSourceInfoMgr.fGetTitle( theSourceResult)
        unSourceArchetypeName = self.vRefactor.vSourceMetaInfoMgr.fGetArchetypeName( theSourceResult)
        
        unSourceHasDefaultTitle = unSourceTitle == unSourceArchetypeName
        
        someSubElements =  theTargetElement.objectValues( theTypeToCreate)
        if not someSubElements:
            return ( None, False, )
        
        unosSubElementsMatching = [ ]
        
        for unSubElement in someSubElements:
            
            unSubElementTitle = unSubElement.Title()
            
            if unSubElementTitle == unSourceTitle:
                return ( unSubElement, False, )
                
            else:
                unSubElementArchetypeName = ''
                try:
                    unSubElementArchetypeName = unSubElement.archetype_name
                except:
                    None
                if unSubElementTitle == unSubElementArchetypeName:
                    return ( unSubElement, True, )
                 
        if unSourceHasDefaultTitle:
            return ( someSubElements[ 0], False, ) 
                
        return ( None, False, )
    
    
    
    
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
            return ''
        
        if not theTarget:
            return ''
    
        unTypeName = ''
        try:
            unTypeName = theTarget.meta_type
        except:
            None
        
        return unTypeName
    

    def fPlonePortalTypeForMetaType(self, theMetaType):
        if not theMetaType:
            return ''
        
        aPlonePortalTypeSpec = cPloneTypes.get( theMetaType, {})
        if not aPlonePortalTypeSpec:
            return theMetaType
        
        unPortalType = aPlonePortalTypeSpec.get( 'portal_type', '')
        
        return unPortalType
        
    
    def fTypeConfig( self, theTarget, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theTarget:
            return {}

        unTargetType = self.fTypeName( theTarget)
        if not unTargetType:
            return {}
        
        unTypeConfig = self.fTypeConfigForType( unTargetType, theTypeConfigName)
        return unTypeConfig
    
    
        
    
    def fTypeConfigForType( self, theTargetType, theTypeConfigName=''):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theTargetType:
            return {}

        unTargetAllTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',) 
        if not unTargetAllTypeConfigs:
            return {}
        
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
            return []
        
        if ( not theTargetType) or ( not theSourceType):
            return []

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
            return {}
        
        if ( not theTargetType) or ( not theTraversalConfig):
            return {}
        
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
            return []
        
        if not theTargetType:
            return []

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
            return False
        
        if not theTraversalConfig:
            return False
 
        if not self.fIsTraversalConfigAggregation( theTraversalConfig):
            return False
        
        unContainsCollection = theTraversalConfig.get( 'contains_collections', False) == True
        return unContainsCollection
        
    
    
    
    

    def fAggregationNameFromTraversalConfig( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theTraversalConfig:
            return ''
        
        unAggregationName = theTraversalConfig.get( 'aggregation_name', '')
        return unAggregationName
        
     
    def fAggregatedTypesFromTraversalConfig( self, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
        if not theTraversalConfig:
            return []
        
        unAggregationName = theTraversalConfig.get( 'aggregation_name', '')
        if not unAggregationName:
            return []

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
            return []
        
        if not theTraversalConfig:
            return []
        
        unRelationName = theTraversalConfig.get( 'relation_name', '')
        if not unRelationName:
            return []

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
            return []
        
        if not theTraversalConfig:
            return []
        
        unRelationName = theTraversalConfig.get( 'relation_name', '')
        if not unRelationName:
            return ''
        
        unCandidatesScope = theTraversalConfig.get( 'candidates_scope','').lower()
        return unCandidatesScope

    
    
    
    def fAggregationTraversalConfigsFromTypeConfig( self, theTypeConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
        if not theTypeConfig:
            return []
        
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
            return ''
        
        if not theTraversalConfig:
            return ''
        
        unRelationName = theTraversalConfig.get( 'relation_name', '')
        return unRelationName
        
     
    def fRelationTraversalConfigsFromTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
        if not theTarget:
            return []
        
        unTypeConfig = self.fTypeConfig( theTarget)
        if not unTypeConfig:
            return []
        
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
            return []
        
        if not theTypeConfig:
            return []

        unosAttrConfigs = theTypeConfig.get( 'attrs', [])
        if not unosAttrConfigs:
            return []
        
        unosAttributeNamesAndTypes = [ ]
        
        for unAttrConfig in unosAttrConfigs:
            unAttrName = unAttrConfig.get( 'name', '')
            if unAttrName:
                unAttrType = unAttrConfig.get( 'type', '')
                if unAttrType:
                    unosAttributeNamesAndTypes.append( [ unAttrName, unAttrType, unAttrConfig,])
                    
                
        return unosAttributeNamesAndTypes
        

    
    
    
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
            return None
        
        if ( not theSourceType) or ( not theTargetType):
            return None
        
        if theTargetType.lower() == theSourceType.lower():
            return theSourceValue
        
        return theSourceValue
    
    
    
    
    
    def pRegisterSourceToTargetCorrespondence( self, theSource, theTarget, theMapping):
        
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return self
        
        if ( not theSource) or ( not theTarget):
            return self
     
        unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
        if not unSourceUID:
            return self
        
        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
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
            
        self.vMappingsForTargets[ unTargetUID] = theMapping
        
        return self
    
    
    
    
    def fGetMappingForTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theTarget:
            return {}
        
        if not self.vMappingsForTargets:
            return {}

        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
        if not unTargetUID:
            return {}
        
        unMapping = self.vMappingsForTargets.get( unTargetUID, {})
        
        return unMapping
        
        
    def fGetTargets( self, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        
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
            return None

        if not theTarget:
            return None
        
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
            return None

        if not theSource:
            return None
        
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
            return self
        
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
            return ''
        
        if not theSourceType or not theTargetType:
            return ''
        
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
            return {}
        
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
            return []
        
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
            return []
        
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
            return []

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
            return ''

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
        
        if self.vRefactor.vSourceMetaInfoMgr.fHasTraversalNamed( theSource, unMappedFeature):
            return unMappedFeature
        
        return ''

    

    
    def fMappedTraversalNameFromSourceForTargetRelationName( self, theSource, theRelationName, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''

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
        
        if self.vRefactor.vSourceMetaInfoMgr.fHasTraversalNamed( theSource, unMappedFeature):
            return unMappedFeature
        
        return ''

    
    
    def fMappingAndTargetTypeFromSourceAndAllowedTypes( self, theSource, theAllowedTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []

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
            return ''

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
            return ''

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
            return ''

        if not theSource or not theTraversalConfig:
            return None
        
        """StraightCopy : expression is same aggregation name, if source has it
        
        """
        unTargetRelationName = self.vRefactor.vTargetMetaInfoMgr.fRelationNameFromTraversalConfig( theTraversalConfig)
        someSourceRelationNames = self.vRefactor.vSourceMetaInfoMgr.fRelationNamesFromSource( theSource)
        
        if unTargetRelationName in someSourceRelationNames:
            return unTargetRelationName
        
        return ''
       
    
    
    

        
    
class MDDRefactor_Paste_Walker ( MDDRefactor_Role_Walker):
    """
    
    """
    
    
    
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_Walker.fInitInRefactor( self, theRefactor,):
            return False
        
        unRefactorStack = MDDRefactor_Paste_Walker_Stack()        
        
        self.vRefactor.pSetContextParam( 'stack', unRefactorStack)        
        
        return True
    
    
    
    
    
    
    # MDDRefactor_Paste_Walker also invokes fRefactor_IntoRoot, rather than forcing fRefactor_RootAggregations
    # as now MDDRefactor_Paste_Walker also invokes fRefactor_IntoRoot, rather than forcing fRefactor_RootAggregations
    #
    def fRefactor( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return { 'success': False, }

        unosSourceRoots             = self.vRefactor.vSourceInfoMgr.fGetSourceRoots()
        
        if not unosSourceRoots:
            return  { 'success': False, }
        
        unTargetRoot = self.vRefactor.vTargetInfoMgr.fGetTargetRoot()
        if ( unTargetRoot == None):
            return  { 'success': False, }
        
        unTargetRootResult = self.vRefactor.vTargetInfoMgr.fGetTargetRootResult()
        if ( unTargetRootResult == None):
            return  { 'success': False, }
        
        if not self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'read_permission'):
            return  { 'success': False, }
        
        if not self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'write_permission'):
            return  { 'success': False, }
        
        aVoid = self.fRefactor_IntoRoot( unosSourceRoots, unTargetRoot)
        
        #aVoid = self.fRefactor_RootAggregations( unosSourceRoots, unTargetRoot)
        
        unIsMoveOperation =  self.vRefactor.fGetContextParam( 'is_move_operation')
        if unIsMoveOperation:
            aVoid = self.fRefactor_Moves()
                
        aVoid = self.fRefactor_Relations( )
        
        return { 'success': True, }
           
    
    
    

    
    
    # ACV 20090922 Moved here from MDDRefactor_Import_Walker, 
    #
    def fRefactor_IntoRoot( self, theSourceRoots, theTargetRoot):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
    
        if not theSourceRoots or ( theTargetRoot == None):
            return None
        
        unTargetRootType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTargetRoot)
        if not unTargetRootType:
            return None

        unTargetRootTitle = self.vRefactor.vTargetInfoMgr.fGetTitle( theTargetRoot)
        if not unTargetRootTitle:
            return None
        
        unTargetRootResult = self.vRefactor.vTargetInfoMgr.fGetTargetRootResult() 
        if not unTargetRootResult:
            return None
        
        unTargetRootTypeConfig =  self.vRefactor.vTargetMetaInfoMgr.fTypeConfig( theTargetRoot)     
        if not unTargetRootTypeConfig:
            return None
        
        unRefactorStack = self.vRefactor.fGetContextParam( 'stack')  
        if not unRefactorStack:
            return None
        
        someSourcesMappedToSameTypeAsTargetRoot     = [ ]
        someSourcesMappedToAggregationsInTargetRoot = [ ]
        
        for unSourceRoot in theSourceRoots:
            if self.vRefactor.vSourceInfoMgr.fIsSourceOk( unSourceRoot):
                
                if self.vRefactor.vSourceInfoMgr.fIsSourceReadable( unSourceRoot):
                    
                    unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unSourceRoot)
                    if unSourceType:
                        
                        if ( unSourceType == unTargetRootType):
                            someSourcesMappedToSameTypeAsTargetRoot.append( unSourceRoot)
                            continue
                        
                        unMappedType = self.vRefactor.vMapperMetaInfoMgr.fFirstMappedTypeFromSourceTypeToTargetType( unSourceType, unTargetRootType)
                        if unMappedType:
                            
                            if unMappedType == unTargetRootType:
                                someSourcesMappedToSameTypeAsTargetRoot.append( unSourceRoot)
                                continue
                        
                        unMappingTargetAggregationConfigAndType = self.vRefactor.vMapperMetaInfoMgr.fMappingAndTargetAggregationConfigAndTypeToAggregateSourceIn( unSourceRoot, theTargetRoot)
                        if unMappingTargetAggregationConfigAndType and len( unMappingTargetAggregationConfigAndType) > 2:
                            unaTargetAggregationConfig = unMappingTargetAggregationConfigAndType[ 1]
                            unTypeToCreate             = unMappingTargetAggregationConfigAndType[ 2]
                            
                            if unaTargetAggregationConfig and unTypeToCreate:
                                someSourcesMappedToAggregationsInTargetRoot.append( unSourceRoot)
                                continue
                        
        if ( not someSourcesMappedToSameTypeAsTargetRoot) and ( not someSourcesMappedToAggregationsInTargetRoot):
            return None
        
        if ( not someSourcesMappedToSameTypeAsTargetRoot):
            return self.fRefactor_RootAggregations( someSourcesMappedToAggregationsInTargetRoot, theTargetRoot)
        
        
        
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
        
                
                
        for unSourceRoot in someSourcesMappedToSameTypeAsTargetRoot:
        
            unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( unSourceRoot)
            if unSourceType:
                
                if ( unSourceType == unTargetRootType):
                    unMapping = []
                else:
                    unMapping = self.vRefactor.vMapperMetaInfoMgr.fCompileMappingFromSourceTypeToMappedType( unSourceType, unTargetRootType, )
                
                unSourceRootTitle = self.vRefactor.vSourceInfoMgr.fGetTitle( unSourceRoot)
                
                if not ( unSourceRootTitle == unTargetRootTitle):
                    unNewTargetRootTitle = self.vRefactor.vTargetInfoMgr.fUniqueStringWithCounter( unSourceRootTitle, unosExistingRootSiblingsTitles)
                    if unNewTargetRootTitle:
                        theTargetRoot.setTitle( unNewTargetRootTitle)
                        theTargetRoot.reindexObject( )
                
                    
                self.vRefactor.vMapperInfoMgr.pRegisterSourceToTargetCorrespondence( unSourceRoot, theTargetRoot, unMapping)
        
                unRefactorFrame = unRefactorStack.fAddRootStackFrame( self, unSourceRoot, theTargetRoot, unTargetRootTypeConfig, unMapping)
                if unRefactorFrame:
                    try:
                        self.fRefactor_Frame( unRefactorFrame)
                    finally:
                        unRefactorStack.fPopStackFrame()
                                          
        return self
        
    
    
    def fRefactor_RootAggregations( self, theSourceRoots, theTargetRoot):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
    
        if not theSourceRoots:
            return self
        
        if theTargetRoot == None:
            return None
        
        unTargetRootResult = self.vRefactor.vTargetInfoMgr.fGetTargetRootResult() 
        if not unTargetRootResult:
            return None
        
        if not self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'traverse_permission'):
            return None

        unRefactorStack = self.vRefactor.fGetContextParam( 'stack')  
        if not unRefactorStack:
            return None
        
        for unSourceRoot in theSourceRoots:
            if self.vRefactor.vSourceInfoMgr.fIsSourceOk( unSourceRoot):
                
                if self.vRefactor.vSourceInfoMgr.fIsSourceReadable( unSourceRoot):

                    unMappingTargetAggregationConfigAndType = self.vRefactor.vMapperMetaInfoMgr.fMappingAndTargetAggregationConfigAndTypeToAggregateSourceIn( unSourceRoot, theTargetRoot)
                    if unMappingTargetAggregationConfigAndType and len( unMappingTargetAggregationConfigAndType) > 2:
                        
                        unMapping                  = unMappingTargetAggregationConfigAndType[ 0]
                        unaTargetAggregationConfig = unMappingTargetAggregationConfigAndType[ 1]
                        unTypeToCreate             = unMappingTargetAggregationConfigAndType[ 2]
                        
                        if unaTargetAggregationConfig and unTypeToCreate:
                            
                            unContainsCollections = self.vRefactor.vTargetMetaInfoMgr.fGetAggregationConfigContainsCollections( unaTargetAggregationConfig)
                            
                            unAddingPermitted = False
                            if unContainsCollections:
                                
                                if self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'add_collection_permission'):
                                    unAddingPermitted = True
                            else:
                                if self.vRefactor.vTargetInfoMgr.fGetPermissionFromElementResult( unTargetRootResult, 'add_permission'):
                                    unAddingPermitted = True
                                    

                            if unContainsCollections:
                                
                                unaCollectionToMergeWith, aOverrideTitle = self.vRefactor.vTargetInfoMgr.fCollectionToMergeWith( theTargetRoot, unTypeToCreate, unSourceRoot)
                                
                                if unaCollectionToMergeWith:
                                         
                                    if aOverrideTitle:
                                        unSourceRootTitle = self.vRefactor.vSourceInfoMgr.fGetTitle( unSourceRoot)
                                        
                                        unNewTargetTitle = self.vRefactor.vTargetInfoMgr.fUniqueAggregatedTitle( theTargetRoot, unSourceRootTitle)
                                        if unNewTargetTitle:
                                            unaCollectionToMergeWith.setTitle( unNewTargetTitle)
                                        
                                    unaCollectionType       = self.vRefactor.vTargetMetaInfoMgr.fTypeName( unaCollectionToMergeWith)
                                    unaCollectionTypeConfig = self.vRefactor.vTargetMetaInfoMgr.fTypeConfigForType( unaCollectionType)
                                    
                                    self.vRefactor.vMapperInfoMgr.pRegisterSourceToTargetCorrespondence( unSourceRoot, unaCollectionToMergeWith, unMapping)
                                    
                                    unRefactorFrame = unRefactorStack.fAddRootStackFrame( self, unSourceRoot, unaCollectionToMergeWith, unaCollectionTypeConfig, unMapping)
                                    if unRefactorFrame:
                                        try:
                                            self.fRefactor_Frame( unRefactorFrame)
                                        finally:
                                            unRefactorStack.fPopStackFrame()
                                        
                                        continue
                                        
                                    
                            if unAddingPermitted:
                                
                                unaTargetAggregationName = self.vRefactor.vTargetMetaInfoMgr.fAggregationNameFromTraversalConfig( unaTargetAggregationConfig)
                                if unaTargetAggregationName:
                                    
                                    unRootAggregationResult  = self.vRefactor.vTargetInfoMgr.fTraversalResultNamed( unTargetRootResult, unaTargetAggregationName)
                                    if unRootAggregationResult:
                                        
                                        if self.vRefactor.vTargetInfoMgr.fGetPermissionFromTraversalResult( unRootAggregationResult, 'read_permission') and \
                                           self.vRefactor.vTargetInfoMgr.fGetPermissionFromTraversalResult( unRootAggregationResult, 'write_permission'):
    
                                            unCreatedElement = self.vRefactor.vTargetInfoMgr.fCreateAggregatedElement( unSourceRoot, theTargetRoot, unTypeToCreate, )
                                            if unCreatedElement:
                                                
                                                unCreatedElementTypeConfig = self.vRefactor.vTargetMetaInfoMgr.fTypeConfigForType( unTypeToCreate)
                                                self.vRefactor.vMapperInfoMgr.pRegisterSourceToTargetCorrespondence( unSourceRoot, unCreatedElement, unMapping)
                                                
                                                unRefactorFrame = unRefactorStack.fAddRootStackFrame( self, unSourceRoot, unCreatedElement, unCreatedElementTypeConfig, unMapping)
                                                if unRefactorFrame:
                                                    try:
                                                        self.fRefactor_Frame( unRefactorFrame)
                                                    finally:
                                                        unRefactorStack.fPopStackFrame()
            
        return self
    
        
    
                    
                    
                    
                    
    def fRefactor_Frame( self, theRefactorFrame):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
    
        if not theRefactorFrame or not theRefactorFrame.fIsFrameOk():
            return None
        
        self.vRefactor.vTargetInfoMgr.pPopulateElementAttributes( theRefactorFrame.vSource, theRefactorFrame.vTarget, theRefactorFrame.vTargetTypeConfig, theRefactorFrame.vMapping)
        
        self.fRefactor_Frame_Aggregations( theRefactorFrame)
        
        #self.fRefactor_Frame_PloneContent( theRefactorFrame)
        
        return theRefactorFrame
    
    
    
    
    
    
    def fRefactor_Frame_Aggregations( self, theRefactorFrame):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
    
        if not theRefactorFrame or not theRefactorFrame.fIsFrameOk():
            return None
        
        unRefactorStack = self.vRefactor.fGetContextParam( 'stack')  
        if not unRefactorStack:
            return None
        
        someAggregationTraversalConfigs = self.vRefactor.vTargetMetaInfoMgr.fAggregationTraversalConfigsFromTypeConfig( theRefactorFrame.vTargetTypeConfig)
        if not someAggregationTraversalConfigs:
            return None
        
        for anAggregationTraversalConfig in someAggregationTraversalConfigs:
            
            unAggregationName = self.vRefactor.vTargetMetaInfoMgr.fAggregationNameFromTraversalConfig( anAggregationTraversalConfig)
            if unAggregationName:
   
                someAggregatedTypes = self.vRefactor.vTargetMetaInfoMgr.fAggregatedTypesFromTraversalConfig( anAggregationTraversalConfig)
                if someAggregatedTypes:

                    unSourceTraversalNameToRetrieve = self.vRefactor.vMapperMetaInfoMgr.fMappedTraversalNameFromSourceForTargetAggregationName( theRefactorFrame.vSource, unAggregationName, theRefactorFrame.vMapping)
                    if unSourceTraversalNameToRetrieve:

                        unosAggregatedSources = self.vRefactor.vSourceInfoMgr.fGetTraversalValues( theRefactorFrame.vSource, unSourceTraversalNameToRetrieve, [])
                        if unosAggregatedSources:
                            
                            for unAggregatedSource in unosAggregatedSources:
                                
                                if self.vRefactor.vSourceInfoMgr.fIsSourceOk( unAggregatedSource):
                                                                            
                                    unMappingAndType = self.vRefactor.vMapperMetaInfoMgr.fMappingAndTargetTypeFromSourceAndAllowedTypes( unAggregatedSource, someAggregatedTypes)
                                    if unMappingAndType:
                                        
                                        unMapping      = unMappingAndType[ 0]
                                        unTypeToCreate = unMappingAndType[ 1]
                                        
                                        if unTypeToCreate:
                                        
                                            unContainsCollections = self.vRefactor.vTargetMetaInfoMgr.fGetAggregationConfigContainsCollections( anAggregationTraversalConfig)

                                            if unContainsCollections:
                                                
                                                unaCollectionToMergeWith, aOverrideTitle = self.vRefactor.vTargetInfoMgr.fCollectionToMergeWith( theRefactorFrame.vTarget, unTypeToCreate, unAggregatedSource)
                                                
                                                if unaCollectionToMergeWith:
                                                    
                                                    if aOverrideTitle:
                                                        unAggregatedSourceTitle = self.vRefactor.vSourceInfoMgr.fGetTitle( unAggregatedSource)
                                                        
                                                        unNewTargetTitle = self.vRefactor.vTargetInfoMgr.fUniqueAggregatedTitle( theRefactorFrame.vTarget, unAggregatedSourceTitle)
                                                        if unNewTargetTitle:
                                                            unaCollectionToMergeWith.setTitle( unNewTargetTitle)

                                    
                                                    unaCollectionType       = self.vRefactor.vTargetMetaInfoMgr.fTypeName( unaCollectionToMergeWith)
                                                    unaCollectionTypeConfig = self.vRefactor.vTargetMetaInfoMgr.fTypeConfigForType( unaCollectionType)
                                                    
                                                    self.vRefactor.vMapperInfoMgr.pRegisterSourceToTargetCorrespondence( unAggregatedSource, unaCollectionToMergeWith, unMapping)
                                                    
                                                    unRefactorFrame = unRefactorStack.fAddRootStackFrame( self, unAggregatedSource, unaCollectionToMergeWith, unaCollectionTypeConfig, unMapping)
                                                    if unRefactorFrame:
                                                        try:
                                                            self.fRefactor_Frame( unRefactorFrame)
                                                        finally:
                                                            unRefactorStack.fPopStackFrame()
                                                        
                                                        continue
                                            
                                            
                                            
                                            unCreatedElementTypeConfig = self.vRefactor.vTargetMetaInfoMgr.fTypeConfigForTypeFromAggregationTraversalConfig( unTypeToCreate, anAggregationTraversalConfig, )
                                            if unCreatedElementTypeConfig:
                                                
                                                unCreatedAggregatedElement = self.vRefactor.vTargetInfoMgr.fCreateAggregatedElement( unAggregatedSource, theRefactorFrame.vTarget, unTypeToCreate, )
                                                if unCreatedAggregatedElement:
                                                    
                                                    self.vRefactor.vMapperInfoMgr.pRegisterSourceToTargetCorrespondence( unAggregatedSource, unCreatedAggregatedElement, unMapping)
                                                    
                                                    unSubRefactorFrame = unRefactorStack.fPushStackFrame( self, unAggregatedSource, unCreatedAggregatedElement, unCreatedElementTypeConfig, unMapping)
                                                    if unSubRefactorFrame:
                                                        try:
                                                            self.fRefactor_Frame( unSubRefactorFrame)
                                                        finally:
                                                            unRefactorStack.fPopStackFrame()
                                                
        return self
    
    
    
    
    
    
                        
    def fRefactor_Moves( self, ):
        """Delete source objects that have been copied and have the same root path as the target.
        If target root is same as source root or is under source root, then move is not possible (removing the source would remove the copies, too, loosing information).
        if source root is under target root, then move is possible.
        If there is no parent-child relationship between elements, then move is possible.
        
        """
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        
        unIsMoveOperation =  self.vRefactor.fGetContextParam( 'is_move_operation')
        if not unIsMoveOperation:
            return None
        
        unTargetRoot = self.vRefactor.vTargetInfoMgr.fGetTargetRoot()
        if ( unTargetRoot == None):
            return None

        unTargetRootPath = self.vRefactor.vTargetInfoMgr.fRootPath( unTargetRoot)
                
            
        unosTargets = self.vRefactor.vMapperInfoMgr.fGetTargets()
        if not unosTargets:
            return self
        
        for unTarget in unosTargets:
            
            unosSources = self.vRefactor.vMapperInfoMgr.fGetSourcesForTarget( unTarget)
            
            for unSource in unosSources:
                
                if not unSource in unosTargets:
                    
                    unSourcePath = self.vRefactor.vSourceInfoMgr.fGetPath( unSource)
                    
                    if not self.fPathIsSameOrParentPathOf( unSourcePath, unTargetRootPath):
                        
                        self.vRefactor.vSourceInfoMgr.fDeleteSource( unSource)
                    
        return self        
                         
    
    
    
        
    
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
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        
        unTargetRoot = self.vRefactor.vTargetInfoMgr.fGetTargetRoot()
        if ( unTargetRoot == None):
            return None


        unTargetRootPath = self.vRefactor.vTargetInfoMgr.fRootPath( unTargetRoot)
        
        unosTargets = self.vRefactor.vMapperInfoMgr.fGetTargets()
        if not unosTargets:
            return self
        
        for unTarget in unosTargets:
            
            unMapping = self.vRefactor.vMapperInfoMgr.fGetMappingForTarget( unTarget)
            
            unasTargetRelationTraversalConfigs = self.vRefactor.vTargetMetaInfoMgr.fRelationTraversalConfigsFromTarget( unTarget)
            if unasTargetRelationTraversalConfigs:
        
                unosSources = self.vRefactor.vMapperInfoMgr.fGetSourcesForTarget( unTarget)
                
                for unaTargetRelationTraversalConfig in unasTargetRelationTraversalConfigs:
                    
                    unRelationFieldName = self.vRefactor.vTargetMetaInfoMgr.fRelationNameFromTraversalConfig( unaTargetRelationTraversalConfig)
                    if unRelationFieldName:
                        
                        unTargetOwnerPath = ''
                        unRelationCandidatesScope = self.vRefactor.vTargetMetaInfoMgr.fCandidatesScopeFromRelationTraversalConfig( unaTargetRelationTraversalConfig)
                        if unRelationCandidatesScope.lower() == 'owner':
                            unTargetOwnerPath = self.vRefactor.vTargetInfoMgr.fOwnerPath( unTarget)
                            

                        someRelatedTypes = self.vRefactor.vTargetMetaInfoMgr.fRelatedTypesFromTraversalConfig( unaTargetRelationTraversalConfig)
                        if someRelatedTypes:
                        
                            allRelatedSources    = [ ]
                            allRelatedSourceUIDs = set()
                            
                            for unSource in unosSources:
                                if self.vRefactor.vSourceInfoMgr.fIsSourceOk( unSource):
                                    
                                    unSourceTraversalNameToRetrieve = self.vRefactor.vMapperMetaInfoMgr.fMappedTraversalNameFromSourceForTargetRelationName( unSource, unRelationFieldName, unMapping)
                                    if unSourceTraversalNameToRetrieve:
                                    
                                            unosRelatedSources = self.vRefactor.vSourceInfoMgr.fGetTraversalValues( unSource, unSourceTraversalNameToRetrieve, [])
                                            if unosRelatedSources:
                                                
                                                for unRelatedSource in unosRelatedSources:
                                                    if self.vRefactor.vSourceInfoMgr.fIsSourceOk( unRelatedSource):
                                                        
                                                        unRelatedSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( unRelatedSource)
                                                        if unRelatedSourceUID:
                                                            
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
                                            self.vRefactor.vTargetInfoMgr.fLink_Relation( unTarget, unosTargetsToBeRelatedOfRightType, unRelationFieldName)
                                    
                                    else:
                                        """Because the related source has not been refactored, the target is linked to the original related source.
                                        
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
                                                    self.vRefactor.vTargetInfoMgr.fLink_Relation( unTarget, [ unRelatedSourceObject, ], unRelationFieldName)
                
        return self        
                         
    
            
    
    
    
    
    
    
    
        
                        
        
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

        theOriginalRoot, 
        theNewVersionRoot,
        theNewVersionRootResult,
        theNewVersionName,
        theNewVersionComment,
        theTargetMDDTypeConfigs, 
        theTargetPloneTypeConfigs, 
        theTargetAllTypeConfigs):
        
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
            unInitialContextParms,
            MDDRefactor_NewVersion_SourceInfoMgr_MDDElements(), 
            MDDRefactor_NewVersion_SourceMetaInfoMgr_MDDElements(), 
            MDDRefactor_Paste_TargetInfoMgr_MDDElement(), 
            MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement(), 
            MDDRefactor_NewVersion_MapperInfoMgr_NoConversion(), 
            MDDRefactor_NewVersion_MapperMetaInfoMgr_NoConversion(), 
            MDDRefactor_NewVersion_Walker(), 
        )
    
        


        
    
class MDDRefactor_NewVersion_SourceMetaInfoMgr_MDDElements ( MDDRefactor_Role_SourceMetaInfoMgr):
    """
    
    """
    

    def fTypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unTypeName = theSource.meta_type
        return unTypeName
    
    
    def fGetArchetypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unArchetypeName = theSource.archetype_name
        return unArchetypeName
    
         

    def fPloneTypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if ( thePloneElement == None):
            return ''
        
        unMetaType = ''
        try:
            unMetaType = thePloneElement.meta_type
        except:
            None
            
        return unMetaType
    
    
    def fPloneArchetypeName( self, thePloneElement):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
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
            return ''
        
        
        if not theSource:
            return {}
        
        unTypeName = self.fTypeName( theSource)
        if not unTypeName:
            return {}
        
        unTypeConfig = self.fTypeConfigForType( unTypeName, theTypeConfigName)
        return unTypeConfig
    
    
    
    
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
            
            unAttributeName = unAttributeConfig.get( 'attribute_name', '')
            if unAttributeName and ( unAttributeName == theAttributeName):
                
                unAttributeType = unAttributeConfig.get( 'type', '')
                return unAttributeType
            
        return ''
                        
        
    
    

    
    
    
    
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
    
    
    
    
    def fGetSourceRoots( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        
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
            return False
        if ( theSource == None):
            return False
    
        return True
    
    
    
    
    def fIsSourceOk( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not theSource:
            return False
        
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
    
    

     
     
    
    # ACV 20091003 Should not be necessary. Copied from the XML flavor.
    #def fFromUnicodeToSystemEncoding( self, theXMLString,):
        
        #if not theXMLString:
            #return ''
        
        #if isinstance( theXMLString, unicode):
            #unStringUnicode = theXMLString
            
        #else:
            
            #unStringUnicode = None
            #try:
                #unStringUnicode = theXMLString.decode( cEncodingUTF8, errors=cEncodingErrorHandleMode_Strict)
            #except UnicodeDecodeError:
                #None
        
            #if not unStringUnicode:
                #return None
 
        #unSiteEncoding = self.fGetSiteEncoding()
        #if not unSiteEncoding:
            #unSiteEncoding = cEncodingUTF8
        
        #unStringEncoded  = None
        #try:
            #unStringEncoded = unStringUnicode.encode( unSiteEncoding, cEncodingErrorHandleMode_Strict)      
        #except UnicodeEncodeError:
            #None
                
        #if not unStringEncoded:
            #return None
        
        #return unStringEncoded
    
    
    
    
    
    def fGetId( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        
        unaId = theSource.getId()
        return unaId
        
    
    
    def fGetUID( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        
        if theSource.meta_type in cPloneSiteMetaTypes:
            return cFakeUIDForPloneSite
        
        unaUID = theSource.UID()
        return unaUID    
    
    
    
    def fGetPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        
        unPath = '/'.join( theSource.getPhysicalPath())
        return unPath    
     
    
    def fGetTitle( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        
        unTitle = theSource.Title()
        return unTitle    
    
    
    
    
    def fOwnerPath( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''        
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
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource):
            return ''
        unRootPath = '/'.join( theSource.getRaiz().getPhysicalPath())
        return unRootPath
    
    
    
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

        unSchema = None
        try:
            unSchema = theSource.schema
        except:
            None
        if not unSchema:
            return None
        
        if not unSchema.has_key( theAttributeName):
            return None
        
        unField  = unSchema[ theAttributeName]
        if not unField:
            return None
        
        unAccessor = unField.getAccessor( theSource)
        if not unAccessor:
            return None
        
        unAttributeValue = None
        try:
            unAttributeValue = unAccessor( )
        except:
            return None
 
        
        return unAttributeValue

            
    
    
    
    def fGetTraversalValues( self, theSource, theTraversalName, theAcceptedSourceTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized or not self.fIsSourceOk( theSource) or ( not theTraversalName):
            return []
        

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
            return None
 
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
      
    
    

    
    
    def fCreateAggregatedElement( self, theSource, theTarget, theMetaTypeToCreate, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
    
        unCreatedElement = MDDRefactor_Paste_TargetInfoMgr_MDDElement.fCreateAggregatedElement( self, theSource, theTarget, theMetaTypeToCreate, )
        if ( unCreatedElement == None):
            return None
        
        # ACV 200091003 Only the roots have version name
        #unNewVersionName = self.vRefactor.fGetContextParam( 'new_version_name',) 
        #if not unNewVersionName:
            #return unCreatedElement
        
        #unCreatedElement.setVersionInterna( unNewVersionName)
        
        #unNewVersionComment = self.vRefactor.fGetContextParam( 'new_version_comment',) 
        #if not unNewVersionComment :
            #return unCreatedElement
        #unCreatedElement.setComentarioVersionInterna( unNewVersionComment )
        
        return unCreatedElement
    
    
    
    
                        
    
class MDDRefactor_NewVersion_MapperInfoMgr_NoConversion ( MDDRefactor_Role_MapperInfoMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_MapperInfoMgr.__init__( self)
        
        self.vSourcesForTargetsMap = { }
        self.vTargetsForSourcesMap = { }
        self.vMappingsForTargets   = { }
        
        
        

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
            return None
      
        return theSourceValue
    
    
    

     
    
    def pRegisterSourceToTargetCorrespondence( self, theSource, theTarget, theMapping):
        
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return self
        
        if ( not theSource) or ( not theTarget):
            return self
     
        unSourceUID = self.vRefactor.vSourceInfoMgr.fGetUID( theSource)
        if not unSourceUID:
            return self
        
        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
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
            
        self.vMappingsForTargets[ unTargetUID] = theMapping
        
        
        
        
        # #######################################
        """ Link new version with its previous.
        
        """      
        unPreviousVersionsRelationName = self.vRefactor.fGetContextParam( 'previous_relation')        
        if unPreviousVersionsRelationName:
            aRelationsLibrary = self.vRefactor.fGetContextParam( 'relations_library')        
            if aRelationsLibrary:
                try:
                    gRelationsProcessor.process( aRelationsLibrary, connect=[( unTargetUID, unSourceUID, unPreviousVersionsRelationName ), ], disconnect=[])
                except:
                    None
            
            
            
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
                unSchema = None
                try:
                    unSchema = theSource.schema
                except:
                    None
                if unSchema and unSchema.has_key( unInterVersionFieldName):
                    unInterVersionField = unSchema[ unInterVersionFieldName]
                    if unInterVersionField:
                        unInterVersionFieldsCache[ unTypeName] = unInterVersionField
                        
        if unInterVersionField:
            unSourceAccessor = unInterVersionField.getAccessor( theSource)
            unSourceInterVersionUID = unSourceAccessor()
            if not unSourceInterVersionUID:
                unSourceInterVersionUID = theSource.UID()
                # ACV OJO 20091003 We are writing on the source, while creating a new version: 
                # may not be a good idea: we did not even check for write access to the source
                #unSourceMutator = unInterVersionField.getMutator( theSource)
                #unSourceMutator( unSourceInterVersionUID)
            
            unTargetMutator = unInterVersionField.getMutator( theTarget)
            unTargetMutator( unSourceInterVersionUID)
            #logging.getLogger( 'ModelDDvlPlone').info( 'target %s  unSourceInterVersionUID %s' % ( '/'.join( theTarget.getPhysicalPath()), unSourceInterVersionUID, ))
            
            
            
           
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
                unSchema = None
                try:
                    unSchema = theSource.schema
                except:
                    None
                if unSchema and unSchema.has_key( unChangeCounterFieldName):
                    unChangeCounterField = unSchema[ unChangeCounterFieldName]
                    if unChangeCounterField:
                        unChangeCounterFieldsCache[ unTypeName] = unChangeCounterField
                        
        if unChangeCounterField:
            unSourceAccessor = unChangeCounterField.getAccessor( theSource)
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
                unSchema = None
                try:
                    unSchema = theSource.schema
                except:
                    None
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
            try:
                unTargetMutator( unNewTargetSourcesCountersString)
            except:
                None
            #logging.getLogger( 'ModelDDvlPlone').info( 'target %s  SET unNewTargetSourcesCountersString %s' % ( '/'.join( theTarget.getPhysicalPath()), unNewTargetSourcesCountersString, ))
            #logging.getLogger( 'ModelDDvlPlone').info( 'target %s  GET unNewTargetSourcesCountersString %s' % ( '/'.join( theTarget.getPhysicalPath()), unTargetAccessor(), ))
            #logging.getLogger( 'ModelDDvlPlone').info( 'target %s  getContadoresDeFuentes() %s' % ( '/'.join( theTarget.getPhysicalPath()), theTarget.getContadoresDeFuentes(), ))

            #transaction.commit()
            
        return self
    
    
    
    
    def fGetMappingForTarget( self, theTarget):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        if not theTarget:
            return {}
        
        if not self.vMappingsForTargets:
            return {}

        unTargetUID = self.vRefactor.vTargetInfoMgr.fGetUID( theTarget)
        if not unTargetUID:
            return {}
        
        unMapping = self.vMappingsForTargets.get( unTargetUID, {})
        
        return unMapping
        
        
    def fGetTargets( self, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        
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
            return None

        if not theTarget:
            return None
        
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
            return None

        if not theSource:
            return None
        
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
            return self
        
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
            
        self.vMappingsForTargets[ unTargetUID] = None
        
        return self
    
    
    
    
    
    
    
    
    
class MDDRefactor_NewVersion_Walker ( MDDRefactor_Paste_Walker):
    """
    
    """
    
    
    
    def fInitInRefactor( self, theRefactor):
        return MDDRefactor_Paste_Walker.fInitInRefactor( self, theRefactor,)

       
    
    
    

    
    
    
    
    
class MDDRefactor_NewVersion_MapperMetaInfoMgr_NoConversion ( MDDRefactor_Role_MapperMetaInfoMgr):
    """
    
    """   
    def __init__( self, ):

        MDDRefactor_Role_MapperMetaInfoMgr.__init__( self)
        
        self.vMappingsByTargetTypeMap = { }
        
        
    
        
        
                
                
    def fFirstMappedTypeFromSourceTypeToTargetType( self, theSourceType, theTargetType, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSourceType or not theTargetType:
            return ''
        
        return theSourceType
    
    
    
                 
                
    def fCompileMappingFromSourceTypeToMappedType( self, theSourceType, theMappedType, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return {}
        
        return {}
        

    
    def fTargetAggregationConfigAndTypeToAggregateSourceIn( self, theSource, theTarget, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
        if not theSource or not theTarget:
            return []
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            return []
        
        unTargetType = self.vRefactor.vTargetMetaInfoMgr.fTypeName( theTarget)
        if not unTargetType:
            return []
        
        unasAggregationsWithType = self.vRefactor.vTargetMetaInfoMgr.fAggregationConfigsWithType( unTargetType, unSourceType)
        if not unasAggregationsWithType:
            return []
        
        return [ unasAggregationsWithType[ 0], unSourceType, ]
    
    
    
    
    def fMappingAndTargetAggregationConfigAndTypeToAggregateSourceIn( self, theSource, theTarget, ):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []
        
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
            
        return []
    
    
    
   
       
    def fSourceAttributeNameAndTypeForTargetNameAndType( self, theSource, theNameAndTypeToPopulate, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []

        return theNameAndTypeToPopulate
        

    
    
    def fMappedTraversalNameFromSourceForTargetAggregationName( self, theSource, theAggregationName, theMapping):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''

        return theAggregationName

   
    def fMappedTraversalNameFromSourceForTargetRelationName( self, theSource, theRelationName, theMapping,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''

        return theRelationName


    
    
    def fMappingAndTargetTypeFromSourceAndAllowedTypes( self, theSource, theAllowedTypes):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return []

        if not theSource or not theAllowedTypes:
            return []
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:    
            return []

        return [ None, unSourceType, ]

    
    
            
    
    def fTargetTypeFromSourceForTargetAggregationTraversalConfig( self, theSource, theTraversalConfig,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''

        if not theSource or not theTraversalConfig:
            return ''
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        return unSourceType
        
    
    
    
    def fTargetTypeFromSourceForTargetRelationTraversalConfig( self, theSource, theTraversalConfig,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''

        if not theSource or not theTraversalConfig:
            return ''
        
        unSourceType = self.vRefactor.vSourceMetaInfoMgr.fTypeName( theSource)
        if not unSourceType:        
            return ''
        
        unosAggregatedTypes = self.vRefactor.vTargetMetaInfoMgr.fRelatedTypesFromTraversalConfig( theTraversalConfig)
        if not unosAggregatedTypes:
            return ''
        
        if unSourceType in unosAggregatedTypes:
            return unSourceType
        
        return ''
        
                       
    def fTraversalNameFromSourceForTargetRelationConfig( self, theSource, theTraversalConfig):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''

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
        theMappingConfigs):
        
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
            unInitialContextParms,
            MDDRefactor_Import_SourceInfoMgr_XMLElements(), 
            MDDRefactor_Import_SourceMetaInfoMgr_XMLElements(), 
            MDDRefactor_Paste_TargetInfoMgr_MDDElement(), 
            MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement(), 
            MDDRefactor_Paste_MapperInfoMgr(), 
            MDDRefactor_Paste_MapperMetaInfoMgr_ConvertTypes(), 
            MDDRefactor_Import_Walker(), 
        )
    
        
            

class MDDRefactor_Import_SourceInfoMgr_XMLElements( MDDRefactor_Role_SourceInfoMgr):
    """
    
    """
    def fInitInRefactor( self, theRefactor):
        if not MDDRefactor_Role_SourceInfoMgr.fInitInRefactor( self, theRefactor,):
            return False
        
        if not self.vRefactor.fGetContextParam( 'zip_file',):
            return False
        
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
    
        
       

    
    def fGetSiteEncoding( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
        
        aSiteEncoding = self.vRefactor.fGetContextParam( 'site_encoding',)
        return aSiteEncoding
    
    
    
    
    def fGetSourceRoots( self,):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return None
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
            return False
        if ( theSource == None):
            return False
    
        return True
    
    
    
    
    def fIsSourceOk( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized or not theSource:
            return False
        
        allTypeConfigs = self.vRefactor.fGetContextParam( 'target_all_type_configs',)
        if not allTypeConfigs:
            return False
        
        unSourceType = theSource.nodeName
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
            return ''
        
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
            return ''
        
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
            unNodeName = unChildNode.nodeName
            if unNodeName and not ( unNodeName == cXMLElementName_CommentText):
                                
                if unNodeName == theAttributeName:
                    
                    unAttrValue = ''

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
                        pass
                    
                    
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
                        
                    elif unAttributeType in [ 'float', 'fixedpoint', ]:
                        unNumber = None
                        try:
                            unNumber = float( unAttrValue)                                               
                        except:
                            None
                        if not ( unNumber == None):
                            unAttrValue =  unNumber
                        
                    elif unAttributeType in [ 'datetime', 'date', ]:
                        unDate = None
                        try:
                            unDate = DateTime( unAttrValue)                                               
                        except:
                            None
                        if unDate:
                            unAttrValue =  unDate
                        
                    elif unAttributeType == 'file':
                        unFilePath = unAttrValue
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
        
        for unChildNode in unosChildNodes:
            unNodeName = unChildNode.nodeName
            if unNodeName and not ( unNodeName == cXMLElementName_CommentText):
                                
                if unNodeName == theTraversalName:
                    
                    unosRetrievedElements = [ ]
                    
                    unosAggregatedChildNodes = unChildNode.childNodes
                    if unosAggregatedChildNodes:
                        
                        for unAggregatedChildNode in unosAggregatedChildNodes:
                            
                            unAggregatedChildNodeName = unAggregatedChildNode.nodeName
                            
                            if not ( unAggregatedChildNodeName == cXMLElementName_CommentText):
                                if unAggregatedChildNode.nodeType == clsXMLNode.ELEMENT_NODE:
                                    if ( not theAcceptedSourceTypes) or ( unAggregatedChildNodeName in theAcceptedSourceTypes):
                                        unosRetrievedElements.append( unAggregatedChildNode)
                            
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

        unUnicodeTypeName = self.vRefactor.vSourceInfoMgr.fFromUnicodeToSystemEncoding( unTypeName) 
            
        return unUnicodeTypeName
    
    
    
    
    def fGetArchetypeName( self, theSource):
        if not self.vInitialized or not self.vRefactor.vInitialized:
            return ''
        
        if not theSource:
            return ''
        
        unArchetypeName = theSource.nodeName
        
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
            
            unAttributeName = unAttributeConfig.get( 'attribute_name', '')
            if unAttributeName and ( unAttributeName == theAttributeName):
                
                unAttributeType = unAttributeConfig.get( 'type', '')
                return unAttributeType
            
        return ''
                
                

    
    
    

        
    
class MDDRefactor_Import_Walker ( MDDRefactor_Paste_Walker):
    """
    
    """
    
    
    
    def fInitInRefactor( self, theRefactor):
        return MDDRefactor_Paste_Walker.fInitInRefactor( self, theRefactor,)

    
            
    
    
    