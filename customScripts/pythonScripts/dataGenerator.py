import pandas as pd
import random as rd
import numpy as np
import faker
from datetime import datetime, timedelta

fake = faker.Faker()

def valid_date_gen(date):
    while True:
        mod_date = datetime.today() - timedelta(days = rd.randint(0, 18*365))
        if mod_date > date:
            return mod_date

def unique_id_gen(prefix, id_list, n):
    while True:
        id = f"{prefix}_{rd.randint(1, n)}"
        if id in id_list:
            continue
        return id
        
def user_generator(n):
    def valid_phone_gen(phone_list):
        while True:
            phone = f'({rd.randint(0, 9)}{rd.randint(0, 9)}{rd.randint(0, 9)}) {rd.randint(0, 9)}{rd.randint(0, 9)}{rd.randint(0, 9)}-{rd.randint(0, 9)}{rd.randint(0, 9)}{rd.randint(0, 9)}{rd.randint(0, 9)}'
            if phone in phone_list:
                continue
            return phone
 
    gen_user_df = pd.DataFrame(columns = ["id", "name", "address", "phone", "join_date", "modified_date"])
    unique_id_set = set()
    while len(gen_user_df['id'])<n:
        row = []
        id = unique_id_gen('CUST', unique_id_set, n)
        unique_id_set.add(id)
        row.append(id)
        row.append(fake.name())
        row.append(fake.address().replace('\n', ' ').replace(',', ' '))
        row.append(valid_phone_gen(gen_user_df['phone']))
        join_date = datetime.today() - timedelta(days = rd.randint(0, 18*365))
        row.append(join_date)
        if fake.boolean(chance_of_getting_true = 30):
            row.append(valid_date_gen(join_date))
        else:
            row.append(row[4])
        gen_user_df.loc[(len(gen_user_df))] = row
    print("Users generated.")
    return gen_user_df

