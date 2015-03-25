__author__ = 'Mohammad Hossein Amri- hossein.amri@photobookworldwide.com - mhamri@gmail.com'

import threading
import logging
import os
import time


logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


def agent(full_path_file):
    """

    :param full_path_file: the full path of the file that need to be run
    """
    logging.debug('Starting')
    os.system(full_path_file)
    logging.debug('Exiting')


def check_alive_threads(threads_array):
    """

    it will get an array of threads and check which one is alive.
    if it wasn't alive, then it will remove it from the reference

    :rtype : array threading.thread()
    :param array threads_array: array of threads
    :return: array of threads after removing reference to stopped one
    """
    for threadItem in threads_array:

        if not threadItem.is_alive():
            threads_array.remove(threadItem)

    return threads_array


noThreads = 3  # number of threads that can run all together, the whole number of threads will call a job
time_between_threads = 0  # how many SECONDS gap between run of each thread
time_between_batches = 50  # how many SECONDS gap between run of each job
threads = []  # to keep track of all jobs
file_name = 'test.php'
file_path = 'php ' + os.getcwd() + file_name

while True:

    threads = check_alive_threads(threads)
    if len(threads) < noThreads:
        t = threading.Thread(target=agent, args=(file_path,))
        t.setDaemon(True)
        t.start()
        threads.append(t)

    else:
        for thread_item in threads:
            thread_item.join()
        time.sleep(time_between_batches)





