# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval_I18N.py
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


from AccessControl       import ClassSecurityInfo

import logging

import sys
import traceback


class ModelDDvlPloneTool_Retrieval_I18N:
    """
    """
    security = ClassSecurityInfo()






    security.declarePrivate('fNewVoidAttributeTranslationResult')
    def fNewVoidAttributeTranslationResult(self):
        unResult = { 
            'label':                        '',
            'description' :                 '', 
            'translated_label':             '', 
            'translated_label_msgid':       '', 
            'translated_description':       '', 
            'translated_description_msgid': '', 
            'translated_label_and_value':   '',
            'i18ndomain':                   '',
        }
        return unResult   
   

    
    security.declarePrivate('fNewVoidObjectTranslationResult')
    def fNewVoidObjectTranslationResult(self):
        unObjectTranslationResult = {
            'meta_type':                    '',
            'archetype_name' :              '', 
            'type_description':             '', 
            'translated_archetype_name':    '', 
            'archetype_name_msgid':         '',
            'translated_type_description':  '', 
            'type_description_msgid':       '', 
            'content_icon':                 '',
        }
        return unObjectTranslationResult
    

    
    
    
# ###########################################
#  Internationalisation methods
#
    security.declarePrivate( 'fTranslateI18N')
    def fTranslateI18N( self, theI18NDomain, theString, theDefault, theContextualElement):
        if not theString:
            return ''

        if ( theContextualElement == None) :
            return theDefault

        aI18NDomain = self.fTranslationI18NDomain( theI18NDomain, theContextualElement)
        if not aI18NDomain:
            return theDefault
             
        aTranslation = theDefault
        
        aTranslationService = None
        try:
            aTranslationService = theContextualElement.translation_service
        except:
            None
            
        if aTranslationService:
            aTranslation = aTranslationService.utranslate( aI18NDomain, theString, mapping=None, context=theContextualElement , target_language= None, default=theDefault)                       
            if not aTranslation:
                aTranslation = theDefault

        if not aTranslation:
            aTranslation = theString

        return aTranslation
        
           

    security.declarePrivate( 'fTranslationI18NDomain')
    def fTranslationI18NDomain( self, theI18NDomain, theElement=None):

        aI18NDomain = theI18NDomain
        if not aI18NDomain:
            if theElement:
                try:
                    aI18NDomain = theElement.getNombreProyecto()
                except:
                    None
            if not aI18NDomain:
                aI18NDomain = 'ModelDDvlPlone'
                
        if not aI18NDomain:
            aI18NDomain = "plone"
            
        return aI18NDomain



# ###########################################
#  I10N dates internacionalization  methods
#


    security.declarePrivate( 'fTranslateMonth')
    def fTranslateMonth( self, theMonthNumber, theContextualElement):
        if not theMonthNumber or theMonthNumber < 1 or theMonthNumber > 12:
            return ''

        aDefaultTranslation = str( theMonthNumber)

        if ( theContextualElement == None) :
            return aDefaultTranslation
        
        aTranslationService = None
        try:
            aTranslationService = theContextualElement.translation_service
        except:
            None
        if not aTranslationService:
            return aDefaultTranslation               
            
        aMonthMsgId = aTranslationService.month_msgid( theMonthNumber)
        if not aMonthMsgId:
            return aDefaultTranslation               

        aTranslation = aTranslationService.utranslate( 'plone', aMonthMsgId, mapping=None, context=theContextualElement , target_language= None, default=aDefaultTranslation)                       
        if not aTranslation:
            aTranslation = aDefaultTranslation

        return aTranslation






    security.declarePrivate( 'fTranslateDayOfWeek')
    def fTranslateDayOfWeek( self, theDayOfWeek, theContextualElement):
        if not theDayOfWeek:
            return ''

        aDefaultTranslation = str( theDayOfWeek)
        

        if ( theContextualElement == None) :
            return aDefaultTranslation
        
        aTranslationService = None
        try:
            aTranslationService = theContextualElement.translation_service
        except:
            None
        if not aTranslationService:
            return aDefaultTranslation               
        
        someWeekDaysEnglish = [ aTranslationService.weekday_english( aWeekDayNumber) for aWeekDayNumber in range( 0, 7) ]
        if not (theDayOfWeek in someWeekDaysEnglish):
            return aDefaultTranslation               

        unDayIndex = someWeekDaysEnglish.index( theDayOfWeek)                    
            
        aDayMsgId = aTranslationService.day_msgid( unDayIndex)
        if not aDayMsgId:
            return aDefaultTranslation               

        aTranslation = aTranslationService.utranslate( 'plone', aDayMsgId, mapping=None, context=theContextualElement , target_language= None, default=aDayMsgId)                       
        if not aTranslation:
            aTranslation = aDefaultTranslation

        return aTranslation






    security.declarePrivate( 'fTranslateAllMonths')
    def fMonthsVocabularyTranslations( self,  theContextualElement):
        
        
        if ( theContextualElement == None) :
            return []

        aTranslationService = None
        try:
            aTranslationService = theContextualElement.translation_service
        except:
            None
        if not aTranslationService:
            return []  
            
        unVocabularyTranslations = []
                         
        for unMonthNumber in range( 1, 13):    
            aMonthMsgId = aTranslationService.month_msgid( unMonthNumber)
            if aMonthMsgId:
                aMonthTranslation = aTranslationService.utranslate( 'plone', aMonthMsgId, mapping=None, context=theContextualElement , target_language= None, default=aMonthMsgId)                       
                if aMonthTranslation:
                    unVocabularyTranslations.append( { 'option': unMonthNumber, 'translation':  aMonthTranslation, } )

        return unVocabularyTranslations




    security.declarePrivate( 'fTranslateAllDaysOfWeek')
    def fDaysOfWeekVocabularyTranslations( self,  theContextualElement):
                
        if ( theContextualElement == None) :
            return []

        aTranslationService = None
        try:
            aTranslationService = theContextualElement.translation_service
        except:
            None
        if not aTranslationService:
            return []  
                         
        unVocabularyTranslations = []
        for unDayNumber in range( 0, 7):    
            aDayMsgId = aTranslationService.day_msgid( unDayNumber)
            if aDayMsgId:
                aDayOfWeekTranslation = aTranslationService.utranslate( 'plone', aDayMsgId, mapping=None, context=theContextualElement , target_language= None, default=aDayMsgId)                       
                if aDayOfWeekTranslation:
                    unVocabularyTranslations.append( { 'option': unDayNumber, 'translation':  aDayOfWeekTranslation, } )

        return unVocabularyTranslations




