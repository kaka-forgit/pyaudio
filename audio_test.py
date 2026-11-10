import sounddevice as sd
import numpy as np
import time

MIC_DEVICE = 2
SYSTEM_DEVICE = 1
SAMPLE_RATE = 48000

levels = {
    "Microphone": 0.0,
    "System Audio": 0.0
}

def make_callback(name):
    def callback(indata, frames, time_info, status):
        if status:
            print(f"[{name}] {status}")

        rms = np.sqrt(np.mean(indata ** 2))
        levels[name] = float(rms)

    return callback


print("音声入力テストを開始します。")
print("マイクに向かって話してください。")
print("Macで動画や音楽を再生してください。")
print("15秒後に終了します。\n")

try:
    with sd.InputStream(
        device=MIC_DEVICE,
        channels=1,
        samplerate=SAMPLE_RATE,
        callback=make_callback("Microphone")
    ) as mic_stream:

        with sd.InputStream(
            device=SYSTEM_DEVICE,
            channels=2,
            samplerate=SAMPLE_RATE,
            callback=make_callback("System Audio")
        ) as system_stream:

            for i in range(15):
                time.sleep(1)

                mic_db = 20 * np.log10(max(levels["Microphone"], 1e-10))
                system_db = 20 * np.log10(max(levels["System Audio"], 1e-10))

                print(
                    f"マイク: {mic_db:6.1f} dBFS | "
                    f"内部音声: {system_db:6.1f} dBFS"
                )

except Exception as e:
    print("\n音声取得エラー:")
    print(e)

print("\nテスト終了")
