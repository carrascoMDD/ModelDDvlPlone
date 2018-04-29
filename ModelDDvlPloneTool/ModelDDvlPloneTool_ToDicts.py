# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_ToDicts.py
#
# Copyright (c) 2008, 2009, 2010 by Model Driven Development sl and Antonio Carrasco Valero
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


import sys
import logging
import traceback

from StringIO import StringIO

from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

from DateTime import DateTime



from AccessControl import ClassSecurityInfo



from ModelDDvlPloneTool_ImportExport_Constants import cMDDZIPFilePostfix, cMDDPythonFilePostfix

from ModelDDvlPloneTool_ToDicts_Constants      import *


from ModelDDvlPloneToolSupport                 import fReprAsString





# ############################################################
        
        

        
def fResolveByIndex(
    theTestModelSpecification =None,
    theIndexName              =None,
    theDictId                 =None,):
    """Auxiliary method to deliver a callable for index lookup. Resolves model elements from their identity.
    Indexes hold access paths to the elements, including dictionary keys and list indexes. The model shall not change from the time the indexes were created to the time the indexes are used to look up dictionaries.
    
    """        
            
    if not theTestModelSpecification:
        return None
    
    if not theIndexName:
        return None

    if not theDictId:
        return None    
    
    someIndexes = theTestModelSpecification.get( cMDDModelDict_theIndexes, None)
    if not someIndexes:
        return None

    
    anIndex = someIndexes.get( theIndexName, None)
    if anIndex == None:
        return None
    
    someDictPathsById = anIndex.get( theDictId, None)
    if not someDictPathsById:
        return None
    
    someIndexes = theTestModelSpecification.get( cMDDModelDict_theIndexes, None)
    if not someIndexes:
        return None
    
    
    someResolvedDicts = [ ]
    
    
    aDictsRoot = theTestModelSpecification.get( 'dicts_root', None)
    
    for aDictPath in someDictPathsById:
        
        aDict = aDictsRoot
        for aPathStep in aDictPath:
            
            if isinstance( aDict, dict):
                
                aDict = aDict.get( aPathStep, None)
                if aDict == None:
                    break
                
            elif isinstance( aDict, list):
                
                if ( aPathStep >= 0) and ( aPathStep < len( aDict)):
                    aDict = aDict[ aPathStep]
                else:
                    aDict = None
                    break
                
        if not( aDict == None):
            someResolvedDicts.append( aDict)
    
    return someResolvedDicts

        



def fResolveByIndex_OLD(
    theTestModelSpecification =None,
    theIndexName              =None,
    theDictId                 =None,):
    """Auxiliary method to deliver a callable for index lookup. Resolves model elements from their identity.
    
    """        
            
    if not theTestModelSpecification:
        return None
    
    if not theIndexName:
        return None

    if not theDictId:
        return None    
    
    someIndexes = theTestModelSpecification.get( cMDDModelDict_theIndexes, None)
    if not someIndexes:
        return None

    
    anIndex = someIndexes.get( theIndexName, None)
    if anIndex == None:
        return None
    
    someDictsById = anIndex.get( theDictId, None)
    
    return someDictsById

    
    
    
    

    
    
# ############################################################
# ############################################################
    