def category_item_generator():
    supermarket_categories = {
    "Fruits & Vegetables": [
        "Apple", "Banana", "Carrot", "Tomato", "Potato", "Onion", "Lettuce", "Spinach", "Strawberry", "Blueberry",
        "Pineapple", "Mango", "Grapes", "Avocado", "Cucumber", "Bell Pepper", "Watermelon", "Peach", "Cherry", "Broccoli",
        "Garlic", "Cauliflower", "Zucchini", "Brussels Sprouts", "Asparagus", "Celery", "Radish", "Pumpkin", "Papaya", "Pomegranate"
    ],
    "Dairy & Eggs": [
        "Milk", "Cheese", "Butter", "Yogurt", "Cream", "Eggs", "Cottage Cheese", "Sour Cream", "Ghee", "Greek Yogurt",
        "Mozzarella", "Cheddar", "Parmesan", "Almond Milk", "Soy Milk", "Coconut Milk", "Oat Milk", "Egg Whites",
        "Buttermilk", "Feta Cheese", "Swiss Cheese", "Ricotta", "Lactose-Free Milk", "Probiotic Yogurt", "Colby Jack Cheese",
        "Blue Cheese", "Whipping Cream", "Evaporated Milk", "Cream Cheese", "Halloumi"
    ],
    "Bakery": [
        "Bread", "Baguette", "Croissant", "Muffin", "Bagel", "Donut", "Brownie", "Cake", "Cupcake", "Pie",
        "Tart", "Scone", "Pita Bread", "Breadsticks", "Crackers", "Biscotti", "Danish Pastry", "Cinnamon Roll", "Focaccia",
        "Rye Bread", "Gluten-Free Bread", "Whole Wheat Bread", "Brioche", "English Muffin", "Pretzel", "Cornbread",
        "Eclair", "Shortbread", "Challah", "Puff Pastry"
    ],
    "Meat & Poultry": [
        "Chicken Breast", "Ground Beef", "Pork Chops", "Turkey", "Lamb Chops", "Sausages", "Bacon", "Steak",
        "Ham", "Duck", "Venison", "Quail", "Goat Meat", "Rabbit Meat", "Tilapia", "Tuna", "Cod", "Crab", "Lobster", "Halibut",
        "Trout", "Oysters", "Squid", "Clams", "Sardines", "Anchovies", "Mussels", "Octopus", "Salmon", "Shrimp"
    ],
    "Snacks": [
        "Potato Chips", "Nachos", "Pretzels", "Popcorn", "Trail Mix", "Granola Bars", "Peanut Butter Crackers",
        "Energy Bars", "Pita Chips", "Cheese Puffs", "Rice Cakes", "Beef Jerky", "Chocolate Chip Cookies",
        "Oreo", "Digestive Biscuits", "Salted Peanuts", "Dark Chocolate", "Milk Chocolate", "White Chocolate",
        "Wafer Cookies", "Nutella Breadsticks", "Gummy Bears", "Candy Bars", "Cotton Candy", "Marshmallows",
        "Roasted Almonds", "Crispy Seaweed", "Coconut Chips", "Banana Chips", "Caramel Popcorn"
    ],
    "Frozen Foods": [
        "Frozen Pizza", "Frozen Vegetables", "Ice Cream", "Frozen Chicken Nuggets", "Frozen French Fries",
        "Frozen Fish Fillets", "Frozen Mixed Berries", "Frozen Peas", "Frozen Dumplings", "Frozen Meatballs",
        "Frozen Pancakes", "Frozen Waffles", "Frozen Burritos", "Frozen Lasagna", "Frozen Spring Rolls", "Frozen Soup",
        "Frozen Tater Tots", "Frozen Yogurt", "Frozen Edamame", "Frozen Chicken Wings", "Frozen Hash Browns",
        "Frozen Cheesecake", "Frozen Pies", "Frozen Pasta", "Frozen Rice", "Frozen Bagels", "Frozen Garlic Bread",
        "Frozen Sausages", "Frozen Egg Rolls", "Frozen Smoothies"
    ],
    "Beverages": [
        "Coffee", "Tea", "Orange Juice", "Apple Juice", "Cola", "Lemonade", "Energy Drinks", "Sports Drinks",
        "Milkshakes", "Smoothies", "Ginger Ale", "Root Beer", "Coconut Water", "Flavored Water", "Hot Chocolate",
        "Sparkling Water", "Iced Coffee", "Iced Tea", "Vegetable Juice", "Herbal Tea", "Chai Tea", "Matcha",
        "Kombucha", "Wine", "Beer", "Whiskey", "Vodka", "Rum", "Gin", "Cocktail Mixers"
    ],
    "Electronics": [
        "Smartphone", "Tablet", "Smartwatch", "Wireless Earbuds", "Bluetooth Speaker", "Gaming Console",
        "4K TV", "Portable Charger", "VR Headset", "Router", "Digital Camera", "Fitness Tracker", "Headphones",
        "Electric Toothbrush", "Streaming Device", "Drone", "Smart Home Hub", "Dash Cam", "Projector",
        "Smart Light Bulb", "Smart Plug", "Robot Vacuum", "Sound System", "Smart Doorbell", "E-Reader",
        "Home Theater System", "Wireless Charger", "Smart Glasses", "Portable Bluetooth Radio", "Walkie Talkies"
    ],
    "Computer Hardware": [
        "CPU", "Motherboard", "RAM", "Graphics Card", "Power Supply", "Cooling Fan", "SSD", "HDD",
        "Mechanical Keyboard", "Wireless Mouse", "Webcam", "Monitor", "Ethernet Cable", "Router",
        "USB Hub", "Sound Card", "Laptop Stand", "Processor Cooler", "Gaming Controller",
        "HDMI Cable", "NVMe SSD", "External GPU", "UPS", "Network Switch", "Thunderbolt Dock",
        "Capture Card", "Mini PC", "VR Headset", "Mechanical Key Switches", "Gaming Mouse"
    ],
    "Kitchen Equipment": [
        "Blender", "Toaster", "Microwave", "Coffee Maker", "Rice Cooker", "Slow Cooker", "Air Fryer", "Pressure Cooker",
        "Electric Kettle", "Juicer", "Stand Mixer", "Hand Mixer", "Food Processor", "Ice Cream Maker", "Oven Thermometer",
        "Bread Maker", "Cast Iron Skillet", "Knife Set", "Cutting Board", "Colander", "Measuring Cups", "Rolling Pin",
        "Tongs", "Whisk", "Spatula", "Ladle", "Peeler", "Grater", "Can Opener", "Pizza Cutter"
    ],
    "Tools & Hardware": [
        "Hammer", "Screwdriver Set", "Wrench", "Drill", "Pliers", "Tape Measure", "Saw", "Level", "Socket Set",
        "Cordless Screwdriver", "Utility Knife", "Chisel Set", "Glue Gun", "Stud Finder", "Hex Keys", "Workbench",
        "Ladder", "Crowbar", "Nail Gun", "Voltage Tester", "Sander", "Workbench Vise", "Bolt Cutter", "Angle Grinder",
        "Hand Saw", "Clamps", "Wire Stripper", "Multimeter", "Workbench Light", "Workbench Stool"
    ],
    "Stationery Supplies": [
        "Notebook", "Pen", "Pencil", "Eraser", "Sharpener", "Highlighter", "Markers", "Glue Stick", "Stapler",
        "Tape Dispenser", "Post-it Notes", "Scissors", "Paper Clips", "Binder", "Calculator", "Ruler", "Compass",
        "Whiteboard Markers", "Fountain Pen", "Mechanical Pencil", "Sticky Notes", "Correction Tape", "Folders",
        "Laminator", "Printer Paper", "Envelopes", "Desk Organizer", "Clipboard", "Calligraphy Set", "Index Cards"
    ]
    }
    category_names = list(supermarket_categories.keys())
    category_df = pd.DataFrame(columns = ['id', 'category'])
    unique_id_set_categories = set()
    unique_id_set_items = set()
    while len(category_df['id']) < len(supermarket_categories.keys()):
        row = []
        id = unique_id_gen('CAT', unique_id_set_categories, 99)
        unique_id_set_categories.add(id)
        row.append(id)
        row.append(category_names[len(category_df['id'])])
        category_df.loc[len(category_df)] = row

    print("Categories generated.")

    item_df = pd.DataFrame(columns = ['id', 'category_id', 'item', 'brand', 'price_per_unit', 'created_at', 'modified_at'])

    for i in supermarket_categories.keys():
        brand_names = []
        while len(brand_names) <= rd.randint(3, 8):
            brand_names.append(f"{fake.last_name()}")
        cat_id = category_df.loc[category_df['category'] == i, 'id'].iloc[0]
        
        for j in supermarket_categories[i]:
            k = 0
            while k < rd.randint(0, len(brand_names) - 1):
                row = []
                id_item = unique_id_gen('ITEM',unique_id_set_items, 999)
                unique_id_set_items.add(id_item)
                row.append(id_item)
                row.append(cat_id)
                row.append(j)
                brand = brand_names[rd.randint(0, len(brand_names) - 1)]
                if (brand, j) in set(zip(item_df['brand'], item_df['item'])):
                    continue
                row.append(brand)
                row.append(rd.randint(1, 999))
                date = (datetime.today() - timedelta(days = rd.randint(0, 18*365)))
                row.append(date)
                if fake.boolean(chance_of_getting_true = 30):
                    row.append(valid_date_gen(date))
                else:
                    row.append(date)
                item_df.loc[len(item_df)] = row
                k += 1
        print("Items generated.")
    return category_df, item_df

