import streamlit as st
import sqlite3
import pandas as pd

import requests
from streamlit_lottie import st_lottie

#function to handle lottie animation
def loti(url):
    r = requests.get(url)
    if r.status_code != 200:
       return None
    else:
        return r.json()

#project school database

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
            contact TEXT,
            fee INTEGER,
            driver_contact TEXT,
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

# Create finance table
def create_finance_table():
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    #c.execute("DROP TABLE IF EXISTS finance")
    c.execute("""CREATE TABLE IF NOT EXISTS finance 
        
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            month DATE,    
            building_rent TEXT,
            electricity TEXT,
            staff_food TEXT,
            transport_fuel TEXT,
            transport_mechanic TEXT,
            internet_bill TEXT,
            generator_cost TEXT,
            advertisement TEXT,
            other TEXT,
            date DATE DEFAULT (date('now', 'localtime')))""")
    conn.commit()
    conn.close()

# Connect to the database
def fiance_record (month1):
    conn = sqlite3.connect("school.db")


    # Execute the query and fetch the record for the selected month into a DataFrame
    query = """
        SELECT building_rent, electricity, staff_food, transport_fuel, transport_mechanic,
            internet_bill, generator_cost, advertisement, other
        FROM finance
        WHERE month = ?
    """

    df_finance_record = pd.read_sql_query(query, conn, params=(month1,))

    numeric_columns = df_finance_record.columns[0:]

    df_finance_record[numeric_columns] = df_finance_record[numeric_columns].apply(pd.to_numeric)
    # Calculate the total expenditure for the selected month
    total_expenditure = df_finance_record[numeric_columns].sum().sum()

    # Close the database connection
    conn.close()
    return total_expenditure



# Add a new finance record
def add_finance_record(month,building_rent, electricity, staff_food, transport_fuel, transport_mechanic, internet_bill, generator_cost, advertisement, other):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO finance (month,building_rent, electricity, staff_food, transport_fuel, transport_mechanic, internet_bill, generator_cost, advertisement, other)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (month,building_rent, electricity, staff_food, transport_fuel, transport_mechanic, internet_bill, generator_cost, advertisement, other))
    conn.commit()
    conn.close()
    st.success("Record Added successfully") 

#wieve fiana records
def get_all_finance_records():
    conn = sqlite3.connect("school.db")
    df = pd.read_sql_query("SELECT * FROM finance", conn)
    conn.close()
    return df                                                             

#Edite fiance records
def update_finance_record(record_id, month, building_rent, electricity, staff_food, transport_fuel, transport_mechanic, internet_bill, generator_cost, advertisement, other):
    conn = sqlite3.connect("school.db")
    c = conn.cursor()
    c.execute("""
        UPDATE finance
        SET month=?, building_rent=?, electricity=?, staff_food=?, transport_fuel=?, transport_mechanic=?, internet_bill=?, generator_cost=?, advertisement=?, other=?
        WHERE id=?
    """, (month,building_rent, electricity, staff_food, transport_fuel, transport_mechanic, internet_bill, generator_cost, advertisement, other, record_id))
    conn.commit()
    conn.close()

#delete finance record
def delete_finance_record(record_id):
    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    # Delete the record from the finance table
    c.execute("DELETE FROM finance WHERE id = ?", (record_id,))
    
    conn.commit()
    conn.close()    

