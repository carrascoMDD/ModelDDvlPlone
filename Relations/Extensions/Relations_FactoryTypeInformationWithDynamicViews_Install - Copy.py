from StringIO import StringIO

from Products.Archetypes.public import listTypes
from Products.Archetypes.utils import shasattr
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName

from Products.Relations.config import *
import Products.Relations.ruleset as ruleset
import Products.Relations.Extensions.utils as utils

def install_tools(self, out):
    if shasattr(self, RELATIONS_LIBRARY):
        print >> out, "%r already existed." % RELATIONS_LIBRARY
        return
    pt = getToolByName(self, 'portal_types')
    pt.constructContent('Relations Library', self, RELATIONS_LIBRARY)
    library = getattr(self, RELATIONS_LIBRARY)
    t = pt.getTypeInfo('Relations Library').Title()
    library.setTitle(t)

    # hide tool inside navigation
    portal_props = getToolByName(self, 'portal_properties', None)
    if portal_props is not None:
        navtree_props = getattr(portal_props, 'navtree_properties', None)
        if navtree_props is not None:
            if not RELATIONS_LIBRARY in navtree_props.idsNotToList:
                navtree_props.manage_changeProperties(
                    idsNotToList = list(navtree_props.idsNotToList) + \
                                   [RELATIONS_LIBRARY] 
                )

    # register as ActionProvider
    at = getToolByName(self, 'portal_actions')
    at.addActionProvider(RELATIONS_LIBRARY)

    print >> out, "%s installed." % t

def install_dependencies(self, out):
    DEPS = 'Archetypes',
    qi = self.portal_quickinstaller
    qi.installProducts(DEPS)
    print >> out, "Installed dependencies: %s" % DEPS

def install(self):
    out = StringIO()

    install_dependencies(self, out)
    
    # ########################################
    """ACV OJO 20101027 To fix error when installing product through the test machinery.
    
    """
    
    someTypes = listTypes(PROJECTNAME)
    for aType in someTypes:
        aKlass = aType.get( 'klass', None)
        if not ( aKlass == None):
            aFTIMetaType = getattr( aKlass, '_at_fti_meta_type', None)
            if not ( aFTIMetaType == 'Factory-based Type Information with dynamic views'):
                aKlass._at_fti_meta_type = 'Factory-based Type Information with dynamic views'
                
    """ACV OJO 20101027 To fix error when installing product through the test machinery.
    
    """
    # ########################################
    
    installTypes(self, out, listTypes(PROJECTNAME), PROJECTNAME)
    install_subskin(self, out, GLOBALS)
    install_tools(self, out)
    print >> out, utils.installConfiglets(self, CONFIGLETS)

    print >> out, "Successfully installed %s." % PROJECTNAME
    return out.getvalue()

def uninstall(self):
    out = StringIO()
    # XXX: Why does QuickInstaller think we own Archetypes' portal objects?
    at = getattr(self.portal_quickinstaller, 'Archetypes')
    NO_REMOVE = [RELATIONS_LIBRARY] + at.portalobjects
    prod = getattr(self.portal_quickinstaller, PROJECTNAME)
    prod.portalobjects = [p for p in prod.portalobjects if p not in NO_REMOVE]
    print >> out, utils.uninstallConfiglets(self, CONFIGLETS)

    print >> out, "Successfully uninstalled %s." % PROJECTNAME
    return out.getvalue()
