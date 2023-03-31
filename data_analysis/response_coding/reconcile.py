
import csv, copy

pid_filter = []#[4]#[220,221,223,224,225,227,228,231,234,243,244,246,247,269,274,276,284]
# questions = ("S1","S3","S5","S6","S8","S10","P4","P8","P9","C3","C7","Sm3","Sc8","Sc9")
# questions = ("S4 (Q25)","S5 (Q81)","FS5 (Q12)","FS7 (Q64)","FS10 (Q34)","NU1 (Q17)","NU2 (Q18)","P5 (Q5)",
#              "P7 (Q7)","IP2 (Q83)","C5 (Q6)","FN3 (Q23)","O2 (Q38)","O4 (Q39)")
# questions = ("AI4","AI7","D5","D7","D8","D9","C1","C2","C7")
questions = ("G1 (Q1)", "G2 (Q3)", "O1 (Q35)", "O2 (Q5)", "O3 (Q6)", "O5 (Q37)")

base_name = "ai2_coder_1.csv"
fixed_name = "ai_reconciliation.csv"

def main():
    base = readCSVFile(base_name)
    fixed = readCSVFile(fixed_name)
    combined = combine(base, fixed)
    writeToFile(combined, "combo.csv")

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
                            d[pid][column] = eval(codes)
    return d

def combine(d1, d2):
    d3 = copy.deepcopy(d1)
    for pid in d1.keys():
        for question in questions:
            if d2[pid].get(question, False):
                d3[pid][question] = d2[pid][question]
            elif d1[pid].get(question, False):
                d3[pid][question] = d1[pid][question]
    return d3

def writeToFile(d, fileName):
    with open(fileName, "w", encoding="utf-8") as file:
        file.write("," + ",".join(questions) + "\n")
        for pid in d.keys():
            print(pid)
            file.write(pid + ",")
            for i, q in enumerate(questions):
                if d[pid].get(q, False):
                    resp = d[pid][q]
                    file.write('"' + str(resp) + '"')
                if i < len(questions) - 1:
                    file.write(",")
            file.write("\n")
        file.flush()

if __name__ == "__main__":
    main()
