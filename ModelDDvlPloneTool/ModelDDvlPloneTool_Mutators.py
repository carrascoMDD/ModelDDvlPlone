# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneMutators.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
#
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
#
# Authors: 
# Model Driven Development sl  Valencia (Spain) www.ModelDD.org 
# Antonio Carrasco Valero                       carrasco@ModelDD.org
#

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

import logging

from logging import ERROR as cLoggingLevel_ERROR

from DateTime import DateTime

from Acquisition  import aq_inner, aq_parent


from Products.CMFCore.exceptions import AccessControl_Unauthorized

from AccessControl      import ClassSecurityInfo

from Products.Archetypes.utils import shasattr

from Products.Archetypes.config import REFERENCE_CATALOG, UID_CATALOG



from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from Products.Relations.config                  import RELATIONS_LIBRARY
from Products.Relations                         import processor            as  gRelationsProcessor


from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Profiling       import ModelDDvlPloneTool_Profiling
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval       import ModelDDvlPloneTool_Retrieval
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Mutators_Plone  import ModelDDvlPloneTool_Mutators_Plone

from ModelDDvlPloneTool_Permissions_Definitions       import *










class ModelDDvlPloneTool_Mutators( ModelDDvlPloneTool_Profiling, ModelDDvlPloneTool_Mutators_Plone):
    """
    """
    security = ClassSecurityInfo()



 
    # #############################################################
    """Generic attribute mutators by name
    
    """


    
    
    security.declarePrivate( 'fNewVoidChangeValuesReport')
    def fNewVoidChangeValuesReport( self,):
        aReport = {
            'object_reports':        [],
            'impacted_objects_UIDs': [],
            'field_reports':         [],
            'field_reports_by_name': {},
        } 
        return aReport
 
   
    
    
    security.declarePrivate( 'pImpactChangeValuesIntoReport')
    def pImpactChangeValuesIntoReport( self, theChangedElement, theChangeReport):

        if theChangeReport == None:
            return self
        
        #unosImpactedObjects     = theChangeReport[ 'impacted_objects']
        unosImpactedObjectsUIDs = theChangeReport[ 'impacted_objects_UIDs']
        
        if theChangedElement == None:
            return self
        #if not ( theChangedElement in unosImpactedObjects):
            #unosImpactedObjects.append( theChangedElement)

        unaUIDChangedElement = ''
        try:
            unaUIDChangedElement = theChangedElement.UID()
        except:
            None
        if unaUIDChangedElement:
            if not ( unaUIDChangedElement in unosImpactedObjectsUIDs):
                unosImpactedObjectsUIDs.append( unaUIDChangedElement)
        

        aMustImpactContainerAndOwner = False
        aMustImpactPreviousAndNext   = False
        aMustImpactOwnedContents     = False
        aMustImpactAllContents       = False
        aMustImpactAllRelated        = False
        aMustImpactAllRelatedContainerAndOwners = False
        
        
        someFieldReports = theChangeReport.get( 'field_reports')   
        for aReportForField in someFieldReports:
            anAttributeName = aReportForField.get( 'attribute_name', '')
            if anAttributeName:
                if aReportForField.get( 'effect', '') == 'changed':
                    
                    if anAttributeName.lower() == 'id':
                        aMustImpactContainerAndOwner = True
                        aMustImpactPreviousAndNext   = True
                        aMustImpactOwnedContents     = True
                        aMustImpactAllContents       = True
                        aMustImpactAllRelated        = True
                        aMustImpactAllRelatedContainerAndOwners = True
                        break
                    
                    if anAttributeName.lower() == 'title':
                        aMustImpactContainerAndOwner = True
                        aMustImpactPreviousAndNext   = True
                        aMustImpactOwnedContents     = True
                        aMustImpactAllContents       = True
                        aMustImpactAllRelated        = True
                        aMustImpactAllRelatedContainerAndOwners = True
                        break
                    
                    if anAttributeName.lower() == 'description':
                        aMustImpactContainerAndOwner = True
                        aMustImpactPreviousAndNext   = True
                        aMustImpactOwnedContents     = True
                        aMustImpactAllRelated        = True
                        aMustImpactAllRelatedContainerAndOwners = True
                        continue
                        
                    aMustImpactAllRelated                   = True
                    aMustImpactAllRelatedContainerAndOwners = True
                   
                
        if aMustImpactContainerAndOwner or aMustImpactPreviousAndNext:
            
            unContenedor = self.fImpactChangedContenedorYPropietario_IntoReport( theChangedElement, theChangeReport)

            if not ( ( unContenedor == None) or ( unContenedor == theChangedElement)):
                
                if aMustImpactPreviousAndNext:
                    
                    unosSiblings = unContenedor.objectValues()
                    
                    if theChangedElement in unosSiblings:
                        
                        unIndexChangedElement = unosSiblings.index( theChangedElement)

                        unosSiblingsToImpact = [ ]
                        if ( unIndexChangedElement == 0) or ( unIndexChangedElement == (len( unosSiblings) - 1)):
                            unosSiblingsToImpact = unosSiblings[:]
                        else:
                            unosSiblingsToImpact = [ unosSiblings[ unIndexChangedElement - 1], unosSiblings[ unIndexChangedElement + 1], ]
                            
                        for unSiblingToImpact in unosSiblingsToImpact:
                            
                            #if not ( unSiblingToImpact in unosImpactedObjects):
                                #unosImpactedObjects.append( unSiblingToImpact)
                            
                            unaUIDSiblingToImpact = ''
                            try:
                                unaUIDSiblingToImpact = unSiblingToImpact.UID()
                            except:
                                None
                            if unaUIDSiblingToImpact:
                                if not ( unaUIDSiblingToImpact in unosImpactedObjectsUIDs):
                                    unosImpactedObjectsUIDs.append( unaUIDSiblingToImpact)
                
                                    
        if aMustImpactAllContents or aMustImpactOwnedContents:
            
            self.pImpactChangeValuesIntoReport_RecurseContents( theChangedElement, theChangeReport, aMustImpactAllContents)
            
            
        if aMustImpactAllRelated and unaUIDChangedElement:
                
            aReferenceCatalog = getToolByName( theChangedElement, REFERENCE_CATALOG, None)
            
            if aReferenceCatalog:
                
                someRelationsNotPropagatingViewInvalidation = []
                try:
                    someRelationsNotPropagatingViewInvalidation = theChangedElement.fRelationsNotPropagatingViewInvalidation( )
                except:
                    None
                if not someRelationsNotPropagatingViewInvalidation:
                    someRelationsNotPropagatingViewInvalidation = []
                
                allRelatedUIDs = []
                
                aTargetCatalogSearch = { 'sourceUID'  : unaUIDChangedElement,}
                aTargetsResults = aReferenceCatalog.searchResults( **aTargetCatalogSearch)
                for aTargetResult  in aTargetsResults:
                    aRelationName = aTargetResult[ 'relationship']
                    if not ( aRelationName in someRelationsNotPropagatingViewInvalidation):                   
                        aTargetUID = aTargetResult[ 'targetUID']
                        if not ( aTargetUID in unosImpactedObjectsUIDs):
                            unosImpactedObjectsUIDs.append( aTargetUID)
                        if not ( aTargetUID in allRelatedUIDs):
                            allRelatedUIDs.append( aTargetUID)
                        
                aSourceCatalogSearch = { 'targetUID'  : unaUIDChangedElement,}
                aSourcesResults = aReferenceCatalog.searchResults( **aSourceCatalogSearch)
                for aSourceResult  in aSourcesResults:
                    aRelationName = aSourceResult[ 'relationship']
                    if not ( aRelationName in someRelationsNotPropagatingViewInvalidation):                   
                        aSourceUID = aSourceResult[ 'sourceUID']
                        if not ( aSourceUID in unosImpactedObjectsUIDs):
                            unosImpactedObjectsUIDs.append( aSourceUID)
                        if not ( aSourceUID in allRelatedUIDs):
                            allRelatedUIDs.append( aSourceUID)

                            
                if aMustImpactAllRelatedContainerAndOwners:
                    
                    aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()                
                    
                    for aRelatedUID in allRelatedUIDs:
                        aRelatedElement = aModelDDvlPloneTool_Retrieval.fElementoPorUID( aRelatedUID, theChangedElement)
                        if not ( aRelatedElement == None):
                            
                            #if not ( aRelatedElement in unosImpactedObjects):
                                #unosImpactedObjects.append( aRelatedElement)
                                    
                            unVoid = self.fImpactChangedContenedorYPropietario_IntoReport( aRelatedElement, theChangeReport)
                            
                            
        return self
    
    
    
    
    
   
    security.declarePrivate( 'pImpactChangeValuesIntoReport_RecurseContents')
    def pImpactChangeValuesIntoReport_RecurseContents( self, theChangedElement, theChangeReport, theImpactAllContents=False):

        if theChangeReport == None:
            return self
        
        #unosImpactedObjects     = theChangeReport[ 'impacted_objects']
        unosImpactedObjectsUIDs = theChangeReport[ 'impacted_objects_UIDs']
        
        unosContentsElements = []
        try:
            unosContentsElements = theChangedElement.objectValues()
        except:
            None
        
        if not unosContentsElements:
            return self
        
        for unContentElement in unosContentsElements:
                    
            #if not ( unContentElement in unosImpactedObjects):
                #unosImpactedObjects.append( unContentElement)
            
            unaUIDContentElement = ''
            try:
                unaUIDContentElement = unContentElement.UID()
            except:
                None
            if unaUIDContentElement:
                if not ( unaUIDContentElement in unosImpactedObjectsUIDs):
                    unosImpactedObjectsUIDs.append( unaUIDContentElement)
                    
            unEsColeccion = False
            try:
                unEsColeccion = unContentElement.getEsColeccion()
            except:
                None

            if theImpactAllContents or unEsColeccion:
                
                unosSubContentsElements = unContentElement.objectValues()
                
                if unosSubContentsElements:
                    
                    for unSubContentElement in unosSubContentsElements:
                                
                        #if not ( unSubContentElement in unosImpactedObjects):
                            #unosImpactedObjects.append( unSubContentElement)
                        
                        unaUIDSubContentElement = ''
                        try:
                            unaUIDSubContentElement = unSubContentElement.UID()
                        except:
                            None
                        if unaUIDSubContentElement:
                            if not ( unaUIDSubContentElement in unosImpactedObjectsUIDs):
                                unosImpactedObjectsUIDs.append( unaUIDSubContentElement)
                                
                        if theImpactAllContents:
                            self.pImpactChangeValuesIntoReport_RecurseContents(  unSubContentElement, theChangeReport, True)                           
            
        return self
                                
                                
    

    
    
    
    security.declarePrivate( 'fImpactChangedContenedorYPropietario_IntoReport')
    def fImpactChangedContenedorYPropietario_IntoReport( self, theChangedElement, theChangeReport, ):

        if theChangeReport == None:
            return None
        
        unosImpactedObjectsUIDs = theChangeReport[ 'impacted_objects_UIDs']
        
        unContenedor = None
        try:
            unContenedor = theChangedElement.getContenedor()
        except:
            None
        if  not ( ( unContenedor == None) or ( unContenedor == theChangedElement)):
            unaUIDContenedor = ''
            try:
                unaUIDContenedor = unContenedor.UID()
            except:
                None
            if unaUIDContenedor:
                if not ( unaUIDContenedor in unosImpactedObjectsUIDs):
                    unosImpactedObjectsUIDs.append( unaUIDContenedor)
                    
    
        unPropietario = None
        try:
            unPropietario = theChangedElement.getPropietario()
        except:
            None
        if not ( ( unPropietario == None) or ( unPropietario == unContenedor)  or ( unPropietario == theChangedElement)):

            unaUIDPropietario = ''
            try:
                unaUIDPropietario = unPropietario.UID()
            except:
                None
            if unaUIDPropietario:
                if not ( unaUIDPropietario in unosImpactedObjectsUIDs):
                    unosImpactedObjectsUIDs.append( unaUIDPropietario)
                    
                 
        unosPropagateDeleteImpactTo = None
        try:
            unosPropagateDeleteImpactTo = theChangedElement.propagate_delete_impact_to
        except:
            None

            
            
        if unosPropagateDeleteImpactTo:
            
            for unPropagateDeleteImpactTo in unosPropagateDeleteImpactTo:
                
                if unPropagateDeleteImpactTo:
                    
                    unPropagateStep = unPropagateDeleteImpactTo[ 0]
                    if unPropagateStep == 'contenedor_contenedorYPropietario':
                        
                        if not ( unContenedor == None):
                            
                            unContenedor_Contenedor = None
                            try:
                                unContenedor_Contenedor = unContenedor.getContenedor()
                            except:
                                None
                            
                            if not ( unContenedor_Contenedor == None):   
                                unaUIDContenedor_Contenedor = ''
                                try:
                                    unaUIDContenedor_Contenedor = unContenedor_Contenedor.UID()
                                except:
                                    None
                                if unaUIDContenedor_Contenedor:
                                    if not ( unaUIDContenedor_Contenedor in unosImpactedObjectsUIDs):
                                        unosImpactedObjectsUIDs.append( unaUIDContenedor_Contenedor)
                            
                            
                            unContenedor_Propietario = None
                            try:
                                unContenedor_Propietario = unContenedor.getPropietario()
                            except:
                                None
                            
                            if not ( unContenedor_Propietario == None):   
                                unaUIDContenedor_Propietario = ''
                                try:
                                    unaUIDContenedor_Propietario = unContenedor_Propietario.UID()
                                except:
                                    None
                                if unaUIDContenedor_Propietario:
                                    if not ( unaUIDContenedor_Propietario in unosImpactedObjectsUIDs):
                                        unosImpactedObjectsUIDs.append( unaUIDContenedor_Propietario)
                                
        return unContenedor
                                    
    
            
    security.declarePrivate( 'fChangeValues')
    def fChangeValues(self , 
        theTimeProfilingResults =None,
        theElement              =None, 
        theNewValuesDict        =None,
        theAdditionalParams     =None):        

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fChangeValues', theTimeProfilingResults)

        try:

            if ( theElement == None) or not theNewValuesDict:
                return None

            aTranslationService = getToolByName( theElement, 'translation_service', None)            
             
            unValueForId = theNewValuesDict.get( 'attribute_id', '')
            
            unosNombresAtributos = [ unNombreAtributo for unNombreAtributo  in theNewValuesDict.keys() if unNombreAtributo.__class__.__name__ == 'str']
            if not ( unosNombresAtributos or unValueForId):
                return None
                
            unosPosiblesNombresAtributos = []
            for unNombreAtributo in unosNombresAtributos:
                unSubIndex = unNombreAtributo.find( '_sub_value_')
                if unSubIndex > 1:
                    otroNombreAtributo = unNombreAtributo[:unSubIndex]
                    unosPosiblesNombresAtributos.append( otroNombreAtributo)
                else:
                    unosPosiblesNombresAtributos.append( unNombreAtributo)
                          
            unResult = ModelDDvlPloneTool_Retrieval().fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'dynamic_vocabularies',],
                theWritePermissions         =[ 'object', 'attrs',],
                theFeatureFilters           ={ 'attrs': unosPosiblesNombresAtributos, 'aggregations' : [], 'relations' : [] }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =None,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unResult:
                return None
            someValueResults = unResult.get( 'values')
            if not ( someValueResults or unValueForId):
                return None
    
            unAnyAttributeChanged = False
            
            aReport = self.fNewVoidChangeValuesReport()
            someObjectReports   = aReport.get( 'object_reports')
            someFieldReports    = aReport.get( 'field_reports')
            aFieldReportsByName = aReport.get( 'field_reports_by_name')
            
            if not unResult.get( 'read_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_read_permission',}
                someObjectReports.append( aReportForObject)
                return aReport
            
            if not unResult.get( 'write_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_write_permission',}
                someObjectReports.append( aReportForObject)
                return aReport
            
            
            if unValueForId:
                
                unPortalPropertiesTool = getToolByName( theElement, 'portal_properties', None)
                if not ( unPortalPropertiesTool == None):
                    unSiteProperties = getattr( unPortalPropertiesTool, 'site_properties', None)
                    if not ( unSiteProperties == None):
                        unVisibleIds = unSiteProperties.getProperty('visible_ids')
                        if unVisibleIds:
                    
                            unCurrentId = unResult.get( 'id', '')
                            
                            if unCurrentId:
                            
                                aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
                                unCurrentIdResult = aModelDDvlPloneTool_Retrieval.fNewVoidValueResult()
                                unCurrentIdResult.update({ 
                                    'attribute_name':           'id', 
                                    'type':                     'string', 
                                    'computed':                 False,
                                    'attribute_config':         {   'name': 'id', 'kind': 'Data', 'type': 'String',},
                                    'attribute_translations':   { 'translated_label': aModelDDvlPloneTool_Retrieval.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_id_label', 'Identity-', theElement),},
                                    'vocabulary':               None,
                                    'raw_value':                unCurrentId, 
                                    'value':                    unCurrentId, 
                                    'uvalue':                   unCurrentId, 
                                    'translated_value':         unCurrentId,
                                    'vocabulary_translations':  None,
                                    'read_permission':          True,
                                    'write_permission':         True,
                                    'sub_values':               [ ],
                                    'sub_values_by_name':       { },            
                                })
            
                                
                                unNuevaId = unValueForId.replace( '\t',' ')
                                unNuevaId = unNuevaId.replace( '\r',' ')
                                unNuevaId = unNuevaId.replace( '\n',' ')
                                unNuevaId = unNuevaId.strip()
                                
                                unNuevaId = self.fAsEncodedFromUIToDB( unNuevaId, aTranslationService)
                                
                                unosExistingIds = [ ]
                                
                                unParent = aq_parent( aq_inner( theElement))
                                if unParent:
                                    unosExistingAggregatedElements = unParent.objectValues()
                                
                                    unosExistingIds    = [ unElement.getId() for unElement in unosExistingAggregatedElements]
                                    
                                aPloneToolForNormalizeString = getToolByName( theElement, 'plone_utils', None)
                                if aPloneToolForNormalizeString  and  shasattr( aPloneToolForNormalizeString, 'normalizeString'):
                                    unNuevaId = aPloneToolForNormalizeString.normalizeString( unNuevaId)
                                  
                                aReportForField = None                 
                                
                                unCurrentIdResult.update({ 
                                    'raw_value':                unNuevaId, 
                                    'value':                    unNuevaId, 
                                    'uvalue':                   unNuevaId, 
                                    'translated_value':         unNuevaId,
                                })
                                
                                if unNuevaId == unCurrentId:
                                    aReportForField = { 'attribute_name': 'id', 'effect': 'no_change',    'previous_value': unCurrentIdResult,}                        
                                elif unNuevaId in unosExistingIds:
                                    aReportForField = { 'attribute_name': 'id', 'effect': 'error', 'failure': 'duplicate_id', 'previous_value': unCurrentIdResult,}                        
                                else:
                                    unChanged = False
                                    try:
                                        aDisableLevel = logging.getLogger('Zope.ZCatalog').manager.disable
                                        logging.getLogger('Zope.ZCatalog').manager.disable = cLoggingLevel_ERROR
            
                                        try:
                                            theElement.setId( unNuevaId) 
                                            unChanged = True
                                        except:
                                            aReportForField = { 'attribute_name': 'id', 'effect': 'error', 'failure': 'invoking_mutator', 'new_value': unNuevaId, 'previous_value': unCurrentIdResult,}                                                                                                                        
                                    finally:
                                        logging.getLogger('Zope.ZCatalog').manager.disable = aDisableLevel
                                        
                                    if unChanged:
                                        unAnyAttributeChanged = True
                                        aReportForField = { 'attribute_name': 'id', 'effect': 'changed', 'new_value': unNuevaId, 'previous_value': unCurrentIdResult,}                                                                                                                        
                                        aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                                
                                
                                if aReportForField:
                                    someFieldReports.append( aReportForField)
                        
                                     
            for unValueResult in someValueResults:
                unAttributeName = unValueResult.get( 'attribute_name', '')
                unAttributeType = unValueResult.get( 'type', '').lower()
    
                aReportForField = None
                aInvokeMutator  = False
                unMutator       = None
                unNewValue      = None
                
                if unAttributeName and unAttributeType:
                    unEsDateSubValueChange = unAttributeType == 'datetime' and (  theNewValuesDict.has_key( '%s_sub_value_year' % unAttributeName) or theNewValuesDict.has_key( '%s_sub_value_month' % unAttributeName) or theNewValuesDict.has_key( '%s_sub_value_day_of_month' % unAttributeName) )
                    if theNewValuesDict.has_key( unAttributeName) or unEsDateSubValueChange:
                        if not unValueResult.get( 'read_permission', False):
                            aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'field_read_permission', 'previous_value': unValueResult,}
                        elif not unValueResult.get( 'write_permission', False):
                            aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'field_write_permission', 'previous_value': unValueResult,}
                        else:
                            if not unEsDateSubValueChange:        
                                unFormValue = theNewValuesDict.get( unAttributeName, None)    
                            
                            if not theElement.schema.has_key( unAttributeName):
                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'no_schema_field', 'previous_value': unValueResult,}                                                    
                            else:
                                unField  = theElement.schema[ unAttributeName]
                                if not unField:
                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'no_schema_field', 'previous_value': unValueResult,}                                                                                    
                                else:
                                    unMutator = unField.getMutator( theElement)
                                    if not unMutator:
                                        aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'no_field_mutator', 'previous_value': unValueResult,}                                                                                                                        
                                    else:
                                        unCurrentRawValue = unValueResult.get( 'raw_value', None)
                            
                                        if unAttributeType == 'string':
                                            
                                            unNewValue = unFormValue.replace( '\t',' ')
                                            unNewValue = unNewValue.replace( '\r',' ')
                                            unNewValue = unNewValue.replace( '\n',' ')
                                            unNewValue = unNewValue.strip()
                                                
                                            unNewValue = self.fAsEncodedFromUIToDB( unNewValue, aTranslationService)
                                            if unNewValue == unCurrentRawValue:
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                            else:
                                                aInvokeMutator = True
                                                
                                        elif unAttributeType == 'text':
                                            
                                            unNewValue = unFormValue.replace( '\r\n','\n')
                                            unNewValue = unNewValue.replace( '\r','\n')
                                            unNewValue = unNewValue.strip()
                                                
                                            unNewValue = self.fAsEncodedFromUIToDB( unNewValue, aTranslationService)
                                            if unNewValue == unCurrentRawValue:
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                            else:
                                                aInvokeMutator = True
    
    
                                        elif unAttributeType == 'integer':
                                            unNewValue = None
                                            try:
                                                unNewValue = int( unFormValue)    
                                            except ValueError:
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormValue,}                                                                                                                        
                                            if not( unNewValue == None):
                                                if unNewValue == unCurrentRawValue:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                                else:
                                                    aInvokeMutator = True
                                                    
                                        elif unAttributeType == 'float':
                                            unNewValue = None
                                            try:
                                                unNewValue = float( unFormValue)    
                                            except ValueError:
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormValue,}                                                                                                                        
                                            if not( unNewValue == None):
                                                if unNewValue == unCurrentRawValue:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                                else:
                                                    aInvokeMutator = True
     
                                        elif unAttributeType == 'boolean':
                                            unNewValue = unFormValue == '1'
                                            if unNewValue == unCurrentRawValue:
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                            else:
                                                aInvokeMutator = True
                                                #unMutator( unNewValue) 
                                                #unAnyAttributeChanged = True
                                                #aReportForField = { 'attribute_name': unAttributeName, 'effect': 'changed', 'new_value': unFormValue, 'previous_value': unValueResult,}                                                                                                                        
                                            
                                        elif unAttributeType == 'selection':
                                            unNewValue = unFormValue
                                            unVocabulary = unValueResult.get( 'vocabulary', [])
                                            if not unVocabulary:
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'no_vocabulary', 'previous_value': unValueResult, 'new_value': unFormValue, }                                                                                                                        
                                            elif not ( unFormValue in unVocabulary):
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'value_not_in_vocabulary', 'previous_value': unValueResult, 'new_value': unFormValue,}                                                                                                                       
                                            else:   
                                                if unNewValue == unCurrentRawValue:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                                else:
                                                    aInvokeMutator = True
                                        
                                        elif unAttributeType == 'datetime':
                                            unNewYearValue  = None
                                            unNewMonthValue = None
                                            unNewDayOfMonthValue = None
                                            aReportForField = None
                                            
                                            if theNewValuesDict.has_key( '%s_sub_value_year' % unAttributeName):
                                                unFormYearValue = theNewValuesDict.get( '%s_sub_value_year' % unAttributeName, None)                                             
                                                try:
                                                    unNewYearValue = int( unFormYearValue)    
                                                except ValueError:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'sub_value': 'year',  'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormYearValue,}                                                                                                                        
                                            
                                            if not aReportForField and theNewValuesDict.has_key( '%s_sub_value_month' % unAttributeName):
                                                unFormMonthValue = theNewValuesDict.get( '%s_sub_value_month' % unAttributeName, None)                                             
                                                try:
                                                    unNewMonthValue = int( unFormMonthValue)    
                                                except ValueError:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'sub_value': 'month',  'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormMonthValue,}                                                                                                                                                                
                                            
                                            if not aReportForField and theNewValuesDict.has_key( '%s_sub_value_day_of_month' % unAttributeName):
                                                unFormDayOfMonthValue = theNewValuesDict.get( '%s_sub_value_day_of_month' % unAttributeName, None)                                             
                                                try:
                                                    unNewDayOfMonthValue = int( unFormDayOfMonthValue)    
                                                except ValueError:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'sub_value': 'day_of_month',  'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormDayOfMonthValue,}                                                                                                                        
                                            
                                            if unNewYearValue or unNewMonthValue or unNewDayOfMonthValue:
                                                if unNewYearValue < 1:
                                                    unNewYearValue = 1900
                                                if ( unNewMonthValue < 1) or ( unNewMonthValue > 12):
                                                    unNewMonthValue = 1
                                                if ( unNewDayOfMonthValue < 1) or ( unNewMonthValue > 31):
                                                    unNewDayOfMonthValue = 1
                                                unNewDateValue = None
                                                try:
                                                    unNewDateValue = DateTime( unNewYearValue, unNewMonthValue, unNewDayOfMonthValue)   
                                                except:
                                                    None
                                                if not unNewDateValue:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult,'new_value': unNewDateValue,}                                                                                                                                                                    
                                                elif  unCurrentRawValue and ( unCurrentRawValue == unNewDateValue):
                                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                                else:
                                                    unNewValue = unNewDateValue
                                                    aInvokeMutator = True
                                                                                    
                if aInvokeMutator and unMutator and not ( unNewValue == None ):
                    unChanged = False
                    try:
                        unMutator( unNewValue) 
                        unChanged = True
                    except:
                        aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'invoking_mutator', 'new_value': unNewValue, 'previous_value': unValueResult,}                                                                                                                        

                    if unChanged:
                        unAnyAttributeChanged = True
                        aReportForField = { 'attribute_name': unAttributeName, 'effect': 'changed', 'new_value': unNewValue, 'previous_value': unValueResult,}                                                                                                                        
                    
                    
                if aReportForField:
                    someFieldReports.append( aReportForField)
                            
            for aReportForField in someFieldReports:
                aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                
                
            if unAnyAttributeChanged:
                
                self.pImpactChangeValuesIntoReport( theElement, aReport)
                
                self.pSetAudit_Modification( theElement)       
                
                try:
                    theElement.at_post_edit_script()
                except:
                    None
                    
                theElement.reindexObject()
                               
            return aReport
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fChangeValues', theTimeProfilingResults)
    
    
    




