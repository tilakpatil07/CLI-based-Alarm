# Multi-Threaded CLI Alarm Clock Engine

A robust, thread-safe Python CLI alarm clock application built entirely with the Python Standard Library. This application features an interactive text-driven menu, support for scheduling and managing multiple simultaneous alarms, active status toggles, and cross-platform hardware audio alerts—all running without any external dependencies or databases.

---

## 🛠️ Architectural Decisions

To deliver a high-quality CLI application without relying on a database or web server, the project utilizes an asynchronous, decoupled multi-threaded architecture:

* **Separation of Concerns:** Business logic and state management are encapsulated entirely within the `AlarmManager` class (`alarm_helpers.py`), decoupling data manipulation from terminal I/O and rendering loops (`main.py`).
* **Thread Safety (Mutex Locking):** Because multiple threads access and mutate the alarm collection concurrently, a `threading.Lock()` primitive enforces mutual exclusion. This guarantees that background clock checks never suffer from race conditions or data corruption if a user attempts to add, delete, or toggle an alarm at the exact same millisecond.
* **Non-Blocking Background Engine:** A background daemon thread manages time tracking by sweeping the inventory of active alarms every second. 
* **Transient Alert Threading:** When an alarm matches, the engine spawns an isolated, transient thread to execute the visual-audio alert loop. This ensures that the primary background ticker loop is never blocked, allowing multiple alarms scheduled for the exact same second to fire simultaneously without lagging.
* **Resource Cleanup:** The background components run as `daemon` threads, ensuring that when the user exits the main thread interface, all background workers terminate instantly without leaving orphaned processes.

## 🚀 Key Features
Interactive Control Panel: A persistent terminal menu allowing users to view current alarms, add new entries, toggle active/inactive states, or delete alarms cleanly.

Intelligent Date Roll-Over: Schedules times that have already passed for tomorrow automatically (e.g., setting a 10:00 alarm at 14:00 will dynamically schedule it for 10:00 AM the following calendar day).

State Toggling: Temporarily pause/unpause individual alarms by their unique ID without deleting their configuration.

Visual Polish: Uses terminal carriage returns (\r) to display visual flashing alerts right in place without printing endless rows of spam down the terminal screen history.

## 🚀 Usage Guide
Upon launching, interact with the application using numeric menu entries:

Press 1 to view all configured alarms along with their status (ON/OFF) and exact calculated next ring timestamps. While in this menu, you can input an Alarm ID to toggle it.

Press 2 to provision a new alarm using HH:MM 24-hour syntax (e.g., 07:30, 16:45).

Press 3 to permanently remove an alarm from memory by target ID.

Press 4 (or type exit/quit) to gracefully stop the engine and close the app. Use Ctrl+C inside an active alarm trigger loop to silence the sound.

🧪 Automated Testing
The project contains an isolated test suite validating formatting boundary inputs, input mutation handling, and core date/time calculations.

* 🚀 Here are those future improvements condensed into quick, high-impact bullet points:

**JSON Persistence Layer**: Saves alarms to a local alarms.json file so scheduled alerts survive application restarts and system reboots.

**Event-Driven Scheduling**: Replaces the 1-second busy-wait polling loop with Python's sched or asyncio modules to wake up only when an alarm is due, drastically reducing CPU usage.

**Snooze & Recurrence Features**: Adds functionality for calendar-based recurring profiles (e.g., Weekdays at 08:00) and temporary 5-minute snooze delays.

