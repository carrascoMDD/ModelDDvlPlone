# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Profiling.py
#
# Copyright (c) 2008 by 2008 Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Model Driven Development sl <gvSIGwhys@ModelDD.org>,
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'



import logging

from time import time


from AccessControl      import ClassSecurityInfo

from StringIO import StringIO


cIndentLen = 4
cIndent = ' ' * cIndentLen    



class ModelDDvlPloneTool_Profiling:
    """
    """
    security = ClassSecurityInfo()

   
    
    
####################################
# Time Profiling methods
#    
    
    
    security.declarePrivate('pProfilingStart')
    def pProfilingStart(self, theMethodName, theTimeProfilingResults=None):
        if theTimeProfilingResults == None:
            return self
                                           
        unCurrent =  theTimeProfilingResults.get( 'current', None)
        unNewContext = [ theMethodName, int( time() / 1000), [], unCurrent, ]
        if unCurrent:
            theTimeProfilingResults[ 'current'][2].append( unNewContext)
        theTimeProfilingResults[ 'current'] = unNewContext
       
        if not theTimeProfilingResults.has_key( 'root'):
            theTimeProfilingResults[ 'root'] = theTimeProfilingResults[ 'current']

        return self
       
       
       
       
       
    security.declarePrivate('pProfilingEnd')
    def pProfilingEnd(self, theMethodName, theTimeProfilingResults=None):
        if theTimeProfilingResults == None:
            return self
            
        if (not theTimeProfilingResults.has_key( 'current')):
            return self
            
        theTimeProfilingResults[ 'current'][ 1] = int( time() / 1000) - theTimeProfilingResults[ 'current'][ 1]
       
        if not (theMethodName == theTimeProfilingResults[ 'current'][ 0]):
            aLogger = logging.getLogger( 'ModelDDvlPloneTool::pProfilingEnd')
            aLogger.error("Profiling stack end method name does not match start name")
         
        unPreviousContext = theTimeProfilingResults[ 'current'][ 3]
        theTimeProfilingResults[ 'current'][ 3] = None
        theTimeProfilingResults[ 'current'] = unPreviousContext

       
        return self
       


# ##################################################################
# Time Profiling rendering
#        


    security.declarePrivate( 'fPrettyPrintProfilingResultHTML')
    def fPrettyPrintProfilingResultHTML(self, theProfilingResult):
    
        aResult = self.fPrettyPrintProfilingResult( theProfilingResult)
        if not aResult:
            return ''
        
        anHTMLResult = '<p>%s</p>' % aResult.replace('\n', '\n<br/>\n').replace( cIndent, '&nbsp; ' * len( cIndent))
        return anHTMLResult
        
        
        
        
    security.declarePrivate( 'fPrettyPrintProfilingResult')
    def fPrettyPrintProfilingResult(self, theProfilingResult):
    
        anOutput = StringIO()
        
        self.prettyPrintProfilingResult( anOutput, theProfilingResult, 0)
        aResult = anOutput.getvalue()
        
        return aResult
 
 

     
    
    security.declarePrivate( 'prettyPrintProfilingResult')
    def prettyPrintProfilingResult(self, theOutput, theProfilingResult, theIndentLevel):
        if not theProfilingResult:
            return self
            
        if theIndentLevel:
            theOutput.write(  cIndent *  theIndentLevel)
                    
        someSubProfilingResults = theProfilingResult[ 2]
        if not someSubProfilingResults:
            theOutput.write( '[%d %s]\n' % ( theProfilingResult[ 1], theProfilingResult[ 0]))            
        else:
            theOutput.write( '[%d %s\n' % ( theProfilingResult[ 1], theProfilingResult[ 0])) 
            
            for aSubProfilingResult in someSubProfilingResults:                       
                self.prettyPrintProfilingResult( theOutput, aSubProfilingResult, theIndentLevel + 1)
                
            if theIndentLevel:
                theOutput.write(  cIndent *  theIndentLevel)
            theOutput.write( ']\n')            
        
        return self      
       
           