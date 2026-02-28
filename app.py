import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
from pathlib import Path


st.set_page_config(
    page_title="K Star Canteen - Digital Ordering System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF6B35;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .menu-item-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .status-placed {
        background-color: #FFF3CD;
        color: #856404;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .status-preparing {
        background-color: #D1ECF1;
        color: #0C5460;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .status-ready {
        background-color: #D4EDDA;
        color: #155724;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .status-completed {
        background-color: #E2E3E5;
        color: #383D41;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .cart-summary {
        position: sticky;
        top: 100px;
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    if 'orders' not in st.session_state:
        st.session_state.orders = []
    if 'menu' not in st.session_state:
        st.session_state.menu = get_initial_menu()
    if 'order_counter' not in st.session_state:
        st.session_state.order_counter = 1000
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []

def get_initial_menu():
    return [
        {"id": 1, "name": "Maggi", "price": 40, "category": "Snacks", "available": True, "emoji": "🍜"},
        {"id": 2, "name": "Veg Sandwich", "price": 50, "category": "Snacks", "available": True, "emoji": "🥪"},
        {"id": 3, "name": "Cheese Sandwich", "price": 60, "category": "Snacks", "available": True, "emoji": "🥪"},
        {"id": 4, "name": "Coffee", "price": 20, "category": "Beverages", "available": True, "emoji": "☕"},
        {"id": 5, "name": "Tea", "price": 15, "category": "Beverages", "available": True, "emoji": "🍵"},
        {"id": 6, "name": "Cold Coffee", "price": 40, "category": "Beverages", "available": True, "emoji": "🥤"},
        {"id": 7, "name": "Samosa (2pc)", "price": 30, "category": "Snacks", "available": True, "emoji": "🥟"},
        {"id": 8, "name": "Vada Pav", "price": 25, "category": "Snacks", "available": True, "emoji": "🍔"},
        {"id": 9, "name": "Parle-G Biscuit", "price": 10, "category": "Snacks", "available": True, "emoji": "🍪"},
        {"id": 10, "name": "Pav Bhaji", "price": 60, "category": "Snacks", "available": True, "emoji": "🍛"},
        {"id": 11, "name": "Misal Pav", "price": 50, "category": "Snacks", "available": True, "emoji": "🍲"},
        {"id": 12, "name": "Lemon Tea", "price": 15, "category": "Beverages", "available": True, "emoji": "🍋"},
    ]

def create_notification(user_id, order_id, title, message, notification_type):
    notification = {
        'id': len(st.session_state.notifications) + 1,
        'user_id': user_id,
        'order_id': order_id,
        'title': title,
        'message': message,
        'type': notification_type,
        'is_read': False,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.notifications.append(notification)

def get_user_notifications(user_id, unread_only=False):
    user_notifications = [
        notif for notif in st.session_state.notifications 
        if notif['user_id'] == user_id
    ]
    if unread_only:
        user_notifications = [n for n in user_notifications if not n['is_read']]
    return sorted(user_notifications, key=lambda x: x['timestamp'], reverse=True)

def mark_notification_as_read(notification_id):
    """Mark a notification as read"""
    for notif in st.session_state.notifications:
        if notif['id'] == notification_id:
            notif['is_read'] = True
            break

# Login Page
def show_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-header'>🍽️ K Star Canteen</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Digital Ordering System</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["👨‍🎓 Student Login", "👨‍💼 Admin Login"])
        
        with tab1:
            st.markdown("### Student Login")
            college_id = st.text_input("College ID", key="student_id", placeholder="Enter your college ID")
            
            if st.button("Login as Student", use_container_width=True, type="primary"):
                if college_id:
                    st.session_state.logged_in = True
                    st.session_state.user_type = "student"
                    st.session_state.user_id = college_id
                    st.rerun()
                else:
                    st.error("Please enter your College ID")
        
        with tab2:
            st.markdown("### Admin Login")
            admin_username = st.text_input("Username", key="admin_user", placeholder="admin")
            admin_password = st.text_input("Password", type="password", key="admin_pass", placeholder="admin123")
            
            if st.button("Login as Admin", use_container_width=True, type="primary"):
                if admin_username == "admin" and admin_password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.session_state.user_id = "admin"
                    st.rerun()
                else:
                    st.error("Invalid credentials! Use admin/admin123")
            
            st.info("Demo credentials: **admin** / **admin123**")

def show_student_dashboard():
    with st.sidebar:
        st.markdown(f"### 👨‍🎓 Welcome!")
        st.markdown(f"**College ID:** {st.session_state.user_id}")
        unread_notifications = get_user_notifications(st.session_state.user_id, unread_only=True)
        if unread_notifications:
            st.markdown(f"🔔 **{len(unread_notifications)} New Notification(s)**")
        
        st.divider()
        
        page = st.radio(
            "Navigation",
            ["🍽️ Menu", "🛒 Cart", "📦 My Orders", "🔔 Notifications", "📜 Order History"],
            label_visibility="collapsed"
        )
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_id = None
            st.session_state.cart = []
            st.rerun()
    
    # Main content
    if page == "🍽️ Menu":
        show_menu_page()
    elif page == "🛒 Cart":
        show_cart_page()
    elif page == "📦 My Orders":
        show_student_orders_page()
    elif page == "🔔 Notifications":
        show_notifications_page()
    elif page == "📜 Order History":
        show_order_history_page()

def show_menu_page():
    st.markdown("<h1 class='main-header'>🍽️ Menu</h1>", unsafe_allow_html=True)
    categories = ["All"] + list(set([item["category"] for item in st.session_state.menu]))
    selected_category = st.selectbox("Filter by Category", categories)
    filtered_menu = st.session_state.menu if selected_category == "All" else [
        item for item in st.session_state.menu if item["category"] == selected_category
    ]
    cols = st.columns(3)
    for idx, item in enumerate(filtered_menu):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"### {item['emoji']} {item['name']}")
                st.markdown(f"**₹{item['price']}** • {item['category']}")
                
                if item['available']:
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        quantity = st.number_input(
                            "Qty",
                            min_value=1,
                            max_value=10,
                            value=1,
                            key=f"qty_{item['id']}",
                            label_visibility="collapsed"
                        )
                    with col2:
                        if st.button("➕ Add", key=f"add_{item['id']}", use_container_width=True):
                            add_to_cart(item, quantity)
                            st.success("Added!")
                else:
                    st.error("Not Available")
                
                st.divider()

def add_to_cart(item, quantity):
    for cart_item in st.session_state.cart:
        if cart_item['id'] == item['id']:
            cart_item['quantity'] += quantity
            return
    st.session_state.cart.append({
        'id': item['id'],
        'name': item['name'],
        'price': item['price'],
        'quantity': quantity,
        'emoji': item['emoji']
    })

def show_cart_page():
    st.markdown("<h1 class='main-header'>🛒 Your Cart</h1>", unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("Your cart is empty! Add items from the menu.")
        if st.button("Go to Menu", type="primary"):
            st.rerun()
        return
    total = 0
    for idx, item in enumerate(st.session_state.cart):
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 1])
        
        with col1:
            st.markdown(f"## {item['emoji']}")
        with col2:
            st.markdown(f"**{item['name']}**")
        with col3:
            new_qty = st.number_input(
                "Quantity",
                min_value=1,
                max_value=10,
                value=item['quantity'],
                key=f"cart_qty_{idx}",
                label_visibility="collapsed"
            )
            if new_qty != item['quantity']:
                st.session_state.cart[idx]['quantity'] = new_qty
                st.rerun()
        with col4:
            item_total = item['price'] * item['quantity']
            st.markdown(f"**₹{item_total}**")
            total += item_total
        with col5:
            if st.button("🗑️", key=f"remove_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()
        
        st.divider()
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col2:
        st.markdown(f"### Total: ₹{total}")
    
    with col3:
        if st.button("🛍️ Place Order", type="primary", use_container_width=True):
            place_order(total)
            st.success("✅ Order placed successfully!")
            st.balloons()
            st.rerun()

def place_order(total):
    st.session_state.order_counter += 1
    order = {
        'order_id': st.session_state.order_counter,
        'user_id': st.session_state.user_id,
        'items': st.session_state.cart.copy(),
        'total': total,
        'status': 'Placed',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'date': datetime.now().strftime("%Y-%m-%d")
    }
    st.session_state.orders.append(order)
    st.session_state.cart = []

def show_student_orders_page():
    st.markdown("<h1 class='main-header'>📦 My Active Orders</h1>", unsafe_allow_html=True)
    user_orders = [
        order for order in st.session_state.orders 
        if order['user_id'] == st.session_state.user_id and order['status'] != 'Completed'
    ]
    
    if not user_orders:
        st.info("No active orders. Place an order from the menu!")
        return
    
    for order in sorted(user_orders, key=lambda x: x['timestamp'], reverse=True):
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"### Order #{order['order_id']}")
                st.markdown(f"**Time:** {order['timestamp']}")
            
            with col2:
                st.markdown(f"**Total:** ₹{order['total']}")
                st.markdown(f"**Items:** {len(order['items'])}")
            
            with col3:
                status_class = f"status-{order['status'].lower()}"
                st.markdown(f"<span class='{status_class}'>{order['status']}</span>", unsafe_allow_html=True)

            if order['status'] == 'Ready':
                st.success("🎉 **Your order is ready for pickup at the counter!**")
            
            with st.expander("View Items"):
                for item in order['items']:
                    st.markdown(f"- {item['emoji']} {item['name']} x {item['quantity']} = ₹{item['price'] * item['quantity']}")
            
            st.divider()

