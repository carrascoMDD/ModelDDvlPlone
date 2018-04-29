# -*- coding: utf-8 -*-
#
# File: MDDCacheDump.py
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
            [ 'ModelDDvlPlone_Cache_NoProjectsInCache_Title', 'No Projects in Cache-',],
            [ 'ModelDDvlPlone_Cache_ChooseAProject_Title',    'Choose one of the Projects-',],
            [ 'ModelDDvlPlone_Cache_Projects_Label',          'Projects-',],
            [ 'ModelDDvlPlone_Cache_NumEntries_Label',        '# entries-',],
            

        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)

   
        
    aModelDDvlPloneTool_Cache     = theModelDDvlPloneTool.fModelDDvlPloneTool_Cache(     theContextualObject)        

    
    aContextualObjectURL = theContextualObject.absolute_url()
    
    
    aNumColumns = 14
    aBeginMillis = fMillisecondsNow()
    
    someProjectNames        = []
    someNumEntriesByProject = { }
        
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
        
        
        someProjectNames = aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,)
        
        for aProjectName in someProjectNames:
            
            someNumEntriesByProject[ aProjectName] = aModelDDvlPloneTool_Cache.fCountElementDependentCachedEntriesInProjectLanguageRoot( 
                theModelDDvlPloneTool  =theModelDDvlPloneTool, 
                theContextualObject    =theContextualObject, 
                theCacheName           =theCacheName, 
                theProjectName         =aProjectName, 
                theLanguage            =None,
                theRoot                =None,
                theEnforceThreadSafety =False,
            )
            
        
    finally:
        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                        


    
    if not someProjectNames:
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                %(ModelDDvlPlone_Cache_NoProjectsInCache_Title)s
            </font>        
        </h3>
        <br/>
        """ % {
            'ModelDDvlPlone_Cache_NoProjectsInCache_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoProjectsInCache_Title']),
        })
        return None
    
    
    
    
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
            <th align="right" >
                %(ModelDDvlPlone_Cache_NumEntries_Label)s
            </th>
        </thead>
        <tbody>
    """ % {
        'ModelDDvlPlone_Cache_ChooseAProject_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_ChooseAProject_Title']),
        'ModelDDvlPlone_Cache_Projects_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Projects_Label']),
        'ModelDDvlPlone_Cache_NumEntries_Label':       fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NumEntries_Label']),
    })
    
    
    
    unasClasesFilas = ('odd','even',)

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
                <td class="MDD_Cache_Cell_NumEntries" align="right"  >
                    <a id="cidMDDCache_ChooseProject_%(aProjectName)s" href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s">
                        %(aNumEntries)d
                    </a>
                </td>
            </tr>
            """ % {
                'theCacheName': fCGIE( theCacheName),
                'aURL':         aContextualObjectURL,
                'aProjectName': fCGIE( aProjectName),
                'aNumEntries':  someNumEntriesByProject.get( aProjectName, 0),
                'row-class':    unasClasesFilas[ aProjectIndex % 2],
            })
                    
                                 
    theOutput.write( """
        </tbody>
    </table>
    <br/>
    """ )
    
    
    return None





def _fCacheDump_ForElements_Header_ProjectLanguageRoot(
    theModelDDvlPloneTool =None, 
    theContextualObject   =None, 
    theCacheName          =None, 
    theProjectName        =None,
    theLanguage           =None,
    theRoot               =None,
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
            [ 'ModelDDvlPlone_Cache_Selection_Label',                     'Selection-',],
            [ 'ModelDDvlPlone_Cache_Selected_Id_Label',                   'Id-',],
            [ 'ModelDDvlPlone_Cache_Selected_NumEntries_Label',           '# entries-',],
            [ 'ModelDDvlPlone_Cache_Selected_Path_Label',                 'Path-',],
            [ 'ModelDDvlPlone_Cache_Selected_UID_Label',                  'UID-',],
            [ 'ModelDDvlPlone_Cache_Project_Label',                       'Project-',],
            [ 'ModelDDvlPlone_Cache_Language_Label',                      'Language-',],
            [ 'ModelDDvlPlone_Cache_Root_Label',                          'Root-',],
            [ 'ModelDDvlPlone_Cache_ChosenProjectLanguageHost_Title',     'Chosen Cache Project, Language and Root element-',],
            [ 'ModelDDvlPlone_Cache_Change',                              'Change-',],
            [ 'ModelDDvlPlone_Cache_Flush',                               'Flush-',],
            [ 'ModelDDvlPlone_Cache_Select',                              'Select-',],
            [ 'ModelDDvlPlone_Cache_NoProjectSelected',                   'No Project Selected-',],
            [ 'ModelDDvlPlone_Cache_NoLanguageSelected',                  'No Language Selected-',],
            [ 'ModelDDvlPlone_Cache_NoRootSelected',                      'No Root Selected-',],

            
            
        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)
    
    

    theOutput.write( """
    <br/>
    <h3>
    %(ModelDDvlPlone_Cache_ChosenProjectLanguageHost_Title)s
    </h3>
    <table class="listing" id="cidMDDCache_Selected_table" name="cidMDDCache_Selected_table" >
        <thead>
            <tr >
                <th class="nosort">
                    %(ModelDDvlPlone_Cache_Selection_Label)s
                </th>
                <th class="nosort">
                    %(ModelDDvlPlone_Cache_Selected_Id_Label)s
                </th>
                <th class="nosort">
                    %(ModelDDvlPlone_Cache_Selected_NumEntries_Label)s
                </th>
                <th class="nosort">
                    %(ModelDDvlPlone_Cache_Change)s
                </th>
                <th class="nosort">
                    %(ModelDDvlPlone_Cache_Flush)s
                </th>
                <th class="nosort">
                    %(ModelDDvlPlone_Cache_Selected_Path_Label)s
                </th>
                <th class="nosort">
                    %(ModelDDvlPlone_Cache_Selected_UID_Label)s
                </th>
            </tr>
        </thead>
        <tbody>
    """ % {
        'ModelDDvlPlone_Cache_ChosenProjectLanguageHost_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_ChosenProjectLanguageHost_Title']),
        'ModelDDvlPlone_Cache_Selection_Label':                   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Selection_Label']),
        'ModelDDvlPlone_Cache_Selected_Id_Label':                 fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Selected_Id_Label']),
        'ModelDDvlPlone_Cache_Selected_NumEntries_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Selected_NumEntries_Label']),
        'ModelDDvlPlone_Cache_Selected_Path_Label':               fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Selected_Path_Label']),
        'ModelDDvlPlone_Cache_Selected_UID_Label':                fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Selected_UID_Label']),
        'ModelDDvlPlone_Cache_Change':                            fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Change']),
        'ModelDDvlPlone_Cache_Flush':                             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Flush']),
    })
    
    
    aModelDDvlPloneTool_Cache     = theModelDDvlPloneTool.fModelDDvlPloneTool_Cache(     theContextualObject)        
    
    
    aContextualObjectURL = theContextualObject.absolute_url()
    
    
    
    if theProjectName:
        
        aNumEntriesProject = aModelDDvlPloneTool_Cache.fCountElementDependentCachedEntriesInProjectLanguageRoot( 
            theModelDDvlPloneTool  =theModelDDvlPloneTool, 
            theContextualObject    =theContextualObject, 
            theCacheName           =theCacheName, 
            theProjectName         =theProjectName, 
            theLanguage            =None,
            theRoot                =None,
            theEnforceThreadSafety =False,
        )    
    
        theOutput.write( """
            <tr class="odd" >
                <td align="left">
                    <strong>
                        %(ModelDDvlPlone_Cache_Project_Label)s
                    </strong>
                </td>
                <td align="left" >
                    %(theProjectName)s
                </td>
                <td align="right" >
                    %(aNumEntries)d
                </td>
                <td>
                    <a id="cidMDDCache_ChooseOtherProject_link" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s">
                        %(ModelDDvlPlone_Cache_Change)s
                    </a>
                </td>
                <td>
                    <a id="cidMDDCache_FlushProject_link" 
                        onclick="return fMDDConfirmFlushSelected( '%(theProjectName)s', '', '', '%(theCacheName)s', ' from Memory and Disk')"
                        href="%(aURL)s/MDDFlushCachedTemplatesSelected?theCacheName=%(theCacheName)s&theProjectName=%(theProjectName)s">
                        %(ModelDDvlPlone_Cache_Flush)s
                    </a>
                </td>
                <td colspan="2" />
            </tr>
        """ % {
            'aURL':                                    aContextualObjectURL,
            'aNumEntries':                             aNumEntriesProject,
            'theCacheName':                            fCGIE( theCacheName),
            'theProjectName':                          fCGIE( theProjectName),
            'ModelDDvlPlone_Cache_Project_Label':      fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Project_Label']),
            'ModelDDvlPlone_Cache_Change':             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Change']),
            'ModelDDvlPlone_Cache_Flush':              fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Flush']),
        })

    else:
    
        theOutput.write( """
            <tr class="odd" >
                <td align="left" colspan="3" >
                    <strong>
                        %(ModelDDvlPlone_Cache_NoProjectSelected)s
                    </strong>
                </td>
                <td>
                    <a id="cidMDDCache_ChooseOtherProject_link" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s">
                        %(ModelDDvlPlone_Cache_Select)s
                    </a>
                </td>
                <td colspan="2" />
            </tr>
        """ % {
            'aURL':                                    aContextualObjectURL,
            'theCacheName':                            fCGIE( theCacheName),
            'ModelDDvlPlone_Cache_Select':             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Select']),
            'ModelDDvlPlone_Cache_NoProjectSelected':  fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoProjectSelected']),
        })
        
    
        
        
        
        
        
    if theLanguage:
        
        aNumEntriesLanguage= aModelDDvlPloneTool_Cache.fCountElementDependentCachedEntriesInProjectLanguageRoot( 
            theModelDDvlPloneTool  =theModelDDvlPloneTool, 
            theContextualObject    =theContextualObject, 
            theCacheName           =theCacheName, 
            theProjectName         =theProjectName, 
            theLanguage            =theLanguage,
            theRoot                =None,
            theEnforceThreadSafety =False,
        )    
            
        theOutput.write( """
            <tr class="odd" >
                <td align="left">
                    <strong>
                        %(ModelDDvlPlone_Cache_Language_Label)s
                    </strong>
                </td>
                <td align="left" >
                    %(theLanguage)s
                </td>
                <td align="right" >
                    %(aNumEntries)d
                </td>
                <td>
                    <a id="cidMDDCache_ChooseOtherLanguage_link" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(theProjectName)s">
                        %(ModelDDvlPlone_Cache_Change)s
                    </a>
                </td>
                <td>
                    <a id="cidMDDCache_FlushLanguage_link" 
                        onclick="return fMDDConfirmFlushSelected( '%(theProjectName)s', %(theLanguage)s, '', '%(theCacheName)s', ' from Memory and Disk')"
                        href="%(aURL)s/MDDFlushCachedTemplatesSelected?theCacheName=%(theCacheName)s&theProjectName=%(theProjectName)s&theLanguage=%(theLanguage)s">
                        %(ModelDDvlPlone_Cache_Flush)s
                    </a>
                </td>
                <td colspan="2" />
            </tr>
        """ % {
            'aURL':                                    aContextualObjectURL,
            'aNumEntries':                             aNumEntriesLanguage,
            'theCacheName':                            fCGIE( theCacheName),
            'theProjectName':                          fCGIE( theProjectName),
            'theLanguage':                             fCGIE( theLanguage),
            'ModelDDvlPlone_Cache_Language_Label':     fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Language_Label']),
            'ModelDDvlPlone_Cache_Change':             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Change']),
            'ModelDDvlPlone_Cache_Flush':              fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Flush']),
        })
        
        
    else:
    
        theOutput.write( """
            <tr class="odd" >
                <td align="left" colspan="3" >
                    <strong>
                        %(ModelDDvlPlone_Cache_NoLanguageSelected)s
                    </strong>
                </td>
                <td>
        """ % {
            'aURL':                                    aContextualObjectURL,
            'aNumEntriesProject':                      aNumEntriesProject,
            'theCacheName':                            fCGIE( theCacheName),
            'theProjectName':                          fCGIE( theProjectName),
            'ModelDDvlPlone_Cache_Select':             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Select']),
            'ModelDDvlPlone_Cache_NoLanguageSelected': fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoLanguageSelected']),
        })

        if theProjectName:
 
            theOutput.write( """
                <a id="cidMDDCache_ChooseOtherProject_link" 
                    href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(theProjectName)s">
                    %(ModelDDvlPlone_Cache_Select)s
                </a>
            """ % {
                'aURL':                                    aContextualObjectURL,
                'aNumEntriesProject':                      aNumEntriesProject,
                'theCacheName':                            fCGIE( theCacheName),
                'theProjectName':                          fCGIE( theProjectName),
                'ModelDDvlPlone_Cache_Select':             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Select']),
                'ModelDDvlPlone_Cache_NoLanguageSelected': fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoLanguageSelected']),
            })
            
        theOutput.write( """
                </td>
                <td colspan="2" />            
            </tr>
        """)
        
        
    if theRoot:
        
        aRootId   = '?'
        aRootPath = '?'
        
        aRootResult = theModelDDvlPloneTool.fNewResultForElementByUID( 
            theContextualElement =theContextualObject, 
            theUID               =theRoot,
        )
        if aRootResult:
            aRootId   = aRootResult.get( 'id',   theRoot)
            aRootPath = aRootResult.get( 'path', theRoot)
            
            
        aNumEntriesRoot= aModelDDvlPloneTool_Cache.fCountElementDependentCachedEntriesInProjectLanguageRoot( 
            theModelDDvlPloneTool  =theModelDDvlPloneTool, 
            theContextualObject    =theContextualObject, 
            theCacheName           =theCacheName, 
            theProjectName         =theProjectName, 
            theLanguage            =theLanguage,
            theRoot                =theRoot,
            theEnforceThreadSafety =False,
        )    
            
        theOutput.write( """
            <tr class="odd" >
                <td align="left">
                    <strong>
                        %(ModelDDvlPlone_Cache_Root_Label)s
                    </strong>
                </td>
                <td align="left" >
                    %(aRootId)s
                </td>
                <td align="right" >
                    %(aNumEntries)d
                </td>
                <td>
                    <a id="cidMDDCache_ChooseOtherRoot_link" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(theProjectName)s&theLanguage=%(theLanguage)s">
                        %(ModelDDvlPlone_Cache_Change)s
                    </a>
                </td>
                <td>
                    <a id="cidMDDCache_FlushRoot_link" 
                        onclick="return fMDDConfirmFlushSelected( '%(theProjectName)s', %(theLanguage)s, %(theRoot)s, '%(theCacheName)s', ' from Memory and Disk')"
                        href="%(aURL)s/MDDFlushCachedTemplatesSelected?theCacheName=%(theCacheName)s&theProjectName=%(theProjectName)s&theLanguage=%(theLanguage)s&theRoot=%(theRoot)s">
                        %(ModelDDvlPlone_Cache_Flush)s
                    </a>
                </td>
                <td>
                    %(aRootPath)s
                </td>
                <td>
                    %(theRoot)s
                </td>
            </tr>
        """ % {
            'aURL':                                    aContextualObjectURL,
            'aNumEntries':                             aNumEntriesRoot,
            'theCacheName':                            fCGIE( theCacheName),
            'theProjectName':                          fCGIE( theProjectName),
            'theLanguage':                             fCGIE( theLanguage),
            'theRoot':                                 fCGIE( theRoot),
            'aRootId':                                 fCGIE( aRootId),
            'aRootPath':                               fCGIE( aRootPath.replace( '/', '/ ')),
            'ModelDDvlPlone_Cache_Root_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Root_Label']),
            'ModelDDvlPlone_Cache_Change':             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Change']),
            'ModelDDvlPlone_Cache_Flush':              fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Flush']),
        })
        
        
    else:
    
        theOutput.write( """
            <tr class="odd" >
                <td align="left" colspan="3" >
                    <strong>
                        %(ModelDDvlPlone_Cache_NoRootSelected)s
                    </strong>
                </td>
                <td>
        """ % {
            'aURL':                                    aContextualObjectURL,
            'aNumEntriesProject':                      aNumEntriesProject,
            'theCacheName':                            fCGIE( theCacheName),
            'theProjectName':                          fCGIE( theProjectName),
            'theLanguage':                             fCGIE( theLanguage),
            'ModelDDvlPlone_Cache_Select':             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Select']),
            'ModelDDvlPlone_Cache_NoRootSelected':     fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoRootSelected']),
        })
        
        
        
        if theProjectName and theLanguage:

            theOutput.write( """
                <a id="cidMDDCache_ChooseOtherProject_link" 
                    href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(theProjectName)s&theLanguage=%(theLanguage)s">
                    %(ModelDDvlPlone_Cache_Select)s
                </a>
            """ % {
                'aURL':                                    aContextualObjectURL,
                'aNumEntriesProject':                      aNumEntriesProject,
                'theCacheName':                            fCGIE( theCacheName),
                'theProjectName':                          fCGIE( theProjectName),
                'theLanguage':                             fCGIE( theLanguage),
                'ModelDDvlPlone_Cache_Select':             fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Select']),
                'ModelDDvlPlone_Cache_NoRootSelected':     fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoRootSelected']),
            })
        
        
        theOutput.write( """
                </td>
                <td colspan="2" />            
            </tr>
        """)        
        
        
        
     
    theOutput.write( """
            </tbody>
        </table>
        <br/>
    """)
    
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
            [ 'ModelDDvlPlone_Cache_NoProjectNamedInCache_Title',                         'Cache does not hold a Project named-',],
            [ 'ModelDDvlPlone_Cache_NoLanguagesInCacheForProjectNamed_Title',             'No Languages in cache for project named: -',],
            [ 'ModelDDvlPlone_Cache_ChooseALanguage_Title',                               'Choose one of the Languages-',],
            [ 'ModelDDvlPlone_Cache_Languages_Label',                                     'Languages-',],
            [ 'ModelDDvlPlone_Cache_NumEntries_Label',                                    '# entries-',],
        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)

    

    aProjectName = theAdditionalParams.get( 'theProjectName', '')
    
    
    
    _fCacheDump_ForElements_Header_ProjectLanguageRoot(
        theModelDDvlPloneTool =theModelDDvlPloneTool, 
        theContextualObject   =theContextualObject, 
        theCacheName          =theCacheName, 
        theProjectName        =aProjectName,
        theLanguage           =None,
        theRoot               =None,
        theOutput             =theOutput,
        theAdditionalParams   =theAdditionalParams,
    )
        
    
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
    
    aProjectFound            = False
    someLanguages            = []
    someNumEntriesByLanguage = { }
        
    try:
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        someProjectNames = aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,)
        if aProjectName in someProjectNames:   
    
            aProjectFound = True
        
            someTemplatesByLanguageForProject = aModelDDvlPloneTool_Cache.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, aProjectName)                              
            if someTemplatesByLanguageForProject:
                
                someLanguages = sorted( someTemplatesByLanguageForProject.keys())

                for aLanguage in someLanguages:
                    
                    aNumEntriesInLanguage = aModelDDvlPloneTool_Cache.fCountElementDependentCachedEntriesInProjectLanguageRoot( 
                        theModelDDvlPloneTool  =theModelDDvlPloneTool, 
                        theContextualObject    =theContextualObject, 
                        theCacheName           =theCacheName, 
                        theProjectName         =aProjectName, 
                        theLanguage            =aLanguage,
                        theRoot                =None,
                        theEnforceThreadSafety =False,
                    )
                    
                    someNumEntriesByLanguage[ aLanguage] = aNumEntriesInLanguage
                    
        
    finally:
        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                          
        
        
    if not aProjectFound:   
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                %(ModelDDvlPlone_Cache_NoProjectNamedInCache_Title)s
                <strong>
                    %(aProjectName)s
                </strong>
            </font>        
        </h3>
        """ % {
            'aProjectName':                                       fCGIE( aProjectName),
            'ModelDDvlPlone_Cache_NoProjectNamedInCache_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoProjectNamedInCache_Title']),
        })
        return None
        
        
    
        
    if not someLanguages:   
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                %(ModelDDvlPlone_Cache_NoLanguagesInCacheForProjectNamed_Title)s
                <strong>
                    %(aProjectName)s
                </strong>
            </font>        
        </h3>
        """ % {
            'aProjectName':                                                 fCGIE( aProjectName),
            'ModelDDvlPlone_Cache_NoLanguagesInCacheForProjectNamed_Title': fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoLanguagesInCacheForProjectNamed_Title']),
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
            <th align="right" >
                %(ModelDDvlPlone_Cache_NumEntries_Label)s
            </th>
        </thead>
        <tbody>
    """ % {
        'ModelDDvlPlone_Cache_ChooseALanguage_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_ChooseALanguage_Title']),
        'ModelDDvlPlone_Cache_Languages_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Languages_Label']),
        'ModelDDvlPlone_Cache_NumEntries_Label':        fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NumEntries_Label']),
    })

    
    unasClasesFilas = ('odd','even',)
        
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
                </td>
                <td class="MDD_Cache_Cell_NumEntries"  align="right" >
                    <a id="cidMDDCache_ChooseLanguage_%(aLanguage)s" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s&theLanguage=%(aLanguage)s">
                        %(aNumEntries)d
                    </a>
                </td>
            </tr>
            """ % {
                'aURL':         aContextualObjectURL,
                'theCacheName': fCGIE( theCacheName),
                'aProjectName': fCGIE( aProjectName),
                'aLanguage':    fCGIE( aLanguage),
                'aNumEntries':  someNumEntriesByLanguage.get( aLanguage, 0),
                'row-class':    unasClasesFilas[ aLanguageIndex % 2],
            })
            
            
    theOutput.write( """
        </tbody>
    </table>
    <br/>
    """ )       
    
    return None




    
def _fCacheDump_ForElements_RootChooser(
    theModelDDvlPloneTool =None, 
    theContextualObject   =None, 
    theCacheName          =None, 
    theOutput             =None,
    theAdditionalParams   =None):
    """ Return theHTML, with a list of id of root elements in the selected project in the named cache.
    
    """
    
    if theOutput == None:
        return None    

    if theModelDDvlPloneTool == None:
        theOutput.write( """
        <h2><font color="red">No parameter theModelDDvlPloneTool in _fCacheDump_ForElements_RootChooser</font></h2>
        """)
        return None

    if theContextualObject == None:
        theOutput.write( """
        <h2><font color="red">No parameter theContextualObject in _fCacheDump_ForElements_RootChooser</font></h2>
        """)
        return None

    if not ( theCacheName in cCacheNamesForElementsOrUsers):
        theOutput.write( """
        <h2><font color="red">Named cache must be one of : %s in _fCacheDump_ForElements_RootChooser</font></h2>
        """ % ','.join( cCacheNamesForElementsOrUsers),
        )
        return None
  
   
    
    
    someSymbolsAndDefaultsToTranslate = [
        [ 'ModelDDvlPlone', [ 
            [ 'ModelDDvlPlone_Cache_NoProjectNamedInCache_Title',                                 'Cache does not hold a Project named-',],
            [ 'ModelDDvlPlone_Cache_MustChooseAProjectAndALanguageBeforeChoosingARoot_Title',     'Must choose one of the Projects and a Language before choosing a Root-',],
            [ 'ModelDDvlPlone_Cache_MustChooseALanguageInTheProjectBeforeChoosingARoot_Title',    'Must choose one of the Languages in the project before choosing a Root-',],
            [ 'ModelDDvlPlone_Cache_CachedProjectHasNoLanguageNamed_Title',                       'Cached Project does not hold a Language named-',],
            [ 'ModelDDvlPlone_Cache_NoRootsInCacheForProjectAndLanguageNamed_Title',              'No Roots in Cache for Project and Language named-',],
            [ 'ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamed_Title',                       'No cache entries for project named: -',],
            [ 'ModelDDvlPlone_Cache_ChooseARoot_Title',                                           'Choose one of the Roots-',],
            [ 'ModelDDvlPlone_Cache_Root_Id_Label',                                               'Id-',],
            [ 'ModelDDvlPlone_Cache_Root_Path_Label',                                             'Path-',],
            [ 'ModelDDvlPlone_Cache_Root_UID_Label',                                              'UID-',],
            [ 'ModelDDvlPlone_Cache_NumEntries_Label',                                            '# entries-',],
        ]],
    ]
    
    someTranslations = { }
    theModelDDvlPloneTool.fTranslateI18NManyIntoDict( theContextualObject, someSymbolsAndDefaultsToTranslate, someTranslations)

    
    
    aProjectName = theAdditionalParams.get( 'theProjectName', '')
    
    aLanguage = theAdditionalParams.get( 'theLanguage', '')
        
    
    _fCacheDump_ForElements_Header_ProjectLanguageRoot(
        theModelDDvlPloneTool =theModelDDvlPloneTool, 
        theContextualObject   =theContextualObject, 
        theCacheName          =theCacheName, 
        theProjectName        =aProjectName,
        theLanguage           =aLanguage,
        theRoot               =None,
        theOutput             =theOutput,
        theAdditionalParams   =theAdditionalParams,
    )
            
    
    if not aProjectName:
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                <strong>
                    %(ModelDDvlPlone_Cache_MustChooseAProjectAndALanguageBeforeChoosingARoot_Title)s
                </strong>
            </font>        
        </h3>
        """ % {
            'ModelDDvlPlone_Cache_MustChooseAProjectAndALanguageBeforeChoosingARoot_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_MustChooseAProjectAndALanguageBeforeChoosingARoot_Title']),
        })
        return None
    
    
    

    if not aLanguage:
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                <strong>
                    %(ModelDDvlPlone_Cache_MustChooseALanguageInTheProjectBeforeChoosingARoot_Title)s
                </strong>
            </font>        
        </h3>
        """ % {
            'ModelDDvlPlone_Cache_MustChooseALanguageInTheProjectBeforeChoosingARoot_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_MustChooseALanguageInTheProjectBeforeChoosingARoot_Title']),
        })
        return None
    
        
    aContextualObjectURL = theContextualObject.absolute_url()
        
    aModelDDvlPloneTool_Cache     = theModelDDvlPloneTool.fModelDDvlPloneTool_Cache(     theContextualObject)        


    aBeginMillis = fMillisecondsNow()
    
    aProjectFound        = False
    aLanguageFound       = False
    someRoots            = []
    someNumEntriesByRoot = { }
    
    try:
        
        # #################
        """MUTEX LOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
                    

    
        someProjectNames = aModelDDvlPloneTool_Cache.fGetCachedProjects( theModelDDvlPloneTool, theContextualObject, theCacheName,)
        if aProjectName in someProjectNames:   
            
            aProjectFound = True
        
            someTemplatesByLanguageForProject = aModelDDvlPloneTool_Cache.fGetCachedTemplatesForProject( theModelDDvlPloneTool, theContextualObject, theCacheName, aProjectName)                              
            someLanguages = ( someTemplatesByLanguageForProject and someTemplatesByLanguageForProject.keys()) or []

            if someLanguages:
                if aLanguage in someLanguages:
                    
                    aLanguageFound = True
                    
                    someTemplatesByRootForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
                    if someTemplatesByRootForLanguage:
                        someRoots = sorted( someTemplatesByRootForLanguage.keys()) 
                        
                        for aRoot in someRoots:
                            
                            aNumEntriesInRoot = aModelDDvlPloneTool_Cache.fCountElementDependentCachedEntriesInProjectLanguageRoot( 
                                theModelDDvlPloneTool  =theModelDDvlPloneTool, 
                                theContextualObject    =theContextualObject, 
                                theCacheName           =theCacheName, 
                                theProjectName         =aProjectName, 
                                theLanguage            =aLanguage,
                                theRoot                =aRoot,
                                theEnforceThreadSafety =False,
                            )
                            
                            someNumEntriesByRoot[ aRoot] = aNumEntriesInRoot
                            
                                    
        
    finally:
        # #################
        """MUTEX UNLOCK. 
        
        """
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        aModelDDvlPloneTool_Cache.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        
        
    if not aProjectFound:   
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                %(ModelDDvlPlone_Cache_NoProjectNamedInCache_Title)s
                <strong>
                    %(aProjectName)s
                </strong>
            </font>        
        </h3>
        """ % {
            'aProjectName':                                       fCGIE( aProjectName),
            'ModelDDvlPlone_Cache_NoProjectNamedInCache_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoProjectNamedInCache_Title']),
        })
        return None
        
                
    if not aLanguageFound:   
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                %(ModelDDvlPlone_Cache_CachedProjectHasNoLanguageNamed_Title)s
                <strong>
                    %(aLanguage)s
                </strong>
            </font>        
        </h3>
        """ % {
            'aLanguage':                                                    fCGIE( aLanguage),
            'ModelDDvlPlone_Cache_CachedProjectHasNoLanguageNamed_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_CachedProjectHasNoLanguageNamed_Title']),
        })
        return None
        
    

    if not someRoots:   
        theOutput.write( """
        <br/>
        <h3>
            <font color="red">
                %(ModelDDvlPlone_Cache_NoRootsInCacheForProjectAndLanguageNamed_Title)s
                <strong>
                    %(aProjectName)s
                    &emsp;
                    &emsp;
                    %(aLanguage)s
                </strong>
            </font>        
        </h3>
        """ % {
            'aProjectName':                                                 fCGIE( aProjectName),
            'aLanguage':                                                    fCGIE( aLanguage),
            'ModelDDvlPlone_Cache_NoRootsInCacheForProjectAndLanguageNamed_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NoRootsInCacheForProjectAndLanguageNamed_Title']),
        })
        return None
    
         
    
    theOutput.write( """
    <br/>
    <h3>
    %(ModelDDvlPlone_Cache_ChooseARoot_Title)s
    </h3>
    <table class="listing" id="cidMDDCache_RootChooser_table" >
        <thead>
            <th>
                %(ModelDDvlPlone_Cache_Root_Id_Label)s
            </th>
            <th align="right" >
                %(ModelDDvlPlone_Cache_NumEntries_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Root_Path_Label)s
            </th>
            <th>
                %(ModelDDvlPlone_Cache_Root_UID_Label)s
            </th>
        </thead>
        <tbody>
    """ % {
        'ModelDDvlPlone_Cache_ChooseARoot_Title':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_ChooseARoot_Title']),
        'ModelDDvlPlone_Cache_NumEntries_Label':    fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_NumEntries_Label']),
        'ModelDDvlPlone_Cache_Root_Id_Label':       fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Root_Id_Label']),
        'ModelDDvlPlone_Cache_Root_Path_Label':     fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Root_Path_Label']),
        'ModelDDvlPlone_Cache_Root_UID_Label':      fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Root_UID_Label']),
    })

    
    
    
    unasClasesFilas = ('odd','even',)

    
    aNumRoots = len( someRoots)
    
    for aRootIndex  in range( aNumRoots):
        
        aRoot = someRoots[ aRootIndex]

        
        if aRoot:
            
            aRootId   = aRoot
            aRootPath = aRoot
            
            aRootResult = theModelDDvlPloneTool.fNewResultForElementByUID( 
                theContextualElement =theContextualObject, 
                theUID               =aRoot,
            )
            if aRootResult:
                aRootId   = aRootResult.get( 'id',   aRoot)
                aRootPath = aRootResult.get( 'path', aRoot)
                
            
            theOutput.write( """
            <tr class="MDD_Cache_Row_Root %%(row-class)s" >
                <td class="MDD_Cache_Cell_Root_id" >
                    <a id="cidMDDCache_ChooseRoot_%(aRoot)s" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s&theLanguage=%(aLanguage)s&theRoot=%(aRoot)s">
                        %(aRootId)s
                    </a>
                </td>
                <td class="MDD_Cache_Cell_NumEntries" align="right" >
                    <a id="cidMDDCache_ChooseRoot_%(aRoot)s" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s&theLanguage=%(aLanguage)s&theRoot=%(aRoot)s">
                        %(aNumEntries)d
                    </a>
                </td>
                <td class="MDD_Cache_Cell_Root_path" >
                    <a id="cidMDDCache_ChooseRoot_%(aRoot)s" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s&theLanguage=%(aLanguage)s&theRoot=%(aRoot)s">
                        %(aRootPath)s
                    </a>
                </td>
                <td class="MDD_Cache_Cell_Root_UID" >
                    <a id="cidMDDCache_ChooseRoot_%(aRoot)s" 
                        href="%(aURL)s/MDDInspectCache?theCacheName=%(theCacheName)s&theProjectName=%(aProjectName)s&theLanguage=%(aLanguage)s&theRoot=%(aRoot)s">
                        %(aRoot)s
                    </a>
                </td>
            </tr>
            """ % {
                'aRootId':      fCGIE( aRootId),
                'aRootPath':    fCGIE( aRootPath.replace('/', '/ ')),
                'aURL':         aContextualObjectURL,
                'theCacheName': fCGIE( theCacheName),
                'aProjectName': fCGIE( aProjectName),
                'aLanguage':    fCGIE( aLanguage),
                'aRoot':        fCGIE( aRoot),
                'aNumEntries':  someNumEntriesByRoot.get( aRoot, 0),
                'row-class':    unasClasesFilas[ aRootIndex % 2],
            })
            
            
    theOutput.write( """
        </tbody>
    </table>
    <br/>
    """ )
            
                 
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
  
    

    
    someSymbolsAndDefaultsToTranslate = [
        [ 'ModelDDvlPlone', [ 
            [ 'ModelDDvlPlone_Cache_Entries_Title' ,          'Cache Entries for Project, Language and Root-'],
            [ 'ModelDDvlPlone_Cache_NoEntriesInCacheForProjectNamedAndLanguage_Title' , 'No cache entries for project and language:-'],
            [ 'ModelDDvlPlone_Cache_ChooseOtherProject',      'Choose other Project-',],
            [ 'ModelDDvlPlone_Cache_ChooseOtherLanguage',     'Choose other Language-',],
            [ 'ModelDDvlPlone_Cache_ChooseOtherRoot',         'Choose other Root-',],
            [ 'ModelDDvlPlone_Cache_Entry_Action_FlushMem',   'Flush Mem.-',],
            [ 'ModelDDvlPlone_Cache_Entry_Action_FlushDisc',  'Flush Disc-',],
            [ 'ModelDDvlPlone_Cache_Project_Label',           'Project-',],
            [ 'ModelDDvlPlone_Cache_Language_Label',          'Language-',],
            [ 'ModelDDvlPlone_Cache_Root_Label',              'Root-',],
            [ 'ModelDDvlPlone_Cache_Element_Label',           'Element-',],
            [ 'ModelDDvlPlone_Cache_View_Label',              'View-',],
            [ 'ModelDDvlPlone_Cache_Relation_Label',          'Relation-',],
            [ 'ModelDDvlPlone_Cache_Current_Label',           'Current-',],
            [ 'ModelDDvlPlone_Cache_SchemeHostAndDomain_Label', 'Scheme-Host-Domain-',],
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
    <script type="text/javascript">
        function fMDDConfirmFlush( theCacheEntryId, theCacheName, thePostfix) {
            if ( window.confirm( "Do you want to Flush the  " + theCacheName + " cache entry " + theCacheEntryId + thePostfix) && window.confirm( "Do you REALLY want to Flush the cache entry " + theCacheEntryId + thePostfix)) { 
                return true;
            } 
            else { 
                return false;
            }    
        }
        
        function fMDDConfirmFlushSelected( theProjectName, theLanguage, theRoot, theCacheName, thePostfix) {
            if ( window.confirm( "Do you want to Flush the  " + theCacheName + " cache entries from Project " + theProjectName + ', Language ' + theLanguage + ' and Root ' + theRoot + thePostfix) && window.confirm( "Do you REALLY want to Flush the  " + theCacheName + " cache entries from Project " + theProjectName + ', Language ' + theLanguage + ' and Root ' + theRoot + thePostfix)) { 
                return true;
            } 
            else { 
                return false;
            }    
        }
    
    </script>
    """)
    
    
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

    

        
    aRoot    = theAdditionalParams.get( 'theRoot', '')
    
    if not aRoot:
        _fCacheDump_ForElements_RootChooser(
            theModelDDvlPloneTool =theModelDDvlPloneTool, 
            theContextualObject   =theContextualObject, 
            theCacheName          =theCacheName, 
            theOutput             =unOutput,
            theAdditionalParams   =theAdditionalParams,
        )
        return unOutput.getvalue()
    
    
    
    _fCacheDump_ForElements_Header_ProjectLanguageRoot(
        theModelDDvlPloneTool =theModelDDvlPloneTool, 
        theContextualObject   =theContextualObject, 
        theCacheName          =theCacheName, 
        theProjectName        =aProjectName,
        theLanguage           =aLanguage,
        theRoot               =aRoot,
        theOutput             =unOutput,
        theAdditionalParams   =None,
    )
    
        
    aModelDDvlPloneTool_Retrieval = theModelDDvlPloneTool.fModelDDvlPloneTool_Retrieval( theContextualObject)
    aModelDDvlPloneTool_Cache     = theModelDDvlPloneTool.fModelDDvlPloneTool_Cache(     theContextualObject)        

    

    aContextualObjectURL = theContextualObject.absolute_url()
    

    
    
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
        
    
    someErrorReports = [ ]
    
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
            <br/>
            <h3>
            %(ModelDDvlPlone_Cache_Entries_Title)s
            </h3>        
            <table class="listing" id="cidMDDCache_EntriesTable" name="cidMDDCache_EntriesTable" >
            <thead>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_Element_Label)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_View_Label)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_Relation_Label)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_Current_Label)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_SchemeHostAndDomain_Label)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_RoleOrUser_Label)s
                </th>
                <th>
                    %(ModelDDvlPlone_Cache_Entry_Action_FlushMem)s
                </th>
                <th>
                    %(ModelDDvlPlone_Cache_Entry_Action_FlushDisc)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_Entry_UniqueId)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_Entry_NumProblems)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_Entry_UniqueId_Registry)s
                </th>
                <th>
                    %(ModelDDvlPlone_Cache_Entry_UID_Registry)s
                </th>
                <th class="sortable"> 
                    %(ModelDDvlPlone_Cache_Entry_Valid)s
                </th>
                <th class="sortable">
                    %(ModelDDvlPlone_Cache_Entry_Promise)s
                </th>
                <th  class="sortable" align="right">
                    %(ModelDDvlPlone_Cache_Entry_AgeSeconds)s
                </th>
                <th align="right">
                    %(ModelDDvlPlone_Cache_Entry_Memory)s
                </th>
                <th class="sortable" align="right">
                    %(ModelDDvlPlone_Cache_Entry_Milliseconds)s
                </th>
            </thead>
            <tbody>
        """ % {
            'ModelDDvlPlone_Cache_Entries_Title':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entries_Title']),
            'ModelDDvlPlone_Cache_Entry_Action_FlushMem': fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Action_FlushMem']),
            'ModelDDvlPlone_Cache_Entry_Action_FlushDisc':fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Action_FlushDisc']),
            'ModelDDvlPlone_Cache_Project_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Project_Label']),
            'ModelDDvlPlone_Cache_Language_Label':        fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Language_Label']),
            'ModelDDvlPlone_Cache_Element_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Element_Label']),
            'ModelDDvlPlone_Cache_View_Label':            fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_View_Label']),
            'ModelDDvlPlone_Cache_Relation_Label':        fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Relation_Label']),
            'ModelDDvlPlone_Cache_Current_Label':         fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Current_Label']),
            'ModelDDvlPlone_Cache_SchemeHostAndDomain_Label':   fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_SchemeHostAndDomain_Label']),
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
        
        someTemplatesByRootForLanguage = someTemplatesByLanguageForProject.get( aLanguage, {})
        someTemplatesByUIDForRoot      = someTemplatesByRootForLanguage.get(    aRoot, {})
        
        someUIDs = (someTemplatesByUIDForRoot and someTemplatesByUIDForRoot.keys()) or [] 
        
        someUIDsElementsToRetrieve.update( someUIDs)
        
        for anUID in someUIDs:
            someTemplatesByViewForUID = someTemplatesByUIDForRoot.get( anUID, {})
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
        someUIDs = sorted( (someTemplatesByUIDForRoot and someTemplatesByUIDForRoot.keys()) or [])
        aNumUIDs = len( someUIDs)
                
        
        for anUIDIndex in range ( aNumUIDs):
            
            
            try:
                    
                anUID = someUIDs[ anUIDIndex]
                
        
                # ########################
                """Dump UID
                
                """
                    
                 
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
                
                aRowIndex += 1
                unOutput.write( unUIDString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                            
                
                # ###########################################################
                """Iterate over Views
                
                """
        
                
                someTemplatesByViewForUID = someTemplatesByUIDForRoot.get( anUID, {})
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
        
                        aRowIndex += 1
                        unOutput.write( unUIDString  % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                         
        
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
    
                            aRowIndex += 1
                            unOutput.write( unViewString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                        
                        
        
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
    
                                aRowIndex += 1
                                unOutput.write( unRelationString  % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                            
                            
            
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
                            """Iterate over Host-Domain names
                            
                            """
                            someTemplatesBySchemeHostAndDomainForRelatedUID = someTemplatesByRelatedUIDForRelation.get( aRelatedUID, {})
                            someSchemeHostAndDomains = sorted( ( someTemplatesBySchemeHostAndDomainForRelatedUID and someTemplatesBySchemeHostAndDomainForRelatedUID.keys()) or [])
                            aNumSchemeHostAndDomains = len( someSchemeHostAndDomains)
                            
                            
                            if not aNumSchemeHostAndDomains:
                           
                                unOutput.write( """
                                    <td class="MDD_Cache_Cells_Empty" colspan="%(colspan)d">&ensp;</td>
                                </tr>
                                """ % {
                                'colspan':                            aNumColumns -6,
                                })
                                    
                                continue   
                            
                            for aSchemeHostAndDomainIndex in range( aNumSchemeHostAndDomains):
                            
                                aSchemeHostAndDomain = someSchemeHostAndDomains[  aSchemeHostAndDomainIndex]
                         
                                if aSchemeHostAndDomainIndex :
        
                                    aRowIndex += 1
                                    unOutput.write( unRelatedString  % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                                
                                
                
                                # ########################
                                """Dump SchemeHostAndDomain
                                
                                """
                                unSchemeHostAndDomainString = """
                                    <td class="MDD_Cache_Cell_SchemeHostAndDomain">%(aSchemeHostAndDomain)s</td>
                                """ % {
                                    'aSchemeHostAndDomainIndex': aSchemeHostAndDomainIndex + 1,
                                    'aSchemeHostAndDomain':      fCGIE( aSchemeHostAndDomain),
                                    'aNumSchemeHostAndDomains':  aNumSchemeHostAndDomains,
                                }
                                unOutput.write( unSchemeHostAndDomainString)
        
                                unSchemeHostAndDomainString = unRelatedString + unSchemeHostAndDomainString
                              
                                      
                            
                            
                             
                                # ###########################################################
                                """Iterate over RoleOrUsers
                                
                                """
                                someTemplatesByRoleOrUserForSchemeHostAndDomain = someTemplatesBySchemeHostAndDomainForRelatedUID.get( aSchemeHostAndDomain, {})
                                someRoleOrUsers = sorted( ( someTemplatesByRoleOrUserForSchemeHostAndDomain and someTemplatesByRoleOrUserForSchemeHostAndDomain.keys()) or [])
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
                         
                                        aRowIndex += 1
                                        unOutput.write( unRelatedString % { 'row-class': unasClasesFilas[ aRowIndex % 2],})
                                    
                                    
                    
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
                                    aCacheEntry = someTemplatesByRoleOrUserForSchemeHostAndDomain.get( aRoleOrUserName, None)
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
                                            </td>
                                            <td  align="center"  class="MDD_Cache_Cell_Entry_Flush">
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
                                                
                                           
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during _fCacheDump_ForElements\n'
                if anUID:
                    unInformeExcepcion += 'UID=%s' % anUID
                    
                try:
                    unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                except:
                    None
                try:
                    unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                except:
                    None
                unInformeExcepcion += unaExceptionFormattedTraceback   
                
                someErrorReports.append( unInformeExcepcion)
                
                logging.getLogger( 'gvSIGi18n').info("EXCEPTION: exception details follow:\n%s\n" % unInformeExcepcion) 
                      
                continue
                                
        
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
                 
        if someErrorReports:
            unOutput.write( """
                <h3>%d Errors during _fCacheDump_ForElements</h3>
            """ %  len( someErrorReports),
            )
            for anErrorReport in someErrorReports:
                unOutput.write( """
                    <br/>
                    <h4>Error</h4>
                """
                )
                                
                someLines = anErrorReport.splitlines()
                for aLine in someLines:
                    unOutput.write( """
                        <span>%s</span>
                        <br/>
                    """ %  aLine,
                    )
        
                    
                    
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
            [ 'ModelDDvlPlone_Cache_Entry_Action_FlushMem',      'Flush-',],
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
                %(ModelDDvlPlone_Cache_Entry_Action_FlushMem)s
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
        'ModelDDvlPlone_Cache_Entry_Action_FlushMem':    fCGIE( someTranslations[ 'ModelDDvlPlone_Cache_Entry_Action_FlushMem']),
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
            

        