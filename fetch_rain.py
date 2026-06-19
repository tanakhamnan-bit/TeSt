import os
import requests
from datetime import datetime, timedelta

def main():
    # 🔄 1. ตรวจสอบวันปัจจุบัน และคำนวณหาวันที่ของเมื่อวาน
    yesterday = datetime.now() - timedelta(days=1)
    year_str = yesterday.strftime("%Y")
    month_str = yesterday.strftime("%m")
    day_str = yesterday.strftime("%d")
    date_part = f"{year_str}-{month_str}-{day_str}"
    
    # 🔗 2. ประกอบร่าง URL ดึงข้อมูลดิบ
    dynamic_url = f"http://122.155.135.51/api/map/climateContourGeo?t=period&y={year_str}&m={month_str}&fd={date_part}&td={date_part}&f=rf_sum"
    
    try:
        response = requests.get(dynamic_url, timeout=30)
        data = response.json()
        features = data.get("features", [])
        
        # 📋 รวมข้อความ TEXT ดั้งเดิม (ไม่มีหัวตาราง และไม่เรียงลำดับใหม่)
        text_output = ""
        
        for feat in features:
            props = feat.get("properties", {})
            site_id = props.get("site_id")
            site_name = props.get("site_name")
            rain = props.get("data") if props.get("data") is not None else 0.0
            
            if site_id is not None:
                # 🔤 ต่อข้อความเป็น TEXT รูปแบบเดิมดั้งเดิม: id,ชื่อ,,,ค่าฝน
                text_output += f"{site_id},{site_name},,,{rain}\n"
                
        # 💾 บันทึกก้อนข้อความลงเป็นไฟล์ชื่อ rain_data.txt
        with open("rain_data.txt", "w", encoding="utf-8") as f:
            f.write(text_output)
            
        print("แปลงข้อมูลดิบเป็น TEXT ดั้งเดิมสำเร็จ!")
            
    except Exception as e:
        print("เกิดข้อผิดพลาดในการดึงข้อมูล:", str(e))

if __name__ == "__main__":
    main()
