import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time
import sys
from random import random
from pygame import key


class DigitalInstrumentWidget(QWidget):

  def __init__(self):
    super(DigitalInstrumentWidget, self).__init__()
    
    self.initUI()
    self.initInsturment()

  def initUI(self):
    self.resize(500, 300)
    self.move(300, 300)
    self.setWindowTitle('EECS 481 Digital Instrument')
    self.show()

  def initInsturment(self):
    self.octave = 0;

  def noteMapper(self, key):
    print "key mapper called"

  def commandMapper(self, key):
 #check if clicked key is an unmappable key
    if key == Qt.Key_Down:
      self.octave = (self.octave - 1) % 8
      return True

    elif key == Qt.Key_Up:
      self.octave = (self.octave + 1) % 8
      return True

    elif key == Qt.Key_0:
      self.octave = 0
      return True

    elif key == Qt.Key_1:
      self.octave = 1
      return True

    elif key == Qt.Key_2:
      self.octave = 2
      return True

    elif key == Qt.Key_3:
      self.octave = 3
      return True

    elif key == Qt.Key_4:
      self.octave = 4
      return True

    elif key == Qt.Key_5:
      self.octave = 5
      return True     

    elif key == Qt.Key_6:
      self.octave = 6
      return True

    elif key == Qt.Key_7:
      self.octave = 7
      return True

    elif key == Qt.Key_Escape:
      QCoreApplication.quit()
      return True

    else:
      return False

  def keyReleaseEvent(self, event):
    if event.isAutoRepeat():
      return  

    print('key released: ' + event.text())

  def keyPressEvent(self, event):
    if event.isAutoRepeat():
      return

    if self.commandMapper(event.key()):
      print "command"

    elif self.noteMapper(event.key()):
      print "note"

    else:
      print "key not mapped"

def main():
  app = QApplication(sys.argv)

  window = DigitalInstrumentWidget()

  sys.exit(app.exec_())

if __name__ == '__main__':
  main()