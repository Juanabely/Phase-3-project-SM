# main.py
from sqlalchemy.orm import sessionmaker
from models import Student, Teacher, Course, Enrollment, Base, engine

# Create database tables if they don't exist
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Function to register a new student
def register_student():
    print("Student Registration")
    name = input("Enter student's name: ")
    adm = input("Enter admission number: ")
    # Create a new student instance and add it to the session
    student = Student(student_name=name, student_adm=adm, student_fee_balance=15000)
    session.add(student)
    session.commit()
    paying_fee=input('Is student paying fee now? (y/n)')
    if paying_fee == 'y':
        student.student_fee_balance = 0
    else:
        student.student_fee_balance = 15000    
    print(f"Registered student: {name}, Admission Number: {adm} and student's fee is {student.student_fee_balance} ")

# Function to add academic marks for a student (Teacher)
def add_academics():
    print("Add Academics")
    teacher_id=int(input('enter teacher id '))
    teacher = session.query(Teacher).filter_by(teacher_id=teacher_id).first()
    if not teacher:
        print('Not a registered teacher🚩')
    else:    
      student_id = int(input("Enter student ID: "))
      student = session.query(Student).filter_by(student_id=student_id).first()
    
      if not student:
        print("Student not registered yet,please follow the registration prompts.")
        return

      marks = int(input("Enter academic marks: "))
      # Update the student's academic marks and commit the changes
      student.student_academics = marks
      session.commit()
      print(f"Academic marks added for {student.student_name}: {marks}")

# Function to view a student's fee balance (Parent)
def view_fee_balance():
    print("View Fee Balance")
    student_id = int(input("Enter student ID: "))
    student = session.query(Student).filter_by(student_id=student_id).first()
    
    if not student:
        print("Student not registered yet,please follow the registration prompts")
        return

    fee_balance = student.student_fee_balance
    print(f"Fee balance for {student.student_name}: {fee_balance}")
    

# Function to view all students with their marks (Teacher)
def view_students_with_marks():
    print("View Students with Marks")
    teacher_id=int(input('enter teacher id '))
    teacher = session.query(Teacher).filter_by(teacher_id=teacher_id).first()
    if not teacher:
        print('Not a registered teacher🚩')
    else:    
     students = session.query(Student).all()

     if not students:
        print("No students found.")
        return

     print("\nStudents with Marks:")
     for student in students:
        print(f"Student Name: {student.student_name}, Marks: {student.student_academics}")

# Function to enroll a student in a course
def enroll_student():
    print("Enroll Student in Course")
    student_id = int(input("Enter student ID: "))
    course_name = str(input("Enter course name: "))
    
    student = session.query(Student).filter_by(student_id=student_id).first()
    course = session.query(Course).filter_by(course_name=course_name).first()
    studentadded =Course(enrolled_student=student.student_name) 
    if not student:
        print("Student not found.")
        return
    
    if not course:
        print("Course not found.")
        return
    
    # Add the student to the course and commit the changes
    session.add(studentadded)
    session.commit()
    print(f"Enrolled {student.student_name} in {course.course_name}.")

# Function to register a new teacher
def register_teacher():
    print("Teacher Registration")
    name = input("Enter teacher's name: ")
    # Create a new teacher instance and add it to the session
    teacher = Teacher(teacher_name=name)
    session.add(teacher)
    session.commit()
    print(f"Registered teacher: {name}")

def deregister_teacher():
    print('Teacher removal')
    teacher_name = input("Enter teacher's name: ")
    teacher = session.query(Teacher).filter(teacher_name == teacher_name).first()  # replace with your filter
# delete the object
    session.delete(teacher)

    # commit the transaction
    session.commit()  
    print(f"Teacher: {teacher_name} has been removed from your database! ") 

def view_all_students():
    print('Students available as per 26/3/2024')
    students = session.query(Student).all()
    for student in students:
      print(f"Student in the database as per 26/3/2024 is {student.student_id}: {student.student_name}")   

# Main function to display the menu and handle user choices
def main():
    while True:
        date='3/26/2024'
        print("\n<=> Super Manager by Abel'stech.co 🧑‍💻 <=>\n")
        print("1. Register Student👥\n")
        print("2. Register Teacher👔\n")
        print("3. Enroll Student in Course📝\n")
        print("4. Add student marks (Teacher)📈\n")
        print("5. View Fee Balance (Parent)💸\n")
        print("6. View Students with Marks (Teacher)📄\n")
        print("7. Remove teacher --xx \n")
        print(f'8. View students in database as per {date}....\n')
        print("9. Exit🚨\n")
        choice = input("Enter your choice✏️: ")

        if choice == '1':
            register_student()
        elif choice == '2':
            register_teacher()
        elif choice == '3':
            enroll_student()
        elif choice == '4':
            add_academics()
        elif choice == '5':
            view_fee_balance()
        elif choice == '6':
            view_students_with_marks()
        elif choice == '7':
            deregister_teacher() 
        elif choice == '8':
            view_all_students()       
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
