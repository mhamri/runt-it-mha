import json
import os
import subprocess
import shlex


__author__ = 'Mohammad Hossein Amri - mhamri@gmail.com'

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
    process_path= process_path.replace('"', '')
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


def main():
    command_file = os.getcwd() + '/commands.json'
    commands_file_content = read_command_file(command_file)
    batch_to_run = read_json(commands_file_content)

    for json_object in batch_to_run["commands"]:
        process = check_process(json_object["run"])
        if len(process) != 1:
            # kill process
            # run new process
            subprocess.Popen(shlex.split(json_object["run"]))

    os._exit(-1)

if __name__ == '__main__':
    main()








