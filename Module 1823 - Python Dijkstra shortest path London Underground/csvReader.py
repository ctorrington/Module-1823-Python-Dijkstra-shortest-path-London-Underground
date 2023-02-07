import csv

class csvReader:
    def __init__(self, file):
        self._rows = []
        self.readFile = file

        # check if list is empty
        if not self._rows:
            self._readcsv()

    # read csv method
    def _readcsv(self):
        self.file = open(self.readFile)
        self.csv_reader = csv.reader(self.file, delimiter = ",")

        # loop over csv appending _rows variable
        for i in self.csv_reader:
            if i[0] == "":
                break

            self._rows.append(i)
            
    # returns the value from _rows in csv file
    def get_csv(self):
        return self._rows
