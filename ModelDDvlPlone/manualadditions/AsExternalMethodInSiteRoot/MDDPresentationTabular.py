# -*- coding: utf-8 -*-
#
# File: MDDPresentationTabular.py
#
# Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
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


from Acquisition                    import aq_get

from StringIO                       import StringIO

from Products.CMFCore.utils         import getToolByName



from Products.ExternalMethod.ExternalMethod import ExternalMethod

from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport     import fEvalString, fMillisecondsNow, fNewRenderContext, cResultCondition_MissingParameter

from Products.ModelDDvlPloneTool.PloneElement_TraversalConfig  import cPloneElement_ColumnName_Details, cPloneImage_DetailsHeight, cPloneDocument_DetailsLen

# ####################################
"""External method names.

"""

from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Inicializacion_Constants     import cMDDExtMethod_MDDPresentationEmpty



# ####################################
"""Development configuration parameter.

"""

cExtensionsForbidden = True

cLogMissingMethodBindings      = True


cForcePref_AllowExtensions = True


cForcePref_DisplayActionLabels = True



# ####################################
"""Request parameter names.

"""
cRqstParmName_NoCache      = 'theNoCache'
cRqstParmName_NoCacheCode  = 'theNoCacheCode'






# ####################################
"""Development configuration parameter.

"""
cPref_Pres_AllowExtensions_Name        = 'AllowExtensions'
cPref_Pres_AllowExtensions_Force       = True

cPref_Pres_DisplayActionLabels_Name    = 'DisplayActionLabels'
cPref_Pres_DisplayActionLabels_Force   = True


cPref_Pres_SectionsMenu_Item_MaxLength = '64'
cPref_Pres_SectionsMenu_Item_MaxLengthExceeded_Postfix = '...'


cPref_Pres_SiblingsMenu_Item_MaxLength = '128'
cPref_Pres_SiblingsMenu_Item_MaxLengthExceeded_Postfix = '...'




# ####################################
"""Constants.

"""
cClasesFilas = [ 'odd','even',]

cNoValueBGColor = 'silver'



cTraversalNames_GeneralReferences_WithTypeColumn = [
    'referentes',
    'referidos',
    'relatedItems',  # ACV 20091204 As of today still not supported (it was, but the generic references view was made obsolete, before this rewrite. Must implement support.
    'todosRelacionados',
    #'referenciasCualificadas',
    #'referentesCualificados',
]





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
# #######################################################################
"""PRESENTATION OF ACTION RESULTS, CLIPBOARD, PAGE BODY and EMPTY PAGE

"""




# #######################################################################
# #######################################################################
"""PRESENTATION OF EMPTY PAGE

"""


def MDDPresentationEmpty( theCtxt, theErrorMessage, theErrorFeature, theErrorValue):
    """Main service for rendering blank empty page with possibly an error message.

    PUBLIC VIEW METHOD for Tabular renderings, allowing manipulation of elements to authoried users.
    Must be registered as an External method as:
        Id            MDDPresentationEmpty
        Title         MDDPresentationEmpty
        Module name   MDDPresentationTabular
        Function name MDDPresentationEmpty

    """

    theCtxt.pOS( """
    <h1>ERROR</h1>
    <p><strong>%s</strong></p>
    <p>%s</p>
    <p>%s</p>
    """ % ( fCGIE( repr( theErrorMessage)), fCGIE( repr( theErrorFeature)), fCGIE( repr( theErrorValue), )))

    return None






def _MDDRender_EmptyPageContents( theRdCtxt, theErrorMessage, theErrorFeature, theErrorValue):
    aBrowsedElement =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aBrowsedElement == None:
        return None
    
    
    unRenderEmptyPageExternalMethod = None
    try:
        unRenderEmptyPageExternalMethod = aq_get( aBrowsedElement, cExtMethod_MDDPresentationEmpty, None, 1)
    except:
        None  
    if unRenderEmptyPageExternalMethod and isinstance( unRenderEmptyPageExternalMethod, ExternalMethod):
        unRenderEmptyPageExternalMethod( theRdCtxt, theErrorMessage, theErrorFeature, theErrorValue)
        
    return None








# #######################################################################
# #######################################################################
"""PRESENTATION OF Tabular PAGE BODY

"""


def MDDPresentationTabular(  
    theInteractionCtxt                  =None, 
    theViewParms                        =None, 
    theQueryMethodBindingNames          =False, 
    theQueryMethodBindingExtensionsNames=False,  
    theResolveMethodBindings            =False, 
    theRetrieveVoidParms                =False,):
    """Main service for rendering tabular views for manipulation of the objects network.

    Entry point invoked from a template, may be first to query the names of methods that can be customized, or to actually render the view.

    PUBLIC VIEW METHOD for Tabular renderings, allowing manipulation of elements to authoried users.
    Must be registered as an External method as:
        Id            MDDPresentationTabular
        Title         MDDPresentationTabular
        Module name   MDDPresentationTabular
        Function name MDDPresentationTabular

    """



    # #################################################################
    """Return the names of methods open for the caller to resolve by supplying a callable object like a external method, script, template, or python code.

    """    
    if theQueryMethodBindingNames:
        if cExtensionsForbidden:
            return []
        else:
            return _MDDInit_MethodBindings_Names()


    if theQueryMethodBindingExtensionsNames:
        if cExtensionsForbidden:
            return []
        else:
            return _MDDInit_MethodBindings_Extensions_Names()






    # #################################################################
    """Return a structure with parameters appropiate for this service, with void values.

    """    
    if theRetrieveVoidParms:
        return _fNewVoidViewParms_Tabular()








    # #################################################################
    """Create root render context.Initialize with received basic parameters. Initialize output streaming. 

    """
    aModelDDvlPloneTool = None
    aBrowsedElement     = None
    aRequest            = None

   
    if theInteractionCtxt == None:
 
        aModelDDvlPloneTool = theViewParms.get( 'theModelDDvlPloneTool', None)
        aBrowsedElement     = theViewParms.get( 'theBrowsedElement', None) 
        aRequest            = theViewParms.get( 'theRequest', None)    
        
        anOutput = StringIO( u'')
        aCallable_pO  = lambda theString: anOutput.write( theString)
        aCallable_pOL = lambda theString: anOutput.write( '%s\n' % theString)
        aCallable_pOS = lambda theString: anOutput.write( '%s\n' % '\n'.join( [ unaLine.strip() for unaLine in theString.splitlines()]))    
        
        someInitialParms = { } # do not add more parms that supplied, not even with null values _fNewVoidViewParms_Tabular()
        someInitialParms.update( theViewParms)
        someInitialParms.update( {
            'theViewParms':                 theViewParms,
            'theBeginTime':                 None,
            'theEndTime':                   None,
            'output':                       anOutput,
            'pO':                           aCallable_pO,
            'pOL':                          aCallable_pOL,
            'pOS':                          aCallable_pOS,      
        })
        aRdCtxt = fNewRenderContext( 
            theViewParms.get( 'theBrowsedElement', None),
            someInitialParms,
        )

    else:
        
        aRdCtxt = theInteractionCtxt.fNewCtxt( theViewParms)
            
        aModelDDvlPloneTool = aRdCtxt.fGP( 'theModelDDvlPloneTool', None)
        aBrowsedElement     = aRdCtxt.fGP( 'theBrowsedElement', None) 
        aRequest            = aRdCtxt.fGP( 'theRequest', None)    



    # #################################################################
    """Resolve methods with default or specified callable objects: default methods here, external methods, scripts, templates, or python code.

    """

    _MDDInit_MethodBindings( aRdCtxt)




    # #################################################################
    """May have been invoked not to render, but to obtain the resolved method bindings, to be cached by the caller (possibly a singleton tool fachade).

    """    
    if theResolveMethodBindings:
        return someMethodBindings




    anOk          = None
    aGo           = True
    unUnwindTrick = True
    while( unUnwindTrick):

        unUnwindTrick = False


        # #################################################################
        """Make sure essential parameters are supplied, or return an error page.

        """
        if not theViewParms:
            _MDDRender_EmptyPageContents(   
                aRdCtxt,
                aModelDDvlPloneTool.fTranslateI18N( theViewParms.get( 'theBrowsedElement', None), 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
                'theViewParms',
                None
            )
            break

        if not aModelDDvlPloneTool:
            _MDDRender_EmptyPageContents(   
                aRdCtxt, 
                aModelDDvlPloneTool.fTranslateI18N( theViewParms.get( 'theBrowsedElement', None), 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
                'theModelDDvlPloneTool',
                None
            )
            break

        if aBrowsedElement == None:
            _MDDRender_EmptyPageContents(   
                aRdCtxt, 
                aModelDDvlPloneTool.fTranslateI18N( theViewParms.get( 'theBrowsedElement', None), 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
                'theBrowsedElement',
                None
            )
            break

        if not aRequest:
            _MDDRender_EmptyPageContents(   
                aRdCtxt, 
                aModelDDvlPloneTool.fTranslateI18N(  theViewParms.get( 'theBrowsedElement', None), 'ModelDDvlPlone', cResultCondition_MissingParameter, cResultCondition_MissingParameter + '-'),
                'theRequest',
                None
            ) 
            break       




        # #################################################################
        """Begin Render Process.

        """
        aRdCtxt.pSP( 'theBeginRenderTime', fMillisecondsNow() )




        # #################################################################
        """First extension invoked (there are many below).

        """    
        if not cExtensionsForbidden:
            anOk, aGo = anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_Before')( aRdCtxt)
            if not aGo:
                break






        # #################################################################
        """Initialize parameters.

        """
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_InitParms_Before')( aRdCtxt)
            if not aGo:
                break
        anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDInit_Parms_Tabular')(         aRdCtxt)
        if not aGo:
            break
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_InitParms_After')(  aRdCtxt)
            if not aGo:
                break




        # ACV 20100611 Now done in MDDInteractionTabular such that translations are available to render clipboard and action results.
        ## #################################################################
        #"""Retrieve localizations for internationalized strings.

        #"""
        #if theRdCtxt.fGP( 'theUITranslations', None) == None:
            
            #if not cExtensionsForbidden:
                #anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_InitUITranslations_Before')(  aRdCtxt)
                #if not aGo:
                    #break
            #anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDInit_UITranslations_Tabular')(          aRdCtxt)
            #if not aGo:
                #break
            #if not cExtensionsForbidden:
                #anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_InitUITranslations_After')(   aRdCtxt)
                #if not aGo:
                    #break





        # #################################################################
        """Retrieve Presentation preferences

        """
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_RetrievePreferences_Before')(      aRdCtxt)
            if not aGo:
                break
        anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRetrieve_Preferences_Presentation_Tabular')( aRdCtxt)
        if not aGo:
            break
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_RetrievePreferences_After')(       aRdCtxt)
            if not aGo:
                break









        # #################################################################
        """Retrieve the information from the element, contents, related, and Plone elements, to render the view.

        """
        aRdCtxt.pSP( 'theRetrievalBeginTime', fMillisecondsNow(),)   

        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_Retrieval_Before')( aRdCtxt)
            if not aGo:
                break


        if aRdCtxt.fGP( 'theRelationCursorName', ''):
            anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRetrieve_Info_RelationCursor_Owner')(      aRdCtxt)
            if not aGo:
                break

        else:    
            anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRetrieve_Info_Tabular')(      aRdCtxt)
            if not aGo:
                break

            anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRetrieve_Info_Plone')(      aRdCtxt)
            if not aGo:
                break



        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_Retrieval_After')(  aRdCtxt)    
            if not aGo:
                break

        aRdCtxt.pSP( 'theRetrievalEndTime',   fMillisecondsNow(),)      





        # #################################################################
        """Render the view.

        """
        aRdCtxt.pSP( 'theRenderBeginTime',fMillisecondsNow(),) 


        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_Render_Tabular_Before')( aRdCtxt)
            if not aGo:
                break




        if aRdCtxt.fGP( 'theRelationCursorName', ''):
            anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRender_Tabular_Relation')(      aRdCtxt)
            if not aGo:
                break
        else:    
            anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRender_Tabular')(            aRdCtxt)
            if not aGo:
                break

        if not cExtensionsForbidden:
            if aRequest.get ( 'theCustom', None):
                anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRender_Customization_Form')( aRdCtxt)
                if not aGo:
                    break



        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_Render_Tabular_After')( aRdCtxt)  
            if not aGo:
                break



        aRdCtxt.pSP( 'theRenderEndTime', fMillisecondsNow(),) 






        # #################################################################
        """Process completed.

        """        
        aRdCtxt.pSP( 'theEndTime', fMillisecondsNow())




        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_After')( aRdCtxt)
            if not aGo:
                break






        # #################################################################
        """Append profiling information, if so configured.

        """

        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_RenderProfiling_Before')(   aRdCtxt)
            if not aGo:
                break
        anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRender_Tabular_Profiling')(           aRdCtxt)
        if not aGo:
            break
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_RenderProfiling_After')(    aRdCtxt)
            if not aGo:
                break






        # #################################################################
        """Produce the final output string.

        """
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_StripFinalOutput_Before')(    aRdCtxt)
            if not aGo:
                break

        anOk, aGo = _fMCtx( False, aRdCtxt, 'MDDRender_Tabular_StripFinalOutput')(      aRdCtxt)
        if not aGo:
            break

        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, aRdCtxt, 'MDDExtension_StripFinalOutput_After')(     aRdCtxt)
            if not aGo:
                break





    # #################################################################
    """Return the rendered string.

    """
    anOutputString = aRdCtxt.fGP( 'output_string', '')
    if not anOutputString:
        anOutput = aRdCtxt.fGP( 'output', None)
        if anOutput:
            anOutputString = anOutput.getvalue()
    if not anOutputString:
        anOutputString = ''

    return anOutputString







def _MDDRender_Tabular( theRdCtxt):

    # #################################################################
    """Render a tabular view on an object.

    """

    # #################################################################
    """Open Page

    """
    theRdCtxt.pOS( u"""     

                   <!-- #################################################################
                   PAGE WITH CONTENT: TABULAR view
                   ################################################################# -->
                   """)

    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Javascript')(                                 theRdCtxt)
    if not aGo:
        return [ True, aGo,]


    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_Before')(                theRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera')(                                 theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_After')(                 theRdCtxt)
        if not aGo:
            return [ True, aGo,]    





    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SectionsMenu_Before')( theRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_SectionsMenu')(        theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SectionsMenu_After')(  theRdCtxt)
        if not aGo:
            return [ True, aGo,] 




    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SiblingsMenu_Before')( theRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_SiblingsMenu')(        theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SiblingsMenu_After')(  theRdCtxt)
        if not aGo:
            return [ True, aGo,] 




    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Values_Before')(                theRdCtxt)
        if not aGo:
            return [ True, aGo,]    
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Values')(                                   theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Values_After')(                 theRdCtxt)
        if not aGo:
            return [ True, aGo,]    




    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Texts_Before')(                   theRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Texts')(                                    theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Texts_After')(                    theRdCtxt)
        if not aGo:
            return [ True, aGo,]



    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_CustomPresentationViews_Before')( theRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_CustomPresentationViews')(                  theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_CustomPresentationViews_After')(  theRdCtxt)
        if not aGo:
            return [ True, aGo,]



    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Traversals_Before')(              theRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Traversals')(                               theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Traversals_After')(               theRdCtxt)
        if not aGo:
            return [ True, aGo,]



    #anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_GenericReferences_Before')(       theRdCtxt)
    #if not aGo:
        #return [ True, aGo,]
    #anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_GenericReferences')(                        theRdCtxt)
    #if not aGo:
        #return [ True, aGo,]
    #anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_GenericReferences_After')(        theRdCtxt)
    #if not aGo:
        #return [ True, aGo,]



    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Plone_Before')(                   theRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Plone')(                                    theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Plone_After')(                    theRdCtxt)
        if not aGo:
            return [ True, aGo,]

    return [ True, aGo,]






def _MDDRender_Customization_Form( theRdCtxt):
    return [ True, True,]






def _MDDInit_Parms_Tabular( theRdCtxt):
    """Initialize caches if not supplied by service caller

    """

    aViewParms = theRdCtxt.fGP( 'theViewParms', None)
    if not aViewParms:
        return [ False, False, ]


    # #################################################################
    aMetaTranslationsCaches = theRdCtxt.fGP( 'theTranslationsCache', None)
    aPermissionsCache       = theRdCtxt.fGP( 'thePermissionsCache',  None)
    aRolesCache             = theRdCtxt.fGP( 'theRolesCache',        None)
    if ( aMetaTranslationsCaches == None) or (aPermissionsCache == None) or ( aRolesCache == None):
        aModelDDvlPloneTool_Retrieval = theRdCtxt.fGP( 'theModelDDvlPloneTool', None).fModelDDvlPloneTool_Retrieval( theRdCtxt.fGP( 'theBrowsedElement', None))

        if ( aMetaTranslationsCaches == None):
            aMetaTranslationsCaches =  aModelDDvlPloneTool_Retrieval.fCreateTranslationsCaches()

        if ( aPermissionsCache == None):
            aPermissionsCache =        aModelDDvlPloneTool_Retrieval.fCreateCheckedPermissionsCache()

        if ( aRolesCache == None):
            aRolesCache =              aModelDDvlPloneTool_Retrieval.fCreateRolesCache()


    anExtraLinkHrefParams = ''
    # ACV 20100226 No longer keeping the no cache params from request to request
    #if aViewParms.get( 'theRequest', {}).get( 'theNoCache', ''):
        #anExtraLinkHrefParams = '%s%s%s' % ( anExtraLinkHrefParams,  ((anExtraLinkHrefParams and '&') or ''), 'theNoCache=on')

    #aNoCacheId = aViewParms.get( 'theRequest', {}).get( 'theNoCacheCode', '')
    #if aNoCacheId :
        #anExtraLinkHrefParams = '%s%s%s' % ( anExtraLinkHrefParams, ((anExtraLinkHrefParams and '&') or ''), 'theNoCacheCode=%s' % aNoCacheId )


    theRdCtxt.pSPs( {
        'theEndTime':                   None,
        'theActionsBeginTime':          None,
        'theActionsEndTime':            None,
        'theRetrievalBeginTime':        None,
        'theRetrievalEndTime':          None,
        'theRenderBeginTime':           None,
        'theRenderEndTime':             None,

        'thePerformanceAnalysis':       aViewParms.get( 'thePerformanceAnalysis',None),
        'theTraversalName':             aViewParms.get( 'theTraversalName',      None),
        'theRelationCursorName':        aViewParms.get( 'theRelationCursorName', None),
        'theCurrentElementUID':         aViewParms.get( 'theCurrentElementUID',  None),


        'theClearClipboard':            aViewParms.get( 'theClearClipboard',     None),
        'thePasteRequested':            aViewParms.get( 'thePasteRequested',     None),
        'theGroupAction':               aViewParms.get( 'theGroupAction',        None),
        'theUIDs':                      aViewParms.get( 'theUIDs',               None),
        'theMovedElementID':            aViewParms.get( 'theMovedElementID',     None),
        'theMoveDirection':             aViewParms.get( 'theMoveDirection',      None),
        'theMovedReferenceUID':         aViewParms.get( 'theMovedReferenceUID',  None),
        'theMovedObjectUID':            aViewParms.get( 'theMovedObjectUID',     None),

        'theAdditionalParms':           aViewParms.get( 'theAdditionalParms',    None),

        'theMetaTranslationsCaches':    aMetaTranslationsCaches,
        'thePermissionsCache':          aPermissionsCache,
        'theRolesCache':                aRolesCache,
        'theUITranslations':            theRdCtxt.fGP( 'theUITranslations', { }),
        'theExtraLinkHrefParams':       anExtraLinkHrefParams,
        'theExtraLinkHrefParamsFirst':  ( anExtraLinkHrefParams and ('?%s' % anExtraLinkHrefParams)) or '',
        'theExtraLinkHrefParamsCont':   ( anExtraLinkHrefParams and ('&%s' % anExtraLinkHrefParams)) or '',
    })

    return [ True, True,]








# #######################################################################
""" RETRIEVAL METHOD FOR PRESENTATION PREFERENCES.

"""


def _MDDRetrieve_Preferences_Presentation_Tabular( theRdCtxt):

    theRdCtxt.pSP( 'PREFS_PRES', {})

    if True:
        return [ True, True,]

    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return [ False, False,]

    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return [ False, False,]

    aBeginTime  = fMillisecondsNow()

    aPresentationPreferences = aModelDDvlPloneTool.fRetrievePreferences( 
        theTimeProfilingResults     =None,
        theElement                  =aContainerObject, 
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='Tabular', 
        thePreferencesExtents       = [ 'presentation'],
        theTranslationsCaches       =None,
        theCheckedPermissionsCache  =None,
        theAdditionalParams         =None
    )

    anEndTime  = fMillisecondsNow()

    theRdCtxt.pSP( 'PREFS_PRES', aPresentationPreferences)


    theRdCtxt.pAppendRetrievalResult( {
        'subject':      'PREFS_PRES',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
    })

    return [ True, True,]








# #######################################################################
""" RETRIEVAL METHOD FOR ELEMENTS TRAVERSAL DATA, METAINFO, TRANSLATIONS and CLIPBOARD.

"""








def _MDDRetrieve_Info_Tabular( theRdCtxt):


    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return [ False, False,]

    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return [ False, False,]

    aBeginTime  = fMillisecondsNow()

    aSRES = aModelDDvlPloneTool.fRetrieveTypeConfig( 
        theTimeProfilingResults     =None,
        theElement                  =aContainerObject, 
        theParent                   =None,
        theParentTraversalName      ='',
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='Tabular', 
        theRetrievalExtents         =[ 'traversals', 'owner', 'cursor', 'extra_links',],
        theWritePermissions         =[ 'object', 'aggregations', 'relations', 'add', 'delete', 'add_collection', ],
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =theRdCtxt.fGP( 'theMetaTranslationsCaches', None),
        theCheckedPermissionsCache  =theRdCtxt.fGP( 'thePermissionsCache', None),
        theAdditionalParams         =theRdCtxt.fGP( 'theAdditionalParms', None),
    )

    anEndTime  = fMillisecondsNow()

    theRdCtxt.pSP( 'SRES', aSRES)


    theRdCtxt.pAppendRetrievalResult( {
        'subject':      'SRES',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
    })

    return [ True, True,]







def _MDDRetrieve_Info_Plone( theRdCtxt):


    aSRES =     theRdCtxt.fGP( 'SRES', None)
    if not aSRES:
        return [ False, False,]

    aContainerObject =     aSRES.get( 'object', None)
    if aContainerObject == None:
        return [ False, False,]

    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return [ False, False,]

    aBeginTime  = fMillisecondsNow()

    aSRES = aModelDDvlPloneTool.fRetrievePloneContent( 
        theTimeProfilingResults     =None,
        theContainerElement         =aContainerObject, 
        thePloneSubItemsParameters  =None, 
        theRetrievalExtents         =[ 'traversals', ],
        theWritePermissions         =[ 'object', 'aggregations', 'add', 'plone', 'delete_plone', ],
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =theRdCtxt.fGP( 'theMetaTranslationsCaches', None),
        theCheckedPermissionsCache  =theRdCtxt.fGP( 'thePermissionsCache', None),
        theAdditionalParams         =theRdCtxt.fGP( 'theAdditionalParms', None),
    )

    anEndTime  = fMillisecondsNow()

    theRdCtxt.pSP( 'PLONERES', aSRES)


    theRdCtxt.pAppendRetrievalResult( {
        'subject':      'PLONERES',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
    })

    return [ True, True,]









def _MDDRetrieve_Info_RelationCursor_Owner( theRdCtxt):


    aContainerObject =     theRdCtxt.fGP( 'theBrowsedElement', None)
    if aContainerObject == None:
        return [ False, False,]

    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return [ False, False,]

    aRelationCursorName = theRdCtxt.fGP( 'theRelationCursorName', '')
    if not aRelationCursorName:
        return [ False, False,]

    aBeginTime  = fMillisecondsNow()

    aSRES = aModelDDvlPloneTool.fRetrieveTypeConfig( 
        theTimeProfilingResults     =None,
        theElement                  =aContainerObject, 
        theParent                   =None,
        theParentTraversalName      ='',
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='Tabular', 
        theRetrievalExtents         =[ 'traversals', 'owner', 'cursor', 'extra_links', 'relation_cursors', ],
        theWritePermissions         =[ 'object', 'aggregations', 'relations', 'add', 'delete', 'add_collection', ],
        theFeatureFilters           ={ 'attrs': [], 'aggregations': [], 'relations': [ aRelationCursorName, ],}, 
        theInstanceFilters          =None,
        theTranslationsCaches       =theRdCtxt.fGP( 'theMetaTranslationsCaches', None),
        theCheckedPermissionsCache  =theRdCtxt.fGP( 'thePermissionsCache', None),
        theAdditionalParams         =theRdCtxt.fGP( 'theAdditionalParms', None),
    )

    anEndTime  = fMillisecondsNow()

    theRdCtxt.pSP( 'SRES', aSRES)

    theRdCtxt.pAppendRetrievalResult( {
        'subject':      'SRES',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
    })

    if not aSRES:
        return [ False, False, ]

    return [ True, True,]










def _MDDRetrieve_Info_RelationCursor_Current( theRdCtxt):


    aRELRES =  theRdCtxt.fGP( 'SRES', None)
    if not aRELRES:
        return [ False, False,]

    theRdCtxt.pSP( 'RELRES', aRELRES)

    aModelDDvlPloneTool =  theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return [ False, False,]

    aRelationCursorName = theRdCtxt.fGP( 'theRelationCursorName', '')
    if not aRelationCursorName:
        return [ False, False,]

    aCurrentElementUID = theRdCtxt.fGP( 'theCurrentElementUID', '')

    aTRAVRES = aRELRES.get( 'traversals_by_name', {}).get( aRelationCursorName, None)  
    if not aTRAVRES:
        return [ False, False, ]

    if not ( aTRAVRES.get( 'traversal_kind', '') == 'relation'):
        return [ False, False, ]

    theRdCtxt.pSP( 'TRAVRES', aTRAVRES)


    aCurrentElementResult = None
    if aCurrentElementUID:
        someElementsByUID = aTRAVRES.get( 'elements_by_UID', {})
        aCurrentElementResult = someElementsByUID.get( aCurrentElementUID, None)            
    else:
        someElements = aTRAVRES.get( 'elements', [])
        if someElements:
            aCurrentElementResult = someElements[ 0]

    if not aCurrentElementResult:
        return [ True, True,]

    aCurrentElement = aCurrentElementResult.get( 'object', None)
    if ( aCurrentElement == None):
        return [ True, True,]


    aBeginTime  = fMillisecondsNow()

    aSRES = aModelDDvlPloneTool.fRetrieveTypeConfig( 
        theTimeProfilingResults     =None,
        theElement                  =aCurrentElement, 
        theParent                   =None,
        theParentTraversalName      ='',
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theViewName                 ='Tabular', 
        theRetrievalExtents         =[ 'traversals', 'owner', 'extra_links',],
        theWritePermissions         =[ 'object', 'aggregations', 'relations', 'add', 'delete', 'add_collection', ],
        theFeatureFilters           =None, 
        theInstanceFilters          =None,
        theTranslationsCaches       =theRdCtxt.fGP( 'theMetaTranslationsCaches', None),
        theCheckedPermissionsCache  =theRdCtxt.fGP( 'thePermissionsCache', None),
        theAdditionalParams         =theRdCtxt.fGP( 'theAdditionalParms', None),
    )

    anEndTime  = fMillisecondsNow()

    aSRES.update( { 'cursor': aCurrentElementResult[ 'cursor'], 'owner_element': aRELRES, 'container_element': aRELRES, })   

    theRdCtxt.pSP( 'SRES', aSRES)


    theRdCtxt.pAppendRetrievalResult( {
        'subject':      'SRES',
        'begin_time':   aBeginTime,
        'end_time':     anEndTime,
    })

    return [ True, True,]




















# #######################################################################
""" RENDERING METHODS.

"""




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

    return [ True, True,]








def _MDDRender_Tabular_Relation( theRdCtxt):
    """Render a tabular view with the header for an element and the detail of one of its related elements.

    """

    # #################################################################
    """Render a tabular view on an object.

    """

    # #################################################################
    """Open Page

    """
    theRdCtxt.pOS( u"""     

                   <!-- #################################################################
                   PAGE WITH CONTENT: TABULAR view
                   ################################################################# -->
                   """)

    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Javascript')(                                 theRdCtxt)
    if not aGo:
        return [ True, aGo,]


    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_Before')(                theRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera')(                                 theRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_After')(                 theRdCtxt)
        if not aGo:
            return [ True, aGo,]    





    #anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SectionsMenu_Before')( theRdCtxt)
    #if not aGo:
        #return [ True, aGo,]
    #anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_SectionsMenu')(        theRdCtxt)
    #if not aGo:
        #return [ True, aGo,]
    #anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SectionsMenu_After')(  theRdCtxt)
    #if not aGo:
        #return [ True, aGo,] 




    #anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SiblingsMenu_Before')( theRdCtxt)
    #if not aGo:
        #return [ True, aGo,]
    #anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_SiblingsMenu')(        theRdCtxt)
    #if not aGo:
        #return [ True, aGo,]
    #anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SiblingsMenu_After')(  theRdCtxt)
    #if not aGo:
        #return [ True, aGo,] 












    aCurrentRdCtxt = theRdCtxt.fNewCtxt( )
    anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDRetrieve_Info_RelationCursor_Current')(   aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]


    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRetrieve_Info_Plone')(      aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]



    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_Relation_Cabecera_Before')(   aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_Relation_Cabecera')(                   aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_Relation_Cabecera_After')(    aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]    





    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_SectionsMenu_Before')( aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_SectionsMenu')(        aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_SectionsMenu_After')(  aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,] 




    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_SiblingsMenu_Before')( aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_SiblingsMenu')(        aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_SiblingsMenu_After')(  aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,] 







    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Values_Before')(               aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]    
    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_Values')(                       aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Values_After')(                aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]    




    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_Texts_Before')(                   aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_Texts')(                                    aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_Texts_After')(                    aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]



    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_CustomPresentationViews_Before')( aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_CustomPresentationViews')(                  aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_CustomPresentationViews_After')(  aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]



    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_Traversals_Before')(              aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_Traversals')(                               aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_Traversals_After')(               aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]



    #anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_GenericReferences_Before')(       aCurrentRdCtxt)
    #if not aGo:
        #return [ True, aGo,]
    #anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_GenericReferences')(                        aCurrentRdCtxt)
    #if not aGo:
        #return [ True, aGo,]
    #anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_GenericReferences_After')(        aCurrentRdCtxt)
    #if not aGo:
        #return [ True, aGo,]



    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_Plone_Before')(                   aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]
    anOk, aGo = _fMCtx( False, aCurrentRdCtxt, 'MDDRender_Tabular_Plone')(                                    aCurrentRdCtxt)
    if not aGo:
        return [ True, aGo,]
    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, aCurrentRdCtxt, 'MDDExtension_Render_Tabular_Plone_After')(                    aCurrentRdCtxt)
        if not aGo:
            return [ True, aGo,]

    return [ True, aGo,]












def MDDPresentationActionsResults( theRdCtxt):

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
                anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_RefactorResultsDump')( theRdCtxt, anActionResult)


            if anAction == 'Clear Clipboard':
                pass

            if anAction == 'Move':
                pass

            if anAction == 'Delete':
                pass

    return [ True, True,]









