import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql

class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phần mềm tạo đơn hàng")

        # Database connection fields
        self.db_name = tk.StringVar(value='donhang')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='luutru')

        # Create the GUI elements
        self.create_widgets()
        
        self.connect_db()
    def create_widgets(self):
        # Order section
        order_frame = tk.Frame(self.root)
        order_frame.pack(pady=10)
        
    
        self.product_name = tk.StringVar()
        self.price = tk.DoubleVar()
        self.quantity = tk.IntVar()

        tk.Label(order_frame, text="Tên sản phẩm:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(order_frame, textvariable=self.product_name).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(order_frame, text="Đơn giá:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(order_frame, textvariable=self.price).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(order_frame, text="Số lượng:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(order_frame, textvariable=self.quantity).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(order_frame, text="Lập đơn hàng", command=self.create_order).grid(row=4, columnspan=2, pady=10)

       
        self.order_summary = tk.Text(self.root, height=10, width=50)
        self.order_summary.pack(pady=10)
        # Search section
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=10)

        self.search_product = tk.StringVar()
        tk.Label(search_frame, text="Tìm kiếm theo tên sản phẩm:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.search_product).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(search_frame, text="Tìm kiếm", command=self.search_order).grid(row=0, column=2, padx=5, pady=5)
    def search_order(self):
        product_name = self.search_product.get()
        if not product_name:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên sản phẩm để tìm kiếm.")
            return
        
        # Thực hiện truy vấn để tìm kiếm
        try:
            search_query = sql.SQL("SELECT * FROM {} WHERE tensp ILIKE %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(search_query, (f"%{product_name}%",))
            results = self.cur.fetchall()

            # Hiển thị kết quả tìm kiếm
            if results:
                self.order_summary.delete(1.0, tk.END)  # Xóa nội dung hiện tại
                for row in results:
                    self.order_summary.insert(tk.END, f"Sản phẩm: {self.product_name.get()}, Đơn giá: {self.price.get()}, Số lượng: {self.quantity.get()}\n")
            else:
                messagebox.showinfo("Kết quả", "Không tìm thấy đơn hàng nào với tên sản phẩm này.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching order: {e}")
    
    def connect_db(self):
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            
    def create_order(self):
        

        # Kiểm tra thông tin đầu vào
            self.product_name.get() and self.price.get() > 0 and self.quantity.get() > 0
            total_price = self.price.get() * self.quantity.get()
            order_info = f"Sản phẩm: {self.product_name.get()}, Đơn giá: {self.price.get()}, Số lượng: {self.quantity.get()}, Tổng giá: {total_price}\n"
            self.order_summary.insert(tk.END, order_info)

            # Chèn đơn hàng vào cơ sở dữ liệu
            try:
                insert_query = sql.SQL("INSERT INTO {} (tensp, dongia, soluong) VALUES (%s, %s, %s)").format(sql.Identifier(self.table_name.get()))
                data_to_insert = (self.product_name.get(), self.price.get(), self.quantity.get())
                self.cur.execute(insert_query, data_to_insert)
                self.conn.commit()
                messagebox.showinfo("Success", "Order inserted into the database successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error inserting order: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()