# -*- coding: utf-8 -*-
#
# File: MDDInteractionTabular.py
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


# #####################################################################
"""Create an ExternalMethod on the plone site:
container plone_skins/custom 
id MDDInteractionTabular
Title MDDInteractionTabular
Module nane MDDInteractionTabular
Function Name MDDInteractionTabular

"""


import cgi 

import logging


from Acquisition                    import aq_get

from StringIO                       import StringIO

from Products.CMFCore.utils         import getToolByName



from Products.ExternalMethod.ExternalMethod import ExternalMethod

from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport     import fEvalString, fMillisecondsNow, fNewInteractionContext, cResultCondition_MissingParameter





# ####################################
"""External method names.

"""

from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion_Constants     import cMDDExtMethod_MDDManageActions, cMDDExtMethod_MDDPresentationActionsResults, cMDDExtMethod_MDDPresentationClipboard, cMDDExtMethod_MDDPresentationEmpty, cMDDExtMethod_MDDPresentationTabular



# ####################################
"""Request parameter names.

"""
cRqstParmName_NoCache         = 'theNoCache'
cRqstParmName_NoCacheCode     = 'theNoCacheCode'
cRqstParmName_FlushCacheCode  = 'theFlushCacheCode'
cRqstParmName_FlushDiskCache  = 'theFlushDiskCache'






# #######################################################################
""" Utility to escape strings written as HTML.

"""
def fCGIE( theString, quote=1):
    aString = theString
    if not ( aString.__class__.__name__ in ( 'str', 'unicode')):
        aString = str( aString) 
    if not aString:
        return aString
    return cgi.escape( aString, quote=quote)














# #######################################################################
"""Parameters relevant to the interaction with a Tabular view.

"""
def _fNewVoidInteractionParms_Tabular( ):
    unosParms = {
        'theModelDDvlPloneTool'   :None,
        'thePerformanceAnalysis'  :{},
        'theBrowsedElement'       :None, 
        'theTraversalName'        : '',
        'theRelationCursorName'   : '',
        'theCurrentElementUID'    : '',
        'theRequest'              :None, 
        'thePasteRequested'       :False,
        'theGroupAction'          :'',
        'theUIDs'                 :[],
        'theMovedElementID'       : '',
        'theMovedReferenceUID'    : '',
        'theMovedObjectUID'       : '',
        'theMoveDirection'        : '',
        'theTranslationsCache'    :None,
        'thePermissionsCache'     :None, 
        'theRolesCache'           :None,
        'theParentExecutionRecord':None,
        'theAdditionalParms'      :{},   
        'output'                  :None,
        'pO'                      :None,
        'pOL'                     :None,
        'pOS'                     :None,
    }
    return unosParms







