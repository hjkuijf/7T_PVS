from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import os



class MNI( AlgorithmMacroModule ):
  def __init__( self, ctx ):
    AlgorithmMacroModule.__init__( self, ctx )
    
    # input
    self.inDoField = self._ctx.field("inDo")
    self.inOutputDirField = self._ctx.field("inOutputDir")
    
    # output
    self.outT1_to_T2Field = self._ctx.field("outT1_to_T2")
    self.outMNI_to_T1Field = self._ctx.field("outMNI_to_T1")
    self.outWMModule = self._ctx.module("OutWM")
    self.outT1atT2Module = self._ctx.module("T1_at_T2")
    
  
  def _validateInput( self ):
    self.__validateInputImages()
    self.__validateInputParameters()
    
  def __validateInputParameters( self ):
    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    if not MLABFileManager.isDir(outputDir):
      raise InputParameterError( u"Output dir is not valid")
    
    
      
  def __validateInputImages( self ):
    if ( not self._ctx.field( "inT1" ).isValid()):
      raise InputObjectError( u"No valid input image connected at field: {}.".format( "inT1" ))
    
    if ( not self._ctx.field( "inT2" ).isValid()):
      raise InputObjectError( u"No valid input image connected at field: {}.".format( "inT2" ))
    
    if ( not self._ctx.field( "inWM" ).isValid()):
      raise InputObjectError( u"No valid input image connected at field: {}.".format( "inWM" ))
      
      

  def _update( self ):    
    
    # Load from cache
    if not self.inDoField.boolValue():
      self.getOutput()
      return
    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    
    tempDir = MLABFileManager.normalizePath( os.path.join(outputDir, "temp") )
    MLABFileManager.mkdir(tempDir)
    
    wmFilename, t1AtT2Filename = self.getOutputFilename()
    
    # Register the T1 to the E2 (affine)
    T1_to_T2_Dir = MLABFileManager.normalizePath( os.path.join(tempDir, "t12t2") )
    MLABFileManager.mkdir(T1_to_T2_Dir)
    ctx.field("T1_to_E2.temporaryDirectory").setStringValue(T1_to_T2_Dir)  
    ctx.field("T1_to_E2.update").touch()
    ctx.field("T1_to_E2.resultingTransformationFileCopy").setStringValue( os.path.join(outputDir, "T1_to_T2.txt") )
    ctx.field("T1_to_E2.saveResultingTransformationFileCopy").touch()  
    ctx.field("T1_at_T2_Save.fileName").setStringValue(t1AtT2Filename)
    ctx.field("T1_at_T2_Save.save").touch()
    
    # Register the MNI to the T1 (affine + bspline)
    MNI_to_T1_Dir = MLABFileManager.normalizePath( os.path.join(tempDir, "mni2t1") )
    MLABFileManager.mkdir(MNI_to_T1_Dir)
    ctx.field("MNI_to_T1.temporaryDirectory").setStringValue(MNI_to_T1_Dir)  
    ctx.field("MNI_to_T1.update").touch()
    ctx.field("MNI_to_T1.resultingTransformationFileCopy").setStringValue( os.path.join(outputDir, "MNI_to_T1.txt") )
    ctx.field("MNI_to_T1.saveResultingTransformationFileCopy").touch()
    
        
    # Transform the WM mask from the T1 to the E2
    ctx.field("Transformix1.workingDirectory").setStringValue(T1_to_T2_Dir)
    ctx.field("Transformix1.update").touch()  
    
    
    # Save them shizzle !  
    ctx.field("MLImageFormatSave.fileName").setStringValue( wmFilename )
    ctx.field("MLImageFormatSave.save").touch()
       
    
    
    self.getOutput()
    
    # Clean
    MLABFileManager.recursiveRemoveDir(tempDir)
  

  def _clear( self ):
    pass
  


  def getOutputFilename( self ):
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
  
    return MLABFileManager.normalizePath( os.path.join(outputDir, "WM.mlimage")), MLABFileManager.normalizePath( os.path.join(outputDir, "T1_at_T2.mlimage"))
  
  def getOutput( self ):  
    wmFilename, t1AtT2Filename = self.getOutputFilename()    
    self.outWMModule.field("fileName").setStringValue(wmFilename)
    self.outT1atT2Module.field("fileName").setStringValue(t1AtT2Filename)    
    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    self.outMNI_to_T1Field.setStringValue(os.path.join(outputDir, "MNI_to_T1.txt"))
    self.outT1_to_T2Field.setStringValue(os.path.join(outputDir, "T1_to_T2.txt"))
  