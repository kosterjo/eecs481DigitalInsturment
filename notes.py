from mingus.core import progressions, intervals
from mingus.core import chords as ch
from mingus.containers import NoteContainer, Note
from mingus.midi import fluidsynth
import time
import sys

fluidsynth.init("HS Synth Collection I.sf2", "alsa")
n = Note("C-5")
n.channel = 5
n.velocity = 100
fluidsynth.play_Note(60)
fluidsynth.play_Note(Note("C-5"))
#fluidsynth.play_Note(Note("E-5"))
#fluidsynth.play_Note(Note("G-5"))
time.sleep(5)
fluidsynth.stop_Note(1, 1)
#fluidsynth.stop_Note(Note("E-5"), 1)
#fluidsynth.stop_Note(Note("G-5"), 1)

#fluidsynth.play_NoteContainer(ch.major_triad("C"))
#time.sleep(5)
#fluidsynth.stop_NoteContainer(ch.major_triad("C"), 1)

