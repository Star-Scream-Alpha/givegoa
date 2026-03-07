# 🍽️ K Star Canteen — Digital Ordering System

A web-based canteen ordering system built with **Streamlit** that allows students to browse menus, place orders, and track order status in real time — while giving admins full control over order management, menu configuration, and sales analytics.

---

## ✨ Features

### 👨‍🎓 Student Side
- **Login** using College ID (no password required)
- **Browse Menu** filtered by category (Snacks, Beverages, etc.)
- **Add to Cart** with quantity selection
- **Place Orders** and receive a unique order ID
- **Track Active Orders** with live status updates
- **Notifications** when your order is ready for pickup
- **Order History** with total spend summary

### 👨‍💼 Admin Side
- **Dashboard** with key metrics (revenue, pending/completed orders)
- **Order Management** — filter by status/date, update order status
- **Automatic Notifications** sent to students when orders are marked "Ready"
- **Menu Management** — add, edit, delete items and toggle availability
- **Analytics** — top-selling items, revenue, completion rate breakdown

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/kstar-canteen.git
cd kstar-canteen

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## 🔐 Default Credentials

| Role    | Username | Password  |
|---------|----------|-----------|
| Admin   | `admin`  | `admin123`|
| Student | Any College ID | *(no password)* |

---

## 📦 Dependencies

```
streamlit
pandas
```

Create a `requirements.txt`:
```
streamlit>=1.28.0
pandas>=2.0.0
```

---

## 📁 Project Structure

```
kstar-canteen/
│
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🛒 Order Flow

```
Student places order
        ↓
Admin sees order (Status: Placed)
        ↓
Admin updates → Preparing
        ↓
Admin updates → Ready  ← 🔔 Student gets notified
        ↓
Student picks up → Admin marks Completed
```

---

## 🍽️ Default Menu

| Item              | Category   | Price  |
|-------------------|------------|--------|
| Maggi             | Snacks     | ₹40    |
| Veg Sandwich      | Snacks     | ₹50    |
| Cheese Sandwich   | Snacks     | ₹60    |
| Pav Bhaji         | Snacks     | ₹60    |
| Misal Pav         | Snacks     | ₹50    |
| Vada Pav          | Snacks     | ₹25    |
| Samosa (2pc)      | Snacks     | ₹30    |
| Coffee            | Beverages  | ₹20    |
| Tea               | Beverages  | ₹15    |
| Lemon Tea         | Beverages  | ₹15    |
| Cold Coffee       | Beverages  | ₹40    |
| Parle-G Biscuit   | Snacks     | ₹10    |

---

## ⚠️ Notes

- All data is stored in **Streamlit session state** — it resets on page refresh. For persistent storage, integrate a database (SQLite, PostgreSQL, etc.).
- This project is intended as a **demo/prototype** for college canteen digitization.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)
