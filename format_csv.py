import os, argparse
import csv

parser = argparse.ArgumentParser(description='Convert CSV format to standard CSV used by COVIDx.')
parser.add_argument('--filename', type=str, help='full path to csv file', required=True)
parser.add_argument('--out_csvname', default='metadata.csv', type=str, help='name of output csv file')
parser.add_argument('--imagefolder', default='images', type=str, help='path to image folder')
args = parser.parse_args()

infos = []
label_mapping = {'normal': 'No finding', 'COVID-19': 'COVID-19', 'doubt': '',
                 'Level1': 'No finding', 'Level2': '', 'COVID-19': 'COVID-19'}
notes_mapping = {'normal': 'Negative (covid-19 viral infection is excluded)',
                 'COVID-19': '',
                 'doubt': 'Inconclusive'}

with open(args.filename, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        if os.path.exists(os.path.join(args.imagefolder, row[1])):
            xray_info = {'patientid': row[0],
                         'imagename': row[1],
                         'finding': label_mapping[row[2]],
                         'view': row[3],
                         'modality': 'X-ray',
                         'notes': notes_mapping[row[2]] + ', date taken (YYYYMMDD): ' + row[5]}
            infos.append(xray_info)

titles = ['patientid', 'offset', 'sex', 'age', 'finding', 'survival',
          'temperature', 'pO2 saturation', 'view', 'modality',
          'imagename', 'artifacts/distortion', 'notes']

with open(args.out_csvname, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=titles)
    writer.writeheader()
    for row in infos:
        writer.writerow(row)