#student statistics and analysis
def student_statistic():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()
    st.subheader("Students Statistics :chart: ")
    class_numbers = ['1', '2', '3', '4', '5']
    section = ['RED', 'BLUE','PINK','YELLOW','GREEN']

    selected_class = st.selectbox("Select Class", class_numbers)
    selected_section = st.selectbox("Select Section", section)

    query_fee_paid = f"SELECT COUNT(*) AS total_students FROM student WHERE class_='{selected_class}' AND section='{selected_section}' AND fee_status = 'Paid'"
    df_feepaid = pd.read_sql_query(query_fee_paid, conn)
    #total_students_fee_paid = c.fetchone()[0]


    query_fee_unpaid = f"SELECT COUNT(*) AS total_students FROM student WHERE class_='{selected_class}' AND section='{selected_section}' AND fee_status='Unpaid'"
    c.execute(query_fee_unpaid)
    total_students_fee_unpaid = c.fetchone()[0]

    query_class_teacher = f"SELECT teacher_name from student WHERE class_='{selected_class}' AND section = '{selected_section}'"
    c.execute(query_class_teacher)
    
    result_teacher_name = c.fetchone()
    teacher_name = result_teacher_name[0] if result_teacher_name else "N/A"    

    # Query to get total students with selected fee status
    toalt_student_inclass = f"SELECT COUNT(*) AS total_students_fee_status FROM student WHERE class_='{selected_class}' AND section='{selected_section}'"
    c.execute(toalt_student_inclass)
    total_students_inclass = c.fetchone()[0]    

    conn.close()

    
    st.write("Total student in class ",selected_class," in section ",selected_section)
    st.write(total_students_inclass)
    st.write("Total Students in class ",selected_class,"who fee is Paid")
    st.write(df_feepaid)
    #st.write(total_students_fee_paid)
    st.write()
    st.write("Total Students in class ",selected_class,"who fee is Unpaid")
    st.write(total_students_fee_unpaid)    
    st.write("Teacher name ")
    st.write(teacher_name)
    

    return



# Add a new student
def add_student(col1,col2):


                                
        with col1:
            
            st.subheader("Add Student Record :male-student:")
            name = st.text_input("Enter student name",key="name")
            class_ = st.text_input("Enter student class",key = "class_")
            section = st.radio("Student section",['RED','BLUE','PINK','YELLOW','GREEN'],key = "section")
            gender = st.radio("Select student gender", ["Male", "Female"],key = "gender")
            grade = st.radio("Select student grade",['A','B','C','D'],key = "grade")
            teacher_name = st.text_input("Enter teacher name",key = "teacher_name")
            address = st.text_input("Enter student address")
        with col2:

            
            st.write("##")  
            st.write("##")
            
             
            contact = st.text_input("Enter student contact",value = "03331234567",key="contact")
            fee = st.number_input("Enter student fee", value = 0,key = "fee")
            driver_contact = st.text_input("Enter driver contact",value = "03331234567",key = "driver_contact")
            transport_fee = st.number_input("Enter transport fee",value=0,key = "transport_fee")
            uniform_dues = st.number_input("Enter uniform dues",value = 0,key = "uniform_dues")
            books_dues = st.number_input("Enter books dues",value=0,key = "books_dues")
            admission_fee = st.number_input("Enter admission fee",value=0,key = "admission_fee")
            paper_money = st.number_input("Enter paper money",value=0,key = "paper_money")
            fee_status = st.radio("Select fee status", ["Paid", "Unpaid"],key = "fee_status")

     
    

        if st.button("Save Chang :inbox_tray: "):
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
    st.subheader("Add  Teacher Record :female-teacher:")
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
    st.subheader("Add Staff Record :male-guard:")
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
    st.subheader("All Students :clipboard: ")
    conn = sqlite3.connect('school.db')
    df = pd.read_sql_query("SELECT * FROM student", conn)
    conn.close()

    if df.empty:
        st.warning("No records found.")
    else:
        st.write("List of all Students:")
        st.table(df)

def view_teacher():
    st.subheader("All Teacher :clipboard: ")
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
    st.subheader("All Staff :clipboard: ")
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
    st.subheader("Search for a student :mag_right: ")
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
    
#search function for staff
def search_staff():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    st.subheader('Search Staff Record :magnifying_glass_tilted_right: ')

    search_option = st.selectbox('Search by:', ['Name', 'Contact'])

    if not search_option:
        st.warning('Please select a search option.')
        return False

    search_term = st.text_input(f'Enter staff {search_option.lower()}:')

    if not search_term:
        st.warning(f'Please enter a staff {search_option.lower()}.')
        return False

    if search_option == 'Contact':
        c.execute('SELECT * FROM staff WHERE staff_contact = ?', (search_term,))
        result = c.fetchone()

    elif search_option == 'Name':
        c.execute('SELECT * FROM staff WHERE staff_name = ?', (search_term,))
        result = c.fetchone()

    conn.close()

    if not result:
        st.info(f'No staff record found with {search_option.lower()} "{search_term}".')
        return False

    cols = ['ID', 'Name', 'Scall', 'Contact', 'Salary', 'Transport','Education','Age']
    df = pd.DataFrame([result], columns=cols)
    st.table(df)

    return True   


