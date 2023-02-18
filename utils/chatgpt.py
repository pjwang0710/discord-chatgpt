from collections import defaultdict
import openai
import os
from dotenv import load_dotenv
load_dotenv()


class MemoryInterface:
    def append(self, user_id: str, text: str) -> None:
        pass

    def get(self, user_id: str) -> str:
        return ""

    def remove(self, user_id: str) -> None:
        pass


class Memory(MemoryInterface):
    def __init__(self):
        self.storage = defaultdict(list)

    def append(self, user_id: str, text: str) -> None:
        self.storage[user_id] += text

    def get(self, user_id: str) -> str:
        return '\n\n'.join(self.storage.get(user_id, [])[-10:])

    def remove(self, user_id: str) -> None:
        self.storage[user_id] = []


class ModelInterface:
    def completion(self, prompt: str) -> str:
        pass


class OpenAIModel(ModelInterface):
    def __init__(self, api_key: str, model_engine: str, max_tokens: int = 128):
        openai.api_key = api_key
        self.model_engine = model_engine
        self.max_tokens = max_tokens

    def completion(self, prompt: str) -> str:
        comp = openai.Completion.create(
            engine=self.model_engine,
            prompt=prompt,
            max_tokens=self.max_tokens,
            stop=None,
            temperature=0.5,
        )
        response = comp.choices[0].text.strip()
        return response


class ChatGPT:
    def __init__(self, model: ModelInterface, memory: MemoryInterface = None):
        self.model = model
        self.memory = memory

    def get_response(self, user_id: str, text: str) -> str:
        prompt = text if self.memory is None else f'{self.memory.get(user_id)}\n\n{text}'
        response = self.model.completion(f'{prompt} <|endoftext|>')
        if self.memory is not None:
            self.memory.append(user_id, [prompt, response])
        return response

    def clean_history(self, user_id: str) -> None:
        self.memory.remove(user_id)


model = OpenAIModel(api_key=os.getenv('OPENAI_API'), model_engine=os.getenv('OPENAI_MODEL_ENGINE'), max_tokens=int(os.getenv('OPENAI_MAX_TOKENS')))
memory = Memory()
chatgpt = ChatGPT(model, memory)
