from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import TTSRequest
from app.services.tts_service import text_to_speech

router = APIRouter()


@router.post(
    "/speak",
    summary="Convert text to speech (MP3 stream)",
    response_class=StreamingResponse,
    responses={
        200: {
            "content": {"audio/mpeg": {}},
            "description": "MP3 audio stream",
        }
    },
)
async def speak(payload: TTSRequest):
    """
    Converts any text to an MP3 audio stream via Google Text-to-Speech (gTTS).

    - **text**: The text to narrate (required).
    - **lang**: BCP-47 language code, defaults to `"en"`.
    - **slow**: Set `true` for slower, clearer speech.

    Returns a streaming MP3 response that the frontend can play directly.
    """
    try:
        audio_buf = text_to_speech(
            text=payload.text,
            lang=payload.lang,
            slow=payload.slow,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return StreamingResponse(
        audio_buf,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "inline; filename=udaya_narration.mp3"},
    )
