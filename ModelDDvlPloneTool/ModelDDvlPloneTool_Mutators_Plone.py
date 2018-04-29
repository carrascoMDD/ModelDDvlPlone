# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Mutators_Plone.py
#
# Copyright (c) 2008, 2009, 2010 by Model Driven Development sl and Antonio Carrasco Valero
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


from Acquisition  import aq_inner, aq_parent


from Products.CMFCore.exceptions import AccessControl_Unauthorized

from AccessControl      import ClassSecurityInfo

from Products.Archetypes.utils import shasattr

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from Products.Relations.config                  import RELATIONS_LIBRARY
from Products.Relations                         import processor            as  gRelationsProcessor




from ModelDDvlPloneTool_Profiling       import ModelDDvlPloneTool_Profiling
  
from ModelDDvlPloneTool_Retrieval       import ModelDDvlPloneTool_Retrieval


from ModelDDvlPloneToolSupport          import fSecondsNow



cModificationKind_DeletePloneSubElement = 'DeletePloneSubElement'
cModificationKind_MovePloneSubObject    = 'MovePloneSubObject'

cModificationKind_DeletePloneSubElement_abbr = 'dpl'
cModificationKind_MovePloneSubObject_abbr    = 'mvp'



class ModelDDvlPloneTool_Mutators_Plone:
    """
    """
    security = ClassSecurityInfo()
                
    
    
    security.declarePrivate( 'fNewVoidDeletePloneElementReport')
    def fNewVoidDeletePloneElementReport( self,):
        aReport = {
            'parent_traversal_name':   '',
            'impact_report':           None,
            'impacted_objects_UIDs':   [],
            'effect':                  'error', 
            'failure':                 'Not executed',
        } 
        return aReport
        
   
    security.declarePrivate(   'fEliminarElementoPlone')
    def fEliminarElementoPlone(self , 
        theModelDDvlPloneTool   =None,
        theTimeProfilingResults =None,                          
        theContainerElement     =None, 
        theUIDToDelete          =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete an element of an standard Plone archetype (ATLink, ATDocument, ATImage, ATNewsItem).
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fEliminarElementoPlone', theTimeProfilingResults)

        try:

            aDeleteReport = self.fNewVoidDeletePloneElementReport()

            aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            
            if theModelDDvlPloneTool == None:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'No theModelDDvlPloneTool', })
                return aDeleteReport                 

            unSecondsNow = fSecondsNow()            
            if not ( (unSecondsNow >= theRequestSeconds) and ( ( unSecondsNow - theRequestSeconds) < theModelDDvlPloneTool.fSecondsToReviewAndDelete( theContainerElement))):
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'time_out', })
                return aDeleteReport                     

            if ( theContainerElement == None)  or not theUIDToDelete or not theRequestSeconds:
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'required_parameters_missing', })
                return aDeleteReport     
            
            unResultadoContenedor = aModelDDvlPloneTool_Retrieval.fRetrievePloneContent( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theContainerElement         =theContainerElement, 
                thePloneSubItemsParameters  =aModelDDvlPloneTool_Retrieval.fDefaultPloneSubItemsParameters( theContainerElement), 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'aggregations', 'plone', 'delete_plone', ],
                theFeatureFilters           =None, 
                theInstanceFilters          ={ 'UIDs': [ theUIDToDelete, ], },
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =None,
                theAdditionalParams         =theAdditionalParams
            )                

            if not unResultadoContenedor:
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'container_retrieval_failure', })
                return aDeleteReport     
            
            if not unResultadoContenedor[ 'traversals']:
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'traversal_retrieval_failure', })
                return aDeleteReport     
                
            unTraversalResult = unResultadoContenedor[ 'traversals'][ 0]
            if not unTraversalResult[ 'elements']:
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'traversal_elements_retrieval_failure',})
                return aDeleteReport  
                
            unTraversalName = unTraversalResult[ 'traversal_name' ]                   
            if not unTraversalResult[ 'elements']:
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'traversal_name_retrieval_failure', })
                return aDeleteReport  
            
            unElementResult = unTraversalResult[ 'elements'][ 0]
            if not unElementResult:
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'target_retrieval_failure', 'parent_traversal_name': unTraversalName, })
                return aDeleteReport     
            
            if not ( unElementResult[ 'UID'] == theUIDToDelete):
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'get_by_id_failure', 'parent_traversal_name': unTraversalName, })
                return aDeleteReport     
                
            unTargetElement = unElementResult[ 'object']
            if not unTargetElement:
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'target_object_retrieval_failure', 'parent_traversal_name': unTraversalName, })
                return aDeleteReport     
                                              
            unaIdToDelete = unElementResult[ 'id']
            if not unaIdToDelete:
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'target_id_retrieval_failure', 'parent_traversal_name': unTraversalName, })
                return aDeleteReport     

    
            if not ( unResultadoContenedor[ 'read_permission'] and unResultadoContenedor[ 'write_permission'] and unElementResult[ 'read_permission'] and unElementResult[ 'write_permission']):
                aDeleteReport.update(  { 'effect': 'error', 'failure': 'no_delete_permission', })
                return aDeleteReport     
                           
                
            self.pImpactDeletePloneIntoReport( unTargetElement, aDeleteReport)
            
            aDeleteReport.update(  { 'effect': 'deleted', 'parent_traversal_name': unTraversalName, 'plone_element_result': unElementResult })

            unContenedor = aq_parent( aq_inner( unTargetElement))
            if unContenedor:
                self.pSetAudit_Modification( unContenedor, cModificationKind_DeletePloneSubElement, aDeleteReport)    
            
            # ACV We are not really keeping defunct objects at this time, so we do not expend the effort on object that shall be gone immediately.
            # self.pSetAudit_Deletion( unTargetElement, cModificationKind_DeletePloneSubElement, aDeleteReport)  
                            
            theContainerElement.manage_delObjects( [ unaIdToDelete, ])
                
            return aDeleteReport     
    
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fEliminarElementoPlone', theTimeProfilingResults)

       
       
       

    
    security.declarePrivate( 'ImpactReport')
    def pImpactDeletePloneIntoReport( self, theElement, theDeleteReport):
 
        if ( theElement == None) or ( not theDeleteReport):
            return self

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
        
        return self
                    
                
                       

