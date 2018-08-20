class Fields:
    "This Class is used to more easily reference specific information once it is pulled from EPIC and NYPL.org"
    def __init__(self, number, name, borough, address, block_lot, project_class, month_year, library_adr, lib_phone,PmName,PmPhone,PmEmail):
        self.number=number
        self.link_address  = name
        self.borough = borough
        self.address = address
        self.block_lot = block_lot
        self.project_class = project_class
        self.month_year = month_year
        self.library_adr = library_adr
        self.library_ph =   lib_phone
        self.PmName=PmName
        self.PmPhone= PmPhone
        self.PmEmail=PmEmail

    def __iter__(self):
        return self

    def __repr__(self):
        return repr((self.number, self.link_address, self.borough, self.address, self.block_lot, self.project_class,
                     self.month_year, self.library_adr, self.library_ph,self.PmName,self.PmPhone,self.PmEmail))
    def set_id(self,string):
        self.number=string
        return self.number
    def set_contact_name(self,string):
        self.PmName=string
        return self.PmName
    def set_contact_phone(self,string):
        self.PmPhone=string
        return self.PmPhone
    def set_contact_email(self,string):
        self.PmEmail=string
        return self.PmEmail

def WriteTo(object, outstring):
    import csv
    with open(str(outstring), 'w', newline='') as f:
        if isinstance(object, Fields) == True:
            file = csv.writer(f,dialect="excel")
            headers="VCP Number, Repository URL,Borough, Address, Block, Lot, Site Status,Month and Year, Library Address, Library Phone,PM Contact, PM Phone, PM Email"
            headers=headers.split(',')
            file.writerow(headers)

            fieldlist = list(vars(object).values())
            file.writerow(fieldlist)
            f.close()
            return "Done"
        elif isinstance(object, NoLibraryMatch) == True:
            file = csv.writer(f,dialect="excel")
            headers=" VCP Number, Repository URL,Borough, Address, Block, Lot, Site Status, Month and Year,PM Contact, PM Phone, PM Email"
            headers=headers.split(',')
            file.writerow(headers)
            fieldlist = list(vars(object).values())
            file.writerow(fieldlist)
            f.close()
            return "Done"
def main():
    text = Fields(' 16CVCP085K  ', 'https://a002-epic.nyc.gov/app/workspace/3473/docrepository', 'Brooklyn',
                  '710 Grand Street', 'Block: 2788, Lot:19', 'Completed (C)', 'August 2018',
                  'Leonard 81 Devoe Street Brooklyn, NY 11211 ', '718-486-6006', 'Anna Brooks',
                  '212-788-7527', 'abrooks@dep.nyc.gov')

    WriteTo(text,'test.csv')
main()

"""
def WriteTo(object, outstring):
    import csv
    if isinstance(object,Fields)==True:
        file= csv.writer(open(str(outstring),'w',newline=''),)
        file.write(" VCP Number, Repository URL,Borough, Address, Block, Lot, Site Status,"
                   " Month and Year, Library Address, Library Phone,PM Contact, PM Phone, PM Email,\n")
        for i in vars(object).values():
            fieldlist= list(vars(object).values())
            if i == fieldlist[-5]:

                file.write(str(i).strip(',')+',')

            elif i != fieldlist[-1]:
                file.write(str(i)+',')
            else:
                file.write(str(i))
        file.close()
        return "Done"
    elif isinstance(object,NoLibraryMatch)==True:
        file = open(str(outstring), 'w')
        file.write(" VCP Number, Repository URL,Borough, Address, Block, Lot, Site Status,"
                   " Month and Year,PM Contact, PM Phone, PM Email,\n")
        for i in vars(object).values():
            fieldlist = list(vars(object).values())

            if i != fieldlist[-1]:
                file.write(str(i) + ',')
            else:
                file.write(str(i))
        file.close()
        return "Done"
"""