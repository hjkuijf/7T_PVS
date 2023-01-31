from AlgorithmMacroModule.AlgorithmMacroModule import AlgorithmMacroModule, InputObjectError, InputParameterError, InternalError
from AlgorithmModule.Definitions import StatusCode

from mevis import *
import os, string, subprocess, _winreg


class MatlabNotFoundError(Exception):
  pass


class SPM( AlgorithmMacroModule ):
  def __init__( self, ctx ):
    AlgorithmMacroModule.__init__( self, ctx )
    
    self.inDoField = self._ctx.field("inDo")
    self.inOutputDirField = self._ctx.field("inOutputDir")
    self.outputFilename = "T1.nii"
    
  
  def _validateInput( self ):
    self.__validateInputImages()
    self.__validateInputParameters()
    
  def __validateInputParameters( self ):
    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    if not MLABFileManager.isDir(outputDir):
      raise InputParameterError( u"Output dir is not valid")
    
    try:
      self.getMatlabPath()
    except MatlabNotFoundError:
      raise InternalError( u"Matlab not found." )
    
      
  def __validateInputImages( self ):
    if ( not self._ctx.field( "inT1" ).isValid()):
      raise InputObjectError( u"No valid input image connected at field: {}.".format( "inT1" ))
      
      

  def _update( self ):    
    
    # Load from cache
    if not self.inDoField.boolValue():
      self.getOutput()
      return
    
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    
    matlabPath = self.getMatlabPath()      
    spmPath = MLABFileManager.normalizePath( os.path.join(ctx.networkPath(), 'spm12_6685') )
    
    # Save T1 image as nifti
    ctx.field("T1Save.fileName").setStringValue(os.path.join(outputDir, self.outputFilename))
    ctx.field("T1Save.save").touch()
    
    # Run SPM
    args = []
    args.append(matlabPath)
    args.extend(['-nodesktop', '-nosplash', '-wait']) # , '-singleCompThread'
      
    spmCommands = []
    spmCommands.append("spmPath='"+spmPath+"'")
    spmCommands.append("addpath(spmPath)")
    spmCommands.append("subjectDir='"+outputDir+"'")
    spmCommands.append("run('"+ MLABFileManager.normalizePath( os.path.join(ctx.networkPath(), "run_spm.m") ) +"')")
    
    args.extend(['-r', string.join(spmCommands, ';')+';'])
    
    MLAB.log("SPM started with arguments: " + str(args) )
    subprocess.call(args) 
    
    self.getOutput()
  

  def _clear( self ):
    pass
  

  def getMatlabPath( self ):
    # The location of matlab.exe is stored in:
    # HKEY_LOCAL_MACHINE\SOFTWARE\MathWorks\MATLAB\[version]
  
    # Open the MATLAB registry
    registry = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    matlabKey = _winreg.OpenKey(registry, "SOFTWARE\MathWorks\MATLAB")
    
    # Find the latest Matlab version
    matlabVersion = str(0)        
    for i in range(1000):
      try:
        currentMatlabVersion = _winreg.EnumKey(matlabKey, i)
        if currentMatlabVersion > matlabVersion:
          matlabVersion = currentMatlabVersion
      except WindowsError:
        # Since you cannot determine the number of keys, you must
        # loop until error
        break
    
    if matlabVersion == str(0):
      raise MatlabNotFoundError
    
    # Registry key of latest Matlab version
    currentMatlabKey = _winreg.OpenKey(matlabKey, currentMatlabVersion)
    
    # Find the tag MATLABROOT
    matlabRoot = ""
    for i in range(1000):
      try:
        value = _winreg.EnumValue(currentMatlabKey, i)                
        # value = ('MATLABROOT', path, datatype (=string))
  
        if value[0] == "MATLABROOT":
          matlabRoot = value[1]        
      except WindowsError:
        break
        
        
    matlabPath = os.path.join(matlabRoot, 'bin', 'matlab.exe')
    
    if not os.path.exists(matlabPath):
      raise MatlabNotFoundError
        
    return MLABFileManager.normalizePath( matlabPath )

  
  def getOutput( self ):
    outputDir = MLABFileManager.normalizePath( self.inOutputDirField.stringValue() )
    
    for i in ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']:
      cFilename = MLABFileManager.normalizePath( os.path.join(outputDir, i+self.outputFilename) )
      
      self._ctx.module(i).field("fileName").setStringValue(cFilename)
  
  