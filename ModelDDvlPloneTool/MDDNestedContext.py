# -*- coding: utf-8 -*-
#
# File: MDDNestedContext.py
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



from AccessControl import ClassSecurityInfo



_cParamsAccess_KeyNotFound_Sentinel = object()



# #######################################################################
""" ACTION AND RENDERING CONTEXT CLASS.

"""

class MDDNestedContext:
    
    security = ClassSecurityInfo()

    
    def __init__( self, theInitialParams={}, theParentContext=None):
        
        self.vParams           = { }
        self.vRetrievalResults = [ ]
        self.vActionResults    = [ ]
        self.vExceptionReports = [ ]

        self.vChildrenContexts = [ ]
        
        if theInitialParams:
            self.vParams.update( theInitialParams)

            
            
            
    security.declarePublic( 'pSPs')            
    def pSPs( self, theParams):
        
        if not theParams:
            return self
        
        self.vParams.update( theParams)
        
        return self
    
    
    
                
            
    security.declarePublic( 'fNewCtxt')        
    def fNewCtxt( self, theInitialParams={}):
        
        aNewCtxt = MDDNestedSubContext( self, theInitialParams)
        
        if self.vChildrenContexts == None:
            self.vChildrenContexts = [ ]

        self.vChildrenContexts.append( aNewCtxt)
        
        return aNewCtxt    
            
        
    
            
    security.declarePublic( 'fGP')        
    def fGP( self, theParamKey, theDefault=None):
        
        if not theParamKey:
            return theDefault
        
        unValue = self.vParams.get( theParamKey, _cParamsAccess_KeyNotFound_Sentinel)
        if unValue == _cParamsAccess_KeyNotFound_Sentinel:
            return theDefault
        
        return unValue
    
    
    
    

    security.declarePublic( 'fGPlocal')        
    def fGPlocal( self, theParamKey, theDefault=None):
        return fGPlocal( theParamKey, theDefault)
    

    
    
    
    
    security.declarePublic( 'fGP_AndCacheLocal')        
    def fGP_AndCacheLocal( self, theParamKey, theDefault=None):
        return self.fGP( theParamKey, theDefault)
    
    
    
    security.declarePublic( 'pSP')            
    def pSP( self, theParamKey, theParamValue):
        
        if not theParamKey:
            return self
        
        self.vParams[ theParamKey] = theParamValue
        
        return self
    
    
    
    security.declarePublic( 'pSPGlobal')            
    def pSPGlobal( self, theParamKey, theParamValue):
        
        self.pSP( theParamKey, theParamValue)
        
        return self
        
    
    
 
            
    security.declarePublic( 'pAppendRetrievalResult')            
    def pAppendRetrievalResult( self, theRetrievalResult):
        
        if not theRetrievalResult:
            return self
        
        if self.vRetrievalResults == None:
            self.vRetrievalResults = [ ]
        
        self.vRetrievalResults.append( theRetrievalResult)
        
        return self
    
        
    security.declarePublic( 'pAppendActionResult')                    
    def pAppendActionResult( self, theActionResult):
        
        if not theActionResult:
            return self
        
        if self.vActionResults == None:
            self.vActionResults = [ ]
        
        self.vActionResults.append( theActionResult)
        
        return self
    

        
    security.declarePublic( 'pAppendExceptionReport')                    
    def pAppendExceptionReport( self, theExceptionReport):
        
        if not theExceptionReport:
            return self
        
        if self.vExceptionReports == None:
            self.vExceptionReports = [ ]
        
        self.vExceptionReports.append( theExceptionReport)
        
        return self
    
         
    
    
    security.declarePublic( 'fActionResults')        
    def fActionResults( self,):
        if self.vActionResults == None:
            return []
        
        return self.vActionResults[:]
    
                  
                   
                   
                   
                   
    security.declarePublic( 'pOS')        
    def pOS( self, theString):
        aPOS = self.fGP_AndCacheLocal( 'pOS', None)
        if not aPOS:
            return self
        
        aPOS( theString)
        return self
    
    
    
                   
                   
    security.declarePublic( 'pOL')        
    def pOL( self, theString):
        aPOL = self.fGP_AndCacheLocal( 'pOL', None)
        if not aPOL:
            return self
        
        aPOL( theString)
        return self
    
    
                    
    security.declarePublic( 'pO')        
    def pO( self, theString):
        aPO = self.fGP_AndCacheLocal( 'pO', None)
        if not aPO :
            return self
        
        aPO ( theString)
        return self
    
    
    
    security.declarePublic( 'fUITr')        
    def fUITr( self, theSymbol):
        if not theSymbol:
            return u''
        
        someTRs   = self.fGP_AndCacheLocal( 'theUITranslations', {})
        if not someTRs :
            return unicode( theSymbol)
        
        aTranslation = someTRs.get( theSymbol, _cParamsAccess_KeyNotFound_Sentinel)
        if not ( aTranslation == _cParamsAccess_KeyNotFound_Sentinel):
            return aTranslation

        return unicode( theSymbol)
         
    
   
    
    
        
        
class MDDNestedSubContext( MDDNestedContext):
    
    
    security = ClassSecurityInfo()

    
    def __init__( self, theParentContext, theInitialParams={},):
        
        MDDNestedContext.__init__( self, theInitialParams)
        
        self.vParentContext    = theParentContext
        
        
        
    security.declarePublic( 'fGP')        
    def fGP( self, theParamKey, theDefault=None):
        
        if not theParamKey:
            return theDefault
        
        unValue = self.vParams.get( theParamKey, _cParamsAccess_KeyNotFound_Sentinel)
        if not ( unValue == _cParamsAccess_KeyNotFound_Sentinel):
            return unValue
        
        if not self.vParentContext:
            return theDefault
   
        return self.vParentContext.fGP( theParamKey, theDefault)
        
            
    

    security.declarePublic( 'fGPlocal')        
    def fGPlocal( self, theParamKey, theDefault=None):
        return MDDNestedContext.fGP( self, theParamKey, theDefault)
    
    
        
  
        
        
    security.declarePublic( 'pSPGlobal')        
    def pSPGlobal( self, theParamKey, theParamValue):
        if not self.vParentContext:
            self.pSP( theParamKey, theParamValue)
            
        self.vParentContext.pSPGlobal( theParamKey, theParamValue)
        
        return self
    
    
    
    
    security.declarePublic( 'fGP_AndCacheLocal')        
    def fGP_AndCacheLocal( self, theParamKey, theDefault=None):
        if not theParamKey:
            return theDefault
        
        unValue = self.vParams.get( theParamKey, _cParamsAccess_KeyNotFound_Sentinel)
        
        if not( unValue == _cParamsAccess_KeyNotFound_Sentinel):
            return unValue
        
        if not self.vParentContext:
            return theDefault
        
        unValue = self.vParentContext.fGP( theParamKey, _cParamsAccess_KeyNotFound_Sentinel)
        if unValue == _cParamsAccess_KeyNotFound_Sentinel:
            return theDefault
        
        self.vParams[ theParamKey] = unValue
        
        return unValue
    
        