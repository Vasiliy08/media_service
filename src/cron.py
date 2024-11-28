from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

sheduler = AsyncIOScheduler(timezone="Europe/Moscow")
trigger = CronTrigger(hour=12)


            