def MDDInteractionTabular(  theInteractionParms=None, theViewParms=None):
    """Main service for handling the request-reply interaction  on tabular views, allowing actions for manipulation of the clipboard and the objects network.

    Entry point invoked from a template.

    PUBLIC METHOD for Tabular renderings with handling of Actions allowing manipulation of elements by authoried users.
    Must be registered as an External method as:
        Id            MDDInteractionTabular
        Title         MDDInteractionTabular
        Module name   MDDInteractionTabular
        Function name MDDInteractionTabular

    """

    if not theInteractionParms:
        return u''



    # #################################################################
    """Create interaction context.Initialize with received basic parameters. Initialize output streaming. 

    """
    aModelDDvlPloneTool = theInteractionParms.get( 'theModelDDvlPloneTool', None)
    aBrowsedElement     = theInteractionParms.get( 'theBrowsedElement',     None) 
    aRequest            = theInteractionParms.get( 'theRequest',            None)    
    aPasteRequested     = theInteractionParms.get( 'thePasteRequested',     False) 


    anOutput            = StringIO( u'')

    aInteractionCtxt = fNewInteractionContext( 
        aBrowsedElement,
        {
            'theInteractionParms':          theInteractionParms,
            'theViewParms':                 theViewParms,
            'theModelDDvlPloneTool':        aModelDDvlPloneTool,
            'theBrowsedElement':            theInteractionParms.get( 'theBrowsedElement', None),
            'theRequest':                   aRequest,
            'thePasteRequested':            aPasteRequested,
            'theBeginTime':                 None,
            'theEndTime':                   None,
            'output':                       anOutput,
            'pO':                           lambda theString: anOutput.write( theString),
            'pOL':                          lambda theString: anOutput.write( '%s\n' % theString),
            'pOS':                          lambda theString: anOutput.write( '%s\n' % '\n'.join( [ unaLine.strip() for unaLine in theString.splitlines()])),      
        }
    )



    # #################################################################
    """Retrieve localizations for internationalized strings.

    """

    _MDDInit_UITranslations_Tabular( aInteractionCtxt)



    # #################################################################
    """Make sure essential parameters are supplied, or return an error page.

    """
    if not theInteractionParms:
        _MDDRender_EmptyPageContents(  
            aInteractionCtxt,
            cResultCondition_MissingParameter + '-',
            'theInteractionParms',
            None
        )
        anHTMLToReturn = anOutput.getvalue()
        return anHTMLToReturn


    if not aModelDDvlPloneTool:
        _MDDRender_EmptyPageContents(  
            aInteractionCtxt,
            cResultCondition_MissingParameter + '-',
            'theModelDDvlPloneTool',
            None
        )
        anHTMLToReturn = anOutput.getvalue()
        return anHTMLToReturn


    if aBrowsedElement == None:
        _MDDRender_EmptyPageContents(  
            aInteractionCtxt,
            cResultCondition_MissingParameter + '-',
            'theBrowsedElement',
            None
        )
        anHTMLToReturn = anOutput.getvalue()
        return anHTMLToReturn


    if not aRequest:
        _MDDRender_EmptyPageContents(  
            aInteractionCtxt,
            aModelDDvlPloneTool.fTranslateI18N(  aBrowsedElement, 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
            'theRequest',
            None
        ) 
        anHTMLToReturn = anOutput.getvalue()
        return anHTMLToReturn




    # #################################################################
    """Begin Process.

    """
    aInteractionCtxt.pSP( 'theBeginTime', fMillisecondsNow())


    
    
    # #################################################################
    """Flush cache entries, if so requested.

    """   

    aFlushCacheCode = aRequest.get( cRqstParmName_FlushCacheCode, None)
    aFlushDiskCache = aRequest.get( cRqstParmName_FlushDiskCache, None)
    if aFlushCacheCode:
        aModelDDvlPloneTool.fFlushCachedTemplateForElement( aBrowsedElement, aFlushCacheCode,  'Tabular_NoHeaderNoFooter', aFlushDiskCache)



    # #################################################################
    """Try to get and execute the external method to Manage Actions.

    """   
    anActionsResult = None

    aBeginTime  = fMillisecondsNow()
    try:
        unManageActionsExternalMethod = aq_get( aBrowsedElement, cMDDExtMethod_MDDManageActions, None, 1)
    except:
        None  
    if unManageActionsExternalMethod and isinstance( unManageActionsExternalMethod, ExternalMethod):

        anActionsResult = unManageActionsExternalMethod( aInteractionCtxt)
        if anActionsResult:
            aInteractionCtxt.pSP( 'actions_result', anActionsResult)

            anEndTime  = fMillisecondsNow()
            theInteractionCtxt.pAppendRetrievalResult( {
                'subject':      'ACTIONS',
                'begin_time':   aBeginTime,
                'end_time':     anEndTime,
                'result':       anActionsResult,
            })



    # #################################################################
    """Retrieve Clipboard content,.

    """
    aBeginTime  = fMillisecondsNow()

    aClipboardResult = aModelDDvlPloneTool.fClipboardResult( 
        theTimeProfilingResults     =None,
        theContextualElement        =aBrowsedElement, 
        theAdditionalParams         =None,
    )
    if aClipboardResult:
        aInteractionCtxt.pSP( 'clipboard_result', aClipboardResult)

        anEndTime  = fMillisecondsNow()

        aInteractionCtxt.pAppendRetrievalResult( {
            'subject':      'CLIPBOARD',
            'begin_time':   aBeginTime,
            'end_time':     anEndTime,
            'result':       aClipboardResult,
        })








    # #################################################################
    """If element not writeable, present a note.

    """

    _MDDRender_NotAllowWrite( aInteractionCtxt, aBrowsedElement)







    # #################################################################
    """Invoke External Method to Present Clipboard content, if any.

    """
    if aClipboardResult and aClipboardResult.get( 'num_elements', 0):
        #if unPortalRoot:
        unPresentationClipboardExternalMethod = None
        try:
            unPresentationClipboardExternalMethod = aq_get( aBrowsedElement, cMDDExtMethod_MDDPresentationClipboard, None, 1)
        except:
            None  
        if unPresentationClipboardExternalMethod and isinstance( unPresentationClipboardExternalMethod, ExternalMethod):
            unPresentationClipboardExternalMethod( aInteractionCtxt)










    # #################################################################
    """Invoke External Method to Present Action results, if any.

    """
    if anActionsResult:
        unPresentationActionResultsExternalMethod = None
        try:
            unPresentationActionResultsExternalMethod = aq_get( aBrowsedElement, cMDDExtMethod_MDDPresentationActionsResults, None, 1)
        except:
            None  
        if unPresentationActionResultsExternalMethod and isinstance( unPresentationActionResultsExternalMethod, ExternalMethod):
            unPresentationActionResultsExternalMethod( aInteractionCtxt)



    # #################################################################
    """Present Page body: render on supplied output stream, by-passing cache and forcing to render, or trying first to obtain the rendered HTML from cache.

    """
    aPresentationOutput            = StringIO( u'')

    aPresentationCtxt = aInteractionCtxt.fNewCtxt( 
        {
            'output':                       aPresentationOutput,
            'pO':                           lambda theString: aPresentationOutput.write( theString),
            'pOL':                          lambda theString: aPresentationOutput.write( '%s\n' % theString),
            'pOS':                          lambda theString: aPresentationOutput.write( '%s\n' % '\n'.join( [ unaLine.strip() for unaLine in theString.splitlines()])),      
        }
    )

    unPresentationTabularExternalMethod = None
    try:
        unPresentationTabularExternalMethod = aq_get( aBrowsedElement, cMDDExtMethod_MDDPresentationTabular, None, 1)
    except:
        None  

    if unPresentationTabularExternalMethod and isinstance( unPresentationTabularExternalMethod, ExternalMethod):

        aNoCache     = aRequest.get( cRqstParmName_NoCache, None)
        aNoCacheCode = aRequest.get( cRqstParmName_NoCacheCode, None)
        aNoCacheAllowed = aModelDDvlPloneTool.fNoCacheIdAllowsRender( aBrowsedElement, aNoCacheCode, 'Tabular_NoHeaderNoFooter')

        aPresentedString = ''
        if aNoCacheAllowed:
            aPresentedString = unPresentationTabularExternalMethod( theInteractionCtxt=aPresentationCtxt, theViewParms=theViewParms)                
        else:
            aPresentedString = aModelDDvlPloneTool.fRenderCallableOrCachedForElement( 
                aBrowsedElement, 
                'Tabular_NoHeaderNoFooter', 
                lambda otherInteractionCtxt, otherViewParms: unPresentationTabularExternalMethod( 
                    theInteractionCtxt=otherInteractionCtxt,
                    theViewParms=otherViewParms
                    ), 
                aPresentationCtxt,
                theViewParms 
                )        

        if aPresentedString:
            anOutput.write( aPresentedString)


    # #################################################################
    """Present Page footer: sub-componentes (invoked templates) may delegate on cache, for example to present the Credits.

    """
    aHTMLPresentationFooter = aModelDDvlPloneTool.fRenderTemplate( aBrowsedElement, '%sFooter_view' )
    if aHTMLPresentationFooter:
        anOutput.write( aHTMLPresentationFooter)

    aInteractionCtxt.pSP( 'theEndTime', fMillisecondsNow())

    anHTMLToReturn = anOutput.getvalue()
    return anHTMLToReturn










def _MDDRender_EmptyPageContents( theInteractionCtxt, theErrorMessage, theErrorFeature, theErrorValue):
    aBrowsedElement =     theInteractionCtxt.fGP( 'theBrowsedElement', None)
    if aBrowsedElement == None:
        return None


    unRenderEmptyPageExternalMethod = None
    try:
        unRenderEmptyPageExternalMethod = aq_get( aBrowsedElement, cMDDExtMethod_MDDPresentationEmpty, None, 1)
    except:
        None  
    if unRenderEmptyPageExternalMethod and isinstance( unRenderEmptyPageExternalMethod, ExternalMethod):
        unRenderEmptyPageExternalMethod( theInteractionCtxt, theErrorMessage, theErrorFeature, theErrorValue)

    return None










def _MDDRender_NotAllowWrite( theInteractionCtxt=None, theBrowsedElement=None, ):
    """If element not writeable, present a note.

    """
    if not theInteractionCtxt:
        return None

    if theBrowsedElement == None:
        return None


    if theBrowsedElement.fAllowWrite():
        return None

    aModelDDvlPloneTool = theInteractionCtxt.fGP( 'theModelDDvlPloneTool', None)

    theInteractionCtxt.pOS( """
        <div class="portalMessage" >
                <font size="1">
                    <span>%(pTitle)s<span/>
                    <span>%(pMessage)s<span/>
                </font>
        </div>
    """ % {
            'pTitle': theBrowsedElement.Title(),
            'pMessage': aModelDDvlPloneTool.fTranslateI18N( theBrowsedElement, 'ModelDDvlPlone', 'ModelDDvlPlone_ElementLockedAgainstModifications', 'is Locked against modifications'),
        })
    return None






# #######################################################################
""" LOCALIZATION SUPPORT METHODS.

"""



def _MDDInit_UITranslations_Tabular( theRdCtxt,):
    """Preload some translations to use during rendering.

    """

    aContainerObject = theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return [ False, False,]

    someTranslations = theRdCtxt.fGP( 'theUITranslations', None)
    if someTranslations == None:
        someTranslations = { }
        theRdCtxt.pSP( 'theUITranslations', someTranslations)

    aModelDDvlPloneTool = theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return [ False, False,]

    aModelDDvlPloneTool.fTranslateI18NManyIntoDict( aContainerObject, cDomainsStringsAndDefaults, someTranslations)

    for aTranslationKey in someTranslations.keys():

        aTranslation = someTranslations.get( aTranslationKey, u'')
        anEncodedTranslation = fCGIE( aTranslation)
        someTranslations[ aTranslationKey] = anEncodedTranslation

    return [ True, True,]














# #######################################################################
"""Internationalized strings.

"""
cDomainsStringsAndDefaults = [
    [ 'plone', [    
        [ 'heading_actions',           'Actions-' ,],    
        [ 'Cut',                       'Cut-' ,],    
        [ 'Copy',                      'Copy-' ,],    
        [ 'Paste',                     'Paste-' ,],    
        [ 'Delete',                    'Delete-' ,],    
        [ 'Reorder',                   'Reorder-' ,],    

        ]],
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
        [ 'ModelDDvlPlone_recorrercursorrelacion_action_label', 'Browse elements Related as-',],
        [ 'ModelDDvlPlone_deorigenrelacioncuandoenlazando', 'of',],
        [ 'ModelDDvlPlone_tipo_label',                   'Type-',],
        [ 'ModelDDvlPlone_path_label',                   'Path-',],
        [ 'ModelDDvlPlone_desenlazar_action_label',      'Unlink-',],
        [ 'ModelDDvlPlone_desenlazar_DE',                'from-',],
        [ 'ModelDDvlPlone_cambiar_referencias_action_label',  'Change References-',],
        [ 'ModelDDvlPlone_Clipboard_Title',              'Clipboard-',],
        [ 'ModelDDvlPlone_Clipboard_Clear_action',       'Clear Clipboard',],
        [ 'ModelDDvlPlone_Clipboard_ContentsFrom',       'Clipboard Contents comes from-',],
        [ 'ModelDDvlPlone_Clipboard_ElementsWereCopied', 'Elements were COPIED and Shall be REPLICATED upon Paste operation.-',],
        [ 'ModelDDvlPlone_Clipboard_ElementsWereCut',    'Elements wer CUT and Shall be MOVED upon Paste operation.-',],
        [ 'ModelDDvlPlone_and',                          'and-',],
        [ 'ModelDDvlPlone_Clipboard_ContentsFromOutsideOfApplicationRoots', 'outside of the applications-',],
        [ 'ModelDDvlPlone_Clipboard_ContentsSameRoot',    'Same root-',],
        [ 'ModelDDvlPlone_Clipboard_ContentsOtherRoots',  'other roots-',],
        [ 'ModelDDvlPlone_Clipboard_NumElements',         'Number of elements-',],
        [ 'ModelDDvlPlone_Clipboard_NumContainedElements','Contained-',],
        [ 'ModelDDvlPlone_Clipboard_TotalElements',       'Total-',],
        [ 'ModelDDvlPlone_Clipboard_Empty',               'Empty Clipboard-',],
        [ 'ModelDDvlPlone_Tabular_Section_Features',      'Features-',],
        [ 'ModelDDvlPlone_Tabular_Sections',              'Sections-',],
        [ 'ModelDDvlPlone_Tabular_Section_Top',           'Top-',],
        [ 'ModelDDvlPlone_subir_action_label',            'Up-',],
        [ 'ModelDDvlPlone_bajar_action_label',            'Down-',],
        [ 'ModelDDvlPlone_refrescar_action_label',        'Refresh-',],
        [ 'ModelDDvlPlone_editar_action_label',           'Edit-',],
        [ 'ModelDDvlPlone_eliminar_action_label',         'Delete-',],
        [ 'ModelDDvlPlone_textual_action_label',          'Textual-',],
        [ 'ModelDDvlPlone_success',                       'Success-',],
        [ 'ModelDDvlPlone_refactor_Paste',                'Paste-',],
        [ 'ModelDDvlPlone_refactor_Import',               'Import-',],
        [ 'ModelDDvlPlone_paste_status',                  'Status-',],
        [ 'ModelDDvlPlone_paste_condition',               'Condition-',],
        [ 'ModelDDvlPlone_exception',                     'Exception-',],
        [ 'ModelDDvlPlone_class_name',                    'class-',   ],                                                               
        [ 'ModelDDvlPlone_method_name',                   'method-',  ],                                                                                   
        [ 'ModelDDvlPlone_error_status',                  'status-',  ],                                                                                  
        [ 'ModelDDvlPlone_error_reason',                  'reason-',  ],                                    
        [ 'ModelDDvlPlone_error_params',                  'params-',  ],

        ]],

]

