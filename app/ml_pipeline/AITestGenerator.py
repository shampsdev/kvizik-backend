import json
import logging
from typing import Dict, List

import httpx
from pydantic import BaseModel

from app.ml_pipeline.extras import (
    LLM_REQUEST,
    REQUEST_HEADERS,
    REQUEST_URL,
    SYS_MESSAGE,
)

logging.basicConfig(level=logging.INFO)


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

    # Set overall test difficulty
    def set_difficulty(self, difficulty: str):
        self.config["difficulty"] = difficulty
        return self

    # Set amount of questions asked
    def set_questions_amount(self, questions_amount: int):
        self.config["questions_amount"] = questions_amount
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

    # Generate test from user's text
    def generate_test(self, users_text: str) -> AITest:
        users_prompt: str = self.__generate_prompt(users_text)

        # Update role for model and add user's text
        LLM_REQUEST["messages"] = [
            {"role": "system", "text": SYS_MESSAGE},
            {"role": "user", "text": users_prompt},
        ]

        try:
            logging.log(logging.INFO, users_prompt)
            response = httpx.post(
                url=REQUEST_URL, headers=REQUEST_HEADERS, json=LLM_REQUEST
            )

        # If failed to send request using httpx
        except Exception as e:
            logging.log(logging.ERROR, str(e))
            raise httpx.RequestError(f"Failed to send POST response. Error: {e}")

        # Something went wrong with LLM Service
        if response.status_code != 200:
            raise httpx.HTTPStatusError(
                f"Incorrect POST request with text: {response.text}"
            )

        logging.log(logging.INFO, response.text)

        json_llm_response = json.loads(response.text)["result"]["alternatives"][0][
            "message"
        ]["text"]
        cleaned_json_llm_response = json_llm_response.replace("`", "")
        llm_answer = json.loads(cleaned_json_llm_response)["test"]

        return AITest(**llm_answer)


# Run module in a unit-environment
if __name__ == "__main__":
    ai = AITestGenerator().set_difficulty("easy").set_questions_amount(1)

    print(
        ai.generate_test(
            "Кириллица — одна из самых известных и широко используемых письменностей в мире, особенно в странах Восточной Европы и на Балкана"
        )
    )
