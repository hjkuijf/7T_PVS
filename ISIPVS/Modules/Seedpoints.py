from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import os
import numpy as np
import cPickle
import subprocess


class Seedpoints( AlgorithmMacroModule ):
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
    
    for i in ['T2', 'T1', 'Vesselness', 'Mask']:
      if ( not self._ctx.field( "input"+i ).isValid()):
        raise InputObjectError( u"No valid input image connected at field: {}.".format( "input"+i ))
    
    
    
            

  def _update( self ):      
    
    # Load from cache
    if not self.inDoField.boolValue():
      self.getOutput()
      return
    
    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )  
    for i in ['T2', 'T1', 'Vesselness', 'Mask']:
      self._ctx.field("itkImageFileWriter.input0").connectFrom(self._ctx.field(i+'.output0'))
      self._ctx.field("itkImageFileWriter.fileName").setStringValue(os.path.join(outputDir, i+'.nii'))
      self._ctx.field("itkImageFileWriter.save").touch()
      
      
    # Run kNN
    try:
      subprocess.check_output('D:/Anaconda2/Scripts/activate.bat D:/Anaconda2 && python D:/data/j/script/knn.py "'+outputDir+'" -k 51 -p 0.05 -t1 -d -w distance', shell=True)      
    except subprocess.CalledProcessError as e:
      raise InternalError( u"kNN Computation did not succeed." )
      
    
    self._ctx.field("itkImageFileReader.fileName").setStringValue(os.path.join(outputDir, 'p.nii'))
    
    
    
    self._ctx.field("MaskToMarkers.update").touch()
    seedpointFilename = self.getOutputFilename()
    self._ctx.field("SaveBase.filename").setStringValue(seedpointFilename)
    self._ctx.field("SaveBase.save").touch()
    
    self.getOutput()
    
  

  def _clear( self ):
    self._ctx.field("LoadBase.delete").touch()
  


  def getOutputFilename( self ):
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )  
    return MLABFileManager.normalizePath( os.path.join(outputDir, "seedpoint.xml"))
  
  def getOutput( self ):  
    seedpointFilename = self.getOutputFilename()
    self._ctx.field("LoadBase.filename").setStringValue(seedpointFilename)
    self._ctx.field("LoadBase.load").touch()
    
  
