from datetime import datetime
import os
from item import Item
from getData import GetData

class FileUtil:
    @staticmethod
    def checkfile(directory, file_path, day):
        # ファイルが存在するかどうかを判定
        if not os.path.exists(directory):
            print(f"tmpディレクトリの作成")
            os.makedirs(directory)

        if not os.path.exists(file_path):
            print(f"{day}のファイルは存在しません。")
            getData = GetData
            extracted_values = getData.getChData(day=day)
            
            # テキストファイルに書き込む
            FileUtil.__writeFile(file_path=file_path, extracted_values=extracted_values)
    
    def __writeFile(file_path, extracted_values):
        with open(file_path, 'w', encoding='utf-8') as file:
            for value in extracted_values:
                file.write(f"chArea: {value['chArea']}, date: {value['date']}, s: {value['s']}, e: {value['e']}, program_title: {value['program_title']}\n")
    
    @staticmethod
    def readFile(file_path, day, nextDay):
        lines = []
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        itemList = []
        
        # データクラスのインスタンスに変換
        for item in lines:
            # データを分割
            data = item.split(',')

            if len(data) == 5:
                itemList.append(Item(*data))
            else:
                # title_without_commas, data[5], data[6] を1つの塊として結合
                combined_title = ','.join(data[4:])

                # 一時的に除去したタイトルを使って判定
                item_instance = Item(data[0], data[1], data[2], data[3], combined_title)
                # インスタンスをリストに追加
                itemList.append(item_instance)

        sorted_items = sorted(itemList, key=lambda x: x.startTime)
        for item in sorted_items:
            item.chArea = item.chArea.replace("chArea: " , "").strip()

            # 'date: 'の部分を取り除き、日付部分を抽出
            date_str = item.date.split(': ')[1]
            # datetimeオブジェクトに変換
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            # 新しいフォーマットに変換
            item.date = date_obj.strftime('%Y/%m/%d')

            startTime_str = item.startTime.replace(day, "").replace(nextDay , "").replace('s: ', "").strip()
            startTime_obj = datetime.strptime(startTime_str, "%H%M")
            item.startTime = startTime_obj.strftime("%H:%M")

            endTime_str = item.endTime.replace(day, "").replace(nextDay , "").replace('e: ', "").strip()
            endTime_obj = datetime.strptime(endTime_str, "%H%M")
            item.endTime = endTime_obj.strftime("%H:%M")
            
            item.title = item.title.replace("program_title: ", "")
        return sorted_items