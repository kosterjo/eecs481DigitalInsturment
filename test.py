import sys
from PyQt5.QtWidgets import *
from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time
import sys
from random import random

class DigitalInstrumentWidget(QWidget):

	def keyReleaseEvent(self, event):
		if event.isAutoRepeat():
			return
		print('key released: ' + event.text())

	def keyPressEvent(self, event):
		if event.isAutoRepeat():
			return
		print('key pressed: ' + event.text())


def main():
	app = QApplication(sys.argv)

	window = DigitalInstrumentWidget()
	window.resize(500, 300)
	window.move(300, 300)
	window.setWindowTitle('EECS 481 Digital Instrument')
	window.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()