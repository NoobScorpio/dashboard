
import pandas as pd
import pyodbc
import datetime as dt
dataFrame=pd.DataFrame([])
print('Started')
def connectSQLServer(driver, server, db,uid,pwd):
    print('Inside FUNCTION')
    connSQLServer = pyodbc.connect(
        r'DRIVER={' + driver + '};'
        r'SERVER=' + server + ';'
        r'DATABASE=' + db + ';'
        r'Trusted_Connection=yes;'
       r'UID='+uid+';'
       r'PWD='+pwd+'',
       autocommit=True
    )
    print('RETURNED')
    return connSQLServer

conn=connectSQLServer('ODBC Driver 17 for SQL Server'
,'DESKTOP-3VRPUGO'
,'alhawama','cifer','Cifer')


#FOR CUSTOMER
print("Connection Successful")
data=pd.read_csv(r"C:\\Users\\CIFER\\Downloads\\Customer\\totalCustomers.csv")
name=data['Name']
respName=data['ResponsiblePersonName']
contact=data['Contact']
vat=data['VatNumber']
credit=data['CreditAmount']
tele=data['TelephoneNumber']
respContact=data['ResponsiblePersonContact']
email=data['Email']
print("COLUMNS MADE")
print(name[0])

# data = pd.read_csv(r"C:\\Users\\JMM Tech\\Downloads\\totalItems.csv")
# Name=data['ItemName']
# ManufName=data['ManufacturerName']
# Pieces=data['PiecesPerUnit']
# ThresQuantity=data['ThresholdQuantity']
# ShelfNumber=data['ShelfNumber']
# RCPrice=data['RetailCostPrice']
# WSPrice=data['WholeSalePrice']
# RSPrice=data['RetailSellPrice']


from datetime import datetime as dt

# FOR CUSTOMERS
for i in range(0,50000):
    cursor = conn.cursor()
    cursor.execute(
        "insert into dbo.Accounts (AccountNameEnglish,AccountType,SubAccountTypeID,ParentAccountID,CanDeleted,IsDeleted,DeletedAt)" +
        "values ('" + name[i] + "',1,1,1,0,0,0)")
    cursor.execute("SELECT AccountID FROM dbo.Accounts ORDER BY AccountID DESC")
    id = cursor.fetchall()
    id = id[0][0]
    date=dt.now()
    print(date)
    cursor.execute("insert into dbo.Customers (CustomerNameEnglish,Contact,Email,CreditAmountLimit,CustomerTypeID,"
                   +"CustomerVATNo,AccountID,ResponsibleNameEnglish,ResponsibleContact,IsDeleted,CreditDurationLimit,"
                    +"OpeningBalanceDate,DebitOpeningBalance,CreditOpeningBalance,Debit,Credit)"
                   +"values ('"+name[i]+"',"+str(contact[i])+",'"+email[i]+"',"+str(credit[i])+""
                    +",'CUST-TYP-001',"+str(vat[i])+","+str(id)+",'"+respName[i]+"','"+str(respContact[i])+"',0,0,'"+str(date)+"',0,0,0,0)")

    cursor.execute("SELECT CustomerID FROM dbo.Customers ORDER BY CustomerID DESC")
    id2 = cursor.fetchall()
    id2 = id2[0][0]
    print(id2)
    for j in range(0, 200):
        cursor.execute(
            "insert into dbo.CustomerProject(IsDeleted,CreatedAt,CustomerID,CreditLimit,PaymentDueDate,Status,DeletedAt)"
            + f"values(0,'{dt.now()}','"+str(id2)+"',1000,'"+str(date)+"','ACTIVE',0)"
            )

        print(f'DATA INSERTED: {j+1}')

    print(f'DATA INSERTED: {i+1}')

    for k in range(0, 200):
        cursor.execute("insert into dbo.CustomerTargets(CustomerID, IsDeleted, DeletedAt, TargetAmount, TargetDiscountAmount,"
                      +"TargetDiscountPercentage, TargetIssueDate, Status,TargetDeadlineDate)"
                       +f"values('"+str(id2)+"', 0,0,100000,1000,10,'"+str(date)+"',0,'"+str(date)+"')"
                       )






# FOR ITEMS

