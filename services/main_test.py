import unittest

import main
from mock import MagicMock, patch
from datetime import datetime


class MainTest(unittest.TestCase):

    def testgetScheduleBlock(self):
        # getScheduleBlock

        main.schList = [(30, 90), (120, 150)]  # initiate the list

        expectedSchBlock = (30, 90)
        retSchBlock = main.getScheduleBlock()

        self.assertTupleEqual(expectedSchBlock, retSchBlock)

    def testgetSchedules(self):
        # getSchedules
        sTxt = "[(30, 90), (120, 150)]"
        expList = [(30, 90), (120, 150)]

        retList = main.getSchedules(sTxt)

        self.assertListEqual(expList, retList)

    def testgetScheduleString(self):
        # test
        expStr = "[(540, 600), (660, 780)]"

        retStr = main.getScheduleString()

        self.assertEqual(expStr, retStr)

    @patch('main.getScheduleString', autospec=True)
    def testmain(self, schStrMock):
        # test the main function

        schStrMock.getScheduleString = MagicMock(
            return_value="[(540, 600), (660, 780)]")

        dt = datetime.now()

        ue = main.UserEvent(dt, main.UserEvent.UNLOCKED)

        main.userEvent = ue

        main.main()

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
