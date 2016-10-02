#!/usr/local/bin/python3
import tkinter
from tkinter import filedialog
import threading
from lal_modules import core

version = 'v2.1.1'
program_title = '台灣郵局存證信函產生器 ' + version
opened_filename = None

senders = []
senders_addr = []
receivers = []
receivers_addr = []
ccs = []
cc_addr = []

target_lists = {
    '寄件人': (senders, senders_addr),
    '收件人': (receivers, receivers_addr),
    '副本收件人': (ccs, cc_addr)
}

def start_working(sender_list, sender_addr_list,
                  receiver_list, receiver_addr_list,
                  cc_list, cc_addr_list, text, output):
    status_label.config(text='工作中...')
    change_widgets_state('disable')
    core.generate_text_and_letter(sender_list, sender_addr_list,
                                  receiver_list, receiver_addr_list,
                                  cc_list, cc_addr_list,
                                  text)
    core.merge_text_and_letter(output)
    core.clean_temp_files()
    change_widgets_state('normal')
    status_label.config(text='檔案已匯出至：' + output)

def change_widgets_state(mode):
    menubar.entryconfig('檔案', state=mode)
    btn_add_cc.config(state=mode)
    btn_add_recver.config(state=mode)
    btn_add_sender.config(state=mode)
    article_text.config(state=mode)

def open_old_file():
    global opened_filename
    temp = opened_filename
    opened_filename = tkinter.filedialog.askopenfilename(
                filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                title = "開啟舊檔")
    if not opened_filename:
        opened_filename = temp
        return
    content = core.read_main_article(opened_filename)
    if not content:
        status_label.config(text='讀檔錯誤。請開啟以 UTF-8 編碼的純文字檔案')
        return
    article_text.delete('1.0', 'end')
    article_text.insert('end', content)
    window.title(opened_filename + ' - ' + program_title)
    status_label.config(text='就緒')

def save_current_file():
    global opened_filename
    temp = opened_filename
    if opened_filename is None:
        opened_filename = tkinter.filedialog.asksaveasfilename(
                    filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                    title = "存檔")
    if not opened_filename:
        opened_filename = temp
        return
    window.title(opened_filename + ' - ' + program_title)
    current_text = article_text.get('1.0', 'end')
    with open(opened_filename, 'w', encoding='utf-8') as text_file:
        text_file.write(current_text)
    status_label.config(text='已存檔')

def save_to_new_file():
    global opened_filename
    temp = opened_filename
    opened_filename = tkinter.filedialog.asksaveasfilename(
                filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                title = "存檔")
    if not opened_filename:
        opened_filename = temp
        return
    window.title(opened_filename + ' - ' + program_title)
    current_text = article_text.get('1.0', 'end')
    with open(opened_filename, 'w', encoding='utf-8') as text_file:
        text_file.write(current_text)
    status_label.config(text='已存檔')

def export_to_pdf(sender_list, sender_addr_list,
                  receiver_list, receiver_addr_list,
                  cc_list, cc_addr_list):
    output_filename = tkinter.filedialog.asksaveasfilename(
                filetypes =(("PDF File", "*.pdf"),("All Files","*.*")),
                title = "匯出至PDF")
    if not output_filename:
        return
    text = article_text.get("1.0", 'end')
    threading.Thread(target=start_working,
                     args=(sender_list, sender_addr_list,
                           receiver_list, receiver_addr_list,
                           cc_list, cc_addr_list, text, output_filename)).start()

def dialog_add_info(genre):
    dialog = tkinter.Toplevel()
    dialog.title('新增' + genre + '資訊')
    frame = tkinter.Frame(dialog)
    name_label = tkinter.Label(frame, text='姓名：')
    addr_label = tkinter.Label(frame, text='地址：')
    name_label.grid(row=0, sticky='W')
    addr_label.grid(row=1, sticky='W')
    name_entry = tkinter.Entry(frame, width=40)
    addr_entry = tkinter.Entry(frame, width=40)
    name_entry.grid(row=0, column=1)
    addr_entry.grid(row=1, column=1)
    btn_ok = tkinter.Button(frame, text='OK',
                            command=lambda: fill_info(dialog, genre,
                                                      name_entry.get(),
                                                      addr_entry.get()))
    btn_ok.grid(row=2, columnspan=2)
    frame.pack()
    dialog.grab_set()
    dialog.resizable(width=False, height=False)

