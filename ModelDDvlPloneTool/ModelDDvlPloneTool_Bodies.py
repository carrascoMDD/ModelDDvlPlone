# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Bodies.py
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



import locale

from Products.CMFCore.utils             import getToolByName

from AccessControl                      import ClassSecurityInfo

from reStructuredText                   import HTML

from Acquisition                        import aq_inner

from StringIO import StringIO





from ModelDDvlPloneTool_Profiling       import ModelDDvlPloneTool_Profiling

from PloneElement_TraversalConfig       import cPloneTypes 
  
from ModelDDvlPloneTool_Retrieval       import ModelDDvlPloneTool_Retrieval






cReplaceWithPortalURLslashedMark              = '|replace_with_portal_url_slashed|'
cEditableBody_ReusedRestDefinitions_i18n_view = 'EditableBody_ReusedRestDefinitions_i18n_view'
     


class ModelDDvlPloneTool_Bodies ( ModelDDvlPloneTool_Profiling):
    """
    """
    security = ClassSecurityInfo()




 

# #############################################################
# Editable Body Generation methods
#


 
    security.declarePrivate('fEditableBodyBlock_MetaTypeIcons')
    def fEditableBodyBlock_MetaTypeIcons(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Produce a REST structute defining substitutions for icons for all meta types.
        
        """
        
        unOutput= StringIO( u'')
        
            
        unPortalURL = ModelDDvlPloneTool_Retrieval().fPortalURL( theElement)
        if not unPortalURL:
            unPortalURL = ''
        else:
            if not ( unPortalURL[-1:] == '/'):
                unPortalURL = '%s/' % unPortalURL
            
        
        unosRestHeaders = self.getEditableBody_forLevel_WithTemplate( theElement, cEditableBody_ReusedRestDefinitions_i18n_view, theLevel=1, theTimeProfilingResults=theTimeProfilingResults)
        if unosRestHeaders:
        
            unosRestHeadersWithPortalURLReplacements = unosRestHeaders.replace( cReplaceWithPortalURLslashedMark, unPortalURL)
            unOutput.write( unosRestHeadersWithPortalURLReplacements)
            
            
        for unPloneMetaType in sorted( cPloneTypes.keys()):
            unPloneIcon = cPloneTypes.get( unPloneMetaType, {}).get( 'content_icon', '')
            if unPloneIcon:
                unOutput.write( '\n\n.. |PloneIcon_%s| image:: %s%s\n\n' % ( unPloneMetaType, unPortalURL, unPloneIcon,))
                
        if theElement == None:
            return unOutput.getvalue()
        
        someClassNames = []
        try:
            someClassNames = theElement.fArchetypeClassNames( )
        except:
            None
            
        if not someClassNames:
            return unOutput.getvalue()
        
        
        for aClassName in someClassNames:
            unArchetypeClass = theElement.fArchetypeClassByName( aClassName)
            if unArchetypeClass:
                unIcon = None
                try:
                    unIcon = unArchetypeClass.content_icon
                except:
                    None
                if unIcon:
                    unOutput.write( '\n\n.. |MDDIcon_%s| image:: %s%s\n\n' % ( aClassName, unPortalURL, unIcon,))
        
        return unOutput.getvalue()
    
    
    
      

    security.declarePrivate('fEditableBodyForElement')
    def fEditableBodyForElement(self, 
        theTimeProfilingResults =None,
        theElement              =None,
        theAdditionalParams     =None):
        """Retrieve a REST presentation of an element's content as a Textual view.
        
        """

        return self.getEditableBody_forLevel(  theElement, theLevel=1, theTimeProfilingResults=theTimeProfilingResults)
        
      
      
    security.declarePrivate('getEditableBody_forLevel')
    def getEditableBody_forLevel( self, theElement, theLevel=1, theTimeProfilingResults=None):
        
        return self.getEditableBody_forLevel_WithTemplate( theElement, "EditableBody_i18n_view", theLevel=1, theTimeProfilingResults=theTimeProfilingResults)
 
      
   

    security.declarePrivate('getEditableBody_forLevel_WithTemplate')
    def getEditableBody_forLevel_WithTemplate( self, theElement, theTemplateName='',theLevel=1, theTimeProfilingResults=None):
        
        if not theTemplateName:
            return "\n\n**No template name parameter to render getEditableBody_forLevel_WithTemplate**\n\n"

        if ( theElement == None):
            return "\n\n**No theElement supplied to render EditableBody**\n\n"

        aTemplate   = theElement.unrestrictedTraverse( theTemplateName)
 
        if not aTemplate:
            return "\n\n**No template EditableBody_i18n_view.pt found to render getEditableBody**\n\n"
        
        aContext = aq_inner( theElement)
       
        aTemplateInContext = aTemplate.__of__(aContext)

        # ACV 20091004 Still fails with characters that do not fit cp1252
        #
        #aContentTypeHeaders = aContext.REQUEST.RESPONSE.headers['content-type']
        #aUnicodeContentHeaders = aContentTypeHeaders.replace(';charset=utf-8', '')
        #aContext.REQUEST.RESPONSE.headers['content-type'] = aUnicodeContentHeaders
        
        try:
            anEditableBodyString = aTemplateInContext(aContext, aContext.REQUEST, theLevel=theLevel)        
        finally:
            # ACV 20091004 Still fails with characters that do not fit cp1252
            #
            #aContext.REQUEST.RESPONSE.headers['content-type'] = aContentTypeHeaders
            None

        
        aCleanEditableBodyString = anEditableBodyString.replace('<tal>', '').replace('</tal>', '').replace('<div>', '').replace('</div>', '')
         
#        aCleanEditableBodyString = "aContext.REQUEST.RESPONSE.headers['content-type']= %s\n\n\n" % str( aContentTypeHeaders) + aCleanEditableBodyString
#        aCleanEditableBodyString = "locale.getpreferredencoding()= %s\n\n\n" % str( locale.getpreferredencoding())   + aCleanEditableBodyString
        
        # ACV 20091004 Still fails with characters that do not fit cp1252
        #
        #aPreferredEncoding = locale.getpreferredencoding()
        #if aPreferredEncoding.startswith("ANSI"):
            #aPreferredEncoding = 'cp1252'     
         
        aPreferredEncoding = 'utf-8'
        aUnicodeEditableBodyString =  unicode( aCleanEditableBodyString, aPreferredEncoding, errors="replace")
        return aUnicodeEditableBodyString
        
    


    security.declarePrivate('fCompositeEditableBodyForElement')
    def fCompositeEditableBodyForElement(self, theElement, theTimeProfilingResults=None):
        return self.getCompositeEditableBody_forLevel(  theElement, theLevel=1, theTimeProfilingResults=theTimeProfilingResults)
        
      
      
      
      
      
      
        
        
    security.declarePrivate('getCompositeEditableBody_forLevel')
    def getCompositeEditableBody_forLevel(self, theElement, theLevel=1, theTimeProfilingResults=None):
        
        aTraversalConfig = theElement.getTraversalConfig()
        if not aTraversalConfig:
            return []
            

        anEditableBodyString = self.getEditableBody_forLevel( theElement, theLevel, theTimeProfilingResults) 
        aCleanEditableBodyString = anEditableBodyString.replace('<tal>', '').replace('</tal>', '').replace('<div>', '').replace('</div>', '')
         
        return aCleanEditableBodyString
  
  



    security.declarePrivate( 'fCookedBodyForElement')
    def fCookedBodyForElement(self, 
        theTimeProfilingResults =None,
        theElement              =None, 
        stx_level               =None, 
        setlevel                =0,
        theAdditionalParams     =None):
        """Retrieve an HTML presentation of an element's content as a Textual view.
        
        """
        
        if ( theElement == None):
            return '\n<em>No Element</em><br/>\n\n'
        
        # From CMFDefault.Document.py see Products.PortalTransforms.Transforms.rest.py
        
        anEditableBody = self.fEditableBodyForElement( theTimeProfilingResults, theElement, theTimeProfilingResults)
        if not anEditableBody:
            return "\n<em>No EditableBody obtained for %s</em><br/>\n\n" % str( self)

        aCookedBody = HTML( anEditableBody, initial_header_level=1, input_encoding='utf-8', output_encoding='utf-8')
   
        if not anEditableBody:
            return "\n<em>Empty HTML obtained for CookedBody for %s</em>\n\n" % str( self)

        aCookedBodyReClassed = aCookedBody.replace( 'class="docutils"', 'class="listing"').replace( 'class="head"', 'class="nosort"')

        return aCookedBodyReClassed






    security.declarePrivate( 'fCompositeCookedBodyForElement')
    def fCompositeCookedBodyForElement(self, 
        theElement,
        stx_level=None, 
        setlevel=0, 
        theTimeProfilingResults=None):
        
        if ( theElement == None):
            return '\n<em>No Element</em><br/>\n\n'
        
        
        # From CMFDefault.Document.py see Products.PortalTransforms.Transforms.rest.py
        
        anEditableBody = self.fCompositeEditableBodyForElement( theElement)
        if not anEditableBody:
            return "\n<em>No EditableBody obtained for %s</em><br/>\n\n" % str( self)

        aCookedBody = HTML( anEditableBody, initial_header_level=1, input_encoding='utf-8', output_encoding='utf-8')
   
        if not anEditableBody:
            return "\n<em>Empty HTML obtained for CookedBody for %s</em>\n\n" % str( self)

        aCookedBodyReClassed = aCookedBody.replace( 'class="docutils"', 'class="listing"').replace( 'class="head"', 'class="nosort"')

        return aCookedBodyReClassed
   
        









        

