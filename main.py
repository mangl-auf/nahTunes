#!/usr/bin/python3

#import eyed3

import sqlite3
import string
import random
import sys
import os
import shutil

def generate_location_name():
    return "".join(random.choices(string.ascii_uppercase, k=4))

def generate_item_pid():
    return random.randint(-(2 ** 63), 2 ** 63)

# TODO: add support of different file types (now works only with m4a and mp3)
def main():
    if len(sys.argv) < 2:
        print("No song or album provided!")
        return -1
    elif not os.path.exists(sys.argv[1]):
        print(f"No such file: {sys.argv[1]}!")
        return -1

    db_connection = sqlite3.connect("/mnt/iPod_Control/iTunes/iTunes Library.itlp/Locations.itdb")
    db = db_connection.cursor()
    res = db.execute("SELECT item_pid, location FROM location")
    
    item_pid = generate_item_pid()
    location_name = generate_location_name()
    extension = 0

    file_extension = sys.argv[1].split(".")[-1]
    if "mp3" == file_extension:
        extension = 1297101600
    elif "m4a" == file_extension:
        extension = 1295270176
    else:
        print("Unknown file extension!")
    
    for row in res.fetchall():
        if item_pid == row[0]:
            item_pid = generate_item_pid()
        elif "F99/" in row[1] and location_name in row[1]:
            location_name = generate_location_name()
            
    shutil.copy2(sys.argv[1], f"/mnt/iPod_Control/Music/F99/{location_name}.{file_extension}")
    db.execute(f"INSERT INTO location VALUES ({item_pid}, 0, 1, 1179208773, 'F99/{location_name}.{file_extension}', {extension}, 1, 690432076, {os.path.getsize(sys.argv[1])}, NULL, NULL, NULL, NULL)")
    db_connection.commit()
    db_connection.close()
    print("Done")

    # db_connection = sqlite3.connect("/mnt/iPod_Control/iTunes/iTunes Library.itlp/Library.itdb")
    
if __name__ == "__main__":
    main()
