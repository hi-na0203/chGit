import re
from bs4 import BeautifulSoup
import requests

class GetData:
    @staticmethod
    def getChData(day):
        # 情報を取得したいHPのアドレスを記載
        url = f"https://bangumi.org/epg/td?broad_cast_date={day}&ggm_group_id=42"
        
        # HPから情報を取得
        response = requests.get(url)
        
        # 取得した情報をtextに変換
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        ul_tags = soup.find_all('ul', id=re.compile(r'^program_line_'))

        # 抽出した値を保存するリスト
        extracted_values = []

        for ul_tag in ul_tags:
            area_value = GetData.__convChArea(ul_tag['id'])

            # 特定のクラスを持つliタグを取得
            li_tags = ul_tag.find_all('li', class_=['sc-past', 'sc-current', 'sc-future'])
            
            GetData.__makeWritingData(li_tags, extracted_values, day, area_value)
        return extracted_values
    
    def __makeWritingData(li_tags, extracted_values, day, area_value):
        # liタグ内の特定の値を抽出
        for li in li_tags:
            e_value = li.get('e')
            s_value = li.get('s')
            program_title = li.find('p', class_='program_title').get_text()
            
            # 重複チェック
            if not any(d['e'] == e_value and d['s'] == s_value and d['program_title'] == program_title for d in extracted_values):
                extracted_values.append({'chArea': area_value, 'date': day, 'e': e_value, 's': s_value, 'program_title': program_title})
    
    def __convChArea(area_value_str): 
        channel_map = {
            'program_line_1': "NHK総合",
            'program_line_2': "NHKEテレ",
            'program_line_3': "日テレ",
            'program_line_4': "テレビ朝日",
            'program_line_5': "TBS",
            'program_line_6': "テレ東",
            'program_line_7': "フジテレビ",
            'program_line_8': "TOKYO MX1",
            'program_line_9': "TOKYO MX2",
            'program_line_10': "tvk",
            'program_line_11': "チバテレ",
            'program_line_12': "テレ玉"
        }
        return channel_map.get(area_value_str, "")