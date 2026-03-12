'''
import for date/time
import for csv
import os

make a csv dictionary with tuples. allows for 1 place for things to be changed within csv format

function to read csv -- done
function to write csv -- done
function to update csv -- done

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

def write_csv(key,row):
    read_csv(key) # validates file exists
    filepath, headers = CSV_FILES[key]

    with open(filepath, "a", newline="") as f:
        csv.DictWriter(f, fieldnames = headers).writerow(row)

def update_csv(key, match_field, match_value, update_field, new_value):
    #update the field in all rows where the field matches the value given.
    rows = read_csv(key)

    for row in rows:
        if row[match_field] == match_value:
            row[update_field] = new_value
        
    filepath, headers = CSV_FILES[key]
    with open(filepath, "w", newline="") as f:
        w = csv.DictWriter(f,fieldnames = headers)
        w.writeheader()
        w.writerows(row)

