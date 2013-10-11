from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.internet.protocol import ProcessProtocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.task import LoopingCall

from datadealer import DataDealer
from config import get_config
from calcposition import CalcPosition
from output import CsvOutput
from datetime import datetime
import csv


class Calculator(ProcessProtocol):

    def __init__(self, stations, outputfile):
        self.stations = stations
        self.outputfile = outputfile
        self.output = CsvOutput(self.outputfile)
        self.calc = CalcPosition(self.stations, self.output)

    def start_calc(self):
        self.calc.start_calc()
        self.csvfile = open(self.outputfile, "ab")
        self.csvwriter = csv.writer(self.csvfile, dialect="excel")
        self.csvwriter.writerow([10, 20, "D202"])
        self.csvfile.close()
        print 'Calculation Started.'


class BaseStationProtocol(LineReceiver):

    def connectionMade(self):
        #print("4. base station protocol invoked")
        self.transport.write("\r\n")

    def lineReceived(self, line):
        #print("5. data received")
        #print(line)

        t = datetime.now()
        #Format as Year:Month:Day:Hour:Minute:Second:Microsecond
        timestamp = t.strftime("%Y:%m:%d:%H:%M:%S:%f")

        self.factory.textfile.write(timestamp + " ")
        self.factory.textfile.write(line)
        self.factory.textfile.write("\n")
        self.factory.dlist.receive_data(self.factory.ID, line)
        # you can get at the filename from the factory
        #using self.factory.filename


class BaseStationFactory(ReconnectingClientFactory):
    protocol = BaseStationProtocol

    def __init__(self, station):
        self.station = station
        self.filename = station.filename
        self.ID = station.ID
        self.textfile = open(self.filename, "w")
        self.dlist = DataDealer(self.ID)

    def startedConnecting(self, transport):
        print 'Started connection to Base Station', self.ID

    def buildProtocol(self, addr):
        #print("3. connected to %s" % addr)
        bp = BaseStationProtocol()
        bp.factory = self
        self.resetDelay()
        return bp

    def clientConnectionLost(self, transport, reason):
        print 'Lost connection.  Reason:', reason
        ReconnectingClientFactory.clientConnectionLost(self, transport,
                                                        reason)

    def clientConnectionFailed(self, transport, reason):
        print 'Failed connection to ', self.ID, '.  Reason:', reason
        ReconnectingClientFactory.clientConnectionFailed(self,
                                                    transport, reason)

if __name__ == "__main__":
    port = 84
    stations = get_config('conf.xml')
    calculation = Calculator(stations, 'output.csv')

    task = LoopingCall(calculation.start_calc)
    task.start(0.5, False)

    for bs in stations:
        #print("1. ready to connect to %s" % address)
        reactor.connectTCP(bs.IP, port, BaseStationFactory(bs), 15)
    reactor.run()
