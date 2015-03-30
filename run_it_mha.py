

__author__ = 'Mohammad Hossein Amri- mhamri@gmail.com'

import sys
import threading
import logging
import os
import time
import getopt


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
    time.sleep(10)


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


# --------------------------------------------------------------------
def print_help():
    print
    print '#  Run a file multi thread :'
    print '-h  <show this help>'
    print '-c  <command to run>'
    print '-n  <number of threads, default: 3>'
    print '-t  <time between threads, default: 0sec>'
    print '-b  <time between batches, default: 50sec>'
    print


def main(argv):
    if len(argv) == 0:
        print_help()
        sys.exit(2)

    no_threads = 3  # number of threads that can run all together, the whole number of threads will call a job
    time_between_threads = float(0)  # how many SECONDS gap between run of each thread
    time_between_batches = float(50)  # how many SECONDS gap between run of each job
    threads = []  # to keep track of all jobs
    command_to_run = '';

    try:
        opts, args = getopt.getopt(argv, "hc:n:t:b:", ["help"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            print_help()
            sys.exit()
        elif o in "-c":
            command_to_run = a
        elif o in "-n":
            no_threads = int(a)
        elif o in "-t":
            time_between_threads = float(a)
        elif o in "-b":
            time_between_batches = float(a)
        else:
            sys.exit()

    if command_to_run == '':
        print "it's needed to insert a command to run"
        sys.exit()

    cnt = 0
    while True:

        if cnt == no_threads:
            time.sleep(time_between_batches)
            cnt = 0

        threads = check_alive_threads(threads)

        if len(threads) < no_threads:
            t = threading.Thread(target=agent, args=(command_to_run,))
            t.setDaemon(True)
            t.start()
            threads.append(t)
            cnt += 1
            time.sleep(time_between_threads)

        else:
            for thread_item in threads:
                thread_item.join()


if __name__ == "__main__":
    main(sys.argv[1:])





