#!/usr/local/bin/python3

import tkinter

version = 'v1.1.1'

window = tkinter.Tk()
window.title('台灣郵局存證信函產生器 ' + version)
window.geometry('600x600')

mainframe = tkinter.Frame(window)


menubar = tkinter.Menu(window)
m_file = tkinter.Menu(menubar)
m_file.add_command(label='關閉', command=window.quit)
menubar.add_cascade(label='檔案', menu=m_file)
window.config(menu=menubar)



info_frame = tkinter.LabelFrame(mainframe, text='姓名與地址資訊')
info_text = tkinter.Text(info_frame, height=10)
info_text.pack()
info_frame.pack()
#info_text.config(state='disable')


article_frame = tkinter.LabelFrame(mainframe, text='內文')
article_text = tkinter.Text(article_frame)
article_text.pack(fill='both', expand='yes')
article_frame.pack(fill='both', expand='yes')


mainframe.pack(fill='both', expand='yes')
window.mainloop()
