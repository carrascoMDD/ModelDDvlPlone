Overview

  ModelDDvlPlone and its companion ModelDDvlPloneTool
  provide respectively the skins (visual presentation)
  and logic (retrieve, modify) to manage the creation of 
  complex Archetypes networks, including their linkage
  through relations.
  
  
Dependencies

  ModelDDvlPlone and its companion ModelDDvlPloneTool
  require the installation of the products:
  
  - "Archetypes"
  
  - "Relations"
  
  - "PloneLanguageTool"
  
  Installation will fail if these products are not 
  correctly deployed and available in the Plone instance.
  
  The installer will automatically install the prerequisite
  products, if corretly deployed and available in the Plone instance.
 


Copyright


Copyright (c) 2008,2009,2010 by Model Driven Development sl and Antonio Carrasco Valero
  

Project Home

  - "ModelDD.org":http://www.ModelDD.org 

  
  
Authors

  - "Antonio Carrasco Valero and "Model Driven Development sl  Valencia (Spain)":http://www.ModelDD.org 

  
License

  GNU General Public License (GPL)
 
  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
  02110-1301, USA.
  
  



------------------
Description

The ModelDDvlPlone project is not an application for end-users. ModelDDvlPlone realizes a technical facility in support of other projects, that are applications for end-users, like gvSIG-i18n and gvSIG-business process definition (all by same developer Model Driven Development, sl and Antonio Carrasco Valero).

Framework by MDDsl that animates the Plone products gvSIG-i18n, gvSIG-business process definition (gvSIG-bpd), ModelDDploneMOF, ModelDDploneRDB, ModelDDploneBMM.  Runs on Zope2.9/Plone2.5. Tested on Debian Ubuntu 8 and Windows (TM) XP and Vista.


------------------
Features

Retrieve information from a network of Plone content elements, specified as a traversal over an object oriented model, in a single interaction.
Assert security permissions required on the connected users to access the Plone elements and fields.
Retrieve Plone type and field names, localized (translated when availaible) to the preferred user interface language.
Render the information as a textual view.
Render the information retrieved as a tabular editor.
Allow authorized users to edit ( create/read/update/delete CRUD) Plone elements and fields, as well as re-ordering contained and referenced elements.
Cache of rendered pages, for anonymous users, users with special roles, and specific users.
Support for long-running processes, with the ability to pause, continue and stop running processes, examine intermediate progress, and store final results.


------------------
Future plans

Integrate external sources in the retrieval, render and edit use cases.
Expose the retrieval an edit services with XML content interchange.
