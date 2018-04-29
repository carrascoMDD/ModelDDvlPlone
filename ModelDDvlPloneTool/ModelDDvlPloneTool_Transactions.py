# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Transactions.py
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


import sys
import traceback
import logging

import transaction


from time import time


from AccessControl      import ClassSecurityInfo

from StringIO import StringIO



# ##############################################
"""Configuration constants.

"""
cTransactionDescription_MaxLen = 4096





class ModelDDvlPloneTool_Transactions:
    """
    """
    security = ClassSecurityInfo()

   
    

    
    security.declarePrivate('fTransaction_Commit')
    def fTransaction_Commit(self,):
      
        aResult = transaction.commit( ) 
        
        return aResult      
        
        
        
        
    
    security.declarePrivate('fTransaction_Savepoint')
    def fTransaction_Savepoint(self, theOptimistic=True):
      
        aResult = transaction.savepoint( optimistic=theOptimistic) 
        
        return aResult
    
    

    
    security.declarePrivate('fTransaction_Abort')
    def fTransaction_Abort(self,):
      
        aResult = transaction.abort( ) 
        
        return aResult      
        
        
    
    

    security.declarePrivate('fTransaction_Description')
    def fTransaction_Description( self,):
        aTransaction = transaction.get()
        if not aTransaction:
            return ''
        if not( aTransaction.status == 'Active'):
            return ''
        aTransactionDescription = aTransaction.description

        return aTransactionDescription
    
    
                
    
    
    
    security.declarePrivate('fTransaction_AppendNote')
    def fTransaction_CanAppendNote( self,):

        aTransaction = transaction.get()
        if not aTransaction:
            return False
        if not( aTransaction.status == 'Active'):
            return False
        
        aTransactionDescription = aTransaction.description
        aTransactionDescriptionLen = len( aTransactionDescription)
        
        if aTransactionDescriptionLen >= cTransactionDescription_MaxLen:
            return False
               
        return True
                    
    
    
    
    security.declarePrivate('fTransaction_AppendNote')
    def fTransaction_AppendNote( self, theTransactionNote):
        
        if not theTransactionNote:
            return False
        
        unTransactionNote = theTransactionNote
        unTransactionNoteLen = len( theTransactionNote)
        if unTransactionNoteLen > cTransactionDescription_MaxLen:
            unTransactionNote = unTransactionNote[ :cTransactionDescription_MaxLen]
        
        aTransaction = transaction.get()
        if not aTransaction:
            return False
        if not( aTransaction.status == 'Active'):
            return False
        
        aTransactionDescription = aTransaction.description
        aTransactionDescriptionLen = len( aTransactionDescription)
        
        if aTransactionDescriptionLen >= cTransactionDescription_MaxLen:
            return False
        
        if ( aTransactionDescriptionLen + unTransactionNoteLen) > cTransactionDescription_MaxLen:
            unTransactionNote = unTransactionNote[ :cTransactionDescription_MaxLen - ( aTransactionDescriptionLen + unTransactionNoteLen)]
        
        aTransaction.note( unTransactionNote)
        
        return True
            