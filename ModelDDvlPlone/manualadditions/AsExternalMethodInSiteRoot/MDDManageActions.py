# -*- coding: utf-8 -*-
#
# File: MDDManageActions.py
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




import cgi 

import logging



from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport     import fMillisecondsNow








# ####################################
"""Request parameter names.

"""
cRqstParmName_NoCache      = 'theNoCache'
cRqstParmName_NoCacheCode  = 'theNoCacheCode'












# #######################################################################
"""MANAGE ACTIONS REQUESTED BY THE USER 

"""


def MDDManageActions(  theInteractionCtxt=None):
    """Main service for handling the actions requested by users for manipulation of the objects network, or the clipboard.

    Entry point invoked from a the MDDInteractionTabular external method.

    Must be registered as an External method as:
        Id            MDDManageActions
        Title         MDDManageActions
        Module name   MDDManageActions
        Function name MDDManageActions

    """

    
    if not theInteractionCtxt:
        return None
    

    # #################################################################
    """Get basic parameters from received interaction context.

    """
    aModelDDvlPloneTool = theInteractionCtxt.fGP( 'theModelDDvlPloneTool', None)
    aBrowsedElement     = theInteractionCtxt.fGP( 'theBrowsedElement', None) 
    aRequest            = theInteractionCtxt.fGP( 'theRequest', None)    
    anOutput            = theInteractionCtxt.fGP( 'output', None)    
    aPasteRequested     = theInteractionCtxt.fGP( 'thePasteRequested', False) 


       
    # #################################################################
    """Record time now

    """

    theInteractionCtxt.pSP( 'theActionsBeginTime', fMillisecondsNow())


    # #################################################################
    """Manage paste into the current element

    """
    if aPasteRequested:
        _MDDManageActions_Paste( theInteractionCtxt)




    # #################################################################
    """Manage actions on an element's aggregation or relationship

    """
    aRequestForm = aRequest.get( 'form', None)
    if aRequestForm:
        aGroupAction = aRequestForm.get( 'theGroupAction', None)
        if aGroupAction:
            aReferenceFieldName = aRequestForm.get( 'theReferenceFieldName', None) 
            someGroupUIDs       = aRequestForm.get( 'theUIDs', []) 

            _MDDManageActions_GroupActions( theInteractionCtxt, aGroupAction, aReferenceFieldName, someGroupUIDs)



    # #################################################################
    """Manage clear clipboard

    """
    aClearClipboard = aRequest.get( 'theClearClipboard', None)
    if aClearClipboard:
        _MDDManageActions_ClearClipboard( theInteractionCtxt)


    # #################################################################
    """Manage reorder contained (MDD aware) elements

    """
    aTraversalName  = aRequest.get( 'theTraversalName', None)
    aMovedElementID = aRequest.get( 'theMovedElementID', None)
    aMoveDirection  = aRequest.get( 'theMoveDirection', None)        
    if aTraversalName and aMovedElementID and aMoveDirection:
        _MDDManageActions_MoveElementos( theInteractionCtxt, aTraversalName, aMovedElementID, aMoveDirection)


    # #################################################################
    """Manage reorder referenced elements

    """
    aMovedReferenceUID = aRequest.get( 'theMovedReferenceUID', None)
    if aTraversalName and aMovedReferenceUID and aMoveDirection:
        _MDDManageActions_MoveReferencias( theInteractionCtxt, aTraversalName, aMovedReferenceUID, aMoveDirection)




    # #################################################################
    """Manage reorder contained Plone elements

    """
    aMovedObjectUID = aRequest.get( 'theMovedObjectUID', None)
    if aTraversalName and aMovedObjectUID and aMoveDirection:
        _MDDManageActions_MoveElementosPlone( theInteractionCtxt, aTraversalName, aMovedObjectUID, aMoveDirection)


    # #################################################################
    """Record time now

    """
    theInteractionCtxt.pSP( 'theActionsEndTime', fMillisecondsNow())

    return None











