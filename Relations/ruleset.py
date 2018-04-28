# ###################################################################################
# ACV OJO FIX 2008/04/30
#     fails to load multiple allowedSourceType elements or multiple allowedTargetType elements
# SEE BELOW in ruleset.XMLImportDOM.importDOM() 
#

from xml.dom import minidom

from Acquisition import ImplicitAcquisitionWrapper, aq_parent, aq_inner
from Globals import InitializeClass
import zExceptions
import transaction

from OFS.ObjectManager import BeforeDeleteException
from Products import CMFCore
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore.Expression import Expression
from Products.Archetypes.interfaces.referenceable import IReferenceable
from Products.Archetypes.Referenceable import Referenceable
from Products.Archetypes.ReferenceEngine import Reference
from Products.Archetypes.utils import shasattr, getRelURL
from Products.Archetypes.public import *

from config import *
from Products.Relations import config
import interfaces
import brain
import schema
import utils

class XMLImportExport:
    __implements__ = interfaces.IXMLImportExport,

    schema=Schema((
        StringField('xml',
                    mutator='importXML',
                    accessor='exportXML',
                    default_method='exportXML',
                    widget=TextAreaWidget(rows=20),
                    schemata='xml',
                    mode='w',
                    ))
                  )

    def importXML(self, xmlstring):
        doc=minidom.parseString(xmlstring)
        #extract the main element node
        element=[el for el in doc.childNodes
                 if el.nodeType==doc.ELEMENT_NODE][0]
        return self.importDOM(doc, element)
    
    def importDOM(self, doc, element, root=1):
        if root:
            doc.objectsByUid={}
            doc.references=[]
            
        childnodes = [node for node in element.childNodes
                      if node.nodeType == element.ELEMENT_NODE]
            
        title=element.getAttribute('title') or self.getId()
        self.setTitle(title)
        
        # counter to enable subtransactions on ever X imported rulesets
        counter = 0
            
        for node in childnodes:
            counter += 1
            tagname=node.tagName
            if tagname in self.Schema().keys():
                key=tagname
                ref=self.Schema()[key]
                
                if ref.type!='reference':
                    value=node.firstChild.nodeValue.strip()
                    if value =='None':
                        value=None
                        
                    self.update(**{str(key):value})
                else:
                    doc.references.append(
                        (self, ref, node.getAttribute('uidref').strip()))
                    
            elif tagname+'s' in self.Schema().keys():
                key=tagname+'s'

