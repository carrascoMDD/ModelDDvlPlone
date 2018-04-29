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

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName



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
            'seconds_now':              0,
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
            'seconds_now':               0,
        }                
        return aReport
    

     

    security.declarePrivate( 'fDeleteManyImpactReports')
    def fDeleteManyImpactReports(self , 
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
            
            if ( theContainerElement == None):
                return aDeleteManyImpactReports
            
            
            aSecondsNow = self.getSecondsNow()
            aDeleteManyImpactReports[ 'seconds_now'] = aSecondsNow
            
            
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
                        theAdditionalParams
                    )
                    if aReport:
                        aReport[ 'delete_permission'] = unCanDeleteHolder[ 0] and aReport[ 'here'][ 'delete_permission'] and \
                               aReport[ 'here'][ 'owner_element'][ 'read_permission'] and aReport[ 'here'][ 'owner_element'][ 'write_permission']  and \
                               aReport[ 'here'][ 'cursor'][ 'traversal_result'][ 'read_permission'] and aReport[ 'here'][ 'cursor'][ 'traversal_result'][ 'write_permission']
                        aReport[ 'related'] = allRelatedResults
                        aReport[ 'column_names'] = someDefaultColumnNames
                        aReport[ 'column_translations'] = someDefaultColumnTranslations
                        aReport[ 'seconds_now'] = aSecondsNow
        
                        self.pBuildDeleteImpactReport_RelatedPass(
                            theTimeProfilingResults, 
                            unElementToDeleteResult, 
                            allIncludedElements, 
                            allRelatedElements, 
                            allRelatedResults, 
                            unCanDeleteHolder, 
                            theAdditionalParams
                        )
                        
                        aDeleteManyImpactReports[ 'impact_reports'].append( aReport)

            aDeleteManyImpactReports[ 'delete_permission'] = True
            someImpactReports = aDeleteManyImpactReports[ 'impact_reports']
            for anImpactReport in someImpactReports:
                if not anImpactReport.get( 'delete_permission', False):
                    aDeleteManyImpactReports[ 'delete_permission'] = False
                    break

            return aDeleteManyImpactReports
        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fDeleteManyImpactReports', theTimeProfilingResults)


                
                



    security.declarePrivate( 'fDeleteImpactReport')
    def fDeleteImpactReport(self , 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a report of the impact of deleting an element, including all elements that will be related (contained elements) and elements that will be affected (related elements).
        
        """
 
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fDeleteImpactReport', theTimeProfilingResults)

        try:

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
                theAdditionalParams
            )
            if aReport:
                aReport[ 'delete_permission'] = unCanDeleteHolder[ 0] and aReport[ 'here'][ 'delete_permission'] and aReport[ 'here'][ 'owner_element'][ 'read_permission'] and aReport[ 'here'][ 'owner_element'][ 'write_permission']  and aReport[ 'here'][ 'cursor'][ 'traversal_result'][ 'read_permission'] and aReport[ 'here'][ 'cursor'][ 'traversal_result'][ 'write_permission']
                aReport[ 'related'] = allRelatedResults
                aReport[ 'column_names'] = [ 'title', 'description', ]
                aReport[ 'column_translations'] = self.getTranslationsForDefaultAttributes( theElement)
                aReport[ 'seconds_now'] = self.getSecondsNow()

                self.pBuildDeleteImpactReport_RelatedPass(
                    theTimeProfilingResults, 
                    unRootResult, 
                    allIncludedElements, 
                    allRelatedElements, 
                    allRelatedResults, 
                    unCanDeleteHolder, 
                    theAdditionalParams
                )
                
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
                        if not ( unTraversalResult[ 'read_permission'] and unTraversalResult[ 'write_permission']):
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
            somePloneSubItemsParameters = self.fDefaultPloneSubItemsParameters()
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
        
    
    
 