#edit student record function
def edit_student(col1,col2):
    with col1:
         st.subheader("Edit Students Records :memo: ")
        
    conn = sqlite3.connect('school.db')

    # c is the controle variable.
    c = conn.cursor() 

    with col2:
         st.write("##")
         st.write("##")
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
       new_driver_contact = st.text_input("Enter new driver contact", value=result[10])
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
        st.subheader("Edit Teacher Records :mag_right: ")

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

#delet a student 
def delete_student():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    st.subheader("Delete Student Record :plunger: ")

    search_option = st.selectbox('Delete by:', ['Name', 'Contact'])

    if not search_option:
        st.warning('Please select a delete option.')
        return False

    search_term = st.text_input(f'Enter student {search_option.lower()} to delete:')

    if not search_term:
        st.warning(f'Please enter a student {search_option.lower()} to delete.')
        return False

    if search_option == 'Contact':
        c.execute('SELECT * FROM student WHERE contact = ?', (search_term,))
        result = c.fetchone()

    elif search_option == 'Name':
        c.execute('SELECT * FROM student WHERE name = ?', (search_term,))
        result = c.fetchone()

    if not result:
        st.info(f'No student record found with {search_option.lower()} "{search_term}".')
        return False

    confirm_delete = st.button(f'Confirm delete for student {result[1]} ({result[3]}-{result[4]})')

    if confirm_delete:
        c.execute('DELETE FROM student WHERE id = ?', (result[0],))
        conn.commit()
        st.success(f'Student record for {result[1]} ({result[3]}-{result[4]}) has been deleted.')
        conn.close()
        return True

    conn.close()
    return False

#Delete teacher record
def teacher_delete():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    st.subheader('Delete Teacher Record')

    search_option = st.selectbox('Delete by:', ['Name', 'Contact'])

    if not search_option:
        st.warning('Please select a delete option.')
        return False

    search_term = st.text_input(f'Enter teacher {search_option.lower()} to delete:')

    if not search_term:
        st.warning(f'Please enter a teacher {search_option.lower()} to delete.')
        return False

    if search_option == 'Contact':
        c.execute('SELECT * FROM teacher WHERE teacher_contact = ?', (search_term,))
        result = c.fetchone()

    elif search_option == 'Name':
        c.execute('SELECT * FROM teacher WHERE teacher_name = ?', (search_term,))
        result = c.fetchone()

    if not result:
        st.info(f'No teacher record found with {search_option.lower()} "{search_term}".')
        return False

    confirm_delete = st.button(f'Confirm delete for teacher {result[1]} ({result[3]})')

    if confirm_delete:
        c.execute('DELETE FROM teacher WHERE id = ?', (result[0],))
        conn.commit()
        st.success(f'Teacher record for {result[1]} ({result[3]}) has been deleted.')
        conn.close()
        return True

    conn.close()
    return False

#Delete staff function
def delete_staff():
    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    st.subheader('Delete Staff Record')

    search_option = st.selectbox('Delete by:', ['Name', 'Contact'])

    if not search_option:
        st.warning('Please select a delete option.')
        return False

    search_term = st.text_input(f'Enter staff {search_option.lower()} to delete:')

    if not search_term:
        st.warning(f'Please enter a staff {search_option.lower()} to delete.')
        return False

    if search_option == 'Contact':
        c.execute('SELECT * FROM staff WHERE staff_contact = ?', (search_term,))
        result = c.fetchone()

    elif search_option == 'Name':
        c.execute('SELECT * FROM staff WHERE staff_name = ?', (search_term,))
        result = c.fetchone()

    if not result:
        st.info(f'No staff record found with {search_option.lower()} "{search_term}".')
        return False

    confirm_delete = st.button(f'Confirm delete for staff {result[1]} ({result[3]})')

    if confirm_delete:
        c.execute('DELETE FROM staff WHERE id = ?', (result[0],))
        conn.commit()
        st.success(f'Staff record for {result[1]} ({result[3]}) has been deleted.')
        conn.close()
        return True

    conn.close()
    return False






