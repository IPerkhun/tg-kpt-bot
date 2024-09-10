from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Создаем один экземпляр планировщика
scheduler = AsyncIOScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.start()


def get_scheduler():
    return scheduler