def discount_generator(category_id_list, n):
    discount_df = pd.DataFrame(columns = ['discount_code', 'discount_percent', 'discount_type', 'category_id' ,'discount_limit', 'start_date', 'end_date'])
    discount_code_set = set()

    while len(discount_df['discount_code']) < n:
        row = []
        discount_perc = rd.choice(range(5, 50, 5))
        discount_code = f"{chr(rd.randint(65, 90))}{chr(rd.randint(65, 90))}{chr(rd.randint(65, 90))}{discount_perc}"
        if discount_code in discount_code_set:
            continue
        discount_code_set.add(discount_code)
        row.append(discount_code)
        row.append(discount_perc)
        if discount_perc >= 30:
            if fake.boolean(chance_of_getting_true = 15):
                row.append('Universal')
            else:
                row.append('Category-Specific')
        else:
            if fake.boolean(chance_of_getting_true = 35):
                row.append('Universal')
            else:
                row.append('Category-Specific')
        if row[2] == 'Category-Specific':
            row.append(category_id_list[rd.randint(0, len(category_id_list) - 1)])
        else:
            row.append(np.nan)
        if fake.boolean(chance_of_getting_true = 60):
            row.append(rd.choice(range(10, 500, 5)))
        else:
            row.append(np.nan)
        date = (datetime.today() - timedelta(days = rd.randint(0, 18*365)))
        row.append(date)
        end_date = date + timedelta(days = 7*(rd.randint(1, 4)))
        row.append(end_date)

        discount_df.loc[len(discount_df)] = row
    print("Discounts generated.")
    return discount_df