def student_page(col1,col2):
    st.sidebar.title("Options")
    menu_options = ["Students Statistics","Add Student", "View Students", "Edit Student", "Search Student", "Delete Student"]
    choice = st.sidebar.radio("Select an option", menu_options)

    if choice == "Students Statistics":
        student_statistic()

    elif choice == "Add Student":
        add_student(col1,col2)

    elif choice == "View Students":
        view_all_student()

    elif choice == "Edit Student":
        edit_student(col1,col2)

    elif choice == "Search Student":
        search_student()

    elif choice == "Delete Student":
        delete_student()
    

def teacher_page(col1,col2):
    st.sidebar.title("Options")
    menu_options = ["Add Teacher", "View Teachers", "Edit Teacher", "Search Teacher", "Delete Teacher"]
    choice = st.sidebar.radio("Select an option", menu_options)

    if choice == "Add Teacher":
        add_teacher()

    elif choice == "View Teachers":
        view_teacher()

    elif choice == "Edit Teacher":
        edit_teacher(col1,col2)

    elif choice == "Search Teacher":
        search_teacher()

    elif choice == "Delete Teacher":
        teacher_delete()

def staff_page(col1,col2):
    st.sidebar.title("Options")
    menu_options = ["Add Staff", "View Staff", "Edit Staff", "Search Staff", "Delete Staff"]
    choice = st.sidebar.radio("Select an option", menu_options)

    if choice == "Add Staff":
        add_staff()

    elif choice == "View Staff":
        view_all_staff()

    elif choice == "Edit Staff":
        edit_staff(col1,col2)

    elif choice == "Search Staff":
        search_staff()

    elif choice == "Delete Staff":
        delete_staff()