def show_notifications_page():
    st.markdown("<h1 class='main-header'>🔔 Notifications</h1>", unsafe_allow_html=True)
    
    notifications = get_user_notifications(st.session_state.user_id)
    
    if not notifications:
        st.info("No notifications yet. We'll notify you when your orders are ready!")
        return
    unread = [n for n in notifications if not n['is_read']]
    read = [n for n in notifications if n['is_read']]
    
    if unread:
        st.markdown("### 🔔 New Notifications")
        for notif in unread:
            with st.container():
                if notif['type'] == 'order_ready':
                    st.success(f"**{notif['title']}**")
                    st.markdown(f"📦 {notif['message']}")
                    st.markdown(f"*{notif['timestamp']}*")
                    
                    if st.button(f"Mark as Read", key=f"mark_read_{notif['id']}"):
                        mark_notification_as_read(notif['id'])
                        st.rerun()
                else:
                    st.info(f"**{notif['title']}**")
                    st.markdown(f"{notif['message']}")
                    st.markdown(f"*{notif['timestamp']}*")
                
                st.divider()
    
    if read:
        st.markdown("### 📋 Previous Notifications")
        for notif in read:
            with st.container():
                st.markdown(f"**{notif['title']}**")
                st.markdown(f"{notif['message']}")
                st.markdown(f"*{notif['timestamp']}*")
                st.divider()

