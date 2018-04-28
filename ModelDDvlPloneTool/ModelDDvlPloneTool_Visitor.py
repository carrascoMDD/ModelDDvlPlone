# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Visitor.py
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

import StringIO

import logging

from AccessControl import ClassSecurityInfo


from ModelDDvlPloneTool_Visitor_Dumper import ModelDDvlPloneTool_Visitor_Dumper



class ModelDDvlPloneTool_Visitor:
    """
    """
    security = ClassSecurityInfo()

    vDumper = ModelDDvlPloneTool_Visitor_Dumper()
    vDumper.setBeDummy( False)





# #########################
#  Traversal config scanning and resolution methods
#

 

            
    def preScanTypeConfigs( self, theTravCtxt, theItemsConfig):
        # self.logDebug( theTravCtxt, "preScanTypeConfigs START theItemsConfig=\n%s\n" % str( theItemsConfig ))
        if theTravCtxt is None or theItemsConfig is None:
            self.logError( theTravCtxt, "preScanTypeConfigs theTravCtxt is None or theItemsConfig is None")
            return self

        if not theTravCtxt.has_key('type_configs'):
            theTravCtxt[ 'type_configs'] = {}
        
        someFoundTypeConfigs = theTravCtxt[ 'type_configs']
        
        self.preScanTypeConfigsStandAloneRecursive( theItemsConfig, someFoundTypeConfigs)
        
        return self





            
    def chooseTypeConfig( self, theTravCtxt, theItemsConfig, theTypeName):
        if not theTravCtxt or not theItemsConfig or not theTypeName :
            return None

        for aTypeConfig in theItemsConfig:
            if aTypeConfig.has_key( 'portal_types'):
                somePortalTypes = aTypeConfig[ 'portal_types']
                if theTypeName in somePortalTypes:
                    if not aTypeConfig.has_key( 'reuse_config'):
                        if aTypeConfig.has_key( 'mode'):
                            aMode = aTypeConfig[ 'mode']
                            if not ( aMode == 'Reference'):
                                return aTypeConfig
                        else:
                            return aTypeConfig
            
        for aTypeConfig in theItemsConfig:
            if aTypeConfig.has_key( 'portal_types'):
                somePortalTypes = aTypeConfig[ 'portal_types']
                if theTypeName in somePortalTypes:
                    if not aTypeConfig.has_key( 'reuse_config'):
                        return aTypeConfig
                    else:
                    
                        unTypeConfigName = aTypeConfig[ 'reuse_config']
                
                        if theTravCtxt.has_key( 'type_configs'):
                        
                            allypeConfigs = theTravCtxt[ 'type_configs']
                            if allypeConfigs.has_key( theTypeName):
                        
                                someTypeConfigs = allypeConfigs[ theTypeName]
                                if someTypeConfigs.has_key( unTypeConfigName):
                        
                                    aTypeConfig = someTypeConfigs[ unTypeConfigName]
                                    return aTypeConfig
                                else:
                                    if someTypeConfigs.has_key( 'Default'):
                        
                                        aTypeConfig = someTypeConfigs[ 'Default']
                                        return aTypeConfig

        return None

     
     
     
     
  




    def typeNamesFromItemsConfigs( self, theItemsConfigs):       
        unosNombresTipos = []
        for aSubitemConfig in theItemsConfigs:
            if aSubitemConfig.has_key( 'portal_types'):
                unosPortalTypes = aSubitemConfig[ 'portal_types']
                unosNombresTipos = unosNombresTipos + unosPortalTypes 
        return unosNombresTipos
    





# #########################
#  Auxiliary content accessor methods
#



    def getContenidosFromSubitemsConfigs( self, theObject, theItemsConfigs):
        if not theObject:
            return []
        unosNombresTipos = self.typeNamesFromItemsConfigs( theItemsConfigs)
        if not unosNombresTipos:
            return []
            
        someSubObjects = theObject.getContenidos( unosNombresTipos)               
        return someSubObjects


     
     
     
     
     
 

