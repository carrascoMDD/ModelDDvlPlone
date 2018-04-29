# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Mutators_Plone.py
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


from Acquisition  import aq_inner, aq_parent


from Products.CMFCore.exceptions import AccessControl_Unauthorized

from AccessControl      import ClassSecurityInfo

from Products.Archetypes.utils import shasattr

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from Products.Relations.config                  import RELATIONS_LIBRARY
from Products.Relations                         import processor            as  gRelationsProcessor


from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Profiling       import ModelDDvlPloneTool_Profiling
  
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval       import ModelDDvlPloneTool_Retrieval



class ModelDDvlPloneTool_Mutators_Plone:
    """
    """
    security = ClassSecurityInfo()
                
   
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

            aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            
            if theModelDDvlPloneTool == None:
                aDeleteReport.update( { 'effect': 'error', 'failure': 'No theModelDDvlPloneTool', })
                return aDeleteReport                 

            unSecondsNow = ModelDDvlPloneTool_Retrieval().fSecondsNow()            
            if not ( (unSecondsNow >= theRequestSeconds) and ( ( unSecondsNow - theRequestSeconds) < theModelDDvlPloneTool.fSecondsToReviewAndDelete( theContainerElement))):
                anActionReport = { 'effect': 'error', 'failure': 'time_out', }
                return anActionReport                     

            if ( theContainerElement == None)  or not theUIDToDelete or not theRequestSeconds:
                anActionReport = { 'effect': 'error', 'failure': 'required_parameters_missing', }
                return anActionReport     
            
            unResultadoContenedor = aModelDDvlPloneTool_Retrieval.fRetrievePloneContent( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theContainerElement         =theContainerElement, 
                thePloneSubItemsParameters  =aModelDDvlPloneTool_Retrieval.fDefaultPloneSubItemsParameters(), 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'aggregations', 'plone', 'delete_plone', ],
                theFeatureFilters           =None, 
                theInstanceFilters          ={ 'UIDs': [ theUIDToDelete, ], },
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =None,
                theAdditionalParams         =theAdditionalParams
            )                

            if not unResultadoContenedor:
                anActionReport = { 'effect': 'error', 'failure': 'container_retrieval_failure', }
                return anActionReport     
            
            if not unResultadoContenedor[ 'traversals']:
                anActionReport = { 'effect': 'error', 'failure': 'traversal_retrieval_failure', }
                return anActionReport     
                
            unTraversalResult = unResultadoContenedor[ 'traversals'][ 0]
            if not unTraversalResult[ 'elements']:
                anActionReport = { 'effect': 'error', 'failure': 'traversal_elements_retrieval_failure',}
                return anActionReport  
                
            unTraversalName = unTraversalResult[ 'traversal_name' ]                   
            if not unTraversalResult[ 'elements']:
                anActionReport = { 'effect': 'error', 'failure': 'traversal_name_retrieval_failure', }
                return anActionReport  
            
            unElementResult = unTraversalResult[ 'elements'][ 0]
            if not unElementResult:
                anActionReport = { 'effect': 'error', 'failure': 'target_retrieval_failure', 'parent_traversal_name': unTraversalName, }
                return anActionReport     
            
            if not ( unElementResult[ 'UID'] == theUIDToDelete):
                anActionReport = { 'effect': 'error', 'failure': 'get_by_id_failure', 'parent_traversal_name': unTraversalName, }
                return anActionReport     
                
            unTargetElement = unElementResult[ 'object']
            if not unTargetElement:
                anActionReport = { 'effect': 'error', 'failure': 'target_object_retrieval_failure', 'parent_traversal_name': unTraversalName, }
                return anActionReport     
                                              
            unaIdToDelete = unElementResult[ 'id']
            if not unaIdToDelete:
                anActionReport = { 'effect': 'error', 'failure': 'target_id_retrieval_failure', 'parent_traversal_name': unTraversalName, }
                return anActionReport     

    
            if not ( unResultadoContenedor[ 'read_permission'] and unResultadoContenedor[ 'write_permission'] and unElementResult[ 'read_permission'] and unElementResult[ 'write_permission']):
                anActionReport = { 'effect': 'error', 'failure': 'no_delete_permission', }
                           
                
            unContenedor = aq_parent( aq_inner( unTargetElement))
            if unContenedor:
                self.pSetAudit_Modification( unContenedor)       
            
            self.pSetAudit_Deletion( unTargetElement)  
                            
            theContainerElement.manage_delObjects( [ unaIdToDelete, ])
                
            anActionReport = { 'effect': 'deleted', 'parent_traversal_name': unTraversalName, }
            return anActionReport     
    
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fEliminarElementoPlone', theTimeProfilingResults)

       
       
       
       

# #############################################################
# Plone content order mutators
#


    security.declarePrivate( 'pMoveSubObjectPlone')
    def pMoveSubObjectPlone(self , 
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

            if ( theContainerElement == None)  or not  theTraversalName or not theMovedObjectUID or not theMoveDirection or not ( theMoveDirection.lower() in ['up', 'down', 'top', 'bottom', ]):
                return self

            aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
            
            unResult = aModelDDvlPloneTool_Retrieval.fRetrievePloneContent( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theContainerElement         =theContainerElement, 
                thePloneSubItemsParameters  =aModelDDvlPloneTool_Retrieval.fDefaultPloneSubItemsParameters(), 
                theRetrievalExtents         =[ 'traversals', ],
                theWritePermissions         =[ 'object', 'aggregations', 'plone', ],
                theFeatureFilters           ={ 'aggregations': [ theTraversalName], }, 
                theInstanceFilters          =None,
                theTranslationsCaches       =None,
                theCheckedPermissionsCache  =None,
                theAdditionalParams         =theAdditionalParams
            )
                        
            if not unResult:
                return self
        
            if not (  unResult[ 'read_permission'] and unResult[ 'write_permission']):
                return self
    
            unTraversalResult =  unResult[ 'traversals_by_name'].get( theTraversalName, None)
            if not unTraversalResult:
                return self

            if not (  unTraversalResult[ 'traversal_kind'] == 'aggregation-plone'):
                return self
                
            if not (  unTraversalResult[ 'read_permission'] and unTraversalResult[ 'write_permission']):
                return self
    
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
                
                theContainerElement.moveObjectsByDelta( [ unResultToMove[ 'id'], ], unDelta)

                self.pSetAudit_Modification( theContainerElement)   
                
            return self
            
       
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pMoveSubObjectPlone', theTimeProfilingResults)
    
               