def MDDPresentationClipboard( theRdCtxt):

    """Main service for rendering tabular views for manipulation of the objects network.

    Entry point invoked from external methods MDDInteractionTabular or MDDInteractionTextual.

    PUBLIC VIEW METHOD for Tabular renderings, allowing manipulation of elements to authoried users.
    Must be registered as an External method as:
        Id            MDDPresentationClipboard
        Title         MDDPresentationClipboard
        Module name   MDDPresentationTabular
        Function name MDDPresentationClipboard

    """

    anOutput = theRdCtxt.fGP( 'output', None)
    if anOutput == None:
        return None
    
    aModelDDvlPloneTool = theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return None

    aClipboardResult = theRdCtxt.fGP( 'clipboard_result', {})
    if not aClipboardResult:
        return None

    aBrowsedElement = theRdCtxt.fGP( 'theBrowsedElement', None)
    if aBrowsedElement == None:
        return None



    someElementsByRoot = aClipboardResult[ 'elements_by_roots']
    aNumElementsByRoot  = len( someElementsByRoot )
    if not aNumElementsByRoot:
        return None


    anOutput.write( """
    <!-- ######### Start collapsible  section ######### --> 
    <dl id="cid_MDDClipboardCollapsibleSection" class="collapsible inline collapsedInlineCollapsible" >
        <dt class="collapsibleHeader">
                <img alt="%(pClipboardContentsTitle)s" title="%(pClipboardContentsTitle)s" id="icon-clipboard" src="%(portal_url)s/portapapeles.gif" />
                <strong>%(pClipboardContentsTitle)s</strong>        
        </dt>
        <dd class="collapsibleContent">    
            <a class="state-visible" id="cid_ClipboardClear" href="%(SRES-url)s/Tabular/?theClearClipboard=on%(theExtraLinkHrefParams)s">

                    <strong>%(ModelDDvlPlone_Clipboard_Clear_action)s</strong>
            </a>
            <br/>
    """ % {
            'portal_url':                            aClipboardResult[ 'portal_url'],
            'pClipboardContentsTitle':               theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_Title'),
            'ModelDDvlPlone_Clipboard_Clear_action': theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_Clear_action'),
            'SRES-url':                              aBrowsedElement.absolute_url(),            
            'theExtraLinkHrefParams':                theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
        })



    if not aNumElementsByRoot:
        anOutput.write("""
        <p>
            <font size="2">ModelDDvlPlone_Clipboard_Empty</font> 
        </p>
        """ % {
                'ModelDDvlPlone_Clipboard_Empty':   theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_Empty'),
            })

    else:    
        anOutput.write( """
        <p>
        """)

    if aClipboardResult.get( 'is_move_operation', False):
        anOutput.write( """
        <font size="2">
        <strong>%(ModelDDvlPlone_Clipboard_ElementsWereCut)s</strong>
        </font>
        """ %  {
                'ModelDDvlPlone_Clipboard_ElementsWereCut': theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_ElementsWereCut'),
            })
    else:
        anOutput.write( """
        <font size="2">
        <strong>%(ModelDDvlPlone_Clipboard_ElementsWereCopied)s</strong>
        </font>
        """ %  {
                'ModelDDvlPlone_Clipboard_ElementsWereCopied': theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_ElementsWereCopied'),
            })

    anOutput.write( """
    </p>
    """)





    anOutput.write( """
    <p>
        <span>%(ModelDDvlPlone_Clipboard_ContentsFrom)s</span>
        &emsp;
    """  %  {
             'ModelDDvlPlone_Clipboard_ContentsFrom': theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_ContentsFrom'),
         })



    if aClipboardResult.get( 'has_same_root_as_context', False):

        anOutput.write("""
        <span>%(ModelDDvlPlone_Clipboard_ContentsSameRoot)s</span>
        """ %  {
                'ModelDDvlPlone_Clipboard_ContentsSameRoot': theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_ContentsSameRoot'),
            })



    if aClipboardResult.get( 'num_other_roots', False):
        if aClipboardResult.get( 'has_same_root_as_context', False):
            anOutput.write("""
            <span>%(ModelDDvlPlone_and)s</span>
            """ %  {
                    'ModelDDvlPlone_and': theRdCtxt.fUITr( 'ModelDDvlPlone_and'),
                })

        anOutput.write("""
        <span>%(ModelDDvlPlone_Clipboard_ContentsOtherRoots)s</span>
        """%  {
               'ModelDDvlPlone_Clipboard_ContentsOtherRoots': theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_ContentsOtherRoots'),
           })

    if aClipboardResult.get( 'num_unsupported_roots', False):
        if aClipboardResult.get( 'has_same_root_as_context', False) or aClipboardResult.get( 'num_other_roots', False):
            anOutput.write("""
            <span>%(ModelDDvlPlone_and)s</span>
            """ %  {
                    'ModelDDvlPlone_and': theRdCtxt.fUITr( 'ModelDDvlPlone_and'),
                })

            anOutput.write("""
            <span>%(ModelDDvlPlone_Clipboard_ContentsFromOutsideOfApplicationRoots)s</span>
            """%  {
                   'ModelDDvlPlone_Clipboard_ContentsFromOutsideOfApplicationRoots': theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_ContentsFromOutsideOfApplicationRoots'),
               })

    anOutput.write("""
    </p>
    """)



    anOutput.write("""
    <p>
        <font size="2">%(ModelDDvlPlone_Clipboard_NumElements)s %(num_elements)d,  %(ModelDDvlPlone_Clipboard_NumContainedElements)s %(num_contained_elements)d, %(ModelDDvlPlone_Clipboard_TotalElements)s %(total_elements)d</font> 
    </p>
    """ % {
            'ModelDDvlPlone_Clipboard_NumElements':          theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_NumElements'),
            'ModelDDvlPlone_Clipboard_NumContainedElements': theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_NumContainedElements'),
            'ModelDDvlPlone_Clipboard_TotalElements':        theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_TotalElements'),
            'num_elements':                                  aClipboardResult[ 'num_elements'],
            'num_contained_elements':                        aClipboardResult[ 'num_contained_elements'],
            'total_elements':                                aClipboardResult[ 'total_elements'],
        })


    for aClipboardResultForOneRoot in someElementsByRoot:
        if aClipboardResultForOneRoot:

            someClipboardElements = aClipboardResultForOneRoot['elements']
            someColumnNames       = [ aValueResult['attribute_name']                              for aValueResult in someClipboardElements[0]['values'] ]
            someColumnLabels      = [ aValueResult[ 'attribute_translations']['translated_label'] for aValueResult in someClipboardElements[0]['values'] ]; 

            if someClipboardElements:

                anOutput.write("""
                <table width="100%%" id="cid_ClipboardElements" class="listing" summary="%(pClipboardContentsTitle)s" > 
                    <thead>
                        <tr>
                            <th width="80" class="sortable" align="right">%(ModelDDvlPlone_Clipboard_NumContainedElements)s</th>
                            <th class="sortable" align="left">%(ModelDDvlPlone_tipo_label)s</th>
                """ % {
                        'pClipboardContentsTitle':    theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_Title'),
                        'ModelDDvlPlone_Clipboard_NumContainedElements':  theRdCtxt.fUITr( 'ModelDDvlPlone_Clipboard_NumContainedElements'),
                        'ModelDDvlPlone_tipo_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_tipo_label'),

                    })


                for aColumnLabel in someColumnLabels:
                    anOutput.write("""
                        <th class="sortable" align="left" >%(aColumnLabel)s</th>
                    """ % {
                            'aColumnLabel':  aColumnLabel,

                        })


                anOutput.write("""
                    <th class="sortable" align="left" >%(ModelDDvlPlone_Path_label)s</th>
                </thead>
                <tbody>
                """ % {
                        'ModelDDvlPlone_Path_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_Path_label'),
                    })



                unIndexClassFila = 0
                for aClipboardElementResult in someClipboardElements:
                    anOutput.write("""
                    <tr class="%(RowClass)s">   
                        <td align="right" >%(num_contained)d</td>
                        <td align="left">
                            <span>%(translated_archetype_name)s</span>
                        </td>""" % {
                                     'ModelDDvlPlone_Path_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_Path_label'),
                                     'RowClass':                   cClasesFilas[ unIndexClassFila % 2],
                                     'num_contained':              aClipboardElementResult[ 'num_contained'],
                                     'translated_archetype_name':  aClipboardElementResult['type_translations']['translated_archetype_name'],

                                 })


                    for aColumnName in someColumnNames:
                        if aColumnName == 'title':

                            anOutput.write("""
                            <td align="left" >
                                <a class="state-visible" id="cid_ClipboardElement_%(RowIndex)d" href="%(SRES-url)s%(theExtraLinkHrefParams)s" >
                                    <img alt="%(SRES-title)s" title="%(SRES-title)s" id="cid_ClipboardElement_%(RowIndex)d_Icon"  
                                        src="%(portal_url)s/%(content_icon)s"/>
                                    &ensp;
                                    <span>%(aColumnValue)s</span>
                                </a>
                            </td>
                            """ % {
                                    'RowIndex':      unIndexClassFila,
                                    'aColumnName':   aColumnName,
                                    'aColumnValue':  fCGIE( aClipboardElementResult['values_by_name'][ aColumnName]['translated_value']),
                                    'SRES-url':      aClipboardElementResult[ 'url'],
                                    'SRES-title':    fCGIE( aClipboardElementResult['values_by_name'][ 'title'][ 'uvalue']),
                                    'portal_url':    aClipboardResult[ 'portal_url'],
                                    'content_icon':  aClipboardElementResult[ 'content_icon'],
                                    'theExtraLinkHrefParams':  theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                })
                        else:
                            anOutput.write("""
                            <td align="left" >%(aColumnValue)s</td>
                            """ % {
                                    'aColumnValue':  aClipboardElementResult['values_by_name'][aColumnName]['translated_value'],
                                })

                anOutput.write("""
                    <td align="left" >%(SRES-path)s</td>
                    """ % {
                            'SRES-path':  aClipboardElementResult['path'],
                        })

                unIndexClassFila += 1


            anOutput.write("""
                </tbody>
            </table>
            """ )


    anOutput.write("""
        </dd>
    </dl>
    <br/>
    """)


    return [ True, True,]








def _MDDRender_Tabular_RefactorResultsDump( theRdCtxt, theRefactorReport):

    if not theRefactorReport:
        return [ True, True,]

    aRefactorLabel = 'Paste'
    aRefactorLabelI18N = theRdCtxt.fUITr( 'ModelDDvlPlone_refactor_' + aRefactorLabel)


    if theRefactorReport.get( 'success', False) and ( theRefactorReport.get( 'num_elements_pasted', 0) or theRefactorReport.get( 'num_mdd_elements_pasted ', 0) or theRefactorReport.get( 'num_plone_elements_pasted ', 0) or theRefactorReport.get( 'num_attributes_pasted  ', 0) or theRefactorReport.get( 'num_links_pasted ', 0)):
        theRdCtxt.pOS( """
        <div class="portalMessage" >
            <p><font color="green" size="2"><strong>%(aRefactorLabelI18N)s %(ModelDDvlPlone_success)s</strong></font></p>
        """ % {
                'aRefactorLabelI18N':          aRefactorLabelI18N,
                'ModelDDvlPlone_success':      theRdCtxt.fUITr( 'ModelDDvlPlone_success'),
            })

        aStatus =  theRefactorReport.get( 'status', '').strip()
        if aStatus:
            theRdCtxt.pOS( """
            <div><strong>%(ModelDDvlPlone_paste_status)s %(aStatus)s</strong></div>
            """ % {
                    'aStatus':                          aStatus,
                    'ModelDDvlPlone_paste_status':      theRdCtxt.fUITr( 'ModelDDvlPlone_paste_status'),
                })

        aCondition =  theRefactorReport.get( 'condition', '').strip()
        if aCondition:
            theRdCtxt.pOS( """
            <div><strong>%(ModelDDvlPlone_paste_status)s %(aCondition)s</strong></div>
            """ % {
                    'aStatus':                          aStatus,
                    'ModelDDvlPlone_paste_condition':   theRdCtxt.fUITr( 'ModelDDvlPlone_paste_condition'),
                })

        aException =  theRefactorReport.get( 'exception', '').strip()
        someExceptionLines = aException.splitlines()
        aNumExceptionLines = max( min( len( someExceptionLines), 18), 3)
        if aException and someExceptionLines:
            theRdCtxt.pOS( """
                <p><strong>%(ModelDDvlPlone_exception)s</strong></p>
                <textarea style="font-size: 9pt;" cols="80" rows="%(aNumExceptionLines)d" name="MDDExceptionDump" id="cid_MDDExceptionDump" >
            """ % {
                    'aNumExceptionLines':                          aNumExceptionLines,
                    'ModelDDvlPlone_exception':   theRdCtxt.fUITr( 'ModelDDvlPlone_exception'),
                })

            for aLineIndex in range( aNumExceptionLines):
                aLine = someExceptionLines[ aLineIndex]
                theRdCtxt.pOL( aLine)

            theRdCtxt.pOS( """
            </textarea>
            <br/>
            """)

        someErrorReports =  theRefactorReport.get( 'error_reports', [])
        if someErrorReports:
            unasClasesFiles = ('odd','even')
            unIndexClassFila = 0
            theRdCtxt.pOS( """
            <table id="cid_MDDTablaRefactorErrorReports" class="listing" summary="MDDTablaRefactorErrorReports"            
                <thead>
                    <tr>
                        <th class="nosort">%(ModelDDvlPlone_class_name)s</th>
                        <th class="nosort">%(ModelDDvlPlone_method_name)s</th>
                        <th class="nosort">%(ModelDDvlPlone_error_status)s</th>
                        <th class="nosort">%(ModelDDvlPlone_error_reason)s</th>
                    </tr>
                </thead>
                <tbody>
            """ % {
                    'ModelDDvlPlone_class_name':     theRdCtxt.fUITr( 'ModelDDvlPlone_class_name'),
                    'ModelDDvlPlone_method_name':    theRdCtxt.fUITr( 'ModelDDvlPlone_method_name'),
                    'ModelDDvlPlone_error_status':   theRdCtxt.fUITr( 'ModelDDvlPlone_error_status'),
                    'ModelDDvlPlone_error_reason':   theRdCtxt.fUITr( 'ModelDDvlPlone_error_reason'),
                })

            for unIndexReport in range( len( someErrorReports)):
                anErrorReport = someErrorReports[ aunIndexReport]
                theRdCtxt.pOS( """
                <tr class="%(row-class)s">
                    <td>%(theclass)s</td>
                    <td>%(method)s</td>
                    <td>%(status)s</td>
                    <td>%(reason)s</td>
                </tr>
                """ % {
                        'row-class':         cClasesFilas[ unIndexReport % 2],
                        'theclass':          anErrorReport.get( 'theclass', ''),
                        'method':            anErrorReport.get( 'method', ''),
                        'status':            anErrorReport.get( 'status', ''),
                        'reason':            anErrorReport.get( 'reason', ''),
                    })

                someErrorParams = anErrorReport.get( 'params', {})
                someErrorParamsKeys = someErrorParams.keys()[:]
                if someErrorParamsKeys:
                    someErrorParamsKeys.sort()
                    theRdCtxt.pOS( """
                    <tr "%(row-class)s">
                        <td colspan="4">
                            <table width="100%">
                                <tbody>
                    """ % {
                            'row-class':         cClasesFilas[ unIndexReport % 2],
                        })

                    for anErrorParamKey in someErrorParamsKeys:
                        #aTranslatedErrorParamKey = theRdCtxt.fUITr( 'ModelDDvlPlone_refactor_error_param_' + anErrorParamKey)
                        theRdCtxt.pOS( """
                        <tr>
                            <td>%(anErrorParamKey)s</td>
                            <td>%(anErrorParam)s</td>
                        </tr>
                        """ % {
                                'anErrorParamKey': anErrorParamKey,
                                'anErrorParam':    someErrorParams.get( anErrorParamKey, ''),
                            })

                    theRdCtxt.pOS( """
                                </tbody>
                            </table>
                        </td>
                    </tr>
                    """)

    #else:


    return [ True, True,]