# ###################################################################################
# ACV OJO FIX 2008/04/30
#
#   Problem:
#       ruleset.XMLImportDOM.importDOM() fails to load multiple allowedSourceType elements or multiple allowedTargetType elements
#
#   Prerequisites:
#       Installed Module: Relations 0.6b 
#
#   When:
#       In a Plone Site, which as already installed Relations 0.6b
#       Installing a new Product which utilizes the Relations functionality
#       by including a relations.xml file
#       with a RuleSetCollection element with a RuleSet element with a TypeConstraint element
#       with multiple allowedSourceType elements or multiple allowedTargetType elements
#
#   Error log:
#       Module Products.CMFQuickInstallerTool.QuickInstallerTool, line 322, in installProduct
#           - __traceback_info__: ('gvSigPPP',)
#       Module Products.ExternalMethod.ExternalMethod, line 225, in __call__
#           - __traceback_info__: ((<PloneSite at /p1>,), {}, (False,))
#       Module D:\dvpt\Plone251\Data\Products\gvSigPPP\Extensions\Install.py, line 88, in install
#       Module Products.Relations.ruleset, line 45, in importXML
#       Module Products.Relations.ruleset, line 110, in importDOM
#       Module Products.Relations.ruleset, line 110, in importDOM
#       Module Products.Relations.ruleset, line 110, in importDOM
#       Module Products.Relations.ruleset, line 80, in importDOM
#       TypeError: can only concatenate tuple (not "list") to tuple
#
#   Sample input:
#		<Ruleset id="Guias_detallan_Reglamento" uid="-64--88-1-33-76a6eb09:1199c527f27:-8000:0000000000000DD0">
#			<TypeConstraint id="type_constraint">
#				<allowedSourceType>
#					Guia
#				</allowedSourceType>
#				<allowedTargetType>
#					Reglamento
#				</allowedTargetType>
#				<allowedTargetType>
#					Procedimento
#				</allowedTargetType>
#				<allowedTargetType>
#					ProcedimentoSimple
#				</allowedTargetType>
#				<allowedTargetType>
#					Norma
#				</allowedTargetType>
#			</TypeConstraint>
#			<InverseImplicator id="inverse_relation">
#				<inverseRuleset uidref="reglamentos_guias"/>
#			</InverseImplicator>
#		</Ruleset>
#
#   Diagnosis:
#       The first allowedSourceType or allowedTargetType is registered in self dictionary as a tuple, not as a list
#       To register additional allowedSourceType or allowedTargetType the concatenation of the new element list
#       with the existing one fails with error TypeError: can only concatenate tuple (not "list") to tuple
#
#   Fix:
#      To convert the node value tuple already existing in the self dictionary, when not empty,
#      to a list that can be concatenated with the just read new element list
#
#   Previous code:
#                self.update(
#                    ** { str(key):
#                         (self.Schema().get(key).get(self) or []) +
#                         [node.firstChild.nodeValue]
#                       }
#                    )                
#
#                log("\n\n!!!ACVOJO!!!  ruleset.importDOM()" )
#                log("!!!ACVOJO!!! key %s >>>" % str( key) )
#                log("!!!ACVOJO!!! self.Schema().get(key).get(self) %s >>>" % str( self.Schema().get(key).get(self)) )
#                log("!!!ACVOJO!!! self.Schema().get(key) %s >>>" % str( self.Schema().get(key)) )
#                log("!!!ACVOJO!!! self.Schema() %s >>>" % str( self.Schema()) )
#                log("!!!ACVOJO!!! [node.firstChild.nodeValue] %s >>>" % str( [node.firstChild.nodeValue]) )
#                log("!!!ACVOJO!!! [node.firstChild] %s >>>" % str( [node.firstChild]) )
#                log("!!!ACVOJO!!! [node] %s >>>" % str( [node]) )
#
                
                if self.Schema().get(key).get(self):
                   unExistingNodeValue=[aV for aV in self.Schema().get(key).get(self)]
                else:
                   unExistingNodeValue=[]

#
#                log("!!!ACVOJO!!! unACVOJOValue %s >>>" % str( unACVOJOValue) )
#
               

                self.update(
                    ** { str(key):
# ACV OJO FIX replaced line         (self.Schema().get(key).get(self) or []) +
                         unExistingNodeValue +                                # ACV OJO FIX replacing line 
                         [node.firstChild.nodeValue]
                       }
                    )                
            else:
                id=node.getAttribute('id')
                uid=node.getAttribute('uid')
                
                typename_=[tagname[0]]
                for c in tagname[1:]:
                    if c.isupper():
                        typename_.append(' '+c)
                    else:
                        typename_.append(c)
                        
                typename=str(''.join(typename_))
                
                #we are in overwrite mode, so we delete the existing subobjects
                if hasattr(self.aq_base,id):
                    self.manage_delObjects([id])
                    
                self.invokeFactory(typename,id)
                obj=getattr(self,id)

                if uid:
                    doc.objectsByUid[uid]=obj

                if hasattr(obj.aq_base,'importDOM'):
                    obj.importDOM(doc, node, root=0)
                    
                    
                #restore the references
                if root:
                    for r in doc.references:
                        target=doc.objectsByUid[r[2]]
                        ssource=r[0]
                        field=r[1]
                        field.set(ssource,target)
                        
            # check for subtransaction
            if counter % IMPORT_TRANSACTION_STEPPING == 0:
                transaction.commit(1)
            
    def exportXML(self):
        doc=minidom.Document()
        
        self.exportDOM(doc,doc)
        return doc.toprettyxml()
    
    def exportDOM(self,doc,dom):
        classNode=doc.createElement(self.portal_type.replace(' ',''))
        classNode.setAttribute('id',self.id)
        classNode.setAttribute('title',self.Title())
        classNode.setAttribute('uid',self.UID())

        fields=[f for f in self.Schema().fields() if f.getName() \
             not in ('id','title','xml') and not f.isMetadata]

        for field in fields:
            if field.type=='lines':
                values=field.get(self)
                for value in values:
                    node=doc.createElement(field.getName()[:-1])
                    textnode=doc.createTextNode(value)
                    node.appendChild(textnode)
                    classNode.appendChild(node)
            elif field.type=='reference':
                node=doc.createElement(field.getName())
                node.setAttribute('uidref',field.getRaw(self))
                classNode.appendChild(node)
            else:
                node=doc.createElement(field.getName())
                textnode=doc.createTextNode(str(field.get(self)))
                node.appendChild(textnode)
                classNode.appendChild(node)
            
        for o in self.objectValues():
            o.exportDOM(doc,classNode)
            
        dom.appendChild(classNode)

