import unittest
from app.unit_tests.dbTest import DBTest
from app.unit_tests.funcTest import FuncTest

calcST = unittest.TestSuite()
calcST.addTest(unittest.TestLoader().loadTestsFromTestCase(DBTest))
calcST.addTest(unittest.TestLoader().loadTestsFromTestCase(FuncTest))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(calcST)
