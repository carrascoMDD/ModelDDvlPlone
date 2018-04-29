# -*- coding: utf-8 -*-
#
# File: MDDRefactor_NewVersion.py
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


import time



from AccessControl             import ClassSecurityInfo



from Products.CMFCore          import permissions

from Products.CMFCore.utils    import getToolByName



from Products.Relations.config                  import RELATIONS_LIBRARY
from Products.Relations                         import processor            as  gRelationsProcessor



from PloneElement_TraversalConfig               import cPloneTypes

from ModelDDvlPloneTool_Refactor_Constants      import *
from ModelDDvlPloneTool_ImportExport_Constants  import *

from ModelDDvlPloneToolSupport                  import fEvalString, fReprAsString



from MDDRefactor           import MDDRefactor, MDDRefactor_Role_SourceInfoMgr, MDDRefactor_Role_SourceMetaInfoMgr, MDDRefactor_Role_TargetInfoMgr, MDDRefactor_Role_TargetMetaInfoMgr, MDDRefactor_Role_TimeSliceMgr, MDDRefactor_Role_TraceabilityMgr, MDDRefactor_Role_MapperInfoMgr, MDDRefactor_Role_MapperMetaInfoMgr, MDDRefactor_Role_Walker   
from MDDRefactor_Paste     import MDDRefactor_Paste_Walker, MDDRefactor_Paste_TargetInfoMgr_MDDElement, MDDRefactor_Paste_TargetMetaInfoMgr_MDDElement, MDDRefactor_Paste_MapperInfoMgr, MDDRefactor_Paste_MapperMetaInfoMgr_ConvertTypes
from MDDRefactor_Import    import MDDRefactor_Import_TimeSliceMgr


    
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
            MDDRefactor_Import_TimeSliceMgr(),
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
            #aSiteEncoding = cMDDEncodingUTF8
        
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
        
        unaIdentification = 'Title=%s; id=%s; path=%s UID=%s' % ( str( unTitle), str( unaId), str( unPath), str( unaUID),)

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
                        raise self.vRefactor.vExceptionToRaise, fReprAsString( anErrorReport)
                    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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
      
    
    
    def fAuditChanges( self,):
        
        unStack = self.vRefactor.vSetContextParam( 'stack', None)
        if ( unStack == None):
            return False
        
        if unStack.fIsSameElementAsRoot():
            return True
        
        return False

     
        
        
     
        

    
    
                        
    
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
                        unTargetSourcesCounters = fEvalString( unTargetSourcesCountersString)
                        if not unTargetSourcesCounters:
                            unTargetSourcesCounters = { }
                            if not ( unTargetSourcesCounters.__class__.__name__ == 'dict'):
                                unTargetSourcesCounters = { }
                    
                    unTargetSourcesCounters[ unSourceUID] = unSourceChangeCounter
                
                    unNewTargetSourcesCountersString = fReprAsString( unTargetSourcesCounters)    
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
                        raise self.vRefactor.vExceptionToRaise, fReprAsString( anErrorReport)
                    
    
    
                    
                
                
                
                
                
                
                
                
                
                
                
                    
    
    
    
                        
    
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
                        raise self.vRefactor.vExceptionToRaise, fReprAsString( anErrorReport)
                    
    
    
                
                
                
                
                
                
                
    
    
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
       
    
    
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

