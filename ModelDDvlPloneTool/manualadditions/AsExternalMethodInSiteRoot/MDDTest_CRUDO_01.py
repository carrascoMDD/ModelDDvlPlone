## Script (Python) "MDDTest_CRUDO_01"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=theReportDetailLevel=0
##title=Exercise ModelDDvlPlone framework structural operations (CRUDO) Create Read Update Delete Object (links, inheritance)
##

import sys
import traceback
import logging


from StringIO import StringIO

from ZODB.POSException import ConflictError




cLogExceptions = True




# #################################################
"""Just during development - Make bigger for longer scenarios. 
This code never enters production, but may be used in quality assesment on production systems.

"""


cMaxCycles = 10 * 1000  

def fMDDTest_CRUDO_01( theModelDDvlPloneTool, theContextualObject):
    
    aProgramDef ={
        'name':                       'CRUDO_01',
        'states': {
            'eInitial':  { 
                'init': {
                    'history':        'hisNewEpisode',
                },
                'outcomes': {
                    'success': {  
                        'state':   'eCreateRoot', 
                        'stack':   'stkPush',
                    },
                },
            },
            'eCreateRoot':  { 
                'init': {
                    'history':        'hisNewEpisode',
                },
                'parms': {
                    'theContainer':    [ 'value', aRootCtxt.fGP( 'theCtxtObj'),],
                    'theType':         [ 'value', 'BPDOrganizacion',],
                    'theId':           [ 'value', 'organization-01',],
                    'theTitle':        [ 'value', 'Organization 01',],
                },
                'do': [
                    [ 'invoke', ta_fCreateElement,]
                ],
                'outcomes': {
                    'success': {  
                        'state':    'eReadRootCollections', 
                        'stack':    'stkPush',
                    },
                },
            },
            'eReadRootCollections':  { 
                'init': {
                    'history':        'hisNewEpisode',
                },
                'outcomes': {
                    'any': {
                        'state':    'eEnd', 
                    },
                },
            },
        },

    }
    
    
    aRootCtxt = self.fMDDTest_InitAutomaton( theModelDDvlPloneTool, theContextualObject, aProgramDef)
    
    self.fMDDTest_RunAutomaton( aRootCtxt)
    
    return self


    
    
    
    
    

def fMDDTest_InitAutomaton( theModelDDvlPloneTool, theContextualObject, theProgramDef, theInitialState='eInitial'):
    
    if theContextualObject == None:
        return None
    
    anOutput = StringIO( u'')
    
    aRootCtxt = theContextualObject.ModelDDvlPlone_tool.fNewNestedContext( 
        theContextualObject,
        {
            'theTstName': theProgramDef[ 'name'],
            'theCtxtObj': theContextualObject,
            'theMDDTool': theModelDDvlPloneTool,
            
            'output':     anOutput,
            'pO':         lambda theString: anOutput.write( theString),
            'pOL':        lambda theString: anOutput.write( '%s\n' % theString),
            'pOS':        lambda theString: anOutput.write( '%s\n' % '\n'.join( [ unaLine.strip() for unaLine in theString.splitlines()])),      
        },
    )
    
    
    aRootCtxt.pSP( 'theHistory',    theModelDDvlPloneTool.fNewLinkedList( theContextualObject))
    
    aRootCtxt.pSP( 'theEpisodes', [ aRootCtxt.fGP( 'theHistory').fNewNodeWithProperties_Last( theProperties={ 'theCtxts': [ aRootCtxt,],})])
    
    aRootCtxt.pSP( 'theTestPrg', theProgramDef)
    
    aRootCtxt.pSP( 'theState', theInitialState)
    
    return aRootCtxt





        

