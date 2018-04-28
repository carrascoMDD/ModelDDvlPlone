# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval_Derivation.py
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


from AccessControl      import ClassSecurityInfo


from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
   


class ModelDDvlPloneTool_Retrieval_Derivation:
    """
    """
    security = ClassSecurityInfo()


     
      
    security.declarePrivate( 'getTransBool')
    def getTransBool( self, theFieldName, theValueToShow=None, theSeparatorToAdd=''):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return ''

        if not theFieldName:
            return ''
            
        unAttributeMetaAndValue= self.getAttributeMetaAndValue( theFieldName)
        if not unAttributeMetaAndValue:
            return ''
            
        unValue             = unAttributeMetaAndValue[ 1]
        unType              = unAttributeMetaAndValue[ 6]
        unTranslatedLabel   = unAttributeMetaAndValue[ 8]
        if not unType == 'boolean':
            return str( unValue)
           
        unString = ''    
        if (theValueToShow == None) or (theValueToShow == unValue):
            if unValue == True:
                unString = unTranslatedLabel + theSeparatorToAdd
            else:
                unString = self.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_predicado_No', 'No') + ' ' + unTranslatedLabel + theSeparatorToAdd
        
        return unString       
      
 

      
    security.declarePrivate( 'getTransBool')
    def concatenateTransBools( self, theFieldNamesAndValuesToShow, theSeparatorToAdd=''):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return ''

        if not theFieldNamesAndValuesToShow:
            return ''
            
        unosFieldNames = [unFieldAndValueToShow[ 0] for unFieldAndValueToShow in theFieldNamesAndValuesToShow]
                    
        unosAttributesMetaAndValues = self.getAttributesMetaAndValues( unosFieldNames)
        if not unosAttributesMetaAndValues:
            return ''
        
        unosConcatenatedTransBools = ''
        
        for unAttributeIndex in range( len( unosAttributesMetaAndValues)):
            unAttributeMetaAndValue = unosAttributesMetaAndValues[ unAttributeIndex]
            unValueToShow = [ unFieldAndValueToShow[ 1] for unFieldAndValueToShow in theFieldNamesAndValuesToShow if unFieldAndValueToShow[ 0] == unAttributeMetaAndValue[ 0]][ 0]
            
            if unAttributeMetaAndValue:                
                unValue             = unAttributeMetaAndValue[ 1]
                unType              = unAttributeMetaAndValue[ 6]
                unTranslatedLabel   = unAttributeMetaAndValue[ 8]
                if unType == 'boolean':                   
                    unString = ''    
                    if (unValueToShow == None) or (unValueToShow == unValue):
                        if unValue == True:
                            unString = unTranslatedLabel 
                        else:
                            unString = self.fTranslateI18N( 'ModelDDvlPlone', 'ModelDDvlPlone_predicado_No', 'No') + ' ' + unTranslatedLabel 
                    if unString:
                        if unosConcatenatedTransBools:
                            unosConcatenatedTransBools += theSeparatorToAdd
                        unosConcatenatedTransBools += unString
                else:
                    if unosConcatenatedTransBools:
                        unosConcatenatedTransBools += theSeparatorToAdd
                    unosConcatenatedTransBools += str( unValue)
                    
        
        return unosConcatenatedTransBools       
      
 
 
 
 
    security.declarePrivate( 'fComposeQualifiedName')
    def fComposeQualifiedName( self, theSeparator, theAttributeName, theExcludeRoot=True):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return ''

        if not theAttributeName:
            return ''
            
        unSeparator = theSeparator
        if not unSeparator:
            unSeparator = ''
                 
        if self.getEsRaiz():
            if theExcludeRoot:
                return ''
            else:
                unValue = self.getAttributeMetaAndValue( theAttributeName)[ 0][ 1]
                return unValue
        else:
            unContenedorQualifiedName = ''
            unContenedor = self.getContenedor()
            if unContenedor:
                unContenedorQualifiedName = unContenedor.fComposeQualifiedName( theSeparator, theAttributeName, theExcludeRoot)
                if unContenedorQualifiedName:
                    unContenedorQualifiedName += unSeparator
            
            unValue = self.getAttributeMetaAndValue( theAttributeName)[ 1]
            return unContenedorQualifiedName + unValue
             
 

 
    security.declarePrivate( 'fComposeOwnerName')
    def fComposeOwnerName( self, theSeparator, theAttributeName, theExcludeRoot=True):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return ''

        if not theAttributeName:
            return ''
            
        unSeparator = theSeparator
        if not unSeparator:
            unSeparator = ''
                 
        if self.getEsRaiz():
            return ''
            
        unContenedorQualifiedName = ''
        unContenedor = self.getContenedor()
        if unContenedor:
            unContenedorQualifiedName = unContenedor.fComposeQualifiedName( theSeparator, theAttributeName, theExcludeRoot)
        
        return unContenedorQualifiedName
         
 
 
 
 
    security.declarePrivate( 'fTraverseAndGetValues')
    def fTraverseAndGetValues( self, theFieldNamesToTraverse, theFieldNamesToGet):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return [ ]

        if not theFieldNamesToTraverse:
            return [ self.getAttributesMetaAndValues( theFieldNamesToGet), ]
        
        unSonMulti = False
        unosElementosPasoAnterior = [ self]
        unosElementosNuevoPaso = [ ]
        for unFieldNameToTraverse in theFieldNamesToTraverse:
            for unElementoAnterior in unosElementosPasoAnterior:
                unSchema = unElementoAnterior.schema
                if unSchema.has_key( unFieldNameToTraverse):
                    unField     = unSchema[ unFieldNameToTraverse]
                    
                    if not self.fGetFieldReadPermission( self, unFieldNameToTraverse):
                        return []
                    
                    unEsMulti   = unField.multiValued
                    unAccesor   = unField.getAccessor( unElementoAnterior)
                    unValue     = unAccesor( )
                    if unEsMulti:
                        unSonMulti = True
                        if unValue:
                            unosElementosNuevoPaso += unValue
                    else:
                        if unValue:
                            unosElementosNuevoPaso.append( unValue)
                                
            unosElementosPasoAnterior = unosElementosNuevoPaso
        
        if not unosElementosPasoAnterior:
            return []
            
        unosMetaAndValues = []            
        for unElemento in unosElementosPasoAnterior:
            unMetaAndValues  = unElemento.getAttributesMetaAndValues( theFieldNamesToGet) 
            unosMetaAndValues.append( unMetaAndValues) 
        
        return unosMetaAndValues



    security.declarePrivate( 'fRecurseCollectingReferences')
    def fRecurseCollectingReferences( self, theFieldNameToRecurse, theReferenceFieldNameToGet, theExcludeInitial=True):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return [ ]

        if not theFieldNameToRecurse or not theReferenceFieldNameToGet:
            return [ ]
        
        todosElementosReferenciados = [ ]
        someAlreadyTraversed = [ self]

        if not theExcludeInitial:
            unosMetaAndValuesReferenciados = self.getReferenceMetaAndValue( theReferenceFieldNameToGet)
            if unosMetaAndValuesReferenciados:
                unosElementosReferenciados = unosMetaAndValuesReferenciados[ 1]
                if unosElementosReferenciados:
                    for unElemento in unosElementosReferenciados:
                        if not ( unElemento in todosElementosReferenciados):
                            todosElementosReferenciados.append( unElemento)
        
        unosMetaAndValuesRecurrentes = self.getReferenceMetaAndValue( theFieldNameToRecurse)
        if unosMetaAndValuesRecurrentes:
            unosElementosRecurrentes = unosMetaAndValuesRecurrentes[ 1]
            if unosElementosRecurrentes:
                for unElementoRecurrente in unosElementosRecurrentes:
                    unElementoRecurrente.pRecurseCollectingReferencesInto( theFieldNameToRecurse, theReferenceFieldNameToGet, todosElementosReferenciados, someAlreadyTraversed)
        
        return todosElementosReferenciados





    def pRecurseCollectingReferencesInto( self, theFieldNameToRecurse, theReferenceFieldNameToGet, theElementosReferenciados, theAlreadyTraversed):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return [ ]

        if not theFieldNameToRecurse or not theReferenceFieldNameToGet:
            return
            
        if self in theAlreadyTraversed:
            return 
           
        theAlreadyTraversed.append( self)
            
        unosMetaAndValuesReferenciados = self.getReferenceMetaAndValue( theReferenceFieldNameToGet)
        if unosMetaAndValuesReferenciados:
            unosElementosReferenciados = unosMetaAndValuesReferenciados[ 1]
            if unosElementosReferenciados:
                for unElemento in unosElementosReferenciados:
                    if not ( unElemento in theElementosReferenciados):
                        theElementosReferenciados.append( unElemento)
        
        unosMetaAndValuesRecurrentes = self.getReferenceMetaAndValue( theFieldNameToRecurse)
        if unosMetaAndValuesRecurrentes:
            unosElementosRecurrentes = unosMetaAndValuesRecurrentes[ 1]
            if unosElementosRecurrentes:
                for unElementoRecurrente in unosElementosRecurrentes:
                    unElementoRecurrente.pRecurseCollectingReferencesInto( theFieldNameToRecurse, theReferenceFieldNameToGet, theElementosReferenciados, theAlreadyTraversed)
        
        return self






    security.declarePrivate( 'fRecurseCollect')
    def fRecurseCollect( self, theFieldNameToRecurse, theExcludeInitial=True):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return [ ]

        if not theFieldNameToRecurse:
            return [ ]
        
        todosElementos = [ ]

        if not theExcludeInitial:
            unosElementos.append( self)
        
        unosMetaAndValuesRecurrentes = self.getReferenceMetaAndValue( theFieldNameToRecurse)
        if unosMetaAndValuesRecurrentes:
            unosElementosRecurrentes = unosMetaAndValuesRecurrentes[ 1]
            if unosElementosRecurrentes:
                for unElementoRecurrente in unosElementosRecurrentes:
                    unElementoRecurrente.pRecurseCollectInto( theFieldNameToRecurse, todosElementos)
        
        return todosElementos





    def pRecurseCollectInto( self, theFieldNameToRecurse, theElementosReferenciados):
        if not theFieldNameToRecurse:
            return
        
        if self in theElementosReferenciados:
            return
            
        theElementosReferenciados.append( self)
        
        unosMetaAndValuesRecurrentes = self.getReferenceMetaAndValue( theFieldNameToRecurse)
        if unosMetaAndValuesRecurrentes:
            unosElementosRecurrentes = unosMetaAndValuesRecurrentes[ 1]
            if unosElementosRecurrentes:
                for unElementoRecurrente in unosElementosRecurrentes:
                    unElementoRecurrente.pRecurseCollectInto( theFieldNameToRecurse, theElementosReferenciados)
        
        return self






    security.declarePrivate( 'fTraverseAndGetJustValues')
    def fTraverseAndGetJustValues( self, theFieldNamesToTraverse, theFieldNamesToGet):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return []

        unosElementosMetaAndValues= self.fTraverseAndGetValues( theFieldNamesToTraverse, theFieldNamesToGet)
        unosValoresElementos = []
        for unElementoMetaAndVaues in unosElementosMetaAndValues:
            unosValoresElementos.append( [ unMetaAndValue[ 1] for unMetaAndValue in unElementoMetaAndVaues])
                 
        return unosValoresElementos
        
        

    security.declarePrivate( 'fTraverseAndGetJustOneValue')
    def fTraverseAndGetJustOneValue( self, theFieldNamesToTraverse, theFieldNamesToGet):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return None

        unosValoresElementos= self.fTraverseAndGetJustValues( theFieldNamesToTraverse, theFieldNamesToGet)
        if not unosValoresElementos or not unosValoresElementos[ 0]:
            return None
        return unosValoresElementos[ 0][ 0]
        
        
    security.declarePrivate( 'fTraverseAndConcatenateValues')
    def fTraverseAndConcatenateValues( self, theFieldNamesToTraverse, theFieldNamesToGet):
        aPortalTool = getToolByName( self, 'portal_membership')
        if not aPortalTool.checkPermission( permissions.View, self):
            return None

        unosValoresElementos= self.fTraverseAndGetJustValues( theFieldNamesToTraverse, theFieldNamesToGet)
        if not unosValoresElementos:
            return None
        unosValores = [unValorElemento[ 0] for unValorElemento in unosValoresElementos]
        unosValoresConcatenados = ''
        for unValor in unosValores:
            if unosValoresConcatenados:
                unosValoresConcatenados += ', '
            unosValoresConcatenados += str( unValor)
        return unosValoresConcatenados
        
        
        
        






