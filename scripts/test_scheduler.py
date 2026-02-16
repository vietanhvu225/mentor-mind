"""
Full scheduler diagnostic — simulates the bot's scheduler lifecycle.
Logs everything to data/scheduler_diagnostic.log AND stdout.
"""
import asyncio
import logging
import sys
sys.path.insert(0, ".")

# Log to BOTH file and stdout
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.FileHandler("data/scheduler_diagnostic.log", mode="w"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("DIAG")

import config

async def main():
    logger.info("=" * 60)
    logger.info("SCHEDULER DIAGNOSTIC")
    logger.info("=" * 60)
    
    # 1. Check config
    logger.info(f"SCHEDULE_HOUR = {config.SCHEDULE_HOUR}")
    logger.info(f"SCHEDULE_MINUTE = {config.SCHEDULE_MINUTE}")
    logger.info(f"SCHEDULE_ENABLED = {config.SCHEDULE_ENABLED} (type={type(config.SCHEDULE_ENABLED).__name__})")
    logger.info(f"TIMEZONE = {config.TIMEZONE}")
    logger.info(f"CHAT_ID = {config.TELEGRAM_CHAT_ID}")
    
    # 2. Test APScheduler with CronTrigger (same as real code)
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    from datetime import datetime
    
    fired_event = asyncio.Event()
    
    async def test_cron_job():
        logger.info("✅✅✅ CRON JOB FIRED! ✅✅✅")
        fired_event.set()
    
    # Use current minute + 1 for testing
    now = datetime.now()
    test_minute = (now.minute + 1) % 60
    test_hour = now.hour if test_minute > now.minute else (now.hour + 1) % 24
    
    logger.info(f"Current time: {now.strftime('%H:%M:%S')}")
    logger.info(f"Setting cron to: {test_hour:02d}:{test_minute:02d}")
    
    scheduler = AsyncIOScheduler(timezone=config.TIMEZONE)
    
    scheduler.add_job(
        test_cron_job,
        CronTrigger(
            hour=test_hour,
            minute=test_minute,
            timezone=config.TIMEZONE,
        ),
        id="diag_test",
        name="Diagnostic Test Job",
        replace_existing=True,
    )
    
    scheduler.start()
    logger.info("Scheduler started")
    
    # List all jobs
    jobs = scheduler.get_jobs()
    for job in jobs:
        logger.info(f"Job: {job.name}, next_run={job.next_run_time}, trigger={job.trigger}")
    
    # Wait up to 90 seconds for the job to fire
    logger.info(f"Waiting up to 90 seconds for job to fire at {test_hour:02d}:{test_minute:02d}...")
    
    try:
        await asyncio.wait_for(fired_event.wait(), timeout=90)
        logger.info("✅ CRON JOB SUCCESSFULLY FIRED")
    except asyncio.TimeoutError:
        logger.error("❌ CRON JOB DID NOT FIRE WITHIN 90 SECONDS")
    
    scheduler.shutdown()
    logger.info("Done")

if __name__ == "__main__":
    asyncio.run(main())
