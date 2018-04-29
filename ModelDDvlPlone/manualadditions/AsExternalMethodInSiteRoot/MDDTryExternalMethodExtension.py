# -*- coding: utf-8 -*-
#
# File: MDDTryExternalMethodExtension.py
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




import cgi 



# #######################################################################
""" Utility to escape strings written as HTML.

"""
def fCGIE( theString, quote=1):
    if not theString:
        return theString
    return cgi.escape( theString, quote=quote)
    


     

# #######################################################################
            


    
def MDDTryExternalMethodExtension( theRdCtxt=None):
    
    if not theRdCtxt:
        return None
    
    theRdCtxt.pOS( """
    <p>MDDTryExternalMethodExtension executed.</p>
    """)
    
    return [ True, True,]


    