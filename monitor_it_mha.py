import getopt
import json
import os
import subprocess
import shlex
import sys
from tabulate import tabulate
import re
# test

__author__ = 'Mohammad Hossein Amri- mhamri@gmail.com'

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
    print '-i name    information about an action item '
    print '-p           list of process'
    print '-t name    show subtree of an action item'
    print '-k name    kill the process belong to an action item'
    print '-k name_pid    kill the process belong to an action item'
    print '-r name    run the process belong to an action item'
    print '-q name    run the process belong to an action item without taking care of one instance'
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


def show_process_report(command_json_list, just_this=None, subtree=False, kill=False):
    any_process = False
    for json_object in command_json_list["commands"]:
        if just_this is not None:
            if json_object['name'] != (just_this.split('_'))[0].lower():
                continue

        process = check_process(json_object["run"])
        for p in process:
            if subtree or kill:
                rg = re.compile("\s{2,}")
                replaced_command = rg.sub('||:||', p)
                replaced_command_array = replaced_command.split("||:||")
                # show subtree
                if subtree:
                    os.system('pstree -a -p ' + (replaced_command_array[1]))

                if kill and just_this is not None and len(just_this.split('_')) <= 1:  # if arg is -k but no PID number provided
                    os.system('kill ' + (replaced_command_array[1]))
                elif kill and just_this is not None and len(just_this.split('_')) >= 1 and replaced_command_array[1] == (just_this.split('_'))[1]:  # if arg is -k and PID is provided
                    os.system('kill ' + (replaced_command_array[1]))
                elif kill and just_this is None:  # if arg is --kill-all
                    os.system('kill ' + (replaced_command_array[1]))

            elif len(p) > 0:
                print
                print json_object["name"] + ':'
                print '-' * 18
                print p
                any_process = True

    if any_process:
        print '-' * 18
    elif not kill:
        print
        print "there isn't any process that is running atm!"

    print


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hli:pt:k:r:q:", ["help", "kill-all"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    show_all_command = False
    show_command = False
    show_process = False
    show_subtree = False
    kill_process = False
    kill_all = False
    run_process = False
    run_any_way = False
    passed_arg = ''


    for o, a in opts:
        if o in ("-h", "--help"):
            print_help()
            sys.exit()
        elif o in "-l":
            show_all_command = True
        elif o in "-i":
            show_command = True
            passed_arg = a
        elif o in "-p":
            show_process = True
        elif o in "-t":
            show_subtree = True
            passed_arg = a
        elif o in "-k":
            kill_process = True
            passed_arg = a
        elif o in "--kill-all":
            kill_all = True
            passed_arg = None
        elif o in "-r":
            run_process = True
            passed_arg = a
        elif o in "-q":
            run_any_way = True
            passed_arg = a
        else:
            sys.exit()

    command_file = os.getcwd() + '/commands.json'
    commands_file_content = read_command_file(command_file)
    batch_to_run = read_json(commands_file_content)

    # show_process_report(batch_to_run, 'pbsys_pbww', show_subtree)

    # show_command_list(batch_to_run)

    if show_all_command:
        show_command_list(batch_to_run)
    elif show_command:
        show_command_list(batch_to_run, passed_arg)
    elif show_process:
        show_process_report(batch_to_run, None, show_subtree)
    elif show_subtree:
        show_process_report(batch_to_run, passed_arg, show_subtree, kill_process)
    elif kill_all:
        show_process_report(batch_to_run, passed_arg, show_subtree, kill_all)
    elif kill_process:
        show_process_report(batch_to_run, passed_arg, show_subtree, kill_process)
    else:

        for json_object in batch_to_run["commands"]:

            if run_process or run_any_way:
                if json_object["name"] != passed_arg:
                    continue

            process = check_process(json_object["run"])
            if len(process) != 1 or run_any_way:
                # run new process
                if str2bool(json_object["enable"]) or run_any_way or run_process:
                    run_shell_command(json_object["run"])

    os._exit(-1)


if __name__ == '__main__':
    main(sys.argv[1:])








