from tkinter import StringVar, Tk, Toplevel, ttk, Menu
from tkinter import filedialog
from tkinter import messagebox as msg
import db_handlers

ACCESS = "reception"
ACTIVE_SCREEN = "search"

class App():

    def __init__(self):
        """
        create the main app
        and create menu bar based on the user access level
        """
        self.root = Tk()
        self.root.geometry("1280x720")
        self.root.title('MRFM')
        self.menu_bar = Menu(self.root)
        self.add_menu()
        self.root.config(menu=self.menu_bar)
        self.root.columnconfigure(0,weight=1)
        self.main_frame = ttk.LabelFrame(self.root)
        self.main_frame.columnconfigure(0,weight=1)
        self.main_frame.grid(row=0,column=0,sticky="NSEW")
        self.create_window()

    def add_menu(self):
        """
        function to create menu bar
        """
        #Default Menus
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Account")
        self.file_menu.add_command(label="Sign Out")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.patient_menu = Menu(self.menu_bar, tearoff=0)
        self.patient_menu.add_command(label="Patient Lookup")
        self.menu_bar.add_cascade(label="Patient", menu=self.patient_menu)
        #Access Specific Menu
        if ACCESS == "doctor":
            self.patient_menu.add_command(label="My Patients")
        elif ACCESS == "reception":
            self.patient_menu.add_command(label="Add Patient")

    def create_window(self):
        if ACTIVE_SCREEN == 'search':
            self.search_window()

    def search_window(self):
        self.search_var = StringVar(value='Type Search Here')
        self.search_label = ttk.Label(self.main_frame,
                                      text='Patient Lookup')
        self.search_label.config(font=("Arial", 24))
        self.search_label.grid(row=1, column=0)
        self.search_entry = ttk.Entry(self.main_frame,
                                 textvariable=self.search_var)
        self.search_entry.grid(row=2,column=0,pady=1,sticky="NS")
        self.search_butn = ttk.Button(self.main_frame,text='Go',command=lambda:create_mysqlsearch_result())
        self.search_butn.grid(row=3,column=0,sticky="NS",pady=10)
        self.search_result = ttk.Treeview(self.main_frame,
                                     columns=['Id',
                                              'Name',
                                              'Mobile #',
                                              'Phone #',
                                              'Date of Birth',
                                              'Address']
                                     )
        self.search_result.heading('Id', text='Id')
        self.search_result.heading('Name', text='Name')
        self.search_result.heading('Mobile #', text='Mobile #')
        self.search_result.heading('Phone #', text='Phone #')
        self.search_result.heading('Date of Birth', text='Date of Birth')
        self.search_result.heading('Address', text='Address')
        self.search_result['show'] = 'headings'
        self.search_result.grid(row=4,column=0,sticky='NSEW')

        def create_mysqlsearch_result():
            """
                Function clears the treeview children, call a
                bronze_db function to do a general search to MySQL records
                using the value of search_var and display the query time
            """
            self.search_result.delete(*self.search_result.get_children())
            result = db_handlers.mysql_search_data(self.search_var.get())
            show_result(result)

        def show_result(result):
            """
            function takes result iterate through the list and insert
            them to the treeview, then bind an "<Double-1>" on the treeview
            :param result: list of contact details

            """
            for each in result:
                self.search_result.insert('', 'end', values=each)
            self.search_result.bind("<Double-1>", lambda e: self.on_click())

    def on_click(self):
        """
           Function assigned to the <Double-1> event for the treeview children
        """

        self.profile_window = Toplevel(self.main_frame)
        self.profile_window.grab_set()
        self.profile_frame = ttk.LabelFrame(self.profile_window)
        self.profile_frame.grid(row=0)
        self.profile_selected = self.search_result.item(self.search_result.focus())
        widget = 0
        label_counter = 0
        label = {}
        self.profile_labels = ['Id',
                          'Name',
                          'Mobile #',
                          'Phone #',
                          'Date of Birth',
                          'Address']

        for each in self.profile_selected['values']:
            label[widget] = ttk.Label(
                self.profile_frame,
                text=each)
            label[widget].grid(column=1, row=widget, sticky='W')
            label[label_counter] = ttk.Label(
                self.profile_frame,
                text=self.profile_labels[label_counter] + ': ')
            label[label_counter].grid(column=0, row=label_counter, sticky='E')
            widget += 1
            label_counter += 1
        self.file_list = ttk.Treeview(self.profile_window,
                                      columns=['Document ID',
                                               'Document']
                                      )
        self.file_list.heading('Document ID', text='Document ID')
        self.file_list.heading('Document', text='Document')
        self.file_list['show'] = 'headings'
        self.file_list.grid(row=1)
        self.profile_add_btn = ttk.Button(self.profile_frame,text='Add Document',command=lambda:self.open_file())
        self.profile_add_btn.grid(column=0)
        self.profile_add_btn = ttk.Button(self.profile_frame, text='Upload Document', command=lambda: self.ul_file())
        self.profile_add_btn.grid(column=0)
        self.profile_dl_btn = ttk.Button(self.profile_window, text='View Documents', command=lambda: self.view_file())
        self.profile_dl_btn.grid(row=2)
        self.profile_view_btn = ttk.Button(self.profile_window, text='Download Document', command=lambda: self.dl_file())
        self.profile_view_btn.grid(row=3)

    def open_file(self):
        """
        create a filedialog box that would allow us to choose our file
        """
        self.file_name = filedialog.askopenfilename(filetypes = [("All files", "*.*")])
        self.file_label = ttk.Label(self.profile_frame,text=self.file_name)
        self.file_label.grid(row=6,column=1)

    def dl_file(self):
        """
        download the selected file on the file_list
        """
        cur_item = self.file_list.focus()
        cur_id = self.file_list.item(cur_item)
        doc = db_handlers.get_document(cur_id['values'][0])
        with open('MedicalDocument.jpg','wb') as f:
            f.write(doc)

    def view_file(self):

        def pull_document():
            """
                Function clears the treeview children, call a
                bronze_db function to do a general search to MySQL records
                using the value of search_var and display the query time
            """
            self.file_list.delete(*self.file_list.get_children())
            result = db_handlers.search_documents(self.profile_selected['values'][0])
            documents(result)

        def documents(result):
            """
            function takes result iterate through the list and insert
            them to the treeview, then bind an "<Double-1>" on the treeview
            :param result: list of contact details

            """
            for each in result:
                self.file_list.insert('', 'end', values=each)
            #self.file_list.bind("<Double-1>", lambda e: self.on_click())

        pull_document()

    def ul_file(self):
        """
        upload our file to the database and link it to the client
        """
        with open(self.file_name,'rb') as f:
            data = f.read()
        id = self.profile_selected['values'][0]
        name = self.file_name
        name = name.split('/')
        db_handlers.upload_document(id,data,name)

main = App()
main.root.mainloop()