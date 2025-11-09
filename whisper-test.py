# -*- coding: utf-8 -*-

import whisper

model = whisper.load_model("turbo")
result = model.transcribe("week7.mp3")
print(result["text"])