def fMDDTest_RunAutomaton( theRootCtxt):

    aThisCtxt = theRootCtxt
    
    unaFinalException = None
    
    unCounter = 0
    
    while aThisCtxt.fGP( 'theState') and not ( aThisCtxt.fGP( 'theState') == 'eEnd') and not ( unCounter > cMaxCycles):
        
        unCounter += 1
        
        try:
            # #################################################
            if aThisCtxt.fGP( 'theState') == 'eInitial':
                """
                
                """
                aThisCtxt = fStateTransition( aThisCtxt,)
                continue
            
            
            
            
            
            
            # #################################################
            elif aThisCtxt.fGP( 'theState') == 'eCreateRoot':
                """
                
                """
                aThisCtxt = fStateInit( aThisCtxt)
                
                unCreateRootResult = aThisCtxt.fGP( 'theMDDTool').fCrearElementoDeTipo( 
                    theTimeProfilingResults =None,
                    theContainerElement     =aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['parms'][ 'theContainer'], 
                    theTypeName             =aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['parms'][ 'theType'], 
                    theId                   =aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['parms'][ 'theId'],
                    theTitle                =aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['parms'][ 'theTitle'], 
                    theDescription          ='Created by Test=%s, at State=%s; on Date=%s' % ( aThisCtxt.fGP( 'theTestPrg')['name'], aThisCtxt.fGP( 'theState'), fMillisecondsNow()),
                    theAdditionalParams     =None,
                    theAllowFactoryMethods  =False,
                )  
                aThisCtxt.pAppendActionResult( [ 'fCrearElementoDeTipo', unCreateRootResult,])
                
                if ( not unCreateRootResult) or not ( unCreateRootResult[ 'effect'] == 'created'):
                    unState = 'eFailure'
                    continue
                    
                unResultadoNuevoElemento = unCreateRootResult.get( 'new_object_result', {})
                if ( not unResultadoNuevoElemento) or ( unResultadoNuevoElemento.get( 'object') == None):
                    unState = 'eFailure'
                    continue
                
                aThisCtxt.pSP( 'theObject', unResultadoNuevoElemento.get( 'object'))
                
                aThisCtxt = fStateTransition( aThisCtxt, 'success')
                continue
            
            
            
            # #################################################
            elif aThisCtxt.fGP( 'theState') == 'eReadRootCollections':
                """
                
                """
                aThisCtxt = fStateTransition( aThisCtxt,)
                continue
            
                
             
            # #################################################
            elif aThisCtxt.fGP( 'theState') == 'eFailure':
                """
                
                """
                aThisCtxt = fStateTransition( aThisCtxt,)
                continue
            
                
                
            
             
            # #################################################
            elif aThisCtxt.fGP( 'theState') == 'eSuccess':
                """
                
                """
                aThisCtxt = fStateTransition( aThisCtxt,)
                continue
            
                
                
            
                
            # #################################################
            elif aThisCtxt.fGP( 'theState') == 'eEnd':
                """
                
                """
                break
            
            
            
            else:
                break
            
        except ConflictError:
            raise
        except Exception, anException:
            unaExceptionInfo = sys.exc_info()
            unaExceptionFormattedTraceback = '\n'.join( traceback.format_exception( *unaExceptionInfo))
            
            unInformeExcepcion = 'Exception during Test automaton' 
            unInformeExcepcion += 'exception class %s\n' % unaExceptionInfo[1].__class__.__name__ 
            unInformeExcepcion += 'exception message %s\n\n' % str( unaExceptionInfo[1].args)
            unInformeExcepcion += unaExceptionFormattedTraceback   

            aThisCtxt.pAppendExceptionReport( [ unaExceptionInfo[1].__class__.__name__, unInformeExcepcion,])
            
            if cLogExceptions:
                logging.getLogger( 'ModelDDvlPlone').error( unInformeExcepcion)
            
            aThisCtxt = fStateTransition( aThisCtxt, 'exception')

            continue
                
       
                        
           

def fStateInit( theThisCtxt):
    if not theThisCtxt:
        return theThisCtxt

    aThisCtxt = theThisCtxt
    
    aInitDef = None
    
    if aThisCtxt.fGP_AndCacheLocal( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')].has_key( 'init'):
        aInitDef = aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['init']
    
        if aInitDef:
            if aInitDef.has_key( 'history'):
                if 'hisNewEpisode' in aInitDef['history']:
                    aThisCtxt.fGP_AndCacheLocal( 'theHistory').fNewNodeWithProperties_Last( theProperties={ 'theCtxts': [ aThisCtxt,],})
            
            if aInitDef.has_key( 'stack'):
                if 'stkPush' in aInitDef['stack']:
                    aThisCtxt = aThisCtxt.fNewCtxt()
                    aThisCtxt.pSP( 'theEpisodes', [  aThisCtxt.fGP_AndCacheLocal( 'theHistory').fNode_Last(),])
                    aThisCtxt.fGP_AndCacheLocal( 'theHistory').fNode_Last().fGP( 'theCtxts').append( aThisCtxt)
    
    return aThisCtxt

            
            
            

def fStateTransition( theThisCtxt, theOutcome=''):
    if not theThisCtxt:
        return theThisCtxt

    unNewState ='eEnd'
    aThisCtxt = theThisCtxt
    
    if aThisCtxt.fGP_AndCacheLocal( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')].has_key( 'outcomes')  and \
        aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['outcomes']:
        
        anOutcomeDef = None
       
        if theOutcome:
            if aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['outcomes'].has_key( theOutcome):
                anOutcomeDef = aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['outcomes'][ theOutcome]
        else:
            anOutcomeDef = aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['outcomes'][ sorted( aThisCtxt.fGP( 'theTestPrg')['states'][ aThisCtxt.fGP( 'theState')]['outcomes'].keys())[0]]
            
        if anOutcomeDef:
            unNewState = anOutcomeDef['state']
         
            if not ( unNewState == 'eEnd'):
                if anOutcomeDef.has_key( 'history'):
                    if 'hisNewEpisode' in anOutcomeDef['history']:
                        aThisCtxt.fGP_AndCacheLocal( 'theHistory').fNewNodeWithProperties_Last( theProperties={ 'theCtxts': [ aThisCtxt,],})
            
                if anOutcomeDef.has_key( 'stack'):
                    if 'stkPush' in anOutcomeDef['stack']:
                        aThisCtxt = aThisCtxt.fNewCtxt()
                        aThisCtxt.pSP( 'theEpisodes', [ aThisCtxt.fGP_AndCacheLocal( 'theHistory').fNode_Last(),])
                        aThisCtxt.fGP_AndCacheLocal( 'theHistory').fNode_Last().fGP( 'theCtxts').append( aThisCtxt)

                
    aThisCtxt.pSP( 'theState', unNewState)        
        
    return aThisCtxt

