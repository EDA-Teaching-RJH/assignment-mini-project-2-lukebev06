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
 --- lots of subclasses and inheritance of the same functions e.g. get_details. use a abstract base class. --- 

  class patient

  class staff
--- use an abc like with person. due to the amount of subclasses that will use the same methods ---
    class doctor
    class nurse
    class receptionist

 class appointment
 class
 
'''

from datetime import date
from abc import ABC, abstractmethod
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

class person(ABC):
    
    id_counter = 1

    def __init__(self,name,age):
        self.id = person.id_counter
        person.id_counter += 1

        self.name = name
        self.age = age
    
    def get_details(self):
        pass

    def __str__(self):
        return self.get_details()
    
class patient(person):

    def __init__(self,name,age,condition):
        super().__init__(name,age)
        self.condition = condition
        self.history = self.load_history()

    def load_history(self):
        for r in read_csv("patients"):
            if r["name"] == self.name:
                return r["medical_record"]
        return[]
    
    def save(self):
        if not any(r["name"] == self.name for r in read_csv("patients")):
            write_csv("patients", {"id": self.id, "name": self.name, "age": self.age, "condition": self.condition, "medical_record": ""})

    
    def add_history(self,entry):
        dated = f"[{date.todat()}] {entry}"
        self.history.append(dated)
        new_record = self.history

        update_csv("patients", "name", self.name, "medical_record", new_record)

    def get_history(self):
        if len(self.history) == 0:
            return " no history "
        for entry in self.history:
            result = result + " " + entry + "\n"
        return result
    
    def get_details(self):
        return f"Patient [{self.id}] | {self.name} | Age: {self.age} | Condition: {self.condition}"

    def load_all():
        for r in read_csv("patients"):
            p = patient(r["name"], int(r["age"]), r["condiion"])
            patient.append(p)
        return patient
    
class staff(person, ABC):

    def __init__(self,name,age):
        super().__init__(name, age)
        self.department = "unassigned"

    def get_role(self):
        pass

    def save(self):
        if not any(r["name"] == self.name for r in read_csv("staff")):
            write_csv("staff", {"id": self.id, "name": self.name, "age": self.age, "role": self.get_role(), "extra": self.get_extra()})

    def extra():
        return ""
    
    def get_details(self):
        return f" {self.get_role()} [{self.id}]  | {self.name} | age: {self.age} | Department: {self.department} "

    def load_all():
        result = []

        for r in read_csv("staff"):
            name = r["name"]
            age = int(r["age"])
            role = r["role"]
            extra = r["extra"]

            if role == "doctor":
                result.append(doctor(name,age,extra))
            elif role == "nurse":
                result.append(nurse(name,age,extra))
            elif role == "receptionist":
                result.append(receptionist(name,age,extra))

        return result
    
class doctor(staff):

    def __init__(self,name,age,field):
        super().__init__(name,age)
        self.field = field
    
    def get_role(self):
        return "doctor"

    def extra(self):
        return self.field
    
    def see_patient(self,patient,notes):
        patient.add_history(f"seen by Dr. {self.name} ({self.field}): {notes}")
        print(f" [Dr. {self.name}] consulted {patient.name} - {notes}")

    def get_details(self):
        return (f"[{self.id} | Dr.{self.name} | Age: {self.age} | {self.field} | Department: {self.department}]")

class nurse(staff):

    def __init__(self,name,age,shift):
        super().__init__(name,age)
        self.shift = shift
    
    def get_role(self):
        return "nurse"

    def extra(self):
        return self.shift
    
    def care_for(self, patient):
        patient.add_history(f"care given by nurse {self.name} ({self.shift} shift )")
        print(f" [{self.name} Provided care to {patient.name}]")

class receptionist(staff):

    def __init__(self,name,age):
        super().__init__(name,age)
    
    def get_role(self):
        return "receptionist"

    def book_appointment(self, patient,doctor, appt_date):
        appt = appointment(patient,doctor, appt_date)
        appt.save()
        print(f"[{self.name}] booked: {patient.name} with Dr. {doctor.name} on {appt_date}")
        return appt

class appointment:
    def __init__(self,patient,doctor,appt_date):
        self.patient = patient
        self.doctor = doctor
        self.appt_date = appt_date
        self.status = "scheduled"

    def save(self):

        existing = read_csv("appointments")

        if not any(r["patient_name"] == self.patient.name and r["date"] == self.appt_date for r in existing):
            write_csv("appointments", {"patient_name": self.patient.name, "doctor_name": self.doctor.name, "date": self.appt_date, "status": self.status})

    def confirm(self):
        self.status = "confirmed"
        update_csv("appointments", "patient_name", self.patient.name, "status", "confirmed")
        
        print(f" confirmed {self.patient.name} with Dr. {self.doctor.name}")
        
    def cancel(self):
        self.status = "cancelled"
        update_csv("appointments", "patient_name", self.patient.name, "status", "cancelled")

        print(f" cancelled: {self.patient.name} with Dr. {self.doctor.name}")
    
    def load_all(patients, staff):
        patient_2 = {patient.name: p for p in patients}
        doctor_2 = {staff.name: s for s in staff if isinstance(s, doctor)}
        result = []

        for r in read_csv("appointments"):
            p = patient_2.get(r["patient_name"])
            d = doctor_2.get(r["doctor_name"])

            if p and d:
                appt = appointment(p, d, r["date"])
                appt.status = r["status"]
                result.append(appt)
        return result
    
    def __str__(self):
        return f" "