from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import EPICscrape
import time

class Win(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.Base = ttk.Frame(master).grid()
        def FS1():
            Win.draw_FS1(self)
        def FS2():
            Win.draw_FS2(self)
        def FS3():
            Win.draw_FS3(self)
        def CL():
            pass
        def intfunc():
            Win.draw_FS(self)
        Button1 = ttk.Button(master=self.Base,text= "click for Factsheet 1",command=self.draw_FS1)
        Button1.grid(row=0,column=0, sticky=N+E+W+S)
        Button2 = ttk.Button(master=self.Base,text= "click for Factsheet 2",command=self.draw_FS2)
        Button2.grid(row=0,column=1, sticky=N+E+W+S)
        Button3 = ttk.Button(master=self.Base,text= "click for Factsheet 3",command=self.draw_FS3)
        Button3.grid(row=0,column=2, sticky=N+E+W+S)
        Button4 = ttk.Button(master=self.Base,text= "click for Contact list",command=self.draw_CL)
        Button4.grid(row=0,column=3, sticky=N+E+W+S)
        #STYLES
        linkLabel = ttk.Style()
        linkLabel.configure("link.TLabel",foreground= 'blue')
        clicked = ttk.Style()
        clicked.configure("clickedlink.link.TLabel",foreground="purple3")
    def draw_FS1(self):
        IDS = ["15TMP060M", "16CVCP060M", "18TMP1339K"]
        Factsheet1_window= Toplevel()
        Factsheet1_window.title("Factsheet 1")
        FS1_Frame= ttk.Frame(Factsheet1_window)
        FS1_Frame.grid()

        #LABELS

        centerL = ttk.Style(master=Factsheet1_window)
        centerL.configure("centerL",justify=CENTER,pady=3)
        commentperiodL = ttk.Label(FS1_Frame, text="Start of Comment Period")
        developer_orgL = ttk.Label(FS1_Frame, text= "Developer organization")
        Neighborhood = ttk.Label(FS1_Frame, text= "Neighborhood")
        ProjectIdL = ttk.Label(FS1_Frame, text= "Project Identifier")
        commentperiodL.grid(row=0, column = 0)
        developer_orgL.grid(row=1, column = 0)
        Neighborhood.grid(row=2, column = 0)
        ProjectIdL.grid(row=3,column =0)

        #WIDGETS
        commentperiodE = ttk.Entry(FS1_Frame,width = 30)
        developer_orgE = ttk.Entry(FS1_Frame, width = 30)
        NeighborhoodE = ttk.Entry(FS1_Frame, width = 30)
        ProjectIdC = ttk.Combobox(FS1_Frame,values= IDS)

        commentperiodE.insert(0,"%s" % time.strftime("%m/%d/%Y"))
        commentperiodE.grid(row=0,column=1)
        developer_orgE.grid(row=1,column=1)
        NeighborhoodE.grid(row=2,column=1)
        ProjectIdC.grid(row=3,column=1)


        print('twirl')
    def draw_FS2(self):
        Factsheet2_window= Toplevel()
        Factsheet2_window.title("Factsheet 2")
        Factsheet2_Frame = ttk.Frame(Factsheet2_window)

        IDS = ["15TMP060M", "16CVCP060M", "18TMP1339K"]
        chosenID= StringVar()
        #LABELS
        workstartL_FS2 = ttk.Label(Factsheet2_Frame,text="Construction Start Date")
        developer_orgL_FS2 = ttk.Label(Factsheet2_Frame,text="Developer Organization")
        ProjectIdL_FS2 = ttk.Label(Factsheet2_Frame,text="Project Identifier")


        #WIDGETS
        workstartE_FS2 = ttk.Entry(Factsheet2_Frame)
        workstartE_FS2.insert(0,"mm/dd/yyyy")
        developer_orgE_FS2= ttk.Entry(Factsheet2_Frame)
        ProjectIdC_FS2 = ttk.Combobox(Factsheet2_Frame, values= IDS, textvariable= chosenID)

        #GRID
        Factsheet2_Frame.grid()
        workstartL_FS2.grid(row=0)
        developer_orgL_FS2.grid(row=1)
        ProjectIdL_FS2.grid(row=2)

        workstartE_FS2.grid(row=0,column=1)
        developer_orgE_FS2.grid(row=1,column=1)
        ProjectIdC_FS2.grid(row=2,column=1)

        print('burl')
    def draw_FS3(self):
        Factsheet_3_window= Toplevel()
        Factsheet_3_window.title("Factsheet 3")
        Factsheet_3_Frame= ttk.Frame(Factsheet_3_window)

        IDS = ["15TMP060M", "16CVCP060M", "18TMP1339K"]
        chosenID = StringVar()
        #LABELS
        FS3completiondateL= ttk.Label(Factsheet_3_Frame,text="Remedial Work Completion Date")
        FS3developer_orgL = ttk.Label(Factsheet_3_Frame,text= "Developer Organization")
        FS3projectIdL = ttk.Label(Factsheet_3_Frame,text= "Project Identifier")

        #WIDGETS
        FS3completiondateE = ttk.Entry(Factsheet_3_Frame)
        FS3completiondateE.insert(0,"mm/dd/yyyy")
        FS3developer_orgE = ttk.Entry(Factsheet_3_Frame)
        FS3projectIdC = ttk.Combobox(Factsheet_3_Frame,values= IDS, textvariable= chosenID)

        #GRID
        Factsheet_3_Frame.grid()

        FS3completiondateL.grid(row = 0)
        FS3developer_orgL.grid(row = 1)
        FS3projectIdL.grid(row = 2)

        FS3completiondateE.grid(row = 0, column = 1)
        FS3developer_orgE.grid(row = 1, column = 1)
        FS3projectIdC.grid(row= 2 , column = 1)

        print('star')
    def draw_CL(self):
        Contact_window= Toplevel()
        Contact_window.title("Contact List")
        ContactFrameCity= ttk.Labelframe(Contact_window,text="City-Borough Contacts")
        ContactFrameSS= ttk.Labelframe(Contact_window, text="Site/Local Area Contacts")

        #VARIABLES
        BoroughPresidentvar = StringVar()
        CityCouncilvar = StringVar()
        NYCDCPvar = StringVar()
        self.CB = IntVar()
        CBadr=StringVar(value="Community Board %s Address" % self.CB.get())

        NYCityCC= """CityCouncil info goes here
         with email here
         yadda
         yadda
         """
        #LABELS
        BoroughPresidentL= ttk.Label(ContactFrameCity, text= "Borough President")
        CityCouncilL=ttk.Label(ContactFrameCity,text="City Council")
        NYCDCP_L = ttk.Label(ContactFrameCity, text="NYCDCP Borough Director")
        self.EditStored = ttk.Label(ContactFrameCity, text="Am I out of date? Click here to change my stored values.",
                               style="link.TLabel")
        self.EditStored.bind('<Button-1>', self.ChangeStored)

        CommunityBoardNUML = ttk.Label(ContactFrameSS, text="Community Board ##")
        CommunityBoardADRL = ttk.Label(ContactFrameSS, textvariable=CBadr)
        CommunityBoardDistrictManNL = ttk.Label(ContactFrameSS, text= ("Community Board " +str(self.CB.get())+" District Manager"))
        CBDistrictManemailL = ttk.Label(ContactFrameSS, text= "CB {:2d} District Manager E-mail".format(self.CB.get()))
        CommunityBoardHelp = ttk.Label(ContactFrameSS,text="Go to CB site",style="link.TLabel")
        CommunityBoardHelp.bind(('<Button-1>', '<Return>'),self.OpenCBsite)
        #Get CB info from NYCity? 1 brooklyn, 8 queens is format

        #WIDGETS
        BoroughPresidentC = ttk.Combobox(ContactFrameCity, textvariable= BoroughPresidentvar,state='readonly')
        NYCDCP_C = ttk.Combobox(ContactFrameCity, textvariable= NYCDCPvar,state='readonly')
        CityCouncilT = Text(ContactFrameCity,width= 30, height= 10)
        CityCouncilT.insert(1.0, NYCityCC) #get City Council Info from NYCity


        vcmd = (self.register(self.onValidate),'%S','%P')
        self.CommunityBoardNUME = ttk.Entry(ContactFrameSS, textvariable=self.CB,validate='key',validatecommand=vcmd )

        CommunityBoardADRE= ttk.Entry(ContactFrameSS)
        CommunityBoardDistrictManNE= ttk.Entry(ContactFrameSS)
        CBDistrictManEmailE= ttk.Entry(ContactFrameSS)





        #GRID
        ContactFrameCity.grid(row=0)
        BoroughPresidentL.grid(row=0)
        NYCDCP_L.grid(row=1)
        self.EditStored.grid(row=2)
        CityCouncilL.grid(row=3)

        BoroughPresidentC.grid(row=0, column=1)
        NYCDCP_C.grid(row=1,column=1)
        CityCouncilT.grid(row=3,column=1)

        ContactFrameSS.grid(row=1)
        CommunityBoardNUML.grid(row=0)
        CommunityBoardADRL.grid(row=1)
        CommunityBoardDistrictManNL.grid(row=2)
        CBDistrictManemailL.grid(row=3)

        self.CommunityBoardNUME.grid(row=0,column = 1)
        # ContactFrameSS.wait_variable(self.onValidate)
        CommunityBoardADRE.grid(row=1,column=1)
        CommunityBoardDistrictManNE.grid(row=2,column=1)
        CBDistrictManEmailE.grid(row=3,column=1)

        print('keys')
    def onValidate(ContactFrameSS, new,combo):
        Check= True
        for ch in new:
            if ch.isdigit()!= True:
                Check=False
        if Check==True:
            ContactFrameSS.CommunityBoardNUME.delete("0",'end')

            ContactFrameSS.CB.set(combo)
        else:
            ContactFrameSS.CommunityBoardNUME.delete("0",'end')
        return Check

    def OpenCBsite(self, Event):
        pass
    def ChangeStored(self, Event):
        print(Event.type)
        print("registered")
        Event.widget.configure(style="clickedlink.link.TLabel")
        Event.widget.grid()
        #open a choose file dialog box and an alert about copying the original csv and editing that.

    def draw_FS(self):
        new_window= Toplevel(self)
        self.topframe= ttk.Frame(master=new_window)
        self.topframe.grid()
        #select what worksheet you're creating
        self.FS_choice = IntVar()
        self.FS_choice.set(0)
        FS1= ttk.Radiobutton(self.topframe,text= "Fact Sheet 1",variable=self.FS_choice,value=1)
        FS2= ttk.Radiobutton(self.topframe,text= "Fact Sheet 2",variable=self.FS_choice,value=2)
        FS3= ttk.Radiobutton(self.topframe,text= "Fact Sheet 3",variable=self.FS_choice,value=3)
        CL= ttk.Radiobutton(self.topframe,text= "Contact List",variable=self.FS_choice,value=4)

        FS1.grid(row=1,column=0)
        FS2.grid(row=1,column=1)
        FS3.grid(row=1,column=2)
        CL.grid(row=1,column=3)

        check= ttk.Button(self.topframe, text= "check", command=Win.getval(self))
        check.grid(row=2,column=3)


    def val(self):
        pass





def main():
    root = Tk()
    # root.geometry("550x550")
    app = Win(master=root)
    app.mainloop()

main()