# #########################
#  Traversal and visit methods
#
    
     


    def visitAttrs( self, theTravCtxt, theTypeConfig, theObject):
        # self.logDebug( theTravCtxt, "visitAttrs START theObject=%s theTypeConfig=\n%s\n" % ( str( theObject), str( theTypeConfig),) )

        if theTravCtxt is None or theTypeConfig is None or theObject is None:
            self.logError( theTravCtxt, "visitAttrs theTravCtxt is None or theTypeConfig is None or theObject is None")
            return self

        
        if theTypeConfig.has_key( 'attrs'):
        
            someAttrConfig = theTypeConfig[ 'attrs']
            
            
            
            someExtraOptionsMeta        = [ ]
            unExtraOption = 'Content'
            if theTypeConfig.has_key( 'mode') and theTypeConfig[ 'mode'] == 'Reference':
                unExtraOption = 'Reference'
            someExtraOptionsTitle       = [ unExtraOption]
            someExtraOptionsDescription = [ ]
            someExtraOptionsAttrs       = [ ]
            someExtraOptionsTexts       = [ ]
            aBreakBeforeMetaAttrs       = True
            aBreakBeforeNonTextAttrs    = True
            aBreakBeforeTextAttrs       = True

            if theTypeConfig.has_key( 'extension'):
                unaExtension = theTypeConfig[ 'extension']
                
                if unaExtension == 'OneParagraph':
                    someExtraOptionsMeta.append( 'OneParagraph')
                    someExtraOptionsTitle.append( 'OneParagraph')
                    someExtraOptionsDescription.append( 'OneParagraph')
                    someExtraOptionsAttrs.append( 'OneParagraph')
                    someExtraOptionsTexts.append( 'OneParagraph')
                    aBreakBeforeMetaAttrs       = False
                    aBreakBeforeNonTextAttrs    = False
                    aBreakBeforeTextAttrs       = False
                    
                if unaExtension == 'AttrsOneParagraph':
                    someExtraOptionsMeta.append( 'OneParagraph')
                    someExtraOptionsAttrs.append( 'OneParagraph')
                    someExtraOptionsDescription.append( 'OneParagraph')
                    someExtraOptionsTexts.append( 'OneParagraph')
                    aBreakBeforeMetaAttrs       = False
                    aBreakBeforeTextAttrs       = False
                    aBreakBeforeNonTextAttrs    = False

                if unaExtension == 'NonTextAttrsOneParagraph':
                    someExtraOptionsMeta.append( 'OneParagraph')
                    someExtraOptionsAttrs.append( 'OneParagraph')
                    aBreakBeforeMetaAttrs       = False
                    aBreakBeforeNonTextAttrs    = False
                    
            
            someNonTextAttrConfigMetaAndValues  = []
            someTextAttrConfigMetaAndValues     = []
            aTitleAttrConfigMetaAndValue          = None
            aDescriptionAttrConfigMetaAndValue    = None
            someMetaAttrConfigMetaAndValues  = []

            
            for unAttrConfig in someAttrConfig:
                unAttrName      = unAttrConfig[0]
                someAttrOptions = unAttrConfig[2:]
                
                #ACV OJO
                if unAttrName == "titleAndOwnerTitle":
                    a = 23
                    
                if 'Meta' in someAttrOptions:
                    unAttrMetaAndValue = theObject.getMetaValue( unAttrName)
                    if unAttrMetaAndValue:
                        if unAttrMetaAndValue[ 6].lower() == 'string[]':
                            unStringCompleta = ""
                            unValue = unAttrMetaAndValue[ 1]
                            if unValue:
                                for unString in unValue:
                                    unStringCompleta += (unString + " ")
                                unAttrMetaAndValue[ 1] = unStringCompleta
                        someMetaAttrConfigMetaAndValues.append( [ unAttrConfig, unAttrMetaAndValue, someExtraOptionsMeta, ])
                else:                
                    unAttrMetaAndValue = theObject.getAttributeMetaAndValue( unAttrName)

                    if unAttrMetaAndValue:
                        unAttrValue   = unAttrMetaAndValue[ 1]
                        unAttrType    = unAttrMetaAndValue[ 6]
    
                        if 'Title' in someAttrOptions:
                            if not unAttrValue:
                                unAttrMetaAndValue[1] = theObject.title_or_id()                                        
                            aTitleAttrConfigMetaAndValue = [ unAttrConfig, unAttrMetaAndValue, someExtraOptionsTitle, ]
                        elif 'Description' in someAttrOptions:
                            if unAttrValue or ( 'Optional' in someAttrOptions):
                                aDescriptionAttrConfigMetaAndValue = [ unAttrConfig, unAttrMetaAndValue, someExtraOptionsDescription, ]
                        elif unAttrValue or ( 'Optional' in someAttrOptions):                
                            if unAttrMetaAndValue[6].lower() == 'text':
                                someTextAttrConfigMetaAndValues.append( [ unAttrConfig, unAttrMetaAndValue, someExtraOptionsTexts, ])
                            else:
                                someNonTextAttrConfigMetaAndValues.append( [ unAttrConfig, unAttrMetaAndValue, someExtraOptionsAttrs, ])



            self.vDumper.pO_attrs_begin( theTravCtxt)

# ACV OJO 20080627
            if len( theTravCtxt[ 'stack']) > 0:                
                if aTitleAttrConfigMetaAndValue:
                    self.vDumper.pO_title( theTravCtxt, theTypeConfig, theObject, aTitleAttrConfigMetaAndValue)

                if someMetaAttrConfigMetaAndValues:
                    if aBreakBeforeMetaAttrs:
                        self.vDumper.pO_break( theTravCtxt)
                    for unMetaAttrConfigMetaAndValues in someMetaAttrConfigMetaAndValues:
                        self.vDumper.pO_attr_meta( theTravCtxt, theTypeConfig, theObject, unMetaAttrConfigMetaAndValues)                
                

                
            if someNonTextAttrConfigMetaAndValues:     
                if aBreakBeforeNonTextAttrs:
                    self.vDumper.pO_break( theTravCtxt)
                               
                for unNonTextAttrConfigMetaAndValue in someNonTextAttrConfigMetaAndValues:
                    self.vDumper.pO_attr_nonText( theTravCtxt, theTypeConfig, theObject, unNonTextAttrConfigMetaAndValue)                



            if aBreakBeforeTextAttrs:
                self.vDumper.pO_break( theTravCtxt)

