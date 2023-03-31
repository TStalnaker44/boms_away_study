
import csv, pprint

questions = ("S1","S3","S5","S6","S8","S10","P4","P8","P9","C3","C7","Sm3","Sc8","Sc9")
#questions = ("G1 (Q1)","G2 (Q3)","O1 (Q35)","O2 (Q5)","O3 (Q6)", "O5 (Q37)")
#questions = ("AI4","AI7","D5","D7","D8","D9","C1","C2","C7")
#questions = ('S4 (Q25)','S5 (Q81)','FS5 (Q12)','FS7 (Q64)','FS10 (Q34)','NU1 (Q17)','NU2 (Q18)','P5 (Q5)','P7 (Q7)','IP2 (Q83)','C5 (Q6)','FN3 (Q23)','O2 (Q38)','O4 (Q39)')

pid_filter = [4]#[220,221,223,224,225,227,228,231,234,243,244,246,247,269,274,276,284]

def readCSVFile(path):
    d = {}
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i > 0:
                pid = row[0]
                if pid.strip() != "" and not int(pid) in pid_filter:
                    d[pid] = {}
                    for j, column in enumerate(questions):
                        codes = row[j+2].strip()
                        if codes != "":
                            d[pid][column] = set(eval(codes))
    return d

path1 = "initial2_coder_1.csv"
d1 = readCSVFile(path1)
path2 = "initial2_coder_2.csv"
d2 = readCSVFile(path2)

count = 0
lyst = []
for pid in d1.keys():

    for question in questions:

        if d1[pid].get(question, None) == d2[pid].get(question, None):
            if not int(pid) in pid_filter:
                lyst.append((pid, question))
                count += 1

print(count)
print(lyst)

with open("temp.csv", "w", encoding="utf-8") as file:
    file.write("," + ",".join(questions) + "\n")
    for pid in d1.keys():
        file.write(pid + ",")
        for q in questions:
            if (pid, q) in lyst:
                file.write(",")
            else:
                file.write("X,")
        file.write("\n")
    file.flush()

