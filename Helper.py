from datetime import datetime, timedelta
import time
from AlarmManager import AlarmManager
from Alarm import Alarm
import threading

shared_manager = AlarmManager()

def trigger_alarm_sequence(alarm: Alarm):
    """Fires when an alarm time matches. Rings until a key is pressed."""
    print(f"\n\n⏰!!! ALARM TRIGGERED: [{alarm.time_string}] !!!⏰")
    print("Press Ctrl+C inside the menu to halt ring loops.")
    
    # Simple alert block
    for _ in range(5):  # Ring 5 times so it doesn't indefinitely hang the thread
        time.sleep(0.5)
    print("\nAlarm alert ended. Return to your menu selections.")


def global_alarm_ticker():
    """Background engine that constantly sweeps the array of alarms."""
    while True:
        now = datetime.now()
        alarms = shared_manager.get_all_alarms()
        
        for alarm in alarms:
            if alarm.is_enabled and now >= alarm.target_datetime:
                # Disable it immediately so it doesn't re-trigger next second
                shared_manager.toggle_alarm(alarm.id)
                
                # Fire the alarm sequence on a separate transient thread 
                # so the ticking loop keeps tracking remaining alarms
                alert_thread = threading.Thread(target=trigger_alarm_sequence, args=(alarm,), daemon=True)
                alert_thread.start()
                
        time.sleep(1)


def display_alarms_menu():
    print("\n--- Current Alarms ---")
    alarms = shared_manager.get_all_alarms()
    if not alarms:
        print("No alarms set currently.")
        return

    for alarm in alarms:
        status = "ON" if alarm.is_enabled else "OFF"
        target_str = alarm.target_datetime.strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{alarm.id}] Time: {alarm.time_string} | Status: {status} | Next Ring: {target_str}")