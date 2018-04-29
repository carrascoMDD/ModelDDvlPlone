# -*- coding: utf-8 -*-
#
# File: MDDTool_Mutators.py
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

import os
import sys
import traceback
import logging


# Zope
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo

from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation

from time import time

from DateTime import DateTime




from Products.CMFCore                    import permissions
from Products.CMFCore.utils              import getToolByName, UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase




from Acquisition  import aq_inner, aq_parent,aq_get









# #######################################################
# #######################################################









class MDDTool_Mutators:
    """Subject Area Facade singleton object exposing services layer to the presentation layer, and delegating into a number of specialized, collaborating role realizations. 
    
    """

    
    security = ClassSecurityInfo()
    
    
    
    
    
    # ######################################
    """Operations on elements.
    
    """

    security.declareProtected( permissions.View, 'fDeleteImpactReport')
    def fDeleteImpactReport(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a report of the impact of deleting an element, including all elements that will be related (contained elements) and elements that will be affected (related elements).
        
        """
        
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theElement)
        
        unDeleteImpactReport =  aModelDDvlPloneTool_Retrieval.fDeleteImpactReport( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement,
            theAdditionalParams     =theAdditionalParams 
        )
        
        if not unDeleteImpactReport:
            return unDeleteImpactReport
        
        self.pBuildResultDictsForImpactReport( aModelDDvlPloneTool_Retrieval, unDeleteImpactReport)
                 
        return unDeleteImpactReport
        
        
    


    
    
    
    
    security.declareProtected( permissions.View, 'fDeleteImpactReport')
    def fDeleteManyImpactReports(self, 
        theTimeProfilingResults =None,
        theContainerElement     =None,
        theGroupUIDs            =[],
        theAdditionalParams     =None):
        """Retrieve a report of the impact of deleting an element, including all elements that will be related (contained elements) and elements that will be affected (related elements).
        
        """
        
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContainerElement)
        
        unDeleteManyImpactReports =  aModelDDvlPloneTool_Retrieval.fDeleteManyImpactReports( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement,
            theGroupUIDs            =theGroupUIDs,
            theAdditionalParams     =theAdditionalParams 
        )
        
        if not unDeleteManyImpactReports:
            return unDeleteManyImpactReports
        
        unContainerElementResult = unDeleteManyImpactReports.get( 'container_result', None)
        if unContainerElementResult:
            aModelDDvlPloneTool_Retrieval.pBuildResultDicts( unContainerElementResult)
            
        someImpactReports = unDeleteManyImpactReports[ 'impact_reports']
        for anImpactReport in someImpactReports:
            self.pBuildResultDictsForImpactReport( aModelDDvlPloneTool_Retrieval, anImpactReport)
                 
        return unDeleteManyImpactReports
        
    
    
            
    
    
    
    
    
    def pBuildResultDictsForImpactReport( self, theModelDDvlPloneTool_Retrieval, theImpactReport):
        if not theImpactReport:
            return self
        
        unElementResult =  theImpactReport.get( 'here', {})
        if unElementResult:        
            theModelDDvlPloneTool_Retrieval.pBuildResultDicts( unElementResult)
        
        unosPloneImpactResults = theImpactReport.get( 'plone', [])
        for unPloneImpactResult in unosPloneImpactResults:
            unPloneResult = unPloneImpactResult.get( 'here', {}) 
            if unPloneResult:
                theModelDDvlPloneTool_Retrieval.pBuildResultDicts( unPloneResult)
 
        unosRelatedResults = theImpactReport.get( 'related', [])
        for unRelatedResult in unosRelatedResults:
            theModelDDvlPloneTool_Retrieval.pBuildResultDicts( unRelatedResult)
                
        unosIncludedImpactReports = theImpactReport.get( 'included', [])
        for unIncludedImpactReport in unosIncludedImpactReports:
            self.pBuildResultDictsForImpactReport( theModelDDvlPloneTool_Retrieval, unIncludedImpactReport)

        return self
    
    
    
    
        
    
    
    
    
    

    
    
    
    # ####################################################
    """Change element methods.
    
    """
                
    
    
    
    # security.declareProtected( permissions.AddPortalContent,  'fCrearElementoDeTipo')
    security.declareProtected( permissions.View,  'fCrearElementoDeTipo')
    def fCrearElementoDeTipo(self, 
        theTimeProfilingResults =None,
        theContainerElement      =None, 
        theTypeName             ='', 
        theId                   =None,
        theTitle                ='', 
        theDescription          ='',
        theAdditionalParams     =None,
        theAllowFactoryMethods  =False,):           
        """Create a new contained element of a type.
        
        """
        
        aCreationReport = self.fModelDDvlPloneTool_Mutators( theContainerElement).fCrearElementoDeTipo( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement, 
            theTypeName             =theTypeName, 
            theId                   =theId,
            theTitle                =theTitle, 
            theDescription          =theDescription,
            theAdditionalParams     =theAdditionalParams,
            theAllowFactoryMethods  =theAllowFactoryMethods,
        )
        if not aCreationReport:
            return aCreationReport
        
        unNewElementResult = aCreationReport.get( 'new_object_result', None)
        if not unNewElementResult:
            return aCreationReport
        
        if not aCreationReport:
            return aCreationReport
        
        unosImpactedObjectsUIDs = aCreationReport.get( 'impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theContainerElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return aCreationReport
        
        
        
    
    
    
    
   
    # ACV OJO 20090917 Seems unused
    # security.declareProtected( permissions.AddPortalContent,  'fCrearElementoDeTipoEspecial')
    security.declareProtected( permissions.View,  'fCrearElementoDeTipoEspecial')
    def fCrearElementoDeTipoEspecial(self, 
        theTimeProfilingResults =None,
        theContainerElement     =None, 
        theId                   =None,
        theTypeName             ='', 
        theTitle                ='', 
        theDescription          ='',
        theAdditionalParams     =None):           
        """Create a new contained element of an special type type.
        
        """
        
        aCreationReport = self.fModelDDvlPloneTool_Mutators( theContainerElement).fCrearElementoDeTipo( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement, 
            theTypeName             =theTypeName, 
            theId                   =theId,
            theTitle                =theTitle, 
            theDescription          =theDescription,
            theAdditionalParams     =theAdditionalParams
        )
        if not aCreationReport:
            return aCreationReport
        
        if not aCreationReport:
            return aCreationReport
        
        unNewElementResult = aCreationReport.get( 'new_object_result', None)
        if not unNewElementResult:
            return aCreationReport
        
        if not aCreationReport:
            return aCreationReport
        
        unosImpactedObjectsUIDs = aCreationReport.get( 'impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theContainerElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return aCreationReport
       
        
        
                    
    
    
    
    
        
    # security.declareProtected(  permissions.ModifyPortalContent, 'fChangeValues')
    security.declareProtected(  permissions.View, 'fChangeValues')
    def fChangeValues(self, 
        theTimeProfilingResults =None,
        theElement              =None, 
        theNewValuesDict        =None,
        theAdditionalParams     =None):        
        """Apply changes to an element's attributes values.
        
        """
        
        unChangeReport = self.fModelDDvlPloneTool_Mutators( theElement).fChangeValues(  
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement, 
            theNewValuesDict        =theNewValuesDict,
            theAdditionalParams     =theAdditionalParams
        )
        if not unChangeReport:
            return unChangeReport
        
        unosImpactedObjectsUIDs = unChangeReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theElement, unosImpactedObjectsUIDs)
            
        return unChangeReport
        
        
    
    
    
    
    
    # security.declareProtected( permissions.ModifyPortalContent, 'fMoveSubObject')
    security.declareProtected( permissions.View, 'fMoveSubObject')
    def fMoveSubObject(self, 
        theTimeProfilingResults =None,
        theContainerElement      =None,  
        theTraversalName        =None, 
        theMovedObjectId        =None, 
        theMoveDirection        =None, 
        theAdditionalParams     =None):        
        """Change the order index of an element in the collection of elements aggregated in its container.
        
        """
        
        unMoveReport = self.fModelDDvlPloneTool_Mutators( theContainerElement).fMoveSubObject( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement,  
            theTraversalName        =theTraversalName, 
            theMovedObjectId        =theMovedObjectId, 
            theMoveDirection        =theMoveDirection, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unMoveReport:
            return unMoveReport
        
        unosImpactedObjectsUIDs = unMoveReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theContainerElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return unMoveReport
                
        
        
    
    
    
           
    # security.declareProtected( permissions.ModifyPortalContent, 'fMoveReferencedObject')
    security.declareProtected( permissions.View, 'fMoveReferencedObject')
    def fMoveReferencedObject(self,
        theTimeProfilingResults =None,
        theSourceElement        =None,  
        theReferenceFieldName   =None, 
        theMovedReferenceUID    =None, 
        theMoveDirection        =None,
        theAdditionalParams     =None):        
        """Change the order index of an element in the collection of related elements.
        
        """
        
        unMoveReport = self.fModelDDvlPloneTool_Mutators( theSourceElement).fMoveReferencedObject(
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theSourceElement        =theSourceElement,  
            theReferenceFieldName   =theReferenceFieldName, 
            theMovedReferenceUID    =theMovedReferenceUID, 
            theMoveDirection        =theMoveDirection, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unMoveReport:
            return unMoveReport
        
        unosImpactedObjectsUIDs = unMoveReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theSourceElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theSourceElement, unosImpactedObjectsUIDs)
            
        return unMoveReport
                  
    
    
 
    
    
    
     
    security.declareProtected( permissions.View, 'fLinkToUIDReferenceFieldNamed')
    # security.declareProtected(  permissions.ModifyPortalContent, 'fLinkToUIDReferenceFieldNamed')
    def fLinkToUIDReferenceFieldNamed(self, 
        theTimeProfilingResults =None,
        theSourceElement        =None, 
        theReferenceFieldName   =None, 
        theTargetUID            =None,
        theAdditionalParams     =None):        
        """Link an element as related to another element.
        
        """
        
        unLinkReport = self.fModelDDvlPloneTool_Mutators( theSourceElement).fLinkToUIDReferenceFieldNamed( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,            
            theSourceElement        =theSourceElement, 
            theReferenceFieldName   =theReferenceFieldName, 
            theTargetUID            =theTargetUID, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unLinkReport:
            return unLinkReport
        
        unosImpactedObjectsUIDs = unLinkReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theSourceElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theSourceElement, unosImpactedObjectsUIDs)
            
        return unLinkReport
        
       
    
    
    
        
    
    security.declareProtected( permissions.View, 'fUnlinkFromUIDReferenceFieldNamed')
    # security.declareProtected(  permissions.ModifyPortalContent, 'fUnlinkFromUIDReferenceFieldNamed')
    def fUnlinkFromUIDReferenceFieldNamed(self, 
        theTimeProfilingResults =None,
        theSourceElement        =None, 
        theReferenceFieldName   =None, 
        theTargetUID            =None,
        theAdditionalParams     =None):        
        """Unink an element from another related element.
        
        """

        unUnlinkReport = self.fModelDDvlPloneTool_Mutators( theSourceElement).fUnlinkFromUIDReferenceFieldNamed( 
            theTimeProfilingResults =theTimeProfilingResults,            
            theSourceElement        =theSourceElement, 
            theReferenceFieldName   =theReferenceFieldName, 
            theTargetUID            =theTargetUID, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unUnlinkReport:
            return unUnlinkReport
        
        unosImpactedObjectsUIDs = unUnlinkReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theSourceElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theSourceElement, unosImpactedObjectsUIDs)
            
        return unUnlinkReport
        
        
        
    
    
    
    
    
    security.declareProtected( permissions.DeleteObjects,  'fEliminarElemento')
    def fEliminarElemento(self, 
        theTimeProfilingResults =None,                          
        theElement              =None, 
        theIdToDelete           =None, 
        theUIDToDelete          =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete an element and all its contents.
        
        """

        unDeleteReport = self.fModelDDvlPloneTool_Mutators( theElement).fEliminarElemento( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theElement              =theElement,            
            theIdToDelete           =theIdToDelete, 
            theUIDToDelete          =theUIDToDelete, 
            theRequestSeconds       =theRequestSeconds, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unDeleteReport:
            return unDeleteReport
        
        unosImpactedObjectsUIDs = unDeleteReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theElement, unosImpactedObjectsUIDs)
            
        return unDeleteReport
        
    
              

    
    
    
    security.declareProtected( permissions.DeleteObjects,  'fEliminarVariosElementos')
    def fEliminarVariosElementos(self, 
        theTimeProfilingResults =None,                          
        theContainerElement     =None, 
        theIdsToDelete          =None, 
        theUIDsToDelete         =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete an element and all its contents.
        
        """

        someDeleteManyReports = self.fModelDDvlPloneTool_Mutators( theContainerElement).fEliminarVariosElementos( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,
            theContainerElement     =theContainerElement,            
            theIdsToDelete          =theIdsToDelete, 
            theUIDsToDelete         =theUIDsToDelete, 
            theRequestSeconds       =theRequestSeconds, 
            theAdditionalParams     =theAdditionalParams
        )
        if not someDeleteManyReports:
            return someDeleteManyReports
        
        unasUIDsAlreadyFlushed = set( )
        
        for unDeleteReport in someDeleteManyReports:
        
            if unDeleteReport and ( unDeleteReport.get( 'effect', '') == 'deleted'):
                unImpactReport = unDeleteReport.get( 'impact_report', {})
                unosImpactedObjectsUIDs = unDeleteReport.get('impacted_objects_UIDs', [])
                unasUIDsNoFlushed = [ unaUID for unaUID in unosImpactedObjectsUIDs if not ( unaUID in unasUIDsAlreadyFlushed)]
    
                if unasUIDsNoFlushed:
                    self.fModelDDvlPloneTool_Cache( theContainerElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unasUIDsNoFlushed)
                    unasUIDsAlreadyFlushed.update( unasUIDsNoFlushed)
            
        return someDeleteManyReports
    
                
    
        
    
    
    
    
    
    
    
    
    
    # ####################################################
    """Change Plone methods.
    
    """
                
                
    
    
    
    security.declareProtected( permissions.DeleteObjects,  'fEliminarElementoPlone')
    def fEliminarElementoPlone(self, 
        theTimeProfilingResults =None,                          
        theContainerElement     =None, 
        theUIDToDelete          =None, 
        theRequestSeconds       =None, 
        theAdditionalParams     =None):        
        """Delete an element of an standard Plone archetype (ATLink, ATDocument, ATImage, ATNewsItem).
        
        """

        unDeleteReport = self.fModelDDvlPloneTool_Mutators_Plone( theContainerElement).fEliminarElementoPlone( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults, 
            theContainerElement     =theContainerElement,
            theUIDToDelete          =theUIDToDelete, 
            theRequestSeconds       =theRequestSeconds, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unDeleteReport:
            return unDeleteReport
        
        unosImpactedObjectsUIDs = unDeleteReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theContainerElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return unDeleteReport

            
    
    
    
    
    security.declareProtected( permissions.View, 'fMoveSubObjectPlone')
    # security.declareProtected( permissions.ModifyPortalContent, 'fMoveSubObjectPlone')
    def fMoveSubObjectPlone(self, 
        theTimeProfilingResults =None,                          
        theContainerElement     =None,  
        theTraversalName        ='', 
        theMovedObjectUID       =None, 
        theMoveDirection        ='', 
        theAdditionalParams     =None):        
        """Change the order index of an element of an standard Plone archetype (ATLink, ATDocument, ATImage, ATNewsItem) in the collection of elements aggregated in its container.
        
        """

        unMoveReport = self.fModelDDvlPloneTool_Mutators_Plone( theContainerElement).fMoveSubObjectPlone( 
            theModelDDvlPloneTool   =self,
            theTimeProfilingResults =theTimeProfilingResults,            
            theContainerElement     =theContainerElement,  
            theTraversalName        =theTraversalName, 
            theMovedObjectUID       =theMovedObjectUID, 
            theMoveDirection        =theMoveDirection, 
            theAdditionalParams     =theAdditionalParams
        )
        if not unMoveReport:
            return unMoveReport
        
        unosImpactedObjectsUIDs = unMoveReport.get('impacted_objects_UIDs', [])

        if unosImpactedObjectsUIDs:
            self.fModelDDvlPloneTool_Cache( theContainerElement).pFlushCachedTemplatesForImpactedElementsUIDs( self, theContainerElement, unosImpactedObjectsUIDs)
            
        return unMoveReport
                  
    
    
    
    
    
    
    
    
    
    

        
    # #############################################################
    """Actions applied to multiple elements selected in the same aggregation or collection or relations table.
    
    """


       
    security.declareProtected( permissions.View, 'fGroupAction')
    def fGroupAction(self, 
        theTimeProfilingResults     =None,
        theContainerObject          =None, 
        theGroupAction              =None,
        theGroupUIDs                =None,
        theReferenceFieldName       =None,
        theAdditionalParams         =None):
        """Process a request for an action affecting multiple elements, given their UIDs. Actions may be Delete objects, or Prepare to Cut (move) or Prepare to Copy objects. 
        Cut and Copy are prepared by setting a cookie in the HTTP request response including references ( monikers) for the selected elements.        
        
        """
        
        aModelDDvlPloneTool_Retrieval = self.fModelDDvlPloneTool_Retrieval( theContainerObject)

        if theGroupAction == 'Cut':
            return self.fModelDDvlPloneTool_Refactor( theContainerObject).fGroupAction_CutOrCopy( 
                theTimeProfilingResults        = theTimeProfilingResults,
                theModelDDvlPloneTool          = self,
                theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
                theContainerObject             = theContainerObject, 
                theGroupUIDs                   = theGroupUIDs,
                theReferenceFieldName          = theReferenceFieldName,
                theIsCut                       = True,
                theAdditionalParams            = theAdditionalParams
            )
           
            
        elif theGroupAction == 'Copy':
            return self.fModelDDvlPloneTool_Refactor( theContainerObject).fGroupAction_CutOrCopy( 
                theTimeProfilingResults        = theTimeProfilingResults,
                theModelDDvlPloneTool          = self,
                theModelDDvlPloneTool_Retrieval= aModelDDvlPloneTool_Retrieval,
                theContainerObject             = theContainerObject, 
                theGroupUIDs                   = theGroupUIDs,
                theReferenceFieldName          = theReferenceFieldName,
                theIsCut                       = False,
                theAdditionalParams            = theAdditionalParams
            )
            
        # ACV 20090930 Handled by the standard Plone manage_paste, implemented in all non-abstract types
        #elif theGroupAction == 'Paste':
            #return self.fPaste( 
                #theTimeProfilingResults        = theTimeProfilingResults,
                #theContainerObject             = theContainerObject, 
                #theGroupUIDs                   = theGroupUIDs,
                #theAdditionalParams            = theAdditionalParams
            #)
            
            
        elif theGroupAction == 'Delete':
            # ACV 20090930 Handled by a specific view MDDEliminarVarios
            pass
        
   
        return None
    
        
        
        
        
    
    
    
    
    

        
    
    
    
    
    
        
    

    
    
    
    
    
    
    security.declarePrivate('_pSetAudit_Modification')
    def _pSetAudit_Modification(self, theElement, theChangeKind, theChangeReport, theReverseRelation=False):     
        """Invoked from an element intercepting drag&drop reordering and logging its changes.
        
        """
        self.fModelDDvlPloneTool_Mutators( theElement).pSetAudit_Modification( theElement, theChangeKind, theChangeReport, theReverseRelation)
        return self
    
    
        