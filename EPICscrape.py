"""Dylan Murphy"
"2018-07-24"""

"""This program takes a VCP Number given by the user and returns:
the doc repository URL, the Borough, the address the E designation as well as the Block and Lot if its a valid search. 

It makes use of the Selenium, lxml, and BeautifulSoup modules.
"""
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from time import gmtime, strftime

class Fields:
    "This Class is used to more easily reference specific information once it is pulled from EPIC and NYPL.org"
    def __init__(self, number, name, borough, address, block, lot, project_class, month_year, library_adr, lib_phone,PmName,PmPhone,PmEmail):
        self.number=number
        self.link_address  = name
        self.borough = borough
        self.address = address
        self.block= block
        self.lot= lot
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
        return repr((self.number, self.link_address, self.borough, self.address, self.block, self.lot, self.project_class,
                     self.month_year, self.library_adr, self.library_ph,self.PmName,self.PmPhone,self.PmEmail))
    def set_id(self,string):
        self.number=string
        return self.number
    def separate_BL(self):
        split=self.block.split(',')
        self.block=split[0]
        self.lot=split[1]
        return self.block,self.lot
    def set_contact_name(self,string):
        self.PmName=string
        return self.PmName
    def set_contact_phone(self,string):
        self.PmPhone=string
        return self.PmPhone
    def set_contact_email(self,string):
        self.PmEmail=string
        return self.PmEmail

class NoLibraryMatch:
    "This Class is used in case the library search fails"
    def __init__(self, number, name, borough, address, block, lot, project_class, month_year,PmName,PmPhone,PmEmail):
        self.number= number
        self.link_address  = name
        self.borough = borough
        self.address = address
        self.block= block
        self.lot= lot
        self.project_class = project_class
        self.month_year = month_year
        self.PmName = PmName
        self.PmPhone = PmPhone
        self.PmEmail = PmEmail
    def __repr__(self):
        return repr((self.number, self.link_address, self.borough, self.address, self.block, self.lot, self.project_class,
                     self.month_year,self.PmName,self.PmPhone,self.PmEmail))

    def set_id(self,string):
        self.number=string
        return self.number
    def separate_BL(self):
        split=self.block.split(',')
        self.block=split[0]
        self.lot=split[1]
        return self.block,self.lot
    def set_contact_name(self,string):
        self.PmName=string
        return self.PmName
    def set_contact_phone(self,string):
        self.PmPhone=string
        return self.PmPhone
    def set_contact_email(self,string):
        self.PmEmail=string
        return self.PmEmail

def play_it_again_selena(project_search_result):
    """This Function uses the Selenium module to open and login to EPIC in order to pull data.
    Parameters:
    project-search-result= the url of the page the driver should go to after logging in.

    returns the Javascript rendered HTML of the Epic search result
    """
    from selenium.common.exceptions import TimeoutException,NoSuchElementException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice

    browser.get(str(project_search_result)) #navigate to page behind login
    # Explicit Wait & Expected Conditions
    designation = project_search_result[-10:]
    print(designation)
    wait = WebDriverWait(browser, 10)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[2]/ui-view/div/div[2]/table/tbody/tr/td[2]/a')))
    except (TimeoutException,NoSuchElementException):
        return False

    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    browser.quit()
    return innerHTML

def purell(address_string):
    """this function is rudimentary and regex would definitely be better. regardless this takes a string composed of
    numbers spaces, dashes and letters and separates it either at its second space character or at the first letter"""
    address_number=''
    spacecount = 0
    i=0
    for ch in address_string:
        if ch.isnumeric()==True or ch == '-':
            address_number+= ch
            i+=1
        elif ch.isspace()== True and spacecount<=1:
            spacecount +=1
            i+=1
        elif (ch.isspace()== True and spacecount>= 1):
            street= address_string[i:]
            print(("Address: {} Address Number: {} Address Street: {}").format(address_string, address_number, street))
            return address_number, street
        elif ch.isalpha()==True:
            street= address_string[i-1:]
            print(("Address: {} Address Number: {} Address Street: {}").format(address_string, address_number, street))
            return address_number, street

