# import dash
# from dash.dependencies import Output, Input
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly
# import plotly.graph_objs as go
# from collections import deque
# import pandas as pd
# import pyodbc
# from datetime import datetime as dt
# dataFrame=pd.DataFrame([])
# def connectSQLServer(driver, server, db,uid,pwd):
#     connSQLServer = pyodbc.connect(
#         r'DRIVER={' + driver + '};'
#         r'SERVER=' + server + ';'
#         r'DATABASE=' + db + ';'
#         r'Trusted_Connection=yes;'
#        r'UID='+uid+';'
#        r'PWD='+pwd+'',
#        autocommit=True
#     )
#     return connSQLServer

# conn=connectSQLServer('ODBC Driver 17 for SQL Server'
# ,'DESKTOP-3VRPUGO'
# ,'alhawama','cifer','Cifer')

# # print('CONNECTED TO DATABASE')
# # date=dt.now()
# # print(str(date))
# # # print(conn)
# # cursor = conn.cursor()
# # # cursor.execute("insert into dbo.SaleInvoices (InvoiceID,IssuedDate,CustomerID,NetTotal,TotalCost)"
# # #                 "values (1,'"+str(date)+"',1,500,200),"
# # #                 "(2,'"+str(date)+"',2,600,400),"
# # #                 "(3,'"+str(date)+"',3,700,400),"
# # #                 "(4,'"+str(date)+"',4,500,400),"
# # #                 "(5,'"+str(date)+"',5,600,400),"
# # #                 "(6,'"+str(date)+"',6,500,300);")
# # # print('DATA INSERTED')

# # # SALES INVOICE
# # cursor.execute('''SELECT InvoiceID,IssuedDate,CustomerID,NetTotal FROM dbo.SaleInvoices;''')
# # rows = cursor.fetchall()
# # data=[[],[],[],[],[]]
# # for i in rows:
# #     data[0].append(i[0])
# #     data[1].append(i[1])
# #     data[2].append(i[2])
# #     data[3].append(i[3])

# # df={'InvoiceNo':data[0],
# #     'InvoiceDate':data[1],
# #     'CustomerNo':data[2],
# #     'Total':data[3],
# #     }
# # df = pd.DataFrame (df, columns = ['InvoiceNo','InvoiceDate','CustomerNo','Total',])

# # # SALES INVOICE DETAILS

# # cursor.execute('''SELECT SaleInvoiceID,ItemID,SellPrice,CostPrice,Quantity,DiscountAmount FROM dbo.SaleInvoiceDetails;''')
# # rows = cursor.fetchall()
# # data=[[],[],[],[],[],[]]
# # for i in rows:
# #     data[0].append(i[0])
# #     data[1].append(i[1])
# #     data[2].append(i[2])
# #     data[3].append(i[3])
# #     data[4].append(i[4])
# #     data[5].append(i[5])
# # df_details={'InvoiceNo':data[0],
# #     'ItemNo':data[1],
# #     'Price':data[2],
# #     'Cost':data[3],
# #     'Qnty':data[4],
# #     'Discount':data[5],
# #     }
# # df_details = pd.DataFrame (df_details, columns = ['InvoiceNo','ItemNo','Price','Cost','Qnty','Discount'])



# # print("SALES INVOICE TABLE")
# # print(df)
# # print("SALES INVOICE DETAILS TABLE")
# # print(df_details)

# # if df.empty or df_details.empty:
# #     print("NO DATA")
# # else:
# #     df['InvoiveDate']=pd.to_datetime(df['InvoiceDate'])
# #     df['Year']=df['InvoiceDate'].dt.year
# #     df['Month']=df['InvoiceDate'].dt.month
# #     df['Day']=df['InvoiceDate'].dt.day
# #     dataFrame=pd.merge(df_details,df,on='InvoiceNo')
# #     dataFrame['TotalCost']=dataFrame['Cost']*dataFrame['Qnty']
# #     dataFrame['TotalPrice']=dataFrame['Price']*dataFrame['Qnty']
# #     dataFrame['TotalProfit']=dataFrame['TotalPrice']-dataFrame['TotalCost']-dataFrame['Discount']

# # def getData():
# #     return dataFrame