# #######################################################################
""" ACTION METHODS.

"""




def _MDDManageActions_ClearClipboard( theInteractionCtxt):

    if not theInteractionCtxt:
        return None

    aContextualElement = theInteractionCtxt.fGP( 'theBrowsedElement', None)
    if aContextualElement == None:
        return None

    aModelDDvlPloneTool = theInteractionCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None

    someAdditionalParms = theInteractionCtxt.fGP( 'theAdditionalParms', None)

    aBeginTime  = fMillisecondsNow()

    aReport = aModelDDvlPloneTool.pClearClipboard( 
        theTimeProfilingResults     =None,
        theContextualElement        =aContextualElement, 
        theAdditionalParams         =someAdditionalParms,
    )

    anEndTime  = fMillisecondsNow()
 
    anActionResult= {
        'action':       'ClearClipboard',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aReport,
    }
    theInteractionCtxt.pAppendActionResult( anActionResult)
        
    return None






def _MDDManageActions_Paste( theInteractionCtxt):

    if not theInteractionCtxt:
        return None

    aContextualElement = theInteractionCtxt.fGP( 'theBrowsedElement', None)
    if aContextualElement == None:
        return None

    aModelDDvlPloneTool = theInteractionCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None

    someAdditionalParms = theInteractionCtxt.fGP( 'theAdditionalParms', None)

    aBeginTime  = fMillisecondsNow()

    aPasteReport = aModelDDvlPloneTool.fObjectPaste( 
        theTimeProfilingResults     =None,
        theContainerObject          =aContextualElement, 
        theAdditionalParams         =someAdditionalParms,
    )

    anEndTime  = fMillisecondsNow()

    anActionResult= {
        'action':       'Paste',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aPasteReport,
    }
        
    theInteractionCtxt.pAppendActionResult( anActionResult)

    return None







def _MDDManageActions_GroupActions( theInteractionCtxt):

    if not theInteractionCtxt:
        return None

    aContextualElement = theInteractionCtxt.fGP( 'theBrowsedElement', None)
    if aContextualElement == None:
        return None

    aModelDDvlPloneTool = theInteractionCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None

    someAdditionalParms = theInteractionCtxt.fGP( 'theAdditionalParms', None)
    
    aRequest            = theInteractionCtxt.fGP( 'theRequest', None)    

    aRequestForm = aRequest.get( 'form', None)
    if not aRequestForm:
        return None

    aGroupAction = aRequestForm.get( 'theGroupAction', None)
    if not aGroupAction:
        return None

    aReferenceFieldName = aRequestForm.get( 'theReferenceFieldName', None) 
    someGroupUIDs       = aRequestForm.get( 'theUIDs', []) 

    if not someGroupUIDs:
        return None
    
    aBeginTime  = fMillisecondsNow()

    aGroupActionReport   = aModelDDvlPloneTool.fGroupAction( 
        theTimeProfilingResults     =None,
        theContainerObject          =aContextualElement, 
        theGroupAction              =aGroupAction,
        theGroupUIDs                =someGroupUIDs,
        theReferenceFieldName       =aReferenceFieldName,
        theAdditionalParams         =someAdditionalParms,
    )

    anEndTime  = fMillisecondsNow()

    anActionResult= {
        'action':       aGroupAction,
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aGroupActionReport,
    }
    theInteractionCtxt.pAppendActionResult( anActionResult)
        

    return None











