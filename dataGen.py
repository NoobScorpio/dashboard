
from random import seed
from random import random
from random import uniform
from random import randint
from random import randrange
from datetime import timedelta
from datetime import datetime
import pandas as pd



print('STARTED')

df = pd.read_csv('data/genData.csv')
print('DATA OPENED')

df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'])
print('CONVERTED TO DATES')

df['Year']=df['InvoiceDate'].dt.year
print('YEARS CREATED')

df['Month']=df['InvoiceDate'].dt.month
print('MONTHS CREATED')

df['Day']=df['InvoiceDate'].dt.day
print('DAYS CREATED')

df['TotalCost']=df['Cost']*df['Qnty']
print('COSTS CREATED')

df['TotalPrice']=df['Price']*df['Qnty']
print('PRICES CREATED')

df['TotalProfit']=df['TotalPrice']-df['TotalCost']-df['Discount']
print('PROFITS CREATED')

print('SAVING DATA...')
pd.to_csv('data/genData.csv')
print('SAVED')
# d1 = datetime.strptime('1/1/2005 1:30 PM', '%m/%d/%Y %I:%M %p')
# d2 = datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p')

# invoice=0
# invoiceNo=[]
# itemNo=[]
# items=dict()
# cost=[]
# qnty=[]
# cust=1
# discount=[]
# dates=[]
# custNo=[]
# price=[]

# def random_date(start, end):
#     """
#     This function will return a random datetime between two datetime 
#     objects.
#     """
#     delta = end - start
#     int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
#     random_second = randrange(int_delta)
#     return start + timedelta(seconds=random_second)

# date=random_date(d1,d2)

# for i in range(1,6331):
#     items[i]=uniform(0.5,65160.5)


# print('Making Data Set')
# for i in range(0,20000000):
#     if i%25==0:
#         invoice=invoice+1
#         date=random_date(d1,d2)
#         cust=randint(1,1500)
#     invoiceNo.append(invoice)
#     no=randint(1,6330)
#     itemNo.append(no)
#     cost.append(items[no])
#     dates.append(date)
#     custNo.append(cust)
#     price.append(cost[-1]+uniform(2.5,15000.5))
#     discount.append(uniform(0,1500))
#     qnty.append(randint(1,3300))
#     if i%1000000==0:
#         print('Million REACHER -----------------')

# df_details={
#     'InvoiceNo':invoiceNo,
#     'ItemNo':itemNo,
#     'CustomerNo':custNo,
#     'Price':price,
#     'Cost':cost,
#     'Qnty':qnty,
#     'Discount':discount,
#     'InvoiceDate':dates,
#     }
# df_details = pd.DataFrame(df_details, columns = ['InvoiceNo','ItemNo','CustomerNo','Price','Cost','Qnty','Discount','InvoiceDate'])
# df_details.to_csv('genData.csv')
# df=pd.read_csv('genData.csv')
# print(df.head())