import sounddevice as sd
import numpy as np

device = 2
rate = 48000
duration = 5

print("マイクに向かって話してください（5秒間）")

try:
    audio = sd.rec(
        int(duration * rate),
        samplerate=rate,
        channels=1,
        dtype="float32",
        device=device
    )
    sd.wait()

    rms = np.sqrt(np.mean(audio ** 2))
    peak = np.max(np.abs(audio))

    db = 20 * np.log10(max(rms, 1e-10))

    print(f"RMS: {rms:.6f}")
    print(f"Peak: {peak:.6f}")
    print(f"音量: {db:.1f} dBFS")

except Exception as e:
    print("エラー:", e)
