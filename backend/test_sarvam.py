"""
Sarvam STT Real Audio Test

Purpose:
- Read WAV
- Convert to 16000Hz if needed
- Send to Sarvam
- Print transcript

Run:
docker compose exec backend python test_sarvam.py
"""

import asyncio
import websockets
import os
import json
import base64
import wave
import audioop
from dotenv import load_dotenv


load_dotenv()

API_KEY=os.getenv(
    "SARVAM_API_KEY"
)


async def main():

    audio_path="/app/hindi.wav"

    print(
        "\nReading:"
    )

    print(
        audio_path
    )


    with wave.open(
        audio_path,
        "rb"
    ) as wav:

        original_rate=wav.getframerate()

        channels=wav.getnchannels()

        sample_width=wav.getsampwidth()

        frames=wav.getnframes()

        audio_bytes=wav.readframes(
            frames
        )


    print(
        "\nOriginal Sample Rate:",
        original_rate
    )


    TARGET_RATE=16000


    if original_rate!=TARGET_RATE:

        print(
            "\nResampling..."
        )

        audio_bytes,_=audioop.ratecv(

            audio_bytes,
            sample_width,
            channels,
            original_rate,
            TARGET_RATE,
            None

        )


    print(
        "\nNew Sample Rate:",
        TARGET_RATE
    )

    print(
        "Bytes:",
        len(audio_bytes)
    )


    url=(

        "wss://api.sarvam.ai/speech-to-text/ws"
        "?language-code=unknown"
        "&model=saaras:v3"
        "&mode=codemix"
        "&sample_rate=16000"
        "&input_audio_codec=pcm_s16le"

    )


    ws=await websockets.connect(

        url,

        additional_headers={

            "Api-Subscription-Key":
            API_KEY

        }

    )


    print(
        "\n[OK] Connected"
    )


    payload={

        "audio":{

            "data":
            base64.b64encode(
                audio_bytes
            ).decode(),

            "encoding":
            "audio/wav",

            "sample_rate":
            16000

        }

    }


    print(
        "\nSending..."
    )


    await ws.send(
        json.dumps(
            payload
        )
    )


    await ws.send(
        json.dumps(
            {
                "type":"flush"
            }
        )
    )


    while True:

        try:

            response=await ws.recv()

            print(
                "\nSERVER:\n"
            )

            print(
                response
            )

        except Exception as e:

            print(
                "\nDONE"
            )

            print(
                e
            )

            break


    await ws.close()


asyncio.run(
    main()
)