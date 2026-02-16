"""Verify scheduler-and-commands implementation."""
import sys
sys.path.insert(0, ".")

print("=" * 60)
print("TEST: Message Splitting")
print("=" * 60)

from bot.telegram_handler import split_message

# Test 1: Short message
c1 = split_message("hello world")
assert len(c1) == 1, f"Expected 1 chunk, got {len(c1)}"
print(f"✅ Short message → {len(c1)} chunk")

# Test 2: Long message (10K chars)
c2 = split_message("x" * 10000)
assert len(c2) >= 3, f"Expected 3+ chunks, got {len(c2)}"
print(f"✅ 10K chars → {len(c2)} chunks, sizes: {[len(x) for x in c2]}")

# Test 3: Paragraph split
text = "Para 1 content\n\nPara 2 content\n\n" + "x" * 5000
c3 = split_message(text)
assert len(c3) >= 2
print(f"✅ Paragraph split → {len(c3)} chunks")

# Test 4: Exactly 4000 chars
c4 = split_message("y" * 4000)
assert len(c4) == 1
print(f"✅ Exactly 4000 → {len(c4)} chunk")

# Test 5: 4001 chars
c5 = split_message("z" * 4001)
assert len(c5) == 2
print(f"✅ 4001 chars → {len(c5)} chunks")

print(f"\n{'='*60}")
print("TEST: Config")
print("=" * 60)

import config
print(f"✅ SCHEDULE_HOUR = {config.SCHEDULE_HOUR}")
print(f"✅ SCHEDULE_MINUTE = {config.SCHEDULE_MINUTE}")
print(f"✅ SCHEDULE_ENABLED = {config.SCHEDULE_ENABLED}")
print(f"✅ TIMEZONE = {config.TIMEZONE}")

print(f"\n{'='*60}")
print("TEST: Scheduler Import")
print("=" * 60)

from services.scheduler import init_scheduler, get_scheduler_info, reschedule, pause_scheduler, resume_scheduler
print("✅ All scheduler functions importable")

info = get_scheduler_info()
assert info["status"] == "not_initialized"
print(f"✅ Before init: status = {info['status']}")

print(f"\n{'='*60}")
print("TEST: Command Functions")
print("=" * 60)

from bot.telegram_handler import (
    next_command, skip_command, schedule_command,
    send_long_message, build_application,
)
print("✅ next_command importable")
print("✅ skip_command importable")
print("✅ schedule_command importable")
print("✅ send_long_message importable")
print("✅ build_application importable")

print(f"\n{'='*60}")
print("ALL TESTS PASSED ✅")
print("=" * 60)
