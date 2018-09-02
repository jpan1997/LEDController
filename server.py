import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import math

no_channels = 1
sample_rate = 48000
chunk = 4096 
device = 1 

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,
                channels = no_channels,
                rate = sample_rate,
                input = True,
                frames_per_buffer = chunk,
                input_device_index = device)

# log scale
mapping = np.log10(range(10,1200))/math.log10(1200)*443

# list of original bins mapped to each new bin
mapping_list = [None]*300

# offset index
offset = math.floor(mapping[0])

for idx, x in enumerate(mapping):
   curr_idx = int(math.floor(x) - offset)
   # Handle edge case of last element
   if(idx < len(mapping)-1):
      next_idx = int(math.floor(mapping[idx+1]) - offset)
   else:
      next_idx = curr_idx
   if mapping_list[curr_idx] == None:
      mapping_list[curr_idx] = []
   mapping_list[curr_idx].append(idx)
   # pad all bins without mappings to the closest one below it
   while curr_idx < next_idx - 1:
      curr_idx += 1
      if mapping_list[curr_idx] == None:
         mapping_list[curr_idx] = []
      mapping_list[curr_idx].append(idx)

bin_hts = [0]*300


fig, ax = plt.subplots(5)
plt.tight_layout()

line0, = ax[0].plot((np.array(range(chunk/2), dtype=int)*sample_rate/chunk)[:1200],[0]*1200)
line1, = ax[1].plot((np.array(range(chunk/2), dtype=int)*sample_rate/chunk)[:1200],[0]*1200)
line2, = ax[2].plot(bin_hts)
line3, = ax[3].plot(bin_hts)
line4, = ax[4].plot(bin_hts)
ax[0].set_ylim(0,200000)
ax[0].set_xscale('linear')
ax[0].set_title('Raw Data')
ax[1].set_ylim(0,200000)
ax[1].set_xscale('log')
ax[1].set_title('LogX')
ax[2].set_xlim(-175,320)
ax[2].set_ylim(0,200000)
ax[2].set_xscale('linear')
ax[2].set_title('Bin Mapped')
ax[3].set_xlim(-175,320)
ax[3].set_ylim(5,14)
ax[3].set_xscale('linear')
ax[3].set_title('Bin Mapped - Log_e Y')
ax[4].set_xlim(-175,320)
ax[4].set_ylim(0, 10)
ax[4].set_xscale('linear')
ax[4].set_title('Bin Mapped - Log_10 Y')
plt.draw()



stream.start_stream()

while True:
   raw_data = stream.read(chunk)
   audio_data = np.fromstring(raw_data, np.int16)
   fourier = abs(np.fft.rfft(audio_data))
   fourier = np.delete(fourier, len(fourier)-1)
   
   for i, lst in enumerate(mapping_list):
      temp = 0
      for x in lst:
         temp += fourier[10+x]
      temp = temp / len(lst)
      bin_hts[i] = temp

   line0.set_ydata(fourier[:1200])
   line1.set_ydata(fourier[:1200])
   line2.set_ydata(bin_hts)
   line3.set_ydata(np.log(bin_hts))
   line4.set_ydata(np.log10(bin_hts))
   plt.pause(0.01)




# import pylab as plt
# import numpy as np

# X = np.linspace(0,2,1000)
# Y = X**2 + np.random.random(X.shape)

# plt.ion()
# graph = plt.plot(X,Y)[0]

# while True:
#     Y = X**2 + np.random.random(X.shape)
#     graph.set_ydata(Y)
#     plt.draw()
#     plt.pause(0.01)


# dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))


# try:
#     import pyaudio
#     import numpy as np
#     # import pylab
#     import matplotlib.pyplot as plt
#     # from scipy.io import wavfile
#     # import time
#     # import sys
#     # import seaborn as sns
# except:
#     print "Something didn't import"

# i=0
# f,ax = plt.subplots(2)

# # Prepare the Plotting Environment with random starting values
# x = np.arange(10000)
# y = np.random.randn(10000)

# # Plot 0 is for raw audio data
# li, = ax[0].plot(x, y)
# ax[0].set_xlim(0,1000)
# ax[0].set_ylim(-5000,5000)
# ax[0].set_title("Raw Audio Signal")
# # Plot 1 is for the FFT of the audio
# li2, = ax[1].plot(x, y)
# ax[1].set_xlim(0,7)
# ax[1].set_ylim(0,8)
# ax[1].set_title("Fast Fourier Transform")
# # Show the plot, but without blocking updates
# plt.pause(0.01)
# plt.tight_layout()

# FORMAT = pyaudio.paInt16 # We use 16bit format per sample
# CHANNELS = 1
# RATE = 44100
# CHUNK = 1024 # 1024bytes of data red from a buffer
# RECORD_SECONDS = 0.1
# WAVE_OUTPUT_FILENAME = "file.wav"

# audio = pyaudio.PyAudio()

# # start Recording
# stream = audio.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True)#,
#                     #frames_per_buffer=CHUNK)

# global keep_going
# keep_going = True

# def piff(val):
#    return int(2*chunk*val/sample_rate)

# def plot_data(in_data):
#     # get and convert the data to float
#     audio_data = np.fromstring(in_data, np.int16)
#     # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
#     # and make sure it's not imaginary
#     matrix = [0, 0, 0, 0, 0, 0, 0, 0]
#     fourier=np.fft.rfft(data)
#     print "hi"
#     # fourier=np.delete(fourier,len(fourier)-1)
#     # power = np.abs(fourier)   
#     # matrix[0]= int(np.mean(power[piff(0)    :piff(156):1]))
#     # matrix[1]= int(np.mean(power[piff(156)  :piff(313):1]))
#     # matrix[2]= int(np.mean(power[piff(313)  :piff(625):1]))
#     # matrix[3]= int(np.mean(power[piff(625)  :piff(1250):1]))
#     # matrix[4]= int(np.mean(power[piff(1250) :piff(2500):1]))
#     # matrix[5]= int(np.mean(power[piff(2500) :piff(5000):1]))
#     # matrix[6]= int(np.mean(power[piff(5000) :piff(10000):1]))
#     # matrix[7]= int(np.mean(power[piff(10000):piff(20000):1]))
#     # weighting = [2,8,8,16,16,32,32,64]
#     # matrix=np.divide(np.multiply(matrix,weighting),1000000)
#     # matrix=matrix.clip(0,8)


#     # Force the new data into the plot, but without redrawing axes.
#     # If uses plt.draw(), axes are re-drawn every time
#     #print audio_data[0:10]
#     #print dfft[0:10]
#     #print
#     # li.set_xdata(np.arange(len(audio_data)))
#     # li.set_ydata(audio_data)
#     # li2.set_xdata(range(8))
#     # li2.set_ydata(matrix)

#     # Show the updated plot, but without blocking
#     # plt.pause(0.01)
#     if keep_going:
#         return True
#     else:
#         return False

# # Open the connection and start streaming the data
# stream.start_stream()
# print "\n+---------------------------------+"
# print "| Press Ctrl+C to Break Recording |"
# print "+---------------------------------+\n"

# # Loop so program doesn't end while the stream callback's
# # itself for new data
# while keep_going:
#     try:
#         plot_data(stream.read(CHUNK))
#     except KeyboardInterrupt:
#         keep_going=False
#     except:
#         pass

# # Close up shop (currently not used because KeyboardInterrupt
# # is the only way to close)
# stream.stop_stream()
# stream.close()

# audio.terminate()