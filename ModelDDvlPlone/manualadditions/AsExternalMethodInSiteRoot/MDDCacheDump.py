# -*- coding: utf-8 -*-
#
# File: MDDCacheDump.py
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


cMDDCacheDump_NumEntries_Default = 100
cMDDCacheDump_NumEntries_Maximum = 5000


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

     
 


    
def _pCacheDump_ForElements_QueryForm(
    theModelDDvlPloneTool =None, 
    theContextualObject   =None, 
    theCacheName          =None, 
    theOutput             =None,
    theAdditionalParams   =None):
    """Render into theOutput a form to query and paginate on entries in the named cache.
    
    """

    if theOutput == None:
        return None

    if theModelDDvlPloneTool == None:
        theOutput.write( """
        <h2><font color="red">Query and Paginate form: No parameter theModelDDvlPloneTool</font></h2>
        """)
        return None

    if theContextualObject == None:
        theOutput.write( """
        <h2><font color="red">Query and Paginate form: No parameter theContextualObject</font></h2>
        """)
        return None
    
    if not ( theCacheName in cCacheNamesForElementsOrUsers):
        theOutput.write( """
        <h2><font color="red">Query and Paginate form: Named cache must be one of : %s</font></h2>
        """ % ','.join( cCacheNamesForElementsOrUsers),
        )
        return None
  
    
    
    aProjectName = theAdditionalParams.get( 'theProjectName', '')
    aLanguage    = theAdditionalParams.get( 'theLanguage', '')
    
        
    
    aFirstEntryIndex = theAdditionalParams.get( 'theFirstEntryIndex', 0)
    if not isinstance( aFirstEntryIndex, int):
        aFirstEntryIndex = 0
        try:
            aFirstEntryIndex = int( aFirstEntryIndex)
        except:
            None
    if ( not aFirstEntryIndex) or ( aFirstEntryIndex < 1):
        aFirstEntryIndex = 1
        
    
    
    aNumEntries = theAdditionalParams.get( 'theNumEntries', 0)
    if not isinstance( aNumEntries, int):
        aNumEntries = 0
        try:
            aNumEntries = int( aNumEntries)
        except:
            None
    if ( not aNumEntries) or ( aNumEntries < 1):
        aNumEntries = cMDDCacheDump_NumEntries_Default
    if aNumEntries > cMDDCacheDump_NumEntries_Maximum:
        aNumEntries = cMDDCacheDump_NumEntries_Maximum
        
    

         
    someSymbolsAndDefaultsToTranslate = [
        [ 'ModelDDvlPlone', [ 
            [ 'ModelDDvlPlone_Cache_Query_FirstEntryIndex',   'First Entry index-',],
            [ 'ModelDDvlPlone_Cache_Query_NumEntries',        'Number of entries-',],
            [ 'ModelDDvlPlone_Cache_Query_ProjectName',       'Project name-',],
            [ 'ModelDDvlPlone_Cache_Query_Language',          'Language-',],
            
        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)
        
        
    theOutput.write( """
    <br/>
    <form name="MDDCacheQueryAndPagingForm" id="cidMDDCacheQueryAndPagingForm"  method="post" 
        action="%(theElementURL)s/MDDInspectCache" >
        
        <input type="hidden" name="theCacheName" id="cid_theCacheName_input_hidden" value="%(theCacheName)s" />
        
        <table class="listing" id="cidMDDCache_QueryForm_table">
            <thead>
                <tr>
                    <th class="nosort"/>
                    <th class="nosort"/>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <font size="1"><strong>%(projectName_label)s</strong></font>
                    </td>
                    <td>
                        <input type="text" style="font-size: 9pt;" size="32" maxlength="256" name="theProjectName" id="cid_theProjectName_input" 
                            value="%(theProjectName)s" />
                    </td>
                </tr>
                <tr>
                    <td>
                        <font size="1"><strong>%(language_label)s</strong></font>
                    </td>
                    <td>
                        <input type="text" style="font-size: 9pt;" size="16" maxlength="256" name="theLanguage" id="cid_theLanguage_input" 
                            value="%(theLanguage)s" />
                    </td>
                </tr>
                <tr>
                    <td>
                        <font size="1"><strong>%(firstEntry_label)s</strong></font>
                    </td>
                    <td>
                        <input type="text" style="font-size: 9pt;" size="8" maxlength="8" name="theFirstEntryIndex" id="cid_theFirstEntryIndex_input" 
                            value="%(theFirstEntryIndex)d" />
                    </td>
                </tr>
                <tr>
                    <td>
                        <font size="1"><strong>%(numEntries_label)s</strong></font>
                    </td>
                    <td>
                        <input type="text" style="font-size: 9pt;" size="8" maxlength="8" name="theNumEntries" id="cid_theNumEntries_input" 
                            value="%(theNumEntries)d" />
                    </td>
                </tr>
            </tbody>
        </table>
        
    </form>
    <br/>
    """ % {
        'projectName_label':  someTranslations[ 'ModelDDvlPlone_Cache_Query_ProjectName'],
        'language_label':     someTranslations[ 'ModelDDvlPlone_Cache_Query_Language'],
        'firstEntry_label':   someTranslations[ 'ModelDDvlPlone_Cache_Query_FirstEntryIndex'],
        'numEntries_label':   someTranslations[ 'ModelDDvlPlone_Cache_Query_NumEntries'],
        'theCacheName' :      theCacheName,
        'theElementURL':      theContextualObject.absolute_url(),
        'theProjectName':     aProjectName,
        'theLanguage':        aLanguage,
        'theFirstEntryIndex': aFirstEntryIndex,
        'theNumEntries':      aNumEntries,
    })
    
    return None










    
def _fCacheDump_ForElements_ProjectChooser(
    theModelDDvlPloneTool =None, 
    theContextualObject   =None, 
    theCacheName          =None, 
    theOutput             =None,
    theAdditionalParams   =None):
    """ Return theHTML, with a list of projects in the named cache.
    
    """
    
    if theOutput == None:
        return None    

    if theModelDDvlPloneTool == None:
        theOutput.write( """
        <h2><font color="red">No parameter theModelDDvlPloneTool in _fCacheDump_ForElements_ProjectChooser</font></h2>
        """)
        return None

    if theContextualObject == None:
        theOutput.write( """
        <h2><font color="red">No parameter theContextualObject in _fCacheDump_ForElements_ProjectChooser</font></h2>
        """)
        return None

    if not ( theCacheName in cCacheNamesForElementsOrUsers):
        theOutput.write( """
        <h2><font color="red">Named cache must be one of : %s in _fCacheDump_ForElements_ProjectChooser</font></h2>
        """ % ','.join( cCacheNamesForElementsOrUsers),
        )
        return None
  
   
    
    
    someSymbolsAndDefaultsToTranslate = [
        [ 'ModelDDvlPlone', [ 
            [ 'ModelDDvlPlone_Cache_ChooseAProject_Title',     'Choose one of the Projects-',],
            [ 'ModelDDvlPlone_Cache_Projects_Label',          'Projects-',],

        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)

   
        
    aModelDDvlPloneTool_Cache     = theModelDDvlPloneTool.fModelDDvlPloneTool_Cache(     theContextualObject)        

    

    theOutput.write( """
    <br/>
    <h3>
    %(ModelDDvlPlone_Cache_ChooseAProject_Title)s
    </h3>
    <table class="listing" id="cidMDDCache_ProjectChooser_table" >
        <thead>
            <th>
                %(ModelDDvlPlone_Cache_Projects_Label)s
            </th>
        </thead>
        <tbody>
    """ % {
        'ModelDDvlPlone_Cache_ChooseAProject_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_ChooseAProject_Title']),
        'ModelDDvlPlone_Cache_Projects_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Projects_Label']),
    })

    
    aContextualObjectURL = theContextualObject.absolute_url()
    
    
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
        """Traverse cache control structures to collect UIDs of elements in the cache, to retrieve them in a single search.
        
        """
        
        unasClasesFilas = ('odd','even',)
        
        someProjectNames = aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,)
        for aProjectIndex in range( len( someProjectNames)):
            
            aProjectName = someProjectNames[ aProjectIndex]
            
            if aProjectName:
                theOutput.write( """
                <tr class="MDD_Cache_Row_Project %%(row-class)s" >
                    <td class="MDD_Cache_Cell_Project" >
                        <a id="cidMDDCache_ChooseProject_%(aProjectName)s" href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s">
                            %(aProjectName)s
                        </a>
                    </td>
                </tr>
                """ % {
                    'theCacheName': fCGIE( theCacheName),
                    'aURL':         aContextualObjectURL,
                    'aProjectName': fCGIE( aProjectName),
                    'row-class':    unasClasesFilas[ aProjectIndex % 2],
                })
                
        
    finally:
        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                        
                                 
    theOutput.write( """
        </tbody>
    </table>
    <br/>
    """ )

    return None








    
