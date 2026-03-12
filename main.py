'''
import for date/time
import for csv
import os

make a csv dictionary with tuples. allows for 1 place for things to be changed within csv format

function to read csv
function to write csv
function to update csv

class hospital

 class person

  class patient
  class staff
  class doctor
  class nurse
  class receptionist

 class appointment
 class
 
'''

from datetime import date
import csv
import os

CSV_FILES = {
    "patients", ("patients.csv", ["id","name","age","condition","medical_record"]),
    "staff", ("staff.csv", ["id","name","age","role","extra"]),
    "appointments", ("appointments.csv", ["patient_name","doctor_name","date","status"])
}

def read_csv(key):
    filepath, headers = CSV_FILES[key]
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="") as f:
            csv.writer(f).writerow(headers)
    
    with open(filepath, "r", newline = "") as f:
        return list(csv.DictReader(f))
