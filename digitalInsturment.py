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

    self.notes = {
      Qt.Key_A: 'C',
      Qt.Key_S: 'D', 
      Qt.Key_D: 'E', 
      Qt.Key_F: 'F',
      Qt.Key_G: 'G', 
      Qt.Key_H: 'A',
      Qt.Key_J: 'B',
      Qt.Key_K: 'C',
    }

    self.commands = {
      Qt.Key_Down: self.updateOctave,
    }
    self.command_args = {
      Qt.Key_Down: self.octave - 1,
    }

  def updateOctave(self, value):
    self.octave = value % 8

  def noteMapper(self, key):
    print self.notes[key]

  def commandMapper(self, key):
  #check if clicked key is an unmappable key
    if key == Qt.Key_Down:
      self.updateOctave(self.octave - 1)
      print self.octave 
      return True

    elif key == Qt.Key_Up:
      self.updateOctave(self.octave + 1)
      print self.octave 
      return True

    elif key == Qt.Key_0:
      self.updateOctave(0)
      return True

    elif key == Qt.Key_1:
      self.updateOctave(1)
      return True

    elif key == Qt.Key_2:
      self.updateOctave(2)
      return True

    elif key == Qt.Key_3:
      self.updateOctave(3)
      return True

    elif key == Qt.Key_4:
      self.updateOctave(4)
      return True

    elif key == Qt.Key_5:
      self.updateOctave(5)
      return True     

    elif key == Qt.Key_6:
      self.updateOctave(6)
      return True

    elif key == Qt.Key_7:
      self.updateOctave(7)
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