import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

package = 'Products.Relations.doc'

from Products.CMFTestCase import CMFTestCase

import common
common.installProducts()
CMFTestCase.setupCMFSite()

from Products.Relations.config import *

class TestOverviewTxt(CMFTestCase.CMFTestCase):

    def afterSetUp(self):
        common.installWithinPortal(self, self.portal)
        self.folder.invokeFactory('SimpleType', 'alfred')
        self.folder.invokeFactory('ComplexType', 'manfred')
        self.ruleset = common.createRuleset(self, 'IsParentOf')
        

def test_suite():
    from unittest import TestSuite
    from Testing.ZopeTestCase.zopedoctest import ZopeDocFileSuite

    return TestSuite((
        ZopeDocFileSuite('Overview.txt',
                         package='Products.Relations.doc',
                         test_class=TestOverviewTxt),
    ))

if __name__ == '__main__':
    framework()

