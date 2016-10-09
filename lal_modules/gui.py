import tkinter
from tkinter import filedialog
import threading
from lal_modules import core

class GUI:
    """
    The GUI for generator.
    """
    def __init__(self):
        self.__init_var()
        self.root = tkinter.Tk()
        self.root.title(self.program_title)
        self.root.geometry('600x700')

        self.menubar = tkinter.Menu(self.root)
        self.m_file = tkinter.Menu(self.menubar)
        self.m_file.add_command(label='開啟舊檔', command=self.__open_old_file)
        self.m_file.add_separator()
        self.m_file.add_command(label='存檔', command=self.__save_current_file)
        self.m_file.add_command(label='另存新檔...',
                                command=self.__save_to_new_file)
        self.m_file.add_separator()
        self.m_file.add_command(label='匯出成PDF...',
                                command=self.__export_to_pdf)
        self.m_file.add_separator()
        self.m_file.add_command(label='關閉', command=self.root.quit)
        self.menubar.add_cascade(label='檔案', menu=self.m_file)
        self.root.config(menu=self.menubar)

        self.mainframe = tkinter.Frame(self.root)

        self.info_frame = tkinter.LabelFrame(self.mainframe,
                                             text='姓名與地址資訊')
        self.info_text = tkinter.Text(self.info_frame, height=10,
                                      state='disable', font=('Arial', 14))
        self.info_scroll = tkinter.Scrollbar(self.info_frame,
                                             orient='vertical',
                                             command=self.info_text.yview)
        self.info_text['yscrollcommand'] = self.info_scroll.set
        self.__show_info()
        self.info_scroll.pack(side='right', fill='y')
        self.info_text.pack()
        self.info_frame.pack()

        self.button_frame = tkinter.Frame(self.mainframe)
        self.btn_add_sender = tkinter.Button(self.button_frame,
                            text='新增寄件人資訊...',
                            command=lambda: self.__dialog_add_info('寄件人'))
        self.btn_add_recver = tkinter.Button(self.button_frame,
                            text='新增收件人資訊...',
                            command=lambda: self.__dialog_add_info('收件人'))
        self.btn_add_cc = tkinter.Button(self.button_frame,
                            text='新增副本收件人資訊...',
                            command=lambda: self.__dialog_add_info('副本收件人'))
        self.btn_add_sender.grid(column=0, row=0, sticky='E')
        self.btn_add_recver.grid(column=1, row=0, sticky='E')
        self.btn_add_cc.grid(column=2, row=0, sticky='E')
        self.button_frame.pack()

        self.article_frame = tkinter.LabelFrame(self.mainframe, text='內文')
        self.article_text = tkinter.Text(self.article_frame, font=('Arial', 14))
        self.article_scroll = tkinter.Scrollbar(self.article_frame,
                                 orient='vertical',
                                 command=self.article_text.yview)
        self.article_text['yscrollcommand'] = self.article_scroll.set
        self.article_scroll.pack(side='right', fill='y')
        self.article_text.pack(fill='both', expand='yes')
        self.article_frame.pack(fill='both', expand='yes')

        self.status_label = tkinter.Label(self.mainframe, text='就緒')
        self.status_label.pack(side='right')

        self.mainframe.pack(fill='both', expand='yes')

    def __init_var(self):
        self.program_title = '台灣郵局存證信函產生器 ' + core.VERSION
        self.opened_filename = None
        self.senders = []
        self.senders_addr = []
        self.receivers = []
        self.receivers_addr = []
        self.ccs = []
        self.cc_addr = []
        self.target = ['寄件人', '收件人', '副本收件人']
        self.target_lists = {
            self.target[0]: (self.senders, self.senders_addr),
            self.target[1]: (self.receivers, self.receivers_addr),
            self.target[2]: (self.ccs, self.cc_addr)
        }

    def __do_work(self, sender_list, sender_addr_list,
                      receiver_list, receiver_addr_list,
                      cc_list, cc_addr_list, text, output):
        self.status_label.config(text='工作中...')
        self.__change_widgets_state('disable')
        core.generate_text_and_letter(sender_list, sender_addr_list,
                                      receiver_list, receiver_addr_list,
                                      cc_list, cc_addr_list,
                                      text)
        core.merge_text_and_letter(output)
        core.clean_temp_files()
        self.__change_widgets_state('normal')
        self.status_label.config(text='檔案已匯出至：' + output)

    def __change_widgets_state(self, mode):
        self.menubar.entryconfig('檔案', state=mode)
        self.btn_add_cc.config(state=mode)
        self.btn_add_recver.config(state=mode)
        self.btn_add_sender.config(state=mode)
        self.article_text.config(state=mode)

    def __open_old_file(self):
        temp = self.opened_filename
        self.opened_filename = tkinter.filedialog.askopenfilename(
                    filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                    title = "開啟舊檔")
        if not self.opened_filename:
            self.opened_filename = temp
            return
        content = core.read_main_article(self.opened_filename)
        if not content:
            self.status_label.config(
                        text='讀檔錯誤。請開啟以 UTF-8 編碼的純文字檔案')
            return
        self.article_text.delete('1.0', 'end')
        self.article_text.insert('end', content)
        self.root.title(self.opened_filename + ' - ' + self.program_title)
        self.status_label.config(text='就緒')

    def __save_current_file(self):
        temp = self.opened_filename
        if self.opened_filename is None:
            self.opened_filename = tkinter.filedialog.asksaveasfilename(
                        filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                        title = "存檔")
        if not self.opened_filename:
            self.opened_filename = temp
            return
        self.__do_save()

    def __save_to_new_file(self):
        temp = self.opened_filename
        self.opened_filename = tkinter.filedialog.asksaveasfilename(
                    filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                    title = "存檔")
        if not self.opened_filename:
            self.opened_filename = temp
            return
        self.__do_save()

    def __do_save(self):
        self.root.title(self.opened_filename + ' - ' + self.program_title)
        current_text = self.article_text.get('1.0', 'end')
        with open(self.opened_filename, 'w', encoding='utf-8') as text_file:
            for k in self.target:
                text_file.write(k + '：\n')
                core.fill_name_address(self.target_lists[k][0],
                                       self.target_lists[k][1],
                                       self.__save_info_if_zero,
                                       self.__save_info_if_nonzero,
                                       **{'fd': text_file})
            text_file.write('########################################\n')
            text_file.write(current_text)
        self.status_label.config(text='已存檔')

    def __save_info_if_zero(self, **kwargs):
        kwargs['fd'].write('\t\t姓名：\n')
        kwargs['fd'].write('\t\t詳細地址：\n')

    def __save_info_if_nonzero(self, all_name, address, **kwargs):
        kwargs['fd'].write('\t\t姓名： ' + all_name + '\n')
        kwargs['fd'].write('\t\t詳細地址： ' + address + '\n')
        return kwargs

    def __export_to_pdf(self):
        self.output_filename = tkinter.filedialog.asksaveasfilename(
                    filetypes =(("PDF File", "*.pdf"),("All Files","*.*")),
                    title = "匯出至PDF")
        if not self.output_filename:
            return
        text = self.article_text.get("1.0", 'end')
        threading.Thread(target=self.__do_work,
                         args=(self.senders, self.senders_addr,
                               self.receivers, self.receivers_addr,
                               self.ccs, self.cc_addr,
                               text, self.output_filename)).start()

    def __dialog_add_info(self, genre):
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
                                command=lambda: self.__fill_info(dialog,
                                                          genre,
                                                          name_entry.get(),
                                                          addr_entry.get()))
        btn_ok.grid(row=2, columnspan=2)
        frame.pack()
        dialog.grab_set()
        dialog.resizable(width=False, height=False)

    def __fill_info(self, toplevel, genre, all_name, addr):
        names = all_name.split(' ')
        self.target_lists[genre][0].append([])
        for n in names:
            self.target_lists[genre][0][-1].append(n)
        self.target_lists[genre][1].append(addr)
        self.__show_info()
        toplevel.destroy()

    def __show_info(self):
        self.info_text.config(state='normal')
        self.info_text.delete('1.0', 'end')
        for k in self.target:
            self.info_text.insert('end', k + '：\n')
            core.fill_name_address(self.target_lists[k][0],
                                   self.target_lists[k][1],
                                   self.__insert_info_if_empty,
                                   self.__insert_info_if_nonempty)
        self.info_text.config(state='disable')

    def __insert_info_if_empty(self, **kwargs):
        self.info_text.insert('end', '\t\t姓名：\n')
        self.info_text.insert('end', '\t\t詳細地址：\n')

    def __insert_info_if_nonempty(self, all_name, address, **kwargs):
        self.info_text.insert('end', '\t\t姓名： ' + all_name + '\n')
        self.info_text.insert('end', '\t\t詳細地址： ' + address + '\n')
        return kwargs

    def mainloop(self):
        self.root.mainloop()
