"""
This script will watch a folder for changes and do the following : 

a) Rename the file according to the "Course Name" column in the csv or excel.
b) If the file exists it will auto delete it and prompt a message telling the user the file existed.
c) save about 15 minutes per week when doing this.

will need to re-factor code to make it more "dry" lots of redundancy here.

"""

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import os
from shutil import copyfile
my_path = r"C:\Users\umarh\OneDrive\Documents\watchdog test"
from datetime import datetime, timedelta

# create a date variable for the filename 
file_date = datetime.today().strftime('%d%m%Y')

os.chdir(my_path)

print("Hi, this program will autorename the Training Credits files we receive on a weekly basis")
print(f"The current location is set to {my_path}")
print("To close the program hit CTRL-C on your keyboard whilst on the command terminal.\n")



class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_modified = datetime.now()
    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        elif event.src_path.split('.')[-1] == 'xlsx':
            df = pd.read_excel(event.src_path) # read the file
            course = df['Course Name'].unique().tolist()[0] # pass course name to a variable
            try:
                self.last_modified = datetime.now()
                print(f'Event type: {event.event_type}  path : {event.src_path}')
                print(course)
                os.rename(event.src_path, f"{course+file_date}.xlsx") # rename file
                print(f"file renamed to {course+file_date}.xlsx")
            except (FileExistsError,FileNotFoundError):
                print(f"This course file : {course+file_date} already exists.")
                os.remove(event.src_path)
                print("Duplicate file removed.")
        else:
            df = pd.read_csv(event.src_path) # read the file
            course = df['Course Name'].unique().tolist()[0] # pass course name to a variable
            try:
                self.last_modified = datetime.now()
                print(f'Event type: {event.event_type}  path : {event.src_path}')
                print(course)
                os.rename(event.src_path, f"{course+file_date}.csv") # rename file
                print(f"file renamed to {course+file_date}.csv")
            except (FileExistsError,FileNotFoundError):
                print(f"This course file : {course+file_date} already exists.")
                os.remove(event.src_path)
                print("Duplicate file removed.")
                
    def on_deleted(self,event):
        file= event.src_path.split('\\')[-1]
        print(f"what the f**k! Someone deleted {file}!")

    
                

# starts the program.

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=my_path, recursive=False)
    observer.start()

# Runs until user presses CTRL-C to stop program.

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join() 
 


