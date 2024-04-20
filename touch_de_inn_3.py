import binascii
import nfc
import os
import csv
    
if __name__ == '__main__':
    while (True):
        clf = nfc.ContactlessFrontend('usb')
        flag = 0
        count = 0
        list_data = []
        print("Please Touch your IC card.")
        try:
            tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        finally:
            clf.close()
        idm = binascii.hexlify(tag._nfcid)
        
        with open('memberlist.csv', 'r') as f:
            gotdata = csv.reader(f, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
            header1 = next(gotdata)
            count = int(header1[1])
            header2 = next(gotdata)
            for i in range(count):
                content = next(gotdata)
                list_data.append(content)
        
        for i in range(count):
            if idm.decode() == list_data[i][2]:
                print(list_data[i][1])
                flag = 1
                break
        if flag == 0:
            print("不法侵入者を発見")