# ACV OJO 20080627
            if len( theTravCtxt[ 'stack']) > 0:                
                if aDescriptionAttrConfigMetaAndValue:
                    self.vDumper.pO_description( theTravCtxt, theTypeConfig, theObject, aDescriptionAttrConfigMetaAndValue)
 
                 
            if someTextAttrConfigMetaAndValues:
                for unTextAttrConfigMetaAndValue in someTextAttrConfigMetaAndValues:
                    self.vDumper.pO_attr_text( theTravCtxt, theTypeConfig, theObject, unTextAttrConfigMetaAndValue)

        self.vDumper.pO_attrs_end( theTravCtxt)

        # self.logDebug( theTravCtxt, "visitAttrs END")

        return self








  



    def visitTraversals( self, theTravCtxt, theTypeConfig, theObject):
        # self.logDebug( theTravCtxt, "visitTraversals START theObject=%s theTypeConfig=\n%s\n" % ( str( theObject), str( theTypeConfig),) )

        if theTravCtxt is None or theTypeConfig is None or theObject is None:
            self.logError( theTravCtxt, "visitTraversals theTravCtxt is None or theTypeConfig is None or theObject is None")
            return self

        if not theTypeConfig.has_key( 'traversals'):
            return self
        
        someTraversalConfigs = theTypeConfig[ 'traversals']
        for aTraversalConfig in someTraversalConfigs:
            if aTraversalConfig.has_key( 'subitems'):
                self.visitSubitems( theTravCtxt, aTraversalConfig, theObject)                        

            elif aTraversalConfig.has_key( 'related_types'):
                self.visitRelation( theTravCtxt, aTraversalConfig, theObject)        
              
        # self.logDebug( theTravCtxt, "visitTraversals END")

        return self

      
        



    def visitSubitems( self, theTravCtxt, theTraversalConfig, theObject):
        # self.logDebug( theTravCtxt, "visitSubitems START theObject=%s theTraversalConfig=\n%s\n" % ( str( theObject), str( theTraversalConfig),) )

        if theTravCtxt is None or theTraversalConfig is None or theObject is None:
            self.logError( theTravCtxt, "visitSubitems theTravCtxt is None or theTraversalConfig is None or theObject is None")
            return self

        if not theTraversalConfig.has_key( 'subitems'):
            return self   
        someSubitemsConfigs = theTraversalConfig[ 'subitems']
        
        someSubObjects = self.getContenidosFromSubitemsConfigs( theObject, someSubitemsConfigs)               
        if not someSubObjects:
            return self

        aTitleLevel = theTravCtxt[ 'titleLevel']        

        aCustomTitle = None            
        if theTraversalConfig.has_key( 'custom_title'):
            if len( theTravCtxt[ 'stack']) > 2: 
                theTravCtxt[ 'titleLevel'] = aTitleLevel + 1
            aCustomTitle = theTraversalConfig[ 'custom_title']
            
        unExcludeFromTextualView = False
        for aSubitemConfig in someSubitemsConfigs:
            if aSubitemConfig.has_key( 'exclude_from_views'):
                if 'General' in aSubitemConfig[ 'exclude_from_views']:
                    unExcludeFromTextualView = True
            
            
        if not unExcludeFromTextualView:
            self.vDumper.pO_subitems_begin( theTravCtxt, aCustomTitle)
        
        unSubObjectIndex = 0
        aSubObjectsLen = len( someSubObjects)
        for aSubObject in someSubObjects:
        
            if theTravCtxt.has_key( 'collectSubitemsAndRelateds') and theTravCtxt[ 'collectSubitemsAndRelateds'] == True and theTravCtxt.has_key( 'subitemsAndRelatedsByObjectPath'):
                someSubitemsAndRelatedsByObjectPath = theTravCtxt[ 'subitemsAndRelatedsByObjectPath']
                anObjectPath = theObject.fPhysicalPathString()
                if someSubitemsAndRelatedsByObjectPath.has_key( anObjectPath):
                    anObjectSubitemsAndRelateds = someSubitemsAndRelatedsByObjectPath[ anObjectPath]
                else:
                    anObjectSubitemsAndRelateds = [ ]                
                    someSubitemsAndRelatedsByObjectPath[ anObjectPath] = anObjectSubitemsAndRelateds
                if not aSubObject in anObjectSubitemsAndRelateds:
                    anObjectSubitemsAndRelateds.append( aSubObject)

                unEsColeccion = False
                try:
                    unEsColeccion = theObject.getEsColeccion()
                except:
                    None
                
                if unEsColeccion:
                    unContenedor = theObject.getContenedor()
                    if unContenedor:
                        aContenedorObjectPath = unContenedor.fPhysicalPathString()
                        if someSubitemsAndRelatedsByObjectPath.has_key( aContenedorObjectPath):
                            aContenedorSubitemsAndRelateds = someSubitemsAndRelatedsByObjectPath[ aContenedorObjectPath]
                        else:
                            aContenedorSubitemsAndRelateds = [ ]                
                            someSubitemsAndRelatedsByObjectPath[ aContenedorObjectPath] = aContenedorSubitemsAndRelateds
                        for aSubitemHere in anObjectSubitemsAndRelateds:
                            if not aSubitemHere in aContenedorSubitemsAndRelateds:
                                aContenedorSubitemsAndRelateds.append( aSubitemHere)

                
            self.chooseRootOrSubitem( theTravCtxt, someSubitemsConfigs, aSubObject, unSubObjectIndex, aSubObjectsLen, unExcludeFromTextualView) 
            unSubObjectIndex += 1
                
        if not unExcludeFromTextualView:
            self.vDumper.pO_subitems_end( theTravCtxt)
        
        theTravCtxt[ 'titleLevel'] = aTitleLevel
            
        # self.logDebug( theTravCtxt, "visitSubitems END")

        return self

           
           

            
           
            
             
           

           
           
           



    def visitRelation( self, theTravCtxt, theRelationConfig, theObject):
        # self.logDebug( theTravCtxt, "visitRelation START theObject=%s theRelationConfig=\n%s\n" % ( str( theObject), str( theRelationConfig),) )

        if theTravCtxt is None or theRelationConfig is None or theObject is None:
            self.logError( theTravCtxt, "visitRelation theTravCtxt is None or theRelationConfig is None or theObject is None")
            return self
           
        if not( theRelationConfig.has_key( 'relation_name')):
            return self            
        unRelationName = theRelationConfig[ 'relation_name']
        if not unRelationName:
            return self
            
        unReferenceMeta = theObject.getReferenceMeta( unRelationName)
        if not unReferenceMeta:
            return []
            
        if not( theRelationConfig.has_key( 'related_types')):
            return self            
        someRelatedTypeConfigs = theRelationConfig[ 'related_types']
        if not someRelatedTypeConfigs:
            return self              
    
        todosNombresTipos = self.typeNamesFromItemsConfigs( someRelatedTypeConfigs)
        if not todosNombresTipos:
            return self
            
        aReferenceMetaAndValue = theObject.getReferenceMetaAndValue( unRelationName)
        if not aReferenceMetaAndValue:
            return self
        aReferenceValue = aReferenceMetaAndValue[ 1]
        unEsMultiValued = aReferenceMetaAndValue[ 6]
        
        if not aReferenceValue:
            return self

        if unEsMultiValued:
            someRelatedObjectsOfRightTypes = [ unElemento for unElemento in aReferenceValue if unElemento.meta_type in todosNombresTipos] 
            if not someRelatedObjectsOfRightTypes:
                return self
        else:
            if not aReferenceValue[0]:
                return self
            else:
                if not aReferenceValue[ 0].meta_type in todosNombresTipos:
                    return self
                someRelatedObjectsOfRightTypes = [ aReferenceValue[ 0] ]
        
        aTitleLevel = theTravCtxt[ 'titleLevel']
        if len( theTravCtxt[ 'stack']) > 2: 
            theTravCtxt[ 'titleLevel'] = aTitleLevel + 1
     
        unExcludeFromTextualView = False
        if theRelationConfig.has_key( 'exclude_from_views'):
            if 'General' in theRelationConfig[ 'exclude_from_views']:
                unExcludeFromTextualView = True
                    
  
        if not unExcludeFromTextualView:
            self.vDumper.pO_relation_begin( theTravCtxt, theRelationConfig, theObject, unReferenceMeta)
        
        unReferencedObjectIndex = 0
        aRelatedObjectsLen = len( someRelatedObjectsOfRightTypes)
        for aReferencedObject in someRelatedObjectsOfRightTypes:

            if theTravCtxt.has_key( 'collectSubitemsAndRelateds') and theTravCtxt[ 'collectSubitemsAndRelateds'] == True and theTravCtxt.has_key( 'subitemsAndRelatedsByObjectPath'):
                someSubitemsAndRelatedsByObjectPath = theTravCtxt[ 'subitemsAndRelatedsByObjectPath']
                anObjectPath = theObject.fPhysicalPathString()
                if someSubitemsAndRelatedsByObjectPath.has_key( anObjectPath):
                    anObjectSubitemsAndRelateds = someSubitemsAndRelatedsByObjectPath[ anObjectPath]
                else:
                    anObjectSubitemsAndRelateds = [ ]                
                    someSubitemsAndRelatedsByObjectPath[ anObjectPath] = anObjectSubitemsAndRelateds
                if not aReferencedObject in anObjectSubitemsAndRelateds:
                    anObjectSubitemsAndRelateds.append( aReferencedObject)                

            self.chooseRelated( theTravCtxt, theRelationConfig, theObject, someRelatedTypeConfigs, aReferencedObject, unReferencedObjectIndex, aRelatedObjectsLen, unExcludeFromTextualView) 
            unReferencedObjectIndex += 1
            
        if not unExcludeFromTextualView:
            self.vDumper.pO_relation_end( theTravCtxt)

        theTravCtxt[ 'titleLevel'] = aTitleLevel
        
        return self








       
           
            
            
    def chooseRelated( self, theTravCtxt, theRelationConfig, theSourceObject, theItemsConfig, theObject, theIndex, theCount , theExcludeFromTextualView):
        # self.logDebug( theTravCtxt, "chooseRelated START theObject=%s theItemsConfig=\n%s\n" % ( str( theObject), str( theItemsConfig),) )

        if theTravCtxt is None or theItemsConfig is None or theObject is None:
            self.logError( theTravCtxt, "chooseRelated theTravCtxt is None or theItemsConfig is None or theObject is None")
            return self
        
        aTypeName = theObject.meta_type
        aTypeConfig = self.chooseTypeConfig( theTravCtxt, theItemsConfig, aTypeName)
        if not aTypeConfig:
            # self.logDebug( theTravCtxt, "chooseRelated no aTypeConfig for aTypeName=%s" % aTypeName)
            return self                         
            
        self.visit_asRelated( theTravCtxt, theRelationConfig, theSourceObject, aTypeConfig, theObject, theIndex, theCount , theExcludeFromTextualView)

        # self.logDebug( theTravCtxt, "choose END")
        
        return self
            

  

            
            
    def visit_asRelated( self, theTravCtxt, theRelationConfig, theSourceObject, theTypeConfig, theObject, theIndex, theCount , theExcludeFromTextualView):
        # self.logDebug( theTravCtxt, "visit_asRelated START theObject=%s theTypeConfig=\n%s\n" % ( str( theObject), str( theTypeConfig),) )

        if theTravCtxt is None or theTypeConfig is None or theObject is None:
            self.logError( theTravCtxt, "visit_asRelated theTravCtxt is None or theTypeConfig is None or theObject is None")
            return self
                    

        theTravCtxt[ 'stack'].append( [theObject,])


        if not theObject in theTravCtxt[ 'referencedObjects']:
            theTravCtxt[ 'referencedObjects'].append( theObject)
            
        if not theRelationConfig.has_key( 'if_not_included') or not theRelationConfig[ 'if_not_included' ] == 'NotInAnnex':
            someAddToAnnexIfNotIncludedObjects = theTravCtxt[ 'addToAnnexIfNotIncludedObjects']
            if not theObject in someAddToAnnexIfNotIncludedObjects:
                someAddToAnnexIfNotIncludedObjects.append( theObject)                


        aTitleLevel = theTravCtxt[ 'titleLevel']
        if len( theTravCtxt[ 'stack']) > 2: 
            theTravCtxt[ 'titleLevel'] = aTitleLevel + 1
        
        if theTypeConfig.has_key( 'divider') and len( theTravCtxt[ 'stack']) > 0:
            unasOpcionesDivider = theTypeConfig[ 'divider']
            if 'Before' in unasOpcionesDivider  and ('Always' in unasOpcionesDivider or  theIndex > 0):
                if 'White' in unasOpcionesDivider:
                    if not theExcludeFromTextualView:
                        self.vDumper.pO_white( theTravCtxt)
                if not theExcludeFromTextualView:
                    self.vDumper.pO_divider( theTravCtxt)
        
        if not theExcludeFromTextualView:
            self.vDumper.pO_object_begin( theTravCtxt, theObject) 
            
        if not theExcludeFromTextualView:
            self.visitAttrs( theTravCtxt, theTypeConfig, theObject)
        
        if not theExcludeFromTextualView:
            self.visitTraversals( theTravCtxt, theTypeConfig, theObject)
        
        
                
        if not theExcludeFromTextualView:
            self.vDumper.pO_object_end( theTravCtxt)

        if theTypeConfig.has_key( 'divider') and len( theTravCtxt[ 'stack']) > 0:
            unasOpcionesDivider = theTypeConfig[ 'divider']
            if 'After' in unasOpcionesDivider  and ('Always' in unasOpcionesDivider or theIndex < (theCount - 1) ):
                if not theExcludeFromTextualView:
                    self.vDumper.pO_divider( theTravCtxt)
                if 'White' in unasOpcionesDivider:
                    if not theExcludeFromTextualView:
                        self.vDumper.pO_white( theTravCtxt)


        theTravCtxt[ 'stack'].pop()

        theTravCtxt[ 'titleLevel'] = aTitleLevel


        # self.logDebug( theTravCtxt, "visit_asRelated END")
        
        return self
     
     
     



         
     
 




            
            
    def visit( self, theTravCtxt, theTypeConfig, theObject, theIndex, theCount, theExcludeFromTextualView ):
        # self.logDebug( theTravCtxt, "visit START theObject=%s theTypeConfig=\n%s\n" % ( str( theObject), str( theTypeConfig),) )

        if theTravCtxt is None or theTypeConfig is None or theObject is None:
            self.logError( theTravCtxt, "visit theTravCtxt is None or theTypeConfig is None or theObject is None")
            return self
            
        if theTypeConfig.has_key( 'conditions'):
            someConditions = theTypeConfig[ 'conditions']
            
            if 'ObjectValuesNotEmpty' in someConditions:
                if theTypeConfig.has_key( 'traversals'):
                    someTraversalConfigs = theTypeConfig[ 'traversals']
                    allSubitemsConfigs = [ ]
                    for aTraversalConfig in someTraversalConfigs:
                        if aTraversalConfig.has_key( 'subitems'):
                            someSubitemsConfigs = aTraversalConfig[ 'subitems']
                            allSubitemsConfigs = allSubitemsConfigs + someSubitemsConfigs
                    someSubObjects = self.getContenidosFromSubitemsConfigs( theObject, allSubitemsConfigs)                         
                    if len( someSubObjects) < 1:
                        return self
        
        if not theObject in theTravCtxt[ 'includedObjects']:
            theTravCtxt[ 'includedObjects'].append( theObject)

        theTravCtxt[ 'stack'].append( [theObject,])

        aTitleLevel = theTravCtxt[ 'titleLevel']
        if len( theTravCtxt[ 'stack']) > 2: 
            theTravCtxt[ 'titleLevel'] = aTitleLevel + 1


        if theTypeConfig.has_key( 'divider') and len( theTravCtxt[ 'stack']) > 0:
            unasOpcionesDivider = theTypeConfig[ 'divider']
            if 'Before' in unasOpcionesDivider  and ('Always' in unasOpcionesDivider or theIndex > 0 ):
                if 'White' in unasOpcionesDivider:
                    if not theExcludeFromTextualView:
                        self.vDumper.pO_white( theTravCtxt)
                if not theExcludeFromTextualView:
                    self.vDumper.pO_divider( theTravCtxt)

        
        if not theExcludeFromTextualView:
            self.vDumper.pO_object_begin( theTravCtxt, theObject ) 
        
        if not theExcludeFromTextualView:
            self.visitAttrs( theTravCtxt, theTypeConfig, theObject)
                
        if not theExcludeFromTextualView:
            self.visitTraversals( theTravCtxt, theTypeConfig, theObject)
                 
        
        if not theExcludeFromTextualView:
            self.vDumper.pO_object_end( theTravCtxt)

        if theTypeConfig.has_key( 'divider') and len( theTravCtxt[ 'stack']) > 0:
            unasOpcionesDivider = theTypeConfig[ 'divider']
            if 'After' in unasOpcionesDivider  and ('Always' in unasOpcionesDivider or theIndex < (theCount - 1) ):
                if not theExcludeFromTextualView:
                    self.vDumper.pO_divider( theTravCtxt)
                if 'White' in unasOpcionesDivider:
                    if not theExcludeFromTextualView:
                        self.vDumper.pO_white( theTravCtxt)

        theTravCtxt[ 'stack'].pop()

        theTravCtxt[ 'titleLevel'] = aTitleLevel

        # self.logDebug( theTravCtxt, "visit END")
        
        return self
     
     
     





            
            
    def chooseRootOrSubitem( self, theTravCtxt, theItemsConfig, theObject, theIndex, theCount, theExcludeFromTextualView ):
        # self.logDebug( theTravCtxt, "choose START theObject=%s theItemsConfig=\n%s\n" % ( str( theObject), str( theItemsConfig),) )

        if theTravCtxt is None or theItemsConfig is None or theObject is None:
            self.logError( theTravCtxt, "choose theTravCtxt is None or theItemsConfig is None or theObject is None")
            return self
        
        aTypeName = theObject.meta_type
        aTypeConfig = self.chooseTypeConfig( theTravCtxt, theItemsConfig, aTypeName)
        if not aTypeConfig:
            # self.logDebug( theTravCtxt, "choose no aTypeConfig for aTypeName=%s" % aTypeName)
            return self
            
        self.visit( theTravCtxt, aTypeConfig, theObject, theIndex, theCount, theExcludeFromTextualView)

        # self.logDebug( theTravCtxt, "choose END")
        
        return self
         
         
         
   



    def root( self, theTravCtxt, theItemsConfig, theRootObject):
        # self.logDebug( theTravCtxt, "root START theRootObject=%s theItemsConfig=\n%s\n" % ( str( theRootObject), str( theItemsConfig),) )

        if theTravCtxt is None or theItemsConfig is None or theRootObject is None:
            self.logError( theTravCtxt, "root theTravCtxt is None or theItemsConfig is None or theRootObject is None")
            return self

        self.vDumper.pO_inicio( theTravCtxt)
        
        self.chooseRootOrSubitem( theTravCtxt, theItemsConfig, theRootObject, 0, 1, False)

        self.vDumper.pO_fin( theTravCtxt)

        # self.logDebug( theTravCtxt, "root END")

        return self
            
            
                

      
            

    security.declarePrivate( 'preScanIncludedObjects')
    def preScanIncludedObjects( self, theTravCtxt, theItemsConfig, theRootObject):
        # self.logDebug( theTravCtxt, "preScanIncludedObjects START theRootObject=%s theItemsConfig=\n%s\n" % ( str( theRootObject), str( theItemsConfig),) )
              
        self.chooseRootOrSubitem( theTravCtxt, theItemsConfig, theRootObject, 0 , 1, False)
        
        # self.logDebug( theTravCtxt, "preScanIncludedObjects END theRootObject=%s theItemsConfig=\n%s\n" % ( str( theRootObject), str( theItemsConfig),) )
        
        return self
    
    
    
    
    
    
    
    def preScanIncludedAndAnnexObjects( self, theTravCtxt, theItemsConfig, theRootObject):
        # self.logDebug( theTravCtxt, "preScanIncludedAndAnnexObjects START theRootObject=%s theItemsConfig=\n%s\n" % ( str( theRootObject), str( theItemsConfig),) )

        aCollectSubitemsAndRelateds = False
        if theTravCtxt.has_key( 'collectSubitemsAndRelateds'):
            aCollectSubitemsAndRelateds = theTravCtxt[ 'collectSubitemsAndRelateds']
        theTravCtxt[ 'collectSubitemsAndRelateds'] = False

        aUseSubitemsAndRelateds = False
        if theTravCtxt.has_key( 'useSubitemsAndRelateds'):
            aUseSubitemsAndRelateds = theTravCtxt[ 'useSubitemsAndRelateds']
        theTravCtxt[ 'useSubitemsAndRelateds'] = False



        aTitleLevel = theTravCtxt[ 'titleLevel']
        aDumper = self.vDumper
        
        self.vDumper = ModelDDvlPloneTool_Visitor_Dumper()
        self.vDumper.setBeDummy( True)



        self.preScanIncludedObjects( theTravCtxt, theItemsConfig, theRootObject)

        someAddToAnnexIfNotIncludedObjects = theTravCtxt[ 'addToAnnexIfNotIncludedObjects']
        someIncludedObjects                = theTravCtxt[ 'includedObjects']
        
        someAddToAnnexObjects              = someAddToAnnexIfNotIncludedObjects + []
        for anObject in someIncludedObjects:
            if anObject in someAddToAnnexObjects:
                someAddToAnnexObjects.remove( anObject)   
        
        someToScan = someAddToAnnexObjects + []

        while len( someToScan):

            anAddToAnnexObject = someToScan[ 0]
            
            somePrevIncludedObjects = theTravCtxt[ 'includedObjects'] + [] 
                                  
            theTravCtxt[ 'addToAnnexIfNotIncludedObjects'] = [ ]
            self.preScanIncludedObjects(  theTravCtxt, theItemsConfig, anAddToAnnexObject)   
            
            someNowIncludedObjects = theTravCtxt[ 'includedObjects'] + []
            
            
            someJustIncludedObjects = someNowIncludedObjects + []
            for anObject in somePrevIncludedObjects:
                if anObject in someJustIncludedObjects:
                    someJustIncludedObjects.remove( anObject)   

            if anAddToAnnexObject in someJustIncludedObjects:
                someJustIncludedObjects.remove( anAddToAnnexObject)
                
            
            someNowAddToAnnexIfNotIncludedObjects = theTravCtxt[ 'addToAnnexIfNotIncludedObjects']
            someNowAddToAnnexObjects = someNowAddToAnnexIfNotIncludedObjects + []
            for anObject in someNowIncludedObjects:
                if anObject in someNowAddToAnnexObjects:
                    someNowAddToAnnexObjects.remove( anObject)   
                                    
            for anObject in someJustIncludedObjects:
                if anObject in someAddToAnnexObjects:
                    someAddToAnnexObjects.remove( anObject)   
            
            
            for anObject in someJustIncludedObjects:
                if anObject in someToScan:
                    someToScan.remove( anObject)   
                
            someToScan +=  someNowAddToAnnexObjects
            if anAddToAnnexObject in someToScan:
                someToScan.remove( anAddToAnnexObject)
            
        theTravCtxt[ 'addToAnnexObjects'] =  someAddToAnnexObjects 

        theTravCtxt[ 'titleLevel'] = aTitleLevel
        self.vDumper = aDumper

        theTravCtxt[ 'collectSubitemsAndRelateds'] = aCollectSubitemsAndRelateds 
        theTravCtxt[ 'useSubitemsAndRelateds'] = aUseSubitemsAndRelateds 

        # self.logDebug( theTravCtxt, "preScanIncludedAndAnnexObjects END theRootObject=%s theItemsConfig=\n%s\n" % ( str( theRootObject), str( theItemsConfig),) )
        
        return self            
            
      
      
      
      
      
      
    def rootScanPasses( self, theTravCtxt , theItemsConfig, theRootObject):
        # self.logDebug( theTravCtxt, "rootScanPasses START theRootObject=%s theItemsConfig=\n%s\n" % ( str( theRootObject), str( theItemsConfig),) )

        unInitialTitleLevel = theTravCtxt[ 'titleLevel']
           
        self.root( theTravCtxt, theItemsConfig, theRootObject)
            
        
        someAddToAnnexObjects = theTravCtxt[ 'addToAnnexObjects']
        if someAddToAnnexObjects:
            
            
            # hack to simulate that we've gone down two levels, 
            # and have the title index increased for top object subitems
            theTravCtxt[ 'stack'].append( [theRootObject,])
            theTravCtxt[ 'stack'].append( [theRootObject,])
    
            self.vDumper.pO_annex_begin( theTravCtxt)

    
            theTravCtxt[ 'titleLevel'] = unInitialTitleLevel
   
            unAddToAnnexObjectIndex = 0
            anAddToAnnexObjectsLen = len( someAddToAnnexObjects)
            for unAddToAnnexObject in someAddToAnnexObjects:
                self.chooseRootOrSubitem( theTravCtxt, theItemsConfig, unAddToAnnexObject, unAddToAnnexObjectIndex, anAddToAnnexObjectsLen, False)
                unAddToAnnexObjectIndex += 1
            
            # see hack above 
            theTravCtxt[ 'stack'].pop()
            theTravCtxt[ 'stack'].pop()
            
        theTravCtxt[ 'titleLevel'] = unInitialTitleLevel

        # self.logDebug( theTravCtxt, "rootScanPasses END theRootObject=%s theItemsConfig=\n%s\n" % ( str( theRootObject), str( theItemsConfig),) )
    
        return self
        
                 
            
            
            
            
    security.declarePrivate( 'traverseCompositeFromRoot')
    def traverseCompositeFromRoot( self, theTravCtxt = {}, theItemsConfig= {}, theRootObject=None):

        if not theTravCtxt.has_key( 'logger'):
            aLogger = logging.getLogger( 'ModelDDvlPlone-ModelDDvlPloneTool_Visitor')
            theTravCtxt[ 'logger'] = aLogger

        if theRootObject is None:
            # self.logDebug( theTravCtxt, "No theRootObject")                        
            return "No theRootObject"                     
            
        if not theItemsConfig:
            # self.logDebug( theTravCtxt, "No theItemsConfig")                        
            return "No theItemsConfig"    
        
        aResult = "No sucessful execution"        

        
        if not theTravCtxt.has_key( 'includedObjects'):
            theTravCtxt[ 'includedObjects'] = [ ]

        if not theTravCtxt.has_key( 'referencedObjects'):
            theTravCtxt[ 'referencedObjects'] = [ ]
            
        if not theTravCtxt.has_key( 'addToAnnexIfNotIncludedObjects'):
            theTravCtxt[ 'addToAnnexIfNotIncludedObjects'] = [ ]
        
        if not theTravCtxt.has_key( 'addToAnnexObjects'):
            theTravCtxt[ 'addToAnnexObjects'] = [ ]
            
            
        unRequestedStartLevel = 1
        if theTravCtxt.has_key( 'theLevel'):
            unRequestedStartLevel = theTravCtxt[ 'theLevel']
        if unRequestedStartLevel < 1:
            unRequestedStartLevel = 1
        
        if not theTravCtxt.has_key( 'titleLevel'):
            theTravCtxt[ 'titleLevel'] = unRequestedStartLevel - 1
    
        someInitialTitleHeaders = { }
        if theTravCtxt.has_key( 'titleHeaders'):
            someInitialTitleHeaders = theTravCtxt[ 'titleHeaders'].copy()
        else:
            theTravCtxt[ 'titleHeaders'] = someInitialTitleHeaders.copy()
            

        theTravCtxt[ 'indent'] = 4

        theTravCtxt[ 'stack']= []
        theTravCtxt[ 'type_configs']= {}
        
        unInitialTitleLevel = theTravCtxt[ 'titleLevel']
        
        self.preScanTypeConfigs( theTravCtxt, theItemsConfig)

        self.preScanIncludedAndAnnexObjects( theTravCtxt, theItemsConfig, theRootObject)

        
        try:            
            if theTravCtxt.has_key( 'output'):
                anOutput = theTravCtxt[ 'output']
                theTravCtxt[ 'close_output_at_end'] = False
            else:
                anOutput = StringIO.StringIO()
                theTravCtxt[ 'output'] = anOutput
                theTravCtxt[ 'close_output_at_end'] = True
            
            # self.logDebug( theTravCtxt, "START TRAVERSAL on %s\nwith:%s\n" % ( theRootObject.title_or_id(), str( theItemsConfig), ) )                        


            theTravCtxt[ 'reusableTitlesByObjectPath'] = { }
            theTravCtxt[ 'reusableTitlesByStackPaths'] = { }
            
            
            theTravCtxt[ 'collectSubitemsAndRelateds'] = True
            theTravCtxt[ 'useSubitemsAndRelateds'] = False
            theTravCtxt[ 'subitemsAndRelatedsByObjectPath'] = { }
            theTravCtxt[ 'titleLevel'] = unInitialTitleLevel
            theTravCtxt[ 'titleHeaders'] = someInitialTitleHeaders.copy()
            self.vDumper.setBeJustCollectHeaders( True)
            theTravCtxt[ 'reuse_headers'] = False

            self.rootScanPasses( theTravCtxt, theItemsConfig, theRootObject)

            
            theTravCtxt[ 'useSubitemsAndRelateds'] = True
            theTravCtxt[ 'collectSubitemsAndRelateds'] = False
            theTravCtxt[ 'titleLevel'] = unInitialTitleLevel
            theTravCtxt[ 'titleHeaders'] = someInitialTitleHeaders.copy()
            self.vDumper.setBeJustCollectHeaders( False)
            theTravCtxt[ 'reuse_headers'] = True
            
            self.rootScanPasses( theTravCtxt, theItemsConfig, theRootObject)

            

            aResult = theTravCtxt[ 'output'].getvalue()        
        finally:
            if theTravCtxt[ 'close_output_at_end'] and theTravCtxt[ 'output']:
                theTravCtxt[ 'output'].close()
        
        # self.logDebug( theTravCtxt, "TRAVERSAL result \n%s\n" % str( aResult) )                        
    
        return aResult   
   
   
   
   
   

   
          
            
    security.declarePrivate( 'traverseFromRoot')
    def traverseFromRoot( self, theTravCtxt = {}, theItemsConfig= {}, theRootObject=None):

        if not theTravCtxt.has_key( 'logger'):
            aLogger = logging.getLogger( 'ModelDDvlPlone-ModelDDvlPloneTool_Visitor')
            theTravCtxt[ 'logger'] = aLogger

        if theRootObject is None:
            # self.logDebug( theTravCtxt, "No theRootObject")                        
            return "No theRootObject"                     
            
        if not theItemsConfig:
            # self.logDebug( theTravCtxt, "No theItemsConfig")                        
            return "No theItemsConfig"    
        
        aResult = "No sucessful execution"        

        
        if not theTravCtxt.has_key( 'includedObjects'):
            theTravCtxt[ 'includedObjects'] = [ ]

        if not theTravCtxt.has_key( 'referencedObjects'):
            theTravCtxt[ 'referencedObjects'] = [ ]
            
        if not theTravCtxt.has_key( 'addToAnnexIfNotIncludedObjects'):
            theTravCtxt[ 'addToAnnexIfNotIncludedObjects'] = [ ]
        
        if not theTravCtxt.has_key( 'addToAnnexObjects'):
            theTravCtxt[ 'addToAnnexObjects'] = [ ]
            
            
        unRequestedStartLevel = 1
        if theTravCtxt.has_key( 'theLevel'):
            unRequestedStartLevel = theTravCtxt[ 'theLevel']
        if unRequestedStartLevel < 1:
            unRequestedStartLevel = 1
        
        if not theTravCtxt.has_key( 'titleLevel'):
            theTravCtxt[ 'titleLevel'] = unRequestedStartLevel - 1
    
        someInitialTitleHeaders = { }
        if theTravCtxt.has_key( 'titleHeaders'):
            someInitialTitleHeaders = theTravCtxt[ 'titleHeaders'].copy()
        else:
            theTravCtxt[ 'titleHeaders'] = someInitialTitleHeaders.copy()
            

        theTravCtxt[ 'indent'] = 4

        theTravCtxt[ 'stack']= []
        theTravCtxt[ 'type_configs']= {}
        
        unInitialTitleLevel = theTravCtxt[ 'titleLevel']
        
        self.preScanTypeConfigs( theTravCtxt, theItemsConfig)

