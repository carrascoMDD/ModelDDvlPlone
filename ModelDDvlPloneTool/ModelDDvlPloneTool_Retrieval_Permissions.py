# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Retrieval_Permissions.py
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

from Products.CMFCore       import permissions
from Products.CMFCore.utils import getToolByName


from Acquisition  import aq_inner, aq_parent




class ModelDDvlPloneTool_Retrieval_Permissions:
    """
    """
    security = ClassSecurityInfo()
    
    
    
    security.declarePrivate( 'fCreateCheckedPermissionsCache')
    def fCreateCheckedPermissionsCache( self):
        return { }
    
       
    security.declarePrivate( 'fCreateRolesCache')
    def fCreateRolesCache( self):
        return { }
    
     
    
    

    security.declarePrivate( 'fCheckElementPermission')
    def fCheckElementPermission(self, theObject, thePermissionsToCheck, theCheckedPermissionsCache ):
        if ( theObject == None):
            return False
        
        if not thePermissionsToCheck:
            return True
        
        unaObjectKey = None
        try:
            unaObjectKey = theObject.UID()
        except:
            None
        
        unCachedPermissions = None
        
        if not ( unaObjectKey == None):
            if theCheckedPermissionsCache:
                if theCheckedPermissionsCache.has_key( unaObjectKey):
                    unCachedPermissions = theCheckedPermissionsCache.get( unaObjectKey, None)
                if unCachedPermissions == None:
                    unCachedPermissions = {  }
                    theCheckedPermissionsCache[ unaObjectKey] = unCachedPermissions
        
        aPortalMembershipTool = None
                     
        for aPermission in thePermissionsToCheck:
            if unCachedPermissions and unCachedPermissions.has_key( aPermission):
                aPermitted = unCachedPermissions.get( aPermission, False)
            else:

                if not aPortalMembershipTool:
                    aPortalTool           = getToolByName( theObject,   'portal_url').getPortalObject()
                    if not aPortalTool:
                        return False
                    aPortalMembershipTool = getToolByName( aPortalTool, 'portal_membership')
                    if not aPortalMembershipTool:
                        return False
                        
                aPermitted = aPortalMembershipTool.checkPermission( aPermission, theObject)
                if not( unCachedPermissions == None):
                    unCachedPermissions[ aPermission] = aPermitted
            if not aPermitted:
                return False
            
        return True
    
    

    
    security.declarePrivate( 'fCheckTypeReadPermission')
    def fCheckTypeReadPermission(self, theObject,  thePermissionsToCheck=[], theCheckedPermissionsCache=[]):
        if ( theObject == None):
            return False

        unasPermissionsToCheck = thePermissionsToCheck[:]

        aTypePermission = None
        try:
            aTypePermission = theObject.read_permission
        except:
            None            
        if aTypePermission and not ( aTypePermission in unasPermissionsToCheck):
            unasPermissionsToCheck.append( aTypePermission)
            
        return self.fCheckElementPermission( theObject, unasPermissionsToCheck, theCheckedPermissionsCache)
    
    
    
    security.declarePrivate( 'fCheckTypeWritePermission')
    def fCheckTypeWritePermission(self, theObject, thePermissionsToCheck=[], theCheckedPermissionsCache=[]):
        if ( theObject == None):
            return False

        unasPermissionsToCheck = thePermissionsToCheck[:]

        aTypePermission = None
        try:
            aTypePermission = theObject.write_permission
        except:
            None            
        if aTypePermission and not ( aTypePermission in unasPermissionsToCheck):
            unasPermissionsToCheck.append( aTypePermission)
            
        return self.fCheckElementPermission( theObject, unasPermissionsToCheck, theCheckedPermissionsCache)
   
    
    
  
        
    security.declarePrivate( 'fCheckFieldReadPermission')
    def fCheckFieldReadPermission(self, theObject, theFieldName, thePermissionsToCheck=[], theCheckedPermissionsCache=[]):
        if ( theObject == None) or not theFieldName:
            return False

        unasPermissionsToCheck = thePermissionsToCheck[:]
        
        unSchema = theObject.schema
        if not unSchema.has_key( theFieldName):
            return False
                        
        unField             = unSchema[ theFieldName]
        if not unField:
            return False
            
        aFieldPermission = None
        try:
            aFieldPermission = unField.read_permission
        except:
            None            
        if aFieldPermission and not ( aFieldPermission in unasPermissionsToCheck):
            unasPermissionsToCheck.append( aFieldPermission)
            
        return self.fCheckElementPermission( theObject, unasPermissionsToCheck, theCheckedPermissionsCache, )
           
        

    
    security.declarePrivate( 'fCheckFieldWritePermission')
    def fCheckFieldWritePermission(self, theObject, theFieldName, thePermissionsToCheck=[], theCheckedPermissionsCache=[]):
        if ( theObject == None) or not theFieldName:
            return False
        
        unasPermissionsToCheck = thePermissionsToCheck[:]

        unSchema = theObject.schema
        if not unSchema.has_key( theFieldName):
            return False
                        
        unField             = unSchema[ theFieldName]
        if not unField:
            return False
            
        aFieldPermission = None
        try:
            aFieldPermission = unField.write_permission
        except:
            None            
            
        if aFieldPermission and not ( aFieldPermission in unasPermissionsToCheck):
            unasPermissionsToCheck.append( aFieldPermission)
             
        return self.fCheckElementPermission( theObject, unasPermissionsToCheck, theCheckedPermissionsCache, )
           

    
    
    
    
    

 

    # #############################################################
    """User and Role access methods.
    
    """

        
        
    security.declarePublic( 'fRoleQuery_IsAnyRol')
    def fRoleQuery_IsAnyRol( self, theRolesUsuario, theElement=None):
        return len( self.fWhichRoles( theRolesUsuario, theElement)) > 0
  
    
    
    

    
    security.declarePublic( 'fIsRoles')
    def fWhichRoles( self, theRolesUsuario, theElement):
        if not theRolesUsuario:
            return set()
        
        if theElement == None:
            return set()
        
        unosRolesUsuario = theRolesUsuario
        if not ( unosRolesUsuario.__class__.__name__ in [ 'list', 'tuple', ]):
            unosRolesUsuario = [ unosRolesUsuario,]
            
        todosRolesPoseidos = set( self.fGetRequestingUserRoles( theElement))
        
        unosRoles = set( unosRolesUsuario).intersection(  todosRolesPoseidos)
        
        return unosRoles
    
              
              


    security.declarePublic( 'fGetRequestingUserRoles')
    def fGetRequestingUserRoles(self, theElement):
        if theElement == None:
            return []
        
        unUser = self.fGetRequestingUserObject( theElement)
        if not unUser:
            return []
        
        unosRoles = self.fGetRolesForUserObject( unUser, theElement)
        return unosRoles
    

    
    security.declarePrivate( 'fGetRequestingUserObject')
    def fGetRequestingUserObject(self, theContextualObject):
        unaRequest = theContextualObject.REQUEST
        if not unaRequest:
            return None
        
        unUser = unaRequest.get("AUTHENTICATED_USER", None)
        return unUser

    
    
    security.declarePrivate( 'fGetRolesForUserObject')
    def fGetRolesForUserObject(self, theUserObject, theElement):
        if theElement == None:
            return set()
        unosRoles = theUserObject.getRolesInContext( theElement)
        if not unosRoles:
            return set()
        return set( unosRoles)
    


    
        
    security.declarePublic( 'fGetMemberId')
    def fGetMemberId(self, theContextualObject ):
        """Connected user Membership 
        
        """
        if theContextualObject == None:
            return ''
        
        aMembershipTool = getToolByName( theContextualObject, 'portal_membership', None)
        if not aMembershipTool:
            return ''
        
        unMember = aMembershipTool.getAuthenticatedMember()   

        if not unMember:
            return ''
        
        if unMember.getUserName() == 'Anonymous User':
            unMemberId = unMember.getUserName()
        else:
            unMemberId = unMember.getMemberId()   
            
        return unMemberId
        
    
    
        
    
    

        