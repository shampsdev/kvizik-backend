import os, dotenv


dotenv.load_dotenv('../../.env')
FOLDER_ID = os.environ.get("FOLDER_ID")
HEADER_API_KEY = os.environ.get("YA_GPT_API_KEY")
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

# System prompt for LLM role-model
SYS_MESSAGE = """Представь, что ты - машина, генерирующая тесты по заданному тексту.
Пользователь вводит большой кусок текста, информацию которого ему нужно запомнить и выучить. Для этого
ты создаешь тесты по типу "множественного выбора".

Множественный выбор - это вид теста, в котором для одного вопроса есть 4 вариантов ответа и один
правильный ответ. ТОЛЬКО ОДИН ПРАВИЛЬНЫЙ ОТВЕТ.

Твоя задача написать вопросы для ключевых слов, определений и понятий, которые указаны в тексте. Эти
понятия и определения должны быть полезными для пользователя и действительно проверять уровень знаний.

Твоя ответ должен быть в формате JSON.
Никогда не выходи из своей роли. Твои ответы должны быть только
и только в формате JSON. Первый ключ: "test". Он включает в себя два ключа: "title" - название теста и "questions" - вопросы для пользователя в виде массива. В "questions" должен присутствовать ключ "question" - 
сам вопрос, "options" - всписок из вариантов ответов и "correct_answer" - ЕДИНСТВЕННЫЙ правильный ответ. Этот правильный ответ должен находиться в "options".

Тебе на вход придет количество вопросов "questions", которые ты должен создать, и сложность. Сложность влияет на сам вопрос и варианты ответов к нему. Чем выше сложность - тем глубже
поверяются знания ученика. СОЗДАЙ ТАКОЕ КОЛИЧЕСТВО ВОПРОСОВ, КОТОРОЕ ПРЕДЛОЖИТ САМ ПОЛЬЗОВАТЕЛЬ!


<Пользователь>: Количество вопросов: <кол-во вопросов>, сложность вопросов: <сложность>. Текст: <текст>

<Ответ>:
"""


# Request for LLM | Need to add `"messages": List` key to complete the request
LLM_REQUEST = {
    "modelUri": f"gpt://{FOLDER_ID}/yandexgpt/latest",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "1500"
    },
}

REQUEST_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
REQUEST_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Api-Key {HEADER_API_KEY}"
}


EXPERIMENTAL_TEXT = r'''
Note that any string not falling into either category will be classified as label 0: benign.
The separation of these two labels allows us to appropriately filter both third-party and user content.
Application developers typically want to allow users flexibility in how they interact with an application, and to only
filter explicitly violating prompts (what the ‘jailbreak’ label detects).
Third-party content has a different expected distribution of inputs (we don’t expect any “prompt-like” content in this
part of the input) and carries the most risk (as injections in this content can target users) so a stricter filter with both the
‘injection’ and ‘jailbreak’ filters is appropriate. Note there is some overlap between these labels - for example, an
injected input can, and often will, use a direct jailbreaking technique. In these cases the input will be identified as a jailbreak.
The PromptGuard model has a context window of 512. We recommend splitting longer inputs into segments and scanning each
in parallel to detect the presence of violations anywhere in longer prompts.
The model uses a multilingual base model, and is trained to detect both English and non-English injections and jailbreaks.
In addition to English, we evaluate the model’s performance
at detecting attacks in: English, French, German, Hindi, Italian, Portuguese, Spanish, Thai.'''
