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

  def keyMapper(self, key):
    print("key mapper called")

  def keyReleaseEvent(self, event):
    if event.isAutoRepeat():
      return  

    print('key released: ' + event.text())

  def keyPressEvent(self, event):
    if event.isAutoRepeat():
      return

    #check if clicked key is an unmappable key
    if event.key() == Qt.Key_Down:
      self.octave = (self.octave - 1) % 8

    elif event.key() == Qt.Key_Up:
      self.octave = (self.octave + 1) % 8

    elif event.key() == Qt.Key_0:
      self.octave = 0

    elif event.key() == Qt.Key_1:
      self.octave = 1

    elif event.key() == Qt.Key_2:
      self.octave = 2

    elif event.key() == Qt.Key_3:
      self.octave = 3

    elif event.key() == Qt.Key_4:
      self.octave = 4

    elif event.key() == Qt.Key_5:
      self.octave = 5

    elif event.key() == Qt.Key_6:
      self.octave = 6

    elif event.key() == Qt.Key_7:
      self.octave = 7

    elif event.key() == Qt.Key_Escape:
      QCoreApplication.quit()
      return 

    else:
      self.keyMapper(event.key())

    print('key pressed: ' + event.text())

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