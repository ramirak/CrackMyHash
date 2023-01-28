import os, hashes, threading
import argparse

logo = """                                                                                  
 ,-----.                 ,--.   ,--.   ,--.       ,--.  ,--.            ,--.      
'  .--.,--.--.,--,--.,---|  |,-.|   `.'   ,--. ,--|  '--'  |,--,--.,---.|  ,---.  
|  |   |  .--' ,-.  | .--|     /|  |'.'|  |\\  '  /|  .--.  ' ,-.  (  .-'|  .-.  | 
'  '--'|  |  \\ '-'  \\ `--|  \\  \\|  |   |  | \\   ' |  |  |  \\ '-'  .-'  `|  | |  | 
 `-----`--'   `--`--'`---`--'`--`--'   `--.-'  /  `--'  `--'`--`--`----'`--' `--' 
                                          `---'                                   
"""

MIN_CHAR_RANGE=0
MAX_CHAR_RANGE=0
MIN_LEN=4
MAX_LEN=16
FOUND_NOTIF = threading.Event()
dict_mode = False

do_sha = None
hash_name = None
hash_to_find = None

parser = argparse.ArgumentParser(description="CrackMyHash - Multithreaded app that uses bruteforce or a dictionary file to find the value behind your hashed passwords.")
parser.add_argument("-m", "--mode", help = "FULL (slow) / REGULAR (default) / LIMITED (quick)", required = False, default = "REGULAR")
parser.add_argument("-u", "--use-hash", help = "sha1 / sha256", required = True, default = "")
parser.add_argument("-v", "--value", help = "ed1706c82c77b99e4276522967f7563fa7cd8f2d", required = True, default = "")
parser.add_argument("-d", "--dictionary", help = "dict/passowrds.txt", required = False, default = "")

argument = parser.parse_args()


def prepare():
    global do_sha, hash_name, hash_to_find, dict_mode, MIN_CHAR_RANGE, MAX_CHAR_RANGE
    hash_name = argument.use_hash
    hash_to_find = argument.value

    if argument.mode == "LIMITED":
        MIN_CHAR_RANGE = 97
        MAX_CHAR_RANGE = 122
    elif argument.mode == "REGULAR":
        MIN_CHAR_RANGE = 32
        MAX_CHAR_RANGE = 126
    elif argument.mode == "FULL":
        MIN_CHAR_RANGE = 0
        MAX_CHAR_RANGE = 255
    else:
        print("Mode not supported. Exiting.")
        exit(0)

    if hash_name == "sha1":
        do_sha = hashes.do_sha1
    elif hash_name == "sha256":
        do_sha = hashes.do_sha256
    else:
        print("Not supported hash function. Exiting.")
        exit(0)

    if os.path.isfile(argument.dictionary):
        dict_mode = True     
    else:
        print("Dictionary file not supplied, trying with brute-force..")


def try_match(current_str):
    global dict_mode
    if not dict_mode:
        current_str = ''.join(chr(x) for x in current_str)
    current_hash = do_sha(current_str)
    if current_hash == hash_to_find:
        print("Found a match: " + str(current_str))
        return True
    return False


def dictionary_mode(dict, my_task_id, task_size ,FOUND_NOTIF):
    dict_len = len(dict)
    for i in range(task_size):
        if FOUND_NOTIF.is_set():
            break
        if my_task_id + i >= dict_len:
            break
        if try_match(dict[my_task_id+i]):
            print("Notify threads..")
            FOUND_NOTIF.set()
            break


def bruteforce_mode(current_len, my_task_id, FOUND_NOTIF):
    my_str = [ MIN_CHAR_RANGE for i in range(current_len - 1)]
    my_str.append(my_task_id)

    while not FOUND_NOTIF.is_set():
        done = True
        for i in range(len(my_str) - 1):
            if my_str[i] >= MAX_CHAR_RANGE:
                my_str[i] = MIN_CHAR_RANGE
            else:
                my_str[i] += 1
                done = False
                break
        if try_match(my_str):
            print("Notify threads..")
            FOUND_NOTIF.set()
        if done:
            break
            

def init_dict(filename):
    lst = []
    with open(filename) as file:
        for line in file:
            lst.append(line.rstrip())
    return lst


def task_manager():
    print("Starting..")

    if dict_mode:
        dict = init_dict(argument.dictionary)
        task_size = int(len(dict) / 100)
        
        for task in range(100):
            t = threading.Thread(target=dictionary_mode, args=(dict, task, task_size, FOUND_NOTIF))
            t.start()
            break

        if(FOUND_NOTIF.is_set()):
            print("Exiting!")
            exit(0)
    else:
        task_index = MIN_CHAR_RANGE
        current_len = MIN_LEN
        threads = []

        while(current_len <= MAX_LEN):
            print("Trying with length " + str(current_len))
            while(task_index <= MAX_CHAR_RANGE):
                # Create all threads for current run
                threads.append(threading.Thread(target=bruteforce_mode, args=(current_len, task_index, FOUND_NOTIF), daemon=True))
                task_index += 1
                
            # start all threads 
            for t in threads:
                t.start()
            
            # wait for threads to finish and extend the string if no match was found
            for t in threads:
                t.join()

            threads.clear()
            task_index = MIN_CHAR_RANGE
            current_len += 1 

            if(FOUND_NOTIF.is_set()):
                print("Exiting!")
                exit(0)
                
            print("Not found")


print(logo)
prepare()
task_manager()    
    
