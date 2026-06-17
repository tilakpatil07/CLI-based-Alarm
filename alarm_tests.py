import unittest
from datetime import datetime, timedelta
# Assuming your helper file is named alarm_helpers.py
from AlarmManager import AlarmManager

class TestAlarmManager(unittest.TestCase):

    def setUp(self):
        """Runs before every individual test. Gives us a fresh manager instance."""
        self.manager = AlarmManager()

    def test_add_valid_alarm(self):
        """Ensure a properly formatted 24h string creates an active alarm instance."""
        # Setup a time format we know is valid
        alarm = self.manager.add_alarm("23:45")
        
        self.assertEqual(alarm.time_string, "23:45")
        self.assertTrue(alarm.is_enabled)
        self.assertEqual(len(self.manager.get_all_alarms()), 1)
        self.assertEqual(alarm.id, 1)

    def test_add_invalid_alarm_format(self):
        """Ensure bad inputs throw clear ValueErrors instead of corrupting state."""
        invalid_inputs = ["abc", "25:00", "2:30 PM", "1430", "12.30"]
        
        for bad_input in invalid_inputs:
            with self.subTest(input=bad_input):
                with self.assertRaises(ValueError):
                    self.manager.add_alarm(bad_input)
                    
        # Verify no alarms were accidentally stored
        self.assertEqual(len(self.manager.get_all_alarms()), 0)

    def test_past_time_rollover(self):
        """Ensure an alarm set for a time that already passed today schedules for tomorrow."""
        now = datetime.now()
        # Calculate a time string from 5 minutes ago
        past_time_obj = now - timedelta(minutes=5)
        past_time_str = past_time_obj.strftime("%H:%M")
        
        alarm = self.manager.add_alarm(past_time_str)
        
        # The target date MUST be strictly greater than right now (scheduled for tomorrow)
        self.assertTrue(alarm.target_datetime > now)
        self.assertEqual(alarm.target_datetime.date(), (now + timedelta(days=1)).date())

    def test_toggle_alarm_state(self):
        """Verify that toggling flips the enable status and handles non-existent IDs."""
        alarm = self.manager.add_alarm("12:00")
        self.assertTrue(alarm.is_enabled)
        
        # Toggle OFF
        success = self.manager.toggle_alarm(alarm.id)
        self.assertTrue(success)
        self.assertFalse(alarm.is_enabled)
        
        # Toggle ON
        success = self.manager.toggle_alarm(alarm.id)
        self.assertTrue(success)
        self.assertTrue(alarm.is_enabled)
        
        # Test toggling an invalid ID
        fail_success = self.manager.toggle_alarm(999)
        self.assertFalse(fail_success)

    def test_delete_alarm(self):
        """Verify that an alarm is completely removed from memory by its ID."""
        alarm1 = self.manager.add_alarm("08:00")
        alarm2 = self.manager.add_alarm("09:00")
        self.assertEqual(len(self.manager.get_all_alarms()), 2)
        
        # Delete the first alarm
        success = self.manager.delete_alarm(alarm1.id)
        self.assertTrue(success)
        
        # State verification
        remaining_alarms = self.manager.get_all_alarms()
        self.assertEqual(len(remaining_alarms), 1)
        self.assertEqual(remaining_alarms[0].id, alarm2.id)
        
        # Test deleting a non-existent ID
        fail_success = self.manager.delete_alarm(999)
        self.assertFalse(fail_success)

if __name__ == "__main__":
    unittest.main()