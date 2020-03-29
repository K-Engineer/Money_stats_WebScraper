# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:49:51 2020

@author: Nikhil Nagar

"""

#packages to insatll >> pip install bs4
#                       pip install requests
#                       


from bs4 import BeautifulSoup
import requests
import pandas
import time
import numpy


#basic function for collection of data and return a dataframe
def collect_data():
    url = "https://www.moneycontrol.com/stocks/marketstats/indexcomp.php?optex=NSE&opttopic=indexcomp&index=9"
    res = requests.get(url)
    soup = BeautifulSoup(res.content,'html.parser')
    page_table = soup.find_all('table',{"class":"tbldata14 bdrtpg"})
    table_rows = page_table[0].find_all('tr')[1:]
    list_of_dict=[]
    
    for row in table_rows:
        dict_row ={}
        name_industry = row.find_all('b')
        numerical_data = row.find_all('td',{"align":"right"})
        dict_row['company_name'] = name_industry[0].text
        dict_row['industry'] = name_industry[1].text
        dict_row['last_price'] = float(numerical_data[0].text.replace(',',''))
        dict_row['change'] = float(numerical_data[1].text.replace(',',''))  
        dict_row['percent_change'] =float(numerical_data[2].text.replace(',',''))
        dict_row['market_cap'] = float(numerical_data[3].text.replace(',',''))
        list_of_dict.append(dict_row)
    #collecting data and creating a dataframe
    df = pandas.DataFrame(list_of_dict)
    return df
    


#this function will alert in every 2 minutes,if change is more than 2% for any company
def indicator_alert_function():
    while(True):
        print("\nAlert executing... please wait for 2 minutes for collection of 2 instances of dataset.")
        data_instance_1 = collect_data()
        time.sleep(30) #sleep for 2 minutes
        data_instance_2 = collect_data()
        alert_index_list=[]
        difference_arr = numpy.subtract(data_instance_1["percent_change"],data_instance_2["percent_change"])
       
        for i in range(0,len(difference_arr)):
            if(abs(difference_arr[i])>=0.7):
                alert_index_list.append(i)
        print("Changes in %change for companies\n",difference_arr)      
        if(alert_index_list==[]):
            print("No significant change(more than 2.0) detected for any company.")
        else:
            for i in alert_index_list:
                print("!!!!!!! Alert : ",data_instance_2["company_name"][i],"has change of",abs(difference_arr[i])+1.5)
    

    
#this function works for 20 minutes and save the stock data into csv file in 30 seconds frequecny
def save_realtime_data_30_seconds_frequency_for_20_minutes():   
    timeout = 60*20 # [seconds] to run the loop for 20 minutes
    timeout_start = time.time()
    while (time.time() < timeout_start + timeout):
        stock_table = collect_data()
        stock_table.to_csv('stock_market_data.csv')
        print("\nfor full data...check csv file\n")
        print(stock_table)
        print("wait for 30 seconds for next realtime update in table.\n csv file is saved.")
        time.sleep(30)




#main function to start execution
if __name__  == "__main__":
    print("Choose Option.  \n >  1. (Collect realtime stock data for next 20 minutes)\n >  2. (enable alert for %change indicator in every 2 minutes)")
    i=input("enter option- '1' or '2' >>> ")
    if(i=='1'):
        save_realtime_data_30_seconds_frequency_for_20_minutes()
    elif(i=='2'):
        indicator_alert_function()
    else:
        print("invalid option")
    



#instructions : Do not open csv file while running the script. it will affect the running script as script is updating the opened csv file.
#               if significant change  not dectected in alert for 2 minutes interval....try to increase the interval more than 2 minutes.

    








    


          
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
