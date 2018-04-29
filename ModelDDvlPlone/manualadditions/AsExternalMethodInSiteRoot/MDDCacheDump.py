# -*- coding: utf-8 -*-
#
# File: MDDCacheDump.py
#
# Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
#
# GNU General Public License (GPL)
#anElementUIDModulus
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


import cgi 

import sys
import traceback

import logging

from StringIO import StringIO





from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_CacheConstants          import *

#from Products.ModelDDvlPloneTool.MDDStringConversions                       import *

from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Cache                   import ModelDDvlPloneTool_Cache
from Products.ModelDDvlPloneTool.ModelDDvlPloneTool_Retrieval               import ModelDDvlPloneTool_Retrieval
from Products.ModelDDvlPloneTool.ModelDDvlPloneToolSupport                  import fMillisecondsNow, fMillisecondsToDateTime, fDateTimeNow





# #######################################################################
""" Utility to escape strings written as HTML.

"""
def fCGIE( theString, quote=1):
    if not theString:
        return theString
    return cgi.escape( theString, quote=quote)
    



# #######################################################
# #######################################################

# #######################################################
# #######################################################

# #######################################################
# #######################################################








def MDDCacheDump( 
    theModelDDvlPloneTool  =None,
    theContextualObject   =None, 
    theCacheName           ='', 
    theAdditionalParams    =None):
    """Exposed as an ExternalMethod.
    
    """
    return _fCacheDump( 
        theModelDDvlPloneTool   =theModelDDvlPloneTool,
        theContextualObject     =theContextualObject, 
        theCacheName            =theCacheName, 
        theAdditionalParams     =theAdditionalParams,
    )
    
    
        

    
def _fCacheDump( 
    theModelDDvlPloneTool  =None,
    theContextualObject    =None, 
    theCacheName           ='', 
    theAdditionalParams    =None):
    """ Return theHTML, with a representation of entries in the named cache.
    
    """
    
    if theCacheName in cCacheNamesForElementsOrUsers:
        return _fCacheDump_ForElements( 
            theModelDDvlPloneTool   =theModelDDvlPloneTool, 
            theContextualObject     =theContextualObject, 
            theCacheName            =theCacheName, 
            theAdditionalParams     =theAdditionalParams
        )
    
    if theCacheName == cCacheName_ElementIndependent:
        return _fCacheDump_ElementIndependent( 
            theModelDDvlPloneTool   =theModelDDvlPloneTool, 
            theContextualObject     =theContextualObject, 
            theCacheName            =theCacheName, 
            theAdditionalParams     =theAdditionalParams
        )
        
    return """<h2><font color="red">Cache Name requested is not known</font></h2>"""

     

 


    
