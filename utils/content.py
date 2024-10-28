# Сохраняем приветственное сообщение в переменную
help_text = """
Привет! Добро пожаловать в КПТ-Бот — твой личный помощник на пути к отказу от курения и улучшению психоэмоционального состояния.
Ты можешь в любой момент *написать* боту и он поможет тебе в сложные моменты. 
Ну или просто запиши голосовое. 


*Что может сделать для тебя КПТ-Бот?*

- *Помочь бросить курить* — с использованием проверенных методов когнитивно-поведенческой терапии (КПТ).
- *Поддержать в трудные моменты* — когда захочешь закурить, бот предложит техники, которые помогут справиться с этим желанием.
- *Проанализировать твои мысли и чувства* — бот задаст наводящие вопросы, чтобы помочь тебе лучше понять свои триггеры и автоматические мысли.
- *Отслеживать твой прогресс* — веди журнал, анализируй свои успехи и смотри, как меняется твое состояние со временем.

*Команды, которые ты можешь использовать:*

- `/start_quiz` — начни с квиза, чтобы бот узнал больше о твоих привычках.
- `/stop_smoking` — готов отказаться от курения? Бот будет присылать тебя актуальную информацию о твоих изменениях здоровья. 
- `/relapse_warning` — если чувствуешь, что можешь сорваться, сообщи об этом боту. Это очень важно для твоего прогресса. Потом ты сможешь посмотреть на всю историю и понять, что помогает тебе справиться с желанием.
- `/notes` — доступ к твоим заметкам.

*Как начать?*
Просто нажми `/start_quiz`, и мы начнем вместе работать над твоими привычками и эмоциональным состоянием. Бот доступен 24/7, так что помощь всегда под рукой.

Начни свой путь к здоровому образу жизни прямо сейчас!
"""

welcome_text = """
Привет! Добро пожаловать в КПТ-Бот — твой личный помощник на пути к отказу от курения и улучшению психоэмоционального состояния.
Ты можешь в любой момент *написать* боту и он поможет тебе в сложные моменты. 
Ну или просто запиши голосовое. 

*Что мы можем сделать вместе?*

- *Изучить твои привычки* — начнем с небольшого квиза, чтобы я лучше понял, что именно тебе нужно.
- *Поддерживать в трудные моменты* — когда тебе захочется закурить, я буду рядом, чтобы предложить техники преодоления желания.
- *Помочь лучше понять свои чувства* — с помощью вопросов и анализа мы разберем триггеры и автоматические мысли.

*Как начать?*
Нажми кнопку ниже и начнем с простого квиза, который поможет мне больше узнать о тебе и твоих привычках.
"""
# Текстовые сообщения для квиза
WELCOME_MESSAGE = """
Я рад, что ты решил сделать важный шаг на пути к отказу от курения! 🚭 Это нелегкое дело, но я буду с тобой на каждом этапе, помогая и поддерживая тебя в борьбе за здоровую и счастливую жизнь. 🌿

Мы вместе справимся с вызовами, и начнем этот путь с небольшого опроса, чтобы я узнал больше о твоих привычках. Это поможет мне лучше понять, как тебя поддержать.

*Итак, что ты куришь?* 🌟
"""


STEP1_CIGARETTES_MESSAGE = "Сколько сигарет в день?"
STEP1_ELECTRONIC_MESSAGE = "Когда ты куришь?"
STEP1_HOOKAH_MESSAGE = "Как часто ты забиваешь чаши?"
STEP1_IQOS_MESSAGE = "Сколько стиков в день?"

STEP2_MESSAGE = "Как давно ты куришь? Выбери один из вариантов:"

STEP3_MESSAGE = "Какова причина твоего желания бросить курить? Лучше всего не торопись и напиши свои мысли. В последствии, мы сможем использовать их для того, чтобы помочь тебе в сложные моменты."

CUSTOM_REASON_PROMPT = "Введите свою причину:"
FINISH_QUIZ_MESSAGE = """
*Отличная работа! Спасибо за ответы!* 🎉

Теперь, когда ты на шаг ближе к свободе от курения, не забывай — ты всегда можешь продолжить свой путь. 


Ксатати просто вызови команду `/stop_smoking`, и мы вместе начнем новый этап — твою жизнь без сигарет! 🚭

Если тебе нужно пересмотреть свои ответы или хочешь пройти квиз заново, ты можешь в любой момент вызвать команду `/start`.

Ты на верном пути, и помощь всегда рядом! 💪
"""


