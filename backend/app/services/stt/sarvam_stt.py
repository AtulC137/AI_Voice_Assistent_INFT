"""
Sarvam STT Service

Audio:
16000Hz
Mono
16-bit PCM
PCM S16LE
Mode: codemix
"""

import os
import json
import base64
import websockets

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv(
    "SARVAM_API_KEY"
)


class SarvamSTT:

    def __init__(self):

        self.ws = None

        self.url=(

            "wss://api.sarvam.ai/speech-to-text/ws"
            "?language-code=unknown"
            "&model=saaras:v3"
            "&mode=codemix"
            "&sample_rate=16000"
            "&input_audio_codec=pcm_s16le"

        )


    async def connect(self):

        self.ws = await websockets.connect(

            self.url,

            additional_headers={

                "Api-Subscription-Key":
                API_KEY

            }

        )


    async def send_audio(
        self,
        audio_bytes
    ):

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

        await self.ws.send(
            json.dumps(
                payload
            )
        )


    async def flush(self):

        await self.ws.send(

            json.dumps({

                "type":"flush"

            })

        )


    async def receive(self):

        response = await self.ws.recv()

        return json.loads(
            response
        )


    async def close(self):

        if self.ws:

            await self.ws.close()