import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# 数据库连接配置
db_config = {
    "server": "localhost",  # SQL Server 地址
    "database": "JD",  # 数据库名称
    "username": "SS",  # 数据库用户名
    "password": "888888",  # 数据库密码
}

# 连接数据库
def connect_to_db():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={db_config['server']};"
        f"DATABASE={db_config['database']};"
        f"UID={db_config['username']};"
        f"PWD={db_config['password']};"
    )
    return pyodbc.connect(conn_str)

# 加载数据
def load_data():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT FID, FBillNo, FEntryID, FSrcBillNo, FDemandBillNo, FDocumentStatus FROM PurchaseOrders")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except pyodbc.Error as e:
        messagebox.showerror("数据库错误", f"无法加载数据: {e}")
        return []

# 保存数据
def save_data(row_id, column, new_value):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        column_map = {
            0: "FID",
            1: "FBillNo",
            2: "FEntryID",
            3: "FSrcBillNo",
            4: "FDemandBillNo",
            5: "FDocumentStatus",
        }
        column_name = column_map[column]
        cursor.execute(f"UPDATE PurchaseOrders SET {column_name} = ? WHERE FEntryID = ?", (new_value, row_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("成功", "数据已保存")
    except pyodbc.Error as e:
        messagebox.showerror("数据库错误", f"无法保存数据: {e}")

# 创建主界面
def create_gui():
    root = tk.Tk()
    root.title("PurchaseOrders 数据编辑界面")
    root.geometry("800x400")

    # 表格
    tree = ttk.Treeview(root, columns=("FID", "FBillNo", "FEntryID", "FSrcBillNo", "FDemandBillNo", "FDocumentStatus"), show="headings")
    tree.heading("FID", text="FID")
    tree.heading("FBillNo", text="FBillNo")
    tree.heading("FEntryID", text="FEntryID")
    tree.heading("FSrcBillNo", text="FSrcBillNo")
    tree.heading("FDemandBillNo", text="FDemandBillNo")
    tree.heading("FDocumentStatus", text="FDocumentStatus")
    tree.pack(fill=tk.BOTH, expand=True)

    # 加载数据到表格
    def refresh_table():
        for row in tree.get_children():
            tree.delete(row)
        rows = load_data()
        for row in rows:
            tree.insert("", tk.END, values=row)

    refresh_table()

    # 双击单元格进行编辑
    def on_double_click(event):
        item = tree.selection()[0]
        values = tree.item(item, "values")
        column = tree.identify_column(event.x)
        column_index = int(column.replace("#", "")) - 1
        row_id = values[2]  # FEntryID 作为主键

        # 弹出编辑窗口
        def save_edit():
            new_value = entry.get()
            save_data(row_id, column_index, new_value)
            refresh_table()
            edit_window.destroy()

        edit_window = tk.Toplevel(root)
        edit_window.title("编辑数据")
        tk.Label(edit_window, text=f"编辑 {tree.heading(column)['text']}").pack(pady=10)
        entry = tk.Entry(edit_window)
        entry.insert(0, values[column_index])
        entry.pack(pady=10)
        tk.Button(edit_window, text="保存", command=save_edit).pack(pady=10)

    tree.bind("<Double-1>", on_double_click)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
