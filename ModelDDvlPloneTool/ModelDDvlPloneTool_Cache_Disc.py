# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Cache_Disc.py
#
# Copyright (c) 2008, 2009, 2010, 2011  by Model Driven Development sl and Antonio Carrasco Valero
#
# GNU General Public License (GPL)
#anElementUIDModulus
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


import cgi 

import sys
import traceback

import logging


from App.config import getConfiguration

from AccessControl import ClassSecurityInfo



from Products.CMFCore import permissions



from ModelDDvlPloneTool_CacheConstants          import *

from MDDStringConversions                       import *




# #######################################################
# #######################################################







class ModelDDvlPloneTool_Cache_Disc:
    """Manager for Caching of rendered templates, in charge of the responsibility to deal with the disc usage by the caching machinery.
    
    """

    # Standard security settings
    security = ClassSecurityInfo()
    
    
       
    
    security.declarePrivate( 'fCacheContainerPath')
    def fCacheContainerPath(self, 
        theModelDDvlPloneTool, 
        theContextualObject,):
        """Return path to contain the cache file, obtained from Zope instance global Zope configuration object.
        
        """
        aContainerPath = getConfiguration().clienthome
        
        return aContainerPath
                
    
    
    
    # ###################################################################
    """Directories associated with specific element.
    
    """
       
    security.declarePrivate( 'fDirectoriesForElement')
    def fDirectoriesForElement(self, theModelDDvlPloneTool, theContextualObject, ):
        """The Disk Cache Directory for an element, for a project, for an element (by it's UID), for the specified view, and for the currently negotiared language.
        
        """
        
        someDirectories = [ ]
                
        if theModelDDvlPloneTool == None:
            return someDirectories

        if not self.fIsCachingActive( theModelDDvlPloneTool, theContextualObject):
            return someDirectories
          
        if theContextualObject == None:
            return someDirectories
        
        
        # ###########################################################
        """Only cache objects that allow caching.
        
        """
        anIsCacheable = False
        try:
            anIsCacheable = theContextualObject.fIsCacheable()
        except:
            None
        if not anIsCacheable:    
            return someDirectories
            
        
        
        
        
        # ###########################################################
        """Gather all information to look up the cache for a matching cached entry with a rendered template.
        
        """
        aProjectName = ''
        try:
            aProjectName = theContextualObject.getNombreProyecto()
        except:
            None
        if not aProjectName:    
            aProjectName = cDefaultNombreProyecto
              
        
        unElementUID = ''
        try:
            unElementUID = theContextualObject.UID()
        except:
            None
        if not unElementUID:
            return someDirectories
        
               
        unRootElementUID = ''
        
        unRootElement = None
        try:
            unRootElement = theContextualObject.getRaiz()
        except:
            None
        if ( unRootElement == None):
            unRootElementUID  = unElementUID
            unRootElementPath = unElementPath
        else:
            try:
                unRootElementUID     = unRootElement.UID()
            except:
                None
            if not unRootElementUID:
                unRootElementUID = unElementUID
                
                        
        someCacheDiskPaths = [ ]
        
        
        # ###################################################################
        """CRITICAL SECTION to access configuration information.
        
        """
        try:
            
            # #################
            """MUTEX LOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pAcquireCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
            # ###########################################################
            """Retrieve within thread safe section, to be used later, the configuration paameters specifying: whether to render a cache hit information collapsible section at the top or bottom of the view, or none at all, whether the disk caching is enabled, and the disk cache files base path.
            
            """
            for aCacheName in [ cCacheName_ForElements, cCacheName_ForUsers, ]:
                
                aCacheDiskEnabled        = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskEnabled)
                
                if aCacheDiskEnabled:
                    aCacheDiskPath       = theModelDDvlPloneTool.fGetCacheConfigParameterValue(  theContextualObject, aCacheName, cCacheConfigPpty_CacheDiskPath)
                    
                    if aCacheDiskPath:
                        someCacheDiskPaths.append( aCacheDiskPath)
                        
        finally:
            # #################
            """MUTEX UNLOCK. 
            
            """
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.pReleaseCacheLock( theModelDDvlPloneTool, theContextualObject,)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            


    
        # ###########################################################
        """Assemble the names of the directories )one per cache: for elements, and for users) holding all disk files with cached HTML for all entries on the element.
            
        """            
                
        for aCacheDiskPath in someCacheDiskPaths:
            aProjectPath           = os.path.join( aCacheDiskPath, aProjectName)
            aRootUIDPath           = os.path.join( aProjectPath, unRootElementUID)
            anElementUIDModulus    = self.fModulusUID( unElementUID, cCacheDisk_UIDModulus)
            aElementUIDModulusPath = os.path.join( aRootUIDPath, anElementUIDModulus)
            aElementUIDPath        = os.path.join( aElementUIDModulusPath, unElementUID)
    
            someDirectories.append(  aElementUIDPath)
        
        return someDirectories
    
    
                
                

    
    security.declarePrivate( '_pAllFilePathsInto')
    def _pAllFilePathsInto(self, theDirectory, theFilesToDelete):
        if not theDirectory:
            return self
        
        if ( theFilesToDelete == None):
            return self
        
                            
        unDirectoryExists = False
        try:
            unDirectoryExists = os.path.exists( theDirectory)
        except:
            None
        if not unDirectoryExists:
            return self
        
        aFilesToDeleteSet = set( theFilesToDelete)
        for unRoot, unosDirectories, unosFileNames in os.walk( theDirectory):
            
            for unFileName in unosFileNames:
                
                unFilePath = os.path.join( unRoot, unFileName)
                
                if not ( unFilePath in aFilesToDeleteSet):
                    
                    theFilesToDelete.append( unFilePath)
                    
                    aFilesToDeleteSet.add( unFilePath)
                
        return self
        
        
        
        
   
    security.declarePrivate( '_pAllFilePathsInto_Filtering')
    def _pAllFilePathsInto_Filtering(self, theDirectory, theSubDirectoryNames, theFilesToDelete):
        if not theDirectory:
            return self
        
        if ( theFilesToDelete == None):
            return self
        
                            
        unDirectoryExists = False
        try:
            unDirectoryExists = os.path.exists( theDirectory)
        except:
            None
        if not unDirectoryExists:
            return self
        
        aFilesToDeleteSet = set( theFilesToDelete)
        for unRoot, unosDirectories, unosFileNames in os.walk( theDirectory):
            
            for unFileName in unosFileNames:
                
                if ( not theSubDirectoryNames) or (  unFileName in theSubDirectoryNames):
                
                    unFilePath = os.path.join( unRoot, unFileName)
                    
                    if not ( unFilePath in aFilesToDeleteSet):
                        
                        theFilesToDelete.append( unFilePath)
                        
                        aFilesToDeleteSet.add( unFilePath)
                
        return self
        
            
    
    
    
    
    
    

            