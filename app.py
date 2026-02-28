import streamlit as st
from google.cloud import firestore
import datetime
import pandas as pd

# --- DB CONNECTION ---
db = firestore.Client.from_service_account_json("serviceAccountKey.json")

# --- THE MENU (Centralized) ---
MENU = {
    "Classic Burger": {"price": 120, "category": "Food"},
    "Cheese Maggi": {"price": 50, "category": "Food"},
    "Cold Coffee": {"price": 40, "category": "Drinks"},
    "Iced Tea": {"price": 30, "category": "Drinks"}
}

def main():
    st.sidebar.title("🍱 K-Star Digital")
    app_mode = st.sidebar.selectbox("Select Interface", ["Student: Order Food", "Admin: Kitchen Dashboard", "Admin: Sales Analytics"])

    if app_mode == "Student: Order Food":
        student_interface()
    elif app_mode == "Admin: Kitchen Dashboard":
        admin_kitchen_view()
    else:
        sales_analytics()

# --- 1. THE MENU & ORDERING (Student Side) ---
def student_interface():
    st.title("🚀 Quick Order")
    
    # User ID Session State
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""

    user_id = st.text_input("Enter College ID to start:", value=st.session_state.user_id)
    if not user_id:
        st.info("Please enter your ID to see the menu.")
        return
    st.session_state.user_id = user_id

    # Display Menu in Columns
    cols = st.columns(2)
    for i, (item, info) in enumerate(MENU.items()):
        with cols[i % 2]:
            st.write(f"**{item}**")
            st.caption(f"Price: ₹{info['price']}")
            if st.button(f"Add {item}", key=f"btn_{item}"):
                # Place Order logic
                order_ref = db.collection("orders").add({
                    "student_id": user_id,
                    "item": item,
                    "status": "Placed", # Flow: Placed -> Cooking -> Ready -> Collected
                    "timestamp": datetime.datetime.now(),
                    "total": info['price']
                })
                st.toast(f"✅ {item} added to queue!", icon="🔥")

    # --- 2. THE PICKUP MSG (Student Status Area) ---
    st.divider()
    st.subheader("🔔 Order Status & Pickup")
    
    my_orders = db.collection("orders").where("student_id", "==", user_id).order_by("timestamp", direction="DESCENDING").limit(3).stream()
    
    for doc in my_orders:
        o = doc.to_dict()
        if o['status'] == "Ready":
            st.balloons() # Visual celebration for pickup!
            st.success(f"**ORDER READY!** Please pick up your {o['item']} at the counter.")
        elif o['status'] == "Cooking":
            st.warning(f"Chef is preparing your {o['item']}... 🍳")
        else:
            st.info(f"{o['item']} is in the queue.")

# --- 3. THE POPPING UP (Admin Side) ---
def admin_kitchen_view():
    st.title("👨‍🍳 Live Kitchen Queue")
    st.caption("New orders appear here automatically on refresh.")

    # Get active orders
    active_orders = db.collection("orders").where("status", "in", ["Placed", "Cooking", "Ready"]).order_by("timestamp").stream()
    
    for doc in active_orders:
        o = doc.to_dict()
        oid = doc.id
        
        # Color coding based on urgency
        color = "blue" if o['status'] == "Placed" else "orange" if o['status'] == "Cooking" else "green"
        
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f":{color}[**{o['item']}**] | ID: {o['student_id']}")
                st.caption(f"Ordered at: {o['timestamp'].strftime('%H:%M:%S')}")
            
            with col2:
                if o['status'] == "Placed":
                    if st.button("Start", key=f"start_{oid}"):
                        db.collection("orders").document(oid).update({"status": "Cooking"})
                        st.rerun()
                elif o['status'] == "Cooking":
                    if st.button("Ready", key=f"ready_{oid}"):
                        db.collection("orders").document(oid).update({"status": "Ready"})
                        st.rerun()
                elif o['status'] == "Ready":
                    if st.button("Picked Up", key=f"done_{oid}"):
                        db.collection("orders").document(oid).update({"status": "Collected"})
                        st.rerun()

# --- 4. SALES ANALYTICS (Management Side) ---
def sales_analytics():
    st.title("📊 K-Star Sales Overview")
    all_orders = list(db.collection("orders").stream())
    if all_orders:
        df = pd.DataFrame([o.to_dict() for o in all_orders])
        st.metric("Total Revenue", f"₹{df['total'].sum()}")
        st.subheader("Top Selling Items")
        st.bar_chart(df['item'].value_counts())
    else:
        st.write("No sales data yet.")

if __name__ == "__main__":
    main()