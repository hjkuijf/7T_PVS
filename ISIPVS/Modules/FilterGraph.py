from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import os
import numpy as np
import cPickle
import subprocess


class FilterGraph( AlgorithmMacroModule ):
  def __init__( self, ctx ):
    AlgorithmMacroModule.__init__( self, ctx )
    
    # input
    self.inDoField = self._ctx.field("inDo")
    self.inOutputDirField = self._ctx.field("inOutputDir")        
  
  def _validateInput( self ):
    self.__validateInputParameters()
    
    if self._ctx.field("baseIn0").isNull():
      raise InputObjectError( u"Input graph is not valid")
    
  def __validateInputParameters( self ):    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    if not MLABFileManager.isDir(outputDir):
      raise InputParameterError( u"Output dir is not valid")
    
    
    
            

  def _update( self ):      
    
    # Load from cache
    if not self.inDoField.boolValue():
      self.getOutput()
      return
    
    self._ctx.field("GraphFilter.update").touch()
    
    seedpointFilename = self.getOutputFilename()
    self._ctx.field("SaveBase.filename").setStringValue(seedpointFilename)
    self._ctx.field("SaveBase.save").touch()
    
    
    self.getOutput()
    
  

  def _clear( self ):
    self._ctx.field("LoadBase.delete").touch()
  


  def getOutputFilename( self ):
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )  
    return MLABFileManager.normalizePath( os.path.join(outputDir, "filter_graph.xml"))
  
  
  def getOutput( self ):  
    seedpointFilename = self.getOutputFilename()
    self._ctx.field("LoadBase.filename").setStringValue(seedpointFilename)
    self._ctx.field("LoadBase.load").touch()
    
  