# for i in range(200,10000):
#     cursor = conn.cursor()
#     date=dt.datetime.now()
#     print(date)
#     print("Starting Execution")
#     cursor.execute("insert into dbo.Items (ItemNameEnglish,PiecesPerUnit,ManufacturerNameEnglish,RetailSellPrice,WholeSellPrice,"
#                    +"RetailCostPrice,Location,ShelfNumber,ThresholdQuantity,IsDeleted,CategoryID,DeletedAt)"
#                    +"values ('"+Name[i]+"',"+str(Pieces[i])+",'"+ManufName[i]+"',"+str(RSPrice[i])+""
#                     +","+str(WSPrice[i])+","+str(RCPrice[i])+",0,"+str(ShelfNumber[i])+",'"+str(ThresQuantity[i])+"',0,'CAT-1',0)")
#     print(f'DATA INSERTED: {i+1}')

# from datetime import datetime as dt
#
# #FOR Supplier
# for i in range(10,len(name)):
#     cursor = conn.cursor()
#     cursor.execute(
#         "insert into dbo.Accounts (AccountNameEnglish,AccountType,SubAccountTypeID,ParentAccountID,CanDeleted,IsDeleted,DeletedAt)" +
#         "values ('" + name[i] + "','LIABILITIES',1,1,0,0,0)")
#     cursor.execute("SELECT AccountID FROM dbo.Accounts ORDER BY AccountID DESC")
#     id = cursor.fetchall()
#     id = id[0][0]
#     date=dt.now()
#     print(date)
#     cursor.execute("insert into dbo.Suppliers (SupplierNameEnglish,MobilePhone,Email,CreditAmountLimit,SupplierTypeID,"
#                    +"SupplierVATNo,AccountID,IsDeleted,CreditDurationLimit,"
#                     +"OpeningBalanceDate,DebitBalance,DeletedAt)"
#                    +"values ('"+name[i]+"',"+str(contact[i])+",'"+email[i]+"',"+str(credit[i])+""
#                     +",'SUP-TYP-001',"+str(vat[i])+","+str(id)+",0,0,'"+str(date)+"',0,0)")

#     cursor.execute("SELECT SupplierID FROM dbo.Suppliers ORDER BY SupplierID DESC")
#     id2 = cursor.fetchall()
#     id2 = id2[0][0]
#     cursor.execute("insert into dbo.PurchaseInvoice(IsDeleted,DeletedAt,IssuedDate,SupplierID,Total,"
#                     +"GrossTotal,NetTotal,AmountPaid,ReturnAmount,"
#                     +"DiscountAmount,DiscountPercentage,TotalVAT,VATPercentage,PaymentMethod,"
#                     +"PaymentType,InvoiceStatus,ReceiveType,ReceiveAs,PriceType,PaymentCompletionDate)"
#                     +f"values (0,0,'{dt.now()}','"+str(id2)+"',1500,2000,2000,0,0,0,200,15,1000,'CASH',0"
#                     +",0,'PAID',0,'{dt.now()}')")



# # FOR CUSTOMER CLEARANCE
# from datetime import datetime as dt
# for i in range(0,50000):
#     date=str(dt.now())
#     print(date)
#     cursor = conn.cursor()
#     cursor.execute("insert into dbo.CustomerClearenceVouchers(IsDeleted,DeletedAt,Amount,IssueDate,CustomerID,PaymentMethod)"
#                    +f"values (0,0,100,'{dt.now()}','CUST-0003','CASH')"
#                    )

#     print(f'DATA INSERTED: {i+1}')

# # FOR CUSTOMER PROJECTS
# from datetime import datetime as dt
# for i in range(0,50000):
#     cursor = conn.cursor()
#     cursor.execute("insert into dbo.CustomerProject(IsDeleted,CreatedAt,CustomerID,CreditLimit,PaymentDueDate,Status,DeletedAt)"
#                    +f"values(0,'{dt.now()}','CUST-0001',1000,'{dt.now()}','PENDING',0)"
#                    )
# #
# for k in range(0, 200):
#     cursor = conn.cursor()
#     cursor.execute("insert into dbo.CustomerTargets(CustomerID, IsDeleted, DeletedAt, TargetAmount, TargetDiscountAmount,"
#                       +"TargetDiscountPercentage, TargetIssueDate, Status,TargetDeadlineDate)"
#                        +f"values('"+str(id2)+"', 0,0,100000,1000,10,'"+str(date)+"',0,'"+str(date)+"')"
#                        )