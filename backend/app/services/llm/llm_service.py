import os
import re
import time

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMService:

    def __init__(self):

        self.client = OpenAI(

            api_key=os.getenv(
                "SARVAM_API_KEY"
            ),

            base_url="https://api.sarvam.ai/v1"

        )


    async def generate(
        self,
        text
    ):

        try:

            start=time.time()


            response = (

                self.client.chat.completions.create(

                    model="sarvam-30b",

                    temperature=0.2,

                    messages=[

                        {
                            "role": "system",

                            "content":
                            """
You are Aria, a warm and professional AI event assistant.

ONLY answer questions about the Adobe Exclusive Roundtable event.

Rules:
- Maximum 1-2 short sentences
- Keep answers concise
- Speak naturally
- No bullet points
- No long explanations
- No <think> tags
- Do not invent information

Event:
Adobe Exclusive Roundtable

Date:
8 May 2026

Venue:
The Pride Hotel, Pune

Topics:
PDF innovation, Gen AI, creative workflows, collaboration, networking.

Eligibility:
CMOs, CIOs, CTOs, Heads of Design, Heads of Legal.
Not open for channel partners.
"""
                        },

                        {
                            "role": "user",

                            "content": text
                        }

                    ]

                )

            )


            answer = (

                response
                .choices[0]
                .message
                .content
            )


            answer = re.sub(

                r"<think>.*?</think>",

                "",

                answer,

                flags=re.DOTALL

            )


            end=time.time()


            print(
                f"\n[LLM LATENCY] {round(end-start,2)} sec"
            )


            return answer.strip()


        except Exception as e:

            print(
                "\n[LLM ERROR]"
            )

            print(e)

            return ""