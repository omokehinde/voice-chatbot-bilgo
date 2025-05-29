import os
import soundfile as sf
import numpy as np

def save_audio_file(file, save_path, fs=44100):
    data, samplerate = sf.read(file)
    sf.write(save_path, data / np.max(np.abs(data)), fs)
