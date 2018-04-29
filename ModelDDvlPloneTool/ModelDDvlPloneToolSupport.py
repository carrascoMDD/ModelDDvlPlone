# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneToolSupport.py
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

import logging

from StringIO import StringIO


from time     import time
from DateTime import DateTime

from AccessControl import ClassSecurityInfo

from Products.CMFCore import permissions

from MDDNestedContext import MDDNestedContext
from MDDLinkedList    import MDDLinkedList, MDDLinkedNode, MDDLinkedNodeWithProperties





cResultCondition_MissingParameter = 'MDDResultCondition_MissingParameter'

# ####################################################
"""Methods for safe evaluation of strings.

"""

cIndentLen = 4
cIndent = ' ' * cIndentLen


cLogEvalStringExceptions = True




cEvalStringGlobalsDict_Default = { 
    '__builtins__':None, 
    'True':  True, 
    'False': False, 
    'None':  None, 
    'DateTime': DateTime,
    'time':  time,
    'set':   set,
}
    



cEvalStringGlobalsDict_Usual = cEvalStringGlobalsDict_Default.copy()
cEvalStringGlobalsDict_Usual.update( { 
    'abs':    abs, 
    'apply':  apply,
    'basestring': basestring,
    'bool': bool,
    'buffer': buffer,
    'callable': callable,
    'chr': chr,
    'cmp': cmp,
    'coerce': coerce,
    'compile': compile,
    'complex': complex,
    'copyright': copyright,
    'credits': credits,
    'DateTime': DateTime,
    'delattr': delattr,
    'dict': dict,
    'dir': dir,
    'divmod': divmod,
    'enumerate': enumerate,
    'eval': eval,
    'execfile': execfile,
    'file': file,
    'file': filter,
    'frozenset': frozenset,
    'float': float,
    'getattr': getattr,
    'globals': globals,
    'hasattr': hasattr,
    'hash': hash,
    'help': help,
    'hex': hex,
    'id': id,
    'int': int,
    'intern': intern,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'iter': iter,
    'len': len,
    'license': license,
    'list': list,
    'locals': locals,
    'long': long,
    'map': map,
    'max': max,
    'min': min,
    'None': None,
    'object': object,
    'oct': oct,
    'open': open,
    'ord': ord,
    'pow': pow,
    'property': property,
    'range': range,
    'reduce': reduce,
    'reload': reload,
    'repr': repr,
    'reversed': reversed,
    'round': round,
    'setattr': setattr,
    'slice': slice,
    'sorted': sorted,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'type': type,
    'unichr': unichr,
    'unicode': unicode,
    'vars': vars,
    'xrange': xrange,
    'zip': zip,
})

    


cEvalStringGlobalsDict_Extra = cEvalStringGlobalsDict_Usual.copy()
cEvalStringGlobalsDict_Extra.update( { 
    'os':           os, 
})
                                     
                                     

cExtraGlobalsDicts = {
    'default': cEvalStringGlobalsDict_Default,
    'usual':   cEvalStringGlobalsDict_Usual,
    'extra':   cEvalStringGlobalsDict_Extra,
}
    






def fEvalString( theString, theExtraGlobalsDictName='default', theExtraGlobals={}, theRaiseExceptions=True):
    if not theString:
        return None
    
    if isinstance( theExtraGlobalsDictName, str) or isinstance( theExtraGlobalsDictName, str):
        unGlobalsDict = cExtraGlobalsDicts.get( theExtraGlobalsDictName, cEvalStringGlobalsDict_Default)
        if not unGlobalsDict:
            unGlobalsDict = { '__builtins__':None, }

    unGlobalsDict = unGlobalsDict.copy()

    if theExtraGlobals:
        unGlobalsDict.update( theExtraGlobals)
        if isinstance( theExtraGlobals.get( '__builtins__', None), __builtins__.__class__):                
            unGlobalsDict.pop( '__builtins__')                
        
            
    unValue = None
    
    if theRaiseExceptions:
        unValue = eval( theString, unGlobalsDict)
        
    else:
        try:
            unValue = eval( theString, unGlobalsDict)
        except:
            unGlobalsString = ', '.join( unGlobalsDict.keys())
            if cLogEvalStringExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( 'EXCEPTION during fEvalString( "%s", with globals %s)' % ( str( theString), unGlobalsString))
        
    return unValue
    






def fReprAsString( theObject):
    if ( theObject == None):
        return repr( theObject)
    
    aRepresentation = repr( theObject)
    return aRepresentation





        
        
        

# ####################################################
"""Methods to obtain ModelDDvlPlone_XXX instances.

"""

    




# ######################################
"""Time methods.

"""


def fSecondsNow():   

    return int( time())


    
def fMillisecondsNow():   

    return int( time() * 1000)



def fDateTimeNow():   
    return DateTime()




