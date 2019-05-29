import pyaudio							#conda install PyAudio
import socket
from threading import Thread

frames = []

print("Voice Client Open")

def udpStream():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    			#AF_INET : Can connect to Internet Protocol v4 addresses
															#SOCK_DGRAM: UDP, SOCK_STREAM: TCP
    while True:
        if len(frames) > 0:
            udp.sendto(frames.pop(0), ("127.0.0.1", 12345))		#Change it to the other PC IP

    udp.close()

def record(stream, CHUNK):    
    while True:
        frames.append(stream.read(CHUNK))

if __name__ == "__main__":
    CHUNK = 1024														#Buffer
    FORMAT = pyaudio.paInt16											#Int 16
    CHANNELS = 2														#1 for send, 1 for recieve
    RATE = 44100														#44k Hertz

    p = pyaudio.PyAudio()												#Intialization

    stream = p.open(format = FORMAT,									# open stream
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK,
                    )

    Tr = Thread(target = record, args = (stream, CHUNK,))
    Ts = Thread(target = udpStream)
    Tr.setDaemon(True)				#It will die after the main thread dies.
    Ts.setDaemon(True)
    Tr.start()						#Start Threading.
    Ts.start()
    Tr.join()						#Wait until thread terminates.
    Ts.join()