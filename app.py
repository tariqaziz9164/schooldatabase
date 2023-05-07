import streamlit as st
import sqlite3
import pandas as pd



def create_student_table():
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            class_ TEXT,
            section TEXT,
            gender TEXT,
            grade TEXT,
            teacher_name TEXT,
            address TEXT,
            contact INTEGER,
            fee INTEGER,
            driver_contact INTEGER,
            transport_fee REAL,
            uniform_dues REAL,
            books_dues REAL,
            admission_fee REAL,
            paper_money REAL,
            fee_status TEXT
        )
    """)
    conn.commit()
    conn.close()
    
# Create staff table
def create_teacher_table():
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS teacher (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT,
            teacher_scale TEXT,
            teacher_contact TEXT,
            teacher_salary TEXT,
            teacher_transport TEXT,
            teacher_education TEXT,
            teacher_subject TEXT,
            teacher_age TEXT,
            teacher_class TEXT)""")
    conn.commit()
    conn.close()



# Create staff table
def create_staff_table():
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_name TEXT,
            staff_scale TEXT,
            staff_contact TEXT,
            staff_salary TEXT,
            staff_transport TEXT,
            staff_education TEXT,
            staff_age TEXT
        )
       """)
    conn.commit()
    conn.close()



# Add a new student
def add_student(col1,col2):
        
        with col1:
            
            name = st.text_input("Enter student name",key="name")
            class_ = st.text_input("Enter student class",key = "class_")
            section = st.radio("Student section",['RED','BLUE','PINK','YELLOW','GREEN'],key = "section")
            gender = st.radio("Select student gender", ["Male", "Female"],key = "gender")
            grade = st.radio("Select student grade",['A','B','C','D'],key = "grade")
            teacher_name = st.text_input("Enter teacher name",key = "teacher_name")
            address = st.text_input("Enter student address")
        with col2:
            st.header("Add Student Record")
            st.header(" ")
            st.header("")   
            contact = st.number_input("Enter student contact",value = 12341234567,key="contact")
            fee = st.number_input("Enter student fee", value = 0,key = "fee")
            driver_contact = st.number_input("Enter driver contact",value = 12341234567,key = "driver_contact")
            transport_fee = st.number_input("Enter transport fee",value=0,key = "transport_fee")
            uniform_dues = st.number_input("Enter uniform dues",value = 0,key = "uniform_dues")
            books_dues = st.number_input("Enter books dues",value=0,key = "books_dues")
            admission_fee = st.number_input("Enter admission fee",value=0,key = "admission_fee")
            paper_money = st.number_input("Enter paper money",value=0,key = "paper_money")
            fee_status = st.radio("Select fee status", ["Paid", "Unpaid"],key = "fee_status")

     
    

        if st.button("Save Chang"):
             if not name or not class_ or not contact:
                 st.warning("Please fill in required fields")
                 return False
             else:
                 conn = sqlite3.connect("school.db")
                 c = conn.cursor()
                 
                 c.execute('SELECT * FROM student WHERE contact=?', (contact,))
                 data = c.fetchone()
                 if data is not None:
                    st.warning("Customer with this phone number already exists.")
                    conn.close()
                    return False

                     
                 c.execute("""INSERT INTO student (name, class_, section, gender, grade, teacher_name, address, contact, fee,driver_contact, transport_fee, uniform_dues, books_dues, admission_fee,paper_money, fee_status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                 (name, class_, section, gender, grade, teacher_name, address, contact,fee, driver_contact, transport_fee, uniform_dues, books_dues, admission_fee,paper_money, fee_status))
                 conn.commit()
                 conn.close()
                 st.success("Student added successfully")
                 return True
    



