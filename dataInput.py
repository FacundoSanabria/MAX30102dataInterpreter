import csv


def getDataFromCSV():
    red_raw = []
    ir_raw = []

    # cargo los vectores con los valores medidos desde un csv
    with open('C:\\Users\\katyVa\\Desktop\\Facundo\\medicionesMAX30102\\viejas\\oxigenacionCopia.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            red_raw.append(int(row[0]))
            ir_raw.append(int(row[1]))

    red_raw = red_raw[90:]
    ir_raw = ir_raw[90:]

    return red_raw, ir_raw