#        self.preScanIncludedAndAnnexObjects( theTravCtxt, theItemsConfig, theRootObject)

        
        try:            
            if theTravCtxt.has_key( 'output'):
                anOutput = theTravCtxt[ 'output']
                theTravCtxt[ 'close_output_at_end'] = False
            else:
                anOutput = StringIO.StringIO()
                theTravCtxt[ 'output'] = anOutput
                theTravCtxt[ 'close_output_at_end'] = True
            


            theTravCtxt[ 'reusableTitlesByObjectPath'] = { }
            theTravCtxt[ 'reusableTitlesByStackPaths'] = { }
            theTravCtxt[ 'subitemsAndRelatedsByObjectPath'] = { }
            
            theTravCtxt[ 'useSubitemsAndRelateds'] = False
            theTravCtxt[ 'collectSubitemsAndRelateds'] = False
            theTravCtxt[ 'titleLevel'] = unInitialTitleLevel
            self.vDumper.setBeJustCollectHeaders( False)
            theTravCtxt[ 'reuse_headers'] = False
            
            self.root( theTravCtxt, theItemsConfig, theRootObject)

            

            aResult = theTravCtxt[ 'output'].getvalue()        
        finally:
            if theTravCtxt[ 'close_output_at_end'] and theTravCtxt[ 'output']:
                theTravCtxt[ 'output'].close()
        
        # self.logDebug( theTravCtxt, "TRAVERSAL result \n%s\n" % str( aResult) )                        
    
        return aResult   
   
   
   
   
      
   
   
   











   
   

   
   
   
   
   






    
# #########################
#  Log methods
#

     
               
    def logInfo( self, theTravCtxt, theMessage):
# DO NOT EXECUTE        
        if True:
            return self
    
        if not theTravCtxt or not theMessage:
            return self
            
        aLogger = theTravCtxt[ 'logger']
        if aLogger:
            aLogger.info( theMessage)                           
            
                 
           
            
    def logDebug( self, theTravCtxt, theMessage):
        if not theTravCtxt or not theMessage:
            return self
            
        aLogger = theTravCtxt[ 'logger']
        if aLogger:
            aLogger.debug( theMessage)                           
            
             
                        
            
    def logError( self, theTravCtxt, theMessage):
        if not theTravCtxt or not theMessage:
            return self
            
        aLogger = theTravCtxt[ 'logger']
        if aLogger:
            aLogger.error( theMessage)                           
                        
             
     