def sam(address):
    """"uses NYCity Map the address to get the zip code then uses the find nearest feature to find a nearby library
    Parameters:
    address+ address_string from EPIC

    Returns:
        if Library wasn't found the function returns False
        else it returns the js rendered HTML of the site between the document.body tags
    """
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException,NoSuchElementException

    browser = webdriver.Chrome()
    browser.get('https://www.nypl.org/locations/list')
    searchbar = browser.find_element_by_id("searchTerm")
    searchbar.send_keys(address)
    searchgo= browser.find_element_by_id("find-location")
    searchgo.click()

    listview = browser.find_element_by_xpath("//*[@id=\"main-content\"]/div/div[1]/section[2]/div[1]")
    is_active = "active" in listview.get_attribute("class")
    print('list_active', is_active)
    if is_active == False:
        listview = browser.find_element_by_xpath("//*[@id=\"main-content\"]/div/div[1]/section[2]/div[1]")
        listview.click()
    # listview = browser.find_element_by_class_name("list-view-btn") #//*[@id="main-content"]/div/div[1]/section[2]/div[1]

    wait = WebDriverWait(browser, 10) #waits for the (distance) marker to appear
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"main-content\"]/div/div[1]/section[3]/section/div/div/table/tbody/tr[1]/td[1]")))
    except (TimeoutException,NoSuchElementException):
        return False

    innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
    return innerHTML
def CommunityBoard(url):
    """Takes a user to the homepage of the site's Community Board
    parameters:
    url- passed by a DataFrame in the Contact List Window, stored in Community Board Websites.csv
    returns nothing"""
    browser= webdriver.Chrome()
    browser.get(url)

def B_Q_library_search(address_number, street, koq):
    """uses NYCity Map the address to get the zip code then uses the find nearest feature to find a nearby library
    Parameters:
    address_number = 'sanitized' output from purell()
    street= 'sanitized' output from purell()
    koq = these are letters which when typed while a selection dropdown is selected serve to select either queens ('q')
          or Brooklyn('bb')

    Returns:
        if Library wasn't found the function returns False
        else it returns list of strings (taken care of >>)!!the convention of writing city state as "Flushing, NY" means that
        when written to a csv this list will take an extra cell
    """
    from selenium.common.exceptions import TimeoutException,NoSuchElementException
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By
    browser = webdriver.Chrome()
    browser.get('http://maps.nyc.gov/doitt/nycitymap/')
    AdvancedSearch_label = browser.find_element_by_xpath('//*[@id="dijit_layout_ContentPane_0_button_title"]')
    AdvancedSearch_label.click()

    address_number_field = browser.find_element_by_id('dijit_form_ValidationTextBox_1')
    street_name_field = browser.find_element_by_id('dijit_form_ComboBox_0')
    borough_dropdown = browser.find_element_by_id('wm_widget_BoroughCombo_0')
    find_btn = browser.find_element_by_id('dijit_form_Button_2_label')

    address_number_field.send_keys(address_number)
    street_name_field.send_keys(street)
    borough_dropdown.send_keys(str(koq))
    find_btn.click()
    wait= WebDriverWait(browser, 10)
    try:
        zip_there = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"wm_widget_InfoItemRenderer_0\"]/div[1]/div[1]/span[15]")))
    except(TimeoutException,NoSuchElementException):
        return False

    #libary parent fill menu id = dijit_PopupMenuItem_8_text
    # library selection id = dijit_MenuItem_37_text

    find_nearest_tab= browser.find_element_by_id('dijit_layout_ContentPane_13_button_title')
    find_nearest_tab.click()
    choose_dropstart = browser.find_element_by_id('dijit_PopupMenuBarItem_1')
    choose_dropstart.click()

    Res_services_id_item = browser.find_element_by_id('dijit_PopupMenuItem_8_text')
    library_id_item = browser.find_element_by_id('dijit_MenuItem_37_text')
    actions = ActionChains(browser)
    actions.move_to_element(Res_services_id_item)
    actions.click(Res_services_id_item)
    actions.move_to_element(library_id_item)
    actions.perform()
    library_id_item.click()

    lib_find_btn = browser.find_element_by_id('dijit_form_Button_8_label')
    lib_find_btn.click()


    wait = WebDriverWait(browser,10)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id=\"wm_widget_InfoItemRenderer_1\"]/div[1]/div/span[8]")))
    except(TimeoutException, NoSuchElementException):
        return False
    text_elem=[]
    for element in browser.find_elements_by_xpath("//*[@id=\"wm_widget_InfoItemRenderer_1\"]/div[1]/div/span"):
        txt= element.text
        txt= txt.strip(',')
        text_elem.append(txt)
    #Phone Numbers
    if koq =='q':
        browser.get('http://www.queenslibrary.org/branch/'+text_elem[1])
        library_phone = browser.find_element_by_id('phone')
        library_phone=library_phone.text
        library_phone.strip('\n')
        text_elem.append(library_phone)
        browser.quit()
        return text_elem
    elif koq=='bb':
        #switching focus to active tab
        citymaptab=browser.window_handles[0]
        browser.find_element_by_id('wm_widget_DataItemLink_12').click()
        bklnpl=browser.window_handles[1]
        browser.switch_to.window(bklnpl)

        wait=WebDriverWait(browser,10)
        try:
            wait.until(EC.presence_of_element_located((By.ID, "dirbtn")))
        except(TimeoutException,NoSuchElementException) as err:
            print(err)
            return False
        bkphone= browser.find_element_by_class_name("telephone")
        bkphone=bkphone.text
        bkphone=str(bkphone).replace('.','-',3)
        text_elem.append(bkphone)
        browser.quit()
        return text_elem
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
            headers=" VCP Number, Repository URL,Borough, Address, Block, Lot, " \
                    "Site Status, Month and Year,PM Contact, PM Phone, PM Email"
            headers=headers.split(',')
            file.writerow(headers)
            fieldlist = list(vars(object).values())
            file.writerow(fieldlist)
            f.close()
            return "Done"

