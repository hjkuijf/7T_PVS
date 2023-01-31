from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import cPickle
import os

class PVSDetection( AlgorithmMacroModule ):
  def __init__( self, ctx ):
    AlgorithmMacroModule.__init__( self, ctx )
    
    # set up fields
    self.inSubjectDirField = self._ctx.field("inSubjectDir")
    self.inT1FilenameField = self._ctx.field("inT1Filename")
    self.inT2FilenameField = self._ctx.field("inT2Filename")
    
    self.inPlaneField = self._ctx.field("SoView2DPlane.plane")
    
    # set up field listeners
    self._ctx.addFieldListener( self.inSubjectDirField, self.subjectDirChanged, False )
    self._ctx.addFieldListener( self._ctx.field("loadPlane"), self.loadPlane, False )
    self._ctx.addFieldListener( self._ctx.field("savePlane"), self.savePlane, False )
    
    # set up modules
    self.T1Module = self._ctx.module("T1")
    self.T2Module = self._ctx.module("T2")

  def _validateInput( self ):
    self.__validateInputParameters()
    

  def __validateInputParameters( self ):
    
    subjectDir = MLABFileManager.normalizePath( self.inSubjectDirField.stringValue() )
    if not MLABFileManager.isDir(subjectDir):
      raise InputParameterError( u"Subject dir is not valid")
    
    if not MLABFileManager.exists( os.path.join(subjectDir, self.inT1FilenameField.stringValue()) ):
      raise InputParameterError( u"T1 image file does not exist")
    
    if not MLABFileManager.exists( os.path.join(subjectDir, self.inT2FilenameField.stringValue()) ):
      raise InputParameterError( u"T2 image file does not exist")
      

  def _update( self ):
    
    # Load the files
    subjectDir = MLABFileManager.normalizePath( self.inSubjectDirField.stringValue() )
    
    self.T1Module.field("fileName").setStringValue( os.path.join(subjectDir, self.inT1FilenameField.stringValue()) )
    if not self.T1Module.field("output0").isValid():
      raise InternalError( "T1 image not valid" )
    
    self.T2Module.field("fileName").setStringValue( os.path.join(subjectDir, self.inT2FilenameField.stringValue()) )
    if not self.T2Module.field("output0").isValid():
      raise InternalError( "T2 image not valid" )
    
    
    # do all the steps needed
    
    self.doStep('SPM')
    self.doStep('MNI')
    self.doStep('PVSVesselness')
    self.doStep('ROIPlane')
    self.doStep('Seedpoints')
    self.doStep('3DTracking')
    self.doStep('FilterGraph')
    self.doStep('GraphToMNI')
    
    
  
  def doStep( self, step ):
    
    if not self._ctx.hasModule(step):
      raise InternalError( u"No module exists for "+ str(step) )
    
    stepModule = self._ctx.module(step)
    
    # Output dir
    outputDir = os.path.join(self.inSubjectDirField.stringValue(), step)
    if not MLABFileManager.isDir(outputDir):
      if not MLABFileManager.mkdir(outputDir):
        raise InternalError( u"Cannot create output dir: "+ outputDir)      
    stepModule.field("inOutputDir").setStringValue( outputDir )
    
    # Do or load from cache ?
    stepModule.field("inDo").setBoolValue(self._ctx.field("inDo"+str(step)).boolValue())
    
    # Go, go, go
    stepModule.field("update").touch()
    
    if not stepModule.field("hasValidOutput").boolValue():
      raise InternalError( u"Module "+ str(step) +" has not produced valid output: '"+ stepModule.field("statusMessage").stringValue() +"'" )
    

  def _clear( self ):
    pass
  
  def subjectDirChanged( self ):
    subjectDir = MLABFileManager.normalizePath( self.inSubjectDirField.stringValue() )
    
    subjectDirContents = MLABFileManager.contentOfDirectory(subjectDir, "*.mlimage")
    for item in subjectDirContents:
      if "T1" in item:
        self.inT1FilenameField.setStringValue(item)
      if "T2" in item or "TSE" in item:
        self.inT2FilenameField.setStringValue(item)
        
  def loadPlane( self ):
    planeFilename = MLABFileDialog.getOpenFileName("MNI_plane", "Plane file (*.plane)", "Open Plane")
    if not planeFilename == "":
      with open(planeFilename, "rb") as planeFile:
        self.inPlaneField.setValue(cPickle.load(planeFile))
    
  
  def savePlane( self ):
    planeFilename = MLABFileDialog.getSaveFileName("MNI_plane", "Plane file (*.plane)", "Save Plane")
    if not planeFilename == "":
      with open(planeFilename, "wb") as planeFile:
        cPickle.dump(self.inPlaneField.value, planeFile)