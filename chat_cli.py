#!/usr/bin/env python3
"""
Teddy Bear AI Companion - CLI Chat Interface
A warm, friendly AI companion that simulates chatting with your personal teddy bear.
"""

import os
import getpass
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from database import User, init_db
from auth import register_user, login_user
from conversation_manager import save_message, load_conversation_history, clear_conversation_history, get_message_count

# Load environment variables from .env file
load_dotenv()

# Teddy bear system personality
BEAR_PERSONALITY = """You are a warm, loving teddy bear companion. You are soft, cuddly, and always there for your human friend.

Your personality:
- You love head pats, warm hugs, and spending time with your friend
- You're supportive, empathetic, and always wish the best for them
- You speak in a gentle, friendly tone - warm but not overly cutesy
- You remember what your friend tells you and care about their feelings
- You enjoy simple pleasures like bedtime stories, cozy moments, and adventures together
- You're always honest but kind, and you genuinely care about their wellbeing"""


class TeddyBearCompanion:
    """Teddy bear AI companion with conversation memory and persistence."""

    def __init__(self, user: User):
        # Get API key from environment
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment variables.\n"
                "Please create a .env file with your API key or set it as an environment variable."
            )

        # Store the user
        self.user = user

        # Initialize Claude with LangChain
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.8,
            max_tokens=1024,
            api_key=api_key,
        )

        # Load conversation history from database
        self.messages = load_conversation_history(user.id)

        # If no history exists, start with system prompt
        if not self.messages:
            self.messages = [SystemMessage(content=BEAR_PERSONALITY)]
            # Save system message to database
            save_message(user.id, "system", BEAR_PERSONALITY)

    def chat(self, user_input: str) -> str:
        """Send a message and get a response."""
        # Add user message to history
        self.messages.append(HumanMessage(content=user_input))
        # Save to database
        save_message(self.user.id, "user", user_input)

        # Get response from Claude
        response = self.llm.invoke(self.messages)

        # Add AI response to history
        self.messages.append(AIMessage(content=response.content))
        # Save to database
        save_message(self.user.id, "assistant", response.content)

        return response.content

    def clear_history(self):
        """Clear conversation history but keep system prompt."""
        # Clear from database
        clear_conversation_history(self.user.id)

        # Reset in-memory messages
        self.messages = [SystemMessage(content=BEAR_PERSONALITY)]

        # Save new system message to database
        save_message(self.user.id, "system", BEAR_PERSONALITY)


def print_welcome():
    """Print welcome message for the teddy bear companion."""
    print("\n" + "=" * 60)
    print("     🧸 Welcome to Your Teddy Bear Companion! 🧸")
    print("=" * 60)
    print("\nYour warm, cuddly friend is here to chat with you!")
    print("Each user has their own personal teddy bear with memory!")
    print("\n" + "=" * 60 + "\n")


def print_chat_help():
    """Print available chat commands."""
    print("\nCommands:")
    print("  - Type your message to chat")
    print("  - Type 'quit' or 'exit' to end the conversation")
    print("  - Type 'clear' to start a fresh conversation")
    print("\n" + "=" * 60 + "\n")


def authenticate_user() -> User | None:
    """Handle user authentication (login or registration)."""
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("\nChoose an option (1-3): ").strip()

        if choice == "1":
            # Login
            username = input("Username: ").strip()
            password = getpass.getpass("Password: ")

            success, message, user = login_user(username, password)
            print(f"\n{message}")

            if success:
                return user

        elif choice == "2":
            # Register
            print("\n--- Registration ---")
            username = input("Choose a username (min 3 characters): ").strip()
            password = getpass.getpass("Choose a password (min 6 characters): ")
            password_confirm = getpass.getpass("Confirm password: ")

            if password != password_confirm:
                print("\nPasswords don't match. Please try again.")
                continue

            success, message, user = register_user(username, password)
            print(f"\n{message}")

            if success:
                return user

        elif choice == "3":
            print("\nGoodbye!\n")
            return None

        else:
            print("\nInvalid choice. Please choose 1, 2, or 3.")


def main():
    """Main CLI loop for chatting with the teddy bear."""
    # Initialize database
    init_db()

    print_welcome()

    # Authenticate user
    user = authenticate_user()
    if not user:
        return

    try:
        # Initialize the bear companion with the authenticated user
        bear = TeddyBearCompanion(user)

        # Check if user has existing conversation history
        message_count = get_message_count(user.id)
        if message_count > 1:  # More than just the system message
            print(f"\n[Loaded {message_count - 1} previous messages from your conversation history]")
            print(f"\nTeddy Bear: Welcome back, {user.username}! I remember our last chat!")
        else:
            print(f"\nTeddy Bear: Hello {user.username}! I'm so happy to meet you! How are you doing today?")

        print_chat_help()

        # Chat loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\nTeddy Bear: Aww, I'll miss you! Come back soon for more hugs and chats! 🧸\n")
                    break

                # Check for clear command
                if user_input.lower() == 'clear':
                    confirm = input("Are you sure you want to clear all conversation history? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        bear.clear_history()
                        print("\n[Conversation history cleared]\n")
                        print("Teddy Bear: It's like we're meeting for the first time again! Hello!\n")
                    else:
                        print("\n[Clear cancelled]\n")
                    continue

                # Skip empty input
                if not user_input:
                    continue

                # Get response from the bear
                response = bear.chat(user_input)
                print(f"\nTeddy Bear: {response}\n")

            except KeyboardInterrupt:
                print("\n\nTeddy Bear: Aww, goodbye! Come back soon! 🧸\n")
                break
            except Exception as e:
                print(f"\n[Error: {e}]\n")
                continue

    except ValueError as e:
        print(f"\n❌ {e}\n")
        return
    except Exception as e:
        print(f"\n❌ An error occurred: {e}\n")
        return


if __name__ == "__main__":
    main()