def _fCacheDump_ForElements(
    theModelDDvlPloneTool =None, 
    theContextualObject   =None, 
    theCacheName          =None, 
    theAdditionalParams   =None):
    """ Return theHTML, with a representation of entries in the named cache.
    
    """
    
    unosMillisecondsNow   = fMillisecondsNow()
    
    unOutput = StringIO()


    if not theModelDDvlPloneTool:
        unOutput.write( """
        <h2><font color="red">No parameter theModelDDvlPloneTool</font></h2>
        """)
        return unOutput.getvalue()

    if theContextualObject == None:
        unOutput.write( """
        <h2><font color="red">No parameter theContextualObject</font></h2>
        """)
        return unOutput.getvalue()

        
    someSymbolsAndDefaultsToTranslate = [
        [ 'ModelDDvlPlone', [ 
            [ 'ModelDDvlPlone_Cache_Entry_Action_Flush',      'Flush-',],
            [ 'ModelDDvlPlone_Cache_Project_Label',           'Project-',],
            [ 'ModelDDvlPlone_Cache_Language_Label',          'Language-',],
            [ 'ModelDDvlPlone_Cache_Element_Label',           'Element-',],
            [ 'ModelDDvlPlone_Cache_View_Label',              'View-',],
            [ 'ModelDDvlPlone_Cache_Relation_Label',          'Relation-',],
            [ 'ModelDDvlPlone_Cache_Current_Label',           'Current-',],
            [ 'ModelDDvlPlone_Cache_RoleOrUser_Label',        'Role or User-',],
            [ 'ModelDDvlPlone_Cache_Entry_UniqueId',          'Id-',],
            [ 'ModelDDvlPlone_Cache_Entry_NumProblems',       'Errs-',],
            [ 'ModelDDvlPlone_Cache_Entry_UniqueId_Registry', 'Id.Reg.-',],       
            [ 'ModelDDvlPlone_Cache_Entry_UID_Registry',      'UID.Reg.-',],                       
            [ 'ModelDDvlPlone_Cache_Entry_Valid',             'Valid-',],
            [ 'ModelDDvlPlone_Cache_Entry_Promise',           'Promise-',],
            [ 'ModelDDvlPlone_Cache_Entry_AgeSeconds',        'Age-',],
            [ 'ModelDDvlPlone_Cache_Entry_Memory',            'Memory-',],
            [ 'ModelDDvlPlone_Cache_Entry_Milliseconds',      'ms.-',],
           
        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)

    if not ( theCacheName in cCacheNamesForElementsOrUsers):
        unOutput.write( """
        <h2><font color="red">Named cache must be one of : %s</font></h2>
        """ % ','.join( cCacheNamesForElementsOrUsers),
        )
        return unOutput.getvalue()
  
    
    aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
    aModelDDvlPloneTool_Cache     = ModelDDvlPloneTool_Cache()        

    
    
    unOutput.write( """
    <script type="text/javascript">
    function fMDDConfirmFlush( theCacheEntryId) {
        if ( window.confirm( "Do you want to Flusch cache entry " + theCacheEntryId) && window.confirm( "Do you REALLY want to Flusch cache entry " + theCacheEntryId)) { 
            return true;
        } 
        else { 
            return false;
        }    
    }
    </script>
    """)


    unOutput.write( """
    <table class="listing">
        <thead>
            <th>
                %(ModelDDvlPlone_Cache_Project_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Language_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Element_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_View_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Relation_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Current_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_RoleOrUser_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_Action_Flush)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_UniqueId)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_NumProblems)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_UniqueId_Registry)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_UID_Registry)s
            </th>
            <th> 
                %(ModelDDvlPlone_Cache_Entry_Valid)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_Promise)s
            </th>
            <th align="right">
                %(ModelDDvlPlone_Cache_Entry_AgeSeconds)s
            </th>
            <th align="right">
                %(ModelDDvlPlone_Cache_Entry_Memory)s
            </th>
            <th align="right">
                %(ModelDDvlPlone_Cache_Entry_Milliseconds)s
            </th>
        </thead>
        <tbody>
    """ % {
        'ModelDDvlPlone_Cache_Entry_Action_Flush':    fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Action_Flush']),
        'ModelDDvlPlone_Cache_Project_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Project_Label']),
        'ModelDDvlPlone_Cache_Language_Label':        fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Language_Label']),
        'ModelDDvlPlone_Cache_Element_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Element_Label']),
        'ModelDDvlPlone_Cache_View_Label':            fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_View_Label']),
        'ModelDDvlPlone_Cache_Relation_Label':        fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Relation_Label']),
        'ModelDDvlPlone_Cache_Current_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Current_Label']),
        'ModelDDvlPlone_Cache_RoleOrUser_Label':      fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_RoleOrUser_Label']),
        'ModelDDvlPlone_Cache_Entry_UniqueId':        fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_UniqueId']),
        'ModelDDvlPlone_Cache_Entry_NumProblems':     fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_NumProblems']),
        'ModelDDvlPlone_Cache_Entry_UniqueId_Registry':fCGIE( someTranslations['ModelDDvlPlone_Cache_Entry_UniqueId_Registry']),
        'ModelDDvlPlone_Cache_Entry_UID_Registry':    fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_UID_Registry']),
        'ModelDDvlPlone_Cache_Entry_Valid':           fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Valid']),
        'ModelDDvlPlone_Cache_Entry_Promise':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Promise']),
        'ModelDDvlPlone_Cache_Entry_AgeSeconds':      fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_AgeSeconds']),
        'ModelDDvlPlone_Cache_Entry_Memory':          fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Memory']),
        'ModelDDvlPlone_Cache_Entry_Milliseconds':    fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Milliseconds']),
    })

    aNumColumns = 14
    aBeginMillis = fMillisecondsNow()
        
    try:
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        
        
        # ###########################################################
        """Obtain diagnostics, to be able to highlight entries with problems.
        
        """
        allDiagnostics = aModelDDvlPloneTool_Cache.fCachesDiagnostics_WithinCriticalSection( theModelDDvlPloneTool, theContextualObject, theCacheNames=[ theCacheName,], theAdditionalParams=theAdditionalParams)
        allEntriesWithProblems = allDiagnostics.get( 'allEntriesWithProblems', {})
        
                   
        # ###########################################################
        """Traverse cache control structures to collect UIDs of elements in the cache, to retrieve them in a single search.
        
        """
        someUIDsElementsToRetrieve = set()
        
        someProjectNames = aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,)
        for aProjectName in someProjectNames:
            someTemplatesByLanguageForProject = aModelDDvlPloneTool_Cache.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, aProjectName)                              
            someLanguages =  ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or []
            for aLanguage  in someLanguages:
                someTemplatesByUIDForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
                someUIDs = (someTemplatesByUIDForLanguage and someTemplatesByUIDForLanguage.keys()) or [] 
                
                someUIDsElementsToRetrieve.update( someUIDs)
                
                for anUID in someUIDs:
                    someTemplatesByViewForUID = someTemplatesByUIDForLanguage.get( anUID, {})
                    someViewNames = ( someTemplatesByViewForUID and someTemplatesByViewForUID.keys()) or []
                    for aViewName in someViewNames:
                        someTemplatesByRelationForView = someTemplatesByViewForUID.get( aViewName, {})
                        someRelations = ( someTemplatesByRelationForView and someTemplatesByRelationForView.keys()) or []
                        for aRelationName in someRelations:
                            someTemplatesByRelatedUIDForRelation = someTemplatesByRelationForView.get( aRelationName, {})
                            someRelatedUIDs = ( someTemplatesByRelatedUIDForRelation and someTemplatesByRelatedUIDForRelation.keys()) or []
                            for aRelatedUID in someRelatedUIDs:
                                if not ( aRelatedUID == cNoCurrentElementUID):
                                    someUIDsElementsToRetrieve.add( aRelatedUID)
            
        someElementsByUID = {}
        if someUIDsElementsToRetrieve:
            someElementsByUID =  aModelDDvlPloneTool_Retrieval.fElementosPorUIDs( someUIDsElementsToRetrieve, theContextualObject)
            
        
        

        # ###########################################################
        """Traverse cache control structures to access the cache entries
        
        """
        
        
        # ###########################################################
        """Iterate over Projects
        
        """
        someProjectNames = sorted( aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,))
        aNumProjects = len( someProjectNames)
        
        if not aNumProjects:
            unOutput.write( """
            </body>
            </table
            """)
       
        unasClasesFilas = ('odd','even',)
        aRowIndex = 0
        
        aMillisecondsNow = fMillisecondsNow()
        
        aPortalURL = theModelDDvlPloneTool.fPortalURL()
        
        aContextualObjectURL = theContextualObject.absolute_url()
        
        for aProjectIndex in range( aNumProjects):
            
            # ########################
            """Dump Project
            
            """
            aProjectName = someProjectNames[ aProjectIndex]
            
            aProjectString = """
            <tr class="MDD_Cache_Row_Project %%(row-class)s" >
                <td class="MDD_Cache_Cell_Project" >%(project_name)s</td>
            """ % {
                'aNumProjects':  aNumProjects,
                'aProjectIndex': aProjectIndex + 1,
                'project_name': fCGIE( aProjectName),
            }
            unOutput.write( aProjectString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
            aRowIndex += 1
            
            # ###########################################################
            """Iterate over Languages
            
            """
            
            someTemplatesByLanguageForProject = aModelDDvlPloneTool_Cache.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, aProjectName)                              
            someLanguages = sorted( ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or [])
            aNumLanguages = len( someLanguages)
            

        
            for aLanguageIndex  in range( aNumLanguages):
                
                aLanguage = someLanguages[ aLanguageIndex]
            
                # ########################
                """Dump Language
                
                """
                if aLanguageIndex:
                    unOutput.write( aProjectString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                    aRowIndex += 1
                
                aLanguageString = """
                <td class="MDD_Cache_Cell_Language">%(aLanguage)s</td>
                """ % {
                    'aLanguageIndex': aLanguageIndex + 1,
                    'aNumLanguages':    aNumLanguages,
                    'aLanguage': fCGIE( aLanguage),
                }
                unOutput.write( aLanguageString)
                
                aLanguageString = aProjectString + aLanguageString
                
                # ###########################################################
                """Iterate over Elements UIDs
                
                """
                someTemplatesByUIDForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
                someUIDs = sorted( (someTemplatesByUIDForLanguage and someTemplatesByUIDForLanguage.keys()) or [])
                aNumUIDs = len( someUIDs)
                

                
                for anUIDIndex in range ( aNumUIDs):
                    
                    anUID = someUIDs[ anUIDIndex]
                    
            
                    # ########################
                    """Dump UID
                    
                    """
                    if anUIDIndex:
                        unOutput.write( aLanguageString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                        aRowIndex += 1
                        
                
                       
                    
                    unElement = someElementsByUID.get( anUID, None)
                    unTitle = aModelDDvlPloneTool_Retrieval.fAsUnicode( anUID)
                    unURL   = ''
                    if not ( unElement == None):
                        unTitle = aModelDDvlPloneTool_Retrieval.fAsUnicode( unElement.Title())
                        if len( unTitle) > cMaxLenCacheEntryTitleDisplay:
                            unTitle = '%s...'% unTitle[:cMaxLenCacheEntryTitleDisplay]
                        unURL   = unElement.absolute_url()
                        
                    unUIDString = """
                    <td class="MDD_Cache_Cell_UID">
                        <a href="%(unURL)s" title="%(unTitle)s %(anUID)s" >%(unTitle)s</a>
                    </td>
                    """ % {
                        'unTitle': fCGIE( unTitle),
                        'aNumUIDs':  aNumUIDs,
                        'anUIDIndex': anUIDIndex + 1,
                        'anUID': fCGIE( anUID),
                        'unURL': unURL,
                    }
                    
                    unOutput.write( unUIDString)
                    
                    unUIDString = aLanguageString + unUIDString
                    
                    
                    # ###########################################################
                    """Iterate over Views
                    
                    """
            
                    
                    someTemplatesByViewForUID = someTemplatesByUIDForLanguage.get( anUID, {})
                    someViewNames = sorted( ( someTemplatesByViewForUID and someTemplatesByViewForUID.keys()) or [])
                    unNumViews = len( someViewNames)
                    
                    if not unNumViews:

                        unOutput.write( """
                            <td class="MDD_Cache_Cells_Empty" colspan="%(colspan)d">&ensp;</td>
                        </tr>
                        """ % {
                        'colspan':        aNumColumns - 4,
                        })
                            
                        continue   
                    
                    
                    for aViewIndex in range( unNumViews):
                    
                        aViewName = someViewNames[  aViewIndex]
                        aViewNameToDisplay = aViewName
                        if aViewNameToDisplay.endswith( cViewPostfix_NoHeaderNoFooter):
                            aViewNameToDisplay = aViewNameToDisplay[:0-len( cViewPostfix_NoHeaderNoFooter)]
                        
                        if aViewIndex:
            
                            unOutput.write( unUIDString  % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                            aRowIndex += 1
                             
            
                        # ########################
                        """Dump View
                        
                        """
                        unViewString = ''
                        if unURL:
                            unViewString += """
                                <td class="MDD_Cache_Cell_ViewName">
                                    <a href="%(unURL)s/%(aViewNameToDisplay)s/" title="%(unTitle)s %(aViewNameToDisplay)s %(anUID)s" >%(aViewNameToDisplay)s</a>
                                </td>
                            """ % {
                                'unTitle':    fCGIE( unTitle),
                                'unURL':      unURL,
                                'unNumViews': unNumViews,
                                'aViewIndex': aViewIndex + 1,
                                'aViewName':  fCGIE( aViewName),
                                'aViewNameToDisplay':  fCGIE( aViewNameToDisplay),
                                'anUID': fCGIE( anUID),
                            }
                        else:
                            unViewString += """
                                <td class="MDD_Cache_Cell_ViewName">%(aViewNameToDisplay)s</td>
                            """ % {
                                'unNumViews': unNumViews,
                                'aViewIndex': aViewIndex + 1,
                                'aViewName':  fCGIE( aViewName),
                                'aViewNameToDisplay':  fCGIE( aViewNameToDisplay),                                    
                            }

                        unOutput.write( unViewString)
                              
                        unViewString = unUIDString + unViewString
                        
                        
                            
                        # ###########################################################
                        """Iterate over Relations
                        
                        """
                        someTemplatesByRelationForView = someTemplatesByViewForUID.get( aViewName, {})
                        someRelations = sorted( ( someTemplatesByRelationForView and someTemplatesByRelationForView.keys()) or [])
                        aNumRelations = len( someRelations)
                        
                         
                        if not aNumRelations:

                            
                            unOutput.write( """
                                <td class="MDD_Cache_Cells_Empty" colspan="%(colspan)d">&ensp;</td>
                            </tr>
                            """ % {
                            'colspan':                            aNumColumns - 5,
                            })
                                
                            continue   
                        
                        for aRelationIndex in range( aNumRelations):
                        
                            aRelationName = someRelations[  aRelationIndex]
                     
                            if aRelationIndex:

                                unOutput.write( unViewString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                                aRowIndex += 1
                            
                            
            
                            # ########################
                            """Dump Relation
                            
                            """
                            unRelationString = """
                                <td class="MDD_Cache_Cell_RelationName">%(aRelationName)s</td>
                            """ % {
                                'aNumRelations':                      aNumRelations,
                                'aRelationIndex': aRelationIndex + 1,
                                'aRelationName': fCGIE( aRelationName),
                            }

                            unOutput.write( unRelationString)
                          
                            unRelationString = unViewString + unRelationString
                            
                              
                            # ###########################################################
                            """Iterate over Related Element UIDs
                            
                            """
                            someTemplatesByRelatedUIDForRelation = someTemplatesByRelationForView.get( aRelationName, {})
                            someRelatedUIDs = sorted( ( someTemplatesByRelatedUIDForRelation and someTemplatesByRelatedUIDForRelation.keys()) or [])
                            aNumRelatedUIDs = len( someRelatedUIDs)
                            
                            
                            if not aNumRelatedUIDs:
                           
                                unOutput.write( """
                                    <td class="MDD_Cache_Cells_Empty" colspan="%(colspan)d">&ensp;</td>
                                </tr>
                                """ % {
                                'colspan':                            aNumColumns -6,
                                })
                                    
                                continue   
                            
                            for aRelatedUIDsIndex in range( aNumRelatedUIDs):
                            
                                aRelatedUID = someRelatedUIDs[  aRelatedUIDsIndex]
                         
                                if aRelatedUIDsIndex :

                                    unOutput.write( unRelationString  % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                                    aRowIndex += 1
                                
                                
                
                                # ########################
                                """Dump RelatedUID
                                
                                """
                                unRelatedString = """
                                    <td class="MDD_Cache_Cell_RelatedUID">%(aRelatedUID)s</td>
                                """ % {
                                    'aRelatedUIDIndex': aRelatedUIDsIndex + 1,
                                    'aRelatedUID': fCGIE( aRelatedUID),
                                    'aNumRelatedUIDs':                      aNumRelatedUIDs,
                                }
                                unOutput.write( unRelatedString)

                                unRelatedString = unRelationString + unRelatedString
                              
                                                                       
                            
                            
                         
                            
                                # ###########################################################
                                """Iterate over RoleOrUsers
                                
                                """
                                someTemplatesByRoleOrUserForRelatedUID = someTemplatesByRelatedUIDForRelation.get( aRelatedUID, {})
                                someRoleOrUsers = sorted( ( someTemplatesByRoleOrUserForRelatedUID and someTemplatesByRoleOrUserForRelatedUID.keys()) or [])
                                aNumRolesOrUsers = len( someRoleOrUsers)
                                
                                
                               
                                if not aNumRolesOrUsers:
                                    
                                    unOutput.write( """
                                        <td class="MDD_Cache_Cells_Empty" colspan="%(colspan)d">&ensp;</td>
                                    </tr>
                                    """ % {
                                    'colspan':                            aNumColumns - 7,
                                    })
                                        
                                    continue   
                                
                                for aRoleOrUserIndex in range( aNumRolesOrUsers):
                                
                                    aRoleOrUserName = someRoleOrUsers[  aRoleOrUserIndex]
                             
                                    if aRoleOrUserIndex:
                         
                                        unOutput.write( unRelatedString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                                        aRowIndex += 1
                                    
                                    
                    
                                    # ########################
                                    """Dump RoleOrUser
                                    
                                    """
                                    unRoleOrUserString = """
                                        <td class="MDD_Cache_Cell_RoleOrUserName">%(aRoleOrUserName)s</td>
                                    """ % {
                                        'aNumRolesOrUsers': aNumRolesOrUsers,
                                        'aRoleOrUserIndex': aRoleOrUserIndex + 1,
                                        'aRoleOrUserName': fCGIE( aRoleOrUserName),
                                    }
                                    
                                    unOutput.write(  unRoleOrUserString)
                                    
                                    
                                    
                                    
                                    # ########################
                                    """Dump CacheEntry
                                    
                                    """
                                    aCacheEntry = someTemplatesByRoleOrUserForRelatedUID.get( aRoleOrUserName, None)
                                    if not aCacheEntry:
                                        unOutput.write( """
                                            <td class="MDD_Cache_Cells_Empty" colspan="%(colspan)d">&ensp;</td>
                                        </tr>
                                        """ % {
                                        'colspan':                            aNumColumns - 8,
                                        })
                                    else:
                                        
                                        unEntryByUniqueId = aModelDDvlPloneTool_Cache._fGetCachedEntryById( theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUniqueId)
                                        unRegistryByUniqueId = (( unEntryByUniqueId and ( unEntryByUniqueId == aCacheEntry)) and 'OK') or (( unEntryByUniqueId and not ( unEntryByUniqueId == aCacheEntry)) and 'ERR') or 'NO'
                                        
                                        unasEntriesByUID = aModelDDvlPloneTool_Cache._fGetCachedEntriesByUID(  theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUID)
                                        unRegistryByUID = ( ( aCacheEntry in unasEntriesByUID) and 'OK') or 'ERR'
                                        
                                        aCacheEntryProblems = allEntriesWithProblems.get( aCacheEntry, [])
                                        aNumCacheEntryProblems = len( aCacheEntryProblems)
                                        aNumCacheEntryProblemsBGColor = ( aNumCacheEntryProblems and 'bgcolor="Red"') or ''
                                         
                                        unOutput.write( """
                                            <td  align="center"  class="MDD_Cache_Cell_Entry_Flush">
                                                <a onclick="return fMDDConfirmFlush( '%(aUniqueId)s', ' from Memory')"
                                                   href="%(aFlushFromMemoryHref)s" name="Flush Cache Entry  %(aUniqueId)s from Memory">
                                                    <img alt="Flush Cache Entry %(aUniqueId)s from Memory" title="Flush Cache Entry %(aUniqueId)s from Memory" id="icon-flush-memory" 
                                                    src="%(aPortalURL)s/mddflushmemory.gif"/>
                                                </a>
                                                &emsp;
                                                <a onclick="return fMDDConfirmFlush( '%(aUniqueId)s', ' from Memory and Disk')"
                                                    href="%(aFlushFromDiskHref)s" name="Flush Cache Entry %(aUniqueId)s from Disk">
                                                    <img alt="Flush Cache Entry %(aUniqueId)s from Disk" title="Flush Cache Entry %(aUniqueId)s from Disk" id="icon-flush-disk" 
                                                    src="%(aPortalURL)s/mddflushdisk.gif"/>
                                                </a>
                                            </td>
                                            <td  align="right"  class="MDD_Cache_Cell_Entry_UniqueId">%(aUniqueId)d</td>
                                            <td  align="right" %(aNumProblemsBGColor)s class="MDD_Cache_Cell_Entry_NumProblems">%(aNumProblems)d</td>
                                            <td align="right" class="MDD_Cache_Cell_Entry_UniqueId_Registry">%(unRegistryByUniqueId)s</td>
                                            <td align="right" class="MDD_Cache_Cell_Entry_UID_Registry">%(unRegistryByUID)s</td>
                                            <td class="MDD_Cache_Cell_Entry_Valid">%(aValid)s</td>
                                            <td class="MDD_Cache_Cell_Entry_Promise">%(aPromise)s</td>
                                            <td align="right" class="MDD_Cache_Cell_Entry_AgeSeconds">%(unosSeconds)d</td>
                                            <td align="right" class="MDD_Cache_Cell_Entry_Memory">
                                                <a href="%(aHTMLHref)s" name="HTML" >
                                                    %(aMemory)d
                                                </a>
                                            </td>
                                            <td align="right" class="MDD_Cache_Cell_Entry_Time">%(aMilliseconds)d</td>
                                        </tr>
                                        """ % {
                                            'aFlushFromMemoryHref': '%s/MDDFlushCachedTemplateByUniqueId/?theCacheEntryUniqueId=%s&theFlushCacheCode=%d&theCacheName=%s' % ( aContextualObjectURL, aCacheEntry.vUniqueId, aMillisecondsNow, theCacheName,),
                                            'aFlushFromDiskHref': '%s/MDDFlushCachedTemplateByUniqueId/?theCacheEntryUniqueId=%s&theFlushCacheCode=%d&theFlushDiskCache=on&theCacheName=%s' % ( aContextualObjectURL, aCacheEntry.vUniqueId, aMillisecondsNow, theCacheName,),
                                            'aHTMLHref':  '%s/MDDCachedHTML/?theCacheEntryUniqueId=%s' % ( aContextualObjectURL, aCacheEntry.vUniqueId),
                                            'aPortalURL': aPortalURL,
                                            'aUniqueId': aCacheEntry.vUniqueId or 0,
                                            'aNumProblems': aNumCacheEntryProblems,
                                            'aNumProblemsBGColor': aNumCacheEntryProblemsBGColor,
                                            'aValid':    (aCacheEntry.vValid and 'Y') or 'N',
                                            'aPromise':  (( aCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel) and 'OK') or ( aCacheEntry.vPromise and '...') or '?',
                                            'unosSeconds':  int( ( unosMillisecondsNow - aCacheEntry.vDateMillis) / 1000),
                                            'aMemory':   ( aCacheEntry.vHTML and len( aCacheEntry.vHTML) ) or 0,
                                            'aMilliseconds':  aCacheEntry.vMilliseconds  or 0,
                                            'unRegistryByUniqueId': unRegistryByUniqueId,
                                            'unRegistryByUID':       unRegistryByUID,
                                        })
                                        
                                           

        
    finally:
        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                        
                                           
                            
        unOutput.write( """
            </tbody>
            </table>
        """)
                 
        unOutputString = unOutput.getvalue()
        return unOutputString
            



 
     
     
    

def _fCacheDump_ElementIndependent( 
    theModelDDvlPloneTool =None, 
    theContextualObject   =None, 
    theCacheName          =None, 
    theAdditionalParams   =None):
    """ Return theHTML, with a representation of entries in the named cache.
    
    """
    
    unosMillisecondsNow   = fMillisecondsNow()
    
    unOutput = StringIO()


    if not theModelDDvlPloneTool:
        unOutput.write( """
        <h2><font color="red">No parameter theModelDDvlPloneTool</font></h2>
        """)
        return unOutput.getvalue()

    if theContextualObject == None:
        unOutput.write( """
        <h2><font color="red">No parameter theContextualObject</font></h2>
        """)
        return unOutput.getvalue()

        
    someSymbolsAndDefaultsToTranslate = [
        [ 'ModelDDvlPlone', [ 
            [ 'ModelDDvlPlone_Cache_Entry_Action_Flush',      'Flush-',],
            [ 'ModelDDvlPlone_Cache_Project_Label',           'Project-',],
            [ 'ModelDDvlPlone_Cache_Language_Label',          'Language-',],
            [ 'ModelDDvlPlone_Cache_View_Label',              'View-',],
            [ 'ModelDDvlPlone_Cache_Relation_Label',          'Relation-',],
            [ 'ModelDDvlPlone_Cache_Current_Label',           'Current-',],
            [ 'ModelDDvlPlone_Cache_RoleOrUser_Label',        'Role or User-',],
            [ 'ModelDDvlPlone_Cache_Entry_UniqueId',          'Id-',],
            [ 'ModelDDvlPlone_Cache_Entry_NumProblems',       'Errs-',],
            [ 'ModelDDvlPlone_Cache_Entry_UniqueId_Registry', 'Id.Reg.-',],       
            [ 'ModelDDvlPlone_Cache_Entry_UID_Registry',      'UID.Reg.-',],                       
            [ 'ModelDDvlPlone_Cache_Entry_Valid',             'Valid-',],
            [ 'ModelDDvlPlone_Cache_Entry_Promise',           'Promise-',],
            [ 'ModelDDvlPlone_Cache_Entry_AgeSeconds',        'Age-',],
            [ 'ModelDDvlPlone_Cache_Entry_Memory',            'Memory-',],
            [ 'ModelDDvlPlone_Cache_Entry_Milliseconds',      'ms.-',],
           
        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)

    if not ( theCacheName == cCacheName_ElementIndependent):
        unOutput.write( """
        <h2><font color="red">Named cache must be %s</font></h2>
        """ % cCacheName_ElementIndependent,
        )
        return unOutput.getvalue()
  
    
    
    aModelDDvlPloneTool_Retrieval = ModelDDvlPloneTool_Retrieval()
    aModelDDvlPloneTool_Cache     = ModelDDvlPloneTool_Cache()
    
    unOutput.write( """
    <script type="text/javascript">
    function fMDDConfirmFlush( theCacheEntryId, thePostfix) {
        if ( window.confirm( "Do you want to Flusch cache entry " + theCacheEntryId + thePostfix) && window.confirm( "Do you REALLY want to Flusch cache entry " + theCacheEntryId + thePostfix)) { 
            return true;
        } 
        else { 
            return false;
        }    
    }
    </script>
    """)

    
    unOutput.write( """
    <table class="listing">
        <thead>
            <th>
                %(ModelDDvlPlone_Cache_Project_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Language_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_View_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_Action_Flush)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_UniqueId)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_NumProblems)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_UniqueId_Registry)s
            </th>
            <th> 
                %(ModelDDvlPlone_Cache_Entry_Valid)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Entry_Promise)s
            </th>
            <th align="right">
                %(ModelDDvlPlone_Cache_Entry_AgeSeconds)s
            </th>
            <th align="right">
                %(ModelDDvlPlone_Cache_Entry_Memory)s
            </th>
            <th align="right">
                %(ModelDDvlPlone_Cache_Entry_Milliseconds)s
            </th>
        </thead>
        <tbody>
    """ % {
        'ModelDDvlPlone_Cache_Entry_Action_Flush':    fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Action_Flush']),
        'ModelDDvlPlone_Cache_Project_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Project_Label']),
        'ModelDDvlPlone_Cache_Language_Label':        fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Language_Label']),
        'ModelDDvlPlone_Cache_View_Label':            fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_View_Label']),
        'ModelDDvlPlone_Cache_Entry_UniqueId':        fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_UniqueId']),
        'ModelDDvlPlone_Cache_Entry_NumProblems':     fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_NumProblems']),
        'ModelDDvlPlone_Cache_Entry_UniqueId_Registry':fCGIE( someTranslations['ModelDDvlPlone_Cache_Entry_UniqueId_Registry']),
        'ModelDDvlPlone_Cache_Entry_Valid':           fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Valid']),
        'ModelDDvlPlone_Cache_Entry_Promise':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Promise']),
        'ModelDDvlPlone_Cache_Entry_AgeSeconds':      fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_AgeSeconds']),
        'ModelDDvlPlone_Cache_Entry_Memory':          fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Memory']),
        'ModelDDvlPlone_Cache_Entry_Milliseconds':    fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Milliseconds']),
    })

    aNumColumns = 11
    aBeginMillis = fMillisecondsNow()
        
    try:
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
         
        
    
        # ###########################################################
        """Obtain diagnostics, to be able to highlight entries with problems.
        
        """
        allDiagnostics = aModelDDvlPloneTool_Cache.fCachesDiagnostics_WithinCriticalSection( theModelDDvlPloneTool, theContextualObject, theCacheNames=[ theCacheName,], theAdditionalParams=theAdditionalParams)
        allEntriesWithProblems = allDiagnostics.get( 'allEntriesWithProblems', {})
        
        

        # ###########################################################
        """Traverse cache control structures to access the cache entries
        
        """
        
        
        # ###########################################################
        """Iterate over Projects
        
        """
        someProjectNames = sorted( aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,))
        aNumProjects = len( someProjectNames)
        
        if not aNumProjects:
            unOutput.write( """
            </body>
            </table
            """)
       
        unasClasesFilas = ('odd','even',)
        aRowIndex = 0
                    
        aMillisecondsNow = fMillisecondsNow()
        
        aPortalURL = theModelDDvlPloneTool.fPortalURL()
        
        aContextualObjectURL = theContextualObject.absolute_url()
        
        for aProjectIndex in range( aNumProjects):
            
            # ########################
            """Dump Project
            
            """
            aProjectName = someProjectNames[ aProjectIndex]
            
            aProjectString = """
            <tr class="MDD_Cache_Row_Project %%(row-class)s">
                <td class="MDD_Cache_Cell_Project" >%(project_name)s</td>
            """ % {
                'aNumProjects':  aNumProjects,
                'aProjectIndex': aProjectIndex + 1,
                'project_name': fCGIE( aProjectName),
            }
            unOutput.write( aProjectString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
            aRowIndex += 1
            
            # ###########################################################
            """Iterate over Languages
            
            """
            
            someTemplatesByLanguageForProject = aModelDDvlPloneTool_Cache.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, aProjectName)                              
            someLanguages = sorted( ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or [])
            aNumLanguages = len( someLanguages)
            

        
            for aLanguageIndex  in range( aNumLanguages):
                
                aLanguage = someLanguages[ aLanguageIndex]
            
                # ########################
                """Dump Language
                
                """
                if aLanguageIndex:
                    unOutput.write( aProjectString)
                
                aLanguageString = """
                <td class="MDD_Cache_Cell_Language">%(aLanguage)s</td>
                """ % {
                    'aLanguageIndex': aLanguageIndex + 1,
                    'aNumLanguages':    aNumLanguages,
                    'aLanguage': fCGIE( aLanguage),
                }
                unOutput.write( aLanguageString)
                
                aLanguageString = aProjectString + aLanguageString
                
                    
                
                
                # ###########################################################
                """Iterate over Views
                
                """
                someTemplatesByViewForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
                someViewNames = sorted( ( someTemplatesByViewForLanguage and someTemplatesByViewForLanguage.keys()) or [])
                unNumViews = len( someViewNames)
                
                if not unNumViews:

                    unOutput.write( """
                        <td class="MDD_Cache_Cells_Empty" colspan="%(colspan)d">&ensp;</td>
                    </tr>
                    """ % {
                    'colspan':        aNumColumns - 3,
                    })
                        
                    continue   
                
                
                for aViewIndex in range( unNumViews):
                
                    aViewName = someViewNames[  aViewIndex]
                    aViewNameToDisplay = aViewName
                    if aViewNameToDisplay.endswith( cViewPostfix_NoHeaderNoFooter):
                        aViewNameToDisplay = aViewNameToDisplay[:0-len( cViewPostfix_NoHeaderNoFooter)]
                    
                    if aViewIndex > 1:
        
                        unOutput.write( aLanguageString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                        aRowIndex += 1
                         
        
                    # ########################
                    """Dump View
                    
                    """
                    unViewString = """
                        <td class="MDD_Cache_Cell_ViewName">%(aViewNameToDisplay)s</td>
                    """ % {
                        'unNumViews': unNumViews,
                        'aViewIndex': aViewIndex + 1,
                        'aViewName':  fCGIE( aViewName),
                        'aViewNameToDisplay':  fCGIE( aViewNameToDisplay),                                    
                    }

                    unOutput.write( unViewString)
                                                                              
                    # ########################
                    """Dump CacheEntry
                    
                    """
                    aCacheEntry = someTemplatesByViewForLanguage.get( aViewName, None)
                    if not aCacheEntry:
                        unOutput.write( """
                            <td class="MDD_Cache_Cells_Empty" colspan="%(colspan)d">&ensp;</td>
                        </tr>
                        """ % {
                        'colspan':                            aNumColumns - 4,
                        })
                    else:
                        
                        unEntryByUniqueId = aModelDDvlPloneTool_Cache._fGetCachedEntryById( theModelDDvlPloneTool, theContextualObject, aCacheEntry.vUniqueId)
                        unRegistryByUniqueId = (( unEntryByUniqueId and ( unEntryByUniqueId == aCacheEntry)) and 'OK') or (( unEntryByUniqueId and not ( unEntryByUniqueId == aCacheEntry)) and 'ERR') or 'NO'
                        
                        aCacheEntryProblems = allEntriesWithProblems.get( aCacheEntry, [])
                        aNumCacheEntryProblems = len( aCacheEntryProblems)
                        aNumCacheEntryProblemsBGColor = ( aNumCacheEntryProblems and 'bgcolor="Red"') or ''
                         
                        unOutput.write( """
                            <td  align="center"  class="MDD_Cache_Cell_Entry_Flush">
                                <a onclick="return fMDDConfirmFlush( '%(aUniqueId)s', ' from Memory')"
                                   href="%(aFlushFromMemoryHref)s" name="Flush Cache Entry  %(aUniqueId)s from Memory">
                                    <img alt="Flush Cache Entry %(aUniqueId)s from Memory" title="Flush Cache Entry %(aUniqueId)s from Memory" id="icon-flush-memory" 
                                    src="%(aPortalURL)s/mddflushmemory.gif"/>
                                </a>
                                &emsp;
                                <a onclick="return fMDDConfirmFlush( '%(aUniqueId)s', ' from Memory and Disk')"
                                   href="%(aFlushFromDiskHref)s" name="Flush Cache Entry %(aUniqueId)s from Disk">
                                    <img alt="Flush Cache Entry %(aUniqueId)s from Disk" title="Flush Cache Entry %(aUniqueId)s from Disk" id="icon-flush-disk" 
                                    src="%(aPortalURL)s/mddflushdisk.gif"/>
                                </a>
                            </td>
                             <td  align="right"  class="MDD_Cache_Cell_Entry_UniqueId">%(aUniqueId)d</td>
                            <td  align="right" %(aNumProblemsBGColor)s class="MDD_Cache_Cell_Entry_NumProblems">%(aNumProblems)d</td>
                            <td align="right" class="MDD_Cache_Cell_Entry_UniqueId_Registry">%(unRegistryByUniqueId)s</td>
                            <td class="MDD_Cache_Cell_Entry_Valid">%(aValid)s</td>
                            <td class="MDD_Cache_Cell_Entry_Promise">%(aPromise)s</td>
                            <td align="right" class="MDD_Cache_Cell_Entry_AgeSeconds">%(unosSeconds)d</td>
                            <td align="right" class="MDD_Cache_Cell_Entry_Memory">
                                <a href="%(aHTMLHref)s" name="HTML" >
                                    %(aMemory)d
                                </a>
                            </td>
                            <td align="right" class="MDD_Cache_Cell_Entry_Time">%(aMilliseconds)d</td>
                        </tr>
                        """ % {
                            'aFlushFromMemoryHref': '%s/MDDFlushCachedTemplateByUniqueId/?theCacheEntryUniqueId=%s&theFlushCacheCode=%d&theCacheName=%s' % ( aContextualObjectURL, aCacheEntry.vUniqueId, aMillisecondsNow, theCacheName,),
                            'aFlushFromDiskHref': '%s/MDDFlushCachedTemplateByUniqueId/?theCacheEntryUniqueId=%s&theFlushCacheCode=%d&theFlushDiskCache=on&theCacheName=%s' % ( aContextualObjectURL, aCacheEntry.vUniqueId, aMillisecondsNow, theCacheName,),
                            'aHTMLHref':  '%s/MDDCachedHTML/?theCacheEntryUniqueId=%s' % ( aContextualObjectURL, aCacheEntry.vUniqueId),
                            'aPortalURL': aPortalURL,
                            'aUniqueId': aCacheEntry.vUniqueId or 0,
                            'aNumProblems': aNumCacheEntryProblems,
                            'aNumProblemsBGColor': aNumCacheEntryProblemsBGColor,
                            'aValid':    (aCacheEntry.vValid and 'Y') or 'N',
                            'aPromise':  (( aCacheEntry.vPromise == cCacheEntry_PromiseFulfilled_Sentinel) and 'OK') or ( aCacheEntry.vPromise and '...') or '?',
                            'unosSeconds':  int( ( unosMillisecondsNow - aCacheEntry.vDateMillis) / 1000),
                            'aMemory':   ( aCacheEntry.vHTML and len( aCacheEntry.vHTML) ) or 0,
                            'aMilliseconds':  aCacheEntry.vMilliseconds  or 0,
                            'unRegistryByUniqueId': unRegistryByUniqueId,
                        })
                        
                                           

        
    finally:
        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                        
                                           
                            
        unOutput.write( """
            </tbody>
            </table>
        """)
                 
        unOutputString = unOutput.getvalue()
        return unOutputString
            

        