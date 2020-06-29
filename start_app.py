from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from app import laclef_window

app = QtWidgets.QApplication([])
application = laclef_window()

# Change these parameters accordingly
application.rpi = False
application.test = False


application.scanned.connect(application.on_event_received)
application.showFullScreen() if application.rpi else application.show()

sys.exit(app.exec())