def fDateTimeAfterSeconds( theDateTime, theSeconds):

    if not theDateTime:
        return None

    if not theSeconds:
        return theDateTime
    
    unaDateTimeAfter = DateTime( ( theDateTime.millis() / 1000) + int( theSeconds))
        
    return unaDateTimeAfter

         
    
def fMillisecondsToDateTime( theMilliseconds):
    
    if not theMilliseconds:
        return None
    
    if isinstance( theMilliseconds, DateTime):
        return theMilliseconds
    
    unDateTime = None
    try:
        unDateTime = DateTime( theMilliseconds / 1000)
    except:
        None
        
    return unDateTime












# ####################################################
"""Methods to operate on nested contexts and linked lists.

"""
        
def fNewLinkedList( theContextualElement,):
    
    return MDDLinkedList()

        




    
def fNewLinkedNode(  theContextualElement,):
    
    return MDDLinkedNode()

        
    
    
def fNewLinkedNodeWithProperties( theContextualElement, theProperties):
    
    return MDDLinkedNodeWithProperties( theProperties=theProperties)

        

 
  
    
def fNewNestedContext( theContextualElement, theInitialParams={}):
    
    return MDDNestedContext( theInitialParams)

        

    
def fNewInteractionContext( theContextualElement, theInitialParams={}):
    
    return MDDNestedContext( theInitialParams)






    
def fNewRenderContext( theContextualElement, theInitialParams={}):
    
    return MDDNestedContext( theInitialParams)













    
# ##################################################################
# List / Dict conversion to a formatted multiline indented string
#        



def fPrettyPrintHTML( theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):

    aResult = fPrettyPrint( theList, theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theFindAlreadyPrinted=theFindAlreadyPrinted)
    if not aResult:
        return ''
    
    anHTMLResult = '<p>%s</p>' % aResult.replace('\n', '\n<br/>\n').replace( cIndent, '&nbsp; ' * len( cIndent))
    return anHTMLResult




def fPrettyPrint( theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):

    anOutput = StringIO()
    
    if theFindAlreadyPrinted:
        anAlreadyPrinted = { 'elements':[], 'line_numbers': [], }
    else:
        anAlreadyPrinted = None 
    
    prettyPrintList( anOutput, theList, 0, theIndentAtStart = True, theFinalComa=False, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=anAlreadyPrinted)
    aResult = anOutput.getvalue()
    
    return aResult







def fAreAllElementsStrings( theList):
    for unElement in theList:
        if not ( unElement.__class__.__name__ == 'str'):
            return False
    return True





def fAreAllElementsAllElementsStrings( theList):
    for unElement in theList:
        if not unElement.__class__.__name__ == 'list':
            return False
        
        if not fAreAllElementsStrings( unElement):
            return False
    return True






def prettyPrintList( theOutput, theList, theIndentLevel, theIndentAtStart = True, theFinalComa = True, theDictKeysToExclude=None, theDictKeysOrder=None, theAlreadyPrinted=None):
    if theIndentAtStart:
        theOutput.write(  cIndent *  theIndentLevel)
        
    theOutput.write( '[')
    
    if (not theAlreadyPrinted) or not (theList in theAlreadyPrinted[ 'elements']):
        if theAlreadyPrinted:
            theAlreadyPrinted[ 'elements'].append( theList)
            theAlreadyPrinted[ 'line_numbers'].append( len( theOutput.getvalue().splitlines()))

        unTodosStrings = fAreAllElementsStrings( theList)
        
        if unTodosStrings:
            theOutput.write( ' ')
            for unElement in theList:
                theOutput.write( "'%s', " % unElement)
            theOutput.write( "],\n")     
        else:
            if fAreAllElementsAllElementsStrings( theList):
                unosMaxWidths = []
                for unaSubList in theList:
                    for unSubElementIndex in range( 0, len( unaSubList)):
                        if len( unosMaxWidths) <= unSubElementIndex:
                            unosMaxWidths.append( 0)
                        unSubElement = unaSubList[ unSubElementIndex]
                        if len( unSubElement) > unosMaxWidths[ unSubElementIndex]:
                            unosMaxWidths[ unSubElementIndex] = len( unSubElement)    
                        
                theOutput.write( '\n')
                for unaSubList in theList:
                    theOutput.write(  cIndent *  (theIndentLevel + 1))
                    theOutput.write( '[ ')
          #        theOutput.write(  cIndent[0: len( cIndent) -1])
                    for unSubElementIndex in range( 0, len( unaSubList)):
                        unSubElement = unaSubList[ unSubElementIndex]
                        theOutput.write( "'%s', " % unSubElement)
                        if len( unSubElement) < unosMaxWidths[ unSubElementIndex]:
                            theOutput.write(  ' ' * (unosMaxWidths[ unSubElementIndex] - len( unSubElement)) )
                    theOutput.write( ' ],\n')
                    
                theOutput.write(  cIndent *  theIndentLevel)
                theOutput.write( "],\n")     

            else:
                theOutput.write( "\n") 
                for unElement in theList:
                    unElementTypeName = unElement.__class__.__name__
                    if unElementTypeName == 'str':
                        theOutput.write(  cIndent *  (theIndentLevel + 1))
                        theOutput.write( "'%s',\n" % unElement)
                    elif unElementTypeName == 'list':
                        prettyPrintList( theOutput, unElement, theIndentLevel + 1,  theIndentAtStart = True, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=theAlreadyPrinted)
                    elif unElementTypeName == 'dict':
                        prettyPrintDict( theOutput, unElement, theIndentLevel + 1, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=theAlreadyPrinted)
                    elif unElementTypeName == 'bool':
                        theOutput.write( "%s,\n" % str( unElement))
                    elif isinstance( unElement, __class__):
                        theOutput.write( "'(un %s at path %s)',\n" % (unElement.__class__.__name__, unElement.absolute_url_path()))
                    else:
                        try:
                            theOutput.write( "'%s',\n" % str( unElement))
                        except:
                            theOutput.write( "'Value with Unicode error',\n")
                        
                theOutput.write(  cIndent *  theIndentLevel)
                if theFinalComa:
                    theOutput.write( "],\n")     
                else:
                    theOutput.write( "]\n")     
    else:
        theOutput.write( "SEEABOVE line#%d]\n" % theAlreadyPrinted[ 'line_numbers'][ theAlreadyPrinted[ 'elements'].index( theList)])     
                   
    return None      