#finance page
def finance_page():
    menu = ["Finance Home","Add Finance Records", "View Finance Records", "Update Finance Records", "Delete Finance Record"]
    select = st.sidebar.radio("Select an option", menu)


    if select == "Finance Home":
        st.subheader("Here is some information about school finance :bar_chart:")



        # Establish connection to the database
        conn = sqlite3.connect('school.db')
        c = conn.cursor()
        # Execute the query and fetch the result into a DataFrame
        query_expens = "SELECT SUM(building_rent + electricity + staff_food + transport_fuel + transport_mechanic + internet_bill + generator_cost + advertisement + other) AS total_cost FROM finance"
        df_expenditure = pd.read_sql_query(query_expens, conn)

        # Execute the query and fetch the result into a DataFrame
        query_student_all_dues = "SELECT SUM(fee + transport_fee + uniform_dues + books_dues + admission_fee + paper_money ) AS total_student_dues FROM student"
        df_total_student_dues = pd.read_sql_query(query_student_all_dues, conn) 

        # Query to grab and add all teachers' salaries
        c.execute("SELECT SUM(teacher_salary) FROM teacher")
        teachers_salary_total = c.fetchone()[0]

        # Query to grab and add all staff salaries
        c.execute("SELECT SUM(staff_salary) FROM staff")
        staff_salary_total = c.fetchone()[0]   

        st.write("Total Teacher salaries",teachers_salary_total)
        st.write("Total Staff salaries",staff_salary_total)    

        st.write("Total Deus of all students",df_total_student_dues)
        
        st.write("Total expenditure of school",df_expenditure )


        # Execute the query and fetch the result into a DataFrame
        query = "SELECT SUM(building_rent) AS building_rent_total, \
                SUM(electricity) AS electricity_total, \
                SUM(staff_food) AS staff_food_total, \
                SUM(transport_fuel) AS transport_fuel_total, \
                SUM(transport_mechanic) AS transport_mechanic_total, \
                SUM(internet_bill) AS internet_bill_total, \
                SUM(generator_cost) AS generator_cost_total, \
                SUM(advertisement) AS advertisement_total, \
                SUM(other) AS other_total \
                FROM finance"
        dftotal = pd.read_sql_query(query, conn)

        # Close the database connection
        conn.close()

        st.write(dftotal)
        search = st.date_input("Select a month to calculat expenditure")
        df_expenditure = fiance_record (search)
        st.write("Total school expenditure in Selected month")
        st.write(df_expenditure)


    elif select == "Add Finance Records":
        st.header("Add Finance Records")
        month = st.date_input("Enter month")
        building_rent = st.text_input("Building Rent")
        electricity = st.text_input("Electricity")
        staff_food = st.text_input("Staff Food")
        transport_fuel = st.text_input("Transport Fuel")
        transport_mechanic = st.text_input("Transport Mechanic")
        internet_bill = st.text_input("Internet Bill")
        generator_cost = st.text_input("Generator Cost")
        advertisement = st.text_input("Advertisement")
        other = st.text_input("Other")

        if st.button("Add Record"):
            if building_rent and electricity and internet_bill and month :
                add_finance_record(month,building_rent, electricity, staff_food, transport_fuel, transport_mechanic, internet_bill, generator_cost, advertisement, other)
            else:
                st.warning("Please fill in all the fields.")

    elif select == "View Finance Records":
        st.header("View Finance Records")
        record=get_all_finance_records()
        if record.empty :
             st.write("No records found.")
        else:     
            st.dataframe(record)

    elif select == "Update Finance Records":
        st.header("Update Finance Records")

        # Retrieve existing finance records
        finance_records = get_all_finance_records()

        if finance_records.empty:
            st.warning("No finance records found.")
        else:
            # Display the records in a table
            st.dataframe(finance_records)

            # Select the record to update
            search = st.selectbox("select a searh option",["id","month"])
            #record_id = int(record_id) if record_id.isdigit() else None
      
            if search is None :
                st.warning("Please select a search option.")
            else:
                if search == "id":
                   search_term=st.number_input("Enter an ID to search",value=1)
                elif search == "month":
                   search_term1=st.date_input("Select a date to search")
                   search_term=search_term1.strftime('%Y-%m-%d')        
                if search_term is None:
                    st.warning("Please select search term")
                else:    
                    conn = sqlite3.connect('school.db')
                    c = conn.cursor()
                    c.execute('''SELECT * FROM finance WHERE id = ? OR DATE(month) = DATE(?)''', (search_term, search_term))
                    result = c.fetchone()
                    conn.close()
                    if result is None:
                        st.warning("No record found")
                    else:    
                        # Get updated values from the user
                        month = st.date_input("select month",value=None)
                        building_rent = st.text_input("Building Rent",value=result[2])
                        electricity = st.text_input("Electricity",value=result[3])
                        staff_food = st.text_input("Staff Food",value=result[4])
                        transport_fuel = st.text_input("Transport Fuel",value=result[5])
                        transport_mechanic = st.text_input("Transport Mechanic",value=result[6])
                        internet_bill = st.text_input("Internet Bill",value=result[7])
                        generator_cost = st.text_input("Generator Cost",value=result[8])
                        advertisement = st.text_input("Advertisement",value=result[9])
                        other = st.text_input("Other",value=result[10])
                
                        if st.button("Update Record"):
                            update_finance_record(result[0],month,building_rent,electricity,staff_food,transport_fuel,transport_mechanic,internet_bill,generator_cost,advertisement,other)
                            st.success("Record updated successfully.")
                

    elif select == "Delete Finance Record":
            st.header("Delete Finance Record")

            # Retrieve existing finance records
            finance_records = get_all_finance_records()

            if finance_records.empty:
                st.warning("No finance records found.")
            else:
                # Display the records in a table
                st.dataframe(finance_records)

                # Select the record to delete
                search = st.selectbox("Select a search option", ["id", "month"])

                if search is None:
                    st.warning("Please select a search option.")
                else:
                    if search == "id":
                        search_term = st.number_input("Enter an ID to delete", value=1)
                    elif search == "month":
                        search_term1 = st.date_input("Select a date to delete")
                        search_term = search_term1.strftime('%Y-%m-%d')

                    if search_term is None:
                        st.warning("Please select a search term.")
                    else:
                        conn = sqlite3.connect('school.db')
                        c = conn.cursor()
                        c.execute('''SELECT * FROM finance WHERE id = ? OR DATE(month) = DATE(?)''', (search_term, search_term))
                        result = c.fetchone()
                        conn.close()

                        if not result:
                            st.warning("Record not found.")
                        else:
                            st.info("Record to be deleted:")
                            st.write(result)

                            if st.button("Delete Record"):
                                delete_finance_record(result[0])
                                st.success("Record deleted successfully.")


