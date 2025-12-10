# Module Explanations

## 1. main.py
- The entry point of the application
- Loads the Tkinter GUI dashboard
- Handles navigation to each tool window

---

## 2. calculator.py
- Contains Calculator class
- Performs arithmetic operations
- Logs results into `calculator_log.csv`

---

## 3. notes_manager.py
- Stores notes in JSON format
- Supports add, edit, delete, search
- Implements Note class & data handling

---

## 4. timer.py
- Contains Timer and Stopwatch classes
- Uses Tkinter popups for time display

---

## 5. file_organizer.py
- Reads files from a selected directory
- Categorizes and moves files safely

---

## 6. unit_converter.py
- Converts units: length, weight, temperature
- Extensible design for adding more units

---

## 7. backup_manager.py
- Creates timestamped backups
- Restores old backups safely
- Handles file copying operations

---

## 8. utils.py
- Shared functions: time formatting, paths, validation
