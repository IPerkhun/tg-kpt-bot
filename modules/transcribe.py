import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


async def transcribe_audio(file_path: str) -> str:
    """Транскрибирует аудиофайл с использованием Whisper API."""
    with open(file_path, "rb") as audio_file:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
    print(transcription)
    return transcription.text
