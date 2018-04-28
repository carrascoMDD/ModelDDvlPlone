import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from App.Common import package_home

from Products.CMFTestCase import CMFTestCase
from Products.Relations import config

import common
common.installProducts()
CMFTestCase.setupCMFSite()


class TestXMLImportExport(CMFTestCase.CMFTestCase):

    def afterSetUp(self):
        common.installWithinPortal(self, self.portal)

    def testXMLImport(self):
        self.loginAsPortalOwner()
        xmlpath=os.path.join(
            package_home(config.GLOBALS), 'tests', 'relations_sample.xml')
        f=open(xmlpath)
        xml=f.read()
        f.close()
        
        tool=self.portal.relations_library
        tool.importXML(xml)
        ruleset=tool.getRuleset('document_files')
        
        #export it
        xml=tool.exportXML()

        #now reimport the junk again
        tool.manage_delObjects(tool.objectIds())
        tool.importXML(xml)

        # Make sure the imported ruleset contains the same set of components
        tool.getRuleset('document_files').objectIds() == ruleset.objectIds()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestXMLImportExport))
    return suite

if __name__ == '__main__':
    framework()
