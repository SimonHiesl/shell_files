from datetime import datetime
import sys

def give_weekday(day, month, year):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    date = datetime(year, month, day)
    print("The", str(day)+"."+str(month)+"."+str(year), "is a", str(weekdays[date.weekday()])+".")

def help():
    print("""Arguments must be passed in the order as shown:    [day] [month] [year]
             - [day] in int (no default).
             - [month] in int (no default).
             - [year] in int (no default).""")

if(len(sys.argv) == 4 and sys.argv[1].isdigit() and sys.argv[2].isdigit() and sys.argv[3].isdigit()):
    give_weekday(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
else:
    help()
