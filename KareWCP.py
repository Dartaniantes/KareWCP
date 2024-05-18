import translator as tr
import os
from tkinter import *
import scrapper as sc
import admin as adm
import pyperclip as clip
import threading as thread



root = Tk()

icon = PhotoImage(file='static\\chair2-48.png')
root.iconbitmap('static\\chair2.ico')

root.title("Kare WCP")
w = 650
h = 500
x = root.winfo_screenwidth()
y = root.winfo_screenheight()

size = "{width}x{height}".format(width=w, height=h)

root.geometry(size)
root.resizable(height=False, width=False)


def on_close():
    if adm.driver is not None:
        adm.driver.quit()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)

id_frame = Frame(root)
id_frame.grid(column=0, row=0)

lbl = Label(id_frame, text="Введіть артикул товару:", font=("Arial", 14))
lbl.grid(column=0, row=0)

id_input = Entry(id_frame, width=10)
id_input.grid(column=1, row=0)

donorData = None


def disable_scrap():
    global scrap_btn
    scrap_btn.config(text='Завантаження...')
    scrap_btn['state'] = DISABLED


def enable_scrap():
    global scrap_btn
    scrap_btn.config(text='Отримати дані')
    scrap_btn['state'] = NORMAL


def getdata():
    info_en.config(state=NORMAL)
    if info_en.get(index1='1.0', index2=END).__str__() != '':
        info_en.delete(index1='1.0', index2=END)
    if info_ua.get(index1='1.0', index2=END).__str__() != '':
        info_ua.delete(index1='1.0', index2=END)
    if info_ru.get(index1='1.0', index2=END).__str__() != '':
        info_ru.delete(index1='1.0', index2=END)

    articul = id_input.get().__str__().strip()
    scrap(articul)
    copy_btn.grid(column=0, row=0, sticky='se')

    commit_btn['state'] = DISABLED
    commit_btn.config(text='Заванаження...')

    thread.Thread(target=get_product_enable_save_toggle_scrap, args=(articul,)).start()


def scrap(articul):
    info_en.insert(END, str(sc.get_info(articul)))
    info_en.config(state=DISABLED)
    rb_en.invoke()


def get_check_product(articul):
    adm.open_product(articul)


scrap_btn = Button(id_frame, text="Отримати дані", command=getdata)
scrap_btn.grid(column=2, row=0)
disable_scrap()


def admin_init_enable_scrap():
    adm.init()
    enable_scrap()


thread.Thread(target=admin_init_enable_scrap).start()


def set_lang():
    if lang.get() == 'en':
        info_ua.grid_forget()
        info_ru.grid_forget()
        info_en.grid(column=0, row=2)
        commit_btn.grid_forget()
        copy_btn.grid(column=0, row=0, sticky='se')
    else:
        info_en.grid_forget()
        copy_btn.grid_forget()
        commit_btn.grid(column=0, row=0, sticky='se')
        if lang.get() == 'ua':
            info_ru.grid_forget()
            info_ua.grid(column=0, row=2)
        elif lang.get() == 'ru':
            info_ua.grid_forget()
            info_ru.grid(column=0, row=2)


info_frame = Frame(root)
info_frame.grid(column=0, row=2)

lang = StringVar()
rb_frame = Frame(info_frame)
rb_frame.grid(column=0, row=0, pady=10)
rb_en = Radiobutton(rb_frame, text="Англійська", value='en', variable=lang, command=set_lang, font=("Arial", 10))
rb_en.grid(column=0, row=0)
rb_ua = Radiobutton(rb_frame, text="Українська", value='ua', variable=lang, command=set_lang, font=("Arial", 10))
rb_ua.grid(column=1, row=0)
rb_ru = Radiobutton(rb_frame, text="Російська", value='ru', variable=lang, command=set_lang, font=("Arial", 10))
rb_ru.grid(column=2, row=0)


info_en = Text(info_frame)
info_en.grid(column=0, row=1)
info_ua = Text(info_frame)
info_ru = Text(info_frame)


def copy_en():
    clip.copy(info_en.get('1.0', END).__str__())


def save():
    thread.Thread(target=save_product_disable_save_toggle_scrap, args=(info_ua.get('1.0', END).__str__(), info_ru.get('1.0', END).__str__())).start()
    #adm.commit_product(info_ua.get('1.0', END).__str__(), info_ru.get('1.0', END).__str__())


copy_btn = Button(info_frame, text="Копіювати", command=copy_en, font=("Arial", 10))

commit_btn = Button(info_frame, text="Зберегти товар", command=save, font=("Arial", 10))
commit_btn['state'] = DISABLED


def get_product_enable_save_toggle_scrap(articul):
    disable_scrap()
    adm.open_product(articul)
    enable_save()
    enable_scrap()


def save_product_disable_save_toggle_scrap(urk_text, rus_text):
    disable_scrap()
    disable_for_saving()
    adm.commit_product(urk_text, rus_text)
    commit_btn.config(text="Збережено")
    enable_scrap()


def enable_save():
    global commit_btn
    commit_btn.config(text='Зберегти товар')
    commit_btn['state'] = NORMAL


def disable_for_saving():
    global commit_btn
    commit_btn.config(text='Збереження...')
    commit_btn['state'] = DISABLED


root.mainloop()

