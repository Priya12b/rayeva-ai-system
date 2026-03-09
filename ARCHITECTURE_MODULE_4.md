# Module 4: AI WhatsApp Support Bot
## Architecture & Implementation Guide

### Overview
The AI WhatsApp Support Bot provides automated customer support via WhatsApp, handling order queries, policy questions, and escalating issues intelligently. It maintains conversation context and logs all interactions.

### 1. Data Models

#### WhatsAppConversation Model
```python
# app/models/whatsapp_conversation.py
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, Enum
from datetime import datetime
from app.database import Base
import enum

class ConversationStatus(str, enum.Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    PENDING_RESPONSE = "pending_response"

class WhatsAppConversation(Base):
    __tablename__ = "whatsapp_conversations"

    id = Column(Integer, primary_key=True, index=True)
    
    # User identification
    whatsapp_phone = Column(String, unique=True, index=True)
    customer_id = Column(Integer, nullable=True, index=True)
    
    # Conversation management
    conversation_history = Column(JSON)  # List of messages
    status = Column(Enum(ConversationStatus), default=ConversationStatus.ACTIVE)
    
    # Context
    order_id = Column(Integer, nullable=True)
    query_type = Column(String)  # "order_status", "return_policy", "product_inquiry", etc.
    
    # AI decisions
    ai_response = Column(Text)
    confidence_score = Column(Float)  # 0-1, how confident is the AI response
    requires_human_review = Column(Bool, default=False)
    
    # Resolution
    resolved_by = Column(String)  # "ai" or agent name
    resolution_time = Column(Float, nullable=True)  # minutes
    customer_satisfaction = Column(Integer, nullable=True)  # 1-5 rating
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### WhatsAppTemplate Model
```python
class WhatsAppTemplate(Base):
    __tablename__ = "whatsapp_templates"
    
    id = Column(Integer, primary_key=True)
    template_key = Column(String, unique=True)  # "order_status", "refund_approved", etc.
    message_template = Column(Text)
    requires_approval = Column(Boolean)  # Is human approval needed?
    priority_level = Column(String)  # "routine", "urgent", "escalation"
```

### 2. AI Prompt Design

#### Query Classification Prompt
```
You are a WhatsApp customer support AI. Classify customer query and route appropriately.

CUSTOMER MESSAGE: {message}
ORDER CONTEXT: {order_data if available}

CLASSIFY AS:
1. ORDER_STATUS - "Where is my order?"
2. RETURN_REQUEST - "I want to return this"
3. REFUND_QUERY - "Where is my refund?"
4. PRODUCT_INFO - "Tell me about this product"
5. COMPLAINT - "The product is damaged"
6. ESCALATION_NEEDED - Complex or sensitive

Return JSON:
{
    "query_type": "ORDER_STATUS",
    "confidence": 0.95,
    "requires_human": false,
    "suggested_response": "Your order... expected delivery..."
}
```

#### Response Generation Prompt
```
You are a friendly, professional WhatsApp support agent for sustainable commerce.

CUSTOMER QUERY: {query}
ORDER INFO: {order_details}
POLICY: {return_policy}

RESPOND WITH:
- Empathy and clarity
- Specific order details when relevant
- Action items and timeline
- Escalation notice if needed

Keep response under 160 characters for SMS format.
Do not promise refunds without human approval.
```

### 3. API Endpoints

```python
# app/routers/whatsapp.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()

class WhatsAppMessage(BaseModel):
    phone_number: str
    message: str
    timestamp: datetime

@router.post("/webhook/whatsapp")
def receive_whatsapp_message(msg: WhatsAppMessage, db: Session = Depends(get_db)):
    """
    Webhook endpoint for incoming WhatsApp messages.
    (Integration with WhatsApp Business API)
    """
    # 1. Find or create conversation
    conversation = db.query(WhatsAppConversation).filter_by(
        whatsapp_phone=msg.phone_number
    ).first()
    
    if not conversation:
        conversation = WhatsAppConversation(whatsapp_phone=msg.phone_number)
        db.add(conversation)
        db.commit()
    
    # 2. Classify query
    query_type = classify_query(msg.message, conversation.order_id)
    
    # 3. Generate response
    response = generate_whatsapp_response(msg.message, conversation, db)
    
    # 4. Check if escalation needed
    if response.get("requires_escalation"):
        conversation.status = ConversationStatus.ESCALATED
        notify_support_team(conversation)
    
    # 5. Send response
    send_whatsapp_message(msg.phone_number, response.get("message"))
    
    # 6. Log interaction
    log_conversation(conversation, msg.message, response, db)
    
    return {"status": "received", "response_sent": True}

@router.get("/conversation/{phone_number}")
def get_conversation(phone_number: str, db: Session = Depends(get_db)):
    """Retrieve conversation history"""
    pass

@router.post("/conversation/{conversation_id}/escalate")
def escalate_to_human(conversation_id: int, db: Session = Depends(get_db)):
    """Manually escalate to support team"""
    pass

@router.post("/conversation/{conversation_id}/rate")
def rate_support(conversation_id: int, rating: int, db: Session = Depends(get_db)):
    """Customer satisfaction rating"""
    pass
