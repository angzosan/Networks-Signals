import wave
import numpy as np
import random
from numba import njit
from scipy.io.wavfile import write



@njit    #using gpu to run the program
def MyConvolve(A,B):
    C=np.zeros((len(A)+len(B)-1))
    b=0
    for i in range(len(A)):
        for j in range (b+1):
            C[i]=C[i]+A[i-j]*B[j]
        if b+1!=len(B):
            b=b+1
    b=len(B)-1
    for i in range(len(A),len(C)):
        if b==0:
            break
        for j in range (1,b+1):
            C[i]=C[i]+A[len(A)-j]*B[j]
        if b-1!=len(B):
            b=b-1
    return C

def WavFileToArray(name):
    file = wave.open(name)
    sample = file.getnframes()
    audio = file.readframes(sample)
    # Convert buffer to float32 using NumPy                                                                                 
    audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
    audio_as_np_float32 = audio_as_np_int16.astype(np.float32)
    # Normalise float32 array so that values are between -1.0 and +1.0                                                      
    max_int16 = 2**15
    return audio_as_np_float32 / max_int16


def ArrayToWavFile(new_audio,name):
   sps = 16000
   # Frequency / pitch of the sine wave
   freq_hz = 440.0
   
   sample = new_audio
   waveform = np.sin(2 * np.pi * sample* freq_hz / sps)
   waveform_quiet = waveform * 0.3
   waveform_integers = np.int16(waveform_quiet * 32767)
   # Write the .wav file
   write(name, sps, waveform_integers)

    
    
#PART ONE 
#asking thel length of the vector and cheching if it's greater thatn 10
N = input('Choose the length of your vector(greater than 10): ')
while int(N)<11:
  N = input('Wrong number.Try again.Choose the length of your vector(greater than 10): ')
  if int(N)>10:
    break
#creating the vectors A  and B
A=np.array([random.random() for x in range(int(N))])
A=np.array([float(x) for x in A])
B = np.array([1/5, 1/5, 1/5, 1/5, 1/5])
#we fip the second vector so we can use it for the convolution
np.flip(B,0)
C=MyConvolve(A,B)
print(C)

print()
print("Part two of the assignment")
print()



#PART TWO (A)
#we use thw 'WavToArray' function for the "reading" of the wav file
audio_normalised1=WavFileToArray("sample_audio.wav")
audio_normalised2=WavFileToArray("pink_noise.wav")
#we repeat the process from before
np.flip(audio_normalised2,0)
new_audio=MyConvolve(audio_normalised1,audio_normalised2)
print()
print(new_audio)
ArrayToWavFile(new_audio,'pinkNoise_sampleAudio.wav')



#PART TWO (B)
#we create a white noise 
mean = 0 
std = 1 #standart derivation
num_samples = 10000 #size
samples = np.random.normal(mean, std, size=num_samples)
#we flip the second vector and then we use the convolution function
np.flip(samples,0)
D=MyConvolve(audio_normalised1,samples)
ArrayToWavFile(D, 'whiteNoise_sampleAudio.wav')
print()
print(D)
