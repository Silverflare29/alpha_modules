"""
FileName: example_usage.py
Date: 2024-05-22
Time: 14:35:00
Iteration: 1
Description: Test script to verify the functionality of a_thread module.
"""

import a_thread
import time

def my_heavy_work():
    # 📝 Simple function to simulate background work
    print("...Working in background...")
    time.sleep(1)

def main():
    print("🚀 Main Program Started.")

    # 1. Run a thread for 5 seconds
    print("\n--- Test 1: Time Bound (5s) ---")
    a_thread.run(my_heavy_work, thread_name="TimerTask", iter_type='t', lim=5)

    # 2. Run a thread for 3 iterations
    print("\n--- Test 2: Iteration Bound (3 times) ---")
    a_thread.run(my_heavy_work, thread_name="IterTask", iter_type='i', lim=3)

    # 3. Run an infinite thread and stop it manually
    print("\n--- Test 3: Infinite then Manual Stop ---")
    a_thread.run(my_heavy_work, thread_name="ManualTask", iter_type='o')
    
    time.sleep(3) # Let it run for 3 seconds
    a_thread.stop("ManualTask")

    # 4. Collision Test (Try running the same name twice)
    print("\n--- Test 4: Collision Handling ---")
    a_thread.run(my_heavy_work, thread_name="CollisionTest", iter_type='o')
    time.sleep(1)
    # This should trigger the "Stop previous instance" logic
    a_thread.run(my_heavy_work, thread_name="CollisionTest", iter_type='i', lim=2)

    print("\n🏁 Main Program Finished. (Background threads may still be closing)")

if __name__ == "__main__":
    main()