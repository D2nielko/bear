"""
Authentication module for the Teddy Bear Companion.
Handles user registration, login, and password management.
"""

import bcrypt
from sqlalchemy.orm import Session
from database import User, get_db, init_db


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def register_user(username: str, password: str) -> tuple[bool, str, User | None]:
    """
    Register a new user.

    Returns:
        tuple: (success: bool, message: str, user: User | None)
    """
    # Validate username
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long.", None

    # Validate password
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long.", None

    db = get_db()

    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return False, "Username already exists. Please choose a different username.", None

        # Create new user
        password_hash = hash_password(password)
        new_user = User(username=username, password_hash=password_hash)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return True, "Registration successful! Welcome!", new_user

    except Exception as e:
        db.rollback()
        return False, f"An error occurred during registration: {e}", None

    finally:
        db.close()


def login_user(username: str, password: str) -> tuple[bool, str, User | None]:
    """
    Authenticate a user.

    Returns:
        tuple: (success: bool, message: str, user: User | None)
    """
    db = get_db()

    try:
        # Find user by username
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return False, "Invalid username or password.", None

        # Verify password
        if not verify_password(password, user.password_hash):
            return False, "Invalid username or password.", None

        return True, "Login successful!", user

    except Exception as e:
        return False, f"An error occurred during login: {e}", None

    finally:
        db.close()


def get_user_by_id(user_id: int) -> User | None:
    """Get a user by their ID."""
    db = get_db()

    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    finally:
        db.close()
