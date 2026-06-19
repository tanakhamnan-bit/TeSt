import os
import requests
from datetime import datetime, timedelta

def main():
    # 1. คำนวณหาวันที่ของ "เมื่อวานนี้"
    yesterday = datetime.now() - timedelta(days=1)
    date_part = yesterday.strftime("%Y-%m-%d")
    year_str = yesterday.strftime("%Y")
    month_str = yesterday.strftime("%m")
    
    # 2. วิ่งไปดึงข้อมูลน้ำฝนจาก IP Server ปลายทาง
    url = f"http://122.155.135.51/api/map/climateContourGeo?t=period&y={year_str}&m={month_str}&fd={date_part}&td={date_part}&f=rf_sum"
    
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        features = data.get("features", [])
        
        # 3. สร้างตัว Mapping อำเภอ/จังหวัด (Master)
        area_mapping = {
            "85": ["เมืองปัตตานี", "ปัตตานี"], "86": ["เมืองยะลา", "ยะลา"], "87": ["เมืองนราธิวาส", "นราธิวาส"],
            "1091": ["เบตง", "ยะลา"], "3939": ["เบตง", "ยะลา"], "3901": ["เมืองนราธิวาส", "นราธิวาส"],
            "3905": ["เมืองนราธิวาส", "นราธิวาส"], "3906": ["เมืองนราธิวาส", "นราธิวาส"], "3936": ["เมืองปัตตานี", "ปัตตานี"],
            "3907": ["บาเจาะ", "นราธิวาส"], "3908": ["ยี่งอ", "นราธิวาส"], "3909": ["ไม้แก่น", "ปัตตานี"],
            "3910": ["สายบุรี", "ปัตตานี"], "3911": ["ปานาเระ", "ปัตตานี"], "3912": ["ยะหริ่ง", "ปัตตานี"],
            "3913": ["ทุ่งยางแดง", "ปัตตานี"], "3914": ["แม่ลาน", "ปัตตานี"], "3915": ["รือเสาะ", "นราธิวาส"],
            "3916": ["เจาะไอร้อง", "นราธิวาส"], "3917": ["ตากใบ", "นราธิวาส"], "3918": ["จะแนะ", "นราธิวาส"],
            "3919": ["สุคิริน", "นราธิวาส"], "3920": ["ศรีสาคร", "นราธิวาส"], "3921": ["โคกโพธิ์", "ปัตตานี"],
            "3922": ["แว้ง", "นราธิวาส"], "3923": ["ระแงะ", "นราธิวาส"], "3924": ["สุไหงปาดี", "นราธิวาส"],
            "3925": ["สุไหงโก-ลก", "นราธิวาส"], "3926": ["กะพ้อ", "ปัตตานี"], "3927": ["รามัน", "ยะลา"],
            "3928": ["เมืองยะลา", "ยะลา"], "3929": ["กรงปินัง", "ยะลา"], "3930": ["กาบัง", "ยะลา"],
            "3931": ["บันนังสตา", "ยะลา"], "3932": ["ยะหา", "ยะลา"], "3933": ["ธารโต", "ยะลา"],
            "3934": ["มายอ", "ปัตตานี"], "3935": ["ยะรัง", "ปัตตานี"], "3937": ["หนองจิก", "ปัตตานี"]
        }
        
        output_data = []
        for feat in features:
            props = feat.get("properties", {})
            site_id = str(props.get("site_id"))
            
            if site_id in area_mapping:
                amphoe = area_mapping[site_id][0]
                province = area_mapping[site_id][1]
                rain = props.get("data") if props.get("data") is not None else 0.0
                
                output_data.append([int(site_id), props.get("site_name"), amphoe, province, rain])
        
        # เรียงลำดับจากฝนตกมากสุดไปน้อยสุด
        output_data.sort(key=lambda x: x[4], reverse=True)
        
        # 4. ส่งข้อมูลชุดนี้ไปพ่นลงใน Google Sheets ของคุณผ่านเว็บแอปสคริปต์
        google_script_url = os.environ.get("GG_SCRIPT_URL")
        if google_script_url:
            res = requests.post(google_script_url, json=output_data)
            print("Status:", res.text)
        else:
            print("Error: ไม่พบข้อมูลลิงก์ GG_SCRIPT_URL")
            
    except Exception as e:
        print("เกิดข้อผิดพลาดในการดึงข้อมูล:", str(e))

if __name__ == "__main__":
    main()
