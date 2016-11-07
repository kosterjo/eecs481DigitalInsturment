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
    #init octave to 0
    self.octave = 0;

    #keys A-K map to notes G-F
    self.noteDict = {
      Qt.Key_A: 'G',
      Qt.Key_S: 'A', 
      Qt.Key_D: 'B', 
      Qt.Key_F: 'C',
      Qt.Key_G: 'D', 
      Qt.Key_H: 'E',
      Qt.Key_J: 'F',
    }

    #init octave dict to map to the number keys
    #key up and down are special cases caught by updateOctave
    self.octaveDict = {
      Qt.Key_Up:   -2,
      Qt.Key_Down: -1,
      Qt.Key_0:     0,
      Qt.Key_1:     1,
      Qt.Key_2:     2,
      Qt.Key_3:     3,
      Qt.Key_4:     4,
      Qt.Key_5:     5,
      Qt.Key_6:     6,
      Qt.Key_7:     7,
    }

    #so far, utils dict only maps esc to quitting
    self.utilsDict = {
      Qt.Key_Escape: QCoreApplication.instance().quit
    }

  def updateOctave(self, value):
    #if value is -2, up key was pressed
    #so move octave up one step
    if value == -2:
      self.octave = (self.octave + 1) % 8

    #if value is -1, down key was pressed
    #so move octave down one step
    elif value == -1:
      self.octave = (self.octave - 1) % 8

    #update octave to value mod 8
    else:
      self.octave = value % 8

    print "Octave: " + str(self.octave)

  def startNote(self, note):
    print note + " started"

  def endNote(self, note):
    print note + " ended"

  def noteMapper(self, key):
    #if key pressed is mapped to a note, 
    #return that note, else return false
    if key in self.noteDict:
      return self.noteDict[key]

    return False

  def commandMapper(self, key):
    #if key pressed is mapped to an octave,
    #change current octave to that key
    if key in self.octaveDict:
      argument = self.octaveDict[key]
      self.updateOctave(argument)
      return True

    #if key is in the utility dictionary
    #call function mapped to that key
    elif key in self.utilsDict:
      self.utilsDict[key]()
      return True

    #else key pressed is not a command
    else:
      return False

  def keyPressEvent(self, event):
    if event.isAutoRepeat():
      return

    #if the key pressed is a command, return
    #command mapper takes care of the command's actions
    if self.commandMapper(event.key()):
      return

    #note mapper maps a key to a note
    #returns false if key is not maped to a note
    note = self.noteMapper(event.key())
    
    #if key is mapped to a note, start the note
    if note:
      self.startNote(note)
      return

    #else the key pressed does nothing currently
    print "key not mapped"

  def keyReleaseEvent(self, event):
    if event.isAutoRepeat():
      return  

    #key release only matters for notes
    #because notes can be held
    note = self.noteMapper(event.key())
    
    #if the key is mapped, end the note
    if note:
      self.endNote(note)
      return

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