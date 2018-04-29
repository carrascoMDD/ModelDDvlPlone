# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Refactor.py
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

from Acquisition        import aq_inner, aq_parent


from OFS             import Moniker        
from OFS.CopySupport import CopyError

from marshal import loads, dumps
from urllib import quote, unquote
from zlib import compress, decompress

from AccessControl import ClassSecurityInfo

from App.Dialogs import MessageDialog

from webdav.Lockable import ResourceLockedError

from Products.CMFCore.utils import getToolByName


from ModelDDvlPloneTool_Refactor_Constants      import *

from ModelDDvlPloneTool_Transactions            import ModelDDvlPloneTool_Transactions

from ModelDDvlPloneTool_Profiling               import ModelDDvlPloneTool_Profiling

from MDD_RefactorComponents                     import MDDRefactor_Paste

from ModelDDvlPloneToolSupport               import fPrettyPrint





cLogExceptions = True




cClipboardCookieName = '__cp'



class MDDRefactor_Paste_Exception( Exception): pass


    
# ######################################################
# 
# ######################################################
    

class ModelDDvlPloneTool_Refactor( ModelDDvlPloneTool_Profiling):
    """
    """
    security = ClassSecurityInfo()

    
    
    def fNewVoidClipboardResult( self,):
        
        unResult = {
            'is_move_operation':       False,
            'num_elements':            0,
            'num_contained_elements':  0,
            'total_elements':          0,
            'has_same_root_as_context':False,
            'num_other_roots':         0,
            'num_unsupported_roots':   0,
            'elements_by_roots':       [],
            'num_elements':            0,
            'num_contained_elements':  0,
            'total_elements':          0,
            'portal_url':              '',
        }
        return unResult
    
    
   
    def fNewVoidElementsResultForOneRoot( self,):
        
        unResult = {
            'is_supported_root':       False,
            'root_path':               '',
            'root_title':              '',
            'root_url':                '',
            'is_same_root_as_context': False,
            'num_elements':            0,
            'num_contained_elements':  0,
            'total_elements':          0,
            'elements':                [],
        }
        return unResult
    
    
    
   
    security.declarePrivate( 'pClearClipboard')
    def pClearClipboard(self, 
        theModelDDvlPloneTool            =None,
        theTimeProfilingResults          =None,
        theContextualElement             =None, 
        theAdditionalParams              =None):
        
        aRequest = None
        try:
            aRequest = theContextualElement.REQUEST
        except:
            None
        if ( aRequest == None):
            return self
        
        if aRequest.has_key( cClipboardCookieName):
            try:
                aRequest.form.pop( cClipboardCookieName)
            except:
                None
            try:
                aRequest.cookies.pop( cClipboardCookieName)
            except:
                None
            try:
                aRequest.other.pop( cClipboardCookieName)
            except:
                None
        
        aResponse =  aRequest.response        
        aResponse.expireCookie(cClipboardCookieName, path='%s' % self.fPathForCookie( aRequest))

        return self
    
    
    
    
    
        
    
    
    security.declarePrivate( 'fClipboardResult')
    def fClipboardResult(self, 
        theModelDDvlPloneTool            =None,
        theModelDDvlPloneTool_Retrieval  =None,
        theTimeProfilingResults          =None,
        theContextualElement             =None, 
        theAdditionalParams              =None):
    
        unClipboardResult = self.fNewVoidClipboardResult()
    
        aClipboardOperation, someElementsInClipboard = self.fClipboardOperationAndElements( theModelDDvlPloneTool, theContextualElement)
        
        unClipboardResult[ 'is_move_operation']  = aClipboardOperation == 1
        
        if not someElementsInClipboard:
            return unClipboardResult
        
        
        unContextualPathDelRaiz = ''
        try:
            unContextualPathDelRaiz = theContextualElement.fPathDelRaiz()
        except:
            None
        
        
        unNumElements          = 0
        unNumContainedElements = 0
        
        someElementsByRoots = { }
        
        for anElement in someElementsInClipboard:
            anElementResult = theModelDDvlPloneTool_Retrieval.fRetrieveElementoBasicInfoAndTranslations( 
                theTimeProfilingResults     =theTimeProfilingResults,
                theElement                  =anElement, 
                theRetrievalExtents         =[ 'num_contained',],
                theTranslationsCaches       =None, 
                theCheckedPermissionsCache  =None, 
                theResult                   =None,
                theParentTraversalResult    =None,
                theWritePermissions         =None,
                theAdditionalParams         =theAdditionalParams)
            
            if anElementResult and not ( anElementResult[ 'object'] == None):
                
                unPathDelRaiz = anElementResult.get( 'root_path', '')
                unResultForOneRoot = someElementsByRoots.get( unPathDelRaiz, None)
                if unResultForOneRoot == None:
                    unResultForOneRoot = self.fNewVoidElementsResultForOneRoot()
                    unResultForOneRoot[ 'root_title'] = anElementResult.get( 'root_title', '')
                    unResultForOneRoot[ 'root_url']   = anElementResult.get( 'root_url', '')
                    unResultForOneRoot[ 'root_path']  = unPathDelRaiz
                    unResultForOneRoot[ 'is_root_supported']  = anElementResult[ 'is_root_supported']
                    if unPathDelRaiz == unContextualPathDelRaiz:
                        unResultForOneRoot[ 'is_same_root_as_context'] = True
                    someElementsByRoots[ unPathDelRaiz] = unResultForOneRoot
                
                unResultForOneRoot[ 'elements'].append( anElementResult)
                
                unResultForOneRoot[ 'num_elements']           += 1
                unResultForOneRoot[ 'num_contained_elements'] += anElementResult.get( 'num_contained', 0)
                unResultForOneRoot[ 'total_elements']         += 1 + anElementResult.get( 'num_contained', 0)
                
            
        unThisRoot     = None
        someOtherRoots = [ ]                
        for unResultForOneRoot in someElementsByRoots.values():
            unResultForOneRoot[ 'elements'] = sorted( unResultForOneRoot['elements'], lambda unR, otroR: cmp( unR.get( 'title', ''), otroR.get( 'title', '')))
            
            unClipboardResult[ 'num_elements']           += unResultForOneRoot[ 'num_elements']
            unClipboardResult[ 'num_contained_elements'] += unResultForOneRoot[ 'num_contained_elements']
            unClipboardResult[ 'total_elements']         += unResultForOneRoot[ 'total_elements']
            
            if unResultForOneRoot[ 'root_path'] == unContextualPathDelRaiz:
                unClipboardResult[ 'has_same_root_as_context'] = True
                unThisRoot = unResultForOneRoot
            else:
                someOtherRoots.append( unResultForOneRoot)
                if unResultForOneRoot.get( 'is_root_supported', False):
                    unClipboardResult[ 'num_other_roots'] += 1
                else:
                    unClipboardResult[ 'num_unsupported_roots'] += 1
                    
                
        someSortedOtherRoots = sorted( someOtherRoots, lambda unR, otroR: cmp( unR.get( 'root_path', ''), otroR.get( 'root_path', '')))
         
        if unThisRoot:
            unClipboardResult[ 'elements_by_roots'].append( unThisRoot)
        unClipboardResult[ 'elements_by_roots'].extend( someSortedOtherRoots)
               
        
        unPortalObject = None
        unPortalURLTool = getToolByName( theContextualElement, 'portal_url')
        if unPortalURLTool:
            unPortalURL = ''
            try:
                unPortalURL = unPortalURLTool()
            except: 
                None
            if unPortalURL:
                unClipboardResult[ 'portal_url'] = unPortalURL 
            try:
                unPortalObject = unPortalURLTool.getPortalObject()
            except: 
                None
            if not ( unPortalObject == None):
                unClipboardResult[ 'portal_object'] = unPortalObject         

        return unClipboardResult
    
    
    
    
    
    
    
    # ACV 20091001 Unused. Removed.
    #security.declarePrivate( 'fTraversalTargetAdditionalParams')    
    #def fTraversalTargetAdditionalParams( self,):
        #unosParams = {
            #'Do_Not_Translate' : True,
            #'Retrieve_Minimal_Related_Results': True,
        #}
        #return unosParams
    
    
    
    security.declarePrivate( 'fTraversalSourcesAdditionalParams')    
    def fTraversalSourcesAdditionalParams( self,):
        unosParams = {
            'Do_Not_Translate' : True,
            'Retrieve_Minimal_Related_Results': True,
        }
        return unosParams
    
        
    
    security.declarePrivate( 'fNewVoidPasteContext')    
    def fNewVoidPasteContext( self,):
        unContext = {
            'container_object':         None,
            'objects_to_paste':         [],
            'is_move_operation':        False,
            'ModelDDvlPloneTool':       None,
            'ModelDDvlPloneTool_Retrieval': None,
            'ModelDDvlPloneTool_Mutators': None,
            'checked_permissions_cache': None,
            'mdd_copy_type_configs':    {},
            'plone_copy_type_configs':  {},
            'all_copy_type_configs':    {},
            'mapping_configs':          [],
            'additional_params':        self.fTraversalSourcesAdditionalParams(),
            'report':                   self.fNewVoidPasteReport(),
        }
        return unContext
    
      
    
    security.declarePrivate( 'fNewVoidPasteReport')    
    def fNewVoidPasteReport( self,):
        unInforme = {
            'success':                  False,
            'status':                   '',
            'condition':                None,
            'exception':                '',
            'num_elements_pasted':      0,
            'num_mdd_elements_pasted':  0,
            'num_plone_elements_pasted': 0,
            'num_elements_failed':      0,
            'num_mdd_elements_failed':  0,
            'num_plone_elements_failed': 0,
            'num_elements_bypassed':      0,
            'num_mdd_elements_bypassed':  0,
            'num_plone_elements_bypassed': 0,
            'error_reports':            [ ],
        }
        return unInforme
    
                
    
    
    
    security.declarePrivate( 'fGroupAction_CutOrCopy')
    def fGroupAction_CutOrCopy( self,
        theTimeProfilingResults     =None,
        theModelDDvlPloneTool      = None,
        theModelDDvlPloneTool_Retrieval= None,
        theContainerObject          =None, 
        theGroupUIDs                =[],
        theIsCut                    =False,
        theAdditionalParams         =None):
        """Prepare for Cut or Copy the elements given their UIDs, by setting a cookie in the HTTP request response including references ( monikers) for the selected elements, and whether the operation is a move (cut) or not (just copy).        

        """
        if not theModelDDvlPloneTool_Retrieval:
            return CopyError, 'Internal Parameter missing theModelDDvlPloneTool_Retrieval'
        
        if not theGroupUIDs:
            return self.fExceptionDialog_NoItemsSpecified( theModelDDvlPloneTool, theContainerObject)
        
        unasGroupUIDs = theGroupUIDs
        if not ( unasGroupUIDs.__class__.__name__ in [ 'list', 'tuple', 'set']):
            unasGroupUIDs = [ unasGroupUIDs, ]
                
        unosMonikers = [ ]
        
        for unaUID in unasGroupUIDs:
            unElemento = theModelDDvlPloneTool_Retrieval.fElementoPorUID( unaUID, theContainerObject)
            if unElemento:
            
                if unElemento.wl_isLocked():
                    raise ResourceLockedError, 'Object "%s" is locked via WebDAV' % '/'.join( unElemento.getPhysicalPath())
    
                if theIsCut and not unElemento.cb_isMoveable():
                    raise CopyError, self.fExceptionDialog_MoveNotSupported( theModelDDvlPloneTool, theContainerObject) 
                
                if ( not theIsCut)  and not unElemento.cb_isCopyable():
                    raise CopyError, self.fExceptionDialog_CopyNotSupported( theModelDDvlPloneTool, theContainerObject) 
                
                unMoniker = Moniker.Moniker( unElemento)
                
                unosMonikers.append( unMoniker.dump())
                
        if not unosMonikers:
            raise CopyError, self.fExceptionDialog_NoItemsCopied( theModelDDvlPloneTool, theContainerObject)
                
        unIsMoveClipboardParameter = ( theIsCut and 1) or 0
        
        unClipBoardContent = ( unIsMoveClipboardParameter, unosMonikers) 
        
        unClipBoardCookieContent = self.fClipboardEncode( unClipBoardContent)
        
        aRequest = None
        try:
            aRequest = theContainerObject.REQUEST
        except:
            None
        if ( aRequest == None):
            return True
        
        aResponse =  aRequest.response
        if aResponse:
            aResponse.setCookie(cClipboardCookieName, unClipBoardCookieContent, path='%s' % self.fPathForCookie( aRequest))
        aRequest[cClipboardCookieName] = unClipBoardCookieContent
    
        return len( unosMonikers)
        
        
    
    
    
    
    
        
    
    security.declarePrivate( 'fPathForCookie')
    def fPathForCookie( self, theRequest):
        if not theRequest:
            return '/'
        
        # Return a "path" value for use in a cookie that refers
        # to the root of the Zope object space.
        return theRequest.get( 'BASEPATH1', '') or "/"
        
        
        
    security.declarePrivate( 'fClipboardEncode')
    def fClipboardEncode( self, theData):
        return quote( compress( dumps( theData), 9))        
        
    
    security.declarePrivate( 'fClipboardDecode')
    def fClipboardDecode( self, theClipboard):
        return loads(decompress(unquote( theClipboard)))        
        
     
    
    security.declarePrivate( 'fExceptionDialog_NoItemsSpecified')
    def fExceptionDialog_NoItemsSpecified( self, theModelDDvlPloneTool, theContextualElement):
        
        aMessageDialog =MessageDialog(
            title    = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'No items specified','No items specified-'),
            message  = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'You must select one or more items to perform this operation.', 'You must select one or more items to perform this operation.'),
            action ='Tabular'
        )    
        return aMessageDialog
    
    
    
    security.declarePrivate( 'fExceptionDialog_NoItemsCopied')
    def fExceptionDialog_NoItemsSpecified( self, theModelDDvlPloneTool, theContextualElement):
        
        aMessageDialog =MessageDialog(
            title    = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'ModelDDvlPlone', 'ModelDDvlPlone_No_items_copied','No items copied-'),
            message  = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'You must select one or more items to perform this operation.', 'You must select one or more items to perform this operation.'),
            action ='Tabular'
        )    
        return aMessageDialog
    
    
        
    
    security.declarePrivate( 'fExceptionDialog_MoveNotSupported')
    def fExceptionDialog_MoveNotSupported( self, theModelDDvlPloneTool, theContextualElement):
        
        aMessageDialog =MessageDialog(
            title    = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'Move not supported','Move not supported'),
            message  = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'Object can not be moved: %s', 'Object can not be moved:- %s') % '/'.join( theContextualElement.getPhysicalPath()),
            action ='Tabular'
        )    
        return aMessageDialog
        
    
    
    
    security.declarePrivate( 'fExceptionDialog_CopyNotSupported')
    def fExceptionDialog_CopyNotSupported( self, theModelDDvlPloneTool, theContextualElement):
        
        aMessageDialog =MessageDialog(
            title    = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'Copy not supported','Move not supported'),
            message  = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'Object can not be copied: %s', 'Object can not be copied: %s') % '/'.join( theContextualElement.getPhysicalPath()),
            action ='Tabular'
        )    
        return aMessageDialog
    
        
    
    
    
    

    security.declarePrivate( 'fClipboardOperationAndElements')
    def fClipboardOperationAndElements( self,        
        theModelDDvlPloneTool            =None,
        theContextualElement             =None,):
        
        aRequest = theContextualElement.REQUEST
        if not aRequest:
            return ( 0, [], )
        
        if not aRequest.has_key(cClipboardCookieName):
            return ( 0, [], )
            
        aClipboard = aRequest[cClipboardCookieName]
        
        if aClipboard is None:
            return ( 0, [], )
             
        try:
            anOperation, someMonikerDatas = self.fClipboardDecode( aClipboard) # _cb_decode(cp)
        except:
            return ( 0, [], )

    
        someObjects = []
        anApplication = theContextualElement.getPhysicalRoot()
        for aMonikerData in someMonikerDatas:
            aMoniker= Moniker.loadMoniker( aMonikerData)
            anObject = None
            try:
                anObject = aMoniker.bind( anApplication)
            except:
                None
            if not ( anObject == None):
                someObjects.append( anObject)
            
        return ( anOperation, someObjects)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    security.declarePrivate( 'fObjectPaste')
    def fObjectPaste( self,
        theTimeProfilingResults     =None,
        theModelDDvlPloneTool       = None,
        theModelDDvlPloneTool_Retrieval= None,
        theModelDDvlPloneTool_Mutators= None,
        theContainerObject          =None, 
        theIsMoveOperation          =False,
        theMDDCopyTypeConfigs       =None, 
        thePloneCopyTypeConfigs     =None, 
        theMappingConfigs           =None, 
        theAdditionalParams         =None):

        aPasteReport = self.fNewVoidPasteReport()
        
    
        aClipboardOperation, someObjects = self.fClipboardOperationAndElements( theModelDDvlPloneTool, theContainerObject)
            
        someObjectsToPaste = someObjects[:]
        
        unIsMoveOperation = aClipboardOperation == 1
        
        unPasteReport = self.fPaste( 
            theTimeProfilingResults        = theTimeProfilingResults,
            theModelDDvlPloneTool          = theModelDDvlPloneTool,
            theModelDDvlPloneTool_Retrieval= theModelDDvlPloneTool_Retrieval,
            theModelDDvlPloneTool_Mutators = theModelDDvlPloneTool_Mutators,
            theContainerObject             = theContainerObject, 
            theObjectsToPaste              = someObjectsToPaste,
            theIsMoveOperation             = unIsMoveOperation,
            theMDDCopyTypeConfigs          = theMDDCopyTypeConfigs, 
            thePloneCopyTypeConfigs        = thePloneCopyTypeConfigs, 
            theMappingConfigs              = theMappingConfigs, 
            theAdditionalParams            = theAdditionalParams
        )
        
        return unPasteReport
        
        
        
    
    
        
        
        
    security.declarePrivate( 'fPaste')
    def fPaste( self,
        theTimeProfilingResults     =None,
        theModelDDvlPloneTool       = None,
        theModelDDvlPloneTool_Retrieval= None,
        theModelDDvlPloneTool_Mutators= None,
        theContainerObject          =None, 
        theObjectsToPaste           =[],
        theIsMoveOperation          =False,
        theMDDCopyTypeConfigs       =None, 
        thePloneCopyTypeConfigs     =None, 
        theMappingConfigs           =None, 
        theAdditionalParams         =None):
        """Paste into an element the elements previously copied (references held in the clipboard internet browser cookie), and all its contents, reproducing between the copied elements the relations between the original elements.        
        
        """
        
        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fPaste', theTimeProfilingResults)
                      
        try:
            unPasteReport = None
            try:      
                
                # ##############################################################################
                """Transaction Save point before import to get a clean view on the existing object network.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                unPasteContext = self.fNewVoidPasteContext()
                unPasteReport  = unPasteContext.get( 'report', {})
                
                
                
                # ##############################################################################
                """Check parameters.
                
                """      
                
                if ( theContainerObject == None):
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_MissingParameter_ContainerElement,
                    })
                    return unPasteReport
                unPasteContext[ 'container_object'] = theContainerObject
        
                
                if ( theObjectsToPaste == None) or ( len( theObjectsToPaste) < 1):
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_MissingParameter_ObjectsToPaste,
                    })
                    return unPasteReport
                
                
                
                unIsMoveOperation = ( theIsMoveOperation and True) or False
                
                unPasteContext[ 'is_move_operation'] = unIsMoveOperation
                
                someObjectsToPaste = []
                if not unIsMoveOperation:
                    someObjectsToPaste = theObjectsToPaste[:]
                    
                else:                    
                    for unObjectToPaste in theObjectsToPaste:
                        if not ( unObjectToPaste == None):
                            
                            if unObjectToPaste == theContainerObject:
                                continue
                            
                            unObjectToPasteParent = aq_parent( aq_inner( unObjectToPaste)) 
        
                            if not ( unObjectToPasteParent == None):
                                if not( unObjectToPasteParent == theContainerObject):
                                    someObjectsToPaste.append( unObjectToPaste)
                                    
                    if not someObjectsToPaste:
                        unPasteReport.update( { 
                            'success':      False,
                            'status':       cRefactorStatus_Ignored_Cut_Paste_SameSourceAndTarget_or_ObjectsPastedInSame_Container,
                        })
                        return unPasteReport
                
                unPasteContext[ 'objects_to_paste'] = someObjectsToPaste
                   
        
                if not theMDDCopyTypeConfigs:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_MissingParameter_MDDCopyTypeConfigs,
                    })
                    return unPasteReport
                unPasteContext[ 'mdd_copy_type_configs'] = theMDDCopyTypeConfigs
                
                somePloneCopyTypeConfigs = thePloneCopyTypeConfigs
                if not somePloneCopyTypeConfigs:
                    somePloneCopyTypeConfigs = {}
                unPasteContext[ 'plone_copy_type_configs'] = somePloneCopyTypeConfigs
        
                someMappingConfigs = theMappingConfigs
                if not someMappingConfigs:
                    someMappingConfigs = []
                unPasteContext[ 'mapping_configs'] = someMappingConfigs
    
                allCopyTypeConfigs = somePloneCopyTypeConfigs.copy()
                allCopyTypeConfigs.update( theMDDCopyTypeConfigs)
                unPasteContext[ 'all_copy_type_configs'] = allCopyTypeConfigs
                
                if not theModelDDvlPloneTool:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_MissingTool_ModelDDvlPloneTool,
                    })
                    return unPasteReport
                unPasteContext[ 'ModelDDvlPloneTool'] = theModelDDvlPloneTool
                
                if not theModelDDvlPloneTool_Retrieval:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_MissingTool_ModelDDvlPloneTool_Retrieval,
                    })
                    return unPasteReport
                unPasteContext[ 'ModelDDvlPloneTool_Retrieval'] = theModelDDvlPloneTool_Retrieval
                
                unCheckedPermissionsCache = theModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()
                unPasteContext[ 'checked_permissions_cache'] = unCheckedPermissionsCache
                
                if not theModelDDvlPloneTool_Mutators:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_MissingTool_ModelDDvlPloneTool_Mutators,
                    })
                    return unPasteReport
                unPasteContext[ 'ModelDDvlPloneTool_Mutators'] = theModelDDvlPloneTool_Mutators
                
                
                if theAdditionalParams:
                    unPasteContext[ 'additional_params'].update( theAdditionalParams)
                    
                
                # ##############################################################################
                """Retrieve original object result.
                
                """      
                unContainerObjecResult = self.fRetrieveContainer( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    thePasteContext             =unPasteContext,
                )
                
                if (not unContainerObjecResult) or ( unContainerObjecResult.get( 'object', None) == None):
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_Internal_NoContainerRetrieved,
                    })
                    return unPasteReport
        
                unAllowPaste = unContainerObjecResult.get( 'allow_paste', True)
                if not unAllowPaste:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_NotAllowedInElement,
                    })
                    return unPasteReport
                
                unContainerReadPermission = unContainerObjecResult.get( 'read_permission', False)
                if not unContainerReadPermission:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_Container_NotReadable,
                    })
                    return unPasteReport
                    
                unContainerWritePermission = unContainerObjecResult.get( 'write_permission', False)
                if not unContainerWritePermission:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_Container_NotWritable,
                    })
                    return unPasteReport
                    
                
                someSources = self.fRetrieveSourceElements( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    thePasteContext             =unPasteContext,
                    theCheckDeletePermission   =theIsMoveOperation,
                )
                
                if not someSources:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_Internal_NoSourcesRetrieved,
                    })
                    return unPasteReport
        
                
                
                
                unRefactor = MDDRefactor_Paste( 
                    theModelDDvlPloneTool,
                    theModelDDvlPloneTool_Retrieval,
                    theModelDDvlPloneTool_Mutators,
                    theIsMoveOperation,
                    someSources, 
                    theContainerObject, 
                    unContainerObjecResult, 
                    allCopyTypeConfigs, 
                    someMappingConfigs,
                    True, # theAllowMappings
                    MDDRefactor_Paste_Exception,
                    True, # theAllowPartialCopies
                    True, # theIgnorePartialLinksForMultiplicityOrDifferentOwner
                )  
                if ( not unRefactor) or not unRefactor.vInitialized:
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized,
                    })
                    return unPasteReport
    
                # ##############################################################################
                """Transaction Save point.
                
                """      
                ModelDDvlPloneTool_Transactions().fTransaction_Savepoint( theOptimistic=True)
                
                unHuboRefactorException  = False
                unHuboException  = False
                unRefactorResult = False
                try:
                    
                    try:
                        unRefactorResult = unRefactor.fRefactor()
                    
                    except MDDRefactor_Paste_Exception:
                        
                        unHuboRefactorException = True
                        
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                        
                        unInformeExcepcion = 'Exception during ModelDDvlPloneTool_Refactor::fPaste invoking MDDRefactor_Paste::fRefactor\n' 
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        unPasteReport[ 'exception'] = unInformeExcepcion
                                 
                        if cLogExceptions:
                            logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                        
                except:
                    unHuboException = True
                    raise
                    
                
                unPasteReport.update( {
                    'num_elements_expected':       unRefactor.vNumElementsExpected,
                    'num_mdd_elements_expected':   unRefactor.vNumMDDElementsExpected,
                    'num_plone_elements_expected': unRefactor.vNumPloneElementsExpected,
                    'num_attributes_expected':     unRefactor.vNumAttributesExpected,
                    'num_links_expected':          unRefactor.vNumLinksExpected,
                    'num_elements_pasted':         unRefactor.vNumElementsPasted,
                    'num_mdd_elements_pasted':     unRefactor.vNumMDDElementsPasted,
                    'num_plone_elements_pasted':   unRefactor.vNumPloneElementsPasted,
                    'num_attributes_pasted':       unRefactor.vNumAttributesPasted,
                    'num_links_pasted':            unRefactor.vNumLinksPasted,
                    'num_elements_failed':         unRefactor.vNumElementsFailed,
                    'num_mdd_elements_failed':     unRefactor.vNumMDDElementsFailed,
                    'num_plone_elements_failed':   unRefactor.vNumPloneElementsFailed,
                    'num_attributes_failed':       unRefactor.vNumAttributesFailed,
                    'num_links_failed':            unRefactor.vNumLinksFailed,
                    'num_elements_bypassed':       unRefactor.vNumElementsBypassed,
                    'num_mdd_elements_bypassed':   unRefactor.vNumMDDElementsBypassed,
                    'num_plone_elements_bypassed': unRefactor.vNumPloneElementsBypassed,
                    'num_attributes_bypassed':     unRefactor.vNumAttributesBypassed,
                    'num_links_bypassed':          unRefactor.vNumLinksBypassed,
                    'impacted_objects_UIDs':       unRefactor.vImpactedObjectUIDs,
                })
                unPasteReport[ 'error_reports'].extend( unRefactor.vErrorReports )
                        
                
                ModelDDvlPloneTool_Transactions().fTransaction_Commit()
                if cLogPasteResults:
                    logging.getLogger( 'ModelDDvlPlone').info( 'COMMIT: %s::fPaste\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unPasteReport, ])))
                    
            
                if ( not unHuboException) and ( not unHuboRefactorException) and unRefactorResult:
    
                    unPasteReport.update( { 
                         'success':      True,
                    })
                    
                    if cLogPasteResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'COMMITTED COMPLETED: %s::fPaste\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unPasteReport, ])))
                    
                else:
                    
                    unPasteReport.update( { 
                        'success':      False,
                        'status':       cRefactorStatus_Error_Paste_Internal_Refactor_Failed,
                    })
                    
                    if cLogPasteResults:
                        logging.getLogger( 'ModelDDvlPlone').info( 'COMMITTED WITH ERRORS during: %s::fPaste\n%s' % ( self.__class__.__name__, fPrettyPrint( [ unPasteReport, ])))
                    
                return unPasteReport
            
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = '\n'.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during ModelDDvlPloneTool_Refactor::fPaste\n' 
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                         
                if not unPasteReport:
                    unPasteReport = self.fNewVoidPasteReport()
                    
                anErrorReport = { 
                    'theclass': self.__class__.__name__, 
                    'method': u'fPaste', 
                    'status': unicode( 'Exception'),
                    'reason': unicode( 'Exception'),
                    'params': { 
                        'theTarget':          str( theContainerObject), 
                        'numElementsToPaste': unicode( str( len( theObjectsToPaste))),
                    }, 
                }
                    
                    
                unPasteReport[ 'error_reports'].append( anErrorReport)
                    
                unPasteReport.update( { 
                    'success':      False,
                    'status':       cRefactorStatus_Error_Paste_Exception,
                    'exception':    unInformeExcepcion,
                })
                    
                if cLogExceptions:
                    logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
                
                return unPasteReport
                        
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fPaste', theTimeProfilingResults)
            
        
    
    
   
    
    security.declarePrivate( 'fRetrieveSourceElements')
    def fRetrieveSourceElements( self,
        theTimeProfilingResults     =None,
        thePasteContext             =None,
        theCheckDeletePermission    =False):
        """Retrieve a tree of traversal information from each element to be pasted .
        
        """
    
        someSourcesResults = [ ]

        if not thePasteContext:
            return someSourcesResults
        
        someSourceObjects = thePasteContext.get( 'objects_to_paste', [])
        if ( someSourceObjects == None) or ( len( someSourceObjects) < 1):
            return someSourcesResults
        
        for unSourceObject in someSourceObjects:
            
            unSourceMetaType = unSourceObject.meta_type
            if unSourceMetaType:
            
                unSourceResult = self.fRetrieveSource_MDD(
                    theTimeProfilingResults,
                    thePasteContext,
                    unSourceObject,
                    theCheckDeletePermission,
                )
                if unSourceResult and not  ( unSourceResult.get( 'object', None) == None) and ( unSourceResult.get( 'read_permission', False) == True):
                    someSourcesResults.append( unSourceResult)
                    
        return someSourcesResults
    
                        
                        


    security.declarePrivate( 'fRetrieveSources_MDD')
    def fRetrieveSource_MDD( self,
        theTimeProfilingResults     =None,
        thePasteContext             =None,
        theSourceObject             =None,
        theCheckDeletePermission    =False):
        """
        
        """
    
        if not thePasteContext:
            return None
       
        if not theSourceObject:
            return None
       
        allCopyTypeConfigs = thePasteContext.get( 'all_copy_type_configs', {})
        if not allCopyTypeConfigs:
            return None
                        
        someAdditionalParams = thePasteContext.get(  'additional_params', None)
        
        aModelDDvlPloneTool_Retrieval = thePasteContext.get( 'ModelDDvlPloneTool_Retrieval', None)
        if not aModelDDvlPloneTool_Retrieval:
            return None
        
        unCheckedPermissionsCache = thePasteContext.get( 'checked_permissions_cache', None)
        
        unasWritePermissions = [ ]
        if theCheckDeletePermission:
            unasWritePermissions.append( 'delete')
        
        unElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
            theTimeProfilingResults     = theTimeProfilingResults,
            theElement                  = theSourceObject, 
            theParent                   = None,
            theParentTraversalName      = '',
            theTypeConfig               = None, 
            theAllTypeConfigs           = allCopyTypeConfigs, 
            theViewName                 = '', 
            theRetrievalExtents         = [ 'tree', ],
            theWritePermissions         = unasWritePermissions,
            theFeatureFilters           =None, 
            theInstanceFilters          =None,
            theTranslationsCaches       =None,
            theCheckedPermissionsCache  =unCheckedPermissionsCache,
            theAdditionalParams         =someAdditionalParams
        )
        if not unElementResult or not( unElementResult.get( 'object', None) == theSourceObject):
            return None
                    
    
        return unElementResult

   

   



   
    
    security.declarePrivate( 'fRetrieveContainer')
    def fRetrieveContainer( self,
        theTimeProfilingResults     =None,
        thePasteContext             =None):
        """Retrieve basic information from the target element into which to paste the elements in theObjectsToPaste.
        
        """
    
        aContainerResult = None

        if not thePasteContext:
            return aContainerResult
        
        unTargetObject = thePasteContext.get( 'container_object', None)
        if ( unTargetObject == None):
            return aContainerResult
        
        someMDDCopyTypeConfigs   = thePasteContext.get( 'mdd_copy_type_configs',   {})

        unTargetMetaType = unTargetObject.meta_type
        if unTargetMetaType:
        
            unTargetMDDTypeConfig = someMDDCopyTypeConfigs.get( unTargetMetaType, None)
            if unTargetMDDTypeConfig:
                
                aContainerResult = self.fRetrieveContainer_MDD(
                    theTimeProfilingResults,
                    thePasteContext,
                    unTargetObject,
                )
                if aContainerResult and not  ( aContainerResult.get( 'object', None) == None):
                    aContainerResult[ 'is_MDD']   = True
                    aContainerResult[ 'is_Plone'] = False
                else:
                    return None
                

                        
            if aContainerResult:
                aContainerReadPermission = aContainerResult.get( 'read_permission', False)
                if not aContainerReadPermission:
                    return None
                
                aContainerWritePermission = aContainerResult.get( 'write_permission', False)
                if not aContainerWritePermission:
                    return None

        return aContainerResult
    
                        
                        



    security.declarePrivate( 'fRetrieveContainer_MDD')
    def fRetrieveContainer_MDD( self,
        theTimeProfilingResults     =None,
        thePasteContext             =None,
        theTargetObject             =None):
        """
        
        """
        

        if not thePasteContext:
            return None
       
        if not theTargetObject:
            return None
       
        allCopyTypeConfigs = thePasteContext.get( 'all_copy_type_configs', {})
        if not allCopyTypeConfigs:
            return None
                        
        someAdditionalParams = thePasteContext.get(  'additional_params', None)
        
        aModelDDvlPloneTool_Retrieval = thePasteContext.get( 'ModelDDvlPloneTool_Retrieval', None)
        if not aModelDDvlPloneTool_Retrieval:
            return None
        
        unCheckedPermissionsCache = thePasteContext.get( 'checked_permissions_cache', None)
        
        unElementResult = aModelDDvlPloneTool_Retrieval.fRetrieveTypeConfig( 
            theTimeProfilingResults     = theTimeProfilingResults,
            theElement                  = theTargetObject, 
            theParent                   = None,
            theParentTraversalName      = '',
            theTypeConfig               = None, 
            theAllTypeConfigs           = allCopyTypeConfigs, 
            theViewName                 = '', 
            theRetrievalExtents         = [ 'traversals', ],
            theWritePermissions         =[ 'object', 'add', 'add_collection', 'aggregations', ],
            theFeatureFilters           =None, 
            theInstanceFilters          =None,
            theTranslationsCaches       =None,
            theCheckedPermissionsCache  =unCheckedPermissionsCache,
            theAdditionalParams         =someAdditionalParams
        )
        if not unElementResult or not( unElementResult.get( 'object', None) == theTargetObject):
            return None
                    
    
        return unElementResult
        
   

    
     