from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import os
import numpy as np



class PVSVesselness( AlgorithmMacroModule ):
  def __init__( self, ctx ):
    AlgorithmMacroModule.__init__( self, ctx )
    
    # input
    self.inDoField = self._ctx.field("inDo")
    self.inOutputDirField = self._ctx.field("inOutputDir")
    
    # network
    self.VesselnessModule = self._ctx.module("Vesselness")
    
    self.LoadModule = self._ctx.module("MLImageFormatLoad")
    self.SaveModule = self._ctx.module("MLImageFormatSave")
    
  
  def _validateInput( self ):
    self.__validateInputParameters()
    
  def __validateInputParameters( self ):
    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    if not MLABFileManager.isDir(outputDir):
      raise InputParameterError( u"Output dir is not valid")
    
    
    
            

  def _update( self ):    
    
    # Load from cache
    if not self.inDoField.boolValue():
      self.getOutput()
      return
    
    
    self.VesselnessModule.field("update").touch()
    
    vesselnessFilename = self.getOutputFilename() 
    self.SaveModule.field("fileName").setStringValue(vesselnessFilename)
    self.SaveModule.field("save").touch()

    self.getOutput()
    
  

  def _clear( self ):
    self.LoadModule.field("close").touch()
  


  def getOutputFilename( self ):
    return MLABFileManager.normalizePath( os.path.join(self.inOutputDirField.stringValue(), "Vesselness.mlimage"))
  
  def getOutput( self ):  
    vesselnessFilename = self.getOutputFilename() 
    
    self.LoadModule.field("fileName").setStringValue(vesselnessFilename)
  