def fSortedConfigDictKeys(  theKeys, theDictKeysOrder=None):
    if not theDictKeysOrder:
        return sorted( theKeys)

    someOrderedKeys = []
    someOtherKeys = []

    for unaKey in theDictKeysOrder:
        if unaKey in theKeys:
            someOrderedKeys.append( unaKey)

    for unaKey in theKeys:
        if not( unaKey in someOrderedKeys):
            someOtherKeys.append( unaKey)
                            
    someOrderedKeys.extend( sorted( someOtherKeys))
    return someOrderedKeys
        
    




def prettyPrintDict( theOutput, theDict, theIndentLevel, theDictKeysToExclude=None, theDictKeysOrder=None, theAlreadyPrinted=None):
    theOutput.write(  cIndent *  theIndentLevel)
    theOutput.write( '{')

    if (not theAlreadyPrinted) or not (theDict in theAlreadyPrinted['elements']):
        if theAlreadyPrinted:
            theAlreadyPrinted[ 'elements'].append( theDict)
            theAlreadyPrinted[ 'line_numbers'].append( len( theOutput.getvalue().splitlines()))
        
        unasKeys = fSortedConfigDictKeys( theDict.keys(), theDictKeysOrder)
        
        unaMaxKeyLen = 0
        for unaKey in unasKeys:
            if len( unaKey) > unaMaxKeyLen:
                unaMaxKeyLen = len( unaKey)       
    
        unaFirstKey = True
        for unaKey in unasKeys:
            if (not theDictKeysToExclude) or not ( unaKey in theDictKeysToExclude):
                unElement = theDict[ unaKey]
                
                if unaFirstKey:
                    unaFirstKey = False
                    theOutput.write(  cIndent[0: len( cIndent) -1] )
                else:
                    theOutput.write(  cIndent *  (theIndentLevel + 1))
                    
                theOutput.write(  "'%s': " % unaKey)
                
                if len( unaKey) < unaMaxKeyLen:
                    theOutput.write(  ' ' * (unaMaxKeyLen - len( unaKey)) )
                     
                if unElement == None:
                    theOutput.write( "'None',\n")
                else:
                    unElementTypeName = unElement.__class__.__name__
                    if unElementTypeName == 'str':
                        theOutput.write( "'%s',\n" % unElement)
                    elif unElementTypeName == 'list':
                        prettyPrintList( theOutput, unElement, theIndentLevel + 1, theIndentAtStart = False, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=theAlreadyPrinted)
                    elif unElementTypeName == 'dict':
                        prettyPrintDict( theOutput, unElement, theIndentLevel + 1, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=theAlreadyPrinted)
                    elif unElementTypeName == 'bool':
                        theOutput.write( "%s,\n" % str( unElement))
                    #elif isinstance( unElement, type):
                        #theOutput.write( "'(un %s at path %s)',\n" % (unElement.__class__.__name__, unElement.absolute_url_path()))
                    else:
                        try:
                            theOutput.write( "'%s',\n" % str( unElement))
                        except:
                            theOutput.write( "'Value with Unicode error',\n")

    else:           
        theOutput.write( "SEEABOVE line#%d\n" % theAlreadyPrinted[ 'line_numbers'][ theAlreadyPrinted[ 'elements'].index( theDict)])     


    theOutput.write(  cIndent *  theIndentLevel)
    theOutput.write( "},\n")     
    return None

       

