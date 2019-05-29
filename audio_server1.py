import pyaudio															#conda install PyAudio
import socket
from threading import Thread

frames = []
print("Voice Server Open")

def udpStream(CHUNK, CHANNELS):

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	#AF_INET : Can connect to Internet Protocol v4 addresses
															#SOCK_DGRAM: UDP, SOCK_STREAM: TCP
    udp.bind(("127.0.0.1", 12345))							#Change it to your PC IP

    while True:
        soundData, addr = udp.recvfrom(CHUNK * CHANNELS * 2)	#Reduce Noise
        frames.append(soundData)

    udp.close()

def play(stream, CHUNK):
    BUFFER = 10
    while True:
            if len(frames) == BUFFER:
                while True:
                    stream.write(frames.pop(0), CHUNK)

#s.send(request.encode)
#result=s.recv(4096)
if __name__ == "__main__":
    FORMAT = pyaudio.paInt16									#Int 16
    CHUNK = 1024												#Buffer
    CHANNELS = 2												#1 for send, 1 for recieve
    RATE = 44100												#44k Hertz

    p = pyaudio.PyAudio()										#Intialization

    stream = p.open(format=FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    output = True,
                    frames_per_buffer = CHUNK,
                    )

    Ts = Thread(target = udpStream, args=(CHUNK, CHANNELS))
    Tp = Thread(target = play, args=(stream, CHUNK,))
    Ts.setDaemon(True)						#It will die after the main thread dies.
    Tp.setDaemon(True)
    Ts.start()								#Start Threading.
    Tp.start()
    Ts.join()								#Wait until thread terminates.
    Tp.join()