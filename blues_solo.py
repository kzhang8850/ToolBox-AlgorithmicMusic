""" Synthesizes a blues solo algorithmically """

from Nsound import *
import numpy as np
import random


def add_note(out, instr, key_num, duration, bpm, volume):
    """ Adds a note from the given instrument to the specified stream

        out: the stream to add the note to
        instr: the instrument that should play the note
        key_num: the piano key number (A 440Hzz is 49)
        duration: the duration of the note in beats
        bpm: the tempo of the music
        volume: the volume of the note
	"""
    freq = (2.0**(1/12.0))**(key_num-49)*440.0
    stream = instr.play(duration*(60.0/bpm),freq)
    stream *= volume
    out << stream

# this controls the sample rate for the sound file you will generate
sampling_rate = 44100.0
Wavefile.setDefaults(sampling_rate, 16)

bass = GuitarBass(sampling_rate)	# use a guitar bass as the instrument
solo = AudioStream(sampling_rate, 1)

""" these are the piano key numbers for a 3 octave blues scale in A
	See: http://en.wikipedia.org/wiki/Blues_scale """
blues_scale = [25, 28, 30, 31, 32, 35, 37, 40, 42, 43, 44, 47, 49, 52, 54, 55, 56, 59, 61]
beats_per_minute = 45				# Let's make a slow blues solo
duration = [.5, .6, .7 ,.8, .9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5] #added a varying duration on each note
volume = [.7, .8, .9, 1.0, 1.1, 1.2, 1.3] #added a varying volume

curr_note = 6 #changed starting position
add_note(solo, bass, blues_scale[curr_note], 1.0, beats_per_minute, 1.0)


#added a whole of licks, all at random durations
licks = [[ [-1,0.5*random.choice(duration)], [2,0.5*random.choice(duration)], [-1, 0.5*random.choice(duration)], [2, 0.5*random.choice(duration)] ], 
		[ [1,0.5*random.choice(duration)], [-2,0.5*random.choice(duration)], [-2, 0.5*random.choice(duration)], [1, 0.5*random.choice(duration)] ], 
		[ [2,0.5*random.choice(duration)], [2,0.5*random.choice(duration)], [-3, 0.5*random.choice(duration)], [2, 0.5*random.choice(duration)] ], 
		[ [4,0.5*random.choice(duration)], [-1,0.5*random.choice(duration)], [2, 0.5*random.choice(duration)], [-5, 0.5*random.choice(duration)]], 
		[ [-2,0.5*random.choice(duration)], [-3,0.5*random.choice(duration)], [6, 0.5*random.choice(duration)], [-3, 0.5*random.choice(duration)] ],
		[ [2,0.5*random.choice(duration)], [2,0.5*random.choice(duration)], [2, 0.5*random.choice(duration)], [2, 0.5*random.choice(duration)] ],
		[ [4,0.5*random.choice(duration)], [1,0.5*random.choice(duration)], [-3, 0.5*random.choice(duration)], [-2, 0.5*random.choice(duration)] ],
		[ [0,0.5*random.choice(duration)], [1,0.5*random.choice(duration)], [2, 0.5*random.choice(duration)], [0, 0.5*random.choice(duration)] ],
		[ [3,0.5*random.choice(duration)], [2,0.5*random.choice(duration)], [-1, 0.5*random.choice(duration)], [-1, 0.5*random.choice(duration)] ],
		[ [-3,0.5*random.choice(duration)], [4,0.5*random.choice(duration)], [0, 0.5*random.choice(duration)], [-4, 0.5*random.choice(duration)] ]]

for i in range(95):
    lick = random.choice(licks)
    for note in lick:
        curr_note += note[0]
        if curr_note > len(blues_scale)-1 or curr_note < 0:  #checks for out of bounds cases
        	curr_note = random.choice([0,6,12,18])  #note will now automatically swtich a random root note if it passes a boundary
        add_note(solo, bass, blues_scale[curr_note], note[1], beats_per_minute, random.choice(volume))


backing_track = AudioStream(sampling_rate, 1)
Wavefile.read('backing.wav', backing_track)

m = Mixer()

solo *= .6             # volumes were adjusted for slightly balancing of songs (although tbh hard to tell when my song is so random lol)
backing_track *= 1.6

m.add(2.25, 0, solo)    # delay the solo to match up with backing track    
m.add(0, 0, backing_track)

#changed the length of the track
m.getStream(265.0) >> "slow_blues.wav"