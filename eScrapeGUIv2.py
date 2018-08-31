"Dylan Murphy 08-06-18"
import csv
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import EPICscrape


class Contact():
    def __init__(self, BoroPres, BoroPresAdr, BoroPresEmail, CCouncil, CCouncilAdr, CBNumber, CBAdr, CBDistMan,
                 CBDistManEmail):
        self.BoroPres = BoroPres
        self.BoroPresAdr = None
        self.BoroPresEmail = None
        self.CCouncil = None
        self.CCouncilAdr = None
        self.CBNumber = None
        self.CBAdr = None
        self.CBDistMan = None
        self.CBDistManEmail = None

    def __setattr__(self, key, value):
        self.key = value
        return self.key


class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.master.title("EPICscrape")
        self.EPIC_data = None
        self.epic_street_address = None
        self.project_ids = None
        self.codify = None
        self.v = IntVar()
        self.usesameID = IntVar()

        Buttonstyle = ttk.Style()
        Buttonstyle.map('TButton',
                        background=[('disabled', '#d9d9d9'), ('active', '  #ececec')],
                        foreground=[('disabled', '#a3a3a3')],
                        relief=[('pressed', '!disabled', 'sunken')])
        LabelStyle = ttk.Style().configure("TLabel", background="light grey", padding=5, border="black")
        TopStyle = ttk.Style().configure("r.TFrame", background="light grey")
        MidStyle = ttk.Style().configure("b.TFrame", background="blue")
        BottomStyle = ttk.Style().configure("g.TFrame", background="white")
        checkstyle = ttk.Style().configure('lg.TCheckbutton', background="light grey", padding=5)

        TopFrame = ttk.Frame(master, borderwidth=2, style="r.TFrame")
        TopFrame.grid(row=0, column=0, rowspan=5, columnspan=4, sticky=W + E + N + S)
        vcp = (self.register(self.get_vcp), self, None)
        mid = (self.register(self.draw_midframe), self, None)
        s = (self.register(self.save), self)
        # Labels
        ttk.Label(TopFrame, text="Project Manager").grid(row=0, column=0, sticky=W + E + N + S)
        ttk.Label(TopFrame, text="Project Manager phone").grid(row=1, column=0, sticky=W + E + N + S)
        ttk.Label(TopFrame, text="Project Manager email").grid(row=2, column=0, sticky=W + E + N + S)
        ttk.Label(TopFrame, text="OER Project #").grid(row=4, column=0, sticky=W + N + E + S)

        # Entry Fields
        self.PM_name = Entry(TopFrame, width=50)
        self.PM_name.grid(row=0, column=1, columnspan=2, sticky=W + E)
        self.PM_phone = Entry(TopFrame, width=50)
        self.PM_phone.grid(row=1, column=1, columnspan=2, sticky=W + E)
        self.PM_email = Entry(TopFrame, width=50)
        self.PM_email.grid(row=2, column=1, columnspan=2, sticky=W + E)
        self.project = Entry(TopFrame, width=50)
        self.project.bind("<Return>", vcp)
        self.project.bind("<Shift Return>", mid)
        self.project.grid(row=4, column=1, columnspan=2, sticky=W + E + N + S)

        # try filling Entrys from stored info
        try:
            file = open("PM_contact.txt", 'r')
            user_em = file.readlines()
            file.close()
            memorized_auth = user_em
            self.PM_name.insert(0, memorized_auth[0])
            self.PM_phone.insert(0, memorized_auth[1])
            self.PM_email.insert(0, memorized_auth[2])
        except IOError:
            self.PM_name.insert(0, "Captain Planet")
            self.PM_phone.insert(0, "212-788-7527")
            self.PM_email.insert(0, "cplanet@nyc.oer.gov")

        # Remember Me box
        self.var1 = IntVar()
        chk = ttk.Checkbutton(TopFrame, text="Remember Me", variable=self.var1, style="lg.TCheckbutton")
        chk.grid(row=3, column=1, columnspan=3)

        self.Go = ttk.Button(TopFrame, text="Go", command=vcp)
        self.Go.grid(row=5, column=1, columnspan=2, sticky=W + E + N + S)

        GoFast = ttk.Checkbutton(TopFrame, text="Use this number in my recipients list", variable=self.usesameID,
                                 style="lg.TCheckbutton")
        GoFast.grid(row=5, column=0, sticky=W + E + N + S)

        last = 7
        ttk.Label(TopFrame, text="What would you like to do?").grid(row=last, column=0, columnspan=1,
                                                                    sticky=N + E + W + S)
        self.save_button = ttk.Button(TopFrame, text="save", command=s, state=DISABLED)
        self.save_button.grid(row=last, column=1, sticky=N + W + E + S)
        self.q = ttk.Button(TopFrame, text="quit", command=master.quit).grid(row=last, column=2, sticky=N + E + W + S)

    def draw_results(self, f):
        TopFrame.destroy()

        self.results = StringVar()
        BottomFrame = ttk.Frame(master, borderwidth=2, style="g.TFrame")
        BottomFrame.grid(row=5, column=0, rowspan=2, columnspan=4, sticky=N + S + E + W)
        results_label = ttk.Label(BottomFrame, text="Here are your results:")
        results_label.grid(row=0, column=0, sticky=N + E + W + S)

        self.res_print = ttk.Label(BottomFrame, textvariable=self.results, wraplength=300, justify=LEFT)
        self.res_print.grid(pady=5, row=1, column=0, columnspan=2, sticky=N + E + W + S)

    def checked(self):
        """opens the designated file and checks if the pm_name
        field has changed if it has it writes the current cred"""
        try:
            file = open('PM_contact.txt', 'r')
            data = file.readlines()
            file.close()
            if (self.PM_name.get(), self.PM_phone.get(), self.PM_email.get()) not in data:
                file = open("PM_contact.txt", "w")
                file.write(self.PM_name.get() + '\n' + self.PM_phone.get() + '\n' + self.PM_email.get())
                file.close()
        except IOError:
            file = open("PM_contact.txt", "w")
            file.write(self.PM_name.get() + '\n' + self.PM_phone.get() + '\n' + self.PM_email.get())
            file.close()

    def get_vcp(self, Event=None):
        if self.var1.get() == 1:
            checked()
        rendered_search = EPICscrape.retrieve_EPIC_html(self.project.get())
        (self.EPIC_data, self.epic_street_address) = EPICscrape.return_all_EPIC_fields(rendered_search)
        self.project_ids = EPICscrape.format_IDs(self.EPIC_data)
        new = (self.register(self.draw_midframe), TopFrame, self.project_ids)
        if self.project_ids:
            btn = ttk.Button(TopFrame, command=Application.draw_midframe, text="next")
            btn.grid(row=7, column=1)

    def save(self):
        filename = filedialog.asksaveasfilename(initialdir="./Desktop", title="Select file",
                                                filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        msg = EPICscrape.WriteTo(self.codify, str(filename) + '.csv')
        if msg == "Done":
            master.quit()
        # done=ttk.Style().configure("f.Label", background="black", foreground="white", relief="raised")
        # ttk.Label(master,text=msg,style="f.Label").grid_anchor(CENTER)

    def draw_midframe(Topframe, Event=None):

        selection_window = Toplevel()
        selection_window.title("Select an option")
        self.Base = ttk.Frame(selection_window).grid()

        Button1 = ttk.Button(master=self.Base, text="click for Factsheet 1", command=self.draw_FS1)
        Button1.grid(row=0, column=0, sticky=N + E + W + S)
        Button2 = ttk.Button(master=self.Base, text="click for Factsheet 2", command=self.draw_FS2)
        Button2.grid(row=0, column=1, sticky=N + E + W + S)
        Button3 = ttk.Button(master=self.Base, text="click for Factsheet 3", command=self.draw_FS3)
        Button3.grid(row=0, column=2, sticky=N + E + W + S)
        Button4 = ttk.Button(master=self.Base, text="click for Contact list", command=self.draw_CL)
        Button4.grid(row=0, column=3, sticky=N + E + W + S)
        # STYLES
        linkLabel = ttk.Style()
        linkLabel.configure("link.TLabel", foreground='blue')
        clicked = ttk.Style()
        clicked.configure("clickedlink.link.TLabel", foreground="purple3")

        linkBtn = ttk.Style()
        linkBtn.configure("link.TButton", foreground="blue", relief='sunken')

    def draw_FS1(self):
        IDS = ["15TMP060M", "16CVCP060M", "18TMP1339K"]
        Factsheet1_window = Toplevel()
        Factsheet1_window.title("Factsheet 1")
        FS1_Frame = ttk.Frame(Factsheet1_window)
        FS1_Frame.grid()

        # LABELS

        centerL = ttk.Style(master=Factsheet1_window)
        centerL.configure("centerL", justify=CENTER, pady=3)
        commentperiodL = ttk.Label(FS1_Frame, text="Start of Comment Period")
        developer_orgL = ttk.Label(FS1_Frame, text="Developer organization")
        Neighborhood = ttk.Label(FS1_Frame, text="Neighborhood")
        ProjectIdL = ttk.Label(FS1_Frame, text="Project Identifier")
        commentperiodL.grid(row=0, column=0)
        developer_orgL.grid(row=1, column=0)
        Neighborhood.grid(row=2, column=0)
        ProjectIdL.grid(row=3, column=0)

        # WIDGETS
        commentperiodE = ttk.Entry(FS1_Frame, width=30)
        developer_orgE = ttk.Entry(FS1_Frame, width=30)
        NeighborhoodE = ttk.Entry(FS1_Frame, width=30)
        ProjectIdC = ttk.Combobox(FS1_Frame, values=IDS)

        commentperiodE.insert(0, "%s" % time.strftime("%m/%d/%Y"))
        commentperiodE.grid(row=0, column=1)
        developer_orgE.grid(row=1, column=1)
        NeighborhoodE.grid(row=2, column=1)
        ProjectIdC.grid(row=3, column=1)

        print('twirl')

    def draw_FS2(self):
        Factsheet2_window = Toplevel()
        Factsheet2_window.title("Factsheet 2")
        Factsheet2_Frame = ttk.Frame(Factsheet2_window)

        IDS = ["15TMP060M", "16CVCP060M", "18TMP1339K"]
        chosenID = StringVar()
        # LABELS
        workstartL_FS2 = ttk.Label(Factsheet2_Frame, text="Construction Start Date")
        developer_orgL_FS2 = ttk.Label(Factsheet2_Frame, text="Developer Organization")
        ProjectIdL_FS2 = ttk.Label(Factsheet2_Frame, text="Project Identifier")

        # WIDGETS
        workstartE_FS2 = ttk.Entry(Factsheet2_Frame)
        workstartE_FS2.insert(0, "mm/dd/yyyy")
        developer_orgE_FS2 = ttk.Entry(Factsheet2_Frame)
        ProjectIdC_FS2 = ttk.Combobox(Factsheet2_Frame, values=IDS, textvariable=chosenID)

        # GRID
        Factsheet2_Frame.grid()
        workstartL_FS2.grid(row=0)
        developer_orgL_FS2.grid(row=1)
        ProjectIdL_FS2.grid(row=2)

        workstartE_FS2.grid(row=0, column=1)
        developer_orgE_FS2.grid(row=1, column=1)
        ProjectIdC_FS2.grid(row=2, column=1)

        print('burl')

    def draw_FS3(self):
        Factsheet_3_window = Toplevel()
        Factsheet_3_window.title("Factsheet 3")
        Factsheet_3_Frame = ttk.Frame(Factsheet_3_window)

        IDS = ["15TMP060M", "16CVCP060M", "18TMP1339K"]
        chosenID = StringVar()
        # LABELS
        FS3completiondateL = ttk.Label(Factsheet_3_Frame, text="Remedial Work Completion Date")
        FS3developer_orgL = ttk.Label(Factsheet_3_Frame, text="Developer Organization")
        FS3projectIdL = ttk.Label(Factsheet_3_Frame, text="Project Identifier")

        # WIDGETS
        FS3completiondateE = ttk.Entry(Factsheet_3_Frame)
        FS3completiondateE.insert(0, "mm/dd/yyyy")
        FS3developer_orgE = ttk.Entry(Factsheet_3_Frame)
        FS3projectIdC = ttk.Combobox(Factsheet_3_Frame, values=IDS, textvariable=chosenID)

        # GRID
        Factsheet_3_Frame.grid()

        FS3completiondateL.grid(row=0)
        FS3developer_orgL.grid(row=1)
        FS3projectIdL.grid(row=2)

        FS3completiondateE.grid(row=0, column=1)
        FS3developer_orgE.grid(row=1, column=1)
        FS3projectIdC.grid(row=2, column=1)

        print('star')

    def draw_CL(self):
        Contact_window = Toplevel()
        Contact_window.title("Contact List")
        ContactFrameCity = ttk.Labelframe(Contact_window, text="City-Borough Contacts")
        ContactFrameSS = ttk.Labelframe(Contact_window, text="Site/Local Area Contacts")

        # VARIABLES
        BoroughPresidentvar = StringVar()
        CityCouncilvar = StringVar()
        NYCDCPvar = StringVar()
        self.CB = StringVar()
        self.CBadr = StringVar()
        self.CBDMName = StringVar()
        self.CBDMEmail = StringVar()
        NYCityCC = """CityCouncil info goes here
         with email here
         yadda
         yadda
         """
        # LABELS
        BoroughPresidentL = ttk.Label(ContactFrameCity, text="Borough President")
        CityCouncilL = ttk.Label(ContactFrameCity, text="City Council")
        NYCDCP_L = ttk.Label(ContactFrameCity, text="NYCDCP Borough Director")
        self.EditStored = ttk.Label(ContactFrameCity,
                                    text="Am I out of date? Click here to change my stored values.",
                                    style="link.TLabel")
        self.EditStored.bind('<Button-1>', self.ChangeStored)
        # Calls to python Funcs
        tt = (self.register(self.OpenCBsite), ContactFrameSS)
        vcmd = (self.register(self.onValidate), '%s', '%S')
        rdctct = (self.register(self.LoadContacts), ContactFrameCity)

        CommunityBoardNUML = ttk.Label(ContactFrameSS, text="Community Board ##")
        CommunityBoardADRL = ttk.Label(ContactFrameSS, text="CB Address")
        CommunityBoardDistrictManNL = ttk.Label(ContactFrameSS, text='CB District Manager')
        CBDistrictManemailL = ttk.Label(ContactFrameSS, text="CB District Manager Email")
        CommunityBoardHelp = ttk.Button(ContactFrameSS, text="Take me to the CB site", style="link.TButton",
                                        command=tt)

        # Validation for Community Board
        # WIDGETS
        BoroughPresidentC = ttk.Combobox(ContactFrameCity, textvariable=BoroughPresidentvar, state='readonly')
        NYCDCP_C = ttk.Combobox(ContactFrameCity, textvariable=NYCDCPvar, state='readonly')
        CityCouncilT = Text(ContactFrameCity, width=30, height=10)
        CityCouncilT.insert(1.0, NYCityCC)  # get City Council Info from NYCity
        self.CommunityBoardNUME = ttk.Entry(ContactFrameSS, textvariable=self.CB, validate='key',
                                            validatecommand=vcmd)
        CommunityBoardADRE = ttk.Entry(ContactFrameSS)
        CommunityBoardDistrictManNE = ttk.Entry(ContactFrameSS)
        CBDistrictManEmailE = ttk.Entry(ContactFrameSS)

        # GRID
        ContactFrameCity.grid(row=0)
        BoroughPresidentL.grid(row=0)
        NYCDCP_L.grid(row=1)
        self.EditStored.grid(row=2)
        CityCouncilL.grid(row=3)
        BoroughPresidentC.grid(row=0, column=1)
        NYCDCP_C.grid(row=1, column=1)
        CityCouncilT.grid(row=3, column=1)

        ContactFrameSS.grid(row=1)
        CommunityBoardNUML.grid(row=0)
        CommunityBoardADRL.grid(row=1)
        CommunityBoardDistrictManNL.grid(row=2)
        CBDistrictManemailL.grid(row=3)
        CommunityBoardHelp.grid(row=4)

        self.CommunityBoardNUME.grid(row=0, column=1)
        # ContactFrameSS.wait_variable(self.onValidate)
        CommunityBoardADRE.grid(row=1, column=1)
        CommunityBoardDistrictManNE.grid(row=2, column=1)
        CBDistrictManEmailE.grid(row=3, column=1)

    def onValidate(ContactFrameSS, old, new):
        Check = True
        for ch in new:
            if ch.isdigit() != True:
                Check = False
        if Check == True:
            ContactFrameSS.CommunityBoardNUME.delete("0", 'end')
            ContactFrameSS.CommunityBoardNUME.insert("end", old + new)
        else:
            ContactFrameSS.CommunityBoardNUME.delete("0", 'end')
        return Check

    def OpenCBsite(ContactFrameSS, borough=None):
        import pandas as pd
        Borough = 'Brooklyn'  # EPICscrape.Fields.borough
        CBnumber = ContactFrameSS.CB.get()
        try:
            file = 'Community Board Websites.csv'
            df = pd.read_csv(file, index_col=["rowidx"])
            boroughcolumn = df["%s Community Boards" % Borough]
            sitecolumn = df["%s Community Board Websites" % Borough]
            ter = boroughcolumn.loc['row %s' % (int(CBnumber) - 1)]
            print("CB ##", ter)
            astro = sitecolumn.loc['row %s' % (int(CBnumber) - 1)]
            print(astro)
            # WORKS!
            EPICscrape.CommunityBoard(astro)
        except IOError as err:
            messagebox.showerror("File not found",
                                 "File {} was not found make sure its in the same path as {}".format(file,
                                                                                                     sys.path[
                                                                                                         0]))

    def LoadContacts(ContactFrameCity):
        try:
            box = 'StoredContacts.csv'
            with open(box, 'r') as f:
                file = csv.DictReader(f, dialect='excel')
                for row in file:
                    if EPICscrape.Fields.borough in row[0]:
                        ContactFrameCity.BoroughPresidentC.configure(values=str(row[0] + ',' + row[1]))
        except IOError as err:
            messagebox.showerror("File not found",
                                 "File {} was not found."
                                 " Make sure its in the same path (folder) as {}.".format(box, sys.path[0]))

    def SetContact(ContactFrameCity, Event):
        Event.widget.get()
        box = 'StoredContacts.csv'
        with open(box, 'r') as f:
            file = csv.DictReader(f, dialect='excel')
            for row in file:
                valuelist.append((row[0], row[1]))
                if EPICscrape.Fields.borough in row[0]:
                    ContactFrameCity.BoroughPresidentC.configure(values=str(row[0] + ',' + row[1]))

    def ChangeStored(self, Event):
        try:
            box = 'StoredContacts.csv'
            with open(box, 'r') as f:
                file = csv.DictReader(f, dialect='excel')
                for row in file:
                    if EPICscrape.Fields.borough in row[0]:
                        print(row)
        except IOError as err:
            messagebox.showerror("File not found",
                                 "File {} was not found. Make sure its in the same path (folder) as {}.".format(
                                     box, sys.path[0]))
        print(Event.type)
        print("registered")
        Event.widget.configure(style="clickedlink.link.TLabel")
        Event.widget.grid()
        # open a choose file dialog box and an alert about copying the original csv and editing that.

    def draw_FS(self):
        new_window = Toplevel(self)
        self.topframe = ttk.Frame(master=new_window)
        self.topframe.grid()
        # select what worksheet you're creating
        self.FS_choice = IntVar()
        self.FS_choice.set(0)
        FS1 = ttk.Radiobutton(self.topframe, text="Fact Sheet 1", variable=self.FS_choice, value=1)
        FS2 = ttk.Radiobutton(self.topframe, text="Fact Sheet 2", variable=self.FS_choice, value=2)
        FS3 = ttk.Radiobutton(self.topframe, text="Fact Sheet 3", variable=self.FS_choice, value=3)
        CL = ttk.Radiobutton(self.topframe, text="Contact List", variable=self.FS_choice, value=4)

        FS1.grid(row=1, column=0)
        FS2.grid(row=1, column=1)
        FS3.grid(row=1, column=2)
        CL.grid(row=1, column=3)

        check = ttk.Button(self.topframe, text="check", command=Win.getval(self))
        check.grid(row=2, column=3)

    def val(self):
        pass
        midframe_window = Toplevel(self)
        self.MidFrame = ttk.Frame(midframe_window, borderwidth=5)
        self.MidFrame.grid(row=3, column=0, rowspan=2, columnspan=4, sticky=W + E + N + S)
        CanISeeID = ttk.Label(self.MidFrame, text="Choose the OER Project ID you'd like to use from EPIC")
        CanISeeID.grid(pady=3, row=0, column=0, columnspan=4, sticky=N + S + E + W)
        Application.pop_rad(self, self.project_ids)

    def pop_rad(self, mylist):
        r = 1
        c = 0
        t = 0
        tupled_epic_ids = []
        index = 0
        for id in mylist:
            tup = (id, index)
            tupled_epic_ids.append(tup)
            index += 1

        for id, idx in tupled_epic_ids:
            rad = ttk.Radiobutton(self.MidFrame, command=Application.midframe_click(self), text=id, variable=self.v,
                                  value=idx)
            if t % 4 == 0 and t != 0:
                r += 1
                c = 0
            rad.grid(row=r, column=c, sticky=W + E + N + S)
            c += 1
            t += 1

    def midframe_click(self):
        """once a project ID is selected, runs this"""
        self.codify = EPICscrape.return_codify(self.EPIC_data, self.epic_street_address)
        x = self.v.get()
        repr(x)
        self.codify = Application.final(self, self.codify, x)
        self.results.set(
            self.codify)  # Fix the first bit, make the text wrap and get it saving coreectly and your dolden
        self.res_print.config(text=self.codify)
        self.save_button.config(state=NORMAL)
        print('codify', self.codify)

    def final(self, object, idx=None):
        # i'm gonna say that i did this for clarity but actually
        # i just started doing this before i realized it was unnecessary
        if self.usesameID.get() == 0:
            if isinstance(object, EPICscrape.Fields):
                object.set_id(self.project_ids[idx])
                object.set_contact_name(self.PM_name.get().strip())
                object.set_contact_phone(self.PM_phone.get().strip())
                object.set_contact_email(self.PM_email.get().strip())
                object.separate_BL()
                return object
            elif isinstance(object, EPICscrape.NoLibraryMatch):
                object.set_id(self.project_ids[idx])
                object.set_contact_name(self.PM_name.get().strip())
                object.set_contact_phone(self.PM_phone.get().strip())
                object.set_contact_email(self.PM_email.get().strip())
                object.separate_BL()
                return object
        else:
            object.set_id(self.project.get().upper())
            object.set_contact_name(self.PM_name.get().strip())
            object.set_contact_phone(self.PM_phone.get().strip())
            object.set_contact_email(self.PM_email.get().strip())
            object.separate_BL()
            return object

    def comment_period(self):
        import datetime
        frmtstrg = '%m/%d/%Y'
        startdate = datetime.datetime.strptime(FS1Date_start.get(), frmtstrg)
        enddate = startdate + datetime.timedelta(30)

        FS1Date_start = ttk.Entry()


def main():
    root = Tk()
    # root.geometry("550x550")
    app = Application(master=root)
    app.mainloop()


main()

"""
entry error
15cvcp0060m
5cvcp0060m

City, State creates a cell in csv formats ((just keep it separate.))
add PM_email header
create entry just for PM_phone

"""
