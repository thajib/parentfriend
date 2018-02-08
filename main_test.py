import unittest

from main import PinEntry


class MainTest(unittest.TestCase):
    # test some of the functions

    def testgetIndx(self):
        #  pinIDs = OrderedDict({1: 'PIN1', 2: 'PIN2', 3: 'PIN3', 4: 'PIN4'})

        expIndx = 2
        pinName = "PIN0"

        mainApp = PinEntry()
        retIndx = mainApp.getIndx(pinName)

        self.assertEqual(expIndx, retIndx)

    def testgetNextPIN_immediateNext(self):
        expPIN = "PIN1"
        pinName = "PIN0"

        pinEntry = PinEntry()
        retPIN = pinEntry.getNextPIN(pinName)

        self.assertEqual(expPIN, retPIN)

    def testgetNextPIN_rollOver(self):
        expPIN = "PIN1"
        pinName = "PIN4"

        pinEntry = PinEntry()
        retPIN = pinEntry.getNextPIN(pinName)

        self.assertEqual(expPIN, retPIN)


if __name__ == "__main__":
    unittest.main()
