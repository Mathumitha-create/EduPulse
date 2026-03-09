import streamlit as st
import bcrypt
from sqlalchemy.orm import Session
from models import User, AcademicData
from database import SessionLocal

def verify_password(plain_password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, name: str, email: str, password: str, role: str):
    hashed_password = get_password_hash(password)
    db_user = User(name=name, email=email, password_hash=hashed_password, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Initialize default academic data for students
    if role == "student":
        acad = AcademicData(user_id=db_user.id)
        db.add(acad)
        db.commit()
        
    return db_user

def init_auth_session():
    """Initialize authentication session state variables."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None

def login_user(email, password):
    db = SessionLocal()
    try:
        user = get_user(db, email)
        if user and verify_password(password, user.password_hash):
            st.session_state.logged_in = True
            st.session_state.user_id = user.id
            st.session_state.user_name = user.name
            st.session_state.user_role = user.role
            return True, "Login successful!"
        return False, "Invalid email or password."
    finally:
        db.close()

def logout_user():
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_role = None
