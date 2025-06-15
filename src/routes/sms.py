from flask import Blueprint, jsonify, request
from src.models.user import db # Import the shared db instance
from src.models.sms import Message, Sender, Recipient # Import our SMS models
from sqlalchemy import func, desc # For database functions like count, sum, and ordering
from datetime import datetime

# Create a Blueprint for SMS routes
sms_bp = Blueprint("sms_bp", __name__)

# --- API Endpoints will be defined below --- #

@sms_bp.route("/messages", methods=["GET"])
def get_messages():
    """API endpoint to get all messages with optional filtering"""
    # We will implement filtering and pagination later
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    category = request.args.get("category")
    search_term = request.args.get("search")

    query = Message.query

    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            query = query.filter(Message.timestamp >= start_date)
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD."}), 400
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            # To include the entire end day, we can filter up to the end of that day
            from datetime import timedelta
            end_date = end_date + timedelta(days=1) - timedelta(seconds=1)
            query = query.filter(Message.timestamp <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD."}), 400

    if category and category.lower() != "all categories":
        query = query.filter(Message.category == category)
    
    if search_term:
        query = query.filter(Message.message_body.ilike(f"%{search_term}%"))

    # Order by timestamp in descending order (newest first)
    query = query.order_by(desc(Message.timestamp))

    paginated_messages = query.paginate(page=page, per_page=per_page, error_out=False)
    messages_data = [msg.to_dict() for msg in paginated_messages.items]
    
    return jsonify({
        "messages": messages_data,
        "total_messages": paginated_messages.total,
        "total_pages": paginated_messages.pages,
        "current_page": paginated_messages.page
    })

@sms_bp.route("/statistics", methods=["GET"])
def get_statistics():
    """API endpoint to get overall SMS statistics"""
    total_messages = Message.query.count()
    
    # Calculate total transaction volume (sum of transaction_amount where it's not null)
    total_volume_query = db.session.query(func.sum(Message.transaction_amount)).filter(Message.transaction_amount != None)
    total_volume_result = total_volume_query.scalar() # scalar() returns the first element of the first result or None
    total_volume = total_volume_result if total_volume_result is not None else 0.0

    # Count only messages that represent a transaction (e.g., have a transaction_amount)
    total_transactions = Message.query.filter(Message.transaction_amount != None).count()
    
    avg_transaction = (total_volume / total_transactions) if total_transactions > 0 else 0
    
    return jsonify({
        "total_messages": total_messages,
        "total_transactions": total_transactions,
        "total_volume": total_volume,
        "avg_transaction": avg_transaction
    })

@sms_bp.route("/categories", methods=["GET"])
def get_categories():
    """API endpoint to get message counts per category"""
    category_counts = db.session.query(Message.category, func.count(Message.category)).group_by(Message.category).all()
    categories_data = {cat: count for cat, count in category_counts if cat}
    return jsonify(categories_data)

@sms_bp.route("/trends/daily", methods=["GET"])
def get_daily_trends():
    """API endpoint to get daily transaction trends (count of messages per day)"""
    # This query groups messages by date and counts them
    # Note: SQLite date functions might require specific handling for date extraction
    # For simplicity, we assume timestamp is stored as DateTime and can be truncated or grouped
    
    # Using func.date for SQLite to extract date part from datetime
    daily_counts = db.session.query(func.date(Message.timestamp).label("date"), func.count(Message.message_id).label("count")) \
                               .group_by(func.date(Message.timestamp)) \
                               .order_by(func.date(Message.timestamp)) \
                               .all()
    
    trends_data = {str(date_obj): count for date_obj, count in daily_counts}
    return jsonify(trends_data)

@sms_bp.route("/trends/volume/daily", methods=["GET"])
def get_daily_volume_trends():
    """API endpoint to get daily transaction volume trends"""
    daily_volume = db.session.query(
                            func.date(Message.timestamp).label("date"), 
                            func.sum(Message.transaction_amount).label("total_volume")
                        ) \
                        .filter(Message.transaction_amount != None) \
                        .group_by(func.date(Message.timestamp)) \
                        .order_by(func.date(Message.timestamp)) \
                        .all()
    
    volume_data = {str(date_obj): (volume if volume is not None else 0) for date_obj, volume in daily_volume}
    return jsonify(volume_data)

@sms_bp.route("/top/recipients", methods=["GET"])
def get_top_recipients():
    """API endpoint to get top recipients by transaction volume"""
    # This query groups by recipient_name and sums transaction_amount
    top_recipients_query = db.session.query(
                                Message.recipient_name, 
                                func.sum(Message.transaction_amount).label("total_spent")
                            ) \
                            .filter(Message.recipient_name != None, Message.transaction_amount != None) \
                            .group_by(Message.recipient_name) \
                            .order_by(desc("total_spent")) \
                            .limit(5) # Get top 5
    
    top_recipients_data = {name: (amount if amount is not None else 0) for name, amount in top_recipients_query.all()}
    return jsonify(top_recipients_data)

@sms_bp.route("/top/senders", methods=["GET"])
def get_top_senders():
    """API endpoint to get top senders by transaction volume (for incoming money)"""
    # This query groups by sender's name (if available, otherwise phone) and sums transaction_amount for 'Incoming Money'
    # For simplicity, we'll assume recipient_name in Message can also be used for sender name in 'Incoming Money' context
    # or we can join with Sender table if sender names are populated there.
    # Here, we'll use recipient_name from the message body if it was extracted as the sender for incoming transactions.
    
    top_senders_query = db.session.query(
                                Message.recipient_name, # Assuming this field stores the sender's name for incoming money
                                func.sum(Message.transaction_amount).label("total_received")
                            ) \
                            .filter(Message.category == "Incoming Money", Message.recipient_name != None, Message.transaction_amount != None) \
                            .group_by(Message.recipient_name) \
                            .order_by(desc("total_received")) \
                            .limit(5) # Get top 5

    top_senders_data = {name: (amount if amount is not None else 0) for name, amount in top_senders_query.all()}
    return jsonify(top_senders_data)