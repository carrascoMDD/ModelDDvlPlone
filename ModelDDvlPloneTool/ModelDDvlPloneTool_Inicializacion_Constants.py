# -*- coding: utf-8 -*-
#
# File: ModelDDvlPloneTool_Inicializacion_Constants.py
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

from AccessControl import ClassSecurityInfo

##code-section module-header #fill in your manual code here




##/code-section module-header

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


##code-section after-schema #fill in your manual code here





cLazyCreateExternalMethod              = True
cLazyCreateModelDDvlPloneTool          = True
cLazyCreateModelDDvlPloneConfiguration = True




# #############################################################
# External methods to create
#

cExtMethod_MDDCacheDump                          = "MDDCacheDump"
cExtMethod_MDDView_Tabular                       = "MDDView_Tabular"
cExtMethod_MDDLoadModules                        = "MDDLoadModules"
cExtMethod_MDDInformeContenidoZipFile            = "MDDInformeContenidoZipFile"
cExtMethod_MDDDescomprimirContenidoZipFile       = "MDDDescomprimirContenidoZipFile"





cExternalMetodDefinitions = [
    [ cExtMethod_MDDCacheDump,                                # module  
        [ cExtMethod_MDDCacheDump,    ]                  * 3, # function id title name
    ],
    [ 'MDDRenderTabular',                                     # module  
       [ cExtMethod_MDDView_Tabular,  ]                  * 3, # function id title name
    ],    
    [ cExtMethod_MDDLoadModules,                              # module  
        [ cExtMethod_MDDLoadModules,  ]                  * 3, # function id title name
    ],
    [ 'MDDZipFileExpansionUtils',                                # module  
       [ cExtMethod_MDDInformeContenidoZipFile,  ]       * 3, # function id title name
       [ cExtMethod_MDDDescomprimirContenidoZipFile,  ]  * 3, # function id title name
    ],    
]


##/code-section module-footer



