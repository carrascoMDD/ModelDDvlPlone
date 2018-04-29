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

from OFS             import Moniker        
from OFS.CopySupport import CopyError

from marshal import loads, dumps
from urllib import quote, unquote
from zlib import compress, decompress

from AccessControl import ClassSecurityInfo

from App.Dialogs import MessageDialog

from webdav.Lockable import ResourceLockedError


from ModelDDvlPloneTool_Refactor_Constants import *

from MDD_RefactorComponents import MDDRefactor_Paste

cLogExceptions = True



    
# ######################################################
# 
# ######################################################
    

class ModelDDvlPloneTool_Refactor:
    """
    """
    security = ClassSecurityInfo()

    
    
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
            'ModelDDvlPloneTool_Retrieval': None,
            'ModelDDvlPloneTool_Mutators': None,
            'checked_permissions_cache': None,
            'mdd_copy_type_configs':    {},
            'plone_copy_type_configs':  {},
            'all_copy_type_configs':    {},
            'mapping_configs':          [],
            'additional_params':        self.fTraversalSourcesAdditionalParams(),
            'report':                   self.fNewVoidPasteReport(),
            #'source_frames':            [ ],
            #'source_elements':          [ ],
            #'source_elements_by_UID':   { },
            #'source_stack':             [ ],
            #'target_elements':          [ ],
            #'target_elements_by_UID':   { },
            #'target_stack':             [ ],
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
    
                if not unElemento.cb_isMoveable():
                    raise CopyError, self.fExceptionDialog_MoveNotSupported( theModelDDvlPloneTool, theContainerObject) 
                
                unMoniker = Moniker.Moniker( unElemento)
                
                unosMonikers.append( unMoniker.dump())
                
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
            aResponse.setCookie('__cp', unClipBoardCookieContent, path='%s' % self.fPathForCookie( aRequest))
        aRequest['__cp'] = unClipBoardCookieContent
    
        return True
        
        
    
    
    
    
    
        
    
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
        
    
    
    
    security.declarePrivate( 'fExceptionDialog_NoItemsSpecified')
    def fExceptionDialog_NoItemsSpecified( self, theModelDDvlPloneTool, theContextualElement):
        
        aMessageDialog =MessageDialog(
            title    = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'No items specified','No items specified'),
            message  = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'You must select one or more items to perform this operation.', 'You must select one or more items to perform this operation.'),
            action ='Tabular'
        )    
        return aMessageDialog
    
    
    
    
    security.declarePrivate( 'fExceptionDialog_MoveNotSupported')
    def fExceptionDialog_MoveNotSupported( self, theModelDDvlPloneTool, theContextualElement):
        
        aMessageDialog =MessageDialog(
            title    = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'Move not supported','Move not supported'),
            message  = theModelDDvlPloneTool.fTranslateI18N( theContextualElement, 'plone', 'Object can not be moved: %s', 'Object can not be moved: %s') % '/'.join( theContextualElement.getPhysicalPath()),
            action ='Tabular'
        )    
        return aMessageDialog
        

    # From Zope/lib/python/OFS/CopySupport.py  class CopyContainer
    #
    #def manage_cutObjects(self, ids=None, REQUEST=None):
        #"""Put a reference to the objects named in ids in the clip board"""
        #if ids is None and REQUEST is not None:
            #return eNoItemsSpecified
        #elif ids is None:
            #raise ValueError, 'ids must be specified'

        #if type(ids) is type(''):
            #ids=[ids]
        #oblist=[]
        #for id in ids:
            #ob=self._getOb(id)

            #if ob.wl_isLocked():
                #raise ResourceLockedError, 'Object "%s" is locked via WebDAV' % ob.getId()

            #if not ob.cb_isMoveable():
                #raise CopyError, eNotSupported % escape(id)
            #m=Moniker.Moniker(ob)
            #oblist.append(m.dump())
        #cp=(1, oblist)
        #cp=_cb_encode(cp)
        #if REQUEST is not None:
            #resp=REQUEST['RESPONSE']
            #resp.setCookie('__cp', cp, path='%s' % cookie_path(REQUEST))
            #REQUEST['__cp'] = cp
            #return self.manage_main(self, REQUEST)
        #return cp
        
        
        
        
        
    security.declarePrivate( 'fPaste')
    def fPaste( self,
        theTimeProfilingResults     =None,
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
        
        unPasteReport = None
        try:      
            unPasteContext = self.fNewVoidPasteContext()
            unPasteReport  = unPasteContext.get( 'report', {})
            
            unPasteContext[ 'is_move_operation'] = ( theIsMoveOperation and True) or False
             
            if ( theContainerObject == None):
                unPasteReport.update( { 
                    'success':      False,
                    'status':       cRefactorStatus_Error_Paste_MissingParameter_ContainerElement,
                })
                return unRefactorReport
            
                
            unPasteContext[ 'container_object'] = theContainerObject
    
            
            
            if ( theObjectsToPaste == None) or ( len( theObjectsToPaste) < 1):
                unPasteReport.update( { 
                    'success':      False,
                    'status':       cRefactorStatus_Error_Paste_MissingParameter_ObjectsToPaste,
                })
                return unRefactorReport
            unPasteContext[ 'objects_to_paste'] = theObjectsToPaste
            
    
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
                return unRefactorReport
            
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
                theIsMoveOperation,
                someSources, 
                theContainerObject, 
                unContainerObjecResult, 
                allCopyTypeConfigs, 
                someMappingConfigs,
            )  
            if ( not unRefactor) or not unRefactor.vInitialized:
                unPasteReport.update( { 
                    'success':      False,
                    'status':       cRefactorStatus_Error_Paste_Internal_Refactor_NotInitialized,
                })
                return unPasteReport
                
            unRefactorResult = unRefactor.fRefactor()
            
            if unRefactorResult:
                unPasteReport.update( { 
                     'success':      True,
                })
            else:
                unPasteReport.update( { 
                    'success':      False,
                    'status':       cRefactorStatus_Error_Paste_Internal_Refactor_Failed,
                })
                
            
            return unPasteReport
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during fPaste\n' 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            if not unPasteReport:
                unPasteReport = { }
                
            unPasteReport.update( { 
                'success':      False,
                'status':       cRefactorStatus_Error_Paste_Exception,
                'exception':    unInformeExcepcion,
            })
                
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            return unPasteReport
                    
        return { 'success': False, }
    
    
    
   
    
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
        
        try:
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
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during fPaste fRetrieveSource_MDD\n' 
            unInformeExcepcion += 'source object %s\n' % str( theSourceObject) 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            return None
                    
        return None    
    

   

   



   
    
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
        
        try:
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
        
        except:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during fPaste fRetrieveContainer_MDD\n' 
            unInformeExcepcion += 'source object %s\n' % str( theTargetObject) 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   
                     
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            return None
                    
        return None    
    

   

    
     