def _MDDRender_Tabular_SectionsMenu( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    aPLONERES = theRdCtxt.fGP( 'PLONERES', {})


    theRdCtxt.pOS( u"""
                   &emsp;
                   <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="bottom">
                   """
                   )

    theRdCtxt.pOS( u"""
                   <dl class="actionMenu deactivated" id="cid_MDDSectionList_ActionsMenu" style="padding: 0 0 0 0 !important" ><font style="font-size: 0px" >
                   <!-- <dt class="actionMenuHeader" style="display: inline">
                   <a>
                   %(ModelDDvlPlone_Tabular_Sections)s
                   </a>
                   </dt>
                   -->
                   <dd class="actionMenuContent" style="left: 1px; top: -1em;">
                   <font size="1" style="font-size: 1en" >
                   <ul>

                   """ % {
                           'portal_url':                        aSRES[ 'portal_url'],
                           'ModelDDvlPlone_Tabular_Sections':   theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                       })   



    anOwnerElement    = aSRES[ 'owner_element']
    aContainerElement = aSRES[ 'container_element']

    if not ( anOwnerElement == None):

        unTituloEnlace = '%s %s %s %s' % ( 
            anOwnerElement[ 'type_translations'][ 'translated_archetype_name'], 
            anOwnerElement[ 'values_by_name'][ 'title'][ 'uvalue'], 
            anOwnerElement[ 'values_by_name'][ 'description'][ 'uvalue'], 
            anOwnerElement[ 'type_translations'][ 'translated_type_description'],
        )

        aMenuItemLabel = fCGIE( anOwnerElement['values_by_name'][ 'title'][ 'uvalue'])
        aLenMenuItem = len( aMenuItemLabel)
        if aLenMenuItem > cPref_Pres_SectionsMenu_Item_MaxLength:
            aMenuItemLabel = '%s%s' % ( aMenuItemLabel[:cPref_Pres_SectionsMenu_Item_MaxLength], cPref_Pres_SectionsMenu_Item_MaxLengthExceeded_Postfix,)

        theRdCtxt.pOS( u"""
                       <li >
                       <a id="cid_MDDTOC_Link_Propietario"  title="%(unTituloEnlace)s " 
                       href="%(OWNER-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_title"   
                       onclick="hideAllMenus(); return true;">
                       <img src="%(portal_url)s/propietario.gif" title="%(unTituloEnlace)s" alt="%(OWNER-title)s" id="icon-owner" />
                       <img src="%(portal_url)s/%(OWNER_icon)s"  title="%(unTituloEnlace)s" alt="%(OWNER-title)s" id="icon-owner" />
                       <span style="color: black">%(aMenuItemLabel)s</span>
                       </a>
                       </li>
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'OWNER-title':                 aMenuItemLabel,
                               'aMenuItemLabel':              aMenuItemLabel,
                               'OWNER-url':                   anOwnerElement[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'OWNER_icon':                  anOwnerElement[ 'content_icon'],
                               'translated_archetype_name':   anOwnerElement[ 'type_translations']['translated_archetype_name'],
                               'translated_type_description': anOwnerElement[ 'type_translations']['translated_type_description'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           })




    if not ( aContainerElement == None) and ( anOwnerElement and not ( aContainerElement == anOwnerElement)):

        unTituloEnlace = '%s %s %s %s' % ( 
            aContainerElement[ 'type_translations'][ 'translated_archetype_name'], 
            aContainerElement[ 'values_by_name'][ 'title'][ 'uvalue'], 
            aContainerElement[ 'values_by_name'][ 'description'][ 'uvalue'], 
            aContainerElement[ 'type_translations'][ 'translated_type_description'],
        )

        aMenuItemLabel = fCGIE( aContainerElement['values_by_name'][ 'title'][ 'uvalue'])
        aLenMenuItem = len( aMenuItemLabel)
        if aLenMenuItem > cPref_Pres_SectionsMenu_Item_MaxLength:
            aMenuItemLabel = '%s%s' % ( aMenuItemLabel[:cPref_Pres_SectionsMenu_Item_MaxLength], cPref_Pres_SectionsMenu_Item_MaxLengthExceeded_Postfix,)

        theRdCtxt.pOS( u"""
                       <li>
                       <a id="cid_MDDTOC_Link_Contenedor"  title="%(unTituloEnlace)s " 
                       href="%(CONTAINER-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_title"  
                       onclick="hideAllMenus(); return true;" >
                       <img src="%(portal_url)s/contenedor.gif" title="%(unTituloEnlace)s" alt="%(CONTAINER-title)s" id="icon-owner" />
                       <img src="%(portal_url)s/%(CONTAINER_icon)s"  title="%(unTituloEnlace)s" alt="%(CONTAINER-title)s" id="icon-owner" />
                       <span style="color: black">%(CONTAINER-title)s</span>
                       </a>
                       </li>
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'CONTAINER-title':             aMenuItemLabel,
                               'aMenuItemLabel':              aMenuItemLabel,
                               'CONTAINER-url':               aContainerElement[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'CONTAINER_icon':              aContainerElement[ 'content_icon'],
                               'SRES-title':                  fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                               'translated_archetype_name':   aContainerElement[ 'type_translations']['translated_archetype_name'],
                               'translated_type_description': aContainerElement[ 'type_translations']['translated_type_description'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           })





    theRdCtxt.pOS( u"""
                   <li>
                   """ )
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_Cursor')(        theRdCtxt)
    theRdCtxt.pOS( u"""
                   </li>
                   """ )    


    theRdCtxt.pOS( u"""
                   <li>
                   <a id="cid_MDDTOC_Link_Values" title="%(ModelDDvlPlone_Tabular_Section_Top)s " 
                   href="%(SRES-url)sTabular/%(theExtraLinkHrefParams)s#portal-globalnav"  
                   onclick="hideAllMenus(); return true;">
                   <span style="color: black">%(ModelDDvlPlone_Tabular_Section_Top)s</span>
                   </a>
                   </li>
                   """ % {
                           'ModelDDvlPlone_Tabular_Section_Top':   theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Section_Top',),
                           'theExtraLinkHrefParams':               theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           'SRES-url':                             aSRES[ 'url'],
                       })



    theRdCtxt.pOS( u"""
                   <li>
                   <a id="cid_MDDTOC_Link_Values" title="%(ModelDDvlPlone_Tabular_Section_Features)s " 
                   href="%(SRES-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDValues"  
                   onclick="hideAllMenus(); return true;" >
                   <span style="color: black">%(ModelDDvlPlone_Tabular_Section_Features)s</span>
                   </a>
                   </li>
                   """ % {
                           'ModelDDvlPlone_Tabular_Section_Features':   theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Section_Features',),
                           'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           'SRES-url':                                aSRES[ 'url'],
                       })





    unosTextFieldsNames = aSRES.get( 'text_field_names', [])

    if unosTextFieldsNames:

        someValueResults = aSRES.get( 'values', [])

        for aATTRRES in someValueResults:

            if aATTRRES and aATTRRES.get( 'read_permission', False):

                unAttributeName   = aATTRRES.get( 'attribute_name', '')
                unAttributeConfig = aATTRRES.get( 'attribute_config', '')

                if unAttributeName  and \
                   ( unAttributeName in unosTextFieldsNames) and \
                   ( not unAttributeConfig.get('exclude_from_values_form', False)) and \
                   (( not unAttributeConfig.has_key( 'custom_presentation_view') or not aATTRRES[ 'attribute_config'][ 'custom_presentation_view'])):

                    theRdCtxt.pOS( u"""
                                   <li>
                                   <a id="cid_MDDTOC_Link_Texto_%(attribute_name)s" title="%(attribute_label)s %(attribute_description)s" 
                                   href="%(SRES-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDTexto_%(attribute_name)s_table"   
                                   onclick="hideAllMenus(); return true;">
                                   <span style="color: black">%(attribute_label)s</span>
                                   </a>
                                   </li>
                                   """ % {
                                           'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                           'SRES-url':                    aSRES[ 'url'],
                                           'attribute_name':              fCGIE( unAttributeName),
                                           'attribute_label':             fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_label', '')),
                                           'attribute_description':       fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_description', '')),
                                       })






    unasTraversals = aSRES.get( 'traversals', [])

    unasTraversalsPLONE = aPLONERES.get( 'traversals', [])

    todasTraversals = unasTraversals + unasTraversalsPLONE

    if todasTraversals:

        for aTRAVRES in todasTraversals:

            if aTRAVRES:

                someElements = aTRAVRES.get( 'elements', [])
                unSiempre = theRdCtxt.fGP( 'theSiempre', True)



                if ( someElements or unSiempre):

                    theRdCtxt.pOS( u"""
                                   <li>
                                   <a id="cid_MDDTOC_Link_Traversal_%(traversal_name)s" title="%(traversal_label)s %(traversal_description)s" 
                                   href="%(SRES-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDTraversal_%(traversal_name)s_label"  
                                   onclick="hideAllMenus(); return true;" >
                                   """ % {
                                           'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                           'SRES-url':                    aSRES[ 'url'],
                                           'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                                           'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                                           'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
                                       })



                    aTraversalKind    = aTRAVRES.get( 'traversal_kind', '')

                    if aTraversalKind == 'aggregation':

                        someFactories = aTRAVRES[ 'factories']

                        for unaFactoriaElemento in someFactories:
                            theRdCtxt.pOS( u"""
                                           <img src="%(portal_url)s/%(FACTORY-icon)s" 
                                           title=%(FACTORY-translated_archetype_name)s"/>
                                           """ % {
                                                   'portal_url':                  aSRES[ 'portal_url'],
                                                   'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                                                   'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                                               })     


                    elif aTraversalKind == 'relation':

                        aTraversalName = aTRAVRES.get( 'traversal_name', '')
                        if not ( aTraversalName in [ 'referidos', 'referentes', 'referidosCualificados',]):

                            someRelatedTypesAndIcons = aTRAVRES[ 'related_types_and_icons']

                            for unTipoElemento, unIconElemento in someRelatedTypesAndIcons:
                                if unIconElemento:
                                    theRdCtxt.pOS( u"""
                                                   <img src="%(portal_url)s/%(RELATED-icon)s" 
                                                   title=%(RELATED-type)s"/>
                                                   """ % {
                                                           'portal_url':                  aSRES[ 'portal_url'],
                                                           'RELATED-icon':                unIconElemento,
                                                           'RELATED-type':                unTipoElemento,
                                                       })     


                    elif aTraversalKind == 'aggregation-plone':

                        someFactories = aTRAVRES[ 'factories']

                        for unaFactoriaElemento in someFactories:
                            theRdCtxt.pOS( u"""
                                           <img src="%(portal_url)s/%(FACTORY-icon)s" 
                                           title=%(FACTORY-translated_archetype_name)s"/>
                                           """ % {
                                                   'portal_url':                          aSRES[ 'portal_url'],
                                                   'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                                                   'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                                               })     



                    theRdCtxt.pOS( u"""
                                   <span style="color: black">%(traversal_label)s</span>
                                   </a>
                                   </li>
                                   """ % {
                                           'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                                       })


    theRdCtxt.pOS( u"""
                   </ul></font><dd></dl>
                   """)

    theRdCtxt.pOS( u"""
                   </font></font></td></tr></tbody></table>
                   """)      

    #theRdCtxt.pOS( u"""
    #</td></tr></tbody></table>
    #""")

    return [ True, True,]





def _MDDRender_Tabular_Javascript( theRdCtxt):

    theRdCtxt.pOS( cMDDRenderTabular_SectionsMenu_JavaScript)

    return [ True, True,]







def _MDDRender_Tabular_Cabecera( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    anOk          = None
    aGo           = True
    unUnwindTrick = True
    while( unUnwindTrick):

        unUnwindTrick = False


        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_TypeAndDescription_Before')( theRdCtxt)
            if not aGo:
                break
        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_TypeAndDescription')(        theRdCtxt)
        if not aGo:
            break
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_TypeAndDescription_After')(  theRdCtxt)
            if not aGo:
                break  


        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_OwnerAndContainer_Before')( theRdCtxt)
            if not aGo:
                break
        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_OwnerAndContainer')(        theRdCtxt)
        if not aGo:
            break
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_OwnerAndContainer_After')(  theRdCtxt)
            if not aGo:
                break  


        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_Refresh')(        theRdCtxt)
        if not aGo:
            break


        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_Textual')(        theRdCtxt)
        if not aGo:
            break


        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_Cursor_Before')( theRdCtxt)
            if not aGo:
                break
        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_Cursor')(        theRdCtxt)
        if not aGo:
            break
        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_Cursor_After')(  theRdCtxt)
            if not aGo:
                break     


        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_ChangeActions_Before')( theRdCtxt)
            if not aGo:
                break

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_ChangeActions')(        theRdCtxt)
        if not aGo:
            break

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_ClipboardActions')(        theRdCtxt)
        if not aGo:
            break

        if not cExtensionsForbidden:
            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Cabecera_ChangeActions_After')(  theRdCtxt)
            if not aGo:
                break   



        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_SectionsMenu_Anchor')(        theRdCtxt)
        if not aGo:
            break



    return [ True, aGo,]








def _MDDRender_Tabular_Cabecera_TypeAndDescription( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    


    theRdCtxt.pOS( u"""
                   <span class="formHelp" >
                   <font size="2">
                   <img src="%(portal_url)s/%(content_icon)s" title="%(SRES-title)s" alt="%(SRES-title)s" />
                   <strong>%(translated_archetype_name)s</strong>
                   </font>
                   </span>
                   &ensp;
                   <span class="formHelp">%(translated_type_description)s</span>
                   <br/>
                   """ % {
                           'portal_url':                   aSRES[ 'portal_url'],
                           'content_icon':                 aSRES[ 'content_icon'],
                           'SRES-title':                   fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                           'translated_archetype_name':    aSRES[ 'type_translations']['translated_archetype_name'],
                           'translated_type_description':  aSRES[ 'type_translations']['translated_type_description'],
                       })


    return [ True, True,]








def _MDDRender_Tabular_Cabecera_OwnerAndContainer( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    if aSRES[ 'is_root']:
        return [ False, True,]    

    anOwnerElement    = aSRES[ 'owner_element']
    aContainerElement = aSRES[ 'container_element']

    if not ( anOwnerElement == None):

        unTituloEnlace = u'%s %s %s %s' % ( 
            anOwnerElement[ 'type_translations'][ 'translated_archetype_name'], 
            anOwnerElement[ 'values_by_name'][ 'title'][ 'uvalue'], 
            anOwnerElement[ 'values_by_name'][ 'description'][ 'uvalue'], 
            anOwnerElement[ 'type_translations'][ 'translated_type_description'],
        )

        theRdCtxt.pOS( u"""
                       <table  cellspacing="0" cellpadding="0" frame="void"  style="display: inline" ><tbody><tr><td valign="center">
                       <a id="cid_MDDLink_Propietario"  class="state-visible" title="%(unTituloEnlace)s " 
                       href="%(OWNER-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_title"  >
                       <img src="%(portal_url)s/propietario.gif" title="%(unTituloEnlace)s" alt="%(OWNER-title)s" id="icon-owner" />
                       <img src="%(portal_url)s/%(OWNER_icon)s"  title="%(unTituloEnlace)s" alt="%(OWNER-title)s" id="icon-owner" />
                       <!-- <span>%(OWNER-title)s</span> -->
                       </a></td></tr></tbody></table>
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'OWNER-title':                 fCGIE( anOwnerElement['values_by_name'][ 'title'][ 'uvalue']),
                               'OWNER-url':                   anOwnerElement[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'OWNER_icon':                  anOwnerElement[ 'content_icon'],
                               'translated_archetype_name':   anOwnerElement[ 'type_translations']['translated_archetype_name'],
                               'translated_type_description': anOwnerElement[ 'type_translations']['translated_type_description'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           })




    if not ( aContainerElement == None) and ( anOwnerElement and not ( aContainerElement == anOwnerElement)):

        unTituloEnlace = u'%s %s %s %s' % ( 
            aContainerElement[ 'type_translations'][ 'translated_archetype_name'], 
            aContainerElement[ 'values_by_name'][ 'title'][ 'uvalue'], 
            aContainerElement[ 'values_by_name'][ 'description'][ 'uvalue'], 
            aContainerElement[ 'type_translations'][ 'translated_type_description'],
        )

        theRdCtxt.pOS( u"""
                       &emsp;
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center"> 
                       <a id="cid_MDDLink_Contenedor"  class="state-visible" title="%(unTituloEnlace)s " 
                       href="%(OWNER-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_title"  >
                       <img src="%(portal_url)s/contenedor.gif" title="%(unTituloEnlace)s" alt="%(OWNER-title)s" id="icon-owner" />
                       <img src="%(portal_url)s/%(OWNER_icon)s"  title="%(unTituloEnlace)s" alt="%(OWNER-title)s" id="icon-owner" />
                       <!-- <span>%(OWNER-title)s</span> -->
                       </a></td></tr></tbody></table>
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'OWNER-title':                 fCGIE( aContainerElement['values_by_name'][ 'title'][ 'uvalue']),
                               'OWNER-url':                   aContainerElement[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'OWNER_icon':                  aContainerElement[ 'content_icon'],
                               'SRES-title':                  fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                               'translated_archetype_name':   aContainerElement[ 'type_translations']['translated_archetype_name'],
                               'translated_type_description': aContainerElement[ 'type_translations']['translated_type_description'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           })

    return [ True, True,]






def _MDDRender_Tabular_Cabecera_Refresh( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    unTituloEnlace = u'%s %s %s %s %s' % ( 
        aSRES[ 'type_translations'][ 'translated_archetype_name'], 
        aSRES[ 'values_by_name'][ 'title'][ 'uvalue'], 
        aSRES[ 'values_by_name'][ 'description'][ 'uvalue'], 
        aSRES[ 'type_translations'][ 'translated_type_description'],
        theRdCtxt.fUITr( 'ModelDDvlPlone_refrescar_action_label'),
    )

    theRdCtxt.pOS( u"""
                   &emsp;
                   <table  cellspacing="0" cellpadding="0" frame="void"  style="display: inline" ><tbody><tr><td valign="center">
                   <a id="cid_MDDLink_Refresh"  class="state-visible" title="%(unTituloEnlace)s " 
                   href="%(SRES-url)sTabular/%(theExtraLinkHrefParams)s"  >
                   <img src="%(portal_url)s/refrescar.gif" alt="%(ModelDDvlPlone_refrescar_action_label)s" title="%(ModelDDvlPlone_refrescar_action_label)s" 
                   id="icon-refrescar" />
                   <!-- <span>%(ModelDDvlPlone_refrescar_action_label)s</span> -->
                   </a></td></tr></tbody></table>
                   """ % {
                           'unTituloEnlace':              fCGIE( unTituloEnlace),
                           'portal_url':                  aSRES[ 'portal_url'],
                           'OWNER-title':                 fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                           'SRES-url':                    aSRES[ 'url'],
                           'SRES-UID':                    aSRES[ 'UID'],
                           'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           'ModelDDvlPlone_refrescar_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_refrescar_action_label'),
                       })


    return [ True, True,]









def _MDDRender_Tabular_Cabecera_Textual( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    unTituloEnlace = u'%s %s %s %s %s' % ( 
        aSRES[ 'type_translations'][ 'translated_archetype_name'], 
        aSRES[ 'values_by_name'][ 'title'][ 'uvalue'], 
        aSRES[ 'values_by_name'][ 'description'][ 'uvalue'], 
        aSRES[ 'type_translations'][ 'translated_type_description'],
        theRdCtxt.fUITr( 'ModelDDvlPlone_textual_action_label'),
    )

    theRdCtxt.pOS( u"""
                   &emsp;
                   <table  cellspacing="0" cellpadding="0" frame="void"  style="display: inline" ><tbody><tr><td valign="center">
                   <a id="cid_MDDLink_Refresh"  class="state-visible" title="%(unTituloEnlace)s " 
                   href="%(SRES-url)sTextual/%(theExtraLinkHrefParams)s"  >
                   <img src="%(portal_url)s/textual.gif" alt="%(ModelDDvlPlone_textual_action_label)s" title="%(ModelDDvlPlone_textual_action_label)s" 
                   id="icon-refrescar" />
                   <!-- <span>%(ModelDDvlPlone_textual_action_label)s</span> -->
                   </a></td></tr></tbody></table>
                   """ % {
                           'unTituloEnlace':              fCGIE( unTituloEnlace),
                           'portal_url':                  aSRES[ 'portal_url'],
                           'OWNER-title':                 fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                           'SRES-url':                    aSRES[ 'url'],
                           'SRES-UID':                    aSRES[ 'UID'],
                           'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           'ModelDDvlPlone_textual_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_textual_action_label'),
                       })


    return [ True, True,]






def _MDDRender_Tabular_Relation_Cabecera( theRdCtxt):

    aRELRES = theRdCtxt.fGP( 'RELRES', {})
    if not aRELRES:
        return [ False, True,]

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]



    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})



    theRdCtxt.pOS( u"""
                   <br/>
                   <h2 id="hidMDDTraversal_%(traversal_name)s_label" 
                   <a  id="hidMDDTraversal_%(traversal_name)s_link"
                   title="%(ModelDDvlPlone_recorrercursorrelacion_action_label)s %(traversal_label)s %(ModelDDvlPlone_deorigenrelacioncuandoenlazando)s %(RELRES-title)s"
                   href="%(RELRES-url)sTabular/#hidMDDTraversal_%(traversal_name)s_link" >
                   """ % {
                           'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           'theExtraLinkHrefParams':                             theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                           'ModelDDvlPlone_recorrercursorrelacion_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_recorrercursorrelacion_action_label'),
                           'ModelDDvlPlone_deorigenrelacioncuandoenlazando':     theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),
                           'RELRES-url':               aRELRES[ 'url'],
                           'portal_url':               aRELRES[ 'portal_url'],
                           'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                           'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                           'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                           'RELRES-title':             fCGIE( aRELRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                       })


    aTraversalName = aTRAVRES.get( 'traversal_name', '')
    if not ( aTraversalName in [ 'referidos', 'referentes', 'referidosCualificados',]):

        someRelatedTypesAndIcons = aTRAVRES[ 'related_types_and_icons']

        for unTipoElemento, unIconElemento in someRelatedTypesAndIcons:
            if unIconElemento:
                theRdCtxt.pOS( u"""
                               <img src="%(portal_url)s/%(RELATED-icon)s" 
                               title=%(RELATED-type)s"/>
                               """ % {
                                       'portal_url':                  aSRES[ 'portal_url'],
                                       'RELATED-icon':                unIconElemento,
                                       'RELATED-type':                unTipoElemento,
                                   })     

    theRdCtxt.pOS( u"""
                   <span class="state-visible" id="hidMDDTraversal_%(traversal_name)s_title" >%(traversal_label)s</span>
                   </a>
                   <font size=1">            
                   &emsp;
                   &emsp;
                   <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr>
                   <td id="cid_MDDTOC_Holder_Traversal_%(traversal_name)s" valign="top" align="left">
                   <a title="%(ModelDDvlPlone_Tabular_Sections)s"
                   onclick="document.getElementById( 'cid_MDDTOC_Holder_Traversal_%(traversal_name)s').appendChild( document.getElementById( 'cid_MDDSectionList_ActionsMenu')); if ( hasClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated' )) { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated', 'activated');} else { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'activated', 'deactivated')} return true;">
                   <img src="%(portal_url)s/menusecciones.gif" title="%(ModelDDvlPlone_Tabular_Sections)s" alt="%(ModelDDvlPlone_Tabular_Sections)s" id="icon-sectionsmenu" />
                   """ % {
                           'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           'theExtraLinkHrefParams':                             theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                           'ModelDDvlPlone_recorrercursorrelacion_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_recorrercursorrelacion_action_label'),
                           'ModelDDvlPlone_deorigenrelacioncuandoenlazando':     theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),
                           'SRES-url':                 aSRES[ 'url'],
                           'portal_url':               aSRES[ 'portal_url'],
                           'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                           'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                           'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                           'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                       })




    if aPREFS_PRES.get( 'DisplayActionLabels', False):
        theRdCtxt.pOS( u"""
                       <span>%(ModelDDvlPlone_Tabular_Sections)s</span>
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           })


    theRdCtxt.pOS( u"""
                   </a>
                   </td>
                   </tr></tbody></table>
                   </font>            
                   </h2>
                   <p class="formHelp">%(traversal_description)s</p>
                   """ % {
                           'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           'theExtraLinkHrefParams':                             theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                           'ModelDDvlPlone_recorrercursorrelacion_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_recorrercursorrelacion_action_label'),
                           'ModelDDvlPlone_deorigenrelacioncuandoenlazando':     theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),
                           'SRES-url':                 aSRES[ 'url'],
                           'portal_url':               aSRES[ 'portal_url'],
                           'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                           'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                           'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                           'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                       })



    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Relation_Cabecera_Cursor_Before')( theRdCtxt)
        if not aGo:
            return [ False, True,]

    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Relation_Cabecera_Cursor')(        theRdCtxt)
    if not aGo:
        return [ False, True,]

    if not cExtensionsForbidden:
        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Relation_Cabecera_Cursor_After')(  theRdCtxt)
        if not aGo:
            return [ False, True,]




    theRdCtxt.pOS( u"""
                   <br/>
                   <h1 id="hidMDDTraversal_%(traversal_name)s_Element" 
                   <a  id="hidMDDTraversal_%(traversal_name)s_Element_link"
                   title="%(ModelDDvlPlone_recorrercursorrelacion_action_label)s %(traversal_label)s %(ModelDDvlPlone_deorigenrelacioncuandoenlazando)s %(SRES-title)s"
                   href="%(SRES-url)sTabular/#hidMDDTraversal_%(traversal_name)s_link" >
                   %(SRES-title)s
                   </a>
                   </h1>

                   """ % {
                           'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           'theExtraLinkHrefParams':                             theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                           'ModelDDvlPlone_recorrercursorrelacion_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_recorrercursorrelacion_action_label'),
                           'ModelDDvlPlone_deorigenrelacioncuandoenlazando':     theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),
                           'SRES-url':                 aSRES[ 'url'],
                           'portal_url':               aSRES[ 'portal_url'],
                           'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                           'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                           'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                           'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                       })



    theRdCtxt.pOS( u"""
                   <span class="formHelp" >
                   <font size="2">
                   <img src="%(portal_url)s/%(content_icon)s" title="%(SRES-title)s" alt="%(SRES-title)s" />
                   <strong>%(translated_archetype_name)s</strong>
                   </font>
                   </span>
                   &ensp;
                   <span class="formHelp">%(translated_type_description)s</span>
                   <br/>
                   """ % {
                           'portal_url':                   aSRES[ 'portal_url'],
                           'content_icon':                 aSRES[ 'content_icon'],
                           'SRES-title':                   fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                           'translated_archetype_name':    aSRES[ 'type_translations']['translated_archetype_name'],
                           'translated_type_description':  aSRES[ 'type_translations']['translated_type_description'],
                       })



    return [ True, True,]









def _MDDRender_Tabular_SiblingsMenu( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    aCursor          = aSRES[   'cursor']
    someSiblings     = aCursor[ 'siblings']

    if not someSiblings:
        return [ False, True,]



    theRdCtxt.pOS( u"""
                   <dl class="actionMenu deactivated" id="cid_MDDSiblingsList_ActionsMenu" style="z-index: 6;padding: 0 0 0 0 !important" ><font style="font-size: 0px" >
                   <dt class="actionMenuHeader" style="display: inline">
                   <!-- 
                   <a>
                   <span>%(element_index)d</span>
                   /
                   <span>%(elements_count)d</span>
                   </a>
                   -->
                   </dt>
                   <dd class="actionMenuContent"  id="cid_MDDSiblingsList_ActionsMenuContent" style="z-index: 6;left: 1px; top: -1em;">
                   <font size="1" style="font-size: 1en" >
                   <ul>

                   """ % {
                           'element_index':    aCursor[ 'element_index'],
                           'elements_count':    aCursor[ 'elements_count'],
                           'portal_url':                        aSRES[ 'portal_url'],
                       })   


    anOwnerElement    = aSRES[ 'owner_element']
    aContainerElement = aSRES[ 'container_element']

    if not ( anOwnerElement == None):

        unTituloEnlace = '%s %s %s %s' % ( 
            anOwnerElement[ 'type_translations'][ 'translated_archetype_name'], 
            anOwnerElement[ 'values_by_name'][ 'title'][ 'uvalue'], 
            anOwnerElement[ 'values_by_name'][ 'description'][ 'uvalue'], 
            anOwnerElement[ 'type_translations'][ 'translated_type_description'],
        )

        aMenuItemLabel = fCGIE( anOwnerElement['values_by_name'][ 'title'][ 'uvalue'])
        aLenMenuItem = len( aMenuItemLabel)
        if aLenMenuItem > cPref_Pres_SectionsMenu_Item_MaxLength:
            aMenuItemLabel = '%s%s' % ( aMenuItemLabel[:cPref_Pres_SectionsMenu_Item_MaxLength], cPref_Pres_SectionsMenu_Item_MaxLengthExceeded_Postfix,)

        theRdCtxt.pOS( u"""
                       <li>
                       <a id="cid_MDDTOC_Link_Propietario"  class="state-visible" title="%(unTituloEnlace)s " 
                       href="%(OWNER-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_title"   
                       onclick="hideAllMenus(); return true;">
                       <img src="%(portal_url)s/propietario.gif" title="%(unTituloEnlace)s" alt="%(OWNER-title)s" id="icon-owner" />
                       <img src="%(portal_url)s/%(OWNER_icon)s"  title="%(unTituloEnlace)s" alt="%(OWNER-title)s" id="icon-owner" />
                       <span style="color: black" >%(aMenuItemLabel)s</span>
                       </a>
                       </li>
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'OWNER-title':                 aMenuItemLabel,
                               'aMenuItemLabel':              aMenuItemLabel,
                               'OWNER-url':                   anOwnerElement[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'OWNER_icon':                  anOwnerElement[ 'content_icon'],
                               'translated_archetype_name':   anOwnerElement[ 'type_translations']['translated_archetype_name'],
                               'translated_type_description': anOwnerElement[ 'type_translations']['translated_type_description'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           })




    if not ( aContainerElement == None) and ( anOwnerElement and not ( aContainerElement == anOwnerElement)):

        unTituloEnlace = '%s %s %s %s' % ( 
            aContainerElement[ 'type_translations'][ 'translated_archetype_name'], 
            aContainerElement[ 'values_by_name'][ 'title'][ 'uvalue'], 
            aContainerElement[ 'values_by_name'][ 'description'][ 'uvalue'], 
            aContainerElement[ 'type_translations'][ 'translated_type_description'],
        )

        aMenuItemLabel = fCGIE( anOwnerElement['values_by_name'][ 'title'][ 'uvalue'])
        aLenMenuItem = len( aMenuItemLabel)
        if aLenMenuItem > cPref_Pres_SectionsMenu_Item_MaxLength:
            aMenuItemLabel = '%s%s' % ( aMenuItemLabel[:cPref_Pres_SectionsMenu_Item_MaxLength], cPref_Pres_SectionsMenu_Item_MaxLengthExceeded_Postfix,)

        theRdCtxt.pOS( u"""
                       <li>
                       <a id="cid_MDDTOC_Link_Contenedor"  title="%(unTituloEnlace)s " 
                       href="%(CONTAINER-url)sTabular/%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_title"  
                       onclick="hideAllMenus(); return true;" >
                       <img src="%(portal_url)s/contenedor.gif" title="%(unTituloEnlace)s" alt="%(CONTAINER-title)s" id="icon-owner" />
                       <img src="%(portal_url)s/%(CONTAINER_icon)s"  title="%(unTituloEnlace)s" alt="%(CONTAINER-title)s" id="icon-owner" />
                       <span style="color: black">%(CONTAINER-title)s</span>
                       </a>
                       </li>
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'CONTAINER-title':             aMenuItemLabel,
                               'aMenuItemLabel':              aMenuItemLabel,
                               'CONTAINER-url':               aContainerElement[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'CONTAINER_icon':              aContainerElement[ 'content_icon'],
                               'SRES-title':                  fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                               'translated_archetype_name':   aContainerElement[ 'type_translations']['translated_archetype_name'],
                               'translated_type_description': aContainerElement[ 'type_translations']['translated_type_description'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           })





    theRdCtxt.pOS( u"""
                   <li>
                   """ )
    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Cabecera_Cursor')(        theRdCtxt)
    theRdCtxt.pOS( u"""
                   </li>
                   """ )    



    for aSiblingIndex in range( len( someSiblings)):

        aSibling = someSiblings[ aSiblingIndex]

        if not ( aSibling == None):

            unTituloEnlace = '%s %s %s %s' % ( 
                aSibling[ 'type_translations'][ 'translated_archetype_name'], 
                aSibling[ 'values_by_name'][ 'title'][ 'uvalue'], 
                aSibling[ 'values_by_name'][ 'description'][ 'uvalue'], 
                aSibling[ 'type_translations'][ 'translated_type_description'],
            )

            aMenuItemLabel = fCGIE( aSibling['values_by_name'][ 'title'][ 'uvalue'])
            aLenMenuItem = len( aMenuItemLabel)
            if aLenMenuItem > cPref_Pres_SiblingsMenu_Item_MaxLength:
                aMenuItemLabel = '%s%s' % ( aMenuItemLabel[:cPref_Pres_SiblingsMenu_Item_MaxLength], cPref_Pres_SiblingsMenu_Item_MaxLengthExceeded_Postfix,)

            if not ( aSibling[ 'object'] == aSRES[ 'object']):
                theRdCtxt.pOS( u"""
                               <li>
                               <a id="cid_MDDTOC_Link_Sibling_%(SIBLING-id)s"  title="%(unTituloEnlace)s " 
                               href="%(SIBLING-url)sTabular/%(theExtraLinkHrefParams)s"   
                               onclick="hideAllMenus(); return true;">
                               <span>%(aSiblingIndex)d</span>&nbsp;
                               <img src="%(portal_url)s/%(SIBLING_icon)s"  title="%(unTituloEnlace)s" alt="%(SIBLING-title)s" id="icon-owner" />
                               <span style="color: black">%(aMenuItemLabel)s</span>
                               </a>
                               </li>
                               """ % {
                                       'aSiblingIndex':               aSiblingIndex + 1,
                                       'unTituloEnlace':              fCGIE( unTituloEnlace),
                                       'portal_url':                  aSRES[ 'portal_url'],
                                       'SIBLING-title':               aMenuItemLabel,
                                       'aMenuItemLabel':              aMenuItemLabel,
                                       'SIBLING-id':                  aSibling[ 'id'],
                                       'SIBLING-url':                 aSibling[ 'url'],
                                       'SIBLING_icon':                aSibling[ 'content_icon'],
                                       'translated_archetype_name':   aSibling[ 'type_translations']['translated_archetype_name'],
                                       'translated_type_description': aSibling[ 'type_translations']['translated_type_description'],
                                       'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                   })
            else:
                theRdCtxt.pOS( u"""
                               <li>
                               <span>%(aSiblingIndex)d</span>&nbsp;
                               <img src="%(portal_url)s/%(SIBLING_icon)s"  title="%(unTituloEnlace)s" alt="%(SIBLING-title)s" id="icon-owner" />
                               <span style="color: blue">%(aMenuItemLabel)s</span>
                               </li>
                               """ % {
                                       'aSiblingIndex':               aSiblingIndex + 1,
                                       'unTituloEnlace':              fCGIE( unTituloEnlace),
                                       'portal_url':                  aSRES[ 'portal_url'],
                                       'SIBLING-title':               aMenuItemLabel,
                                       'aMenuItemLabel':              aMenuItemLabel,
                                       'SIBLING-id':                  aSibling[ 'id'],
                                       'SIBLING-url':                 aSibling[ 'url'],
                                       'SIBLING_icon':                aSibling[ 'content_icon'],
                                       'translated_archetype_name':   aSibling[ 'type_translations']['translated_archetype_name'],
                                       'translated_type_description': aSibling[ 'type_translations']['translated_type_description'],
                                       'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                   })




    theRdCtxt.pOS( u"""
                   </ul></font><dd></dl>
                   """)

    theRdCtxt.pOS( u"""
                   </font></font>
                   """)      

    #theRdCtxt.pOS( u"""
    #</td></tr></tbody></table>
    #""")      

    #theRdCtxt.pOS( u"""
    #</td></tr></tbody></table>
    #""")

    return [ True, True,]











def _MDDRender_Tabular_Cabecera_Cursor( theRdCtxt):


    aRenderedCursor = theRdCtxt.fGP( 'RenderedCursor', '')
    if aRenderedCursor:
        theRdCtxt.pO( aRenderedCursor)    
        return [ True, True,]

    aCurrentOutput = theRdCtxt.fGP( 'output', None)

    aNewOutput = StringIO()
    theRdCtxt.pSP( 'output', aNewOutput)



    try:

        aSRES = theRdCtxt.fGP( 'SRES', {})
        if not aSRES:
            return [ False, True,]    

        aCURSORRES = theRdCtxt.fGP( 'CURSORRES', aSRES)
        if not aCURSORRES:
            return [ False, True,]    

        if aSRES[ 'is_root']:
            return [ False, True,]    

        aCursor          = aSRES[ 'cursor']

        if not ( aCursor and ( aCursor[ 'elements_count'] > 1) and (  aCursor[ 'previous_element'] or aCursor[ 'next_element'])):
            return [ False, True,]    

        theRdCtxt.pOS( u"""
                       &emsp;
                       <table   style="display: inline" cellspacing="0" cellpadding="0" frame="void"  ><tbody><tr>
                       <td  id="cid_MDDSiblingsMenu_Holder" valign="center" >
                       """)

        aRelationCursorName = theRdCtxt.fGP( 'theRelationCursorName', '')
        aReferenceFieldName = theRdCtxt.fGP( 'theReferenceFieldName', '')


        theRdCtxt.pOS( u"""
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)
        if aCursor[ 'first_element'] and not ( aCursor[ 'element_index'] == 1) and not ( aCursor[ 'element_index'] == 2):
            unTituloEnlace = u'%s %s %s %s' % ( 
                aCursor[ 'first_element'][ 'type_translations'][ 'translated_archetype_name'], 
                aCursor[ 'first_element'][ 'values_by_name'][ 'title'][ 'uvalue'], 
                aCursor[ 'first_element'][ 'values_by_name'][ 'description'][ 'uvalue'], 
                aCursor[ 'first_element'][ 'type_translations'][ 'translated_type_description'],
            )

            aLinkHREF = '%sTabular/' % aCursor[ 'first_element'][ 'url']

            if aRelationCursorName:
                aLinkHREF = '%s?theRelationCursorName=%s%s' % ( aLinkHREF, aRelationCursorName, theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            elif aReferenceFieldName:
                aLinkHREF = '%s?theReferenceFieldName=%s%s' % ( aLinkHREF, aReferenceFieldName, theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            else:
                aLinkHREF = '%s%s' % ( aLinkHREF, theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),)



            theRdCtxt.pOS( u"""
                           <a id="cid_MDDLink_First"  class="state-visible" title="%(unTituloEnlace)s " 
                           href="%(aLinkHREF)s"  >
                           <img src="%(portal_url)s/primero.gif" title="%(unTituloEnlace)s" alt="%(ELEMENT-title)s" id="icon-first" />
                           <!-- <span>%(ELEMENT-title)s</span> -->
                           </a>
                           """ % {
                                   'unTituloEnlace':              fCGIE( unTituloEnlace),
                                   'portal_url':                  aSRES[ 'portal_url'],
                                   'ELEMENT-title':               fCGIE( aCursor[ 'first_element']['values_by_name'][ 'title'][ 'uvalue']),
                                   'aLinkHREF':                   aLinkHREF,
                               })
        else:
            theRdCtxt.pOS( u"""
                           <img src="%(portal_url)s/blank_icon.gif" />
                           """ % {
                                   'portal_url':                  aSRES[ 'portal_url'],
                               })

        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       &ensp;
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)



        if aCursor[ 'previous_element'] and ( aCursor[ 'element_index'] > 1):
            unTituloEnlace = u'%s %s %s %s' % ( 
                aCursor[ 'previous_element'][ 'type_translations'][ 'translated_archetype_name'], 
                aCursor[ 'previous_element'][ 'values_by_name'][ 'title'][ 'uvalue'], 
                aCursor[ 'previous_element'][ 'values_by_name'][ 'description'][ 'uvalue'], 
                aCursor[ 'previous_element'][ 'type_translations'][ 'translated_type_description'],
            )

            aLinkHREF = '%sTabular/' % aCursor[ 'previous_element'][ 'url']

            if aRelationCursorName:
                aLinkHREF = '%s?theRelationCursorName=%s%s' % ( aLinkHREF, aRelationCursorName, theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            elif aReferenceFieldName:
                aLinkHREF = '%s?theReferenceFieldName=%s%s' % ( aLinkHREF, aReferenceFieldName, theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            else:
                aLinkHREF = '%s%s' % ( aLinkHREF, theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),)



            theRdCtxt.pOS( u"""
                           <a id="cid_MDDLink_Previous"  class="state-visible" title="%(unTituloEnlace)s " 
                           href="%(aLinkHREF)s"  >
                           <img src="%(portal_url)s/anterior.gif" title="%(unTituloEnlace)s" alt="%(ELEMENT-title)s" id="icon-previous" />
                           <!-- <span>%(ELEMENT-title)s</span> -->
                           </a>
                           """ % {
                                   'unTituloEnlace':              unTituloEnlace,
                                   'portal_url':                  aSRES[ 'portal_url'],
                                   'ELEMENT-title':               fCGIE(  aCursor[ 'previous_element']['values_by_name'][ 'title'][ 'uvalue']),
                                   'aLinkHREF':                   aLinkHREF,
                               })
        else:
            theRdCtxt.pOS( u"""
                           <img src="%(portal_url)s/blank_icon.gif" />
                           """ % {
                                   'portal_url':                  aSRES[ 'portal_url'],
                               })

        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)








        theRdCtxt.pOS( u"""
                       &emsp;
                       &emsp;
                       <font size="2" >
                       <a  title="Siblings-" alt="Siblings-"
                       onclick="
                       document.getElementById( 'cid_MDDSiblingsMenu_Holder').appendChild( document.getElementById( 'cid_MDDSiblingsList_ActionsMenu')); 
                       replaceClassName( document.getElementById( 'cid_MDDSiblingsList_ActionsMenu') ,'deactivated', 'activated'); 
                       return true;">
                       <span>%(element_index)d</span>
                       /
                       <span>%(elements_count)d</span>
                       </a>
                       </font>  
                       """ % {
                               'element_index':     aCursor[ 'element_index'],
                               'elements_count':    aCursor[ 'elements_count'],
                               'portal_url':        aSRES[ 'portal_url'],
                           })   



        #theRdCtxt.pOS( u"""
        #<span>%(element_index)d</span>
        #/
        #<span>%(elements_count)d</span>
        #""" % {
            #'element_index':    aCursor[ 'element_index'],
            #'elements_count':    aCursor[ 'elements_count'],
        #})

        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       <table cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)



        if aCursor[ 'next_element'] and ( aCursor[ 'element_index'] < aCursor[ 'elements_count']):
            unTituloEnlace = u'%s %s %s %s' % ( 
                aCursor[ 'next_element'][ 'type_translations'][ 'translated_archetype_name'], 
                aCursor[ 'next_element'][ 'values_by_name'][ 'title'][ 'uvalue'], 
                aCursor[ 'next_element'][ 'values_by_name'][ 'description'][ 'uvalue'], 
                aCursor[ 'next_element'][ 'type_translations'][ 'translated_type_description'],
            )

            aLinkHREF = '%sTabular/' % aCursor[ 'next_element'][ 'url']

            if aRelationCursorName:
                aLinkHREF = '%s?theRelationCursorName=%s%s' % ( aLinkHREF, aRelationCursorName, theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            elif aReferenceFieldName:
                aLinkHREF = '%s?theReferenceFieldName=%s%s' % ( aLinkHREF, aReferenceFieldName, theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            else:
                aLinkHREF = '%s%s' % ( aLinkHREF, theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),)



            theRdCtxt.pOS( u"""
                           <a id="cid_MDDLink_Previous"  class="state-visible" title="%(unTituloEnlace)s " 
                           href="%(aLinkHREF)s"  >
                           <img src="%(portal_url)s/siguiente.gif" title="%(unTituloEnlace)s" alt="%(ELEMENT-title)s" id="icon-next" />
                           <!-- <span>%(ELEMENT-title)s</span> -->
                           </a>
                           """ % {
                                   'unTituloEnlace':              fCGIE( unTituloEnlace),
                                   'portal_url':                  aSRES[ 'portal_url'],
                                   'ELEMENT-title':               fCGIE(  aCursor[ 'next_element']['values_by_name'][ 'title'][ 'uvalue']),
                                   'aLinkHREF':                   aLinkHREF,
                               })
        else:
            theRdCtxt.pOS( u"""
                           <img src="%(portal_url)s/blank_icon.gif" />
                           """ % {
                                   'portal_url':                  aSRES[ 'portal_url'],
                               })


        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       &ensp;
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)



        if aCursor[ 'last_element'] and not ( aCursor[ 'element_index'] == aCursor[ 'elements_count']) and not ( aCursor[ 'element_index'] == ( aCursor[ 'elements_count'] - 1)):
            unTituloEnlace = '%s %s %s %s' % ( 
                aCursor[ 'last_element'][ 'type_translations'][ 'translated_archetype_name'], 
                aCursor[ 'last_element'][ 'values_by_name'][ 'title'][ 'uvalue'], 
                aCursor[ 'last_element'][ 'values_by_name'][ 'description'][ 'uvalue'], 
                aCursor[ 'last_element'][ 'type_translations'][ 'translated_type_description'],
            )

            aLinkHREF = '%sTabular/' % aCursor[ 'last_element'][ 'url']

            if aRelationCursorName:
                aLinkHREF = '%s?theRelationCursorName=%s%s' % ( aLinkHREF, aRelationCursorName, theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            elif aReferenceFieldName:
                aLinkHREF = '%s?theReferenceFieldName=%s%s' % ( aLinkHREF, aReferenceFieldName, theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            else:
                aLinkHREF = '%s%s' % ( aLinkHREF, theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),)



            theRdCtxt.pOS( u"""
                           <a id="cid_MDDLink_last"  class="state-visible" title="%(unTituloEnlace)s " 
                           href="%(aLinkHREF)s"  >
                           <img src="%(portal_url)s/ultimo.gif" title="%(unTituloEnlace)s" alt="%(ELEMENT-title)s" id="icon-last" />
                           <!-- <span>%(ELEMENT-title)s</span> -->
                           </a>
                           """ % {
                                   'unTituloEnlace':              fCGIE( unTituloEnlace),
                                   'portal_url':                  aSRES[ 'portal_url'],
                                   'ELEMENT-title':               fCGIE( aCursor[ 'last_element']['values_by_name'][ 'title'][ 'uvalue']),
                                   'aLinkHREF':                   aLinkHREF,
                               })
        else:
            theRdCtxt.pOS( u"""
                           <img src="%(portal_url)s/blank_icon.gif" />
                           """ % {
                                   'portal_url':                  aSRES[ 'portal_url'],
                               })

        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       </td></tr></tbody></table>
                       """)    


    finally:
        theRdCtxt.pSP( 'output', aCurrentOutput)

    aRenderedCursor = aNewOutput.getvalue() 
    if aRenderedCursor:
        theRdCtxt.pSP( 'RenderedCursor', aRenderedCursor)
        theRdCtxt.pO( aRenderedCursor)

    return [ True, True,]






def _MDDRender_Tabular_Relation_Cabecera_Cursor( theRdCtxt):


    aRenderedCursor = theRdCtxt.fGP( 'RenderedRelationCursor', '')
    if aRenderedCursor:
        theRdCtxt.pO( aRenderedCursor)    
        return [ True, True,]

    aCurrentOutput = theRdCtxt.fGP( 'output', None)

    aNewOutput = StringIO()
    theRdCtxt.pSP( 'output', aNewOutput)



    try:

        aSRES = theRdCtxt.fGP( 'SRES', {})
        if not aSRES:
            return [ False, True,]    

        aRELRES = theRdCtxt.fGP( 'RELRES', {})
        if not aRELRES:
            return [ False, True,]    

        if aSRES[ 'is_root']:
            return [ False, True,]    

        aCursor          = aSRES[ 'cursor']

        if not ( aCursor and ( aCursor[ 'elements_count'] > 1) and (  aCursor[ 'previous_element'] or aCursor[ 'next_element'])):
            return [ False, True,]    

        theRdCtxt.pOS( u"""
                       &emsp;
                       <table   style="display: inline" cellspacing="0" cellpadding="0" frame="void"  ><tbody><tr>
                       <td  id="cid_MDDSiblingsMenu_Holder" valign="center" >
                       """)

        aRelationCursorName = theRdCtxt.fGP( 'theRelationCursorName', '')
        aReferenceFieldName = theRdCtxt.fGP( 'theReferenceFieldName', '')


        theRdCtxt.pOS( u"""
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)
        if aCursor[ 'first_element'] and not ( aCursor[ 'element_index'] == 1) and not ( aCursor[ 'element_index'] == 2):
            unTituloEnlace = u'%s %s %s %s' % ( 
                aCursor[ 'first_element'][ 'type_translations'][ 'translated_archetype_name'], 
                aCursor[ 'first_element'][ 'values_by_name'][ 'title'][ 'uvalue'], 
                aCursor[ 'first_element'][ 'values_by_name'][ 'description'][ 'uvalue'], 
                aCursor[ 'first_element'][ 'type_translations'][ 'translated_type_description'],
            )

            aLinkHREF = '%sTabular/' % aRELRES[ 'url']

            if aRelationCursorName:
                aLinkHREF = '%s?theRelationCursorName=%s&theCurrentElementUID=%s%s' % ( aLinkHREF, aRelationCursorName, aCursor[ 'first_element'][ 'UID'], theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            elif aReferenceFieldName:
                aLinkHREF = '%s?theReferenceFieldName=%s&theCurrentElementUID=%s%s' % ( aLinkHREF, aReferenceFieldName, aCursor[ 'first_element'][ 'UID'], theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            else:
                aLinkHREF = '%s%s' % ( aLinkHREF, theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),)



            theRdCtxt.pOS( u"""
                           <a id="cid_MDDLink_First"  class="state-visible" title="%(unTituloEnlace)s " 
                           href="%(aLinkHREF)s"  >
                           <img src="%(portal_url)s/primero.gif" title="%(unTituloEnlace)s" alt="%(ELEMENT-title)s" id="icon-first" />
                           <!-- <span>%(ELEMENT-title)s</span> -->
                           </a>
                           """ % {
                                   'unTituloEnlace':              fCGIE( unTituloEnlace),
                                   'portal_url':                  aSRES[ 'portal_url'],
                                   'ELEMENT-title':               fCGIE( aCursor[ 'first_element']['values_by_name'][ 'title'][ 'uvalue']),
                                   'aLinkHREF':                   aLinkHREF,
                               })
        else:
            theRdCtxt.pOS( u"""
                           <img src="%(portal_url)s/blank_icon.gif" />
                           """ % {
                                   'portal_url':                  aSRES[ 'portal_url'],
                               })

        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       &ensp;
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)



        if aCursor[ 'previous_element'] and ( aCursor[ 'element_index'] > 1):
            unTituloEnlace = u'%s %s %s %s' % ( 
                aCursor[ 'previous_element'][ 'type_translations'][ 'translated_archetype_name'], 
                aCursor[ 'previous_element'][ 'values_by_name'][ 'title'][ 'uvalue'], 
                aCursor[ 'previous_element'][ 'values_by_name'][ 'description'][ 'uvalue'], 
                aCursor[ 'previous_element'][ 'type_translations'][ 'translated_type_description'],
            )

            aLinkHREF = '%sTabular/' % aRELRES[ 'url']

            if aRelationCursorName:
                aLinkHREF = '%s?theRelationCursorName=%s&theCurrentElementUID=%s%s' % ( aLinkHREF, aRelationCursorName, aCursor[ 'previous_element'][ 'UID'], theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            elif aReferenceFieldName:
                aLinkHREF = '%s?theReferenceFieldName=%s&theCurrentElementUID=%s%s' % ( aLinkHREF, aReferenceFieldName, aCursor[ 'previous_element'][ 'UID'], theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            else:
                aLinkHREF = '%s%s' % ( aLinkHREF, theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),)



            theRdCtxt.pOS( u"""
                           <a id="cid_MDDLink_Previous"  class="state-visible" title="%(unTituloEnlace)s " 
                           href="%(aLinkHREF)s"  >
                           <img src="%(portal_url)s/anterior.gif" title="%(unTituloEnlace)s" alt="%(ELEMENT-title)s" id="icon-previous" />
                           <!-- <span>%(ELEMENT-title)s</span> -->
                           </a>
                           """ % {
                                   'unTituloEnlace':              unTituloEnlace,
                                   'portal_url':                  aSRES[ 'portal_url'],
                                   'ELEMENT-title':               fCGIE(  aCursor[ 'previous_element']['values_by_name'][ 'title'][ 'uvalue']),
                                   'aLinkHREF':                   aLinkHREF,
                               })
        else:
            theRdCtxt.pOS( u"""
                           <img src="%(portal_url)s/blank_icon.gif" />
                           """ % {
                                   'portal_url':                  aSRES[ 'portal_url'],
                               })

        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)








        theRdCtxt.pOS( u"""
                       &emsp;
                       &emsp;
                       <font size="2" >
                       <a  title="Siblings-" alt="Siblings-"
                       onclick="
                       document.getElementById( 'cid_MDDSiblingsMenu_Holder').appendChild( document.getElementById( 'cid_MDDSiblingsList_ActionsMenu')); 
                       replaceClassName( document.getElementById( 'cid_MDDSiblingsList_ActionsMenu') ,'deactivated', 'activated'); 
                       return true;">
                       <span>%(element_index)d</span>
                       /
                       <span>%(elements_count)d</span>
                       </a>
                       </font>  
                       """ % {
                               'element_index':     aCursor[ 'element_index'],
                               'elements_count':    aCursor[ 'elements_count'],
                               'portal_url':        aSRES[ 'portal_url'],
                           })   



        #theRdCtxt.pOS( u"""
        #<span>%(element_index)d</span>
        #/
        #<span>%(elements_count)d</span>
        #""" % {
            #'element_index':    aCursor[ 'element_index'],
            #'elements_count':    aCursor[ 'elements_count'],
        #})

        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       <table cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)



        if aCursor[ 'next_element'] and ( aCursor[ 'element_index'] < aCursor[ 'elements_count']):
            unTituloEnlace = u'%s %s %s %s' % ( 
                aCursor[ 'next_element'][ 'type_translations'][ 'translated_archetype_name'], 
                aCursor[ 'next_element'][ 'values_by_name'][ 'title'][ 'uvalue'], 
                aCursor[ 'next_element'][ 'values_by_name'][ 'description'][ 'uvalue'], 
                aCursor[ 'next_element'][ 'type_translations'][ 'translated_type_description'],
            )

            aLinkHREF = '%sTabular/' % aRELRES[ 'url']

            if aRelationCursorName:
                aLinkHREF = '%s?theRelationCursorName=%s&theCurrentElementUID=%s%s' % ( aLinkHREF, aRelationCursorName, aCursor[ 'next_element'][ 'UID'], theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            elif aReferenceFieldName:
                aLinkHREF = '%s?theReferenceFieldName=%s&theCurrentElementUID=%s%s' % ( aLinkHREF, aReferenceFieldName, aCursor[ 'next_element'][ 'UID'], theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            else:
                aLinkHREF = '%s%s' % ( aLinkHREF, theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),)



            theRdCtxt.pOS( u"""
                           <a id="cid_MDDLink_Previous"  class="state-visible" title="%(unTituloEnlace)s " 
                           href="%(aLinkHREF)s"  >
                           <img src="%(portal_url)s/siguiente.gif" title="%(unTituloEnlace)s" alt="%(ELEMENT-title)s" id="icon-next" />
                           <!-- <span>%(ELEMENT-title)s</span> -->
                           </a>
                           """ % {
                                   'unTituloEnlace':              fCGIE( unTituloEnlace),
                                   'portal_url':                  aSRES[ 'portal_url'],
                                   'ELEMENT-title':               fCGIE(  aCursor[ 'next_element']['values_by_name'][ 'title'][ 'uvalue']),
                                   'aLinkHREF':                   aLinkHREF,
                               })
        else:
            theRdCtxt.pOS( u"""
                           <img src="%(portal_url)s/blank_icon.gif" />
                           """ % {
                                   'portal_url':                  aSRES[ 'portal_url'],
                               })


        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       &ensp;
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr><td valign="center">
                       """)



        if aCursor[ 'last_element'] and not ( aCursor[ 'element_index'] == aCursor[ 'elements_count']) and not ( aCursor[ 'element_index'] == ( aCursor[ 'elements_count'] - 1)):
            unTituloEnlace = '%s %s %s %s' % ( 
                aCursor[ 'last_element'][ 'type_translations'][ 'translated_archetype_name'], 
                aCursor[ 'last_element'][ 'values_by_name'][ 'title'][ 'uvalue'], 
                aCursor[ 'last_element'][ 'values_by_name'][ 'description'][ 'uvalue'], 
                aCursor[ 'last_element'][ 'type_translations'][ 'translated_type_description'],
            )

            aLinkHREF = '%sTabular/' % aRELRES[ 'url']

            if aRelationCursorName:
                aLinkHREF = '%s?theRelationCursorName=%s&theCurrentElementUID=%s%s' % ( aLinkHREF, aRelationCursorName, aCursor[ 'last_element'][ 'UID'], theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            elif aReferenceFieldName:
                aLinkHREF = '%s?theReferenceFieldName=%s&theCurrentElementUID=%s%s' % ( aLinkHREF, aReferenceFieldName, aCursor[ 'last_element'][ 'UID'], theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),)

            else:
                aLinkHREF = '%s%s' % ( aLinkHREF, theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),)



            theRdCtxt.pOS( u"""
                           <a id="cid_MDDLink_last"  class="state-visible" title="%(unTituloEnlace)s " 
                           href="%(aLinkHREF)s"  >
                           <img src="%(portal_url)s/ultimo.gif" title="%(unTituloEnlace)s" alt="%(ELEMENT-title)s" id="icon-last" />
                           <!-- <span>%(ELEMENT-title)s</span> -->
                           </a>
                           """ % {
                                   'unTituloEnlace':              fCGIE( unTituloEnlace),
                                   'portal_url':                  aSRES[ 'portal_url'],
                                   'ELEMENT-title':               fCGIE( aCursor[ 'last_element']['values_by_name'][ 'title'][ 'uvalue']),
                                   'aLinkHREF':                   aLinkHREF,
                               })
        else:
            theRdCtxt.pOS( u"""
                           <img src="%(portal_url)s/blank_icon.gif" />
                           """ % {
                                   'portal_url':                  aSRES[ 'portal_url'],
                               })

        theRdCtxt.pOS( u"""
                       </td></tr></tbody></table>
                       </td></tr></tbody></table>
                       """)    


    finally:
        theRdCtxt.pSP( 'output', aCurrentOutput)

    aRenderedCursor = aNewOutput.getvalue() 
    if aRenderedCursor:
        theRdCtxt.pSP( 'RenderedRelationCursor', aRenderedCursor)
        theRdCtxt.pO( aRenderedCursor)

    return [ True, True,]






def _MDDRender_Tabular_Cabecera_SectionsMenu_Anchor( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        #return [ False, True,]

    theRdCtxt.pOS( u"""
                   &emsp;
                   &emsp;
                   <font size="1">
                   <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr>
                   <td id="cid_MDDTOC_Holder" valign="top" align="left" >
                   <a style="cursor: pointer" title="Sections-"
                   onclick="document.getElementById( 'cid_MDDTOC_Holder').appendChild( document.getElementById( 'cid_MDDSectionList_ActionsMenu')); replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated', 'activated'); return true;">
                   <img src="%(portal_url)s/menusecciones.gif" title="%(ModelDDvlPlone_Tabular_Sections)s" alt="%(ModelDDvlPlone_Tabular_Sections)s" id="icon-sectionsmenu" />
                   """ % {
                           'portal_url':                        aSRES[ 'portal_url'],
                           'ModelDDvlPlone_Tabular_Sections':   theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                       })   




    if aPREFS_PRES.get( 'DisplayActionLabels', False):
        theRdCtxt.pOS( u"""
                       <span>%(ModelDDvlPlone_Tabular_Sections)s</span>
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           })




    theRdCtxt.pOS( u"""
                   </a>
                   </td>
                   </tr></tbody></table>
                   </font>  
                   """ % {
                           'portal_url':                        aSRES[ 'portal_url'],
                           'ModelDDvlPlone_Tabular_Sections':   theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                       })   


    return [ True, True,]








def _MDDRender_Tabular_Cabecera_ChangeActions( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        #return [ False, True,]

    unPermiteEditar   = aSRES[ 'read_permission'] and aSRES[ 'write_permission']    

    if unPermiteEditar:
        unTituloEnlace = u'%s %s %s %s %s' % ( 
            theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
            aSRES[ 'type_translations'][ 'translated_archetype_name'], 
            aSRES[ 'values_by_name'][ 'title'][ 'uvalue'], 
            aSRES[ 'values_by_name'][ 'description'][ 'uvalue'], 
            aSRES[ 'type_translations'][ 'translated_type_description'],
        )

        theRdCtxt.pOS( u"""
                       &emsp;
                       <table  cellspacing="0" cellpadding="0" frame="void"  style="display: inline" ><tbody><tr><td valign="center">
                       <a id="cid_MDDActionLink_Editar"  class="state-visible" title="%(unTituloEnlace)s " 
                       href="%(SRES-url)sEditar/%(theExtraLinkHrefParams)s"  >
                       <img src="%(portal_url)s/edit.gif" alt="%(ModelDDvlPlone_editar_action_label)s" title="%(ModelDDvlPlone_editar_action_label)s" 
                       id="icon-edit" />
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'OWNER-title':                 fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                               'SRES-url':                    aSRES[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                               'ModelDDvlPlone_editar_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                           })

        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
                           <span>%(ModelDDvlPlone_editar_action_label)s</span>
                           """ % {
                                   'ModelDDvlPlone_editar_action_label':    theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label',),
                               })

        theRdCtxt.pOS( u"""
                       </a></td></tr></tbody></table>
                       """ )





    unPermiteEliminar = unPermiteEditar and aSRES[ 'delete_permission'] and aSRES[ 'container_element'][ 'read_permission'] and aSRES[ 'container_element'][ 'write_permission']    

    if unPermiteEliminar:
        unTituloEnlace = u'%s %s %s %s %s' % ( 
            theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
            aSRES[ 'type_translations'][ 'translated_archetype_name'], 
            aSRES[ 'values_by_name'][ 'title'][ 'uvalue'], 
            aSRES[ 'values_by_name'][ 'description'][ 'uvalue'], 
            aSRES[ 'type_translations'][ 'translated_type_description'],
        )

        theRdCtxt.pOS( u"""
                       &emsp;
                       <table  cellspacing="0" cellpadding="0" frame="void"  style="display: inline" ><tbody><tr><td valign="center">
                       <a id="cid_MDDActionLink_Eliminar"  class="state-visible" title="%(unTituloEnlace)s " 
                       href="%(SRES-url)sEliminar/%(theExtraLinkHrefParams)s"  >
                       <img src="%(portal_url)s/delete_icon.gif" alt="%(ModelDDvlPlone_eliminar_action_label)s" title="%(ModelDDvlPlone_eliminar_action_label)s" 
                       id="icon-delete" />
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'OWNER-title':                 fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                               'SRES-url':                    aSRES[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                               'ModelDDvlPlone_eliminar_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
                           })


        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
                           <span>%(ModelDDvlPlone_editar_action_label)s</span>
                           """ % {
                                   'ModelDDvlPlone_editar_action_label':    theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label',),
                               })

        theRdCtxt.pOS( u"""
                       </a></td></tr></tbody></table>
                       """)

    return [ True, True,]









def _MDDRender_Tabular_Cabecera_ClipboardActions( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]    

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        #return [ False, True,]

    unPermiteCopiar   = aSRES[ 'read_permission'] and aSRES[ 'is_copyable']    

    if unPermiteCopiar:
        unTituloEnlace = u'%s %s %s %s %s' % ( 
            theRdCtxt.fUITr( 'Copy'),
            aSRES[ 'type_translations'][ 'translated_archetype_name'], 
            aSRES[ 'values_by_name'][ 'title'][ 'uvalue'], 
            aSRES[ 'values_by_name'][ 'description'][ 'uvalue'], 
            aSRES[ 'type_translations'][ 'translated_type_description'],
        )

        theRdCtxt.pOS( u"""
                       &emsp;
                       <table  cellspacing="0" cellpadding="0" frame="void"  style="display: inline" ><tbody><tr><td valign="center">
                       <a id="cid_MDDActionLink_Copy"  class="state-visible" title="%(unTituloEnlace)s " 
                       href="%(SRES-url)sobject_copy"  >
                       <img src="%(portal_url)s/copy_icon.gif" alt="%(Copy)s" title="%(Copy)s" 
                       id="icon-edit" />
                       """ % {
                               'unTituloEnlace':              fCGIE( unTituloEnlace),
                               'portal_url':                  aSRES[ 'portal_url'],
                               'OWNER-title':                 fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                               'SRES-url':                    aSRES[ 'url'],
                               'SRES-UID':                    aSRES[ 'UID'],
                               'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                               'Copy': theRdCtxt.fUITr( 'Copy'),
                           })


        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
                           <span>%(Copy)s</span>
                           """ % {
                                   'Copy':    theRdCtxt.fUITr( 'Copy',),
                               })

        theRdCtxt.pOS( u"""
                       </a></td></tr></tbody></table>
                       """)


    unPermitePegar = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and aSRES[ 'allow_paste']    

    if unPermitePegar:
        aClipboardResult = theRdCtxt.fGP( 'CLIPBOARD', {})
        if aClipboardResult:

            someClipboardElementsByRoot = aClipboardResult[ 'elements_by_roots']
            if someClipboardElementsByRoot:

                unTituloEnlace = u'%s %s %s %s %s' % ( 
                    theRdCtxt.fUITr( 'Paste'),
                    aSRES[ 'type_translations'][ 'translated_archetype_name'], 
                    aSRES[ 'values_by_name'][ 'title'][ 'uvalue'], 
                    aSRES[ 'values_by_name'][ 'description'][ 'uvalue'], 
                    aSRES[ 'type_translations'][ 'translated_type_description'],
                )

                theRdCtxt.pOS( u"""
                               &emsp;
                               <table  cellspacing="0" cellpadding="0" frame="void"  style="display: inline" ><tbody><tr><td valign="center">
                               <a id="cid_MDDActionLink_Eliminar"  class="state-visible" title="%(unTituloEnlace)s " 
                               href="%(SRES-url)sobject_paste"  >
                               <img src="%(portal_url)s/paste_icon.gif" alt="%(Paste)s" title="%(Paste)s" 
                               id="icon-delete" />
                               """ % {
                                       'unTituloEnlace':              fCGIE( unTituloEnlace),
                                       'portal_url':                  aSRES[ 'portal_url'],
                                       'OWNER-title':                 fCGIE( aSRES['values_by_name'][ 'title'][ 'uvalue']),
                                       'SRES-url':                    aSRES[ 'url'],
                                       'SRES-UID':                    aSRES[ 'UID'],
                                       'theExtraLinkHrefParams':      theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                       'Paste': theRdCtxt.fUITr( 'Paste'),
                                   })

                if aPREFS_PRES.get( 'DisplayActionLabels', False):
                    theRdCtxt.pOS( u"""
                                   <span>%(Paste)s</span>
                                   """ % {
                                           'Paste':    theRdCtxt.fUITr( 'Paste'),
                                       })


                theRdCtxt.pOS( u"""
                               </a></td></tr></tbody></table>
                               """ )

    return [ True, True,]







def _MDDRender_Tabular_Values( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    aExcludeTitle = theRdCtxt.fGP( 'ExcludeTitle', True)
    aExcludeID    = theRdCtxt.fGP( 'ExcludeId',    False)

    unosNonTextFieldsNames = aSRES.get( 'non_text_field_names', [])

    if aExcludeTitle and aExcludeID and ( not unosNonTextFieldsNames):
        return [ False, True,]

    theRdCtxt.pOS( u"""
                   <table id="hidMDDValues" width="100%%" class="listing" summary="%(ModelDDvlPlone_caracteristicas_tabletitle)s" >
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
                       <tr id="hidMDDValues_Row_id" class="%(RowClass)s" 
                       <td align="left">
                       <strong id="hidMDDValores_Row_id_label">%(ModelDDvlPlone_id_label)s</strong>
                       &emsp;
                       <span   id="hidMDDValores_Row_id_help"class="formHelp">%(ModelDDvlPlone_id_help)s</span>                   
                       </td>
                       <td align="left" >%(SRES_id)s</td>
                       """ %  {
                               'RowClass':                                  cClasesFilas[ unIndexClassFila % 2],
                               'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
                               'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
                               'SRES_id':                                   fCGIE( aSRES.get( 'id', '')),
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
                               <tr id="hidMDDValores_Row_%(attribute_name)s" class="%(RowClass)s"  >
                               <td align="left">
                               <strong id="hidMDDValores_Row_%(attribute_name)s_label">%(attribute_label)s</strong>
                               &emsp;
                               <span   id="hidMDDValores_Row_%(attribute_name)s_help" class="formHelp">%(attribute_description)s</span>                   
                               </td>
                               """ % {
                                       'attribute_name':                            fCGIE( unAttributeName),
                                       'attribute_label':                           fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_label', '')),
                                       'attribute_description':                     fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_description', '')),
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
                                   <td id="hidMDDValores_Row_%(attribute_name)s_value" align="left" >%(attribute_value)s</td>
                                   """ % {
                                           'attribute_name':                        fCGIE( unAttributeName),
                                           'attribute_value':                       fCGIE( unAttributeValue),
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

    return [ True, True,]










def _MDDRender_Tabular_Texts( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        #return [ False, True,]

    unosTextFieldsNames = aSRES.get( 'text_field_names', [])

    if not unosTextFieldsNames:
        return [ False, True,]

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
                               <table id="hidMDDTexto_%(attribute_name)s_table" width="100%%" class="listing" summary="%(attribute_label)s" >
                               <thead>
                               <tr>
                               <th class="nosort" align="left">
                               <strong id="hidMDDTexto_%(attribute_name)s_label">%(attribute_label)s</strong>
                               &emsp;
                               <span   id="hidMDDTexto_%(attribute_name)s_help" class="formHelp">%(attribute_description)s</span>  
                               &emsp;
                               &emsp;
                               <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr>
                               <td id="cid_MDDTOC_Holder_Texto_%(attribute_name)s" valign="top" align="left">
                               <a    title="%(ModelDDvlPlone_Tabular_Sections)s"
                               onclick="
                               document.getElementById( 'cid_MDDTOC_Holder_Texto_%(attribute_name)s').appendChild( document.getElementById( 'cid_MDDSectionList_ActionsMenu')); 
                               replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated', 'activated');">
                               <img src="%(portal_url)s/menusecciones.gif" title="%(ModelDDvlPlone_Tabular_Sections)s" alt="%(ModelDDvlPlone_Tabular_Sections)s" id="icon-sectionsmenu" />
                               """ % {        
                                       'portal_url':                                aSRES[ 'portal_url'],
                                       'ModelDDvlPlone_Tabular_Sections':           theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                                       'attribute_name':                            fCGIE( unAttributeName),
                                       'attribute_label':                           fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_label', '')),
                                       'attribute_description':                     fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_description', '')),
                                       'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
                                       'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
                                   })






                if aPREFS_PRES.get( 'DisplayActionLabels', False):
                    theRdCtxt.pOS( u"""
                                   <span>%(ModelDDvlPlone_Tabular_Sections)s</span>
                                   """ % {
                                           'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                                       })





                theRdCtxt.pOS( u"""
                               </a>
                               </td>
                               </tr></tbody></table>
                               </th>
                               </tr>
                               </thead>
                               <tbody>
                               <tr class="odd">
                               """ % {        
                                       'portal_url':                                aSRES[ 'portal_url'],
                                       'ModelDDvlPlone_Tabular_Sections':           theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                                       'attribute_name':                            fCGIE( unAttributeName),
                                       'attribute_label':                           fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_label', '')),
                                       'attribute_description':                     fCGIE( aATTRRES.get( 'attribute_translations', {}).get( 'translated_description', '')),
                                       'ModelDDvlPlone_id_label':                   theRdCtxt.fUITr( 'ModelDDvlPlone_id_label'),
                                       'ModelDDvlPlone_id_help':                    theRdCtxt.fUITr( 'ModelDDvlPlone_id_help'),
                                   })






                if aATTRRES.get( 'read_permission', False):

                    unAttributeValue = aATTRRES.get( 'translated_value', u'')

                    theRdCtxt.pOS( u"""
                                   <td>
                                   <p id="hidMDDTexto_%(attribute_name)s_para">
                                   """% {
                                          'attribute_name':                            unAttributeName,
                                      })

                    if unAttributeValue:

                        unasLineasTexto = unAttributeValue.splitlines()
                        unNumLineas     = len( unasLineasTexto)

                        unIndexLinea = 0
                        for unaLineaTexto in unasLineasTexto:

                            unaLineaTextoStripped = fCGIE( unaLineaTexto.lstrip())
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
                                   <td bgcolor="%(cNoValueBGColor)s"><p id="hidMDDTexto_%(attribute_name)s_para" />&ensp;</td>
                                   """ % {
                                           'cNoValueBGColor':                           cNoValueBGColor,
                                           'attribute_name':                            fCGIE( unAttributeName),
                                       })


                theRdCtxt.pOS( u"""
                               </tr>
                               </table>
                               <br/>""" )


    return [ True, True,]











def _MDDRender_Tabular_CustomPresentationViews( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    unosTextFieldsNames = aSRES.get( 'text_field_names', [])

    if not unosTextFieldsNames:
        return [ False, True,]

    aModelDDvlPloneTool = theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if not aModelDDvlPloneTool:
        return [ False, False,]

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
                theRdCtxt.pO( unCustomViewRendering)


    return [ True, True,]









def _MDDRender_Tabular_Traversals( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    unasTraversals = aSRES.get( 'traversals', [])

    if not unasTraversals:
        return [ False, True,]


    anOk          = None
    aGo           = True
    unUnwindTrick = True
    while( unUnwindTrick):

        unUnwindTrick = False


        for aTRAVRES in unasTraversals:

            if aTRAVRES:

                aTraversalKind    = aTRAVRES.get( 'traversal_kind', '')

                if aTraversalKind == 'aggregation':

                    aRdCtxt = theRdCtxt.fNewCtxt( {
                        'TRAVRES': aTRAVRES
                    })

                    anIsCollection = aTRAVRES.get( 'is_collection', False)

                    if anIsCollection:

                        if not cExtensionsForbidden:
                            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Coleccion_Sola_Before')( aRdCtxt)
                            if not aGo:
                                break
                        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Coleccion_Sola')( aRdCtxt)
                        if not aGo:
                            break
                        if not cExtensionsForbidden:
                            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Coleccion_Sola_After')( aRdCtxt)
                            if not aGo:
                                break

                    else:

                        aContainsCollections = aTRAVRES.get( 'contains_collections', False)

                        if aContainsCollections:

                            if not cExtensionsForbidden:
                                anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_ColeccionesEnTabla_Before')( aRdCtxt)
                                if not aGo:
                                    break
                            anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_ColeccionesEnTabla')( aRdCtxt)
                            if not aGo:
                                break
                            if not cExtensionsForbidden:
                                anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_ColeccionesEnTabla_After')( aRdCtxt)
                                if not aGo:
                                    break

                        else:

                            if not cExtensionsForbidden:
                                anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SinColeccionEnTabla_Before')( aRdCtxt)
                                if not aGo:
                                    break
                            anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_SinColeccionEnTabla')( aRdCtxt)
                            if not aGo:
                                break
                            if not cExtensionsForbidden:
                                anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_SinColeccionEnTabla_After')( aRdCtxt)
                                if not aGo:
                                    break




                elif aTraversalKind == 'relation':

                    aRdCtxt = theRdCtxt.fNewCtxt( {
                        'TRAVRES': aTRAVRES
                    })

                    anIsMultiValued = aTRAVRES.get( 'is_multivalued', False)

                    if anIsMultiValued:

                        if not cExtensionsForbidden:
                            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_ReferenciasEnTabla_Before')( aRdCtxt)
                            if not aGo:
                                break
                        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_ReferenciasEnTabla')( aRdCtxt)
                        if not aGo:
                            break
                        if not cExtensionsForbidden:
                            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_ReferenciasEnTabla_After')( aRdCtxt)
                            if not aGo:
                                break

                    else:

                        if not cExtensionsForbidden:
                            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_ReferenciaEnTabla_Before')( aRdCtxt)
                            if not aGo:
                                break
                        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_ReferenciaEnTabla')( aRdCtxt)
                        if not aGo:
                            break
                        if not cExtensionsForbidden:
                            anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_ReferenciaEnTabla_After')( aRdCtxt)
                            if not aGo:
                                break
                        pass 



                elif aTraversalKind == 'aggregation-plone':

                    aRdCtxt = theRdCtxt.fNewCtxt( {
                        'TRAVRES': aTRAVRES
                    })


                    if not cExtensionsForbidden:
                        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Tabla_Plone_Before')( aRdCtxt)
                        if not aGo:
                            break
                    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Tabla_Plone')( aRdCtxt)
                    if not aGo:
                        break
                    if not cExtensionsForbidden:
                        anOk, aGo = _fMCtx( True, theRdCtxt, 'MDDExtension_Render_Tabular_Tabla_Plone_After')( aRdCtxt)
                        if not aGo:
                            break


    return [ True, aGo,]








def _MDDRender_Tabular_Coleccion_Sola( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]



    someElements = aTRAVRES.get( 'elements', [])

    unSiempre = theRdCtxt.fGP( 'theSiempre', True)



    if someElements or unSiempre:

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Tabla')( theRdCtxt)


    return [ True, aGo,]





def _MDDRender_Tabular_SinColeccionEnTabla( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        #return [ False, True,]

    someElements = aTRAVRES.get( 'elements', [])

    unSiempre = theRdCtxt.fGP( 'theSiempre', True)



    if someElements or unSiempre:

        theRdCtxt.pOS( u"""
                       <h2 id="hidMDDTraversal_%(traversal_name)s_label" >
                       %(traversal_label)s
                       <font size=1">            
                       &emsp;
                       &emsp;
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr>
                       <td id="cid_MDDTOC_Holder_Traversal_%(traversal_name)s" valign="top" align="left">
                       <a title="%(ModelDDvlPlone_Tabular_Sections)s"
                       onclick="document.getElementById( 'cid_MDDTOC_Holder_Traversal_%(traversal_name)s').appendChild( document.getElementById( 'cid_MDDSectionList_ActionsMenu')); if ( hasClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated' )) { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated', 'activated');} else { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'activated', 'deactivated')} return true;">
                       <img src="%(portal_url)s/menusecciones.gif" title="%(ModelDDvlPlone_Tabular_Sections)s" alt="%(ModelDDvlPlone_Tabular_Sections)s" id="icon-sectionsmenu" />
                       """ % {
                               'portal_url':                       aSRES[ 'portal_url'],
                               'ModelDDvlPlone_Tabular_Sections':  theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                               'traversal_name':                   fCGIE( aTRAVRES[ 'traversal_name']),        
                               'traversal_label':                  fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                               'traversal_description':            fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
                           })





    if aPREFS_PRES.get( 'DisplayActionLabels', False):
        theRdCtxt.pOS( u"""
                       <span>%(ModelDDvlPlone_Tabular_Sections)s</span>
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           })





    if someElements or unSiempre:

        theRdCtxt.pOS( u"""
                       </a>
                       </td>
                       </tr></tbody></table>
                       </font>
                       </h2>
                       <table id="hidMDDTraversal_%(traversal_name)s_table" width="100%%" cellspacing="0" cellpadding="0" frame="void">
                       <tr>
                       <td id="hidMDDTraversal_%(traversal_name)s_description" align="left" valign="baseline" class="formHelp">%(traversal_description)s</td>
                       <td align="right" valign="baseline"> 
                       </td>
                       </tr>
                       </table>
                       """ % {
                               'portal_url':                       aSRES[ 'portal_url'],
                               'ModelDDvlPlone_Tabular_Sections':  theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                               'traversal_name':                   fCGIE( aTRAVRES[ 'traversal_name']),        
                               'traversal_label':                  fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                               'traversal_description':            fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
                           })




        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Tabla')( theRdCtxt)

    return [ True, aGo,]








def _MDDRender_Tabular_ColeccionesEnTabla( theRdCtxt):
    """Render an aggregation traversal containing collections, rendering a header for the traversal, and rendering each contained collection with a header and a table with a row for each collection element.

    """
    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, False,]

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, False,]

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        #return [ False, True,]


    someElements = aTRAVRES.get( 'elements', [])
    unSiempre = theRdCtxt.fGP( 'theSiempre', True)

    if not( someElements or unSiempre):
        return [ False, True,]


    # ######################################################
    """Traversal name and description as a prominent header for multiple collections, each of them is rendered below with its own header and table.

    """
    theRdCtxt.pOS( u"""
                   <h2 id="hidMDDTraversal_%(traversal_name)s_label" >
                   %(traversal_label)s
                   <font size=1">
                   &emsp;
                   &emsp;
                   <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr>
                   <td id="cid_MDDTOC_Holder_Traversal_%(traversal_name)s" valign="top" align="left">
                   <a title="%(ModelDDvlPlone_Tabular_Sections)s"
                   onclick="document.getElementById( 'cid_MDDTOC_Holder_Traversal_%(traversal_name)s').appendChild( document.getElementById( 'cid_MDDSectionList_ActionsMenu')); if ( hasClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated' )) { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated', 'activated');} else { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'activated', 'deactivated')} return true;">
                   <img src="%(portal_url)s/menusecciones.gif" title="%(ModelDDvlPlone_Tabular_Sections)s" alt="%(ModelDDvlPlone_Tabular_Sections)s" id="icon-sectionsmenu" />
                   """ % {
                           'portal_url':                         aSRES[ 'portal_url'],
                           'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           'traversal_name':                     fCGIE( aTRAVRES[ 'traversal_name']),        
                           'traversal_label':                    fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                           'traversal_description':              fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
                       })


    if aPREFS_PRES.get( 'DisplayActionLabels', False):
        theRdCtxt.pOS( u"""
                       <span>%(ModelDDvlPlone_Tabular_Sections)s</span>
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           })



    theRdCtxt.pOS( u"""
                   </a>
                   </td>
                   </tr></tbody></table>
                   </font>
                   </h2>
                   <table id="hidMDDTraversal_%(traversal_name)s_table" width="100%%" cellspacing="0" cellpadding="0" frame="void">
                   <tbody>
                   <tr>
                   <td id="hidMDDTraversal_%(traversal_name)s_description" align="left" valign="baseline" class="formHelp">%(traversal_description)s</td>
                   <td align="right" valign="baseline"> 
                   """ % {
                           'portal_url':                         aSRES[ 'portal_url'],
                           'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           'traversal_name':                     fCGIE( aTRAVRES[ 'traversal_name']),        
                           'traversal_label':                    fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                           'traversal_description':              fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
                       })

    # ######################################################
    """Factories to create contained collections.

    """
    someFactories = aTRAVRES.get( 'factories', [])
    if someFactories:

        unPermiteCrearColecciones = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                                  aSRES[ 'add_permission'] and aSRES[ 'add_collection_permission'] and \
                                  aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                                  ( not aTRAVRES[ 'max_multiplicity_reached']) and \
                                  not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))

        if unPermiteCrearColecciones :

            if len( someFactories) == 1:

                theRdCtxt.pOS( u"""
                               <a  id="hidMDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Link"
                               href="%(url)sCrear/?theNewTypeName=%(theMetaType)s&theAggregationName=%(traversal_name)s"  
                               title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" >

                               <img src="%(portal_url)s/add_icon.gif" id="hidMDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Icon"
                               title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" 
                               alt="%(ModelDDvlPlone_crear_action_label)s" />
                               """ % {
                                       'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                       'translated_archetype_name':         fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name']),
                                       'translated_type_description':       fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_type_description']),
                                       'url':                               aSRES[ 'url'],
                                       'theMetaType':                       fCGIE( aTRAVRES[ 'factories'][ 0][ 'meta_type']),
                                       'traversal_name':                    fCGIE( aTRAVRES[ 'traversal_name']),
                                       'portal_url':                        aSRES[ 'portal_url'],
                                   })

                if aPREFS_PRES.get( 'DisplayActionLabels', False):
                    theRdCtxt.pOS( u"""
                                   &nbsp;
                                   %(ModelDDvlPlone_crear_action_label)s
                                   &nbsp;
                                   %(translated_archetype_name)s       
                                   """ % {
                                           'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                           'translated_archetype_name':         fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name']),
                                       })

                theRdCtxt.pOS( u"""
                               </a>
                               """)

            else:

                theRdCtxt.pOS( u""" 
                               <img src="%(portal_url)s/add_icon.gif" title="%(ModelDDvlPlone_crear_action_label)s " alt="%(ModelDDvlPlone_crear_action_label)s" />
                               &nbsp;
                               %(ModelDDvlPlone_crear_action_label)s
                               """ % {
                                       'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                       'url':                               aSRES[ 'url'],
                                       'traversal_name':                    fCGIE( aTRAVRES[ 'traversal_name']),
                                       'portal_url':                        aSRES[ 'portal_url'],
                                   })

                for aFactory in someFactories:

                    theRdCtxt.pOS( u"""
                                   <a  id="hidMDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Link"
                                   href="%(url)sCrear/?theNewTypeName=%(theMetaType)s&theAggregationName=%(traversal_name)s"  
                                   title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" >

                                   <img src="%(portal_url)s/add_icon.gif" id="hidMDDTraversal_%(traversal_name)s_Factory_%(theMetaType)s_Icon"
                                   title="%(ModelDDvlPlone_crear_action_label)s %(translated_archetype_name)s: %(translated_type_description)s" 
                                   alt="%(ModelDDvlPlone_crear_action_label)s" />
                                   </a>
                                   """ % {
                                           'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                           'translated_archetype_name':         fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name']),
                                           'translated_type_description':       fCGIE( aFactory[ 'type_translations'][ 'translated_type_description']),
                                           'url':                               aSRES[ 'url'],
                                           'theMetaType':                       fCGIE( aFactory[ 'meta_type']),
                                           'traversal_name':                    fCGIE( aTRAVRES[ 'traversal_name']),
                                           'portal_url':                        aSRES[ 'portal_url'],
                                       })

                    if False and aPREFS_PRES.get( 'DisplayActionLabels', False):
                        theRdCtxt.pOS( u"""
                                       &nbsp;
                                       %(ModelDDvlPlone_crear_action_label)s
                                       &nbsp;
                                       %(translated_archetype_name)s       
                                       """ % {
                                               'ModelDDvlPlone_crear_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                               'translated_archetype_name':         fCGIE( aTRAVRES[ 'factories'][ 0][ 'type_translations'][ 'translated_archetype_name']),
                                           })

                    theRdCtxt.pOS( u"""
                                   </a>
                                   """)


    theRdCtxt.pOS( u"""
                   </td>
                   </tr>
                   </tbody>
                   </table>
                   """)


    if ( not someElements):
        theRdCtxt.pOS( u"""
                       <br/>
                       """)
        return [ True, True,]



    # ######################################################
    """Iterate and drill-down into each contained collection, rendering for each one a title and a table with a row for each collection content element.

    """

    unIndex = 0
    for aSUBSRES in someElements:

        aSubRdCtxt = theRdCtxt.fNewCtxt( {
            'PARENT_SRES':    aSRES,
            'PARENT_TRAVRES': aTRAVRES,
            'SRES':           aSUBSRES,
            'index':          unIndex,
        })

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_ColeccionEnTabla')( aSubRdCtxt)
        if not aGo:
            return [ False, True,]
        unIndex += 1

    theRdCtxt.pOS( u"""
                   <br/>
                   """)

    return [ True, True,]









def _MDDRender_Tabular_ColeccionEnTabla( theRdCtxt):
    """Render a collection, with a header and a table with a row for each collection element.

    """

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]


    anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_ColeccionEnTabla_Header')( theRdCtxt)
    if not aGo:
        return [ False, True,]

    someTraversalNames = aSRES.get( 'traversal_names', [])

    for aTraversalName in someTraversalNames: 
        """Collections usually have a single traversal for their aggregated contents, but may have many, as any other aggregation traversal config.

        """

        aTRAVRES = aSRES[ 'traversals_by_name'][ aTraversalName]

        aRdCtxt = theRdCtxt.fNewCtxt( {
            'TRAVRES': aTRAVRES,
        })

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Tabla')(                  aRdCtxt)
    if not aGo:
        return [ False, True,]

    return [ True, True,]





def _MDDRender_Tabular_ColeccionEnTabla_Header( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    if not aPARENT_SRES:
        return [ False, True,]

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        #return [ False, True,]


    aNumCollections = len( aTRAVRES.get( 'elements', []))

    aSRESIndex = theRdCtxt.fGP( 'index', 0)


    theRdCtxt.pOS( u"""
                   <table id="hidMDDCol_%(parent_traversal_name)s_Elem_%(SRES-id)s_Header" 
                   width="100%%" cellspacing="0" cellpadding="0" frame="void">
                   <tbody>
                   <tr>
                   """   % {
                             'parent_traversal_name':             fCGIE( aTRAVRES[ 'traversal_name']),
                             'SRES-id':                           fCGIE( aSRES[ 'id']),
                         })




    unPermiteOrdenarColecciones = aPARENT_SRES[ 'read_permission'] and aPARENT_SRES[ 'write_permission'] and \
                                aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                                aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission']

    if ( aNumCollections > 1) and unPermiteOrdenarColecciones:
        theRdCtxt.pOS( u"""
                       <td align="left" valign="baseline" width="40" >
                       """ )

        if aSRESIndex:
            theRdCtxt.pOS( u"""
                           <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Subir_Link"
                           title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                           href="%(PARENTSRES-url)sTabular/?theMovedElementID=%(SRES-id)s&theMoveDirection=Up&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_link" >                
                           <img id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Subir_Icon"
                           alt="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                           title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                           src="%(portal_url)s/arrowUp.gif" />
                           </a>
                           """ % {
                                   'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                   'ModelDDvlPlone_subir_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                                   'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                                   'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                   'SRES-id':                             fCGIE( aSRES[ 'id']),
                                   'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
                                   'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                   'millis':                              fMillisecondsNow(), 
                                   'SRES-UID':                            fCGIE( aSRES[ 'UID']),
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


        if not( aSRESIndex == ( aNumCollections - 1)):
            theRdCtxt.pOS( u"""
                           <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Bajar_Link"
                           title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                           href="%(PARENTSRES-url)sTabular/?theMovedElementID=%(SRES-id)s&theMoveDirection=Down&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(SRES-UID)s_link" >                
                           <img  id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Bajar_Icon"
                           alt="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                           title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(SRES-title)s"
                           src="%(portal_url)s/arrowDown.gif" />
                           </a>
                           """ % {
                                   'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                   'ModelDDvlPlone_bajar_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                                   'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                                   'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                   'SRES-id':                             fCGIE( aSRES[ 'id']),
                                   'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
                                   'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                   'millis':                              fMillisecondsNow(), 
                                   'SRES-UID':                            fCGIE( aSRES[ 'UID']),
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
                   <a name="hidMDDElemento_%(SRES-UID)s_link" 
                   href="%(SRES-url)sTabular/%(theExtraLinkHrefParams)s" 
                   title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(Element-title)s" >
                   <img src="%(portal_url)s/%(content_icon)s" 
                   alt="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                   title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(SRES-title)s" />
                   <span id="hidMDDElemento_%(SRES-UID)s_title" class="state-visible">%(Element-title)s</span>
                   </a>
                   <font size=1" style="font-weight: normal;">            
                   &emsp;
                   &emsp;
                   <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr>
                   <td id="cid_MDDTOC_Holder_Traversal_%(traversal_name)s_%(SRES-id)s" valign="top" align="left">
                   <a title="%(ModelDDvlPlone_Tabular_Sections)s"
                   onclick="document.getElementById( 'cid_MDDTOC_Holder_Traversal_%(traversal_name)s_%(SRES-id)s').appendChild( document.getElementById( 'cid_MDDSectionList_ActionsMenu')); if ( hasClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated' )) { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated', 'activated');} else { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'activated', 'deactivated')} return true;">
                   <img src="%(portal_url)s/menusecciones.gif" title="%(ModelDDvlPlone_Tabular_Sections)s" alt="%(ModelDDvlPlone_Tabular_Sections)s" id="icon-sectionsmenu" />
                   """ % {
                           'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                           'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                           'Element-title':                       fCGIE( aTitleForElement),
                           'SRES-title':                          fCGIE( aSRES[ 'title']),
                           'SRES-id':                             fCGIE( aSRES[ 'id']),
                           'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
                           'SRES-url':                            aSRES[ 'url'],
                           'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                           'millis':                              fMillisecondsNow(), 
                           'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                           'portal_url':                          aSRES[ 'portal_url'],
                           'content_icon':                        fCGIE( aSRES[ 'content_icon']),
                       })


    if aPREFS_PRES.get( 'DisplayActionLabels', False):
        theRdCtxt.pOS( u"""
                       <span>%(ModelDDvlPlone_Tabular_Sections)s</span>
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           })



    theRdCtxt.pOS( u"""
                   </a>
                   </td>
                   </tr></tbody></table>
                   </font>
                   </h3>
                   </td>        
                   """ % {
                           'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                           'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                           'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                           'Element-title':                       fCGIE( aTitleForElement),
                           'SRES-title':                          fCGIE( aSRES[ 'title']),
                           'SRES-id':                             fCGIE( aSRES[ 'id']),
                           'PARENTSRES-url':                      aPARENT_SRES[ 'url'],
                           'SRES-url':                            aSRES[ 'url'],
                           'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                           'millis':                              fMillisecondsNow(), 
                           'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                           'portal_url':                          aSRES[ 'portal_url'],
                           'content_icon':                        fCGIE( aSRES[ 'content_icon']),
                       })




    if aSRESIndex:
        theRdCtxt.pOS( u"""
                       <td align="left" valign="baseline">
                       &nbsp;
                       <span class="formHelp">%(translated_type_description)s</span>
                       </td>        
                       """ % {
                               'translated_type_description':           fCGIE( aSRES[ 'type_translations'][ 'translated_type_description']), 
                           })
    else:
        theRdCtxt.pOS( u"""
                       <td align="left" valign="baseline">
                       &nbsp;
                       </td>        
                       """ )


    unPermiteCopiarColeccion = aSRES[ 'read_permission'] and aSRES[ 'is_copyable'] 
    unPermiteEditarColeccion = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] 
    unPermiteEliminarColeccion = aPARENT_SRES[ 'read_permission'] and aPARENT_SRES[ 'write_permission'] and \
                               aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and aSRES[ 'delete_permission']

    if unPermiteCopiarColeccion:                                
        theRdCtxt.pOS( u"""
                       <td width="%(CELL-width)d" align="center" valign="baseline">                                
                       <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Copy_Link"
                       href="%(SRES-url)sobject_copy/" 
                       title="%(Copy)s %(translated_archetype_name)s %(SRES-title)s" >
                       <img src="%(portal_url)s/copy_icon.gif"
                       alt="%(Copy)s" 
                       title="%(Copy)s %(translated_archetype_name)s %(SRES-title)s" 
                       id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Copy_Icon" />
                       """ % {
                               'CELL-width':                          (aPREFS_PRES.get( 'DisplayActionLabels', False) and 120) or 20,
                               'Copy':                                theRdCtxt.fUITr( 'Copy'),
                               'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                               'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                               'SRES-id':                             fCGIE( aSRES[ 'id']),
                               'SRES-url':                            aSRES[ 'url'],
                               'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                               'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                               'portal_url':                          aSRES[ 'portal_url'],
                           })

        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
                           <span>%(Copy)s</span>        
                           """ % {
                                   'Copy':  theRdCtxt.fUITr( 'Copy'),
                               })

        theRdCtxt.pOS( u"""
                       </a>
                       </td>
                       """)


    if unPermiteCopiarColeccion and ( unPermiteEliminarColeccion or unPermiteEditarColeccion):
        theRdCtxt.pOS( u"""
                       <td width="20" />
                       """)        

    if unPermiteEditarColeccion:                                
        theRdCtxt.pOS( u"""
                       <td width="%(CELL-width)d" align="center" valign="baseline">                                
                       <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Editar_Link"
                       href="%(SRES-url)sEditar/'" 
                       title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(SRES-title)s" >
                       <img src="%(portal_url)s/edit.gif"
                       alt="%(ModelDDvlPlone_editar_action_label)s" 
                       title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                       id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Editar_Icon" />
                       """ % {
                               'CELL-width':                          (aPREFS_PRES.get( 'DisplayActionLabels', False) and 120) or 20,
                               'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                               'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                               'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                               'SRES-id':                             fCGIE( aSRES[ 'id']),
                               'SRES-url':                            aSRES[ 'url'],
                               'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                               'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                               'portal_url':                          aSRES[ 'portal_url'],
                           })

        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
                           <span>%(ModelDDvlPlone_editar_action_label)s</span>        
                           """ % {
                                   'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                               })

        theRdCtxt.pOS( u"""
                       </a>
                       </td>
                       """)

    if unPermiteEditarColeccion and unPermiteEliminarColeccion:
        theRdCtxt.pOS( u"""
                       <td width="20" />
                       """)


    if unPermiteEliminarColeccion:                                
        theRdCtxt.pOS( u"""
                       <td width="%(CELL-width)d" align="center" valign="baseline" >                                
                       <a id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Eliminar_Link"
                       href="%(SRES-url)sEliminar/'" 
                       title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(SRES-title)s" >
                       <img src="%(portal_url)s/delete_icon.gif"
                       alt="%(ModelDDvlPlone_eliminar_action_label)s" 
                       title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(SRES-title)s" 
                       id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-UID)s_Eliminar_Icon" />
                       """ % {
                               'CELL-width':                          (aPREFS_PRES.get( 'DisplayActionLabels', False) and 120) or 20,
                               'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
                               'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                               'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                               'SRES-id':                             fCGIE( aSRES[ 'id']),
                               'SRES-url':                            aSRES[ 'url'],
                               'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                               'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                               'portal_url':                          aSRES[ 'portal_url'],
                           })
        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
                           <span>%(ModelDDvlPlone_eliminar_action_label)s</span>        
                           """ % {
                                   'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
                               })

        theRdCtxt.pOS( u"""
                       </a>
                       </td>
                       """)

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


    return [ True, True,]














def _MDDRender_Tabular_Tabla( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    #aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    #if not aPARENT_SRES:
        #return [ False, True,]


    aSRESIndex = theRdCtxt.fGP( 'index', 0)

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]

    aPARENT_TRAVRES = theRdCtxt.fGP( 'PARENT_TRAVRES', {})

    aTableTraversalName = ''
    if aPARENT_TRAVRES:
        aTableTraversalName = aPARENT_TRAVRES[ 'traversal_name']
    else:        
        aTableTraversalName = aTRAVRES[ 'traversal_name']

    if not aTableTraversalName:
        return [ False, True,]

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        # return [ False, True,]

    someElements  = aTRAVRES.get( 'elements', [])
    unNumElements = len( someElements)
    unSiempre    = theRdCtxt.fGP( 'theSiempre', True)


    unIdTabla = 'hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Table' % {
        'traversal_name':                     aTableTraversalName,
        'SRES-id':                            aSRES[ 'id'],
    }
    theRdCtxt.pSP( 'unIdTabla', unIdTabla)

    theRdCtxt.pOS( u"""
                   <table width="100%%" class="listing"  id="hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Table"
                   summary="%(SRES-title)s">
                   <tbody>
                   <tr>
                   """ % {
                           'unIdTabla':                           fCGIE( unIdTabla),
                           'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
                           'translated_archetype_name':           fCGIE( aSRES[ 'type_translations'][ 'translated_archetype_name']), 
                           'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                           'SRES-id':                             fCGIE( aSRES[ 'id']),
                           'SRES-url':                            aSRES[ 'url'],
                           'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                           'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                           'portal_url':                          aSRES[ 'portal_url'],
                       })



    unPermiteModificarAlgunElemento = False
    for aERES in someElements:
        if aERES[ 'read_permission'] and ( aERES[ 'write_permission'] or aERES[ 'delete_permission']):
            unPermiteModificarAlgunElemento = True
            break



    unPermiteEliminarAlgunElemento = False
    unPermiteEliminarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                               aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                               not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))

    if unPermiteEliminarElementos:
        for aERES in someElements:
            if aERES[ 'read_permission'] and ( aERES[ 'write_permission'] or aERES[ 'delete_permission']):
                unPermiteEliminarAlgunElemento = True
                break


    theRdCtxt.pOS( u"""
                   <col width="24" />
                   """)

    if unPermiteModificarAlgunElemento:
        theRdCtxt.pOS( u"""
                       <col width="%d" />
                       """ % ( unPermiteEliminarAlgunElemento and 120) or 100 )



    unosColumnNames = aTRAVRES.get( 'column_names', [])

    unNumColumnNames =len( unosColumnNames)

    theRdCtxt.pOS( u"""
                   <col/>
                   """ * unNumColumnNames)


    theRdCtxt.pOS( u"""
                   <thead>
                   <tr>
                   """)



    theRdCtxt.pOS( u"""
                   <th class="nosort" align="left" >
                   <input type="checkbox"  class="noborder"  value=""
                   name="%(unIdTabla)s_SelectAll" id="%(unIdTabla)s_SelectAll" 
                   onchange="pMDDToggleAllSelections('%(unIdTabla)s'); return true;"/>
                   """ %{
                           'unIdTabla':                           fCGIE( unIdTabla),
                       })


    if not unPermiteModificarAlgunElemento:

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Traversals_Aggregations_GroupActionsMenu')( theRdCtxt)

        theRdCtxt.pOS( u"""
                       </th>
                       """)
    else:
        theRdCtxt.pOS( u"""
                       </th>
                       <th class="nosort" align="left" > 
                       """)

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Traversals_Aggregations_GroupActionsMenu')( theRdCtxt)

        theRdCtxt.pOS( u"""
                       </th>
                       """)





    for unColumnName in unosColumnNames:
        theRdCtxt.pOS( u"""
                       <th class="nosort" align="left">%s</th>
                       """ % fCGIE( aTRAVRES[ 'column_translations'].get( unColumnName, {}).get( 'translated_label', unColumnName))
                           )

    theRdCtxt.pOS( u"""
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
                                'unIdTabla': fCGIE( unIdTabla),
                                'Row-Class': cClasesFilas[ unIndexElemento % 2],
                                'Row-Index': unIndexElemento,
                            })


        aSubRdCtxt.pOS( u"""
                        <td align="center" valign="baseline">
                        <input type="checkbox"  class="noborder"  value=""
                        name="%(unIdTabla)s_Select_%(Row-Index)d"
                        id="%(unIdTabla)s_Select_%(Row-Index)d"  />
                        </td>
                        """ % {
                                'Row-Index': unIndexElemento,
                                'unIdTabla': fCGIE( unIdTabla),
                            })



        if unPermiteModificarAlgunElemento:

            aSubRdCtxt.pOS( u"""
                            <td align="center" valign="baseline" id="%(unIdTabla)s_%(ERES-UID)s_ChangesLinks_Cell">
                            """ % {
                                    'unIdTabla':                fCGIE( unIdTabla),
                                    'ERES-UID':                 fCGIE( aERES[ 'UID']),
                                })

            if aERES[ 'write_permission']:

                if aERES[ 'delete_permission']:
                    aSubRdCtxt.pOS( u"""
                                    <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Delete_Link"
                                    href="%(ERES-url)sEliminar/%(theExtraLinkHrefParams)s" 
                                    title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                    <img 
                                    alt="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                    title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                    id="icon-delete" src="%(portal_url)s/delete_icon.gif"  />
                                    </a>
                                    &nbsp;    

                                    """ %{
                                            'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                            'Row-Index':                           unIndexElemento,
                                            'unIdTabla':                           fCGIE( unIdTabla),
                                            'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
                                            'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                            'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                            'ERES-url':                            aERES[ 'url'],
                                            'portal_url':                          aERES[ 'portal_url'],
                                        })

                else:
                    aSubRdCtxt.pOS( u"""
                                    <img src="%s/blank_icon.gif"  alt="Blank" title="Blank" id="icon-blank" />
                                    """ %  aERES[ 'portal_url']
                                        )


                if aERES[ 'write_permission']:
                    aSubRdCtxt.pOS( u"""
                                    <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Edit_Link"
                                    href="%(ERES-url)sEditar/%(theExtraLinkHrefParams)s" 
                                    title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                    <img 
                                    alt="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                    title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                    id="icon-edit" src="%(portal_url)s/edit.gif"  />
                                    </a>
                                    &nbsp;    

                                    """ %{
                                            'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                            'Row-Index':                           unIndexElemento,
                                            'unIdTabla':                           fCGIE( unIdTabla),
                                            'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                                            'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                            'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                            'ERES-url':                            aERES[ 'url'],
                                            'portal_url':                          aERES[ 'portal_url'],
                                        })

                else:
                    aSubRdCtxt.pOS( u"""
                                    <img src="%s/blank_icon.gif"  alt="Blank" title="Blank" id="icon-blank" />
                                    """ %  aERES[ 'portal_url']
                                        )



                if unNumElements > 1 and aSRES[ 'write_permission']:

                    if  unIndexElemento:
                        aSubRdCtxt.pOS( u"""
                                        <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Subir_Link"
                                        href="%(SRES-url)sTabular/?theMovedElementID=%(ERES-id)s&theMoveDirection=Up&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(ERES-id)s" 
                                        title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                        <img 
                                        alt="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                        title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                        id="icon-edit" src="%(portal_url)s/arrowUp.gif"  />
                                        </a>
                                        &nbsp;    

                                        """ %{
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                                'Row-Index':                           unIndexElemento,
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_subir_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
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



                    if  unIndexElemento < ( unNumElements -1):
                        aSubRdCtxt.pOS( u"""
                                        <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Bajar_Link"
                                        href="%(SRES-url)sTabular/?theMovedElementID=%(ERES-id)s&theMoveDirection=Down&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(ERES-id)s" 
                                        title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                        <img 
                                        alt="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                        title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                        id="icon-edit" src="%(portal_url)s/arrowDown.gif"  />
                                        </a>
                                        &nbsp;    

                                        """ %{
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                                'Row-Index':                           unIndexElemento,
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_bajar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
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

                unTitle = u'%s %s %s %s %s (%s)' % ( 
                    theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'), 
                    fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']),
                    fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']), 
                    ( not ( unColumnName == 'title')       and  fCGIE( aERES[ 'values_by_name'].get( 'title', {}).get( 'uvalue', ''))) or '', 
                    ( not ( unColumnName == 'description') and  fCGIE( aERES[ 'values_by_name'].get( 'description', {}).get( 'uvalue', ''))) or '',
                    fCGIE( aERES[ 'type_translations'][ 'translated_type_description']),
                )


                aSubRdCtxt.pOS( u"""
                                <a  class="state-visible" 
                                name="hidMDDElemento_%(ERES-UID)s_title"
                                id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Link"
                                href="%(ERES-url)sTabular/%(theExtraLinkHrefParams)s" 
                                title="%(unTitle)s" >
                                <h4>
                                <img src="%(portal_url)s/%(content_icon)s" 
                                alt="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" />
                                <span  class="state-visible">%(column_value)s</span>
                                </h4>
                                </a>
                                &nbsp;    

                                """ %{
                                        'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                        'Row-Index':                           unIndexElemento,
                                        'unTitle':                             fCGIE( unTitle),
                                        'millis':                              fMillisecondsNow(), 
                                        'unIdTabla':                           fCGIE( unIdTabla),
                                        'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                        'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                        'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                        'ERES-id':                             fCGIE( aERES[ 'id']),
                                        'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                        'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                        'SRES-url':                            aSRES[ 'url'],
                                        'ERES-url':                            aERES[ 'url'],
                                        'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                        'portal_url':                          aERES[ 'portal_url'],
                                        'column_value':                        fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']),

                                    })

            else:

                unAttributeResult =  aERES[ 'values_by_name'].get( unColumnName, {})

                if unAttributeResult:

                    if unAttributeResult[ 'type'].lower() in [ 'selection', 'boolean', ]:
                        aSubRdCtxt.pOS( u"""
                                        <span>%s</span>
                                        </tal:block>
                                        """ % fCGIE( unAttributeResult.get( 'translated_value', ''))
                                            )
                    else:
                        if unAttributeResult[ 'uvalue'] and not ( unAttributeResult[ 'uvalue'] =='None'):
                            aSubRdCtxt.pOS( u"""
                                            <span>%s</span>
                                            """ % fCGIE( unAttributeResult.get( 'uvalue', '') ))

            aSubRdCtxt.pOS( u"""
                            </td>
                            """ )



        aSubRdCtxt.pOS( u"""
                        </tr>
                        """ )


    theRdCtxt.pOS( u"""
                   </tbody>
                   """ )


    unPermiteCrearElementos = aSRES[ 'add_permission'] and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                            aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and ( not aTRAVRES[ 'max_multiplicity_reached']) and \
                            not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))

    someFactories = aTRAVRES[ 'factories']
    aNumFactories = len( someFactories)

    if unPermiteCrearElementos and aNumFactories:

        theRdCtxt.pOS( u"""
                       </tbody>
                       <tfoot>
                       """ )

        if aNumFactories == 1:

            unaFactoriaElemento = someFactories[ 0]

            unaVistaCreacion = ( aTRAVRES.get( 'factory_views', None) or {}).get( unaFactoriaElemento[ 'meta_type'], 'Crear')


            theRdCtxt.pOS( u"""
                           <tr class="%(Row-Class)s" >
                           <td colspan="%(theColspan)s" align="center" valign="baseline">
                           <a  id="hidMDDAggregation_%(traversal_name)s_Create_Link"
                           href="%(SRES-url)s%(unaVistaCreacion)s/?theNewTypeName=%(FACTORY-meta_type)s&theAggregationName=%(traversal_name)s"
                           title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                           <img id="hidMDDAggregation_%(traversal_name)s_Create_Icon"
                           src="%(portal_url)s/add_icon.gif" 
                           alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                           title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                           </a>
                           </td>
                           """ % {
                                   'Row-Class':                           cClasesFilas[ unNumElements % 2],    
                                   'theColspan':                          ( unPermiteModificarAlgunElemento and 2) or 1,
                                   'unaVistaCreacion':                    unaVistaCreacion,
                                   'FACTORY-meta_type':                   unaFactoriaElemento[ 'meta_type'],
                                   'ModelDDvlPlone_crear_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                   'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                   'SRES-url':                            aSRES[ 'url'],
                                   'portal_url':                          aSRES[ 'portal_url'],
                                   'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                                   'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                                   'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                                   'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
                               })

            theRdCtxt.pOS( u"""
                           <td colspan="%(theColspan)s" align="left" valign="baseline">
                           <a  id="hidMDDAggregation_%(traversal_name)s_Create_Link"
                           href="%(SRES-url)s%(unaVistaCreacion)s/?theNewTypeName=%(FACTORY-meta_type)s&theAggregationName=%(traversal_name)s"
                           title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                           <img id="hidMDDAggregation_%(traversal_name)s_Create_Icon"
                           src="%(portal_url)s/%(FACTORY-icon)s" 
                           alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                           title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                           <span>%(FACTORY-translated_archetype_name)s</span>
                           </a>
                           </td>
                           </tr>
                           """ % {
                                   'theColspan':                          len( unosColumnNames),
                                   'unaVistaCreacion':                    fCGIE( unaVistaCreacion),
                                   'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                                   'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                                   'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                                   'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
                                   'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                   'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                   'SRES-url':                            aSRES[ 'url'],
                                   'portal_url':                          aSRES[ 'portal_url'],

                               })

        else:
            theRdCtxt.pOS( u"""
                           <tr class="%(Row-Class)s" >
                           <td colspan="%(theColspan)s" align="left" valign="baseline">
                           """ % {
                                   'Row-Class':                           cClasesFilas[ unNumElements % 2],    
                                   'theColspan':                          (( unPermiteModificarAlgunElemento and 2) or 1) + len( unosColumnNames),
                                   'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                               })

            if cPref_Pres_DisplayActionLabels_Force or aPREFS_PRES.get( cPref_Pres_DisplayActionLabels_Name, False):
                theRdCtxt.pOS( u"""
                               <span>%(ModelDDvlPlone_crear_action_label)s</span>
                               &emsp;
                               """ % {
                                       'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                   })

            for unaFactoriaElemento in someFactories:
                unaVistaCreacion = ( aTRAVRES.get( 'factory_views', None) or {}).get( unaFactoriaElemento[ 'meta_type'], 'Crear')
                theRdCtxt.pOS( u"""
                               &emsp;
                               <a  id="hidMDDAggregation_%(traversal_name)s_Create_Link_%(FACTORY-meta_type)s"
                               href="%(SRES-url)s%(unaVistaCreacion)s/?theNewTypeName=%(FACTORY-meta_type)s&theAggregationName=%(traversal_name)s"
                               title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                               <img id="hidMDDAggregation_%(traversal_name)s_Create_Icon"
                               src="%(portal_url)s/%(FACTORY-icon)s" 
                               alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                               title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                               <span>%(FACTORY-translated_archetype_name)s</span>
                               </a>
                               """ % {
                                       'unaVistaCreacion':                    fCGIE( unaVistaCreacion),
                                       'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                                       'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                                       'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                                       'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
                                       'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                       'SRES-url':                            aSRES[ 'url'],
                                       'portal_url':                          aSRES[ 'portal_url'],
                                       'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                   })      

            theRdCtxt.pOS( u"""
                           </td>
                           </tr>
                           """ ) 


            theRdCtxt.pOS( u"""
                           </td>
                           """)


        theRdCtxt.pOS( u"""
                       </tfoot>
                       """ )









    theRdCtxt.pOS( u"""
                   </tr>
                   </tfoot>
                   </table>
                   """ )







    theRdCtxt.pOS( u"""
                   <form method="POST" id="%(unIdTabla)s_Form">

                   <input type="hidden" value="%(SRES-UID)s"
                   name="theContainerUID" id="%(unIdTabla)s_ContainerUID"/> 

                   <input type="hidden" value=""
                   name="theGroupAction"  id="%(unIdTabla)s_GroupAction" />
                   """ % {
                           'unIdTabla':                           fCGIE( unIdTabla),
                           'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                       })


    for unIndexElemento in range( unNumElements):

        aERES = someElements[ unIndexElemento]
        aSubRdCtxt = theRdCtxt.fNewCtxt( {
            'ERES' : aERES,
        })

        aSubRdCtxt.pOS( u"""
                        <input type="hidden" disabled value="%(ERES-UID)s"
                        name="theUIDs" id="%(unIdTabla)s_Select_%(unIndexElemento)d_UID" /> 
                        """ % {
                                'unIdTabla':                           fCGIE( unIdTabla),
                                'unIndexElemento':                     unIndexElemento,
                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                            })



    theRdCtxt.pOS( u"""
                   </form>
                   """)






    return [ True, True,]












def _MDDRender_Tabular_Tabla_Plone( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    #aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    #if not aPARENT_SRES:
        #return [ False, True,]


    aSRESIndex = theRdCtxt.fGP( 'index', 0)

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]

    aPARENT_TRAVRES = theRdCtxt.fGP( 'PARENT_TRAVRES', {})

    aTableTraversalName = ''
    if aPARENT_TRAVRES:
        aTableTraversalName = aPARENT_TRAVRES[ 'traversal_name']
    else:        
        aTableTraversalName = aTRAVRES[ 'traversal_name']

    if not aTableTraversalName:
        return [ False, True,]

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        # return [ False, True,]

    someElements  = aTRAVRES.get( 'elements', [])
    unNumElements = len( someElements)
    unSiempre    = theRdCtxt.fGP( 'theSiempre', True)


    if someElements or unSiempre:

        theRdCtxt.pOS( u"""
                       <h2 id="hidMDDTraversal_%(traversal_name)s_label" >
                       %(traversal_label)s
                       <font size=1">            
                       &emsp;
                       &emsp;
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr>
                       <td id="cid_MDDTOC_Holder_Traversal_%(traversal_name)s" valign="top" align="left">
                       <a title="%(ModelDDvlPlone_Tabular_Sections)s"
                       onclick="document.getElementById( 'cid_MDDTOC_Holder_Traversal_%(traversal_name)s').appendChild( document.getElementById( 'cid_MDDSectionList_ActionsMenu')); if ( hasClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated' )) { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated', 'activated');} else { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'activated', 'deactivated')} return true;">
                       <img src="%(portal_url)s/menusecciones.gif" title="%(ModelDDvlPlone_Tabular_Sections)s" alt="%(ModelDDvlPlone_Tabular_Sections)s" id="icon-sectionsmenu" />
                       """ % {
                               'portal_url':                       aSRES[ 'portal_url'],
                               'ModelDDvlPlone_Tabular_Sections':  theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                               'traversal_name':                   fCGIE( aTRAVRES[ 'traversal_name']),        
                               'traversal_label':                  fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                               'traversal_description':            fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
                           })





    if aPREFS_PRES.get( 'DisplayActionLabels', False):
        theRdCtxt.pOS( u"""
                       <span>%(ModelDDvlPlone_Tabular_Sections)s</span>
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                           })





    if someElements or unSiempre:

        theRdCtxt.pOS( u"""
                       </a>
                       </td>
                       </tr></tbody></table>
                       </font>
                       </h2>
                       <table id="hidMDDTraversal_%(traversal_name)s_table" width="100%%" cellspacing="0" cellpadding="0" frame="void">
                       <tr>
                       <td id="hidMDDTraversal_%(traversal_name)s_description" align="left" valign="baseline" class="formHelp">%(traversal_description)s</td>
                       <td align="right" valign="baseline"> 
                       </td>
                       </tr>
                       </table>
                       """ % {
                               'portal_url':                       aSRES[ 'portal_url'],
                               'ModelDDvlPlone_Tabular_Sections':  theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                               'traversal_name':                   fCGIE( aTRAVRES[ 'traversal_name']),        
                               'traversal_label':                  fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                               'traversal_description':            fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),        
                           })




    unIdTabla = 'hidMDDTraversal_%(traversal_name)s_Elem_%(SRES-id)s_Table' % {
        'traversal_name':                     aTableTraversalName,
        'SRES-id':                            aSRES[ 'id'],
    }
    theRdCtxt.pSP( 'unIdTabla', unIdTabla)

    theRdCtxt.pOS( u"""
                   <table width="100%%" class="listing"  id="%(unIdTabla)s"
                   summary="%(SRES-title)s">
                   <tbody>
                   <tr>
                   """ % {
                           'unIdTabla':                           fCGIE( unIdTabla),
                           'SRES-title':                          fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                       })



    unPermiteModificarAlgunElemento = False
    for aERES in someElements:
        if aERES[ 'read_permission'] and ( aERES[ 'write_permission'] or aERES[ 'delete_permission']):
            unPermiteModificarAlgunElemento = True
            break



    unPermiteEliminarAlgunElemento = False
    unPermiteEliminarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                               aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                               not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))

    if unPermiteEliminarElementos:
        for aERES in someElements:
            if aERES[ 'read_permission'] and ( aERES[ 'write_permission'] or aERES[ 'delete_permission']):
                unPermiteEliminarAlgunElemento = True
                break


    theRdCtxt.pOS( u"""
                   <col width="24" />
                   """)

    if unPermiteModificarAlgunElemento:
        theRdCtxt.pOS( u"""
                       <col width="%d" />
                       """ % ( unPermiteEliminarAlgunElemento and 120) or 100 )



    unosColumnNames = aTRAVRES.get( 'column_names', [])

    unNumColumnNames =len( unosColumnNames)

    theRdCtxt.pOS( u"""
                   <col/>
                   """ * unNumColumnNames)


    theRdCtxt.pOS( u"""
                   <thead>
                   <tr>
                   """)



    theRdCtxt.pOS( u"""
                   <th class="nosort" align="left" >
                   <input type="checkbox"  class="noborder"  value=""
                   name="%(unIdTabla)s_SelectAll" id="%(unIdTabla)s_SelectAll" 
                   onchange="pMDDToggleAllSelections('%(unIdTabla)s'); return true;"/>
                   """ %{
                           'unIdTabla':                           fCGIE( unIdTabla),
                       })


    if not unPermiteModificarAlgunElemento:

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Traversals_Aggregations_GroupActionsMenu')( theRdCtxt)

        theRdCtxt.pOS( u"""
                       </th>
                       """)
    else:
        theRdCtxt.pOS( u"""
                       </th>
                       <th class="nosort" align="left" > 
                       """)

        anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Traversals_Aggregations_GroupActionsMenu')( theRdCtxt)

        theRdCtxt.pOS( u"""
                       </th>
                       """)





    for unColumnName in unosColumnNames:
        theRdCtxt.pOS( u"""
                       <th class="nosort" align="left">%s</th>
                       """ % fCGIE( aTRAVRES[ 'column_translations'].get( unColumnName, {}).get( 'translated_label', unColumnName))
                           )

    theRdCtxt.pOS( u"""
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
                                'unIdTabla': fCGIE( unIdTabla),
                                'Row-Class': cClasesFilas[ unIndexElemento % 2],
                                'Row-Index': unIndexElemento,
                            })


        aSubRdCtxt.pOS( u"""
                        <td align="center" valign="baseline">
                        <input type="checkbox"  class="noborder"  value=""
                        name="%(unIdTabla)s_Select_%(Row-Index)d"
                        id="%(unIdTabla)s_Select_%(Row-Index)d"  />
                        </td>
                        """ % {
                                'Row-Index': unIndexElemento,
                                'unIdTabla': fCGIE( unIdTabla),
                            })



        if unPermiteModificarAlgunElemento:

            aSubRdCtxt.pOS( u"""
                            <td align="center" valign="baseline" id="%(unIdTabla)s_%(ERES-UID)s_ChangesLinks_Cell">
                            """ % {
                                    'unIdTabla':                fCGIE( unIdTabla),
                                    'ERES-UID':                 fCGIE( aERES[ 'UID']),
                                })

            if aERES[ 'write_permission']:

                if aERES[ 'delete_permission']:
                    aSubRdCtxt.pOS( u"""
                                    <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Delete_Link"
                                    href="%(SRES-url)sEliminarPlone?theUIDToDelete=%(ERES-UID)s%(theExtraLinkHrefParams)s" 
                                    title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                    <img 
                                    alt="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                    title="%(ModelDDvlPlone_eliminar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                    id="icon-delete" src="%(portal_url)s/delete_icon.gif"  />
                                    </a>
                                    &nbsp;    

                                    """ %{
                                            'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                            'Row-Index':                           unIndexElemento,
                                            'unIdTabla':                           fCGIE( unIdTabla),
                                            'ModelDDvlPlone_eliminar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_eliminar_action_label'),
                                            'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                            'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                            'SRES-url':                            aSRES[ 'url'],
                                            'ERES-UID':                            aERES[ 'UID'],
                                            'portal_url':                          aERES[ 'portal_url'],
                                        })

                else:
                    aSubRdCtxt.pOS( u"""
                                    <img src="%s/blank_icon.gif"  alt="Blank" title="Blank" id="icon-blank" />
                                    """ %  aERES[ 'portal_url']
                                        )


                if aERES[ 'write_permission']:
                    aSubRdCtxt.pOS( u"""
                                    <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Edit_Link"
                                    href="%(ERES-url)sbase_edit/%(theExtraLinkHrefParams)s" 
                                    title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                    <img 
                                    alt="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                    title="%(ModelDDvlPlone_editar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                    id="icon-edit" src="%(portal_url)s/edit.gif"  />
                                    </a>
                                    &nbsp;    

                                    """ %{
                                            'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                            'Row-Index':                           unIndexElemento,
                                            'unIdTabla':                           fCGIE( unIdTabla),
                                            'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                                            'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                            'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                            'ERES-url':                            aERES[ 'url'],
                                            'portal_url':                          aERES[ 'portal_url'],
                                        })

                else:
                    aSubRdCtxt.pOS( u"""
                                    <img src="%s/blank_icon.gif"  alt="Blank" title="Blank" id="icon-blank" />
                                    """ %  aERES[ 'portal_url']
                                        )



                if unNumElements > 1 and aSRES[ 'write_permission']:

                    if  unIndexElemento:
                        aSubRdCtxt.pOS( u"""
                                        <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Subir_Link"
                                        href="%(SRES-url)sTabular/?theMovedObjectUID=%(ERES-UID)s&theMoveDirection=Up&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(ERES-UID)s" 
                                        title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                        <img 
                                        alt="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                        title="%(ModelDDvlPlone_subir_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                        id="icon-edit" src="%(portal_url)s/arrowUp.gif"  />
                                        </a>
                                        &nbsp;    

                                        """ %{
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                                'Row-Index':                           unIndexElemento,
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_subir_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
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



                    if  unIndexElemento < ( unNumElements -1):
                        aSubRdCtxt.pOS( u"""
                                        <a  id="%(unIdTabla)s_RowIndex_%(Row-Index)d_Bajar_Link"
                                        href="%(SRES-url)sTabular/?theMovedObjectUID=%(ERES-UID)s&theMoveDirection=Down&theTraversalName=%(traversal_name)s&dd=%(millis)d%(theExtraLinkHrefParams)s#hidMDDElemento_%(ERES-UID)s" 
                                        title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s" >
                                        <img 
                                        alt="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                        title="%(ModelDDvlPlone_bajar_action_label)s %(translated_archetype_name)s %(ERES-title)s"  
                                        id="icon-edit" src="%(portal_url)s/arrowDown.gif"  />
                                        </a>
                                        &nbsp;    

                                        """ %{
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                                'Row-Index':                           unIndexElemento,
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_bajar_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
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

                unTitle = u'%s %s %s %s %s (%s)' % ( 
                    theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'), 
                    fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']),
                    fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']), 
                    ( not ( unColumnName == 'title')       and  fCGIE( aERES[ 'values_by_name'].get( 'title', {}).get( 'uvalue', ''))) or '', 
                    ( not ( unColumnName == 'description') and  fCGIE( aERES[ 'values_by_name'].get( 'description', {}).get( 'uvalue', ''))) or '',
                    fCGIE( aERES[ 'type_translations'][ 'translated_type_description']),
                )


                aSubRdCtxt.pOS( u"""
                                <a  class="state-visible" 
                                name="hidMDDElemento_%(ERES-UID)s"
                                id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Link"
                                href="%(ERES-url)sview/%(theExtraLinkHrefParams)s" 
                                title="%(unTitle)s" >
                                <h4>
                                <img src="%(portal_url)s/%(content_icon)s" 
                                alt="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" />
                                <span  class="state-visible">%(column_value)s</span>
                                </h4>
                                </a>
                                &nbsp;    

                                """ %{
                                        'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                        'Row-Index':                           unIndexElemento,
                                        'unTitle':                             fCGIE( unTitle),
                                        'millis':                              fMillisecondsNow(), 
                                        'unIdTabla':                           fCGIE( unIdTabla),
                                        'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                        'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                        'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                        'ERES-id':                             fCGIE( aERES[ 'id']),
                                        'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                        'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                        'SRES-url':                            aSRES[ 'url'],
                                        'ERES-url':                            aERES[ 'url'],
                                        'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                        'portal_url':                          aERES[ 'portal_url'],
                                        'column_value':                        fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']),

                                    })

            elif unColumnName == cPloneElement_ColumnName_Details:

                aERES_MetaType = aERES[ 'meta_type']

                if aERES_MetaType == 'ATImage':
                    aContentURL = aERES[ 'values_by_name'][ 'content_url'][ 'value']
                    if aContentURL:
                        aSubRdCtxt.pOS( u"""
                                        <a  class="state-visible" 
                                        name="hidMDDElemento_%(ERES-UID)s_Details"
                                        id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Details_Link"
                                        href="%(ERES-url)sview/%(theExtraLinkHrefParams)s" 
                                        title="%(unTitle)s" >
                                        <img src="%(content_url)s" height="%(cPloneImage_DetailsHeight)d"
                                        alt="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                        title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" />
                                        </a>
                                        &nbsp;    

                                        """ %{
                                                'cPloneImage_DetailsHeight':           cPloneImage_DetailsHeight,
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                                'Row-Index':                           unIndexElemento,
                                                'unTitle':                             fCGIE( unTitle),
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                                'SRES-url':                            aSRES[ 'url'],
                                                'ERES-url':                            aERES[ 'url'],
                                                'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                                'portal_url':                          aERES[ 'portal_url'],
                                                'content_url':                         fCGIE( aContentURL)
                                            })

                elif aERES_MetaType == 'ATLink':
                    aContentURL  = aERES[ 'values_by_name'][ 'content_url'][ 'value']
                    if aContentURL:
                        aSubRdCtxt.pOS( u"""
                                        <a  class="state-visible" 
                                        name="hidMDDElemento_%(ERES-UID)s_Details"
                                        id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Details_Link"
                                        href="%(ERES-url)sview/%(theExtraLinkHrefParams)s" 
                                        title="%(unTitle)s" >
                                        %(content_url)s
                                        </a>
                                        &nbsp;    

                                        """ %{
                                                'cPloneImage_DetailsHeight':           cPloneImage_DetailsHeight,
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                                'Row-Index':                           unIndexElemento,
                                                'unTitle':                             fCGIE( unTitle),
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                                'SRES-url':                            aSRES[ 'url'],
                                                'ERES-url':                            aERES[ 'url'],
                                                'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                                'portal_url':                          aERES[ 'portal_url'],
                                                'content_url':                         fCGIE( aContentURL)
                                            })

                elif aERES_MetaType == 'ATDocument':
                    aContentText = aERES[ 'values_by_name'][ 'text'][ 'uvalue'][:cPloneDocument_DetailsLen]
                    if aContentText:
                        aSubRdCtxt.pOS( u"""
                                        <a  class="state-visible" 
                                        name="hidMDDElemento_%(ERES-UID)s_Details"
                                        id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Details_Link"
                                        href="%(ERES-url)sview/%(theExtraLinkHrefParams)s" 
                                        title="%(unTitle)s" >
                                        %(content_text)s
                                        </a>
                                        &nbsp;    

                                        """ %{
                                                'cPloneImage_DetailsHeight':           cPloneImage_DetailsHeight,
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                                'Row-Index':                           unIndexElemento,
                                                'unTitle':                             fCGIE( unTitle),
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                                'SRES-url':                            aSRES[ 'url'],
                                                'ERES-url':                            aERES[ 'url'],
                                                'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                                'portal_url':                          aERES[ 'portal_url'],
                                                'content_text':                        fCGIE( aContentText)
                                            })


                elif aERES_MetaType == 'ATNewsItem':
                    aContentURL  = aERES[ 'values_by_name'][ 'content_url'][ 'value']
                    aContentText = aERES[ 'values_by_name'][ 'text'][ 'uvalue'][:cPloneDocument_DetailsLen]
                    if aContentURL or aContentText:
                        aSubRdCtxt.pOS( u"""
                                        <a  class="state-visible" 
                                        name="hidMDDElemento_%(ERES-UID)s_Details"
                                        id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Details_Link"
                                        href="%(ERES-url)sview/%(theExtraLinkHrefParams)s" 
                                        title="%(unTitle)s" >
                                        """ %{
                                                'cPloneImage_DetailsHeight':           cPloneImage_DetailsHeight,
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                                'Row-Index':                           unIndexElemento,
                                                'unTitle':                             fCGIE( unTitle),
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                                'SRES-url':                            aSRES[ 'url'],
                                                'ERES-url':                            aERES[ 'url'],
                                                'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                                'portal_url':                          aERES[ 'portal_url'],
                                            })
                        if aContentText:
                            aSubRdCtxt.pOS( u"""
                                            <span>%(content_text)s</span>
                                            """ %{
                                                    'content_text':                        fCGIE( aContentText),
                                                })
                        if aContentURL and aContentText:
                            aSubRdCtxt.pOS( u"""
                                            <br/>
                                            """
                                            )
                        if aContentURL:
                            aSubRdCtxt.pOS( u"""
                                            <img src="%(content_url)s" height="%(cPloneImage_DetailsHeight)d"
                                            alt="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                            title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" />
                                            """ %{
                                                    'cPloneImage_DetailsHeight':           cPloneImage_DetailsHeight,
                                                    'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                                    'Row-Index':                           unIndexElemento,
                                                    'unTitle':                             fCGIE( unTitle),
                                                    'millis':                              fMillisecondsNow(), 
                                                    'unIdTabla':                           fCGIE( unIdTabla),
                                                    'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                                    'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                    'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                    'ERES-id':                             fCGIE( aERES[ 'id']),
                                                    'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                    'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                                    'SRES-url':                            aSRES[ 'url'],
                                                    'ERES-url':                            aERES[ 'url'],
                                                    'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                                    'portal_url':                          aERES[ 'portal_url'],
                                                    'content_url':                         fCGIE( aContentURL)
                                                })
                    aSubRdCtxt.pOS( u"""
                                    </a>
                                    &nbsp;    
                                    """)


                elif aERES_MetaType == 'ATFile':
                    aContentURL  = aERES[ 'values_by_name'][ 'content_url'][ 'value']
                    if aContentURL:
                        aSubRdCtxt.pOS( u"""
                                        <a  class="state-visible" 
                                        name="hidMDDElemento_%(ERES-UID)s_Details"
                                        id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Details_Link"
                                        href="%(ERES-url)sview/%(theExtraLinkHrefParams)s" 
                                        title="%(unTitle)s" >
                                        %(content_url)s
                                        </a>
                                        &nbsp;    

                                        """ %{
                                                'cPloneImage_DetailsHeight':           cPloneImage_DetailsHeight,
                                                'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                                'Row-Index':                           unIndexElemento,
                                                'unTitle':                             fCGIE( unTitle),
                                                'millis':                              fMillisecondsNow(), 
                                                'unIdTabla':                           fCGIE( unIdTabla),
                                                'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                                'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                                'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                'ERES-id':                             fCGIE( aERES[ 'id']),
                                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                                'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                                'SRES-url':                            aSRES[ 'url'],
                                                'ERES-url':                            aERES[ 'url'],
                                                'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                                'portal_url':                          aERES[ 'portal_url'],
                                                'content_url':                         fCGIE( aERES[ 'values_by_name'][ 'content_url'][ 'value'])
                                            })

            else:

                unAttributeResult =  aERES[ 'values_by_name'].get( unColumnName, {})

                if unAttributeResult:

                    if unAttributeResult[ 'type'] in [ 'selection', 'boolean']:
                        aSubRdCtxt.pOS( u"""
                                        <span>%s</span>
                                        </tal:block>
                                        """ % fCGIE( unAttributeResult.get( 'translated_value', ''))
                                            )
                    else:
                        if unAttributeResult[ 'uvalue'] and not ( unAttributeResult[ 'uvalue'] =='None'):
                            aSubRdCtxt.pOS( u"""
                                            <span>%s</span>
                                            """ % fCGIE( unAttributeResult.get( 'uvalue', '') ))



            aSubRdCtxt.pOS( u"""
                            </td>
                            """ )



        aSubRdCtxt.pOS( u"""
                        </tr>
                        """ )


    theRdCtxt.pOS( u"""
                   </tbody>
                   """ )


    unPermiteCrearElementos = aSRES[ 'add_permission'] and aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                            aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and ( not aTRAVRES[ 'max_multiplicity_reached']) and \
                            not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))

    someFactories = aTRAVRES[ 'factories']
    aNumFactories = len( someFactories)

    if unPermiteCrearElementos and aNumFactories:

        theRdCtxt.pOS( u"""
                       </tbody>
                       <tfoot>
                       """ )

        if aNumFactories == 1:

            unaFactoriaElemento = someFactories[ 0]

            theRdCtxt.pOS( u"""
                           <tr class="%(Row-Class)s" >
                           <td colspan="%(theColspan)s" align="center" valign="baseline">
                           <a  id="hidMDDAggregationPlone_%(traversal_name)s_Create_Link"
                           href="%(SRES-url)sMDDCreatePloneElement/?type_name=%(FACTORY-archetype_name)s"
                           title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                           <img id="hidMDDAggregationPlone_%(traversal_name)s_Create_Icon"
                           src="%(portal_url)s/add_icon.gif" 
                           alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                           title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                           </a>
                           </td>
                           """ % {
                                   'Row-Class':                           cClasesFilas[ unNumElements % 2],    
                                   'theColspan':                          ( unPermiteModificarAlgunElemento and 2) or 1,
                                   'FACTORY-meta_type':                   unaFactoriaElemento[ 'meta_type'],
                                   'ModelDDvlPlone_crear_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                   'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                   'SRES-url':                            aSRES[ 'url'],
                                   'portal_url':                          aSRES[ 'portal_url'],
                                   'FACTORY-archetype_name':              fCGIE( unaFactoriaElemento[ 'archetype_name']),
                                   'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                                   'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                                   'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                                   'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
                               })

            theRdCtxt.pOS( u"""
                           <td colspan="%(theColspan)s" align="left" valign="baseline">
                           <a  id="hidMDDAggregationPlone_%(traversal_name)s_Create_Link"
                           href="%(SRES-url)sMDDCreatePloneElement/?type_name=%(FACTORY-archetype_name)s"
                           title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                           <img id="hidMDDAggregationPlone_%(traversal_name)s_Create_Icon"
                           src="%(portal_url)s/%(FACTORY-icon)s" 
                           alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                           title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                           <span>%(FACTORY-translated_archetype_name)s</span>
                           </a>
                           </td>
                           </tr>
                           """ % {
                                   'theColspan':                          len( unosColumnNames),
                                   'FACTORY-archetype_name':              fCGIE( unaFactoriaElemento[ 'archetype_name']),
                                   'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                                   'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                                   'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                                   'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
                                   'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                   'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                   'SRES-url':                            aSRES[ 'url'],
                                   'portal_url':                          aSRES[ 'portal_url'],

                               })

        else:
            theRdCtxt.pOS( u"""
                           <tr class="%(Row-Class)s" >
                           <td colspan="%(theColspan)s" align="left" valign="baseline">
                           """ % {
                                   'Row-Class':                           cClasesFilas[ unNumElements % 2],    
                                   'theColspan':                          (( unPermiteModificarAlgunElemento and 2) or 1) + len( unosColumnNames),
                                   'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                               })

            if cPref_Pres_DisplayActionLabels_Force or aPREFS_PRES.get( cPref_Pres_DisplayActionLabels_Name, False):
                theRdCtxt.pOS( u"""
                               <span>%(ModelDDvlPlone_crear_action_label)s</span>
                               &emsp;
                               """ % {
                                       'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                   })

            for unaFactoriaElemento in someFactories:
                theRdCtxt.pOS( u"""
                               &emsp;
                               <a  id="hidMDDAggregationPlone_%(traversal_name)s_Create_Link_%(FACTORY-meta_type)s"
                               href="%(SRES-url)sMDDCreatePloneElement/?type_name=%(FACTORY-archetype_name)s"
                               title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s" >
                               <img id="hidMDDAggregationPlone_%(traversal_name)s_Create_Icon"
                               src="%(portal_url)s/%(FACTORY-icon)s" 
                               alt="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"
                               title="%(ModelDDvlPlone_crear_action_label)s %(FACTORY-translated_archetype_name)s: %(FACTORY-translated_type_description)s"/>
                               <span>%(FACTORY-translated_archetype_name)s</span>
                               </a>
                               """ % {
                                       'FACTORY-archetype_name':              fCGIE( unaFactoriaElemento[ 'archetype_name']),
                                       'FACTORY-meta_type':                   fCGIE( unaFactoriaElemento[ 'meta_type']),
                                       'FACTORY-icon':                        fCGIE( unaFactoriaElemento[ 'content_icon']),
                                       'FACTORY-translated_archetype_name':   fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_archetype_name']),
                                       'FACTORY-translated_type_description': fCGIE( unaFactoriaElemento[ 'type_translations'][ 'translated_type_description']),
                                       'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                       'SRES-url':                            aSRES[ 'url'],
                                       'portal_url':                          aSRES[ 'portal_url'],
                                       'ModelDDvlPlone_crear_action_label':   theRdCtxt.fUITr( 'ModelDDvlPlone_crear_action_label'),
                                   })      

            theRdCtxt.pOS( u"""
                           </td>
                           </tr>
                           """ ) 


            theRdCtxt.pOS( u"""
                           </td>
                           """)


        theRdCtxt.pOS( u"""
                       </tfoot>
                       """ )









    theRdCtxt.pOS( u"""
                   </tr>
                   </tfoot>
                   </table>
                   """ )







    theRdCtxt.pOS( u"""
                   <form method="POST" id="%(unIdTabla)s_Form">

                   <input type="hidden" value="%(SRES-UID)s"
                   name="theContainerUID" id="%(unIdTabla)s_ContainerUID"/> 

                   <input type="hidden" value=""
                   name="theGroupAction"  id="%(unIdTabla)s_GroupAction" />
                   """ % {
                           'unIdTabla':                           fCGIE( unIdTabla),
                           'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                       })


    for unIndexElemento in range( unNumElements):

        aERES = someElements[ unIndexElemento]
        aSubRdCtxt = theRdCtxt.fNewCtxt( {
            'ERES' : aERES,
        })

        aSubRdCtxt.pOS( u"""
                        <input type="hidden" disabled value="%(ERES-UID)s"
                        name="theUIDs" id="%(unIdTabla)s_Select_%(unIndexElemento)d_UID" /> 
                        """ % {
                                'unIdTabla':                           fCGIE( unIdTabla),
                                'unIndexElemento':                     unIndexElemento,
                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                            })



    theRdCtxt.pOS( u"""
                   </form>
                   """)






    return [ True, True,]










def _MDDRender_Tabular_Traversals_Aggregations_GroupActionsMenu( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    #aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    #if not aPARENT_SRES:
        # return [ False, True,]

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]

    someElements  = aTRAVRES.get( 'elements', [])


    unPermitePegarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                            aSRES[ 'add_permission'] and  ( ( not aTRAVRES[ 'contains_collections']) or aSRES[ 'add_collection_permission']) and \
                            aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                            ( not aTRAVRES[ 'max_multiplicity_reached']) and \
                            not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))  

    unPermiteOrdenarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                              aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                              not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))  



    unPermiteEliminarAlgunElemento = False
    unPermiteEliminarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                               aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                               not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))

    if unPermiteEliminarElementos:
        for anElement in someElements:
            if anElement[ 'read_permission'] and ( anElement[ 'write_permission'] or anElement[ 'delete_permission']):
                unPermiteEliminarAlgunElemento = True
                break



    if not  theRdCtxt.fGP( cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName, False):

        theRdCtxt.pOS( cMDDRenderTabular_MenuAccionesGrupo_JavaScript)

        theRdCtxt.pSPGlobal( cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName, True)


    theRdCtxt.pOS("""
    <dl class="actionMenu deactivated" id="%(unIdTabla)s_ActionsMenu" >
        <dt class="actionMenuHeader" style="display: inline">
            <a>%(plone-heading_actions)s</a>
        </dt>
        <dd class="actionMenuContent">
            <ul>
    """ % {
            'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-heading_actions': theRdCtxt.fUITr( 'heading_actions'),
        })




    if unPermiteEliminarAlgunElemento:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Cut)s" id="%(unIdTabla)s_MenuAction_Cut_Link"
                onclick="pMDDSubmit_varios( 'Cut', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/cut_icon.gif"  alt="%(plone-Cut)s" title="%(plone-Cut)s"  />
                <span>%(plone-Cut)s</span>        
            </a>
        </li>
        """ % {
                'unIdTabla':             theRdCtxt.fGP(   'unIdTabla', ''),
                'plone-Cut':             theRdCtxt.fUITr( 'Cut'),
                'portal_url':            aSRES[ 'portal_url'],
            })

    if someElements:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Copy)s" id="%(unIdTabla)s_MenuAction_Copy_Link"
                onclick="pMDDSubmit_varios( 'Copy', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/copy_icon.gif"  alt="%(plone-Copy)s" title="%(plone-Copy)s"  />
                <span>%(plone-Copy)s</span>        
            </a>
        </li>
        """ % {
                'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
                'plone-Copy':            theRdCtxt.fUITr( 'Copy'),
                'portal_url':            aSRES[ 'portal_url'],
            })




    if unPermitePegarElementos:

        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Paste)s" id="%(unIdTabla)s_MenuAction_Paste_Link"
            href="%(SRES-url)sMDDPaste" >
                <img src="%(portal_url)s/paste_icon.gif"  alt="%(plone-Paste)s" title="%(plone-Paste)s"  />
                <span>%(plone-Paste)s</span>        
            </a>
        </li>
        """ % {
                'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
                'plone-Paste':          theRdCtxt.fUITr( 'Paste'),
                'portal_url':           aSRES[ 'portal_url'],
                'SRES-url':             aSRES[ 'url'],
            })


    if unPermiteEliminarAlgunElemento:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Delete)s" id="%(unIdTabla)s_MenuAction_Delete_Link"
                onclick="pMDDSubmit_varios( 'Delete', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/delete_icon.gif"  alt="%(plone-Delete)s" title="%(plone-Delete)s"  />
                <span>%(plone-Delete)s</span>        
            </a>
        </li>
        """ % {
                'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
                'plone-Delete':          theRdCtxt.fUITr( 'Delete'),
                'portal_url':            aSRES[ 'portal_url'],
            })


    if unPermiteOrdenarElementos:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Reorder)s" id="%(unIdTabla)s_MenuAction_Reorder_Link"
            href="%(SRES-url)sMDDOrdenar/" >
                <img src="%(portal_url)s/subirbajar.gif"  alt="%(plone-Reorder)s" title="%(plone-Reorder)s"  />
                <span>%(plone-Reorder)s</span>        
            </a>
        </li>
        """ % {
                'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
                'plone-Reorder':           theRdCtxt.fUITr( 'Reorder'),
                'portal_url':            aSRES[ 'portal_url'],
                'SRES-url':              aSRES[ 'url'],
            })

    theRdCtxt.pOS("""
            </ul>
        </dd>
    </dl>
    """)


    return [ True, True,]