```

### 4. Business Logic

#### Query Classification Engine
```python
# app/services/whatsapp_service.py

def classify_query(message: str, order_id: int = None) -> dict:
    """
    Classify WhatsApp query into categories for routing.
    
    Returns:
    {
        "query_type": "ORDER_STATUS",
        "confidence": 0.95,
        "requires_human": False,
        "keywords": ["order", "delivery", "track"]
    }
    """
    keywords_map = {
        "ORDER_STATUS": ["where", "order", "delivery", "track", "when", "arrived", "awaiting"],
        "RETURN_REQUEST": ["return", "send back", "refund", "change", "exchange"],
        "COMPLAINT": ["broken", "damaged", "defective", "wrong", "bad"],
        "PRODUCT_INFO": ["tell me", "about", "specs", "material", "eco"],
        "REFUND": ["refund", "money back", "reimbursement"],
    }
    
    message_lower = message.lower()
    
    # Find best matching category
    best_match = None
    best_score = 0
    
    for category, keywords in keywords_map.items():
        match_count = sum(1 for kw in keywords if kw in message_lower)
        score = match_count / len(keywords)
        if score > best_score:
            best_score = score
            best_match = category
    
    # High sensitivity for refund/return queries
    if best_score > 0.5:
        return {
            "query_type": best_match,
            "confidence": best_score,
            "requires_human": best_match in ["REFUND", "COMPLAINT"]
        }
    else:
        return {
            "query_type": "GENERAL_INQUIRY",
            "confidence": 0.5,
            "requires_human": True
        }

def generate_whatsapp_response(message: str, conversation: WhatsAppConversation, db: Session) -> dict:
    """Generate appropriate WhatsApp response"""
    
    # Get order info if exists
    order = None
    if conversation.order_id:
        order = db.query(Order).filter_by(id=conversation.order_id).first()
    
    query_type = conversation.query_type
    
    # Template-based responses
    if query_type == "ORDER_STATUS" and order:
        return {
            "message": f"Hi! Your order #{order.id} is {order.status}. "
                      f"Expected delivery: {order.expected_delivery}. "
                      f"Track here: {order.tracking_url}",
            "requires_escalation": False
        }
    
    elif query_type == "RETURN_REQUEST":
        return {
            "message": "Your return request noted. 🔄 Our team will review within 24 hours. "
                      "We offer free returns within 30 days. "
                      "Reply APPROVE to confirm or MODIFY for changes.",
            "requires_escalation": True
        }
    
    elif query_type == "REFUND":
        return {
            "message": "Refund requests are processed carefully. "
                      "An agent will contact you shortly to finalize. "
                      "Thank you for your patience!",
            "requires_escalation": True
        }
    
    else:
        return {
            "message": "Thanks for reaching out! Our support team will respond shortly. ⏱️",
            "requires_escalation": True
        }

def send_whatsapp_message(phone_number: str, message: str):
    """
    Send WhatsApp message via WhatsApp Business API.
    (Requires WhatsApp Business Account setup)
    """
    # Implementation with Twilio/Meta WhatsApp Business API
    pass
```

### 5. Integration Points

#### WhatsApp Business API Setup
```
1. Register Meta Business Account
2. Create WhatsApp Business App
3. Get webhook credentials
4. Configure webhook URL: https://your-api.com/ai/webhook/whatsapp
5. Verify phone numbers
```

#### Escalation Workflow
```
Customer Message
    ↓
Classification (AI)
    ↓
[High Confidence] → Template Response
    ↓
[Low Confidence/Sensitive] → Escalate to Human
    ↓
Database Log + Analytics
```

### 6. Key Features

✅ **Intelligent Query Classification**
- Order status tracking
- Return/refund policy guidance
- Immediate routing to human for sensitive issues

✅ **Context-Aware Responses**
- Access order history
- Personalized messaging
- Sustainability tips included in responses

✅ **Escalation Safeguards**
- High-confidence threshold
- Manual override capability
- All escalations logged

✅ **Analytics Dashboard**
- Response time tracking
- Customer satisfaction scoring
- Common query patterns

### 7. Testing Strategy

```python
# test_whatsapp_service.py
def test_order_status_classification():
    result = classify_query("Where is my order?")
    assert result["query_type"] == "ORDER_STATUS"
    assert result["confidence"] > 0.8

def test_refund_escalation():
    result = classify_query("I want a refund")
    assert result["requires_human"] == True

def test_response_generation():
    conversation = WhatsAppConversation(order_id=123)
    conversation.query_type = "ORDER_STATUS"
    response = generate_whatsapp_response("Where is my order?", conversation, db)
    assert "order" in response["message"].lower()
    assert "#123" in response["message"]
```

### 8. Future Enhancements

- [ ] Multi-language support
- [ ] Payment processing via WhatsApp
- [ ] Order tracking hyperlinks
- [ ] Image sharing (product photos)
- [ ] WhatsApp Business Catalog integration
- [ ] Callback scheduling
- [ ] Sentiment analysis for escalation
