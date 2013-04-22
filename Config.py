# -*- coding: utf-8 *-*

import xml.etree.ElementTree as ET


class BaseStation():

    def __init__(self, X, Y, ID, IP):
        self.X = X
        self.Y = Y
        self.ID = ID
        self.IP = IP
        self.filename = 'BaseStation' + self.ID + '.txt'


def get_config(configFile):
    """Gets the basestation details from an xml config file.

    Outputs a list of basestations.
    """
    tree = ET.parse(configFile)
    root = tree.getroot()

    stations = []

    for bs in root.iter('BaseStation'):
        X = bs.find('X').text
        Y = bs.find('Y').text
        ID = bs.find('ID').text
        IP = bs.find('IP').text

        stations.append(BaseStation(X, Y, ID, IP))

    return stations
