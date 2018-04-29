# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval_Impact.py
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

from AccessControl      import ClassSecurityInfo

from DateTime import DateTime



from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName



from ModelDDvlPloneToolSupport import fSecondsNow



class ModelDDvlPloneTool_Retrieval_Impact:
    """
    """
    security = ClassSecurityInfo()

                
    security.declarePrivate( 'fNewVoidDeleteImpactReport')
    def fNewVoidDeleteImpactReport(self ,):
        aReport = {
            'here':                     None,
            'included':                 [], # reports
            'related':                  [], # elements
            'parent_traversal_name':    '',
            'plone':                    [],
            'delete_permission':        False,
            'column_names':             [],
            'column_translations':      {},
            'num_elements_to_delete':   0,
            'num_elements_to_affect':   0,                    
            'date_now':                 None,
            'seconds_now':              0,
            'seconds_to_delete':        0,
            'latest_date_to_delete':    None,
        }                
        return aReport
    

    security.declarePrivate( 'fNewVoidDeleteManyImpactReports')
    def fNewVoidDeleteManyImpactReports(self ,):
        aReport = {
            'container_result':          None,
            'impact_reports':            [], 
            'delete_permission':         False,
            'column_names':              [],
            'column_translations':       {},
            'num_elements_to_delete':   0,
            'num_elements_to_affect':   0,                    
            'date_now':                 None,
            'seconds_now':              0,
            'seconds_to_delete':        0,
            'latest_date_to_delete':    None,
        }                
        return aReport
    

     

    security.declarePrivate( 'fDeleteManyImpactReports')
    def fDeleteManyImpactReports(self , 
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,
        theContainerElement     =None,
        theGroupUIDs            =[],
        theAdditionalParams     =None):
        """Retrieve a report of the impact of deleting an element, including all elements that will be related (contained elements) and elements that will be affected (related elements).
        
        """
 
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fDeleteManyImpactReports', theTimeProfilingResults)

        try:
            
            aDeleteManyImpactReports = self.fNewVoidDeleteManyImpactReports()
            
            if theModelDDvlPloneTool == None:
                return aDeleteManyImpactReports
            
            if ( theContainerElement == None):
                return aDeleteManyImpactReports
            
            
            unContainerElementResult = self.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theContainerElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', 'owner', 'cursor',],
                theWritePermissions         =[ ],
                theFeatureFilters           ={ 'attrs': [ 'title', 'description'], 'aggregations': [], 'relations': [], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =None,
                theAdditionalParams         =theAdditionalParams                
            )
            if unContainerElementResult:  
                aDeleteManyImpactReports[ 'container_result'] = unContainerElementResult
                
            
            allIncludedElements = []
            allRelatedElements  = []
            allRelatedResults   = []
            unCanDeleteHolder   = [ True ]
            
            someDefaultColumnNames        = [ 'title', 'description', ]
            someDefaultColumnTranslations = self.getTranslationsForDefaultAttributes( theContainerElement)
            
            aDeleteManyImpactReports[ 'column_names']        = someDefaultColumnNames
            aDeleteManyImpactReports[ 'column_translations'] = someDefaultColumnTranslations
                        
            if not theGroupUIDs:
                return aDeleteManyImpactReports
            
            someGroupUIDs = theGroupUIDs
            if not ( someGroupUIDs.__class__.__name__ in [ 'list', 'tuple', 'set']):
                someGroupUIDs = [ someGroupUIDs, ]
            
            someElementsToDelete = [ ]
            
            for anElementUID in someGroupUIDs:
                unElementToDelete = self.fElementoPorUID( anElementUID, theContainerElement)
                if not ( unElementToDelete == None):
                    someElementsToDelete.append( unElementToDelete)
                    
            if not someElementsToDelete:
                return aDeleteManyImpactReports
            
            someAdditionalParams = theAdditionalParams
            if someAdditionalParams == None:
                someAdditionalParams = { }
            else:
                someAdditionalParams = someAdditionalParams.copy()
                
            someAdditionalParams[ 'DoNotForbidDeletionFor_Aggregations_ReadOnly'] =  True
            
            
            for unElementToDelete in someElementsToDelete:
                              
                unElementToDeleteResult = self.fRetrieveTypeConfig( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =unElementToDelete, 
                    theParent                   =None,
                    theParentTraversalName      ='',
                    theTypeConfig               =None, 
                    theAllTypeConfigs           =None, 
                    theViewName                 ='', 
                    theRetrievalExtents         =[ 'traversals', 'tree', 'owner', 'cursor', ],
                    theWritePermissions         =[ 'object', 'attrs', 'aggregations', 'relations', 'delete',],
                    theFeatureFilters           ={ 'attrs': [ 'title', 'description'], }, 
                    theInstanceFilters          =None,
                    theTranslationsCaches       =None,
                    theCheckedPermissionsCache  =None,
                    theAdditionalParams         =theAdditionalParams                
                )
                if unElementToDeleteResult:

                    aReport = self.fBuildDeleteImpactReport_AggregatedPass( 
                        theTimeProfilingResults,
                        unElementToDeleteResult, 
                        allIncludedElements, 
                        allRelatedElements, 
                        allRelatedResults, 
                        unCanDeleteHolder, 
                        someAdditionalParams
                    )
                    if aReport:
                        aReport[ 'delete_permission'] = unCanDeleteHolder[ 0] and aReport[ 'here'][ 'delete_permission'] and \
                               aReport[ 'here'][ 'owner_element'][ 'read_permission'] and aReport[ 'here'][ 'owner_element'][ 'write_permission']  and \
                               aReport[ 'here'][ 'cursor'][ 'traversal_result'][ 'read_permission'] and aReport[ 'here'][ 'cursor'][ 'traversal_result'][ 'write_permission']
                        aReport[ 'related'] = allRelatedResults
                        aReport[ 'column_names'] = someDefaultColumnNames
                        aReport[ 'column_translations'] = someDefaultColumnTranslations
        
                        self.pBuildDeleteImpactReport_RelatedPass(
                            theTimeProfilingResults, 
                            unElementToDeleteResult, 
                            allIncludedElements, 
                            allRelatedElements, 
                            allRelatedResults, 
                            unCanDeleteHolder, 
                            someAdditionalParams
                        )
                        
                        aDeleteManyImpactReports[ 'impact_reports'].append( aReport)

            aDeleteManyImpactReports[ 'delete_permission'] = True
            someImpactReports = aDeleteManyImpactReports[ 'impact_reports']
            for anImpactReport in someImpactReports:
                if not anImpactReport.get( 'delete_permission', False):
                    aDeleteManyImpactReports[ 'delete_permission'] = False
                    break
                
                
            for anImpactReport in someImpactReports:
                someRelated = anImpactReport.get( 'related', [])
                for anIncludedElement in allIncludedElements:
                    try:
                        someRelated.remove( anIncludedElement)
                    except:
                        None
                        
                    
            aReport.update( {
                'num_elements_to_delete':  len( allIncludedElements),
                'num_elements_to_affect':  len( allRelatedElements),
            })
            
            
            
            aSecondsNow          = fSecondsNow()
            
            aDateNow             = DateTime( aSecondsNow * 1.0)
            aSecondsToDelete     = theModelDDvlPloneTool.fSecondsToReviewAndDelete( theContainerElement)
            aLatestDeleteSeconds = aSecondsNow + aSecondsToDelete
            aLatestDeleteTime    = DateTime( aLatestDeleteSeconds * 1.0) 
            
            aDeleteManyImpactReports.update( {
                'date_now':                aDateNow,
                'seconds_now':             aSecondsNow,
                'seconds_to_delete':       aSecondsToDelete,
                'latest_date_to_delete':   aLatestDeleteTime,
            })
            

            return aDeleteManyImpactReports
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fDeleteManyImpactReports', theTimeProfilingResults)


                
                
    security.declarePrivate( 'fObjectsToDeleteAndRelated_FromImpactReport')
    def fObjectsToDeleteAndRelated_FromImpactReport(self, theDeleteImpactReport):
        
        if not theDeleteImpactReport:
            return ( [], [], )

        someElementsToDelete = [ ]
        someRelatedElements  = [ ]
        
        someApplicationElementToDeleteImpactReports = theDeleteImpactReport[ 'included']
        if not someApplicationElementToDeleteImpactReports:
            someApplicationElementToDeleteImpactReports = []
        
        somePloneElementToDeleteImpactReports = theDeleteImpactReport[ 'plone']
        if not somePloneElementToDeleteImpactReports:
            somePloneElementToDeleteImpactReports = []
            
        someElementToDeleteImpactReports = someApplicationElementToDeleteImpactReports + somePloneElementToDeleteImpactReports    
        
        for anElementToDeleteImpactReport in someElementToDeleteImpactReports:
            self.pObjectsToDelete_FromElementImpactReport_recursive( 
                anElementToDeleteImpactReport, 
                someElementsToDelete, 
                someRelatedElements
            )
        
            
        someRelatedElements = []
        someRelatedReports = theDeleteImpactReport[ 'related']
        for aRelatedReport in someRelatedReports:
            unElement = aRelatedReport.get( 'object', '')
            if not ( unElement == None):
                someRelatedElements.append( unElement)
                
        
        return ( someElementsToDelete, someRelatedElements,)
    
    
        
        
    security.declarePrivate( 'pObjectsToDelete_FromElementImpactReport_recursive')
    def pObjectsToDelete_FromElementImpactReport_recursive(self, theElementDeleteImpactReport, theElementsToDelete, theRelatedElements):
        
        if not theElementDeleteImpactReport:
            return self
        
        unElementToDeleteResult = theElementDeleteImpactReport.get( 'here', {})
        if not unElementToDeleteResult:
            return self
        
        unElementToDelete = unElementToDeleteResult.get( 'object', None)
        if unElementToDelete == None:
            return self
            
        if not ( unElementToDelete in theElementsToDelete):
            theElementsToDelete.append( unElementToDelete)
   
        someElementsToDeleteReports = theElementDeleteImpactReport[ 'included']
        
        for unElementToDeleteReport in someElementsToDeleteReports:
            self.pObjectsToDelete_FromElementImpactReport_recursive( 
                unElementToDeleteReport, 
                someElementsToDelete, 
                someRelatedElements
            )
                    
                        
    
        return None    
    

    
    
    
    security.declarePrivate( 'fDeleteImpactReport')
    def fDeleteImpactReport(self , 
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a report of the impact of deleting an element, including all elements that will be related (contained elements) and elements that will be affected (related elements).
        
        """
 
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fDeleteImpactReport', theTimeProfilingResults)

        try:

            if theModelDDvlPloneTool == None:
                return None

            unSecondsNow = fSecondsNow()            
            if ( theElement == None):
                return None
                              
            
            unRootResult = self.fRetrieveTypeConfig( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =theElement, 
                theParent                   =None,
                theParentTraversalName      ='',
                theTypeConfig               =None, 
                theAllTypeConfigs           =None, 
                theViewName                 ='', 
                theRetrievalExtents         =[ 'traversals', 'tree', 'owner', 'cursor', ],
                theWritePermissions         =[ 'object', 'attrs', 'aggregations', 'relations', 'delete',],
                theFeatureFilters           ={ 'attrs': [ 'title', 'description'], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =None,
                theAdditionalParams         =theAdditionalParams                
            )
            if not unRootResult:
                return None


            
            someAdditionalParams = theAdditionalParams
            if someAdditionalParams == None:
                someAdditionalParams = { }
            else:
                someAdditionalParams = someAdditionalParams.copy()
                
            someAdditionalParams[ 'DoNotForbidDeletionFor_Aggregations_ReadOnly'] =  True
            
            
            allIncludedElements = []
            allRelatedElements = []
            allRelatedResults = []
            unCanDeleteHolder  = [ True ]
            
            aReport = self.fBuildDeleteImpactReport_AggregatedPass( 
                theTimeProfilingResults,
                unRootResult, 
                allIncludedElements, 
                allRelatedElements, 
                allRelatedResults, 
                unCanDeleteHolder, 
                someAdditionalParams
            )
            if not aReport:
                return None
        
            aReport[ 'delete_permission'] = unCanDeleteHolder[ 0] and aReport[ 'here'][ 'delete_permission'] and aReport[ 'here'][ 'owner_element'][ 'read_permission'] and aReport[ 'here'][ 'owner_element'][ 'write_permission']  and aReport[ 'here'][ 'cursor'][ 'traversal_result'][ 'read_permission'] and aReport[ 'here'][ 'cursor'][ 'traversal_result'][ 'write_permission']
            aReport[ 'related'] = allRelatedResults
            aReport[ 'column_names'] = [ 'title', 'description', ]
            aReport[ 'column_translations'] = self.getTranslationsForDefaultAttributes( theElement)

            self.pBuildDeleteImpactReport_RelatedPass(
                theTimeProfilingResults, 
                unRootResult, 
                allIncludedElements, 
                allRelatedElements, 
                allRelatedResults, 
                unCanDeleteHolder, 
                someAdditionalParams
            )
            
            #self.pBuildDeleteImpactReport_PropagatedPass(
                #theTimeProfilingResults, 
                #unRootResult, 
                #allIncludedElements, 
                #allRelatedElements, 
                #allRelatedResults, 
                #unCanDeleteHolder, 
                #theAdditionalParams
            #)
            
            
            
            aReport.update( {
                'num_elements_to_delete':  len( allIncludedElements),
                'num_elements_to_affect':  len( allRelatedElements),
            })
                
            
            
            aSecondsNow          = fSecondsNow()
            
            aDateNow             = DateTime( aSecondsNow * 1.0)
            aSecondsToDelete     = theModelDDvlPloneTool.fSecondsToReviewAndDelete( theElement)
            aLatestDeleteSeconds = aSecondsNow + aSecondsToDelete
            aLatestDeleteTime    = DateTime( aLatestDeleteSeconds * 1.0) 
            
            aReport.update( {
                'date_now':                aDateNow,
                'seconds_now':             aSecondsNow,
                'seconds_to_delete':       aSecondsToDelete,
                'latest_date_to_delete':   aLatestDeleteTime,
            })

            return aReport
            
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fDeleteImpactReport', theTimeProfilingResults)





    security.declarePrivate( 'fBuildDeleteImpactReport_AggregatedPass')
    def fBuildDeleteImpactReport_AggregatedPass(self , 
        theTimeProfilingResults =None,
        theRootResult           =None, 
        theAllIncludedElements  =[], 
        theAllRelatedElements   =[], 
        theAllRelatedResults    =[], 
        theCanDeleteHolder      =[],
        theAdditionalParams     =None):
    
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fBuildDeleteImpactReport_AggregatedPass', theTimeProfilingResults)

        try:

            if not theRootResult:
                return None
    
            unElement = theRootResult[ 'object']
            if not unElement:
                return None
            
            if unElement in theAllIncludedElements:
                return None
            
            theAllIncludedElements.append( unElement)
            
            if theCanDeleteHolder[ 0]:
                if not ( theRootResult[ 'read_permission'] and theRootResult[ 'write_permission'] and theRootResult[ 'delete_permission']):
                    theCanDeleteHolder[ 0] = False    
            
            someIncludedReports = []
            aReport = self.fNewVoidDeleteImpactReport()
            aReport.update( {
                'here':                     theRootResult,
                'included':                 someIncludedReports,
                'parent_traversal_name':    (theRootResult.get( 'cursor', {}) or {}).get( 'traversal_name', ''),
                'plone':                    [],
            })
    
            someObjectValues = unElement.objectValues()
            someObjectValuesPendingToReport = someObjectValues[:]
            someObjectValuesPendingToReport = [ anObject for anObject in someObjectValuesPendingToReport if not (  anObject.__class__.__name__ == 'ZCatalog')]
            
            someTraversalResults = theRootResult[ 'traversals']
            for unTraversalResult in someTraversalResults:
    
                if unTraversalResult[ 'traversal_kind'] == 'aggregation':
                    if theCanDeleteHolder[ 0]:
                        if not ( unTraversalResult[ 'read_permission'] and ( unTraversalResult[ 'write_permission'] or ( theAdditionalParams and theAdditionalParams.get('DoNotForbidDeletionFor_Aggregations_ReadOnly', False)))):
                            theCanDeleteHolder[ 0] = False 
                
                    if unTraversalResult[ 'contains_collections']:
                        someCollectionResults = unTraversalResult[ 'elements']
                        for unCollectionResult in someCollectionResults:
                            if theCanDeleteHolder[ 0]:
                                if not ( unCollectionResult[ 'read_permission'] and unCollectionResult[ 'write_permission'] and unCollectionResult[ 'delete_permission']):
                                    theCanDeleteHolder[ 0] = False 
                        
                            unaCollection = unCollectionResult[ 'object']
                            if unaCollection in someObjectValuesPendingToReport:
                                someObjectValuesPendingToReport.remove( unaCollection)
                            
                            someCollectionTraversalResults = unCollectionResult[ 'traversals']
                            for unCollectionTraversalResult in someCollectionTraversalResults:
                                if theCanDeleteHolder[ 0]:
                                    if not ( unCollectionTraversalResult[ 'read_permission'] and unCollectionTraversalResult[ 'write_permission']):
                                        theCanDeleteHolder[ 0] = False 
                            
                                someCollectionElementResults = unCollectionTraversalResult[ 'elements']
                                for unCollectionElementResult in someCollectionElementResults:
                                    unIncludedReport = self.fBuildDeleteImpactReport_AggregatedPass( 
                                        theTimeProfilingResults,
                                        unCollectionElementResult,  
                                        theAllIncludedElements, 
                                        theAllRelatedElements, 
                                        theAllRelatedResults, 
                                        theCanDeleteHolder,
                                        theAdditionalParams
                                    )
                                    if unIncludedReport:
                                        someIncludedReports.append( unIncludedReport)
                                        
                    else:
                        someElementResults = unTraversalResult[ 'elements']
                        for unElementResult in someElementResults:
                            unIncludedReport = self.fBuildDeleteImpactReport_AggregatedPass(
                                theTimeProfilingResults,
                                unElementResult,  
                                theAllIncludedElements, 
                                theAllRelatedElements, 
                                theAllRelatedResults, 
                                theCanDeleteHolder,
                                theAdditionalParams
                            )
                            if unIncludedReport:
                                someIncludedReports.append( unIncludedReport)
                                
                                unContainedElement = unElementResult[ 'object']
                                if unContainedElement in someObjectValuesPendingToReport:
                                    someObjectValuesPendingToReport.remove( unContainedElement)
    
                                
            if someObjectValuesPendingToReport:
                self.pBuildPendingDeleteImpactReports(
                    theTimeProfilingResults,
                    someObjectValuesPendingToReport, 
                    unElement, 
                    aReport, 
                    theAllIncludedElements, 
                    theAllRelatedElements, 
                    theAllRelatedResults, 
                    theCanDeleteHolder, 
                    theAdditionalParams
                )    
                

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fBuildDeleteImpactReport_AggregatedPass', theTimeProfilingResults)

        return aReport
        
    
                    
    
    
    
                
    security.declarePrivate( 'pBuildPendingDeleteImpactReports')
    def pBuildPendingDeleteImpactReports(self, 
        theTimeProfilingResults =None,
        theElements             =None, 
        theContainerElement     =None, 
        theContainerReport      =None, 
        theAllIncludedElements  =None, 
        theAllRelatedElements   =None, 
        theAllRelatedResults    =None, 
        theCanDeleteHolder      =None, 
        theAdditionalParams     =None):
    
    
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fBuildDeleteImpactReport', theTimeProfilingResults)
                
        try:

            if ( theContainerElement == None) or ( not theElements) or ( not theContainerReport):
                return self
                
            someArchetypeClassNames = []
            try:
                someArchetypeClassNames = theContainerElement.fArchetypeClassNames()
            except:
                None
            if not someArchetypeClassNames:
                someArchetypeClassNames = []
                
                
            somePloneSubItemsByTypeName = {}
            somePloneSubItemsParameters = self.fDefaultPloneSubItemsParameters( theElements[ 0])
            for aPloneSubItemsParameters in somePloneSubItemsParameters:
                someMetaTypeNames = aPloneSubItemsParameters[ 'allowed_types']
                for unMetaTypeName in someMetaTypeNames:
                    somePloneSubItemsByTypeName[ unMetaTypeName[ 'meta_type']] = aPloneSubItemsParameters  
             
                
            someKnownArchetypeObjectsPendingToReport = []
            someKnownPloneObjectsAndSubItemsParametersPendingToReport = []
            someUnknownPloneObjectsPendingToReport = []
            
            for anElement in theElements:
                if not ( anElement in theAllIncludedElements):
                    unMetaType = anElement.meta_type
                    if unMetaType in someArchetypeClassNames:
                        someKnownArchetypeObjectsPendingToReport.append( anElement)
                    elif somePloneSubItemsByTypeName.has_key( unMetaType):
                        someKnownPloneObjectsAndSubItemsParametersPendingToReport.append( [ anElement, somePloneSubItemsByTypeName.get( unMetaType, ''), ] )    
                    else:
                        someUnknownPloneObjectsPendingToReport.append( anElement)
                    
            if not( someKnownArchetypeObjectsPendingToReport or someKnownPloneObjectsAndSubItemsParametersPendingToReport or  someUnknownPloneObjectsPendingToReport):
                return self
                
            unAllTypeConfigs = {}
            unTranslationsCaches = self.fCreateTranslationsCaches()
            unCheckedPermissionsCache = self.fCreateCheckedPermissionsCache()
            
            for aKnownArchetypeObjectPendingToReport  in someKnownArchetypeObjectsPendingToReport:
                aResult = self.fRetrieveTypeConfig(
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =aKnownArchetypeObjectPendingToReport, 
                    theParent                   =None,
                    theParentTraversalName      ='',
                    theTypeConfig               =None, 
                    theAllTypeConfigs           =unAllTypeConfigs, 
                    theViewName                 ='', 
                    theRetrievalExtents         =None,
                    theWritePermissions         =[ 'object', 'delete', ],
                    theFeatureFilters           ={ 'attrs': [ 'title', 'description' ], 'aggregations': [], 'relations': [], }, 
                    theInstanceFilters          =None,
                    theTranslationsCaches       =unTranslationsCaches,
                    theCheckedPermissionsCache  =unCheckedPermissionsCache,
                    theAdditionalParams         =theAdditionalParams
                )
                if aResult:
                    if theCanDeleteHolder[ 0] and not ( aResult[ 'write_permission'] and  aResult[ 'delete_permission']):
                        theCanDeleteHolder[ 0] = False    

                    aReport = self.fNewVoidDeleteImpactReport()
                    aReport.update( {
                        'here':                     aResult,
                        'included':                 [],
                        'parent_traversal_name':    '',
                        'plone':                    []
                    })                
                    theContainerReport[ 'included'].append( aReport)
                    theAllIncludedElements.append( aKnownArchetypeObjectPendingToReport)

                
            for aKnownPloneObjectsAndSubItemsParametersPendingToReport in someKnownPloneObjectsAndSubItemsParametersPendingToReport:
                aKnownPloneObjectPendingToReport = aKnownPloneObjectsAndSubItemsParametersPendingToReport[ 0]
                aSubItemsParameter               = aKnownPloneObjectsAndSubItemsParametersPendingToReport[ 1]
                aResult = self.fRetrievePloneElement(
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =aKnownPloneObjectPendingToReport, 
                    thePloneSubItemsParameter   =aSubItemsParameter, 
                    theCanChangeValues          =theCanDeleteHolder[ 0],
                    theRetrievalExtents         =None,
                    theWritePermissions         =[ 'plone', 'delete_plone', ],
                    theFeatureFilters           =None, 
                    theInstanceFilters          =None,
                    theTranslationsCaches       =None,
                    theCheckedPermissionsCache  =None,
                    theAdditionalParams         =theAdditionalParams                    
                )
                if aResult:
                    if theCanDeleteHolder[ 0] and not ( aResult[ 'write_permission'] and  aResult[ 'delete_permission']):
                        theCanDeleteHolder[ 0] = False    

                    aReport = self.fNewVoidDeleteImpactReport()
                    aReport.update( {
                        'here':                     aResult,
                        'included':                 [],
                        'parent_traversal_name':    aSubItemsParameter[ 'traversal_name'],
                        'plone':                    []
                    })            
                    theContainerReport[ 'plone'].append( aReport)
                    theAllIncludedElements.append( aKnownPloneObjectPendingToReport)
                         

                
            for aUnknownPloneObjectPendingToReport in someUnknownPloneObjectsPendingToReport:
                aResult = self.fRetrievePloneElement(
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =aUnknownPloneObjectPendingToReport, 
                    thePloneSubItemsParameter   =None, 
                    theCanChangeValues          =theCanDeleteHolder[ 0],
                    theRetrievalExtents         =None,
                    theWritePermissions         =[ 'plone', 'delete_plone', ],
                    theFeatureFilters           =None, 
                    theInstanceFilters          =None,
                    theTranslationsCaches       =unTranslationsCaches,
                    theCheckedPermissionsCache  =unCheckedPermissionsCache,
                    theAdditionalParams         =None
                )
                if aResult:
                    if theCanDeleteHolder[ 0] and not ( aResult[ 'write_permission'] and  aResult[ 'delete_permission']):
                        theCanDeleteHolder[ 0] = False    

                    aReport = self.fNewVoidDeleteImpactReport()
                    aReport.update( {
                        'here':                     aResult,
                        'included':                 [],
                        'parent_traversal_name':    '',
                        'plone':                    []
                    })              
                    theContainerReport[ 'plone'].append( aReport)
                    theAllIncludedElements.append( aUnknownPloneObjectPendingToReport)
                
                    
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pBuildPendingDeleteImpactReports', theTimeProfilingResults)

        return self
        
    
    
    
    
    

    
    

    security.declarePrivate( 'pBuildDeleteImpactReport_RelatedPass')
    def pBuildDeleteImpactReport_RelatedPass(self , 
        theTimeProfilingResults =None,
        theRootResult           =None, 
        theAllIncludedElements  =None, 
        theAllRelatedElements   =None, 
        theAllRelatedResults    =None, 
        theCanDeleteHolder      =None, 
        theAdditionalParams     =None):
    
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'pBuildDeleteImpactReport_RelatedPass', theTimeProfilingResults)

        try:

            someTraversalResults = theRootResult[ 'traversals']
            for unTraversalResult in someTraversalResults:
                if unTraversalResult[ 'traversal_kind'] == 'relation':
                    
                    if not unTraversalResult.get( 'computed', False):
                            
                        someRelatedElementResults = unTraversalResult[ 'elements']
                        for unRelatedElementResult in someRelatedElementResults:
                            unRelatedElement = unRelatedElementResult[ 'object']
                            if not ( unRelatedElement in theAllRelatedElements) and not ( unRelatedElement in theAllIncludedElements):
                                if theCanDeleteHolder[ 0]:
                                    if not ( unRelatedElementResult[ 'read_permission'] and unRelatedElementResult[ 'write_permission']): # ACVOJO 20090210 and unRelatedElementResult[ 'delete_permission']):
                                        theCanDeleteHolder[ 0] = False 
                            
                                theAllRelatedResults.append( unRelatedElementResult) 
                                theAllRelatedElements.append( unRelatedElement) 

        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pBuildDeleteImpactReport_RelatedPass', theTimeProfilingResults)

        return self
        
    
    
    
    
 


    #security.declarePrivate( 'pBuildDeleteImpactReport_PropagatedPass')
    #def pBuildDeleteImpactReport_PropagatedPass(self , 
        #theTimeProfilingResults =None,
        #theRootResult           =None, 
        #theAllIncludedElements  =None, 
        #theAllRelatedElements   =None, 
        #theAllRelatedResults    =None, 
        #theCanDeleteHolder      =None, 
        #theAdditionalParams     =None):
    
        #if not ( theTimeProfilingResults == None):
            #self.pProfilingStart( 'pBuildDeleteImpactReport_PropagatedPass', theTimeProfilingResults)

        #try:

            #someDeletedAndRelatedElements = theAllIncludedElements + theAllRelatedElements
            #for aDeletedOrRelatedElement in someDeletedAndRelatedElements:
                
                #unosPropagateDeleteImpactTo = None
                #try:
                    #unosPropagateDeleteImpactTo = aDeletedOrRelatedElement.propagate_delete_impact_to
                #except:
                    #None

                #if unosPropagateDeleteImpactTo:
                    
                    #for unPropagateDeleteImpactTo in unosPropagateDeleteImpactTo:
                        #if unPropagateDeleteImpactTo:
                            #unPropagateStep = unPropagateDeleteImpactTo[ 0]
                            
                            #if unPropagateStep == 'contenedor_contenedorYPropietario':
                                
                                #unContenedor = None
                                #try:
                                    #unContenedor = aDeletedOrRelatedElement.getContenedor()
                                #except:
                                    #None
                                    
                                #if not ( unContenedor == None):
                                    
                                    #unContenedor_Propietario = None
                                    #try:
                                        #unContenedor_Propietario = unContenedor.getPropietario()
                                    #except:
                                        #None
                                    
                                    #unContenedor_Contenedor = None
                                    #try:
                                        #unContenedor_Contenedor = unContenedor.getContenedor()
                                    #except:
                                        #None
                                        
                                    #if ( not ( unContenedor_Propietario == None)) or( not ( unContenedor_Contenedor == None)):
                                        
                                        #unTranslationsCaches      = self.fCreateTranslationsCaches()
                                        #unCheckedPermissionsCache = self.fCreateCheckedPermissionsCache()                                    
                            
                                                                     
                                        #if not ( unContenedor_Propietario == None):
                                            #unContenedor_Propietario_Result = self.fRetrieveElementoBasicInfoAndTranslations( 
                                                #theTimeProfilingResults     =theTimeProfilingResults,
                                                #theElement                  =unContenedor_Propietario,      
                                                #theRetrievalExtents         =[],
                                                #theTranslationsCaches       =unTranslationsCaches,       
                                                #theCheckedPermissionsCache  =unCheckedPermissionsCache,
                                                #theResult                   =None,
                                                #theParentTraversalResult    =None,
                                                #theWritePermissions         =[ 'object',],     
                                                #theAdditionalParams         =theAdditionalParams     
                                            #)    
                                            #if unContenedor_Propietario_Result:
                                                #theAllRelatedResults.append( unContenedor_Propietario_Result) 
                                                #theAllRelatedElements.append( unContenedor_Propietario) 
                            
                                        #if ( not ( unContenedor_Contenedor == None)) and not ( unContenedor_Contenedor == unContenedor_Propietario_Result):
                                            #unContenedor_Contenedor_Result = self.fRetrieveElementoBasicInfoAndTranslations( 
                                                #theTimeProfilingResults     =theTimeProfilingResults,
                                                #theElement                  =unContenedor_Contenedor,      
                                                #theRetrievalExtents         =[],
                                                #theTranslationsCaches       =unTranslationsCaches,       
                                                #theCheckedPermissionsCache  =unCheckedPermissionsCache,
                                                #theResult                   =None,
                                                #theParentTraversalResult    =None,
                                                #theWritePermissions         =[ 'object',],     
                                                #theAdditionalParams         =theAdditionalParams     
                                            #)    
                                            #if unContenedor_Contenedor_Result:
                                                #theAllRelatedResults.append( unContenedor_Contenedor_Result) 
                                                #theAllRelatedElements.append( unContenedor_Contenedor) 
                                
                    
        #finally:
            #if not ( theTimeProfilingResults == None):
                #self.pProfilingEnd( 'pBuildDeleteImpactReport_PropagatedPass', theTimeProfilingResults)

        #return self
        
    
    
 
