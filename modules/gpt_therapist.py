# %%
import openai
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

PROMPT_INSTRUCTIONS = """
Ты КПТ психотерапевт. Твоя задача - помочь пациенту справиться с никотиновой зависимостью. Пациент рассказывает тебе о своих заметках о том как он справлялся с желанием курить. 
Заметки получаешь в виде json.
{
    "current_step": null,
    "date_time": "03.09.2024 12:01",
    "situation": "На вечеринке",
    "thoughts": "Курение поможет мне успокоиться",
    "emotion_type": "Тревога",
    "emotion_score": 4,
    "physical": "Дрожь в руках",
    "behavior": "Сделать физическую нагрузку"
},

Так же ты будешь получать дату когда пациент решил бросить курить.
Верни рекомендации и поддержи его в его нелёгком решении. 
Это должно быть короткое сообщение 30-50 слов, которое поможет пациенту справиться с желанием курить.
Должно несколько советов действий, которые помогут пациенту справиться с желанием курить и максимум одно поддерживающее утверждение.

Примеры ответов:
Ты на верном пути! В моменты тревоги попробуй заменить курение на глубокое дыхание или короткую прогулку. Это поможет снизить напряжение. Также может помочь записать свои мысли и чувства. Ты справляешься с этим! Я в тебя верю!
"""


class GPTTherapist:
    def __init__(self, api_key: str = API_KEY):
        self.prompt = PROMPT_INSTRUCTIONS
        openai.api_key = api_key
        self.client = openai.OpenAI()

    def _build_user_input(
        self, start_date: str, current_date: str, data: List[Dict]
    ) -> str:
        user_input = f"{data} не курю с {start_date} время сейчас {current_date}"
        return user_input

    def get_help(self, data: List[Dict], start_date=None, current_date=None) -> str:
        user_input = self._build_user_input(start_date, current_date, data)
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": user_input},
            ],
            max_tokens=200,
            temperature=1.0,
        )
        return completion.choices[0].message.content
