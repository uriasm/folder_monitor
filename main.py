# -*- coding: utf-8 -*-
from multiprocessing import Process
from app.monitor import Monitor
from app.guest import Guest
import sys
import os


def run_parallel(*fns):
    processes = []
    try:
        for fn in fns:
            process = Process(target=fn)
            process.daemon = True
            process.start()
            processes.append(process)
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise Exception("Sorry! Path argument is required")
    observed_folder = sys.argv[1]
    if not os.path.isdir(observed_folder):
        try:
            os.mkdir(path=observed_folder)
        except Exception as e:
            raise Exception("Sorry! Path argument must be a directory")
    guest = Guest()
    monitor = Monitor(path=observed_folder)
    run_parallel(guest.start_server, monitor.start_observer)
