# -*- coding: utf-8 -*-
#
# File: MDDTool_Dates.py
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

import os
import sys
import traceback
import logging


# Zope
from OFS import SimpleItem
from OFS.PropertyManager import PropertyManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from AccessControl import ClassSecurityInfo

from AccessControl.Permissions                 import access_contents_information   as perm_AccessContentsInformation

import time

from DateTime import DateTime




from Products.CMFCore                    import permissions
from Products.CMFCore.utils              import getToolByName, UniqueObject
from Products.CMFCore.ActionProviderBase import ActionProviderBase




from Acquisition  import aq_inner, aq_parent,aq_get









# #######################################################
# #######################################################









class MDDTool_Dates:
    """Subject Area Facade class exposing services layer to the presentation layer, implemented directly here as not considered worth to create role class instances and delegate to them. 
    
    """
    
    
    security = ClassSecurityInfo()

    

    

   
    # ####################################################
    """Methods to limit the amount of time available for users from the last system response to their next request, usually when about to launch a modification or a long-lived process.
    
    """


    security.declareProtected( permissions.View, 'fSecondsToReviewAndDelete')
    def fSecondsToReviewAndDelete(self, theContextualObject,):

        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return 30 * 60
        return aModelDDvlPloneToolConfiguration.fSecondsToReviewAndDelete( self, theContextualObject,)

        
    
    


    security.declareProtected( permissions.View, 'fSecondsToReviewAndUnlink')
    def fSecondsToReviewAndUnlink(self, theContextualObject,):

        aModelDDvlPloneToolConfiguration = self.fModelDDvlPloneConfiguration()
        if not aModelDDvlPloneToolConfiguration:
            return 30 * 60
        return aModelDDvlPloneToolConfiguration.fSecondsToReviewAndUnlink( self, theContextualObject,)

        

    
     
        
  

    
    # #######################################################
    """Time utilities not worth to delegate on specific tool role classes.
    
    """
    
  
    
    

    # #######################################################
    """Time now.
    
    """
        
    security.declarePublic( 'fDateTimeNowString')
    def fDateTimeNowString(self):   
        
        return self.fDateTimeToString( self.fDateTimeNow())
    
        
    
    security.declarePublic( 'fDateTimeNowTextual')
    def fDateTimeNowTextual(self):   
        return self.fDateToStoreString( self.fDateTimeNow())


    
    


    security.declarePublic( 'fDateTimeNow')
    def fDateTimeNow(self, ):   
        return DateTime()    
    
    
    
    security.declareProtected( permissions.View, 'fSecondsNow')
    def fSecondsNow(self, ):   
    
        return int( time.time())
    
        
    
    security.declarePublic( 'fMillisecondsNow')
    def fMillisecondsNow(self, ):   
        """Time accessor to minimize instantiation of DateTime while profiling.
       
        """
   
        return int( time.time() * 1000)
    
        
    
    
    

    # #######################################################
    """Time and string conversions.
    
    """
            
    
    security.declarePublic( 'fDateTimeFromMilliseconds')
    def fDateTimeFromMilliseconds(self, theMilliseconds):   
        return DateTime( float( theMilliseconds / 1000))
    
   
    security.declarePublic( 'fDateTimeFromMillisecondsTextual')
    def fDateTimeFromMillisecondsTextual(self, theMilliseconds): 
        return self.fDateToStoreString( self.fDateTimeFromMilliseconds( theMilliseconds))
    
    
    security.declarePublic( 'fMillisecondsToDateTime')
    def fMillisecondsToDateTime(self, theMilliseconds):
        
        if not theMilliseconds:
            return None
        
        if isinstance( theMilliseconds, DateTime):
            return theMilliseconds
        
        unDateTime = None
        try:
            unDateTime = DateTime( theMilliseconds / 1000)
        except:
            None
            
        return unDateTime
    
    
    
    
    security.declarePublic( 'fDateTimeToString')
    def fDateTimeToString(self, theDateTime):  
        if not theDateTime:
            return ''
        return str( theDateTime)
    
    
    
    
    
      
    
   
    # #################################################
    """Handling of Dates as strings to avoid catalog schema overhead
    Using ISO format AAAA-MM-DD HH:MM:SS '2009-03-21 01:36:00'
    No time zone is stored. 
    It is encoded as the time in the server zone  (i.e. Valencia: Madrid Spain GMT+1)
    
    """
    
    
    security.declarePublic( 'fStoreStringToDate')
    def fStoreStringToDate( self, theString):
        if not theString:
            return None
        
        unDate = None
        try:
            unDate = DateTime( theString)   
        except:
            None
        
        return unDate
    
    
    
    security.declarePublic( 'fDateToStoreString')
    def fDateToStoreString( self, theDate):
        if not theDate:
            return None
        #%04d-%02d-%02d %02d:%02d:%02d YMDHMS
        unString = theDate.ISO()
        return unString
    
    

  


    
   
    # #################################################
    """Time delta methods.
    
    """    
    
    
    security.declareProtected( permissions.View, 'fDateTimeAfterSeconds')
    def fDateTimeAfterSeconds(self, theDateTime, theSeconds):
    
        if not theDateTime:
            return None
    
        if not theSeconds:
            return theDateTime
        
        unaDateTimeAfter = DateTime( ( theDateTime.millis() / 1000) + int( theSeconds))
            
        return unaDateTimeAfter
        
    
    
    
    
    
    
    

    # #################################################
    """Sleep Time methods.
    
    """    
    
        
    

    security.declarePrivate( 'pSleepMilliseconds')
    def pSleepMilliseconds( self, theMilliseconds):
        if not cTRAYieldProcessorEnabled:
            return self
        
        if not theMilliseconds:
            return self
        
        unosSecondsToSleep = float( theMilliseconds) / 1000
        self.pSleepSeconds( unosSecondsToSleep)
        
        return self
    

        

    security.declarePrivate('pSleepSeconds')
    def pSleepSeconds( self, theSeconds):
        if not cTRAYieldProcessorEnabled:
            return self
        
        if not theSeconds:
            return self
        
        unosSecondsToSleep = float( theSeconds) 
        time.sleep( unosSecondsToSleep )
        
        return self
        
    
        
