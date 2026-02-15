from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse
from app.utils.logger import logger

router = APIRouter()


@router.post("/twilio/webhook")
async def receive_message(request: Request):
    form = await request.form()

    sender = form.get("From")
    message = form.get("Body")

    logger.info(f"Twilio message from {sender}: {message}")

    # Temporary static reply
    return PlainTextResponse("Message received.")
