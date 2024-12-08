import wave
import os
import socket

import whisper
import librosa
from pydub import AudioSegment
from threading import Thread
import keyboard
import pyaudio
import audioop
import scipy.fftpack as fft
import soundfile as sf
from scipy.signal import medfilt
import numpy as np

model = whisper.load_model("base")
steps_in_sec:int =1
len_in_sec:int =6

def clean_input(index):
    filename = f"audio_sequences/sequence_{index}.wav"

    y, sr = librosa.load(filename, sr=None)

    #   add path2

    s_full, phase = librosa.magphase(librosa.stft(y))

    noise_power = np.mean(s_full[:, :int(sr * 0.1)], axis=1)

    mask = s_full > noise_power[:, None]

    mask = mask.astype(float)

    mask = medfilt(mask, kernel_size=(1, 5))

    s_clean = s_full * mask

    yclean = librosa.istft(s_clean * phase)

    sf.write(f'clean_sequences/clean_{index}.wav', yclean, sr)


def list_audio_input_channels():
    audio = pyaudio.PyAudio()
    print("Available Audio Input Channels:\n")

    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:  # Check if the device has input channels
            print(f"Device ID: {i}")
            print(f"  Name: {device_info['name']}")
            print(f"  Max Input Channels: {device_info['maxInputChannels']}")
            print(f"  Default Sample Rate: {device_info['defaultSampleRate']}")
            print("-" * 40)

    audio.terminate()

def gettext():
    while os.path.exists(f"audio_sequences/sequence_{gettext.counter}.wav") == 0:
        pass
    #    print("passed")
    clean_input(gettext.counter)
    sound = AudioSegment.from_wav(f'clean_sequences/clean_{gettext.counter}.wav')
    sound.export(f"audio_sequences/sequence_{gettext.counter}.mp3", format="mp3")
    results = model.transcribe(f"audio_sequences/sequence_{gettext.counter}.mp3", language="en", fp16=False)
    print(results["text"])
    gettext.counter += 1
    #   os.remove(f"audio_sequences/sequence_{gettext.counter}.mp3")
    #   os.remove(f"audio_sequences/sequence_{gettext.counter}.wav")
    #   sos.system(f"curl http://127.0.0.1:5040/new_audio/{results['text'].replace(' ', '_')}")


gettext.counter = 0


def startThr():
    thr1 = Thread(target=gettext)
    thr1.start()


def record_audio(filename, duration):
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    INPUT_INDEX = 1
    RATE = 44100
    sound_level = 400
    p = pyaudio.PyAudio()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("192.168.36.131", 4321))

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,

                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    print("Recording...")
    for i in range(0, int(RATE / CHUNK * duration)):
        data, addr = sock.recvfrom(4*CHUNK)
        frames.append(data)
        rms = audioop.rms(data, 2)
        # print(rms)
        sound_level = (rms + sound_level)/2
        # add a break condition if the volume drops bellow a certain value
        if keyboard.is_pressed('q'):
            break

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()
    #it stops the

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    #prev place of start thread



'''
def concatenate_audio(file1, file2, output_file):
    # Load audio files
    with wave.open(file1, 'rb') as f1, wave.open(file2, 'rb') as f2:
        frames1 = f1.readframes(f1.getnframes())
        frames2 = f2.readframes(f2.getnframes())

    # Concatenate frames
    combined_frames = frames1 + frames2

    # Write the combined frames to a new file
    with wave.open(output_file, 'wb') as outf:
        outf.setnchannels(f1.getnchannels())
        outf.setsampwidth(f1.getsampwidth())
        outf.setframerate(f1.getframerate())
        outf.writeframes(combined_frames)
'''


def main():

    sequence_duration = 20

    folder_path = "audio_sequences"  # enter path here
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    print("Deletion done")
    print("imkill")
    clean_path = "clean_sequences"  # enter path here
    for filename in os.listdir(clean_path):
        file_path = os.path.join(clean_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
    print("Deletion done")

    output_dir = "audio_sequences"
    os.makedirs(output_dir, exist_ok=True)
    i = 0
    allow_rec = 1
    startThr()
    while True:
        # Record audio
        # print("To start recording press s")
        while allow_rec == 0:
            pass

        filename = os.path.join(output_dir, f"sequence_{i}.wav")
        record_audio(filename, sequence_duration)
        print(f"Sequence {i} recorded.")

        # Concatenate the first two audio sequences

        i += 1


if __name__ == "__main__":
    list_audio_input_channels()
    main()
