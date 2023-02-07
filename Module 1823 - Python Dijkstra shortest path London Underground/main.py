from dijkstra import *
import random
from gui import *
from sys import exit

# call main Ui class
def main():
    app =  QApplication([])
    app.setStyle('Fusion')
    window = Ui()
    window.show()
    (app.exec_())

if __name__ == "__main__":
    main()