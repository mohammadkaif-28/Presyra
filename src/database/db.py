from src.database.config import supabase
import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def check_teacher_credentials(username: str) -> bool:
    """
    Check if the provided username exists in the database.
    Args:
        username (str): The teacher's username.
    Returns:
        bool: True if the credentials are exists, False otherwise.
    """
    # Query the database for the teacher with the given username
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username: str, password: str, name: str) -> bool:
    """
    Create a new teacher in the database.
    Args:
        username (str): The teacher's username.
        password (str): The teacher's password.
        name (str): The teacher's name.
    Returns:
        bool: True if the teacher was created successfully, False otherwise.
    """
    # Hash the password
    hashed_password = hash_password(password)

    # Insert the new teacher into the database
    data = {"username": username,"password": hashed_password, "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username: str, password: str) -> bool:
    """
    Check if the provided username and password match a teacher in the database.
    Args:
        username (str): The teacher's username.
        password (str): The teacher's password.
    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    # Query the database for the teacher with the given username
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    
    if response.data:
        teacher = response.data[0]
        if check_password(password, teacher["password"]):
            return teacher  # Return the teacher object if credentials are valid

    return None

def get_all_students():
    """
    Retrieve all students from the database.
    Returns:
        list: A list of student records.
    """
    response = supabase.table("students").select("*").execute()
    return response.data

def create_student(new_name, face_embedding = None, voice_embedding = None):
    data = {'name':new_name, 'face_embedding':face_embedding, 'voice_embedding':voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data

def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name": name, "section": section, "teacher_id": teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendance_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions
        
        sub.pop('subject_student', None)
        sub.pop('attendance_logs', None)

    return subjects

def enroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, "subject_id": subject_id}
    response = supabase.table('subject_students').insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id, subject_id):
    response = supabase.table('subject_students').delete().eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data

def get_student_subject(student_id):
    response = supabase.table('subject_students').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data

def get_student_attendance(student_id):
    response = supabase.table('attendance_logs').select('*, subjects(*)').eq('student_id', student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data

def get_attendance_for_teacher(teacher_id):

    response = (supabase.table("attendance_logs").select("""*,subjects!inner(*),students(student_id,name)""").eq("subjects.teacher_id", teacher_id).execute())

    return response.data