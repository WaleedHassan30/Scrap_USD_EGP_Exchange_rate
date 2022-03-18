import requests , pandas , csv
from bs4 import BeautifulSoup as bs
from pathlib import Path
from datetime import datetime
        ##################################################################
class script:
    def __init__(self,name_file="log_exchanges.csv"):
        self.api_get = requests.get("https://www.exchangerates.org.uk/Dollars-to-Egyptian-Pounds-currency-conversion-page.html")
        self.soup = bs(self.api_get.text,"html.parser")
        self.exchange_rate = None
        self.amount = ""
        self.result = ""
        self.last_update_date = ""
        self.last_update_time = ""
        self.creation_Date = ""
        self.temp = False
        self.file_data = {}
        self.log_exchanges = name_file
        ##################################################################
    def get_exchange_rate(self):
        self.exchange_rate = self.soup.find(class_="p_conv30",)
        self.exchange_rate = self.soup.find(id="shd2b;").text
        return float(self.exchange_rate)
        ##################################################################
    def get_date_time(self):
        date = list(self.soup.findAll(class_="p_conv"))[1]
        str_date=str(date).split('The Dollar to Egyptian Pound exchange rate (USD EGP) as of ')[1].split('.</p>\n</div>')[0].split('at')
        self.last_update_date = str_date[0]
        self.last_update_time = str_date[1]
        return f" last update {self.last_update_date} at{self.last_update_time}"
        ##################################################################
    def calculate(self):
        self.get_exchange_rate()
        self.amount = int(input("Enter amount in USD: "))
        self.result = round(self.amount * self.get_exchange_rate(),3)
        print(f"{self.amount} USD = {self.result} LE. | Exchange rate is: {self.exchange_rate} | {self.get_date_time()}")
        print(f"saved data to {self.log_exchanges}")
        print("ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ")
        ##################################################################
    def get_creation_Date(self):
        now = datetime.now()
        self.creation_Date = now.strftime("%d/%m/%y %H:%M:%S")
        ##################################################################
    def create_data_dict(self):
                self.get_creation_Date()       
                self.file_data["USD"]=self.amount
                self.file_data["LE"]=self.result
                self.file_data["Rate"]=self.exchange_rate
                self.file_data["Last Update Date"]=self.last_update_date
                self.file_data["Last Update Time"]=self.last_update_time
                self.file_data["Creation Date"]=self.creation_Date
        ##################################################################
    def save_data(self):
            self.create_data_dict()
            if Path(self.log_exchanges).is_file(): 
                self.log_save()
            else:
                with open(self.log_exchanges,"w+",newline="")as create_file:
                   writer = csv.DictWriter(create_file,fieldnames=["USD","LE","Rate","Last Update Date","Last Update Time","Creation Date"])
                   writer.writeheader()
                   writer.writerow(self.file_data)
        ##################################################################
    def log_save(self):
        self.create_data_dict()
        with open(self.log_exchanges,"r+",newline="")as read_row:
                row = read_row.readline()
                if "USD" in row:
                        self.temp = True
                else:
                        self.temp = False
                if self.temp ==True:
                    with  open(self.log_exchanges,"a",newline="") as f:
                        writer = csv.DictWriter(f,fieldnames=["USD","LE","Rate","Last Update Date","Last Update Time","Creation Date"])
                        writer.writerow(self.file_data)
                else:
                    with  open(self.log_exchanges,"w+",newline="") as f:
                        writer = csv.DictWriter(f,fieldnames=["USD","LE","Rate","Last Update Date","Last Update Time","creation date"])
                        writer.writeheader()
        ##################################################################              
    def Show_Table(self):
        table = pandas.read_csv(self.log_exchanges)
        print(table)
        ##################################################################
    def main(self):
        print("                Convert USD to EGP at the real exchange rate                     ")
        print("ــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــــ")
        self.calculate()
        self.save_data()
        self.Show_Table()
        ########################### END ###############################