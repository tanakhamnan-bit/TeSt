import os
import requests
from datetime import datetime, timedelta

def main():
    # 🔄 คำนวณหาวันที่ของ "เมื่อวานนี้" แบบ Dynamic
    yesterday = datetime.now() - timedelta(days=1)
    year_str = yesterday.strftime("%Y")
    month_str = yesterday.strftime("%m")
    day_str = yesterday.strftime("%d")
    date_part = f"{year_str}-{month_str}-{day_str}"
    
    # 🔗 ประกอบร่าง URL ดึงข้อมูลทั้งหมดใน Link
    dynamic_url = f"http://122.155.135.51/api/map/climateContourGeo?t=period&y={year_str}&m={month_str}&fd={date_part}&td={date_part}&f=rf_sum"
    
    try:
        response = requests.get(dynamic_url, timeout=30)
        data = response.json()
        features = data.get("features", [])
        
        # 📋 กำหนดหัวตาราง (Header) วางที่แถวที่ 1 (A1) แปลงเป็น TEXT ทั้งหมด
        output_data = [["site_id", "site_name", "amphoe", "province", "rf_sum"]]
        
        for feat in features:
            props = feat.get("properties", {})
            site_id = props.get("site_id")
            site_name = props.get("site_name")
            rain = props.get("data") if props.get("data") is not None else 0.0
            
            if site_id is not None:
                # 🔤 มั่นใจดึงและแปลงทุกฟิลด์ให้กลายเป็น TEXT (String) ก่อนส่งออก
                row = [
                    str(site_id), 
                    str(site_name), 
                    "", 
                    "", 
                    str(rain)
                ]
                output_data.append(row)
        
        #  Sorting ข้อมูลฝนตกจากมากไปน้อย (ยกเว้นแถวหัวตารางตัวแรก)
        header = output_data[0]
        rows = output_data[1:]
        rows.sort(key=lambda x: float(x[4]), reverse=True)
        final_output = [header] + rows
        
        # 🚀 ส่งก้อนข้อมูล TEXT ทั้งหมดไปที่ Google Sheets ของคุณ
        google_script_url = os.environ.get("GG_SCRIPT_URL")
        if google_script_url:
            res = requests.post(google_script_url, json=final_output)
            print("ผลการส่งข้อมูลไป Google Sheets:", res.text)
        else:
            print("Error: ไม่พบลิงก์ปลายทาง (GG_SCRIPT_URL)")
            
    except Exception as e:
        print("เกิดข้อผิดพลาด:", str(e))

if __name__ == "__main__":
    main()
