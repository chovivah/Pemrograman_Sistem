import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

def hubungkan_db():
    with sqlite3.connect('perpustakaan.db') as koneksi:
        cursor = koneksi.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS buku
                          (id INTEGER PRIMARY KEY, judul TEXT, penulis TEXT, tahun INTEGER, isbn TEXT)''')

def tambah_buku():
    try:
        with sqlite3.connect('perpustakaan.db') as koneksi:
            cursor = koneksi.cursor()
            cursor.execute("INSERT INTO buku (judul, penulis, tahun, isbn) VALUES (?, ?, ?, ?)",
                           (judul_var.get(), penulis_var.get(), int(tahun_var.get()), isbn_var.get()))
        muat_buku()
        bersihkan_field_buku()
    except ValueError:
        messagebox.showerror("Kesalahan", "Tahun harus berupa angka")
    except Exception as e:
        messagebox.showerror("Kesalahan", str(e))

def muat_buku():
    for i in pohon_buku.get_children():
        pohon_buku.delete(i)
    with sqlite3.connect('perpustakaan.db') as koneksi:
        cursor = koneksi.cursor()
        cursor.execute("SELECT * FROM buku")
        baris = cursor.fetchall()
    for row in baris:
        pohon_buku.insert("", END, values=row)

def hapus_buku():
    buku_terpilih = pohon_buku.selection()
    if buku_terpilih:
        id_buku = pohon_buku.item(buku_terpilih)['values'][0]
        with sqlite3.connect('perpustakaan.db') as koneksi:
            cursor = koneksi.cursor()
            cursor.execute("DELETE FROM buku WHERE id=?", (id_buku,))
        muat_buku()
    else:
        messagebox.showwarning("Peringatan", "Pilih buku untuk dihapus")

def edit_buku():
    buku_terpilih = pohon_buku.selection()
    if buku_terpilih:
        try:
            id_buku = pohon_buku.item(buku_terpilih)['values'][0]
            with sqlite3.connect('perpustakaan.db') as koneksi:
                cursor = koneksi.cursor()
                cursor.execute("UPDATE buku SET judul=?, penulis=?, tahun=?, isbn=? WHERE id=?",
                               (judul_var.get(), penulis_var.get(), int(tahun_var.get()), isbn_var.get(), id_buku))
            muat_buku()
            bersihkan_field_buku()
        except ValueError:
            messagebox.showerror("Kesalahan", "Tahun harus berupa angka")
        except Exception as e:
            messagebox.showerror("Kesalahan", str(e))
    else:
        messagebox.showwarning("Peringatan", "Pilih buku untuk diedit")

def isi_field_buku(event):
    buku_terpilih = pohon_buku.selection()
    if buku_terpilih:
        buku = pohon_buku.item(buku_terpilih)['values']
        judul_var.set(buku[1])
        penulis_var.set(buku[2])
        tahun_var.set(buku[3])
        isbn_var.set(buku[4])

def bersihkan_field_buku():
    judul_var.set("")
    penulis_var.set("")
    tahun_var.set("")
    isbn_var.set("")

root = Tk()
root.title("Daftar Buku")

judul_var = StringVar()
penulis_var = StringVar()
tahun_var = StringVar()
isbn_var = StringVar()

tabControl = ttk.Notebook(root)
tab_buku = ttk.Frame(tabControl)
tabControl.add(tab_buku, text='Buku')
tabControl.pack(expand=1, fill="both")

Label(tab_buku, text="Judul").grid(row=0, column=0, padx=10, pady=5)
Entry(tab_buku, textvariable=judul_var).grid(row=0, column=1, padx=10, pady=5)
Label(tab_buku, text="Penulis").grid(row=1, column=0, padx=10, pady=5)
Entry(tab_buku, textvariable=penulis_var).grid(row=1, column=1, padx=10, pady=5)
Label(tab_buku, text="Tahun").grid(row=2, column=0, padx=10, pady=5)
Entry(tab_buku, textvariable=tahun_var).grid(row=2, column=1, padx=10, pady=5)
Label(tab_buku, text="ISBN").grid(row=3, column=0, padx=10, pady=5)
Entry(tab_buku, textvariable=isbn_var).grid(row=3, column=1, padx=10, pady=5)

Button(tab_buku, text="Tambah Buku", command=tambah_buku).grid(row=4, column=0, padx=10, pady=5)
Button(tab_buku, text="Edit Buku", command=edit_buku).grid(row=4, column=1, padx=10, pady=5)
Button(tab_buku, text="Hapus Buku", command=hapus_buku).grid(row=4, column=2, padx=10, pady=5)

kolom_buku = ("ID", "Judul", "Penulis", "Tahun", "ISBN")
pohon_buku = ttk.Treeview(tab_buku, columns=kolom_buku, show='headings')
for kolom in kolom_buku:
    pohon_buku.heading(kolom, text=kolom)
pohon_buku.grid(row=5, column=0, columnspan=3, padx=10, pady=5)
pohon_buku.bind('<<TreeviewSelect>>', isi_field_buku)

hubungkan_db()
muat_buku()

root.mainloop()