def _MDDRender_Tabular_ReferenciasEnTabla( theRdCtxt):


    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]

    aPREFS_PRES = theRdCtxt.fGP( 'PREFS_PRES', {})
    #if not aPREFS_PRES:
        #return [ False, True,]

    theRdCtxt.pSP ( 'thePermiteEnlazarElementos',
                    aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                    aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and ( not aTRAVRES[ 'max_multiplicity_reached']) and \
                    not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True)) and \
                    not (  aTRAVRES.get( 'dependency_supplier', False) == True)
                    )

    #theRdCtxt.pSP ( 'thePermiteEditarElementos',
        #aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
        #aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission']
    #)

    theRdCtxt.pSP ( 'thePermiteOrdenarElementos',
                    aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                    aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission']
                    )

    theRdCtxt.pSP ( 'thePermiteDesenlazarElementos',
                    aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                    aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and\
                    not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True)) and \
                    not (  aTRAVRES.get( 'dependency_supplier', False) == True)
                    )

    theRdCtxt.pSP ( 'thePermiteModificarElementos', theRdCtxt.fGP ( 'thePermiteOrdenarElementos', False) or  theRdCtxt.fGP ( 'thePermiteDesenlazarElementos', False))

    unIdTabla = 'hidMDDTraversal_%(traversal_name)s_Table' % {
        'traversal_name':                      aTRAVRES[ 'traversal_name'],
    }
    theRdCtxt.pSP( 'unIdTabla', unIdTabla)    

    someElements   = aTRAVRES.get( 'elements', [])
    unNumElements = len( someElements)

    unSiempre     = theRdCtxt.fGP( 'theSiempre', True)



    if someElements or unSiempre:

        theRdCtxt.pOS( u"""
                       <h2 id="hidMDDTraversal_%(traversal_name)s_label" 
                       <a  id="hidMDDTraversal_%(traversal_name)s_link"
                       title="%(ModelDDvlPlone_recorrercursorrelacion_action_label)s %(traversal_label)s %(ModelDDvlPlone_deorigenrelacioncuandoenlazando)s %(SRES-title)s"
                       href="%(SRES-url)sTabular/?theRelationCursorName=%(traversal_name)s%(theExtraLinkHrefParams)s" >
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                               'theExtraLinkHrefParams':                             theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                               'ModelDDvlPlone_recorrercursorrelacion_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_recorrercursorrelacion_action_label'),
                               'ModelDDvlPlone_deorigenrelacioncuandoenlazando':     theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),
                               'SRES-url':                 aSRES[ 'url'],
                               'portal_url':               aSRES[ 'portal_url'],
                               'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                               'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                               'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                               'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                           })


        aTraversalName = aTRAVRES.get( 'traversal_name', '')
        if not ( aTraversalName in [ 'referidos', 'referentes', 'referidosCualificados',]):

            someRelatedTypesAndIcons = aTRAVRES[ 'related_types_and_icons']

            for unTipoElemento, unIconElemento in someRelatedTypesAndIcons:
                if unIconElemento:
                    theRdCtxt.pOS( u"""
                                   <img src="%(portal_url)s/%(RELATED-icon)s" 
                                   title=%(RELATED-type)s"/>
                                   """ % {
                                           'portal_url':                  aSRES[ 'portal_url'],
                                           'RELATED-icon':                unIconElemento,
                                           'RELATED-type':                unTipoElemento,
                                       })     

        theRdCtxt.pOS( u"""
                       <span class="state-visible" id="hidMDDTraversal_%(traversal_name)s_title" >%(traversal_label)s</span>
                       </a>
                       <font size=1">            
                       &emsp;
                       &emsp;
                       <table  cellspacing="0" cellpadding="0" frame="void" style="display: inline" ><tbody><tr>
                       <td id="cid_MDDTOC_Holder_Traversal_%(traversal_name)s" valign="top" align="left">
                       <a title="%(ModelDDvlPlone_Tabular_Sections)s"
                       onclick="document.getElementById( 'cid_MDDTOC_Holder_Traversal_%(traversal_name)s').appendChild( document.getElementById( 'cid_MDDSectionList_ActionsMenu')); if ( hasClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated' )) { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'deactivated', 'activated');} else { replaceClassName( document.getElementById( 'cid_MDDSectionList_ActionsMenu') ,'activated', 'deactivated')} return true;">
                       <img src="%(portal_url)s/menusecciones.gif" title="%(ModelDDvlPlone_Tabular_Sections)s" alt="%(ModelDDvlPlone_Tabular_Sections)s" id="icon-sectionsmenu" />
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                               'theExtraLinkHrefParams':                             theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                               'ModelDDvlPlone_recorrercursorrelacion_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_recorrercursorrelacion_action_label'),
                               'ModelDDvlPlone_deorigenrelacioncuandoenlazando':     theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),
                               'SRES-url':                 aSRES[ 'url'],
                               'portal_url':               aSRES[ 'portal_url'],
                               'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                               'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                               'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                               'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                           })




        if aPREFS_PRES.get( 'DisplayActionLabels', False):
            theRdCtxt.pOS( u"""
                           <span>%(ModelDDvlPlone_Tabular_Sections)s</span>
                           """ % {
                                   'ModelDDvlPlone_Tabular_Sections':    theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                               })


        theRdCtxt.pOS( u"""
                       </a>
                       </td>
                       </tr></tbody></table>
                       </font>            
                       </h2>
                       <p class="formHelp">%(traversal_description)s</p>
                       """ % {
                               'ModelDDvlPlone_Tabular_Sections':     theRdCtxt.fUITr( 'ModelDDvlPlone_Tabular_Sections',),
                               'theExtraLinkHrefParams':                             theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                               'ModelDDvlPlone_recorrercursorrelacion_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_recorrercursorrelacion_action_label'),
                               'ModelDDvlPlone_deorigenrelacioncuandoenlazando':     theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),
                               'SRES-url':                 aSRES[ 'url'],
                               'portal_url':               aSRES[ 'portal_url'],
                               'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                               'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                               'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                               'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                           })



        theRdCtxt.pOS( u"""
                       <table width="100%%" id="%(unIdTabla)s" class="listing" summary="%(SRES-title)s"  >
                       """ % {
                               'unIdTabla':                fCGIE( unIdTabla),
                               'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                           })


        theRdCtxt.pOS( u"""
                       <col width="24" />
                       """)

        unTotalColumns = 1

        if theRdCtxt.fGP( 'thePermiteModificarElementos', False):
            theRdCtxt.pOS( u"""
                           <col width="%d" />
                           """ % ( theRdCtxt.fGP ( 'thePermiteDesenlazarElementos', False) and 110 or 90))

            unTotalColumns += 1


        someColumnNames = aTRAVRES.get( 'column_names', [])
        unNumColumnNames =len( someColumnNames)

        theRdCtxt.pOS( u"""
                       <col/>
                       """ * unNumColumnNames)


        theRdCtxt.pOS( u"""
                       <thead>
                       <tr>
                       """ )




        theRdCtxt.pOS( u"""
                       <th class="nosort" align="left" >
                       <input type="checkbox"  class="noborder"  value=""
                       name="%(unIdTabla)s_SelectAll" id="%(unIdTabla)s_SelectAll" 
                       onchange="pMDDToggleAllSelections('%(unIdTabla)s'); return true;"/>
                       """ %{
                               'unIdTabla':    fCGIE( unIdTabla),
                           })


        unPermiteModificarAlgunElemento = False
        for aERES in someElements:
            if aERES[ 'read_permission'] and aERES[ 'write_permission']:
                unPermiteModificarAlgunElemento = True
                break



        if not ( theRdCtxt.fGP( 'thePermiteModificarElementos', False) or unPermiteModificarAlgunElemento):

            anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Traversals_Relations_GroupActionsMenu')( theRdCtxt)

            theRdCtxt.pOS( u"""
                           </th>
                           """)
        else:
            theRdCtxt.pOS( u"""
                           </th>
                           <th class="nosort" align="left" > 
                           """)

            anOk, aGo = _fMCtx( False, theRdCtxt, 'MDDRender_Tabular_Traversals_Relations_GroupActionsMenu')( theRdCtxt)

            theRdCtxt.pOS( u"""
                           </th>
                           """)


        #if theRdCtxt.fGP( 'thePermiteModificarElementos', False):
            #theRdCtxt.pOS( u"""
                #<th align="center" >&ensp;%(ModelDDvlPlone_editar_action_label)s&ensp;</th>
            #""" % {
                #'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),        
            #})


        for unColumnName in someColumnNames:

            theRdCtxt.pOS( u"""
                           <th class="nosort" align="left" >%s</th>
                           """ % fCGIE( aTRAVRES[ 'column_translations'].get( unColumnName, {}).get( 'translated_label', unColumnName)),
                               )

            unTotalColumns += 1



        if aTRAVRES[ 'traversal_name'] in cTraversalNames_GeneralReferences_WithTypeColumn:
            theRdCtxt.pOS( u"""
                           <th class="nosort" width="120" align="left">%(ModelDDvlPlone_tipo_label)s</th>
                           <th class="nosort" align="left">&nbsp;%(ModelDDvlPlone_path_label)s&nbsp;</th>
                           """ % {
                                   'ModelDDvlPlone_tipo_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_tipo_label'),        
                                   'ModelDDvlPlone_path_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_path_label'),        
                               })

            unTotalColumns += 2

        theRdCtxt.pOS( u"""
                       </tr>
                       </thead>
                       <tbody>
                       """ )


        for unIndexElemento in range( unNumElements):

            aERES = someElements[ unIndexElemento]

            if aERES[ 'read_permission'] :

                aELEM = aERES.get( 'object', None)

                aSubRdCtxt = theRdCtxt.fNewCtxt( {
                    'ERES' : aERES,
                })

                aSubRdCtxt.pOS( u"""
                                <tr class="%(Row-Class)s" id="%(unIdTabla)s_RowIndex_%(Row-Index)d" >
                                """ % {
                                        'unIdTabla': fCGIE( unIdTabla),
                                        'Row-Class': cClasesFilas[ unIndexElemento % 2],
                                        'Row-Index': unIndexElemento,
                                    })


                aSubRdCtxt.pOS( u"""
                                <td align="center" valign="baseline">
                                <input type="checkbox"  class="noborder"  value=""
                                name="%(unIdTabla)s_Select_%(Row-Index)d"
                                id="%(unIdTabla)s_Select_%(Row-Index)d"  />
                                </td>
                                """ % {
                                        'Row-Index': unIndexElemento,
                                        'unIdTabla': fCGIE( unIdTabla),
                                    })

                if theRdCtxt.fGP( 'thePermiteModificarElementos', False) or unPermiteModificarAlgunElemento:
                    theRdCtxt.pOS( u"""
                                   <td align="center" valign="baseline" id="%(unIdTabla)s_%(ERES-id)s_ChangesLinks_Cell">
                                   """ % {
                                           'unIdTabla':                fCGIE( unIdTabla),
                                           'ERES-id':                  fCGIE( aERES[ 'id']),
                                       })

                    if theRdCtxt.fGP( 'thePermiteDesenlazarElementos', False) and aERES[ 'write_permission']:
                        theRdCtxt.pOS( u"""
                                       <a id="hidMDDRelation_%(traversal_name)s_%(ERES-id)s_Unlink_link" 
                                       title="%(unActionTitle)s"
                                       href="%(SRES-url)sEnlazar/?theReferenceFieldName=%(traversal_name)s&theUnlinkUID=%(ERES-UID)s%(theExtraLinkHrefParams)s" >
                                       <img id="hidMDDRelation_%(traversal_name)s_%(ERES-id)s_Unlink_icon" 
                                       alt="%(unActionTitle)s"
                                       title="%(unActionTitle)s" 
                                       src="%(portal_url)s/desenlazar.gif" />
                                       </a>
                                       &nbsp;
                                       """ % {
                                               'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                               'unActionTitle': '%s %s %s %s %s'% ( 
                                                   theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_action_label'),
                                                   fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),
                                                   fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                   theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_DE'),
                                                   fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                   ),
                                               'unIdTabla':                fCGIE( unIdTabla),
                                               'ModelDDvlPlone_desenlazar_DE':  theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_DE'),
                                               'ModelDDvlPlone_desenlazar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_action_label'),
                                               'SRES-url':                 aSRES[ 'url'],
                                               'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                                               'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                                               'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                                               'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                               'ERES-title':               fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                               'portal_url':               aERES[ 'portal_url'],
                                               'ERES-UID':                 fCGIE( aERES[ 'UID']),
                                               'ERES-id':                  fCGIE( aERES[ 'id']),
                                           })


                    if  aERES[ 'write_permission']: # and theRdCtxt.fGP( 'thePermiteEditarElementos', False)
                        theRdCtxt.pOS( u"""
                                       <a id="hidMDDRelation_%(traversal_name)s_%(ERES-id)s_Edit_link" 
                                       title="%(ModelDDvlPlone_editar_action_label)s %(SRES-title)s"
                                       href="%(ERES-url)sEditar/%(theExtraLinkHrefParams)s" >
                                       <img id="hidMDDRelation_%(traversal_name)s_%(ERES-id)s_Edit_icon" 
                                       alt="%(ModelDDvlPlone_editar_action_label)s %(SRES-title)s"
                                       title="%(ModelDDvlPlone_editar_action_label)s %(SRES-title)s" 
                                       src="%(portal_url)s/edit.gif" />
                                       </a>
                                       &nbsp;
                                       """ % {
                                               'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                               'ModelDDvlPlone_editar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_editar_action_label'),
                                               'ERES-url':                 aERES[ 'url'],
                                               'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                                               'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                                               'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                                               'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                               'portal_url':               aERES[ 'portal_url'],
                                               'ERES-UID':                 fCGIE( aERES[ 'UID']),
                                               'ERES-id':                  fCGIE( aERES[ 'id']),
                                           })

                    else:
                        theRdCtxt.pOS( u"""
                                       <img src="%(portal_url)s/blank_icon.gif" alt="Blank" title="Blank" id="icon-blank" />
                                       &nbsp;
                                       """ % {
                                               'portal_url':               aERES[ 'portal_url'],
                                           })



                    if ( unNumElements > 1)  and theRdCtxt.fGP( 'thePermiteOrdenarElementos', False):


                        if unIndexElemento:
                            theRdCtxt.pOS( u"""
                                           <a id="hidMDDRelation_%(traversal_name)s_%(ERES-id)s_Up_link" 
                                           title="%(ModelDDvlPlone_subir_action_label)s %(SRES-title)s"
                                           href="%(SRES-url)sTabular/?theReferenceFieldName=%(traversal_name)s&theMovedReferenceUID=%(ERES-UID)s&theMoveDirection=Up&dd=%(millis)d%(theExtraLinkHrefParams)s#%(unIdTabla)s_%(ERES-id)s_ChangesLinks_Cell" >
                                           <img id="hidMDDRelation_%(traversal_name)s_%(ERES-id)s_Up_icon" 
                                           alt="%(ModelDDvlPlone_subir_action_label)s %(SRES-title)s"
                                           title="%(ModelDDvlPlone_subir_action_label)s %(SRES-title)s" 
                                           src="%(portal_url)s/arrowUp.gif" />
                                           </a>
                                           &nbsp;
                                           """ % {
                                                   'theExtraLinkHrefParams':   theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                                   'unIdTabla':                fCGIE( unIdTabla),
                                                   'Row-Index':                unIndexElemento,
                                                   'millis':                   fMillisecondsNow(), 
                                                   'ModelDDvlPlone_subir_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_subir_action_label'),
                                                   'SRES-url':                 aSRES[ 'url'],
                                                   'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                                                   'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),
                                                   'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']), 
                                                   'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                   'portal_url':               aERES[ 'portal_url'],
                                                   'ERES-UID':                 fCGIE( aERES[ 'UID']),
                                                   'ERES-id':                 fCGIE( aERES[ 'id']),
                                               })

                        else:

                            theRdCtxt.pOS( u"""
                                           <img src="%(portal_url)s/arrowBlank.gif" alt="Blank" title="Blank" id="icon-blank" />
                                           &nbsp;
                                           """ % {
                                                   'portal_url':               aERES[ 'portal_url'],
                                               })



                        if unIndexElemento < ( unNumElements - 1):
                            theRdCtxt.pOS( u"""
                                           <a id="hidMDDRelation_%(traversal_name)s_%(ERES-id)s_Down_link" 
                                           title="%(ModelDDvlPlone_bajar_action_label)s %(SRES-title)s"
                                           href="%(SRES-url)sTabular/?theReferenceFieldName=%(traversal_name)s&theMovedReferenceUID=%(ERES-UID)s&theMoveDirection=Down&dd=%(millis)d%(theExtraLinkHrefParams)s#%(unIdTabla)s_%(ERES-id)s_ChangesLinks_Cell" >
                                           <img id="hidMDDRelation_%(traversal_name)s_%(ERES-id)sDown_icon" 
                                           alt="%(ModelDDvlPlone_bajar_action_label)s %(SRES-title)s"
                                           title="%(ModelDDvlPlone_bajar_action_label)s %(SRES-title)s" 
                                           src="%(portal_url)s/arrowDown.gif" />
                                           </a>
                                           &nbsp;
                                           """ % {
                                                   'theExtraLinkHrefParams':   theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                                   'unIdTabla':                fCGIE( unIdTabla),
                                                   'Row-Index':                unIndexElemento,
                                                   'millis':                   fMillisecondsNow(), 
                                                   'ModelDDvlPlone_bajar_action_label':  theRdCtxt.fUITr( 'ModelDDvlPlone_bajar_action_label'),
                                                   'SRES-url':                 aSRES[ 'url'],
                                                   'traversal_name':           fCGIE( aTRAVRES[ 'traversal_name']),        
                                                   'traversal_label':          fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                                                   'traversal_description':    fCGIE( aTRAVRES[ 'traversal_translations']['translated_description']),  
                                                   'SRES-title':               fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                                   'portal_url':               aERES[ 'portal_url'],
                                                   'ERES-UID':                 fCGIE( aERES[ 'UID']),
                                                   'ERES-id':                  fCGIE( aERES[ 'id']),
                                               })

                        else:

                            theRdCtxt.pOS( u"""
                                           <img src="%(portal_url)s/arrowBlank.gif" alt="Blank" title="Blank" id="icon-blank" />
                                           &nbsp;
                                           """ % {
                                                   'portal_url':               aERES[ 'portal_url'],
                                               })

                    theRdCtxt.pOS( u"""
                                   </td>
                                   """ )


                for unColumnName in someColumnNames:

                    theRdCtxt.pOS( u"""
                                   <td align="left" valign="baseline" >
                                   """)

                    if ( unColumnName == 'title') or ( unColumnName.lower().find('title') >= 0) or ( not ( 'title' in someColumnNames) and  ( unColumnName == someColumnNames[ 0])):

                        unTitle = u'%s %s %s %s %s (%s)' % ( 
                            theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'), 
                            fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']),
                            fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']), 
                            ( not ( unColumnName == 'title')       and  fCGIE( aERES[ 'values_by_name'].get( 'title', {}).get( 'uvalue', ''))) or '', 
                            ( not ( unColumnName == 'description') and  fCGIE( aERES[ 'values_by_name'].get( 'description', {}).get( 'uvalue', ''))) or '',
                            fCGIE( aERES[ 'type_translations'][ 'translated_type_description']),
                        )


                        theRdCtxt.pOS( u"""
                                       <a  class="state-visible" 
                                       name="hidMDDElemento_%(ERES-UID)s"
                                       id="%(unIdTabla)s_RowIndex_%(Row-Index)d_NavegarA_Link"
                                       href="%(ERES-url)sTabular/%(theExtraLinkHrefParams)s" 
                                       title="%(unTitle)s" >
                                       <h4>
                                       <img src="%(portal_url)s/%(content_icon)s" 
                                       alt="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" 
                                       title="%(ModelDDvlPlone_navegara_action_label)s %(translated_archetype_name)s %(ERES-title)s" />
                                       <span  id="hidMDDElemento_%(ERES-UID)s" class="state-visible">%(column_value)s</span>
                                       </h4>
                                       </a>
                                       &nbsp;    

                                       """ %{
                                               'theExtraLinkHrefParams':              theRdCtxt.fGP( 'theExtraLinkHrefParamsFirst'),
                                               'Row-Index':                           unIndexElemento,
                                               'unTitle':                             fCGIE( unTitle),
                                               'millis':                              fMillisecondsNow(), 
                                               'unIdTabla':                           fCGIE( unIdTabla),
                                               'ModelDDvlPlone_navegara_action_label':theRdCtxt.fUITr( 'ModelDDvlPlone_navegara_action_label'),
                                               'translated_archetype_name':           fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                               'ERES-title':                          fCGIE( aERES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                               'ERES-id':                             fCGIE( aERES[ 'id']),
                                               'ERES-UID':                            fCGIE( aERES[ 'UID']),
                                               'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                                               'ERES-url':                            aERES[ 'url'],
                                               'content_icon':                        fCGIE( aERES[ 'content_icon']),
                                               'portal_url':                          aERES[ 'portal_url'],
                                               'column_value':                        fCGIE( aERES[ 'values_by_name'][ unColumnName][ 'uvalue']),

                                           })

                    else:

                        unAttributeResult =  aERES[ 'values_by_name'].get( unColumnName, {})

                        if unAttributeResult:

                            if unAttributeResult[ 'type'] in [ 'selection', 'boolean']:
                                theRdCtxt.pOS( u"""
                                               <span>%s</span>
                                               """ % fCGIE( unAttributeResult.get( 'translated_value', ''))
                                                   )
                            else:
                                if unAttributeResult[ 'uvalue'] and not ( unAttributeResult[ 'uvalue'] =='None'):
                                    theRdCtxt.pOS( u"""
                                                   <span>%s</span>
                                                   """ % fCGIE( unAttributeResult.get( 'uvalue', '') ))


                    theRdCtxt.pOS( u"""
                                   </td>
                                   """ )

                if aTRAVRES[ 'traversal_name'] in cTraversalNames_GeneralReferences_WithTypeColumn:
                    theRdCtxt.pOS( u"""
                                   <td >%(ERES-tipo)s</td>
                                   <td >%(ERES-path)s</td>
                                   """ % {
                                           'ERES-tipo': fCGIE( aERES[ 'type_translations'][ 'translated_archetype_name']), 
                                           'ERES-path': fCGIE( aERES[ 'path']), 
                                       })

                theRdCtxt.pOS( u"""
                               </tr>
                               """ )


        theRdCtxt.pOS( u"""
                       </tbody>
                       """ )

        if theRdCtxt.fGP( 'thePermiteEnlazarElementos', False) or theRdCtxt.fGP ( 'thePermiteDesenlazarElementos', False):

            theRdCtxt.pOS( u"""
                           <tfoot>
                           <tr class="%(Row-Class)s" >
                           <td colspan="%(colspan)d">
                           <a  id="hidMDDRelation_%(traversal_name)s_ChangeReferences_Link"
                           href="%(SRES-url)sEnlazar/?theReferenceFieldName=%(traversal_name)s%(theExtraLinkHrefParams)s"
                           title="%(ModelDDvlPlone_cambiar_referencias_action_label)s %(traversal_label)s %(ModelDDvlPlone_deorigenrelacioncuandoenlazando)s %(SRES-title)s" >
                           <img id="hidMDDRelation_%(traversal_name)s_ChangeReferences_Icon"
                           src="%(portal_url)s/enlazar.gif" 
                           alt="%(ModelDDvlPlone_cambiar_referencias_action_label)s"
                           title="%(ModelDDvlPlone_cambiar_referencias_action_label)s"/>
                           &emsp;
                           <span>%(ModelDDvlPlone_cambiar_referencias_action_label)s</span>
                           </a>
                           </td>
                           </tr>
                           </tfoot>
                           """ % {
                                   'ModelDDvlPlone_deorigenrelacioncuandoenlazando':     theRdCtxt.fUITr( 'ModelDDvlPlone_deorigenrelacioncuandoenlazando'),                    
                                   'theExtraLinkHrefParams':                          theRdCtxt.fGP( 'theExtraLinkHrefParamsCont'),
                                   'portal_url':                                      aSRES[ 'portal_url'],
                                   'SRES-url':                                        aSRES[ 'url'],
                                   'SRES-title':                                      fCGIE( aSRES[ 'values_by_name'][ 'title'][ 'uvalue']),
                                   'ModelDDvlPlone_cambiar_referencias_action_label': theRdCtxt.fUITr( 'ModelDDvlPlone_cambiar_referencias_action_label'),
                                   'traversal_name':                                  fCGIE( aTRAVRES[ 'traversal_name']),
                                   'traversal_label':                                 fCGIE( aTRAVRES[ 'traversal_translations']['translated_label']),        
                                   'colspan':                                         unTotalColumns,
                                   'unIdTabla':                                       fCGIE( unIdTabla),
                                   'Row-Class':                                       cClasesFilas[ unNumElements % 2],
                               })





        theRdCtxt.pOS( u"""
                       </tbody>
                       </table>
                       """ )



    theRdCtxt.pOS( u"""
                   <form method="POST" id="%(unIdTabla)s_Form">

                   <input type="hidden" value="%(SRES-UID)s"
                   name="theContainerUID" id="%(unIdTabla)s_ContainerUID"/> 

                   <input type="hidden" value="%(traversal_name)s"
                   name="theReferenceFieldName" id="%(unIdTabla)s_ReferenceFieldName"/> 

                   <input type="hidden" value=""
                   name="theGroupAction"  id="%(unIdTabla)s_GroupAction" />
                   """ % {
                           'unIdTabla':                           fCGIE( unIdTabla),
                           'SRES-UID':                            fCGIE( aSRES[ 'UID']),
                           'traversal_name':                      fCGIE( aTRAVRES[ 'traversal_name']),
                       })


    for unIndexElemento in range( unNumElements):

        aERES = someElements[ unIndexElemento]
        aSubRdCtxt = theRdCtxt.fNewCtxt( {
            'ERES' : aERES,
        })

        aSubRdCtxt.pOS( u"""
                        <input type="hidden" disabled value="%(ERES-UID)s"
                        name="theUIDs" id="%(unIdTabla)s_Select_%(unIndexElemento)d_UID" /> 
                        """ % {
                                'unIdTabla':                           fCGIE( unIdTabla),
                                'unIndexElemento':                     unIndexElemento,
                                'ERES-UID':                            fCGIE( aERES[ 'UID']),
                            })



    theRdCtxt.pOS( u"""
                   </form>
                   """)



    return [ True, True,]










def _MDDRender_Tabular_ReferenciaEnTabla( theRdCtxt):

    if True:
        return _MDDRender_Tabular_ReferenciasEnTabla( theRdCtxt)










def _MDDRender_Tabular_Traversals_Relations_GroupActionsMenu( theRdCtxt):

    aSRES = theRdCtxt.fGP( 'SRES', {})
    if not aSRES:
        return [ False, True,]

    #aPARENT_SRES = theRdCtxt.fGP( 'PARENT_SRES', {})
    #if not aPARENT_SRES:
        #return [ False, True,]

    aTRAVRES = theRdCtxt.fGP( 'TRAVRES', {})
    if not aTRAVRES:
        return [ False, True,]

    someElements  = aTRAVRES.get( 'elements', [])


    unPermitePegarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                            aSRES[ 'add_permission'] and  \
                            aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                            ( not aTRAVRES[ 'max_multiplicity_reached']) and \
                            not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))  

    unPermiteOrdenarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                              aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                              not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True))  



    unPermiteDesenlazarAlgunElemento = False
    unPermiteDesenlazarElementos = aSRES[ 'read_permission'] and aSRES[ 'write_permission'] and \
                                 aTRAVRES[ 'read_permission'] and aTRAVRES[ 'write_permission'] and \
                                 not ( aTRAVRES['traversal_config'].has_key( 'no_ui_changes') and ( aTRAVRES['traversal_config'][ 'no_ui_changes'] == True)) and \
                                 not (  aTRAVRES.get( 'dependency_supplier', False) == True)

    if unPermiteDesenlazarElementos:
        for anElement in someElements:
            if anElement[ 'read_permission'] and ( anElement[ 'write_permission'] or anElement[ 'delete_permission']):
                unPermiteDesenlazarAlgunElemento = True
                break



    if not  theRdCtxt.fGP( cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName, False):

        theRdCtxt.pOS( cMDDRenderTabular_MenuAccionesGrupo_JavaScript)

        theRdCtxt.pSPGlobal( cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName, True)


    theRdCtxt.pOS("""
    <dl class="actionMenu activated" id="%(unIdTabla)s_ActionsMenu" >
        <dt class="actionMenuHeader" style="display: inline">
            <a>%(plone-heading_actions)s</a>
        </dt>
        <dd class="actionMenuContent">
            <ul>
    """ % {
            'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
            'plone-heading_actions': theRdCtxt.fUITr( 'heading_actions'),
        })




    if unPermiteDesenlazarAlgunElemento:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Cut)s" id="%(unIdTabla)s_MenuAction_Cut_Link"
                onclick="pMDDSubmitRelation_varios( 'CutToUnlink', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/cut_icon.gif"  alt="%(plone-Cut)s" title="%(plone-Cut)s"  />
                <span>%(plone-Cut)s</span>        
            </a>
        </li>
        """ % {
                'unIdTabla':             theRdCtxt.fGP(   'unIdTabla', ''),
                'plone-Cut':             theRdCtxt.fUITr( 'Cut'),
                'portal_url':            aSRES[ 'portal_url'],
            })

    if someElements:
        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Copy)s" id="%(unIdTabla)s_MenuAction_Copy_Link"
                onclick="pMDDSubmitRelation_varios( 'Copy', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/copy_icon.gif"  alt="%(plone-Copy)s" title="%(plone-Copy)s"  />
                <span>%(plone-Copy)s</span>        
            </a>
        </li>
        """ % {
                'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
                'plone-Copy':            theRdCtxt.fUITr( 'Copy'),
                'portal_url':            aSRES[ 'portal_url'],
            })




    if unPermitePegarElementos:

        theRdCtxt.pOS("""
        <li >
            <a title="%(plone-Paste)s" id="%(unIdTabla)s_MenuAction_Paste_Link"
            href="%(SRES-url)sMDDPasteReferences/?theReferenceFieldName=%(theReferenceFieldName)s" >
                <img src="%(portal_url)s/paste_icon.gif"  alt="%(plone-Paste)s" title="%(plone-Paste)s"  />
                <span>%(plone-Paste)s</span>        
            </a>
        </li>
        """ % {
                'theReferenceFieldName':  aTRAVRES.get( 'traversal_name', ''),
                'unIdTabla':              theRdCtxt.fGP(   'unIdTabla', ''),
                'plone-Paste':            theRdCtxt.fUITr( 'Paste'),
                'portal_url':             aSRES[ 'portal_url'],
                'SRES-url':               aSRES[ 'url'],
            })


    if unPermiteDesenlazarAlgunElemento:
        theRdCtxt.pOS("""
        <li >
            <a title="%(ModelDDvlPlone_desenlazar_action_label)s" id="%(unIdTabla)s_MenuAction_Unlink"
                onclick="pMDDSubmitRelation_varios( 'Unlink', '%(unIdTabla)s'); return true;" >
                <img src="%(portal_url)s/desenlazar.gif"  alt="%(ModelDDvlPlone_desenlazar_action_label)s" title="%(ModelDDvlPlone_desenlazar_action_label)s"  />
                <span>%(ModelDDvlPlone_desenlazar_action_label)s</span>        
            </a>
        </li>
        """ % {
                'unIdTabla':            theRdCtxt.fGP(   'unIdTabla', ''),
                'ModelDDvlPlone_desenlazar_action_label':          theRdCtxt.fUITr( 'ModelDDvlPlone_desenlazar_action_label'),
                'portal_url':            aSRES[ 'portal_url'],
            })


    theRdCtxt.pOS("""
            </ul>
        </dd>
    </dl>
    """)

    return [ True, True,]






