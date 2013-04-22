
from DataDealer import DataDealer
from Calculations import Circle, CleanedCircle
from Calculations import find_position
from RadiiCleaner import clean_circles


class Tag():

    def __init__(self, x, y, tag):
        self.x = x
        self.y = y
        self.ID = tag


class CalcPosition():

    def __init__(self, stations, output):
        self.stations = stations
        self.output = output

    def start_calc(self):
        """Starts the calculation process, then outputs the result."""

        self.positions = self.calculate_points(self.stations)
        self.output_data(self.positions)

    def calculate_points(self, stations):
        """Calculates the position of each tag.

        Takes an input of the list of stations.

        Process:
            Get data from each basestation.
            Create circles.
            Sort circles by tags.
            Pass through cleaner.
            Run trilateration calculations.

        Outputs a list of the position of each tag.
        """

        tagdict = {}
        tagpositions = []

        for bs in stations:
            data = self.get_data(bs)
            circles = self.create_circles(data, bs)

            self.sort_tags(circles, bs, tagdict)

        for tag in tagdict:
            cleanedcircles = []
            for bs in tagdict[tag]:
                cc = self.clean_radii(bs, tagdict[tag][bs], tag)
                cleanedcircles.append(cc)

            if len(cleanedcircles) > 0:
                position = find_position(cleanedcircles)
                if position is False:
                    pass
                else:
                    tagpositions.append(Tag(position.x, position.y, tag))

        return tagpositions

    def get_data(self, station):
        """Gets the incoming data from the DataDealer."""

        dd = DataDealer(station.ID)
        data = dd.pull_data(station.ID)

        return data

    def sort_tags(self, data, bs, tagdict):
        """Sorts list of data by TagID and basestation into the tagdict.

        Takes an input of a mixed list of tag data from a basestation.
        """

        for x in data:
            tag = x.tag
            if tag in tagdict:
                if bs in tagdict[tag]:
                    tagdict[tag][bs].append(x)
                else:
                    tagdict[tag][bs] = []
                    tagdict[tag][bs].append(x)
            else:
                bsdict = {}
                bsdict[bs] = []
                tagdict[tag] = bsdict
                tagdict[tag][bs].append(x)

    def create_circles(self, datalist, bs):
        """Creates a list of circles from the RSSI and base station data.

        Takes an input of a list of RSSI values and a base station.
        Outputs a list of circles"""

        circles = []
        for data in datalist:
            circles.append(Circle(bs.X, bs.Y, data.rssi, data.tag, bs.ID))

        return circles

    def clean_radii(self, bs, circles, tag):
        """Returns the most likely actual radius from the list of circles.

        Takes an input of a list of circles for a single tag and base station.
        Outputs a single circle.
        """
        radius = clean_circles(circles)
        cleanedcircle = CleanedCircle(bs.X, bs.Y, radius, tag, bs.ID)
        print tag, bs.ID, cleanedcircle.r

        return cleanedcircle

    def output_data(self, data):
        """Outputs the position of each tag."""

        for tag in data:
            self.output.write(tag)








