'''
import for date/time
import for csv
import os

make a csv dictionary with tuples. allows for 1 place for things to be changed within csv format

 -- function to read csv -- 

 -- function to write csv -- 

 -- function to update csv -- 

    --- general format for code ---
class hospital         (root class)

 class person            (parent class)
 --- lots of subclasses and inheritance of the same functions e.g. get_details. use a abstract base class. --- 

  class patient             (child class)

  class staff               (child / parent class)
--- use an abc like with person. due to the amount of subclasses that will use the same methods ---
    class doctor                (child class)
    class nurse                 (child class)
    class receptionist          (child class)

 class appointment          (base class)
 

 main function to use all classes and functions inside the classes
'''

from datetime import date
from abc import ABC, abstractmethod
import csv
import os
import re

CSV_FILES = {
    "patients": ("patients.csv", ["id","name","age","condition","medical_record"]),
    "staff": ("staff.csv", ["id","name","age","role","extra"]),
    "appointments": ("appointments.csv", ["patient_name","doctor_name","date","status"])
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
    filepath, headers = CSV_FILES[key]
    for row in rows:
        if row[match_field] == match_value:
            row[update_field] = new_value
        
    with open(filepath, "w", newline="") as f:
        w = csv.DictWriter(f,fieldnames = headers, extrasaction="ignore")
        w.writeheader()

        for row in rows:
            if all(k in headers for k in row.keys()):
                w.writerow(row)

class Person(ABC):
    
    id_counter = 1

    def __init__(self,name,age):
        self.id = Person.id_counter
        Person.id_counter += 1

        self.name = name
        self.age = age

    @abstractmethod
    def get_details(self):
        pass

    def __str__(self):
        return self.get_details()
    
class Patient(Person):

    def __init__(self,name,age,condition):
        super().__init__(name,age)
        self.condition = condition
        self._history = self.load_history()

    def load_history(self):
        for r in read_csv("patients"):
            if r["name"] == self.name:
                record = r["medical_record"]
                if record:
                    return record.split(" | ")
                else:
                    return []
        return[]
    
    def save(self):
        if not any(r["name"] == self.name for r in read_csv("patients")):
            write_csv("patients", {"id": self.id, "name": self.name, "age": self.age, "condition": self.condition, "medical_record": ""})

    
    def add_history(self,entry):
        dated = f"[{date.today()}] {entry}"
        self._history.append(dated)
        new_record = " | ".join(self._history)

        update_csv("patients", "name", self.name, "medical_record", new_record)

    def get_history(self):
        
        return "\n".join(f"  {e}" for e in self._history) if self._history else " no history "
    
    def get_details(self):
        return f"Patient [{self.id}] | {self.name} | Age: {self.age} | Condition: {self.condition}"

    @staticmethod
    def load_all():
        patients =[]
        for r in read_csv("patients"):
            p = Patient(r["name"], int(r["age"]), r["condition"])
            patients.append(p)
        return patients
    
class Staff(Person, ABC):

    def __init__(self,name,age):
        super().__init__(name, age)
        self.department = "unassigned"

    @abstractmethod
    def get_role(self):
        pass

    def save(self):
        if not any(r["name"] == self.name for r in read_csv("staff")):
            write_csv("staff", {"id": self.id, "name": self.name, "age": self.age, "role": self.get_role(), "extra": self.get_extra()})

    def extra():
        return ""
    
    def get_details(self):
        return f" {self.get_role()} [{self.id}]  | {self.name} | age: {self.age} | Department: {self.department} "

    @staticmethod
    def load_all():
        result = []

        for r in read_csv("staff"):
            name = r["name"]
            age = int(r["age"])
            role = r["role"]
            extra = r["extra"]

            if role == "doctor":
                result.append(Doctor(name,age,extra))
            elif role == "nurse":
                result.append(Nurse(name,age,extra))
            elif role == "receptionist":
                result.append(Receptionist(name,age))

        return result
    
class Doctor(Staff):

    def __init__(self,name,age,field):
        super().__init__(name,age)
        self.field = field
    
    def get_role(self):
        return "doctor"

    def get_extra(self):
        return self.field
    
    def see_patient(self,patient,notes):
        patient.add_history(f"seen by Dr. {self.name} ({self.field}): {notes}")
        print(f" [Dr. {self.name}] consulted {patient.name} - {notes}")

    def get_details(self):
        return (f"[{self.id} | Dr.{self.name} | Age: {self.age} | {self.field} | Department: {self.department}]")

class Nurse(Staff):

    def __init__(self,name,age,shift):
        super().__init__(name,age)
        self.shift = shift
    
    def get_role(self):
        return "nurse"

    def get_extra(self):
        return self.shift
    
    def care_for(self, patient):
        patient.add_history(f"care given by nurse {self.name} ({self.shift} shift )")
        print(f" [{self.name} Provided care to {patient.name}]")

class Receptionist(Staff):

    def __init__(self,name,age):
        super().__init__(name,age)
    
    def get_role(self):
        return "receptionist"

    def book_appointment(self, patient,doctor, appt_date):
        appt = Appointment(patient,doctor, appt_date)
        appt.save()
        print(f"[{self.name}] booked: {patient.name} with Dr. {doctor.name} on {appt_date}")
        return appt

class Appointment:
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
    

    @staticmethod
    def load_all(patients, staff):
        patient_2 = {p.name: p for p in patients}
        doctor_2 = {s.name: s for s in staff if isinstance(s, Doctor)}
        result = []

        for r in read_csv("appointments"):
            p = patient_2.get(r["patient_name"])
            d = doctor_2.get(r["doctor_name"])

            if p and d:
                appt = Appointment(p, d, r["date"])
                appt.status = r["status"]
                result.append(appt)
        return result
    
    def __str__(self):
        return f" {self.patient.name} | Dr. {self.doctor.name} | {self.appt_date} | {self.status}"


class Hospital:
    #add patients . add staff . add appointments . summary of hospital

    def __init__(self, name):
        self.name = name
        self.patients = []
        self.staff =[]
        self.appointments= []

    def register_patient(self,patient):

        self.patients.append(patient)
        patient.save()
        print(f"[{self.name}] Registered: {patient.name}")

    def hire_staff(self,member):

        self.staff.append(member)
        member.save()
        print(f"[{self.name}] Hired: {member.get_role()} {member.name}")

    def add_appointment(self, appt):
        self.appointments.append(appt)

    def get_summary(self):

        print(f" Patients: {len(self.patients)} | staff: {len(self.staff)} | appointments: {len(self.appointments)}")

#change to regex system instead of a function.


import sys

def load_hospital():
    hospital_name = input("enter your hospital name: ")
    hospital = Hospital(hospital_name)

    for p in Patient.load_all():
        hospital.patients.append(p)
    for m in Staff.load_all():
        hospital.staff.append(m)
    return hospital

if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("usage")
        print(" python hospital_system.py add_staff      - add a new staff member")
        print(" python hospital_system.py add_ patient   - register new patient")
        print(" python hospital_system.py book           - book and appointment")
        print(" python hospital_system.py consult        - record a consultation")
        print(" python hospital_system.py nurse_care     - record a nurse care")
        print(" python hospital_system.py list_staff     - list all staff")
        print(" python hospital_system.py list_ patients - list all patients and histories")
        print(" python hospital_system.py appointments   - list all appointments")
        print(" python hospital_system.py demo           - run a demo with example data")

    else:
        command = sys.argv[1]
        hospital = load_hospital()

        if command == "add_staff":
            print("staff roles: 1) doctor, 2) nurce, 3) receptionist")
            role_choice = input("choose role(1-3): ")

            while True:

                name = input(" enter name: ")
                if re.match(r"^[A-Za-z ]+$", name):
                    break
                print("invalid name. only use letters. ")

            age = input("enter their age: ")
            dept = input("enter their department: ")

            if role_choice == "1":
                field = input("enter their field: ")
                member = Doctor(name, age, field)
            
            elif role_choice == "2":
                shift = input("enter shift(day or night): ")
                member = Nurse(name, age, shift)
            
            elif role_choice == "3":
                member = Receptionist(name, age)
            
            else:
                print(" invalid choice ")
                sys.exit()
            member.department = dept
            hospital.hire_staff(member)

        elif command == "add_patient":
            while True:
                name = input("enter patient name: ")
                if re.match(r"^[A-Za-z ]+$", name):
                    break
                print("invalid name. only use letters.")

            age = int(input("enter patient age: "))
            condition = input(" enter condition ")
            patient = Patient(name, age, condition)

            hospital.register_patient(patient)


def main():

    ''' hire staff
        register patient
        book appointment
        medical record
        nurse care
        staff report
        patient history
        load appointments
        staff | role print
        hospital summary

        reload all csv files
    '''

    print("--Hospital managment--")
    
    hospital_name = input("enter hospital name: ")
    hospital = Hospital(hospital_name)

    for patient in Patient.load_all():
        hospital.patients.append(patient)

    for member in Staff.load_all():
        hospital.staff.append(member)

    while True:
        print("-- main menu --")
        print(" 1. Add staff member")
        print(" 2. register patient")
        print(" 3. Book appointment")
        print(" 4. record consult")
        print(" 5.record nurse care")
        print(" 6. view all staff")
        print(" 7. view all patients and histories")
        print(" 8. view all appointments")
        print(" 9. exit")

        choice = input("-- enter your choice: ")

        if choice == "1":
            print("staff roles: 1) doctor, 2) nurce, 3) receptionist")

            role_choice = input("choose role(1-3): ")

            name = input("enter their name: ")
            age = input("enter their age: ")
            dept = input("enter their department: ")

            if role_choice == "1":
                field = input("enter their field: ")
                member = Doctor(name, age, field)
            
            elif role_choice == "2":
                shift = input("enter shift(day or night): ")
                member = Nurse(name, age, shift)
            
            elif role_choice == "3":
                member = Receptionist(name, age)
            
            else:
                print(" invalid choice ")
                continue

            member.department = dept
            hospital.hire_staff(member)

        elif choice == "2":
            name = input("enter patient name: ")
            age = int(input("enter patient age: "))
            condition = input(" enter condition ")
            patient = Patient(name, age, condition)

            hospital.register_patient(patient)

        elif choice == "3":

            if not hospital.patients:
                print(" there are no patients. ")
                continue
            if not any(isinstance(s, Receptionist) for s in hospital.staff ):
                print("there are no receptionists ")
                continue
            if not any(isinstance(s, Doctor) for s in hospital.staff ):
                print("there are no doctors. ")
                continue

            print(" patients: ")
            for i, p in enumerate(hospital.patients):
                print(f"{i+1}. {p.name}")
            
            p_choice = int(input("select patient number: ")) - 1
            patient = hospital.patients[p_choice]

            doctors =[s for s in hospital.staff if isinstance(s,Doctor)]
            print("doctors: ")
            for i, d in enumerate(doctors):
                print(f" {i+1}. Dr. {d.name}")

            while True:
                try:
                    d_choice = int(input(" select doctor number: ")) - 1
                    if d_choice < 0 or d_choice >= len(doctors):
                        print("invalid please try again.")
                    else:
                        break
                except ValueError:
                    print(" please enter a number")
            doctor = doctors[d_choice]

            receptionist = [s for s in hospital.staff if isinstance(s, Receptionist)]
            receptionist = receptionist[0]

            appt_date = input("enter appointment date ( e.g 2026-04-30)")
            appt = receptionist.book_appointment(patient, doctor, appt_date)
            appt.confirm()
            hospital.add_appointment(appt)

        elif choice == "4":

            if not hospital.patients:
                print(" there are no patients. ")
                continue
            if not any(isinstance(s,Doctor) for s in hospital.staff):
                print(" no doctors on staff yet. ")
                continue
            print(" Patients: ")
            
            for i, p in enumerate(hospital.patients):
                print(f"{i+1}. {p.name}")
            
            p_choice = int(input("select patient number: ")) - 1
            patient = hospital.patients[p_choice]

            doctors =[s for s in hospital.staff if isinstance(s,Doctor)]
            print("doctors: ")
            for i, d in enumerate(doctors):
                print(f" {i+1}. Dr. {d.name}")

            d_choice = int(input(" select doctor number: ")) - 1
            doctor = doctors[d_choice]

            notes = input(" enter consultation notes: ")
            doctor.see_patient(patient, notes)

        elif choice == "5":
            if not hospital.patients:
                print(" there are no patients. ")
                continue

            if not any(isinstance(s, Nurse) for s in hospital.staff):
                print("there are no nurses on staff. ")
                continue

            for i, p in enumerate(hospital.patients):
                print(f"{i+1}. {p.name}")
            
            p_choice = int(input("select patient number: ")) - 1
            patient = hospital.patients[p_choice]

            nurses =[s for s in hospital.staff if isinstance(s, Nurse)]
            print(" nurses: ")

            for i, n in enumerate(nurses):
                print(f" {i+1}. {n.name}")
            while True:
                try:
                    n_choice = int(input("select nurse number: ")) - 1
                    if n_choice < 0 or n_choice >= len(nurses):
                        print("invalid. please try again.")
                    else:
                        break
                except ValueError:
                    print("please enter a number")
            nurse = nurses[n_choice]

            nurse.care_for(patient)

        elif choice == "6":
            if not hospital.staff:
                print("no staff registered. ")
                continue
            else:
                print(" staff: ")
                for member in hospital.staff:
                    print(f" {member.get_details()}")

        elif choice == "7":
            if not hospital.patients:
                print(" no patients registered. ")
                continue
            else:
                print(" patients: ")
                for patient in hospital.patients:
                    print(f" {patient.get_details()} | {patient.get_history()}")
                

        elif choice == "8":
            if not hospital.appointments:
                print(" no appointments booked. ")
            else:
                print(" appointments ")
                for a in hospital.appointments:
                    print(a)

        elif choice == "9":
            break

        else:
            print(" invalid selection please enter between 1 and 9. ")

if __name__ =="__main__":
    main()