def _MDDRender_Tabular_Plone( theRdCtxt):


    aPLONERES = theRdCtxt.fGP( 'PLONERES', {})
    if not aPLONERES:
        return [ False, True,]


    aNewRdCtxt = theRdCtxt.fNewCtxt({
        'SRES':  aPLONERES,
    })

    anOk, aGo = _fMCtx( False, aNewRdCtxt, 'MDDRender_Tabular_Traversals')( aNewRdCtxt)
    if not aGo:
        return [ True, aGo,]

    return [ True, True,]






def _MDDRender_Tabular_StripFinalOutput( theRdCtxt):
    """Produce the final output string.

    """    
    aNewOutputString = u''

    anOutput = theRdCtxt.fGP( 'output', None)
    if anOutput:

        anOutputString = anOutput.getvalue()
        if anOutputString:

            aNewOutputString = anOutputString.replace( u"\n\n", u"\n")

            while not ( aNewOutputString == anOutputString):
                anOutputString = aNewOutputString
                aNewOutputString = anOutputString.replace( u"\n\n", u"\n")


    theRdCtxt.pSP( 'output_string', aNewOutputString)

    return [ True, True,]






# #######################################################################
"""Parameters relevant to the rendering of the Tabular view.

"""
def _fNewVoidViewParms_Tabular( ):
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













