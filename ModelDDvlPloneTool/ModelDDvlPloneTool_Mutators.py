# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Mutators.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Model Driven Development sl <ModelDDvlPlone@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

import logging

from logging import ERROR as cLoggingLevel_ERROR



from time import time

from DateTime import DateTime

from StringIO import StringIO


from Acquisition  import aq_inner, aq_parent


from Products.CMFCore.exceptions import AccessControl_Unauthorized

from AccessControl      import ClassSecurityInfo

from Acquisition import aq_parent, aq_inner


from Products.Archetypes.utils import shasattr

from Products.Archetypes.config import REFERENCE_CATALOG, UID_CATALOG



from Products.CMFCore       import permissions
from Products.CMFCore.utils import getToolByName

from Products.Relations.config                  import RELATIONS_LIBRARY
from Products.Relations                         import processor            as  gRelationsProcessor




from ModelDDvlPloneTool_Permissions_Definitions import *

from ModelDDvlPloneTool_Retrieval               import cChangeLogFieldNameField

from ModelDDvlPloneTool_Profiling               import ModelDDvlPloneTool_Profiling
from ModelDDvlPloneTool_Retrieval               import ModelDDvlPloneTool_Retrieval

from ModelDDvlPloneTool_Mutators_Constants      import *

from ModelDDvlPloneTool_Mutators_Plone          import ModelDDvlPloneTool_Mutators_Plone
from ModelDDvlPloneTool_Mutators_Plone          import cModificationKind_DeletePloneSubElement, cModificationKind_DeletePloneSubElement_abbr
from ModelDDvlPloneTool_Mutators_Plone          import cModificationKind_MovePloneSubObject,    cModificationKind_MovePloneSubObject_abbr

from ModelDDvlPloneTool_Transactions            import ModelDDvlPloneTool_Transactions

from ModelDDvlPloneToolSupport                  import fEvalString,  fReprAsString, fSecondsNow 










