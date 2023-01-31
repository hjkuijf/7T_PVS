# **InsertLicense** code

from TestSupport import Fields, Logging
from AlgorithmModuleTestSupport import Checks as AMChecks
from AlgorithmModuleTestSupport import Tests as AMTests
from AlgorithmModule.Definitions import StatusCode

#----------------------------------------------------------------------------------

MODULE_NAME = "PVSDetection"

class TestData( object ):
  """Contains a setting of input and corresponding reference output field values."""
  def __init__( self ):
    self.inSubjectDir = None
    self.inT1Filename = None
    self.inT2Filename = None
    self.inDoSPM = None

def executeTestOfUpdate( testData ):
  __provideInput( testData )
  __processInput()
  __validateOutput( testData )

def __provideInput( testData ):
  __setUpNetworkWithInput( testData )

def __setUpNetworkWithInput( testData ):
  __setUpInputParameters( testData )

def __setUpInputParameters( testData ):
  Fields.setValue( "{}.inSubjectDir".format( MODULE_NAME ), testData.inSubjectDir )
  Fields.setValue( "{}.inT1Filename".format( MODULE_NAME ), testData.inT1Filename )
  Fields.setValue( "{}.inT2Filename".format( MODULE_NAME ), testData.inT2Filename )
  Fields.setValue( "{}.inDoSPM".format( MODULE_NAME ), testData.inDoSPM )

def __processInput():
  AMTests.testUpdate( MODULE_NAME )

def __validateOutput( testData ):
  __setUpNetworkWithOutputReference( testData )
  __executeChecksToValidateOutput( testData )

def __setUpNetworkWithOutputReference( testData ):
  pass

def __executeChecksToValidateOutput( testData ):
  checkList = __getChecksToValidateOutputAfterUpdate( testData )
  for check in checkList:
    check.execute()

def __getChecksToValidateOutputAfterUpdate( testData ):
  checks = (
  )
  return checks

def __getDefaultTestData():
  """Returns a default and valid TestData object."""
  Logging.infoHTML( "<b>ToDo: Set valid values for default TestData object!</b>" )
  testData = TestData()
  testData.inSubjectDir = None
  testData.inT1Filename = None
  testData.inT2Filename = None
  testData.inDoSPM = None
  return testData

#----------------------------------------------------------------------------------

def ITERATIVETEST_Error_Of_Input_Parameter_inSubjectDir():
  """Tests occurrence of an error because of an invalid input value provided at field "inSubjectDir"."""
  Logging.infoHTML( "<b>ToDo: Add more \"TestData\" objects to maximize variations!</b>" )
  testDataVariations = {
    "Invalid_Variation_1" : __getInvalidTestDataVariation1_inSubjectDir(),
    "Invalid_Variation_2" : __getInvalidTestDataVariation2_inSubjectDir(),
  }
  return ( testDataVariations, testError_inSubjectDir )

def __getInvalidTestDataVariation1_inSubjectDir():
  Logging.infoHTML( "<b>ToDo: Rename function that the name matches the intention of returned test data!</b>" )
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with a reliable invalid value of \"inSubjectDir\"!</b>" )
  testData.inSubjectDir = None
  return testData

def __getInvalidTestDataVariation2_inSubjectDir():
  Logging.infoHTML( "<b>ToDo: Rename function that the name matches the intention of returned test data!</b>" )
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with a reliable invalid value of \"inSubjectDir\"!</b>" )
  testData.inSubjectDir = None
  return testData

def testError_inSubjectDir( testData ):
  __provideInput( testData )
  checksToExecute = (
    AMChecks.EqualCheck( fieldName = "{}.statusCode".format( MODULE_NAME ),
                         value     = StatusCode.ERROR_INPUT_PARAMETER ),
  )
  AMTests.testFailedUpdate( MODULE_NAME, checksToExecute )

#----------------------------------------------------------------------------------

def ITERATIVETEST_Error_Of_Input_Parameter_inT1Filename():
  """Tests occurrence of an error because of an invalid input value provided at field "inT1Filename"."""
  Logging.infoHTML( "<b>ToDo: Add more \"TestData\" objects to maximize variations!</b>" )
  testDataVariations = {
    "Invalid_Variation_1" : __getInvalidTestDataVariation1_inT1Filename(),
    "Invalid_Variation_2" : __getInvalidTestDataVariation2_inT1Filename(),
  }
  return ( testDataVariations, testError_inT1Filename )

def __getInvalidTestDataVariation1_inT1Filename():
  Logging.infoHTML( "<b>ToDo: Rename function that the name matches the intention of returned test data!</b>" )
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with a reliable invalid value of \"inT1Filename\"!</b>" )
  testData.inT1Filename = None
  return testData

def __getInvalidTestDataVariation2_inT1Filename():
  Logging.infoHTML( "<b>ToDo: Rename function that the name matches the intention of returned test data!</b>" )
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with a reliable invalid value of \"inT1Filename\"!</b>" )
  testData.inT1Filename = None
  return testData

def testError_inT1Filename( testData ):
  __provideInput( testData )
  checksToExecute = (
    AMChecks.EqualCheck( fieldName = "{}.statusCode".format( MODULE_NAME ),
                         value     = StatusCode.ERROR_INPUT_PARAMETER ),
  )
  AMTests.testFailedUpdate( MODULE_NAME, checksToExecute )

#----------------------------------------------------------------------------------

