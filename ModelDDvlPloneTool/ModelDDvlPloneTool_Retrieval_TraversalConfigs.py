# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval_TraversalConfigs.py
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
from Acquisition        import aq_inner, aq_parent

from PloneElement_TraversalConfig import cExportConfig_PloneElements

   

class ModelDDvlPloneTool_Retrieval_TraversalConfigs:
    """
    """
    security = ClassSecurityInfo()




    
    security.declarePublic( 'getAllTypeConfigs')
    def getAllTypeConfigs(self, theContextElement):
        """Access the traversal configuration to drive Generic retrieval rendering.
        
        """
        if ( theContextElement == None):
            return []
                           
        allTypeConfigs = self.getTraversalConfig( theContextElement)
        if not allTypeConfigs:
            return []
        
        someScannedTypeConfigs = self.preScanTypeConfigsStandAlone( allTypeConfigs)   
         
        return someScannedTypeConfigs
        

       
      
    security.declarePrivate( 'hasTypeConfig')
    def hasTypeConfig(self, theContextElement, theTypeName, theAllTypeConfigs=None, theConfigName=""):   
        
        anAllTypeConfigs = theAllTypeConfigs
        if not anAllTypeConfigs:
            if ( theContextElement == None):
                return []
            anAllTypeConfigs = self.getAllTypeConfigs( theContextElement)
            
        if not anAllTypeConfigs:
            return None

        
        unHasTypeConfig = anAllTypeConfigs.has_key( theTypeName)
        return unHasTypeConfig
       
    
    
    
        
    security.declarePrivate( 'getTypeConfig')
    def getTypeConfig(self, theContextElement, theTypeName, theAllTypeConfigs=None, theConfigName=""):   
        
        anAllTypeConfigs = theAllTypeConfigs
        if not anAllTypeConfigs:
            if ( theContextElement == None):
                return []
            anAllTypeConfigs = self.getAllTypeConfigs( theContextElement)
            
        if not anAllTypeConfigs:
            return None

        
        if not anAllTypeConfigs.has_key( theTypeName):
            return None
        
        aTypeConfig = None

        someConfigsForType =  anAllTypeConfigs[ theTypeName]
        if someConfigsForType:
            if theConfigName:        
                if someConfigsForType.has_key( theConfigName):           
                    aTypeConfig = someConfigsForType[ theConfigName]
                
            if not aTypeConfig:
                if someConfigsForType.has_key( 'Default'):    
                    aTypeConfig = someConfigsForType[ 'Default']
                else:
                    aTypeConfig =  someConfigsForType[ 0]
        return aTypeConfig

   
 
  
  
  
  
 

   
        
    # ACV 20090529 unused removed  
    #security.declarePrivate( 'getRelatedDependentScanTypeConfigs')
    #def getRelatedDependentScanTypeConfigs(self, theNombreProyecto):   
        #"""Access the traversal configuration to find elements impacted by deletion of an element.
        
        #"""
        #return self.getAllTypeConfigs( theNombreProyecto)
  
       
             

             
###########################
#  Traversal config accessors
###########################            
          


           

      
    security.declarePrivate('getTraversalConfig')
    def getTraversalConfig(self, theContextElement):
        
        if ( theContextElement == None):
            return []

        unNombreProyecto = ''
        try:
            unNombreProyecto = theContextElement.getNombreProyecto()   
        except:
            None            
        if not unNombreProyecto:
            return None

        unEditableConfigScriptName = self.traversalConfigScriptName( unNombreProyecto)
        if unEditableConfigScriptName:
            unaConfig = self.scriptEvaluationResult( theContextElement, unEditableConfigScriptName)
            if unaConfig:
                return unaConfig

        unaConfig = None
        try:
            unaConfig = theContextElement.traversalConfig()
        except:
            None
        return unaConfig
           



   



    security.declarePrivate('traversalConfigScriptName')
    def traversalConfigScriptName(self, theNombreProyecto):
        
        if not theNombreProyecto:
            return []
            
        unTraversalConfigScriptName =  "%s_TraversalConfig_Script" % theNombreProyecto
        return unTraversalConfigScriptName






    security.declarePrivate('scriptEvaluationResult')
    def scriptEvaluationResult( self, theContextElement, theTraversalConfigName):
        if ( theContextElement == None):
            return []

        if not theTraversalConfigName:
            return None        

        aScript   = None
        try:
            aScript = theContextElement.unrestrictedTraverse( theTraversalConfigName)
        except:
            None
            
        if not aScript:
            return None

        aContext          = aq_inner( theContextElement)  
        if not aContext:
            return None
                     
        aScriptInContext  = aScript.__of__( aContext)
        if not aScriptInContext:
            return None
        
        anTraversalConfig = aScriptInContext()       
        if anTraversalConfig is None or len( anTraversalConfig) < 1:
            return None 
                   
        return anTraversalConfig

    

          


   
   
