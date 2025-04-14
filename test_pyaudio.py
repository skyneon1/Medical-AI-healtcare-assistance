import pyaudio

# Create an instance of PyAudio
p = pyaudio.PyAudio()

# Get information about audio devices
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
print(f"Total audio devices: {numdevices}")

# List all audio devices
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print(f"Input Device id {i} - {p.get_device_info_by_host_api_device_index(0, i).get('name')}")

# Terminate the PyAudio instance
p.terminate()

print("PyAudio (and PortAudio) are working correctly!")
