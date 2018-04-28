from Products.CMFTestCase import CMFTestCase
from Products.CMFCore.utils import getToolByName

from Products.Relations.config import *

from Products.Relations.Extensions.Install import install as myInstall

from Products.SiteErrorLog.SiteErrorLog import manage_addErrorLog
from Products.Archetypes.Extensions.Install import install as installAT

# eases setting breakpoints for pdb
import os, sys
sys.path.append('%s/Products' % os.environ['INSTANCE_HOME'])

# make Zope products available to test environment
product_dependencies = ['Archetypes', 'PortalTransforms', 'generator',
                        'validation', 'MimetypesRegistry',
                        'CMFFormController', 'CMFQuickInstallerTool',
                        PROJECTNAME]

def installProducts():
    for product in product_dependencies:
        CMFTestCase.installProduct(product)

def installWithinPortal(testcase, portal):
    testcase.loginAsPortalOwner()
    manage_addErrorLog(portal)
    portal.manage_addProduct['CMFQuickInstallerTool'].manage_addTool(
        'CMF QuickInstaller Tool', None)
    installAT(portal, include_demo=1)
    myInstall(portal)
    testcase.logout()
    testcase.login()

def createObjects(testcase, names):
    """Given a testname and a list of portal types "names", I will create
    in testcase.folder objects that correspond to the given names, with their
    ids set to their type names.

    Returns the list of objects created."""
    value = []

    for t in names:
        testcase.folder.invokeFactory(t, t)
        obj = getattr(testcase.folder, t)
        value.append(obj)

    return value

def createRuleset(testcase, id):
    """Creates a ruleset and registers it. Returns the new ruleset."""
    ttool = getToolByName(testcase.portal, 'portal_types')
    construct = ttool.constructContent
    construct('Ruleset', testcase.folder, id)

    ruleset = getattr(testcase.folder, id)
    library = getToolByName(testcase.portal, RELATIONS_LIBRARY)
    library.registerRuleset(ruleset)

    return ruleset
