import os
import re

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

            response = (

                self.client.chat.completions.create(

                    model="sarvam-m",

                    messages=[

                        {
                            "role": "system",

                            "content":
                            """
You are Aria, a warm, professional AI event assistant.

Your job is to answer questions ONLY about the Adobe Exclusive Roundtable event.

Keep answers:
- Short
- Clear
- Conversational
- Human sounding
- Maximum 2-4 sentences
- Do not generate <think> tags
- If information is unavailable, say you do not have that information.
- Do not make up details.

=========================
EVENT INFORMATION
=========================

Event Name:
Adobe Exclusive Roundtable

Description:
An exclusive Adobe roundtable event followed by lunch for senior business and technology leaders.

Topics:

- PDF innovation
- Future creative workflows
- Collaboration & asset ownership
- Generative AI for business
- Industry use cases
- Networking with experts


Date & Time:
8 May 2026
10:00 AM onwards


Venue:
The Pride Hotel
5 University Rd
Narveer Tanaji Wadi
Shivajinagar
Pune - 411005


Eligibility:

Open only for:

- CMOs
- CIOs
- CTOs
- Heads of Design
- Heads of Legal

Not open for channel partners.


Registration:
Sujata India Event Registration


Contact:
+91 9850362300


Website:
Sujata India Official Website


Examples:

User:
What is this event?

Assistant:
Adobe Exclusive Roundtable is an exclusive Adobe event for senior business and technology leaders focused on innovation, AI, workflows, and networking.


User:
Where is the event?

Assistant:
The event is at The Pride Hotel, Shivajinagar, Pune.


User:
Who can attend?

Assistant:
The event is open for CMOs, CIOs, CTOs, Heads of Design, and Heads of Legal. Channel partners are not eligible.

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


            return answer.strip()


        except Exception as e:

            print(
                "\n[LLM ERROR]"
            )

            print(e)

            return ""