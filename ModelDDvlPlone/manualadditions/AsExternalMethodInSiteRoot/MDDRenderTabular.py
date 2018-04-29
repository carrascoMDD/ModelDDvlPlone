# -*- coding: utf-8 -*-
#
# File: MDDRenderTabular.py
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


from codecs                 import lookup           as CODECS_Lookup
from codecs                 import EncodedFile      as CODECS_EncodedFile


from StringIO import StringIO


from Products.CMFCore.utils import getToolByName

cParamsAccess_KeyNotFound_Sentinel = object()

cClasesFilas = [ 'odd','even',]

cNoValueBGColor = 'silver'


# #######################################################################
""" ACTION AND RENDERING CONTEXT CLASS.

"""



        

# #######################################################################
""" PUBLIC VIEW METHOD.

"""
            

    
def MDDView_Tabular( 
    theModelDDvlPloneTool,
    thePerformanceAnalysis  ={},
    theBrowsedElement       =None, 
    theTraversalName        = '',
    theRelationCursorName   = '',
    theCurrentElementUID    = '',
    theRequest              =None, 
    thePasteRequested       =False,
    theGroupAction          ='',
    theUIDs                 =[],
    theMovedElementID       = '',
    theMoveDirection        = '',
    theTranslationsCache    =None,
    thePermissionsCache     =None, 
    theRolesCache           =None,
    theParentExecutionRecord=None,
    theAdditionalParms      ={},):
    """Main service for rendering tabular views for manipulation of the objects network.
    
    Entry point invoked from a template.
    """

        
    if not theModelDDvlPloneTool:
        return pEmptyPageContents(  
            theBrowsedElement, 
            mfTranslateI18N( 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theModelDDvlPloneTool',
            None
        )
     
    if theBrowsedElement == None:
        return pEmptyPageContents(  
            theBrowsedElement, 
            mfTranslateI18N( 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theBrowsedElement',
            None
        )
    if not theRequest:
        return pEmptyPageContents(  
            theBrowsedElement, 
            mfTranslateI18N( 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theRequest',
            None
        )
     
 
       
    # #################################################################
    """Initialize root view context structure. Initialize output streaming. Initialize caches if not supplied by service caller

    """
    anOutput = StringIO( u'')
    aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theBrowsedElement)
    
    aRdCtxt = theModelDDvlPloneTool.fNewRenderContext( 
        theBrowsedElement,
        {
            'theBeginTime':                 theModelDDvlPloneTool.fMillisecondsNow(),
            'theEndTime':                   None,
            'theActionsBeginTime':          None,
            'theActionsEndTime':            None,
            'theRetrievalBeginTime':        None,
            'theRetrievalEndTime':          None,
            'theRenderBeginTime':           None,
            'theRenderEndTime':             None,
            
            'theModelDDvlPloneTool':        theModelDDvlPloneTool,
            'thePerformanceAnalysis':       thePerformanceAnalysis,
            'theBrowsedElement':            theBrowsedElement,
            'theTraversalName':             theTraversalName,
            'theRelationCursorName':        theRelationCursorName,
            'theCurrentElementUID':         theCurrentElementUID,
            
            'theRequest':                   theRequest,
            'thePasteRequested':            thePasteRequested,
            'theGroupAction':               theGroupAction,
            'theUIDs':                      theUIDs,
            'theMovedElementID':            theMovedElementID,
            'theMoveDirection':             theMoveDirection,
    
            'output':                       anOutput,
            'pO':                           lambda theString: anOutput.write( theString),
            'pOL':                          lambda theString: anOutput.write( '%s\n' % theString),
            'pOS':                          lambda theString: anOutput.write( '%s\n' % ''.join( [ unaLine.strip() for unaLine in theString.splitlines()])),      
            
            'theMetaTranslationsCaches':    (( theTranslationsCache == None) and aModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches())      or theTranslationsCache,
            'thePermissionsCache':          (( thePermissionsCache == None)  and aModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()) or thePermissionsCache,
            'theRolesCache':                (( theRolesCache == None)        and aModelDDvlPloneTool_Retrieval.fCreateRolesCache())              or theRolesCache,
            'theUITranslations':            { },
        },
    )

    
    
    

    # #################################################################
    """Manage actions requested, prior to retrieving information and rendering

    """
    aRdCtxt.pSP( 'theActionsBeginTime', theModelDDvlPloneTool.fMillisecondsNow(),)   
    
    _MDDManageActions_Tabular( aRdCtxt)
    
    aRdCtxt.pSP( 'theActionsEndTime', theModelDDvlPloneTool.fMillisecondsNow(),)      
    
    
    
    
    
    # #################################################################
    """Retrieve the information from the element, contents and related, to render the view.
    
    """
    aRdCtxt.pSP( 'theRetrievalBeginTime', theModelDDvlPloneTool.fMillisecondsNow(),)   

    _MDDRetrieveInfo_Tabular( aRdCtxt)
    
    aRdCtxt.pSP( 'theRetrievalEndTime', theModelDDvlPloneTool.fMillisecondsNow(),)      
    
    
    
    
    
    # #################################################################
    """Render the view.
    
    """
    aRdCtxt.pSP( 'theRenderBeginTime', theModelDDvlPloneTool.fMillisecondsNow(),) 
    
    _MDDInitUITranslations(            aRdCtxt, cDomainsStringsAndDefaults)

    _MDDRender_ActionsResults_Tabular( aRdCtxt)

    if theRelationCursorName:
        _MDDRender_TabularCursor(    aRdCtxt)
    else:    
        _MDDRender_Tabular(            aRdCtxt)
    
    aRdCtxt.pSP( 'theRenderEndTime', theModelDDvlPloneTool.fMillisecondsNow(),) 
    
    
    aRdCtxt.pSP( 'theEndTime', theModelDDvlPloneTool.fMillisecondsNow())
    
    
    
    
    
    # #################################################################
    """Append profiling information, if so configured.
    
    """
    
    _MDDRender_Tabular_Profiling(      aRdCtxt)
        
    
    return anOutput.getvalue()
    

     
        

        
# #######################################################################
""" ACTION METHODS.

"""
    
     
def _MDDManageActions_Tabular( theRdCtxt):
    
    if theRdCtxt.fGP( 'thePasteRequested', False):
        _MDDManageActions_Tabular_Paste(        theRdCtxt)
    
    if theRdCtxt.fGP( 'theGroupAction',    False):
        _MDDManageActions_Tabular_GroupActions( theRdCtxt)
        
    _MDDManageActions_Tabular_Move(         theRdCtxt)
    
    return None



    
    
    
    
def _MDDManageActions_Tabular_Paste( theRdCtxt):
    
    if not theRdCtxt.fGP( 'thePasteRequested', False):
        return None

    aContainerObject = theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aBeginTime  = here.ModelDDvlPlone_tool.fMillisecondsNow()
    
    aPasteReport = here.ModelDDvlPlone_tool.fObjectPaste( 
        theTimeProfilingResults =None,
        theContainerObject      =aContainerObject, 
        theAdditionalParams     =None,
    )
    
    anEndTime  = here.ModelDDvlPlone_tool.fMillisecondsNow()
    
    theRdCtxt.pAppendActionResult( {
        'action':       'Paste',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aPasteReport,
    })
        
    return None
        
    





    
def _MDDManageActions_Tabular_GroupActions( theRdCtxt):

    aGroupAction         = theRdCtxt.fGP( 'theGroupAction', '')
    if not aGroupAction:
        return None
    
    someGroupUIDs        = theRdCtxt.fGP( 'theUIDs', [])
    if not someGroupUIDs:
        return None
    
    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aGroupActionReport   = here.ModelDDvlPlone_tool.fGroupAction( 
        theTimeProfilingResults =None,
        theContainerObject      =aContainerObject, 
        theGroupAction          =pGroupAction,
        theGroupUIDs            =pGroupUIDs,
        theAdditionalParams     =None, 
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    theRdCtxt.pAppendActionResult( {
        'action':       aGroupAction,
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aGroupActionReport,
    })
        
    return None

    
    
    
    
    
    
def _MDDManageActions_Tabular_Move( theRdCtxt):
    
    _MDDManageActions_Tabular_MoveElementos(      theRdCtxt)
    
    _MDDManageActions_Tabular_MoveReferencias(    theRdCtxt)
   
    _MDDManageActions_Tabular_MoveElementosPlone( theRdCtxt)
         
    return None





  
def _MDDManageActions_Tabular_MoveElementos( theRdCtxt):
    
    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aTraversalName =       theRdCtxt.fGP( 'theTraversalName', '')
    if not aTraversalName:
        return None
   
    aMovedElementID =      theRdCtxt.fGP( 'theMovedElementID', '')
    if not aMovedElementID:
        return None
  
    aMoveDirection =       theRdCtxt.fGP( 'theMoveDirection', '')
    if not aMoveDirection:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aMoveResult = aModelDDvlPloneTool.fMoveSubObject( 
        theTimeProfilingResults =None,
        theContainerElement     =aContainerObject,  
        theTraversalName        =aTraversalName, 
        theMovedObjectId        =aMovedElementID, 
        theMoveDirection        =aMoveDirection, 
        theAdditionalParams     =None,
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pAppendActionResult( {
        'action':       'Move',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveResult,
    })

    return None




        
      
   
def _MDDManageActions_Tabular_MoveReferencias( theRdCtxt):
    
    aContainerObject =      theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None

    aTraversalName =        theRdCtxt.fGP( 'theTraversalName', '')
    if not aTraversalName:
        return None
   
    aMovedReferenceUID =    theRdCtxt.fGP( 'theMovedReferenceUID', '')
    if not aMovedReferenceUID:
        return None
  
    aMoveDirection =        theRdCtxt.fGP( 'theMoveDirection', '')
    if not aMoveDirection:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aMoveReferenceResult = aModelDDvlPloneTool.pMoveReferencedObject( 
        theTimeProfilingResults =None,
        theSourceElement        =aContainerObject,  
        theReferenceFieldName   =aTraversalName, 
        theMovedReferenceUID    =aMovedReferenceUID, 
        theMoveDirection        =aMoveDirection, 
        theAdditionalParams     =None,
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pAppendActionResult( {
        'action':       'MoveReference',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveReferenceResult,
    })

    return None


                


   
def _MDDManageActions_Tabular_MoveElementosPlone( theRdCtxt):
    
    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None

    
    aTraversalName =       theRdCtxt.fGP( 'theTraversalName', '')
    if not aTraversalName:
        return None
   
    aMovedObjectUID =      theRdCtxt.fGP( 'theMovedObjectUID', '')
    if not aMovedObjectUID:
        return None
  
    aMoveDirection =       theRdCtxt.fGP( 'theMoveDirection', '')
    if not aMoveDirection:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aMoveReferenceResult = aModelDDvlPloneTool.pMoveReferencedObject( 
        theTimeProfilingResults =None,
        theContainerElement     =aContainerObject,  
        theReferenceFieldName   =aTraversalName, 
        theMovedObjectUID       =aMovedObjectUID, 
        theMoveDirection        =aMoveDirection, 
        theAdditionalParams     =None,
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pAppendActionResult( {
        'action':       'MoveReference',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
        'report':       aMoveReferenceResult,
    })

    return None


                










# #######################################################################
""" RETRIEVAL METHOD.

"""
    
     
def _MDDRetrieveInfo_Tabular( theRdCtxt):
    
    
    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    aBeginTime  = aModelDDvlPloneTool.fMillisecondsNow()
    
    aSRES = aModelDDvlPloneTool.fRetrieveTypeConfig( 
        theTimeProfilingResults     =None,
        theElement                  =aContainerObject, 
        theParent                   =None,
        theParentTraversalName      ='',
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='Tabular', 
        theRetrievalExtents         =[ 'traversals', 'owner', 'cursor', 'extra_links',],
        theWritePermissions         =[ 'object', 'ggregations', 'relations', 'add', 'delete', 'add_collection', ],
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None
    )
    
    anEndTime  = aModelDDvlPloneTool.fMillisecondsNow()
       
    theRdCtxt.pSP( 'SRES', aSRES)
    
       
    theRdCtxt.pAppendRetrievalResult( {
        'subject':      'SRES',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
    })

    return None

















# #######################################################################
""" RENDERING METHODS.

"""



def _MDDInitUITranslations( theRdCtxt, theDomainsStringsAndDefaults):
    """Preload some translations to use during rendering.
    
    """
    
    aContainerObject = theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return None
    
    aTRs = theRdCtxt.fGP( 'theUITranslations', {})

    aModelDDvlPloneTool = theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    aModelDDvlPloneTool.fTranslateI18NManyIntoDict( aContainerObject, cDomainsStringsAndDefaults, aTRs)
        
    return None

    

    
    

        
        
     
def _MDDRender_Tabular_Profiling( theRdCtxt):
    """Append profiling information, if so configured.
    
    """
    
    if theRdCtxt.fGP( 'thePerformanceAnalysis', {}).get( 'processing_times', False) or theRdCtxt.fGP( 'thePerformanceAnalysis', {}).get( 'retrieval_times', False):
        
        aDuration = '?'
        if theRdCtxt.fGP( 'theEndTime', 0) and theRdCtxt.fGP( 'theBeginTime', 0):
            aDuration  = str( theRdCtxt.fGP( 'theEndTime', 0) - theRdCtxt.fGP( 'theBeginTime', 0))

        anActionsDuration = '?'
        if theRdCtxt.fGP( 'theActionsEndTime', 0) and theRdCtxt.fGP( 'theActionsBeginTime', 0):
            anActionsDuration  = str( theRdCtxt.fGP( 'theActionsEndTime', 0) - theRdCtxt.fGP( 'theActionsBeginTime', 0))

        aRetrievalDuration = '?'
        if theRdCtxt.fGP( 'theRetrievalEndTime', 0) and theRdCtxt.fGP( 'theRetrievalBeginTime', 0):
            aRetrievalDuration  = str( theRdCtxt.fGP( 'theRetrievalEndTime', 0) - theRdCtxt.fGP( 'theRetrievalBeginTime', 0))
            
        aRenderDuration = '?'
        if theRdCtxt.fGP( 'theRenderEndTime', 0) and theRdCtxt.fGP( 'theRenderBeginTime', 0):
            aRenderDuration  = str( theRdCtxt.fGP( 'theRenderEndTime', 0) - theRdCtxt.fGP( 'theRenderBeginTime', 0))
    
             
        theRdCtxt.pOS("""
        <br/>
        <table cellspacing="2" cellpadding="2" frame="void">
            <thead>
                <tr>
                    <th>
                        Phase
                    </th>
                    <th>
                        Duration
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        Total
                    </td>
                    <td align="right" >
                        %(Duration)s
                    </td>
                </tr>
                <tr>
                    <td>
                        Actions
                    </td>
                    <td align="right" >
                        %(Actions_Duration)s
                    </td>
                </tr>
                <tr>
                    <td>
                        Retrieval
                    </td>
                    <td align="right" >
                        %(Retrieval_Duration)s
                    </td>
                </tr>
                <tr>
                    <td>
                        Render
                    </td>
                    <td align="right" >
                        %(Render_Duration)s
                    </td>
                </tr>
            <tbody>
        </table>
        <br/>
        """ % {
            'Duration':            aDuration,
            'Actions_Duration':    anActionsDuration,
            'Retrieval_Duration':  aRetrievalDuration,
            'Render_Duration':     aRenderDuration,
        })
                
    return None



 




def _MDDRender_TabularCursor( theRdCtxt):
    """Render a tabular view with the header for an element and the detail of one of its related elements.
    
    """
    return None



    
         


def _MDDRender_Tabular( theRdCtxt):
    """Render a tabular view on an object.
    
    """
        
    # #################################################################
    """Cache some translations to be used in the rendering below

    """

   
    # #################################################################
    """Open Page
    
    """
    theRdCtxt.pOS( u"""     
                    
        <!-- #################################################################
        PAGE WITH CONTENT
        ################################################################# -->
    """)
        
    
    _MDDRender_Tabular_Cabecera(                theRdCtxt)
    
    _MDDRender_Tabular_Values(                  theRdCtxt)
    
    _MDDRender_Tabular_Texts(                   theRdCtxt)
    
    _MDDRender_Tabular_CustomPresentationViews( theRdCtxt)
    
    _MDDRender_Tabular_Traversals(  theRdCtxt)
    
    #_MDDRender_Tabular_GenericReferences(  theRdCtxt)
    
    #_MDDRender_Tabular_Plone(  theRdCtxt)
    
    return None





    
def _MDDRender_ActionsResults_Tabular( theRdCtxt):
    
    aTRs   = theRdCtxt.fGP( 'theUITranslations', {})
    someActionsResults = theRdCtxt.fActionResults()

    for anActionResult in someActionsResults:
        anAction = anActionResult.get( 'action', '')
        if anAction:
            
            anActionReport = anActionResult.get( 'report', {})
                
            if anAction == 'Copy':
                if anActionReport:
                    theRdCtxt.pOS("""
                    <div class="portalMessage" tal:content=" =  u'%s %d'/>
                    """ % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_NumElementsCopied'), 
                        anActionReport,
                    ))
                else:
                    theRdCtxt.pOS("""
                    <div class="portalMessage" tal:content=" =  u'%s'/>
                    """ % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_No_items_copied'), 
                        anActionReport,
                    ))
                   
            
            if anAction == 'Cut':
                if anActionReport:
                    theRdCtxt.pOS("""
                    <div class="portalMessage" tal:content=" =  u'%s %d' % ( aTRs( 'ModelDDvlPlone_NumElementsCut',), anActionReport, )" />
                    <div class="portalMessage" tal:content=" =  u'%s %d'/>
                    """ % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_NumElementsCut'), 
                        anActionReport,
                    ))
                else:
                    theRdCtxt.pOS("""
                    <div class="portalMessage" tal:content=" =  u'%s'/>
                    """ % ( 
                        theRdCtxt.fUITr( 'ModelDDvlPlone_No_items_cut'), 
                        anActionReport,
                    ))
 
            if anAction == 'Paste':
                _MDDRenderRefactorResultsDump( theRdCtxt, anActionResult)
                            
    return None

                
            
 
                
                
def _MDDRenderRefactorResultsDump( theRdCtxt, theRefactorReport):
    
    return None



            
            

    
def _MDDRender_Tabular_Cabecera( theRdCtxt):
    
    return None


    
  


    
def _MDDRender_Tabular_Values( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aExcludeTitle = theRdCtxt.fGP( 'ExcludeTitle', True)
    aExcludeID    = theRdCtxt.fGP( 'ExcludeId',    False)
    
    unosNonTextFieldsNames = aSRES.get( 'non_text_field_names', [])
    
    if aExcludeTitle and aExcludeID and ( not unosNonTextFieldsNames):
        return None
    
    theRdCtxt.pOS( u"""
    <table id="ciD_MDDValores" width="100%%" class="listing" summary="%(ModelDDvlPlone_caracteristicas_tabletitle)s"
        <thead>
            <tr>
                <th class="nosort" align="left">%(ModelDDvlPlone_caracteristicas_tabletitle)s</th>
                <th class="nosort" align="left">%(ModelDDvlPlone_valores_tabletitle)s</th>
            </tr>
        </thead>
        <tbody>
    """ %{
        'ModelDDvlPlone_caracteristicas_tabletitle': theRdCtxt.fUITr( 'ModelDDvlPlone_caracteristicas_tabletitle'),
        'ModelDDvlPlone_valores_tabletitle':         theRdCtxt.fUITr( 'ModelDDvlPlone_valores_tabletitle'),
    })
    

    unIndexClassFila = 0
    
    if not aExcludeID:
        theRdCtxt.pOS( u"""
        <tr id="ciD_MDDValores_Row_id" class="%(RowClass)s" 
            <td align="left">
                <strong id="ciD_MDDValores_Row_id_label">%(ModelDDvlPlone_id_label)s</strong>
                &emsp;
                <span   id="ciD_MDDValores_Row_id_help"class="formHelp">%(ModelDDvlPlone_id_help)s</span>                   
            </td>
            <td align="left" >%(SRES_id)s</td>
        """ %  {
            'RowClass':                                  cClasesFilas[ unIndexClassFila % 2],
            'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
            'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
            'SRES_id':                                   aSRES.get( 'id', ''),
        })
        
        unIndexClassFila += 1
        
       
    someValueResults = aSRES.get( 'values', [])
    
    for aATTRRES in someValueResults:
        
        if aATTRRES:
            
            unAttributeName = aATTRRES.get( 'attribute_name', '')
            unAttributeConfig = aATTRRES.get( 'attribute_config', '')
            
            if unAttributeName and ( not ( unAttributeName == 'id')) and \
               (( not ( unAttributeName == 'Title')) or ( not aExcludeTitle)) and \
               ( unAttributeName in unosNonTextFieldsNames) and \
               ( not unAttributeConfig.get('exclude_from_values_form', False)) and \
               (( not unAttributeConfig.has_key( 'custom_presentation_view') or not aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])):
                   
                theRdCtxt.pOS( u"""
                <tr id="ciD_MDDValores_Row_%(attribute_name)s" class="%(RowClass)s" 
                    <td align="left">
                        <strong id="ciD_MDDValores_Row_%(attribute_name)s_label">%(attribute_label)s</strong>
                        &emsp;
                        <span   id="ciD_MDDValores_Row_%(attribute_name)s_help" class="formHelp">%(attribute_description)s</span>                   
                    </td>
                """ % {
                    'attribute_name':                            unAttributeName,
                    'attribute_label':                           aATTRRES.get( 'attribute_translations', {}).get( 'translated_label', ''),
                    'attribute_description':                     aATTRRES.get( 'attribute_translations', {}).get( 'translated_description', ''),
                    'RowClass':                                  cClasesFilas[ unIndexClassFila % 2],
                    'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
                    'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
                })
                
                
                if aATTRRES.get( 'read_permission', False):
                    
                    unAttributeValue = u''
                    if aATTRRES[ 'type'] in [ 'selection', 'boolean']:
                        unAttributeValue = aATTRRES.get( 'translated_value', u'')
                    else:
                        unAttributeValue = aATTRRES.get( 'uvalue', u'')
                        
                    theRdCtxt.pOS( u"""
                    <td id="ciD_MDDValores_Row_%(attribute_name)s_value" align="left" >%(attribute_value)s</td>
                    """ % {
                        'attribute_name':                        unAttributeName,
                        'attribute_value':                       unAttributeValue,
                    })
                else:
                    theRdCtxt.pOS( u"""
                    <td align="left" bgcolor="%s">&ensp;</td>
                    """ % cNoValueBGColor
                    )
                    
                theRdCtxt.pOS( u"""
                </tr>
                """)
                    
                    
                unIndexClassFila += 1
                        
    theRdCtxt.pOS( u"""
        </tbody>
    </table>
    """)

    return None


    
    
   




    
def _MDDRender_Tabular_Texts( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    unosTextFieldsNames = aSRES.get( 'text_field_names', [])
    
    if not unosTextFieldsNames:
        return None
    
    someValueResults = aSRES.get( 'values', [])
    
    for aATTRRES in someValueResults:
        
        if aATTRRES:
            
            unAttributeName   = aATTRRES.get( 'attribute_name', '')
            unAttributeConfig = aATTRRES.get( 'attribute_config', '')
            
            if unAttributeName  and \
               ( unAttributeName in unosTextFieldsNames) and \
               ( not unAttributeConfig.get('exclude_from_values_form', False)) and \
               (( not unAttributeConfig.has_key( 'custom_presentation_view') or not aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])):
                
                theRdCtxt.pOS( u"""
                <table id="ciD_MDDTexto_%(attribute_name)s_table" width="100%%" class="listing" summary="%(attribute_label)s"
                    <thead>
                        <tr>
                            <th class="nosort" align="left">
                                <strong id="ciD_MDDTexto_%(attribute_name)s_label">%(attribute_label)s</strong>
                                &emsp;
                                <span   id="ciD_MDDTexto_%(attribute_name)s_help" class="formHelp">%(attribute_description)s<span/>  
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="odd">
                """ % {
                    'attribute_name':                            unAttributeName,
                    'attribute_label':                           aATTRRES.get( 'attribute_translations', {}).get( 'translated_label', ''),
                    'attribute_description':                     aATTRRES.get( 'attribute_translations', {}).get( 'translated_description', ''),
                    'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
                    'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
                })
                
                
                if aATTRRES.get( 'read_permission', False):
                    
                    unAttributeValue = aATTRRES.get( 'translated_value', u'')
                    
                    theRdCtxt.pOS( u"""
                    <td>
                        <p id="ciD_MDDTexto_%(attribute_name)s_para">
                    """% {
                        'attribute_name':                            unAttributeName,
                    })
                    
                    if unAttributeValue:
                        
                        unasLineasTexto = unAttributeValue.splitlines()
                        unNumLineas     = len( unasLineasTexto)

                        unIndexLinea = 0
                        for unaLineaTexto in unasLineasTexto:
                            
                            unaLineaTextoStripped = unaLineaTexto.lstrip()
                            theRdCtxt.pOS( u"""
                            <span>%s%s</span>
                            """ % (  
                                '&ensp;' * ( len( unaLineaTexto) - len( unaLineaTextoStripped)), 
                                unaLineaTextoStripped,
                            ))
                            unIndexLinea += 1
                            if unIndexLinea < unNumLineas:
                                theRdCtxt.pOS( u"""<br/>""")

                                
                                
                    theRdCtxt.pOS( u"""
                        </td>
                    </p>""" )
                else:
                    theRdCtxt.pOS( u"""
                    <td bgcolor="%(cNoValueBGColor)s"><p id="ciD_MDDTexto_%(attribute_name)s_para" />&ensp;</td>
                    """ % {
                        'cNoValueBGColor':                           cNoValueBGColor,
                        'attribute_name':                            unAttributeName,
                    })
                
                    
                theRdCtxt.pOS( u"""
                    </tr>
                </table>
                <br/>""" )
                        
                        
    return None


    
    






    
def _MDDRender_Tabular_CustomPresentationViews( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None

    unosTextFieldsNames = aSRES.get( 'text_field_names', [])
    
    if not unosTextFieldsNames:
        return None

    aModelDDvlPloneTool = theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None
    
    someValueResults = aSRES.get( 'values', [])
    
    for aATTRRES in someValueResults:
        
        if aATTRRES:
            
            unAttributeName   = aATTRRES.get( 'attribute_name', '')
            unAttributeConfig = aATTRRES.get( 'attribute_config', '')
            
            if unAttributeName  and \
               ( unAttributeName in unosTextFieldsNames) and \
               ( not unAttributeConfig.get('exclude_from_values_form', False)) and \
               (( unAttributeConfig.has_key( 'custom_presentation_view') and aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])):
                
                unCustomViewRendering = aModelDDvlPloneTool.fRenderTemplate( aSRES[ 'object'], aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])
                theRdCtxt.pOS( unCustomViewRendering)
                
                
    return None









def _MDDRender_Tabular_Traversals( theRdCtxt):
    
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    unasTraversals = aSRES.get( 'traversals', [])
    
    if not unasTraversals:
        return None

    for aTRAVRES in unasTraversals:
        
        if aTRAVRES:
            
            aTraversalKind    = aTRAVRES.get( 'traversal_kind', '')
            
            if aTraversalKind == 'aggregation':
                
                aRdCtxt = theRdCtxt.fNewCtxt( {
                    'TRAVRES': aTRAVRES
                })
                
                anIsCollection = aTRAVRES.get( 'is_collection', False)
                
                if anIsCollection:
                    
                    _MDDRender_Tabular_Coleccion_Sola( aRdCtxt)
                    
                else:
                    
                    aContainsCollections = aTRAVRES.get( 'contains_collections', False)
                    
                    if aContainsCollections:
                    
                        _MDDRender_Tabular_ColeccionesEnTabla( aRdCtxt)
                    
                    else:
                        
                        _MDDRender_Tabular_SinColeccionEnTabla( aRdCtxt)
                 
                        
                        
                        
            elif aTraversalKind == 'relation':
                
                anIsMultiValued = aTRAVRES.get( 'is_multivalued', False)
                
                if anIsMultiValued:
                    
                    pass # _MDDRender_Tabular_ReferenciasEnTabla( aRdCtxt)
                    
                else:
                    
                    pass #  _MDDRender_Tabular_ReferenciaEnTabla( aRdCtxt)
                    
                
    return None








def _MDDRender_Tabular_Coleccion_Sola( theRdCtxt):
    
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    theRdCtxt.pSP ( 'thePermiteCrearElementos',
        theRdCtxt.fGP ( 'thePermiteCrearElementos',    False) and aSRES[ 'add_permission'] and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'] and ( not TRAVRES[ 'max_multiplicity_reached']) and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    )
    
    theRdCtxt.pSP ( 'thePermiteEditarElementos',
        theRdCtxt.fGP ( 'thePermiteEditarElementos',   False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission']
    )
    
    theRdCtxt.pSP ( 'thePermiteOrdenarElementos',
        theRdCtxt.fGP ( 'thePermiteOrdenarElementos',  False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission']
    )
    
    theRdCtxt.pSP ( 'thePermiteEliminarElementos',
        theRdCtxt.fGP ( 'thePermiteEliminarElementos', False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'] and\
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    )

    theRdCtxt.pSP ( 'thePermiteModificarElementos', theRdCtxt.fGP ( 'thePermiteEditarElementos', False) or  theRdCtxt.fGP ( 'thePermiteOrdenarElementos', False) or  theRdCtxt.fGP ( 'thePermiteEliminarElementos', False))
    
    
    someElements = aTRAVRES.get( 'elements', [])
    
    unSiempre = theRdCtxt.fGP( 'theSiempre', True)
    
    
         
    if someElements or unSiempre:
        
        _MDDRender_Tabular_Tabla( theRdCtxt)
        
        
    return None


        


def _MDDRender_Tabular_SinColeccionEnTabla( theRdCtxt):
    
  
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    theRdCtxt.pSP ( 'thePermiteCrearElementos',
        theRdCtxt.fGP ( 'thePermiteCrearElementos',    False) and aSRES[ 'add_permission'] and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'] and ( not TRAVRES[ 'max_multiplicity_reached']) and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    )
    
    theRdCtxt.pSP ( 'thePermiteEditarElementos',
        theRdCtxt.fGP ( 'thePermiteEditarElementos',   False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission']
    )
    
    theRdCtxt.pSP ( 'thePermiteOrdenarElementos',
        theRdCtxt.fGP ( 'thePermiteOrdenarElementos',  False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission']
    )
    
    theRdCtxt.pSP ( 'thePermiteEliminarElementos',
        theRdCtxt.fGP ( 'thePermiteEliminarElementos', False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'] and\
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    )
   
    theRdCtxt.pSP ( 'thePermiteModificarElementos', theRdCtxt.fGP ( 'thePermiteEditarElementos', False) or  theRdCtxt.fGP ( 'thePermiteOrdenarElementos', False) or  theRdCtxt.fGP ( 'thePermiteEliminarElementos', False))

    
    
    someElements = aTRAVRES.get( 'elements', [])
    
    unSiempre = theRdCtxt.fGP( 'theSiempre', True)
         
    
    
    if someElements or unSiempre:
        
        theRdCtxt.pOS( u"""
        <h2 id="cid_MDDTraversal_%(traversal_name)s_label" >%(traversal_label)s</h2>
        <table id="cid_MDDTraversal_%(traversal_name)s_table" width="100%%" cellspacing="0" cellpadding="0" frame="void">
            <tr>
                <td id="cid_MDDTraversal_%(traversal_name)s_description" align="left" valign="baseline" class="formHelp">%(traversal_description)s</td>
                <td align="right" valign="baseline"> 
                </td>
            </tr>
        </table>
        """ % {
            'traversal_name':           aTRAVRES[ 'traversal_name'],        
            'traversal_label':          aTRAVRES[ 'traversal_translations']['translated_label'],        
            'traversal_description':    aTRAVRES[ 'traversal_translations']['translated_description'],        
        })
        
        _MDDRender_Tabular_Tabla( theRdCtxt)
        
        
    return None

        
 





def _MDDRender_Tabular_ColeccionesEnTabla( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    theRdCtxt.pSP ( 'thePermiteCrearColecciones',
        theRdCtxt.fGP ( 'thePermiteCrearColecciones',    False) and aSRES[ 'add_permission'] and aSRES[ 'add_collection_permission'] and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'] and ( not TRAVRES[ 'max_multiplicity_reached']) and \
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    )
    
    theRdCtxt.pSP ( 'thePermiteEditarColecciones',
        theRdCtxt.fGP ( 'thePermiteEditarColecciones',   False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission']
    )
    
    theRdCtxt.pSP ( 'thePermiteOrdenarColecciones',
        theRdCtxt.fGP ( 'thePermiteOrdenarColecciones',  False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission']
    )
    
    theRdCtxt.pSP ( 'thePermiteEliminarColecciones',
        theRdCtxt.fGP ( 'thePermiteEliminarColecciones', False) and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        aTRAVRES[ 'read_permission'] and TRAVRES[ 'write_permission'] and\
        not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))
    )

    theRdCtxt.pSP ( 'thePermiteModificarElementos', theRdCtxt.fGP ( 'thePermiteEditarElementos', False) or  theRdCtxt.fGP ( 'thePermiteOrdenarElementos', False) or  theRdCtxt.fGP ( 'thePermiteEliminarElementos', False))

    
    someElements = aTRAVRES.get( 'elements', [])
    unSiempre = theRdCtxt.fGP( 'theSiempre', True)

    if not( someElements or unSiempre):
        return None
    
    
    
    theRdCtxt.pOS( u"""
    <h2 id="cid_MDDTraversal_%(traversal_name)s_label" >%(traversal_label)s</h2>
    <table id="cid_MDDTraversal_%(traversal_name)s_table" width="100%%" cellspacing="0" cellpadding="0" frame="void">
        <tbody>
            <tr>
                <td id="cid_MDDTraversal_%(traversal_name)s_description" align="left" valign="baseline" class="formHelp">%(traversal_description)s</td>
                <td align="right" valign="baseline"> 
    """ % {
        'traversal_name':           aTRAVRES[ 'traversal_name'],        
        'traversal_label':          aTRAVRES[ 'traversal_translations']['translated_label'],        
        'traversal_description':    aTRAVRES[ 'traversal_translations']['translated_description'],        
    })

    
    
    
    someFactories = aTRAVRES.get( 'factories', [])
    if theRdCtxt.fGP( 'thePermiteCrearColecciones', False) and someFactories:
        
        if len( someFactories) == 1:
            
            theRdCtxt.pOS( u"""
            <a  id="cid_MDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Link"
                href="%(url)sCrear/?theNewTypeName=%(theMetaType)s&theAggregationName=%(traversal_name)s"  
                title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" >
                
                <img src="%(portal_url)s/add_icon.gif" id="cid_MDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Icon"
                    title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" 
                    alt="%(ModelDDvlPlone_crear_action_label)s" />
                &nbsp;
                
                %(ModelDDvlPlone_crear_action_label)s
                 &nbsp;
                %(translated_archetype_name)s       
            </a>
            """ % {
                'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                'translated_archetype_name':         aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name'],
                'translated_type_description':       aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_type_description'],
                'url':                               aSRES[ 'url'] ,
                'theMetaType':                       aTRAVRES[ 'factories'][ 0][ 'meta_type'],
                'traversal_name':                    aTRAVRES[ 'traversal_name'],
                'portal_url':                        aSRES[ 'portal_url'],
            })
            
        else:
            
            theRdCtxt.pOS( u"""
            <img src="%(portal_url)s/add_icon.gif" title="%(ModelDDvlPlone_crear_action_label)s " alt="%(ModelDDvlPlone_crear_action_label)s" />
                &nbsp;
                %(ModelDDvlPlone_crear_action_label)s
            """ % {
                'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                'url':                               aSRES[ 'url'] ,
                'traversal_name':                    aTRAVRES[ 'traversal_name'],
                'portal_url':                        aSRES[ 'portal_url'],
            })
            
            for aFactory in someFactories:
                
                theRdCtxt.pOS( u"""
                <a  id="cid_MDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Link"
                    href="%(url)sCrear/?theNewTypeName=%(theMetaType)s&theAggregationName=%(traversal_name)s"  
                    title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" >
                    
                    <img src="%(portal_url)s/add_icon.gif" id="cid_MDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Icon"
                        title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" 
                        alt="%(ModelDDvlPlone_crear_action_label)s" />
                    &nbsp;
                    
                    %(ModelDDvlPlone_crear_action_label)s
                     &nbsp;
                    %(translated_archetype_name)s       
                </a>
                """ % {
                    'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                    'translated_archetype_name':         aFactory[ 'type_translations'][ 'translated_archetype_name'],
                    'translated_type_description':       aFactory[ 'type_translations'][ 'translated_type_description'],
                    'url':                               aSRES[ 'url'] ,
                    'theMetaType':                       aFactory[ 'meta_type'],
                    'traversal_name':                    aTRAVRES[ 'traversal_name'],
                    'portal_url':                        aSRES[ 'portal_url'],
                })
        
    theRdCtxt.pOS( u"""
            </tr>
        </tbody>
    </table>
    """)
             
                
    if ( not someElements):
        theRdCtxt.pOS( u"""
        <br/>
        """)
        return None
    
     
                  
     
    unIndex = 0
    for aSUBSRES in someElements:
        
        aSubRdCtxt = theRdCtxt.fNewCtxt( {
            'PARENT_SRES':    aSRES,
            'PARENT_TRAVRES': aTRAVRES,
            'SRES':           aSUBSRES,
            'index':          unIndex,
        })
       
        
        _MDDRender_Tabular_ColeccionesEnTabla_OneHeader( aSubRdCtxt)
        
        _MDDRender_Tabular_Tabla(                        aSubRdCtxt)
            
        unIndex += 1
        
        
    return None           
        
        
        
        
        
        



def _MDDRender_Tabular_ColeccionesEnTabla_OneHeader( theRdCtxt):
 
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    if not aPARENT_SRES:
        return None
    
    
    aSRESIndex = theRdCtxt.fGP( 'index', 0)
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    
    someElements  = aTRAVRES.get( 'elements', [])
    unNumElements = len(someElements)
    unSiempre     = theRdCtxt.fGP( 'theSiempre', True)
    
        
    theRdCtxt.pOS( u"""
    <table width="100%%" cellspacing="0" cellpadding="0" frame="void" id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Header">
        <tbody>
            <tr>
    """ )
    
    if ( unNumElements > 1) and theRdCtxt.fGP( 'thePermiteOrdenarColecciones', False):
        theRdCtxt.pOS( u"""
        <td align="left" valign="baseline" width="40" >
        """ )
    
        if not aSRESIndex:
            theRdCtxt.pOS( u"""
            <a id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Subir_Link"
                title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                href="'%(PARENTSRES-url)sTabular/?theMovedElementID=%s&theMoveDirection=Up&theTraversalName=%(traversal_name)s&dd=%(millis)d#cid_MDDElemento_%(SRES-UID)s_title" >                
                <img id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Subir_Icon"
                   alt="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                    title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                    src="%(portal_url)s/arrowUp.gif" />
            """ % {
                'ModelDDvlPlone_subir_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                'translated_archetype_name':           aSRES[ 'type_translations'][ 'translated_archetype_name'], 
                'SRES-title':                          aSRES[ 'values_by_name'][ 'title'][ 'uvalue'],
                'SRES-id':                             aSRES[ 'id'],
                'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
                'traversal_name':                      aTRAVRES[ 'traversal_name'],
                'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                'SRES-UID':                            aSRES[ 'UID'],
                'portal_url':                          aSRES[ 'portal_url'],
            })

        else:
                
            theRdCtxt.pOS( u"""
            <img   alt="Blank" title="Blank" id="icon-blank"  src="%(portal_url)s/arrowBlank.gif" />
            """ % {
                'portal_url':                          aSRES[ 'portal_url'],
            })

        theRdCtxt.pOS( u"""
        &nbsp;
        """ )
                                                                
            
        if aSRESIndex == ( unNumElements - 1):
            theRdCtxt.pOS( u"""
            <a id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Bajar_Link"
                title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                href="'%(PARENTSRES-url)sTabular/?theMovedElementID=%s&theMoveDirection=Down&theTraversalName=%(traversal_name)s&dd=%(millis)d#cid_MDDElemento_%(SRES-UID)s_link" >                
                <img  id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Bajar_Icon"
                    alt="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                    title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                    src="%(portal_url)s/arrowDown.gif" />
            """ % {
                'ModelDDvlPlone_bajar_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                'translated_archetype_name':           aSRES[ 'type_translations'][ 'translated_archetype_name'], 
                'SRES-title':                          aSRES[ 'values_by_name'][ 'title'][ 'uvalue'],
                'SRES-id':                             aSRES[ 'id'],
                'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
                'traversal_name':                      aTRAVRES[ 'traversal_name'],
                'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                'SRES-UID':                            aSRES[ 'UID'],
                'portal_url':                          aSRES[ 'portal_url'],
            })

        else:
                
            theRdCtxt.pOS( u"""
            <img   alt="Blank" title="Blank" id="icon-blank"  src="%(portal_url)s/arrowBlank.gif" />
            """ % {
                'portal_url':                          aSRES[ 'portal_url'],
            })
            
        theRdCtxt.pOS( u"""
        </td>
        """ )


    theRdCtxt.pOS( u"""
    <td align="left" valign="baseline">
    """ )
            
    aTitleForElement = aSRES[ 'values_by_name'][ 'title'][ 'uvalue']
    if ( aSRES[ 'values_by_name'][ 'title'][ 'uvalue'] == aSRES[ 'archetype_name']):
        aTitleForElement = aSRES[ 'type_translations'][ 'translated_archetype_name']
        
    theRdCtxt.pOS( u"""
    <td align="left" valign="baseline">
        <h3 > 
            <a name="cid_MDDElemento_%(SRES-UID)s_link" 
                href="%(SRES-url)s/Tabular/" 
                title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(Element-title)s" >
                <span id="cid_MDDElemento_%(SRES-UID)s_title" class="state-visible">%(Element-title)s</span>
            </a>
        </h3>
    </td>        
    """ % {
        'ModelDDvlPlone_navegara_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
        'translated_archetype_name':           aSRES[ 'type_translations'][ 'translated_archetype_name'], 
        'Element-title':                       aTitleForElement,
        'SRES-id':                             aSRES[ 'id'],
        'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
        'SRES-url':                            aSRES[ 'url'],
        'traversal_name':                      aTRAVRES[ 'traversal_name'],
        'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
        'SRES-UID':                            aSRES[ 'UID'],
        'portal_url':                          aSRES[ 'portal_url'],
    })
            

                        
            
    if aSRESIndex:
        theRdCtxt.pOS( u"""
        <td align="left" valign="baseline">
            &nbsp;
            <span class="formHelp">%(translated_type_description)s</span>
        </td>        
        """ % {
            'translated_type_description':           aSRES[ 'type_translations'][ 'translated_type_description'], 
        })
    else:
        theRdCtxt.pOS( u"""
        <td align="left" valign="baseline">
            &nbsp;
        </td>        
        """ )
        
                        

    if theRdCtxt.fGP( 'thePermiteEditarColecciones', False) and SRES[ 'read_permission'] and SRES[ 'write_permission']:                                
        theRdCtxt.pOS( u"""
        <td width="120" align="right" valign="baseline">                                
            <a id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Editar_Link"
                href="%(SRES-url)sEditar/'" 
                title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(SRES-title)s" >
                <img src="%(portal_url)s/edit.gif"
                    alt="%(ModelDDvlPlone_editar_action_label)s" 
                    title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                    id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Editar_Icon" />
                <span>%(ModelDDvlPlone_editar_action_label)s</span>        
            </a>
        </td>
        """ % {
            'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
            'translated_archetype_name':           aSRES[ 'type_translations'][ 'translated_archetype_name'], 
            'SRES-title':                          aSRES[ 'values_by_name'][ 'title'][ 'uvalue'],
            'SRES-id':                             aSRES[ 'id'],
            'SRES-url':                            aSRES[ 'url'],
            'traversal_name':                      aTRAVRES[ 'traversal_name'],
            'SRES-UID':                            aSRES[ 'UID'],
            'portal_url':                          aSRES[ 'portal_url'],
        })

    if theRdCtxt.fGP( 'thePermiteEliminarColecciones', False) and SRES[ 'read_permission'] and SRES[ 'write_permission']  and SRES[ 'delete_permission']:                                
        theRdCtxt.pOS( u"""
        <td width="120" align="right" valign="baseline" >                                
            <a id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Eliminar_Link"
                href="%(SRES-url)sEditar/'" 
                title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(SRES-title)s" >
                <img src="%(portal_url)s/delete_icon.gif"
                    alt="%(ModelDDvlPlone_eliminar_action_label)s" 
                    title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                    id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Eliminar_Icon" />
                <span>%(ModelDDvlPlone_eliminar_action_label)s</span>        
            </a>
        </td>
        """ % {
            'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
            'translated_archetype_name':           aSRES[ 'type_translations'][ 'translated_archetype_name'], 
            'SRES-title':                          aSRES[ 'values_by_name'][ 'title'][ 'uvalue'],
            'SRES-id':                             aSRES[ 'id'],
            'SRES-url':                            aSRES[ 'url'],
            'traversal_name':                      aTRAVRES[ 'traversal_name'],
            'SRES-UID':                            aSRES[ 'UID'],
            'portal_url':                          aSRES[ 'portal_url'],
        })
                           
                    
    theRdCtxt.pOS( u"""
            </tr>
        </tbody>
    </table>
    """ )

        
    unaDescription = aSRES[ 'values_by_name'][ 'description'][ 'uvalue']
    if unaDescription:
        theRdCtxt.pOS( u"""
        <p>%s</p>
        """ % unaDescription)
                 
                
    return None

        























def _MDDRender_Tabular_Tabla( theRdCtxt):
    
  
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return None
    
    aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    if not aPARENT_SRES:
        return None
    
    
    aSRESIndex = theRdCtxt.fGP( 'index', 0)
    
    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return None
    
    
    someElements = aTRAVRES.get( 'elements', [])
    unSiempre    = theRdCtxt.fGP( 'theSiempre', True)

    unNumElements = len( aTRAVRES[ 'elements'])
    
    unIdTabla = 'cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Table' % {
        'traversal_name':                      aTRAVRES[ 'traversal_name'],
        'SRES-UID':                            aSRES[ 'UID'],
    }
    
    theRdCtxt.pOS( u"""
    <table width="100%%" cellspacing="0" cellpadding="0" frame="void" id="cid_MDDTraversal_%(traversal_name)s_Elemento_%(SRES-UID)s_Table"
        summary="%(SRES-title)s">
        <tbody>
            <tr>
    """ % {
            'unIdTabla':                           unIdTabla,
            'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
            'translated_archetype_name':           aSRES[ 'type_translations'][ 'translated_archetype_name'], 
            'SRES-title':                          aSRES[ 'values_by_name'][ 'title'][ 'uvalue'],
            'SRES-id':                             aSRES[ 'id'],
            'SRES-url':                            aSRES[ 'url'],
            'traversal_name':                      aTRAVRES[ 'traversal_name'],
            'SRES-UID':                            aSRES[ 'UID'],
            'portal_url':                          aSRES[ 'portal_url'],
        })

    unPermiteSeleccionarElementos = theRdCtxt.fGP( 'thePermiteSeleccionarElementos', False)
    unPermiteModificarElementos   = theRdCtxt.fGP( 'thePermiteModificarElementos',   False)
    unPermiteEliminarElementos    = theRdCtxt.fGP( 'thePermiteEliminarElementos',    False)
    
    
    if unPermiteSeleccionarElementos:
        theRdCtxt.pOS( u"""
        <col width="24" />
        """)
    
    if unPermiteModificarElementos:
        theRdCtxt.pOS( u"""
        <col width="110" />
        """)
        
        
      
    unosColumnNames = aTRAVRES.get( 'column_names', [])
    
    uNumColumnNames =len( unosColumnNames)
    
    theRdCtxt.pOS( u"""
    <col/>
    """ * uNumColumnNames)


    theRdCtxt.pOS( u"""
    <thead>
        <tr>
    """)
    
    if unPermiteSeleccionarElementos:
        
        theRdCtxt.pOS( u"""
        <th class="nosort" align="left" >
            <input type="checkbox"  class="noborder"  value=""
                name="%(unIdTabla)s_SelectAll" id="%(unIdTabla)s_SelectAll" 
                onchange="pMDDToggleAllSelections('%(unIdTabla)s'); return true;"/>
        """ %{
        'unIdTabla':                           unIdTabla,
       })


        if not unPermiteModificarElementos:
            theRdCtxt.pOS( u"""
                <metal:block metal:use-macro="here/MenuAccionesGrupo/macros/tMenuAccionesGrupo" />   
            """)
            
        else:
            theRdCtxt.pOS( u"""
                <th class="nosort" align="left" > 
                    <metal:block metal:use-macro="here/MenuAccionesGrupo/macros/tMenuAccionesGrupo" />   
                </th>
            """)
            
        for unColumnName in unosColumnNames:
            theRdCtxt.pOS( u"""
            <th class="nosort" align="left">%s</th>
            """ % TRAVRES[ 'column_translations'].get( unColumnName, {}).get( 'translated_label', unColumnName)
            )
            
    theRdCtxt.pOS( u"""
        </tr>
    </thead>
    <tbody>
    """ )
            
            
    for unIndexElemento in range( unNumElements):
        
        aERES = someElements[ unIndexElemento]
        aSubRdCtxt = theRdCtxt.fNewCtxt( {
            'ERES' : aERES,
        })
        
        aSubRdCtxt.pOS( u"""
        <tr class="%(Row-Class)s" id="%(unIdTabla)s_RowIndex_%(Row-Index)d" >
        """ % {
            'unIdTabla': unIdTabla,
            'Row-Class': cClasesFilas[ unIndexElemento % 2],
            'Row-Index': unIndexElemento,
        })
        
        if unPermiteModificarElementos or unPermiteSeleccionarElementos:
    
            if unPermiteSeleccionarElementos:
    
                aSubRdCtxt.pOS( u"""
                <td align="center" valign="baseline">
                    <input type="checkbox"  class="noborder"  value=""
                        name="%(unIdTabla)s_Select_%(Row-Index)d"
                        id="%(unIdTabla)s_RowIndex_%(Row-Index)d_SelectBox"  />
                </td>
                """ % {
                    'Row-Index': unIndexElemento,
                    'unIdTabla': unIdTabla,
                })
    
                
            if unPermiteModificarElementos:
                
                aSubRdCtxt.pOS( u"""
                <td align="center" valign="baseline">
                """)
                
                if aERES[ 'write_permission']:
                
                    if unPermiteEliminarElementos and aERES[ 'delete_permission']:
                        aSubRdCtxt.pOS( u"""
                        <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Delete_Link"
                            href="%(ERES-url)sEliminar/" 
                            title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                            <img 
                                alt="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                id="icon-delete" src="%(portal_url)s/delete_icon.gif"  />
                        </a>
                        &nbsp;    
                                            
                        """ %{
                            'unIdTabla':                           unIdTabla,
                            'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
                            'translated_archetype_name':           aERES[ 'type_translations'][ 'translated_archetype_name'], 
                            'ERES-title':                          aERES[ 'values_by_name'][ 'title'][ 'uvalue'],
                            'ERES-url':                            aERES[ 'url'],
                            'portal_url':                          aERES[ 'portal_url'],
                        })
                    
                    else:
                        aSubRdCtxt.pOS( u"""
                            <img src="%s/blank_icon.gif"  alt="Blank" title="Blank" id="icon-blank" />
                        """ %  aERES[ 'portal_url']
                        )
                        
                
                    if unPermiteEditarElementos and aERES[ 'write_permission']:
                        aSubRdCtxt.pOS( u"""
                        <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Edit_Link"
                            href="%(ERES-url)sEditar/" 
                            title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                            <img 
                                alt="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                id="icon-edit" src="%(portal_url)s/edit.gif"  />
                        </a>
                        &nbsp;    
                                            
                        """ %{
                            'unIdTabla':                           unIdTabla,
                            'ModelDDvlPlone_editar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                            'translated_archetype_name':           aERES[ 'type_translations'][ 'translated_archetype_name'], 
                            'ERES-title':                          aERES[ 'values_by_name'][ 'title'][ 'uvalue'],
                            'ERES-url':                            aERES[ 'url'],
                            'portal_url':                          aERES[ 'portal_url'],
                        })
                    
                    else:
                        aSubRdCtxt.pOS( u"""
                            <img src="%s/blank_icon.gif"  alt="Blank" title="Blank" id="icon-blank" />
                        """ %  aERES[ 'portal_url']
                        )
                        
                          
                        
                    if unPermiteOrdenarElementos and len( aTRAVRES[ 'elements']) > 1 and aSRES[ 'write_permission']:
                        
                        if  unIndexElemento:
                            aSubRdCtxt.pOS( u"""
                            <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Subir_Link"
                                href="%(SRES-url)Tabular/?theMovedElementID=%(ERES-id)s&theMoveDirection=Up&theTraversalName=%(traversal_name)s&dd=%(millis)d#cid_MDDElemento_%(ERES-UID)s" 
                                title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                <img 
                                    alt="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                    title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                    id="icon-edit" src="%(portal_url)s/arrowUp.gif"  />
                            </a>
                            &nbsp;    
                                                
                            """ %{
                                'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                                'unIdTabla':                           unIdTabla,
                                'ModelDDvlPlone_subir_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                                'translated_archetype_name':           aERES[ 'type_translations'][ 'translated_archetype_name'], 
                                'ERES-title':                          aERES[ 'values_by_name'][ 'title'][ 'uvalue'],
                                'ERES-id':                             aERES[ 'id'],
                                'ERES-UID':                            aERES[ 'UID'],
                                'traversal_name':                      aTRAVRES[ 'traversal_name'],
                                'SRES-url':                            aSRES[ 'url'],
                                'portal_url':                          aERES[ 'portal_url'],
                            })
                        
                        else:
                            aSubRdCtxt.pOS( u"""
                                <img src="%s/arrowBlank.gif"  alt="Blank" title="Blank" id="icon-blank" />
                            """ %  aERES[ 'portal_url']
                            )
                        
                         
                        
                        aSubRdCtxt.pOS( u"""
                        &nbsp;
                        """ )
                        
                           
                        
                        if  unIndexElemento:
                            aSubRdCtxt.pOS( u"""
                            <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Bajar_Link"
                                href="%(SRES-url)Tabular/?theMovedElementID=%(ERES-id)s&theMoveDirection=Down&theTraversalName=%(traversal_name)s&dd=%(millis)d#cid_MDDElemento_%(ERES-UID)s" 
                                title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                <img 
                                    alt="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                    title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                    id="icon-edit" src="%(portal_url)s/arrowDown.gif"  />
                            </a>
                            &nbsp;    
                                                
                            """ %{
                                'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                                'unIdTabla':                           unIdTabla,
                                'ModelDDvlPlone_bajar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                                'translated_archetype_name':           aERES[ 'type_translations'][ 'translated_archetype_name'], 
                                'ERES-title':                          aERES[ 'values_by_name'][ 'title'][ 'uvalue'],
                                'ERES-id':                             aERES[ 'id'],
                                'ERES-UID':                            aERES[ 'UID'],
                                'traversal_name':                      aTRAVRES[ 'traversal_name'],
                                'SRES-url':                            aSRES[ 'url'],
                                'portal_url':                          aERES[ 'portal_url'],
                            })
                        
                        else:
                            aSubRdCtxt.pOS( u"""
                                <img src="%s/arrowBlank.gif"  alt="Blank" title="Blank" id="icon-blank" />
                            """ %  aERES[ 'portal_url']
                            )
                                                                      
                aSubRdCtxt.pOS( u"""
                </td>
                """ )
        
        for unColumnName in unosColumnNames:
            aSubRdCtxt.pOS( u"""
            <td align="left" valign="baseline" >
            """ )
             
            if ( unColumnName == 'title') or ( unColumnName.lower().find('title') >= 0) or not ( 'title' in unosColumnNames) and  ( unColumnName == unosColumnNames[ 0]):
                
                unTitle = '%s %s %s %s %s (%s)' % ( 
                    theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'), 
                    aERES[ 'type_translations'][ 'translated_archetype_name'],
                    aERES[ 'values_by_name'][ unColumnName][ 'uvalue'], 
                    ( not ( unColumnName == 'title')       and  aERES[ 'values_by_name'].get( 'title', {}).get( 'uvalue', '')) or '', 
                    ( not ( unColumnName == 'description') and  aERES[ 'values_by_name'].get( 'description', {}).get( 'uvalue', '')) or '',
                    aERES[ 'type_translations'][ 'translated_type_description'],
                )
                
                
                aSubRdCtxt.pOS( u"""
                <a  class="state-visible" 
                    name="cid_MDDElemento_%(ERES-UID)s"
                    id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Link"
                    href="%(SRES-url)sTabular/" 
                    title="%(ERES-title)s" >
                    <img 
                        alt="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                        title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                        id="icon-edit" src="%(portal_url)s/arrowDown.gif"  />
                    <h4>
                        <img src="%(portal_url)s/%(content_icon)s" 
                            alt="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                            title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" />
                        <span  class="state-visible">%(column_value)s</span>
                    </h4>
                </a>
                &nbsp;    
                                    
                """ %{
                    'Row-Index':                           unIndexElemento,
                    'unTitle':                             unTitle,
                    'millis':                              theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fMillisecondsNow(), 
                    'unIdTabla':                           unIdTabla,
                    'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                    'translated_archetype_name':           aERES[ 'type_translations'][ 'translated_archetype_name'], 
                    'ERES-title':                          aERES[ 'values_by_name'][ 'title'][ 'uvalue'],
                    'ERES-id':                             aERES[ 'id'],
                    'ERES-UID':                            aERES[ 'UID'],
                    'traversal_name':                      aTRAVRES[ 'traversal_name'],
                    'SRES-url':                            aSRES[ 'url'],
                    'content_icon':                        aERES[ 'content_icon'],
                    'portal_url':                          aERES[ 'portal_url'],
                    'column_value':                        aERES[ 'values_by_name'][ unColumnName][ 'uvalue'],
                    
                })
                
            else:
                
                unAttributeResult =  aERES[ 'values_by_name'].get( unColumnName, {})
                
                if unAttributeResult:
                    
                    if unAttributeResult[ 'type'] in [ 'selection', 'boolean']:
                        aSubRdCtxt.pOS( u"""
                             <span>%s</span>
                         </tal:block>
                        """ % unAttributeResult.get( 'translated_value', '')
                        )
                    else:
                        if unAttributeResult[ 'uvalue'] and not ( unAttributeResult[ 'uvalue'] =='None'):
                            aSubRdCtxt.pOS( u"""
                                 <span>%s</span>
                            """ % unAttributeResult.get( 'uvalue', '') )

            aSubRdCtxt.pOS( u"""
            </td>
            """ )
                
                
                        
        aSubRdCtxt.pOS( u"""
        </tr>
        """ )
                                                                           

    theRdCtxt.pOS( u"""
    </tbody>
    </table>
    """ )
   
        
    return None




 


 

cDomainsStringsAndDefaults = [
    [ 'ModelDDvlPlone', [    
        [ 'ModelDDvlPlone_NumElementsCopied',           'Number of elements Copied-' ,],    
        [ 'ModelDDvlPlone_No_items_copied',             'NO elements Copied-' ,],    
        [ 'ModelDDvlPlone_NumElementsCut',              'Number of elements Cut-' ,],         
        [ 'ModelDDvlPlone_No_items_cut',                'NO elements Cut-' ,],         
        [ 'ModelDDvlPlone_caracteristicas_tabletitle',  'Features-',],
        [ 'ModelDDvlPlone_valores_tabletitle',          'Values-',],
        [ 'ModelDDvlPlone_id_label',                    'Identity-',],
        [ 'ModelDDvlPlone_id_help',                     'Unique indentifier of the element in its container. Is included in the element URL address.-',],
        [ 'ModelDDvlPlone_navegara_action_label',       'Navigate To-',],
        [ 'ModelDDvlPlone_crear_action_label',          'Create-',],
        [ 'ModelDDvlPlone_editar_action_label',         'Edit-',],
        [ 'ModelDDvlPlone_eliminar_action_label',       'Delete',],
        
        
    ]],
    

]



