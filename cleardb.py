from time import sleep

from database import clear_db

print("WARNING THIS WILL REMOVE ALL ENTRIES FROM THE DATABASE; ARE YOU SURE YOU WANT TO CONTINUE(y/n)")
if input() == "y":
    print("Clearing DB")
    clear_db()
    print("Database cleared. Please start your bot")
    sleep(5)
"""
This file is a quick way to reset the DB after an update
Its not really intended for anyone other then our QA tester in case his bot fails to start due to a DB issue
"""
#
