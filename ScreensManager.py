#!/usr/bin/env python3
import os
import traceback
import getpass
from subprocess import Popen, PIPE, CalledProcessError
import datetime
import sys
import random



LINUX_USER = getpass.getuser()
HOME_DIRECTORY = os.environ["HOME"]
LOG_FILE_LOCATION = os.path.join(HOME_DIRECTORY,".MY_SCREEN.log")
CMD_TO_RUN_FILE_LOCATION = os.path.join(HOME_DIRECTORY,".CMD_TO_RUN.sud")
SCREEN = "screen"
TMUX = "tmux"
LIST_SCREENS_CMD = {
    SCREEN: "screen -ls",
    TMUX: "tmux ls"
}
POSSIBLE_SCREEN_NAMES = [    "Sirius",    "Canopus",    "AlphaCentauri",    "Arcturus",    "Vega",    "Capella",    "Rigel",    "ProximaCentauri",    "Betelgeuse",    "Achernar",    "Hadar",    "Altair",    "Aldebaran",    "Antares",    "Spica",    "Pollux",    "Regulus",    "Deneb",    "Betazed",    "Auriga",    "Acrux",    "Gacrux",    "Alphecca",    "Altarf",    "Gienah",    "Alchiba",    "Alcor",    "Alcyone",    "Alderamin",    "Algenib",    "Algol",    "Alhena",    "Alioth",    "Alkaid",    "Almaak",    "Alnair",    "Alnilam",    "Alnitak",    "AlphaCrucis",    "Alphard",    "Alpheratz",    "Alrescha",    "Altarf",    "Alterf",    "Aludra",    "Alya",    "Amaterasu",    "Ankaa",    "Arcas"]
all_screens = {
    SCREEN: [],
    TMUX: []
}


# Log Errors
def _datetime_print_error(log, show_log = True):
    log = f"{datetime.datetime.now().strftime('%d %B %Y-%H:%M:%S')} |ERROR| {log}"
    if show_log:
        print(log)
    with open(LOG_FILE_LOCATION,"a") as f:
        f.write(log)
        f.write("\n")



# Log Info
def _datetime_print_info(log, show_log = False):
    log = f"{datetime.datetime.now().strftime('%d %B %Y-%H:%M:%S')} |Info| {log}"
    if show_log:
        print(log)
    with open(LOG_FILE_LOCATION,"a") as f:
        f.write(log)
        f.write("\n")



def _write_cmd_to_file(cmd):
    with open(CMD_TO_RUN_FILE_LOCATION, "w") as fl:
        fl.write(cmd)



def _execute_command_locally(command, write_output_to_screen = True):
    result = [False, [], [], None]
    try:
        _datetime_print_info(f"Executing `{command}` locally", write_output_to_screen)
        cmd_process = ""
        with Popen(command, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True, shell=True) as cmd_process:
            for line in cmd_process.stdout:
                _datetime_print_info(line.strip(), write_output_to_screen)
                result[1].append(line.strip())
            result[2].extend(cmd_process.stderr.readlines())
            [_datetime_print_error(line.strip(), write_output_to_screen) for line in result[2]]
        result[3] = cmd_process.returncode
        result[0] = True
        return result
    except:
        _datetime_print_error(f"Exception occured while executing '{command}` locally. Please contact sudesh1611@gmail.com with following error:", write_output_to_screen)
        _datetime_print_error(traceback.format_exc(), write_output_to_screen)
        return result



def _get_random_screen_name():
    global all_screens
    global POSSIBLE_SCREEN_NAMES
    try:
        temp = [screen for screen in POSSIBLE_SCREEN_NAMES if screen not in all_screens[SCREEN] and screen not in all_screens[TMUX]]
        return random.choice(temp)
    except:
        _datetime_print_error(f"Exception occured while getting random screen name. Please contact sudesh1611@gmail.com with following error:")
        _datetime_print_error(traceback.format_exc())
        sys.exit(-1)



def get_screens():
    global all_screens
    try:
        for line in _execute_command_locally(LIST_SCREENS_CMD[SCREEN], False)[1]:
            if "." in line and "(" in line:
                all_screens[SCREEN].append(line.strip().split(".")[1].strip().split("\t")[0].strip())
        for line in _execute_command_locally(LIST_SCREENS_CMD[TMUX], False)[1]:
            if ":" in line and "(" in line:
                all_screens[TMUX].append(line.strip().split(":")[0].strip())
    except:
        _datetime_print_error(f"Exception occured while getting screens. Please contact sudesh1611@gmail.com with following error:")
        _datetime_print_error(traceback.format_exc())
        sys.exit(-1)


def _get_user_input_for_screen():
    global all_screens
    try:
        while True:
            screen_name = input("\nEnter screen name: ")
            screen_name = screen_name.strip()
            if screen_name.lower() in [screen.lower() for screen in all_screens[SCREEN]]+[screen.lower() for screen in all_screens[TMUX]]:
                print("Error: Screen name already exists. Choose different name.")
                continue
            if len(screen_name) < 1:
                print("Error: Screen name can not be empty. Choose different name.")
                continue
            if " " in screen_name:
                print("Error: Screen name can not have blank spaces. Choose different name.")
                continue
            return screen_name
    except:
        _datetime_print_error(f"Exception occured while getting screen name from user. Please contact sudesh1611@gmail.com with following error:")
        _datetime_print_error(traceback.format_exc())
        sys.exit(-1)



def present_screens():
    global all_screens
    try:
        option = -1
        screens_length = len(all_screens[SCREEN]) 
        tmux_length = len(all_screens[TMUX])
        total_screens = screens_length + tmux_length
        while option < 1 or option > total_screens+4:
            print("\nYou have following options for screens:")
            index = 1
            for screen in all_screens[SCREEN]:
                print(f"{index} - {screen} (Screens)")
                index = index +1
            for screen in all_screens[TMUX]:
                print(f"{index} - {screen} (Tmux)")
                index = index +1
            print(f"{index} - Create New Random Screens Terminal")
            index = index +1
            print(f"{index} - Create New Random Tmux Terminal")
            index = index +1
            print(f"{index} - Create New Named Screen Terminal")
            index = index +1
            print(f"{index} - Create New Named Tmux Terminal")
            index = index +1
            print("0 - Exit")
            print
            try:
                option = int(input("\nEnter your choice: ").strip())
                if(option > 0 and option <= screens_length):
                    _write_cmd_to_file(f"screen -rd {all_screens[SCREEN][option-1]}")
                    return True
                if(option > screens_length and option <= screens_length+tmux_length):
                    _write_cmd_to_file(f"tmux attach -d -t {all_screens[TMUX][(option-screens_length)-1]}")
                    return True
                if(option == total_screens+1):
                    _write_cmd_to_file(f"screen -S {_get_random_screen_name()}")
                    return True
                if(option == total_screens+2):
                    _write_cmd_to_file(f"tmux new -s {_get_random_screen_name()}")
                    return True
                if(option == total_screens+3):
                    _write_cmd_to_file(f"screen -S {_get_user_input_for_screen()}")
                    return True
                if(option == total_screens+4):
                    _write_cmd_to_file(f"tmux new -s {_get_user_input_for_screen()}")
                    return True
                if(option == 0):
                    return True
            except Exception as ex:
                option = -1
    except:
        _datetime_print_error(f"Exception occured while presenting screens. Please contact sudesh1611@gmail.com with following error:")
        _datetime_print_error(traceback.format_exc())
        return False

_write_cmd_to_file("echo 'Hey! Have a great day'")
get_screens()
present_screens()
