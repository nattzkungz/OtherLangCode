import random
import pandas as pd
from faker import Faker
from datetime import date
from dateutil.relativedelta import relativedelta
# Localization
# fake = Faker(['en_US'])
phoneLocation = Faker(['th_TH'])

# # Random Customer Data
# names = [fake.unique.name().split() for _ in range(10000)]
# firstname = [_[0] for _ in names]
# lastname = [_[1] for _ in names]
# location = [fake.unique.address().replace('\n', ' ') for _ in range(10000)]
phone = [phoneLocation.unique.phone_number() for _ in range(100000)]

fakePhone = []
for i in phone:
    num = i.replace(' ','').replace('-','')
    if len(num) == 10:
        fakePhone.append(num)
    if len(fakePhone) == 10000:
        break

data = {'Phone': fakePhone}
df = pd.DataFrame(data)
df.to_excel('PhoneData.xlsx', index=False)
# email = [fake.unique.email().replace('example', 'gmail').replace('.net','.com').replace('.org','.com') for _ in range(10000)]
# isMember = [random.choice([True, False]) for _ in range(10000)]


# gender = [random.choice(('F', 'M')) for _ in range(10000)]
# # Member Data

# customerID = [('C' + str(_+1).zfill(5)) for _ in range(10000)]
# memberID = []
# count = 1
# joinDate = []
# endDate = []
# for i in isMember:
#     if i is True:
#         jD = fake.date_between(start_date='-3y', end_date='-1m')
#         eD = jD + relativedelta(years=2)
#         joinDate.append(jD)
#         endDate.append(eD)
#         memberID.append('M' + str(count).zfill(5))
#         count += 1
#     else:
#         memberID.append('None')
#         joinDate.append('None')
#         endDate.append('None')

# data = {'Firstname': firstname,'Lastname': lastname, 'Address': location, 'Phone': phone, 'Email': email, 'Member Status': isMember, 'Gender': gender, 'Customer ID': customerID, 'Member ID': memberID, 'Join Date': joinDate, 'End Date': endDate}
# df = pd.DataFrame(data)
# df.to_excel('CustomerData.xlsx', index=False)
####### END MEMBER SECTION


# Random Product Data
# orderIDRaw = []
# count = 0
# for i in range(1,10001):
#     singleOrder = ('OR'+str(i).zfill(6))
#     orderItemCount = random.randint(1, 10)
#     for i in range(orderItemCount):
#         orderIDRaw.append(singleOrder)
# print(orderIDRaw)

# data = {'Order ID': orderIDRaw}
# df = pd.DataFrame(data)
# df.to_excel('OrderID.xlsx', index=False)

