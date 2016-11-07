from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time
import sys

fluidsynth.init("HS Synth Collection I.sf2", "alsa")
fluidsynth.play_Note(Note("C-5"))
time.sleep(5)
fluidsynth.stop_Note(Note("C-5"), 1)

fluidsynth.play_Note(chords.major_triad("C"))
time.sleep(5)
fluidsynth.stop_Note(chords.major_triad("C"), 1)