# #######################################################################
"""Support for dynamic extensions of the Tabular rendering.

   Callable objects executing the Tabular view rendering are obtained by name from a dictionary.
   The dictionary is intialized with default methods defined in this module,
   and overriden with callable objects supplied or specified in the supplied parameters, or the Request.
   Callable objects to be supported are : external methods, scripts, templates, and Python source code.

"""








# #######################################################################
"""List of all Methods invoked during the execution of the rendering, including extension points. 

"""
cBindeableMethods_Components = [
    _MDDInit_Parms_Tabular,
    _MDDRender_Tabular,
    _MDDRender_Tabular_Javascript,
    _MDDRender_Tabular_Relation,
    _MDDRender_Tabular_Cabecera,
    _MDDRender_Tabular_Cabecera_TypeAndDescription,
    _MDDRender_Tabular_Cabecera_OwnerAndContainer,
    _MDDRender_Tabular_Cabecera_Refresh,
    _MDDRender_Tabular_Cabecera_Textual,
    _MDDRender_Tabular_Cabecera_Cursor,
    _MDDRender_Tabular_SiblingsMenu,
    _MDDRender_Tabular_Cabecera_ChangeActions,
    _MDDRender_Tabular_Cabecera_ClipboardActions,
    _MDDRender_Tabular_SectionsMenu,
    _MDDRender_Tabular_Cabecera_SectionsMenu_Anchor,
    _MDDRender_Tabular_SiblingsMenu,
    _MDDRender_Tabular_ColeccionEnTabla,
    _MDDRender_Tabular_ColeccionEnTabla_Header,
    _MDDRender_Tabular_ColeccionesEnTabla,
    _MDDRender_Tabular_Coleccion_Sola,
    _MDDRender_Tabular_CustomPresentationViews,
    _MDDRender_Tabular_Traversals_Aggregations_GroupActionsMenu,
    _MDDRender_Tabular_Traversals_Relations_GroupActionsMenu,
    _MDDRender_Tabular_Plone,
    _MDDRender_Tabular_Tabla_Plone,
    _MDDRender_Tabular_Profiling,
    _MDDRender_Tabular_ReferenciasEnTabla,
    _MDDRender_Tabular_ReferenciaEnTabla,
    _MDDRender_Tabular_SinColeccionEnTabla,
    _MDDRender_Tabular_Tabla,
    _MDDRender_Tabular_Texts,
    _MDDRender_Tabular_Traversals,
    _MDDRender_Tabular_Values,
    _MDDRender_Customization_Form,
    _MDDRender_Tabular_Relation_Cabecera,
    _MDDRender_Tabular_Relation_Cabecera_Cursor,
    _MDDRetrieve_Info_Tabular,
    _MDDRetrieve_Info_RelationCursor_Owner,
    _MDDRetrieve_Info_RelationCursor_Current,
    _MDDRetrieve_Info_Plone,
    _MDDRetrieve_Preferences_Presentation_Tabular,
    _MDDRender_Tabular_StripFinalOutput,
]







