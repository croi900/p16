import os
import subprocess
from faster_whisper import WhisperModel
import socket
import pyaudio
from pydub import AudioSegment

from hand_tracking import generation2


def begin_read():
    # Define UDP source address and port
    UDP_IP = "192.168.34.119"
    UDP_PORT = 4321

    # Audio constants
    CHUNK = 4096  # Buffer size for each chunk of audio
    FORMAT = pyaudio.paInt16  # 16-bit PCM
    CHANNELS = 1 # Stereo
    RATE = 44100  # Sample rate (44.1 kHz)
    DURATION = 1  # Duration to capture in seconds

    # Calculate how many frames we need to capture for 6 seconds
    TOTAL_FRAMES = int(512)

    # Initialize UDP Socket to receive audio
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((UDP_IP, UDP_PORT))

    p = pyaudio.PyAudio()

    # Open the PyAudio stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"Recording 6 seconds of audio...")

    audio_data = []

    num_frames_received = 0

    # Continuously receive audio data until 6 seconds elapse
    while num_frames_received < TOTAL_FRAMES:
        try:
            data, _ = udp_socket.recvfrom(CHUNK)
            audio_data.append(data)
            num_frames_received += 1
            # print(len(audio_data))

        except KeyboardInterrupt:
            break

    # Stop PyAudio stream
    stream.stop_stream()
    stream.close()

    udp_socket.close()
    p.terminate()

    print("Finished capturing audio.")

    # Merge collected audio chunks
    audio_bytes = b''.join(audio_data)

    # Convert audio_bytes to a Pydub segment
    audio_segment = AudioSegment(
        audio_bytes,
        frame_rate=RATE,
        sample_width=p.get_sample_size(FORMAT),
        channels=CHANNELS
    )

    # Save output to MP3
    audio_segment.export("audio_buffer.mp3", format="mp3")



model_size = "small"

import sys
import os
from pathlib import Path


def set_cuda_paths():
    venv_base = Path(sys.executable).parent.parent
    nvidia_base_path = venv_base / 'Lib' / 'site-packages' / 'nvidia'
    cuda_path = nvidia_base_path / 'cuda_runtime' / 'bin'
    cublas_path = nvidia_base_path / 'cublas' / 'bin'
    cudnn_path = nvidia_base_path / 'cudnn' / 'bin'
    paths_to_add = [str(cuda_path), str(cublas_path), str(cudnn_path)]
    env_vars = ['CUDA_PATH', 'CUDA_PATH_V12_4', 'PATH']

    for env_var in env_vars:
        current_value = os.environ.get(env_var, '')
        new_value = os.pathsep.join(
            paths_to_add + [current_value] if current_value else paths_to_add)
        os.environ[env_var] = new_value


set_cuda_paths()

def begin_transcrbe():
    model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    segments, info = model.transcribe("audio_buffer.mp3", beam_size=5,
                                      language='en')
    trans = ""
    for seg in segments:
        trans += seg.text
    return trans

def begin_process():
    begin_read()
    return begin_transcrbe()


def begin_gen_from_audio():
    transcript = begin_process()
    generation2.generate_recipe(transcript)

if __name__ == '__main__':
    begin_gen_from_audio()