def order_generator(user_df, discount_df, item_df, n):    
    order_df = pd.DataFrame(columns=['id','user_id', 'order_date', 'discount_code', 'final_amount', 'payment_method', 'payment_status'])
    order_details_df = pd.DataFrame(columns = ['id', 'order_id', 'item_id', 'quantity', 'discount_code'])

    unique_id_set_orders = set()
    unique_id_set_ord_det = set()
    while len(order_df)<n:
        row = []
        id = unique_id_gen('ORD', unique_id_set_orders, n)
        unique_id_set_orders.add(id)
        user_id = user_df['id'].loc[rd.randint(0, len(user_df['id']) - 1)]
        ord_date = (datetime.today() - timedelta(days = rd.randint(0, 18*365)))
        disc_code_df = discount_df.loc[
            (discount_df['discount_type'] == 'Universal') &
            (discount_df['start_date']<= ord_date) &
            (discount_df['end_date']>=ord_date), 
            ["discount_code", "discount_percent", "discount_limit"]
        ]
        universal_coupon_found = False
        if len(disc_code_df) != 0:
            disc_code = disc_code_df["discount_code"].tolist()[rd.randint(0, len(disc_code_df) - 1)]
            universal_coupon_found = True
        no_of_items = rd.randint(1, 50)
        coupon_count = 0
        i = 0
        total_amt = 0

        
        while i < no_of_items:
            row_ord = []
            id_od = unique_id_gen('ORDITM', unique_id_set_ord_det, n*50)
            unique_id_set_ord_det.add(id_od)
            row_ord.append(id_od)
            row_ord.append(id)
            row_ord.append(item_df['id'].loc[rd.randint(0, len(item_df['id']) - 1)])
            if row_ord[2] in order_details_df['item_id']:
                continue
            if fake.boolean(chance_of_getting_true = 60):
                row_ord.append(1)
            else:
                if fake.boolean(chance_of_getting_true = 60):
                    row_ord.append(rd.randint(2, 10))
                else:
                    row_ord.append(rd.randint(11, 30))
            price = item_df.loc[
                (item_df['id'] == row_ord[2]), 
                "price_per_unit"
            ].tolist()[0]
            price = price*row_ord[3]
            
            if universal_coupon_found == True or coupon_count == 2:
                row_ord.append(np.nan)
                total_amt = total_amt + price
                order_details_df.loc[len(order_details_df)] = row_ord
                i += 1
                break
                
            cat_id = item_df.loc[
            (item_df['id'] == row_ord[2]), 
            "category_id"
            ].tolist()[0]
            

            disc_code_df = discount_df.loc[
            (discount_df['discount_type'] == 'Category-Specific') &
            (discount_df['category_id'] == cat_id) & 
            (pd.to_datetime(discount_df['start_date'], format = "%d-%m-%Y")<= ord_date) &
            (pd.to_datetime(discount_df['end_date'], format= "%d-%m-%Y")>=ord_date), 
            ["discount_code", "discount_percent", "discount_limit"]
            ]
            
            discount = 0
            if len(disc_code_df) != 0:
                row_ord.append(disc_code_df["discount_code"].tolist()[0])
                discount = price*(disc_code_df["discount_percent"].tolist()[0]/100)
                if disc_code_df["discount_limit"].tolist()[0] != None and (discount>disc_code_df["discount_limit"].tolist()[0]):
                    discount = disc_code_df["discount_limit"].tolist()[0]
            else:
                row_ord.append(np.nan)
            total_amt = total_amt + (price - discount)
            order_details_df.loc[len(order_details_df)] = row_ord
            coupon_count += 1
            i += 1
        discount = 0
        if universal_coupon_found == True:
            discount = total_amt * (disc_code_df["discount_percent"].tolist()[0]/100)
            if disc_code_df["discount_limit"].tolist()[0] != None and (discount>disc_code_df["discount_limit"].tolist()[0] ):
                discount = disc_code_df["discount_limit"].tolist()[0]
        total_amt = total_amt - discount
        payment_method = rd.choice(['Cash', 'Credit Card', 'Online Wallet', 'Crypto Wallet'])
        if fake.boolean(chance_of_getting_true = 70):
            payment_status = 'Success'
        else:
            if fake.boolean(chance_of_getting_true = 80):
                payment_status = 'Pending'
            else: 
                payment_status = 'Failed'
        if universal_coupon_found == False:
            disc_code = None
        row = [id, user_id, ord_date, disc_code, total_amt, payment_method, payment_status]
        order_df.loc[len(order_df)] = row
        print(f"{len(order_df)} order(s) generated.")
    return order_df, order_details_df
        





