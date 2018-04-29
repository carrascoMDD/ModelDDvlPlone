# -*- coding: utf-8 -*-
#
# File: ModelDDvlPlone AppConfig.py
#       config.py imports this module,
#       providing the opportunity to extend it
#
#       Used here to add dependencies of the gvSIGtraducciones product
#       to other products.
#
#       The product installer shall intall these before the
#       gvSIGtraducciones product.
#
# Copyright (c) 2008 by Model Driven Development sl and Antonio Carrasco Valero
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

__author__ = """Antonio Carrasco Valero
Model Driven Development sl and Antonio Carrasco Valero
<carrasco@modeldd.org>"""
__docformat__ = 'plaintext'



##code-section config-head #fill in your manual code here
##/code-section config-head

# Dependencies of Products to be installed by quick-installer
# defined originally in config.py
# and overriden  in custom configuration
DEPENDENCIES = [ 'Archetypes', 'PloneLanguageTool', 'Relations',]
