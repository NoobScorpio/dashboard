headerNamesEn=[
    'Total Sales',
    'Items Sold',
    'Best Item',
    'Profit',
    'Top Customer',
    'Sales',
    'Select Year',
    'Select Month',
    'Max',
    'Average',
    'Weeks breakdown',
    'Week',
    'Top Items',
    'Top',
    'Cost',
    'Sold',
    'Profit',
    'Item',
    'Date',
    'Top Customers',
    'Customer',
    'Change Language',
    'Select Year',
    'Select Month',
    'January',
    'February', 
    'March', 
    'April', 
    'May', 
    'June',
    'July', 
    'August', 
    'September', 
    'October', 
    'November', 
    'December'
    ]


headerNamesAr=[
    'إجمالي المبيعات',
    'العناصر بيعت',
    'أفضل عنصر',
    'الربح',
    'أفضل العملاء',
    'مبيعات',
    'حدد السنة',
    'اختر الشهر',
    'ماكس',
    'معدل',
    'انهيار أسابيع',
    'أسبوع',
    'أهم العناصر',
    'أعلى',
    'كلفة',
    'تم البيع',
    'الربح',
    'بند',
    'تاريخ',
    'كبار العملاء',
    'الزبون',
    'تغيير اللغة',
    'حدد السنة',
    'اختر الشهر',
    'كانون الثاني',
    'شهر فبراير', 
    'مارس', 
    'أبريل', 
    'مايو', 
    'يونيو',
    'يوليو', 
    'أغسطس', 
    'سبتمبر', 
    'اكتوبر', 
    'شهر نوفمبر', 
    'ديسمبر']

# headerNamesAr.reverse()
headerEnDict=dict()
headerArDict=dict()
for i in headerNamesEn:
    headerEnDict[i]=i

for i,j in zip(headerNamesEn,headerNamesAr):
    headerArDict[i]=j

print(headerArDict)