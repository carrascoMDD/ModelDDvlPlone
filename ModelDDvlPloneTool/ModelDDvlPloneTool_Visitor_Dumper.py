# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Visitor_Dumper.py
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

import logging

import StringIO

from AccessControl                  import ClassSecurityInfo
from Products.CMFCore.utils         import getToolByName
from Products.CMFPlone.i18nl10n     import utranslate


_gCentinela= object()

class ModelDDvlPloneTool_Visitor_Dumper:
    """
    """
    security = ClassSecurityInfo()

    
    vTitleAdornments = '''=-`:.'"~^_*+#'''
    vExtendTitleChar = "-"  
    vIndent          = "    "

    vBeDummy                = False
    vBeJustCollectHeaders   = False
    
    vTranslationService     = None
    
    
    def getTranslationService( self):
        if self.vTranslationService:
            return self.vTranslationService
            
        aTranslationService = getToolByName( self, 'translation_service', _gCentinela)
        if not( aTranslationService is _gCentinela):
            self.vTranslationService = aTranslationService
        
        return self.vTranslationService
        
        
    
# #########################
#  Setup methods
#
    
    security.declarePrivate( 'setBeDummy')
    def setBeDummy( self, theBeDummy):
        self.vBeDummy = (theBeDummy == True)
        return self
        
    
    security.declarePrivate( 'setBeJustCollectHeaders')
    def setBeJustCollectHeaders( self, theBeJustCollectHeaders):
        self.vBeJustCollectHeaders = (theBeJustCollectHeaders == True)
        return self
            
    
# #########################
#  Conversion methods
#



    def quotedAttrValue( self, theAttrType, theValue):
        if theValue is None:
            return 'None'
            
        unStrValue = str( theValue)
        
        if theAttrType == 'Number' or theAttrType == 'Boolean':
            return unStrValue
       
        if not( "\n" in unStrValue):
            unQuotedValue = "'%s'" % unStrValue
            return unQuotedValue
            
        unEscapedValue = unStrValue.replace("\n", "\\n")
        unQuotedValue = "'''%s'''" % unStrValue
        return unQuotedValue    



    