class ModelDDvlPloneTool_Mutators( ModelDDvlPloneTool_Profiling, ModelDDvlPloneTool_Mutators_Plone):
    """
    """
    security = ClassSecurityInfo()



 
    # #############################################################
    """Generic attribute mutators by name
    
    """

        
    
    
    security.declarePrivate( 'pImpactChangeValuesIntoReport')
    def pImpactChangeValuesIntoReport( self, theModelDDvlPloneTool_Retrieval, theChangedElement, theChangeReport):

        if theChangeReport == None:
            return self
        
        unosImpactedObjectsUIDs = theChangeReport[ 'impacted_objects_UIDs']
        
        if theChangedElement == None:
            return self
 
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
                                        
                    for aRelatedUID in allRelatedUIDs:
                        aRelatedElement = theModelDDvlPloneTool_Retrieval.fElementoPorUID( aRelatedUID, theChangedElement)
                        if not ( aRelatedElement == None):
                            
                            unVoid = self.fImpactChangedContenedorYPropietario_IntoReport( aRelatedElement, theChangeReport)
                            
                            
        return self
    
    
    
    
    
   
    security.declarePrivate( 'pImpactChangeValuesIntoReport_RecurseContents')
    def pImpactChangeValuesIntoReport_RecurseContents( self, theChangedElement, theChangeReport, theImpactAllContents=False):

        if theChangeReport == None:
            return self
        
        unosImpactedObjectsUIDs = theChangeReport[ 'impacted_objects_UIDs']
        
        unosContentsElements = []
        try:
            unosContentsElements = theChangedElement.objectValues()
        except:
            None
        
        if not unosContentsElements:
            return self
        
        for unContentElement in unosContentsElements:
                    
            
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
        if shasattr( theChangedElement, 'getContenedor'):
            try:
                unContenedor = theChangedElement.getContenedor()
            except:
                None
        else:
            unContenedor = aq_parent( aq_inner( theChangedElement))
                
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
        if shasattr( theChangedElement, 'getPropietario'):
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
                    
                 
        if shasattr( theChangedElement, 'propagate_delete_impact_to'):
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
                                    
    
    
    
    
    security.declarePrivate( 'fNewVoidChangeValuesReport')
    def fNewVoidChangeValuesReport( self,):
        aReport = {
            'object_reports':        [],
            'impacted_objects_UIDs': [],
            'field_reports':         [],
            'field_reports_by_name': {},
        } 
        return aReport
 
    
    
    
            
    security.declarePrivate( 'fChangeValues')
    def fChangeValues(self , 
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,
        theElement              =None, 
        theNewValuesDict        =None,
        theAdditionalParams     =None):        

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fChangeValues', theTimeProfilingResults)

        try:
            
            aReport = self.fNewVoidChangeValuesReport()
            someObjectReports   = aReport.get( 'object_reports')
            someFieldReports    = aReport.get( 'field_reports')
            aFieldReportsByName = aReport.get( 'field_reports_by_name')

            if ( theModelDDvlPloneTool == None) or ( theElement == None) or not theNewValuesDict:
                return None

    
            
            aTranslationService = getToolByName( theElement, 'translation_service', None)            
             
            unValueForId = theNewValuesDict.get( 'theIdAttribute', '')
            
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
             
                    
                    
                    
            aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theElement)
            if aModelDDvlPloneTool_Retrieval == None:
                return None
            
            unResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'dynamic_vocabularies', 'audit',],
                theWritePermissions         =[ 'object', 'attrs', ],
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
            

            if not unResult.get( 'read_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_read_permission',}
                someObjectReports.append( aReportForObject)
                return aReport
            
            if not unResult.get( 'write_permission', False):
                aReportForObject = { 'effect': 'error', 'failure': 'object_write_permission',}
                someObjectReports.append( aReportForObject)
                return aReport
            
            
          
            unChangeCounterString = theNewValuesDict.get( 'theChgCtr', '')
            unChangeCounter = None
            if unChangeCounterString:
                try:
                    unChangeCounter = int( unChangeCounterString)
                except:
                    None
            if not ( unChangeCounter == None):
                
                unCurrentChangeCounter = unResult.get( 'change_counter', None)
                if not ( unCurrentChangeCounter == None):
                    
                    if not ( unChangeCounter == unCurrentChangeCounter):
                        # #######################################################
                        """Other Transaction(s) changed the element since the Edit form was presented to the User. Do not allow changes.
                        Note that objects changed by a relation for which they are the dependency supplier (not the client) should not increment their change counter upon modifications of that relationship."
                        """
                        unChangeLogResult = { }
                        self.fRetrieveChangeLog( 
                            theTimeProfilingResults     =theTimeProfilingResults,
                            theElement                  =theElement, 
                            theRetrievalExtents         =[ 'change_entries', 'change_entries_summaries', 'change_entries_summaries_fields_values',],
                            theTranslationsCaches       =None, 
                            theCheckedPermissionsCache  =None, 
                            theResult                   =unChangeLogResult,
                            theAdditionalParams         ={ 'ChangesAfter': unChangeCounter + 1,})

                        unChangeLog                 = unChangeLogResult.get( 'change_entries',                 [])
                        unosChangeLogSummaries      = unChangeLogResult.get( 'change_entries_summaries',       [])
                        unChangeLogAfter            = unChangeLogResult.get( 'change_entries_after',           unChangeLog)
                        unosChangeLogAfterSummaries = unChangeLogResult.get( 'change_entries_after_summaries', unosChangeLogSummaries)
                        unURLRecentChanges          = '%s/MDDChanges/?theCC=%d' % ( theElement.absolute_url_path(), unChangeCounter + 1,)
                        
                        aReportForObject = { 'effect': 'error', 'failure': 'changed_by_other_transactions', 'url_recent_changes': unURLRecentChanges, 'change_entries': unChangeLog, 'change_entries_summaries': unosChangeLogSummaries, 'change_entries_after': unChangeLogAfter, 'change_entries_after_summaries': unosChangeLogAfterSummaries, }
                        someObjectReports.append( aReportForObject)
                        return aReport
                         
                        
                        
    
            unAnyAttributeChanged = False
            
            if unValueForId:
                
                unPortalPropertiesTool = getToolByName( theElement, 'portal_properties', None)
                if not ( unPortalPropertiesTool == None):
                    unSiteProperties = getattr( unPortalPropertiesTool, 'site_properties', None)
                    if not ( unSiteProperties == None):
                        unVisibleIds = unSiteProperties.getProperty('visible_ids')
                        if unVisibleIds:
                    
                            unCurrentId = unResult.get( 'id', '')
                            
                            if unCurrentId:
                            
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
                                            aReportForField = { 'attribute_name': 'id', 'effect': 'error', 'failure': 'invoking_setId', 'new_value': unNuevaId, 'previous_value': unCurrentIdResult,}                                                                                                                        
                                    finally:
                                        logging.getLogger('Zope.ZCatalog').manager.disable = aDisableLevel
                                        
                                    if unChanged:
                                        unAnyAttributeChanged = True
                                        aReportForField = { 'attribute_name': 'id', 'effect': 'changed', 'new_value': unNuevaId, 'previous_value': unCurrentIdResult,}                                                                                                                        
                                
                                
                                if aReportForField:
                                    aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
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
                                            # ACV OJO 20091201 No change for null values 
                                            if ( unNewValue == unCurrentRawValue) or ( ( not unNewValue) and ( not unCurrentRawValue)):
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                            else:
                                                aInvokeMutator = True
                                                
                                        elif unAttributeType == 'text':
                                            
                                            unNewValue = unFormValue.replace( '\r\n','\n')
                                            unNewValue = unNewValue.replace( '\r','\n')
                                            unNewValue = unNewValue.strip()
                                                
                                            unNewValue = self.fAsEncodedFromUIToDB( unNewValue, aTranslationService)
                                            if ( unNewValue == unCurrentRawValue) or ( ( not unNewValue) and ( not unCurrentRawValue)):
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
                                                if (unNewValue == unCurrentRawValue) or ( ( not unNewValue) and ( not unCurrentRawValue)):
                                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                                else:
                                                    aInvokeMutator = True
                                                    
                                        elif unAttributeType == 'float':
                                            unNewValue = None
                                            try:
                                                unNewValue = float( unFormValue)    
                                            except ValueError:
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormValue,}                                                                                                                        
                                            if not( unNewValue == None) or ( ( not unNewValue) and ( not unCurrentRawValue)):
                                                if unNewValue == unCurrentRawValue:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                                else:
                                                    aInvokeMutator = True
     
                                        elif unAttributeType == 'boolean':
                                            unNewValue = unFormValue == '1'
                                            if ( unNewValue == unCurrentRawValue) or ( ( not unNewValue) and ( not unCurrentRawValue)):
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
                                                if ( unNewValue == unCurrentRawValue) or ( ( not unNewValue) and ( not unCurrentRawValue)):
                                                    aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                                else:
                                                    aInvokeMutator = True
                                        
                                        elif unAttributeType == 'datetime':
                                            unNewYearValue  = None
                                            unNewMonthValue = None
                                            unNewDayOfMonthValue = None
                                            aReportForField = None
                                            
                                            unHasYear  = False
                                            unHasMonth = False
                                            unHasDay   = False
                                            
                                            if theNewValuesDict.has_key( '%s_sub_value_year' % unAttributeName):
                                                unFormYearValue = theNewValuesDict.get( '%s_sub_value_year' % unAttributeName, None)                                             
                                                try:
                                                    unNewYearValue = int( unFormYearValue)    
                                                except ValueError:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'sub_value': 'year',  'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormYearValue,}                                                                                                                        
                                            
                                            if not aReportForField and theNewValuesDict.has_key( '%s_sub_value_month' % unAttributeName):
                                                unHasMonth = True
                                                unFormMonthValue = theNewValuesDict.get( '%s_sub_value_month' % unAttributeName, None)                                             
                                                try:
                                                    unNewMonthValue = int( unFormMonthValue)    
                                                except ValueError:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'sub_value': 'month',  'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormMonthValue,}                                                                                                                                                                
                                            
                                            if not aReportForField and theNewValuesDict.has_key( '%s_sub_value_day_of_month' % unAttributeName):
                                                unHasDay = True
                                                unFormDayOfMonthValue = theNewValuesDict.get( '%s_sub_value_day_of_month' % unAttributeName, None)                                             
                                                try:
                                                    unNewDayOfMonthValue = int( unFormDayOfMonthValue)    
                                                except ValueError:
                                                    aReportForField = { 'attribute_name': unAttributeName, 'sub_value': 'day_of_month',  'effect': 'error', 'failure': 'value_error', 'previous_value': unValueResult, 'new_value': unFormDayOfMonthValue,}                                                                                                                        
                                            
                                            if not ( unHasYear and unHasDay):
                                                aReportForField = { 'attribute_name': unAttributeName, 'effect': 'no_change', 'previous_value': unValueResult,}                        
                                            
                                            else:    
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
                
                self.pImpactChangeValuesIntoReport( aModelDDvlPloneTool_Retrieval, theElement, aReport)
                
                self.pSetAudit_Modification( theElement, cModificationKind_ChangeValues, aReport)       
                
                
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

                
    security.declarePrivate( 'fNewVoidMoveSubObjectReport')
    def fNewVoidMoveSubObjectReport( self,):
        aReport = {
            'effect':                  'error', 
            'failure':                 'Not executed',
            'new_position':            -1,
            'delta':                   0,
            'moved_element':           None,
            'parent_traversal_name':   '',
            'impacted_objects_UIDs':   [],
        } 
        return aReport
    
    
    
    security.declarePrivate( 'fMoveSubObject')
    def fMoveSubObject(self , 
        theModelDDvlPloneTool   =None,
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
            
            if ( theModelDDvlPloneTool == None) or ( theContainerElement == None)  or ( not  theTraversalName)  or ( not theMovedObjectId)  or ( not theMoveDirection) or not ( theMoveDirection.lower() in ['up', 'down', 'top', 'bottom', ]):
                return aMoveReport
                        
            aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContainerElement)
            if aModelDDvlPloneTool_Retrieval == None:
                return aMoveReport
            
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
                
                
                unPositionAfterMove  = -1
                unMovedElementResult = None
                
                unResultAfterMove = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
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
                if unResultAfterMove:
                    aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unResultAfterMove, [ 'traversals',])
                    
                    unTraversalResultAfterMove =  unResultAfterMove[ 'traversals_by_name'].get( theTraversalName, None)
                    if unTraversalResultAfterMove:
                        
                        someElementResultsAfterMove = unTraversalResultAfterMove[ 'elements']
                        for unElementIndex in range( len( someElementResultsAfterMove)):
                            
                            unElementResult = someElementResultsAfterMove[ unElementIndex]
                            if unElementResult.get( 'id', '') == theMovedObjectId:
                                
                                unMovedElementResult = unElementResult
                                unPositionAfterMove = unElementIndex
                                break
                            
                aMoveReport.update( { 'effect': 'moved', 'moved_element': unMovedElementResult, 'new_position': unPositionAfterMove, 'delta': unDelta, 'parent_traversal_name': theTraversalName,})
                            

                self.pSetAudit_Modification( theContainerElement, cModificationKind_MoveSubObject, aMoveReport)       

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


                
    security.declarePrivate( 'fNewVoidLinkReport')
    def fNewVoidMoveReferencedObjectReport( self,):
        aReport = {
            'effect':                  'error', 
            'failure':                 'Not executed',
            'new_position':            -1,
            'delta':                   0,
            'moved_element':           None,
            'parent_traversal_name':   '',
            'impacted_objects_UIDs':   [],
        } 
        return aReport
    
  
    security.declarePrivate( 'fMoveReferencedObject')
    def fMoveReferencedObject(self , 
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,
        theSourceElement        =None,  
        theReferenceFieldName   =None, 
        theMovedReferenceUID    =None, 
        theMoveDirection        =None,
        theAdditionalParams     =None):        
 
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fMoveReferencedObject', theTimeProfilingResults)

        try:

            aMoveReport = self.fNewVoidMoveReferencedObjectReport()
            
            if ( theModelDDvlPloneTool == None) or ( theSourceElement == None)  or ( not  theReferenceFieldName) or (not theMovedReferenceUID) or ( not theMoveDirection) or  not ( theMoveDirection.lower() in ['up', 'down', 'top', 'bottom', ]):
                return aMoveReport
            
            aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theSourceElement)
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
                return aMoveReport
        
            if not (  unResult[ 'read_permission'] and unResult[ 'write_permission']):
                return aMoveReport
    
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unResult, [ 'traversals',])

            unTraversalResult =  unResult[ 'traversals_by_name'].get( theReferenceFieldName, None)
            if not unTraversalResult:
                return aMoveReport
                
            if not (  unTraversalResult[ 'traversal_kind'] == 'relation'):
                return aMoveReport

            if not (  unTraversalResult[ 'read_permission'] and unTraversalResult[ 'write_permission']):
                return aMoveReport
              
            aRelationsLibrary = getToolByName( theSourceElement, RELATIONS_LIBRARY)        
            if not aRelationsLibrary:
                return aMoveReport
        
            someRelatedResults = unTraversalResult[ 'elements']
            unNumRelatedResults = len( someRelatedResults)
            if unNumRelatedResults < 2:
                return aMoveReport

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
                return aMoveReport           
        
            aMoveDirection = theMoveDirection.lower()
            
            someToUnlink = []
            someToLink   = []
    
            if aMoveDirection == 'top':
                if unFoundRelatedIndex < 1:
                    return aMoveReport
                someToUnlink = [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults]
                someToLink =   [ unFoundRelatedResult[ 'UID'] ] + [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults if not (unRelatedResult == unFoundRelated)]
            
            elif aMoveDirection == 'up':
                if unFoundRelatedIndex < 1:
                    return aMoveReport
                someToUnlink = [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex -1: unNumRelatedResults]]
                someToLink =   [ unFoundRelatedResult[ 'UID'], ] + [unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex - 1: unFoundRelatedIndex]] + [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex + 1: unNumRelatedResults]]
                    
            elif aMoveDirection == 'down':
                if unFoundRelatedIndex == (unNumRelatedResults - 1):
                    return aMoveReport
                someToUnlink = [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex: unNumRelatedResults]]
                someToLink =   [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex + 1 : unFoundRelatedIndex + 2]] + [ unFoundRelatedResult[ 'UID'], ] + [ unRelatedResult[ 'UID'] for unRelatedResult in someRelatedResults[ unFoundRelatedIndex + 2: unNumRelatedResults]]
                    
            elif aMoveDirection == 'bottom':
                if unFoundRelatedIndex == (unNumRelatedResults - 1):
                    return aMoveReport
                someToUnlink = [ unFoundRelatedResult[ 'UID'], ]
                someToLink =   [ unFoundRelatedResult[ 'UID'], ] 
            
        
            if not someToLink and not someToUnlink:
                return aMoveReport
                
            aSourceUID = unResult[ 'UID']
            
            unRelationship      = unTraversalResult[ 'relationship']
            someToConnect    = [ [ aSourceUID, anUID, unRelationship] for anUID in someToLink]
            someToDisconnect = [ [ aSourceUID, anUID, unRelationship] for anUID in someToUnlink]
                            
            
            self.pImpactMoveReferencedObjectIntoReport( theSourceElement, someRelatedResults, aMoveReport)
            

            gRelationsProcessor.process( aRelationsLibrary, connect= [],            disconnect=someToDisconnect)
            gRelationsProcessor.process( aRelationsLibrary, connect= someToConnect, disconnect=[])

            
            unPositionAfterMove  = -1
            unMovedElementResult = None

            unResultAfterMove = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
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
            if unResultAfterMove:
                aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unResultAfterMove, [ 'traversals',])
                
                unTraversalResultAfterMove =  unResultAfterMove[ 'traversals_by_name'].get( theReferenceFieldName, None)
                if unTraversalResultAfterMove:
                    
                    someElementResultsAfterMove = unTraversalResultAfterMove[ 'elements']
                    for unElementIndex in range( len( someElementResultsAfterMove)):
                        
                        unElementResult = someElementResultsAfterMove[ unElementIndex]
                        if unElementResult.get( 'UID', '') == theMovedReferenceUID:
                            
                            unMovedElementResult = unElementResult
                            unPositionAfterMove = unElementIndex
                            break
                        
            aMoveReport.update( { 'effect': 'moved', 'moved_element': unMovedElementResult, 'new_position': unPositionAfterMove, 'delta': 0, 'parent_traversal_name': theReferenceFieldName,})
             
            
            self.pSetAudit_Modification( theSourceElement, cModificationKind_MoveReferencedObject, aMoveReport)       
            
            return aMoveReport

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
        theModelDDvlPloneTool   = None,
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
    
            if ( theModelDDvlPloneTool == None) or ( theSourceElement == None) or not theReferenceFieldName or not theTargetUID:
                return None
      
            aReport = self.fNewVoidLinkReport()
            someSourceObjectReports = aReport[ 'source_object_reports']
            someTargetObjectReports = aReport[ 'target_object_reports']
            someLinkReports         = aReport[ 'link_reports']
            aFieldReportsByName     = {}
     
            aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContainerElement)
            if aModelDDvlPloneTool_Retrieval == None:
                aReportForObject = { 'effect': 'error', 'failure': 'no_fModelDDvlPloneTool_Retrieval',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
                
            
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
            
            unInverseRelationName = ''
            try:
                unInverseRelationName = unField.inverse_relationship
            except:
                None
          
            unInverseRelationFieldName = ''
            try:
                unInverseRelationFieldName = unField.inverse_relation_field_name
            except:
                None


            unTranslationsCaches        = aModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()
            unCheckedPermissionsCache   = aModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                
            unSourceElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
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
         
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unSourceElementResult, [ 'traversals', 'values',])

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
                
            unTargetElement = aModelDDvlPloneTool_Retrieval.fElementoPorUID( theTargetUID, theSourceElement)
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
                        
            unTargetElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
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
                
                aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unTargetElementResult, [ 'traversals','values',])

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

                aReportForLink = { 'effect': 'linked', 'source': unSourceElementResult, 'target': unTargetElementResult, 'relation': unRelationName, 'inverse_relation': unInverseRelationName}
                someLinkReports.append( aReportForLink)
                
                
                if not unaSourceTraversalResult.get( 'dependency_supplier', False):
                    unSourceObject = unSourceElementResult.get( 'object', None)
                    if not ( unSourceObject == None):
                        self.pSetAudit_Modification( unSourceObject, cModificationKind_Link, aReport)       

                if not unaTargetTraversalResult.get( 'dependency_supplier', False):
                    unTargetObject = unTargetElementResult.get( 'object', None)
                    if not ( unTargetObject == None):
                        self.pSetAudit_Modification( unTargetObject, cModificationKind_Link, aReport, theReverseRelation=True)
                 
                        
                return aReport

            else:
                
                theSourceElement.addReference( unTargetElement, unRelationName)
                
                self.pImpactReferenceIntoReport( theSourceElement, unSourceElementUID, theReferenceFieldName, unRelationName, aReport)

                aReportForLink = { 'effect': 'linked', 'source': unSourceElementResult, 'target': unTargetElementResult, 'relation': unRelationName,}
                someLinkReports.append( aReportForLink)
                
                
                if not unaSourceTraversalResult.get( 'dependency_supplier', False):
                    unSourceObject = unSourceElementResult.get( 'object', None)
                    if not ( unSourceObject == None):
                        self.pSetAudit_Modification( unSourceObject, cModificationKind_Link, aReport)       

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

            
            unInverseRelationName = ''
            try:
                unInverseRelationName = unField.inverse_relationship
            except:
                None
          
            unInverseRelationFieldName = ''
            try:
                unInverseRelationFieldName = unField.inverse_relation_field_name
            except:
                None

            unTranslationsCaches        = aModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()
            unCheckedPermissionsCache   = aModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()

            unSourceElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
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
         
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unSourceElementResult, [ 'traversals','values',])
            
            unaSourceTraversalResult = unSourceElementResult[ 'traversals_by_name'].get( theReferenceFieldName, {})
            if not unaSourceTraversalResult:
                aReportForObject = { 'effect': 'error', 'failure': 'traversal_not_retrieved',}
                someSourceObjectReports.append( aReportForObject)
                return aReport
                
            unosRelatedElements = [ unRelatedResult[ 'object'] for unRelatedResult in unaSourceTraversalResult.get( 'elements', [])]          
            
            unLimitToRelations = []
            if unInverseRelationFieldName:
                unLimitToRelations.append( unInverseRelationFieldName)

            unTargetElement = aModelDDvlPloneTool_Retrieval.fElementoPorUID( theTargetUID, theSourceElement)
            if not unTargetElement:
                aReportForObject = { 'effect': 'error', 'failure': 'get_by_uid_failure', }
                someTargetObjectReports.append( aReportForObject)
                return aReport    
                
            if not ( unTargetElement in unosRelatedElements):
                aReportForObject = { 'effect': 'error', 'failure': 'target_not_in_related_elements', }
                someTargetObjectReports.append( aReportForObject)
                return aReport                            
                        
            unTargetElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
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
                aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unTargetElementResult, [ 'traversals','values',])
                
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

                
                aReportForLink = { 'effect': 'unlinked', 'source': unSourceElementResult, 'target': unTargetElementResult, 'relation': unRelationName, 'inverse_relation': unInverseRelationName,}
                someLinkReports.append( aReportForLink)
                
                if not unaSourceTraversalResult.get( 'dependency_supplier', False):
                    unSourceObject = unSourceElementResult.get( 'object', None)
                    if not ( unSourceObject == None):
                        self.pSetAudit_Modification( unSourceObject, cModificationKind_Unlink, aReport)       

                if not unaTargetTraversalResult.get( 'dependency_supplier', False):
                    unTargetObject = unTargetElementResult.get( 'object', None)
                    if not ( unTargetObject == None):
                        self.pSetAudit_Modification( unTargetObject, cModificationKind_Unlink, aReport, theReverseRelation=True)                       
                
                return aReport

            else:
                
                theSourceElement.deleteReference( unTargetElement, unRelationName)
                
                self.pImpactReferenceIntoReport( theSourceElement, unSourceElementUID, theReferenceFieldName, unRelationName, aReport)
                
                aReportForLink = { 'effect': 'unlinked', 'source': unSourceElementResult, 'target': unTargetElementResult, 'relation': unRelationName}
                someLinkReports.append( aReportForLink)
                                
                if not unaSourceTraversalResult.get( 'dependency_supplier', False):
                    unSourceObject = unSourceElementResult.get( 'object', None)
                    if not ( unSourceObject == None):
                        self.pSetAudit_Modification( unSourceObject, cModificationKind_Unlink, aReport)       
                                                
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
            
                
    
    security.declarePrivate( 'fNewVoidDeleteElementReport')
    def fNewVoidCreateElementReport( self,):
        aReport = {
            'effect':                  'error',
            'failure':                 'not_executed',
            'container_result':        {},
            'impacted_objects_UIDs':   [],
            'field_reports':           [],
            'field_reports_by_name':   {},
        } 
        return aReport
    
    
    
    
    
    security.declarePrivate( 'fCrearElementoDeTipo')
    def fCrearElementoDeTipo(self, 
        theModelDDvlPloneTool   = None,
        theTimeProfilingResults =None,
        theContainerElement     =None, 
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

            aReport = self.fNewVoidCreateElementReport()

            if ( theModelDDvlPloneTool == None) or ( theContainerElement == None)  or not  theTypeName or not theTitle:
                aReport.update( { 'effect': 'error', 'failure': 'required_parameters_missing', })
                return aReport    

                
            aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContainerElement)
            if aModelDDvlPloneTool_Retrieval == None:
                aReport.update( { 'effect': 'error', 'failure': 'no_fModelDDvlPloneTool_Retrieval', })
                return aReport    

            
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
            
            
            
            unTranslationsCaches      = aModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()
            unCheckedPermissionsCache = aModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                        
            unResultadoContenedor = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
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
                aReport.update( { 'effect': 'error', 'failure': 'retrieval_failure', })
                return aReport     
        
            if not unResultadoContenedor[ 'read_permission']:
                aReport.update( { 'effect': 'error', 'failure': 'read_permission', })
                return aReport     
            
            if not unResultadoContenedor[ 'write_permission']:
                aReport.update( { 'effect': 'error', 'failure': 'write_persmission', })
                return aReport     
        
            if not unResultadoContenedor[ 'add_permission']:
                aReport.update( { 'effect': 'error', 'failure': 'add_persmission', })
                return aReport     
                
            if theAllowFactoryMethods:
                unNombreFactoryMethod = unResultadoContenedor.get( 'factory_methods', {}).get( theTypeName, '')            
                if unNombreFactoryMethod:
                    unFactoryMethod = None
                    try:
                        unFactoryMethod = theContainerElement[ unNombreFactoryMethod]
                    except:
                        None
                    if unFactoryMethod and unFactoryMethod.__class__.__name__ == 'instancemethod':
                        return unFactoryMethod( 
                            theTimeProfilingResults, 
                            self, 
                            theTypeName, 
                            unTitle, 
                            unaDescription, 
                            theAdditionalParams,
                            #theTimeProfilingResults          =theTimeProfilingResults, 
                            #theModelDDvlPloneTool_Mutators   =self, 
                            #theNewTypeName                   =theTypeName, 
                            #theNewOneTitle                   =unTitle, 
                            #theNewOneDescription             =unaDescription, 
                            #theAdditionalParams              =theAdditionalParams,
                            #thePermissionsCache              =None,
                            #theRolesCache                    =None,
                            #theParentExecutionRecord         =None,
                        )

             
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
                        aReport.update( { 'effect': 'error', 'failure': 'duplicate_title', })
                        return aReport     
                
                    
            unaFoundFactoryTypeName = False
            for unaTraversalResult in unResultadoContenedor.get( 'traversals', []):
                unasFactoriesAndTranslations = unaTraversalResult[ 'factories']
                for unaFactoryAndTranslations in unasFactoriesAndTranslations:
                    if theTypeName == unaFactoryAndTranslations[ 'meta_type']:
                        unaFoundFactoryTypeName = True
                        break                    
            if not unaFoundFactoryTypeName:
                aReport.update( { 'effect': 'error', 'failure': 'content_type_not_allowed', })
                return aReport     
                                
            
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
            
            aNewIdCreated = theContainerElement.invokeFactory( theTypeName, aNewIdWithCounter, **anAttrsDict)
            if not aNewIdCreated:
                aReport.update( { 'effect': 'error', 'failure': 'no_created_id', })
                return aReport     
           
            
            
            unosElementosEnContenedor = theContainerElement.objectValues( theTypeName)
            if not unosElementosEnContenedor:
                aReport.update( { 'effect': 'error', 'failure': 'empty_container_after_creation', })
                return aReport     
                
            unNuevoElementoCreado = None
                
            for unElementoEnContenedor in unosElementosEnContenedor:
                if unElementoEnContenedor.getId() == aNewIdCreated:
                    unNuevoElementoCreado = unElementoEnContenedor
                    break
            if ( unElementoEnContenedor == None):
                aReport.update( { 'effect': 'error', 'failure': 'created_element_not_found_in_container', })
                return aReport     
            
            unElementoEnContenedor.manage_fixupOwnershipAfterAdd()
            
            self.pSetElementPermissions( unElementoEnContenedor)
            
            
            #unNuevoResultadoContenedor = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
                #theTimeProfilingResults     =theTimeProfilingResults,
                #theElement                  =theContainerElement, 
                #theParent                   =None,
                #theParentTraversalName      ='',
                #theTypeConfig               =None, 
                #theAllTypeConfigs           =None, 
                #theViewName                 ='', 
                #theRetrievalExtents         =[ 'traversals', ],
                #theWritePermissions         =None,
                #theFeatureFilters           ={ 'attrs': [ 'title',], 'relations': [], 'do_not_recurse_collections': True,}, 
                #theInstanceFilters          =None,
                #theTranslationsCaches       =unTranslationsCaches,
                #theCheckedPermissionsCache  =unCheckedPermissionsCache,
                #theAdditionalParams         =theAdditionalParams                
            #)
            #if not unNuevoResultadoContenedor:
                #aReport.update( { 'effect': 'error', 'failure': 'retrieval_failure', })
                #return aReport     

            #unResultadoNuevoElementoEncontrado = None
            #for unaTraversalResult in unNuevoResultadoContenedor.get( 'traversals', []):
                #unosElementsResults = unaTraversalResult.get( 'elements', [])  
                #for unElementResult in unosElementsResults:
                    #if  unElementResult[ 'id'] == aNewIdWithCounter:
                        #unResultadoNuevoElementoEncontrado = unElementResult
                        #break
                    
            #if not unResultadoNuevoElementoEncontrado:
                #aReport.update( { 'effect': 'error', 'failure': 'factory_failure', })
                #return aReport     
            
            #aNewObject = unResultadoNuevoElementoEncontrado[ 'object']   
            
            aNewObject = unElementoEnContenedor
            
            self.pImpactCreateIntoReport( theContainerElement, aNewObject, aReport)            
                        
            unResultadoNuevoElemento = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
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
                #  aReport.update( { 'effect': 'error', 'failure': 'retrieval_failure', }
                return aReport     
            
            aReport.update( { 'effect': 'created', 'new_object_result': unResultadoNuevoElemento, })
            
            someFieldReports    = aReport[ 'field_reports']
            aFieldReportsByName = aReport[ 'field_reports_by_name']
            
            aReportForField = { 'attribute_name': 'id',          'effect': 'changed', 'new_value': aNewIdWithCounter, 'previous_value': '',}
            someFieldReports.append( aReportForField)            
            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
            
            aReportForField = { 'attribute_name': 'title',       'effect': 'changed', 'new_value': unTitle,           'previous_value': '',}
            someFieldReports.append( aReportForField)            
            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
            
            aReportForField = { 'attribute_name': 'description', 'effect': 'changed', 'new_value': unaDescription,    'previous_value': '',}
            someFieldReports.append( aReportForField)            
            aFieldReportsByName[ aReportForField[ 'attribute_name']] = aReportForField
                               
            self.pSetAudit_Creation( theContainerElement, cModificationKind_CreateSubElement, aReport, theUseCounter=True)       
            self.pSetAudit_Creation( aNewObject,          cModificationKind_Create,           aReport)       
                            
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
                                if ( not unNewCollectionCreateResult) or not ( unNewCollectionCreateResult[ 'effect'] == 'created'):
                                    # just cant initialize collection contents
                                    #  aReport.update( { 'effect': 'error', 'failure': 'collection_creation_failure', }
                                    #return aReport     
                                    None
            
            return aReport     
                
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fCrearElementoDeTipo', theTimeProfilingResults)

        
        
        
        
    
    
    security.declarePrivate( 'pImpactCreateIntoReport')
    def pImpactCreateIntoReport( self, theContainerElement, theNewObject, theCreateReport):

        if theCreateReport == None:
            return self
        
        if ( theContainerElement == None) or ( theNewObject== None):
            return self
        
        
        unosImpactedObjectsUIDs = theCreateReport[ 'impacted_objects_UIDs']

        unaUIDContainerElement = ''
        try:
            unaUIDContainerElement = theContainerElement.UID()
        except:
            None
        if unaUIDContainerElement:
            if not ( unaUIDContainerElement in unosImpactedObjectsUIDs):
                unosImpactedObjectsUIDs.append( unaUIDContainerElement)
   

        unContenedor = self.fImpactChangedContenedorYPropietario_IntoReport( theContainerElement, theCreateReport)

        unosSiblings = theContainerElement.objectValues()

        for unSibling in unosSiblings:
            
            if not ( unSibling == theNewObject):
                
                unaUIDSiblingToImpact = ''
                try:
                    unaUIDSiblingToImpact = unSibling.UID()
                except:
                    None
                if unaUIDSiblingToImpact:
                    if not ( unaUIDSiblingToImpact in unosImpactedObjectsUIDs):
                        unosImpactedObjectsUIDs.append( unaUIDSiblingToImpact)
        
        return self
    
    
    
    
    
    
    security.declarePrivate( 'fImpactCreatePloneUIDs')
    def fImpactCreatePloneUIDs( self, theContainerElement, ):

        if theContainerElement == None:
            return []
        
        unosImpactedObjectsUIDs = [ ]

        unaUIDContainerElement = ''
        try:
            unaUIDContainerElement = theContainerElement.UID()
        except:
            None
        if unaUIDContainerElement:
            if not ( unaUIDContainerElement in unosImpactedObjectsUIDs):
                unosImpactedObjectsUIDs.append( unaUIDContainerElement)
   
        unContenedor = self.fImpactChangedContenedorYPropietario_IntoReport( theContainerElement, { 'impacted_objects_UIDs':   unosImpactedObjectsUIDs, })

        unosSiblings = theContainerElement.objectValues()

        for unSibling in unosSiblings:
        
            unaUIDSiblingToImpact = ''
            try:
                unaUIDSiblingToImpact = unSibling.UID()
            except:
                None
            if unaUIDSiblingToImpact:
                if not ( unaUIDSiblingToImpact in unosImpactedObjectsUIDs):
                    unosImpactedObjectsUIDs.append( unaUIDSiblingToImpact)
        
        return unosImpactedObjectsUIDs
    
    
    
    
    
         
        
        
        
     
    
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

            aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theElement)
            if aModelDDvlPloneTool_Retrieval == None:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'No fModelDDvlPloneTool_Retrieval', })
                return aDeleteReport                 
                        
            unSecondsNow = fSecondsNow()            
            if not(  (unSecondsNow >= theRequestSeconds) and ( unSecondsNow - theRequestSeconds) < theModelDDvlPloneTool.fSecondsToReviewAndDelete( theElement)):
                aDeleteReport.update( { 'effect': 'error', 'failure': 'time_out', })
                return aDeleteReport                 
    
            if ( theElement == None) or ( not theIdToDelete) or ( not theUIDToDelete) or ( not theRequestSeconds):
                aDeleteReport.update( { 'effect': 'error', 'failure': 'required_parameters_missing', })
                return aDeleteReport     
                
            unTargetElement = aModelDDvlPloneTool_Retrieval.fElementoPorUID( theUIDToDelete, theElement)
            if not unTargetElement:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'get_by_uid_failure', })
                return aDeleteReport    

            unElementDeleteImpactReport = aModelDDvlPloneTool_Retrieval.fDeleteImpactReport( 
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
                    
            
            
            self.pImpactDeleteImpactReportIntoReport( aModelDDvlPloneTool_Retrieval, unTargetElement, unElementDeleteImpactReport, aDeleteReport)
            
            aDeleteReport.update( { 
                'effect':                'deleted', 
                'parent_traversal_name': unElementDeleteImpactReport[ 'parent_traversal_name'], 
                'impact_report':         unElementDeleteImpactReport,
            })
                  
            self.pSetAudit_Modification( theElement, cModificationKind_DeleteSubElement, aDeleteReport)     
            
            # ACV We are not really keeping defunct objects at this time, so we do not expend the effort on object that shall be gone immediately.
            # self.pSetAudit_Deletion( unTargetElement, cModificationKind_Delete, aDeleteReport)  
            
         
            theElement.manage_delObjects( [ unaIdAEliminar, ])
           
            return aDeleteReport     
    
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fEliminarElemento', theTimeProfilingResults)

                
         
                
                
                

   
    
    security.declarePrivate( 'pImpactDeleteImpactReportIntoReport')
    def pImpactDeleteImpactReportIntoReport( self, theModelDDvlPloneTool_Retrieval, theElement, theElementDeleteImpactReport, theDeleteReport):
 
        if ( theModelDDvlPloneTool_Retrieval == None) or ( theElement == None) or ( not theElementDeleteImpactReport) or ( not theDeleteReport):
            return self
    
        unosElementsToBeDeleted, unosRelatedElements = theModelDDvlPloneTool_Retrieval.fObjectsToDeleteAndRelated_FromImpactReport( theElementDeleteImpactReport)
        
        
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

            aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContainerElement)
            if aModelDDvlPloneTool_Retrieval == None:
                return [  { 'effect': 'error', 'failure': 'No fModelDDvlPloneTool_Retrieval', }, ]
            
            unSecondsNow = fSecondsNow()            
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
                unElementToDelete = aModelDDvlPloneTool_Retrieval.fElementoPorUID( anElementUID, theContainerElement)
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
            
            #unAuditedContainerModification = False
                
            unElementDeleteImpactReport = None
            for anElementUID, anElementId, unElementToDelete in someElementsToDelete:
                              
                aDeleteReport = self.fNewVoidDeleteElementReport()
            
                unElementDeleteImpactReport = aModelDDvlPloneTool_Retrieval.fDeleteImpactReport( 
                    theModelDDvlPloneTool   =theModelDDvlPloneTool,
                    theTimeProfilingResults =theTimeProfilingResults,
                    theElement              =unElementToDelete,
                    theAdditionalParams     =theAdditionalParams
                )
    
                if not unElementDeleteImpactReport:
                    aDeleteReport.update( { 'effect': 'error', 'failure': 'impact_report_retrieval_failure',  'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,})
                    someElementDeleteReports.append( aDeleteReport)
                    
                elif not unElementDeleteImpactReport[ 'here'][ 'container_element'][ 'object'] == theContainerElement:
                    aDeleteReport.update( { 'effect': 'error', 'failure': 'wrong_container_element', 'impact_report': unElementDeleteImpactReport,  'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,})
                    someElementDeleteReports.append( aDeleteReport)
                            
                elif not unElementDeleteImpactReport[ 'delete_permission']:
                    aDeleteReport.update( { 'effect': 'error', 'failure': 'no_delete_permission', 'impact_report': unElementDeleteImpactReport,  'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,})
                    someElementDeleteReports.append( aDeleteReport)
                        
                else:
                    unaIdAEliminar = unElementDeleteImpactReport[ 'here'][ 'id']
                    if not unaIdAEliminar:
                        aDeleteReport.update( { 'effect': 'error', 'failure': 'element_to_delete_without_id', 'impact_report': unElementDeleteImpactReport,  'uid': anElementUID, 'id': anElementId, 'element': unElementToDelete,})
                        someElementDeleteReports.append( aDeleteReport)
        
                    else:
                        
                        self.pImpactDeleteImpactReportIntoReport( unElementToDelete, unElementDeleteImpactReport, aDeleteReport)
                        
                        unParentTraversalName = ( unElementDeleteImpactReport and unElementDeleteImpactReport[ 'parent_traversal_name']) or ''
                        
                        aDeleteReport.update( { 'effect': 'deleted', 'parent_traversal_name': unParentTraversalName, 'impact_report': unElementDeleteImpactReport,})
                        someElementDeleteReports.append( aDeleteReport)
                        
                        #if not unAuditedContainerModification:
                        self.pSetAudit_Modification( theContainerElement, cModificationKind_DeleteSubElement, aDeleteReport)    
                            #unAuditedContainerModification = True
                        
                        # ACV We are not really keeping defunct objects at this time, so we do not expend the effort on object that shall be gone immediately.
                        # self.pSetAudit_Deletion( unElementToDelete, cModificationKind_Delete, aDeleteReport)  
                        
                        theContainerElement.manage_delObjects( [ unaIdAEliminar, ])
                        
    
            return someElementDeleteReports
    
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
        
    
    
    
    
    
    security.declarePrivate(   'fMethodNameSetPermissionsElement')
    def fMethodNameSetPermissionsElement(self, theElement,):     
        if ( theElement == None):
            return ''
        
        aMethodName = ''
        try:
            aMethodName = theElement.fMethodNameSetPermissions()
        except:
            None
            
        return aMethodName
    
    
    
    
    security.declarePrivate(   'fMethodSetPermissionsElement')
    def fMethodSetPermissionsElement(self, theElement,):     
        if ( theElement == None):
            return None
        
        aMethodName = self.fMethodNameSetPermissionsElement( theElement,)
        if not aMethodName:
            return None
        
        aMethod = None
        try:
            aMethod = getattr( theElement, aMethodName)
        except:
            None
            
        return aMethod
    
    
        
    
    security.declarePrivate(   'pSetElementPermissions')
    def pSetElementPermissions(self, theElement, thePermissionsNotToSet=[],):     
        if ( theElement == None):
            return self

        aPermissionsSet = False
        
        aMethod = self.fMethodSetPermissionsElement( theElement)
        if aMethod:
            
            try:
                aMethod()
                aPermissionsSet = True
            except:
                None
        
            
        if not aPermissionsSet:
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
    def fGetAudit_MemberIdAndNow(self, theElement):     
    
        unMemberId = ''
        
        aMembershipTool = getToolByName( theElement, 'portal_membership', None)
        if aMembershipTool:
            unMember = aMembershipTool.getAuthenticatedMember()   
            if unMember:
                if unMember.getUserName() == 'Anonymous User':
                    unMemberId = unMember.getUserName()
                else:
                    unMemberId = unMember.getMemberId()   
    
        unAhora = int( time() * 1000)
    
        return [ unMemberId, unAhora,]
    
    
    

    
        
        
        
        
        
        
        
        
        
    
    security.declarePrivate(   'pSetAudit_Creation')
    def pSetAudit_Creation(self, theElement, theChangeKind, theChangeReport, theUseCounter=False):     
        if ( theElement == None):
            return self
        
        unMemberId, unAhora = self.fGetAudit_MemberIdAndNow( theElement)
      
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
                
                
        unSchema = theElement.schema
        if not unSchema:
            return self
            
        if unCreationDateFieldName:
            unCreationDateField = unSchema.get( unCreationDateFieldName, )
            if unCreationDateField:
                unMutator = unCreationDateField.getMutator( theElement)
                if unMutator:
                    unDateValue = DateTime( unAhora / 1000)
                    try:
                        unMutator( unDateValue) 
                    except:
                        None
                            
        if unCreationUserFieldName:
            unCreationUserField = unSchema.get( unCreationUserFieldName, )
            if unCreationUserField:
                unMutator = unCreationUserField.getMutator( theElement)
                if unMutator:
                    try:
                        unMutator( unMemberId) 
                    except:
                        None

                        
        unNewCounter = 0
        if theUseCounter:
            
            unChangeCounterFieldName = ''
            try:
                unChangeCounterFieldName = theElement.change_counter_field
            except:
                None
                
            if unChangeCounterFieldName:
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
                        
                        
        self.pAppendToChangeLog(  theElement, theChangeKind, theChangeReport, False, unMemberId, unAhora, unNewCounter)
                                        
        return self
    
    

    
    
    security.declarePrivate(   'pSetAudit_Modification')
    def pSetAudit_Modification(self, theElement, theChangeKind, theChangeReport, theReverseRelation=False):     
        if ( theElement == None):
            return self
      
        unMemberId, unAhora = self.fGetAudit_MemberIdAndNow( theElement)
      
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
                
                
        
        unSchema = theElement.schema
        if not unSchema:
            return self
            
        unNewCounter = 0
        
        if unChangeCounterFieldName:
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
                        
        if unModificationDateFieldName:
            unModificationDateField = unSchema.get( unModificationDateFieldName, )
            if unModificationDateField:
                unMutator = unModificationDateField.getMutator( theElement)
                if unMutator:
                    unDateValue = DateTime( unAhora / 1000)
                    try:
                        unMutator( unDateValue) 
                    except:
                        None         
                        
        if unModificationUserFieldName:
            unModificationUserField = unSchema.get( unModificationUserFieldName, )
            if unModificationUserField:
                unMutator = unModificationUserField.getMutator( theElement)
                if unMutator:
                    try:
                        unMutator( unMemberId) 
                    except:
                        None
                        
        self.pAppendToChangeLog(  theElement, theChangeKind, theChangeReport, theReverseRelation, unMemberId, unAhora, unNewCounter)
                                        
        return self
        

    
  
    
  
    security.declarePrivate(   'pSetAudit_Deletion')
    def pSetAudit_Deletion(self, theElement, theChangeKind, theChangeReport):     
        if ( theElement == None):
            return self
        
        
        unMemberId, unAhora = self.fGetAudit_MemberIdAndNow( theElement)
      
        self.pSetAudit_Deletion_recursive( theElement, unMemberId, unAhora, theChangeKind, theChangeReport)
        
        
        return self    
    
    
    

    security.declarePrivate(   'pSetAudit_Deletion_recursive')
    def pSetAudit_Deletion_recursive(self, theElement, theMemberId, theAhora, theChangeKind, theChangeReport):     
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
                        unDateValue = DateTime( theAhora / 1000)
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
                            
        self.pAppendToChangeLog(  theElement, theChangeKind, theChangeReport, False, theMemberId, theAhora, -1)

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
                
        
    
    
    
    

    
    security.declarePrivate('pAppendToChangeLog')
    def pAppendToChangeLog(self, 
        theElement                  =None, 
        theChangeKind               =None,
        theChangeReport             =None,
        theReverseRelation          =False,
        theMemberId                 =None, 
        theAhora                    =None,
        theChangeCounter            =None):
        """Append a new entry to the change log.
        
        """
        
        
        if ( theElement == None):
            return self

        unSchema = theElement.schema
        if not unSchema:
            return self
                        
        unFieldName = self.fChangeLogFieldNameForElement( theElement)
        
        if not unFieldName:
            return self
                     
        unField = unSchema.get( unFieldName, None)
        if not unField:
            return self
        
        unAccessor = unField.getAccessor( theElement)
        if not unAccessor:
            return self
        
        unMutator = unField.getMutator( theElement)
        if not unMutator:
            return self
        
        
        
        
        aCurrentLogValueString = None
        try:
            aCurrentLogValueString = unAccessor()
        except:
            None
            
        aCurrentLogObject = None
        if aCurrentLogValueString:
            aCurrentLogObject = fEvalString( aCurrentLogValueString)
            if not ( aCurrentLogObject == None):
                if not isinstance( aCurrentLogObject, list):
                    aCurrentLogObject = [ aCurrentLogObject,]
                    
                    
                    
        aLastChangeEntry = None
        if aCurrentLogObject:
            aLastChangeEntry = aCurrentLogObject[ 0]
            
        aNewChangeEntry, anIsSameAsExisting = self.fNewChangeEntry_AndIsSameAs( theElement, theChangeKind, theChangeReport, theReverseRelation, theMemberId, theAhora, theChangeCounter, aLastChangeEntry)
        if not aNewChangeEntry:
            return self
        
        
        aNewLogObject = []
        if aCurrentLogObject:
            aNewLogObject = aCurrentLogObject[:]
        if anIsSameAsExisting:
            if aLastChangeEntry in aNewLogObject: # ACV 20091203 redundant
                aNewLogObject.remove( aLastChangeEntry)
            
        aNewLogObject = [ aNewChangeEntry,] + aNewLogObject
            
        aNewLogValueString = fReprAsString( aNewLogObject)
        
        unMutator( aNewLogValueString)
        
        aModelDDvlPloneTool_Transactions = ModelDDvlPloneTool_Transactions()
        if aModelDDvlPloneTool_Transactions.fTransaction_CanAppendNote():
            aChangeTransactionNote = self.fChangeEntryAsTransactionNote( theElement, aNewChangeEntry, None)
            if aChangeTransactionNote:
                aModelDDvlPloneTool_Transactions.fTransaction_AppendNote( aChangeTransactionNote)
                               
        return self
        





        
           
    
    def fMustLogValueChanges( self, theElement):
        """To delegate in the ModelDDvlPloneTool singleton, that shall have a configuration parameter, and to the root of the element model, which may override and turn off the log values settign in the tool.
        
        """
        return True
    
    

    
    def fNewChangeEntry_AndIsSameAs( self,       
        theElement                  =None, 
        theChangeKind               =None,
        theChangeReport             =None,
        theReverseRelation          =False,
        theMemberId                 =None, 
        theAhora                    =None,
        theChangeCounter            =None,
        theExistingChangeEntry      =None):
        
        aMustLogValueChanges = self.fMustLogValueChanges( theElement)
        
        someDetails = None
        
        unaNewChangeEntry = self.fNewChangeEntry(       
            theElement                  =theElement, 
            theChangeKind               =theChangeKind,
            theChangeReport             =theChangeReport,
            theReverseRelation          =theReverseRelation,
            theMemberId                 =theMemberId, 
            theAhora                    =theAhora,
            theChangeCounter            =theChangeCounter,
        )
        
        if not theExistingChangeEntry:
            return [ unaNewChangeEntry, False, ]
        
        if self.fChangeEntrySameAs( unaNewChangeEntry, theExistingChangeEntry):
            return [ unaNewChangeEntry, True, ]
        
        return [ unaNewChangeEntry, False, ]
    
    
    
    
    def fChangeEntrySameAs( self, theNewChangeEntry, theExistingChangeEntry):   
        if ( not theNewChangeEntry) or ( not theExistingChangeEntry):
            return False
            
        aChangeKind = theNewChangeEntry.get( cChangeDetails_ChangeKind, '')
            
        if not( aChangeKind == theExistingChangeEntry.get( cChangeDetails_ChangeKind, '')):
            return False
        
        if not( theNewChangeEntry.get( cChangeDetails_UserId, '')     == theExistingChangeEntry.get( cChangeDetails_UserId, '')):
            return False
        
        aNewChangeMillis      = theNewChangeEntry.get( cChangeDetails_ChangeDate, 0)
        aExistingChangeMillis = theExistingChangeEntry.get( cChangeDetails_ChangeDate, 0)
        
        if ( aNewChangeMillis or aExistingChangeMillis):
            if abs( aNewChangeMillis - aExistingChangeMillis) > cMaxChangeMillisDifference_ForSameEntries:
                return False
        

        #if theAhora:
            #aNewChangeEntry[ cChangeDetails_ChangeDate]   = theAhora
            
        #if not ( theChangeCounter == None):
            #aNewChangeEntry[ cChangeDetails_ChangeCounter]  = theChangeCounter

        someNewDetails      = theNewChangeEntry.get( cChangeDetails_Details, {})
        someExistingDetails = theExistingChangeEntry.get( cChangeDetails_Details, {})
            
        if aChangeKind == cModificationKind_ChangeValues_abbr:
            
            someNewFieldChanges      = someNewDetails.get( cChangeDetails_FieldChanges, [])
            someExistingFieldChanges = someExistingDetails.get( cChangeDetails_FieldChanges, [])
            
            if ( someNewFieldChanges or someExistingFieldChanges) and not ( someNewFieldChanges == someExistingFieldChanges):
                return False
            
            someNewChangedValues      = someNewDetails.get( cChangeDetails_NewFieldValue, {})
            someExistingChangedValues = someExistingDetails.get( cChangeDetails_NewFieldValue, {})
            if ( someNewChangedValues or someExistingChangedValues) and not ( someNewChangedValues and someExistingChangedValues):
                return False

            if ( not someNewChangedValues)  and ( not someExistingChangedValues):
                return True
            
            unasNewChangeValueFieldNames      = someNewChangedValues.keys()
            unasExistingChangeValueFieldNames = someExistingChangedValues.keys()
            
            if ( unasNewChangeValueFieldNames or unasExistingChangeValueFieldNames) and not ( someNewFieldChanges == someExistingFieldChanges):
                return False
            
            if ( not unasNewChangeValueFieldNames)  and ( not unasExistingChangeValueFieldNames):
                return True
            
            for unValueFieldName in unasNewChangeValueFieldNames:
                unNewValue      = someNewChangedValues.get( unValueFieldName, '')
                unExistingValue = someExistingChangedValues.get( unValueFieldName, '')
                if not ( unNewValue == unExistingValue):
                    return False
                
            return True
                
                
                
                    
        elif aChangeKind == cModificationKind_Link_abbr:
            return False
            #someLinkChangeReports = theChangeReport.get( 'link_reports', [])
            #for aLinkChangeReport in someLinkChangeReports:
                #if aLinkChangeReport.get( 'effect', '') == 'linked':
                    
                    #if theReverseRelation:
                        
                        #unRelation     = aLinkChangeReport.get( 'inverse_relation', '')
                        #unTargetResult = aLinkChangeReport.get( 'source',   {})                
                        
                    #else:
                        #unRelation     = aLinkChangeReport.get( 'relation', '')
                        #unTargetResult = aLinkChangeReport.get( 'target',   {})
                        
                    #unTargetTitle  = unTargetResult.get(  'title', '')
                    #unTargetPath   = unTargetResult.get(  'path', '')
                    #unTargetUID    = unTargetResult.get(  'UID', '')
                    
                    #unLinkDetails = { }
                    #if unRelation:
                        #unLinkDetails[ cChangeDetails_Relation]   = unRelation
                    #if unTargetTitle:
                        #unLinkDetails[ cChangeDetails_TargetTitle]= unTargetTitle
                    #if unTargetPath:
                        #unLinkDetails[ cChangeDetails_TargetPath] = unTargetPath
                    #if unTargetUID:
                        #unLinkDetails[ cChangeDetails_TargetUID]  = unTargetUID
                    #if unLinkDetails:
                        #someDetails = unLinkDetails
                        
                        
                        
                        
        elif aChangeKind == cModificationKind_Unlink_abbr:
            return False
            #someUnlinkChangeReports = theChangeReport.get( 'link_reports', [])
            #for aUnlinkChangeReport in someUnlinkChangeReports:
                #if aUnlinkChangeReport.get( 'effect', '') == 'unlinked':
                    
                    #if theReverseRelation:
                        
                        #unRelation     = aUnlinkChangeReport.get( 'inverse_relation', '')
                        #unTargetResult = aUnlinkChangeReport.get( 'source',   {})                
                        
                    #else:
                        #unRelation     = aUnlinkChangeReport.get( 'relation', '')
                        #unTargetResult = aUnlinkChangeReport.get( 'target',   {})
                    
                    #unTargetTitle  = unTargetResult.get(  'title', '')
                    #unTargetPath   = unTargetResult.get(  'path', '')
                    #unTargetUID    = unTargetResult.get(  'UID', '')
                    
                    #unUnlinkDetails = { }
                    #if unRelation:
                        #unUnlinkDetails[ cChangeDetails_Relation]    = unRelation
                    #if unTargetTitle:
                        #unUnlinkDetails[ cChangeDetails_TargetTitle] = unTargetTitle
                    #if unTargetPath:
                        #unUnlinkDetails[ cChangeDetails_TargetPath]  = unTargetPath
                    #if unTargetUID:
                        #unUnlinkDetails[ cChangeDetails_TargetUID]   = unTargetUID
                    #if unUnlinkDetails:
                        #someDetails = unUnlinkDetails
                        
                        
                        
                        
        elif aChangeKind == cModificationKind_CreateSubElement_abbr:  
            return False
            #if theChangeReport.get( 'effect', '') == 'created':
                
                #unNewObjectResult = theChangeReport.get( 'new_object_result', {})
                #if unNewObjectResult and not ( unNewObjectResult.get( 'object', None) == None):
                    
                    #unNewElementTitle         = unNewObjectResult.get( 'title', '')
                    #unNewElementId            = unNewObjectResult.get( 'id', '')
                    #unNewElementUID           = unNewObjectResult.get( 'UID', '')
                    #unNewElementMetaType      = unNewObjectResult.get( 'meta_type', '')
                    #unNewElementArchetypeName = unNewObjectResult.get( 'archetype_name', '')
                    
                    #unCreateDetails = { }
                    
                    #if unNewElementTitle:
                        #unCreateDetails[ cChangeDetails_NewElementTitle]         = unNewElementTitle
                    #if unNewElementId:
                        #unCreateDetails[ cChangeDetails_NewElementId]            = unNewElementId
                    #if unNewElementUID:
                        #unCreateDetails[ cChangeDetails_NewElementUID]           = unNewElementUID                        
                    #if unNewElementMetaType:
                        #unCreateDetails[ cChangeDetails_NewElementMetaType]      = unNewElementMetaType                        
                    #if unNewElementArchetypeName:
                        #unCreateDetails[ cChangeDetails_NewElementArchetypeName] = unNewElementArchetypeName                        
            
                    #someChangedFieldNames = [ ]
                    #someChangedValues     = { }
                    
                    #someFieldChangeReports = theChangeReport.get( 'field_reports', [])
                    #for aFieldChangeReport in someFieldChangeReports:
                        #if aFieldChangeReport.get( 'effect', '') == 'changed':
                            
                            #aChangedFieldName = aFieldChangeReport.get( 'attribute_name', '')
                            #if aChangedFieldName:
                                #if aMustLogValueChanges:
                                    #someChangedValues[ aChangedFieldName] = aFieldChangeReport.get( 'new_value', None)
                                #else:
                                    #someChangedFieldNames.append( aChangedFieldName)
                    #if aMustLogValueChanges:   
                        #if someChangedValues:
                            #unCreateDetails[ cChangeDetails_NewFieldValue] = someChangedValues
                    #elif someChangedFieldNames:
                        #unCreateDetails[ cChangeDetails_FieldChanges] = someChangedFieldNames
                        
                    #if unCreateDetails:
                        #someDetails = unCreateDetails
                        
                        
                        
                        
                        
        elif aChangeKind == cModificationKind_Create_abbr:  
            return False
            #if theChangeReport.get( 'effect', '') == 'created':
                
                #unNewObjectResult = theChangeReport.get( 'new_object_result', {})
                #if unNewObjectResult and not ( unNewObjectResult.get( 'object', None) == None):
                    
                    #unNewElementTitle         = unNewObjectResult.get( 'title', '')
                    #unNewElementId            = unNewObjectResult.get( 'id', '')
                    #unNewElementUID           = unNewObjectResult.get( 'UID', '')
                    #unNewElementMetaType      = unNewObjectResult.get( 'meta_type', '')
                    #unNewElementArchetypeName = unNewObjectResult.get( 'archetype_name', '')
                    
                    #unCreateDetails = { }
                    
                    #if unNewElementTitle:
                        #unCreateDetails[ cChangeDetails_NewElementTitle]         = unNewElementTitle
                    #if unNewElementId:
                        #unCreateDetails[ cChangeDetails_NewElementId]            = unNewElementId
                    #if unNewElementUID:
                        #unCreateDetails[ cChangeDetails_NewElementUID]           = unNewElementUID                        
                    #if unNewElementMetaType:
                        #unCreateDetails[ cChangeDetails_NewElementMetaType]      = unNewElementMetaType                        
                    #if unNewElementArchetypeName:
                        #unCreateDetails[ cChangeDetails_NewElementArchetypeName] = unNewElementArchetypeName                        
            
                    #someChangedFieldNames = [ ]
                    #someChangedValues     = { }
                    
                    #someFieldChangeReports = theChangeReport.get( 'field_reports', [])
                    #for aFieldChangeReport in someFieldChangeReports:
                        #if aFieldChangeReport.get( 'effect', '') == 'changed':
                            
                            #aChangedFieldName = aFieldChangeReport.get( 'attribute_name', '')
                            #if aChangedFieldName:
                                #if aMustLogValueChanges:
                                    #someChangedValues[ aChangedFieldName] = aFieldChangeReport.get( 'new_value', None)
                                #else:
                                    #someChangedFieldNames.append( aChangedFieldName)
                    #if aMustLogValueChanges:   
                        #if someChangedValues:
                            #unCreateDetails[ cChangeDetails_NewFieldValue] = someChangedValues
                    #elif someChangedFieldNames:
                        #unCreateDetails[ cChangeDetails_FieldChanges] = someChangedFieldNames
                        
                    #if unCreateDetails:
                        #someDetails = unCreateDetails
                        
                        
                        
                        
                        
        elif aChangeKind == cModificationKind_DeleteSubElement_abbr:  
            return False
            #if theChangeReport.get( 'effect', '') == 'deleted':
                
                #unDeletedImpactReport = theChangeReport.get( 'impact_report', {})
                
                #someElementsToDelete, someAffectedElements = ModelDDvlPloneTool_Retrieval().fObjectsToDeleteAndRelated_FromImpactReport( unDeletedImpactReport)
                #unDeletedObjectResult = unDeletedImpactReport.get( 'here', {})
                #if unDeletedObjectResult:
                    
                    #unDeletedElement = unDeletedObjectResult.get( 'object', None)
                                         
                    #if not ( unDeletedElement == None):
                    
                        #unDeletedElementTitle         = unDeletedObjectResult.get( 'title', '')
                        #unDeletedElementId            = unDeletedObjectResult.get( 'id', '')
                        #unDeletedElementUID           = unDeletedObjectResult.get( 'UID', '')
                        #unDeletedElementMetaType      = unDeletedObjectResult.get( 'meta_type', '')
                        #unDeletedElementArchetypeName = unDeletedObjectResult.get( 'archetype_name', '')
                        
                        #unDeletedDetails = { }
                        
                        #if unDeletedElementTitle:
                            #unDeletedDetails[ cChangeDetails_DeletedElementTitle]         = unDeletedElementTitle
                        #if unDeletedElementId:
                            #unDeletedDetails[ cChangeDetails_DeletedElementId]            = unDeletedElementId
                        #if unDeletedElementUID:
                            #unDeletedDetails[ cChangeDetails_DeletedElementUID]           = unDeletedElementUID                        
                        #if unDeletedElementMetaType:
                            #unDeletedDetails[ cChangeDetails_DeletedElementMetaType]      = unDeletedElementMetaType                        
                        #if unDeletedElementArchetypeName:
                            #unDeletedDetails[ cChangeDetails_DeletedElementArchetypeName] = unDeletedElementArchetypeName        
                                                  
                        #unDeletedElementPath = unDeletedElement.getPhysicalPath()
                        
                        #someDeletedElementsDetails = [ ]
                        #for unSubDeletedElement in someElementsToDelete:
                            #if not ( unSubDeletedElement == unDeletedElement):
                                
                                #unSubDeletedElementPath = []
                                #try:
                                    #unSubDeletedElementPath = unSubDeletedElement.getPhysicalPath()
                                #except:
                                    #None
                                #if unSubDeletedElementPath:
                                    #unSubDeletedElementPath = unSubDeletedElementPath[ len( unDeletedElementPath):]
                                #if not unSubDeletedElementPath:
                                    #unSubDeletedElementPath = ''
                                #else:
                                    #unSubDeletedElementPath = '/'.join( unSubDeletedElementPath)                                    
                                #unSubDeletedElementUID = ''
                                #try:
                                    #unSubDeletedElementUID = unSubDeletedElement.UID()
                                #except:
                                    #None
                                #unSubDeletedElementMetaType = ''
                                #try:
                                    #unSubDeletedElementMetaType = unSubDeletedElement.meta_type
                                #except:
                                    #None
                                #unSubDeletedElementArchetypeName = ''
                                #try:
                                    #unSubDeletedElementArchetypeName = unSubDeletedElement.archetype_name
                                #except:
                                    #None
                                
                                #unSubDeletedElementDetails = { }
                                #if unSubDeletedElementPath:
                                    #unSubDeletedElementDetails[ cChangeDetails_DeletedElementPath]          = unSubDeletedElementPath
                                #if unSubDeletedElementUID:
                                    #unSubDeletedElementDetails[ cChangeDetails_DeletedElementUID]           = unSubDeletedElementUID                        
                                #if unSubDeletedElementMetaType:
                                    #unSubDeletedElementDetails[ cChangeDetails_DeletedElementMetaType]      = unSubDeletedElementMetaType                        
                                #if unSubDeletedElementArchetypeName:
                                    #unSubDeletedElementDetails[ cChangeDetails_DeletedElementArchetypeName] = unSubDeletedElementArchetypeName        
                                #if unSubDeletedElementDetails:
                                    #someDeletedElementsDetails.append( unSubDeletedElementDetails)
                        
                        #if someDeletedElementsDetails:   
                            #unDeletedDetails.update( { 
                                #cChangeDetails_IncludedDeleted:    someDeletedElementsDetails,  
                            #})
                            
                        #if unDeletedDetails:
                            #someDetails = unDeletedDetails
            
                        
                            
                            
                            
        elif aChangeKind == cModificationKind_DeletePloneSubElement_abbr:  
            return False
            #if theChangeReport.get( 'effect', '') == 'deleted':
                                
                #unDeletedObjectResult = theChangeReport.get( 'plone_element_result', {})
                #if unDeletedObjectResult:
                    
                    #unDeletedElement = unDeletedObjectResult.get( 'object', None)
                                         
                    #if not ( unDeletedElement == None):
                    
                        #unDeletedElementTitle         = unDeletedObjectResult.get( 'title', '')
                        #unDeletedElementId            = unDeletedObjectResult.get( 'id', '')
                        #unDeletedElementUID           = unDeletedObjectResult.get( 'UID', '')
                        #unDeletedElementMetaType      = unDeletedObjectResult.get( 'meta_type', '')
                        #unDeletedElementArchetypeName = unDeletedObjectResult.get( 'archetype_name', '')
                        
                        #unDeletedDetails = { }
                        
                        #if unDeletedElementTitle:
                            #unDeletedDetails[ cChangeDetails_DeletedElementTitle]         = unDeletedElementTitle
                        #if unDeletedElementId:
                            #unDeletedDetails[ cChangeDetails_DeletedElementId]            = unDeletedElementId
                        #if unDeletedElementUID:
                            #unDeletedDetails[ cChangeDetails_DeletedElementUID]           = unDeletedElementUID                        
                        #if unDeletedElementMetaType:
                            #unDeletedDetails[ cChangeDetails_DeletedElementMetaType]      = unDeletedElementMetaType                        
                        #if unDeletedElementArchetypeName:
                            #unDeletedDetails[ cChangeDetails_DeletedElementArchetypeName] = unDeletedElementArchetypeName        
                        #if unDeletedDetails:
                            #someDetails = unDeletedDetails
           
                            
                            
                            
                        
        elif aChangeKind in [ cModificationKind_MoveSubObject_abbr, cModificationKind_MovePloneSubObject_abbr, cModificationKind_MoveReferencedObject_abbr,]:

            unNewMovedElementTitle          = someNewDetails.get( cChangeDetails_MovedElementTitle, '')
            unNewMovedElementId             = someNewDetails.get( cChangeDetails_MovedElementId, '')
            unNewMovedElementUID            = someNewDetails.get( cChangeDetails_MovedElementUID, '')
            unNewPosition                   = someNewDetails.get( cChangeDetails_Position, '')
            unNewDelta                      = someNewDetails.get( cChangeDetails_Delta, '')
            # ACV 20091202 TraversalName not informed by the container elements move objects by delta
            #
            #unNewTraversalName              = someNewDetails[     cChangeDetails_TraversalName]
            
            unExistingMovedElementTitle     = someExistingDetails.get( cChangeDetails_MovedElementTitle, '')
            unExistingMovedElementId        = someExistingDetails.get( cChangeDetails_MovedElementId, '')
            unExistingMovedElementUID       = someExistingDetails.get( cChangeDetails_MovedElementUID, '')
            unExistingPosition              = someExistingDetails.get( cChangeDetails_Position, '')
            unExistingDelta                 = someExistingDetails.get( cChangeDetails_Delta, '')
            # ACV 20091202 TraversalName not informed by the container elements move objects by delta
            #
            #unExistingTraversalName         = someExistingDetails[     cChangeDetails_TraversalName]
            
            if ( unNewMovedElementTitle or unExistingMovedElementTitle) and not ( unNewMovedElementTitle == unExistingMovedElementTitle):
                return False
            if ( unNewMovedElementId    or unExistingMovedElementId)    and not ( unNewMovedElementId    == unExistingMovedElementId):
                return False
            if ( unNewMovedElementUID   or unExistingMovedElementUID)   and not ( unNewMovedElementUID   == unExistingMovedElementUID):
                return False
            if ( ( unNewPosition >= 0)  or ( unExistingPosition >= 0) ) and not ( unNewPosition          == unExistingPosition):
                return False
            if ( unNewDelta             or unExistingDelta)             and not ( unNewDelta             == unExistingDelta):
                return False
            # ACV 20091202 TraversalName not informed by the container elements move objects by delta
            #
            #if ( unNewTraversalName     or unExistingTraversalName)     and not ( unNewTraversalName == unExistingTraversalName):
                #return False
                 
            return True
                
            
        return False
    
    
    
    
    


    
    def fNewChangeEntry( self,       
        theElement                  =None, 
        theChangeKind               =None,
        theChangeReport             =None,
        theReverseRelation          =False,
        theMemberId                 =None, 
        theAhora                    =None,
        theChangeCounter            =None):
        
        aMustLogValueChanges = self.fMustLogValueChanges( theElement)
        
        someDetails = None
        
        
        
        if theChangeKind == cModificationKind_ChangeValues:

            someChangedFieldNames = [ ]
            someChangedValues     = { }
            
            someFieldChangeReports = theChangeReport.get( 'field_reports', [])
            for aFieldChangeReport in someFieldChangeReports:
                if aFieldChangeReport.get( 'effect', '') == 'changed':
                    
                    aChangedFieldName = aFieldChangeReport.get( 'attribute_name', '')
                    if aChangedFieldName:
                        
                        if aMustLogValueChanges:
                            
                            someChangedValues[ aChangedFieldName] = aFieldChangeReport.get( 'new_value', None)
                            
                        else:
                            someChangedFieldNames.append( aChangedFieldName)
            if aMustLogValueChanges:   
                if someChangedValues:
                    someDetails = {
                        cChangeDetails_NewFieldValue: someChangedValues
                    }
            elif someChangedFieldNames:
                someDetails = {
                    cChangeDetails_FieldChanges: someChangedFieldNames
                }
                    
                
                
                
                    
        elif theChangeKind == cModificationKind_Link:
            someLinkChangeReports = theChangeReport.get( 'link_reports', [])
            for aLinkChangeReport in someLinkChangeReports:
                if aLinkChangeReport.get( 'effect', '') == 'linked':
                    
                    if theReverseRelation:
                        
                        unRelation     = aLinkChangeReport.get( 'inverse_relation', '')
                        unTargetResult = aLinkChangeReport.get( 'source',   {})                
                        
                    else:
                        unRelation     = aLinkChangeReport.get( 'relation', '')
                        unTargetResult = aLinkChangeReport.get( 'target',   {})
                        
                    unTargetTitle  = unTargetResult.get(  'title', '')
                    unTargetPath   = unTargetResult.get(  'path', '')
                    unTargetUID    = unTargetResult.get(  'UID', '')
                    
                    unLinkDetails = { }
                    if unRelation:
                        unLinkDetails[ cChangeDetails_Relation]   = unRelation
                    if unTargetTitle:
                        unLinkDetails[ cChangeDetails_TargetTitle]= unTargetTitle
                    if unTargetPath:
                        unLinkDetails[ cChangeDetails_TargetPath] = unTargetPath
                    if unTargetUID:
                        unLinkDetails[ cChangeDetails_TargetUID]  = unTargetUID
                    if unLinkDetails:
                        someDetails = unLinkDetails
                        
                        
                        
                        
        elif theChangeKind == cModificationKind_Unlink:
            someUnlinkChangeReports = theChangeReport.get( 'link_reports', [])
            for aUnlinkChangeReport in someUnlinkChangeReports:
                if aUnlinkChangeReport.get( 'effect', '') == 'unlinked':
                    
                    if theReverseRelation:
                        
                        unRelation     = aUnlinkChangeReport.get( 'inverse_relation', '')
                        unTargetResult = aUnlinkChangeReport.get( 'source',   {})                
                        
                    else:
                        unRelation     = aUnlinkChangeReport.get( 'relation', '')
                        unTargetResult = aUnlinkChangeReport.get( 'target',   {})
                    
                    unTargetTitle  = unTargetResult.get(  'title', '')
                    unTargetPath   = unTargetResult.get(  'path', '')
                    unTargetUID    = unTargetResult.get(  'UID', '')
                    
                    unUnlinkDetails = { }
                    if unRelation:
                        unUnlinkDetails[ cChangeDetails_Relation]    = unRelation
                    if unTargetTitle:
                        unUnlinkDetails[ cChangeDetails_TargetTitle] = unTargetTitle
                    if unTargetPath:
                        unUnlinkDetails[ cChangeDetails_TargetPath]  = unTargetPath
                    if unTargetUID:
                        unUnlinkDetails[ cChangeDetails_TargetUID]   = unTargetUID
                    if unUnlinkDetails:
                        someDetails = unUnlinkDetails
                        
                        
                        
                        
        elif theChangeKind == cModificationKind_CreateSubElement:  
            if theChangeReport.get( 'effect', '') == 'created':
                
                unNewObjectResult = theChangeReport.get( 'new_object_result', {})
                if unNewObjectResult and not ( unNewObjectResult.get( 'object', None) == None):
                    
                    unNewElementTitle         = unNewObjectResult.get( 'title', '')
                    unNewElementId            = unNewObjectResult.get( 'id', '')
                    unNewElementUID           = unNewObjectResult.get( 'UID', '')
                    unNewElementMetaType      = unNewObjectResult.get( 'meta_type', '')
                    unNewElementArchetypeName = unNewObjectResult.get( 'archetype_name', '')
                    
                    unCreateDetails = { }
                    
                    if unNewElementTitle:
                        unCreateDetails[ cChangeDetails_NewElementTitle]         = unNewElementTitle
                    if unNewElementId:
                        unCreateDetails[ cChangeDetails_NewElementId]            = unNewElementId
                    if unNewElementUID:
                        unCreateDetails[ cChangeDetails_NewElementUID]           = unNewElementUID                        
                    if unNewElementMetaType:
                        unCreateDetails[ cChangeDetails_NewElementMetaType]      = unNewElementMetaType                        
                    if unNewElementArchetypeName:
                        unCreateDetails[ cChangeDetails_NewElementArchetypeName] = unNewElementArchetypeName                        
            
                    someChangedFieldNames = [ ]
                    someChangedValues     = { }
                    
                    someFieldChangeReports = theChangeReport.get( 'field_reports', [])
                    for aFieldChangeReport in someFieldChangeReports:
                        if aFieldChangeReport.get( 'effect', '') == 'changed':
                            
                            aChangedFieldName = aFieldChangeReport.get( 'attribute_name', '')
                            if aChangedFieldName:
                                if aMustLogValueChanges:
                                    someChangedValues[ aChangedFieldName] = aFieldChangeReport.get( 'new_value', None)
                                else:
                                    someChangedFieldNames.append( aChangedFieldName)
                    if aMustLogValueChanges:   
                        if someChangedValues:
                            unCreateDetails[ cChangeDetails_NewFieldValue] = someChangedValues
                    elif someChangedFieldNames:
                        unCreateDetails[ cChangeDetails_FieldChanges] = someChangedFieldNames
                        
                    if unCreateDetails:
                        someDetails = unCreateDetails
                        
                        
                        
                        
                        
        elif theChangeKind == cModificationKind_Create:  
            if theChangeReport.get( 'effect', '') == 'created':
                
                unNewObjectResult = theChangeReport.get( 'new_object_result', {})
                if unNewObjectResult and not ( unNewObjectResult.get( 'object', None) == None):
                    
                    unNewElementTitle         = unNewObjectResult.get( 'title', '')
                    unNewElementId            = unNewObjectResult.get( 'id', '')
                    unNewElementUID           = unNewObjectResult.get( 'UID', '')
                    unNewElementMetaType      = unNewObjectResult.get( 'meta_type', '')
                    unNewElementArchetypeName = unNewObjectResult.get( 'archetype_name', '')
                    
                    unCreateDetails = { }
                    
                    if unNewElementTitle:
                        unCreateDetails[ cChangeDetails_NewElementTitle]         = unNewElementTitle
                    if unNewElementId:
                        unCreateDetails[ cChangeDetails_NewElementId]            = unNewElementId
                    if unNewElementUID:
                        unCreateDetails[ cChangeDetails_NewElementUID]           = unNewElementUID                        
                    if unNewElementMetaType:
                        unCreateDetails[ cChangeDetails_NewElementMetaType]      = unNewElementMetaType                        
                    if unNewElementArchetypeName:
                        unCreateDetails[ cChangeDetails_NewElementArchetypeName] = unNewElementArchetypeName                        
            
                    someChangedFieldNames = [ ]
                    someChangedValues     = { }
                    
                    someFieldChangeReports = theChangeReport.get( 'field_reports', [])
                    for aFieldChangeReport in someFieldChangeReports:
                        if aFieldChangeReport.get( 'effect', '') == 'changed':
                            
                            aChangedFieldName = aFieldChangeReport.get( 'attribute_name', '')
                            if aChangedFieldName:
                                if aMustLogValueChanges:
                                    someChangedValues[ aChangedFieldName] = aFieldChangeReport.get( 'new_value', None)
                                else:
                                    someChangedFieldNames.append( aChangedFieldName)
                    if aMustLogValueChanges:   
                        if someChangedValues:
                            unCreateDetails[ cChangeDetails_NewFieldValue] = someChangedValues
                    elif someChangedFieldNames:
                        unCreateDetails[ cChangeDetails_FieldChanges] = someChangedFieldNames
                        
                    if unCreateDetails:
                        someDetails = unCreateDetails
                        
                        
                        
                        
                        
        elif theChangeKind == cModificationKind_DeleteSubElement:  
            if theChangeReport.get( 'effect', '') == 'deleted':
                
                unDeletedImpactReport = theChangeReport.get( 'impact_report', {})
                
                someElementsToDelete, someAffectedElements = ModelDDvlPloneTool_Retrieval().fObjectsToDeleteAndRelated_FromImpactReport( unDeletedImpactReport)
                unDeletedObjectResult = unDeletedImpactReport.get( 'here', {})
                if unDeletedObjectResult:
                    
                    unDeletedElement = unDeletedObjectResult.get( 'object', None)
                                         
                    if not ( unDeletedElement == None):
                    
                        unDeletedElementTitle         = unDeletedObjectResult.get( 'title', '')
                        unDeletedElementId            = unDeletedObjectResult.get( 'id', '')
                        unDeletedElementUID           = unDeletedObjectResult.get( 'UID', '')
                        unDeletedElementMetaType      = unDeletedObjectResult.get( 'meta_type', '')
                        unDeletedElementArchetypeName = unDeletedObjectResult.get( 'archetype_name', '')
                        
                        unDeletedDetails = { }
                        
                        if unDeletedElementTitle:
                            unDeletedDetails[ cChangeDetails_DeletedElementTitle]         = unDeletedElementTitle
                        if unDeletedElementId:
                            unDeletedDetails[ cChangeDetails_DeletedElementId]            = unDeletedElementId
                        if unDeletedElementUID:
                            unDeletedDetails[ cChangeDetails_DeletedElementUID]           = unDeletedElementUID                        
                        if unDeletedElementMetaType:
                            unDeletedDetails[ cChangeDetails_DeletedElementMetaType]      = unDeletedElementMetaType                        
                        if unDeletedElementArchetypeName:
                            unDeletedDetails[ cChangeDetails_DeletedElementArchetypeName] = unDeletedElementArchetypeName        
                                                  
                        unDeletedElementPath = unDeletedElement.getPhysicalPath()
                        
                        someDeletedElementsDetails = [ ]
                        for unSubDeletedElement in someElementsToDelete:
                            if not ( unSubDeletedElement == unDeletedElement):
                                
                                unSubDeletedElementPath = []
                                try:
                                    unSubDeletedElementPath = unSubDeletedElement.getPhysicalPath()
                                except:
                                    None
                                if unSubDeletedElementPath:
                                    unSubDeletedElementPath = unSubDeletedElementPath[ len( unDeletedElementPath):]
                                if not unSubDeletedElementPath:
                                    unSubDeletedElementPath = ''
                                else:
                                    unSubDeletedElementPath = '/'.join( unSubDeletedElementPath)                                    
                                unSubDeletedElementUID = ''
                                try:
                                    unSubDeletedElementUID = unSubDeletedElement.UID()
                                except:
                                    None
                                unSubDeletedElementMetaType = ''
                                try:
                                    unSubDeletedElementMetaType = unSubDeletedElement.meta_type
                                except:
                                    None
                                unSubDeletedElementArchetypeName = ''
                                try:
                                    unSubDeletedElementArchetypeName = unSubDeletedElement.archetype_name
                                except:
                                    None
                                
                                unSubDeletedElementDetails = { }
                                if unSubDeletedElementPath:
                                    unSubDeletedElementDetails[ cChangeDetails_DeletedElementPath]          = unSubDeletedElementPath
                                if unSubDeletedElementUID:
                                    unSubDeletedElementDetails[ cChangeDetails_DeletedElementUID]           = unSubDeletedElementUID                        
                                if unSubDeletedElementMetaType:
                                    unSubDeletedElementDetails[ cChangeDetails_DeletedElementMetaType]      = unSubDeletedElementMetaType                        
                                if unSubDeletedElementArchetypeName:
                                    unSubDeletedElementDetails[ cChangeDetails_DeletedElementArchetypeName] = unSubDeletedElementArchetypeName        
                                if unSubDeletedElementDetails:
                                    someDeletedElementsDetails.append( unSubDeletedElementDetails)
                        
                        if someDeletedElementsDetails:   
                            unDeletedDetails.update( { 
                                cChangeDetails_IncludedDeleted:    someDeletedElementsDetails,  
                            })
                            
                        if unDeletedDetails:
                            someDetails = unDeletedDetails
            
                        
                            
                            
                            
        elif theChangeKind == cModificationKind_DeletePloneSubElement:  
            if theChangeReport.get( 'effect', '') == 'deleted':
                                
                unDeletedObjectResult = theChangeReport.get( 'plone_element_result', {})
                if unDeletedObjectResult:
                    
                    unDeletedElement = unDeletedObjectResult.get( 'object', None)
                                         
                    if not ( unDeletedElement == None):
                    
                        unDeletedElementTitle         = unDeletedObjectResult.get( 'title', '')
                        unDeletedElementId            = unDeletedObjectResult.get( 'id', '')
                        unDeletedElementUID           = unDeletedObjectResult.get( 'UID', '')
                        unDeletedElementMetaType      = unDeletedObjectResult.get( 'meta_type', '')
                        unDeletedElementArchetypeName = unDeletedObjectResult.get( 'archetype_name', '')
                        
                        unDeletedDetails = { }
                        
                        if unDeletedElementTitle:
                            unDeletedDetails[ cChangeDetails_DeletedElementTitle]         = unDeletedElementTitle
                        if unDeletedElementId:
                            unDeletedDetails[ cChangeDetails_DeletedElementId]            = unDeletedElementId
                        if unDeletedElementUID:
                            unDeletedDetails[ cChangeDetails_DeletedElementUID]           = unDeletedElementUID                        
                        if unDeletedElementMetaType:
                            unDeletedDetails[ cChangeDetails_DeletedElementMetaType]      = unDeletedElementMetaType                        
                        if unDeletedElementArchetypeName:
                            unDeletedDetails[ cChangeDetails_DeletedElementArchetypeName] = unDeletedElementArchetypeName        
                        if unDeletedDetails:
                            someDetails = unDeletedDetails
           
                            
                            
                            
                        
        elif theChangeKind in [ cModificationKind_MoveSubObject, cModificationKind_MovePloneSubObject, cModificationKind_MoveReferencedObject]:
            if theChangeReport.get( 'effect', '') == 'moved':
                                
                unMovedObjectResult = theChangeReport.get( 'moved_element', {})
                if unMovedObjectResult:
                    
                    unMovedElement = unMovedObjectResult.get( 'object', None)
                                         
                    if not ( unMovedElement == None):
                    
                        unMovedElementTitle          = unMovedObjectResult.get( 'title', '')
                        unMovedElementId             = unMovedObjectResult.get( 'id', '')
                        unMovedElementUID            = unMovedObjectResult.get( 'UID', '')
                        #unMovedElementMetaType      = unMovedObjectResult.get( 'meta_type', '')
                        #unMovedElementArchetypeName = unMovedObjectResult.get( 'archetype_name', '')
                        unNewPosition                = theChangeReport.get( 'new_position', -1)
                        unDelta                      = theChangeReport.get( 'delta', -1)
                        unTraversalName              = theChangeReport.get( 'parent_traversal_name', -1)
                        
                        unMovedDetails = { }
                        if unMovedElementTitle:
                            unMovedDetails[ cChangeDetails_MovedElementTitle]         = unMovedElementTitle
                        if unMovedElementId:
                            unMovedDetails[ cChangeDetails_MovedElementId]            = unMovedElementId
                        if unMovedElementUID:
                            unMovedDetails[ cChangeDetails_MovedElementUID]           = unMovedElementUID                        
                        #if unMovedElementMetaType:
                            #unMovedDetails[ cChangeDetails_MovedElementMetaType]      = unMovedElementMetaType                        
                        #if unMovedElementArchetypeName:
                            #unMovedDetails[ cChangeDetails_MovedElementArchetypeName] = unMovedElementArchetypeName      
                        if unNewPosition >= 0:
                            unMovedDetails[ cChangeDetails_Position]                  = unNewPosition                                  
                        if unDelta:
                            unMovedDetails[ cChangeDetails_Delta]                     = unDelta                                  
                        if unTraversalName:
                            unMovedDetails[ cChangeDetails_TraversalName]             = unTraversalName                                  
                        if unMovedDetails:
                            someDetails = unMovedDetails
            
            
        
        aNewChangeEntry = { }
        
        aChangeKind = theChangeKind
        if aChangeKind:
            aChangeKind = cModificationKinds_AbbreviationsByName.get( theChangeKind, theChangeKind)    
        if aChangeKind:
            aNewChangeEntry[ cChangeDetails_ChangeKind] = aChangeKind
            
        if theMemberId:
            aNewChangeEntry[ cChangeDetails_UserId] = theMemberId
         
        if theAhora:
            aNewChangeEntry[ cChangeDetails_ChangeDate]   = theAhora
            
        if not ( theChangeCounter == None):
            aNewChangeEntry[ cChangeDetails_ChangeCounter]  = theChangeCounter

        if someDetails:
            aNewChangeEntry[ cChangeDetails_Details] = someDetails
            
            
        return aNewChangeEntry
    
    
    
    
      
    
    
    
    
    

    
    security.declarePrivate('fRetrieveChangeLog')
    def fRetrieveChangeLog(self, 
        theTimeProfilingResults     =None,
        theElement                  =None, 
        theRetrievalExtents         =None,
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theResult                   =None,
        theAdditionalParams         =None):
        """Retrieve a result structure for an element, initialized with the change log.
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveChangeLog', theTimeProfilingResults)

        try:
        
            if ( theElement == None):
                return []

            unLogValue = ''
            
            unSchema = theElement.schema
            if not unSchema:
                return []
                
            unFieldName = self.fChangeLogFieldNameForElement( theElement)
            
            if not unFieldName:
                return []
            
                    
            unField = unSchema.get( unFieldName, None)
            if not unField:
                return []
                    
            unAccessor = unField.getAccessor( theElement)
            if not unAccessor:
                return []

            unLogValueString = None
            try:
                unLogValueString = unAccessor()
            except:
                None
            if not unLogValueString:
                return []
                
            unLogValue = fEvalString( unLogValueString)            
            if not unLogValue:
                return []
            
            someChangedEntries = unLogValue[:]
            
            if not ( theResult == None):
                theResult[ 'change_entries' ]      = someChangedEntries
                theResult[ 'change_entries_after'] = someChangedEntries
                

            unIncludeFieldValuesInSummaries = theRetrievalExtents and ( 'change_entries_summaries_fields_values' in theRetrievalExtents)
                
            someTranslations = self.fTranslationsBundle_ForChanges( theElement)
            someChangeEntriesSummaries = self.fChangeEntriesI18NSummaries( theElement, someChangedEntries, someTranslations, unIncludeFieldValuesInSummaries)
            if someChangeEntriesSummaries:
                theResult[ 'change_entries_summaries' ]      = someChangeEntriesSummaries
                theResult[ 'change_entries_after_summaries'] = someChangeEntriesSummaries
                
 
            if ( 'change_entries_summaries' in theRetrievalExtents) or  ( 'change_entries_summaries_fields_values' in theRetrievalExtents):
                for aChangeEntry in someChangedEntries:
                    aChangeEntrySummary = self.fChangeEntryDetailsSummaryI18N( theElement, aChangeEntry, someTranslations, unIncludeFieldValuesInSummaries)
                    aChangeEntry[ 'summary'] = aChangeEntrySummary
                    
                    
            if theAdditionalParams:
                
                unEarliestChangeCounter = theAdditionalParams.get( 'ChangesAfter', -1)
                if ( isinstance( unEarliestChangeCounter, int) and ( unEarliestChangeCounter >= 0)) or isinstance( unEarliestChangeCounter, str) or  isinstance( unEarliestChangeCounter, unicode):
                    if isinstance( unEarliestChangeCounter, str) or  isinstance( unEarliestChangeCounter, unicode):
                        unEarliestChangeCounterString = unEarliestChangeCounter
                        unEarliestChangeCounter = -1
                        if unEarliestChangeCounterString:
                            unEarliestChangeCounter = -1
                            try:
                                unEarliestChangeCounter = int( unEarliestChangeCounterString)
                            except:
                                None
                            
                    if unEarliestChangeCounter >= 0:
                        
                        someChangeEntriesAfter     = [ unChgEntry for unChgEntry in someChangedEntries if unChgEntry.get( cChangeDetails_ChangeCounter, -1) >= unEarliestChangeCounter]
                        someChangeEntriesAfterSummaries = self.fChangeEntriesI18NSummaries( theElement, someChangeEntriesAfter, someTranslations, unIncludeFieldValuesInSummaries)
                                    
                        theResult[ 'change_entries_after']           = someChangeEntriesAfter
                        theResult[ 'change_entries_after_summaries'] = someChangeEntriesAfterSummaries                 
                    
            return someChangedEntries
            
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveChangeLog', theTimeProfilingResults)
                  
    
    
    
    
    

    def fTranslationsBundle_ForChanges( self, theContextElement):
        """The translations of change kinds, and property names of changes and change details, to be used in the presentation of changes.
        
        """
        
        someSymbolsAndDefaults = [ ]
        someDomainsStringsAndDefaults = [ [ 'ModelDDvlPlone', someSymbolsAndDefaults]]
        
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        
        for aModificationKindAbbreviated in cModificationKinds_ByAbbreviation.keys():
            aSymbol  = 'ModelDDvlPlone_ChangeKind_%s' % aModificationKindAbbreviated
            aDefault = cModificationKinds_ByAbbreviation.get( aModificationKindAbbreviated, aModificationKindAbbreviated)
            someSymbolsAndDefaults.append( [ aSymbol, aDefault,])
            
        for aDetailKey in cChangeDetails_keys:
            aSymbol  = 'ModelDDvlPlone_ChangeDetail_%s' % aDetailKey
            aDefault = cChangeDetails_long_byAbbreviation.get( aDetailKey, aDetailKey)
            someSymbolsAndDefaults.append( [ aSymbol, aDefault,])
        
        someSymbolsAndDefaults.append( [ 'ModelDDvlPlone_ChangeDetails', 'Details-',])
        
        someTranslations = { }
        aModelDDvlPloneTool_Retrieval.fTranslateI18NManyIntoDict( theContextElement, someDomainsStringsAndDefaults, someTranslations)

        return someTranslations
       
            
    
        
     
    security.declarePrivate( 'fChangeEntriesI18NSummaries')
    def fChangeEntriesI18NSummaries( self, theElement, theChangeEntries, theTranslations=None, theIncludeFieldValuesInSummaries=False):

        if not theChangeEntries:
            return u''
        
        someTranslations = theTranslations
        if not someTranslations:
            someTranslations = self.fTranslationsBundle_ForChanges( theElement)
            
        aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
        someTranslations[ 'ModelDDvlPlone_ChangesAfterNumChanges'] = aModelDDvlPloneTool_Retrieval.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_ChangesAfterNumChanges', 'changes-', theElement)
        someTranslations[ 'ModelDDvlPlone_Audit_ChangesSince']     = aModelDDvlPloneTool_Retrieval.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_Audit_ChangesSince',     'since-',   theElement)
        someTranslations[ 'ModelDDvlPlone_Audit_ChangeBy']         = aModelDDvlPloneTool_Retrieval.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_Audit_ChangeBy',         'by-',      theElement)
        
        anEarliestMillis  = int( time() * 1000) + 1000000
        aLatestMillis     = 0
        someUserIds       = set( )
        someEntriesByKind = { }
        
        
        for unChangeEntry in theChangeEntries:
            
                    
            unChangeEntryKind  = unChangeEntry.get( cChangeDetails_ChangeKind, '')
            someEntriesOfTheKind = someEntriesByKind.get( unChangeEntryKind, [])
            if not someEntriesOfTheKind:
                someEntriesOfTheKind = []
                someEntriesByKind[ unChangeEntryKind] = someEntriesOfTheKind
            someEntriesOfTheKind.append( unChangeEntry)
                    
            unChangeEntryUserId = unChangeEntry.get( cChangeDetails_UserId, '')
            if unChangeEntryUserId:
                someUserIds.add( unChangeEntryUserId)
                
            unChangeEntryMillis = unChangeEntry.get( cChangeDetails_ChangeDate, '')
            if unChangeEntryMillis:
                if unChangeEntryMillis < anEarliestMillis:
                    anEarliestMillis = unChangeEntryMillis
                elif unChangeEntryMillis > aLatestMillis:
                    aLatestMillis = unChangeEntryMillis
                    
        if ( not someUserIds) and ( not someChangesByKind) and ( not someEntriesByKind):
            return u''
        
        someUserIds = sorted( someUserIds)
        
        
        someSummaries = [ ]
        
        someSummaries.append( u'%d %s %s %s' % ( 
            len( theChangeEntries),
            someTranslations.get( 'ModelDDvlPlone_ChangesAfterNumChanges', 'changes-',),
            ( anEarliestMillis and ( u'%s %s' % ( someTranslations.get( 'ModelDDvlPlone_Audit_ChangesSince', 'since-'), self.fMillisecondsToDateTime( anEarliestMillis)))) or '',
            ( someUserIds      and ( u'%s %s' % ( ( someTranslations.get( 'ModelDDvlPlone_Audit_ChangeBy', 'by-') ,u', '.join( someUserIds))))) or '',
        ))
        
        for aChangeKind in sorted( someEntriesByKind.keys()):
            aChangeDetailsString = self.fChangeEntriesOfAKindCombinedSummariesI18NString( theElement, aChangeKind, someEntriesByKind[ aChangeKind], someTranslations, theIncludeFieldValuesInSummaries)
            if aChangeDetailsString:
                someSummaries.append( u'%s: %s' % ( 
                    someTranslations.get( 'ModelDDvlPlone_ChangeKind_%s' % aChangeKind, aChangeKind),
                    aChangeDetailsString,
                ))

        return someSummaries
        
             
            
            
            
    # ACV 20091215 Unused. Removed.       
    #security.declarePrivate( 'fChangeEntryAsI18NString')
    #def fChangeEntryAsI18NString( self, theElement, theChangeEntry, theTranslations=None):
        
        #if not theChangeEntry:
            #return u''
        
        
        #someTranslations = theTranslations
        #if not someTranslations:
            #someTranslations = self.fTranslationsBundle_ForChanges( theElement)

        #aChangeEntryDetailsSummary = self.fChangeEntryDetailsSummaryI18N( theElement, theChangeEntry, someTranslations)
        #if aChangeEntryDetailsSummary:
            #aChangeEntryDetailsSummary = '[%s]' % aChangeEntryDetailsSummary
            
            
        #aChangeEntryAsI18NString = u'%s: %s %s %s %s %s' % ( 
            #someTranslations.get( 'ModelDDvlPlone_ChangeKind_%s' % theChangeEntry.get( cChangeDetails_ChangeKind, ''), theChangeEntry.get( cChangeDetails_ChangeKind, '')),
            #aChangeEntryDetailsSummary,
            #someTranslations.get( 'ModelDDvlPlone_Audit_ChangeOn', 'on-'),
            #self.fMillisecondsToDateTime( theChangeEntry.get( cChangeDetails_ChangeDate, '')),
            #someTranslations.get( 'ModelDDvlPlone_Audit_ChangeBy', 'by-'),
            #theChangeEntry.get( cChangeDetails_UserId, '')
        #)
            
        #return aChangeEntryAsI18NString
    
    
    
    
    
    
    
    security.declarePrivate( 'fChangeEntryAsTransactionNote')
    def fChangeEntryAsTransactionNote( self, theElement, theChangeEntry, theTranslations=None):
        
        if not theChangeEntry:
            return u''
        
        
        someTranslations = theTranslations
        if not someTranslations:
            someTranslations = self.fTranslationsBundle_ForChanges( theElement)

        aChangeEntryDetailsSummary = self.fChangeEntryDetailsSummaryI18N( theElement, theChangeEntry, someTranslations, False) # unIncludeFieldValuesInSummaries
        if aChangeEntryDetailsSummary:
            aChangeEntryDetailsSummary = '[%s]' % aChangeEntryDetailsSummary
            
        
        aType = ''
        try:
            aType = theElement.archetype_name
        except:
            None
        if not aType:
            try:
                aType = theElement.meta_type
            except:
                None
        if not aType:
            aType = u'Element'
            
            
        aChangeEntryAsTransactionNote = u'%s title=%s, path=%s; %s %s. ' % ( 
            aType,
            theElement.Title(),
            '/'.join( theElement.getPhysicalPath()),
            someTranslations.get( 'ModelDDvlPlone_ChangeKind_%s' % theChangeEntry.get( cChangeDetails_ChangeKind, ''), theChangeEntry.get( cChangeDetails_ChangeKind, '')),
            aChangeEntryDetailsSummary,
            #someTranslations.get( 'ModelDDvlPlone_Audit_ChangeOn', 'on-'),
            #self.fMillisecondsToDateTime( theChangeEntry.get( cChangeDetails_ChangeDate, '')),
            #someTranslations.get( 'ModelDDvlPlone_Audit_ChangeBy', 'by-'),
            #theChangeEntry.get( cChangeDetails_UserId, '')
        )
            
        return aChangeEntryAsTransactionNote
        
    

    
    
    
    
    
    
    
    
    
    
    
    
                                        
    security.declarePrivate( 'fChangeEntriesOfAKindCombinedSummariesI18NString')
    def fChangeEntriesOfAKindCombinedSummariesI18NString( self, theElement, theChangeKind, theChangeEntries, theTranslations=None, theIncludeFieldValues=False):
        if not theChangeKind:
            return u''


        someTranslations = theTranslations
        if not someTranslations:
            someTranslations = self.fTranslationsBundle_ForChanges( theElement)

            
        if theChangeKind == cModificationKind_ChangeValues_abbr:
            
            if not theIncludeFieldValues:
                someAllFieldNames = set( )
                
                for aChangeEntry in theChangeEntries:
                    
                    aChangeDetails = aChangeEntry.get( cChangeDetails_Details, {})
                    if aChangeDetails:
                        someChangedFieldNames = aChangeDetails.get( cChangeDetails_NewFieldValue, {}).keys() or aChangeDetails.get( cChangeDetails_FieldChanges, [])                 
                        if someChangedFieldNames:
                            someAllFieldNames.update( someChangedFieldNames)
                        
                if not someAllFieldNames:
                    return u''
                
                aChangeDetailsString = u', '.join( sorted( someAllFieldNames))
                return aChangeDetailsString

                    
            else:
                
                someAllFieldValues = { }
                someAllFieldNames = set( )
                
                someReversedEntries = theChangeEntries[:]
                someReversedEntries.reverse()
                for aChangeEntry in someReversedEntries:
                    
                    aChangeDetails = aChangeEntry.get( cChangeDetails_Details, {})
                    if aChangeDetails:
                        someNewFieldValuesNames = aChangeDetails.get( cChangeDetails_NewFieldValue, {})                  
                        if someNewFieldValuesNames:
                            someAllFieldValues.update( someNewFieldValuesNames)
                            
                        someChangedFieldNames = aChangeDetails.get( cChangeDetails_FieldChanges, [])                 
                        if someChangedFieldNames:
                            someAllFieldNames.update( someChangedFieldNames)
                        
                if ( not someAllFieldNames) and ( not someAllFieldValues):
                    return u''
                
                aChangeDetailsString = u''
                
                if someAllFieldValues:
                    aSortedFieldKeys = sorted ( someAllFieldValues.keys())
                    someFieldValueStrings = [ '%s=%s' % ( aFieldName, someAllFieldValues[ aFieldName]) for aFieldName in aSortedFieldKeys]
                    aChangeDetailsString += u', '.join( someFieldValueStrings)
                    

                someUnreportedChangedFieldNames = set( someAllFieldNames).difference( set( someAllFieldValues.keys()))
                if someUnreportedChangedFieldNames:
                    if someNewFieldValuesNames:
                        aChangeDetailsString += u', '
                    aChangeDetailsString += u', '.join( sorted( someUnreportedChangedFieldNames))
                    
                return aChangeDetailsString


        
        elif theChangeKind in(  cModificationKind_Link_abbr, cModificationKind_Unlink_abbr):
            
            aChangeDetailsString = u''
            someTitlesByRelation = { }
            
            for aChangeEntry in theChangeEntries:
                aChangeDetails = aChangeEntry.get( cChangeDetails_Details, {})
                if aChangeDetails:
                    unRelation           = aChangeDetails.get( cChangeDetails_Relation,    '')
                    unTitlesForRelation  = someTitlesByRelation.get( unRelation, [])
                    if not unTitlesForRelation:
                        unTitlesForRelation = set( )
                        someTitlesByRelation[ unRelation] = unTitlesForRelation
                    
                    unRelatedTitle       = aChangeDetails.get( cChangeDetails_TargetTitle, '')
                    if unRelatedTitle:
                        unTitlesForRelation.add( unRelatedTitle)
             
            if someTitlesByRelation:
                someRelations = sorted( someTitlesByRelation.keys())
                aChangeDetailsString = u', '.join( 
                    [ '( %s: %s)' % (
                        aRelation,
                        ', '.join( someTitlesByRelation[ aRelation]),) for aRelation in someRelations
                    ]
                )
            return aChangeDetailsString

                    
          
        
        
        elif theChangeKind in ( cModificationKind_CreateSubElement_abbr, cModificationKind_Create_abbr,):  
            aChangeDetailsString = u''
            someTitlesByArchetypeName = { }
            
            for aChangeEntry in theChangeEntries:
                aChangeDetails = aChangeEntry.get( cChangeDetails_Details, {})
                if aChangeDetails:
                    unArchetypeName     = aChangeDetails.get( cChangeDetails_NewElementArchetypeName,    '')
                    unTitlesForArchetypeName  = someTitlesByArchetypeName.get( unArchetypeName, [])
                    if not unTitlesForArchetypeName:
                        unTitlesForArchetypeName = set( )
                        someTitlesByArchetypeName[ unArchetypeName] = unTitlesForArchetypeName
                    
                    unCreatedTitle       = aChangeDetails.get( cChangeDetails_NewElementTitle, '')
                    if unCreatedTitle:
                        unTitlesForArchetypeName.add( unCreatedTitle)
             
            if someTitlesByArchetypeName:
                someArchetypeNames = sorted( someTitlesByArchetypeName.keys())
                aChangeDetailsString = u', '.join( 
                    [ '( %s: %s)' % (
                        anArchetypeName,
                        ', '.join( someTitlesByArchetypeName[ anArchetypeName]),) for anArchetypeName in someArchetypeNames
                    ]
                )
            return aChangeDetailsString
            
                    
        

                         
        elif theChangeKind in [ cModificationKind_DeleteSubElement_abbr, cModificationKind_DeletePloneSubElement_abbr,]:  
            aChangeDetailsString      = u''
            someTitlesByArchetypeName = { }
            unTotalIncludedDeleted    = 0 
            
            for aChangeEntry in theChangeEntries:
                aChangeDetails = aChangeEntry.get( cChangeDetails_Details, {})
                if aChangeDetails:
                    unArchetypeName     = aChangeDetails.get( cChangeDetails_DeletedElementArchetypeName,    '')
                    unTitlesForArchetypeName  = someTitlesByArchetypeName.get( unArchetypeName, [])
                    if not unTitlesForArchetypeName:
                        unTitlesForArchetypeName = set( )
                        someTitlesByArchetypeName[ unArchetypeName] = unTitlesForArchetypeName
                    
                    unDeletedTitle       = aChangeDetails.get( cChangeDetails_DeletedElementTitle, '')
                    if unDeletedTitle:
                        unTitlesForArchetypeName.add( unDeletedTitle)
             
                    someIncludedDeleted = aChangeDetails.get( cChangeDetails_IncludedDeleted, [])     
                    if someIncludedDeleted:
                        unTotalIncludedDeleted += len( someIncludedDeleted)
                        
            if someTitlesByArchetypeName:
                someArchetypeNames = sorted( someTitlesByArchetypeName.keys())
                aChangeDetailsString = u', '.join( 
                    [ '( %s: %s)' % (
                        anArchetypeName,
                        ', '.join( someTitlesByArchetypeName[ anArchetypeName]),) for anArchetypeName in someArchetypeNames
                    ]
                )
                
            if unTotalIncludedDeleted:
                aChangeDetailsString = u'%s%s %s %d %s' % ( 
                    aChangeDetailsString,
                    ( aChangeDetailsString and ', ') or '',
                    ModelDDvlPloneTool_Retrieval().fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_and', 'and-', theElement),
                    unTotalIncludedDeleted,
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_IncludedDeleted, cChangeDetails_IncludedDeleted_long), 
                )
                
            return aChangeDetailsString
             
         
   
        
                          
        elif theChangeKind in [ cModificationKind_MoveSubObject_abbr, cModificationKind_MovePloneSubObject_abbr, cModificationKind_MoveReferencedObject_abbr]:
            aChangeDetailsString = u''
            someTitlesByTraversal = { }
            
            for aChangeEntry in theChangeEntries:
                aChangeDetails = aChangeEntry.get( cChangeDetails_Details, {})
                if aChangeDetails:
                    unTraversal           = aChangeDetails.get( cChangeDetails_TraversalName,    '')
                    unTitlesForTraversal  = someTitlesByTraversal.get( unTraversal, [])
                    if not unTitlesForTraversal:
                        unTitlesForTraversal = set( )
                        someTitlesByTraversal[ unTraversal] = unTitlesForTraversal
                    
                    unMovedTitle       = aChangeDetails.get( cChangeDetails_MovedElementTitle, '')
                    if unMovedTitle:
                        unTitlesForTraversal.add( unMovedTitle)
             
            if someTitlesByTraversal:
                someTraversals = sorted( someTitlesByTraversal.keys())
                aChangeDetailsString = u', '.join( 
                    [ '( %s: %s)' % (
                        aTraversal,
                        ', '.join( someTitlesByTraversal[ aTraversal]),) for aTraversal in someTraversals
                    ]
                )
            return aChangeDetailsString
            
             
        return u''
        
        
        

        
        
        
        
        
        
        
        
        
    security.declarePrivate( 'fChangeEntryDetailsSummaryI18N')
    def fChangeEntryDetailsSummaryI18N( self, theElement, theChangeEntry, theTranslations=None, theIncludeFieldValues=True):
        if not theChangeEntry:
            return u''

        aChangeDetails = theChangeEntry.get( cChangeDetails_Details, {})
        if not aChangeDetails:
            return u''
        
        aChangeKind =  theChangeEntry.get( cChangeDetails_ChangeKind, '')
        if ( not aChangeKind) or not ( aChangeKind in cModificationKinds_Abbreviated):
            return u''
        
        someTranslations = theTranslations
        if not someTranslations:
            someTranslations = self.fTranslationsBundle_ForChanges( theElement)

        aChangeDetailsString = u''
        
        
        
        
         
        if aChangeKind == cModificationKind_ChangeValues_abbr:

            if not theIncludeFieldValues:
                someChangedFieldNames = aChangeDetails.get( cChangeDetails_NewFieldValue, {}).keys() or aChangeDetails.get( cChangeDetails_FieldChanges, [])                 
                if someChangedFieldNames:
                    aChangeDetailsString = u'%s: %s' % ( 
                        someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_FieldChanges, cChangeDetails_FieldChanges_long), 
                        u', '.join( someChangedFieldNames),
                    )
                return aChangeDetailsString
            
            else:

                someNewFieldValuesNames = aChangeDetails.get( cChangeDetails_NewFieldValue, {})                                          
                someChangedFieldNames   = aChangeDetails.get( cChangeDetails_FieldChanges, [])                 
            
                if someNewFieldValuesNames or someChangedFieldNames:
                    aChangeDetailsString = u'%s: ' % someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_FieldChanges, cChangeDetails_FieldChanges_long)
                    
                if someNewFieldValuesNames:
                    aSortedFieldKeys = sorted ( someNewFieldValuesNames.keys())
                    someFieldValueStrings = [ '%s=%s' % ( aFieldName, someNewFieldValuesNames[ aFieldName]) for aFieldName in aSortedFieldKeys]
                    aChangeDetailsString += u', '.join( someFieldValueStrings)
                
                someUnreportedChangedFieldNames = set( someChangedFieldNames).difference( set( someNewFieldValuesNames.keys()))
                if someUnreportedChangedFieldNames:
                    if someNewFieldValuesNames:
                        aChangeDetailsString += u', '
                    aChangeDetailsString += u', '.join( sorted( someUnreportedChangedFieldNames))
                
                return aChangeDetailsString

        
        
        
        
        
        elif aChangeKind in [ cModificationKind_Link_abbr, cModificationKind_Unlink_abbr,]:
            
            unRelation           = aChangeDetails.get( cChangeDetails_Relation,    '')
            if unRelation:
                aChangeDetailsString = u'%s: %s' % ( 
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_Relation, cChangeDetails_Relation_long), 
                    unRelation,
                )
            unRelatedTitle       = aChangeDetails.get( cChangeDetails_TargetTitle, '')
            if unRelatedTitle:
                aChangeDetailsString = u' %s%s%s: %s' % ( 
                    aChangeDetailsString,
                    ( aChangeDetailsString and ', ') or '',
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_TargetTitle, cChangeDetails_TargetTitle_long), 
                    unRelatedTitle
                )
            return aChangeDetailsString

                    
       
        
        
        elif aChangeKind in ( cModificationKind_CreateSubElement_abbr, cModificationKind_Create_abbr):  
            unNewElementArchetypeName         = aChangeDetails.get( cChangeDetails_NewElementArchetypeName, '')
            if unNewElementArchetypeName:
                aChangeDetailsString = u'%s: %s' % ( 
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_NewElementArchetypeName, cChangeDetails_NewElementArchetypeName), 
                    unNewElementArchetypeName,
                )
            unNewElementTitle = aChangeDetails.get( cChangeDetails_NewElementTitle, '')
            if unNewElementTitle:
                aChangeDetailsString = u' %s%s%s: %s' % ( 
                    aChangeDetailsString,
                    ( aChangeDetailsString and ', ') or '',
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_NewElementTitle, cChangeDetails_TargetTitle_long), 
                    unNewElementTitle
                )
                
                
            if not theIncludeFieldValues:
                someChangedFieldNames = aChangeDetails.get( cChangeDetails_NewFieldValue, {}).keys() or aChangeDetails.get( cChangeDetails_FieldChanges, [])                 
                if someChangedFieldNames:
                    aChangeDetailsString = u'%s%s%s: %s' % ( 
                        aChangeDetailsString,
                        ( aChangeDetailsString and ', ') or '',
                        someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_FieldChanges, cChangeDetails_FieldChanges_long), 
                        u', '.join( someChangedFieldNames),
                    )
                return aChangeDetailsString
            
            else:

                someNewFieldValuesNames = aChangeDetails.get( cChangeDetails_NewFieldValue, {})                                          
                someChangedFieldNames   = aChangeDetails.get( cChangeDetails_FieldChanges, [])                 
            
                if someNewFieldValuesNames or someChangedFieldNames:
                    aChangeDetailsString = u'%s%s%s: ' % ( 
                        aChangeDetailsString,
                        ( aChangeDetailsString and ', ') or '',
                        someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_FieldChanges, cChangeDetails_FieldChanges_long),
                    )
                    
                if someNewFieldValuesNames:
                    aSortedFieldKeys = sorted ( someNewFieldValuesNames.keys())
                    someFieldValueStrings = [ '%s=%s' % ( aFieldName, someNewFieldValuesNames[ aFieldName]) for aFieldName in aSortedFieldKeys]
                    aChangeDetailsString += u', '.join( someFieldValueStrings)
                
                someUnreportedChangedFieldNames = set( someChangedFieldNames).difference( set( someNewFieldValuesNames.keys()))
                if someUnreportedChangedFieldNames:
                    if someNewFieldValuesNames:
                        aChangeDetailsString += u', '
                    aChangeDetailsString += u', '.join( sorted( someUnreportedChangedFieldNames))
                
                
            return aChangeDetailsString
        
        

        
        
                        
        elif aChangeKind in [ cModificationKind_DeleteSubElement_abbr, cModificationKind_DeletePloneSubElement_abbr,]:  
            unDeletedElementArchetypeName         = aChangeDetails.get( cChangeDetails_DeletedElementArchetypeName, '')
            if unDeletedElementArchetypeName:
                aChangeDetailsString = u'%s: %s' % ( 
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_DeletedElementArchetypeName, cChangeDetails_DeletedElementArchetypeName_long), 
                    unDeletedElementArchetypeName,
                )
            unDeletedElementTitle = aChangeDetails.get( cChangeDetails_DeletedElementTitle, '')
            if unDeletedElementTitle:
                aChangeDetailsString = u' %s%s%s: %s' % ( 
                    aChangeDetailsString,
                    ( aChangeDetailsString and ', ') or '',
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_DeletedElementTitle, cChangeDetails_DeletedElementTitle_long), 
                    unDeletedElementTitle
                )
            someIncludedDeleted = aChangeDetails.get( cChangeDetails_IncludedDeleted, [])                
            if someIncludedDeleted:
                aChangeDetailsString = u'%s%s%s %d %s' % ( 
                    aChangeDetailsString,
                    ( aChangeDetailsString and ', ') or '',
                    ModelDDvlPloneTool_Retrieval().fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_and', 'and-', theElement),
                    len( someIncludedDeleted),
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_IncludedDeleted, cChangeDetails_IncludedDeleted_long), 
                )
            return aChangeDetailsString
                        
        

        
        
        
                        
        elif aChangeKind in [ cModificationKind_MoveSubObject_abbr, cModificationKind_MovePloneSubObject_abbr, cModificationKind_MoveReferencedObject_abbr]:
            unTraversalName           = aChangeDetails.get( cChangeDetails_TraversalName,    '')
            if unTraversalName:
                aChangeDetailsString = u'%s: %s' % ( 
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_TraversalName, cChangeDetails_TraversalName_long), 
                    unTraversalName,
                )
            unMovedTitle       = aChangeDetails.get( cChangeDetails_MovedElementTitle, '')
            if unMovedTitle:
                aChangeDetailsString = u' %s%s%s: %s' % ( 
                    aChangeDetailsString,
                    ( aChangeDetailsString and ', ') or '',
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_MovedElementTitle, cChangeDetails_MovedElementTitle_long), 
                    unMovedTitle
                )
            unPosition       = aChangeDetails.get( cChangeDetails_Position, -1)
            if unPosition >= 0:
                aChangeDetailsString = u' %s%s%s: %d' % ( 
                    aChangeDetailsString,
                    ( aChangeDetailsString and ', ') or '',
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_Position, cChangeDetails_Position_long), 
                    unPosition
                )
            unDelta       = aChangeDetails.get( cChangeDetails_Delta, 0)
            if unDelta >= 0:
                aChangeDetailsString = u' %s%s%s: %d' % ( 
                    aChangeDetailsString,
                    ( aChangeDetailsString and ', ') or '',
                    someTranslations.get( 'ModelDDvlPlone_ChangeDetail_%s' % cChangeDetails_Delta, cChangeDetails_Delta_long), 
                    unDelta
                )
            return aChangeDetailsString

            
             
        return u''
        
        
        

    
            
        
        
        
        
        
        
        

        

                                
    def fChangeLogFieldNameForElement( self, theElement):
        if theElement == None:
            return ''
        aChangeLogFieldName = ''
        try:
            aChangeLogFieldName = theElement.change_log_field
        except:
            None   
            
        return aChangeLogFieldName
    
    
        
                 

        
    security.declarePrivate( 'fMillisecondsToDateTime')
    def fMillisecondsToDateTime( self, theMilliseconds):
        """Duplicated from ModelDDvlPloneToolSupport.
        
        """
        
        if not theMilliseconds:
            return None
        
        if isinstance( theMilliseconds, DateTime):
            return theMilliseconds
        
        unDateTime = None
        try:
            unDateTime = DateTime( theMilliseconds / 1000)
        except:
            None
            
        return unDateTime
    
            

                