from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv
import time

# 設定
json_file = 'touch-de-inn-e5b296c3bc22.json'
file_name = 'タッチでINN'
sheet_name = 'list'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
CSV_FILENAME = 'memberlist.csv'
update_sec = 3600

# メンバーリストを更新する関数
def member_update():
    #最初に表示
    print("Please Wait...")
    # スプレッドシートにアクセスして，メンバーリストを作成する
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    gc = gspread.authorize(credentials)
    sh = gc.open(file_name)
    wks = sh.worksheet(sheet_name)
    # メンバーリスト更新後の時刻をstart 変数に保存
    start = time.time()
    worksheet = gc.open(file_name).worksheet(sheet_name)
    with open(CSV_FILENAME, 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(worksheet.get_all_values())

if __name__ == '__main__':
    start = time.time()
    member_update()
    while True:
        time.sleep(1)
        if time.time() - start > update_sec:
            start = time.time()
            member_update()
        