def fill_info(toplevel, genre, all_name, addr):
    names = all_name.split(' ')
    target_lists[genre][0].append([])
    for n in names:
        target_lists[genre][0][-1].append(n)
    target_lists[genre][1].append(addr)
    show_info(target_lists)
    toplevel.destroy()

def show_info(targets):
    info_text.config(state='normal')
    info_text.delete('1.0', 'end')
    for k in ['寄件人', '收件人', '副本收件人']:
        info_text.insert('end', k + '：\n')
        insert_all_info(info_text, targets[k][0], targets[k][1])
    info_text.config(state='disable')

def insert_all_info(text_widget, namelist, addrlist):
    max_count = max(len(namelist), len(addrlist))
    if max_count == 0:
        text_widget.insert('end', '\t\t姓名：\n')
        text_widget.insert('end', '\t\t詳細地址：\n')

    for i in range(max_count):
        all_name = ' '.join(namelist[i]) if i <= len(namelist)-1 else ''
        text_widget.insert('end', '\t\t姓名： ' + all_name + '\n')
        address = addrlist[i] if i <= len(addrlist)-1 else ''
        text_widget.insert('end', '\t\t詳細地址： ' + address + '\n')

window = tkinter.Tk()
window.title('台灣郵局存證信函產生器 ' + version)
window.geometry('600x700')

menubar = tkinter.Menu(window)
m_file = tkinter.Menu(menubar)
m_file.add_command(label='開啟舊檔', command=open_old_file)
m_file.add_separator()
m_file.add_command(label='存檔', command=save_current_file)
m_file.add_command(label='另存新檔...', command=save_to_new_file)
m_file.add_separator()
m_file.add_command(label='匯出成PDF...',
                   command=lambda: export_to_pdf(senders, senders_addr,
                                                 receivers, receivers_addr,
                                                 ccs, cc_addr))
m_file.add_separator()
m_file.add_command(label='關閉', command=window.quit)
menubar.add_cascade(label='檔案', menu=m_file)
window.config(menu=menubar)

mainframe = tkinter.Frame(window)

info_frame = tkinter.LabelFrame(mainframe, text='姓名與地址資訊')
info_text = tkinter.Text(info_frame, height=10, state='disable', font=('Arial', 14))
info_scroll = tkinter.Scrollbar(info_frame, orient='vertical',
                                command=info_text.yview)
info_text['yscrollcommand'] = info_scroll.set
show_info(target_lists)
info_scroll.pack(side='right', fill='y')
info_text.pack()
info_frame.pack()

button_frame = tkinter.Frame(mainframe)
btn_add_sender = tkinter.Button(button_frame, text='新增寄件人資訊...',
                                command=lambda: dialog_add_info('寄件人'))
btn_add_recver = tkinter.Button(button_frame, text='新增收件人資訊...',
                                command=lambda: dialog_add_info('收件人'))
btn_add_cc = tkinter.Button(button_frame, text='新增副本收件人資訊...',
                            command=lambda: dialog_add_info('副本收件人'))
btn_add_sender.grid(column=0, row=0, sticky='E')
btn_add_recver.grid(column=1, row=0, sticky='E')
btn_add_cc.grid(column=2, row=0, sticky='E')
button_frame.pack()

article_frame = tkinter.LabelFrame(mainframe, text='內文')
article_text = tkinter.Text(article_frame, font=('Arial', 14))
article_scroll = tkinter.Scrollbar(article_frame, orient='vertical',
                                  command=article_text.yview)
article_text['yscrollcommand'] = article_scroll.set
article_scroll.pack(side='right', fill='y')
article_text.pack(fill='both', expand='yes')
article_frame.pack(fill='both', expand='yes')

status_label = tkinter.Label(mainframe, text='就緒')
status_label.pack(side='right')

mainframe.pack(fill='both', expand='yes')
window.mainloop()