class ReferenceLayerManager(Reference):
    """Forwards hooks to ReferenceLayers, see IReferenceLayerProvider."""
    
    def addHook(self, tool, sourceObject=None, targetObject=None):
        self._forEachLayerDo('addHook', self)

    def delHook(self, tool, sourceObject=None, targetObject=None):
        self._forEachLayerDo('delHook', self)

    def beforeTargetDeleteInformSource(self):
        self._forEachLayerDo('beforeTargetDeleteInformSource', self)

    def beforeSourceDeleteInformTarget(self):
        self._forEachLayerDo('beforeSourceDeleteInformTarget', self)

    def getRuleset(self):
        if not getattr(self, '_v_ruleset', None):
            library = getToolByName(self, RELATIONS_LIBRARY)
            self._v_ruleset = library.getRuleset(self.relationship)
        return self._v_ruleset

    def _forEachLayerDo(self, methodName, *args, **kwargs):
        layers = self._getReferenceLayers()
        for l in layers:
            method = getattr(l, methodName, None)
            if callable(method):
                method(*args, **kwargs)

    def _getReferenceLayers(self):
        rs = self.getRuleset()
        providers = rs.getComponents(interfaces.IReferenceLayerProvider)
        return [p.provideReferenceLayer(self) for p in providers]

InitializeClass(ReferenceLayerManager)

class RLMWithBrains(ReferenceLayerManager, brain.ReferenceWithBrains):
    pass

class RuleBase(XMLImportExport):
    __implements__ = interfaces.IRule,

    global_allow = 0 # convenience
    def getRuleset(self): return aq_parent(aq_inner(self))

class DefaultPrimaryImplicator(RuleBase):
    __implements__ = interfaces.IPrimaryImplicator,

    referenceClass = RLMWithBrains

    def __init__(self, ruleset):
        self.ruleset = ruleset
    
    def connect(self, source, target, metadata=None):
        if metadata is None:
            metadata = {}
        
        ref_catalog = getToolByName(self.ruleset, REFERENCE_CATALOG)

        args = (source.UID, target.UID, self.ruleset.getId(),
                self.referenceClass)
        kwargs = metadata
        if config.ALLOW_MULTIPLE_REFS_PER_TRIPLE:
            kwargs['updateReferences'] = False
        
        return ref_catalog.addReference(*args, **kwargs)

    def disconnect(self, reference):
        ref_catalog = getToolByName(self.ruleset, REFERENCE_CATALOG)
        ref_catalog._deleteReference(reference)
        
class Ruleset(utils.AllowedTypesByIface, OrderedBaseFolder, XMLImportExport):
    """See IRuleset."""
    __implements__ = (interfaces.IRuleset,) +\
                     OrderedBaseFolder.__implements__

    schema = schema.RulesetSchema
    portal_type = archetype_name = 'Ruleset'
    global_allow = 0
    content_icon = 'ruleset_icon.gif'
    allowed_interfaces = interfaces.IRule, #used by AllowedTypesByIface