# ###########################################
#  Character set methods
#

    security.declarePrivate( 'fAsUnicode')
    def fAsUnicode( self, theString, theElement=None):
        if not theString:
            return u''

        aTranslationService = None
        try:
            aTranslationService = theElement.translation_service
        except:
            None
            
         
        if not aTranslationService:
            return theString
        
        aUnicodeString = aTranslationService.asunicodetype( theString, errors="ignore")            
        if not aUnicodeString:
            return theString
        
        return aUnicodeString
    
    
    
    

    
    
    
    
    security.declarePrivate( 'fCreateTranslationsCaches')
    def fCreateTranslationsCaches( self):
        unTranslationsCache = {
            'types_translations_cache'      : { },
            'vocabulary_translations_cache' : { },
            'true_translation':               None,
            'false_translation':              None
        }
        return unTranslationsCache
    
    
    
    
    
# ###########################################
#  Translated element access methods
#


   
   
   
    
    security.declarePrivate( 'getTranslationsFromMetaTypeName')
    def getTranslationsFromMetaTypeName(self, theMetaTypeName, theContextualElement):
        
        if not theMetaTypeName or ( theContextualElement == None):
                return []
        
        unArchetypeClass = theContextualElement.fArchetypeClassByName( theMetaTypeName)
        if not unArchetypeClass:
                return []
            
        unArchetypeName             = theMetaTypeName
        unTypeDescription           = theMetaTypeName
        unPluralName                = theMetaTypeName
        unTranslatedArchetypeName   = theMetaTypeName
        unTranslatedDescription     = theMetaTypeName
        unArchetypeNameMsgId        = ''
        unTypeDescriptionMsgId      = ''
        unContentIcon               = ''
         
        unObjectTranslationResult = self.fNewVoidObjectTranslationResult()
        unObjectTranslationResult.update( {
            'meta_type':                    theMetaTypeName,
            'archetype_name' :              unArchetypeName, 
            'type_description':             unTypeDescription, 
            'translated_archetype_name':    unTranslatedArchetypeName, 
            'archetype_name_msgid':         '',
            'translated_type_description':  unTranslatedDescription, 
            'type_description_msgid':       '', 
            'content_icon':                 '',   
        })

            
        try:
            unArchetypeName        = unArchetypeClass.archetype_name
        except:
            None
        try:
            unTypeDescription      = unArchetypeClass.typeDescription
        except:
            None
        try:
            unArchetypeNameMsgId    = unArchetypeClass.archetype_name_msgid            
        except:
            None            
        try:
            unTypeDescriptionMsgId  = unArchetypeClass.typeDescMsgId
        except:
            None
        try:
            unContentIcon  = unArchetypeClass.content_icon
        except:
            None
                   
            
        unTranslatedArchetypeName  = ''
        unActualArchetypeNameMsgId = ''
        if unArchetypeNameMsgId:
            unTranslatedArchetypeName = self.fTranslateI18N( None, unArchetypeNameMsgId, '', theContextualElement)     
            if unTranslatedArchetypeName:
                unActualArchetypeNameMsgId = unArchetypeNameMsgId
        if not unTranslatedArchetypeName:     
            unTranslatedArchetypeName = self.fTranslateI18N( None, unArchetypeName, '', theContextualElement)
            if unTranslatedArchetypeName:
                unActualArchetypeNameMsgId = unArchetypeName
        if not unTranslatedArchetypeName:     
            unTranslatedArchetypeName = unArchetypeName
            
        unTranslatedTypeDescription  = ''
        unActualTypeDescriptionMsgId = ''
        if unTypeDescriptionMsgId:
            unTranslatedTypeDescription = self.fTranslateI18N( None, unTypeDescriptionMsgId,    '', theContextualElement)        
            if unTranslatedTypeDescription:
                unActualTypeDescriptionMsgId = unTypeDescriptionMsgId
        if not unTranslatedTypeDescription:     
            unTranslatedDescription = unTypeDescription

        unObjectTranslationResult.update( {
            'archetype_name' :              unArchetypeName, 
            'type_description':             unTypeDescription, 
            'translated_archetype_name':    unTranslatedArchetypeName, 
            'archetype_name_msgid':         unActualArchetypeNameMsgId,
            'translated_type_description':  unTranslatedTypeDescription, 
            'type_description_msgid':       unActualTypeDescriptionMsgId, 
            'content_icon':                 unContentIcon,         
        })
        
        return unObjectTranslationResult        



    security.declarePrivate( 'getAttributeTranslationResultFromDomainAndMsgids')
    def getAttributeTranslationResultFromDomainAndMsgids(self, theI18NDomain, theLabelMsgId, theLabelDefault, theDescriptionMsgId, theDescriptionDefault, theContextualObject):
        if not theI18NDomain or not theLabelMsgId or ( theContextualObject == None):
            return None
        
        aLabelDefault = theLabelDefault
        if not aLabelDefault:
            aLabelDefault = theLabelMsgId

        aDescriptionDefault = theDescriptionDefault
        if not aDescriptionDefault:
            aDescriptionDefault = theDescriptionMsgId
            
        unAttributeTranslationResult = self.fNewVoidAttributeTranslationResult( )
        
        unTranslatedLabel        = self.fTranslateI18N( theI18NDomain, theLabelMsgId,       aLabelDefault,       theContextualObject)
        unTranslatedDescription  = unTranslatedLabel
        if theDescriptionMsgId:
            unTranslatedDescription  = self.fTranslateI18N( theI18NDomain, theDescriptionMsgId, aDescriptionDefault, theContextualObject)
        
        unAttributeTranslationResult.update( {
            'label':                        unTranslatedLabel,
            'description' :                 unTranslatedDescription, 
            'translated_label':             unTranslatedLabel, 
            'translated_label_msgid':       theLabelMsgId, 
            'translated_description':       unTranslatedDescription, 
            'translated_description_msgid': theDescriptionMsgId, 
            'translated_label_and_value':   unTranslatedLabel,
            'i18ndomain':                   theI18NDomain,            
        } )

        return unAttributeTranslationResult
    
    
    
    security.declarePrivate( 'getPloneTypeTranslationResultFromMsgIdMetatypeAndArchetype')
    def getPloneTypeTranslationResultFromMsgIdMetatypeAndArchetype(self, theMsgId, theMetaType, theArchetypeName, theContextualObject):
        if not theMsgId or not theMetaType or ( theContextualObject == None):
            return None
        
        unTypeTranslation = self.fNewVoidObjectTranslationResult()

        unDefault = theArchetypeName
        if not unDefault:
            unDefault = theMsgId
            
        unTranslatedArchetypeName  = self.fTranslateI18N( 'plone', theMsgId,  unDefault, theContextualObject)

        unTypeTranslation.update( {
            'meta_type':                    theMetaType,
            'archetype_name' :              theArchetypeName,
            'type_description':             unTranslatedArchetypeName, 
            'translated_archetype_name':    unTranslatedArchetypeName, 
            'archetype_name_msgid':         theMsgId,
            'translated_type_description':  unTranslatedArchetypeName, 
            'type_description_msgid':       theMsgId, 
        })
                
        return unTypeTranslation
    
    

    security.declarePrivate( 'getTranslationsForDefaultAttributes')
    def getTranslationsForDefaultAttributes(self, theContextualObject):
        unosAttributeTranslations = {}
        
        unI18NDomain        = 'ModelDDvlPlone'
        unaLabel            = 'title'
        unActualLabelMsgId  = 'ModelDDvlPlone_titulo_label'
        unTranslatedLabel   = self.fTranslateI18N( unI18NDomain, unActualLabelMsgId, unaLabel, theContextualObject)
        unaDescription      = ''
        unActualDescriptionMsgId = 'ModelDDvlPlone_titulo_help'
        unTranslatedDescription   = self.fTranslateI18N( unI18NDomain, unActualDescriptionMsgId, unTranslatedLabel, theContextualObject)
        unAttributeTranslationResult = self.fNewVoidAttributeTranslationResult( )
        unAttributeTranslationResult.update( {
            'label':                        unaLabel,
            'description' :                 unaDescription, 
            'translated_label':             unTranslatedLabel, 
            'translated_label_msgid':       unActualLabelMsgId, 
            'translated_description':       unTranslatedDescription, 
            'translated_description_msgid': unActualDescriptionMsgId, 
            'translated_label_and_value':   unTranslatedLabel,
            'i18ndomain':                   unI18NDomain,            
        } )
        unosAttributeTranslations[ unAttributeTranslationResult[ 'label']] = unAttributeTranslationResult


        unI18NDomain        = 'ModelDDvlPlone'
        unaLabel            = 'description'
        unActualLabelMsgId  = 'ModelDDvlPlone_descripcion_label'
        unTranslatedLabel   = self.fTranslateI18N( unI18NDomain, unActualLabelMsgId, unaLabel, theContextualObject)
        unaDescription      = ''
        unActualDescriptionMsgId = 'ModelDDvlPlone_descripcion_help'
        unTranslatedDescription   = self.fTranslateI18N( unI18NDomain, unActualDescriptionMsgId, unTranslatedLabel, theContextualObject)
        unAttributeTranslationResult = self.fNewVoidAttributeTranslationResult( )
        unAttributeTranslationResult.update( {
            'label':                        unaLabel,
            'description' :                 unaDescription, 
            'translated_label':             unTranslatedLabel, 
            'translated_label_msgid':       unActualLabelMsgId, 
            'translated_description':       unTranslatedDescription, 
            'translated_description_msgid': unActualDescriptionMsgId, 
            'i18ndomain':                   unI18NDomain,            
        } )
        unosAttributeTranslations[ unAttributeTranslationResult[ 'label']] = unAttributeTranslationResult
                      
        unI18NDomain        = 'ModelDDvlPlone'
        unaLabel            = 'text'
        unActualLabelMsgId  = 'ModelDDvlPlone_text_label'
        unTranslatedLabel   = self.fTranslateI18N( unI18NDomain, unActualLabelMsgId, unaLabel, theContextualObject)
        unaDescription      = ''
        unActualDescriptionMsgId = 'ModelDDvlPlone_text_help'
        unTranslatedDescription   = self.fTranslateI18N( unI18NDomain, unActualDescriptionMsgId, unTranslatedLabel, theContextualObject)    
        unAttributeTranslationResult = self.fNewVoidAttributeTranslationResult( )
        unAttributeTranslationResult.update( {
            'label':                        unaLabel,
            'description' :                 unaDescription, 
            'translated_label':             unTranslatedLabel, 
            'translated_label_msgid':       unActualLabelMsgId, 
            'translated_description':       unTranslatedDescription, 
            'translated_description_msgid': unActualDescriptionMsgId, 
            'i18ndomain':                   unI18NDomain,            
        } )
        unosAttributeTranslations[ unAttributeTranslationResult[ 'label']] = unAttributeTranslationResult


        return unosAttributeTranslations 

    
    
    

    

    security.declarePrivate( 'getTranslationsForObjectAttribute')
    def getTranslationsForObjectAttribute(self, theObject, theAttributeName):
       
        if ( theObject == None) or not theAttributeName:
            return []
            
        unAttributeTranslationResult = {
            'label':                        theAttributeName,
            'description' :                 theAttributeName, 
            'translated_label':             theAttributeName, 
            'translated_label_msgid':       '', 
            'translated_description':       theAttributeName, 
            'translated_description_msgid': '', 
            'translated_label_and_value':   theAttributeName,
            'i18ndomain':                   '',
        }

        unaLabel                    = theAttributeName
        unaLabelMsgId               = ''
        unTranslatedLabel           = theAttributeName
        unaDescription              = theAttributeName
        unaDescriptionMsgId         = ''
        unTranslatedDescription     = theAttributeName
        unI18NDomain                = ''

        if not ( theAttributeName in [ 'title', 'description', 'text', ]):
                
            unSchema = theObject.schema
            if not unSchema.has_key( theAttributeName):
                return unAttributeTranslationResult
                
            unField             = unSchema[ theAttributeName]
            unWidget            = unField.widget
            unaLabel            = theAttributeName
            unaDescription      = theAttributeName
            unaLabelMsgId       = ''
            unaDescriptionMsgId = ''
            
            try:
                unaLabel                    = unWidget.label            
            except:
                None            
            try:
                unaDescription              = unWidget.description
            except:
                None            
            try:
                unaLabelMsgId               = unWidget.label_msgid
            except:
                None            
            try:
                unaDescriptionMsgId         = unWidget.description_msgid
            except:
                None

            unI18NDomain = self.fTranslationI18NDomain( None, theObject)
                
            unTranslatedLabel = ''
            if unaLabelMsgId:     
                unTranslatedLabel = self.fTranslateI18N( unI18NDomain, unaLabelMsgId, '', theObject)
            if not unTranslatedLabel:
                unTranslatedLabel = unaLabel
     
            unTranslatedDescription = ''
            if unaDescriptionMsgId:     
                unTranslatedDescription = self.fTranslateI18N( unI18NDomain, unaDescriptionMsgId, '', theObject)
            if not unTranslatedDescription:
                unTranslatedDescription = unaDescription
                
            unAttributeTranslationResult.update( {
                'label':                        unaLabel,
                'description' :                 unaDescription, 
                'translated_label':             unTranslatedLabel, 
                'translated_label_msgid':       unaLabelMsgId, 
                'translated_description':       unTranslatedDescription, 
                'translated_description_msgid': unaDescriptionMsgId, 
                'translated_label_and_value':   unaDescriptionMsgId, 
                'i18ndomain':                   unI18NDomain,            
            } )
        else:
            unosDefaultAttributesTranslations = self.getTranslationsForDefaultAttributes( theObject)
            unAttributeTranslationResult = unosDefaultAttributesTranslations.get( theAttributeName, None)    
     
        return unAttributeTranslationResult 

    
    
    
    
       
    
    
    security.declarePrivate( 'getTranslationsForVocabulary')
    def getTranslationsForVocabulary(self, theElement, theAttributeName): 

        if ( theElement == None):
            return None
        
        unElementSchema = theElement.schema
        
        if not( unElementSchema.has_key( theAttributeName)):
            return None
        
        unElementField  = unElementSchema[ theAttributeName]
        if not unElementField:
            return None
                
        unWidget = unElementField.widget
        if not unWidget:
            return None
        
        if not( unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget'):
            return None
    
        someVocabularyOptions   = []
        try:
            someVocabularyOptions = unElementField.vocabulary   
        except:
            None
        try:
            someVocabularyMsgIds = unElementField.vocabulary_msgids   
        except:
            None

        if not someVocabularyOptions:
            return None
        
        unasVocabularyTranslations = [ ]
        
        for unOptionIndex in range( len( someVocabularyOptions)):
            unaOption = someVocabularyOptions[ unOptionIndex]
            unaTranslatedOption = unaOption
            if len( someVocabularyMsgIds) > unOptionIndex:
                unaOptionMsgId = someVocabularyMsgIds[ unOptionIndex]
                unaTranslatedOption = self.fTranslateI18N( None, unaOptionMsgId, unaOption, theElement)
                unasVocabularyTranslations.append( { 'option': unaOption, 'translation': unaTranslatedOption} )
                
        return unasVocabularyTranslations
    
    
    
    
    security.declarePrivate( 'fVocabularyTranslationsFromCache_into')
    def fVocabularyTranslationsFromCache_into(self, 
        theElement, 
        theAttributeName, 
        theTranslationsCaches, 
        theResultDict):
        
        if ( theElement == None):
            return None
            
        unElementSchema = theElement.schema
        
        if not( unElementSchema.has_key( theAttributeName)):
            return None
        
        unElementField  = unElementSchema[ theAttributeName]
        if not unElementField:
            return None
                
        unWidget = unElementField.widget
        if not unWidget:
            return None
        
        if not( unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget'):
            return None
        
        aVocabularyTranslations = [ ]
        
        try:
            unVocabularyMethodNameOrOptions = unElementField.vocabulary   
        except:
            None
        if not unVocabularyMethodNameOrOptions:
            return unTranslatedValue

        if not unVocabularyMethodNameOrOptions.__class__.__name__ in [ 'str', 'unicode',]:
             
            unVocabularyTranslationsCache = None
            if theTranslationsCaches:
                unVocabularyTranslationsCache = theTranslationsCaches.get( 'vocabulary_translations', { })
            
            unMetaType = theElement.meta_type
        
            if unVocabularyTranslationsCache and unVocabularyTranslationsCache.has_key( unMetaType):
                aVocabularyTranslationsCacheForElementType = unVocabularyTranslationsCache[ unMetaType] 
                if aVocabularyTranslationsCacheForElementType.has_key( theAttributeName):
                    aVocabularyTranslations =  aVocabularyTranslationsCacheForElementType[ theAttributeName]  
                else:
                    aVocabularyTranslations = self.getTranslationsForVocabulary( theElement, theAttributeName)
                    if aVocabularyTranslations:
                        aVocabularyTranslationsCacheForElementType[ theAttributeName] = aVocabularyTranslations
            else:
                aVocabularyTranslations = self.getTranslationsForVocabulary( theElement, theAttributeName)
                if not ( unVocabularyTranslationsCache == None):
                    unVocabularyTranslationsCache[ unMetaType] = { theAttributeName:  aVocabularyTranslations, }   
                    
        else:
            aVocabularyDisplayList = None
            try:
                unVocabularyMethod = theElement[  unVocabularyMethodNameOrOptions]
                if unVocabularyMethod:
                    aVocabularyDisplayList = unVocabularyMethod()
                    
                    if not aVocabularyDisplayList or not len( aVocabularyDisplayList):
                        return unTranslatedValue
                                        
                    someVocabularyOptions = sorted( aVocabularyDisplayList.keys())
                    for unOptionIndex in range( len( someVocabularyOptions)):

                        unaOption = someVocabularyOptions[ unOptionIndex]

                        unaTranslatedOption = unaOption
                        unaOptionMsgId = aVocabularyDisplayList.getMsgId( unaOption)
                        if unaOptionMsgId:
                            unaTranslatedOption = self.fTranslateI18N( 'gvSIGtraducciones', unaOptionMsgId, unaOption, theElement)

                        aVocabularyTranslations.append( { 'option': unaOption, 'translation': unaTranslatedOption} )
                        
            except:
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fVocabularyTranslationsFromCache_into\n' 
                unInformeExcepcion += 'Error accessing element vocabulary method for attribute: meta_type=%s title=%s attribute=%s vocabularyMethod:%s\n' % ( theElement.meta_type, theElement.Title(), theAttributeName , unVocabularyMethodNameOrOptions )
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                logging.getLogger( 'gvSIGtraducciones').error( unInformeExcepcion)
                
                return aVocabularyTranslations
                
        if aVocabularyTranslations:
            theResultDict[ 'vocabulary_translations'] = aVocabularyTranslations
        return aVocabularyTranslations
    

     
    
    
    security.declarePrivate( 'fVocabularyOptionsAndValueTranslationFromCache_into')
    def fVocabularyOptionsAndValueTranslationFromCache_into(self, 
        theElement             =None, 
        theCanReturnValues     =None, 
        theValue               =None, 
        theAttributeName       =None, 
        theRetrievalExtents    =None,
        theTranslationsCaches  =None, 
        theResultDict          =None,
        theAdditionalParams    =None):

        
        unTranslatedValue = ''

        if ( theElement == None):
            return unTranslatedValue

        unElementSchema = theElement.schema        
        if not( unElementSchema.has_key( theAttributeName)):
            return unTranslatedValue
        
        unElementField  = unElementSchema[ theAttributeName]
        if not unElementField:
            return unTranslatedValue
        
        unWidget = unElementField.widget
        if not unWidget:
            return unTranslatedValue
        
        if not( unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget'):
            return unTranslatedValue

        if theCanReturnValues:
            unTranslatedValue = theValue
            
            
        try:
            unVocabularyMethodNameOrOptions = unElementField.vocabulary   
        except:
            None
        if not unVocabularyMethodNameOrOptions:
            return unTranslatedValue
        
        someVocabularyOptions   = [ ]
        aVocabularyTranslations = [ ]
        
        if not unVocabularyMethodNameOrOptions.__class__.__name__ in [ 'str', 'unicode',]:
            someVocabularyOptions = unVocabularyMethodNameOrOptions   
            if not( theAdditionalParams and ( theAdditionalParams.get( 'Do_Not_Translate', False) == True)):

                aVocabularyTranslations = self.fVocabularyTranslationsFromCache_into( 
                    theElement, 
                    theAttributeName, 
                    theTranslationsCaches, 
                    theResultDict)
        else:
            if not ( 'dynamic_vocabularies' in theRetrievalExtents):
                return unTranslatedValue
            
            aVocabularyDisplayList = None
            try:
                unVocabularyMethod = theElement[  unVocabularyMethodNameOrOptions]
                if unVocabularyMethod:
                    aVocabularyDisplayList = unVocabularyMethod()
                    
                    if not aVocabularyDisplayList or not len( aVocabularyDisplayList):
                        return unTranslatedValue
                                        
                    someVocabularyOptions = aVocabularyDisplayList.keys()
                    if not( theAdditionalParams and ( theAdditionalParams.get( 'Do_Not_Translate', False) == True)):
                        for unOptionIndex in range( len( someVocabularyOptions)):
    
                            unaOption = someVocabularyOptions[ unOptionIndex]
    
                            unaTranslatedOption = aVocabularyDisplayList.getValue( unaOption) or unaOption
                            unaOptionMsgId      = aVocabularyDisplayList.getMsgId( unaOption)
                            if unaOptionMsgId:
                                # ACV 20090907 Was hacked for gvSIGtraducciones, 
                                # at the time, the only user of the dynamic vocabularies feature
                                unI18NModuleName = 'gvSIGtraducciones'
                                try:
                                    unI18NModuleName = theElement.getNombreProyecto()
                                except:
                                    None
                                unaTranslatedOption = self.fTranslateI18N( unI18NModuleName, unaOptionMsgId, unaTranslatedOption, theElement)
    
                            aVocabularyTranslations.append( { 'option': unaOption, 'translation': unaTranslatedOption} )
                        
            except:               
                unaExceptionInfo = sys.exc_info()
                unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                
                unInformeExcepcion = 'Exception during fVocabularyOptionsAndValueTranslationFromCache_into\n' 
                unInformeExcepcion += 'Error accessing element vocabulary method for attribute: meta_type=%s title=%s attribute=%s vocabularyMethod:%s\n' % ( theElement.meta_type, theElement.Title(), theAttributeName , unVocabularyMethodNameOrOptions )
                unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                unInformeExcepcion += unaExceptionFormattedTraceback   
                logging.getLogger( 'gvSIGtraducciones').error( unInformeExcepcion)
            
                return unTranslatedValue
             
        theResultDict[ 'vocabulary'] = someVocabularyOptions
        theResultDict[ 'vocabulary_translations'] = aVocabularyTranslations
                    
        if theCanReturnValues:
            if someVocabularyOptions and aVocabularyTranslations and ( theValue in someVocabularyOptions):            
                unSelectionIndex = someVocabularyOptions.index( theValue)
                if unSelectionIndex >= 0 and len( aVocabularyTranslations) > unSelectionIndex:
                    unTranslatedValue = aVocabularyTranslations[ unSelectionIndex][ 'translation']
    
            theResultDict[ 'translated_value'] = unTranslatedValue
            theResultDict[ 'uvalue']           = unTranslatedValue

        return unTranslatedValue 
    
    
    
    
    
    security.declarePrivate( 'fBooleanOptionsAndValueTranslationFromCache_into')
    def fBooleanOptionsAndValueTranslationFromCache_into(self, 
        theElement, 
        theCanReturnValues, 
        theValue, 
        theAttributeName, 
        theTranslationsCaches, 
        theResultDict,
        theAdditionalParams):

        aTrueTranslation = str( False)
        aFalseTranslation = str( False)
        
        someBooleanOptions = [ { 'option': False, 'translation': aFalseTranslation} , { 'option': True, 'translation': aTrueTranslation} , ]
        
        if theAdditionalParams and ( theAdditionalParams.get( 'Do_Not_Translate', False) == True):

            if not theCanReturnValues:
                return someBooleanOptions
             
            unTranslatedValue = ''
            if theValue == True:
                unTranslatedValue = aTrueTranslation
            else:
                unTranslatedValue = aFalseTranslation
    
            if theResultDict:
                theResultDict[ 'translated_value'] = unTranslatedValue
                theResultDict[ 'uvalue']           = unTranslatedValue            
                return someBooleanOptions
            
        
        unElementSchema = theElement.schema        
        if not( unElementSchema.has_key( theAttributeName)):
            return []
        
        unElementField  = unElementSchema[ theAttributeName]
        if not unElementField:
            return []
        
        if not ( unElementField.type == 'boolean'):
            return []
        
        aTrueTranslation = theTranslationsCaches.get( 'true_translation', '')
        if not aTrueTranslation:                
            aTrueTranslation = self.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_True', str( True), theElement) 
            if aTrueTranslation:
                theTranslationsCaches[ 'true_translation'] = aTrueTranslation
        
        aFalseTranslation = theTranslationsCaches.get( 'false_translation', '')
        if not aFalseTranslation:                
            aFalseTranslation = self.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_False', str( False), theElement) 
            if aFalseTranslation:
                theTranslationsCaches[ 'false_translation'] = aFalseTranslation
            
        aEsTranslation = theTranslationsCaches.get( 'es_translation', '')
        if not aEsTranslation:                
            aEsTranslation = self.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_prefijoAttributoBoolean_es', u'Es', theElement) 
            if aEsTranslation:
                theTranslationsCaches[ 'es_translation'] = aEsTranslation

        aNoEsTranslation = theTranslationsCaches.get( 'noes_translation', '')
        if not aNoEsTranslation:                
            aNoEsTranslation = self.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_prefijoAttributoBoolean_noes', u'No es', theElement) 
            if aNoEsTranslation:
                theTranslationsCaches[ 'noes_translation'] = aNoEsTranslation


        
        someBooleanOptions = [ { 'option': False, 'translation': aFalseTranslation} , { 'option': True, 'translation': aTrueTranslation} , ]
        theResultDict[ 'vocabulary_translations'] = someBooleanOptions
        
        if not theCanReturnValues:
            return someBooleanOptions
         
        unTranslatedValue = ''
        if theValue == True:
            unTranslatedValue = aTrueTranslation
        else:
            unTranslatedValue = aFalseTranslation

        theResultDict[ 'translated_value'] = unTranslatedValue
        theResultDict[ 'uvalue']           = unTranslatedValue
        
        
        unTranslatedLabelAndValue = ''
        unTranslatedLabel = theResultDict[ 'attribute_translations'][ 'translated_label']
        if unTranslatedLabel.startswith( aEsTranslation):
            if theValue:
                unTranslatedLabelAndValue = unTranslatedLabel            
            else:
                unBareLabel = unTranslatedLabel[ len( aEsTranslation):].strip()
                unTranslatedLabelAndValue = u'%s %s' % ( aNoEsTranslation, unBareLabel)                        
        else:                                   
            unTranslatedLabelAndValue = u'%s %s' % ( unTranslatedLabel, unTranslatedValue)
                             
        theResultDict[ 'attribute_translations'][ 'translated_label_and_value'] = unTranslatedLabelAndValue
        
        
        return someBooleanOptions                    
               
    
    
    

    
    
   


    
    security.declarePrivate( 'fMetaTypeNameTranslationsFromCache_into')
    def fMetaTypeNameTranslationsFromCache_into(self, 
        theMetaTypeName        =None, 
        theTranslationsCaches  =None, 
        theResultDict          =None, 
        theContextualElement   =None,
        theAdditionalParams    =None):
        
        if theAdditionalParams and ( theAdditionalParams.get( 'Do_Not_Translate', False) == True):
            if not theResultDict:
                return {}
            
            aTypeTranslations = theResultDict.get( 'type_translations', None)
            if aTypeTranslations == None:
                aTypeTranslations = self.fNewVoidObjectTranslationResult()
                theResultDict[ 'type_translations'] = aTypeTranslations
            return aTypeTranslations
            
            
        if not theMetaTypeName or ( theContextualElement == None):
            return None
                
        unTypesTranslationsCache = None
        if theTranslationsCaches:
            unTypesTranslationsCache = theTranslationsCaches.get( 'types_translations_cache', None)

        if unTypesTranslationsCache and unTypesTranslationsCache.has_key(  theMetaTypeName) and unTypesTranslationsCache[ theMetaTypeName].has_key( 'type'):
            aTypeTranslations = unTypesTranslationsCache[ theMetaTypeName][ 'type']
        else:
            aTypeTranslations = self.getTranslationsFromMetaTypeName( theMetaTypeName, theContextualElement)
            if not ( unTypesTranslationsCache == None) and aTypeTranslations:
                unTypesTranslationsCache[ theMetaTypeName] = { 'type' : aTypeTranslations , }
        
        if not( theResultDict == None) and aTypeTranslations:
            theResultDict[ 'type_translations'] = aTypeTranslations
            
        return aTypeTranslations

    
    
    
    
    
    security.declarePrivate( 'fAttributeTranslationsFromCache')
    def fAttributeTranslationsFromCache(self, 
        theElement            = None,
        theFieldName          = None, 
        theTranslationsCaches = None,
        theResultDict         = None, 
        theResultKey          = None,
        theAdditionalParams   = None,
        ):
        
        if theAdditionalParams and ( theAdditionalParams.get( 'Do_Not_Translate', False) == True):
            anAttributeTranslations = self.fNewVoidAttributeTranslationResult()
            return anAttributeTranslations
         
        if ( theElement == None) or not theFieldName:
            return None

        unI18NDomain = self.fTranslationI18NDomain( None, theElement)
        unArchetypeSchema = theElement.fArchetypeSchemaByName( theElement.meta_type)
        anAttributeTranslations = self.fAttributeTranslationsFromCacheOrArchetypeSchema( theElement, theElement.meta_type, unArchetypeSchema, unI18NDomain, theFieldName, theTranslationsCaches)

        if not( theResultDict == None) and theResultKey:
            theResultDict[ theResultKey] = anAttributeTranslations
                
        return anAttributeTranslations
    
    

    
    
      
    
    
    
    
    

    
    security.declarePrivate( 'fAttributeTranslationsFromCacheOrArchetypeSchema')
    def fAttributeTranslationsFromCacheOrArchetypeSchema(self, theContextualElement, theTypeName, theSchema, theI18NDomain, theFieldName, theTranslationsCaches):
        if not theTypeName or not theSchema or not theI18NDomain or not theFieldName:
            return None
        
        unTypesTranslationsCache = None
        if theTranslationsCaches:
            unTypesTranslationsCache = theTranslationsCaches.get( 'types_translations_cache', None)
        
        if unTypesTranslationsCache and unTypesTranslationsCache.has_key(  theTypeName):
            if unTypesTranslationsCache[ theTypeName].has_key( 'attributes'):
                aAttributeTranslationsCacheForType = unTypesTranslationsCache[ theTypeName][ 'attributes']
            else:
                aAttributeTranslationsCacheForType = { }
                unTypesTranslationsCache[ theTypeName][ 'attributes'] = aAttributeTranslationsCacheForType
                
            if aAttributeTranslationsCacheForType.has_key( theFieldName):
                anAttributeTranslations =  aAttributeTranslationsCacheForType[ theFieldName]  
            else:
                anAttributeTranslations = self.getTranslationsForObjectAttributeFromArchetypeSchema( theContextualElement, theTypeName, theSchema, theI18NDomain, theFieldName)
                aAttributeTranslationsCacheForType[ theFieldName] = anAttributeTranslations
        else:
            anAttributeTranslations = self.getTranslationsForObjectAttributeFromArchetypeSchema( theContextualElement, theTypeName, theSchema, theI18NDomain, theFieldName)
            if anAttributeTranslations:
                if not ( unTypesTranslationsCache is None):
                    unTypesTranslationsCache[ theTypeName] = { 'attributes': { theFieldName:  anAttributeTranslations, } }
 
        return anAttributeTranslations
    
    
     
    

    
    
    
    
    

    security.declarePrivate( 'getTranslationsForObjectAttributeFromArchetypeSchema')
    def getTranslationsForObjectAttributeFromArchetypeSchema(self, theContextualElement, theTypeName, theSchema, theI18NDomain, theAttributeName):
       
        if not theTypeName or not theSchema or not theI18NDomain or not theAttributeName:
            return []
            
        unAttributeTranslationResult = {
            'label':                        theAttributeName,
            'description' :                 theAttributeName, 
            'translated_label':             theAttributeName, 
            'translated_label_msgid':       '', 
            'translated_description':       theAttributeName, 
            'translated_description_msgid': '', 
            'i18ndomain':                   '',
        }

        unaLabel                    = theAttributeName
        unaLabelMsgId               = ''
        unTranslatedLabel           = theAttributeName
        unaDescription              = theAttributeName
        unaDescriptionMsgId         = ''
        unTranslatedDescription     = theAttributeName
        unI18NDomain                = ''

        if not ( theAttributeName in [ 'title', 'description', 'text', ]):
                
            if not theSchema.has_key( theAttributeName):
                return unAttributeTranslationResult
                
            unI18NDomain = theI18NDomain
                
            unField             = theSchema[ theAttributeName]
            unWidget            = unField.widget
            unaLabel            = theAttributeName
            unaDescription      = theAttributeName
            unaLabelMsgId       = ''
            unaDescriptionMsgId = ''
            
            try:
                unaLabel                    = unWidget.label            
            except:
                None            
            try:
                unaDescription              = unWidget.description
            except:
                None            
            try:
                unaLabelMsgId               = unWidget.label_msgid
            except:
                None            
            try:
                unaDescriptionMsgId         = unWidget.description_msgid
            except:
                None

            unTranslatedLabel = ''
            if unaLabelMsgId:     
                unTranslatedLabel = self.fTranslateI18N( unI18NDomain, unaLabelMsgId, '', theContextualElement)
            if not unTranslatedLabel:
                unTranslatedLabel = unaLabel
     
            unTranslatedDescription = ''
            if unaDescriptionMsgId:     
                unTranslatedDescription = self.fTranslateI18N( unI18NDomain, unaDescriptionMsgId, '', theContextualElement)
            if not unTranslatedDescription:
                unTranslatedDescription = unaDescription
                
        else:
            if theAttributeName == 'title':
                unI18NDomain        = 'ModelDDvlPlone'
                unaLabel            = 'title'
                unActualLabelMsgId  = 'ModelDDvlPlone_titulo_label'
                unTranslatedLabel   = self.fTranslateI18N( unI18NDomain, unActualLabelMsgId, unaLabel, theContextualElement)
                unaDescription      = ''
                unActualDescriptionMsgId = 'ModelDDvlPlone_titulo_help'
                unTranslatedDescription   = self.fTranslateI18N( unI18NDomain, unActualDescriptionMsgId, unTranslatedLabel, theContextualElement)
            elif theAttributeName == 'description':
                unI18NDomain        = 'ModelDDvlPlone'
                unaLabel            = 'description'
                unActualLabelMsgId  = 'ModelDDvlPlone_descripcion_label'
                unTranslatedLabel   = self.fTranslateI18N( unI18NDomain, unActualLabelMsgId, unaLabel, theContextualElement)
                unaDescription      = ''
                unActualDescriptionMsgId = 'ModelDDvlPlone_descripcion_help'
                unTranslatedDescription   = self.fTranslateI18N( unI18NDomain, unActualDescriptionMsgId, unTranslatedLabel, theContextualElement)
            elif theAttributeName == 'text':
                unI18NDomain        = 'ModelDDvlPlone'
                unaLabel            = 'description'
                unActualLabelMsgId  = 'ModelDDvlPlone_text_label'
                unTranslatedLabel   = self.fTranslateI18N( unI18NDomain, unActualLabelMsgId, unaLabel, theContextualElement)
                unaDescription      = ''
                unActualDescriptionMsgId = 'ModelDDvlPlone_text_help'
                unTranslatedDescription   = self.fTranslateI18N( unI18NDomain, unActualDescriptionMsgId, unTranslatedLabel, theContextualElement)
            
    
        unAttributeTranslationResult.update( {
            'label':                        unaLabel,
            'description' :                 unaDescription, 
            'translated_label':             unTranslatedLabel, 
            'translated_label_msgid':       unaLabelMsgId, 
            'translated_description':       unTranslatedDescription, 
            'translated_description_msgid': unaDescriptionMsgId, 
            'i18ndomain':                   unI18NDomain,            
        } )
     
        return unAttributeTranslationResult 

    
    
    



    security.declarePrivate('pCompleteColumnTranslations')
    def pCompleteColumnTranslations(self,  
        theTimeProfilingResults=None,
        theContextualElement   =None, 
        theTraversalResult     =None, 
        theTypeNames           =None, 
        theTranslationsCaches  =None,
        theAdditionalParams    =None):
        
        if theAdditionalParams and ( theAdditionalParams.get( 'Do_Not_Translate', False) == True):
            return self

        if False and not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'pCompleteColumnTranslations', theTimeProfilingResults)
        
        try:
            if ( theContextualElement == None)  or not theTraversalResult  or not theTypeNames:
                return self
            
            someColumnNames         = theTraversalResult.get( 'column_names', [])
            someColumnTranslations  = theTraversalResult.get( 'column_translations', {})
            unPendingColumnNames = []
            for unColumnName in someColumnNames:
                unExistingColumnTranslation = someColumnTranslations.get( unColumnName, {}) 
                if not unExistingColumnTranslation:
                    unPendingColumnNames.append( unColumnName)
             
            if not unPendingColumnNames:
                return self
            
            unI18NDomain = self.fTranslationI18NDomain( None, theContextualElement)
            
            for unTypeName in theTypeNames:
                unArchetypeSchema = None
                try:
                    unArchetypeSchema = theContextualElement.fArchetypeSchemaByName( unTypeName)
                except:
                    None
                if unArchetypeSchema:
                    unNewPendingColumnNames = unPendingColumnNames[:]
                    for unColumnName in unPendingColumnNames:
                        if unArchetypeSchema.has_key( unColumnName):
                            unColumnTranslation = self.fAttributeTranslationsFromCacheOrArchetypeSchema( theContextualElement, unTypeName, unArchetypeSchema, unI18NDomain, unColumnName, theTranslationsCaches)    
                            if unColumnTranslation:
                                someColumnTranslations[ unColumnName] = unColumnTranslation 
                                unNewPendingColumnNames.remove( unColumnName)
                                if not unNewPendingColumnNames:
                                    return self
                    unPendingColumnNames = unNewPendingColumnNames
                            
            return self
    
        finally:
            if False and not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'pCompleteColumnTranslations', theTimeProfilingResults)




       



    
    security.declarePrivate( 'fMonthsVocabularyTranslationsFromCache_ContextualElement')
    def fMonthsVocabularyTranslationsFromCache_ContextualElement(self,  theElement,  theTranslationsCaches):
        
        if ( theElement == None):
            return None
                    
        unVocabularyTranslationsCache = None
        if theTranslationsCaches:
            unVocabularyTranslationsCache = theTranslationsCaches.get( 'vocabulary_translations', { })
            
        if unVocabularyTranslationsCache and unVocabularyTranslationsCache.has_key( 'DateTime'):
            aVocabularyTranslationsCacheForElementType = unVocabularyTranslationsCache[ 'DateTime'] 
            if aVocabularyTranslationsCacheForElementType.has_key( 'month_name'):
                aVocabularyTranslations =  aVocabularyTranslationsCacheForElementType[ 'month_name']  
            else:
                aVocabularyTranslations = self.fMonthsVocabularyTranslations( theElement)
                if aVocabularyTranslations:
                    aVocabularyTranslationsCacheForElementType[ 'month_name'] = aVocabularyTranslations
        else:
            aVocabularyTranslations = self.fMonthsVocabularyTranslations( theElement)
            if not ( unVocabularyTranslationsCache == None):
                unVocabularyTranslationsCache[ 'DateTime'] = { 'month_name':  aVocabularyTranslations, }    

        return aVocabularyTranslations
    


    
    security.declarePrivate( 'fDaysOfWeekVocabularyTranslationsFromCache_ContextualElement')
    def fDaysOfWeekVocabularyTranslationsFromCache_ContextualElement(self,  theElement,  theTranslationsCaches):
        
        if ( theElement == None):
            return None
                    
        unVocabularyTranslationsCache = None
        if theTranslationsCaches:
            unVocabularyTranslationsCache = theTranslationsCaches.get( 'vocabulary_translations', { })
            
        if unVocabularyTranslationsCache and unVocabularyTranslationsCache.has_key( 'DateTime'):
            aVocabularyTranslationsCacheForElementType = unVocabularyTranslationsCache[ 'DateTime'] 
            if aVocabularyTranslationsCacheForElementType.has_key( 'day_of_week'):
                aVocabularyTranslations =  aVocabularyTranslationsCacheForElementType[ 'day_of_week']  
            else:
                aVocabularyTranslations = self.fDaysOfWeekVocabularyTranslations( theElement)
                if aVocabularyTranslations:
                    aVocabularyTranslationsCacheForElementType[ 'day_of_week'] = aVocabularyTranslations
        else:
            aVocabularyTranslations = self.fDaysOfWeekVocabularyTranslations( theElement)
            if not ( unVocabularyTranslationsCache == None):
                unVocabularyTranslationsCache[ 'DateTime'] = { 'day_of_week':  aVocabularyTranslations, }    

        return aVocabularyTranslations
    

     
 



    security.declarePrivate('pDateSubValuesOptionsAndTranslations_into')
    def pDateSubValuesOptionsAndTranslations_into(self, 
        theElement, 
        theCanReturnValues, 
        theValue, 
        theAttributeName, 
        theTranslationsCaches, 
        theResultDict):
        
        if ( theElement == None):
            return None

        
        unCanReturnValues = False
        if theCanReturnValues and theValue and theValue.__class__.__name__ == 'DateTime':
            unCanReturnValues = True
            unYear          = theValue.year()
            unMonth         = theValue.month()
            unDayOfMonth    = theValue.day()
            unDayOfWeek     = theValue.Day()
     
        if unCanReturnValues:
            theResultDict[ 'uvalue']            = self.fAsUnicode( str( theValue), theElement)
            theResultDict[ 'translated_value']  = theResultDict[ 'uvalue']
            
        unYearResult = self.fNewVoidValueResult()                            
        unYearResult[ 'attribute_name']    = 'year'
        unYearResult[ 'type']              = 'integer'
        theResultDict[ 'sub_values'].append( unYearResult)
        # ACV 20090901 Avoid adding redundant results to dictionaries during service layer processing
        # the dictionaries will be compiled at the completion of the retrieval
        # in method pBuildDictResults_Element
        #
        # theResultDict[ 'sub_values_by_name'][ unYearResult[ 'attribute_name']] = unYearResult
        if unCanReturnValues:
            unYearResult[ 'raw_value']         = unYear
            unYearResult[ 'value']             = unYear
            unYearResult[ 'uvalue']            = unYear
            unYearResult[ 'translated_value']  = unYear
     
        unMonthsVocabularyTranslations = self.fMonthsVocabularyTranslationsFromCache_ContextualElement( theElement, theTranslationsCaches)
        unMonthResult = self.fNewVoidValueResult()                            
        unMonthResult[ 'attribute_name']     = 'month'
        unMonthResult[ 'type']              = 'selection'
        unMonthResult[ 'vocabulary_translations'] = unMonthsVocabularyTranslations
        theResultDict[ 'sub_values'].append( unMonthResult)
        # ACV 20090901 Avoid adding redundant results to dictionaries during service layer processing
        # the dictionaries will be compiled at the completion of the retrieval
        # in method pBuildDictResults_Element
        #
        # theResultDict[ 'sub_values_by_name'][ unMonthResult[ 'attribute_name']] = unMonthResult
        if unCanReturnValues:
            unTranslatedMonth = self.fTranslateMonth( unMonth, theElement)
            unMonthResult[ 'raw_value']         = unMonth
            unMonthResult[ 'value']             = unMonth
            unMonthResult[ 'uvalue']            = unTranslatedMonth
            unMonthResult[ 'translated_value']  = unTranslatedMonth
     
        unDayOfMonthResult = self.fNewVoidValueResult()                            
        unDayOfMonthResult[ 'attribute_name']    = 'day_of_month'
        unDayOfMonthResult[ 'type']              = 'integer'
        theResultDict[ 'sub_values'].append( unDayOfMonthResult)
        # ACV 20090901 Avoid adding redundant results to dictionaries during service layer processing
        # the dictionaries will be compiled at the completion of the retrieval
        # in method pBuildDictResults_Element
        #
        # theResultDict[ 'sub_values_by_name'][ unDayOfMonthResult[ 'attribute_name']] = unDayOfMonthResult
        if unCanReturnValues:
            unDayOfMonthResult[ 'raw_value']         = unDayOfMonth
            unDayOfMonthResult[ 'value']             = unDayOfMonth
            unDayOfMonthResult[ 'uvalue']            = unDayOfMonth
            unDayOfMonthResult[ 'translated_value']  = unDayOfMonth
     
        unDaysOfWeekVocabularyTranslations = self.fDaysOfWeekVocabularyTranslationsFromCache_ContextualElement( theElement, theTranslationsCaches)
        unDayOfWeekResult = self.fNewVoidValueResult()                            
        unDayOfWeekResult[ 'attribute_name']    = 'day_of_week'
        unDayOfWeekResult[ 'type']              = 'selection'
        unDayOfWeekResult[ 'vocabulary_translations'] = unDaysOfWeekVocabularyTranslations
        theResultDict[ 'sub_values'].append( unDayOfWeekResult)
        # ACV 20090901 Avoid adding redundant results to dictionaries during service layer processing
        # the dictionaries will be compiled at the completion of the retrieval
        # in method pBuildDictResults_Element
        #
        # theResultDict[ 'sub_values_by_name'][ unDayOfWeekResult[ 'attribute_name']] = unDayOfWeekResult
        if unCanReturnValues:
            unTranslatedDayOfWeek = self.fTranslateDayOfWeek( unDayOfWeek, theElement)
            unDayOfWeekResult[ 'raw_value']         = unDayOfWeek
            unDayOfWeekResult[ 'value']             = unDayOfWeek
            unDayOfWeekResult[ 'uvalue']            = unTranslatedDayOfWeek
            unDayOfWeekResult[ 'translated_value']  = unTranslatedDayOfWeek
     
        return self
        
                            
   