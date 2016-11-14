from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QBrush, QPalette
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


class PianoKeyItem(QGraphicsRectItem):
  def mousePressEvent(self, event):
    if hasattr(self, 'note') and self.note is not None:
      print('clicked: ' + str(self.note))


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


class DigitalInstrumentWidget(QGraphicsView):

  def __init__(self):
    super(DigitalInstrumentWidget, self).__init__()
    self.initUI()
    self.initInsturment()

  def initUI(self):
    self.resize(800, 500)
    self.move(100, 100)
    self.setWindowTitle('EECS 481 Digital Instrument')
    self.show()

    # Set up graphics stuff
    scene = QGraphicsScene()
    windowWidth = self.size().width()
    windowHeight = self.size().height()
    keyAreaBounds = QRect(0, 0, windowWidth * .85, windowHeight * 0.4)

    # Draw white keys
    self.whiteKeys = []
    whiteKeyWidth = keyAreaBounds.width() / 14
    whiteKeyIndices = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 22]
    for i in range(14):
      key = PianoKeyItem(keyAreaBounds.x() + i * whiteKeyWidth, keyAreaBounds.y(), whiteKeyWidth, keyAreaBounds.height())
      key.note = DiscreteNotes(whiteKeyIndices[i] % 12)
      key.setBrush(Qt.white)
      self.whiteKeys.append(key)
      scene.addItem(key)

    # Draw black keys
    self.blackKeys = []
    blackKeyWidth = whiteKeyWidth / 2
    blackKeyHeight = keyAreaBounds.height() * 0.6
    blackKeyIndices = [1, 3, 6, 8, 10, 13, 15, 18, 20, 23]
    for i in range(10):
      startX = keyAreaBounds.x() + 2 * i * blackKeyWidth + blackKeyWidth * 1.5

      if i > 6:
        startX += 3*whiteKeyWidth

      elif i > 4:
        startX += 2*whiteKeyWidth

      elif i > 1:
        startX += whiteKeyWidth

      key = PianoKeyItem(startX, keyAreaBounds.y(), blackKeyWidth, blackKeyHeight)
      key.note = DiscreteNotes(blackKeyIndices[i] % 12)
      key.setBrush(Qt.black)
      self.blackKeys.append(key)
      scene.addItem(key)

    self.setScene(scene)

    self.updateUI()


  def updateUI(self):
    # Make sure the pressedKeys exists
    if not hasattr(self, 'pressedKeys') or self.pressedKeys is None:
      self.pressedKeys = [False] * 24

    # Update color of white keys (pressed or not)
    whiteKeyIndices = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 22]
    for i in range(len(self.whiteKeys)):
      key = self.whiteKeys[i]
      if self.pressedKeys[whiteKeyIndices[i]]:
        key.setBrush(Qt.gray)
      else:
        key.setBrush(Qt.white)

    # Update color of black keys
    blackKeyIndices = [1, 3, 6, 8, 10, 13, 15, 18, 20, 23]
    for i in range(len(self.blackKeys)):
      key = self.blackKeys[i]
      if self.pressedKeys[blackKeyIndices[i]]:
        key.setBrush(Qt.gray)
      else:
        key.setBrush(Qt.black)

    self.scene().update(self.scene().sceneRect())


  def initInsturment(self):
    #init octave to 0
    self.octave = 0;

    #keys A-K map to notes G-F
    #keys W, E and T-U map to notes C#-A#
    self.noteDict = {
      Qt.Key_Q: DiscreteNotes.C,
      Qt.Key_W: DiscreteNotes.Cs,
      Qt.Key_A: DiscreteNotes.D,
      Qt.Key_E: DiscreteNotes.Ds,
      Qt.Key_S: DiscreteNotes.E,
      Qt.Key_Z: DiscreteNotes.F,
      Qt.Key_R: DiscreteNotes.Fs,
      Qt.Key_X: DiscreteNotes.G,
      Qt.Key_D: DiscreteNotes.Gs,
      Qt.Key_F: DiscreteNotes.A,
      Qt.Key_T: DiscreteNotes.As,
      Qt.Key_C: DiscreteNotes.B,
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
      Qt.Key_F1: "HS Synth Collection I.sf2",
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
    self.updateUI()
    create_sound.play_note(note.value)

  def endNote(self, note):
    print(str(note) + " ended")

    # Mark the key as released for the UI
    self.pressedKeys[note.value] = False
    self.updateUI()
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

def main():
  fluidsynth.init("HS Synth Collection I.sf2", "alsa")
  app = QApplication(sys.argv)
  window = DigitalInstrumentWidget()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
