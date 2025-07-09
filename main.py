from datetime import datetime, timedelta
from flask import Flask, render_template, request
from fileUtil import FileUtil
import os

# 今日を含めた8日間の日付を取得
today = datetime.today().strftime("%Y%m%d")
days = [today]
for plusDay in range(7):
    nextDay = datetime.now() + timedelta(days=(plusDay + 1))
    formatted_Day = nextDay.strftime("%Y%m%d")
    days.append(formatted_Day)

# ファイル操作のクラスのインスタンスを取得
fileUtil = FileUtil()

directory = '/tmp'

# ファイルパスを指定
fileInfoList = []
for day in days:
    fileName = f'program_area_{day}.txt'
    filePath = os.path.join(directory, fileName)
    fileInfoList.append((day, fileName, filePath))

# リストの長さを取得
list_length = len(fileInfoList)

lines = []
for fileInfo in fileInfoList:
    # ファイルが存在するかどうかを判定して、ない場合はファイルを作成
    day, fileName, filePath = fileInfo
    fileUtil.checkfile(directory=directory, file_path=filePath, day=day)

    # ファイルの内容を読み取り、リストに変換
    # 入力された日付文字列を解析
    date_obj = datetime.strptime(day, '%Y%m%d') + timedelta(days=1)
    nextDay = date_obj.strftime("%Y%m%d")
    lines.extend(fileUtil.readFile(file_path=filePath, day=day, nextDay=nextDay))

app = Flask(__name__)
        
@app.route('/', methods=['GET', 'POST'])
def index():
    filteredData = lines
    if request.method == 'POST':
        chArea = request.form['chArea']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        filteredData = filter_data_by_time(filteredData, chArea, date, start_time, end_time)
    return render_template('index.html', filteredData=filteredData)

def filter_data_by_time(lines, chArea, date, start_time, end_time):
    filtered_data = []
    for item in lines:
        item_start_time = datetime.strptime(item.startTime.strip(), '%H:%M').time()
        item_end_time = datetime.strptime(item.endTime.strip(), '%H:%M').time()
        item_date = datetime.strptime(item.date.strip(), '%Y/%m/%d').date()

        # 時間フィルターの条件
        time_condition = True
        if start_time and not end_time:
            if isinstance(start_time, str):
                start_time = datetime.strptime(start_time, '%H:%M').time()
            time_condition = start_time == item_start_time
        elif start_time and end_time:
            if isinstance(start_time, str):
                start_time = datetime.strptime(start_time, '%H:%M').time()
            if isinstance(end_time, str):
                end_time = datetime.strptime(end_time, '%H:%M').time()
            time_condition = start_time <= item_start_time <= end_time and item_end_time <= end_time
        
        # 日付フィルターの条件
        date_condition = True
        if date:
            if isinstance(date, str):
                date = datetime.strptime(date, '%Y-%m-%d').date()
            date_condition = date == item_date

        # フィルター条件の適用
        if time_condition and date_condition and (not chArea or item.chArea == chArea):
            if item not in filtered_data:
                filtered_data.append(item)
    return filtered_data    

if __name__ == '__main__':
    app.run(debug=True)