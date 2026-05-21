import os
import base64
import time

from dotenv import load_dotenv
from sarvamai import SarvamAI

load_dotenv()


class SarvamTTS:

    def __init__(self):

        self.client = SarvamAI(

            api_subscription_key=
            os.getenv(
                "SARVAM_API_KEY"
            )

        )


    async def generate(
        self,
        text
    ):

        try:

            start=time.time()


            response = (

                self.client
                .text_to_speech
                .convert(

                    text=text,

                    model="bulbul:v3",

                    target_language_code="en-IN",

                    speaker="ishita",

                    speech_sample_rate=16000,

                    output_audio_codec="mp3"

                )

            )


            audio_base64=(

                "".join(
                    response.audios
                )

            )


            audio_bytes=(

                base64.b64decode(

                    audio_base64

                )

            )


            end=time.time()


            print(
                f"\n[TTS LATENCY] {round(end-start,2)} sec"
            )


            return audio_bytes


        except Exception as e:

            print(
                "\n[TTS ERROR]"
            )

            print(e)

            return None