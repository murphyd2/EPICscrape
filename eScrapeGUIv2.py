"Dylan Murphy 08-06-18"
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import EPICscrape
import datetime


class Application(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.master.title("EPICscrape")
        self.EPIC_data=None
        self.epic_street_address=None
        self.project_ids=None
        self.codify= None
        self.v = IntVar()
        def checked():
            """opens the designated file and checks if the pm_name
            field has changed if it has it writes the current cred"""
            try:
                file= open('PM_contact.txt','r')
                data = file.readlines()
                file.close()
                if (self.PM_name.get(),self.PM_phone.get(),self.PM_email.get()) not in data:
                    file = open("PM_contact.txt","w")
                    file.write(self.PM_name.get()+'\n'+self.PM_phone.get()+'\n'+self.PM_email.get())
                    file.close()
            except IOError:
                file = open("PM_contact.txt", "w")
                file.write(self.PM_name.get() + '\n' + self.PM_phone.get() + '\n' + self.PM_email.get())
                file.close()


        def get_vcp():
            if var1.get()==1:
                checked()
            rendered_search= EPICscrape.retrieve_EPIC_html(self.project.get())
            (self.EPIC_data, self.epic_street_address)= EPICscrape.return_all_EPIC_fields(rendered_search)
            self.project_ids= EPICscrape.format_IDs(self.EPIC_data)
            Application.draw_midframe(self,self.project_ids)


        def save():
            filename = filedialog.asksaveasfilename(initialdir="./Desktop", title="Select file",
                                                     filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
            msg=EPICscrape.WriteTo(self.codify,str(filename)+'.csv')
            if msg=="Done":
                master.quit()
            # done=ttk.Style().configure("f.Label", background="black", foreground="white", relief="raised")
            # ttk.Label(master,text=msg,style="f.Label").grid_anchor(CENTER)
        Buttonstyle=ttk.Style()
        Buttonstyle.map('TButton',
              background=[('disabled', '#d9d9d9'), ('active','  #ececec')],
              foreground=[('disabled', '#a3a3a3')],
              relief=[('pressed', '!disabled', 'sunken')])
        LabelStyle=ttk.Style().configure("TLabel",background="light grey",padding=5,border="black")
        TopStyle=ttk.Style().configure("r.TFrame",background="light grey")
        MidStyle=ttk.Style().configure("b.TFrame",background="blue")
        BottomStyle=ttk.Style().configure("g.TFrame",background="white")
        checkstyle=ttk.Style().configure('lg.TCheckbutton',background="light grey",padding=5)


        TopFrame = ttk.Frame(master, borderwidth = 2,style="r.TFrame")
        TopFrame.grid(row = 0, column = 0, rowspan=5,columnspan = 4, sticky = W+E+N+S)
        ttk.Label(TopFrame,text="Project Manager").grid(row=0,column=0, sticky=W+E+N+S)
        ttk.Label(TopFrame,text="Project Manager phone").grid(row=1,column=0, sticky=W+E+N+S)
        ttk.Label(TopFrame,text="Project Manager email").grid(row=2,column=0, sticky=W+E+N+S)
        ttk.Label(TopFrame,text="OER Project #").grid(row=4, column=0, sticky= W+N+E+S)

        #Entry Fields
        self.PM_name = Entry(TopFrame, width=50)
        self.PM_name.grid(row=0,column=1,columnspan=5,sticky=W+E)
        self.PM_phone = Entry(TopFrame, width=50)
        self.PM_phone.grid(row=1,column=1,columnspan=5,sticky=W+E)
        self.PM_email = Entry(TopFrame,width=50)
        self.PM_email.grid(row=2, column=1, columnspan=3,sticky=W+E)
        self.project= Entry(TopFrame, width=50)
        self.project.grid(row=4,column=1, columnspan=2,sticky=W+E+N+S)


        # try filling Entrys from stored info
        try:
            file = open("PM_contact.txt",'r')
            user_em = file.readlines()
            file.close()
            memorized_auth=user_em
            self.PM_name.insert(0,memorized_auth[0])
            self.PM_phone.insert(0,memorized_auth[1])
            self.PM_email.insert(0,memorized_auth[2])
        except IOError:
            self.PM_name.insert(0,"Captain Planet")
            self.PM_phone.insert(0,"212-788-7527")
            self.PM_email.insert(0,"cplanet@nyc.oer.gov")

        # Remember Me box
        var1= IntVar()
        chk= ttk.Checkbutton(TopFrame,text= "Remember Me",variable=var1, style="lg.TCheckbutton")
        chk.grid(row=3,column=1,columnspan=3)


        self.Go= ttk.Button(TopFrame,text="Go",command=get_vcp)
        self.Go.grid(row=5,column=1,columnspan=3,sticky=W+E+N+S)
        var2=IntVar()
        GoFast= ttk.Checkbutton(TopFrame,text="Use this number in my recipients list",variable=var2,style="lg.TCheckbutton")
        GoFast.grid(row=5,column=0,sticky=W+E+N+S)

        results = StringVar()
        BottomFrame= ttk.Frame(master,borderwidth=2, style="g.TFrame")
        BottomFrame.grid(row=5,column=0,rowspan=2,columnspan=4,sticky=N+S+E+W)
        results_label=ttk.Label(BottomFrame, text="Here are your results:")
        results_label.grid(row=0,column=0,sticky=N+E+W+S)

        res_print= ttk.Label(BottomFrame,textvariable=results,wraplength=300,justify=LEFT)
        res_print.grid(pady=5, row=1, column=0, columnspan=2, sticky=N + E + W + S)


        last=7
        ttk.Label(TopFrame, text= "What would you like to do?").grid(row=last,column=0,columnspan=2,sticky=N+E+W+S)
        self.save_button = ttk.Button(TopFrame,text="save", command=save,state=DISABLED)
        self.save_button.grid(row=last,column=2,sticky =N+W+E+S)
        self.q= ttk.Button(TopFrame,text="quit", command=master.quit).grid(row=last,column=3,sticky=N+E+W+S)

    def draw_midframe(self,mylist):
        midframe_window = Toplevel(self)
        self.MidFrame = ttk.Frame(midframe_window, borderwidth=5)
        self.MidFrame.grid(row=3, column=0, rowspan=2, columnspan=4, sticky=W + E + N + S)
        CanISeeID=ttk.Label(self.MidFrame, text="Choose the OER Project ID you'd like to use from EPIC")
        CanISeeID.grid(pady=3, row=0, column=0,columnspan=4,sticky=N + S + E + W)
        Application.pop_rad(self,self.project_ids)
    def pop_rad(self,mylist):
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
            rad = ttk.Radiobutton(self.MidFrame, command=Application.midframe_click(self), text=id, variable=self.v, value=idx)
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
        self.codify = Application.final(self.codify, x)
        self.results.set(self.codify)  # Fix the first bit, make the text wrap and get it saving coreectly and your dolden
        self.res_print.config(text=self.codify)
        self.save_button.config(state=NORMAL)
        print('codify', self.codify)

    def final(self, object, idx=None):
        # i'm gonna say that i did this for clarity but actually
        # i just started doing this before i realized it was unnecessary
        if var2.get() == 0:
            if isinstance(object, EPICscrape.Fields):
                object.set_id(self.project_ids[idx])
                object.set_contact_name(PM_name.get().strip())
                object.set_contact_phone(PM_phone.get().strip())
                object.set_contact_email(PM_email.get().strip())
                object.separate_BL()
                return object
            elif isinstance(object, EPICscrape.NoLibraryMatch):
                object.set_id(self.project_ids[idx])
                object.set_contact_name(PM_name.get().strip())
                object.set_contact_phone(PM_phone.get().strip())
                object.set_contact_email(PM_email.get().strip())
                object.separate_BL()
                return object
        else:
            object.set_id(project.get().upper())
            object.set_contact_name(PM_name.get().strip())
            object.set_contact_phone(PM_phone.get().strip())
            object.set_contact_email(PM_email.get().strip())
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
    root.geometry("550x550")
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