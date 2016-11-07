from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time
import sys

class Sound(object):
  self.base_octave = 0

  def set_octave(self, octave):
    self.base_octave = octave
    return

  def convert_note(self, note):
    play = note + 60 + (8 * self.base_octave)
    return play

  def play_note(self, note_enum):
    fluidsynth.play_Note(self.convert_note(note_enum))
    return

  def stop_note(self, note_enum):
    fluidsynth.stop_Note(self.convert_note(note_enum), 1)
    return

Sound()