# Add a new staff member
def add_teacher():
    st.subheader("Add  Teacher Record")
    teacher_name = st.text_input("Enter Teacher name")
    teacher_scale = st.text_input("Enter Teacher scale")
    teacher_contact = st.text_input("Enter Teacher contact")
    teacher_salary = st.text_input("Enter Teacher salary")
    teacher_transport = st.text_input("Enter Teacher transport")
    teacher_education = st.text_input("Enter Teacher education")
    teacher_subject = st.text_input("Enter Teacher Subject")
    teacher_age = st.text_input("Enter Teacher age")
    teacher_class = st.text_input("Enter Teacher Class")
    
    if st.button("Save"):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO teacher (teacher_name, teacher_scale, teacher_contact, teacher_salary, teacher_transport, teacher_education, teacher_subject,teacher_age, teacher_class)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (teacher_name, teacher_scale, teacher_contact, teacher_salary, teacher_transport, teacher_education, teacher_subject, teacher_age,teacher_class))
        conn.commit()
        conn.close()
        st.success("Teacher added successfully")
    elif st.button("Cancel"):
         st.warning("Teacher not added")


# Add a new staff member
def add_staff():
    st.subheader("Add Staff Record")
    staff_name = st.text_input("Enter staff name")
    staff_scale = st.text_input("Enter staff scale")
    staff_contact = st.text_input("Enter staff contact")
    staff_salary = st.text_input("Enter staff salary")
    staff_transport = st.text_input("Enter staff transport")
    staff_education = st.text_input("Enter staff education")
    staff_age = st.text_input("Enter staff age")
    
    if st.button("Save"):
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("""
            INSERT INTO staff (staff_name, staff_scale, staff_contact, staff_salary, staff_transport, staff_education, staff_age)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (staff_name, staff_scale, staff_contact, staff_salary, staff_transport, staff_education, staff_age))
        conn.commit()
        conn.close()
        st.success("Staff member added successfully")
    elif st.button("Cancel"):
        st.warning("Staff member not added")
        




# View all students
def view_all_student():
    st.subheader("All Students")
    conn = sqlite3.connect('school.db')
    df = pd.read_sql_query("SELECT * FROM student", conn)
    conn.close()

    if df.empty:
        st.warning("No records found.")
    else:
        st.write("List of all Students:")
        st.table(df)

def view_teacher():
    st.subheader("All Teacher")
    conn = sqlite3.connect('school.db')
    df = pd.read_sql_query("SELECT * FROM teacher", conn)
    conn.close()

    if df.empty:
        st.warning("No records found.")
    else:
        st.write("List of all Teachers:")
        st.table(df)




# View all staff
def view_all_staff():
    st.subheader("All Staff")
    conn = sqlite3.connect('school.db')
    df = pd.read_sql_query("SELECT * FROM staff", conn)
    conn.close()

    if df.empty:
        st.warning("No records found.")
    else:
        st.write("List of all Students:")
        st.table(df)

#function for searching student
def search_student():
    st.subheader("Search for a student")
    search_term = st.text_input("Enter a student's contact or fee status:")
    
    if search_term:
        conn = sqlite3.connect("school.db")
        c = conn.cursor()
        c.execute("SELECT * FROM student WHERE contact = ? OR fee_status = ?", (search_term, search_term))
        results = c.fetchall()
        conn.close()
        
        if len(results) > 0:
            st.write("Search Results:")
            col_names = ["ID", "Name", "Class", "Section", "Gender", "Grade", "Teacher Name", "Address", "Contact", "Fee",
                         "Driver Contact", "Transport Fee", "Uniform Dues", "Books Dues", "Admission Fee", "Paper Money", "Fee Status"]
            df = pd.DataFrame(results, columns=col_names)
            st.table(df)
        else:
            st.warning("No matching records found")
    else:
        st.info("Please enter a student name")


def search_teacher():
    conn = sqlite3.connect("school.db")
    c = conn.cursor()

    st.subheader("Search Teacher Record")

    search_option = st.selectbox("Search by:", ["Name", "Contact"])

    if search_option == "Contact":
        contact = st.text_input("Enter teacher contact:")
        c.execute('''SELECT * FROM teacher WHERE teacher_contact = ?''', (contact,))
        result = c.fetchone()
        conn.close()

    elif search_option == "Name":
        name = st.text_input("Enter Teacher name:")
        c.execute('''SELECT * FROM teacher WHERE teacher_name = ?''', (name,))
        result = c.fetchone()
        conn.close()

    if not result:
        st.info("Enter a valid teacher info.")
        return False
    else:
        cols = ['ID', 'Teacher Name', 'Scale', 'Contact', 'Salary', 'Transport', 'Education','Subject','age','Class_']    
        df = pd.DataFrame([result], columns=cols) #[result] is use for fetchone while fetchall not requir this conversion of tuple to list
        st.table(df)
    if not search_option:
        st.info("Please enter a teacher name or contact.")
    
    


#edit student record function
def edit_student(col1,col2):
    with col1:
         st.subheader("Edit Students Records")
        
    conn = sqlite3.connect('school.db')

    # c is the controle variable.
    c = conn.cursor() 

    with col2:
         search_option = st.selectbox("Search by:", ["Name", "Contact"])
    with col1:
       if search_option == "Contact":
           contact = st.text_input("Enter customer phone:")
           
           c.execute('''SELECT * FROM student WHERE contact = ?''', (contact,))
           result = c.fetchone()
           
        
       elif search_option == "Name":
            name = st.text_input("Enter Student name:")
           
            c.execute('''SELECT * FROM student WHERE name = ?''', (name,))
            result = c.fetchone()
           

    
      
        
       if not result:
           st.warning("Customer not found.")
           return 0

            # Edit form
       new_name = st.text_input("Enter new name", value=result[1])
       new_class = st.text_input("Enter new class", value=result[2])
       new_section =st.selectbox("Select new section", ['RED','BLUE','PINK','YELLOW','GREEN'],
                                    index=['RED','BLUE','PINK','YELLOW','GREEN'].index(result[3]))
       new_gender = st.selectbox("Select new gender", ["Male", "Female"],
                                    index=["Male", "Female"].index(result[4]))
       new_grade = st.selectbox("Select new grade", ['A', 'B', 'C', 'D'],
                                    index=['A', 'B', 'C', 'D'].index(result[5]))
       new_teacher_name = st.text_input("Enter new teacher name", value=result[6])
       new_address = st.text_input("Enter new address", value=result[7])
       new_contact = st.text_input("Enter new contact", value=result[8])
       new_fee = st.number_input("Enter new fee", value=result[9])
       new_driver_contact = st.number_input("Enter new driver contact", value=result[10])
       new_transport_fee = st.number_input("Enter new transport fee", value=result[11])
       new_uniform_dues = st.number_input("Enter new uniform dues", value=result[12])
       new_books_dues = st.number_input("Enter new books dues", value=result[13])
       new_admission_fee = st.number_input("Enter new admission fee", value=result[14])
       new_paper_money = st.number_input("Enter new paper money", value=result[15])
       new_fee_status = st.selectbox("Select new fee status", ["Paid", "Unpaid"],
                                             index=["Paid", "Unpaid"].index(result[16]))

    
    if st.button("Update Record"):
            
        c.execute("""UPDATE student SET name = ?,class_ = ?,section = ?,gender = ?,grade = ?,teacher_name = ?,address = ?,contact = ?,fee = ?,
                           driver_contact = ?,transport_fee = ?,uniform_dues = ?,books_dues = ?,admission_fee = ?,paper_money = ?,fee_status = ?
                           WHERE id = ?
                    """, (new_name, new_class, new_section, new_gender, new_grade, new_teacher_name,
                          new_address, new_contact, new_fee, new_driver_contact, new_transport_fee,
                          new_uniform_dues, new_books_dues, new_admission_fee, new_paper_money, new_fee_status,
                          result[0]))
        conn.commit()
        conn.close()
        st.success("Record updated successfully")

         
def edit_teacher(col1, col2):
    with col1:
        st.subheader("Edit Teacher Records")

    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    with col2:
        search_option = st.selectbox("Search by:", ["Name", "Contact"])

    with col1:
        if search_option == "Contact":
            contact = st.text_input("Enter teacher contact:")
            c.execute('''SELECT * FROM teacher WHERE teacher_contact = ?''', (teacher_contact,))
            result = c.fetchone()
        
        elif search_option == "Name":
             teacher_name = st.text_input("Enter teacher name:")
             c.execute('''SELECT * FROM teacher WHERE teacher_name = ?''', (teacher_name,))
             result = c.fetchone()
    
        if not result:
            st.warning("Teacher not found.")
            return 0

        # Edit form
        name = st.text_input("Enter new name", value=result[1])
        scale = st.text_input("Enter new Scale", value=result[2])
        contact = st.text_input("Enter new Contact", value=result[3])
        salary = st.text_input("Enter new Salary", value=result[4])
        transport = st.text_input("Enter new Transport", value=result[5])
        education = st.text_input("Enter new Education", value=result[6])
        subject = st.text_input("Enter new Subject", value=result[7])
        age = st.text_input("Enter new Age", value=result[8])
        class_ = st.text_input("Enter new Class", value=result[9])

    if st.button("Update Record"):
        c.execute("""UPDATE teacher SET teacher_name = ?, teacher_scale = ? ,teacher_contact = ?, teacher_salary = ?,teacher_transport= ?, teacher_education = ?,teacher_subject = ?, teacher_age = ?, teacher_class = ? WHERE id = ?""",
                  (name, scale, contact, salary, transport, education,subject,age,class_, result[0]))
        conn.commit()
        conn.close()
        st.success("Record updated successfully")



def edit_staff(col1, col2):
    with col1:
        st.subheader("Edit Staff Records")

    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    with col2:
        search_option = st.selectbox("Search by:", ["Name", "Contact"])

    with col1:
        if search_option == "Contact":
            contact = st.text_input("Enter staff phone:")
            c.execute('''SELECT * FROM staff WHERE staff_contact = ?''', (contact,))
            result = c.fetchone()
        elif search_option == "Name":
            name = st.text_input("Enter staff name:")
            c.execute('''SELECT * FROM staff WHERE staff_name = ?''', (name,))
            result = c.fetchone()

        if not result:
            st.info("Staff member not foun.")
            return 0

        # Edit form
        new_name = st.text_input("Enter new name", value=result[1])
        new_scale = st.text_input("Select new scale",value=result[2])
        new_contact = st.text_input("Enter new contact", value=result[3])
        new_salary = st.text_input("Enter new salary", value=result[4])
        new_transport = st.text_input("Enter new transport", value=result[5])
        new_education = st.text_input("Enter new education", value=result[6])
        new_age = st.text_input("Enter new age", value=result[7])

    if st.button("Update Record"):
        c.execute("""UPDATE staff SET staff_name=?, staff_scale=?, staff_contact=?, staff_salary=?, staff_transport=?,
                    staff_education=?, staff_age=? WHERE id=?""",
                  (new_name, new_scale, new_contact, new_salary, new_transport, new_education, new_age, result[0]))
        conn.commit()
        conn.close()
        st.success("Record updated successfully")




# Main function
def main():

    create_student_table()
    create_teacher_table()
    create_staff_table()
    st.set_page_config(page_title="Welcome to ABC School", page_icon=":school:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.title("School Database System")
    menu_options = ["Home","Add Student","Add Staff","Add Teachers", "View Students","View Staff" ,"View Teachers","Search Student","Edit Student","Edit Teacher","Edit Staff","Search Teacher"]
    choice = st.sidebar.radio("Select an option", menu_options)
    if choice == "Home":
        st.header("Welcome to My School")
        st.write("Brows from side bar") 

    elif choice == "Add Student":
        add_student(col1,col2)

    elif choice == "Add Staff":
        
        add_staff() 

    elif choice == "Add Teachers":
        add_teacher()
    

    elif choice == "View Students":
        view_all_student()
    
    elif choice == "View Staff":
        view_all_staff()

       

    elif choice == "View Teachers":
        view_teacher()

    elif choice == "Search Student":
        search_student()

    elif choice == "Search Teacher":
        search_teacher()     

    elif choice == "Edit Student":
        edit_student(col1,col2)
    elif choice == "Edit Teacher":
        edit_teacher(col1,col2)

    elif choice == "Edit Staff":
        edit_staff(col1,col2)     

if __name__ == "__main__":
    main()
