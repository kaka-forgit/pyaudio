import platform
import queue
import wave
import tempfile
import os
import time

import sounddevice as sd
import numpy as np

# ==========================================
# OS判定・文字起こしエンジン選択
# ==========================================

SYSTEM = platform.system()

if SYSTEM == "Darwin":
    import mlx_whisper

    ENGINE = "mlx"
    MODEL = "mlx-community/whisper-large-v3-turbo"

elif SYSTEM == "Windows":
    from faster_whisper import WhisperModel

    ENGINE = "faster-whisper"
    MODEL = "large-v3-turbo"

else:
    raise RuntimeError(f"未対応のOSです: {SYSTEM}")


# ==========================================
# 設定
# ==========================================

# macOSでは現在使用しているマイク番号
# Windowsでは既定の入力デバイスを使用
DEVICE = 2 if SYSTEM == "Darwin" else None

SAMPLE_RATE = 48000
CHANNELS = 1
CHUNK_SECONDS = 5

audio_queue = queue.Queue(maxsize=500)


# ==========================================
# 音声取得
# ==========================================


def audio_callback(indata, frames, time_info, status):

    if status:
        print(f"\n[Audio] {status}")

    try:
        audio_queue.put_nowait(indata.copy())

    except queue.Full:
        print("\n[警告] 音声処理が追いついていません。")


# ==========================================
# WAV保存
# ==========================================


def save_wav(audio):

    audio_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)

    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

    temp.close()

    with wave.open(temp.name, "wb") as f:
        f.setnchannels(CHANNELS)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        f.writeframes(audio_int16.tobytes())

    return temp.name


# ==========================================
# モデル読み込み
# ==========================================


def load_model():

    print(f"[OS] {SYSTEM}")
    print(f"[Engine] {ENGINE}")
    print(f"[Model] {MODEL}")

    if ENGINE == "mlx":
        return None

    # Windows用モデル
    print("[Model] Faster Whisperを読み込んでいます...")

    return WhisperModel(MODEL, device="cpu", compute_type="int8")


# ==========================================
# 文字起こし
# ==========================================


def transcribe(wav_path, model):

    if ENGINE == "mlx":

        result = mlx_whisper.transcribe(
            wav_path,
            path_or_hf_repo=MODEL,
            language="ja",
            task="transcribe",
            verbose=False,
        )

        return result["text"].strip()

    else:

        segments, info = model.transcribe(
            wav_path, language="ja", task="transcribe", beam_size=5
        )

        return "".join(segment.text for segment in segments).strip()


# ==========================================
# メイン処理
# ==========================================


def main():

    print("====================================")
    print(" 日本語リアルタイム文字起こし")
    print("====================================")

    print("5秒ごとに音声を認識します。")
    print("Ctrl+C で終了します。\n")

    model = load_model()

    buffer = []
    required_samples = SAMPLE_RATE * CHUNK_SECONDS
    current_samples = 0
    chunk_number = 0

    try:

        with sd.InputStream(
            device=DEVICE,
            channels=CHANNELS,
            samplerate=SAMPLE_RATE,
            dtype="float32",
            callback=audio_callback,
            blocksize=1024,
        ):

            print("\n録音開始。話してください。\n")

            while True:

                data = audio_queue.get()

                buffer.append(data)
                current_samples += len(data)

                if current_samples >= required_samples:

                    audio = np.concatenate(buffer, axis=0)

                    buffer = []
                    current_samples = 0

                    chunk_number += 1

                    wav_path = save_wav(audio)

                    print(f"\n[認識中] チャンク {chunk_number}")

                    start = time.time()

                    try:

                        text = transcribe(wav_path, model)

                        elapsed = time.time() - start

                        if text:
                            print(f"[認識結果] {text}")

                        print(f"[処理時間] {elapsed:.2f} 秒")

                    except Exception as e:
                        print(f"[認識エラー] {e}")

                    finally:
                        os.remove(wav_path)

    except KeyboardInterrupt:

        print("\n\n文字起こしを終了しました。")


if __name__ == "__main__":
    main()
