#add or remove students. add teacher and classes. find information on students

def opions():
    print("--options--")
    print("1 - add student - ")
    print("2 - remove student -")
    print("3 - view student -")
    option = input("select a menu option 1 - 3 : ")
    if option == "1":
        add_student()
    elif option == "2":
        remove_student()
    elif option == "3":
        view_student()
    else:
        print("That is not a valid input.")

def add_student():
    new_name_1 = input("Enter a students first name: ")
    new_name_2 = input("Enter a students last name: ")
    new_id = input("enter a valid new student ID: ")
    #add all new information to csv file
def remove_student():
    
    


def view_student():



