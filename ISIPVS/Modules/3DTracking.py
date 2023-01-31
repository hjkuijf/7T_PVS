from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import os
import numpy as np
import pickle


class Tracking( AlgorithmMacroModule ):
  def __init__( self, ctx ):
    AlgorithmMacroModule.__init__( self, ctx )
    
    # input
    self.inDoField = self._ctx.field("inDo")
    self.inOutputDirField = self._ctx.field("inOutputDir")        
  
  def _validateInput( self ):
    self.__validateInputImages()
    self.__validateInputParameters()
    
  def __validateInputParameters( self ):    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    if not MLABFileManager.isDir(outputDir):
      raise InputParameterError( u"Output dir is not valid")
    
  def __validateInputImages( self ):
    if ( not self._ctx.field( "input0" ).isValid()):
      raise InputObjectError( u"No valid input image connected at field: {}.".format( "input0" ))
    
    if ( not self._ctx.field( "input1" ).isValid()):
      raise InputObjectError( u"No valid input image connected at field: {}.".format( "input1" ))
    

  def _update( self ):      
    
    # Load from cache
    if not self.inDoField.boolValue():
      self.getOutput()
      return
    
    self._ctx.field("TubularTracking.update").touch()
    
    graphFilename, trackedPointsFilename = self.getOutputFilename()
    self._ctx.field("SaveGraph.filename").setStringValue(graphFilename)
    self._ctx.field("SaveGraph.save").touch()
    self._ctx.field("SaveTrackedPoints.filename").setStringValue(trackedPointsFilename)
    self._ctx.field("SaveTrackedPoints.save").touch()
    
    self.getOutput()
    
  

  def _clear( self ):
    self._ctx.field("LoadGraph.delete").touch()
    self._ctx.field("LoadTrackedPoints.delete").touch()
  


  def getOutputFilename( self ):
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )  
    return MLABFileManager.normalizePath( os.path.join(outputDir, "graph.xml")), MLABFileManager.normalizePath( os.path.join(outputDir, "trackedPoints.xml"))
  
  def getOutput( self ):  
    graphFilename, trackedPointsFilename = self.getOutputFilename()
    self._ctx.field("LoadGraph.filename").setStringValue(graphFilename)
    self._ctx.field("LoadGraph.load").touch()
    self._ctx.field("LoadTrackedPoints.filename").setStringValue(trackedPointsFilename)
    self._ctx.field("LoadTrackedPoints.load").touch()
    
  