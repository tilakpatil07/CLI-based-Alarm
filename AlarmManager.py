import threading
from datetime import datetime, timedelta
from Alarm import Alarm

class AlarmManager:
    """Manages the array of alarms and business logic operations."""
    def __init__(self):
        self.alarms = []
        self._next_id = 1
        self.lock = threading.Lock()  # Prevents race conditions between Main & BG thread

    def add_alarm(self, time_string: str) -> Alarm:
        try:
            parsed_time = datetime.strptime(time_string.strip(), "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid time format. Please use HH:MM (24-hour format).")

        now = datetime.now()
        target_datetime = datetime.combine(now.date(), parsed_time)
        
        # If time passed today, roll it over to tomorrow
        if target_datetime <= now:
            target_datetime += timedelta(days=1)

        with self.lock:
            new_alarm = Alarm(self._next_id, time_string, target_datetime)
            self.alarms.append(new_alarm)
            self._next_id += 1
            return new_alarm

    def toggle_alarm(self, alarm_id: int) -> bool:
        with self.lock:
            for alarm in self.alarms:
                if alarm.id == alarm_id:
                    alarm.is_enabled = not alarm.is_enabled
                    # If turning back on, ensure it hasn't expired in the past
                    if alarm.is_enabled:
                        alarm.reset_if_passed()
                    return True
        return False

    def delete_alarm(self, alarm_id: int) -> bool:
        with self.lock:
            for i, alarm in enumerate(self.alarms):
                if alarm.id == alarm_id:
                    self.alarms.pop(i)
                    return True
        return False

    def get_all_alarms(self):
        with self.lock:
            # Return a snapshot copy to prevent concurrent modification issues during iteration
            return list(self.alarms)