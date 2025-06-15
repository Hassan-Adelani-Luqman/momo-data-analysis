from src.models.user import db # Import the shared db instance
from datetime import datetime # To handle date and time objects

class Sender(db.Model):
    __tablename__ = "senders"
    sender_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    messages_sent = db.relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")

class Recipient(db.Model):
    __tablename__ = "recipients"
    recipient_id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    messages_received = db.relationship("Message", foreign_keys="Message.recipient_id", back_populates="recipient")

class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("senders.sender_id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("recipients.recipient_id"))
    timestamp = db.Column(db.DateTime, nullable=False)
    message_body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    transaction_amount = db.Column(db.Float)
    currency = db.Column(db.String(10))
    status = db.Column(db.String(20))
    new_balance = db.Column(db.Float)
    fee = db.Column(db.Float)
    transaction_id = db.Column(db.String(50))
    recipient_name = db.Column(db.String(100))

    sender = db.relationship("Sender", foreign_keys=[sender_id], back_populates="messages_sent")
    recipient = db.relationship("Recipient", foreign_keys=[recipient_id], back_populates="messages_received")

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "sender_phone": self.sender.phone_number if self.sender else None,
            "recipient_phone": self.recipient.phone_number if self.recipient else None,
            "timestamp": self.timestamp.isoformat(),
            "message_body": self.message_body,
            "category": self.category,
            "transaction_amount": self.transaction_amount,
            "currency": self.currency,
            "status": self.status,
            "new_balance": self.new_balance,
            "fee": self.fee,
            "transaction_id": self.transaction_id,
            "recipient_name": self.recipient_name
        }