def _fCacheDump_ForElements_LanguageChooser(
    theModelDDvlPloneTool =None, 
    theContextualObject   =None, 
    theCacheName          =None, 
    theOutput             =None,
    theAdditionalParams   =None):
    """ Return theHTML, with a list of languages in the selected project in the named cache.
    
    """
    
    if theOutput == None:
        return None    

    if theModelDDvlPloneTool == None:
        theOutput.write( """
        <h2><font color="red">No parameter theModelDDvlPloneTool in _fCacheDump_ForElements_LanguageChooser</font></h2>
        """)
        return None

    if theContextualObject == None:
        theOutput.write( """
        <h2><font color="red">No parameter theContextualObject in _fCacheDump_ForElements_LanguageChooser</font></h2>
        """)
        return None

    if not ( theCacheName in cCacheNamesForElementsOrUsers):
        theOutput.write( """
        <h2><font color="red">Named cache must be one of : %s in _fCacheDump_ForElements_LanguageChooser</font></h2>
        """ % ','.join( cCacheNamesForElementsOrUsers),
        )
        return None
  
   
    
    
    someSymbolsAndDefaultsToTranslate = [
        [ 'ModelDDvlPlone', [ 
            [ 'ModelDDvlPlone_Cache_MustChooseAProjectBeforeChoosingALanguage_Title',     'Must choose one of the Projects before choosing a Language-',],
            [ 'ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamed_Title',               'No cache entries for project named: -',],
            [ 'ModelDDvlPlone_Cache_ChooseALanguage_Title',                               'Choose one of the Languages-',],
            [ 'ModelDDvlPlone_Cache_Languages_Label',                                     'Languages-',],

        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)

    
    
    
    aProjectName = theAdditionalParams.get( 'theProjectName', '')
    
    if not aProjectName:
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                <strong>
                    %(ModelDDvlPlone_Cache_MustChooseAProjectBeforeChoosingALanguage_Title)s
                </strong>
            </font>        
        </h3>
        """ % {
            'ModelDDvlPlone_Cache_MustChooseAProjectBeforeChoosingALanguage_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_MustChooseAProjectBeforeChoosingALanguage_Title']),
        })
        return None
    
    
    
    aContextualObjectURL = theContextualObject.absolute_url()
        
    aModelDDvlPloneTool_Cache     = theModelDDvlPloneTool.fModelDDvlPloneTool_Cache(     theContextualObject)        

    
    
    aBeginMillis = fMillisecondsNow()
        
    try:
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
                    

    
        someProjectNames = aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,)
        if not ( aProjectName in someProjectNames):   
            theOutput.write( """
            <br/>
            <h3>
                <font color="red">
                    %(ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamed_Title)s
                    <strong>
                        %(aProjectName)s
                    </strong>
                </font>        
            </h3>
            """ % {
                'aProjectName':                                                 aProjectName,
                'ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamed_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_MustChooseAProjectBeforeChoosingALanguage_Title']),
            })
            return None
    
        
        
        
        theOutput.write( """
        <br/>
        <h3>
        %(ModelDDvlPlone_Cache_ChooseALanguage_Title)s
        </h3>
        <table class="listing" id="cidMDDCache_LanguageChooser_table" >
            <thead>
                <th>
                    %(ModelDDvlPlone_Cache_Languages_Label)s
                </th>
            </thead>
            <tbody>
        """ % {
            'ModelDDvlPlone_Cache_ChooseALanguage_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_ChooseALanguage_Title']),
            'ModelDDvlPlone_Cache_Languages_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Languages_Label']),
        })

        
        
        
        unasClasesFilas = ('odd','even',)

        
        someTemplatesByLanguageForProject = aModelDDvlPloneTool_Cache.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, aProjectName)                              
        someLanguages = sorted( ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or [])
        aNumLanguages = len( someLanguages)
        
        for aLanguageIndex  in range( aNumLanguages):
            
            aLanguage = someLanguages[ aLanguageIndex]

            
            if aLanguage:
                theOutput.write( """
                <tr class="MDD_Cache_Row_Language %%(row-class)s" >
                    <td class="MDD_Cache_Cell_Language" >
                        <a id="cidMDDCache_ChooseLanguage_%(aLanguage)s" 
                            href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s&theLanguage=%(aLanguage)s">
                            %(aLanguage)s
                        </a>
                </tr>
                """ % {
                    'aURL':         aContextualObjectURL,
                    'theCacheName': theCacheName,
                    'aProjectName': fCGIE( aProjectName),
                    'aLanguage':    fCGIE( aLanguage),
                    'row-class':    unasClasesFilas[ aLanguageIndex % 2],
                })
                
                
        theOutput.write( """
            </tbody>
        </table>
        <br/>
        """ )
        
    finally:
        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                        
                 
    return None




    
def _fCacheDump_ForElements(
    theModelDDvlPloneTool =None, 
    theContextualObject   =None, 
    theCacheName          =None, 
    theAdditionalParams   =None):
    """ Return theHTML, with a representation of entries in the named cache.
    
    """
    
    unosMillisecondsNow   = fMillisecondsNow()
    
    unOutput = StringIO()


    if theModelDDvlPloneTool == None:
        unOutput.write( """
        <h2><font color="red">No parameter theModelDDvlPloneTool</font></h2>
        """)
        return unOutput.getvalue()

    if theContextualObject == None:
        unOutput.write( """
        <h2><font color="red">No parameter theContextualObject</font></h2>
        """)
        return unOutput.getvalue()

    if not ( theCacheName in cCacheNamesForElementsOrUsers):
        unOutput.write( """
        <h2><font color="red">Named cache must be one of : %s</font></h2>
        """ % ','.join( cCacheNamesForElementsOrUsers),
        )
        return unOutput.getvalue()
  
    

    aContextualObjectURL = theContextualObject.absolute_url()
    

    
    #_pCacheDump_ForElements_QueryForm(
        #theModelDDvlPloneTool =theModelDDvlPloneTool, 
        #theContextualObject   =theContextualObject, 
        #theCacheName          =theCacheName, 
        #theOutput             =unOutput,
        #theAdditionalParams   =theAdditionalParams,
    #)
            
    
    aProjectName = theAdditionalParams.get( 'theProjectName', '')
    
    if not aProjectName:
        _fCacheDump_ForElements_ProjectChooser(
            theModelDDvlPloneTool =theModelDDvlPloneTool, 
            theContextualObject   =theContextualObject, 
            theCacheName          =theCacheName, 
            theOutput             =unOutput,
            theAdditionalParams   =theAdditionalParams,
        )
        return unOutput.getvalue()
    
    
    

    
    someSymbolsAndDefaultsToTranslate = [
        [ 'ModelDDvlPlone', [ 
            [ 'ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamedAndLanguage_Title' , 'No cache entries for project and language:-'],
            [ 'ModelDDvlPlone_Cache_ChooseOtherProject',      'Choose other Project-',],
            [ 'ModelDDvlPlone_Cache_ChooseOtherLanguage',      'Choose other Language-',],
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

   
    
    unOutput.write( """
    <br/>
    <p>
        <font size="2" >
            %(ModelDDvlPlone_Cache_Project_Label)s
            <strong>
                %(aProjectName)s
            </strong>
        </font>
        &emsp;
        &emsp;
        <a id="cidMDDCache_ChooseOtherProject_link" 
            href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s">
            %(ModelDDvlPlone_Cache_ChooseOtherProject)s
        </a>
    </p>
    """ % {
        'aURL':         aContextualObjectURL,
        'theCacheName':                         theCacheName,
        'aProjectName':                         aProjectName,
        'ModelDDvlPlone_Cache_Project_Label':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Project_Label']),
        'ModelDDvlPlone_Cache_ChooseOtherProject': fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_ChooseOtherProject']),
    })
    
    
    
    
    
    aLanguage    = theAdditionalParams.get( 'theLanguage', '')
    
    if not aLanguage:
        _fCacheDump_ForElements_LanguageChooser(
            theModelDDvlPloneTool =theModelDDvlPloneTool, 
            theContextualObject   =theContextualObject, 
            theCacheName          =theCacheName, 
            theOutput             =unOutput,
            theAdditionalParams   =theAdditionalParams,
        )
        return unOutput.getvalue()
    
            
    
    unOutput.write( """
    <br/>
    <p>
        <font size="2" >
            %(ModelDDvlPlone_Cache_Language_Label)s
            <strong>
                %(aLanguage)s
            </strong>
        </font>
        &emsp;
        &emsp;
        <a id="cidMDDCache_ChooseLanguage_%(aLanguage)s" 
            href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s">
            %(ModelDDvlPlone_Cache_ChooseOtherLanguage)s
        </a>
    </p>
    """ % {
        'aURL':         aContextualObjectURL,
        'theCacheName':                         theCacheName,
        'aProjectName':                         aProjectName,
        'aLanguage':                             aLanguage,
        'ModelDDvlPlone_Cache_Language_Label':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Language_Label']),
        'ModelDDvlPlone_Cache_ChooseOtherLanguage':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_ChooseOtherLanguage']),
    })
    
        
    
    
    
 
        
    aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
    aModelDDvlPloneTool_Cache     = theModelDDvlPloneTool.fModelDDvlPloneTool_Cache(     theContextualObject)        

    
    
    
    unOutput.write( """
    <script type="text/javascript">
    function fMDDConfirmFlush( theCacheEntryId, theCacheName, thePostfix) {
        if ( window.confirm( "Do you want to Flush the  " + theCacheName + " cache entry " + theCacheEntryId + thePostfix) && window.confirm( "Do you REALLY want to Flush the cache entry " + theCacheEntryId + thePostfix)) { 
            return true;
        } 
        else { 
            return false;
        }    
    }
    </script>
    """)
    

    
    aFirstEntryIndex = theAdditionalParams.get( 'theFirstEntryIndex', 0)
    if not isinstance( aFirstEntryIndex, int):
        aFirstEntryIndex = 0
        try:
            aFirstEntryIndex = int( aFirstEntryIndex)
        except:
            None
    if ( not aFirstEntryIndex) or ( aFirstEntryIndex <= 1):
        aFirstEntryIndex = 0
        
    
    
    aNumEntries = theAdditionalParams.get( 'theNumEntries', 0)
    if not isinstance( aNumEntries, int):
        aNumEntries = 0
        try:
            aNumEntries = int( aNumEntries)
        except:
            None
    if ( not aNumEntries) or ( aNumEntries < 1):
        aNumEntries = cMDDCacheDump_NumEntries_Default
    if aNumEntries > cMDDCacheDump_NumEntries_Maximum:
        aNumEntries = cMDDCacheDump_NumEntries_Maximum
    
    
    aNumColumns = 12
    aBeginMillis = fMillisecondsNow()
        
    try:
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        
        
        
        

    
        someProjectNames = aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,)
        if not ( aProjectName in someProjectNames):   
            unOutput.write( """
            <br/>
            <h3>
                <font color="red">
                    %(ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamed_Title)s
                    <strong>
                        %(aProjectName)s
                    </strong>
                </font>        
            </h3>
            """ % {
                'aProjectName':                                                 aProjectName,
                'ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamed_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_MustChooseAProjectBeforeChoosingALanguage_Title']),
            })
            return unOutput.getvalue()
    
                
        
        someTemplatesByLanguageForProject = aModelDDvlPloneTool_Cache.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, aProjectName)                              
        if not someTemplatesByLanguageForProject.has_key( aLanguage):   
            unOutput.write( """
            <br/>
            <h3>
                <font color="red">
                    %(ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamedAndLanguage_Title)s
                    <strong>
                        %(aProjectName)s  %(aLanguage)s
                    </strong>
                </font>        
            </h3>
            """ % {
                'aProjectName':    aProjectName,
                'aLanguage':       aLanguage,
                'ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamedAndLanguage_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamedAndLanguage_Title']),
            })
            return unOutput.getvalue()
        
        
    
        unOutput.write( """
        <table class="listing" id="cidMDDCache_EntriesTable" >
            <thead>
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
    
                
        
        # ###########################################################
        """Obtain diagnostics, to be able to highlight entries with problems.
        
        """
        allDiagnostics = aModelDDvlPloneTool_Cache.fCachesDiagnostics_WithinCriticalSection( theModelDDvlPloneTool, theContextualObject, theCacheNames=[ theCacheName,], theAdditionalParams=theAdditionalParams)
        allEntriesWithProblems = allDiagnostics.get( 'allEntriesWithProblems', {})
        
                   
        # ###########################################################
        """Traverse cache control structures to collect UIDs of elements in the cache, to retrieve them in a single search.
        
        """
        someUIDsElementsToRetrieve = set()
        
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
        
        
        unasClasesFilas = ('odd','even',)
        aRowIndex = 0
        
        aMillisecondsNow = fMillisecondsNow()
        
        aPortalURL = theModelDDvlPloneTool.fPortalURL()
        
        
        
        
        # ###########################################################
        """Iterate over Elements UIDs
        
        """
        someUIDs = sorted( (someTemplatesByUIDForLanguage and someTemplatesByUIDForLanguage.keys()) or [])
        aNumUIDs = len( someUIDs)
        

        
        for anUIDIndex in range ( aNumUIDs):
            
            anUID = someUIDs[ anUIDIndex]
            
    
            # ########################
            """Dump UID
            
            """
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
            <tr class="MDD_Cache_Row_Project %%(row-class)s" >
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
            
            unOutput.write( unUIDString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                        
            
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
                                        <a onclick="return fMDDConfirmFlush( '%(aUniqueId)s', '%(theCacheName)s', ' from Memory')"
                                           href="%(aFlushFromMemoryHref)s" name="Flush Cache Entry  %(aUniqueId)s from Memory">
                                            <img alt="Flush Cache Entry %(aUniqueId)s from Memory" title="Flush Cache Entry %(aUniqueId)s from Memory" id="icon-flush-memory" 
                                            src="%(aPortalURL)s/mddflushmemory.gif"/>
                                        </a>
                                        &emsp;
                                        <a onclick="return fMDDConfirmFlush( '%(aUniqueId)s', '%(theCacheName)s', ' from Memory and Disk')"
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
                                    'theCacheName':         theCacheName,
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

    if not ( theCacheName == cCacheName_ElementIndependent):
        unOutput.write( """
        <h2><font color="red">Named cache must be %s</font></h2>
        """ % cCacheName_ElementIndependent,
        )
        return unOutput.getvalue()
    
    
    unOutput.write( """
    <script type="text/javascript">
    function fMDDConfirmFlush( theCacheEntryId, theCacheName, thePostfix) {
        if ( window.confirm( "Do you want to Flush the " + theCacheName + " cache entry " + theCacheEntryId + thePostfix) && window.confirm( "Do you REALLY want to Flush the cache entry " + theCacheEntryId + thePostfix)) { 
            return true;
        } 
        else { 
            return false;
        }    
    }
    </script>
    """)

    
          
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
           

            [ 'ModelDDvlPlone_Cache_Query_FirstEntryIndex',   'First Entry index-',],
            [ 'ModelDDvlPlone_Cache_Query_NumEntries',        'Number of entries-',],
            
        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)


    
    
    aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
    aModelDDvlPloneTool_Cache     = theModelDDvlPloneTool.fModelDDvlPloneTool_Cache(     theContextualObject)        
    
    unOutput.write( """
    <table class="listing" id="cidMDDCache_Entries_table" >
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
                                <a onclick="return fMDDConfirmFlush( '%(aUniqueId)s', '%(theCacheName)s', ' from Memory')"
                                   href="%(aFlushFromMemoryHref)s" name="Flush Cache Entry  %(aUniqueId)s from Memory">
                                    <img alt="Flush Cache Entry %(aUniqueId)s from Memory" title="Flush Cache Entry %(aUniqueId)s from Memory" id="icon-flush-memory" 
                                    src="%(aPortalURL)s/mddflushmemory.gif"/>
                                </a>
                                &emsp;
                                <a onclick="return fMDDConfirmFlushDisk( '%(aUniqueId)s', '%(theCacheName)s', ' from Memory and Disk')"
                                   href="%(aFlushFromDiskHref)s" name="Flush Cache Entry %(aUniqueId)s from Memory and Disk">
                                    <img alt="Flush Cache Entry %(aUniqueId)s from Memory and Disk" title="Flush Cache Entry %(aUniqueId)s from Memory and Disk" id="icon-flush-disk" 
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
                            'theCacheName':         theCacheName,
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
            

        