# -*- coding: utf-8 -*-
#
# File: MDDLinkedList.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Model Driven Development sl and Antonio Carrasco Valero
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

import os

import sys
import traceback
import logging

from time import time

from DateTime import DateTime

from StringIO import StringIO



from AccessControl import ClassSecurityInfo


# #######################################################
"""Configuration of class behavior during development or quality assurance.

"""

_cInDevelopment  = True

_cLogExceptions  = True

        




_cPropertyAccess_KeyNotFound_Sentinel = object()






# #######################################################
"""Cache entry clases as nodes to be linked in a list ordered by the last time the entry was used.

"""
    


class MDDLinked_Element:
    """Abstract cache entry class. Right now just negates all predicates asserted for subtypes.
    
    """
    security = ClassSecurityInfo()
   
    def __init__( self):
        
        pass
    
        
        
    security.declarePublic( 'fIsForElement')        
    def fIsForElement( self):
        return False
    
    security.declarePublic( 'fIsSentinel')        
    def fIsSentinel(self, ):
        return False
        
    security.declarePublic( 'fIsSentinel_First')        
    def fIsSentinel_First(self, ):
        return False
          
    security.declarePublic( 'fIsSentinel_Last')        
    def fIsSentinel_Last(self, ):
        return False
          
        
    
    
class MDDLinked_WithPrevious( MDDLinked_Element):
    """Abstract cache entry class half-able to participate in the linked list, contributing the capability to relate to a previous cache entry.
    
    """
    security = ClassSecurityInfo()
    
    def __init__( self):
        
        MDDLinked_Element.__init__( self)
        
        self.vPrevious    = None
        

        
    security.declarePublic( 'fListDump_Previous')        
    def fListDump_Previous(self,):
        unStream = StringIO()
        
        self.pListDump_Previous_into( unStream)
        unString = unStream.getvalue()
        
        return unString
    
    
    
    

    security.declarePublic( 'pListDump_Previous_into')        
    def pListDump_Previous_into(self, theStream=None):
        
        if theStream == None:
            return self

        theStream.write( "[ ")
        
        if self.fIsSentinel():
            if self.fIsSentinel_First(): 
                theStream.write( "'Old', ")
             
            elif self.fIsSentinel_Last(): 
                theStream.write( "'New', ")  
        else:
            theStream.write( " , '%s'" % self.vUniqueId)

             
        
        unAlreadyVisited = set()
        unNumIterations  = 0
        
        unCurrent = self.vPrevious
        
        while unCurrent and ( unNumIterations < 10000) :
            
            if ( unCurrent in unAlreadyVisited):
                theStream.write( " , '... ... ...' ]")
                break
            
            unAlreadyVisited.add( unCurrent)
            unNumIterations += 1

            if unCurrent.fIsSentinel():
                
                if unCurrent.fIsSentinel_First(): 
                    theStream.write( " , 'Old' ]")
                
                elif unCurrent.fIsSentinel_Last(): 
                    theStream.write( ", '!!!New!!!'")  
                
                else:
                    theStream.write( ", '???Sentinel???'")
                
                break

            theStream.write( " , '%s'" % unCurrent.vUniqueId)
            unCurrent = unCurrent.vPrevious
    
        return self
    
        
    
            
        
    
class MDDLinked_WithNext( MDDLinked_Element):
    """Abstract cache entry class half-able to participate in the linked list, contributing the capability to relate to a next cache entry.
    
    """
    security = ClassSecurityInfo()

    def __init__( self):
        
        MDDLinked_Element.__init__( self)
        
        self.vNext    = None
        
        
        
        
        
        
    security.declarePublic( 'fListDump_Next')        
    def fListDump_Next(self,):
        unStream = StringIO()
        
        self.pListDump_Next_into( unStream)
        unString = unStream.getvalue()
        
        return unString
    
    
    
    
    

    security.declarePublic( 'pListDump_Next_into')        
    def pListDump_Next_into(self, theStream=None):
        
        if theStream == None:
            return self

        theStream.write( "[ ")
        
        if self.fIsSentinel():
            if self.fIsSentinel_First(): 
                theStream.write( "'Old', ")
             
            elif self.fIsSentinel_Last(): 
                theStream.write( "'New', ")  
        else:
            theStream.write( " , '%s'" % self.vUniqueId)
            
        unAlreadyVisited = set()
        unNumIterations  = 0

        unCurrent = self.vNext
        
        while unCurrent and ( unNumIterations < 10000) :
            
            if ( unCurrent in unAlreadyVisited):
                theStream.write( " , '...' ]")
                break
            
            unAlreadyVisited.add( unCurrent)
            unNumIterations += 1
            

            if unCurrent.fIsSentinel():
                
                if unCurrent.fIsSentinel_Last: 
                    theStream.write( " , 'New' ]")
                
                elif unCurrent.fIsSentinel_First()(): 
                    theStream.write( " , '!!!Old!!!'")  
                
                else:
                    theStream.write( " , '???Sentinel???'")
                
                break

            theStream.write( " , '%s'" % unCurrent.vUniqueId)
            unCurrent = unCurrent.vNext
    
        return self   
        
    
    
    
    
    
    
    
    
    
