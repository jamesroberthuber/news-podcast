"""One-off helper: list Google Cloud TTS voices so you can pick one to try.

Run this locally with the same GOOGLE_SERVICE_ACCOUNT_JSON credential used by
generate_episode.py (see SETUP.md for where that comes from):

    GOOGLE_SERVICE_ACCOUNT_JSON="$(cat path/to/service-account.json)" python3 scripts/list_voices.py

It prints every US English voice Google currently offers, grouped by tier, so
you're picking from what's actually available rather than a guessed name --
Google adds new voices (Chirp3-HD, Neural2, etc.) more often than docs get
updated. Studio and Chirp3-HD tiers are generally the most natural-sounding
for long-form narration; Neural2 and WaveNet are a step down but still solid.

Once you find a name you like, copy it into VOICE_NAME in generate_episode.py.
Google's public voice gallery (with audio samples) is also worth a listen:
https://cloud.google.com/text-to-speech/docs/list-voices-and-types
"""

import json
import os

from google.cloud import texttospeech
from google.oauth2 import service_account


def main() -> None:
    creds_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
    creds = service_account.Credentials.from_service_account_info(creds_info)
    client = texttospeech.TextToSpeechClient(credentials=creds)

    response = client.list_voices(language_code="en-US")
    by_tier: dict[str, list] = {}
    for voice in response.voices:
        tier = voice.name.split("-")[2] if voice.name.count("-") >= 2 else "Other"
        by_tier.setdefault(tier, []).append(voice)

    for tier in sorted(by_tier):
        print(f"\n=== {tier} ===")
        for voice in sorted(by_tier[tier], key=lambda v: v.name):
            gender = voice.ssml_gender.name
            print(f"  {voice.name:30s} gender={gender:8s} sample_rate={voice.natural_sample_rate_hertz}")


if __name__ == "__main__":
    main()
