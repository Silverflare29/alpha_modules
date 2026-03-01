# FileName: a_logger.py
# Date: March 1, 2026
# Time: 11:00 AM PST
# Iteration Number: 2

import os
from datetime import datetime
from typing import Optional, List, Dict

class Logger:
    """
    A modular, memory-persistent logging system designed for clean architecture.
    Handles console output, iterative ID generation, and categorized file exporting.
    """
    
    def __init__(self, default_tag: str = "X", log_extension: str = ".log"):
        # Customization parameters (Customization First principle)
        self.default_tag = default_tag
        self.log_extension = log_extension
        
        # State management
        self._memory_bank: List[Dict[str, str]] = []
        self._letter_counter: int = 0
        self._number_counter: int = 1
        self._max_number: int = 99999

    def _generate_iterative_letters(self, index: int) -> str:
        """
        Converts an integer index into an Excel-style column string (A, B... Z, AA, AB...).
        Ensures infinite scalability for the LOG ID prefix.
        """
        result = ""
        index += 1
        while index > 0:
            index, remainder = divmod(index - 1, 26)
            result = chr(65 + remainder) + result
        return result

    def _generate_log_id(self, tag: Optional[str]) -> str:
        """
        Generates the unique identifier following the format:
        LOG_<A-Z iterative>_<5 digit iterative number>_<TAG>
        """
        letter_prefix = self._generate_iterative_letters(self._letter_counter)
        number_str = f"{self._number_counter:05d}"
        active_tag = tag if tag else self.default_tag
        
        generated_id = f"LOG_{letter_prefix}_{number_str}_{active_tag}"
        
        # Increment logic
        self._number_counter += 1
        if self._number_counter > self._max_number:
            self._number_counter = 1
            self._letter_counter += 1
            
        return generated_id

    def write(self, 
              input_text: str, 
              tag: Optional[str] = None, 
              log_typeID: Optional[str] = None, 
              log_ID: Optional[str] = None) -> None:
        """
        Writes a log to the console and saves it into the memory bank.
        """
        now = datetime.now()
        timestamp = now.strftime("%d-%m-%y_%H:%M:%S")
        
        # Resolve the Log ID
        final_log_id = log_ID if log_ID else self._generate_log_id(tag)
        
        # Construct optional display strings to prevent "None" from printing
        display_tag = f"{tag} " if tag else ""
        display_type = f"{log_typeID} " if log_typeID else ""
        
        # Core formatting: [Timestamp] (ID) TAG TYPEID --- \t INPUT
        formatted_log = f"[{timestamp}] ({final_log_id}) {display_tag}{display_type}--- \t{input_text}"
        
        # Output to console
        print(formatted_log)
        
        # Persist to memory for later saving
        self._memory_bank.append({
            "tag": tag,
            "formatted_string": formatted_log
        })

    def save(self, 
             path: str = "/", 
             file_name: Optional[str] = None, 
             log_category: Optional[str] = None) -> None:
        """
        Dumps the memory bank into a physical log file.
        Filters by category if requested. Defaults to current directory if no path is provided.
        """
        now = datetime.now()
        
        # File-system safe timestamp (Replacing ':' with '-')
        # This prevents OS-level errors on Windows/Mac when writing files.
        safe_timestamp = now.strftime("%d-%m-%y_%H-%M-%S")
        prefix = f"LOG_{safe_timestamp}"
        
        # Construct final file name
        final_name = f"{prefix}_{file_name}{self.log_extension}" if file_name else f"{prefix}{self.log_extension}"
        
        # Path resolution logic
        if path == "/":
            # Saves to the exact directory where this python script lives
            save_directory = os.path.dirname(os.path.abspath(__file__))
        else:
            save_directory = path
            
        # Ensure the directory exists (Boilerplate avoidance)
        os.makedirs(save_directory, exist_ok=True)
        full_file_path = os.path.join(save_directory, final_name)
        
        # Filter logic (DRY principle applied via list comprehension)
        logs_to_export = self._memory_bank
        if log_category:
            logs_to_export = [log for log in self._memory_bank if log["tag"] == log_category]
            
        # Write out to file
        with open(full_file_path, "w", encoding="utf-8") as file:
            for log in logs_to_export:
                file.write(log["formatted_string"] + "\n")
                
        print(f"\n✅ System: Log file successfully exported to -> {full_file_path}")

# Module-level default instance (Singleton Pattern implementation)
log = Logger()

# ==========================================
# 🧪 DEMONSTRATION & TESTING (Can be deleted)
# ==========================================
if __name__ == "__main__":
    print("--- Starting Logger Demonstration ---")
    
    # Standard log
    log.write("System Initialized")
    
    # Log with tag
    log.write("Database connected successfully.", tag="DB_AUTH")
    
    # Log with tag and TypeID
    log.write("User 'admin' failed login attempt.", tag="SECURITY", log_typeID="ERR_042")
    
    # Log with custom ID overrides iterative system
    log.write("Manual override triggered.", tag="CORE", log_ID="LOG_CUSTOM_999")
    
    # Let's write a few more to test iteration
    for i in range(3):
        log.write(f"Background worker ping {i+1}", tag="WORKER")

    # Save ALL logs to current directory
    log.save(file_name="Full_System_Dump")
    
    # Save ONLY 'WORKER' tagged logs
    log.save(file_name="Worker_Metrics", log_category="WORKER")