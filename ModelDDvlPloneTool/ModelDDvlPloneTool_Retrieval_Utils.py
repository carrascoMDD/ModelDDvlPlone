# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval_Utils.py
#
# Copyright (c) 2008, 2009, 2010 by Model Driven Development sl and Antonio Carrasco Valero
#
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
#
# Authors: 
# Model Driven Development sl  Valencia (Spain) www.ModelDD.org 
# Antonio Carrasco Valero                       carrasco@ModelDD.org
#

__author__ = """Model Driven Development sl <ModelDDvlPlone@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'


from time import time


from AccessControl          import ClassSecurityInfo
from Products.CMFCore       import permissions


from StringIO import StringIO


cIndentLen = 4
cIndent = ' ' * cIndentLen    


class ModelDDvlPloneTool_Retrieval_Utils:
    """
    """
    security = ClassSecurityInfo()

# ##################################################################
# Accessor for timing constraints 
#        
    
    #security.declarePrivate( 'fSecondsNow')
    #def fSecondsNow(self): 
        #return int( time())
            
    
    
    #security.declarePrivate( 'fMillisecondsNow')
    #def fMillisecondsNow(self):   
        #return int( time() * 1000)
 
    
    #security.declarePrivate( 'fDateTimeNow')
    #def fDateTimeNow(self):   
        #return DateTime()
    
    
    
    
    
    
# ##################################################################
# List / Dict conversion to a formatted multiline indented string
#        




     
    
    security.declarePrivate( 'fPrettyPrintHTML')
    def fPrettyPrintHTML(self, theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):
    
        aResult = self.fPrettyPrint( theList, theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theFindAlreadyPrinted=theFindAlreadyPrinted)
        if not aResult:
            return ''
        
        anHTMLResult = '<p>%s</p>' % aResult.replace('\n', '\n<br/>\n').replace( cIndent, '&nbsp; ' * len( cIndent))
        return anHTMLResult



    security.declarePrivate( 'fPrettyPrint')
    def fPrettyPrint(self, theList, theDictKeysToExclude=None, theDictKeysOrder=None, theFindAlreadyPrinted=False):
    
        anOutput = StringIO()
        
        if theFindAlreadyPrinted:
            anAlreadyPrinted = { 'elements':[], 'line_numbers': [], }
        else:
            anAlreadyPrinted = None 
        
        self.prettyPrintList( anOutput, theList, 0, theIndentAtStart = True, theFinalComa=False, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=anAlreadyPrinted)
        aResult = anOutput.getvalue()
        
        return aResult
 
 
    
  

    
    
    security.declarePrivate( 'fAreAllElementsStrings')
    def fAreAllElementsStrings(self, theList):
        for unElement in theList:
            if not ( unElement.__class__.__name__ == 'str'):
                return False
        return True
    
    
    security.declarePrivate( 'fAreAllElementsAllElementsStrings')
    def fAreAllElementsAllElementsStrings(self, theList):
        for unElement in theList:
            if not unElement.__class__.__name__ == 'list':
                return False
            
            if not self.fAreAllElementsStrings( unElement):
                return False
        return True
   
    
    security.declarePrivate( 'prettyPrintList')
    def prettyPrintList(self, theOutput, theList, theIndentLevel, theIndentAtStart = True, theFinalComa = True, theDictKeysToExclude=None, theDictKeysOrder=None, theAlreadyPrinted=None):
        if theIndentAtStart:
            theOutput.write(  cIndent *  theIndentLevel)
            
        theOutput.write( '[')
        
        if (not theAlreadyPrinted) or not (theList in theAlreadyPrinted[ 'elements']):
            if theAlreadyPrinted:
                theAlreadyPrinted[ 'elements'].append( theList)
                theAlreadyPrinted[ 'line_numbers'].append( len( theOutput.getvalue().splitlines()))

            unTodosStrings = self.fAreAllElementsStrings( theList)
            
            if unTodosStrings:
                theOutput.write( ' ')
                for unElement in theList:
                    theOutput.write( "'%s', " % unElement)
                theOutput.write( "],\n")     
            else:
                if self.fAreAllElementsAllElementsStrings( theList):
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
    #                    theOutput.write(  cIndent[0: len( cIndent) -1])
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
                            self.prettyPrintList( theOutput, unElement, theIndentLevel + 1,  theIndentAtStart = True, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=theAlreadyPrinted)
                        elif unElementTypeName == 'dict':
                            self.prettyPrintDict( theOutput, unElement, theIndentLevel + 1, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=theAlreadyPrinted)
                        elif unElementTypeName == 'bool':
                            theOutput.write( "%s,\n" % str( unElement))
                        elif isinstance( unElement, self.__class__):
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
                       
        return self      


    
    security.declarePrivate( 'fSortedConfigDictKeys')
    def fSortedConfigDictKeys( self, theKeys, theDictKeysOrder=None):
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
            
        
  
    security.declarePrivate( 'prettyPrintDict')
    def prettyPrintDict(self, theOutput, theDict, theIndentLevel, theDictKeysToExclude=None, theDictKeysOrder=None, theAlreadyPrinted=None):
        theOutput.write(  cIndent *  theIndentLevel)
        theOutput.write( '{')
    
        if (not theAlreadyPrinted) or not (theDict in theAlreadyPrinted['elements']):
            if theAlreadyPrinted:
                theAlreadyPrinted[ 'elements'].append( theDict)
                theAlreadyPrinted[ 'line_numbers'].append( len( theOutput.getvalue().splitlines()))
            
            unasKeys = self.fSortedConfigDictKeys( theDict.keys(), theDictKeysOrder)
            
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
                         
                    unElementTypeName = unElement.__class__.__name__
                    if unElementTypeName == 'str':
                        theOutput.write( "'%s',\n" % unElement)
                    elif unElementTypeName == 'list':
                        self.prettyPrintList( theOutput, unElement, theIndentLevel + 1, theIndentAtStart = False, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=theAlreadyPrinted)
                    elif unElementTypeName == 'dict':
                        self.prettyPrintDict( theOutput, unElement, theIndentLevel + 1, theDictKeysToExclude=theDictKeysToExclude, theDictKeysOrder=theDictKeysOrder, theAlreadyPrinted=theAlreadyPrinted)
                    elif unElementTypeName == 'bool':
                        theOutput.write( "%s,\n" % str( unElement))
                    elif isinstance( unElement, self.__class__):
                        theOutput.write( "'(un %s at path %s)',\n" % (unElement.__class__.__name__, unElement.absolute_url_path()))
                    else:
                        try:
                            theOutput.write( "'%s',\n" % str( unElement))
                        except:
                            theOutput.write( "'Value with Unicode error',\n")
    
        else:           
            theOutput.write( "SEEABOVE line#%d\n" % theAlreadyPrinted[ 'line_numbers'][ theAlreadyPrinted[ 'elements'].index( theDict)])     
    
    
        theOutput.write(  cIndent *  theIndentLevel)
        theOutput.write( "},\n")     
        return self
    
           
    
    
