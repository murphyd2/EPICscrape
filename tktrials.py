"Dylan Murphy 08-06-18"
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import EPICscrape



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
                file= open('PM_contact.csv','r')
                data = file.readlines()
                file.close()
                if (PM_name.get(),PM_email.get()) not in data:
                    file = open("PM_contact.csv","w")
                    file.write(PM_name.get()+'\n')
                    file.write("Project Manager\n")
                    file.write(PM_email.get()+'\n')
                    file.close()
            except IOError:
                file = open("PM_contact.csv", "w")
                file.write(PM_name.get() + '\n')
                file.write(PM_email.get() + '\n')
                file.close()

        def get_vcp():
            if var1.get()==1:
                checked()
            rendered_search= EPICscrape.retrieve_EPIC_html(self.project.get())
            (self.EPIC_data, self.epic_street_address)= EPICscrape.return_all_EPIC_fields(rendered_search)
            self.project_ids= EPICscrape.format_IDs(self.EPIC_data)
            if var2.get()==0:
                draw_midframe(MidFrame,self.project_ids)
            else:
                self.codify= EPICscrape.return_codify(self.EPIC_data,self.epic_street_address)
                self.codify=final(self.codify)
                results.set(self.codify)
                res_print.config(text=self.codify)
                save_button.config(state=NORMAL)

        def midframe_click():
            """once a project ID is selected, runs this"""
            self.codify = EPICscrape.return_codify(self.EPIC_data, self.epic_street_address)
            x = self.v.get()
            repr(x)
            self.codify=final(self.codify,x)
            results.set(self.codify) #Fix the first bit, make the text wrap and get it saving coreectly and your dolden
            res_print.config(text=self.codify)
            save_button.config(state=NORMAL)

        def draw_midframe(MidFrame,mylist):
            r = 1
            c = 0
            t = 0
            tupled_epic_ids = []
            index = 0
            for id in mylist:
                tup= ()
                tup= (id,index)
                tupled_epic_ids.append(tup)
                index += 1
            print(tupled_epic_ids)
            for id,idx in tupled_epic_ids:
                rad = ttk.Radiobutton(MidFrame, command=midframe_click, text=id, variable=self.v, value=idx)
                if t % 4 == 0 and t != 0:
                    r += 1
                    c = 0
                rad.grid(row=r, column=c, sticky=W + E + N + S)
                c += 1
                t += 1
            # return tupled_epic_ids
        def final(object,idx=None):
            #i'm gonna say that i did this for clarity but actually
            # i just started doing this before i realized it was unnecessary
            if var2.get()==0:
                if isinstance(object,EPICscrape.Fields):
                    object.set_id(self.project_ids[idx])
                    object.set_contact_name(PM_name.get())
                    object.set_contact_email(PM_email.get())
                    return object
                elif isinstance(object,EPICscrape.NoLibraryMatch):
                    object.set_id(self.project_ids[idx])
                    object.set_contact_name(PM_name.get())
                    object.set_contact_email(PM_email.get())
                    return object
            else:
                object.set_id(self.project.get().upper())
                object.set_contact_email(PM_email.get())
                object.set_contact_name(PM_name.get())
                return object

        def save():
            filename = filedialog.asksaveasfilename(initialdir="./Desktop", title="Select file",
                                                     filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
            msg=EPICscrape.WriteTo(self.codify,str(filename)+'.csv')
            if msg=="Done":
                master.quit()
            # done=ttk.Style().configure("f.Label", background="black", foreground="white", relief="raised")
            # ttk.Label(master,text=msg,style="f.Label").grid_anchor(CENTER)



        LabelStyle=ttk.Style().configure("TLabel",foreground="black",background="light grey",padding=5,border="black")
        TopStyle=ttk.Style().configure("r.TFrame",background="light grey")
        MidStyle=ttk.Style().configure("b.TFrame",background="blue")
        BottomStyle=ttk.Style().configure("g.TFrame",background="white")
        checkst=ttk.Style().configure('lg.TCheckbutton',background="light grey",padding=5)
        for r in range(6):
            self.master.rowconfigure(r, weight=1)
        for c in range(4):
            self.master.columnconfigure(c, weight=1)


        TopFrame = ttk.Frame(master, borderwidth = 2,style="r.TFrame")
        TopFrame.grid(row = 0, column = 0, rowspan = 3, columnspan = 4, sticky = W+E+N+S)
        ttk.Label(TopFrame,text="Project Manager and their phone").grid(row=0,column=0, sticky=W+E+N+S)
        ttk.Label(TopFrame,text="Project Manager email").grid(row=1,column=0, sticky=W+E+N+S)
        ttk.Label(TopFrame,text="OER Project #").grid(row=3, column=0, sticky= W+N+E+S)

        #Entry Fields
        PM_name = Entry(TopFrame, width=100)
        PM_name.grid(row=0,column=1,columnspan=5,sticky=W+E)
        PM_email = Entry(TopFrame,width=100)
        PM_email.grid(row=1, column=1, columnspan=3,sticky=W+E)
        self.project= Entry(TopFrame, width=100)
        self.project.grid(row=3,column=1, columnspan=2,sticky=W+E+N+S)


        # try filling Entrys from stored info
        try:
            file = open("PM_contact.csv",'r')
            user_em = file.readlines()
            file.close()
            PM_name.insert(0,user_em[0])
            PM_email.insert(0,user_em[1])
        except IOError:
            PM_name.insert(0,"Captain Planet at 212-788-7527")
            PM_email.insert(0,"cplanet@nyc.oer.gov")

        # Remember Me box
        var1= IntVar()
        chk= ttk.Checkbutton(TopFrame,text= "Remember Me",variable=var1, style="lg.TCheckbutton")
        chk.grid(row=2,column=1,columnspan=3)


        self.Go= ttk.Button(TopFrame,text="Go",command=get_vcp)
        self.Go.grid(row=4,column=1,columnspan=3,sticky=W+E+N+S)
        var2=IntVar()
        GoFast= ttk.Checkbutton(TopFrame,text="Use this number in my recipients list",variable=var2,style="lg.TCheckbutton")
        GoFast.grid(row=4,column=0,sticky=W+E+N+S)
        #the number of buttons will need to be  created (with a for i in range (len_project_id_list))
        #use lambda function?
        #once clicked, these buttons will place that value in EPICscrape's first codify field
        MidFrame = ttk.Frame(master, borderwidth = 5)
        MidFrame.grid(row = 3, column = 0, rowspan = 2, columnspan = 4, sticky = W+E+N+S)

        #sample [('15TMP0008M',0),('15EHAN008M',1),('15CVCP060M',2),('15TMP$$$8M',3),('15EH-AN008M',4),('15CVfds0M',5)]
        ttk.Label(MidFrame,text="Choose the OER Project ID you'd like to use from EPIC").grid(pady=3,row=0,column=0,columnspan=4,sticky=N+S+E+W)

        results = StringVar()
        BottomFrame= ttk.Frame(master,borderwidth=2, style="g.TFrame")
        BottomFrame.grid(row=5,column=0,rowspan=2,columnspan=4,sticky=N+S+E+W)
        results_label=ttk.Label(BottomFrame, text="Here are your results:")
        results_label.grid(row=0,column=0,sticky=N+E+W+S)
        res_print= ttk.Label(BottomFrame,textvariable=results,wraplength=300,justify=LEFT)
        res_print.grid(pady=5, row=1, column=0, columnspan=2, sticky=N + E + W + S)


        last=7
        ttk.Label(master, text= "What would you like to do?").grid(row=last,column=0,columnspan=2,sticky=N+E+W+S)
        save_button = ttk.Button(master,text="save", command=save,state=DISABLED)
        save_button.grid(row=last,column=2,sticky =N+W+E+S)
        ttk.Button(master,text="quit", command=master.quit).grid(row=last,column=3,sticky=N+E+W+S)


        #not working, setting everything up before hand

#span starts count from 1 not 0 i.e. normally counts



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
should write just 
"""