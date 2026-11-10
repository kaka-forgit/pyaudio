import sounddevice as sd

print("=== Audio Input Devices ===")

for index, device in enumerate(sd.query_devices()):
    if device["max_input_channels"] > 0:
        print(
            f"[{index}] {device['name']} "
            f"(inputs: {device['max_input_channels']}, "
            f"rate: {device['default_samplerate']})"
        )
