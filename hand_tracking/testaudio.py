import socket
import pyaudio

# Configuration
UDP_IP = "192.168.36.131"  # IP address to listen on
UDP_PORT = 4321            # Port to listen on
CHUNK_SIZE = 4096          # Size of audio chunks
FORMAT = pyaudio.paInt16   # Audio format (16-bit PCM)
CHANNELS = 1               # Number of audio channels
RATE = 44100               # Sampling rate (44.1 kHz)
BYTES_PER_SECOND = RATE * CHANNELS * 2  # 2 bytes per sample
BUFFER_SIZE = BYTES_PER_SECOND
def main():
    # Initialize UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Listening for UDP audio stream on {UDP_IP}:{UDP_PORT}...")

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    try:
        while True:
            # Receive audio data from the UDP stream
            data, addr = sock.recvfrom(CHUNK_SIZE)
            print(f"Received {len(data)} bytes from {addr}")

            # Play the audio data
            stream.write(data)
    except KeyboardInterrupt:
        print("\nStopping playback...")
    finally:
        # Clean up resources
        stream.stop_stream()
        stream.close()
        p.terminate()
        sock.close()

if __name__ == "__main__":
    main()
