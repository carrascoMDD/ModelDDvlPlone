# -*- coding: utf-8 -*-
#
# File: MDDRenderContext.py
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




cParamsAccess_KeyNotFound_Sentinel = object()



# #######################################################################
""" ACTION AND RENDERING CONTEXT CLASS.

"""

class MDDRenderContext:
    
    
    def __init__( self, theInitialParams={}, theParentContext=None):
        
        self.vParams           = { }
        self.vRetrievalResults = [ ]
        self.vActionResults    = [ ]
        self.vChildrenContexts = [ ]
        
        if theInitialParams:
            self.vParams.update( theInitialParams)

            
            
            
            
    def fNewCtxt( self, theInitialParams={}):
        
        aNewCtxt = MDDRenderSubContext( self, theInitialParams)
        
        if self.vChildrenContexts == None:
            self.vChildrenContexts = [ ]

        self.vChildrenContexts.append( aNewCtxt)
        
        return aNewCtxt    
            
        
    
            
    def fGP( self, theParamKey, theDefault):
        
        if not theParamKey:
            return theDefault
        
        unValue = self.vParams.get( theParamKey, cParamsAccess_KeyNotFound_Sentinel)
        if unValue == cParamsAccess_KeyNotFound_Sentinel:
            return theDefault
        
        return unValue
    
    
    
    
    def pSP( self, theParamKey, theParamValue):
        
        if not theParamKey:
            return theDefault
        
        self.vParams[ theParamKey] = theParamValue
        
        return self
    
    
    
    
    
 
            
    def pAppendRetrievalResult( self, theRetrievalResult):
        
        if not theRetrievalResult:
            return self
        
        if self.vRetrievalResults == None:
            self.vRetrievalResults = [ ]
        
        self.vRetrievalResults.append( theRetrievalResult)
        
        return self
    
        
            
    def pAppendActionResult( self, theActionResult):
        
        if not theActionResult:
            return self
        
        if self.vActionResults == None:
            self.vActionResults = [ ]
        
        self.vActionResults.append( theActionResult)
        
        return self
    

         
    
    
    def fActionResults( self,):
        if self.vActionResults == None:
            return []
        
        return self.vActionResults[:]
    
                  
                   
                   
                   
                   
    def pOS( self, theString):
        aPOS = self.fGP( 'pOS', None)
        if not aPOS:
            return self
        
        aPOS( theString)
        return self
    
    
    
                   
                   
    def pOL( self, theString):
        aPOL = self.fGP( 'pOL', None)
        if not aPOL:
            return self
        
        aPOL( theString)
        return self
    
    
                    
    def pO( self, theString):
        aPO = self.fGP( 'pO', None)
        if not aPO :
            return self
        
        aPO ( theString)
        return self
    
    
    
    def fUITr( self, theSymbol):
        if not theSymbol:
            return u''
        
        someTRs   = self.fGP( 'theUITranslations', {})
        if not someTRs :
            return unicode( theSymbol)
        
        aTranslation = someTRs.get( theSymbol, cParamsAccess_KeyNotFound_Sentinel)
        if not ( aTranslation == cParamsAccess_KeyNotFound_Sentinel):
            return aTranslation

        return unicode( theSymbol)
         
    
   
    
    
        
        
class MDDRenderSubContext( MDDRenderContext):
    
    
    def __init__( self, theParentContext, theInitialParams={},):
        
        MDDRenderContext.__init__( self, theInitialParams)
        
        self.vParentContext    = theParentContext
        
        
        
    def fGP( self, theParamKey, theDefault):
        
        if not theParamKey:
            return theDefault
        
        unValue = self.vParams.get( theParamKey, cParamsAccess_KeyNotFound_Sentinel)
        if unValue == cParamsAccess_KeyNotFound_Sentinel:
            if not self.vParentContext:
                return theDefault
            return self.vParentContext.fGP( theParamKey, theDefault)
        
        return unValue
            
        
                   