def WriteTranslations(object, outstring):
    import csv
    with open(str(outstring), 'w', newline='') as f:
        if isinstance(object, Fields) == True:
            file = csv.writer(f, dialect="excel")
            headers = "insert site address,name of local repository,insert site-specific url for RAWP," \
                      "insert site-specific URL for translated CPS, mm/dd/yyyy RAWP comments are due, " \
                      "insert mm/dd/yyyy that the cleanup will start," \
                      "OER project manager name,OER project manager’s phone number," \
                      "OER project manager name and phone number,OER project manager email address"
            " VCP Number, Repository URL,Borough, Address, Block, Lot, " \
            "Site Status, Month and Year,PM Contact, PM Phone, PM Email"
            headers = headers.split(',')
            file.writerow(headers)

            fieldlist = list(vars(object).values())
            file.writerow(fieldlist)
            f.close()
            return "Done"
        elif isinstance(object, NoLibraryMatch) == True:
            file = csv.writer(f, dialect="excel")
            headers = " VCP Number, Repository URL,Borough, Address, Block, Lot, Site Status, Month and Year,PM Contact, PM Phone, PM Email"
            headers = headers.split(',')
            file.writerow(headers)
            fieldlist = list(vars(object).values())
            file.writerow(fieldlist)
            f.close()
            return "Done"

def retrieve_EPIC_html(designation_number=None):
    query_page_base = "https://a002-epic.nyc.gov/app/search/results?query="  # 15CVCP060M goes here
    search = str(query_page_base) + designation_number
    rendered_page_string = play_it_again_selena(search)
    return rendered_page_string

def format_IDs(data):
    # list_of_tuples=[]
    ids = data[0].get_text()
    proj_ids = list(ids.split(','))
    # i=0
    # for item in proj_ids:
    #     list_of_tuples.append((item,i))
    #     i+=1
    print("proj_ids", proj_ids)
    return proj_ids

