#!/usr/bin/env python3

import time
import multiprocessing

def cpu_stress():
    while True:
        pass

def main():
    print("Starting CPU stress test for 2 minutes...")
    processes = []

    try:
        for i in range(2):
            process = multiprocessing.Process(target=cpu_stress)
            process.start()
            processes.append(process)

        time.sleep(120)

    finally:
        for process in processes:
            process.terminate()
            process.join()

        print("CPU stress test completed.")

if __name__ == "__main__":
    main()