def show_order_history_page():
    st.markdown("<h1 class='main-header'>📜 Order History</h1>", unsafe_allow_html=True)
    user_orders = [
        order for order in st.session_state.orders 
        if order['user_id'] == st.session_state.user_id
    ]
    
    if not user_orders:
        st.info("No order history yet.")
        return
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Orders", len(user_orders))
    with col2:
        total_spent = sum(order['total'] for order in user_orders)
        st.metric("Total Spent", f"₹{total_spent}")
    with col3:
        completed = sum(1 for order in user_orders if order['status'] == 'Completed')
        st.metric("Completed Orders", completed)
    
    st.divider()
    for order in sorted(user_orders, key=lambda x: x['timestamp'], reverse=True):
        with st.container():
            col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
            
            with col1:
                st.markdown(f"**#{order['order_id']}**")
            with col2:
                st.markdown(f"{order['timestamp']}")
            with col3:
                st.markdown(f"₹{order['total']}")
            with col4:
                status_class = f"status-{order['status'].lower()}"
                st.markdown(f"<span class='{status_class}'>{order['status']}</span>", unsafe_allow_html=True)
            
            with st.expander("View Details"):
                for item in order['items']:
                    st.markdown(f"- {item['emoji']} {item['name']} x {item['quantity']} = ₹{item['price'] * item['quantity']}")
            
            st.divider()

def show_admin_dashboard():
    with st.sidebar:
        st.markdown("### 👨‍💼 Admin Panel")
        st.markdown(f"**User:** {st.session_state.user_id}")
        st.divider()
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "📋 Orders", "🍽️ Menu Management", "📈 Analytics"],
            label_visibility="collapsed"
        )
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_id = None
            st.rerun()
    if page == "📊 Dashboard":
        show_admin_dashboard_page()
    elif page == "📋 Orders":
        show_admin_orders_page()
    elif page == "🍽️ Menu Management":
        show_menu_management_page()
    elif page == "📈 Analytics":
        show_analytics_page()