def return_all_EPIC_fields(rendered):
    alphabet = BeautifulSoup(rendered, 'lxml')
    row = alphabet.find('tr', class_='ng-scope')
    data = row.find_all('td')
    ad= data[3].get_text()
    return data, ad

def man_stat_bronx(data,ad):
    libraryHTML = sam(ad)

    if libraryHTML!= False:
        soup = BeautifulSoup(libraryHTML, 'lxml')
        results = soup.find('table', class_='locations-list-view')
        first_result = results.find('td', class_='location-info')

        lib_name = first_result.find('div', class_='p-org').get_text()
        lib_adr = first_result.find('div', class_='p-adr').get_text()
        lib_phone = first_result.find('div', class_='p-tel').get_text()
        lib_adr=lib_adr.split(',')
        stripped_adr= ''
        t=0
        for field in lib_adr:
            field= field.strip().strip('\n')
            stripped_adr+=field+' '
            t+=1
            print(t,field)
        print(stripped_adr)
        if '\n' in stripped_adr:
            stripped_adr.replace('\n',' ',)
        repository = 'https://a002-epic.nyc.gov' + str(data[1].find('a').get('href'))
        complete_adr = lib_name.strip().strip('\n')+ ' ' + stripped_adr
        codify = Fields(None, repository, data[2].get_text(), data[3].get_text(),
                        data[4].get_text(),None, data[5].get_text(), strftime('%B %Y', gmtime()), complete_adr,
                        lib_phone.strip('\n'),None,None,None)

        return codify
    else:
        raise ValueError("Could not find a nearby library for {}".format(ad))

def queens(data,ad):
    (ad_number, ad_street) = purell(ad)
    library_address = B_Q_library_search(ad_number, ad_street, 'q')
    if library_address != False:
        lib_name = library_address[1]
        library_boo = str(lib_name) + ' '
        for item in library_address[2:6]:
            library_boo += str(item + ' ')
        print(library_boo)

        repository = 'https://a002-epic.nyc.gov' + str(data[1].find('a').get('href'))

        codify = Fields(None, repository, data[2].get_text(), data[3].get_text(),
                        data[4].get_text(), None, data[5].get_text(), strftime('%B %Y', gmtime()), library_boo,
                        library_address[-1],None,None,None)
        return codify
    else:
        raise ValueError("Could not find a nearby library for #: {} Street: {}".format(ad_number, ad_street))

def brooklyn(data,ad):
    (ad_number, ad_street) = purell(ad)
    library_address = B_Q_library_search(ad_number, ad_street, 'bb')
    if library_address !=False:
        lib_name = library_address[1]
        library_boo = str(lib_name) + ' '
        for item in library_address[2:6]:
            library_boo += str(item + ' ')
        print(library_boo)

        repository = 'https://a002-epic.nyc.gov' + str(data[1].find('a').get('href'))

        codify = Fields(None, repository, data[2].get_text(), data[3].get_text(),
                        data[4].get_text(), None, data[5].get_text(), strftime('%B %Y', gmtime()), library_boo,
                        library_address[-1],None,None,None)
        return codify
    else:
        raise ValueError("Could not find a nearby library for #: {} Street: {}".format(ad_number,ad_street))

def no_libary_found(data,ad):
    repository = 'https://a002-epic.nyc.gov' + str(data[1].find('a').get('href'))

    codify = NoLibraryMatch(None, repository, data[2].get_text(), data[3].get_text(),
                    data[4].get_text(), None, data[5].get_text(), strftime('%B %Y', gmtime()),None,None,None)
    return codify