class MDDLinked_WithPreviousAndNext( MDDLinked_WithPrevious, MDDLinked_WithNext):
    """Abstract cache entry class fully able to participate in the linked list, integrating the capabilities to relate to both previous and next cache entries.
    
    """
    security = ClassSecurityInfo()
    
    def __init__( self):
        
        MDDLinked_WithPrevious.__init__( self)
        MDDLinked_WithNext.__init__( self)
        

        

        
        
        
        

class MDDLinked_ListSentinel:
    """Abstract cache entry class able to participate in the linked list with the special responsiblity of sitting at one extreme of the list, and polimorphically simplify the traversal, linking and unlinking algoritms.
    
    """
    security = ClassSecurityInfo()

    
    def __init__(self, ):
        
        pass

    
    
    security.declarePublic( 'fIsSentinel')        
    def fIsSentinel(self, ):
        return True
        
      
    
    
    
    
        

class MDDLinked_ListSentinel_First( MDDLinked_ListSentinel, MDDLinked_WithNext):
    """Abstract cache entry class able to participate in the linked list with the special responsiblity of sitting at the beginning of the list, and polimorphically simplify the traversal, linking and unlinking algoritms.
    
    """
    security = ClassSecurityInfo()

        
    def __init__( self, ):
        
        MDDLinked_ListSentinel.__init__(  self)
        MDDLinked_WithNext.__init__( self)

        
         
    security.declarePublic( 'pLink')        
    def pLink( self, theNode):
        """TheNode must not be linked anywhere in the list. Use Unlink first to move.
        
        """
        theNode.vPrevious    = self
        theNode.vNext        = self.vNext
        
        self.vNext.vPrevious = theNode
        self.vNext           = theNode
        
        return self
    
   
    
    
    
    
    security.declarePublic( 'fIsSentinel_First')        
    def fIsSentinel_First(self, ):
        return True
          

    
    
        
        
class MDDLinked_ListSentinel_Last( MDDLinked_ListSentinel, MDDLinked_WithPrevious):
    """New Entries are linked before this: Abstract cache entry class able to participate in the linked list with the special responsiblity of sitting at the end of the list, and polimorphically simplify the traversal, linking and unlinking algoritms.
    
    """

    security = ClassSecurityInfo()
    
    def __init__( self, theOldSentinel):
        
        MDDLinked_ListSentinel.__init__( self)
        MDDLinked_WithPrevious.__init__( self)

        self.vPrevious       = theOldSentinel
        theOldSentinel.vNext = self
         
 

    
    
    
    security.declarePublic( 'pLink')        
    def pLink( self, theNode):
        """TheNode must not be linked anywhere in the list. Use Unlink first to move.
        
        """
        theNode.vNext        = self
        theNode.vPrevious    = self.vPrevious
        
        self.vPrevious.vNext = theNode
        self.vPrevious       = theNode
        
        return self
    
       
    
    
    
    security.declarePublic( 'fIsSentinel_Last')        
    def fIsSentinel_Last(self, ):
        return True
          
              
    
    
    
    
    
    
    