class ModelDDvlPloneTool_ToDicts:
    """
    """
    security = ClassSecurityInfo()

    
    
    
    
    
    
    # ############################################################
    """Results and context factory methods.
    
    """
    
    
    security.declarePrivate( 'fNewVoidToDictsReport')    
    def fNewVoidToDictsReport( self,):
        unInforme = {
            'success':                  False,
            'status':                   '',
            'condition':                None,
            'exception':                '',
            'root_meta_type':           '',
            'root_id':                  '',
            'root_title':               '',
            'root_UID':                 '',
            'root_physhical_path':      '',
            'num_elements':             0,
            'num_attributes':           0,
            'num_aggregations':         0,
            'num_relations':            0,
            'num_references':           0,
            'num_elementrefs':          0,
            'num_images':               0,
            'num_files':                0,
            'dicts_root':               None,
            'todict_errors':            [ ],
        }
        return unInforme
    
    
    
    
      
    security.declarePrivate( 'fNewVoidToDictsContext')    
    def fNewVoidToDictsContext( self,):
        unInforme = {
            'type_configs':              None,
            'root':                      None,
            'next_dict_id':              0,
            'report':                    self.fNewVoidToDictsReport(),
            'dicts_by_dict_id':          { },
            'dicts_by_physical_path':    { },
            'dicts_root':                None,
            'dicts_stack':               [ ],
            'element_refs':              [ ],
            'ignored_feature_names_by_type': { },
        }
        return unInforme
    
    
    
    
    
    
    
    
    
    
    
    # ############################################################
    """Dictionaries factory methods.
    
    """

    
    
    def fNewToDict(self, theToDictsContext=None,):
        if theToDictsContext == None:
            return None
        
        aDictId     = theToDictsContext.get( 'next_dict_id', 0)
        aNextDictId = aDictId + 1
        theToDictsContext[  'next_dict_id'] = aNextDictId
        
        
        aDict = {
            cMDDDictAttributeName_DictKind:      None,
            cMDDDictAttributeName_DictId:        aDictId,
        }
       
        theToDictsContext[  'dicts_by_dict_id'][ aDictId] = aDict
        
        return aDict
    
    
    
    
    
    
    
    def fNewToDictForElement(self, theToDictsContext=None, theElement=None):
        if theToDictsContext == None:
            return None
     
        if theElement == None:
            return None
     
        unDictsStack = self.fToDictsStack( theToDictsContext)
        if ( unDictsStack == None):
            return None
        
        aParentDict   = None
        aParentDictId = None
        if len( unDictsStack):
            aParentDict = unDictsStack[ -1]
            if not ( aParentDict == None):
                
                if not ( aParentDict.get( cMDDDictAttributeName_DictKind, None) in [ cMDDDictAttributeName_DictKind_Aggregation, ]):
                    return None
                
                aParentDictId = aParentDict.get( cMDDDictAttributeName_DictId, None)
                
                        
                        
        aIsRoot      = aParentDict == None
        aRootElement = None
        if aIsRoot:
            aRootElement = theElement
            theToDictsContext[ 'root'] = theElement
        else:
            aRootElement = theToDictsContext.get( 'root', None)
            if aRootElement == None:
                return None
            
            
        unosDictsByPhysicalPath = theToDictsContext.get( 'dicts_by_physical_path', None)
        if unosDictsByPhysicalPath == None:
            return None   
                 
        
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if unToDictsReport == None:
            return None            
        
        
        aMetaType = None
        try:
            aMetaType = theElement.meta_type
        except:
            None

        aPloneId = None
        try:
            aPloneId = theElement.getId()
        except:
            None

        aTitle = None
        try:
            aTitle = theElement.Title()
        except:
            None
        
        aURL = None
        try:
            aURL = theElement.absolute_url()
        except:
            None
            
        aPath = None
        try:
            aPath = self.fPathStringRelativeToRoot( theElement, aRootElement)
        except:
            None
            
        aPhysicalPath = None
        try:
            aPhysicalPath = self.fPhysicalPathStringForElement( theElement)
        except:
            None
                  
        aUID = None
        try:
            aUID = theElement.UID()
        except:
            None
            
            
        aIsCollection = False
        try:
            aIsCollection = theElement.getEsColeccion()
        except:
            None


        aDict = self.fNewToDict( theToDictsContext)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_DictKind:      cMDDDictAttributeName_DictKind_Element,
            cMDDDictAttributeName_Element:       theElement,
            cMDDDictAttributeName_ParentDictId:  aParentDictId,
            cMDDDictAttributeName_IsRoot:        aIsRoot,
            cMDDDictAttributeName_PloneMetaType: aMetaType,
            cMDDDictAttributeName_PloneId:       aPloneId,
            cMDDDictAttributeName_PloneTitle:    aTitle,
            cMDDDictAttributeName_PloneURL:      aURL,
            cMDDDictAttributeName_PloneUID:      aUID,
            cMDDDictAttributeName_PlonePath:     aPath,
            cMDDDictAttributeName_PhysicalPath:  aPhysicalPath,
            cMDDDictAttributeName_IsCollection:  aIsCollection,
            cMDDDictAttributeName_Features :     [ ],
        })
        
        
        unDictsStack.append( aDict)
        
        
        if aPhysicalPath:
            unosDictsByPhysicalPath[ aPhysicalPath] = aDict
                  
            
        if not ( aParentDict == None):
            aParentDict[ cMDDDictAttributeName_Elements].append( aDict)

            
        if aIsRoot:
            theToDictsContext[ 'dicts_root'] = aDict
            
            unToDictsReport  = self.fToDictsReport( theToDictsContext)
            unToDictsReport[ 'dicts_root'] = aDict

            
        unToDictsReport[ 'num_elements'] += 1
        
            
        return aDict
    
    
    
    
    
    
    
    def fNewToDictForFeature(self, theToDictsContext=None, theFeatureName=None):
        if theToDictsContext == None:
            return None
     
        if not theFeatureName:
            return None        
        
        unDictsStack = self.fToDictsStack( theToDictsContext)
        if not unDictsStack:
            return None
        
        aParentDictId = None
        aParentDict   = unDictsStack[ -1]
        if aParentDict == None:
            return None
        
            
        if not ( aParentDict.get( cMDDDictAttributeName_DictKind, None) in [ cMDDDictAttributeName_DictKind_Element, ]):
            return None
        
        aParentDictId = aParentDict.get( cMDDDictAttributeName_DictId, None)
         
                
        aDict = self.fNewToDict( theToDictsContext,)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_ParentDictId: aParentDictId,
            cMDDDictAttributeName_FeatureName:  theFeatureName,
        })
    
        unDictsStack.append( aDict)
        
        if not ( aParentDict == None):
            aParentDict[ cMDDDictAttributeName_Features].append( aDict)
            
        return aDict
    
    
    
    
        
    
    
    def fNewToDictForAttribute(self, theToDictsContext=None, theFeatureName=None):
        if theToDictsContext == None:
            return None
     
        if not theFeatureName:
            return None        
        
        aDict = self.fNewToDictForFeature( theToDictsContext, theFeatureName)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_DictKind:       cMDDDictAttributeName_DictKind_Attribute,
            cMDDDictAttributeName_AttributeType:  None,
            cMDDDictAttributeName_AttributeValue: None,
        })
        
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if not( unToDictsReport == None):
            unToDictsReport[ 'num_attributes'] += 1
    
        return aDict
    
    
    
    
    
    
 
    
    def fNewToDictForAttribute_Image(self, theToDictsContext=None, theFeatureName=None):
        if theToDictsContext == None:
            return None
     
        if not theFeatureName:
            return None        
        
        aDict = self.fNewToDictForAttribute( theToDictsContext, theFeatureName)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_ContentType:    None,
            cMDDDictAttributeName_ImageId:        None,
            cMDDDictAttributeName_ImageTitle:     None,
            cMDDDictAttributeName_ImageFilename:  None,
        })
        
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if not( unToDictsReport == None):
            unToDictsReport[ 'num_attributes'] += 1
            unToDictsReport[ 'num_images'] += 1
    
        return aDict
    
    
    
    
    

    
    def fNewToDictForAttribute_File(self, theToDictsContext=None, theFeatureName=None):
        if theToDictsContext == None:
            return None
     
        if not theFeatureName:
            return None        
        
        aDict = self.fNewToDictForAttribute( theToDictsContext, theFeatureName)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_ContentType:    None,
            cMDDDictAttributeName_FileId:         None,
            cMDDDictAttributeName_FileTitle:      None,
            cMDDDictAttributeName_FileFilename:   None,
        })
        
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if not( unToDictsReport == None):
            unToDictsReport[ 'num_attributes'] += 1
            unToDictsReport[ 'num_files'] += 1
    
        return aDict
    
    
              
    
    
    
    
    
    def fNewToDictForAggregation(self, theToDictsContext=None, theFeatureName=None):
        if theToDictsContext == None:
            return None

        if not theFeatureName:
            return None        
        
        aDict = self.fNewToDictForFeature( theToDictsContext, theFeatureName)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_DictKind:  cMDDDictAttributeName_DictKind_Aggregation,
            cMDDDictAttributeName_Elements:  [ ], 
        })
    
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if not( unToDictsReport == None):
            unToDictsReport[ 'num_aggregations'] += 1
                  
        
        return aDict
    
    
    
    
    
    
    
    
    def fNewToDictForRelation(self, theToDictsContext=None, theFeatureName=None):
        if theToDictsContext == None:
            return None

        if not theFeatureName:
            return None        

        aDict = self.fNewToDictForFeature( theToDictsContext, theFeatureName)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_DictKind:     cMDDDictAttributeName_DictKind_Relation,
            cMDDDictAttributeName_ElementRefs:  [ ], 
        })
        
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if not( unToDictsReport == None):
            unToDictsReport[ 'num_relations'] += 1
               
        return aDict
    
    
    
    
    
    
    
    
    
    def fNewToDictForReference(self, theToDictsContext=None, theFeatureName=None):
        if theToDictsContext == None:
            return None

        if not theFeatureName:
            return None        

        aDict = self.fNewToDictForFeature( theToDictsContext, theFeatureName)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_DictKind:     cMDDDictAttributeName_DictKind_Reference,
            cMDDDictAttributeName_ElementRefs:  [ ], 
        })
        
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if not( unToDictsReport == None):
            unToDictsReport[ 'num_references'] += 1
    
        return aDict
    
    
    
    
    
    
   
    def fNewToDictForElementRef(self, theToDictsContext=None, theElement=None):
        if theToDictsContext == None:
            return None

        if theElement == None:
            return None
        

        unDictsStack = self.fToDictsStack( theToDictsContext)
        if not unDictsStack:
            return None
        
        aParentDictId = None
        aParentDict   = unDictsStack[ -1]
        if aParentDict == None:
            return None
        
            
        if not ( aParentDict.get( cMDDDictAttributeName_DictKind, None) in [ cMDDDictAttributeName_DictKind_Relation, cMDDDictAttributeName_DictKind_Reference,]):
            return None
        
        aParentDictId = aParentDict.get( cMDDDictAttributeName_DictId, None)
         
        
        unosElementRefs = theToDictsContext.get( 'element_refs', None)
        if unosElementRefs == None:
            return None     
        
                
        
        aMetaType = None
        try:
            aMetaType = theElement.meta_type
        except:
            None

        aPloneId = None
        try:
            aPloneId = theElement.getId()
        except:
            None

        aTitle = None
        try:
            aTitle = theElement.Title()
        except:
            None
        
        aURL = None
        try:
            aURL = theElement.absolute_url()
        except:
            None
            
        aPath = None
        try:
            aPath = theElement.UID()
        except:
            None
            
        aPhysicalPath = None
        try:
            aPhysicalPath = self.fPhysicalPathStringForElement( theElement)
        except:
            None

        aUID = None
        try:
            aUID = theElement.UID()
        except:
            None
            
        aDict = self.fNewToDict( theToDictsContext,)
        if aDict == None:
            return None
        
        aDict.update( {
            cMDDDictAttributeName_DictKind:      cMDDDictAttributeName_DictKind_ElementRef,
            cMDDDictAttributeName_ParentDictId:  aParentDictId,
            cMDDDictAttributeName_PloneMetaType: aMetaType,
            cMDDDictAttributeName_PloneId:       aPloneId,
            cMDDDictAttributeName_PloneTitle:    aTitle,
            cMDDDictAttributeName_PloneURL:      aURL,
            cMDDDictAttributeName_PloneUID:      aUID,
            cMDDDictAttributeName_PlonePath:     aPath,
            cMDDDictAttributeName_PhysicalPath:  aPhysicalPath,
            cMDDDictAttributeName_ReferencedDictId: None,
        })

        unDictsStack.append( aDict)
        
        unosElementRefs.append( aDict)

        if not ( aParentDict == None):
            aParentDict[ cMDDDictAttributeName_ElementRefs].append( aDict)
            
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if not( unToDictsReport == None):
            unToDictsReport[ 'num_elementrefs'] += 1
    
          
        return aDict
    
        
    
    
    
    security.declarePublic( 'fDownloadObjectPythonRepresentation')
    def fDownloadObjectPythonRepresentation(self, 
        theTimeProfilingResults =None,
        theContextualElement    =None,
        theObject               =None, 
        theTitle                =None,
        theAdditionalParams     =None,):
        """Download utility.
        
        """
        if theContextualElement == None:
            return False
        
        
        # ##############################################################################
        """Represent the object as a python literal.
        
        """
        aRepresentationString = fReprAsString( theObject)
        
        
        
      
        # ##############################################################################
        """Create in-memory zip file for exported content, to be sent back to the user in the HTTP request response.
        
        """

        unZipBuffer      = StringIO()
        unZipFile        = None
        try:
            unZipFile = ZipFile( unZipBuffer, "w", compression=ZIP_DEFLATED)
        except:
            None
        if not unZipFile:
            unZipFile = ZipFile( unZipBuffer, "w", compression=ZIP_STORED)
            
        if not unZipFile:
            return False
            
        
        aTitle = theTitle
        if not aTitle:
            aTitle = 'ToDicts'
        aTitle = aTitle.replace( ' ', '')
        if not aTitle:
            aTitle = 'ToDicts'
        aTitle = aTitle.replace( ' ', '')        

        
        unPythonFileName = '%s%s' % ( aTitle, cMDDPythonFilePostfix, )
        
        unZipFile.writestr( unPythonFileName, aRepresentationString)

        unZipFile.close()  
        
        
        unZIPFileName = '%s%s' % ( aTitle, cMDDZIPFilePostfix, )
    
        theContextualElement.REQUEST.RESPONSE.setHeader('Content-Type','application/zip')
        theContextualElement.REQUEST.RESPONSE.addHeader("Content-Disposition","filename=%s" % unZIPFileName)
        theContextualElement.REQUEST.RESPONSE.write( unZipBuffer.getvalue()) 
            
        return True
    
    
    
    
    
    
    
        
        

    # ############################################################
    """Dictionaries tree access acceleration by indexing.
    
    """
    
    
    security.declarePrivate( 'fIndexToDicts')
    def fIndexToDicts( self,
        theModelDDvlPloneTool =None,
        theContextualElement  =None, 
        theDicts              =None, 
        theIndexNames         =None):
        """Create specified indexes with information from the dictionaries in the tree.
        
        """
        
        if not theIndexNames:
            return []
        
        
        if not theDicts:
            return []
        
        
        someIndexNames = [ ]
        
        for anIndexName in theIndexNames:
            if anIndexName in cMDDDictIndexableAttributeNames:
                someIndexNames.append( anIndexName)
                
        if not someIndexNames:
            return [ ]
        

        
        someIndexes = dict ( [ [ anIndexName, { },] for anIndexName in someIndexNames ])

        self.pIndexToDicts_recursive( 
            theDicts,
            someIndexes,
            [],
        )
        
        return someIndexes
    

    
    
    
    
    security.declarePrivate( 'pIndexToDicts_recursive')
    def pIndexToDicts_recursive( self,
        theDicts           =None, 
        theIndexes         =None,
        thePath            =[]):
        """Recurse over the dicts structure to populate specified indexes with information from  the dictionaries in the tree.
        
        """   
        if not theDicts:
            return self
        
        if not theIndexes:
            return self
        
        aDictKind = theDicts.get( cMDDDictAttributeName_DictKind, None)
        if not ( aDictKind in cMDDDictAttributeName_DictKinds):
            return self
        
        
        
        # #####################################
        """Populate indexes with values from the current dict.
        
        """
        if aDictKind in cMDDDictIndexableDictKinds:
            someIndexNames = theIndexes.keys()
            for anIndexName in someIndexNames:
                
                anIndexableValue = theDicts.get( anIndexName, None)
                if not ( anIndexableValue == None):
                    
                    anIndex = theIndexes.get( anIndexName, None)
                    if not ( anIndex == None):
                        
                        someCurrentValues = anIndex.get( anIndexableValue, None)
                        if not someCurrentValues:
                            someCurrentValues = [  ]
                            anIndex[ anIndexableValue] = someCurrentValues
                        
                        someCurrentValues.append( thePath)
                    

                    
        # #####################################
        """Drill down and recurse to sub dictionaries in the tree, according to current dict kind.
        
        """
        if aDictKind == cMDDDictAttributeName_DictKind_Element:
            someSubDicts = theDicts.get( cMDDDictAttributeName_Features, None) 
            if someSubDicts:
                
                aPath = thePath[:]
                aPath.append( cMDDDictAttributeName_Features)
                
                for aSubDictIdx in range( len( someSubDicts)):
                    
                    aSubDict = someSubDicts[ aSubDictIdx]
                    aSubPath = aPath[:]
                    aSubPath.append( aSubDictIdx)
                    
                    self.pIndexToDicts_recursive( 
                        theDicts   =aSubDict,
                        theIndexes =theIndexes,
                        thePath    =aSubPath,
                    )
                    
            return self

        
        if aDictKind == cMDDDictAttributeName_DictKind_Attribute:
            return self
            
        
        if aDictKind == cMDDDictAttributeName_DictKind_Aggregation:
            someSubDicts = theDicts.get( cMDDDictAttributeName_Elements, None) 
            if someSubDicts:
                
                aPath = thePath[:]
                aPath.append( cMDDDictAttributeName_Elements)
                
                for aSubDictIdx in range( len( someSubDicts)):
                    
                    aSubDict = someSubDicts[ aSubDictIdx]
                    aSubPath = aPath[:]
                    aSubPath.append( aSubDictIdx)
                    
                    self.pIndexToDicts_recursive( 
                        theDicts   =aSubDict,
                        theIndexes =theIndexes,
                        thePath    =aSubPath,
                    )
            return self
                    
        
        if aDictKind == cMDDDictAttributeName_DictKind_Relation:
            someSubDicts = theDicts.get( cMDDDictAttributeName_ElementRefs, None) 
            if someSubDicts:
                
                aPath = thePath[:]
                aPath.append( cMDDDictAttributeName_ElementRefs)
                
                for aSubDictIdx in range( len( someSubDicts)):
                    
                    aSubDict = someSubDicts[ aSubDictIdx]
                    aSubPath = aPath[:]
                    aSubPath.append( aSubDictIdx)
                    
                    self.pIndexToDicts_recursive( 
                        theDicts   =aSubDict,
                        theIndexes =theIndexes,
                        thePath    =aSubPath,
                    )
            return self
                    
        
        if aDictKind == cMDDDictAttributeName_DictKind_Reference:
            someSubDicts = theDicts.get( cMDDDictAttributeName_ElementRefs, None) 
            if someSubDicts:
                
                aPath = thePath[:]
                aPath.append( cMDDDictAttributeName_ElementRefs)
                
                for aSubDictIdx in range( len( someSubDicts)):
                    
                    aSubDict = someSubDicts[ aSubDictIdx]
                    aSubPath = aPath[:]
                    aSubPath.append( aSubDictIdx)
                    
                    self.pIndexToDicts_recursive( 
                        theDicts   =aSubDict,
                        theIndexes =theIndexes,
                        thePath    =aSubPath,
                    )
            return self
                    
        
        if aDictKind == cMDDDictAttributeName_DictKind_ElementRef:
            return self
        
        return self
    

        
        
        
        
        


    # ############################################################
    """OLD Dictionaries tree access acceleration by indexing.
    
    """
    
    
    security.declarePrivate( 'fIndexToDicts_OLD')
    def fIndexToDicts_OLD( self,
        theModelDDvlPloneTool =None,
        theContextualElement  =None, 
        theDicts              =None, 
        theIndexNames         =None):
        """Create specified indexes with information from the dictionaries in the tree.
        
        """
        
        if not theIndexNames:
            return []
        
        
        if not theDicts:
            return []
        
        
        someIndexNames = [ ]
        
        for anIndexName in theIndexNames:
            if anIndexName in cMDDDictIndexableAttributeNames:
                someIndexNames.append( anIndexName)
                
        if not someIndexNames:
            return [ ]
        

        
        someIndexes = dict ( [ [ anIndexName, { },] for anIndexName in someIndexNames ])

        self.pIndexToDicts_recursive( 
            theDicts,
            someIndexes,
        )
        
        return someIndexes
    

    
    
    
    
    security.declarePrivate( 'pIndexToDicts_recursive_OLD')
    def pIndexToDicts_recursive_OLD( self,
        theDicts           =None, 
        theIndexes         =None):
        """Recurse over the dicts structure to populate specified indexes with information from  the dictionaries in the tree.
        
        """   
        if not theDicts:
            return self
        
        if not theIndexes:
            return self
        
        aDictKind = theDicts.get( cMDDDictAttributeName_DictKind, None)
        if not ( aDictKind in cMDDDictAttributeName_DictKinds):
            return self
        
        
        
        # #####################################
        """Populate indexes with values from the current dict.
        
        """
        if aDictKind in cMDDDictIndexableDictKinds:
            someIndexNames = theIndexes.keys()
            for anIndexName in someIndexNames:
                
                anIndexableValue = theDicts.get( anIndexName, None)
                if not ( anIndexableValue == None):
                    
                    anIndex = theIndexes.get( anIndexName, None)
                    if not ( anIndex == None):
                        
                        someCurrentValues = anIndex.get( anIndexableValue, None)
                        if not someCurrentValues:
                            someCurrentValues = [  ]
                            anIndex[ anIndexableValue] = someCurrentValues
                        
                        someCurrentValues.append( theDicts)
                    
                    
        # #####################################
        """Drill down and recurse to sub dictionaries in the tree, according to current dict kind.
        
        """
        if aDictKind == cMDDDictAttributeName_DictKind_Element:
            someSubDicts = theDicts.get( cMDDDictAttributeName_Features, None) 
            if someSubDicts:
                for aSubDict in someSubDicts:
                    self.pIndexToDicts_recursive( 
                        theDicts   =aSubDict,
                        theIndexes =theIndexes,
                    )
                    
            return self

        
        if aDictKind == cMDDDictAttributeName_DictKind_Attribute:
            return self
            
        
        if aDictKind == cMDDDictAttributeName_DictKind_Aggregation:
            someSubDicts = theDicts.get( cMDDDictAttributeName_Elements, None) 
            if someSubDicts:
                for aSubDict in someSubDicts:
                    self.pIndexToDicts_recursive( 
                        theDicts   =aSubDict,
                        theIndexes =theIndexes,
                    )
            return self
                    
        
        if aDictKind == cMDDDictAttributeName_DictKind_Relation:
            someSubDicts = theDicts.get( cMDDDictAttributeName_ElementRefs, None) 
            if someSubDicts:
                for aSubDict in someSubDicts:
                    self.pIndexToDicts_recursive( 
                        theDicts   =aSubDict,
                        theIndexes =theIndexes,
                    )
            return self
                    
        
        if aDictKind == cMDDDictAttributeName_DictKind_Reference:
            someSubDicts = theDicts.get( cMDDDictAttributeName_ElementRefs, None) 
            if someSubDicts:
                for aSubDict in someSubDicts:
                    self.pIndexToDicts_recursive( 
                        theDicts   =aSubDict,
                        theIndexes =theIndexes,
                    )
            return self
                    
        
        if aDictKind == cMDDDictAttributeName_DictKind_ElementRef:
            return self
        
        return self
    

        
        
                
    
    # ############################################################
    """Auxiliary method to deliver a callable for index lookup .
    
    """        
        
        
    security.declarePrivate( 'fResolveByIndex_Callable')
    def fResolveByIndex_Callable( self,
        theModelDDvlPloneTool       =None,
        theContextualElement = None,):
        """Obtain a callable element able to resolve model element from their identity.
        
        """
        
        return fResolveByIndex 
            
            
        
        
        
        
        
    
    # ############################################################
    """Traversal and dictionaries tree generation methods.
    
    """
    

    security.declarePrivate( 'fToDicts')
    def fToDicts( self,
        theModelDDvlPloneTool       =None,
        theElement                  =None, 
        theAllToDictsTypeConfigs    =None, 
        theAdditionalParams         =None):
        """Create a dictionaries tree with data from an element and its recursive contents, including binary like files and images."
        
        """

             
        unToDictsContext = self.fNewVoidToDictsContext()
        
        unToDictsContext[ 'type_configs'] = theAllToDictsTypeConfigs
        
        unToDictsReport  = self.fToDictsReport( unToDictsContext)
        if ( unToDictsReport == None):
            unToDictsReport = self.fNewVoidToDictsReport()
            unToDictsReport.update( { 
                'success':      False,
                'status':       cMDDToDictsStatus_Error_Internal_NoToDictsReport,
                'method':       'fToDicts',
            })
            return unToDictsReport
        
 
        if ( theElement == None):
            unToDictsReport.update( { 
                'success':      False,
                'status':       cMDDToDictsStatus_Error_MissingParameter_Element,
                'method':       'fToDicts',
            })
            return unToDictsReport
            
        
        
        if not theAllToDictsTypeConfigs:
            unToDictsReport.update( { 
                'success':      False,
                'status':       cMDDToDictsStatus_Error_MissingParameter_ToDictsTypeConfigs,
                'method':       'fToDicts',
            })
            return unToDictsReport
        
        
        
        
        # ##############################################################################
        """Initialize report with root information.
        
        """
        
        aMetaType = None
        try:
            aMetaType = theElement.meta_type
        except:
            None

        aPloneId = None
        try:
            aPloneId = theElement.getId()
        except:
            None

        aTitle = None
        try:
            aTitle = theElement.Title()
        except:
            None
        
        aUID = None
        try:
            aUID = theElement.UID()
        except:
            None
            

        aPhysicalPath = None
        try:
            aPhysicalPath = self.fPhysicalPathStringForElement( theElement)
        except:
            None
       
        unToDictsReport.update({
            'root_meta_type':           aMetaType,
            'root_id':                  aPloneId,
            'root_title':               aTitle,
            'root_UID':                 aUID,
            'root_physhical_path':      aPhysicalPath,
        })
        
        
        
        

         
        # ##############################################################################
        """Traverse root element and children, recursively building the dictionaries tree.
        
        """
        
        unToDictsResult = self.fToDicts_Recursive( 
            theElement                  =theElement, 
            theToDictsContext           =unToDictsContext,
            theAdditionalParams         =theAdditionalParams)
        
        if not unToDictsResult:
            unToDictsReport.update( { 
                'success':      False,
                'status':       cMDDToDictsStatus_Error_ToDictsRecursive_Failed,
                'method':       'fToDicts',
            })
            return unToDictsReport
        
        
        self.pToDicts_ResolveReferences( 
            theToDictsContext      =unToDictsContext,
            theAdditionalParams    =theAdditionalParams
        )
        
        
        someToDictErrors  = self.fToDictErrors( unToDictsContext)
        if someToDictErrors == None:
            unToDictsReport.update( { 
                'success':      False,
                'status':       cMDDToDictsStatus_Error_Internal_NoToDictsErrors,
                'method':       'fToDicts',
            })
            return unToDictsReport
            
        if len( someToDictErrors):
            unToDictsReport.update( { 
                'success':      False,
                'status':       cMDDToDictsStatus_Error_ToDictsRecursive_ErrorsOccurred,
                'method':       'fToDicts',
            })
            return unToDictsReport
            
 
        
        unDictsRoot = unToDictsContext.get( 'dicts_root', None)
        if unDictsRoot == None:
            unToDictsReport.update( { 
                'success':      False,
                'status':       cMDDToDictsStatus_Error_Internal_NoDictsRoot,
                'method':       'fToDicts',
            })
            return unToDictsReport
        

        unToDictsReport.update( { 
            'success':      True,
        })
                
        return unToDictsReport
        
    
    

    
    
    
    
    
    
    security.declarePrivate( 'fToDicts_Recursive')
    def fToDicts_Recursive( self,
        theElement                  =None, 
        theToDictsContext           =None,
        theAdditionalParams         =None):
        """Create a dictionaries tree with data from an element and its recursive contents, including binary like files and images."
        
        """

        if theElement == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Element,
                'method':       'fToDicts_Recursive',
            })
            return False

        
        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fToDicts_Recursive',
            })
            return False
              
        
        allTypeConfigs = theToDictsContext.get( 'type_configs', None)
        if allTypeConfigs == None:
            return False
        
        
        unElementMetaType = theElement.meta_type
        
        unTypeConfig = allTypeConfigs.get( unElementMetaType, {})
        if not unTypeConfig:
            """If no type config for the element type, Ignore object and do not todicts it, allowing the caller to continue with other objects, if any.
            
            """
            return True
        


            
        # ##############################################################################
        """Create new element in the document and set identifying attributes.
        
        """
        unNewElementDict = self.fNewToDictForElement( theToDictsContext, theElement)
        if unNewElementDict == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Failed_Factory_ForElement,
                'method':       'fToDicts_Recursive',
            })
            return False
        
            

        
        try:
            
            # ##############################################################################
            """Retrieve the element's schema.
            
            """
            unObjectSchema = theElement.schema
            if not unObjectSchema:
                self.pReportToDictError( theToDictsContext, { 
                    'status':       cMDDToDictsStatus_Error_Internal_ObjectHasNoSchema,
                    'method':       'fToDicts_Recursive',
                })
                return False
           
            
            
            
            
            
            # ##############################################################################
            """Iterate and todicts each configured attribute.
            
            """
            unosAttrConfigs       = unTypeConfig.get( 'attrs', [])
            
            if unosAttrConfigs:
                
                unAttributesToDicted = self.fToDicts_Attributes(
                    theAttributeConfigs    =unosAttrConfigs, 
                    theObjectSchema        =unObjectSchema,
                    theToDictsContext      =theToDictsContext,
                    theAdditionalParams    =theAdditionalParams,
                )
                if not unAttributesToDicted:
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_ToDicts_Attributes_Failed,
                        'method':       'fToDicts_Recursive',
                    })
                    return False
                        
                        
                        
            # ##############################################################################
            """Iterate and todicts each configured aggregation or relationship.
            
            """
            unosTraversalConfigs = unTypeConfig.get( 'traversals', [])
            
            if unosTraversalConfigs:
                
                unTraversalsToDicted = self.fToDicts_Traversals( 
                    theTraversalConfigs         =unosTraversalConfigs, 
                    theObjectSchema             =unObjectSchema,
                    theToDictsContext           =theToDictsContext,
                    theAdditionalParams         =theAdditionalParams,
                )
                if not unTraversalsToDicted:
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_ToDicts_Traversals_Failed,
                        'method':       'fToDicts_Recursive',
                    })
                    return False
            
                    
                     
            return True
                     
        finally: 

            if not ( unNewElementDict == None):
                unDictsStack = self.fToDictsStack( theToDictsContext)
                if unDictsStack and ( unNewElementDict == unDictsStack[ -1]):
                    unDictsStack.pop()
                    
                unNewElementDict.pop( cMDDDictAttributeName_Element)
              
   
    
    
                    
    
    
    security.declarePrivate( 'fToDicts_Attributes')
    def fToDicts_Attributes( self,
        theAttributeConfigs         =None, 
        theObjectSchema             =None,
        theToDictsContext           =None,
        theAdditionalParams         =None):
        """Create a dictionaries tree with data from an element and its recursive contents, including binary content like files and images."
        
        """

        if not theAttributeConfigs:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_AttributeConfigs,
                'method':       'fToDicts_Attributes',
            })
            return False
                
        if not theObjectSchema: 
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoObjectSchema,
                'method':       'fToDicts_Attributes',
            })
            return False
                
        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fToDicts_Recursive',
            })
            return False

        anElement = self.fCurrentElement( theToDictsContext)
        if anElement == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoCurrentElement,
                'method':       'fToDicts_Attributes',
            })
            return False
                
        
        someFieldsToIgnore = self.fIgnoredFeatureNamesForElement( 
            theToDictsContext           =theToDictsContext,
            theElement                  =anElement,
        )
        
        for unAttrConfig in theAttributeConfigs:
            
            unAttrName = unAttrConfig.get( 'name', '')
            if unAttrName and not ( unAttrName in someFieldsToIgnore):

                anAttributeToDicted = self.fToDicts_Attribute( 
                    theAttributeConfig          =unAttrConfig, 
                    theObjectSchema             =theObjectSchema,
                    theToDictsContext           =theToDictsContext,
                    theAdditionalParams         =theAdditionalParams,
                )
                if not anAttributeToDicted:
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_ToDicts_Attribute_Failed,
                        'details':      unAttrName,
                        'method':       'fToDicts_Attributes',
                    })
                    return False
            
                     
        return True
    
    
    

    

    
    security.declarePrivate( 'fToDicts_Attribute')
    def fToDicts_Attribute( self,
        theAttributeConfig          =None, 
        theObjectSchema             =None,
        theToDictsContext           =None,
        theAdditionalParams         =None):
        """Create a dictionary with data from an element attribute, including binary content like files and images."
        
        """
                
        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fToDicts_Attribute',
            })
            return False
        
        if not theAttributeConfig:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_AttributeConfig,
                'method':       'fToDicts_Attribute',
            })
            return False
                
        unAttrName = theAttributeConfig.get( 'name', '')
        if not unAttrName:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoAttributeName,
                'method':       'fToDicts_Attribute',
            })
            return False
        
        if not theObjectSchema:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoObjectSchema,
                'details':      unAttrName,
                'method':       'fToDicts_Attribute',
            })
            return False


        anElement = self.fCurrentElement( theToDictsContext)
        if anElement == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoCurrentElement,
                'details':      unAttrName,
                'method':       'fToDicts_Attribute',
            })
            return False
        
        
        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if unToDictsReport == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoToDictsReport,
                'details':      unAttrName,
                'method':       'fToDicts_Attribute',
            })
            return False            
                  

        
        


        unAttrType         = theAttributeConfig.get( 'type',      '').lower()
        
        if not( unAttrType in [ 'computed', 'string', 'text', 'selection', 'boolean', 'number', 'integer', 'float','fixedpoint', 'date', 'datetime', 'image', 'file', ]):  
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Failed_Attribute_UnknownAttributeType,
                'details':      unAttrName,
                'method':       'fToDicts_Atrribute',
            })
            return False
        
        
        
        
        unAttrAccessorName = theAttributeConfig.get( 'accessor',  '')     
        unAttributeName    = theAttributeConfig.get( 'attribute', '')    
        
        
        unElementMetaType = anElement.meta_type

        
        unRawValue             = None
        unObjectAttributeField = None   
        
        unNewAttributeDict     = None
        
        try:
        
            # ##########################################################
            """Retrieve attribute value.
            
            """
            
            if unAttrAccessorName or unAttributeName:
                
                if unAttrAccessorName:
                    unAccessor = None
                    try:
                        unAccessor = anElement[ unAttrAccessorName]    
                    except:
                        None
                    if not unAccessor:
                        self.pReportToDictError( theToDictsContext,  { 
                            'status':       cMDDToDictsStatus_Error_Internal_AttributeAccessorNotFound,
                            'meta_type':    unElementMetaType,
                            'attr':         unAttrName,
                            'accessor':     unAccessor,
                            'path':         '/'.join( anElement.getPhysicalPath()),
                        })
                        return False
                    
                    try:
                        unRawValue = unAccessor()
                        
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                        unInformeExcepcion = 'Exception during fToDicts_Recursive during invocation of element explicit accessor for attribute\n' 
                        try:
                            unInformeExcepcion += 'meta_type=%s path=%s attribute=%s accessor=%s\n' % ( unElementMetaType, '/'.join( anElement.getPhysicalPath()), unAttrName, unAttrAccessorName,)
                        except:
                            None
                        try:
                            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        except:
                            None
                        try:
                            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        except:
                            None
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        self.pReportToDictError( theToDictsContext,  { 
                            'status':       cMDDToDictsStatus_Error_Internal_AttributeValueAccessException,
                            'method':       'fToDicts_Atrribute',
                            'meta_type':    unElementMetaType,
                            'attr':         unAttrName,
                            'path':         '/'.join( anElement.getPhysicalPath()),
                            'exception':    unInformeExcepcion,
                        })
                        aLogger = logging.getLogger( 'ModelDDvlPloneTool')
                        aLogger.error( unInformeExcepcion) 
                        
                        return False
                            
                    
                if unAttributeName:
                    
                    unAttributeOwner = anElement
                    if unAttrAccessorName:
                        unAttributeOwner = unRawValue
                        
                    if ( unAttributeOwner == None):
                        return False
                    
                    try:
                        unRawValue = unAttributeOwner.__getattribute__( unAttributeName)
                        if unRawValue.__class__.__name__ == "ComputedAttribute":
                            unComputedAttribute = unRawValue
                            unRawValue = unComputedAttribute.__get__( unAttributeOwner)
                    except:
                        unaExceptionInfo = sys.exc_info()
                        unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                        unInformeExcepcion = 'Exception during fToDicts_Recursive during access to element getattribute\n' 
                        try:
                            unInformeExcepcion += 'meta_type=%s path=%s attribute=%s attributeName=%s\n' % ( unElementMetaType, '/'.join( anElement.getPhysicalPath()), unAttrName, unAttributeName)
                        except:
                            None
                        try:
                            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                        except:
                            None
                        try:
                            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                        except:
                            None
                        unInformeExcepcion += unaExceptionFormattedTraceback   
                        
                        self.pReportToDictError( theToDictsContext,  { 
                            'status':       cMDDToDictsStatus_Error_Internal_AttributeValueAccessException,
                            'method':       'fToDicts_Atrribute',
                            'meta_type':    unElementMetaType,
                            'attr':         unAttrName,
                            'path':         '/'.join( anElement.getPhysicalPath()),
                            'exception':    unInformeExcepcion,
                        })
                        aLogger = logging.getLogger( 'ModelDDvlPloneTool')
                        aLogger.info( unInformeExcepcion) 
                        
                        return False

                    
            else:
                if not theObjectSchema.has_key( unAttrName):
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_Internal_NoFieldInSchema,
                        'details':      unAttrName,
                        'method':       'fToDicts_Atrribute',
                    })
                    return False
                
                unObjectAttributeField          = theObjectSchema[ unAttrName]
    
                unRawValue = None
                try:
                    unRawValue = unObjectAttributeField.getRaw( anElement)
                except:
                    unaExceptionInfo = sys.exc_info()
                    unaExceptionFormattedTraceback = ''.join(traceback.format_exception( *unaExceptionInfo))
                    unInformeExcepcion = 'Exception during fToDicts_Recursive accessing element attribute with getRaw\n' 
                    try:
                        unInformeExcepcion += 'meta_type=%s path=%s attribute=%s\n' % ( unElementMetaType, '/'.join( anElement.getPhysicalPath()), unAttrName,)
                    except:
                        None
                    try:
                        unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
                    except:
                        None
                    try:
                        unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
                    except:
                        None
                    unInformeExcepcion += unaExceptionFormattedTraceback   
                    
                    self.pReportToDictError( theToDictsContext,  { 
                        'status':       cMDDToDictsStatus_Error_Internal_AttributeValueAccessException,
                        'meta_type':    unElementMetaType,
                        'attr':         unAttrName,
                        'path':         '/'.join( anElement.getPhysicalPath()),
                        'exception':    unInformeExcepcion,
                    })
                    aLogger = logging.getLogger( 'ModelDDvlPloneTool')
                    aLogger.info( unInformeExcepcion) 
                    
                    return False
                
                
                unAttrType      = unObjectAttributeField.type.lower()
                if unAttrType == 'computed':
                    unAttrType = theAttributeConfig.get( 'type', '').lower() 
                    
                unWidget = unObjectAttributeField.widget
                if unWidget and (unWidget.getType() == 'Products.Archetypes.Widget.SelectionWidget') and unObjectAttributeField.__dict__.has_key('vocabulary'):
                    unAttrType = 'selection'
                
                    
                if not( unAttrType in [ 'string', 'text', 'selection', 'boolean', 'number', 'integer', 'float','fixedpoint', 'date', 'datetime', 'image', 'file', ]):  
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_Failed_Attribute_UnknownAttributeType,
                        'details':      unAttrName,
                        'method':       'fToDicts_Atrribute',
                    })
                    return False
                    
               
                
                
            # ##########################################################
            """Create dict according to attribute type.
            
            """

            if unAttrType in [ 'string', 'text', 'selection', 'boolean', 'number', 'integer', 'float','fixedpoint',]:  
                                
                unNewAttributeDict = self.fNewToDictForAttribute( theToDictsContext, unAttrName)
                if unNewAttributeDict == None:
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_Failed_Factory_ForAttribute,
                        'details':      unAttrName,
                        'method':       'fToDicts_Atrribute',
                    })
                    return False
            
                unNewAttributeDict.update( {
                    cMDDDictAttributeName_AttributeType:  unAttrType,
                    cMDDDictAttributeName_AttributeValue: unRawValue,
                })           
                    
                return True
                    
                    
            elif unAttrType in [ 'datetime', 'date', ]: 
                
                unDateValue = None
                if unRawValue:
                    unDateValue = DateTime( unRawValue)
                    
                unNewAttributeDict = self.fNewToDictForAttribute( theToDictsContext, unAttrName)
                if unNewAttributeDict == None:
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_Failed_Factory_ForAttribute,
                        'details':      unAttrName,
                        'method':       'fToDicts_Atrribute',
                    })
                    return False
            
                unNewAttributeDict.update( {
                    cMDDDictAttributeName_AttributeType:  unAttrType,
                    cMDDDictAttributeName_AttributeValue: unDateValue,
                })
    
                return True
                        
                        
                        
            elif unAttrType == 'image':
                                  
                unNewAttributeDict = self.fNewToDictForAttribute_Image( theToDictsContext, unAttrName)
                if unNewAttributeDict == None:
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_Failed_Factory_ForAttribute,
                        'details':      unAttrName,
                        'method':       'fToDicts_Atrribute',
                    })
                    return False
            
                unNewAttributeDict.update( {
                    cMDDDictAttributeName_AttributeType:  unAttrType,
                })
                    
                if unRawValue:
                    
                    unaImage = unRawValue
                    unaImageAsFile = unaImage.getImageAsFile()
                    
                    unImageId          = unaImage.getId()
                    unImageTitle       = unaImage.Title()
                    unImageContentType = None
                    
                    unFilename = unaImage.filename
                    if not unFilename:
                        unFilename = unaImage.getFilename()
                    if not unFilename:
                        unFilename = ''
                    else:
                        if unFilename.__class__.__name__ == 'unicode':
                            unFilename = unFilename.encode()
                                                    
                        
                    if unObjectAttributeField:
                        unImageContentType = unObjectAttributeField.getContentType( anElement)
                  
                    unNewAttributeDict.update( {
                        cMDDDictAttributeName_AttributeValue: unaImageAsFile,
                        cMDDDictAttributeName_ImageId:        unImageId,
                        cMDDDictAttributeName_ImageTitle:     unImageTitle,
                        cMDDDictAttributeName_ImageFilename:  unFilename,
                    })
                    if unImageContentType:
                        unNewAttributeDict.update( {
                            cMDDDictAttributeName_ContentType:  unImageContentType,
                        })
                        
                return True

                        
                                                
            elif unAttrType == 'file':
                
                unNewAttributeDict = self.fNewToDictForAttribute( theToDictsContext, unAttrName)
                if unNewAttributeDict == None:
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_Failed_Factory_ForAttribute,
                        'details':      unAttrName,
                        'method':       'fToDicts_Atrribute',
                    })
                    return False
            
                unNewAttributeDict.update( {
                    cMDDDictAttributeName_AttributeType:  unAttrType,
                })
                    
                if unRawValue:
    
                   
                    unaFile = unRawValue
                    unaFileAsFile = unaFile.getFileAsFile()
                    
                    unFileId          = unaFile.getId()
                    unFileTitle       = unaFile.Title()
                    unFileContentType = None
                    
                    unFilename = unaFile.filename
                    if not unFilename:
                        unFilename = unaFile.getFilename()
                    if not unFilename:
                        unFilename = ''
                    else:
                        if unFilename.__class__.__name__ == 'unicode':
                            unFilename = unFilename.encode()
                                                    
                        
                    if unObjectAttributeField:
                        unFileContentType = unObjectAttributeField.getContentType( anElement)
                  
                    unNewAttributeDict.update( {
                        cMDDDictAttributeName_AttributeValue: unaFileAsFile,
                        cMDDDictAttributeName_FileId:        unFileId,
                        cMDDDictAttributeName_FileTitle:     unFileTitle,
                        cMDDDictAttributeName_FileFilename:  unFilename,
                    })
                    if unFileContentType:
                        unNewAttributeDict.update( {
                            cMDDDictAttributeName_ContentType:  unFileContentType,
                        })
                    
                return True
                    
                    
            else:
                
                return False
            
            
            return True
 
        finally:  
            if not ( unNewAttributeDict == None):
                unDictsStack = self.fToDictsStack( theToDictsContext)
                if unDictsStack and ( unNewAttributeDict == unDictsStack[ -1]):
                    unDictsStack.pop()
              
                     
    
        
   

   
   
   
   

    

    
    security.declarePrivate( 'fToDicts_Traversals')
    def fToDicts_Traversals( self,
        theTraversalConfigs         =None, 
        theObjectSchema             =None,
        theToDictsContext           =None,
        theAdditionalParams         =None):
        """Create a dictionaries tree with data from an element and its recursive contents, including binary content like files and images."
        
        """

        if not theTraversalConfigs:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_TraversalConfigs,
                'method':       'fToDicts_Traversals',
            })
            return True
                
        if not theObjectSchema:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoObjectSchema,
                'method':       'fToDicts_Traversals',
            })
            return False
                
        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fToDicts_Recursive',
            })
            return False

        anElement = self.fCurrentElement( theToDictsContext)
        if anElement == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoCurrentElement,
                'method':       'fToDicts_Traversals',
            })
            return False
        

        someFieldsToIgnore = self.fIgnoredFeatureNamesForElement( 
            theToDictsContext           =theToDictsContext,
            theElement                  =anElement,
        )
        
                    

        for unTraversalConfig in theTraversalConfigs:
            
            unAggregationName = unTraversalConfig.get( 'aggregation_name', '')
            if unAggregationName and not ( unAggregationName in someFieldsToIgnore):
                
                aTraversalToDicted = self.fToDicts_Aggregation( 
                    theTraversalConfig          =unTraversalConfig, 
                    theObjectSchema             =theObjectSchema,
                    theToDictsContext           =theToDictsContext,
                    theAdditionalParams         =theAdditionalParams,
                )
                if not aTraversalToDicted:
                    self.pReportToDictError( theToDictsContext, { 
                        'status':       cMDDToDictsStatus_Error_ToDicts_Aggregation_Failed,
                        'details':      unAggregationName,
                        'method':       'fToDicts_Traversals',
                    })
                    return False
                
            else:
                unRelationName = unTraversalConfig.get( 'relation_name', '')
                if unRelationName and not ( unAggregationName in someFieldsToIgnore):   
                    
                    aTraversalToDicted = self.fToDicts_Relation( 
                        theTraversalConfig          =unTraversalConfig, 
                        theObjectSchema             =theObjectSchema,
                        theToDictsContext           =theToDictsContext,
                        theAdditionalParams         =theAdditionalParams,
                    )
                    if not aTraversalToDicted:
                        self.pReportToDictError( theToDictsContext, { 
                            'status':       cMDDToDictsStatus_Error_ToDicts_Relation_Failed,
                            'details':      unRelationName,
                            'method':       'fToDicts_Traversals',
                        })
                        return False
                    
                    
        return True
    
    
        
    
                    
                    

    

    
    security.declarePrivate( 'fToDicts_Aggregation')
    def fToDicts_Aggregation( self,
        theTraversalConfig          =None, 
        theObjectSchema             =None,
        theToDictsContext           =None,
        theAdditionalParams         =None):
        """Create a dictionary with data from all aggregated elements and their recursively contained elements, including binary content like files and images."
        
        """

        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fToDicts_Recursive',
            })
            return False
        
        if not theTraversalConfig:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_TraversalConfig,
                'method':       'fToDicts_Aggregation',
            })
            return False
                
        
        unAggregationName = theTraversalConfig.get( 'aggregation_name', '')
        if not unAggregationName:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoAggregationName,
                'method':       'fToDicts_Aggregation',
            })
            return False
        
        if not theObjectSchema:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoObjectSchema,
                'details':      unAggregationName,
                'method':       'fToDicts_Aggregation',
            })
            return False           
        

                
        anElement = self.fCurrentElement( theToDictsContext)
        if anElement == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoCurrentElement,
                'details':      unAggregationName,
                'method':       'fToDicts_Aggregation',
            })
            return False
        
 

        
         
        unField  = theObjectSchema.get( unAggregationName, None)
        if not unField:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoFieldInSchema,
                'details':      unAggregationName,
                'method':       'fToDicts_Aggregation',
            })
            return False
                        
        
        unElementMetaType = anElement.meta_type

        
        unNewTraversalDict = None
        
        try:
        
            unContainsCollections = theTraversalConfig.get( 'contains_collections', None)
            if unContainsCollections == None:
                unContainsCollections = True
            else:
                unContainsCollections = ( unContainsCollections == True)
                         
                
            unMultiplicityHigher = -1                                            
            try:
                unMultiplicityHigher = unField.multiplicity_higher
            except:
                None     
                
            unNewTraversalDict = self.fNewToDictForAggregation( theToDictsContext, unAggregationName)
            if unNewTraversalDict == None:
                self.pReportToDictError( theToDictsContext, { 
                    'status':       cMDDToDictsStatus_Error_Failed_Factory_ForAggregation,
                    'details':      unAggregationName,
                    'method':       'fToDicts_Aggregation',
                })
                return False
            
            unNewTraversalDict.update( {
                cMDDDictAttributeName_ContainsCollections: unContainsCollections,
                cMDDDictAttributeName_MultiplicityHigher:  unMultiplicityHigher,
            })
                           
                   

                    
            # ##############################################################################
            """Determine types of subitems to todicts.
            
            """
            someAcceptedPortalTypes = set( )
            
            someSubItemsConfigs   = theTraversalConfig.get( 'subitems', [])
            for aSubItemsConfig in someSubItemsConfigs:
                somePortalTypes = aSubItemsConfig.get( 'portal_types', [])
                
                someAcceptedPortalTypes.update( somePortalTypes)
             
                
                
            # ##############################################################################
            """Retrieve contained objects of the specified types.
            
            """
            someSubItems = anElement.objectValues( list( someAcceptedPortalTypes))
            
                
            if someSubItems:
                
                # ##############################################################################
                """Iterate and todicts recursively each aggregated element from theElement contained objects, which are of one of the configured types.
                
                """                 

                for unSubItem in someSubItems:
                    
                    unSubItemToDicted = self.fToDicts_Recursive( 
                        theElement                  =unSubItem, 
                        theToDictsContext           =theToDictsContext,
                        theAdditionalParams         =theAdditionalParams,
                    )
                    if not unSubItemToDicted:
                        self.pReportToDictError( theToDictsContext, { 
                            'status':       cMDDToDictsStatus_Error_ToDictsRecursive_Failed,
                            'details':      unAggregationName,
                            'method':       'fToDicts_Aggregation',
                        })
                        return False
            
            
            return True
 
        finally:  
            
            if not ( unNewTraversalDict == None):
                unDictsStack = self.fToDictsStack( theToDictsContext)
                if unDictsStack and ( unNewTraversalDict == unDictsStack[ -1]):
                    unDictsStack.pop()
              
                     
        
    
    
    
    
    


    
    security.declarePrivate( 'fToDicts_Relation')
    def fToDicts_Relation( self,
        theTraversalConfig          =None, 
        theObjectSchema             =None,
        theToDictsContext           =None,
        theAdditionalParams         =None):
        """Create a dictionary with data from all aggregated elements and their recursively contained elements, including binary content like files and images."
        
        """

                
        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fToDicts_Relation',
            })
            return False

        if not theTraversalConfig:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_TraversalConfig,
                'method':       'fToDicts_Relation',
            })
            return True
        

        unRelationName = theTraversalConfig.get( 'relation_name', '')
        if not unRelationName:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoAggregationName,
                'method':       'fToDicts_Relation',
            })
            return False
        
                
        if not theObjectSchema:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoObjectSchema,
                'details':      unRelationName,
                'method':       'fToDicts_Relation',
            })
            return False           
        


        anElement = self.fCurrentElement( theToDictsContext)
        if anElement == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoCurrentElement,
                'details':      unRelationName,
                'method':       'fToDicts_Relation',
            })
            return False
        
         
        unField  = theObjectSchema.get( unRelationName, None)
        if not unField:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoFieldInSchema,
                'details':      unRelationName,
                'method':       'fToDicts_Relation',
            })
            return False
                        
        
        unElementMetaType = anElement.meta_type

        unDictsStack = self.fToDictsStack( theToDictsContext)
        if unDictsStack == None:
            return False
        
        
        unNewTraversalDict = None
        
        try:
        
            unMultiplicityHigher = -1                                            
            try:
                unMultiplicityHigher = unField.multiplicity_higher
            except:
                None     
                
            unNewTraversalDict = self.fNewToDictForRelation( theToDictsContext, unRelationName)
            if unNewTraversalDict == None:
                self.pReportToDictError( theToDictsContext, { 
                    'status':       cMDDToDictsStatus_Error_Failed_Factory_ForRelation,
                    'details':      unRelationName,
                    'method':       'fToDicts_Relation',
                })
                return False
            
            unNewTraversalDict.update( {
                cMDDDictAttributeName_MultiplicityHigher:  unMultiplicityHigher,
            })
                           
                   

                
            # ##############################################################################
            """Determine types of related elements to todicts.
            
            """
            someAcceptedPortalTypes = set( )
            
            someRelatedTypesConfigs   = theTraversalConfig.get( 'related_types', [])
            for aRelatedItemsConfig in someRelatedTypesConfigs:
                somePortalTypes = aRelatedItemsConfig.get( 'portal_types', [])
                
                someAcceptedPortalTypes.update( somePortalTypes)
        
            
            # ##############################################################################
            """Retrieve related objects.
            
            """
            someRelatedItems = []
            
            unRelationObjectFieldAccessor = unField.getAccessor( anElement)
            if unRelationObjectFieldAccessor:
                try:
                    someRelatedItems = unRelationObjectFieldAccessor()
                except:
                    None
            
            if someRelatedItems and not ( someRelatedItems.__class__.__name__ in [ 'list', 'tuple', 'set',]):
                someRelatedItems = [ someRelatedItems,]
                        
                    
            # ##############################################################################
            """Filter retrieved related objects of the specified types.
            
            """
            someRelatedItemsOfRightType = [ ]
            if someRelatedItems:
                for aRelatedItem in someRelatedItems:
                    if not ( aRelatedItem == None):
                        aRelatedItemMetaType = aRelatedItem.meta_type
                        if aRelatedItemMetaType in someAcceptedPortalTypes:
                            someRelatedItemsOfRightType.append( aRelatedItem)
                            
                                     
                                    
            if someRelatedItemsOfRightType:
                                       
                # ##############################################################################
                """Iterate and todicts recursively each aggregated element from theElement contained objects, which are of one of the configured types.
                
                """                 


                for aRelatedItem in someRelatedItemsOfRightType:
                    
                    aNewElementRefDict = self.fNewToDictForElementRef( theToDictsContext, aRelatedItem)
                    if aNewElementRefDict == None:
                        self.pReportToDictError( theToDictsContext, { 
                            'status':       cMDDToDictsStatus_Error_Failed_Factory_ForElementRef,
                            'details':      unRelationName,
                            'method':       'fToDicts_Relation',
                        })
                        return False
            
                    if unDictsStack and ( aNewElementRefDict == unDictsStack[ -1]):
                        unDictsStack.pop()
                        
            return True
 
        finally:  
            if not ( unNewTraversalDict == None):
                if unDictsStack and ( unNewTraversalDict == unDictsStack[ -1]):
                    unDictsStack.pop()
              
        
    
    
                    
                    
                    

   
    security.declarePrivate( 'pToDicts_ResolveReferences')
    def pToDicts_ResolveReferences( self,
        theToDictsContext           =None,
        theAdditionalParams         =None):
        """Resolve in all the ElementRef dicts, the identity of the dictionary created for the referenced element, if the referenced element was contained in the root"
        
        """
        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'pToDicts_ResolveReferences',
            })
            return self
        
  
        unosDictsByPhysicalPath = theToDictsContext.get( 'dicts_by_physical_path', None)
        if unosDictsByPhysicalPath:
            
            unosElementRefs = theToDictsContext.get( 'element_refs', None)
            if unosElementRefs:
                
                for anElementRef in unosElementRefs:
                    
                    aReferencedPath = anElementRef.get( cMDDDictAttributeName_PhysicalPath, None)
                    if aReferencedPath:
                        
                        unReferencedDict = unosDictsByPhysicalPath.get( aReferencedPath, None)
                        if not ( unReferencedDict == None):
                            
                            unReferencedDictId = unReferencedDict.get( cMDDDictAttributeName_DictId, None)
                            if unReferencedDictId:
                                anElementRef[ cMDDDictAttributeName_ReferencedDictId] = unReferencedDictId   
    
        return self
    
    
    
 
    
    
    


    
    
    # #######################################################
    """Traversal helpers.
    
    """
    
    
    
    

    
           
    
    security.declarePrivate( 'fToDictsReport')
    def fToDictsReport( self, 
        theToDictsContext    =None,):
        
        if theToDictsContext == None:
            return None

        
        unToDictsReport  = theToDictsContext.get( 'report', None)
        
        if unToDictsReport == None:
            unToDictsReport = self.fNewVoidToDictsReport()
            theToDictsContext[ 'report'] = unToDictsReport
            
        return unToDictsReport
        
    
    
    
    security.declarePrivate( 'fCurrentElement')
    def fCurrentElement( self, 
        theToDictsContext    =None,):
        
        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fToDicts_Recursive',
            })
            return None

        unDictsStack = theToDictsContext.get( 'dicts_stack', None)
        if not unDictsStack:
            return None
        
        unStackLength = len( unDictsStack)
        
        unStackIndex = unStackLength - 1
        while unStackIndex >= 0:
            
            unDict = unDictsStack[ unStackIndex]
            
            if unDict.get( cMDDDictAttributeName_DictKind, None) == cMDDDictAttributeName_DictKind_Element:
                anElement = unDict.get( cMDDDictAttributeName_Element, None)
                return anElement
            
            unStackIndex -= 1
        
        return None
    
            
            
    
    
    security.declarePrivate( 'fToDictErrors')
    def fToDictErrors( self, 
        theToDictsContext    =None,):
        
        if theToDictsContext == None:
            return None

        unToDictsReport  = self.fToDictsReport( theToDictsContext)
        if unToDictsReport == None:
            return None
        
        someDictErrors = unToDictsReport.get( 'todict_errors', None)
        if someDictErrors == None:
            someDictErrors = []
            theToDictsContext[ 'todict_errors'] = someDictErrors
            
        return someDictErrors
                
    
    
    security.declarePrivate( 'fToDictsStack')
    def fToDictsStack( self, 
        theToDictsContext    =None,):
        
        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fToDictsStack',
            })
            return None

        unToDictsStack  = theToDictsContext.get( 'dicts_stack', None)
        
        if unToDictsStack == None:
            self.pReportToDictError( theToDictsContext, { 
                'status':       cMDDToDictsStatus_Error_Internal_NoToDictsStack,
                'method':       'fToDictsStack',
            })
            
        return unToDictsStack
                  
    
    

    security.declarePrivate( 'fToDictsStackDepth')
    def fToDictsStackDepth( self, 
        theToDictsContext    =None,):
        
        aDictsStack = self.fToDictsStack( theToDictsContext)
        if not aDictsStack:
            return 0
        
        return len( aDictsStack)
    
    
                  
    
    
        
    
    security.declarePrivate( 'fIgnoredFeatureNamesForElement')
    def fIgnoredFeatureNamesForElement( self,
        theToDictsContext           =None,
        theElement                  =None):
        """Retrieve the feature names to ignore for elements of the type of the parameter element."
        
        """

        if theToDictsContext == None:
            self.pReportToDictError( theToDictsContext,  { 
                'status':       cMDDToDictsStatus_Error_MissingParameter_Context,
                'method':       'fIgnoredFeatureNamesForElement',
            })
            return []

        if theElement == None:
            return []

        unIgnoredFeatureNamesByType = theToDictsContext.get( 'ignored_feature_names_by_type', None)
        if unIgnoredFeatureNamesByType == None:
            return []   
        
        anElementMetaType = theElement.meta_type
        
        someIgnoredFeatures = unIgnoredFeatureNamesByType.get( anElementMetaType, None)
        if not ( someIgnoredFeatures == None):
            return someIgnoredFeatures
        
        someIgnoredFeatures = set( )
        
        
        # #####################################
        """Retrieve Audit field names.
        
        """
            
        aFieldName = None
        
        try:
            aFieldName = theElement.creation_date_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName =  theElement.creation_user_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.modification_date_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.modification_user_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.deletion_date_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.deletion_user_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.is_inactive_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.change_counter_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.change_log_field
        except:
            None   
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.sources_counters_field
        except:
            None   
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)
            
            
        
        """Retrieve Versioning and Translation fields names
        
        """
        aFieldName = None
        try:
            aFieldName = theElement.inter_version_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.version_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.version_storage_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.version_comment_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.version_comment_storage_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.inter_translation_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.language_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.fields_pending_translation_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)

        aFieldName = None
        try:
            aFieldName = theElement.fields_pending_revision_field
        except:
            None            
        if aFieldName:
            someIgnoredFeatures.add( aFieldName)
           
         
        someFieldNames = None
        try:
            someFieldNames = theElement.versioning_link_fields
        except:
            None            
        if someFieldNames:
            someIgnoredFeatures.update( someFieldNames)

        someFieldNames = None
        try:
            someFieldNames = theElement.translation_link_fields
        except:
            None            
        if someFieldNames:
            someIgnoredFeatures.update( someFieldNames)

        someFieldNames = None
        try:
            someFieldNames = theElement.usage_link_fields
        except:
            None            
        if someFieldNames:
            someIgnoredFeatures.update( someFieldNames)

        someFieldNames = None
        try:
            someFieldNames = theElement.derivation_link_fields
        except:
            None            
        if someFieldNames:
            someIgnoredFeatures.update( someFieldNames)
  
        unIgnoredFeatureNamesByType[  anElementMetaType] = someIgnoredFeatures
        
        return someIgnoredFeatures
    
        
    
    
    
    
    
    
    
    
    

    
    # #######################################################
    
    
    security.declarePrivate( 'pReportToDictError')
    def pReportToDictError( self, 
        theToDictsContext    =None,
        theDictError         =None,):
        """Error reporting method.
        
        """    
        
        if theToDictsContext == None:
            return self
        
        if not theDictError:
            return self
        
        aDictsStackDepth = self.fToDictsStackDepth( theToDictsContext)
        theDictError[ 'stack_depth'] = aDictsStackDepth
        

        someDictErrors  = self.fToDictErrors( theToDictsContext)
        if someDictErrors == None:
            return self
    
        someDictErrors.append( theDictError)
        
        if cMDDLogToDictsErrors:
            aLogger = logging.getLogger( 'ModelDDvlPloneTool')
            anErrorIO = StringIO()
            anErrorIO.write( 'ERROR in ToDict:\n')
            for anErrorKey in sorted( theDictError.keys()):
                anErrorIO.write( '    %s = %s\n' % ( anErrorKey, theDictError.get( anErrorKey, ''),))
            anErrorString = anErrorIO.getvalue()
            
            aLogger.info( anErrorString)
        
        return self
    
            
    
    
    
    
    
    
    
    
    
    
    # #######################################################
    """Path methods.
    
    """
    
    security.declarePublic('fPhysicalPathStringForElement')
    def fPhysicalPathStringForElement(self, theElement=None):
        if theElement == None:
            return ''
        
        unPhysicalPath = theElement.getPhysicalPath()
        if not unPhysicalPath:
            return ''
     
        unPathString = '/'.join( unPhysicalPath)
        return unPathString





    security.declarePrivate( 'fPathRelativeToRoot')
    def fPathRelativeToRoot( self, theElement, theRootElement, theAdditionalPathStep=''):
        
        if ( theElement == None) or ( theRootElement == None):
            return []
    
            
        unElementPath     = theElement.getPhysicalPath()
        unRootPath        = theRootElement.getPhysicalPath()
        
        unRootPathLength = len( unRootPath)
        
        if len( unElementPath) <= unRootPathLength:
            return []
        
        for unPathIndex in range( unRootPathLength):
            
            unElementStep = unElementPath[ unPathIndex]
            unRootStep    = unRootPath[    unPathIndex]
            
            if not ( unElementStep == unRootStep):
                return []
            
        unRelativePath = unElementPath[ unRootPathLength:]    
        unRelativePath = list( unRelativePath)
        
        if theAdditionalPathStep:
            unRelativePath.extend( [ theAdditionalPathStep,])
            
        return unRelativePath
    
   
    
    
    security.declarePrivate( 'fPathStringRelativeToRoot')
    def fPathStringRelativeToRoot( self, theElement, theRootElement, theAdditionalPathStep=''):
        
        unPath = self.fPathRelativeToRoot( theElement, theRootElement, theAdditionalPathStep)
        if not unPath:
            return '/'        
        
        unPathString  = '/' + '/'.join( unPath)
        
        return unPathString 


    
    


    
            
                         