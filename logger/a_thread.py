"""
FileName: a_thread.py
Date: 2026-03-01
Time: 11:04:00
Iteration: 2
Description: A robust, OOP-based threading module for background task execution with state checking.
"""

import threading
import time
from typing import Callable, Optional, Dict

class BackgroundTask:
    # 📝 Registry to track active thread instances by name to prevent collisions
    _registry: Dict[str, 'BackgroundTask'] = {}

    def __init__(self, thread_name: str):
        """
        Initializes a new background task instance.
        :param thread_name: Unique identifier for the thread.
        """
        self.name = thread_name
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    @classmethod
    def run(cls, 
            thread_name: str, 
            func: Callable, 
            iter_type: Optional[str] = 'o', 
            lim: Optional[int] = None):
        """
        Main entry point to execute a function in the background.
        :param thread_name: The name used to track/stop the thread.
        :param func: The function to execute.
        :param iter_type: 't' (time in sec), 'i' (iterations), 'o' (infinite).
        :param lim: The limit value for time or iterations.
        """
        
        # ✅ Logic Check: If thread name exists, stop the previous one first
        if thread_name in cls._registry:
            print(f"⚠️ Thread '{thread_name}' is already active. Refactoring: Stopping previous instance...")
            cls.stop(thread_name)

        # Create new instance and register it
        instance = cls(thread_name)
        cls._registry[thread_name] = instance
        
        # Define the wrapper logic based on iter_type
        def thread_wrapper():
            start_time = time.time()
            iterations = 0

            try:
                while not instance._stop_event.is_set():
                    # Execute the user-provided function
                    func()

                    iterations += 1

                    # 📝 Logic Validation for limits
                    if iter_type == 'i' and lim is not None:
                        if iterations >= lim:
                            break
                    elif iter_type == 't' and lim is not None:
                        if (time.time() - start_time) >= lim:
                            break
                    elif iter_type == 'o':
                        # Infinite loop; relies solely on .stop() or app exit
                        pass
                    else:
                        # Default: Run once if no valid iter_type is provided
                        if iter_type not in ['t', 'i', 'o'] or lim is None:
                            break
                    
                    # Small sleep to prevent 100% CPU usage in infinite loops
                    time.sleep(0.01) 
            finally:
                # Clean up registry upon natural completion or forced stop
                if thread_name in cls._registry:
                    del cls._registry[thread_name]

        # Initialize and start the Python Thread
        instance._thread = threading.Thread(target=thread_wrapper, name=thread_name, daemon=True)
        instance._thread.start()
        print(f"✅ Thread '{thread_name}' started successfully.")

    @classmethod
    def stop(cls, thread_name: str):
        """
        Signals a specific background thread to stop and removes it from registry.
        :param thread_name: The name of the thread to terminate.
        """
        if thread_name in cls._registry:
            instance = cls._registry[thread_name]
            instance._stop_event.set()
            # Wait briefly for the thread to acknowledge the stop signal
            if instance._thread:
                instance._thread.join(timeout=2.0)
            
            # Double check cleanup in case finally block was delayed
            if thread_name in cls._registry:
                del cls._registry[thread_name]
            print(f"🛑 Thread '{thread_name}' has been stopped.")
        else:
            print(f"❓ No active thread found with name: {thread_name}")

    @classmethod
    def running(cls, thread_name: str) -> bool:
        """
        Checks if a specific background thread is currently active and alive.
        :param thread_name: The name of the thread to check.
        :return: True if running, False otherwise.
        """
        if thread_name in cls._registry:
            instance = cls._registry[thread_name]
            if instance._thread:
                # ✅ Validate directly against the OS thread state
                return instance._thread.is_alive()
        return False

# Shorthand aliases to match user request syntax cleanly
def run(func, thread_name="default_task", iter_type='o', lim=None):
    BackgroundTask.run(thread_name, func, iter_type, lim)

def stop(thread_name="default_task"):
    BackgroundTask.stop(thread_name)

def running(thread_name="default_task") -> bool:
    return BackgroundTask.running(thread_name)