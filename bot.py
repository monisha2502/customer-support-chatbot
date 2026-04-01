orders = {
    "101": {"status": "Out for delivery", "eta": "10 mins"},
    "102": {"status": "Preparing", "eta": "20 mins"},
    "103": {"status": "Delivered", "eta": "Completed"}
}
def get_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input or "hi" in user_input:
        return "Hello! How can I assist you with your order today?"
    elif "order" in user_input and "where" in user_input:
        words = user_input.split()
        order_id = None
        for word in words:
            if word.isdigit():
                order_id = word
                break
        if order_id:
            if order_id in orders:
                order = orders[order_id]
                return f"Order Status: {order['status']}, ETA: {order['eta']}"
            else:
                return "Invalid order ID. Please check your order ID and try again."
        else:
            return "Please provide your order ID to check the status."
    elif "refund" in user_input:
        return "Your refund has been initiated."
    elif "cancel" in user_input:
        return "Your order has been successfully cancelled."
    elif "Thank" in user_input:
        return "You're welcome! If you have any more questions, feel free to ask."
    elif user_input.isdigit():
        if user_input in orders:
            order = orders[user_input]
            return f"Order Status: {order['status']}, ETA: {order['eta']}"
        else:
            return "Invalid order ID."
    else:
        return "I'm sorry, I did'nt understand that. Can you please rephrase your question or a specific query about your order?"
while True:
    user = input("You: ")
    print("Bot:", get_response(user))
