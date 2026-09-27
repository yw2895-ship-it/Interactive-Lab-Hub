#!/usr/bin/env bash
set -euo pipefail

OUTPUT="number_answer.wav"

espeak "Please say your five digit zip code. Recording starts now."

sleep 1

arecord \
  -D plughw:CARD=Device,DEV=0 \
  -d 5 \
  -f S16_LE \
  -c 1 \
  -r 16000 \
  "$OUTPUT"

echo "Recording complete."
python transcribe.py "$OUTPUT" --model tiny.en
