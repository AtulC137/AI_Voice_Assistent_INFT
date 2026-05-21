import json

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.services.stt.sarvam_stt import SarvamSTT
from app.services.llm.llm_service import LLMService


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


    audio_buffer=b""


    try:


        while True:


            message=await websocket.receive()


            if "bytes" in message:


                chunk=message["bytes"]

                audio_buffer+=chunk


                print(

                    "[Buffer]",

                    len(audio_buffer)

                )



            elif "text" in message:


                data=json.loads(

                    message["text"]

                )


                if data.get("type")=="stop":


                    print(
                        "\n[STOP RECEIVED]"
                    )


                    print(
                        "\nSending combined audio..."
                    )


                    print(

                        "Bytes:",

                        len(audio_buffer)

                    )


                    await stt.send_audio(

                        audio_buffer

                    )


                    await stt.flush()


                    response=await stt.receive()


                    print(
                        "\n[STT RESPONSE]"
                    )

                    print(
                        response
                    )


                    transcript=(

                        response[
                            "data"
                        ].get(

                            "transcript",

                            ""

                        )

                    )


                    print(
                        "\n================"
                    )

                    print(
                        "[TRANSCRIPT]"
                    )

                    print(
                        transcript
                    )

                    print(
                        "================"
                    )


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


                    await websocket.send_text(

                        llm_response

                    )


                    await websocket.close()


                    break



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