def home_page():
    

    #loti_student = loti("https://assets2.lottiefiles.com/packages/lf20_ei2gf306.json")
    #st_lottie(loti_student,height=300)
    loti_finance = loti("https://assets3.lottiefiles.com/packages/lf20_yMpiqXia1k.json")
        
    col11,col22 = st.columns([1,2])
    with col11:
        st.write("##")
        st.write("##")
        st.write("##")
        st.header("Welcome Admin   :man:")
    with col22:
            
        st_lottie(loti_finance,height=300)

    conn = sqlite3.connect('school.db')
    c = conn.cursor()

    # Get total number of students
    query_students = "SELECT COUNT(*) FROM student"
    c.execute(query_students)
    total_students = c.fetchone()[0]

    # Get total number of teachers
    query_teachers = "SELECT COUNT(*) FROM teacher"
    c.execute(query_teachers)
    total_teachers = c.fetchone()[0]

    # Get total number of staff
    query_staff = "SELECT COUNT(*) FROM staff"
    c.execute(query_staff)
    total_staff = c.fetchone()[0]

    # Get total salaries of all teachers
    query_teacher_salaries = "SELECT SUM(teacher_salary) FROM teacher"
    c.execute(query_teacher_salaries)
    total_teacher_salaries = c.fetchone()[0]

    # Get total salaries of all staff
    query_staff_salaries = "SELECT SUM(staff_salary) FROM staff"
    c.execute(query_staff_salaries)
    total_staff_salaries = c.fetchone()[0]

    # Get total fee of all students
    query_student_fees = "SELECT SUM(fee) FROM student"
    c.execute(query_student_fees)
    total_student_fees = c.fetchone()[0]

    # Get total studentr who fee statuse is paid
    c.execute("SELECT COUNT(*) FROM student WHERE fee_status = 'Paid'")
    total_paid = c.fetchone()[0]

    # Get total studentr who fee statuse is paid
    c.execute("SELECT COUNT(*) FROM student WHERE fee_status = 'Unpaid'")
    total_unpaid = c.fetchone()[0]

    #total transport fee
    c.execute("SELECT SUM(transport_fee) FROM student")
    total_transport = c.fetchone()[0]

    #total admission fee
    c.execute("SELECT SUM(admission_fee) FROM student")
    total_admission = c.fetchone()[0]

    #total uniform dues
    c.execute("SELECT SUM(uniform_dues) FROM student")
    total_uniform_dues = c.fetchone()[0]

    #total book dues
    c.execute("SELECT SUM(books_dues) FROM student")
    total_books_dues = c.fetchone()[0]

    #total revenue
    c.execute("SELECT SUM(fee + transport_fee + uniform_dues + books_dues + admission_fee + paper_money) AS total_revenue FROM student")
    total_revenue = c.fetchone()[0]
    # Display total counts
    st.subheader("School Statistics :bar_chart: ")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Total Students")
        st.write(total_students)
        st.write("Total Student Fee")
        st.write(total_student_fees)
        st.write("Toal student who fee is Paid")
        st.write(total_paid)
        st.write("Total admission fee")
        st.write(total_admission)
        st.write("### Total Revenue of all students :chart: ")
        st.write(total_revenue)
    with col2:
        st.write("Total Teachers")
        st.write(total_teachers)
        st.write("Total Teacher Salaries")
        st.write(total_teacher_salaries)
        st.write("Toal student who fee is Unpaid")
        st.write(total_unpaid)  
        st.write("Total uniform dues")
        st.write(total_uniform_dues)      
    with col3:
        st.write("Total Staff")
        st.write(total_staff)
        st.write("Total Staff Salaries")
        st.write(total_staff_salaries)
        st.write("Total tranport dues")
        st.write(total_transport)
        st.write("Total books Dues")
        st.write(total_books_dues)
    conn.close()

# Main function
def main():

    create_student_table()
    create_teacher_table()
    create_staff_table()
    create_finance_table()

    st.set_page_config(page_title="My School", page_icon=":school:")
    col1, col2 = st.columns(2)
    # Define the pages
    PAGES = {
        "Home": lambda : home_page(),
        "Student": lambda : student_page(col1,col2),
        "Teacher": lambda: teacher_page(col1,col2),
        "Staff": lambda :staff_page(col1,col2),
        "Finance": lambda:finance_page()
    }

    # Render the sidebar with page options
    st.sidebar.title("Navigation :feet:")
    page_choice = st.sidebar.radio("Select a page", list(PAGES.keys()))

    # Call the appropriate page function based on the user's choice
    page = PAGES[page_choice]
    page()    

if __name__ == "__main__":
    main()
