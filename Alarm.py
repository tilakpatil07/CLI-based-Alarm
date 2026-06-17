from datetime import datetime, timedelta

class Alarm:
    """Represents an individual alarm instance."""
    def __init__(self, alarm_id: int, time_string: str, target_datetime: datetime):
        self.id = alarm_id
        self.time_string = time_string  # Original "HH:MM" format
        self.target_datetime = target_datetime
        self.is_enabled = True

    def reset_if_passed(self):
        """If an active alarm's time is in the past, roll it over to tomorrow."""
        now = datetime.now()
        if self.target_datetime <= now:
            self.target_datetime = datetime.combine(now.date(), self.target_datetime.time())
            if self.target_datetime <= now:
                self.target_datetime += timedelta(days=1)