##     def initializeArchetype(self, **kwargs):
##         OrderedBaseFolder.initializeArchetype(self, **kwargs)

    def getComponents(self, interface):
        """Return a list of objects in self that implement the given
        interface."""
        return [obj for obj in self.objectValues()
                if interface.isImplementedBy(obj)]

    def implyOnConnect(self, source, target, chain, metadata=None):
        primaryImplicator = self._getPrimaryImplicator()
        reference = primaryImplicator.connect(source, target, metadata)
        chain.added.append(reference)
        self.addReference(reference, RELATIONSHIP_RULESETTOREF)
        self._forEachDo(interfaces.IImplicator, 'implyOnConnect',
                        reference, chain)

    def implyOnDisconnect(self, reference, chain):
        primaryImplicator = self._getPrimaryImplicator()
        primaryImplicator.disconnect(reference)
        chain.deleted.append(reference)
##         reference = ImplicitAcquisitionWrapper(reference, self)
        self._forEachDo(interfaces.IImplicator, 'implyOnDisconnect',
                        reference, chain)

    def validateConnected(self, reference, chain):
        self._forEachDo(interfaces.IValidator, 'validateConnected',
                        reference, chain)

    def validateDisconnected(self, reference, chain):
        self._forEachDo(interfaces.IValidator, 'validateDisconnected',
                        reference, chain)

    def finalizeOnConnect(self, reference, chain):
        self._forEachDo(interfaces.IFinalizer, 'finalizeOnConnect',
                        reference, chain)

    def finalizeOnDisconnect(self, reference, chain):
        self._forEachDo(interfaces.IFinalizer, 'finalizeOnDisconnect',
                        reference, chain)

    def makeVocabulary(self, source, targets=None):
        iface = interfaces.IVocabularyProvider
        for obj in self.getComponents(iface):
            targets = obj.makeVocabulary(source, targets)
        return targets

    def listActionsFor(self, reference):
        actions = []
        iface = interfaces.IReferenceActionProvider
        for obj in self.getComponents(iface):
            actions = actions + obj.listActionsFor(reference)

        seen_urls = []
        value = []
        for action in actions:
            if action['url'] not in seen_urls:
                seen_urls.append(action['url'])
                value.append(action)
        return value

    def _forEachDo(self, interface, methodname, *args):
        """For each contained object that is implements interface, call method
        with *args."""
        for obj in self.getComponents(interface):
            meth = getattr(obj.aq_explicit, methodname)
            meth(*args)

    def _getPrimaryImplicator(self):
        impls = self.getComponents(interfaces.IPrimaryImplicator)
        if impls:
            return impls[0]
        else:
            return DefaultPrimaryImplicator(self)

    def _afterRename(self, context):
        """We have been renamed -> set relationship attributes on refs."""
        ref_ctl = getToolByName(context, REFERENCE_CATALOG)
        refs = self.__of__(context).getRefs(RELATIONSHIP_RULESETTOREF)
        for ref in refs:
            ref.relationship = self.getId()
            url = getRelURL(aq_parent(aq_inner(ref)), ref.getPhysicalPath())
            ref_ctl.catalog_object(ref, url, idxs=['relationship'])

registerType(Ruleset)


