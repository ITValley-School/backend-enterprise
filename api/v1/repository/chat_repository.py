from sqlalchemy.orm import Session

from db.models.chat_message import ChatMessage

def save_message(db: Session, from_id: str, to_id: str, content: str):
    message = ChatMessage(from_id=from_id, to_id=to_id, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
