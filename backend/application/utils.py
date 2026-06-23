from datetime import datetime
from zoneinfo import ZoneInfo
import json
IST = ZoneInfo("Asia/Kolkata")

def ist_now():
   return datetime.now(IST)

# I have creaed this file to store utility functions that can be used across the application. 