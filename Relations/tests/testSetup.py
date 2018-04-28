import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.PloneTestCase import PloneTestCase
import common
common.installProducts()
PloneTestCase.setupPloneSite()


class TestPloneSetup(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        qi = self.portal.portal_quickinstaller
        qi.installProducts(('Relations',))
    
    def testReinstall(self):
        self.loginAsPortalOwner()
        qi = self.portal.portal_quickinstaller
        qi.reinstallProducts(('Relations',))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPloneSetup))
    return suite

if __name__ == '__main__':
    framework()
