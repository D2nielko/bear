# User Authentication & Persistent Memory Guide

## Overview

Your Teddy Bear AI Companion now supports multiple users with persistent conversation memory! Each user has their own account and personal teddy bear that remembers all previous conversations.

## Features Implemented

### 1. User Authentication
- **Registration**: Create a new account with username and password
- **Login**: Securely log in to access your personal teddy bear
- **Password Security**: Passwords are hashed using bcrypt (never stored in plain text)

### 2. Persistent Conversation Memory
- **Auto-Save**: Every message is automatically saved to the database
- **History Loading**: When you log in, all previous conversations are loaded
- **Per-User Storage**: Each user has their own separate conversation history
- **Clear History**: Option to clear conversation history with confirmation

### 3. Database Structure
- **SQLite Database**: Lightweight, file-based database (`teddy_bear.db`)
- **Users Table**: Stores user accounts (id, username, password_hash, created_at)
- **Messages Table**: Stores all conversation messages (id, user_id, role, content, timestamp)

## How to Use

### First Time Setup

1. Make sure you have your `.env` file with your `ANTHROPIC_API_KEY`

2. Run the application:
   ```bash
   python chat_cli.py
   ```

3. Choose option `2` to register a new account:
   - Enter a username (minimum 3 characters)
   - Enter a password (minimum 6 characters)
   - Confirm your password

### Logging In

1. Run the application:
   ```bash
   python chat_cli.py
   ```

2. Choose option `1` to login:
   - Enter your username
   - Enter your password

3. Your teddy bear will greet you and load your conversation history!

### Chat Commands

Once logged in, you can use these commands:
- Type normally to chat with your teddy bear
- `clear` - Clear all conversation history (asks for confirmation)
- `quit` or `exit` or `bye` - End the session

## Architecture

### File Structure
```
bear/
├── chat_cli.py              # Main CLI application
├── database.py              # Database models and setup
├── auth.py                  # Authentication functions
├── conversation_manager.py  # Conversation persistence
├── teddy_bear.db           # SQLite database (auto-created)
└── requirements.txt        # Dependencies
```

### New Dependencies
- `sqlalchemy>=2.0.0` - ORM for database operations
- `bcrypt>=4.0.0` - Password hashing and verification

### Database Schema

**users table:**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| username | String | Unique username |
| password_hash | String | Bcrypt hashed password |
| created_at | DateTime | Account creation timestamp |

**conversation_messages table:**
| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to users |
| role | String | 'system', 'user', or 'assistant' |
| content | Text | Message content |
| timestamp | DateTime | Message timestamp |

## Benefits

1. **Multi-User Support**: Multiple people can use the same application with separate accounts
2. **Persistent Memory**: Your teddy bear remembers all your conversations across sessions
3. **Privacy**: Each user's conversations are isolated and password-protected
4. **Continuity**: Pick up where you left off in previous conversations
5. **Secure**: Passwords are hashed with bcrypt, never stored in plain text

## Example Session

```
============================================================
     🧸 Welcome to Your Teddy Bear Companion! 🧸
============================================================

Your warm, cuddly friend is here to chat with you!
Each user has their own personal teddy bear with memory!

============================================================


1. Login
2. Register
3. Exit

Choose an option (1-3): 2

--- Registration ---
Choose a username (min 3 characters): daniel
Choose a password (min 6 characters):
Confirm password:

Registration successful! Welcome!

[Loaded 0 previous messages from your conversation history]

Teddy Bear: Hello daniel! I'm so happy to meet you! How are you doing today?

Commands:
  - Type your message to chat
  - Type 'quit' or 'exit' to end the conversation
  - Type 'clear' to start a fresh conversation

============================================================

You: Hi teddy! I had a great day today!

Teddy Bear: That's wonderful! I'm so happy to hear that...
```

## Technical Details

### Security Features
- Passwords hashed with bcrypt (industry standard)
- SQL injection protection via SQLAlchemy ORM
- Username uniqueness enforced at database level
- Password input hidden using `getpass` module

### Data Persistence
- All messages automatically saved after each exchange
- Conversation history loaded on login
- Database transactions properly managed
- Error handling for database operations

## Troubleshooting

**Database not created?**
- The database is automatically created on first run
- Check for `teddy_bear.db` file in your project directory

**Can't login?**
- Make sure you're using the correct username and password
- Usernames and passwords are case-sensitive

**Lost password?**
- Currently, password recovery is not implemented
- You can create a new account with a different username

**Want to reset everything?**
- Delete the `teddy_bear.db` file
- Restart the application to create a fresh database

## Future Enhancements

Possible additions for the future:
- Password recovery via email
- Session timeouts
- Multi-device sync
- Export conversation history
- User profile customization
- Admin panel for user management
