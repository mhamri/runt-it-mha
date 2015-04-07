import getopt
import json
import os
import subprocess
import shlex
import sys
from tabulate import tabulate
# test

__author__ = 'Mohammad Hossein Amri- hossein.amri@photobookworldwide.com - mhamri@gmail.com'

# {
# "command Name" :[
# "command" : "command name ",
# "threads_number": "number of thread",
# "threads_time" : "time between thread",
# "batches_time" : "time between batches"
# ]
# }


def read_json(content):
    return json.loads(content)


# ps -e -T

def check_process(process_path):
    process_path = process_path.replace('"', '')
    proc1 = subprocess.Popen(shlex.split('ps -ef'), stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(shlex.split('grep "[[:digit:]].' + process_path + '"'), stdin=proc1.stdout,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc1.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.
    out, err = proc2.communicate()
    out_array = out.split('\n')

    if len(out_array) > 0:
        for stri in out_array:
            if not stri.strip():
                out_array.remove(stri)

    if not err.strip():
        return out_array
    return []


def read_command_file(command_file):
    with open(command_file, 'r') as content_file:
        content = content_file.read()
        return content
    return false


def print_help():
    print
    print '#  Run a file multi thread :'
    print '-h | --help  shows this help'
    print '-l           list of action action item'
    print '-i <name>    information about an action item '
    print '-p           list of process'
    print '-t <name>    show subtree of an action item'
    print '-k <name>    kill the process belong to an action item'
    print '-r <name>    run the process belong to an action item'
    print


def run_shell_command(command):
    subprocess.Popen(shlex.split(command))


def return_max_length(value):
    array_value = value.split(' ')
    max_length = float("-inf")
    for i in array_value:
        if len(i) > max_length:
            max_length = len(i)
    return max_length


def show_command_list(command_json_list, print_this=None):
    itera = command_json_list['commands']
    header = ['Option', 'Value']

    key_length_max = 1
    value_length_max = 1
    table = []
    item_to_iterate = {}
    for i in itera:

        if print_this is not None:
            if i['name'] == print_this.lower():
                item_to_iterate = i
            else:
                continue
        else:
            item_to_iterate = i

        for k, v in item_to_iterate.iteritems():
            table.append([k, v])

            if key_length_max < len(k):
                key_length_max = len(k)

            if value_length_max < len(v):
                value_length_max = len(v)

        table.append(['-' * key_length_max, '-' * value_length_max])
    print
    # print ('='*key_length_max)+'=='+('='*value_length_max)
    print "Agents Configuration: "
    if print_this is None:
       print "\n\t\t\tuse -i <name> to see running methods of the agent"
    # print ('-'*key_length_max)+'--'+('-'*value_length_max)
    print
    table.insert(0, ['Option', 'Value'])
    table.insert(1, ['=' * key_length_max, '=' * value_length_max])
    print tabulate(table, tablefmt="plain")
    print


def show_process_report(command_json_list):
    for json_object in command_json_list["commands"]:
        process = check_process(json_object["run"])
        print process


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hli:p:", ["help"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    show_all_command = False
    show_command = False
    show_process= False
    passed_arg=''
    for o, a in opts:
        if o in ("-h", "--help"):
            print_help()
            sys.exit()
        elif o in "-l":
            show_all_command = True
        elif o in "-i":
            show_command=True
            passed_arg=a
        elif o in "-p":
            show_process=True
        elif o in "-b":
            time_between_batches = float(a)
        else:
            sys.exit()

    command_file = os.getcwd() + '/commands.json'
    commands_file_content = read_command_file(command_file)
    batch_to_run = read_json(commands_file_content)

    show_process_report(batch_to_run)

    # show_command_list(batch_to_run)
    #
    # if show_all_command:
    #     show_command_list(batch_to_run)
    # elif show_command:
    #     show_command_list(batch_to_run, passed_arg)

    # for json_object in batch_to_run["commands"]:
    # process = check_process(json_object["run"])
    # if len(process) != 1:
    # # kill process
    # # run new process
    # run_shell_command(json_object["run"])
    #
    # os._exit(-1)


if __name__ == '__main__':
    main(sys.argv[1:])