def ITERATIVETEST_Error_Of_Input_Parameter_inT2Filename():
  """Tests occurrence of an error because of an invalid input value provided at field "inT2Filename"."""
  Logging.infoHTML( "<b>ToDo: Add more \"TestData\" objects to maximize variations!</b>" )
  testDataVariations = {
    "Invalid_Variation_1" : __getInvalidTestDataVariation1_inT2Filename(),
    "Invalid_Variation_2" : __getInvalidTestDataVariation2_inT2Filename(),
  }
  return ( testDataVariations, testError_inT2Filename )

def __getInvalidTestDataVariation1_inT2Filename():
  Logging.infoHTML( "<b>ToDo: Rename function that the name matches the intention of returned test data!</b>" )
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with a reliable invalid value of \"inT2Filename\"!</b>" )
  testData.inT2Filename = None
  return testData

def __getInvalidTestDataVariation2_inT2Filename():
  Logging.infoHTML( "<b>ToDo: Rename function that the name matches the intention of returned test data!</b>" )
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with a reliable invalid value of \"inT2Filename\"!</b>" )
  testData.inT2Filename = None
  return testData

def testError_inT2Filename( testData ):
  __provideInput( testData )
  checksToExecute = (
    AMChecks.EqualCheck( fieldName = "{}.statusCode".format( MODULE_NAME ),
                         value     = StatusCode.ERROR_INPUT_PARAMETER ),
  )
  AMTests.testFailedUpdate( MODULE_NAME, checksToExecute )

#----------------------------------------------------------------------------------

def ITERATIVETEST_Error_Of_Input_Parameter_inDoSPM():
  """Tests occurrence of an error because of an invalid input value provided at field "inDoSPM"."""
  Logging.infoHTML( "<b>ToDo: Add more \"TestData\" objects to maximize variations!</b>" )
  testDataVariations = {
    "Invalid_Variation_1" : __getInvalidTestDataVariation1_inDoSPM(),
    "Invalid_Variation_2" : __getInvalidTestDataVariation2_inDoSPM(),
  }
  return ( testDataVariations, testError_inDoSPM )

def __getInvalidTestDataVariation1_inDoSPM():
  Logging.infoHTML( "<b>ToDo: Rename function that the name matches the intention of returned test data!</b>" )
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with a reliable invalid value of \"inDoSPM\"!</b>" )
  testData.inDoSPM = None
  return testData

def __getInvalidTestDataVariation2_inDoSPM():
  Logging.infoHTML( "<b>ToDo: Rename function that the name matches the intention of returned test data!</b>" )
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with a reliable invalid value of \"inDoSPM\"!</b>" )
  testData.inDoSPM = None
  return testData

def testError_inDoSPM( testData ):
  __provideInput( testData )
  checksToExecute = (
    AMChecks.EqualCheck( fieldName = "{}.statusCode".format( MODULE_NAME ),
                         value     = StatusCode.ERROR_INPUT_PARAMETER ),
  )
  AMTests.testFailedUpdate( MODULE_NAME, checksToExecute )

#----------------------------------------------------------------------------------

def ITERATIVETEST_Variation_Of_Input_Parameter_inSubjectDir():
  """Tests variation of input value at field "inSubjectDir"."""
  Logging.infoHTML( "<b>ToDo: Add more \"TestData\" objects to maximize variations!</b>" )
  testDataVariations = {
    "Variation_1" : __getTestDataVariation1_inSubjectDir(),
  }
  return ( testDataVariations, executeTestOfUpdate )

def __getTestDataVariation1_inSubjectDir():
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with reliable variation values!</b>" )
  testData.inSubjectDir = None
  return testData

#----------------------------------------------------------------------------------

def ITERATIVETEST_Variation_Of_Input_Parameter_inT1Filename():
  """Tests variation of input value at field "inT1Filename"."""
  Logging.infoHTML( "<b>ToDo: Add more \"TestData\" objects to maximize variations!</b>" )
  testDataVariations = {
    "Variation_1" : __getTestDataVariation1_inT1Filename(),
  }
  return ( testDataVariations, executeTestOfUpdate )

def __getTestDataVariation1_inT1Filename():
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with reliable variation values!</b>" )
  testData.inT1Filename = None
  return testData

#----------------------------------------------------------------------------------

def ITERATIVETEST_Variation_Of_Input_Parameter_inT2Filename():
  """Tests variation of input value at field "inT2Filename"."""
  Logging.infoHTML( "<b>ToDo: Add more \"TestData\" objects to maximize variations!</b>" )
  testDataVariations = {
    "Variation_1" : __getTestDataVariation1_inT2Filename(),
  }
  return ( testDataVariations, executeTestOfUpdate )

def __getTestDataVariation1_inT2Filename():
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with reliable variation values!</b>" )
  testData.inT2Filename = None
  return testData

#----------------------------------------------------------------------------------

def ITERATIVETEST_Variation_Of_Input_Parameter_inDoSPM():
  """Tests variation of input value at field "inDoSPM"."""
  Logging.infoHTML( "<b>ToDo: Add more \"TestData\" objects to maximize variations!</b>" )
  testDataVariations = {
    "Variation_1" : __getTestDataVariation1_inDoSPM(),
  }
  return ( testDataVariations, executeTestOfUpdate )

def __getTestDataVariation1_inDoSPM():
  testData = __getDefaultTestData()
  Logging.infoHTML( "<b>ToDo: Replace \"None\" with reliable variation values!</b>" )
  testData.inDoSPM = None
  return testData

#----------------------------------------------------------------------------------

def TEST_Update_And_Clear():
  """Tests module's update and clear functionality."""
  executeTestOfUpdate( __getDefaultTestData())
  AMTests.testClear( MODULE_NAME, checkList = __getChecksToValidateOutputAfterClear())

def __getChecksToValidateOutputAfterClear():
  checks = (
  )
  return checks

#----------------------------------------------------------------------------------
