'''
have 440 Hz test tone playing in supercollider + jack
loop through device options to try and capture the tone

Troubleshooting steps that worked:
had to change permissions, followd some instructions here https://bugzilla.redhat.com/show_bug.cgi?id=1189860
Set up to route all audio through jack - follow here https://www.youtube.com/watch?v=UVhRDU6Kcds

in ubuntu then go to then go to settings -> sound -> and change input/output to Jack source- these set defaults for pyaudio
'''

import pyaudio, wave, time

#import sc

#sc.boot_and_connect()

FORMAT = pyaudio.paInt16
CHANNELS_S = [1,2]
CHUNK = 1024
RATES = [44100, 48000]
RECORD_SECONDS = 5

audio = pyaudio.PyAudio()
audio_devices = [audio.get_device_info_by_index(i) for i in range(audio.get_device_count())]

for dev_id, device in enumerate(audio_devices):
	for CHANNELS in CHANNELS_S:
		for RATE in RATES:
			start_time = time.time()
			print (f'Trying device {device["name"]} with id {dev_id} of {audio.get_device_count()} with sr = {RATE} and {CHANNELS} channels')
			try:
				audio = pyaudio.PyAudio()
				WAVE_OUTPUT_FILENAME = f'name_{device["name"]}_index_{device["index"]}_sr_{RATE}_chls{CHANNELS}.wav'


				stream = audio.open(format=FORMAT, channels=CHANNELS,
								rate=RATE, input=True,
								frames_per_buffer=CHUNK, input_device_index=device['index']) #

				print("recording...")

				frames=[]

				for i in range(0, int(RATE / CHUNK * (RECORD_SECONDS) )+8):
					data = stream.read(CHUNK)
					frames.append(data)


				print ('finifhed!!!!!!!!')

				stream.stop_stream()
				stream.close()
				audio.terminate()

				
				waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
				waveFile.setnchannels(CHANNELS)
				waveFile.setsampwidth(audio.get_sample_size(FORMAT))
				waveFile.setframerate(RATE)
				waveFile.writeframes(b''.join(frames))
				waveFile.close()
				print ('THIS ONE WORKED!!!!!!!!')
				
			except (Exception) as e:
				print (f'Device {device["name"]} with index {device["index"]} and sr {RATE} and channels {CHANNELS} Failed!')
				print (e)

			print ('---------------------------------------------------------------------------')


'''
Trying device jack with id 12 of 15 with sr = 48000 and 2 channels
Cannot lock down 82280346 byte memory area (Cannot allocate memory)
Cannot use real-time scheduling (RR/5)(1: Operation not permitted)
JackClient::AcquireSelfRealTime error
recording...
THIS ONE WORKED!!!!!!!!
'''