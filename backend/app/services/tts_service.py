import logging
from io import BytesIO
from gtts import gTTS

logger = logging.getLogger(__name__)


def text_to_speech(text: str, lang: str = "en", slow: bool = False) -> BytesIO:
    """
    Converts *text* to an MP3 audio stream using gTTS.

    Returns a BytesIO object positioned at the start, ready to stream.
    Raises RuntimeError on failure.
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        audio_buf = BytesIO()
        tts.write_to_fp(audio_buf)
        audio_buf.seek(0)
        return audio_buf
    except Exception as exc:
        logger.error("gTTS error: %s", exc)
        raise RuntimeError(f"TTS generation failed: {exc}") from exc
