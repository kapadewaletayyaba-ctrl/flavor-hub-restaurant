import streamlit as st
from datetime import datetime

# Page configuration
st.set_page_config(page_title="FlavorHub - Restaurant & Bar", page_icon="🍽️", layout="wide")

# Initialize Session State for Cart and Reservations
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'reservations' not in st.session_state:
    st.session_state.reservations = []

# Menu Data
MENU_ITEMS = [
    {
        "id": 1, "name": "Truffle Garlic Parmesan Fries", "category": "Appetizers", "price": 8.99,
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=600&q=80",
        "description": "Crispy golden fries tossed in truffle oil, garlic herbs, and freshly grated parmesan cheese.",
        "tags": ["Vegetarian", "Chef's Special"]
    },
    {
        "id": 2, "name": "Crispy Buffalo Wings", "category": "Appetizers", "price": 12.99,
        "image": "https://images.unsplash.com/photo-1527477396000-e27163b481c2?auto=format&fit=crop&w=600&q=80",
        "description": "Jumbo wings tossed in signature spicy buffalo sauce, served with cool ranch and celery sticks.",
        "tags": ["Spicy", "Non-Vegetarian"]
    },
    {
        "id": 3, "name": "Grilled Lemon Herb Salmon", "category": "Main Course", "price": 24.99,
        "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80",
        "description": "Fresh Atlantic salmon fillet grilled to perfection, served with asparagus and garlic butter sauce.",
        "tags": ["Gluten-Free", "Chef's Special"]
    },
    {
        "id": 4, "name": "Wood-Fired Margherita Pizza", "category": "Pizzas", "price": 15.99,
        "image": "https://images.unsplash.com/photo-1604382355076-af4b0eb60143?auto=format&fit=crop&w=600&q=80",
        "description": "San Marzano tomato sauce, fresh Fior di Latte mozzarella, fresh basil leaves, and olive oil.",
        "tags": ["Vegetarian", "Chef's Special"]
    },
    {
        "id": 5, "name": "The Ultimate FlavorHub Burger", "category": "Burgers & Sandwiches", "price": 16.50,
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        "description": "Double smashed beef patties, aged cheddar, caramelized onions, crispy bacon, and secret sauce.",
        "tags": ["Non-Vegetarian", "Chef's Special"]
    },
    {
        "id": 6, "name": "Classic New York Cheesecake", "category": "Desserts", "price": 9.00,
        "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=600&q=80",
        "description": "Rich and creamy classic cheesecake with a buttery graham cracker crust and berry compote.",
        "tags": ["Vegetarian"]
    }
]

# Sidebar Navigation
st.sidebar.title("🍽️ FlavorHub")
page = st.sidebar.radio("Navigate", ["Home & Menu", "Table Reservations", "View Cart"])

# Operating Hours Info
st.sidebar.markdown("---")
st.sidebar.markdown("### 🕒 Operating Hours")
st.sidebar.text("Mon - Thu: 11:00 AM - 10:00 PM\nFri - Sat: 11:00 AM - 11:00 PM\nSunday: 12:00 PM - 9:00 PM")

if page == "Home & Menu":
    st.title("Welcome to FlavorHub 🍔")
    st.write("Experience culinary excellence with our freshly prepared gourmet meals.")
    
    # Category Filter
    category = st.selectbox("Filter by Category", ["All", "Appetizers", "Main Course", "Pizzas", "Burgers & Sandwiches", "Desserts"])
    
    filtered_items = MENU_ITEMS if category == "All" else [item for item in MENU_ITEMS if item["category"] == category]
    
    # Display Menu Grid
    cols = st.columns(2)
    for idx, item in enumerate(filtered_items):
        with cols[idx % 2]:
            st.image(item["image"], use_container_width=True)
            st.subheader(item["name"])
            st.write(item["description"])
            st.markdown(f"**Price: ${item['price']:.2f}**")
            if st.button(f"Add to Cart", key=item["id"]):
                st.session_state.cart.append(item)
                st.success(f"Added {item['name']} to cart!")

elif page == "Table Reservations":
    st.title("📅 Book a Table")
    with st.form("reservation_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        date = st.date_input("Reservation Date")
        time = st.time_input("Reservation Time")
        guests = st.number_input("Number of Guests", min_value=1, max_value=12, value=2)
        
        submitted = st.form_submit_button("Confirm Reservation")
        if submitted:
            if name and email and phone:
                st.success(f"Thank you {name}! Your table for {guests} on {date} at {time} has been reserved.")
            else:
                st.error("Please fill in all required contact details.")

elif page == "View Cart":
    st.title("🛒 Your Order Cart")
    if not st.session_state.cart:
        st.info("Your cart is currently empty.")
    else:
        total = 0
        for i, cart_item in enumerate(st.session_state.cart):
            st.write(f"**{cart_item['name']}** - ${cart_item['price']:.2f}")
            total += cart_item['price']
            if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
        
        st.markdown(f"### Total: ${total:.2f}")
        if st.button("Proceed to Checkout"):
            st.success("Order placed successfully! Your food is being prepared.")
            st.session_state.cart = []
