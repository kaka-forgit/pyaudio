# Offline Transcriber

MacのApple Silicon上で動作する、Python製のオフライン日本語リアルタイム文字起こしツールです。

## 概要

MLX Whisperを利用して、音声をローカル環境で日本語に文字起こしします。

インターネット上の外部APIに音声を送信せず、Mac上で音声認識を実行することを目指しています。

## 主な特徴

- 日本語音声のリアルタイム文字起こし
- Apple Silicon向けMLX Whisperを使用
- ローカル環境で音声認識
- ターミナルへの認識結果表示
- Macのマイク入力に対応
- BlackHoleを利用したMac内部音声の取得に対応予定

## 動作環境

- macOS
- Apple Silicon Mac（Mシリーズ）
- Python 3.12
- インターネット接続（初回セットアップ・モデル取得時）

## セットアップ

```bash
git clone https://github.com/kaka-forgit/pyaudio.git
cd offline-transcriber

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

## 実行方法

```bash
python realtime.py
```

初回実行時にはWhisperモデルのダウンロードが必要です。

## 使用モデル

mlx-community/whisper-large-v3-turbo

## 注意事項

- 現在は開発中の試作版です。
- Windowsでの動作は保証しません。
- 音声入力デバイス番号は環境によって異なります。
- 現在の実装ではMacBook Proのマイクを使用しています。
- Mac内部音声の取得やカーソル位置への自動入力は開発予定です。
- モデルの初回取得後は、ローカルモデルを利用することでオフライン動作を目指しています。

## License

MIT License