# ###############################################################
#  Section header uniqueness and level adjustment methods
#


    def fSectionHeaderAndAdornment( self, theTravCtxt, theObject, theTitle, theTitleObjectMode):
        if (self.vBeDummy == True):
            return None
       
        if not theTitle:
            return None
            
        if (not self.vBeJustCollectHeaders) and theTravCtxt.has_key( 'reuse_headers') and theTravCtxt[ 'reuse_headers'] == True and theObject:
            return self.fSectionHeaderAndAdornmentReusingTitles( theTravCtxt, theObject, theTitle, theTitleObjectMode)
        else:
            return self.fSectionHeaderAndAdornmentBuildTheHeader( theTravCtxt, theObject, theTitle, theTitleObjectMode)
  
     
     
 
 
    def fSectionHeaderAndAdornmentReusingTitles( self, theTravCtxt, theObject, theTitle, theTitleObjectMode):
        if (self.vBeDummy == True):
            return None
       
        if ( theObject == None):
            return None

                                    
        unTitleAndAdornment = self.fSectionHeaderAndAdornmentReusedForObjectStack( theTravCtxt, theObject, theTitle)                 
        if unTitleAndAdornment:
            return unTitleAndAdornment
        
        return u"COULD NOT REUSE so builded it " + fSectionHeaderAndAdornmentBuildTheHeader( theTravCtxt, theObject, theTitle)
     
     
     
    def fStackFramesString( self, theTravCtxt, theObject):
        unStackPath = ""
        unStackObject = None
        for unStackFrame in theTravCtxt[ 'stack']:
            unStackObject = unStackFrame[ 0]
            if unStackObject:
                unStackObjectPath = unStackObject.fPhysicalPathString()
                unStackPath += "::"
                unStackPath += unStackObjectPath
     
        if theObject and unStackObject and not( theObject == unStackObject):
            unObjectPath = theObject.fPhysicalPathString()
            unStackPath += "::"
            unStackPath += unObjectPath     
            
        return unStackPath
        
        
        

    def fSectionHeaderAndAdornmentBuildTheHeader( self, theTravCtxt, theObject, theTitle, theTitleObjectMode):
        if (self.vBeDummy == True):
            return None
       
        if not theTitle:
            return None
            
        unTitle = self.fAsUnicode( theTravCtxt, theTitle)
        unTitle = unTitle.replace(u".", u" ").replace(u"_", u" ")
        
        someTitleHeaders = theTravCtxt[ 'titleHeaders']
        unNumHeaders = 1
        if someTitleHeaders.has_key( unTitle):
            unNumHeaders = someTitleHeaders[ unTitle]
            unTitle += self.vExtendTitleChar * unNumHeaders
            unNumHeaders += 1
        
        someTitleHeaders[ theTitle] = unNumHeaders
        
        unLevel = theTravCtxt.get( 'titleLevel', 0)
        if unLevel < 0:
            unLevel = 0
        unNumTitleAdornments = len( self.vTitleAdornments)
        unAdornmentChar = self.vTitleAdornments[ unLevel % unNumTitleAdornments]
        unTitleAdornment = unAdornmentChar * len( unTitle)
        
        unTitleAndAdornmentAndLevel = [ unTitle, unTitleAdornment, unLevel, theTitleObjectMode]
        
        if theObject:
            unStackPath = self.fStackFramesString( theTravCtxt, theObject)
           
            if not theTravCtxt[ 'reusableTitlesByStackPaths'].has_key( unStackPath):
                theTravCtxt[ 'reusableTitlesByStackPaths'][ unStackPath] = unTitleAndAdornmentAndLevel
                        
            unObjectPath = theObject.fPhysicalPathString()
            if theTravCtxt[ 'reusableTitlesByObjectPath'].has_key( unObjectPath):
                unFoundTitleAndAdornmentAndLevel = theTravCtxt[ 'reusableTitlesByObjectPath'][ unObjectPath]
                
                unFoundLevel    = unFoundTitleAndAdornmentAndLevel[ 2]
                unFoundMode     = unFoundTitleAndAdornmentAndLevel[ 3]
                if unFoundLevel < unLevel and ( not (theTitleObjectMode == 'Reference') or (unFoundMode =='Reference')):
                    theTravCtxt[ 'reusableTitlesByObjectPath'][ unObjectPath] = unTitleAndAdornmentAndLevel  
            else:
                theTravCtxt[ 'reusableTitlesByObjectPath'][ unObjectPath] = unTitleAndAdornmentAndLevel  
                                    
        return unTitleAndAdornmentAndLevel
 
 
 
 

  
  

    def fSectionHeaderAndAdornmentReusedForObjectStack( self, theTravCtxt, theObject, theTitle):
        if (self.vBeDummy == True):
            return None
       
        if ( theObject == None):
            return None


        unLevel = theTravCtxt.get( 'titleLevel', 0)
        if unLevel < 0:
            unLevel = 0                                        

        unStackPath = ""
        for unStackFrame in theTravCtxt[ 'stack']:
            unStackObject = unStackFrame[ 0]
            if unStackObject:
                unStackObjectPath = unStackObject.fPhysicalPathString()
                unStackPath += "::"
                unStackPath += unStackObjectPath


        unObjectPath = theObject.fPhysicalPathString()
        
        if not theTravCtxt[ 'reusableTitlesByStackPaths'].has_key( unStackPath):
            return None
        
        unTitleAndAdornment = theTravCtxt[ 'reusableTitlesByStackPaths'][ unStackPath]                 
        
        return unTitleAndAdornment

  
   
   

    def fSectionHeaderAndAdornmentForObject( self, theTravCtxt, theObject):
        if (self.vBeDummy == True):
            return None
       
        if ( theObject == None):
            return None

        unLevel = theTravCtxt.get( 'titleLevel', 0)
        if unLevel < 0:
            unLevel = 0

        unObjectPath = theObject.fPhysicalPathString()  
        if not theTravCtxt[ 'reusableTitlesByObjectPath'].has_key( unObjectPath):
            return None
 
        unTitleAndAdornment = theTravCtxt[ 'reusableTitlesByObjectPath'][ unObjectPath]                 
        
        return unTitleAndAdornment

  
        
    

