import datetime
from datetime import date

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.snackbar import Snackbar

Window.size = (310, 580)


class TodoCard(FakeRectangularElevationBehavior, MDFloatLayout):
    appliance = StringProperty()
    quantity = StringProperty()
    hours = StringProperty()
    wattage = StringProperty()

class UsageCard(FakeRectangularElevationBehavior, MDFloatLayout):
    appliance = StringProperty()
    quantity = StringProperty()
    hours = StringProperty()
    wattage = StringProperty()


class GreenEnergy(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.current_date = None
        self.previous_date = None
        self.current_date = self.current_date
        self.previous_date = self.previous_date


    def build(self):

        self.title = 'GreenEnergy'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"

        global screen_manager

        screen_manager = ScreenManager()

        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("dashboard.kv"))

        screen_manager.add_widget(Builder.load_file("facility.kv"))
        screen_manager.add_widget(Builder.load_file("appliance.kv"))
        screen_manager.add_widget(Builder.load_file("appliance_additem.kv"))

        screen_manager.add_widget(Builder.load_file('bill.kv'))
        screen_manager.add_widget(Builder.load_file('analysis.kv'))
        screen_manager.add_widget(Builder.load_file('usage_main.kv'))

        screen_manager.add_widget(Builder.load_file('contact.kv'))
        screen_manager.add_widget(Builder.load_file('rate.kv'))

        return screen_manager

    def on_start(self):
        today = date.today()
        wd = date.weekday(today)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))

        #screen_manager.get_screen("usage_main").dates.text = f"{days[wd]}, {day} {month} {year}"


    def on_complete(self, checkbox, value, quantity, bar):
        if value:
            #quantity.text = f"[s]{quantity.text}[/s]"
            bar.md_bg_color = 0, 179 / 255, 0, 1

            #################################
            firebase_connector = True

            #######################################

        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                quantity.text = quantity.text.replace(i, "")
                bar.md_bg_color = 1, 170 / 255, 23 / 255, 1


    ###################################################################

    def usage_data(self):

        """if appliance == "" and quantity == "" and hours == "" and wattage == "" and len(appliance) < 21 and len(quantity) < 11 and len(hours) < 3 and len(wattage) < 6:
            screen_manager.current = "appliance"
            screen_manager.transition.direction = "right" """
        """appliance = 'Bulb'
        quantity = '2'
        hours = '3'
        wattage = '6'"""

        ######################################################

        # print("Valid Email")
        from firebase import firebase

        # Initialize Firebase
        firebase = firebase.FirebaseApplication('https://ge-app-71310-default-rtdb.firebaseio.com/', None)

        try:

            result = firebase.get('ge-app-71310-default-rtdb/ApplianceData', '')
            total = 0
            etotal = 0
            d_cost = 0
            m_cost = 0
            y_cost = 0

            for e in result.keys():
                etotal = etotal + 1


            for i in result.keys():
                total = total + 1

                """print(result[i]['Appliance'])
                print(result[i]['Quantity'])
                print(result[i]['Hours'])
                print(result[i]['Wattage'])"""

                ############################################################

                ############################################################
                """quan = str(result[i]['Quantity'])
                if len(quan) > 1:
                    appls = "s"
"""
                quan_len = int(result[i]['Quantity'])
                appl_name = result[i]['Appliance']
                if quan_len > 1:
                    appl_name = f"{appl_name} - No.: {str(quan_len)}"

                kWh_cost = int(result[i]['Hours']) * int(result[i]['Wattage'])
                d_cost = d_cost + kWh_cost
                kWm_cost = kWh_cost * 30
                m_cost = m_cost + kWm_cost
                kWy_cost = kWm_cost * 12
                y_cost = y_cost + kWy_cost

                appl = appl_name  # str(result[i]['Appliance'])
                # appl = f"{apple}'({s})"
                daily_cost = str(f"Ksh. {kWh_cost}, Daily.")
                monthly_cost = str(f"Ksh. {kWm_cost}, Monthly.")
                yearly_cost = str(f"Ksh. {kWy_cost}, Annually.")

                screen_manager.get_screen("usage_main").todo_list.add_widget(
                    UsageCard(appliance=appl, quantity=daily_cost, hours=monthly_cost, wattage=yearly_cost))


            tt_name = f"Total Appliances: {total}"
            d_name = f"Daily Cost: {str(d_cost)}"
            m_name = f"Monthly Cost: {str(m_cost)}"
            y_name = f"Yearly Cost: {str(y_cost)}"

            screen_manager.get_screen("usage_main").todo_list.add_widget(
                UsageCard(appliance=tt_name, quantity=d_name, hours=m_name, wattage=y_name))




        except:
            pass
            # print("An Error Occurred.")

        ######################################################

        ###################################################################

    def add_todo(self, appliance, quantity, hours, wattage):

        appliance = str(appliance.lower())
        quantity = str(quantity.lower())
        hours = str(hours.lower())
        wattage = str(wattage.lower())


        if appliance != "" and quantity != "" and hours != "" and wattage != "" and len(appliance) < 21 and len(
                quantity) < 11 and len(hours) < 3 and len(wattage) < 6:
            screen_manager.current = "appliance"
            screen_manager.transition.direction = "right"

            s_plus = ""
            try:
                if int(quantity) > 1:
                    s_plus = "s"
            except:
                pass

            tappliance = f"Name: {appliance}"
            tquantity =  f"Quantity: {str(quantity)} Item{s_plus}"
            thours =     f"Usage:    {str(hours)} Hours"
            twattage =   f"Wattage: {str(wattage)} Watts"

            screen_manager.get_screen("appliance").todo_list.add_widget(
                TodoCard(appliance=tappliance, quantity=tquantity, hours=thours, wattage=twattage))
            #screen_manager.get_screen("add_appliance").quantity.text = ""


            ##############################################

            from firebase import firebase

            # Initialize Firebase
            firebase = firebase.FirebaseApplication('https://ge-app-71310-default-rtdb.firebaseio.com/', None)

            try:

                a_result = firebase.get('ge-app-71310-default-rtdb/ApplianceData', '')
                print(" ")
                # print(f_result)

            except:
                print(" ")
                # print("There is no data in the Facility Database.")

            a_result = firebase.get('ge-app-71310-default-rtdb/ApplianceData', '')

            if a_result is None:
                # print(">>> No data in the facility database.")
                print(" ")

                new_appliance_data = {
                    'Appliance': appliance,
                    'Quantity': quantity,
                    'Hours': hours,
                    'Wattage': wattage

                }

                firebase.post('ge-app-71310-default-rtdb/ApplianceData', new_appliance_data)
                # print(institution + " data inserted successfully!")

            else:
                global ttotal
                ttotal = 0
                for i in a_result.keys():
                    ttotal = ttotal + 1

                    if a_result[i]['Appliance'] == appliance:
                        if a_result[i]['Quantity'] == quantity:
                            pass
                            # print("Facility Data already exists.")


                new_appliance_data = {
                    'Appliance': appliance,
                    'Quantity': quantity,
                    'Hours': hours,
                    'Wattage': wattage

                }

                firebase.post('ge-app-71310-default-rtdb/ApplianceData', new_appliance_data)
                # print(institution + " data inserted into Facility Database!")"""

            ##############################################

            # print(appliance)
            # print(quantity)
            # print(hours)
            # print(wattage)


        elif appliance == "":
            Snackbar(text="Appliance name is missing.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif quantity == "":
            Snackbar(text="Quantity value is missing.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif hours == "":
            Snackbar(text="Hours of consumption required.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif wattage == "":
            Snackbar(text="Power rating is needed.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif len(appliance) > 21:
            Snackbar(text="Appliance name exceeds 20 characters.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif len(quantity) > 10:
            Snackbar(text="Quantity value exceeds limit.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif len(hours) > 2:
            Snackbar(text="Hour value exceeds limit.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif len(wattage) > 5:
            Snackbar(text="Wattage value exceeds limit.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

    ##########################################################

    def get_data(self, institution, facility, room, nationalid):
        institution = str(institution.lower())
        facility = str(facility.lower())
        room = str(room.lower())
        nationalid = str(nationalid.lower())


        if institution != "" and facility != "" and room != "" and nationalid != "" and len(institution) > 5 and len(
                facility) > 3 and len(room) >= 1 and len(nationalid) >= 8:
            screen_manager.current = "appliance"
            screen_manager.transition.direction = "right"

            from firebase import firebase

            # Initialize Firebase
            firebase = firebase.FirebaseApplication('https://ge-app-71310-default-rtdb.firebaseio.com/', None)

            try:

                f_result = firebase.get('ge-app-71310-default-rtdb/FacilityData', '')
                #print(" ")
                # print(f_result)

            except:
                pass
                #print(" ")
                # print("There is no data in the Facility Database.")

            if f_result is None:
                pass
                # print(">>> No data in the facility database.")
                #print(" ")

                new_facility_data = {
                    'Institution': institution,
                    'Facility': facility,
                    'Room': room,
                    'NationalID': nationalid

                }

                firebase.post('ge-app-71310-default-rtdb/FacilityData', new_facility_data)
                # print(institution + " data inserted successfully!")

            else:
                for i in f_result.keys():

                    if f_result[i]['Room'] == room:
                        if f_result[i]['NationalID'] == nationalid:
                            pass
                            #print(" ")
                            # print("Facility Data already exists.")

                    else:
                        pass
                        #print(" ")
                        # print("Facility Data does not exist.")

                        new_facility_data = {
                            'Institution': institution,
                            'Facility': facility,
                            'Room': room,
                            'NationalID': nationalid

                        }

                        firebase.post('ge-app-71310-default-rtdb/FacilityData', new_facility_data)
                        # print(institution + " data inserted into Facility Database!")"""

        elif institution == "":
            Snackbar(text="Institution name required.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif facility == "":
            Snackbar(text="Facility name required.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif room == "":
            Snackbar(text="Room identifier required.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif nationalid == "":
            Snackbar(text="Occupant's ID required.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()





    ##########################################################################

    def send_email(self, name, email, message):
        name = str(name.lower())
        email = str(email.lower())
        message = str(message.lower())

        if name == "":
            Snackbar(text="Name is required.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif email == "":
            Snackbar(text="Email address is required.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        elif message == "":
            Snackbar(text="Message is required.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

        else:
            Snackbar(text="Message sent successfully.", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

            ###########################################

            import re
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if (re.fullmatch(regex, email)):
            # print("Valid Email")

                from firebase import firebase

                # Initialize Firebase
                firebase = firebase.FirebaseApplication('https://ge-app-71310-default-rtdb.firebaseio.com/', None)

                try:

                    c_result = firebase.get('ge-app-71310-default-rtdb/ContactData', '')

                    if c_result is None:
                        # print(">>> No data in the facility database.")
                        # print(" ")

                        new_contact_data = {
                            'Name': name,
                            'Email': email,
                            'Message': message

                        }

                        firebase.post('ge-app-71310-default-rtdb/ContactData', new_contact_data)
                        # print(institution + " data inserted successfully!")

                    else:
                        for i in c_result.keys():

                            if c_result[i]['Name'] == name:
                                if c_result[i]['Email'] == email:
                                    screen_manager.current = "dashboard"
                                    screen_manager.transition.direction = "left"
                                    # print(" ")
                                    # print("Facility Data already exists.")

                            else:
                                # pass
                                # print(" ")
                                # print("Facility Data does not exist.")

                                new_contact_data = {
                                    'Name': name,
                                    'Email': email,
                                    'Message': message

                                }

                                firebase.post('ge-app-71310-default-rtdb/ContactData', new_contact_data)
                                # print(institution + " data inserted into Facility Database!")"""

                                screen_manager.current = "dashboard"
                                screen_manager.transition.direction = "left"
                except:
                    pass
                    #print(" ")
                    # print("There is no data in the Facility Database.")



            else:
                # print("Invalid Email")
                Snackbar(text="Invalid Email. Try Again.", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                         bg_color=(1, 170 / 255, 23 / 255, 1),
                         font_size="18sp").open()
            ###########################################

        """# print(name, email, message)
        email = open("email.txt").read()
        password = open("password.txt").read()
        name = ''
        email = ''
        msg = EmailMessage()
        msg["Subject"] = "New Contact Form Enquiry"
        msg["To"] = "jkilonzo2022@gmail.com"
        msg["From"] = formataddr(name.text, sender_email.text)

        msg.set_content(f"Hi, My Name is {name.text}. \n {message.text}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)

        name.text = ''
        email.text = ''
        message.text = ''"""

    ####################################################################

    def starone(self):
        if True:
            Snackbar(text="Rated 'worst' successfully.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

    def startwo(self):
        if True:
            Snackbar(text="Rated 'bad' successfully.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

    def starthree(self):
        if True:
            Snackbar(text="Rated 'not bad' successfully.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

    def starfour(self):
        if True:
            Snackbar(text="Rated 'cool' successfully.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

    def starfive(self):
        if True:
            Snackbar(text="Rated 'best' successfully.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()


    def rate_message(self, comment):
        if comment == "":
            Snackbar(text="Comment is required.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        else:
            Snackbar(text="Comment sent successfully.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

            screen_manager.current = "dashboard"
            screen_manager.transition.direction = "left"


    ##########################################################3

    def on_previous_save(self, instance, value, date_range):
        global pdate_chunks
        global pvalue_str
        if not value == "":
            previous_date = value
            pvalue_str = str(value)
            Snackbar(text="Previous date is " + pvalue_str + " .", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
            pdate_chunks = pvalue_str.split("-")
            #print(pdate_chunks)


    def on_previous_cancel(self, instance, value):
        pass

    def show_previous_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_previous_save, on_cancel=self.on_previous_cancel)
        date_dialog.open()


    def on_current_save(self, instance, value, date_range):
        global cdate_chunks
        global cvalue_str
        if not value == "":
            current_date = value
            cvalue_str = str(value)
            Snackbar(text="Current date is " + cvalue_str + " .", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
            cdate_chunks = cvalue_str.split("-")
            #print(cdate_chunks)


    def on_current_cancel(self, instance, value):
        pass

    def show_current_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_current_save, on_cancel=self.on_current_cancel)
        date_dialog.open()

    def bill_data(self, lastreading, currentreading):
        import time
        import datetime
        from datetime import datetime
        from dateutil.parser import parse
        #print(pdate_chunks)
        #print(cdate_chunks)

        try:

            lpdate_chunks = str(pvalue_str)
            lcdate_chunks = str(cvalue_str)

            td = parse(lcdate_chunks) - parse(lpdate_chunks)

            lastreading = int(lastreading)
            currentreading = int(currentreading)
            meter_difference = currentreading - lastreading
            # meter_difference = str(meter_difference)

            kWh_kSh = 15.61
            bill_Days = td.days

            tt = bill_Days * kWh_kSh * meter_difference

            # print(f"Your bill is Ksh. {tt} .")

            if lastreading and currentreading:
                Snackbar(text=f"Your bill is Ksh. {tt} .", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                         font_size="18sp").open()
                #time.sleep(30)
                screen_manager.current = "dashboard"
                screen_manager.transition.direction = "left"

        except:
            pass




    ###########################################################################

    # Defining the get_data() function
    # def send_data(self, email, password):

    def pass_test(self):
        import hashlib

        salt = b''  # Get the salt you stored for *this* user
        #key = b''  # Get this users key calculated

        salt1 = b''  # Get the salt you stored for *this* user
        #key1 = b''

        password_to_check = 'qwerty'  # The password provided by the user to check

        # Use the exact same setup you used to generate the key, but this time put in the password to check
        new_key = hashlib.pbkdf2_hmac(
            'sha256',
            password_to_check.encode('utf-8'),  # Convert the password to bytes
            salt,
            100000
        )

        new_key1 = hashlib.pbkdf2_hmac(
            'sha256',
            password_to_check.encode('utf-8'),  # Convert the password to bytes
            salt1,
            100000
        )

        if new_key == new_key1:
            print('Password is correct')
        else:
            print('Password is incorrect')

    def signup_data(self, nickname, new_email, new_password):
        from firebase import firebase
        nickname = str(nickname.lower())
        new_email = str(new_email.lower())
        new_password = str(new_password.lower())


        import re
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, new_email)):
            #print("Valid Email")



            # Initialize Firebase
            firebase = firebase.FirebaseApplication('https://ge-app-71310-default-rtdb.firebaseio.com/', None)

            try:

                result = firebase.get('ge-app-71310-default-rtdb/Users', '')
                # print(result)

                if (result == None):
                    """print(">>> No data in the database.")
                    print("### Attempting a database insertion.")
                    print(" ")
                    print(">>> Testing Step Two.")"""

                    try:
                        new_data = {
                            'Nickname': nickname,
                            'Email': new_email,
                            'Password': new_password

                        }

                        firebase.post('ge-app-71310-default-rtdb/Users', new_data)
                        # print(nickname + " account created successfully!")

                    except:

                        pass


                else:
                    for i in result.keys():

                        if result[i]['Email'] == new_email:
                            if result[i]['Password'] == new_password:
                                pass
                                # print("Account already exists.")
                                # account = 0

                                Snackbar(text="Account already exists.", snackbar_x="10dp", snackbar_y="10dp",
                                         size_hint_y=.08,
                                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                                         bg_color=(1, 170 / 255, 23 / 255, 1),
                                         font_size="18sp").open()
                                if new_email != "" and new_password != "" and len(new_email) > 1 and len(
                                        new_password) > 1:
                                    screen_manager.current = "login"
                                    screen_manager.transition.direction = "right"

                        else:
                            new_data = {
                                'Nickname': nickname,
                                'Email': new_email,
                                'Password': new_password

                            }

                            firebase.post('ge-app-71310-default-rtdb/Users', new_data)
                            # print(nickname + " account created successfully!")

                            Snackbar(text="Account created successfully.", snackbar_x="10dp", snackbar_y="10dp",
                                     size_hint_y=.08,
                                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                                     bg_color=(1, 170 / 255, 23 / 255, 1),
                                     font_size="18sp").open()
                            if new_email != "" and new_password != "" and len(new_email) > 1 and len(
                                    new_password) > 1:
                                screen_manager.current = "login"
                                screen_manager.transition.direction = "right"



            except:
                pass
                # print("An Error Occurred.")

        else:
            #print("Invalid Email")
            Snackbar(text="Invalid Email. Try Again.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
            if new_email != "" and new_password != "" and len(new_email) > 1 and len(new_password) > 1:
                screen_manager.current = "signup"
                screen_manager.transition.direction = "left"



    def signin_data(self, email, password):

        email = str(email.lower())
        password = str(password.lower())

        import re
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex, email)):

            # print("Valid Email")
            from firebase import firebase

            # Initialize Firebase
            firebase = firebase.FirebaseApplication('https://ge-app-71310-default-rtdb.firebaseio.com/', None)

            try:

                result = firebase.get('ge-app-71310-default-rtdb/Users', '')
                #print(result)

                if result == None:
                    if result == "":
                        Snackbar(text="Please, create an account.", snackbar_x="10dp", snackbar_y="10dp",
                                         size_hint_y=.08,
                                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                                         bg_color=(1, 170 / 255, 23 / 255, 1),
                                         font_size="18sp").open()
                        if email != "" and password != "" and len(email) > 1 and len(password) > 1:
                            screen_manager.current = "signup"
                            screen_manager.transition.direction = "left"

                        #firebase.post('greenenergydb-default-rtdb/Users', new_data)
                        # print(email + " account created successfully!")

                    else:
                        Snackbar(text="Please, create an account.", snackbar_x="10dp", snackbar_y="10dp",
                                 size_hint_y=.08,
                                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                                 bg_color=(1, 170 / 255, 23 / 255, 1),
                                 font_size="18sp").open()
                        if email != "" and password != "" and len(email) > 1 and len(password) > 1:
                            screen_manager.current = "signup"
                            screen_manager.transition.direction = "left"


                else:
                    for k in result.keys():
                        global waypass
                        if result[k]['Email'] == email:

                            for i in result.keys():

                                if result[i]['Email'] == email:
                                    # print(email)
                                    # print(result[i]['Nickname'])

                                    if result[i]['Password'] == password:
                                        waypass = "Yes"
                                        # print(password)
                                        # print("Account already exists.")
                                        usernickname = result[i]['Nickname']
                                        usernickname = usernickname.upper()

                                        Snackbar(text=f"Welcome, @ {usernickname}.", snackbar_x="10dp", snackbar_y="10dp",
                                                 size_hint_y=.08,
                                                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                                                 bg_color=(1, 170 / 255, 23 / 255, 1),
                                                 font_size="18sp").open()

                                        if email != "" and password != "" and len(email) > 11 and len(password) > 1:
                                            screen_manager.current = "dashboard"
                                            screen_manager.transition.direction = "right"


                    if waypass == "Yes":
                        pass
                    else:
                        Snackbar(text="Please, create an account.", snackbar_x="10dp", snackbar_y="10dp",
                                 size_hint_y=.08,
                                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                                 bg_color=(1, 170 / 255, 23 / 255, 1),
                                 font_size="18sp").open()
                        if email != "" and password != "" and len(email) > 1 and len(password) > 1:
                            screen_manager.current = "signup"
                            screen_manager.transition.direction = "left"


            except:
                pass
                # print("An Error Occurred.")

        else:
            # print("Invalid Email")
            Snackbar(text="Invalid Email. Try Again.", snackbar_x="10dp", snackbar_y="10dp",
                     size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
            if email != "" and password != "" and len(email) > 1 and len(password) > 1:
                screen_manager.current = "signup"
                screen_manager.transition.direction = "left"





if __name__ == "__main__":
    GreenEnergy().run()
