import csv
from datetime import datetime


class CsvOutput():

    def __init__(self, filename):
        self.filename = filename

    def write(self, tag):
        """Outputs a line containing the position of a tag, with timestamp."""
        self.csvfile = open(self.filename, "ab")
        self.csvwriter = csv.writer(self.csvfile, dialect="excel")
        t = datetime.now()
        #Format as Year:Month:Day:Hour:Minute:Second:Microsecond
        timestamp = t.strftime("%Y:%m:%d:%H:%M:%S:%f")
        self.csvwriter.writerow([tag.x, tag.y, tag.ID, timestamp])
        #self.textfile.writerow([self.line, tag.x, tag.y, tag.ID, timestamp])

        self.csvfile.close()
        self.csvfile.flush()

        print tag.x, tag.y, tag.ID, timestamp
