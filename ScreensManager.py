#!/usr/bin/env python3
import os
import traceback
import getpass
from subprocess import Popen, PIPE, CalledProcessError
import datetime
import sys
import random



LINUX_USER = getpass.getuser()
HOME_DIRECTORY = "/home/cyc"
if LINUX_USER == "root":
    HOME_DIRECTORY = "/root"
LOG_FILE_LOCATION = os.path.join(HOME_DIRECTORY,".MY_SCREEN.log")
CMD_TO_RUN_FILE_LOCATION = os.path.join(HOME_DIRECTORY,".CMD_TO_RUN.sud")
CMD_GET_ALL_SCREENS = "screen -ls"
all_screens = []
POSSIBLE_SCREEN_NAMES = [    "Sirius",    "Canopus",    "AlphaCentauri",    "Arcturus",    "Vega",    "Capella",    "Rigel",    "ProximaCentauri",    "Betelgeuse",    "Achernar",    "Hadar",    "Altair",    "Aldebaran",    "Antares",    "Spica",    "Pollux",    "Regulus",    "Deneb",    "Betazed",    "Auriga",    "Acrux",    "Gacrux",    "Alphecca",    "Altarf",    "Gienah",    "Alchiba",    "Alcor",    "Alcyone",    "Alderamin",    "Algenib",    "Algol",    "Alhena",    "Alioth",    "Alkaid",    "Almaak",    "Alnair",    "Alnilam",    "Alnitak",    "AlphaCrucis",    "Alphard",    "Alpheratz",    "Alrescha",    "Altarf",    "Alterf",    "Aludra",    "Alya",    "Amaterasu",    "Ankaa",    "Arcas"]



# Log Errors
def _datetime_print_error(log):
    log = f"{datetime.datetime.now().strftime('%d %B %Y-%H:%M:%S')} |ERROR| {log}"
    print(log)
    with open(LOG_FILE_LOCATION,"a") as f:
        f.write(log)
        f.write("\n")



# Log Info
def _datetime_print_info(log):
    log = f"{datetime.datetime.now().strftime('%d %B %Y-%H:%M:%S')} |Info| {log}"
    #print(log)
    with open(LOG_FILE_LOCATION,"a") as f:
        f.write(log)
        f.write("\n")



def _write_cmd_to_file(cmd):
    with open(CMD_TO_RUN_FILE_LOCATION, "w") as fl:
        fl.write(cmd)



def _execute_command_locally(command):
    result = [False, [], [], None]
    try:
        _datetime_print_info(f"Executing `{command}` locally")
        cmd_process = ""
        with Popen(command, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True, shell=True) as cmd_process:
            for line in cmd_process.stdout:
                _datetime_print_info(line.strip())
                result[1].append(line.strip())
            result[2].extend(cmd_process.stderr.readlines())
            [_datetime_print_error(line.strip()) for line in result[2]]
        result[3] = cmd_process.returncode
        result[0] = True
        return result
    except:
        _datetime_print_error(f"Exception occured while executing '{command}` locally. Please contact sudesh_kumar1@dell.com with following error:")
        _datetime_print_error(traceback.format_exc())
        return result



def _get_random_screen_name():
    global all_screens
    global POSSIBLE_SCREEN_NAMES
    try:
        temp = [screen for screen in POSSIBLE_SCREEN_NAMES if screen not in all_screens]
        return random.choice(temp)
    except:
        _datetime_print_error(f"Exception occured while getting random screen name. Please contact sudesh_kumar1@dell.com with following error:")
        _datetime_print_error(traceback.format_exc())
        sys.exit(-1)



def get_screens():
    global all_screens
    all_screens = []
    try:
        result = _execute_command_locally(CMD_GET_ALL_SCREENS)
        for line in result[1]:
            if "." in line and "(" in line:
                all_screens.append(line.strip().split(".")[1].strip().split("\t")[0].strip())
    except:
        _datetime_print_error(f"Exception occured while getting screens. Please contact sudesh_kumar1@dell.com with following error:")
        _datetime_print_error(traceback.format_exc())
        sys.exit(-1)


def _get_user_input_for_screen():
    global all_screens
    try:
        while True:
            screen_name = input("\nEnter screen name: ")
            screen_name = screen_name.strip()
            if screen_name.lower() in [screen.lower() for screen in all_screens]:
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
        _datetime_print_error(f"Exception occured while getting screen name from user. Please contact sudesh_kumar1@dell.com with following error:")
        _datetime_print_error(traceback.format_exc())
        sys.exit(-1)



def present_screens():
    global all_screens
    try:
        option = -1
        total_screens = len(all_screens)
        while option < 1 or option > total_screens+2:
            print("\nYou have following options for screens:")
            index = 1
            for screen in all_screens:
                print(f"{index} - {screen}")
                index = index +1
            print(f"{index} - Create New Random Screen")
            index = index +1
            print(f"{index} - Create New Named Screen")
            index = index +1
            print("0 - Exit")
            print
            try:
                option = int(input("\nEnter your choice: ").strip())
                if(option > 0 and option <= total_screens):
                    _write_cmd_to_file(f"screen -rd {all_screens[option-1]}")
                    return True
                if(option == total_screens+1):
                    _write_cmd_to_file(f"screen -S {_get_random_screen_name()}")
                    return True
                if(option == total_screens+2):
                    _write_cmd_to_file(f"screen -S {_get_user_input_for_screen()}")
                    return True
                if(option == 0):
                    return True
            except Exception as ex:
                option = -1
    except:
        _datetime_print_error(f"Exception occured while presenting screens. Please contact sudesh_kumar1@dell.com with following error:")
        _datetime_print_error(traceback.format_exc())
        return False

_write_cmd_to_file("echo 'Hey! Have a great day'")
get_screens()
present_screens()
