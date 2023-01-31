from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import os
import numpy as np
import cPickle
import subprocess


class GraphToMNI( AlgorithmMacroModule ):
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
    
    if not MLABFileManager.exists(self._ctx.field("inMNItoT1").stringValue() ):
      raise InputParameterError( u"inMNItoT1 is not valid")
    
    if not MLABFileManager.exists(self._ctx.field("inT1toT2").stringValue() ):
      raise InputParameterError( u"inT1toT2 is not valid")
    
            

  def _update( self ):      
    
    # Load from cache
    if not self.inDoField.boolValue():
      self.getOutput()
      return
    
    self._ctx.field("XMarkerListContainer.deleteAll").touch()
    xMarkerList = self._ctx.field("XMarkerListContainer.outXMarkerList").object()
    
    graph = self._ctx.field("BaseBypass.baseOut0").object()
    for edge in graph.getEdges():
      skeletons = edge.getSkeletons()
      
      for point in skeletons:
        xMarkerList.add( point.position(), (0,0,0), 0)
        
        
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )  
    tempDir = MLABFileManager.normalizePath( os.path.join(outputDir, "temp") )
    MLABFileManager.mkdir(tempDir)
    
    T1_to_T2_Dir = MLABFileManager.normalizePath( os.path.join(tempDir, "t12t2") )
    MLABFileManager.mkdir(T1_to_T2_Dir)
    self._ctx.field("Transformix.workingDirectory").setStringValue(T1_to_T2_Dir)  
    self._ctx.field("Transformix.transformationFile").setStringValue(self._ctx.field("inT1toT2").stringValue())
    self._ctx.field("Transformix.update").touch()
    
    MNI_to_T1_Dir = MLABFileManager.normalizePath( os.path.join(tempDir, "mni2t1") )
    MLABFileManager.mkdir(MNI_to_T1_Dir)
    self._ctx.field("Transformix1.workingDirectory").setStringValue(MNI_to_T1_Dir)  
    self._ctx.field("Transformix1.transformationFile").setStringValue(self._ctx.field("inMNItoT1").stringValue())    
    self._ctx.field("Transformix1.update").touch()
    
    orig, mni = self.getOutputFilename()
    self._ctx.field("SaveOrig.filename").setStringValue(orig)
    self._ctx.field("SaveOrig.save").touch()
    
    self._ctx.field("SaveMNI.filename").setStringValue(mni)
    self._ctx.field("SaveMNI.save").touch()
    
    self.getOutput()
    
    # Clean
    MLABFileManager.recursiveRemoveDir(tempDir)
    
  

  def _clear( self ):
    self._ctx.field("LoadOrig.delete").touch()
    self._ctx.field("LoadMNI.delete").touch()
  


  def getOutputFilename( self ):
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )  
    return MLABFileManager.normalizePath( os.path.join(outputDir, "orig_points.xml")), MLABFileManager.normalizePath( os.path.join(outputDir, "mni_points.xml"))
  
  
  def getOutput( self ):  
    orig, mni = self.getOutputFilename()
    self._ctx.field("LoadOrig.filename").setStringValue(orig)
    self._ctx.field("LoadOrig.load").touch()
    
    self._ctx.field("LoadMNI.filename").setStringValue(mni)
    self._ctx.field("LoadMNI.load").touch()
    
  