def return_codify(data,address_string):
    borough= data[2].get_text()
    borough=borough.lower()

    if borough in ['manhattan', 'bronx', 'staten island']:
        #Staten Island, the Bronx, and Manhattan are all served by the NYPL network and projects located in these
        # boroughs can be easily found
        try:
            codify=man_stat_bronx(data,address_string)
        except ValueError:
            codify=no_libary_found(data,address_string)
        return codify
    elif borough == 'queens':
        try:
            codify=queens(data,address_string)
        except ValueError:
            codify = no_libary_found(data, address_string)
        return codify
    elif borough == "brooklyn":
        try:
            codify=brooklyn(data,address_string)
        except ValueError:
            codify = no_libary_found(data, address_string)
        return codify




"""
# file = open('rendered library html.txt', 'w')
# file.write(libraryHTML)
# file.close()
# lElem=html.fromstring(libraryHTML)
# lib_name = lElem.xpath("//*[@id=\"wm_widget_InfoItemRenderer_1\"]/div[1]/div/span[2]").text
# lib_house_numb= lElem.xpath("//*[@id=\"wm_widget_InfoItemRenderer_1\"]/div[1]/div/span[3]").text
# lib_street_name = lElem.xpath("//*[@id=\"wm_widget_InfoItemRenderer_1\"]/div[1]/div/span[4]").text
# lib_city = lElem.xpath("//*[@id=\"wm_widget_InfoItemRenderer_1\"]/div[1]/div/span[5]").text
# lib_zip = lElem.xpath("//*[@id=\"wm_widget_InfoItemRenderer_1\"]/div[1]/div/span[6]").text
# s = ' '
# library_adr = str(lib_name + s + lib_house_numb + s + lib_street_name + s + lib_city + s + lib_zip)

# url = "https://a858-login2.nyc.gov/osp/a/t1/auth/saml2/sso"
# browser.get(url) #navigate to the page
# 
# 
# #Logging in:
# username = browser.find_element_by_id("Ecom_User_ID") #username form field
# password = browser.find_element_by_id("Ecom_Password") #password form field
# 
# username.send_keys("#############")
# password.send_keys("@@@@@@@@@@@@@@@@")
# 
# submitButton = browser.find_element_by_xpath("//*[@id=\"int-users\"]/div[3]/section/div/div[2]/div[1]/div/form/div[3]/button").click()

# def goo(address):
#     from selenium.webdriver.common.keys import Keys
#     "googles if its not a manhattan Public Library"
#     browser = webdriver.Chrome()
#     browser.get('https://www.google.com/')
#     searchbar = browser.find_element_by_id('lst-ib')
#     searchbar.send_keys('public libraries near '+ address)
#     searchbar.send_keys(Keys.RETURN)
# 
#     # resultstable= browser.

# browser.get('http://www.queenslibrary.org/ql_findabranch')
#     searchtab = browser.find_element_by_id('quicktabs-tab-qtb_find_library-0').click()
#     searchbar= browser.find_element_by_id('frmsearch')
#     searchbar.send_keys(zip_string)
#     searchbar.send_keys(Keys.RETURN)
# 
#     wait = WebDriverWait(browser, 10)
#     link_there= wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"block-ql_set_branch-9\"]/div/table/tbody/tr/td[1]/table[1]")))
    
Doc Repository:
#app > div.app-content.ng-scope > div.app-content-body.fade-in-up > div.ng-scope > ui-view > div > div:nth-child(2) 
> table > tbody > tr > td:nth-child(1) > a

Borough:
#app > div.app-content.ng-scope > div.app-content-body.fade-in-up > div.ng-scope > ui-view > div > div:nth-child(2) 
> table > tbody > tr > td:nth-child(3)

Address:
#app > div.app-content.ng-scope > div.app-content-body.fade-in-up > div.ng-scope > ui-view > div > div:nth-child(2) 
> table > tbody > tr > td:nth-child(4)

Block and Lot:
#app > div.app-content.ng-scope > div.app-content-body.fade-in-up > div.ng-scope > ui-view > div > div:nth-child(2) 
> table > tbody > tr > td:nth-child(5)

Project Status:
#app > div.app-content.ng-scope > div.app-content-body.fade-in-up > div.ng-scope > ui-view > div > div:nth-child(2) 
> table > tbody > tr > td:nth-child(6)
"""