class MDDLinkedNode( MDDLinked_WithPreviousAndNext):
    """"Cache entry class incorporating the list nodes facility above, and the cache entry specific features like an unique id. The unique id is not used in any algorithm, but is set upon cache entry instantiation to facilitate the identification of individual cache entries in quality assurance procedures.
    
    """
    security = ClassSecurityInfo()
        
    def __init__( self, theUniqueId=None, thePropertiesDict={},):
       
        MDDLinked_WithPreviousAndNext.__init__( self)

        self.vUniqueId  = theUniqueId

   
        
        
    
    security.declarePublic( 'pUnLink')        
    def pUnLink( self, ):

        if  self.vPrevious:
            self.vPrevious.vNext = self.vNext
            
        if self.vNext:
            self.vNext.vPrevious = self.vPrevious
        
        self.vPrevious       = None
        self.vNext           = None
        
        return self
        

    
    
    
    security.declarePublic( 'pBeGone')        
    def pBeGone( self, ):
        self.vUniqueId       = None
        self.vPrevious       = None
        self.vNext           = None
        return self
    
    
    
    
    
    

class MDDLinkedNodeWithProperties( MDDLinkedNode):
    """"Cache entry class incorporating the list nodes facility above, and the cache entry specific features like an unique id. The unique id is not used in any algorithm, but is set upon cache entry instantiation to facilitate the identification of individual cache entries in quality assurance procedures.
    
    """
    security = ClassSecurityInfo()
    
    def __init__( self, 
        theUniqueId     =None,
        theProperties   =None):
        
        MDDLinkedNode.__init__( self, theUniqueId=theUniqueId)
        
        self.vProperties       = theProperties
        

        
          
        
    
            
    security.declarePublic( 'fGP')        
    def fGP( self, thePropertyName, theDefault=None):
        
        if not thePropertyName:
            return theDefault
        
        unValue = self.vProperties.get( thePropertyName, _cPropertyAccess_KeyNotFound_Sentinel)
        if unValue == _cPropertyAccess_KeyNotFound_Sentinel:
            return theDefault
        
        return unValue
    
    
    

    
    
    security.declarePublic( 'pSP')        
    def pSP( self, thePropertyName, thePropertyValue):
        
        if not thePropertyName:
            return self
        
        self.vProperties[ thePropertyName] = thePropertyValue
        
        return self
    
    
            
       
 

    
    
    
class MDDLinkedList:
    
    def __init__(self,):
        
        self.vFirst = MDDLinked_ListSentinel_First()
        self.vLast  = MDDLinked_ListSentinel_Last( self.vFirst)
        
        
    security = ClassSecurityInfo()
    
        
    security.declarePublic( 'fSentinel_First')        
    def fSentinel_First(self,):
       
        return self.vFirst
    
    
   
    security.declarePublic( 'fNode_First')        
    def fNode_First(self, ):
        if not self.vFirst:
            return None
        return self.vFirst.vNext
    
       
    security.declarePublic( 'fSentinel_Last')        
    def fSentinel_Last(self,):
       
        return self.vLast
    
    
   
    security.declarePublic( 'fNode_Last')        
    def fNode_Last(self, ):
        if not self.vLast:
            return None
        return self.vLast.vPrevious
    
    
    
    security.declarePublic( 'fNewNode_First')        
    def fNewNode_First(self, theUniqueId=None):
        if self.vFirst == None:
            return None
        
        aNewNode = MDDLinkedNode( theUniqueId=theUniqueId)
        
        self.vFirst.pLink( aNewNode)
        
        return aNewNode
    
    
            
    security.declarePublic( 'fNewNode_Last')        
    def fNewNode_Last(self, theUniqueId=None):
        if self.vLast == None:
            return None
        
        aNewNode = MDDLinkedNode( theUniqueId=theUniqueId)
        
        self.vLast.pLink( aNewNode)
        
        return aNewNode
    
    

    
    security.declarePublic( 'fNewNodeWithProperties_First')        
    def fNewNodeWithProperties_First(self, theUniqueId=None, theProperties=None):
        if self.vFirst == None:
            return None
        
        aNewNode = MDDLinkedNodeWithProperties( theUniqueId=theUniqueId, theProperties=theProperties)
        
        self.vFirst.pLink( aNewNode)
        
        return aNewNode
    
    
            
    security.declarePublic( 'fNewNodeWithProperties_Last')        
    def fNewNodeWithProperties_Last(self, theUniqueId=None, theProperties=None):
        if self.vLast == None:
            return None
        
        aNewNode = MDDLinkedNodeWithProperties( theUniqueId=theUniqueId, theProperties=theProperties)
        
        self.vLast.pLink( aNewNode)
        
        return aNewNode
    
            





            

  
   
    
   

                
            

            
            
