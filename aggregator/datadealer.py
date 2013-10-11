# -*- coding: utf-8 *-*

from collections import deque
import string


class DataString():

    def __init__(self, RSSI, TagID, StationID):
        self.rssi = int(RSSI)
        self.tag = TagID
        self.station = StationID


class DataDealer():

    dataLists = {}

    def __init__(self, ID):
        if ID in self.dataLists:
            pass
        else:
            self.dataLists[ID] = deque()
            #dataLists[ID] = deque(maxlen=100)
        #import pdb; pdb.set_trace()

    def receive_data(self, ID, dataString):
        """Receives data and appends it to a list in the Dictionary."""

        s = string.split(dataString, ',')

        #dir(s)
        if len(s) == 3:
            d = DataString(s[0], s[1], s[2])

            self.dataLists[ID].append(d)
        #import pdb; pdb.set_trace()

    def pull_data(self, ID):
        """Pulls the data from the dataList Dictionary.

        Takes an input of the BaseStationID as the key.
        Outputs a list of DataString objects.
        """

        data = []
        if ID in self.dataLists:
            data.extend(self.dataLists[ID])
            self.dataLists[ID].clear()
            #for i in dataLists[ID]:
                #data.append(dataLists[ID].pop())

        #import pdb; pdb.set_trace()

        return data
