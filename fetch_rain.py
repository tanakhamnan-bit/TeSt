import os
import requests
from datetime import datetime, timedelta

def main():
    # 🔄 สเต็ปที่ 1: ตรวจสอบวันปัจจุบันของคอมพิวเตอร์ และคำนวณหาวันที่ของ "เมื่อวานนี้"
    yesterday = datetime.now() - timedelta(days=1)
    
    # แปลง ปี เดือน วัน ของเมื่อวานให้อยู่ในฟอร์แมต text (yyyy-MM-dd)
    year_str = yesterday.strftime("%Y")
    month_str = yesterday.strftime("%m")
    day_str = yesterday.strftime("%d")
    date_part = f"{year_str}-{month_str}-{day_str}"
    
    # 🔗 สเต็ปที่ 2: ประกอบร่าง URL เป็น Text สตริงเพื่อดึงข้อมูลทั้งหมดใน Link
    dynamic_url = f"http://122.155.135.51/api/map/climateContourGeo?t=period&y={year_str}&m={month_str}&fd={date_part}&td={date_part}&f=rf_sum"
    
    print(f"กำลังดึงข้อมูลจากลิงก์: {dynamic_url}")
    
    try:
        response = requests.get(dynamic_url, timeout=30)
        data = response.json()
        features = data.get("features", [])
        
        output_data = []
        for feat in features:
            props = feat.get("properties", {})
            site_id = props.get("site_id")
            site_name = props.get("site_name")
            
            # ดึงค่าฝน ถ้าไม่มีค่า (null) ให้เป็น 0.0
            rain = props.get("data") if props.get("data") is not None else 0.0
            
            # เก็บข้อมูลทั้งหมดโดยไม่ต้องกรองพื้นที่ (ใส่เป็นค่าว่างไว้สำหรับคอลัมน์อำเภอ/จังหวัดเดิมในชีต)
            if site_id is not None:
                output_data.append([int(site_id), site_name, "", "", rain])
        
        # เรียงลำดับฝนจากมากไปน้อย
        output_data.sort(key=lambda x: x[4], reverse=True)
        
        # ส่งข้อมูลเข้า Google Sheets
        google_script_url = os.environ.get("GG_SCRIPT_URL")
        if google_script_url:
            res = requests.post(google_script_url, json=output_data)
            print("ผลการส่งข้อมูลไป Google Sheets:", res.text)
        else:
            print("Error: ไม่พบลิงก์ปลายทางในระบบ (GG_SCRIPT_URL)")
            
    except Exception as e:
        print("เกิดข้อผิดพลาด:", str(e))

if __name__ == "__main__":
    main()
