"""
Conversation manager for persisting and loading chat history.
"""

from sqlalchemy.orm import Session
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from database import ConversationMessage, get_db
from typing import List


def save_message(user_id: int, role: str, content: str):
    """
    Save a single message to the database.

    Args:
        user_id: The ID of the user
        role: The role ('system', 'user', or 'assistant')
        content: The message content
    """
    db = get_db()

    try:
        message = ConversationMessage(
            user_id=user_id,
            role=role,
            content=content
        )
        db.add(message)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def load_conversation_history(user_id: int) -> List:
    """
    Load the entire conversation history for a user.

    Args:
        user_id: The ID of the user

    Returns:
        List of LangChain message objects
    """
    db = get_db()

    try:
        # Get all messages for this user, ordered by timestamp
        messages = db.query(ConversationMessage).filter(
            ConversationMessage.user_id == user_id
        ).order_by(ConversationMessage.timestamp).all()

        # Convert to LangChain message objects
        langchain_messages = []
        for msg in messages:
            if msg.role == "system":
                langchain_messages.append(SystemMessage(content=msg.content))
            elif msg.role == "user":
                langchain_messages.append(HumanMessage(content=msg.content))
            elif msg.role == "assistant":
                langchain_messages.append(AIMessage(content=msg.content))

        return langchain_messages

    finally:
        db.close()


def clear_conversation_history(user_id: int):
    """
    Clear all conversation history for a user.

    Args:
        user_id: The ID of the user
    """
    db = get_db()

    try:
        db.query(ConversationMessage).filter(
            ConversationMessage.user_id == user_id
        ).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_message_count(user_id: int) -> int:
    """
    Get the total number of messages for a user.

    Args:
        user_id: The ID of the user

    Returns:
        Number of messages
    """
    db = get_db()

    try:
        count = db.query(ConversationMessage).filter(
            ConversationMessage.user_id == user_id
        ).count()
        return count
    finally:
        db.close()