def _MDDManageActions_MoveElementos( theInteractionCtxt):

    if not theInteractionCtxt:
        return None

    aContextualElement = theInteractionCtxt.fGP( 'theBrowsedElement', None)
    if aContextualElement == None:
        return None

    aModelDDvlPloneTool = theInteractionCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None

    someAdditionalParms = theInteractionCtxt.fGP( 'theAdditionalParms', None)

    aRequest        = theInteractionCtxt.fGP( 'theRequest', None)    

    aTraversalName  = aRequest.get( 'theTraversalName', None)
    if not aTraversalName:
        return None

    aMovedElementID = aRequest.get( 'theMovedElementID', None)
    if not aMovedElementID:
        return None

    aMoveDirection  = aRequest.get( 'theMoveDirection', None)        
    if not aMoveDirection:
        return None


    aBeginTime  = fMillisecondsNow()

    aMoveResult = aModelDDvlPloneTool.fMoveSubObject( 
        theTimeProfilingResults     =None,
        theContainerElement         =aContextualElement,  
        theTraversalName            =aTraversalName, 
        theMovedObjectId            =aMovedElementID, 
        theMoveDirection            =aMoveDirection, 
        theAdditionalParams         =someAdditionalParms,
    )

    anEndTime  = fMillisecondsNow()


    anActionResult= {
        'action':       'Move',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveResult,
    }
        
    theInteractionCtxt.pAppendActionResult( anActionResult)

    return None







def _MDDManageActions_MoveReferencias( theRdCtxt):

    if not theInteractionCtxt:
        return None

    aContextualElement = theInteractionCtxt.fGP( 'theBrowsedElement', None)
    if aContextualElement == None:
        return None

    aModelDDvlPloneTool = theInteractionCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None

    someAdditionalParms = theInteractionCtxt.fGP( 'theAdditionalParms', None)

    aRequest        = theInteractionCtxt.fGP( 'theRequest', None)    

    aTraversalName  = aRequest.get( 'theTraversalName', None)
    if not aTraversalName:
        return None

    aMovedReferenceUID = aRequest.get( 'theMovedReferenceUID', None)
    if not aMovedReferenceUID:
        return None

    aMoveDirection  = aRequest.get( 'theMoveDirection', None)        
    if not aMoveDirection:
        return None


    aBeginTime  = fMillisecondsNow()

    aMoveReferenceResult = aModelDDvlPloneTool.pMoveReferencedObject( 
        theTimeProfilingResults     =None,
        theSourceElement            =aContextualElement,  
        theReferenceFieldName       =aTraversalName, 
        theMovedReferenceUID        =aMovedReferenceUID, 
        theMoveDirection            =aMoveDirection, 
        theAdditionalParams         =someAdditionalParms,
    )

    anEndTime  = fMillisecondsNow()

    anActionResult= {
        'action':       'MoveReference',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveResult,
    }
    theInteractionCtxt.pAppendActionResult( anActionResult)
        
    return None






def _MDDManageActions_MoveElementosPlone( theRdCtxt):


    if not theInteractionCtxt:
        return None

    aContextualElement = theInteractionCtxt.fGP( 'theBrowsedElement', None)
    if aContextualElement == None:
        return None

    aModelDDvlPloneTool = theInteractionCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None

    someAdditionalParms = theInteractionCtxt.fGP( 'theAdditionalParms', None)

    aRequest        = theInteractionCtxt.fGP( 'theRequest', None)    

    aTraversalName  = aRequest.get( 'theTraversalName', None)
    if not aTraversalName:
        return None

    aMovedObjectUID = aRequest.get( 'theMovedObjectUID', None)
    if not aMovedObjectUID:
        return None

    aMoveDirection  = aRequest.get( 'theMoveDirection', None)        
    if not aMoveDirection:
        return None



    aBeginTime  = fMillisecondsNow()

    aMoveReferenceResult = aModelDDvlPloneTool.fMoveSubObjectPlone( 
        theTimeProfilingResults     =None,
        theContainerElement         =aContextualElement,  
        theTraversalName            =aTraversalName, 
        theMovedObjectUID           =aMovedObjectUID, 
        theMoveDirection            =aMoveDirection, 
        theAdditionalParams         =someAdditionalParms,
    )

    anEndTime  = fMillisecondsNow()

    anActionResult= {
        'action':       'MovePlone',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveResult,
    }
    theInteractionCtxt.pAppendActionResult( anActionResult)
        
    return None