def show_admin_dashboard_page():
    st.markdown("<h1 class='main-header'>📊 Admin Dashboard</h1>", unsafe_allow_html=True)
    total_orders = len(st.session_state.orders)
    total_revenue = sum(order['total'] for order in st.session_state.orders)
    pending_orders = sum(1 for order in st.session_state.orders if order['status'] != 'Completed')
    completed_orders = sum(1 for order in st.session_state.orders if order['status'] == 'Completed')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", total_orders)
    with col2:
        st.metric("Total Revenue", f"₹{total_revenue}")
    with col3:
        st.metric("Pending Orders", pending_orders)
    with col4:
        st.metric("Completed Orders", completed_orders)
    
    st.divider()
    st.markdown("### 🔔 Recent Orders")
    recent_orders = sorted(st.session_state.orders, key=lambda x: x['timestamp'], reverse=True)[:5]
    
    if recent_orders:
        for order in recent_orders:
            col1, col2, col3, col4 = st.columns([1, 2, 1, 2])
            
            with col1:
                st.markdown(f"**#{order['order_id']}**")
            with col2:
                st.markdown(f"User: {order['user_id']}")
            with col3:
                st.markdown(f"₹{order['total']}")
            with col4:
                status_class = f"status-{order['status'].lower()}"
                st.markdown(f"<span class='{status_class}'>{order['status']}</span>", unsafe_allow_html=True)
            
            st.divider()
    else:
        st.info("No orders yet.")

def show_admin_orders_page():
    st.markdown("<h1 class='main-header'>📋 Order Management</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Placed", "Preparing", "Ready", "Completed"])
    with col2:
        date_filter = st.date_input("Filter by Date", value=None)
    filtered_orders = st.session_state.orders
    if status_filter != "All":
        filtered_orders = [order for order in filtered_orders if order['status'] == status_filter]
    if date_filter:
        date_str = date_filter.strftime("%Y-%m-%d")
        filtered_orders = [order for order in filtered_orders if order['date'] == date_str]
    
    st.divider()
    
    if not filtered_orders:
        st.info("No orders found.")
        return
    for order in sorted(filtered_orders, key=lambda x: x['timestamp'], reverse=True):
        with st.container():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"### Order #{order['order_id']}")
                st.markdown(f"**User ID:** {order['user_id']}")
                st.markdown(f"**Time:** {order['timestamp']}")
            
            with col2:
                st.markdown(f"**Total:** ₹{order['total']}")
                st.markdown(f"**Items:** {len(order['items'])}")
                with st.expander("View Items"):
                    for item in order['items']:
                        st.markdown(f"- {item['emoji']} {item['name']} x {item['quantity']} = ₹{item['price'] * item['quantity']}")
            
            with col3:
                current_status = order['status']
                status_options = ["Placed", "Preparing", "Ready", "Completed"]
                new_status = st.selectbox(
                    "Status",
                    status_options,
                    index=status_options.index(current_status),
                    key=f"status_{order['order_id']}"
                )
                
                if new_status != current_status:
                    for o in st.session_state.orders:
                        if o['order_id'] == order['order_id']:
                            o['status'] = new_status
                            if new_status == 'Ready':
                                create_notification(
                                    user_id=order['user_id'],
                                    order_id=order['order_id'],
                                    title="🎉 Order Ready for Pickup!",
                                    message=f"Your Order #{order['order_id']} is ready! Please collect it from the counter.",
                                    notification_type='order_ready'
                                )
                                st.success(f"✅ Order #{order['order_id']} marked as Ready! Student has been notified.")
                            else:
                                st.success(f"Status updated to {new_status}")
                            break
                    st.rerun()
            
            st.divider()

