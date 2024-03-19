f = open("OtherLangCode/VehiDyna/ANSYS Project/vehiDyna_Ansys_car2.txt", "r")

content = [i.strip("\n").split() for i in f.readlines()]
f.close()
finalDataList = []
last = content[0]


for i in content:
    if content.index(i) != 0:
        h = i
        g = [last, h]

        finalDataList.append(g)

    last = i
    
ghghgh = []
ffggg = []
count = 1
for u in finalDataList:
    o = [count, 1, float(u[0][1]), float(u[0][2]), 0]
    k = [count, 2, float(u[1][1]), float(u[1][2]), 0]
    count += 1
    ffggg.append([o,k])

ffggg.append([[count, 1, float(finalDataList[-1][1][1]), float(finalDataList[-1][1][2]), 0],[count, 2, float(finalDataList[0][0][1]), float(finalDataList[0][0][2]), 0]])


newFile = open("OtherLangCode/VehiDyna/ANSYS Project/vehiDyna_Ansys_car2_refined.txt", "w")
for i in ffggg:
    newFile.write(str(i[0]).strip("]").strip("[").replace(",","\t").replace(" ","") + "\n")
    newFile.write(str(i[1]).strip("]").strip("[").replace(",","\t").replace(" ","") + "\n")
    newFile.write("\n")