class RulesetAwareContainer:
    """Mix-in that's responsible for adding a reference from the
    library to new rulesets and informing rulesets when they get
    renamed.

    XXX: Depends on subclasses to also inherit from
    AllowedTypesByIface and OrderedBaseFolder."""

    # Add reference to Rulesets on invokeFactory
    def invokeFactory(self, type_name, id, RESPONSE = None, *args, **kwargs):
        library = getToolByName(self, RELATIONS_LIBRARY)

        super_invokeFactory = utils.AllowedTypesByIface.invokeFactory
        v = super_invokeFactory(self, type_name, id, RESPONSE, *args, **kwargs)

        obj = getattr(self, v)
        if interfaces.IRuleset.isImplementedBy(obj):

            library.addReference(obj, RELATIONSHIP_LIBRARY)
        return v

    # This hack allows us to inform the ruleset that it has been renamed.
    def _setObject(self, id, obj, roles=None, user=None, set_owner=1):
        library = getToolByName(self, RELATIONS_LIBRARY)
        
        super_setObject = OrderedBaseFolder._setObject
        super_setObject(self, id, obj, roles, user, set_owner)

        if interfaces.IRuleset.isImplementedBy(obj):
            ruleset = obj
            ref_ctl = getToolByName(self, REFERENCE_CATALOG)
            brains = ref_ctl(sourceUID=library.UID(),
                             targetUID=ruleset.UID(),
                             relationship=RELATIONSHIP_LIBRARY)
            if len(brains) != 0: # We assume a rename
                ruleset._afterRename(self)
            else: # Assume a copy: we need to register the ruleset
                library.addReference(ruleset, RELATIONSHIP_LIBRARY)


class Library(RulesetAwareContainer, utils.AllowedTypesByIface,
              ActionProviderBase, OrderedBaseFolder, XMLImportExport):
    """Registry for IRulesets. See ILibrary."""
    __implements__ = ((interfaces.ILibrary,) +
                      (ActionProviderBase.__implements__,
                       OrderedBaseFolder.__implements__, ))
                      

    schema = schema.BaseSchemaWithInvisibleId + XMLImportExport.schema
    portal_type = archetype_name = 'Relations Library'
    global_allow = 0
    content_icon = 'library_icon.gif'
    allowed_interfaces = interfaces.IRuleset, interfaces.IRulesetCollection

    def initializeArchetype(self, **kwargs):
        # add action
        self.addAction(
            id='relations',
            name='Relations',
            action='string:$object_url/relations_form',
            condition='python:object.relations_adddelete_vocab(test_only=1)',
            permission=('Modify portal content',),
            category='object_tabs',
            visible=1)
        
        OrderedBaseFolder.initializeArchetype(self, **kwargs)
        
    ##
    # see ILibrary
    def registerRuleset(self, ruleset):
        self.addReference(ruleset, RELATIONSHIP_LIBRARY)

    def getRuleset(self, id):
        ref_ctl = getToolByName(self, REFERENCE_CATALOG)
        uid_ctl = getToolByName(self, UID_CATALOG)

        # XXX: targetId index of reference_catalog is not being updated
        refs = ref_ctl(sourceUID=self.UID(),
                       relationship=RELATIONSHIP_LIBRARY)
        rulesets = uid_ctl(UID=[r.targetUID for r in refs], id=id)
        if rulesets:
            return rulesets[0].getObject()
        else:
            raise ValueError, "No ruleset with id %r" % id

    def getRulesets(self):
        # We want to have a reasonable order of rulesets.  First come the
        # rulesets in self, then rulesets of collections.
        v = self.objectValues('Ruleset')
        for collection in self.objectValues('Ruleset Collection'):
            v = v + collection.getRulesets()

        # look for objs that are not contained in self
        for obj in self.getRefs(RELATIONSHIP_LIBRARY):
            if obj not in v:
                v.append(obj)
        return v

    def getFolder(self):
        return self

registerType(Library)


class RulesetCollection(RulesetAwareContainer, utils.AllowedTypesByIface,
                        OrderedBaseFolder, XMLImportExport):
    """A container for IRulesets that lives inside the library."""
    __implements__ = (interfaces.IRulesetCollection,) + \
                     OrderedBaseFolder.__implements__

    schema = schema.BaseSchemaWithInvisibleId + XMLImportExport.schema
    portal_type = archetype_name = 'Ruleset Collection'
    global_allow = 0
    allowed_interfaces = interfaces.IRuleset, interfaces.IRulesetCollection

    def getRulesets(self):
        v = self.objectValues('Ruleset')
        for collection in self.objectValues('Ruleset Collection'):
            v = v + collection.getRulesets()
        return v

registerType(RulesetCollection)
