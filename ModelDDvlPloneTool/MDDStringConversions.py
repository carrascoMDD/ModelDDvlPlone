# -*- coding: utf-8 -*-
#
# File: MDDStringConversions.py
#
# Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
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





# #######################################################
# #######################################################
    
# #############################################################
"""Utility methods to format rendered statistics values.

"""

    
def fStrGrp( theInteger):
    """Format a number with comma thousands separator.
    
    """
    
    anInteger = abs( theInteger)
        
    aString = str( anInteger)

    someFragments = [ ]

    while aString:
        aFragment = aString[-3:]
        if aFragment:
            someFragments.append( aFragment)
            aString = aString[ :-3]
        
    someReversedFragments = someFragments.reverse()
    aGroupedString = '.'.join( someFragments)

    if theInteger < 0:
        aGroupedString = '-%s' % aGroupedString
        
    return aGroupedString

        
    
    
    
    
    
    
    
    
    

# #############################################################
"""Utility methods to format a number of seconds into an expresion in higher magnitudes.

"""

def fStrSeconds( theSeconds):
    aRemainder = theSeconds % 60
    if not aRemainder:
        return ''
    return '%s sec' % str( aRemainder)


def fStrMinutes( theSeconds, theIncludeIfZero=False):
    aRemainder = theSeconds % ( 60 * 60)
    if not aRemainder:
        return ''
    aThisMagnitude = int( aRemainder / 60)
    if not aThisMagnitude:
        if theIncludeIfZero:
            return '0 mn %s' % fStrSeconds( theSeconds)
        else:
            return fStrSeconds( theSeconds)
    else:
        return '%d mn %s' % ( aThisMagnitude, fStrSeconds( theSeconds))
    
    
def fStrHours( theSeconds, theIncludeIfZero=False):
    aRemainder = theSeconds % ( 60 * 60 * 24)
    if not aRemainder:
        return ''
    aThisMagnitude = int( aRemainder / ( 60 * 60))
    if not aThisMagnitude:
        if theIncludeIfZero:
            return '0 hr %s' % fStrMinutes( theSeconds)
        else:
            return fStrMinutes( theSeconds)
    else:
        return '%d hr %s' % ( aThisMagnitude, fStrMinutes( theSeconds, True))
    
    
    
def fStrDays( theSeconds, theIncludeIfZero=False):
    aRemainder = theSeconds % ( 60 * 60 * 24 * 7)
    if not aRemainder:
        return ''
    aThisMagnitude = int( aRemainder / ( 60 * 60 * 24))
    if not aThisMagnitude:
        if theIncludeIfZero:
            return '0 d %s' % fStrHours( theSeconds)
        else:
            return fStrHours( theSeconds)
    else:
        return '%d d %s' % ( aThisMagnitude, fStrHours( theSeconds, True))
    
def fStrWeeks( theSeconds, theIncludeIfZero=False):
    aRemainder = theSeconds % ( 60 * 60 * 24 * 30)
    if not aRemainder:
        return ''
    aThisMagnitude = int( aRemainder / ( 60 * 60 * 24 * 7))
    if not aThisMagnitude:
        if theIncludeIfZero:
            return '0 w %s' % fStrDays( theSeconds)
        else:
            return fStrDays( theSeconds)
    else:
        return '%d w %s' % ( aThisMagnitude, fStrDays( theSeconds, True))
    
    
      
def fStrMonths( theSeconds, theIncludeIfZero=False):
    aRemainder = theSeconds % ( 60 * 60 * 24 * 30 * 12)
    if not aRemainder:
        return ''
    aThisMagnitude = int( aRemainder / ( 60 * 60 * 24 * 30))
    if not aThisMagnitude:
        if theIncludeIfZero:
            return '0 m %s' % fStrWeeks( theSeconds)
        else:
            return fStrWeeks( theSeconds)
    else:
        return '%d m %s' % ( aThisMagnitude, fStrWeeks( theSeconds, True))
    
    
def fStrYears( theSeconds, theIncludeIfZero=False):
    aRemainder = theSeconds # This is the last: no unit over years % ( 60 * 60 * 24 * 30 * 12)
    if not aRemainder:
        return ''
    aThisMagnitude = int( aRemainder / ( 60 * 60 * 24 * 30 * 12))
    if not aThisMagnitude:
        if theIncludeIfZero:
            return '0 y %s' % fStrMonths( theSeconds)
        else:
            return fStrMonths( theSeconds)
    else:
        return '%d y %s' % ( aThisMagnitude, fStrMonths( theSeconds, True))
    
    
def fStrTime( theSeconds):
    return fStrYears( theSeconds)
          
            
     
# #######################################################
# #######################################################



            
            

            
            