# Текстовые сообщения для опроса при желании сорваться

# content.py

# Сообщения для опроса при желании сорваться
RELAPSE_QUIZ_START_MESSAGE = "Дата: {date_time}\nЕще один шаг к жизни без сигарет! 🚀"
RELAPSE_QUIZ_SITUATION_PROMPT = "Что за место? Где находишься? 👀"
RELAPSE_QUIZ_CUSTOM_SITUATION_PROMPT = "Расскажи, где именно находишься:"
RELAPSE_QUIZ_THOUGHTS_PROMPT = "Какие мысли пролетели в голове? 💭"
RELAPSE_QUIZ_CUSTOM_THOUGHTS_PROMPT = (
    "Напиши, о чем думаешь сейчас что происходит в голове:"
)
RELAPSE_QUIZ_EMOTIONS_PROMPT = "Какие эмоции захватили тебя? 😔"
RELAPSE_QUIZ_EMOTION_SCORE_PROMPT = (
    "Оцени уровень {emotion_type} от 1 до 5. Насколько мощно? 💥"
)
RELAPSE_QUIZ_PHYSICAL_PROMPT = "Что с телом? Прислушайся и опиши ощущения. 🤕"
RELAPSE_QUIZ_CUSTOM_PHYSICAL_PROMPT = "Опиши свои ощущения:"
RELAPSE_QUIZ_BEHAVIOR_PROMPT = 'Вот что я предлагаю сделать 🚶.\nЕсли у тебя есть другие идеи то нажми кнопку "Другое" и напиши что собираешься сделать'
RELAPSE_QUIZ_CUSTOM_BEHAVIOR_PROMPT = "Расскажи-ка как ты справляешься?"
RELAPSE_QUIZ_FINISH_MESSAGE = """

*Отличная работа! 📝*\n\n
Ты завершил очередной шаг на пути к здоровой жизни. Ниже твоя короткая заметка.
Сейчас пришлю несколько советов, которые помогут тебе двигаться дальше.
"""
RELAPSE_QUIZ_ERROR_MESSAGE = "Что-то пошло не так... Начни заново, окей? 🔄"

# Сообщения для автоматического оповещения при отказе от курения
MESSAGES = {
    1: "Поздравляю! Уже через 1 час после отказа от сигарет твое сердце начинает биться ровнее, и давление приходит в норму. Ты уже на правильном пути!",
    3: "Прошло 3 часа без курения! Твой организм начинает снижать уровень никотина в крови. Продолжай, ты отлично справляешься!",
    5: "С момента последней сигареты прошло 5 часов. Кровообращение улучшается, и твое тело начинает восстанавливаться. Ты делаешь важные шаги к здоровью!",
    12: "Прошло 12 часов! Уровень угарного газа в крови снизился до нормы, и твое тело получает больше кислорода. Дышать становится легче!",
    24: "Сутки без сигарет! Ты сделал большой шаг к здоровой жизни. Твои легкие начинают очищаться от слизи и токсинов. Продолжай в том же духе!",
    36: "Прошло 36 часов! Ты уже почувствовал, что запахи и вкусы стали ярче. Твои нервные рецепторы начинают восстанавливаться!",
    48: "Два дня без сигарет! Ты заметил, что твоя способность к физической нагрузке улучшилась. Ты делаешь правильный выбор!",
    72: "Три дня без курения! Твои легкие полностью очищаются от слизи и токсинов. Ты заслужил поздравления!",
    96: "Четыре дня без сигарет! Ты заметил, что у тебя улучшился сон, и ты стал бодрее. Ты на верном пути!",
    120: "Пять дней без курения! Твой организм полностью очищается от никотина. Ты делаешь важный шаг к здоровой жизни!",
    144: "Прошло шесть дней! Твое дыхание стало свежее, и ты заметил, что у тебя улучшился аппетит. Продолжай в том же духе!",
    168: "Одна неделя без сигарет! Ты заметил, что у тебя улучшилось настроение, и ты стал более спокойным. Ты на верном пути!",
}
