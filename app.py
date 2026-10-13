from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'flavorhub_secret_key_change_me'

# In-memory storage (acting as our database for this frontend project)
MENU_ITEMS = [
    {
        "id": 1,
        "name": "Truffle Garlic Parmesan Fries",
        "category": "Appetizers",
        "price": 8.99,
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=600&q=80",
        "description": "Crispy golden fries tossed in truffle oil, garlic herbs, and freshly grated parmesan cheese.",
        "tags": ["Vegetarian", "Chef's Special"],
        "calories": "450 kcal"
    },
    {
        "id": 2,
        "name": "Crispy Buffalo Wings",
        "category": "Appetizers",
        "price": 12.99,
        "image": "https://images.unsplash.com/photo-1527477396000-e27163b481c2?auto=format&fit=crop&w=600&q=80",
        "description": "Jumbo wings tossed in signature spicy buffalo sauce, served with cool ranch and celery sticks.",
        "tags": ["Spicy", "Non-Vegetarian"],
        "calories": "680 kcal"
    },
    {
        "id": 3,
        "name": "Caprese Bruschetta",
        "category": "Appetizers",
        "price": 10.50,
        "image": "https://images.unsplash.com/photo-1572695157366-5e585ab2b69f?auto=format&fit=crop&w=600&q=80",
        "description": "Grilled artisan sourdough topped with heirloom tomatoes, fresh mozzarella, basil, and balsamic glaze.",
        "tags": ["Vegetarian"],
        "calories": "320 kcal"
    },
    {
        "id": 4,
        "name": "Creamy Wild Mushroom Soup",
        "category": "Soups & Salads",
        "price": 8.50,
        "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=600&q=80",
        "description": "Velvety soup crafted from wild mushrooms, roasted garlic, cream, and a hint of thyme.",
        "tags": ["Vegetarian", "Chef's Special"],
        "calories": "310 kcal"
    },
    {
        "id": 5,
        "name": "Crispy Caesar Salad",
        "category": "Soups & Salads",
        "price": 11.00,
        "image": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?auto=format&fit=crop&w=600&q=80",
        "description": "Crisp romaine hearts, garlic herb croutons, shaved parmesan, and creamy house-made Caesar dressing.",
        "tags": ["Vegetarian"],
        "calories": "380 kcal"
    },
    {
        "id": 6,
        "name": "Grilled Lemon Herb Salmon",
        "category": "Main Course",
        "price": 24.99,
        "image": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80",
        "description": "Fresh Atlantic salmon fillet grilled to perfection, served with asparagus and garlic butter sauce.",
        "tags": ["Gluten-Free", "Chef's Special"],
        "calories": "620 kcal"
    },
    {
        "id": 7,
        "name": "Tuscan Garlic Butter Ribeye",
        "category": "Main Course",
        "price": 32.99,
        "image": "https://images.unsplash.com/photo-1558030006-450675393462?auto=format&fit=crop&w=600&q=80",
        "description": "Prime cut ribeye steak cooked to preference, topped with sun-dried tomatoes, spinach, and garlic cream sauce.",
        "tags": ["Non-Vegetarian", "Chef's Special"],
        "calories": "890 kcal"
    },
    {
        "id": 8,
        "name": "Wood-Fired Margherita Pizza",
        "category": "Pizzas",
        "price": 15.99,
        "image": "https://images.unsplash.com/photo-1604382355076-af4b0eb60143?auto=format&fit=crop&w=600&q=80",
        "description": "San Marzano tomato sauce, fresh Fior di Latte mozzarella, fresh basil leaves, and extra virgin olive oil.",
        "tags": ["Vegetarian", "Chef's Special"],
        "calories": "780 kcal"
    },
    {
        "id": 9,
        "name": "Spicy Pepperoni Feast Pizza",
        "category": "Pizzas",
        "price": 18.50,
        "image": "https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=600&q=80",
        "description": "Loaded with double pepperoni, hot honey drizzle, chili flakes, and mozzarella cheese.",
        "tags": ["Spicy", "Non-Vegetarian"],
        "calories": "950 kcal"
    },
    {
        "id": 10,
        "name": "The Ultimate FlavorHub Burger",
        "category": "Burgers & Sandwiches",
        "price": 16.50,
        "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80",
        "description": "Double smashed beef patties, aged cheddar, caramelized onions, crispy bacon, and secret house sauce.",
        "tags": ["Non-Vegetarian", "Chef's Special"],
        "calories": "980 kcal"
    },
    {
        "id": 11,
        "name": "Classic New York Cheesecake",
        "category": "Desserts",
        "price": 9.00,
        "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=600&q=80",
        "description": "Rich and creamy classic cheesecake with a buttery graham cracker crust and fresh berry compote.",
        "tags": ["Vegetarian"],
        "calories": "520 kcal"
    },
    {
        "id": 12,
        "name": "Signature Iced Caramel Macchiato",
        "category": "Beverages",
        "price": 5.50,
        "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=600&q=80",
        "description": "Espresso poured over iced milk with vanilla syrup and a rich caramel drizzle.",
        "tags": ["Vegetarian", "Chef's Special"],
        "calories": "220 kcal"
    }
]

RESERVATIONS = []
ORDERS = []

@app.route('/')
def index():
    return render_template('index.html', menu_items=MENU_ITEMS)

@app.route('/api/reserve', methods=['POST'])
def make_reservation():
    data = request.json
    reservation = {
        "id": len(RESERVATIONS) + 1,
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "date": data.get("date"),
        "time": data.get("time"),
        "guests": data.get("guests"),
        "requests": data.get("requests", ""),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    RESERVATIONS.append(reservation)
    return jsonify({"success": True, "message": "Table reserved successfully!", "reservation_id": reservation["id"]})

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    order = {
        "id": f"FH-{len(ORDERS) + 1001}",
        "items": data.get("items"),
        "total": data.get("total"),
        "customer": data.get("customer"),
        "status": "Order Placed",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ORDERS.append(order)
    return jsonify({"success": True, "message": "Order placed successfully!", "order_id": order["id"]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)