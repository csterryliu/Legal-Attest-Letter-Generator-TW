#!/usr/local/bin/python3
import tkinter
from lal_modules import core

version = 'v2.1.1'

def export_to_pdf():
    senders = []
    senders_addr = []
    receivers = []
    receivers_addr = []
    ccs = []
    cc_addr = []
    text = article_text.get("1.0", 'end')
    core.generate_text_and_letter(senders, senders_addr,
                                  receivers, receivers_addr,
                                  ccs, cc_addr,
                                  text)
    core.merge_text_and_letter('output.pdf')
    core.clean_temp_files()

def add_info(genre):
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
    btn_ok = tkinter.Button(frame, text='OK')
    btn_ok.grid(row=2, columnspan=2)
    frame.pack()
    dialog.grab_set()
    dialog.resizable(width=False, height=False)

window = tkinter.Tk()
window.title('台灣郵局存證信函產生器 ' + version)
window.geometry('600x600')

menubar = tkinter.Menu(window)
m_file = tkinter.Menu(menubar)
m_file.add_command(label='開啟舊檔', command=window.quit)
m_file.add_separator()
m_file.add_command(label='存檔', command=window.quit)
m_file.add_command(label='另存新檔...', command=window.quit)
m_file.add_separator()
m_file.add_command(label='匯出成PDF...', command=export_to_pdf)
m_file.add_separator()
m_file.add_command(label='關閉', command=window.quit)
menubar.add_cascade(label='檔案', menu=m_file)
window.config(menu=menubar)

mainframe = tkinter.Frame(window)

info_frame = tkinter.LabelFrame(mainframe, text='姓名與地址資訊')
info_text = tkinter.Text(info_frame, height=10)
info_scroll = tkinter.Scrollbar(info_frame, orient='vertical',
                                command=info_text.yview)
info_text['yscrollcommand'] = info_scroll.set
info_scroll.pack(side='right', fill='y')
info_text.pack()
info_frame.pack()
#info_text.config(state='disable')

button_frame = tkinter.Frame(mainframe)
btn_add_sender = tkinter.Button(button_frame, text='新增寄件人資訊...',
                                command=lambda: add_info('寄件人'))
btn_add_recver = tkinter.Button(button_frame, text='新增收件人資訊...',
                                command=lambda: add_info('收件人'))
btn_add_cc = tkinter.Button(button_frame, text='新增副本收件人資訊...',
                            command=lambda: add_info('副本收件人'))
btn_add_sender.grid(column=0, row=0, sticky='E')
btn_add_recver.grid(column=1, row=0, sticky='E')
btn_add_cc.grid(column=2, row=0, sticky='E')
button_frame.pack()

article_frame = tkinter.LabelFrame(mainframe, text='內文')
article_text = tkinter.Text(article_frame)
article_scroll = tkinter.Scrollbar(article_frame, orient='vertical',
                                  command=article_text.yview)
article_text['yscrollcommand'] = article_scroll.set
article_scroll.pack(side='right', fill='y')
article_text.pack(fill='both', expand='yes')
article_frame.pack(fill='both', expand='yes')

mainframe.pack(fill='both', expand='yes')
window.mainloop()
