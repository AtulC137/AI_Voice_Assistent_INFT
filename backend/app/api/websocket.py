import json
import time

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.services.stt.sarvam_stt import SarvamSTT
from app.services.llm.llm_service import LLMService
from app.services.tts.sarvam_tts import SarvamTTS


async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    print(
        "[WS] Connected"
    )


    stt=SarvamSTT()
    await stt.connect()

    llm=LLMService()

    tts=SarvamTTS()


    audio_buffer=b""


    try:

        while True:


            message=await websocket.receive()


            if "bytes" in message:


                chunk=message["bytes"]

                audio_buffer+=chunk


            elif "text" in message:


                data=json.loads(

                    message["text"]

                )


                if data.get("type")=="stop":


                    total_start=time.time()


                    print(
                        "\n[PROCESSING STARTED]"
                    )


                    # ---------------- STT ----------------

                    stt_start=time.time()


                    await stt.send_audio(

                        audio_buffer

                    )


                    await stt.flush()


                    response=await stt.receive()


                    transcript=(

                        response[
                            "data"
                        ].get(

                            "transcript",

                            ""

                        )

                    )


                    stt_end=time.time()


                    print(
                        f"\n[STT LATENCY] {round(stt_end-stt_start,2)} sec"
                    )


                    print(
                        "\n[TRANSCRIPT]"
                    )

                    print(
                        transcript
                    )


                    # ---------------- LLM ----------------

                    llm_response=(

                        await llm.generate(

                            transcript

                        )

                    )


                    print(
                        "\n[LLM RESPONSE]"
                    )

                    print(
                        llm_response
                    )


                    # ---------------- TTS ----------------

                    audio=await tts.generate(

                        llm_response

                    )


                    if audio:


                        await websocket.send_bytes(

                            audio

                        )


                    total_end=time.time()


                    print(
                        f"\n[TOTAL LATENCY] {round(total_end-total_start,2)} sec"
                    )


                    print(
                        "\n[READY FOR NEXT QUESTION]"
                    )


                    # IMPORTANT:
                    # reset only
                    # DO NOT CLOSE WS

                    audio_buffer=b""


    except WebSocketDisconnect:

        print(
            "\n[CLIENT CLOSED]"
        )


    except Exception as e:

        print(
            "\n[ERROR]"
        )

        print(e)


    finally:

        await stt.close()

        print(
            "[WS Closed]"
        )