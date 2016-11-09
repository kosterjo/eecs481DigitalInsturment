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
from enum import Enum
from Sound import Sound

create_sound = Sound()


class DiscreteNotes(Enum):
  C  = 0
  Cs = 1
  D  = 2
  Ds = 3
  E  = 4
  F  = 5
  Fs = 6
  G  = 7
  Gs = 8
  A  = 9
  As = 10
  B  = 11


class DigitalInstrumentWidget(QWidget):

  def __init__(self):
    super(DigitalInstrumentWidget, self).__init__()
    self.initUI()
    self.initInsturment()

  def initUI(self):
    self.resize(800, 500)
    self.move(100, 100)
    self.setWindowTitle('EECS 481 Digital Instrument')
    self.show()

  def initInsturment(self):
    #init octave to 0
    self.octave = 0;

    #keys A-K map to notes G-F
    #keys W, E and T-U map to notes C#-A#
    self.noteDict = {
      Qt.Key_A: DiscreteNotes.C,
      Qt.Key_S: DiscreteNotes.D,
      Qt.Key_D: DiscreteNotes.E,
      Qt.Key_F: DiscreteNotes.F,
      Qt.Key_G: DiscreteNotes.G,
      Qt.Key_H: DiscreteNotes.A,
      Qt.Key_J: DiscreteNotes.B,
      Qt.Key_W: DiscreteNotes.Cs,
      Qt.Key_E: DiscreteNotes.Ds,
      Qt.Key_T: DiscreteNotes.Fs,
      Qt.Key_Y: DiscreteNotes.Gs,
      Qt.Key_U: DiscreteNotes.As,
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
    }

    self.soundDict = {
      Qt.Key_F1: "bla",
    }

    #so far, utils dict only maps esc to quitting
    self.utilsDict = {
      Qt.Key_Escape: QCoreApplication.instance().quit
    }

  def updateOctave(self, value):
    #if value is -2, up key was pressed
    #so move octave up one step
    if value == -2:
      self.octave = (self.octave + 1) % 7

    #if value is -1, down key was pressed
    #so move octave down one step
    elif value == -1:
      self.octave = (self.octave - 1) % 7

    #update octave to value mod 8
    else:
      self.octave = value % 7

    create_sound.set_octave(self.octave)
    print("Octave: " + str(self.octave))

  def startNote(self, note):
    print(str(note) + " started")

    # Mark the key as pressed for the UI
    self.pressedKeys[note.value] = True
    self.repaint()
    create_sound.play_note(note.value)

  def endNote(self, note):
    print(str(note) + " ended")

    # Mark the key as released for the UI
    self.pressedKeys[note.value] = False
    self.repaint()
    create_sound.stop_note(note.value)

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

    elif key in self.soundDict:
      argument = self.soundDict[key]
      fluidsynth.init(argument, "alsa")

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
    print("key not mapped")

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

  # Draws the piano keys in the window
  # Called automatically on window resize etc.
  def paintEvent(self, e):
    qp = QPainter()
    qp.begin(self)
    qp.setBrush(QBrush(Qt.SolidPattern))
    windowWidth = self.size().width()
    windowHeight = self.size().height()
    keyAreaBounds = QRect(windowWidth * 0.1, windowHeight * 0.1, windowWidth * 0.8, windowHeight * 0.8)

    # Make sure the pressedKeys exists
    if not hasattr(self, 'pressedKeys') or self.pressedKeys is None:
      self.pressedKeys = [False] * 12

    # Draw white keys
    whiteKeyWidth = keyAreaBounds.width() / 7
    whiteKeyIndices = [0, 2, 4, 5, 7, 9, 11]
    for i in range(7):
      # Darken keys if pressed
      if self.pressedKeys[whiteKeyIndices[i]]:
        qp.setBrush(Qt.gray)
      else:
        qp.setBrush(Qt.white)

      # Draw the key
      qp.drawRect(QRect(keyAreaBounds.x() + i * whiteKeyWidth, keyAreaBounds.y(), whiteKeyWidth, keyAreaBounds.height()))

    # Draw black keys
    blackKeyWidth = whiteKeyWidth / 2
    blackKeyHeight = keyAreaBounds.height() * 0.6
    blackKeyIndices = [1, 3, 6, 8, 10]
    for i in range(5):
      startX = keyAreaBounds.x() + 2 * i * blackKeyWidth + blackKeyWidth * 1.5
      if i > 1:
        startX += whiteKeyWidth

      # Darken keys if pressed
      if self.pressedKeys[blackKeyIndices[i]]:
        qp.setBrush(Qt.gray)
      else:
        qp.setBrush(Qt.black)

      # Draw the key
      qp.drawRect(QRect(startX, keyAreaBounds.y(), blackKeyWidth, blackKeyHeight))

    qp.end()


def main():
  fluidsynth.init("HS Synth Collection I.sf2", "alsa")
  app = QApplication(sys.argv)
  window = DigitalInstrumentWidget()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