# #########################
#  Output methods
#



    security.declarePrivate( 'pO_break')
    def pO_break( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self





    security.declarePrivate( 'pO_divider')
    def pO_divider( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n--------------------------------\n\n")
        return self

   
    security.declarePrivate( 'pO_white')
    def pO_white( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n|\n|\n\n")
        return self

   



    security.declarePrivate( 'pO_inicio')
    def pO_inicio( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self
    
    
    
    

    security.declarePrivate( 'pO_fin')
    def pO_fin( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self

   


    security.declarePrivate( 'pO_object_begin')
    def pO_object_begin( self, theTravCtxt, theObject):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self





    
   
    security.declarePrivate( 'pO_object_end')
    def pO_object_end( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self
    
   





   
    security.declarePrivate( 'pO_attrs_begin')
    def pO_attrs_begin( self, theTravCtxt ):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self






   
    security.declarePrivate( 'pO_title')
    def pO_title( self, theTravCtxt, theTypeConfig, theObject, theAttrConfigMetaAndValue):
        if (self.vBeDummy == True):
            return self

        if theTravCtxt is None or theTypeConfig is None or theObject is None or theAttrConfigMetaAndValue is None is None:
            return self

        unAttrConfig      = theAttrConfigMetaAndValue[ 0]
        unMetaAndValue    = theAttrConfigMetaAndValue[ 1] 
        someExtraOptions  = theAttrConfigMetaAndValue[ 2] 
        
        unAttrTargetType    = unAttrConfig[1]
        someAttrOptions     = unAttrConfig[2:]
    
        unAttrName              = unMetaAndValue[ 0]
        unAttrValue             = unMetaAndValue[ 1]
        unAttrLabel             = unMetaAndValue[ 2]
        unAttrLabelMsgId        = unMetaAndValue[ 3]
        unAttrDescription       = unMetaAndValue[ 4]
        unAttrDescriptionMsgId  = unMetaAndValue[ 5]
        unAttrType              = unMetaAndValue[ 6]
    
    
    
        if not unAttrValue:
            return self
        
        unTitle = self.fAsUnicode( theTravCtxt, unAttrValue)
        
        if 'Translate' in someAttrOptions:
            unTitle = self.fTranslateI18N( theTravCtxt, u"", unTitle, unTitle)  
                        
        if 'OneParagraph' in someExtraOptions:
            if 'Reference' in someExtraOptions:

                aHyperlinkTarget  =  self.fHyperlinkTargetNameToIncluded( theTravCtxt, theObject)
                if aHyperlinkTarget:
                    aHyperlinkedTitle = "`%s`_" % aHyperlinkTarget.strip()     
                    self.pO( theTravCtxt, "%s\n" % aHyperlinkedTitle)
                    return self 

            aHyperlinkTarget  = self.fHyperlinkTargetNameToOriginal( theTravCtxt, theObject)
            unTitle = unTitle.replace(u".", u" ").replace(u"_", u" ").strip()
            
            unTitle = self.fAsUnicode( theTravCtxt, unTitle)
            
            aHyperlinkedTitle = u"`%s <%s>`__" % ( unTitle, aHyperlinkTarget)        
            self.pO( theTravCtxt, u"%s\n" % aHyperlinkedTitle)

            return self
        


        
        unTitleObjectMode = 'Content'
        if 'Reference' in someExtraOptions:
            unTitleObjectMode = 'Reference'
        unSectionHeaderAndAdornment = self.fSectionHeaderAndAdornment( theTravCtxt, theObject, unTitle, unTitleObjectMode)
        if not unSectionHeaderAndAdornment or len( unSectionHeaderAndAdornment) < 2:
            return self
            
        unUniqueTitle = unSectionHeaderAndAdornment[ 0]
        unAdornment   = unSectionHeaderAndAdornment[ 1]

            
        if 'Reference' in someExtraOptions:
            aHyperlinkTarget =  self.fHyperlinkTargetNameToIncluded( theTravCtxt, theObject)
            aHyperlinkedTitle = u"`%s`_" % aHyperlinkTarget.strip()
             
            aHyperlinkedTitle = self.fAsUnicode( theTravCtxt, aHyperlinkedTitle)
            
            aHyperlinkedTitleAdornment = unAdornment[ 0] * len( aHyperlinkedTitle)
            self.pO( theTravCtxt, u"%s\n" % aHyperlinkedTitle)
            self.pO( theTravCtxt, u"%s\n" % aHyperlinkedTitleAdornment)
            self.pO( theTravCtxt, u"\n")
        else:
            aHyperlinkTarget = self.fHyperlinkTargetNameToOriginal( theTravCtxt, theObject)
            aHyperlinkedTitle = u"`%s <%s>`__" % ( unUniqueTitle, aHyperlinkTarget)
             
            aHyperlinkedTitle = self.fAsUnicode( theTravCtxt, aHyperlinkedTitle)
            
            aHyperlinkedTitleAdornment = unAdornment[ 0] * len( aHyperlinkedTitle)
            self.pO( theTravCtxt, u"%s\n" % aHyperlinkedTitle)
            self.pO( theTravCtxt, u"%s\n" % aHyperlinkedTitleAdornment)
            self.pO( theTravCtxt, u"\n")
                
        return self
               
                            
               
               
               
               
    def fHyperlinkTargetNameToIncluded( self, theTravCtxt, theObject):
        unSectionHeaderAndAdornment = self.fSectionHeaderAndAdornmentForObject( theTravCtxt, theObject)
        if not unSectionHeaderAndAdornment or len( unSectionHeaderAndAdornment) < 2:
            return ""
        unUniqueTitle = unSectionHeaderAndAdornment[ 0]
        return unUniqueTitle               
               
               
               
               
                
    def fHyperlinkTargetNameToOriginal( self, theTravCtxt, theObject):
        aURL = theObject.absolute_url()
        aURL = aURL.replace(" ", "%20")
        return aURL               
               
              
               
    security.declarePrivate( 'pO_description')
    def pO_description( self, theTravCtxt, theTypeConfig, theObject, theAttrConfigMetaAndValue):
        if (self.vBeDummy == True):
            return self

        if theTravCtxt is None or theTypeConfig is None or theObject is None or theAttrConfigMetaAndValue is None is None:
            return self

        unAttrConfig       = theAttrConfigMetaAndValue[ 0]
        unMetaAndValue     = theAttrConfigMetaAndValue[ 1] 
        someExtraOptions   = theAttrConfigMetaAndValue[ 2] 
        
        unAttrTargetType    = unAttrConfig[1]
        someAttrOptions     = unAttrConfig[2:]
    
        unAttrName              = unMetaAndValue[ 0]
        unAttrValue             = unMetaAndValue[ 1]
        unAttrLabel             = unMetaAndValue[ 2]
        unAttrLabelMsgId        = unMetaAndValue[ 3]
        unAttrDescription       = unMetaAndValue[ 4]
        unAttrDescriptionMsgId  = unMetaAndValue[ 5]
        unAttrType              = unMetaAndValue[ 6]
    
        if not unAttrValue:
            return self
           
        unAttrValue = self.fAsUnicode( theTravCtxt, unAttrValue)
          
        self.pO( theTravCtxt, u"%s\n" % unAttrValue)
        
        if not ( 'OneParagraph' in someExtraOptions):
            self.pO( theTravCtxt, u"\n")
                
        return self
               
                                   
            

    security.declarePrivate( 'pO_attr_meta')
    def pO_attr_meta( self, theTravCtxt, theTypeConfig, theObject, theAttrConfigMetaAndValue):
        if (self.vBeDummy == True):
            return self

        if theTravCtxt is None or theTypeConfig is None or theObject is None or theAttrConfigMetaAndValue is None is None:
            return self

        unAttrConfig      = theAttrConfigMetaAndValue[ 0]
        unMetaAndValue    = theAttrConfigMetaAndValue[ 1] 
        someExtraOptions  = theAttrConfigMetaAndValue[ 2] 
        
        unAttrTargetType    = unAttrConfig[1]
        someAttrOptions     = unAttrConfig[2:]
    
        unAttrName              = unMetaAndValue[ 0]
        unAttrValue             = unMetaAndValue[ 1]
        unAttrLabel             = unMetaAndValue[ 2]
        unAttrLabelMsgId        = unMetaAndValue[ 3]
        unAttrDescription       = unMetaAndValue[ 4]
        unAttrDescriptionMsgId  = unMetaAndValue[ 5]
        unAttrType              = unMetaAndValue[ 6]
    
        if not unAttrValue:
            return self
        
        
        if 'Class' in someAttrOptions:
            aTranslatedValue = self.fTranslateI18N( theTravCtxt, "", unAttrValue, unAttrValue)
            self.pO( theTravCtxt, u"(*%s*) \n" % aTranslatedValue.strip())
        else: 
            unAttrValue = self.fAsUnicode( theTravCtxt, unAttrValue)
            self.pO( theTravCtxt, u"%s\n" % unAttrValue)

        if not ( 'OneParagraph' in someExtraOptions):
            self.pO( theTravCtxt, u"\n")
                
        return self
               
                                   
       


  
   
   
    security.declarePrivate( 'pO_attr_nonText')
    def pO_attr_nonText( self, theTravCtxt, theTypeConfig, theObject, theAttrConfigMetaAndValue):
        if (self.vBeDummy == True):
            return self

        if theTravCtxt is None or theTypeConfig is None or theObject is None or theAttrConfigMetaAndValue is None is None:
            return self

        unAttrConfig      = theAttrConfigMetaAndValue[ 0]
        unMetaAndValue    = theAttrConfigMetaAndValue[ 1] 
        someExtraOptions  = theAttrConfigMetaAndValue[ 2] 
        
        unAttrTargetType    = unAttrConfig[1]
        someAttrOptions     = unAttrConfig[2:]
    
        unAttrName              = unMetaAndValue[ 0]
        unAttrValue             = unMetaAndValue[ 1]
        unAttrLabel             = unMetaAndValue[ 2]
        unAttrLabelMsgId        = unMetaAndValue[ 3]
        unAttrDescription       = unMetaAndValue[ 4]
        unAttrDescriptionMsgId  = unMetaAndValue[ 5]
        unAttrType              = unMetaAndValue[ 6]
    
        if unAttrType == "boolean":
            if unAttrValue:
                aTranslatedEs = self.fTranslateI18N( theTravCtxt, "ModelDDvlPlone", "ModelDDvlPlone_predicado_Es", "Es")
                aTranslatedLabel = self.fTranslateI18N( theTravCtxt, "", unAttrLabelMsgId, unAttrLabel)
                self.pO( theTravCtxt, u"*%s  %s*.\n" % (aTranslatedEs.strip(), aTranslatedLabel.strip(), ))
            else:
                aTranslatedNoEs = self.fTranslateI18N( theTravCtxt, "ModelDDvlPlone", "ModelDDvlPlone_predicado_NoEs", "No es")
                aTranslatedLabel = self.fTranslateI18N( theTravCtxt, "", unAttrLabelMsgId, unAttrLabel)
                self.pO( theTravCtxt, u"*%s  %s*.\n" % (aTranslatedNoEs.strip(), aTranslatedLabel.strip(), ))
        else:
            if not unAttrValue:
                if 'Optional' in someAttrOptions:
                    return self
                else:
                    aTranslatedNoTiene = self.fTranslateI18N( theTravCtxt, "ModelDDvlPlone", "ModelDDvlPlone_predicado_NoTiene", "No tiene")
                    aTranslatedLabel = self.fTranslateI18N( theTravCtxt, "", unAttrLabelMsgId, unAttrLabel)
                    self.pO( theTravCtxt, u"%s *%s*.\n" % (aTranslatedNoTiene.strip(), aTranslatedLabel.strip(),) )
            else:
                if 'Class' in someAttrOptions:
                    aTranslatedValue = self.fTranslateI18N( theTravCtxt, "", unAttrValue, unAttrValue)
                    self.pO( theTravCtxt, u"(*%s*)\n" % aTranslatedValue.strip())
                else:
                    aTranslatedLabel = self.fTranslateI18N( theTravCtxt, "", unAttrLabelMsgId, unAttrLabel)
            
                    unAttrValue = self.fAsUnicode( theTravCtxt, unAttrValue)
                    
                    self.pO( theTravCtxt, u"*%s* %s.\n" % (aTranslatedLabel.strip(), unAttrValue.strip(), ))
        
        if not ( 'OneParagraph' in someExtraOptions):
            self.pO( theTravCtxt, "\n")
                
        return self
               
                    
            









   
    security.declarePrivate( 'pO_attr_text')
    def pO_attr_text( self, theTravCtxt, theTypeConfig, theObject, theAttrConfigMetaAndValue):
        if (self.vBeDummy == True):
            return self

        if theTravCtxt is None or theTypeConfig is None or theObject is None or theAttrConfigMetaAndValue is None is None:
            return self

        unAttrConfig      = theAttrConfigMetaAndValue[ 0]
        unMetaAndValue    = theAttrConfigMetaAndValue[ 1] 
        someExtraOptions  = theAttrConfigMetaAndValue[ 2] 
        
        unAttrTargetType    = unAttrConfig[1]
        someAttrOptions     = unAttrConfig[2:]
        
        unIsOneParagraph = 'OneParagraph' in someExtraOptions
    
        unAttrName              = unMetaAndValue[ 0]

        unAttrValue             = unMetaAndValue[ 1]
        unAttrLabel             = unMetaAndValue[ 2]
        unAttrLabelMsgId        = unMetaAndValue[ 3]
        unAttrDescription       = unMetaAndValue[ 4]
        unAttrDescriptionMsgId  = unMetaAndValue[ 5]
        unAttrType              = unMetaAndValue[ 6]
    
        if not unAttrValue and  ( 'Optional' in someAttrOptions):
            return self

        

        unUseLabel = not ( 'HideLabel' in someAttrOptions)
        if unUseLabel:
            unAttrLabelTranslated = self.fTranslateI18N( theTravCtxt, "", unAttrLabelMsgId, unAttrLabel)  
            if unAttrLabelTranslated:
                if not unIsOneParagraph:
                    self.pO( theTravCtxt, u"\n")
                self.pO( theTravCtxt, u"**%s**\n" % unAttrLabelTranslated.strip())        
                if not unIsOneParagraph:
                    self.pO( theTravCtxt, u"\n")
        
        unAttrValue = self.fAsUnicode( theTravCtxt, unAttrValue)
        
        if unAttrValue:
            if theTravCtxt.has_key( 'useSubitemsAndRelateds') and theTravCtxt[ 'useSubitemsAndRelateds'] == True and theTravCtxt.has_key( 'subitemsAndRelatedsByObjectPath'):
                someSubitemsAndRelatedsByObjectPath = theTravCtxt[ 'subitemsAndRelatedsByObjectPath']
                anObjectPath = theObject.fPhysicalPathString()
                if someSubitemsAndRelatedsByObjectPath.has_key( anObjectPath):
                    anObjectSubitemsAndRelateds = someSubitemsAndRelatedsByObjectPath[ anObjectPath]

                    unNewAttrValue = self.fAsUnicode( theTravCtxt, unAttrValue)
                    
                    unScanIndex = 0
                    unLenAttrValue = len( unAttrValue)
                    while unScanIndex < unLenAttrValue:
                        unPostfixIndex = unAttrValue.find('`_', unScanIndex)
                        if unPostfixIndex <= 1:
                            break
                            
                        unPrefixIndex = unPostfixIndex - 1
                        while unPrefixIndex >= unScanIndex and not unAttrValue[ unPrefixIndex] == '`':
                            unPrefixIndex -= 1    
                        
                        aReferencedObjectTitle = ""        
                        if unAttrValue[ unPrefixIndex] == '`' and (unPostfixIndex - unPrefixIndex) > 1:
                            aReferencedObjectTitle = unAttrValue[ unPrefixIndex + 1: unPostfixIndex]
                            unScanIndex = unPostfixIndex + 2
                        else:
                            break
                            
                        if aReferencedObjectTitle:
                            aFoundReferenced = None
                            for unSubitemOrRelated in anObjectSubitemsAndRelateds:
                                unSubitemOrRelatedTitle = unSubitemOrRelated.Title()
                                unSubitemOrRelatedTitle = self.fAsUnicode( theTravCtxt, unSubitemOrRelatedTitle)
                                if not unSubitemOrRelatedTitle:
                                    unSubitemOrRelatedTitle = unSubitemOrRelated.title_or_id()
                                    unSubitemOrRelatedTitle = self.fAsUnicode( theTravCtxt, unSubitemOrRelatedTitle)
                                if unSubitemOrRelatedTitle == aReferencedObjectTitle:
                                    aFoundReferenced = unSubitemOrRelated
                                    break    
                            
                            if aFoundReferenced:
                                
                               if aFoundReferenced.meta_type == 'ATLink':
                                    aHyperlinkTarget  =  aFoundReferenced.getRemoteUrl()
                                    aHyperlinkTarget = self.fAsUnicode( theTravCtxt, aHyperlinkTarget)
                                    unPrevAttrValue = ""
                                    while not (unPrevAttrValue == unNewAttrValue):
                                        unPrevAttrValue = unNewAttrValue
                                        unNewAttrValue = unNewAttrValue.replace(u"`%s`_" % unSubitemOrRelatedTitle, u"`%s <%s>`__" % (unSubitemOrRelatedTitle, aHyperlinkTarget, ))
                                    
                               else:                            
                                    aHyperlinkTarget  =  self.fHyperlinkTargetNameToIncluded( theTravCtxt, aFoundReferenced)
                                    if aHyperlinkTarget:
                                        unPrevAttrValue = ""
                                        while not (unPrevAttrValue == unNewAttrValue):
                                            unPrevAttrValue = unNewAttrValue
                                            unNewAttrValue = unNewAttrValue.replace(u"`%s`_" % unSubitemOrRelatedTitle, u"`%s`_" % aHyperlinkTarget)
                                    else:
                                        aHyperlinkTarget  =  self.fHyperlinkTargetNameToOriginal( theTravCtxt, aFoundReferenced)
                                        aHyperlinkTarget = self.fAsUnicode( theTravCtxt, aHyperlinkTarget)
                                        if aHyperlinkTarget:
                                            unPrevAttrValue = ""
                                            while not (unPrevAttrValue == unNewAttrValue):
                                                unPrevAttrValue = unNewAttrValue
                                                unNewAttrValue = unNewAttrValue.replace(u"`%s`_" % unSubitemOrRelatedTitle, u"`%s <%s>`__" % ( unSubitemOrRelatedTitle, aHyperlinkTarget))
                                        else:
                                            unPrevAttrValue = ""
                                            while not (unPrevAttrValue == unNewAttrValue):
                                                unPrevAttrValue = unNewAttrValue
                                                unNewAttrValue = unNewAttrValue.replace(u"`%s`_" % unSubitemOrRelatedTitle, u"(ref:) %s" % unSubitemOrRelatedTitle)
                    
                    unAttrValue = unNewAttrValue                    
                    unAttrValue = self.fAsUnicode( theTravCtxt, unAttrValue)
                    
        
            self.pO( theTravCtxt, u"%s\n" % unAttrValue)
            if not unIsOneParagraph:
                self.pO( theTravCtxt, u"\n")

        return self






    security.declarePrivate( 'pO_attrs_end')
    def pO_attrs_end( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self


   


   
    security.declarePrivate( 'pO_subitems_begin')
    def pO_subitems_begin( self, theTravCtxt, theTitleI18Nmsg):
        if (self.vBeDummy == True):
            return self
        if not theTravCtxt:
            return self

        if not theTitleI18Nmsg:
            return self

        unaLabel            = theTitleI18Nmsg[ 'label']
        unaLabelMsgId       = theTitleI18Nmsg[ 'label_msgid']
        unaDescription      = theTitleI18Nmsg[ 'description']
        unaDescriptionMsgId = theTitleI18Nmsg[ 'description_msgid']
        
        aTranslatedLabel        = self.fTranslateI18N( theTravCtxt, "", unaLabelMsgId,       unaLabel)
        # aTranslatedDescription  = self.fTranslateI18N( theTravCtxt, "", unaDescriptionMsgId, unaDescription)
       
        unSectionHeaderAndAdornment = self.fSectionHeaderAndAdornment( theTravCtxt, None, aTranslatedLabel, "")
        if not unSectionHeaderAndAdornment or len( unSectionHeaderAndAdornment) < 2:
            return self
            
        unUniqueTitle = unSectionHeaderAndAdornment[ 0]
        unAdornment   = unSectionHeaderAndAdornment[ 1]
        
        unUniqueTitle = self.fAsUnicode( theTravCtxt, unUniqueTitle)
        unAdornment   = self.fAsUnicode( theTravCtxt, unAdornment)

        if theTravCtxt[ 'titleLevel'] <= 4:
            self.pO_white( theTravCtxt)
         
        self.pO( theTravCtxt, unUniqueTitle)
        self.pO( theTravCtxt, u"\n")
        self.pO( theTravCtxt, unAdornment)
        self.pO( theTravCtxt, u"\n\n")

        return self






    security.declarePrivate( 'pO_subitems_end')
    def pO_subitems_end( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self


   

  
   
   


   
    security.declarePrivate( 'pO_relations_begin')
    def pO_relations_begin( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
            
        if theTravCtxt[ 'titleLevel'] <= 4:
            self.pO_white( theTravCtxt)
            
        self.pO( theTravCtxt, u"\n\n")
        return self






    security.declarePrivate( 'pO_relations_end')
    def pO_relations_end( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self
        self.pO( theTravCtxt, u"\n\n")
        return self




    security.declarePrivate( 'pO_relation')
    def pO_relation_begin( self, theTravCtxt, theRelationConfig, theSourceObject, theReferenceMeta):
        if (self.vBeDummy == True):
            return self
        if not theRelationConfig or not theSourceObject or not theReferenceMeta:
            return self            
            
        if not( theRelationConfig.has_key( 'relation_name')):
            return self            
        unRelationName = theRelationConfig[ 'relation_name']
        if not unRelationName:
            return self
        
        unaLabel            = theReferenceMeta[ 2]
        unaLabelMsgId       = theReferenceMeta[ 3]
        unaDescription      = theReferenceMeta[ 4]
        unaDescriptionMsgId = theReferenceMeta[ 5]
        
        aTranslatedLabel        = self.fTranslateI18N( theTravCtxt, "", unaLabelMsgId,       unaLabel)
        # aTranslatedDescription  = self.fTranslateI18N( theTravCtxt, "", unaDescriptionMsgId, unaDescription)
       
        unSectionHeaderAndAdornment = self.fSectionHeaderAndAdornment( theTravCtxt, None, aTranslatedLabel, "")
        if not unSectionHeaderAndAdornment or len( unSectionHeaderAndAdornment) < 2:
            return self
            
        unUniqueTitle = unSectionHeaderAndAdornment[ 0]
        unAdornment   = unSectionHeaderAndAdornment[ 1]
         
        unUniqueTitle = self.fAsUnicode( theTravCtxt, unUniqueTitle)
        unAdornment = self.fAsUnicode( theTravCtxt, unAdornment)

        self.pO( theTravCtxt, unUniqueTitle)
        self.pO( theTravCtxt, u"\n")
        self.pO( theTravCtxt, unAdornment)
        self.pO( theTravCtxt, u"\n\n")

        return self  
  


  
  
    security.declarePrivate( 'pO_relation')
    def pO_relation( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self   
        self.pO( theTravCtxt, u"\n\n")
        return self  
  
  
    security.declarePrivate( 'pO_relation')
    def pO_relation_end( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self   
        self.pO( theTravCtxt, u"\n\n")
        return self  
  
  


   
    security.declarePrivate( 'pO_relations_begin')
    def pO_annex_begin( self, theTravCtxt):
        if (self.vBeDummy == True):
            return self

        self.pO( theTravCtxt,  u"\n\n|\n|\n\n|\n|\n\n--------\n\n|\n|\n\n--------\n\n" )
        anAnnexTitle = self.fTranslateI18N( theTravCtxt, "ModelDDvlPlone", "ModelDDvlPlone_annex_section_title", "ModelDDvlPlone_annex_section_title")
        anAnnexUnderline = u"=" * len( anAnnexTitle)
        
        self.pO( theTravCtxt,  u"%s\n" % anAnnexTitle)
        self.pO( theTravCtxt,  anAnnexUnderline)

        self.pO( theTravCtxt,  u"\n|\n|\n\n|\n|\n")

        return self





# #########################
#  Stream methods
#



    security.declarePrivate( 'pO')
    def pO( self, theTravCtxt, theString):
        if (self.vBeDummy == True):
            return self
        
        if (self.vBeJustCollectHeaders == True):
            return self
        
        aO = theTravCtxt[ 'output']
        if not theString.__class__.__name__ == 'unicode':
            xxx = 3 + 1
        aO.write( theString)
        
        return self





           
           
           
           


# ###########################################
#  Internationalisation methods
#
    security.declarePrivate( 'fTranslateI18N')
    def fTranslateI18N( self, theTravCtxt, theI18NDomain, theString, theDefault):
        if not theString:
            return ''

        if (self.vBeDummy == True):
            return theString        

            
        if not theTravCtxt:
            return theString
            
        if not theTravCtxt.has_key( 'stack'):
            return theString

        aStack =  theTravCtxt['stack']
        if not aStack or len( aStack) < 1:
            return theString
       
        aStackFrame = aStack[ len( aStack) - 1]
        if not aStackFrame or len( aStackFrame) < 1:
            return theString
            
        aContextualObject = aStackFrame[ 0]
        
        aI18NDomain = theI18NDomain
        if not aI18NDomain:
            try:
                aI18NDomain = aContextualObject.getNombreProyecto()
            except:
                None
                
        if not aI18NDomain:
            aI18NDomain = "plone"
             
             
        aTranslation = theDefault
        aTranslationService = aContextualObject.translation_service
        if aTranslationService:
           aTranslation = aTranslationService.utranslate( aI18NDomain, theString, mapping=None, context=aContextualObject , target_language= None, default=theDefault)            
           
        if not aTranslation:
            aTranslation = theDefault

        if not aTranslation:
            aTranslation = theString

        return aTranslation
        
           
             
      

# ###########################################
#  Character set methods
#

    security.declarePrivate( 'fAsUnicode')
    def fAsUnicode( self, theTravCtxt, theString):
        if not theString:
            return ''

        if (self.vBeDummy == True):
            return theString        

            
        if not theTravCtxt:
            return theString
 
        if not theTravCtxt.has_key( 'stack'):
            return theString

        aStack =  theTravCtxt['stack']
        if not aStack or len( aStack) < 1:
            return theString
       
        aStackFrame = aStack[ len( aStack) - 1]

        aContextualObject = aStackFrame[ 0]
        aTranslationService = aContextualObject.translation_service

        aUnicodeString = aTranslationService.asunicodetype( theString, errors="ignore")
        if not aUnicodeString:
            aUnicodeString = theString
        
        return aUnicodeString