# #############################################################
# Plone content order mutators
#

                
    security.declarePrivate( 'fNewVoidMoveSubPloneObjectReport')
    def fNewVoidMoveSubPloneObjectReport( self,):
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
    
    
    

    security.declarePrivate( 'fMoveSubObjectPlone')
    def fMoveSubObjectPlone(self , 
        theTimeProfilingResults =None,                          
        theContainerElement     =None,  
        theTraversalName        ='', 
        theMovedObjectUID       =None, 
        theMoveDirection        ='', 
        theAdditionalParams     =None):        
        """Change the order index of an element of an standard Plone archetype (ATLink, ATDocument, ATImage, ATNewsItem) in the collection of elements aggregated in its container.
        
        """


        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'pMoveSubObjectPlone', theTimeProfilingResults)

        try:
            aMoveReport = self.fNewVoidMoveSubObjectReport()

            if ( theContainerElement == None)  or not  theTraversalName or not theMovedObjectUID or not theMoveDirection or not ( theMoveDirection.lower() in ['up', 'down', 'top', 'bottom', ]):
                return aMoveReport

            aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            
            unResult = aModelDDvlPloneTool_Retrieval.fRetrievePloneContent( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theContainerElement         =theContainerElement, 
                thePloneSubItemsParameters  =aModelDDvlPloneTool_Retrieval.fDefaultPloneSubItemsParameters( theContainerElement), 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'aggregations', 'plone', ],
                theFeatureFilters           ={ 'aggregations': [ theTraversalName], }, 
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

            if not (  unTraversalResult[ 'traversal_kind'] == 'aggregation-plone'):
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
                
                if aContainedResult[ 'UID'] == theMovedObjectUID:
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
                    return self
                
                
                self.pImpactMoveSubObjectIntoReport( theContainerElement, someContainedObjects, aMoveReport)
                
                theContainerElement.moveObjectsByDelta( [ unResultToMove[ 'id'], ], unDelta)

               
                unPositionAfterMove  = -1
                unMovedElementResult = None
                
                unResultAfterMove = aModelDDvlPloneTool_Retrieval.fRetrievePloneContent( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theContainerElement         =theContainerElement, 
                    thePloneSubItemsParameters  =aModelDDvlPloneTool_Retrieval.fDefaultPloneSubItemsParameters( theContainerElement), 
                    theRetrievalExtents         =[ 'traversals', ],
                    theWritePermissions         =[ 'object', 'aggregations', 'plone', ],
                    theFeatureFilters           ={ 'aggregations': [ theTraversalName], }, 
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
                            if unElementResult.get( 'UID', '') == theMovedObjectUID:
                                
                                unMovedElementResult = unElementResult
                                unPositionAfterMove = unElementIndex
                                break
                            
                aMoveReport.update( { 'effect': 'moved', 'moved_element': unMovedElementResult, 'new_position': unPositionAfterMove, 'delta': unDelta, 'parent_traversal_name': theTraversalName,})
                            

                self.pSetAudit_Modification( theContainerElement, cModificationKind_MovePloneSubObject, aMoveReport)       
                
            return aMoveReport
            
       
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pMoveSubObjectPlone', theTimeProfilingResults)
    
               