# #############################################################
# Content order mutators
#

                
    security.declarePrivate( 'fNewVoidLinkReport')
    def fNewVoidMoveSubObjectReport( self,):
        aReport = {
            'impacted_objects_UIDs':   [],
        } 
        return aReport
    
  
    
    
    security.declarePrivate( 'fMoveSubObject')
    def fMoveSubObject(self , 
        theTimeProfilingResults =None,
        theContainerElement     =None,  
        theTraversalName        =None, 
        theMovedObjectId        =None, 
        theMoveDirection        =None, 
        theAdditionalParams     =None):        
        """Change the order index of an element in the collection of elements aggregated in its container.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fMoveSubObject', theTimeProfilingResults)

        try:

            aMoveReport = self.fNewVoidMoveSubObjectReport()
            
            if ( theContainerElement == None)  or not  theTraversalName or not theMovedObjectId or not theMoveDirection or not ( theMoveDirection.lower() in ['up', 'down', 'top', 'bottom', ]):
                return aMoveReport
                        
            aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            unResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theContainerElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'aggregations', ],
                theFeatureFilters           ={ 'attrs': [], 'aggregations': [ theTraversalName,], 'relations': [], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =None,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unResult:
                return aMoveReport
        
            if not (  unResult[ 'read_permission'] and unResult[ 'write_permission']):
                return aMoveReport
    
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unResult, [ 'traversals',])

            unTraversalResult =  unResult[ 'traversals_by_name'].get( theTraversalName, None)
            if not unTraversalResult:
                return aMoveReport

            if not (  unTraversalResult[ 'traversal_kind'] == 'aggregation'):
                return aMoveReport
                
            if not (  unTraversalResult[ 'read_permission'] and unTraversalResult[ 'write_permission']):
                return aMoveReport
    
            someAllContainedObjects = theContainerElement.objectValues()
            
            someElementResults = unTraversalResult[ 'elements']
            someContainedObjects = [ unElement[ 'object'] for unElement in someElementResults]
            unNumContainedObjects = len( someElementResults)
            unResultToMove = None
            unDelta = None
            
            for aContainedObjectIndex in range( unNumContainedObjects):
                aContainedResult = someElementResults[ aContainedObjectIndex]
                aContainedObject = aContainedResult[ 'object']
                
                if aContainedObject.getId() == theMovedObjectId:
                                     
                    unDelta = None
                    if theMoveDirection.lower() == 'up':
                        if aContainedObjectIndex > 0:
                            unPreviousObjectIndex = aContainedObjectIndex - 1
                            unPreviousObject = someContainedObjects[ unPreviousObjectIndex]
                            unPreviousObjectIndexInAllContainedObjects = someAllContainedObjects.index( unPreviousObject)
                            unThisObjectIndexInAllContainedObjects = someAllContainedObjects.index( aContainedObject)
                            unDelta = unPreviousObjectIndexInAllContainedObjects - unThisObjectIndexInAllContainedObjects 
                            unResultToMove = aContainedResult
                    elif theMoveDirection.lower() == 'down':
                        if aContainedObjectIndex < ( unNumContainedObjects - 1):
                            unNextObjectIndex = aContainedObjectIndex + 1
                            unNextObject = someContainedObjects[ unNextObjectIndex]
                            unNextObjectIndexInAllContainedObjects = someAllContainedObjects.index( unNextObject )
                            unThisObjectIndexInAllContainedObjects = someAllContainedObjects.index( aContainedObject)
                            unDelta = unNextObjectIndexInAllContainedObjects - unThisObjectIndexInAllContainedObjects 
                            unResultToMove = aContainedResult
                    elif theMoveDirection.lower() == 'top':
                        unThisObjectIndexInAllContainedObjects = someAllContainedObjects.index( aContainedObject)
                        unDelta = 0 - unThisObjectIndexInAllContainedObjects
                        unResultToMove = aContainedResult
                    elif theMoveDirection.lower() == 'bottom':
                        unThisObjectIndexInAllContainedObjects = someAllContainedObjects.index( aContainedObject)
                        unDelta = unNumContainedObjects - unThisObjectIndexInAllContainedObjects - 1
                        unResultToMove = aContainedResult
    
                    break
                    
                    
            if unResultToMove and not ( unDelta == None):
                if not ( unResultToMove[ 'read_permission'] and unResultToMove[ 'write_permission']):
                    return aMoveReport
                
                self.pImpactMoveSubObjectIntoReport( theContainerElement, someContainedObjects, aMoveReport)
                
                theContainerElement.moveObjectsByDelta( [ theMovedObjectId, ], unDelta)

                self.pSetAudit_Modification( theContainerElement)       

            return aMoveReport
       
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fMoveSubObject', theTimeProfilingResults)
    
        
        
        
        


   
    
    security.declarePrivate( 'pImpactMoveSubObjectIntoReport')
    def pImpactMoveSubObjectIntoReport( self, theContainerElement, theContainedObjects, theMoveReport):
 
        if ( theContainerElement == None) or ( not theContainedObjects) or ( not theMoveReport):
            return self
    
         
        unosImpactedObjectsUIDs = theMoveReport[ 'impacted_objects_UIDs']
        
        unaUIDContainerElement = None
        try:
            unaUIDContainerElement = theContainerElement.UID()
        except:
            None
        if unaUIDContainerElement:
            if not ( unaUIDContainerElement in unosImpactedObjectsUIDs):
                unosImpactedObjectsUIDs.append( unaUIDContainerElement)

        for aContainedObject in theContainedObjects:
            if not ( aContainedObject == None):
                unaUIDContainedObject = None
                try:
                    unaUIDContainedObject = aContainedObject.UID()
                except:
                    None
                if unaUIDContainedObject:
                    if not ( unaUIDContainedObject in unosImpactedObjectsUIDs):
                        unosImpactedObjectsUIDs.append( unaUIDContainedObject)

        return self
    
            
        
        
        
                
        
 
    # #############################################################
    # Relation order mutators
    #



    security.declarePrivate( 'fMoveReferencedObject')
    def fMoveReferencedObject(self , 
        theTimeProfilingResults =None,
        theSourceElement        =None,  
        theReferenceFieldName   =None, 
        theMovedReferenceUID    =None, 
        theMoveDirection        =None,
        theAdditionalParams     =None):        
 
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fMoveReferencedObject', theTimeProfilingResults)

        try:

            if not theSourceElement or not  theReferenceFieldName or not theMovedReferenceUID or not theMoveDirection or not ( theMoveDirection.lower() in ['up', 'down', 'top', 'bottom', ]):
                return self
            
            aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            unResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theSourceElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'relations', ],
                theFeatureFilters           ={ 'attrs': [], 'aggregations': [], 'relations': [theReferenceFieldName], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =None,
                theAdditionalParams         =theAdditionalParams                
                
            )
            if not unResult:
                return self
        
            if not (  unResult[ 'read_permission'] and unResult[ 'write_permission']):
                return self
    
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unResult, [ 'traversals',])

            unTraversalResult =  unResult[ 'traversals_by_name'].get( theReferenceFieldName, None)
            if not unTraversalResult:
                return self
                
            if not (  unTraversalResult[ 'traversal_kind'] == 'relation'):
                return self

            if not (  unTraversalResult[ 'read_permission'] and unTraversalResult[ 'write_permission']):
                return self
              
            aRelationsLibrary = getToolByName( theSourceElement, RELATIONS_LIBRARY)        
            if not aRelationsLibrary:
                self.logError('ACV OJO failed to getToolByName RELATIONS_LIBRARY')
                return None
        
            someRelatedResults = unTraversalResult[ 'elements']
            unNumRelatedResults = len( someRelatedResults)
            if unNumRelatedResults < 2:
                return self

            unFoundRelatedResult= None
            unFoundRelatedIndex = 0
            for unRelatedIndex in range( unNumRelatedResults):
                unRelatedResult = someRelatedResults[ unRelatedIndex]
                if unRelatedResult:
                    if unRelatedResult[ 'UID'] == theMovedReferenceUID: 
                        unFoundRelatedResult = unRelatedResult
                        unFoundRelatedIndex = unRelatedIndex
                        break
    
            if not unFoundRelatedResult:
                return self           
        
            aMoveDirection = theMoveDirection.lower()
            
            someToUnlink = []
            someToLink   = []
    
            if aMoveDirection == 'top':
                if unFoundRelatedIndex < 1:
                    return self
                someToUnlink = [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults]
                someToLink =   [ unFoundRelatedResult[ 'UID'] ] + [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults if not (unRelatedResult == unFoundRelated)]
            
            elif aMoveDirection == 'up':
                if unFoundRelatedIndex < 1:
                    return self
                someToUnlink = [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex -1: unNumRelatedResults]]
                someToLink =   [ unFoundRelatedResult[ 'UID'], ] + [unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex - 1: unFoundRelatedIndex]] + [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex + 1: unNumRelatedResults]]
                    
            elif aMoveDirection == 'down':
                if unFoundRelatedIndex == (unNumRelatedResults - 1):
                    return self
                someToUnlink = [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex: unNumRelatedResults]]
                someToLink =   [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex + 1 : unFoundRelatedIndex + 2]] + [ unFoundRelatedResult[ 'UID'], ] + [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex + 2: unNumRelatedResults]]
                    
            elif aMoveDirection == 'bottom':
                if unFoundRelatedIndex == (unNumRelatedResults - 1):
                    return self
                someToUnlink = [ unFoundRelatedResult[ 'UID'], ]
                someToLink =   [ unFoundRelatedResult[ 'UID'], ] 
            
        
            if not someToLink and not someToUnlink:
                return self
                
            aSourceUID = unResult[ 'UID']
            
            unRelationship      = unTraversalResult[ 'relationship']
            someToConnect    = [ [ aSourceUID, anUID, unRelationship] for anUID in someToLink]
            someToDisconnect = [ [ aSourceUID, anUID, unRelationship] for anUID in someToUnlink]
                            
            
            self.pImpactMoveReferencedObjectIntoReport( theSourceElement, someRelatedResults, aMoveReport)
            

            gRelationsProcessor.process( aRelationsLibrary, connect= [],            disconnect=someToDisconnect)
            gRelationsProcessor.process( aRelationsLibrary, connect= someToConnect, disconnect=[])

            
            self.pSetAudit_Modification( theSourceElement)       
            
            return self

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fMoveReferencedObject', theTimeProfilingResults)

                
                
    security.declarePrivate( 'pImpactMoveReferencedObjectIntoReport')
    def pImpactMoveReferencedObjectIntoReport( self, theSourceElement, theRelatedResults, theMoveReport):
 
        if ( theSourceElement == None) or ( not theRelatedResults) or ( not theMoveReport):
            return self
    
        unosImpactedObjectsUIDs = theMoveReport[ 'impacted_objects_UIDs']

        unaUIDSourceElement = None
        try:
            unaUIDSourceElement = theSourceElement.UID()
        except:
            None
        if unaUIDSourceElement:
            if not ( unaUIDSourceElement in unosImpactedObjectsUIDs):
                unosImpactedObjectsUIDs.append( unaUIDSourceElement)
                
        unContenedorSource = self.fImpactChangedContenedorYPropietario_IntoReport( theSourceElement, theMoveReport)
        
        for aRelatedResult in theRelatedResults:
            anObject = aRelatedResult.get( 'object', None)
            if not ( anObject == None):
                anUID = anObject.UID()
                if anUID:
                    if not ( anUID in unosImpactedObjectsUIDs):
                        unosImpactedObjectsUIDs.append( anUID)
                        
        return self
    
            
            
            
    
    
    
                
                
    security.declarePrivate( 'fNewVoidLinkReport')
    def fNewVoidLinkReport( self,):
        aReport = {
            'impacted_objects_UIDs':   [],
            'source_object_reports':    [],
            'target_object_reports':    [],
            'link_reports':             [],
        } 
        return aReport
    
  
 


    security.declarePrivate( 'fLinkToUIDReferenceFieldNamed')
    def fLinkToUIDReferenceFieldNamed(self , 
        theTimeProfilingResults =None,
        theSourceElement        =None, 
        theReferenceFieldName   =None, 
        theTargetUID            =None,
        theAdditionalParams     =None):        
        """Link an element as related to another element.
        
        """


        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fLinkToUIDReferenceFieldNamed', theTimeProfilingResults)

        try:
    
            if not theSourceElement or not theReferenceFieldName or not theTargetUID:
                return None
      
            aReport = self.fNewVoidLinkReport()
            someSourceObjectReports = aReport[ 'source_object_reports']
            someTargetObjectReports = aReport[ 'target_object_reports']
            someLinkReports         = aReport[ 'link_reports']
            aFieldReportsByName     = {}
     
            
            unSchema = theSourceElement.schema
            if not unSchema.has_key( theReferenceFieldName):
                aReportForObject = { 'effect': 'error', 'failure': 'no_reference_field_name_in_schema',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
               
            unField             = unSchema[ theReferenceFieldName]
            if not unField:
                aReportForObject = { 'effect': 'error', 'failure': 'no_reference_field_in_schema',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
                
            unRelationName = ''
            try:
                unRelationName = unField.relationship
            except:
                None

            if not unRelationName:                
                aReportForLink = { 'effect': 'error', 'failure': 'no_relation_name_in_field',}
                someLinkReports.append( aReportForLink)
                return aReport

            unInverseRelationFieldName = ''
            try:
                unInverseRelationFieldName = unField.inverse_relation_field_name
            except:
                None

            unModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            unTranslationsCaches        = unModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()
            unCheckedPermissionsCache   = unModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                
            unSourceElementResult = unModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theSourceElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'relations', ],
                theFeatureFilters           ={ 'attrs': [], 'aggregations': [], 'relations': [ theReferenceFieldName, ], 'candidates_for_relations': [ theReferenceFieldName, ], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =unTranslationsCaches,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unSourceElementResult:
                aReportForObject = { 'effect': 'error', 'failure': 'retrieval_failure',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
            
            unSourceElementUID = unSourceElementResult.get( 'UID', '')
            if not unSourceElementUID:
                aReportForObject = { 'effect': 'error', 'failure': 'element result has no UID',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
            
            
            if not unSourceElementResult.get( 'read_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_read_permission',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
            
            if not unSourceElementResult.get( 'write_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_write_permission',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
         
            unModelDDvlPloneTool_Retrieval.pBuildResultDicts( unSourceElementResult, [ 'traversals', 'values',])

            unaSourceTraversalResult = unSourceElementResult[ 'traversals_by_name'].get( theReferenceFieldName, {})
            if not unaSourceTraversalResult:
                aReportForObject = { 'effect': 'error', 'failure': 'traversal_not_retrieved',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
                
            if unaSourceTraversalResult[ 'max_multiplicity_reached'] == True:
                aReportForObject = { 'effect': 'error', 'failure': 'max_multiplicity_reached',}
                someSourceObjectReports.append( aReportForObject)
                return aReport        
                
            unosRelatedElements = [ unRelatedResult[ 'object'] for unRelatedResult in unaSourceTraversalResult.get( 'elements', [])]                              
                
            unosCandidateElements = None
            unosCandidates = unaSourceTraversalResult.get( 'candidates', None)            
            if unosCandidates:
                unosCandidateElements = [ unCandidateResult[ 'object'] for unCandidateResult in unosCandidates.get( 'elements', [])]          
            
            unLimitToRelations = []
            if unInverseRelationFieldName:
                unLimitToRelations.append( unInverseRelationFieldName)
                
            unTargetElement = unModelDDvlPloneTool_Retrieval.fElementoPorUID( theTargetUID, theSourceElement)
            if not unTargetElement:
                aReportForObject = { 'effect': 'error', 'failure': 'get_by_uid_failure', }
                someTargetObjectReports.append( aReportForObject)
                return aReport    

            if unTargetElement in unosRelatedElements:
                aReportForObject = { 'effect': 'error', 'failure': 'target_already_linked', }
                someTargetObjectReports.append( aReportForObject)
                return aReport                            
                
            if not ( unosCandidateElements == None) and not ( unTargetElement in unosCandidateElements):
                aReportForObject = { 'effect': 'error', 'failure': 'target_not_in_candidates', }
                someTargetObjectReports.append( aReportForObject)
                return aReport                            
                        
            unTargetElementResult = unModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =unTargetElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'relations', ],
                theFeatureFilters           ={ 'attrs': [], 'aggregations': [], 'relations': unLimitToRelations, }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =unTranslationsCaches,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unTargetElementResult:
                aReportForObject = { 'effect': 'error', 'failure': 'retrieval_failure', }
                someTargetObjectReports.append( aReportForObject)
                return aReport
                            
            
            if not unTargetElementResult.get( 'read_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_read_permission', }
                someTargetObjectReports.append( aReportForObject)
                return aReport
            

            if unInverseRelationFieldName:
                
                unModelDDvlPloneTool_Retrieval.pBuildResultDicts( unTargetElementResult, [ 'traversals','values',])

                unaTargetTraversalResult = unTargetElementResult[ 'traversals_by_name'].get( unInverseRelationFieldName, {})
                if not unaTargetTraversalResult:
                    aReportForObject = { 'effect': 'error', 'failure': 'traversal_not_retrieved',}
                    someTargetObjectReports.append( aReportForObject)
                    return aReport
                    
                if unaTargetTraversalResult[ 'max_multiplicity_reached'] == True:
                    aReportForObject = { 'effect': 'error', 'failure': 'max_multiplicity_reached',}
                    someTargetObjectReports.append( aReportForObject)
                    return aReport            

                if not unaTargetTraversalResult.get( 'read_permission', False):
                    aReportForObject = { 'effect': 'error', 'failure': 'traversal_read_permission',}
                    someTargetObjectReports.append( aReportForObject)
                    return aReport
                
                if not unaTargetTraversalResult.get( 'write_permission', False):
                    aReportForObject = { 'effect': 'error', 'failure': 'traversal_write_permission',}
                    someTargetObjectReports.append( aReportForObject)
                    return aReport

                if not unaTargetTraversalResult[ 'dependency_supplier']:
                    if not unTargetElementResult.get( 'write_permission', False):
                        aReportForObject = { 'effect': 'error', 'failure': 'object_write_permission', }
                        someTargetObjectReports.append( aReportForObject)
                        return aReport
                
            
            if unField.__class__.__name__ == "RelationField":
                aRelationsLibrary = getToolByName( theSourceElement, RELATIONS_LIBRARY)        
                if not aRelationsLibrary:
                    aReportForLink = { 'effect': 'error', 'failure': 'getToolByName RELATIONS_LIBRARY',}
                    someLinkReports.append( aReportForLink)
                    return aReport

                
                
                
                gRelationsProcessor.process( aRelationsLibrary, connect=[( unSourceElementUID, theTargetUID, unRelationName ), ], disconnect=[])
                
                self.pImpactLinkIntoReport( theSourceElement, unSourceElementUID, theReferenceFieldName, unRelationName, unTargetElement, theTargetUID, aReport)

                
                
                if not unaSourceTraversalResult.get( 'dependency_supplier', False):
                    unSourceObject = unSourceElementResult.get( 'object', None)
                    if not ( unSourceObject == None):
                        self.pSetAudit_Modification( unSourceObject)       

                if not unaTargetTraversalResult.get( 'dependency_supplier', False):
                    unTargetObject = unTargetElementResult.get( 'object', None)
                    if not ( unTargetObject == None):
                        self.pSetAudit_Modification( unTargetObject)
                 
                        
                aReportForLink = { 'effect': 'linked', 'source': unSourceElementResult, 'target': unTargetElementResult, 'relation': unRelationName}
                someLinkReports.append( aReportForLink)
                return aReport

            else:
                
                theSourceElement.addReference( unTargetElement, unRelationName)
                
                self.pImpactReferenceIntoReport( theSourceElement, unSourceElementUID, theReferenceFieldName, unRelationName, aReport)

                
                
                if not unaSourceTraversalResult.get( 'dependency_supplier', False):
                    unSourceObject = unSourceElementResult.get( 'object', None)
                    if not ( unSourceObject == None):
                        self.pSetAudit_Modification( unSourceObject)       

                aReportForLink = { 'effect': 'linked', 'source': unSourceElementResult, 'target': unTargetElementResult, 'relation': unRelationName}
                someLinkReports.append( aReportForLink)
                return aReport
            
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fLinkToUIDReferenceFieldNamed', theTimeProfilingResults)

                
                

    
   
    
    security.declarePrivate( 'pImpactLinkIntoReport')
    def pImpactLinkIntoReport( self, theSourceElement, theSourceElementUID, theReferenceFieldName, theRelationName, theTargetElement, theTargetElementUID, theChangeReport):
 
        if ( theSourceElement == None) or ( theTargetElement == None) or ( not theSourceElementUID) or ( not theTargetElementUID) or (not theChangeReport):
            return self
    
        unosImpactedObjectsUIDs = theChangeReport[ 'impacted_objects_UIDs']

        if not ( theSourceElementUID in unosImpactedObjectsUIDs):
            unosImpactedObjectsUIDs.append( theSourceElementUID)
            
        unContenedorSource = self.fImpactChangedContenedorYPropietario_IntoReport( theSourceElement, theChangeReport)
        
        
        if not ( theTargetElementUID in unosImpactedObjectsUIDs):
            unosImpactedObjectsUIDs.append( theTargetElementUID)
            
        unContenedorTarget = self.fImpactChangedContenedorYPropietario_IntoReport( theTargetElement, theChangeReport)

        return self
    
            
            
            
            
            
            
            
    
    
    
    
    security.declarePrivate( 'pImpactReferenceIntoReport')
    def pImpactReferenceIntoReport( self, theSourceElement, theSourceElementUID, theReferenceFieldName, theRelationName, theReport):
 
        if ( theSourceElement == None) or ( not theSourceElementUID) or ( not theTargetElementUID) or (not theChangeReport):
            return self
    
         
        unosImpactedObjectsUIDs = theChangeReport[ 'impacted_objects_UIDs']
        
        if theSourceElement == None:
            return self
        
        if not ( theSourceElementUID in unosImpactedObjectsUIDs):
            unosImpactedObjectsUIDs.append( theSourceElementUID)
            
        unContenedorSource = self.fImpactChangedContenedorYPropietario_IntoReport( theSourceElement, theChangeReport)
        
        return self
    
        
    
    
                  
       
    security.declarePrivate( 'fNewVoidUnlinkReport')
    def fNewVoidUnlinkReport( self,):
        return self.fNewVoidLinkReport()
    
   



    security.declarePrivate( 'fUnlinkFromUIDReferenceFieldNamed')
    def fUnlinkFromUIDReferenceFieldNamed(self , 
        theTimeProfilingResults =None,
        theSourceElement              =None, 
        theReferenceFieldName   =None, 
        theTargetUID            =None,
        theAdditionalParams     =None):        
        """Unink an element from another related element.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fUnlinkFromUIDReferenceFieldNamed', theTimeProfilingResults)

        try:
    
            if not theSourceElement or not theReferenceFieldName or not theTargetUID:
                return None
      
            
            
            aReport = self.fNewVoidUnlinkReport()
            someSourceObjectReports = aReport[ 'source_object_reports']
            someTargetObjectReports = aReport[ 'target_object_reports']
            someLinkReports         = aReport[ 'link_reports']
            aFieldReportsByName     = {}
                 
            
            unSchema = theSourceElement.schema
            if not unSchema.has_key( theReferenceFieldName):
                aReportForObject = { 'effect': 'error', 'failure': 'no_reference_field_name_in_schema',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
               
            unField             = unSchema[ theReferenceFieldName]
            if not unField:
                aReportForObject = { 'effect': 'error', 'failure': 'no_reference_field_in_schema',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
                
            unRelationName = ''
            try:
                unRelationName = unField.relationship
            except:
                None

            if not unRelationName:                
                aReportForLink = { 'effect': 'error', 'failure': 'no_relation_name_in_field',}
                someLinkReports.append( aReportForLink)
                return aReport

            unInverseRelationFieldName = ''
            try:
                unInverseRelationFieldName = unField.inverse_relation_field_name
            except:
                None

            unModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            unTranslationsCaches        = unModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()
            unCheckedPermissionsCache   = unModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()

            unSourceElementResult = unModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theSourceElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'relations', ],
                theFeatureFilters           ={ 'attrs': [], 'aggregations': [], 'relations': [ theReferenceFieldName], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =unTranslationsCaches,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unSourceElementResult:
                aReportForObject = { 'effect': 'error', 'failure': 'retrieval_failure',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
            
            unSourceElementUID = unSourceElementResult.get( 'UID', '')
            if not unSourceElementUID:
                aReportForObject = { 'effect': 'error', 'failure': 'element result has no UID',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
            
            
            if not unSourceElementResult.get( 'read_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_read_permission',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
            
            if not unSourceElementResult.get( 'write_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_write_permission',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
         
            unModelDDvlPloneTool_Retrieval.pBuildResultDicts( unSourceElementResult, [ 'traversals','values',])
            
            unaSourceTraversalResult = unSourceElementResult[ 'traversals_by_name'].get( theReferenceFieldName, {})
            if not unaSourceTraversalResult:
                aReportForObject = { 'effect': 'error', 'failure': 'traversal_not_retrieved',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
                
            unosRelatedElements = [ unRelatedResult[ 'object'] for unRelatedResult in unaSourceTraversalResult.get( 'elements', [])]          
            
            unLimitToRelations = []
            if unInverseRelationFieldName:
                unLimitToRelations.append( unInverseRelationFieldName)

            unTargetElement = unModelDDvlPloneTool_Retrieval.fElementoPorUID( theTargetUID, theSourceElement)
            if not unTargetElement:
                aReportForObject = { 'effect': 'error', 'failure': 'get_by_uid_failure', }
                someTargetObjectReports.append( aReportForObject)
                return aReport    
                
            if not ( unTargetElement in unosRelatedElements):
                aReportForObject = { 'effect': 'error', 'failure': 'target_not_in_related_elements', }
                someTargetObjectReports.append( aReportForObject)
                return aReport                            
                        
            unTargetElementResult = unModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =unTargetElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'relations', ],
                theFeatureFilters           ={ 'attrs': [], 'aggregations': [], 'relations': unLimitToRelations, }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =unTranslationsCaches,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unTargetElementResult:
                aReportForObject = { 'effect': 'error', 'failure': 'retrieval_failure', }
                someTargetObjectReports.append( aReportForObject)
                return aReport
                            
            
            if not unTargetElementResult.get( 'read_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_read_permission', }
                someTargetObjectReports.append( aReportForObject)
                return aReport
            
            if not unTargetElementResult.get( 'write_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_write_permission', }
                someTargetObjectReports.append( aReportForObject)
                return aReport

            if unInverseRelationFieldName:
                unModelDDvlPloneTool_Retrieval.pBuildResultDicts( unTargetElementResult, [ 'traversals','values',])
                
                unaTargetTraversalResult = unTargetElementResult[ 'traversals_by_name'].get( unInverseRelationFieldName, {})
                if not unaTargetTraversalResult:
                    aReportForObject = { 'effect': 'error', 'failure': 'traversal_not_retrieved',}
                    someTargetObjectReports.append( aReportForObject)
                    return aReport
        
                if not unaTargetTraversalResult.get( 'read_permission', False):
                    aReportForObject = { 'effect': 'error', 'failure': 'traversal_read_permission',}
                    someTargetObjectReports.append( aReportForObject)
                    return aReport
                
                if not unaTargetTraversalResult.get( 'write_permission', False):
                    aReportForObject = { 'effect': 'error', 'failure': 'traversal_write_permission',}
                    someTargetObjectReports.append( aReportForObject)
                    return aReport
                
                if not unaTargetTraversalResult[ 'dependency_supplier']:
                    if not unTargetElementResult.get( 'write_permission', False):
                        aReportForObject = { 'effect': 'error', 'failure': 'object_write_permission', }
                        someTargetObjectReports.append( aReportForObject)
                        return aReport
                
            
            if unField.__class__.__name__ == "RelationField":
                aRelationsLibrary = getToolByName( theSourceElement, RELATIONS_LIBRARY)        
                if not aRelationsLibrary:
                    aReportForLink = { 'effect': 'error', 'failure': 'getToolByName RELATIONS_LIBRARY',}
                    someLinkReports.append( aReportForLink)
                    return aReport
                    
                
                self.pImpactUnLinkIntoReport( theSourceElement, unSourceElementUID, theReferenceFieldName, unRelationName, unTargetElement, theTargetUID, aReport)
                
                
                gRelationsProcessor.process( aRelationsLibrary, connect=[], disconnect=[( unSourceElementUID, theTargetUID, unRelationName ), ])

                
                
                if not unaSourceTraversalResult.get( 'dependency_supplier', False):
                    unSourceObject = unSourceElementResult.get( 'object', None)
                    if not ( unSourceObject == None):
                        self.pSetAudit_Modification( unSourceObject)       

                if not unaTargetTraversalResult.get( 'dependency_supplier', False):
                    unTargetObject = unTargetElementResult.get( 'object', None)
                    if not ( unTargetObject == None):
                        self.pSetAudit_Modification( unTargetObject)                       
                
                aReportForLink = { 'effect': 'unlinked', 'source': unSourceElementResult, 'target': unTargetElementResult, 'relation': unRelationName}
                someLinkReports.append( aReportForLink)
                return aReport

            else:
                
                
                theSourceElement.deleteReference( unTargetElement, unRelationName)
                                
                self.pImpactReferenceIntoReport( theSourceElement, unSourceElementUID, theReferenceFieldName, unRelationName, aReport)
                
                
                                
                if not unaSourceTraversalResult.get( 'dependency_supplier', False):
                    unSourceObject = unSourceElementResult.get( 'object', None)
                    if not ( unSourceObject == None):
                        self.pSetAudit_Modification( unSourceObject)       
                
                aReportForLink = { 'effect': 'unlinked', 'source': unSourceElementResult, 'target': unTargetElementResult, 'relation': unRelationName}
                someLinkReports.append( aReportForLink)
                return aReport
            
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fUnlinkFromUIDReferenceFieldNamed', theTimeProfilingResults)

    

                
                
                  
    security.declarePrivate( 'pImpactUnLinkIntoReport')
    def pImpactUnLinkIntoReport( self, theSourceElement, theSourceElementUID, theReferenceFieldName, theRelationName, theTargetElement, theTargetElementUID, theChangeReport):
        return self.pImpactLinkIntoReport( theSourceElement, theSourceElementUID, theReferenceFieldName, theRelationName, theTargetElement, theTargetElementUID, theChangeReport)
 
       
 
    
    
    
    
    
    
    # #############################################################
    # Creation methods
    #

            
 
            
    security.declarePrivate( 'fAreVisibleIds')
    def fAreVisibleIds(self,):
        """here/portal_properties/site_properties/visible_ids
        
        """
        pass
            
                             
                             
    security.declarePrivate( 'fCrearElementoDeTipo')
    def fCrearElementoDeTipo(self, 
        theTimeProfilingResults =None,
        theContainerElement      =None, 
        theTypeName             ='', 
        theId                   =None,
        theTitle                ='', 
        theDescription          ='',
        theAdditionalParams     =None,
        theAllowFactoryMethods  =False,
        theTranslationService   =None,):           
        """Create a new contained element of a type.
        
        """
        
        
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fCrearElementoDeTipo', theTimeProfilingResults)

        try:

            if ( theContainerElement == None)  or not  theTypeName or not theTitle:
                anActionReport = { 'effect': 'error', 'failure': 'required_parameters_missing', }
                return anActionReport     
                
            unTranslationService = theTranslationService
            if not unTranslationService:
                try:
                    unTranslationService = theContainerElement.translation_service
                except:
                    None

            unTitle = theTitle
            if unTranslationService:
                unTitle = unTranslationService.encode( unTitle)

            unaDescription = theDescription
            if unTranslationService:
                unaDescription = unTranslationService.encode( unaDescription)
            
            unModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            unTranslationsCaches = unModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()
            unCheckedPermissionsCache = unModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                        
            unResultadoContenedor = unModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theContainerElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'aggregations', 'add', 'add_collection',],
                theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                theInstanceFilters          =None,
                theTranslationsCaches       =unTranslationsCaches,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams
            )
            if not unResultadoContenedor:
                anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                return anActionReport     
        
            if not unResultadoContenedor[ 'read_permission']:
                anActionReport = { 'effect': 'error', 'failure': 'read_permission', }
                return anActionReport     
            
            if not unResultadoContenedor[ 'write_permission']:
                anActionReport = { 'effect': 'error', 'failure': 'write_persmission', }
                return anActionReport     
        
            if not unResultadoContenedor[ 'add_permission']:
                anActionReport = { 'effect': 'error', 'failure': 'add_persmission', }
                return anActionReport     
                
            if theAllowFactoryMethods:
                unNombreFactoryMethod = unResultadoContenedor.get( 'factory_methods', {}).get( theTypeName, '')            
                if unNombreFactoryMethod:
                    unFactoryMethod = None
                    try:
                        unFactoryMethod = theContainerElement[ unNombreFactoryMethod]
                    except:
                        None
                    if unFactoryMethod and unFactoryMethod.__class__.__name__ == 'instancemethod':
                        return unFactoryMethod( theTimeProfilingResults, self, theTypeName, unTitle, unaDescription, theAdditionalParams)

             
            unResultadoEncontrado = None
            for unaTraversalResult in unResultadoContenedor.get( 'traversals', []):
                unosElementsResults = unaTraversalResult.get( 'elements', [])  
                for unElementResult in unosElementsResults:
                    
                    unTitleValueResult = None
                    unosValueResults = unElementResult[ 'values']
                    for unValueResult in unosValueResults:
                        unAttributeName = unValueResult.get( 'attribute_name', '')
                        if unAttributeName and ( unAttributeName == 'title'):
                            unTitleValueResult = unValueResult
                            break
                            
                    if unTitleValueResult and ( unTitle == unTitleValueResult[ 'value']):
                        unResultadoEncontrado           = unElementResult  
                        anActionReport = { 'effect': 'error', 'failure': 'duplicate_title', }
                        return anActionReport     
                
                    
            unaFoundFactoryTypeName = False
            for unaTraversalResult in unResultadoContenedor.get( 'traversals', []):
                unasFactoriesAndTranslations = unaTraversalResult[ 'factories']
                for unaFactoryAndTranslations in unasFactoriesAndTranslations:
                    if theTypeName == unaFactoryAndTranslations[ 'meta_type']:
                        unaFoundFactoryTypeName = True
                        break                    
            if not unaFoundFactoryTypeName:
                anActionReport = { 'effect': 'error', 'failure': 'content_type_not_allowed', }
                return anActionReport     
                                
            
            if theId:
                aNewId = theId
                aNewId.replace(" ", "-")
            else:
                aNewId = unTitle.lower()

            if unTranslationService:
                aNewId = unTranslationService.encode( aNewId)

     
            aPloneTool = getToolByName( theContainerElement, 'plone_utils', None)
            if aPloneTool  and  shasattr( aPloneTool, 'normalizeString'):
                aNewId = aPloneTool.normalizeString( aNewId)
                
            someIds = []
            for unaTraversalResult in unResultadoContenedor.get( 'traversals', []):
                unosElementsResults = unaTraversalResult.get( 'elements', [])  
                for unElementResult in unosElementsResults:
                    unaId = unElementResult[ 'id']
                    if not ( unaId in someIds):
                        someIds.append( unaId)
                        
            aNewIdWithCounter = aNewId
            aCounter = 0
            aRetry = True
            while aNewIdWithCounter in someIds:
                aCounter = aCounter + 1
                aNewIdWithCounter = "%s-%d" % ( aNewId, aCounter)

                
            anAttrsDict = { 
                'title':        unTitle,
                'description':  unaDescription,
            }
            
            theContainerElement.invokeFactory( theTypeName, aNewIdWithCounter, **anAttrsDict)
            
            
            unNuevoResultadoContenedor = unModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theContainerElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =None,
                theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                theInstanceFilters          =None,
                theTranslationsCaches       =unTranslationsCaches,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unNuevoResultadoContenedor:
                anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                return anActionReport     

            unResultadoNuevoElementoEncontrado = None
            for unaTraversalResult in unNuevoResultadoContenedor.get( 'traversals', []):
                unosElementsResults = unaTraversalResult.get( 'elements', [])  
                for unElementResult in unosElementsResults:
                    if  unElementResult[ 'id'] == aNewIdWithCounter:
                        unResultadoNuevoElementoEncontrado = unElementResult
                        break
                    
            if not unResultadoNuevoElementoEncontrado:
                anActionReport = { 'effect': 'error', 'failure': 'factory_failure', }
                return anActionReport     
            
            aNewObject = unResultadoNuevoElementoEncontrado[ 'object']     
            
            aNewObject.manage_fixupOwnershipAfterAdd()
            
            self.pSetElementPermissions( aNewObject)
            
            self.pSetAudit_Creation( aNewObject)       
                            
                            
                

            anActionReport = { 'effect': 'created', 'new_object_result': unResultadoNuevoElementoEncontrado, }
            
            unResultadoNuevoElemento = unModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =aNewObject, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'attrs', 'aggregations', ],
                theFeatureFilters           ={ 'relations': [], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =unTranslationsCaches,
                theCheckedPermissionsCache  =unCheckedPermissionsCache,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unResultadoNuevoElemento:
                # OJO ACV 20081023 Creation of new element went ok. 
                # With this retrieval failure (who knows why?) 
                # just cant initialize attributes and collection contents
                # Return the "ok" report
                #  anActionReport = { 'effect': 'error', 'failure': 'retrieval_failure', }
                return anActionReport     
            
            for unaTraversalResult in unResultadoNuevoElemento.get( 'traversals', []):
                if ( unaTraversalResult[ 'traversal_kind'] == 'aggregation') and  unaTraversalResult[ 'contains_collections']:
                    if unaTraversalResult[ 'factories']:
                        unaFactoryAndTranslations = unaTraversalResult[ 'factories'][ 0]
                        if unaFactoryAndTranslations:
                            unTypeName = unaFactoryAndTranslations[ 'meta_type']
                            if unTypeName:
                                unNewTitle = unaFactoryAndTranslations[ 'type_translations'][ 'archetype_name']
                                unNewCollectionCreateResult = self.fCrearElementoDeTipo( 
                                    theTimeProfilingResults =theTimeProfilingResults,
                                    theContainerElement     =aNewObject, 
                                    theTypeName             =unTypeName, 
                                    theId                   =None,
                                    theTitle                =unNewTitle, 
                                    theDescription          ='',
                                    theAdditionalParams     =theAdditionalParams)                                             
                                if (not unNewCollectionCreateResult) or not ( unNewCollectionCreateResult[ 'effect'] == 'created'):
                                    # just cant initialize collection contents
                                    #  anActionReport = { 'effect': 'error', 'failure': 'collection_creation_failure', }
                                    #return anActionReport     
                                    None
            
            return anActionReport     
                
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fCrearElementoDeTipo', theTimeProfilingResults)

        
        
        
        

        
        
        
     
    
    security.declarePrivate( 'fAsEncodedFromUIToDB')
    def fAsEncodedFromUIToDB( self, theString, theTranslationService):
        if not theTranslationService:
            return theString
        
        unNewValue = theTranslationService.encode( theString)          
        return unNewValue
    
    
    
    security.declarePrivate( 'fNewVoidDeleteElementReport')
    def fNewVoidDeleteElementReport( self,):
        aReport = {
            'parent_traversal_name':   '',
            'impact_report':           None,
            #'impacted_objects':        [],
            'impacted_objects_UIDs':   [],
            'effect':                  'error', 
            'failure':                 'Not executed',
        } 
        return aReport
    
     
    
    security.declarePrivate(   'fEliminarElemento')
    def fEliminarElemento(self , 
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,                          
        theElement              =None, 
        theIdToDelete           =None, 
        theUIDToDelete          =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete an element and all its contents, given its UID and matching Id, if the time lapsed is within the acceptable interval.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fEliminarElemento', theTimeProfilingResults)

        try:
            
            aDeleteReport = self.fNewVoidDeleteElementReport()
            
            if theModelDDvlPloneTool == None:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'No theModelDDvlPloneTool', })
                return aDeleteReport                 

            unModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
                        
            unSecondsNow = unModelDDvlPloneTool_Retrieval.fSecondsNow()            
            if not(  (unSecondsNow >= theRequestSeconds) and ( unSecondsNow - theRequestSeconds) < theModelDDvlPloneTool.fSecondsToReviewAndDelete( theElement)):
                aDeleteReport.update( { 'effect': 'error', 'failure': 'time_out', })
                return aDeleteReport                 
    
            if ( theElement == None) or ( not theIdToDelete) or ( not theUIDToDelete) or ( not theRequestSeconds):
                aDeleteReport.update( { 'effect': 'error', 'failure': 'required_parameters_missing', })
                return aDeleteReport     
                
            unTargetElement = unModelDDvlPloneTool_Retrieval.fElementoPorUID( theUIDToDelete, theElement)
            if not unTargetElement:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'get_by_uid_failure', })
                return aDeleteReport    

                            
            unElementDeleteImpactReport = unModelDDvlPloneTool_Retrieval.fDeleteImpactReport( 
                theModelDDvlPloneTool   =theModelDDvlPloneTool,
                theTimeProfilingResults =theTimeProfilingResults,
                theElement              =unTargetElement,
                theAdditionalParams     =theAdditionalParams
            )

            if not unElementDeleteImpactReport:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'internal_impact_report_retrieval_failure', })
                return aDeleteReport  
            
            
            
                            
            if not ( unElementDeleteImpactReport[ 'here'][ 'container_element'][ 'object'] == theElement):
                aDeleteReport.update( { 'effect': 'error', 'failure': 'wrong_container_element', })
                return aDeleteReport  
                        
            unaIdAEliminar = unElementDeleteImpactReport[ 'here'][ 'id']
            if unaIdAEliminar == theElement:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'internal_no_element_id', })
                return aDeleteReport  

            if not unElementDeleteImpactReport[ 'delete_permission']:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'no_delete_permission', })
                return aDeleteReport     
                    
            
            
            self.pImpactDeleteImpactReportIntoReport( unTargetElement, unElementDeleteImpactReport, aDeleteReport)
                  
            self.pSetAudit_Modification( theElement)     
            
            # ACV We are not really keeping defunct objects at this time, so we do not expend the effort on object that shall be gone immediately.
            # self.pSetAudit_Deletion( unTargetElement)  
            
         
            theElement.manage_delObjects( [ unaIdAEliminar, ])
           
            aDeleteReport.update( { 
                'effect':                'deleted', 
                'parent_traversal_name': unElementDeleteImpactReport[ 'parent_traversal_name'], 
                'impact_report':         unElementDeleteImpactReport,
            })
            return aDeleteReport     
    
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fEliminarElemento', theTimeProfilingResults)

                
         
                
                
                

   
    
    security.declarePrivate( 'pImpactDeleteImpactReportIntoReport')
    def pImpactDeleteImpactReportIntoReport( self, theElement, theElementDeleteImpactReport, theDeleteReport):
 
        if ( theElement == None) or ( not theElementDeleteImpactReport) or ( not theDeleteReport):
            return self
    
        unosElementsToBeDeleted, unosRelatedElements = ModelDDvlPloneTool_Retrieval().fObjectsToDeleteAndRelated_FromImpactReport( theElementDeleteImpactReport)
        
        
        unosImpactedObjectsUIDs = theDeleteReport[ 'impacted_objects_UIDs']
        
        
        unaUIDDeletedElement = None
        try:
            unaUIDDeletedElement = theElement.UID()
        except:
            None
        if unaUIDDeletedElement:
            if not ( unaUIDDeletedElement in unosImpactedObjectsUIDs):
                unosImpactedObjectsUIDs.append( unaUIDDeletedElement)
                
        unContenedorSource = self.fImpactChangedContenedorYPropietario_IntoReport( theElement, theDeleteReport)
        
        
        for unElementToBeDeleted in unosElementsToBeDeleted:
            
            unaUIDToBeDeleted = None
            try:
                unaUIDToBeDeleted = unElementToBeDeleted.UID()
            except:
                None
            if unaUIDToBeDeleted:
                if not ( unaUIDToBeDeleted in unosImpactedObjectsUIDs):
                    unosImpactedObjectsUIDs.append( unaUIDToBeDeleted)
            
                
                
        for unRelatedElement in unosRelatedElements:
            
            unaUIDRelated = None
            try:
                unaUIDRelated = unRelatedElement.UID()
            except:
                None
            if unaUIDRelated:
                if not ( unaUIDRelated in unosImpactedObjectsUIDs):
                    unosImpactedObjectsUIDs.append( unaUIDRelated)
                    
                                                        
            unContenedorSource = self.fImpactChangedContenedorYPropietario_IntoReport( unRelatedElement, theDeleteReport)
        
        return self
                    
                
                
    
    
    
    
    
    
    
    
    
                
     
    security.declarePrivate(   'fEliminarVariosElementos')
    def fEliminarVariosElementos(self ,
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,                          
        theContainerElement     =None, 
        theIdsToDelete          =None, 
        theUIDsToDelete         =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete some elements and all their contents, givwen their UIDs and matching Ids, if the time lapsed is within the acceptable interval.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fEliminarVariosElementos', theTimeProfilingResults)

        try:

            if theModelDDvlPloneTool == None:
                return [  { 'effect': 'error', 'failure': 'No theModelDDvlPloneTool', }, ]

            unModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            
            unSecondsNow = unModelDDvlPloneTool_Retrieval.fSecondsNow()            
            if not(  (unSecondsNow >= theRequestSeconds) and ( unSecondsNow - theRequestSeconds) < theModelDDvlPloneTool.fSecondsToReviewAndDelete( theContainerElement)):
                return [ { 'effect': 'error', 'failure': 'time_out', },]
 
            if ( theContainerElement == None) or not theRequestSeconds:
                return [ { 'effect': 'error', 'failure': 'required_parameters_missing: theContainerElement or theRequestSeconds', },]                
            
            someIdsToDelete = theIdsToDelete
            if not ( someIdsToDelete.__class__.__name__ in [ 'list', 'tuple', 'set']):
                someIdsToDelete = [ someIdsToDelete, ]
            
            someUIDsToDelete = theUIDsToDelete
            if not ( someUIDsToDelete.__class__.__name__ in [ 'list', 'tuple', 'set']):
                someUIDsToDelete = [ someUIDsToDelete, ]
            
            if not someIdsToDelete or not someUIDsToDelete:
                return [ { 'effect': 'error', 'failure': 'required_parameters_missing: UIDs or Ids', },]

            unNumUIDsToDelete = len( someUIDsToDelete)
            
            if not ( len( someIdsToDelete) == unNumUIDsToDelete):
                return [ { 'effect': 'error', 'failure': 'not same number of Ids UIDs in delete elements request', },]
            

            someElementDeleteReports = [ ]
            someElementsToDelete     = [ ]
            
            for anUIDIndex in range( unNumUIDsToDelete):
                anElementUID = someUIDsToDelete[  anUIDIndex]
                anElementId  = someIdsToDelete[   anUIDIndex]
                unElementToDelete = unModelDDvlPloneTool_Retrieval.fElementoPorUID( anElementUID, theContainerElement)
                if ( unElementToDelete == None):
                    someElementDeleteReports.append( { 'effect': 'error', 'failure': 'get_by_uid_failure', 'uid': anElementUID, 'id': anElementId},)
                else:
                    if unElementToDelete.getId() == anElementId:
                        someElementsToDelete.append( [ anElementUID, anElementId, unElementToDelete,])
                    else:
                        someElementDeleteReports.append( { 'effect': 'error', 'failure': 'element_by_UID_does_not_match_expected_Id', 'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,},)
                   
                    
            if not someElementsToDelete:
                someElementDeleteReports.append( { 'effect': 'error', 'failure': 'no elements to delete', })
                return someElementDeleteReports
            
            unAuditedContainerModification = False
                
            unElementDeleteImpactReport = None
            for anElementUID, anElementId, unElementToDelete in someElementsToDelete:
                              
                unElementDeleteImpactReport = unModelDDvlPloneTool_Retrieval.fDeleteImpactReport( 
                    theModelDDvlPloneTool   =theModelDDvlPloneTool,
                    theTimeProfilingResults =theTimeProfilingResults,
                    theElement              =unElementToDelete,
                    theAdditionalParams     =theAdditionalParams
                )
    
                if not unElementDeleteImpactReport:
                    someElementDeleteReports.append( { 'effect': 'error', 'failure': 'impact_report_retrieval_failure',  'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,})
                    
                elif not unElementDeleteImpactReport[ 'here'][ 'container_element'][ 'object'] == theContainerElement:
                    someElementDeleteReports.append( { 'effect': 'error', 'failure': 'wrong_container_element', 'impact_report': unElementDeleteImpactReport,  'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,})
                            
                elif not unElementDeleteImpactReport[ 'delete_permission']:
                    someElementDeleteReports.append( { 'effect': 'error', 'failure': 'no_delete_permission', 'impact_report': unElementDeleteImpactReport,  'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,})
                        
                else:
                    unaIdAEliminar = unElementDeleteImpactReport[ 'here'][ 'id']
                    if not unaIdAEliminar:
                        someElementDeleteReports.append( { 'effect': 'error', 'failure': 'element_to_delete_without_id', 'impact_report': unElementDeleteImpactReport,  'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,})
        
                    else:
                        if not unAuditedContainerModification:
                            self.pSetAudit_Modification( theContainerElement)    
                            unAuditedContainerModification = True
                        
                        # ACV We are not really keeping defunct objects at this time, so we do not expend the effort on object that shall be gone immediately.
                        # self.pSetAudit_Deletion( unElementToDelete)  
                        
                        theContainerElement.manage_delObjects( [ unaIdAEliminar, ])
                        
                        unParentTraversalName = ( unElementDeleteImpactReport and unElementDeleteImpactReport[ 'parent_traversal_name']) or ''
                        
                        someElementDeleteReports.append( { 'effect': 'deleted', 'parent_traversal_name': unParentTraversalName, 'impact_report': unElementDeleteImpactReport,})
   
    
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fEliminarVariosElementos', theTimeProfilingResults)

                
                                
                
                
                

    security.declarePrivate(   'fElementPermissionsAndRolesToSetForElement')
    def fElementPermissionsAndRolesToSetForElement(self, theElement, ):     
        if ( theElement == None):
            return []

        aMetaType = theElement.meta_type
        
        somePermissionsAndRoles = cPermissionsAndRolesForTypes.get( aMetaType, None)
        if not somePermissionsAndRoles:
            somePermissionsAndRoles = cPermissionsAndRolesForTypes.get( cAnyType, None)
            if not somePermissionsAndRoles:
                return []
                    
        somePermissionsAndRolesToSet = [ ]
        for aPermissionsAndRoles in somePermissionsAndRoles:
            somePermissions = aPermissionsAndRoles[ 0]  
            for unaPermission in somePermissions:
                somePermissionsAndRolesToSet.append( [ unaPermission, aPermissionsAndRoles[ 1], aPermissionsAndRoles[ 2]],)
                    
        return somePermissionsAndRolesToSet
        
    
    
    
    security.declarePrivate(   'pSetElementPermissions')
    def pSetElementPermissions(self, theElement, thePermissionsNotToSet=[],):     
        if ( theElement == None):
            return self

        somePermissionsAndRoles = self.fElementPermissionsAndRolesToSetForElement( theElement)
        
        for aPermissionAndRoles in somePermissionsAndRoles:
            unaPermission = aPermissionAndRoles[ 0]
            if unaPermission:
                unosRoles = aPermissionAndRoles[ 1]
                if unosRoles:
                    unAcquire = aPermissionAndRoles[ 2]

                    theElement.manage_permission( unaPermission, roles=unosRoles, acquire=unAcquire)
                    
        return self
    
    
    
    

    security.declarePrivate(   'fGetAudit_MemberIdAndNow')
    def fGetAudit_MemberIdAndNow(self,):     
    
        unMemberId = ''
        
        aMembershipTool = getToolByName( self, 'portal_membership', None)
        if aMembershipTool:
            unMember = aMembershipTool.getAuthenticatedMember()   
            if unMember:
                if unMember.getUserName() == 'Anonymous User':
                    unMemberId = unMember.getUserName()
                else:
                    unMemberId = unMember.getMemberId()   
    
        unAhora = DateTime()
    
        return [ unMemberId, unAhora,]
    
    
    
        
    
    security.declarePrivate(   'pSetAudit_Creation')
    def pSetAudit_Creation(self, theElement,):     
        if ( theElement == None):
            return self
        
        unMemberId, unAhora = self.fGetAudit_MemberIdAndNow()
      
        unCreationDateFieldName = ''
        try:
            unCreationDateFieldName = theElement.creation_date_field
        except:
            None
            
        unCreationUserFieldName = ''
        try:
            unCreationUserFieldName = theElement.creation_user_field
        except:
            None
                
                
        if not( unCreationDateFieldName or unCreationUserFieldName):
            return self
        
        unSchema = theElement.schema
        if not unSchema:
            return self
            
        unCreationDateField = unSchema.get( unCreationDateFieldName, )
        if unCreationDateField:
            unMutator = unCreationDateField.getMutator( theElement)
            if unMutator:
                try:
                    unMutator( unAhora) 
                except:
                    None
                            
        unCreationUserField = unSchema.get( unCreationUserFieldName, )
        if unCreationUserField:
            unMutator = unCreationUserField.getMutator( theElement)
            if unMutator:
                try:
                    unMutator( unMemberId) 
                except:
                    None
                                        
        return self
    
    

    
    
    security.declarePrivate(   'pSetAudit_Modification')
    def pSetAudit_Modification(self, theElement,):     
        if ( theElement == None):
            return self
      
        unMemberId, unAhora = self.fGetAudit_MemberIdAndNow()
      
        unChangeCounterFieldName = ''
        try:
            unChangeCounterFieldName = theElement.change_counter_field
        except:
            None

        unModificationDateFieldName = ''
        try:
            unModificationDateFieldName = theElement.modification_date_field
        except:
            None
            
        unModificationUserFieldName = ''
        try:
            unModificationUserFieldName = theElement.modification_user_field
        except:
            None
                
                
        if not( unChangeCounterFieldName or unModificationDateFieldName or unModificationUserFieldName):
            return self
        
        unSchema = theElement.schema
        if not unSchema:
            return self
            
        unChangeCounterField = unSchema.get( unChangeCounterFieldName, )
        if unChangeCounterField:
            unAccessor = unChangeCounterField.getAccessor( theElement)
            if unAccessor:
                unCurrentCounter = 0
                try:
                    unCurrentCounter = int( unAccessor())
                except:
                    None
                
                unNewCounter = unCurrentCounter + 1
                
                unMutator = unChangeCounterField.getMutator( theElement)
                if unMutator:
                    try:
                        unMutator( unNewCounter) 
                    except:
                        None
                        
        unModificationDateField = unSchema.get( unModificationDateFieldName, )
        if unModificationDateField:
            unMutator = unModificationDateField.getMutator( theElement)
            if unMutator:
                try:
                    unMutator( unAhora) 
                except:
                    None         
                        
        unModificationUserField = unSchema.get( unModificationUserFieldName, )
        if unModificationUserField:
            unMutator = unModificationUserField.getMutator( theElement)
            if unMutator:
                try:
                    unMutator( unMemberId) 
                except:
                    None
                                        
        return self
        

    
  
    
  
    security.declarePrivate(   'pSetAudit_Deletion')
    def pSetAudit_Deletion(self, theElement,):     
        if ( theElement == None):
            return self
        
        
        unMemberId, unAhora = self.fGetAudit_MemberIdAndNow()
      
        self.pSetAudit_Deletion_recursive( theElement, unMemberId, unAhora)
        
        return self    
    
    
    

    security.declarePrivate(   'pSetAudit_Deletion_recursive')
    def pSetAudit_Deletion_recursive(self, theElement, theMemberId, theAhora):     
        if ( theElement == None):
            return self
        
        
        unChangeCounterFieldName = ''
        try:
            unChangeCounterFieldName = theElement.change_counter_field
        except:
            None
              
        unIsInactiveFieldName = ''
        try:
            unIsInactiveFieldName = theElement.is_inactive_field
        except:
            None

        unDeletionDateFieldName = ''
        try:
            unDeletionDateFieldName = theElement.deletion_date_field
        except:
            None
            
        unDeletionUserFieldName = ''
        try:
            unDeletionUserFieldName = theElement.deletion_user_field
        except:
            None
                
        if unChangeCounterFieldName or unIsInactiveFieldName or unDeletionDateFieldName or unDeletionUserFieldName:
        
            unSchema = theElement.schema
            if unSchema:
                
                unChangeCounterField = unSchema.get( unChangeCounterFieldName, )
                if unChangeCounterField:
                    unAccessor = unChangeCounterField.getAccessor( theElement)
                    if unAccessor:
                        unCurrentCounter = 0
                        try:
                            unCurrentCounter = unAccessor()
                        except:
                            None
                        
                        unNewCounter = unCurrentCounter+ 1
                        
                        unMutator = unChangeCounterField.getMutator( theElement)
                        if unMutator:
                            try:
                                unMutator( unNewCounter) 
                            except:
                                None
                
                unDeletionDateField = unSchema.get( unDeletionDateFieldName, )
                if unDeletionDateField:
                    unMutator = unDeletionDateField.getMutator( theElement)
                    if unMutator:
                        try:
                            unMutator( theAhora) 
                        except:
                            None
                                    
                unDeletionUserField = unSchema.get( unDeletionUserFieldName, )
                if unDeletionUserField:
                    unMutator = unDeletionUserField.getMutator( theElement)
                    if unMutator:
                        try:
                            unMutator( theMemberId) 
                        except:
                            None
                            
                unIsInactiveField = unSchema.get( unIsInactiveFieldName, )
                if unIsInactiveField:
                    unMutator = unIsInactiveField.getMutator( theElement)
                    if unMutator:
                        try:
                            unMutator( True) 
                        except:
                            None

        unosSubObjects = []
        
        try:
            unosSubObjects = theElement.objectValues()
        except:
            None
            
        if not unosSubObjects:
            return self
        
        for unSubObject in unosSubObjects:
            self.fSetAudit_Deletion_recursive( unSubObject, theMemberId, theAhora,)
                                        
        return self
                
        
    
    
    
    
    