# #########################
# Traversal config scanning and resolution methods
#

 

          
    security.declarePrivate( 'preScanTypeConfigsStandAlone')
    def preScanTypeConfigsStandAlone( self, theItemsConfig):
        if  theItemsConfig is None:
            return {}
    
        someFoundTypeConfigsDict = {}
        self.preScanTypeConfigsStandAloneRecursive( theItemsConfig, someFoundTypeConfigsDict)
        return someFoundTypeConfigsDict
        
        
        
        
           
    security.declarePrivate( 'preScanTypeConfigsStandAloneRecursive')
    def preScanTypeConfigsStandAloneRecursive( self,theItemsConfig, theFoundTypeConfigsDict):
        if  theItemsConfig is None or  theFoundTypeConfigsDict is None:
            return { }
    
        for aTypeConfig in theItemsConfig:
            if not aTypeConfig.has_key( 'reuse_config'):  
                
                unConfigName = 'Default'
                if aTypeConfig.has_key( 'config_name'):
                    unConfigName = aTypeConfig[ 'config_name']
                    
                somePortalTypes = aTypeConfig[ 'portal_types'] 
                for aTypeName in somePortalTypes:
                    if not theFoundTypeConfigsDict.has_key( aTypeName):
                        someTypeConfigs = { }
                        theFoundTypeConfigsDict[ aTypeName] = someTypeConfigs
                    else:
                        someTypeConfigs = theFoundTypeConfigsDict[ aTypeName]   
                    
                    if not someTypeConfigs.has_key( unConfigName):
                        someTypeConfigs[ unConfigName] = aTypeConfig                                        
    
                if aTypeConfig.has_key( 'traversals'):
                    someTraversalConfigs = aTypeConfig[ 'traversals']
                    for aTraversalConfig in someTraversalConfigs:
                        if aTraversalConfig.has_key( 'subitems'):
                            someSubitemsTypesConfigs = aTraversalConfig[ 'subitems']
                            self.preScanTypeConfigsStandAloneRecursive( someSubitemsTypesConfigs, theFoundTypeConfigsDict)                        
    
                        elif aTraversalConfig.has_key( 'related_types'):
                            someRelatedTypesConfigs = aTraversalConfig[ 'related_types']
                            self.preScanTypeConfigsStandAloneRecursive( someRelatedTypesConfigs, theFoundTypeConfigsDict)
        
        return theFoundTypeConfigsDict
    

        
        
    
    
    
    
    
    
    
    # ##################################
    # Export traversal configs
    # ##################################
    
    

    
    security.declarePublic( 'getMDDTypeImportConfigs')
    def getMDDTypeImportConfigs(self, theContextElement):
        """Access the traversal configuration to import objects aware of ModelDDvlPloneTool.
        
        """
        if ( theContextElement == None):
            return []
                           
        allTypeConfigs = self.getImportConfig( theContextElement)
        if not allTypeConfigs:
            return []
         
        someScannedTypeConfigs = self.preScanTypeConfigsStandAlone( allTypeConfigs)   
       
        return someScannedTypeConfigs
        

    
    

    
    security.declarePublic( 'getPloneTypeImportConfigs')
    def getPloneTypeImportConfigs(self, theContextElement):
        """Access the traversal configuration to copy Plone objects.
        
        """
        if ( theContextElement == None):
            return []
                           
        somePloneElementsImportConfigs = self.preScanTypeConfigsStandAlone( cExportConfig_PloneElements)
        
       
        return somePloneElementsImportConfigs
            
           
           

    security.declarePrivate('getImportConfig')
    def getImportConfig(self, theContextElement):
        return self.getExportConfig( theContextElement)
    
    
   
    
    security.declarePublic( 'getAllTypeExportConfigs')
    def getAllTypeExportConfigs(self, theContextElement):
        """Access the traversal configuration to export objects.
        
        """
        if ( theContextElement == None):
            return []
                           
        allTypeConfigs = self.getExportConfig( theContextElement)
        if not allTypeConfigs:
            return []
         
        someScannedTypeConfigs = self.preScanExportTypeConfigs( allTypeConfigs)   
                 
        someScannedMetaTypes = set( someScannedTypeConfigs.keys())

        somePloneElementsExportConfigs = self.preScanExportTypeConfigs( cExportConfig_PloneElements)
        
        somePloneElementsMetaTypes = set( somePloneElementsExportConfigs.keys())

        somePloneTypesToExport = someScannedMetaTypes.intersection( somePloneElementsMetaTypes)
        if somePloneTypesToExport:
            for aPloneType in somePloneTypesToExport:
                someScannedTypeConfigs[ aPloneType] = somePloneElementsExportConfigs[ aPloneType].copy()
        
        return someScannedTypeConfigs
        

 
    
    
    security.declarePrivate('getExportConfig')
    def getExportConfig(self, theContextElement):
        
        if ( theContextElement == None):
            return []

        unNombreProyecto = ''
        try:
            unNombreProyecto = theContextElement.getNombreProyecto()   
        except:
            None            
        if not unNombreProyecto:
            return None

        unEditableConfigScriptName = self.exportConfigScriptName( unNombreProyecto)
        if unEditableConfigScriptName:
            unaConfig = self.scriptEvaluationResult( theContextElement, unEditableConfigScriptName)
            if unaConfig:
                return unaConfig

        unaConfig = None
        try:
            unaConfig = theContextElement.exportConfig()
        except:
            None
        return unaConfig
           


    
    
    


    security.declarePrivate('exportConfigScriptName')
    def exportConfigScriptName(self, theNombreProyecto):
        
        if not theNombreProyecto:
            return []
            
        unExportConfigScriptName =  "%s_ExportConfig_Script" % theNombreProyecto
        return unExportConfigScriptName

    
       
   


          
    security.declarePrivate( 'preScanExportTypeConfigs')
    def preScanExportTypeConfigs( self, theItemsConfig):
        if  theItemsConfig is None:
            return {}
    
        someFoundTypeConfigsDict = {}
        self.preScanExportTypeConfigsRecursive( theItemsConfig, someFoundTypeConfigsDict)
        return someFoundTypeConfigsDict
        
        
    security.declarePrivate( 'fDefaultExportTypeConfig')
    def fDefaultExportTypeConfig( self, theTypeName):
        return {   
            'portal_types': [ theTypeName, ],
            'attrs':        [
                {   'name': 'title',
                    'type': 'String',
                },
                {   'name': 'description',
                    'type': 'Text',
                },
            ],
        }
        
        
        
           
    security.declarePrivate( 'preScanExportTypeConfigsRecursive')
    def preScanExportTypeConfigsRecursive( self,theItemsConfig, theFoundTypeConfigsDict):
        if  theItemsConfig is None or  theFoundTypeConfigsDict is None:
            return { }
    
        for aTypeConfig in theItemsConfig:
                
            somePortalTypes = aTypeConfig[ 'portal_types'] 
            for aTypeName in somePortalTypes:
                theFoundTypeConfigsDict[ aTypeName] = aTypeConfig
                    
                    
            unosTraversalConfigs = aTypeConfig.get( 'traversals', [])
            for unTraversalConfig in unosTraversalConfigs:
                
                unAggregationName = unTraversalConfig.get( 'aggregation_name', '')
                if unAggregationName:

                    someAcceptedPortalTypes = set( )
                    someSubItemsConfigs   = unTraversalConfig.get( 'subitems', [])

                    for aSubItemsConfig in someSubItemsConfigs:
                        somePortalTypes = aSubItemsConfig.get( 'portal_types', [])
                        someAcceptedPortalTypes.update( somePortalTypes)

                    for aSubItemTypeName in someAcceptedPortalTypes:
                        if not theFoundTypeConfigsDict.has_key( aSubItemTypeName):
                            theFoundTypeConfigsDict[ aSubItemTypeName] = self.fDefaultExportTypeConfig( aSubItemTypeName)
                            
        return theFoundTypeConfigsDict
    

        
        
    
 
 
    
    
    
    
    
    
    security.declarePublic( 'getMDDTypeCopyConfigs')
    def getMDDTypeCopyConfigs(self, theContextElement):
        """Access the traversal configuration to copy objects aware of ModelDDvlPloneTool.
        
        """
        if ( theContextElement == None):
            return []
                           
        allTypeConfigs = self.getCopyConfig( theContextElement)
        if not allTypeConfigs:
            return []
         
        someScannedTypeConfigs = self.preScanTypeConfigsStandAlone( allTypeConfigs)   
       
        return someScannedTypeConfigs
        

    
    

    
    security.declarePublic( 'getPloneTypeCopyConfigs')
    def getPloneTypeCopyConfigs(self, theContextElement):
        """Access the traversal configuration to copy Plone objects.
        
        """
        if ( theContextElement == None):
            return []
                           
        somePloneElementsExportConfigs = self.preScanTypeConfigsStandAlone( cExportConfig_PloneElements)
        
        return somePloneElementsExportConfigs
            
           

    
    
    security.declarePrivate('getCopyConfig')
    def getCopyConfig(self, theContextElement):
        
        if ( theContextElement == None):
            return []

        unNombreProyecto = ''
        try:
            unNombreProyecto = theContextElement.getNombreProyecto()   
        except:
            None            
        if not unNombreProyecto:
            return None

        unEditableConfigScriptName = self.copyConfigScriptName( unNombreProyecto)
        if unEditableConfigScriptName:
            unaConfig = self.scriptEvaluationResult( theContextElement, unEditableConfigScriptName)
            if unaConfig:
                return unaConfig

        unaConfig = None
        try:
            unaConfig = theContextElement.copyConfig()
        except:
            None
        return unaConfig
           


    
    
    


    security.declarePrivate('copyConfigScriptName')
    def copyConfigScriptName(self, theNombreProyecto):
        
        if not theNombreProyecto:
            return []
            
        unCopyConfigScriptName =  "%s_CopyConfig_Script" % theNombreProyecto
        return unCopyConfigScriptName

    
       
   


          
    security.declarePrivate( 'preScanCopyTypeConfigs')
    def preScanCopyTypeConfigs( self, theItemsConfig):
        if  theItemsConfig is None:
            return {}
    
        someFoundTypeConfigsDict = {}
        self.preScanCopyTypeConfigsRecursive( theItemsConfig, someFoundTypeConfigsDict)
        return someFoundTypeConfigsDict
        
        
    security.declarePrivate( 'fDefaultCopyTypeConfig')
    def fDefaultCopyTypeConfig( self, theTypeName):
        return {   
            'portal_types': [ theTypeName, ],
            'attrs':        [
                {   'name': 'title',
                    'type': 'String',
                },
                {   'name': 'description',
                    'type': 'Text',
                },
            ],
        }
        
        
        
           
    security.declarePrivate( 'preScanCopyTypeConfigsRecursive')
    def preScanCopyTypeConfigsRecursive( self,theItemsConfig, theFoundTypeConfigsDict):
        if  theItemsConfig is None or  theFoundTypeConfigsDict is None:
            return { }
    
        for aTypeConfig in theItemsConfig:
                
            somePortalTypes = aTypeConfig[ 'portal_types'] 
            for aTypeName in somePortalTypes:
                theFoundTypeConfigsDict[ aTypeName] = aTypeConfig
                    
                    
            unosTraversalConfigs = aTypeConfig.get( 'traversals', [])
            for unTraversalConfig in unosTraversalConfigs:
                
                unAggregationName = unTraversalConfig.get( 'aggregation_name', '')
                if unAggregationName:

                    someAcceptedPortalTypes = set( )
                    someSubItemsConfigs   = unTraversalConfig.get( 'subitems', [])

                    for aSubItemsConfig in someSubItemsConfigs:
                        somePortalTypes = aSubItemsConfig.get( 'portal_types', [])
                        someAcceptedPortalTypes.update( somePortalTypes)

                    for aSubItemTypeName in someAcceptedPortalTypes:
                        if not theFoundTypeConfigsDict.has_key( aSubItemTypeName):
                            theFoundTypeConfigsDict[ aSubItemTypeName] = self.fDefaultCopyTypeConfig( aSubItemTypeName)
                            
        return theFoundTypeConfigsDict
    


    
    
    
    

    
    
    security.declarePrivate('getMappingConfigs')
    def getMappingConfigs(self, theContextElement):
        
        if ( theContextElement == None):
            return []

        unNombreProyecto = ''
        try:
            unNombreProyecto = theContextElement.getNombreProyecto()   
        except:
            None            
        if not unNombreProyecto:
            return None

        unEditableConfigScriptName = self.mappingConfigScriptName( unNombreProyecto)
        if unEditableConfigScriptName:
            unaConfig = self.scriptEvaluationResult( theContextElement, unEditableConfigScriptName)
            if unaConfig:
                return unaConfig

        unaConfig = None
        try:
            unaConfig = theContextElement.mappingConfig()
        except:
            None
        return unaConfig
           


    
    
    


    security.declarePrivate('mappingConfigScriptName')
    def mappingConfigScriptName(self, theNombreProyecto):
        
        if not theNombreProyecto:
            return []
            
        unMappingConfigScriptName =  "%s_MappingConfig_Script" % theNombreProyecto
        return unMappingConfigScriptName

    
       
    
    
    

  

    security.declarePublic('objectValuesTraversalConfig')
    def objectValuesTraversalConfig( self):
        return {   
            'aggregation_name':     'objectValues',
            'columns':              [ 'title', 'description', ],
            'contains_collections': False,
            'tabular_tree':         False,
            'subitems':             [
                {   'portal_types': [ 'object', ],
                    'extension':    'NonTextAttrsOneParagraph',
                    'divider':      [ 'Before', ],
                    'attrs':        [
                        {   'name': 'title',
                            'kind': 'Data',
                            'type': 'String',
                        },
                        {   'name': 'archetype_name',
                            'kind': 'Meta',
                            'type': 'String',
                        },
                        {   'name':     'description',
                            'kind':     'Data',
                            'type':     'Text',
                            'optional': True,
                        },
                    ],
                },
            ],
        }
     
       