import xml.etree.ElementTree as ET
import re # We will use this for regular expressions later
from datetime import datetime # To convert timestamps
from src.models.user import db # To access the database instance
from src.models.sms import Message, Sender, Recipient # To interact with our database models

def parse_xml_and_populate_db(xml_file_path):
    """Parse XML file and populate database with SMS data"""
    print(f"Parsing XML file: {xml_file_path}")
    
    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot() # Get the root element (<smses>)
        
        messages_processed = 0
        
        # Iterate through each <sms> element
        for sms_element in root.findall("sms"):
            try:
                # Extract attributes
                address = sms_element.get("address", "")
                date_ms = int(sms_element.get("date", "0"))
                body = sms_element.get("body", "")
                
                # Convert timestamp from milliseconds to datetime object
                timestamp = datetime.fromtimestamp(date_ms / 1000.0)
                
                # Categorize and extract data
                category, transaction_data = categorize_and_extract(body)
                
                # Create or get sender
                sender = Sender.query.filter_by(phone_number=address).first()
                if not sender:
                    sender = Sender(phone_number=address)
                    db.session.add(sender)
                
                # Create or get recipient if phone number exists
                recipient = None
                if 'recipient_phone' in transaction_data:
                    recipient = Recipient.query.filter_by(phone_number=transaction_data['recipient_phone']).first()
                    if not recipient:
                        recipient = Recipient(
                            phone_number=transaction_data['recipient_phone'],
                            name=transaction_data.get('recipient_name')
                        )
                        db.session.add(recipient)
                
                # Create message
                message = Message(
                    sender=sender,
                    recipient=recipient,
                    timestamp=timestamp,
                    message_body=body,
                    category=category,
                    transaction_amount=transaction_data.get('amount'),
                    currency=transaction_data.get('currency'),
                    status='completed',  # Default status
                    new_balance=transaction_data.get('new_balance'),
                    fee=transaction_data.get('fee'),
                    transaction_id=transaction_data.get('transaction_id'),
                    recipient_name=transaction_data.get('recipient_name')
                )
                
                db.session.add(message)
                messages_processed += 1
                
                # Commit every 100 messages to avoid memory issues
                if messages_processed % 100 == 0:
                    db.session.commit()
                    print(f"Processed {messages_processed} messages...")
                
            except Exception as e:
                print(f"Error processing SMS: {e}")
                db.session.rollback()
                continue # Continue to the next SMS even if one fails
        
        # Final commit for remaining messages
        db.session.commit()
        print(f"Successfully processed and stored {messages_processed} messages in the database.")
        return messages_processed
        
    except Exception as e:
        print(f"Error parsing XML: {e}")
        db.session.rollback()
        return 0

def categorize_and_extract(message_body):
    """Categorize SMS message and extract transaction details"""
    body = message_body.lower() # Convert to lowercase for easier matching
    transaction_data = {} # Dictionary to store extracted details
    category = "Other" # Default category if no specific pattern matches

    # --- Extraction of Common Transaction Details ---

    # Extract transaction amount (e.g., "1,000 RWF", "5000RWF")
    # This regex looks for numbers (with optional commas and decimals) followed by "rwf"
    amount_match = re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)\s*rwf', message_body, re.IGNORECASE)
    if amount_match:
        amount_str = amount_match.group(1).replace(',', '') # Remove commas for conversion to float
        transaction_data['amount'] = float(amount_str)
        transaction_data['currency'] = 'RWF'

    # Extract new balance (e.g., "New balance: 10,000 RWF")
    balance_match = re.search(r'(?:new balance|balance)[:\s]*(\d+(?:,\d+)*(?:\.\d+)?)\s*rwf', message_body, re.IGNORECASE)
    if balance_match:
        balance_str = balance_match.group(1).replace(',', '')
        transaction_data['new_balance'] = float(balance_str)

    # Extract fee (e.g., "Fee: 50 RWF")
    fee_match = re.search(r'fee[:\s]*(\d+(?:,\d+)*(?:\.\d+)?)\s*rwf', message_body, re.IGNORECASE)
    if fee_match:
        fee_str = fee_match.group(1).replace(',', '')
        transaction_data['fee'] = float(fee_str)

    # Extract transaction ID (e.g., "TxID: 123456789")
    txid_match = re.search(r'(?:txid|transaction id)[:\s]*(\d+)', message_body, re.IGNORECASE)
    if txid_match:
        transaction_data['transaction_id'] = txid_match.group(1)

    # Extract recipient name (more complex, as it can appear in various contexts)
    name_patterns = [
        r'(?:to|from)\s+([A-Za-z\s]+?)(?:\s+\d+|\s+\(|$)',  # e.g., "to Jane Smith", "from John Doe"
        r">(?:payment|sent).*?to\s+([A-Za-z\s]+?)(?:\s+\d+|\s+has)",  # e.g., "payment to Jane Smith has been..."
        r"transferred to\s+([A-Za-z\s]+?)(?:\s+\(|$)"  # e.g., "transferred to John Doe (250...)"
    ]

    for pattern in name_patterns:
        name_match = re.search(pattern, message_body, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()
            # Basic validation to avoid capturing just numbers or very short strings
            if len(name) > 2 and not name.isdigit():
                transaction_data["recipient_name"] = name
                break

    # Extract recipient phone (looks for a Rwandan mobile number pattern: 250 followed by 9 digits)
    phone_match = re.search(r"\(?(250\d{9})\)?", message_body)
    if phone_match:
        transaction_data["recipient_phone"] = phone_match.group(1)

    # --- Categorization Logic ---
    # This is where we define rules to assign a category based on keywords in the message body.
    # The order of these `if/elif` statements matters! More specific rules should come before general ones.

    if "you have received" in body:
        category = "Incoming Money"
    elif "your payment" in body and "completed" in body:
        category = "Payments to Code Holders"
    elif "bank deposit" in body:
        category = "Bank Deposits"
    elif "transferred to" in body:
        category = "Transfers to Mobile Numbers"
    elif "withdrawn" in body:
        category = "Withdrawals from Agents"
    elif "airtime" in body:
        category = "Airtime Bill Payments"
    elif "cash power" in body:
        category = "Cash Power Bill Payments"
    elif "one-time password" in body or "otp" in body:
        category = "Transactions Initiated by Third Parties" # OTPs often indicate third-party service interaction
    elif "direct payment" in body:
        category = "Direct Payments"
    elif "bank transfer" in body:
        category = "Bank Transfers"
    elif "internet bundle" in body or "voice bundle" in body:
        category = "Internet and Voice Bundle Purchases"
    else:
        category = "Other" # Fallback category for messages that don't match any specific pattern

    return category, transaction_data