def show_menu_management_page():
    st.markdown("<h1 class='main-header'>🍽️ Menu Management</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Current Menu", "Add New Item"])
    
    with tab1:
        st.markdown("### Current Menu Items")
        
        for item in st.session_state.menu:
            col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 2, 2, 2])
            
            with col1:
                st.markdown(f"## {item['emoji']}")
            with col2:
                st.markdown(f"**{item['name']}**")
                st.markdown(f"*{item['category']}*")
            with col3:
                new_price = st.number_input(
                    "Price",
                    min_value=5,
                    max_value=500,
                    value=item['price'],
                    step=5,
                    key=f"price_{item['id']}",
                    label_visibility="collapsed"
                )
                if new_price != item['price']:
                    item['price'] = new_price
            with col4:
                available = st.checkbox(
                    "Available",
                    value=item['available'],
                    key=f"avail_{item['id']}"
                )
                if available != item['available']:
                    item['available'] = available
            with col5:
                if st.button("💾 Update", key=f"update_{item['id']}"):
                    st.success("Updated!")
            with col6:
                if st.button("🗑️ Delete", key=f"delete_{item['id']}"):
                    st.session_state.menu = [i for i in st.session_state.menu if i['id'] != item['id']]
                    st.rerun()
            
            st.divider()
    
    with tab2:
        st.markdown("### Add New Menu Item")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Item Name")
            new_price = st.number_input("Price (₹)", min_value=5, max_value=500, step=5)
            new_category = st.selectbox("Category", ["Snacks", "Beverages", "Main Course"])
        
        with col2:
            new_emoji = st.text_input("Emoji", value="🍽️")
            new_available = st.checkbox("Available", value=True)
        
        if st.button("➕ Add Item", type="primary"):
            if new_name and new_price > 0:
                new_id = max([item['id'] for item in st.session_state.menu]) + 1
                new_item = {
                    'id': new_id,
                    'name': new_name,
                    'price': new_price,
                    'category': new_category,
                    'available': new_available,
                    'emoji': new_emoji
                }
                st.session_state.menu.append(new_item)
                st.success(f"✅ {new_name} added successfully!")
                st.rerun()
            else:
                st.error("Please fill all required fields!")

def show_analytics_page():
    st.markdown("<h1 class='main-header'>📈 Analytics Dashboard</h1>", unsafe_allow_html=True)
    
    if not st.session_state.orders:
        st.info("No order data available yet.")
        return
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("From Date", value=None)
    with col2:
        end_date = st.date_input("To Date", value=None)
    
    st.divider()
    st.markdown("### 💰 Sales Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_orders = len(st.session_state.orders)
    total_revenue = sum(order['total'] for order in st.session_state.orders)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    with col1:
        st.metric("Total Orders", total_orders)
    with col2:
        st.metric("Total Revenue", f"₹{total_revenue}")
    with col3:
        st.metric("Average Order Value", f"₹{avg_order_value:.2f}")
    with col4:
        completed = sum(1 for order in st.session_state.orders if order['status'] == 'Completed')
        st.metric("Completion Rate", f"{(completed/total_orders*100):.1f}%" if total_orders > 0 else "0%")
    
    st.divider()
    st.markdown("### 🏆 Top Selling Items")
    
    item_sales = {}
    for order in st.session_state.orders:
        for item in order['items']:
            if item['name'] in item_sales:
                item_sales[item['name']]['quantity'] += item['quantity']
                item_sales[item['name']]['revenue'] += item['price'] * item['quantity']
            else:
                item_sales[item['name']] = {
                    'quantity': item['quantity'],
                    'revenue': item['price'] * item['quantity'],
                    'emoji': item['emoji']
                }
    
    sorted_items = sorted(item_sales.items(), key=lambda x: x[1]['quantity'], reverse=True)[:5]
    
    for idx, (name, data) in enumerate(sorted_items, 1):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        with col1:
            st.markdown(f"**#{idx}**")
        with col2:
            st.markdown(f"{data['emoji']} **{name}**")
        with col3:
            st.markdown(f"Quantity: **{data['quantity']}**")
        with col4:
            st.markdown(f"Revenue: **₹{data['revenue']}**")
    
    st.divider()
    st.markdown("### 📊 Order Status Breakdown")
    
    status_counts = {}
    for order in st.session_state.orders:
        status = order['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    col1, col2, col3, col4 = st.columns(4)
    statuses = ["Placed", "Preparing", "Ready", "Completed"]
    cols = [col1, col2, col3, col4]
    
    for status, col in zip(statuses, cols):
        with col:
            count = status_counts.get(status, 0)
            st.metric(status, count)
def main():
    init_session_state()
    
    if not st.session_state.logged_in:
        show_login()
    elif st.session_state.user_type == "student":
        show_student_dashboard()
    elif st.session_state.user_type == "admin":
        show_admin_dashboard()

if __name__ == "__main__":
    main()