# #######################################################################
"""Names of Methods invoked as extension points, during the execution of the rendering.

"""




cBindeableMethods_Extension_Names = [
    'MDDExtension_Before',
    'MDDExtension_After',
    'MDDExtension_InitParms_Before',
    'MDDExtension_InitParms_After',
    'MDDExtension_InitUITranslations_Before',
    'MDDExtension_InitUITranslations_After',
    'MDDExtension_Retrieval_Before',
    'MDDExtension_Retrieval_After',
    'MDDExtension_RetrievePreferences_Before',
    'MDDExtension_RetrievePreferences_After',
    'MDDExtension_Render_Tabular_Before',
    'MDDExtension_Render_Tabular_After',  
    'MDDExtension_Render_Tabular_Cabecera_Before',
    'MDDExtension_Render_Tabular_Cabecera_After',
    'MDDExtension_Render_Tabular_Cabecera_TypeAndDescription_Before',
    'MDDExtension_Render_Tabular_Cabecera_TypeAndDescription_After',
    'MDDExtension_Render_Tabular_Cabecera_OwnerAndContainer_Before',
    'MDDExtension_Render_Tabular_Cabecera_OwnerAndContainer_After',
    'MDDExtension_Render_Tabular_Cabecera_Cursor_Before',
    'MDDExtension_Render_Tabular_Cabecera_Cursor_After',   
    'MDDExtension_Render_Tabular_SectionsMenu_Before',
    'MDDExtension_Render_Tabular_SectionsMenu_After',
    'MDDExtension_Render_Tabular_SiblingsMenu_Before',
    'MDDExtension_Render_Tabular_SiblingsMenu_After',
    'MDDExtension_Render_Tabular_Cabecera_ChangeActions_Before',
    'MDDExtension_Render_Tabular_Cabecera_ChangeActions_After',
    'MDDExtension_Render_Values_Before',
    'MDDExtension_Render_Values_After',
    'MDDExtension_Render_Tabular_Texts_Before',
    'MDDExtension_Render_Tabular_Texts_After',
    'MDDExtension_Render_Tabular_CustomPresentationViews_Before',
    'MDDExtension_Render_Tabular_CustomPresentationViews_After',
    'MDDExtension_Render_Tabular_Traversals_Before',
    'MDDExtension_Render_Tabular_Traversals_After',
    'MDDExtension_Render_Tabular_Coleccion_Sola_Before',
    'MDDExtension_Render_Tabular_Coleccion_Sola_After',
    'MDDExtension_Render_Tabular_ColeccionesEnTabla_Before',
    'MDDExtension_Render_Tabular_ColeccionesEnTabla_After',
    'MDDExtension_Render_Tabular_SinColeccionEnTabla_Before',
    'MDDExtension_Render_Tabular_SinColeccionEnTabla_After',
    'MDDExtension_Render_Tabular_ReferenciasEnTabla_Before',
    'MDDExtension_Render_Tabular_ReferenciasEnTabla_After',
    'MDDExtension_Render_Tabular_ReferenciaEnTabla_Before',
    'MDDExtension_Render_Tabular_ReferenciaEnTabla_After',
    'MDDExtension_Render_Tabular_GenericReferences_Before',
    'MDDExtension_Render_Tabular_GenericReferences_After',
    'MDDExtension_Render_Tabular_Plone_Before',
    'MDDExtension_Render_Tabular_Plone_After',    
    'MDDExtension_Render_Tabular_Tabla_Plone_Before',
    'MDDExtension_Render_Tabular_Tabla_Plone_After',    
    'MDDExtension_Render_Tabular_Relation_Cabecera_Before',
    'MDDExtension_Render_Tabular_Relation_Cabecera_After',
    'MDDExtension_Render_Tabular_Relation_Cabecera_Cursor_Before',
    'MDDExtension_Render_Tabular_Relation_Cabecera_Cursor_After',
    'MDDExtension_RenderProfiling_Before',
    'MDDExtension_RenderProfiling_After',
    'MDDExtension_StripFinalOutput_Before',
    'MDDExtension_StripFinalOutput_After',
]







