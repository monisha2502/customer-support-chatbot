import streamlit as st
import re
import time


st.markdown("""
<style>
span {
    animation: fadeIn 0.3s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
button {
    border-radius: 10px;
}
button:hover {
    background-color: #ff4b4b !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_intent" not in st.session_state:
    st.session_state.last_intent = None
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

intents = {
    "track": ["where is my order", "track my order", "order status", "where is my delivery", "track delivery", "my order location", "my order is late", "order delay"],
    "refund": ["I want a refund", "refund my order", "how to get a refund", "refund process", "money back", "return my money", "order problem refund"],
    "cancel": ["cancel my order", "I want to cancel", "how to cancel", "cancel delivery", "stop my order", "change my mind cancel", "cancel request"],
    "greet": ["hello", "hi", "hey", "good morning", "good evening"],
    "refund_status": ["refund status", "where is my refund", "refund update", "refund progress", "refund timeline", "when will I get my refund", "refund ETA", "refund the cash", "refund the money", "refund the amount"],
    "thanks": ["thank you", "thanks", "appreciate it", "grateful"]
}

def detect_intent(user_input):
    all_phrases = []
    labels = []
    for intent, phrases in intents.items():
        for p in phrases:
            all_phrases.append(p)
            labels.append(intent)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(all_phrases + [user_input])
    similarity = cosine_similarity(vectors[-1], vectors[:-1])
    max_score = similarity.max()
    index = similarity.argmax()
    if max_score < 0.3:
        return "unknown"
    return labels[index]

# Order database
orders = {
    "101": {"status": "Out for delivery 🚚", "eta": "10 mins"},
    "102": {"status": "Preparing 🍳", "eta": "20 mins"},
    "103": {"status": "Delivered ✅", "eta": "Completed"}
}

# Bot logic
def get_response(user_input):
    user_input = user_input.lower()
    intent = detect_intent(user_input)
    st.session_state.last_intent = intent
    import re
    numbers = re.findall(r'\d+', user_input)
    if numbers:
        order_id = numbers[0]
        if order_id in orders:
            order = orders[order_id]
            if intent == "track":
                status = order["status"].lower()
                if "preparing" in status:
                    return f"🍳 Your order is being prepared. ETA: {order['eta']}"
                elif "out for delivery" in status:
                    return f"🚚 Your order is out for delivery. ETA: {order['eta']}"
                elif "delivered" in status:
                    return "✅ Your order has been delivered. Enjoy your meal!"
            elif intent == "refund":
                return f"💰 A refund for order {order_id} has been initiated. It will reflect in your account within 5-7 business days."
            elif intent == "refund_status":
                return f"💰 The refund for order {order_id} is currently being processed. It should be completed within 5-7 business days."
            elif intent == "cancel":
                return f"❌ Your order {order_id} has been cancelled. We hope to serve you again!"
        else:
            return "❌ Sorry, I couldn't find that order. Please check your order ID and try again."
    if intent == "greet":
        return "🤖 Hello! How can I assist you today? You can ask about your order, request a refund, or cancel an order."
    elif intent == "track":
        return "🤖 Please provide your order ID to track your order. For example, 'where is my order 101'."
    elif intent == "refund":
        return "🤖 To process a refund, please provide your order ID. For example, 'refund order 102'."
    elif intent == "cancel":
        return "🤖 To cancel your order, please provide your order ID. For example, 'cancel order 103'."
    elif intent == "thanks":
        return "🤖 You're welcome! If you have any more questions, feel free to ask."
        

st.set_page_config(page_title="Chat Bot", page_icon="💬")

st.title("💬 Customer Support Chat")
st.markdown("---")


st.subheader("Quick Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📦 Track Order"):
        st.session_state.messages.append(("user", "track order"))
        response = get_response("where is my order 101")
        st.session_state.messages.append(("bot", response))

with col2:
    if st.button("💰 Refund"):
        st.session_state.messages.append(("user", "refund"))
        response = get_response("refund")
        st.session_state.messages.append(("bot", response))

with col3:
    if st.button("❌ Cancel"):
        st.session_state.messages.append(("user", "cancel"))
        response = get_response("cancel")
        st.session_state.messages.append(("bot", response))
    

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if len(st.session_state.messages) == 0:
    st.session_state.messages.append(("bot", "🤖 Hello! Ask me about your order, refund or cancellation."))

# Input
user_input = st.chat_input(
    placeholder="Ask about your order, refund or cancellation. For example, 'Where is my order 101?'",
    key="input"
)

# When user sends message
if user_input:
    with st.spinner("Bot is typing..."):
        time.sleep(1)  # Simulate thinking time
        response = get_response(user_input)
    if response is None:
        response = "Something went wrong. Please try again."
    st.session_state.messages.append(("user", user_input))
    st.session_state.messages.append(("bot", response))



# Display messages as chat bubbles
for role, msg in st.session_state.messages:
    if role == "user":
        st.markdown(
            f"""
            <div style='text-align:right; margin: 8px 0;'>
                <span style='background:#ff4b4b; color:white;padding:10px 15px; border-radius:15px;
                display:inline-block; max-width:60%;'>
                    {msg}
                </span>
            </div>
            """,  
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='text-align:left; margin: 8px 0;'>
                <span style='background:#2c2f33; color:white;padding:10px 15px; border-radius:15px;
                display:inline-block; max-width:60%;'>
                    {msg}
                </span>
            </div>
            """,  
            unsafe_allow_html=True
        )


st.markdown(
    """
    <script>
    var chat = window.parent.document.querySelector('.main');
    chat.scrollTop = chat.scrollHeight;
    </script>
    """,
    unsafe_allow_html=True
)