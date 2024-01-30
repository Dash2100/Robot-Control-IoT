import pyaudio

audio = pyaudio.PyAudio()

# 列出所有音訊裝置
info = audio.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')

# 遍歷並列印每個裝置的資訊
for i in range(0, num_devices):
    if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))

audio.terminate()
