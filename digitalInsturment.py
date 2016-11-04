import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QBrush
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

    self.noteDict = {
      Qt.Key_A: 'C',
      Qt.Key_S: 'D', 
      Qt.Key_D: 'E', 
      Qt.Key_F: 'F',
      Qt.Key_G: 'G', 
      Qt.Key_H: 'A',
      Qt.Key_J: 'B',
      Qt.Key_K: 'C',
    }

    self.octaveDict = {
      Qt.Key_0: 0,
      Qt.Key_1: 1,
      Qt.Key_2: 2,
      Qt.Key_3: 3,
      Qt.Key_4: 4,
      Qt.Key_5: 5,
      Qt.Key_6: 6,
      Qt.Key_7: 7,
    }

  def updateOctave(self, value):
    self.octave = value % 8
    print self.octave

  def noteMapper(self, key):
    if key in self.noteDict:
      print self.noteDict[key]

  def commandMapper(self, key):
  #check if clicked key is an unmappable key
    if key == Qt.Key_Down:
      self.updateOctave(self.octave - 1) 
      return True

    elif key == Qt.Key_Up:
      self.updateOctave(self.octave + 1)
      return True

    elif key in self.octaveDict:
      argument = self.octaveDict[key]
      self.updateOctave(argument)
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

  # Called automatically on window resize etc.
  def paintEvent(self, e):
    qp = QPainter()
    qp.begin(self)
    self.drawPianoKeys(qp)
    qp.end()
        
  # Draws the piano keys in the window
  def drawPianoKeys(self, qp):
    windowWidth = self.size().width()
    windowHeight = self.size().height()
    keyAreaBounds = QRect(windowWidth * 0.1, windowHeight * 0.1, windowWidth * 0.8, windowHeight * 0.8)

    # Brush setup
    brush = QBrush(Qt.SolidPattern)
    qp.setBrush(brush)

    # Draw white keys
    qp.setBrush(Qt.white)
    whiteKeyWidth = keyAreaBounds.width() / 7
    for i in range(7):
      qp.drawRect(QRect(keyAreaBounds.x() + i * whiteKeyWidth, keyAreaBounds.y(), whiteKeyWidth, keyAreaBounds.height()))

    # Draw black keys
    qp.setBrush(Qt.black)
    blackKeyWidth = whiteKeyWidth / 2
    blackKeyHeight = keyAreaBounds.height() * 0.6
    for i in range(5):
      startX = keyAreaBounds.x() + 2 * i * blackKeyWidth + blackKeyWidth * 1.5
      if i > 1:
        startX += whiteKeyWidth
      qp.drawRect(QRect(startX, keyAreaBounds.y(), blackKeyWidth, blackKeyHeight))

def main():
  app = QApplication(sys.argv)

  window = DigitalInstrumentWidget()

  sys.exit(app.exec_())

if __name__ == '__main__':
  main()