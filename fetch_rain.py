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
    
    # 🔗 2. ประกอบร่าง URL ดึงข้อมูลดิบจากเซิร์ฟเวอร์
    dynamic_url = f"http://122.155.135.51/api/map/climateContourGeo?t=period&y={year_str}&m={month_str}&fd={date_part}&td={date_part}&f=rf_sum"
    
    try:
        response = requests.get(dynamic_url, timeout=30)
        data = response.json()
        features = data.get("features", [])
        
        # 📋 เตรียมตัวแปร Array เพื่อรวมข้อมูลแบบ TEXT ดั้งเดิม (ไม่มีหัวตาราง และไม่เรียงลำดับใหม่)
        output_data = []
        
        for feat in features:
            props = feat.get("properties", {})
            site_id = props.get("site_id")
            site_name = props.get("site_name")
            rain = props.get("data") if props.get("data") is not None else 0.0
            
            if site_id is not None:
                # 🔤 ทุกค่าจะถูกแปลงสภาพเป็น TEXT (String) คั่นด้วย Comma ตามฟอร์แมตเดิม
                row = [str(site_id), str(site_name), "", "", str(rain)]
                output_data.append(row)
        
        # 🚀 3. ส่งข้อมูล TEXT ดั้งเดิมทั้งหมดข้ามคลาวด์ยิงตรงไปพ่นที่ Google Sheets
        google_script_url = os.environ.get("GG_SCRIPT_URL")
        if google_script_url:
            res = requests.post(google_script_url, json=output_data)
            print("ผลการส่งข้อมูลไป Google Sheets:", res.text)
        else:
            print("Error: ไม่พบลิงก์ปลายทางในระบบ (GG_SCRIPT_URL)")
            
    except Exception as e:
        print("เกิดข้อผิดพลาดในการดึงและส่งข้อมูล:", str(e))

if __name__ == "__main__":
    main()
