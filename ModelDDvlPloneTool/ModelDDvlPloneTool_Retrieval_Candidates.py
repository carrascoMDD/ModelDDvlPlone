# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval_Candidates.py
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

from AccessControl      import ClassSecurityInfo


from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

from Products.Relations.config                  import RELATIONS_LIBRARY

   
from ModelDDvlPloneToolSupport          import fEvalString

cElementsOfTypeTraversalName = 'ElementsOfType_TraversalName'   


class ModelDDvlPloneTool_Retrieval_Candidates:
    """
    """
    security = ClassSecurityInfo()




    security.declarePrivate('fNewVoidCandidatesResult')
    def fNewVoidCandidatesResult(self):
        unResult = { 
            'traversal_name' :          '', 
            'traversal_config':         '', 
            'traversal_translations':   None,
            'elements':                 [], 
            'num_elements':             0, 
            'column_names':             [ ],
            'column_translations':      { },
        }
        return unResult   
   
    

 
# #############################################################
# Relation candidate accesors
#

    
    security.declarePrivate('getTiposCandidatosReferenceFieldNamed')
    def getTiposCandidatosReferenceFieldNamed(self , theElement, theReferenceFieldName):

        if ( theElement == None) or not theReferenceFieldName:
            return []

        unSchema = theElement.schema
        if not unSchema.has_key( theReferenceFieldName):
            return []
            
        unField             = unSchema[ theReferenceFieldName]
        if not unField:
            return []
                
        if unField.__class__.__name__ == "RelationField":
            return self.getTiposCandidatosRelationFieldNamed(        theElement, theReferenceFieldName, unField)
        
        if unField.__class__.__name__ == "ComputedField":
            return self.getTiposCandidatosComputedFieldNamed(        theElement, theReferenceFieldName, unField)

        return self.getTiposCandidatosNoRelationReferenceFieldNamed( theElement, theReferenceFieldName, unField)    
        
        
        
     
    security.declarePrivate('getTiposCandidatosComputedFieldNamed')
    def getTiposCandidatosComputedFieldNamed(self , theElement, theReferenceFieldName, theField):
        if not theReferenceFieldName or not theField:
            return []

        someComputedTypesString = ''
        try:
            someComputedTypesString = theField.computed_types
        except:
            None    
        if not someComputedTypesString:
            return []
        
        someComputedTypes = fEvalString( someComputedTypesString)

        return someComputedTypes
             
 
    
                
    security.declarePrivate('getTiposCandidatosNoRelationReferenceFieldNamed')
    def getTiposCandidatosNoRelationReferenceFieldNamed(self , theElement, theReferenceFieldName, theField):
        if not theReferenceFieldName or not theField:
            return []

        someAllowedTypes = []
        try:
            someAllowedTypes = theField.allowed_types
        except:
            None                    

        return someAllowedTypes
             
            
            
            
    security.declarePrivate('getTiposCandidatosRelationFieldNamed')
    def getTiposCandidatosRelationFieldNamed(self , theElement, theReferenceFieldName, theField):
 
        if not theReferenceFieldName or not theField:
            return []

            
        unRelationName     = theField.relationship
       
      
        aRelationslib = getToolByName( theElement, RELATIONS_LIBRARY)        
        if not aRelationslib:
            return []
            
        aRuleset = None
        try:
            aRuleset = aRelationslib.getRuleset( unRelationName)
        except ValueError:
            None
            
        if not aRuleset:
            return []

        someTypeConstraints = aRuleset.objectValues( "PortalTypeConstraint")
        if not someTypeConstraints:
            return []
        someAllowedTypes = []
        for aTypeConstraint in someTypeConstraints:
            aConstraintAllowedTypes = aTypeConstraint.getAllowedTargetTypes()
            if aConstraintAllowedTypes:
                for anAllowedTypeName in aConstraintAllowedTypes:
                    someAllowedTypes.append( anAllowedTypeName)

        return someAllowedTypes
            
            
 
            
    
    
    
 

            
    
    security.declarePrivate('fRetrieveCandidatesTraversalConfig')
    def fRetrieveCandidatesTraversalConfig(self,    
        theTimeProfilingResults     =None,
        theElement                  =None,
        theCanReturnValues          =True, 
        theViewName                 ='',
        theTypeConfig               =None, 
        theAllTypeConfigs           =None, 
        theTraversalConfig          =None, 
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None, 
        theFeatureFilters           =None,
        theCurrentTraversalResult   =None,
        theAdditionalParams         =None):

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveCandidatesTraversalConfig', theTimeProfilingResults)

        try:
    
            unCandidatesResult = self.fNewVoidCandidatesResult()                
                
            if ( theElement == None) or not theTraversalConfig:
                return unCandidatesResult

            unCandidatesResult[ 'traversal_config'] = theTraversalConfig
                
            aFieldName         = theTraversalConfig.get( 'relation_name', '') or ''
            if not aFieldName:
                return unCandidatesResult

            unCandidatesResult[ 'traversal_name'] = aFieldName
            unCandidatesResult[ 'traversal_translations'] = self.fAttributeTranslationsFromCache( 
                theElement            = theElement,
                theFieldName          = aFieldName, 
                theTranslationsCaches = theTranslationsCaches,
                theResultDict         = None, 
                theResultKey          = None,
                theAdditionalParams   = theAdditionalParams,
            )                                         
            unCandidatesResult[ 'column_names'] = [ 'title', 'description', ]
            unCandidatesResult[ 'column_translations'] = self.getTranslationsForDefaultAttributes( theElement)

            unosResultsCandidatos = unCandidatesResult[ 'elements']

            
            unSchema = theElement.schema
            if not unSchema.has_key( aFieldName):
                return unCandidatesResult
                
            unField             = unSchema[ aFieldName]
            if not unField:
                return unCandidatesResult
                        
            unInverseRelationFieldName =  ''
            try:
                unInverseRelationFieldName = unField.inverse_relation_field_name                       
            except:
                None
                        
            unosTiposElementos = []
            if unField.__class__.__name__ == "RelationField":
                unosTiposElementos =  self.getTiposCandidatosRelationFieldNamed(        theElement, aFieldName, unField)
            else:
                unosTiposElementos = self.getTiposCandidatosNoRelationReferenceFieldNamed( theElement, aFieldName, unField)    
            
            someAcceptedPortalTypes = []
            unTodosArquetipos = False
            
            someRelatedItems   = theTraversalConfig.get( 'related_types', []) or []
            for aRelatedItems in someRelatedItems:
                somePortalTypes = aRelatedItems.get( 'portal_types', []) or []
                for unTipoElemento in somePortalTypes:
                    if unTipoElemento == 'Arquetipo':
                        unTodosArquetipos = True
                        break
                    else:
                        if ( not unosTiposElementos or ( unTipoElemento in unosTiposElementos)) and not( unTipoElemento in someAcceptedPortalTypes):
                            someAcceptedPortalTypes.append( unTipoElemento)
                if unTodosArquetipos:
                    break
    
            unosPosiblesCandidatos = []
            
            if theTraversalConfig.get( 'candidates_scope','').lower() == 'owner':
                
                unPropietario = theElement.getContenedor()
                if not unPropietario:
                    return unCandidatesResult
                
                unPropietarioEsColeccion = False
                try:
                    unPropietarioEsColeccion =  unPropietario.getEsColeccion()
                except:
                    None
                if unPropietarioEsColeccion:    
                    unPropietario = unPropietario.getContenedor()
                    
                if not unPropietario:
                    return unCandidatesResult
                    
                unLimitToTypes = someAcceptedPortalTypes
                if unTodosArquetipos:
                    unLimitToTypes = None
                    
                aResult = self.fRetrieveTypeConfig(
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theElement                  =unPropietario, 
                    theParent                   =None,
                    theParentTraversalName      ='',
                    theTypeConfig               =None, 
                    theAllTypeConfigs           =theAllTypeConfigs, 
                    theViewName                 ='', 
                    theRetrievalExtents         =[ 'traversals', ],
                    theWritePermissions         =None,
                    theFeatureFilters           ={ 'types': unLimitToTypes, 'attrs': [ 'title', 'description' ], 'relations': [], }, 
                    theTranslationsCaches       =theTranslationsCaches,
                    theCheckedPermissionsCache  =theCheckedPermissionsCache,
                    theAdditionalParams         =theAdditionalParams
                )
                if aResult:
                    for unTraversalResult in aResult[ 'traversals']:
                        if unTraversalResult[ 'traversal_kind'] == 'aggregation':
                            for unCollectionOrElementResult in unTraversalResult[ 'elements']:
                                if unCollectionOrElementResult.get( 'is_collection', False): 
                                    for unCollectionTraversalResult in unCollectionOrElementResult['traversals']:
                                        if unCollectionTraversalResult[ 'traversal_kind'] == 'aggregation':
                                            for unElementResult in unCollectionTraversalResult[ 'elements']:
                                                unPosibleCandidato = unElementResult[ 'object']   
                                                if unPosibleCandidato and not ( unPosibleCandidato in unosPosiblesCandidatos):
                                                    unosPosiblesCandidatos.append( unPosibleCandidato)   
                                else:
                                    unPosibleCandidato = unCollectionOrElementResult[ 'object']   
                                    if unPosibleCandidato and not ( unPosibleCandidato in unosPosiblesCandidatos):
                                        unosPosiblesCandidatos.append( unPosibleCandidato)   
                                    
                                                    
                                             
            
            else:            
                unPortalCatalog = getToolByName( theElement, 'portal_catalog')
        
                unPathDelRaiz = theElement.fPathDelRaiz()
                
                # OJO ACV 20090609 
                # Want to remove index getPathDelRaiz introduced by BPD, eMOF and other ModelDDvlPlone based applications
                # and use the standard Plone index "path" instead
                if unTodosArquetipos:               
                    unaBusqueda = { 
    #                   'getPathDelRaiz' :   unPathDelRaiz,
                       'path' :              unPathDelRaiz,
                    }
                else:
                    unaBusqueda = { 
                        'meta_type'      :   someAcceptedPortalTypes,
    #                   'getPathDelRaiz' :   unPathDelRaiz,
                        'path' :             unPathDelRaiz,
                    }

         
                unosResultadosBusqueda = unPortalCatalog.searchResults( **unaBusqueda)
                unosPosiblesCandidatos = [ unTraversalResultadoBusqueda.getObject() for unTraversalResultadoBusqueda in unosResultadosBusqueda]
            
            if not unosPosiblesCandidatos:
                return unCandidatesResult
                
            
            someCurrentlyLinked = []
            if theCurrentTraversalResult:
                someCurrentlyLinked = [ unCurrentlyLinkedResult[ 'object'] for unCurrentlyLinkedResult in theCurrentTraversalResult['elements'] ]
     
            unosCandidatos = []        
            
            if unTodosArquetipos:        
                for unCandidato in unosPosiblesCandidatos:
                    if unCandidato and not ( unCandidato == theElement) and not ( unCandidato in someCurrentlyLinked):
                        unEsColeccion = False
                        try:
                            unEsColeccion  = unCandidato.getEsColeccion()
                        except:
                            None
                        if not unEsColeccion:
                            unosCandidatos.append( unCandidato)
            else:                
                for unCandidato in unosPosiblesCandidatos:
                    if unCandidato and not ( unCandidato == theElement) and not ( unCandidato in someCurrentlyLinked):
                        if unCandidato.meta_type in someAcceptedPortalTypes:
                            unosCandidatos.append( unCandidato)
    
    
            if not unosCandidatos:
                return unCandidatesResult
            
            unaListaAOrdenar = [ ( "%s--%s" % ( unCandidato.portal_type , unCandidato.Title().lower()) , unCandidato) for unCandidato in unosCandidatos]
            unaListaAOrdenar.sort()
            unosCandidatosOrdenados = [ unCandidato for (laClave, unCandidato) in unaListaAOrdenar]
        
            for unCandidato in unosCandidatosOrdenados:
                unElementResult = self.fRetrieveTypeConfig_recursive( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theResult                   =None, 
                    theElement                  =unCandidato, 
                    theParent                   =None,
                    theParentTraversalName      =None,
                    theCanReturnValues          =True, 
                    theViewName                 ='',
                    theRetrievalExtents         =[ 'traversals', ], 
                    theTypeConfig               =None, 
                    theAllTypeConfigs           =theAllTypeConfigs, 
                    theParentTraversalResult    =None, 
                    theTranslationsCaches       =theTranslationsCaches, 
                    theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                    theWritePermissions         =[ 'object', 'relations', ], 
                    theFeatureFilters           ={ 'attrs': [ 'title', 'description', ] , 'aggregations':[], 'relations':[ unInverseRelationFieldName, ],}, 
                    theInstanceFilters          =None,                    
                    theAdditionalParams         =theAdditionalParams
                )                    
                if unElementResult:
                    
                    self.pBuildResultDicts( unElementResult, [ 'traversals',])
                    
                    if (not unInverseRelationFieldName) or not unElementResult[ 'traversals_by_name'][ unInverseRelationFieldName][ 'max_multiplicity_reached']:
                        unosResultsCandidatos.append( unElementResult)
        
            unCandidatesResult[ 'num_elements'] = len( unosResultsCandidatos)
            
            return unCandidatesResult
            
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveCandidatesTraversalConfig', theTimeProfilingResults)

            
            
            
            
    
 

            
    
    security.declarePrivate('fRetrieveElementsOfType')
    def fRetrieveElementsOfType(self,    
        theTimeProfilingResults     =None,
        theElement                  =None,
        theTypeNames                =None,
        theAllTypeConfigs           =None, 
        theTranslationsCaches       =None, 
        theCheckedPermissionsCache  =None, 
        theWritePermissions         =None, 
        theAdditionalParams         =None):
        """Retrieve result structures for all elements of a Type in a Plone site.
        
        """

        if not ( theTimeProfilingResults == None):
            self.pProfilingStart( 'fRetrieveElementsOfType', theTimeProfilingResults)

        try:
            
            unCandidatesResult = self.fNewVoidCandidatesResult()                
                
            if ( theElement == None):
                return unCandidatesResult

            unCandidatesResult[ 'traversal_name'] = cElementsOfTypeTraversalName
            unCandidatesResult[ 'column_names'] = [ 'title', 'description', ]
            unCandidatesResult[ 'column_translations'] = self.getTranslationsForDefaultAttributes( theElement)
            
                  
                                         
            unTodosArquetipos = False
            someAcceptedPortalTypes = []
            if not theTypeNames:
                unTodosArquetipos = True
            else:
                for unTipoElemento in theTypeNames:
                    if unTipoElemento == 'Arquetipo':
                        unTodosArquetipos = True
                        break
                    else:
                        if  not( unTipoElemento in someAcceptedPortalTypes):
                            someAcceptedPortalTypes.append( unTipoElemento)

                            
            unPortalCatalog = getToolByName( theElement, 'portal_catalog')
            
            unPathDelRaiz = theElement.fPathDelRaiz()
 
            if unTodosArquetipos:               
                unaBusqueda = { 
                   'path' :              unPathDelRaiz,
                }
            else:
                unaBusqueda = { 
                    'meta_type'      :   someAcceptedPortalTypes,
                    'path' :             unPathDelRaiz,
                }
     
            unosResultadosBusqueda = unPortalCatalog.searchResults( **unaBusqueda)
            unosPosiblesCandidatos = [ unResultadoBusqueda.getObject() for unResultadoBusqueda in unosResultadosBusqueda]
            
            if not unosPosiblesCandidatos:
                return unCandidatesResult
                
            unosCandidatos = []        
            
            if unTodosArquetipos:        
                for unCandidato in unosPosiblesCandidatos:
                    unEsColeccion = False
                    try:
                        unEsColeccion  = unCandidato.getEsColeccion()
                    except:
                        None
                    if not unEsColeccion:
                        unosCandidatos.append( unCandidato)
            else:                
                for unCandidato in unosPosiblesCandidatos:
                    if unCandidato.meta_type in someAcceptedPortalTypes:
                        unosCandidatos.append( unCandidato)
    
            if not unosCandidatos:
                return unCandidatesResult
            
            unaListaAOrdenar = [ ( "%s--%s" % ( unCandidato.portal_type , '/'.join( unCandidato.getPhysicalPath())) , unCandidato) for unCandidato in unosCandidatos]
            unaListaAOrdenar.sort()
            unosCandidatosOrdenados = [ unCandidato for (laClave, unCandidato) in unaListaAOrdenar]
        
            unosResultsCandidatos = unCandidatesResult[ 'elements']

            for unCandidato in unosCandidatosOrdenados:
                unElementResult = self.fRetrieveTypeConfig_recursive( 
                    theTimeProfilingResults     =theTimeProfilingResults,
                    theResult                   =None, 
                    theElement                  =unCandidato, 
                    theParent                   =None,
                    theParentTraversalName      =None,
                    theCanReturnValues          =True, 
                    theViewName                 ='',
                    theRetrievalExtents         =[ 'traversals', ], 
                    theTypeConfig               =None, 
                    theAllTypeConfigs           =theAllTypeConfigs, 
                    theParentTraversalResult    =None, 
                    theTranslationsCaches       =theTranslationsCaches, 
                    theCheckedPermissionsCache  =theCheckedPermissionsCache, 
                    theWritePermissions         =theWritePermissions, 
                    theFeatureFilters           ={ 'attrs': [ 'title', 'description', ] , 'aggregations':[], 'relations':[],}, 
                    theInstanceFilters          =None,                    
                    theAdditionalParams         =theAdditionalParams
                )                    
                if unElementResult:
                    unosResultsCandidatos.append( unElementResult)
        
            unCandidatesResult[ 'num_elements'] = len( unosResultsCandidatos)
            
            return unCandidatesResult
            
        finally:
            if not ( theTimeProfilingResults == None):
                self.pProfilingEnd( 'fRetrieveElementsOfType', theTimeProfilingResults)

            
            
            
            
                    

 
 
 
 
 
 
 
 
 
 

            
    

 

