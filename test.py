#
# This .py file creates the gui for the database
# It calls functions from the bronze_db.py
#

import bronze_db
import time
from tkinter import StringVar, Tk, Toplevel, ttk
from tkinter import messagebox as msg
ACCESS = "reception"

def createWindow():
    """
    Function to create main window
    and set title and size
    :return main_window: a Tk object
    """
    main_window = Tk()
    main_window.geometry("1000x400")
    main_window.title('Contact List')
    return main_window


def create_search_win():
    """
    Function to create and display the widgets on the main_window
    it creates the frames, buttons, labels and treeview
    :return search_result: a treeview object
    """
    search_frame = ttk.LabelFrame(main_window)
    search_entry = ttk.Entry(search_frame,
                             textvariable=search_var)
    search_entry.pack()
    search_button = ttk.Button(search_frame,
                               text='SQLite3 general search',
                               command=lambda:create_search_result())
    mysqlsearch_button = ttk.Button(search_frame,
                               text='MySQL general search',
                               command=lambda: create_mysqlsearch_result())
    search_id_button = ttk.Button(search_frame,
                               text='SQLite3 index search',
                               command=lambda: create_searchindex_result())
    mysqlsearch_id_button = ttk.Button(search_frame,
                                    text='MySQL index search',
                                    command=lambda: create_mysqlindex_result())
    search_result_frame = ttk.LabelFrame(main_window)
    search_result_frame.pack(fill="none", expand=True)
    search_result = ttk.Treeview(search_result_frame,
                                 columns=['Name',
                                          'Mobile #',
                                          'Phone #',
                                          'Date of Birth',
                                          'Address']
                                 )
    search_result.heading('Name', text='Name')
    search_result.heading('Mobile #', text='Mobile #')
    search_result.heading('Phone #', text='Phone #')
    search_result.heading('Date of Birth', text='Date of Birth')
    search_result.heading('Address', text='Address')
    search_result['show'] = 'headings'
    search_result.pack()
    search_button.pack()
    mysqlsearch_button.pack()
    search_id_button.pack()
    mysqlsearch_id_button.pack()
    search_frame.pack(fill="none", expand=True)
    return search_result


def create_search_result():
    """
    Function clears the treeview children, call a
    bronze_db function to do a general search to sqlite3 records
    using the value of search_var and display the query time
    """
    search_result.delete(*search_result.get_children())
    start_search = time.clock()
    result = bronze_db.sqlite_search_data(search_var.get())
    end_search = time.clock()-start_search
    msg.showinfo('Search Complete', 'Total time to search DataBase is {} seconds'.format(end_search))
    show_result(result)


def create_mysqlsearch_result():
    """
        Function clears the treeview children, call a
        bronze_db function to do a general search to MySQL records
        using the value of search_var and display the query time
    """
    search_result.delete(*search_result.get_children())
    start_search = time.clock()
    result = bronze_db.mysql_search_data(search_var.get())
    end_search = time.clock()-start_search
    msg.showinfo('Search Complete', 'Total time to search DataBase is {} seconds'.format(end_search))
    show_result(result)


def create_mysqlindex_result():
    """
        Function clears the treeview children, call a
        bronze_db function to do a index search to sqlite3 records
        using the value of search_var and display the query time
    """
    search_result.delete(*search_result.get_children())
    start_search = time.clock()
    result = bronze_db.mysql_search_index(search_var.get())
    end_search = time.clock()-start_search
    msg.showinfo('Search Complete', 'Total time to search DataBase is {} seconds'.format(end_search))
    show_result(result)


def create_searchindex_result():
    """
        Function clears the treeview children, call a
        bronze_db function to do a index search to sqlite3 records
        using the value of search_var and display the query time
    """
    search_result.delete(*search_result.get_children())
    start_search = time.clock()
    result = bronze_db.sqlite_search_index(search_var.get())
    end_search = time.clock()-start_search
    msg.showinfo('Search Complete','Total time to search DataBase is {} seconds'.format(end_search))
    show_result(result)


def on_click():
    """
       Function assigned to the <Double-1> event for the treeview children
    """
    profile_window = Toplevel(main_window)
    profile_window.grab_set()
    profile_frame = ttk.LabelFrame(profile_window)
    profile_frame.pack()
    profile_selected = search_result.item(search_result.focus())
    widget=0
    label_counter = 0
    label={}
    profile_labels = ['Name',
               'Mobile #',
               'Phone #',
               'Date of Birth',
               'Address']
    for each in profile_selected['values']:
        label[widget]=ttk.Label(
            profile_frame,
            text=each)
        label[widget].grid(column=1,row=widget,sticky='W')
        label[label_counter] = ttk.Label(
            profile_frame,
            text=profile_labels[label_counter]+': ')
        label[label_counter].grid(column=0, row=label_counter,sticky='E')
        widget+=1
        label_counter+=1


def show_result(result):
    """
    function takes result iterate through the list and insert
    them to the treeview, then bind an "<Double-1>" on the treeview
    :param result: list of contact details

    """
    for each in result:
        search_result.insert('', 'end', values=each)
    search_result.bind("<Double-1>", lambda e: on_click())


# Function to initialize main_window, search_var and search_result.
# then call mainloop() on the main_window
if __name__ == '__main__':
    main_window = createWindow()
    search_var = StringVar(value='')
    search_result = create_search_win()
    main_window.mainloop()
