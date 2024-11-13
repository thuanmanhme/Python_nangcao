import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql

# Bảng giá dựa trên sản phẩm 
price_table = {
    "Hoa": 2000,
    "Đường": 20000,
    "Gạo": 150000,
    "Nước mắm": 50000,
    "Nước tương": 15000
}

class EmployeeManagementSystem:
    def __init__(self):
        # Tạo cửa sổ đăng nhập
        self.root = tk.Tk()
        self.root.title("Đăng Nhập")
        
        # Kích thước cửa sổ
        window_width = 300
        window_height = 200
        
        # Lấy kích thước màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Tính toán tọa độ x và y để đặt cửa sổ ở trung tâm
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Đặt kích thước và vị trí cửa sổ
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # Trường nhập liệu cho tên đăng nhập và mật khẩu
        self.label_username = tk.Label(self.root, text="Tên đăng nhập:")
        self.label_username.pack()

        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack()

        self.label_password = tk.Label(self.root, text="Mật khẩu:")
        self.label_password.pack()

        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack()

        # Nút đăng nhập
        self.button_login = tk.Button(self.root, text="Đăng nhập", command=self.login)
        self.button_login.pack(pady=20)

        # Các thông tin kết nối cơ sở dữ liệu
        self.db_name = 'quanly'
        self.user = 'postgres'
        self.password = '123456'
        self.host = 'localhost'
        self.port = '5432'
        self.table_name = 'ktdonhang'

        # Chạy vòng lặp chính
        self.root.mainloop()

    def login(self):
        userid = self.entry_username.get()
        password = self.entry_password.get()

        # Kiểm tra thông tin đăng nhập
        if userid == self.db_name and password == self.password:
            # Kết nối đến cơ sở dữ liệu
            try:
                self.conn = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                self.cur = self.conn.cursor()
                messagebox.showinfo("Đăng nhập thành công", "Bạn đã kết nối với database")
                self.open_management_interface()  # Mở giao diện quản lý
            except Exception as e:
                messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        else:
            messagebox.showerror("Đăng nhập thất bại", "Mời bạn kiểm tra lại Tên đăng nhập và Mật Khẩu")

    def open_management_interface(self):
        self.root.destroy()  # Đóng cửa sổ đăng nhập
        self.master = tk.Tk()
        self.master.title("Quản lý đơn hàng")

        # Tạo các tab
        self.tabs = ttk.Notebook(self.master)
        self.add_tab = tk.Frame(self.tabs)
        self.history_tab = tk.Frame(self.tabs)
        self.search_tab = tk.Frame(self.tabs)
        self.tabs.add(self.add_tab, text="Tạo đơn hàng")
        self.tabs.add(self.history_tab, text="Quản lý đơn hàng")
        self.tabs.add(self.search_tab, text="Tìm kiếm đơn hàng")
        self.tabs.pack(fill="both", expand=True)

        # Tạo các widget trong tab "Thêm đơn hàng"
        self.create_add_tab()

        # Tạo các widget trong tab "Lịch sử"
        self.create_history_tab()

        # Tạo các widget trong tab "Tìm kiếm"
        self.create_search_tab()

        self.order_list = []

        # Chạy vòng lặp chính cho giao diện quản lý
        self.master.mainloop()

    def create_add_tab(self):
        # Tạo các widget
        self.name_label = tk.Label(self.add_tab, text="Tên người mua:")
        self.name_entry = tk.Entry(self.add_tab)

        self.id_label = tk.Label(self.add_tab, text="Số điện thoại:")
        self.id_entry = tk.Entry(self.add_tab)

        self.product_label = tk.Label(self.add_tab, text="Sản phẩm:")
        self.product_combobox = ttk.Combobox(self.add_tab, values=list(price_table.keys()))

        self.quantity_label = tk.Label(self.add_tab, text="Số lượng:")
        self.quantity_entry = tk.Entry(self.add_tab)

        self.total_label = tk.Label(self.add_tab, text="Thành tiền:")
        self.total_label.config(font=("Arial", 12, "bold"))

        self.add_button = tk.Button(self.add_tab, text="Tạo đơn hàng", command=self.add_order)

        # Sắp xếp các widget
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.id_label.grid(row=1, column=0, padx=10, pady=10)
        self.id_entry.grid(row=1, column=1, padx=10, pady=10)

        self.product_label.grid(row=2, column=0, padx=10, pady=10)
        self.product_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.quantity_label.grid(row=3, column=0, padx=10, pady=10)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=10)

        self.total_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.add_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_order(self):
        name = self.name_entry.get()
        id = self.id_entry.get()
        product = self.product_combobox.get()
        quantity = int(self.quantity_entry.get())

        total = price_table[product] * quantity
        self.total_label.config(text=f"Thành tiền: {total:,.0f} VND")

        # Lưu thông tin đơn hàng vào danh sách
        self.order_list.append((name, id, product, quantity, total))

        # Cập nhật tab lịch sử
        self.update_history_tab()

    
        # Xóa dữ liệu sau khi thêm
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.product_combobox.set('')  # Reset combobox

    def create_history_tab(self):
        self.history_tree = ttk.Treeview(self.history_tab)
        self.history_tree["columns"] = ("Name", "ID", "Product", "Quantity", "Total")
        self.history_tree.column("Name", width=150)
        self.history_tree.column("ID", width=100)
        self.history_tree.column("Product", width=150)
        self.history_tree.column("Quantity", width=100)
        self.history_tree.column("Total", width=150)
        self.history_tree.heading("Name", text="Tên Khách hàng")
        self.history_tree.heading("ID", text="Số điện thoại")
        self.history_tree.heading("Product", text="Sản phẩm")
        self.history_tree.heading("Quantity", text="Số lượng")
        self.history_tree.heading("Total", text="Thành tiền")
        self.history_tree.pack(fill="both", expand=True)

        self.save_button = tk.Button(self.history_tab, text="Lưu vào cơ sở dữ liệu", command=self.save_orders)
        self.save_button.pack(padx=10, pady=10)
        
    def save_orders(self):
        for order in self.order_list:
            name, id, product, quantity, total = order
            try:
                insert_query = sql.SQL("INSERT INTO {} (khachhang, sdt, sanpham, soluong, thanhtien) VALUES (%s, %s, %s, %s, %s)".format(self.table_name))
                data_to_insert = (name, id, product, quantity, total)
                self.cur.execute(insert_query, data_to_insert)
                self.conn.commit()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu đơn hàng: {e}")
        messagebox.showinfo("Thành công", "Tất cả đơn hàng đã được lưu vào cơ sở dữ liệu.")

    def create_search_tab(self):
        self.search_label = tk.Label(self.search_tab, text="Nhập tên khách hàng:")
        self.search_entry = tk.Entry(self.search_tab)
        self.search_button = tk.Button(self.search_tab, text="Tìm kiếm", command=self.search_order)

        self.search_result_tree = ttk.Treeview(self.search_tab)
        self.search_result_tree["columns"] = ("Name", "ID", "Product", "Quantity", "Total")
        self.search_result_tree.column("Name", width=150)
        self.search_result_tree.column("ID", width=100)
        self.search_result_tree.column("Product", width=150)
        self.search_result_tree.column("Quantity", width=100)
        self.search_result_tree.column("Total", width=150)
        self.search_result_tree.heading("Name", text="Tên Khách hàng")
        self.search_result_tree.heading("ID", text="Số điện thoại")
        self.search_result_tree.heading("Product", text="Sản phẩm")
        self.search_result_tree.heading("Quantity", text="Số lượng")
        self.search_result_tree.heading("Total", text="Thành tiền")
        self.search_result_tree.pack(fill="both", expand=True)

        # Sắp xếp các widget
        self.search_label.pack(padx=10, pady=10)
        self.search_entry.pack(padx=10, pady=10)
        self.search_button.pack(padx=10, pady=10)

    def update_history_tab(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        for i, order in enumerate(self.order_list):
            self.history_tree.insert("", "end", text=str(i + 1), values=order)

    def search_order(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên khách hàng để tìm kiếm.")
            return

        try:
            select_query = sql.SQL("SELECT khachhang, sdt, sanpham, soluong, thanhtien FROM {} WHERE LOWER(khachhang) LIKE %s".format(self.table_name))
            self.cur.execute(select_query, ('%' + query + '%',))
            results = self.cur.fetchall()

            if not results:
                messagebox.showinfo("Kết quả", "Không tìm thấy đơn hàng nào.")
            
            self.update_search_results(results)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi tìm kiếm: {e}")

    def update_search_results(self, results):
        for item in self.search_result_tree.get_children():
            self.search_result_tree.delete(item)

        for i, order in enumerate(results):
            self.search_result_tree.insert("", "end", text=str(i + 1), values=order)
    
# Khởi tạo ứng dụng
if __name__ == "__main__":
    app = EmployeeManagementSystem()
