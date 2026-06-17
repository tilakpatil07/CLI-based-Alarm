import sys
import threading
from Helper import global_alarm_ticker
from Helper import display_alarms_menu
from Helper import shared_manager


def main():
    # Spin up the background clock worker engine2
    bg_engine = threading.Thread(target=global_alarm_ticker, daemon=True)
    bg_engine.start()


    while True:
        print("\n=== Interactive Alarm Menu ===")
        print("1. View / Toggle Alarms")
        print("2. Add New Alarm")
        print("3. Delete an Alarm")
        print("4. Exit Application")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == "1":
            display_alarms_menu()
            alarms = shared_manager.get_all_alarms()
            if alarms:
                toggle_choice = input("\nEnter an Alarm ID to toggle ON/OFF (or press Enter to return): ").strip()
                if toggle_choice.isdigit():
                    success = shared_manager.toggle_alarm(int(toggle_choice))
                    print("Status updated successfully!" if success else "Alarm ID not found.")

        elif choice == "2":
            time_input = input("Enter alarm time (HH:MM 24-hour format): ").strip()
            try:
                new_alarm = shared_manager.add_alarm(time_input)
                print(f"Success! Saved Alarm [{new_alarm.id}] for {new_alarm.time_string}")

                print(f"[DEBUG] Total alarms in memory: {len(shared_manager.alarms)}")

            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            display_alarms_menu()
            alarms = shared_manager.get_all_alarms()
            if alarms:
                delete_choice = input("\nEnter Alarm ID to permanently delete: ").strip()
                if delete_choice.isdigit():
                    success = shared_manager.delete_alarm(int(delete_choice))
                    print("Alarm removed." if success else "Alarm ID not found.")

        elif choice == "4" or choice.lower() in ['exit', 'quit']:
            print("Shutting down clock engine. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid input choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication closed unexpectedly via Ctrl+C. Goodbye!")
        sys.exit(0)