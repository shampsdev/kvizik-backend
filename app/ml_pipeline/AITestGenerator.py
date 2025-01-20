from extras import SYS_MESSAGE, LLM_REQUEST, REQUEST_HEADERS, REQUEST_URL, HUGGINGFACE_TOKEN, EXPERIMENTAL_TEXT
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from transformers import pipeline, AutoTokenizer
from huggingface_hub import login
from pydantic import BaseModel
from typing import List, Dict
import logging
import httpx
import json


# A model for a single question
class TestQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str


# A model for a test
class AITest(BaseModel):
    title: str
    questions: List[TestQuestion]


class AITestGenerator:
    def __init__(self):
        self.config: Dict = {}
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        try: login(token=HUGGINGFACE_TOKEN)
        except: logging.critical("FAILED TO LOG IN TO HUGGINGFACE")
        logging.debug("Successfully logged into HuggingFace")


        try: self.classifier = pipeline("text-classification", model="meta-llama/Prompt-Guard-86M") 
        except: logging.critical("PROMPT-GUARD FAILED TO LOAD")

        logging.debug("Prompt-guard is ready")


    # Set overall test difficulty
    def set_difficulty(self, difficulty: str):
        self.config["difficulty"] = difficulty
        logging.debug(f"Set difficulty to: {difficulty}")
        return self

    # Set amount of questions asked
    def set_questions_amount(self, questions_amount: int):
        self.config["questions_amount"] = questions_amount
        logging.debug(f"Set amount of questions to: {questions_amount}")
        return self



    # Mock an answer from LLM
    def test_generate_test(self) -> AITest:
        test: str = """{"title":"Природа",
                "questions": [
                    {
                        "question": "Температура кипения воды",
                        "options" : ["100 г. Ц.", "5 г. Ц.", "Вода не кипит", "0 г. Ц."],
                        "correct_answer": "100 г. Ц."
                    }
                ]
            }"""

        parsed_test = json.loads(test)
        return AITest(**parsed_test)


    # Generate a prompt \w user preferences
    def __generate_prompt(self, users_text: str) -> str:
        return f"Количество вопросов: {self.config['questions_amount']}, сложность вопросов: {self.config['difficulty']}. Текст: {users_text}"
    
    

    # Get text, decide whether the prompt is malevolent 
    def is_prompt_safe(self, prompt: str, batch_size: int = 512, overlap: int = 50):
        chunks = []
        score = 0

        start = 0
        
        while start < len(prompt):
            end = start + batch_size
            chunks.append(prompt[start:end])
            start += (batch_size - overlap)  # Move the start index forward by batch_size - overlap

        logging.debug(f"Prompt-guard: Inferencing on: {len(chunks)} chunks of prompt.")

        for batch in chunks:
            result = self.classifier(batch)[0]

            label = 1 if result['label'] == "BENIGN" else -1
            score = result['score']

            score += label * score

        return True if score > 0 else False



    # Generate test from user's text
    def generate_test(self, users_text: str) -> AITest:
        users_prompt: str = self.__generate_prompt(users_text)

        # Update role for model and add user's text
        LLM_REQUEST["messages"] = [
            {"role": "system", "text": SYS_MESSAGE},
            {"role": "user", "text": users_prompt},
        ]

        try:
            response = httpx.post(
                url=REQUEST_URL, headers=REQUEST_HEADERS, json=LLM_REQUEST, timeout=5000
            )

        # If failed to send request using httpx
        except Exception as e:
            logging.critical("FAILED TO SEND POST REQUEST FOR LLM RESPONSE WITH EXCEPTION")
            raise httpx.RequestError(f"Failed to send POST response. Error: {e}")

        # Something went wrong with LLM Service
        if response.status_code != 200:
            logging.critical(f"FAILED TO SEND POST REQUEST FOR LLM RESPONSE WITH STATUS CODE: {response.status_code}")
            raise httpx.HTTPStatusError(
                f"Incorrect POST request with text: {response.text}"
            )

        json_llm_response = json.loads(response.text)["result"]["alternatives"][0][
            "message"
        ]["text"]
        llm_answer = json.loads(json_llm_response.replace('`', ''))[
            "test"
        ]  # Slicing removes compulsory JSON formating

        return AITest(**llm_answer)


# Run module in a unit-environment
if __name__ == "__main__":
    ai = AITestGenerator().set_difficulty("easy").set_questions_amount(1)

    if ai.is_prompt_safe(EXPERIMENTAL_TEXT):
        print(ai.generate_test(EXPERIMENTAL_TEXT))
