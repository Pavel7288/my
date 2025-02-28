import asyncio
import sqlite3
from datetime import datetime

pending_orders = []


class Dishes:
    def __init__(self, name, price, quantity=1):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f'{self.quantity} x {self.name} - {self.price}$ '


class Menu:
    def __init__(self):
        self.menu = []

    def add_to_menu(self, product):
        self.menu.append(product)

    def get_product(self, name):
        for item in self.menu:
            if item.name.lower() == name.lower():
                return item

    def remove_from_order(self, name):
        for dish in self.menu:
            if dish.name == name:
                self.menu.remove(dish)
                print(f' product that called {dish} was removed')
            else:
                print(f"product that called {dish} wasn't found")

    def __str__(self):
        return ''.join([str(product) for product in self.menu])


class Orders:
    def __init__(self, *, name_client):
        self.name_client = name_client
        self.list_of_orders = []
        self.ready = False

    def create_order(self, product, quantity=1):
        if product not in self.list_of_orders:
            product.quantity = quantity
            self.list_of_orders.append(product)
            print(f'{product} is added in order')
        else:
            product.quantity = quantity
            print(f'quantity {product.name} set to {product.quantity}')

    def full_cost_every_order(self):
        sum_of_cost_products = sum(product.price * product.quantity for product in self.list_of_orders)
        return sum_of_cost_products

    def add_to_database(self):
        products_in_order = ''.join([str(product) for product in self.list_of_orders])
        return products_in_order

    def __str__(self):
        products_in_order = ''.join([str(product) for product in self.list_of_orders])
        return f"{self.name_client} : {products_in_order}total_cost:{self.full_cost_every_order()}$, {self.ready}. "


class AllOrders:
    def __init__(self):
        self.current_all_orders = []

    def add(self, item):
        self.current_all_orders.append(item)

    def get_item_all_orders(self, name):
        for item in self.current_all_orders:
            if item.name_client.lower() == name.lower():
                return item

    async def changed_status_of_order(self, name, delay=20):
        if not name.ready:
            name.ready = True
            print(f'{name} is ready')
            await asyncio.sleep(delay)
            self.current_all_orders.remove(name)
            print(f'Order {name}- Was removed')
            await insert_order(customer_name=name.name_client, price=name.full_cost_every_order(),
                               products=name.add_to_database())
        else:
            print('That name was changed status')

    def empty_list(self):
        if not self.current_all_orders:
            return True

    def __str__(self):
        return ''.join([str(item) for item in self.current_all_orders])


def get_next_order_counter():
    current_date = datetime.now().strftime('%Y-%m-%d')
    with sqlite3.connect('/home/pavel/Documents/my_project.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM finished_orders WHERE DATE(datetime) = ?', (current_date,))
        count = cursor.fetchone()[0]
        return count + 1


async def insert_order(customer_name, price, products, order_counter=False, current_datetime=False):
    if not order_counter and not current_datetime:
        order_counter = get_next_order_counter()
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect("/home/pavel/Documents/my_project.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO finished_orders (datetime, order_counter, name_client, price, products)  
                    VALUES (?, ?, ?, ?, ?)
                """, (current_datetime, order_counter, customer_name, price, products))
            conn.commit()
            print(f'Order №{order_counter} added to database')
            return True

    except (sqlite3.OperationalError, sqlite3.DatabaseError) as e:
        print(f"⚠️ Ошибка при записи заказа {order_counter} : {e}")
        products_ = current_datetime, order_counter, customer_name, price, products
        if set(products_) not in pending_orders:
            pending_orders.append(set(products_))
            print(f"Order №{order_counter} added to bad database.")
        else:
            print('Order already exist in bad database')
        print(pending_orders)


async def retry_pending_orders(interval=5):
    """ Периодически повторяет попытки записи заказов из очереди в БД. """
    while True:
        if pending_orders:
            print(f"🔄 Повторная попытка отправки {len(pending_orders)} заказов...")
            for order in pending_orders.copy():
                success = await insert_order(*order)
                if success:
                    pending_orders.remove(order)
                    print('записан')
        await asyncio.sleep(interval)


coffe = Dishes(name='coffe', price=2)
milk = Dishes(name='milk', price=4)
donut = Dishes(name='donut', price=3)
menu = Menu()
menu.add_to_menu(donut)
menu.add_to_menu(milk)
menu.add_to_menu(coffe)
print(menu)

Masha = Orders(name_client='Masha')
Masha.create_order(coffe, 3)

print(Masha)
Natasha = Orders(name_client='Natasha')
Natasha.create_order(donut)
Natasha.create_order(milk)

all_orders = AllOrders()
all_orders.add(Masha)
all_orders.add(Natasha)
print(all_orders)


async def main():
    asyncio.create_task(retry_pending_orders())
    while True:
        command = await asyncio.to_thread(input, 'What you wish: ')
        if command == 'add order':
            name_visitor = await asyncio.to_thread(input, 'Enter client: ')
            print(f'Name of client is {name_visitor}')
            name_client_1 = Orders(name_client=name_visitor)
            while True:
                name_of_order = str(input('Enter name of order: '))
                if name_of_order == 'end':
                    break
                elif menu.get_product(name_of_order):
                    ordered_dish = menu.get_product(name_of_order)
                    while True:
                        try:
                            quantity_of_product = int(await asyncio.to_thread(input, 'enter quantity of product: '))
                            if isinstance(quantity_of_product, int) and quantity_of_product > 0:
                                print(f'quantity of product set {quantity_of_product}')
                                break
                        except ValueError:
                            quantity_of_product = 1
                            print('quantity of product set 1')
                            break
                    name_client_1.create_order(ordered_dish, quantity_of_product)
                    print(name_client_1)
                else:
                    print("That order doesn't exist")
            all_orders.add(name_client_1)
            print(f'Order - {name_client_1} Added')
            print(all_orders)
        elif command == 'ready':
            while True:
                print(all_orders)
                name_that_remove = await asyncio.to_thread(input, 'Enter name that need remove: ')
                item_that_remove = all_orders.get_item_all_orders(name_that_remove)
                if item_that_remove:
                    break
                else:
                    print("Order with name {name_that_remove} not found.")
            asyncio.create_task(all_orders.changed_status_of_order(item_that_remove))
            await asyncio.sleep(0)
            if not all_orders.empty_list():
                print(all_orders)
            else:
                print('List of order is empty')


if __name__ == '__main__':
    asyncio.run(main())
