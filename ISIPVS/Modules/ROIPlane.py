from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import os
import numpy as np
import cPickle


class ROIPlane( AlgorithmMacroModule ):
  def __init__( self, ctx ):
    AlgorithmMacroModule.__init__( self, ctx )
    
    # input
    self.inDoField = self._ctx.field("inDo")
    self.inZField = self._ctx.field("inZ")
    self.inOutputDirField = self._ctx.field("inOutputDir")
    self.inT1_to_T2Field = self._ctx.field("inT1_to_T2")
    self.inMNI_to_T1Field = self._ctx.field("inMNI_to_T1")
    self.inPlane = self._ctx.field("inPlane")
    
    # network
    self.ReadElastixTransformParameterFileModule = self._ctx.module("ReadElastixTransformParameterFile")
    self.MNI_T1Field = self._ctx.module("MNI_T1").field("output0")
    self.MPRModule = self._ctx.module("MPR")
    
  
  def _validateInput( self ):
    self.__validateInputParameters()
    
  def __validateInputParameters( self ):
    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    if not MLABFileManager.isDir(outputDir):
      raise InputParameterError( u"Output dir is not valid")
    
    if not MLABFileManager.exists(self.inMNI_to_T1Field.stringValue()):
      raise InputParameterError( u"MNI to T1 file does not exist." )
    
    if not MLABFileManager.exists(self.inT1_to_T2Field.stringValue()):
      raise InputParameterError( u"T1 to T2 file does not exist." )
    
            

  def _update( self ):      
    
    # Load from cache
    if not self.inDoField.boolValue():
      self.getOutput()
      return
    
    # Set up for T2 ROI
    self._ctx.field("Mask.input0").connectFrom(self._ctx.field("T2.output0"))
    self._ctx.field("Mask.input1").connectFrom(self._ctx.field("WM.output0"))
    self._ctx.field("MPR.input0").connectFrom(self._ctx.field("Mask.output0"))
    self._do('T2')
    
    # Vesselness
    self._ctx.field("Mask.input0").connectFrom(self._ctx.field("Vesselness.output0"))
    self._do('Vesselness')
    
    # T1
    self._ctx.field("Mask.input0").connectFrom(self._ctx.field("T1atT2.output0"))
    self._do('T1')
    
    # Mask itself
    self._ctx.field("MPR.input0").connectFrom(self._ctx.field("WM.output0"))
    self._do('Mask')
    
    
    self.getOutput()
  
  def _do( self, what ):
    
    self.ReadElastixTransformParameterFileModule.field("filename").setStringValue(self.inT1_to_T2Field.stringValue())
    self.ReadElastixTransformParameterFileModule.field("read").touch()
    t1ToT2 = self.ReadElastixTransformParameterFileModule.field("matrix").matrixValue()
    
    self.ReadElastixTransformParameterFileModule.field("filename").setStringValue(self.inMNI_to_T1Field.stringValue().replace(".txt", '.1.txt'))
    self.ReadElastixTransformParameterFileModule.field("read").touch()
    mniToT1i = self.ReadElastixTransformParameterFileModule.field("matrix").matrixValue()
    mniToT1  = self.ReadElastixTransformParameterFileModule.field("inverseMatrix").matrixValue()
    
    
    #mniPlaneVoxel = [96.5 , 132.5 , self.inZField.intValue()]    
    #mniPlaneD = self.MNI_T1Field.mapVoxelToWorld(mniPlaneVoxel)[2]
    #mniPlane = [0, 0, 1, 36.5]
    #mniPlane = [0, -0.437765777111053, 0.899089097976685, 28.8901462554932]
    mniPlane = self.inPlane.vectorValue()
    
    O = np.array( mniPlane[:3] ) * mniPlane[3]
    O = np.append(O, 1)
    N = np.array( mniPlane[:3])
    N = np.append(N, 0)
    
    O = np.array(mniToT1).dot(O)
    N = np.array(mniToT1i).transpose().dot(N)
    
    t1Plane = N[:3]
    t1Plane = np.append(t1Plane, O[:3].dot(N[:3]))
    
    
    self.MPRModule.field("axialOnInput").touch()
    self.MPRModule.field("plane").setValue(t1Plane)
    
    outputImageFilename, outputPlaneFilename = self.getOutputFilename()
    self._ctx.field("MLImageFormatSave.fileName").setStringValue(outputImageFilename.replace("mlimage", what+".mlimage"))
    self._ctx.field("MLImageFormatSave.save").touch()
    
    with open(outputPlaneFilename, "wb") as outputPlaneFile:
      cPickle.dump(t1Plane, outputPlaneFile)
    
    
  

  def _clear( self ):
    for i in ['T1', 'T2', 'Mask', 'Vesselness']:
      self._ctx.field(i+"Load.fileName").setStringValue("")
    self._ctx.field("outPlane").setValue([0,0,0,0])
  


  def getOutputFilename( self ):
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
  
    return MLABFileManager.normalizePath( os.path.join(outputDir, "ROIPlane.mlimage")), MLABFileManager.normalizePath( os.path.join(outputDir, "ROIPlane.plane"))
  
  def getOutput( self ):  
    outputImageFilename, outputPlaneFilename = self.getOutputFilename()
    
    for i in ['T1', 'T2', 'Mask', 'Vesselness']:
      if not MLABFileManager.exists(outputImageFilename.replace('mlimage', i+'.mlimage')):
        raise InternalError( u"Output image does not exist for ROIPlane module: "+ outputImageFilename.replace('mlimage', i+'.mlimage') )
    if not MLABFileManager.exists(outputPlaneFilename):
      raise InternalError( u"Output plane does not exist for ROIPlane module: "+ outputPlaneFilename )
    
    
    for i in ['T1', 'T2', 'Mask', 'Vesselness']:
      self._ctx.field(i+"Load.fileName").setStringValue(outputImageFilename.replace('mlimage', i+'.mlimage') )
    
    with open(outputPlaneFilename, "rb") as outputPlaneFile:
      t2Plane = cPickle.load(outputPlaneFile)
    self._ctx.field("outPlane").setValue(t2Plane)
    
  