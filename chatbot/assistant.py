from groq import Groq

from config import API_KEY
from config import MODEL
from config import SYSTEM_PROMPT

client = Groq(api_key=API_KEY)


class ChatBot:

    def __init__(self, memory):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        self.messages.extend(memory)

    def ask(self, question):

        self.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=self.messages
        )

        answer = response.choices[0].message.content

        self.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer

    def get_memory(self):
        return self.messages[1:]