# #######################################################################
"""Wrappers to execute templates, scripts and Python code supplied as a resolution of bindable methods executed during the rendering. 

"""
def _MDDRender_Wrapper_ForCompiledCode_Eval( theRdCtxt, theModelDDvlPloneTool, theBrowsedElement, theCompiledCode):

    anEvalResult = fEvalString( 
        theCompiledCode, 
        'usual',
        {   '__builtins__':          None, 
            'theRdCtxt':             theRdCtxt, 
            'theModelDDvlPloneTool': theModelDDvlPloneTool, 
            'theBrowsedElement':     theBrowsedElement, 
            'theCompiledCode':       theCompiledCode, 
            },
        theRaiseExceptions=True,
    )

    if anEvalResult:
        theRdCtxt.pO( anEvalResult)

    return [ True, True,]      # Executed correctly, the rendering may indeed proceed





def _MDDRender_Wrapper_ForCompiledCode_Exec( theRdCtxt, theModelDDvlPloneTool, theBrowsedElement, theCompiledCode):


    fEvalString( 
        theCompiledCode, 
        'usual',
        {   '__builtins__':          None, 
            'theRdCtxt':             theRdCtxt, 
            'theModelDDvlPloneTool': theModelDDvlPloneTool, 
            'theBrowsedElement':     theBrowsedElement, 
            'theCompiledCode':       theCompiledCode, 
            },
        theRaiseExceptions=True,
    )

    return [ True, True,]      # Executed correctly, the rendering may indeed proceed




def _MDDRender_Wrap_CompiledCode( theModelDDvlPloneTool, theBrowsedElement, theCompiledCode, theExecutionMode):
    """Wrap the compiled code as callable that shall receive theRdCtxt as parameter, and execute the code with exec() when invoked.

    """
    if not theCompiledCode:
        return None

    if theExecutionMode == 'eval':
        aWrappedCompiledCode = lambda theRdCtxt: _MDDRender_Wrapper_ForCompiledCode_Eval( theRdCtxt, theModelDDvlPloneTool, theBrowsedElement, theCompiledCode)
    else:
        aWrappedCompiledCode = lambda theRdCtxt: _MDDRender_Wrapper_ForCompiledCode_Exec( theRdCtxt, theModelDDvlPloneTool, theBrowsedElement, theCompiledCode)

    return aWrappedCompiledCode







def _MDDRender_Wrapper_ForTemplate( theRdCtxt, theModelDDvlPloneTool, theBrowsedElement, theCallableTemplate):

    if not theRdCtxt:
        return [ False, None,] # Failed to execute, no opinion on whether or not to allow the rendering to proceed

    aTemplateResult = theCallableTemplate()

    if aTemplateResult:
        theRdCtxt.pO( aTemplateResult)

    return [ True, True,]      # Executed correctly, the rendering may indeed proceed








def _MDDRender_Wrap_Template( theModelDDvlPloneTool, theBrowsedElement, theCallableTemplate):
    """Wrap the callable as a callable that shall receive theRdCtxt as parameter, and such that the produced result string is appended to the rendering output.

    """
    if not theCallableTemplate:
        return None

    aWrappedTemplate = lambda theRdCtxt: _MDDRender_Wrapper_ForTemplate( theRdCtxt, theModelDDvlPloneTool, theBrowsedElement, theCallableTemplate)

    return aWrappedTemplate








def _MDDInit_ResolveMethodBinding( theModelDDvlPloneTool, theBrowsedElement, theMethodResolution):
    """Try to get an external method
    My be also a script or a template - with its rendered output appended (or not) to the output stream in the render context.
    May be also a string with python code to evaluate, possibly invoking an external method or script with a supplied name

    """

    if not theModelDDvlPloneTool:
        return None
    if not theBrowsedElement:
        return None
    if not theMethodResolution:
        return None

    # ######################################################
    """If a callable is supplied, resolve the method with the callable.

    """
    if callable( theMethodResolution):
        return theMethodResolution





    # ######################################################
    """Strings are used to name a template or script, or as Python code.

    """
    if not isinstance( theMethodResolution, str) or isinstance( theMethodResolution, unicode):
        return None

    unPortalRoot = theModelDDvlPloneTool.fPortalRoot()
    if unPortalRoot:

        # ######################################################
        """Try to get an external method.

        """
        unExternalMethod = None
        try:
            unExternalMethod = aq_get( unPortalRoot, theMethodResolution, None, 1)
        except:
            None  
        if unExternalMethod:
            if isinstance( unExternalMethod, ExternalMethod):
                return unExternalMethod






    # ######################################################
    """Try to get a template or a script, wrapped such that its output is appended to the render context output.

    """
    aTemplateCallable = None
    try:
        aTemplateCallable = theModelDDvlPloneTool.fTemplateCallable( theBrowsedElement, theMethodResolution)
    except:
        None
    if aTemplateCallable:

        aTemplateCallableWrapper = _MDDRender_Wrap_Template( theModelDDvlPloneTool, theBrowsedElement, aTemplateCallable)
        if aTemplateCallableWrapper:

            return aTemplateCallableWrapper



    # ######################################################
    """Try to compile as Python code, wrapped to call the compiled code as exec() when invoked.

    """
    someCode = theMethodResolution.strip().replace( '\r\n', '\n')
    if someCode.startswith( 'eval '):
        anExecutionMode = 'eval'
        someCode = someCode[ len( 'eval '):]

    elif someCode.startswith( 'exec '):
        anExecutionMode = 'exec'
        someCode = someCode[ len( 'exec '):]

    someCode = '%s\n' % someCode.strip()


    aCompiledCode = None
    try:
        aCompiledCode = compile( someCode, '<string>', anExecutionMode)
    except:
        None
    if aCompiledCode:

        aCompiledCodeWrapper = _MDDRender_Wrap_CompiledCode( theModelDDvlPloneTool, theBrowsedElement, aCompiledCode, anExecutionMode)
        if aCompiledCodeWrapper:

            return aCompiledCodeWrapper

    return None






def _MDDInit_MethodBindings_CombinedWrapper_Sequence( theRdCtxt, theFirstResolvedMethod, theOtherResolvedMethod):

    aFirstOk = True
    if theFirstResolvedMethod:
        aFirstOk, aFirstGo = theFirstResolvedMethod( theRdCtxt)
        if not aFirstGo:
            return [ aFirstOk, False,]

    if not theOtherResolvedMethod:
        return [ aFirstOk, True,]

    aOtherOk, aOtherGo = theOtherResolvedMethod( theRdCtxt)
    return [ aOtherOk, aOtherGo,]





def _MDDInit_MethodBindings_CombineResolvedMethods( theModelDDvlPloneTool, theBrowsedElement, theCombinationMode, theFirstResolvedMethod, theOtherResolvedMethod):

    if not theFirstResolvedMethod:
        return theOtherResolvedMethod

    if not theOtherResolvedMethod:
        return theFirstResolvedMethod

    #if theCombinationMode == 'sequence':
    aCombinedMethod = lambda theRdCtxt: _MDDInit_MethodBindings_CombinedWrapper_Sequence( theRdCtxt, theFirstResolvedMethod, theOtherResolvedMethod)

    return aCombinedMethod






def _MDDInit_MethodBindings_Resolve( theRdCtxt, theModelDDvlPloneTool, theBrowsedElement, theMethodName, theMethodResolutions):

    if not theRdCtxt:
        return False

    if not theModelDDvlPloneTool:
        return False

    if theBrowsedElement == None:
        return False

    if not theMethodResolutions:
        return False

    someMethodBindings = theRdCtxt.fGP( 'method_bindings', None)
    if someMethodBindings == None:
        return False

    anExistingResolvedMethod = someMethodBindings.get( theMethodName, None)

    someMethodResolutions = theMethodResolutions

    if not ( isinstance( someMethodResolutions, list) or isinstance( someMethodResolutions, tuple) or isinstance( someMethodResolutions, set)):
        someMethodResolutions = [ someMethodResolutions, ]

    aFinalResolvedMethod = None
    for aMethodResolution in someMethodResolutions:

        aResolvedMethod = _MDDInit_ResolveMethodBinding( theModelDDvlPloneTool, theBrowsedElement, aMethodResolution)
        if aResolvedMethod:

            if not aFinalResolvedMethod:
                aFinalResolvedMethod = aResolvedMethod

            else:
                aCombinedResolvedMethod = _MDDInit_MethodBindings_CombineResolvedMethods( theModelDDvlPloneTool, theBrowsedElement,'sequence', aFinalResolvedMethod, aResolvedMethod)
                if aCombinedResolvedMethod:
                    aFinalResolvedMethod = aCombinedResolvedMethod                

    someMethodBindings[ theMethodName] = aFinalResolvedMethod

    return True




def _MDDInit_MethodBindings( theRdCtxt):
    """Example in URL:
    http://localhost/modeldd/bpds/gvsig-i18n-manual-imported/Tabular/?theNoCache=1&theNoCacheCode=1261512200027&theCustom={%27MDDExtension_Before%27:%27MDDTryExtension%27,%27MDDExtension_Render_Tabular_Before%27:%27eval%201%20%2b%202%20%2b3%20%2b5%20%2b%207%2b%2011%27,%27MDDExtension_After%27:%27gvSIGbpd_creditos_i18n_view%27,}
    http://localhost:50080/modeldd/bpds/gvsig-i18n-manual-imported/Tabular/?theNoCache=1&theNoCacheCode=1261512200027&theCustom={'MDDExtension_Before':'gvSIGbpd_creditos_i18n_view','MDDExtension_Render_Tabular_Before':'eval 1 %2b 2 %2b3 %2b5 %2b  7%2b 11','MDDExtension_After':'MDDTryExtension',}    
    """
    if not theRdCtxt:
        return False


    someMethodBindings = _MDDInit_MethodBindings_Default().copy()    

    theRdCtxt.pSP( 'initial_method_bindings', someMethodBindings.copy())

    theRdCtxt.pSP( 'method_bindings',         someMethodBindings)


    aModelDDvlPloneTool = theRdCtxt.fGP( 'theModelDDvlPloneTool', None)
    if aModelDDvlPloneTool:

        aBrowsedElement = theRdCtxt.fGP( 'theBrowsedElement', None)
        if aBrowsedElement:


            # ###################################
            """Analyze and resolve custom method bindings explicitely passed in the parameters to the view rendering

            """
            aViewParms = theRdCtxt.fGP( 'theViewParms', {})    
            if aViewParms:

                someCustomMethodBindings = aViewParms.get( 'theCustomMethodBindings', {})

                if someCustomMethodBindings and isinstance( someCustomMethodBindings, dict):

                    for aMethodName in someCustomMethodBindings.keys():

                        someMethodResolutions = someCustomMethodBindings.get( aMethodName, None)
                        if someMethodResolutions:

                            _MDDInit_MethodBindings_Resolve( theRdCtxt, aModelDDvlPloneTool, aBrowsedElement, aMethodName, someMethodResolutions)




            # ###################################
            """Analyze and resolve custom method bindings supplied in the http request

            """
            aRequest = aViewParms.get( 'theRequest', None)
            if aRequest:

                aMethodBindingsString = aRequest.get( 'theCustom', None)
                if aMethodBindingsString:

                    someCustomMethodBindings = fEvalString( aMethodBindingsString)

                    if someCustomMethodBindings and isinstance( someCustomMethodBindings, dict):

                        for aMethodName in someCustomMethodBindings.keys():

                            someMethodResolutions = someCustomMethodBindings.get( aMethodName, None)
                            if someMethodResolutions:

                                _MDDInit_MethodBindings_Resolve( theRdCtxt, aModelDDvlPloneTool, aBrowsedElement, aMethodName, someMethodResolutions)


    return True





def _MDDInit_MethodBindings_Default():
    return dict( [  ( aMethod.__name__[1:], aMethod)  for aMethod in cBindeableMethods_Components])





def _MDDInit_MethodBindings_Names():
    return list( _MDDInit_MethodBindings_Default().keys()) + cBindeableMethods_Extension_Names




def _MDDInit_MethodBindings_Extensions_Names():
    return cBindeableMethods_Extension_Names[:]




# ACV 20091224 Unused
#def _fMC( theMethodBindings, theMethodName, theIsExtension=False):
    #"""Return the callable object bound to the specified name, in the given bindings dictionary.

    #"""  
    #if not theMethodBindings:
    #if theIsExtension:
        #return lambda theRdCtxt: [ False, False,]
        #else:
        #return lambda theRdCtxt: _fLogMethodBindingMissing( theMethodName)

    #unCallable = theMethodBindings.get( theMethodName, None)
    #if unCallable and callable( unCallable):
    #return unCallable

    #if theIsExtension:
    #return lambda theRdCtxt: [ False, False,]

    #return lambda theRdCtxt: _fLogMethodBindingMissing( theMethodName)





def _fLogMethodBindingMissing( theRdCtxt, theMethodName):
    if cLogMissingMethodBindings:
        logging.getLogger( 'ModelDDvlPlone').error( 'MethodBindingMissing %s', theMethodName)
    return [ False, False,]


def _fLogMethodBindingMissing_Lambda( theMethodName):
    return lambda theRdCtxt: _fLogMethodBindingMissing( theRdCtxt, theMethodName)



def  _fMCtx( theIsExtension, theRdCtxt, theMethodName):
    """Return the callable object bound to the specified name, in the given bindings dictionary.

    """  
    if ( not theRdCtxt) or ( not theMethodName):
        return lambda theRdCtxt: [ True, True,]

    if theIsExtension and ( not cPref_Pres_AllowExtensions_Force):

        somePreferences_Presentation = theRdCtxt.fGP( 'PREFS_RES', {})
        anAllowExtensions = somePreferences_Presentation.get( cPref_Pres_AllowExtensions_Name, False)

        if not anAllowExtensions:
            return lambda theRdCtxt: [ True, True,]


    someMethodBindings = theRdCtxt.fGP( 'method_bindings', None)
    if not someMethodBindings:
        if theIsExtension:
            return lambda theRdCtxt: [ True, True,]
        else:
            return _fLogMethodBindingMissing_Lambda( theMethodName)


    unCallable = someMethodBindings.get( theMethodName, None)
    if unCallable and callable( unCallable):
        return unCallable

    if theIsExtension:
        return lambda theRdCtxt: [ True, True,]

    return _fLogMethodBindingMissing_Lambda( theMethodName)













cMDDRenderTabular_SectionsMenu_JavaScript = """
<script type="text/javascript">
    /* MDDRenderTabular_SectionsMenu_JavaScript */

    /*
function MDD_fAbsoluteTop( theElement) {
    if ( !theElement) {
        return 0;
    }

    var unTop = theElement.offsetTop
    var unElement = theElement.offsetParent
    while( unElement) {
        unTop += unElement.offsetTop 
        unElement = unElement.offsetParent
    }
    return unTop
}

function MDD_pMoveMenuTo( theMenuHolder, theTargetElement) {
    var aMenuTop   = MDD_fAbsoluteTop(   theMenuHolder);
    var aTargetTop = MDD_fAbsoluteTop(   theTargetElement);
    var aDisplacement = aTargetTop - aMenuTop;
    theMenuHolder.style.top = "" + aDisplacement + "px";
    return true;
}

*/

</script>
"""            




# #######################################################################
"""Javascript used by menus rendered for the Tabular view.

"""
cAlreadyRendered_MenuAccionesGrupo_JavaScript_PropertyName = 'AlreadyRendered_MenuAccionesGrupo'



cMDDRenderTabular_MenuAccionesGrupo_JavaScript = """
<script type="text/javascript">
    /* MDDRenderTabular_MenuAccionesGrupo_JavaScript */
    function pMDDToggleAllSelections( theIdTabla) {
        var unElementAllSelections = document.getElementById( theIdTabla+'_SelectAll');
        if ( !unElementAllSelections) {
            return false;
        }
        unNewValueForAllSelections = unElementAllSelections.checked;
        for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {

            var unElement = document.getElementById( theIdTabla + '_Select_' +unIdCounter );
            if ( !unElement) {
                break;
            }
            unElement.checked = unNewValueForAllSelections;
        }  
    }



    function pMDDSubmit_varios( theGroupAction, theIdTabla ) {
        var unSomeSelected = false;
        for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {

            var unElementCheckBox = document.getElementById( theIdTabla + '_Select_' +unIdCounter );
            if ( !unElementCheckBox) {
                break;
            }
            var unElementUID = document.getElementById( theIdTabla + '_Select_' +unIdCounter + '_UID' );
            if ( !unElementUID) {
                break;
            }
            if ( unElementCheckBox.checked) {
                unSomeSelected = true;
                unElementUID.disabled = false;
            }
            else {
                unElementUID.disabled = true;
            }
        }
        if (!unSomeSelected) {
            return false;
        }

        var unElementGroupAction = document.getElementById( theIdTabla +'_GroupAction');
        if ( !unElementGroupAction) {
            return false;
        }
        unElementGroupAction.value = theGroupAction;


        var unElementForm = document.getElementById( theIdTabla +'_Form');
        if ( !unElementForm) {
            return false;
        }

        if ( theGroupAction == 'Delete') {
            var unDeleteAction = unElementForm.action;
            if ( unDeleteAction) {
                unDeleteAction = unDeleteAction.replace( '/Tabular', '/MDDEliminarVarios');
                unElementForm.action = unDeleteAction;
            }
        }
        else { // Just in case the user manages to stay in the page, and use the form again
            var unDeleteAction = unElementForm.action;
            if ( unDeleteAction) {
                unDeleteAction = unDeleteAction.replace( '/MDDEliminarVarios', '/Tabular');
                unElementForm.action = unDeleteAction;
            }
         }

        unElementForm.submit();
    }



    function pMDDSubmitRelation_varios( theGroupAction, theIdTabla ) {
        var unSomeSelected = false;
        for( var unIdCounter=0; unIdCounter < 10000; unIdCounter++) {

            var unElementCheckBox = document.getElementById( theIdTabla + '_Select_' +unIdCounter );
            if ( !unElementCheckBox) {
                break;
            }
            var unElementUID = document.getElementById( theIdTabla + '_Select_' +unIdCounter + '_UID' );
            if ( !unElementUID) {
                break;
            }
            if ( unElementCheckBox.checked) {
                unSomeSelected = true;
                unElementUID.disabled = false;
            }
            else {
                unElementUID.disabled = true;
            }
        }
        if (!unSomeSelected) {
            return false;
        }

        var unElementGroupAction = document.getElementById( theIdTabla +'_GroupAction');
        if ( !unElementGroupAction) {
            return false;
        }
        unElementGroupAction.value = theGroupAction;


        var unElementForm = document.getElementById( theIdTabla +'_Form');
        if ( !unElementForm) {
            return false;
        }

        if ( theGroupAction == 'Copy') {
            var unFormAction = unElementForm.action;
            if ( unFormAction) {
                unFormAction = unFormAction.replace( '/Tabular', '/MDDCopyReferences');
                unElementForm.action = unFormAction;
            }
        }
        else {
        if ( theGroupAction == 'Unlink') {
            var unFormAction = unElementForm.action;
            if ( unFormAction) {
                unFormAction = unDeleteAction.replace( '/Tabular', '/MDDUnlinkReferences');
                unElementForm.action = unDeleteAction;
            }
        }
        else { // Just in case the user manages to stay in the page, and use the form again
            var unDeleteAction = unElementForm.action;
            if ( unDeleteAction) {
                unDeleteAction = unDeleteAction.replace( '/MDDEliminarVarios', '/Tabular');
                unElementForm.action = unDeleteAction;
            }
        }}

        unElementForm.submit();
    }


    function fMDDGetConstantValue( theConstantElementName) {
        if (!theConstantElementName) {
            return '';
        }

        var unElemento    = document.getElementById( theConstantElementName);
        if (!unElemento) {
            return '';
        }

        if ( !unElemento.firstChild) {
            return '';
        }

        return unElemento.firstChild.data;
    }

</script>
"""            

