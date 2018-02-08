"""
    This service will read from the saved schedule info and watch for Lock/Unlock Event
    Check if the unlock happened during the schedule, if not notify user 

"""

from time import sleep
from datetime import datetime
from collections import Counter


class UserEvent:
    LOCKED = 1
    UNLOCKED = 2
    STOP = 3

    def __init__(self, e, dt):
        # captures teh event and event time
        self.eventDt = dt
        self.event = e


schBlock = None  # captures the schedule for the current Unlock Event
userEvent = None  # Captures the latest user event. Lock or Unlock event
schList = []  # list of schedules


def getScheduleString():
    # read the file and return the schedule string
    try:
        with open("../schedule.dat", 'r') as f:
            sTxt = f.readline()

    except(Exception) as e:
        return None

    return sTxt


def getSchedules(sTxt):

    if sTxt is None:
        return None

    try:
        initList = list(eval(sTxt))

        schList = []
        c = Counter(sTxt)
        # if there is one comma, then its one schedule
        if c[','] == 1:  # count
            schList.append(tuple(initList))
        else:
            schList = initList[:]  # copy the values

    except(Exception) as e:
        return None

    return schList


def notifyUserToLock():
    pass


def getScheduleBlock():
    # scan thru the list of schedules and identify
    # the one which matches the time now
    minCount = 0
    hrNow = datetime.now().hour

    minCount = (hrNow * 60) + datetime.now().minute

    if len(schList) <= 0:
        return None

    schNow = [s for s in schList if s[1] >= minCount and s[0] <= minCount]

    if len(schNow) <= 0:
        return None
    else:
        return schNow[0]


def main():
    global schList, schBlock, userEvent

    # read the file from the folder and
    # read the schedule

    sTxt = getScheduleString()
    schList = getSchedules(sTxt)

    if schList:
        while True:  # look infinitely, unless break event

            schBlock = getScheduleBlock()
            # if schBlock is none, UNLOCK event is invalid

            if not schBlock and userEvent and userEvent.event == UserEvent.UNLOCKED:
                # here scan thru the schedule and capture the schedule Block
                notifyUserToLock()
                print("Cannot use it man...")
            elif userEvent and userEvent.event == UserEvent.LOCKED:
                # this happens when the user just locked the phone..
                # then delete the data collected for Unlock
                userEvent = None
                schBlock = None
            elif userEvent and userEvent.event == UserEvent.STOP:
                break  # ends teh loop, and stops the service

            sleep(30)  # sleep for 30 secs


if __name__ == "__main__":
    main()
