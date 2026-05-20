"""
Low latency websocket

Fixes:
- Prevent concurrent websocket reads
- Preserve final words
- Keep async processing
- Lower latency
"""

import asyncio

from fastapi import APIRouter
from fastapi import WebSocket

from app.services.stt.sarvam_stt import SarvamSTT


router = APIRouter()

BUFFER_SIZE = 48000


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    print("[WS] Connected")

    stt = SarvamSTT()

    await stt.connect()

    print("[STT] Connected")

    audio_buffer = b""

    pending_task = None


    async def receive_stt():

        try:

            response = await stt.receive()

            print(
                "\n[STT RESPONSE]"
            )

            print(
                response
            )


            if response.get(
                "type"
            ) == "data":

                transcript=(

                    response[
                        "data"
                    ].get(
                        "transcript",
                        ""
                    )

                )


                if transcript:

                    await websocket.send_text(
                        transcript
                    )


        except Exception as e:

            print(
                "\n[STT ERROR]"
            )

            print(e)


    try:

        while True:

            chunk = await websocket.receive_bytes()

            audio_buffer += chunk


            print(

                "[Chunk]",
                len(chunk),

                "| Buffer:",

                len(audio_buffer)

            )


            if len(
                audio_buffer
            ) >= BUFFER_SIZE:


                print(
                    "\n[Sending to STT]"
                )


                await stt.send_audio(
                    audio_buffer
                )


                await stt.flush()


                if (

                    pending_task
                    and
                    not pending_task.done()

                ):

                    await pending_task


                pending_task = (

                    asyncio.create_task(
                        receive_stt()
                    )

                )


                audio_buffer = b""


    except Exception as e:

        print(
            "\n[Closing]"
        )


        if pending_task:

            await pending_task


        if len(audio_buffer)>0:

            print(
                "\n[Sending remaining]"
            )

            await stt.send_audio(
                audio_buffer
            )

            await stt.flush()

            await receive_stt()


        await stt.close()

        print(e)