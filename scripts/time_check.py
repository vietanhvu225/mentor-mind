from datetime import datetime
import pytz  

ict = pytz.timezone('Asia/Ho_Chi_Minh')
now_sys = datetime.now()
now_ict = datetime.now(ict)

with open("data/time_check.txt", "w") as f:
    f.write(f"System datetime.now(): {now_sys}\n")
    f.write(f"ICT datetime.now(ict): {now_ict}\n")
    f.write(f"System hour: {now_sys.hour}, ICT hour: {now_ict.hour}\n")
    f.write(f"Difference: ICT is {(now_ict.hour - now_sys.hour) % 24}h ahead of system\n")

    # What APScheduler sees for a cron job at 00:27 ICT
    import config
    f.write(f"\nConfig: HOUR={config.SCHEDULE_HOUR}, MIN={config.SCHEDULE_MINUTE}\n")
    f.write(f"This means job runs at {config.SCHEDULE_HOUR:02d}:{config.SCHEDULE_MINUTE:02d} ICT\n")
    
    from apscheduler.triggers.cron import CronTrigger
    trigger = CronTrigger(hour=config.SCHEDULE_HOUR, minute=config.SCHEDULE_MINUTE, timezone='Asia/Ho_Chi_Minh')
    next_fire = trigger.get_next_fire_time(None, now_ict)
    f.write(f"Next fire time: {next_fire}\n")
    f.write(f"That is in: {next_fire - now_ict}\n")

print("Written to data/time_check.txt")
