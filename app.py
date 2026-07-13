from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลสถานที่
LOCATIONS = [
    {
        "id": 1,
        "name": "ร้าน ครัวเก๋ากึ๊ก",
        "lat": 7.8807810948116,
        "lng": 98.38026804421995,
        "description": "ร้านอาหารพื้นเมืองภูเก็ต บรรยากาศย้อนยุค ลิ้มลองรสชาติปักษ์ใต้แท้ๆ ในสไตล์โฮมเมดที่สืบทอดกันมา",
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 2,
        "name": "โรงเรียนภูเก็ตไทยหัวอาเซียนวิทยา",
        "lat": 7.883744348639161,
        "lng": 98.37355537007042,
        "description": "แหล่งเรียนรู้ทางประวัติศาสตร์และสถาปัตยกรรมชิโน-โปรตุกีสอันโดดเด่น สะท้อนวัฒนธรรมไทย-จีนของภูเก็ต",
        "image_url": "https://images.unsplash.com/photo-1577985051167-0d49eec21977?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 3,
        "name": "สวนเฉลิมพระเกียรติ (สวนหลวง ร.9)",
        "lat": 7.876576971991001,
        "lng": 98.37616999111417,
        "description": "พื้นที่สีเขียวใจกลางเมือง เหมาะสำหรับการพักผ่อนหย่อนใจ เดินเล่นรับลม และชมทัศนียภาพอันร่มรื่น",
        "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 4,
        "name": "ขนมจีนบ้านรสทิพย์",
        "lat": 7.879316505443622,
        "lng": 98.37236894452104,
        "description": "ร้านขนมจีนขึ้นชื่อรสชาติจัดจ้านสไตล์เมืองคอน พร้อมผักเหนาะสดๆ หลากหลายชนิดให้เลือกทานคู่กัน",
        "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 5,
        "name": "หาดกะรน",
        "lat": 7.843915520247151,
        "lng": 98.29361836977061,
        "description": "ชายหาดขาวสะอาดยาวสุดสายตา เลื่องชื่อเรื่องเม็ดทรายละเอียดและคลื่นลมที่เหมาะแก่การพักผ่อนชมพระอาทิตย์ตก",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80"
    }
]

@app.route('/')
def index():
    # 1. สร้างแผนที่
    m = folium.Map(location=[7.875, 98.35], zoom_start=12, tiles="OpenStreetMap")
    
    # 2. วาดเส้นทางเชื่อมจุด
    route_points = [(loc["lat"], loc["lng"]) for loc in LOCATIONS]
    folium.PolyLine(route_points, color="#222222", weight=3, opacity=0.6).add_to(m)
    
    # 3. ปักหมุด พร้อมใส่ข้อมูลลงใน Popup เมื่อคลิกที่หมุด
    for loc in LOCATIONS:
        html_popup = f"""
        <div style="font-family: sans-serif; width: 220px;">
            <h4 style="margin: 0 0 8px 0; color: #222; font-size: 14px;">{loc['name']}</h4>
            <img src="{loc['image_url']}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 4px; margin-bottom: 8px;">
            <p style="font-size: 12px; color: #666; margin: 0 0 10px 0; line-height: 1.4;">{loc['description']}</p>
            <a href="https://www.google.com/maps/search/?api=1&query={loc['lat']},{loc['lng']}" target="_blank" style="display: block; width: 100%; text-align: center; background: #222; color: #fff; text-decoration: none; padding: 8px 0; border-radius: 4px; font-size: 12px; font-weight: bold;">ไปที่ Google Maps</a>
        </div>
        """
        # ตั้งค่าขนาดหน้าต่าง Popup
        iframe = folium.IFrame(html_popup, width=240, height=280)
        popup = folium.Popup(iframe, max_width=240)
        
        folium.Marker(
            location=[loc["lat"], loc["lng"]],
            popup=popup,
            icon=folium.Icon(color="black", icon="info-sign")
        ).add_to(m)
    
    # 4. แปลงแผนที่เป็น HTML
    map_html = m._repr_html_()
    
    # 5. สร้างลิงก์นำทางรวมทุกจุด
    google_maps_route = "https://www.google.com/maps/dir/" + "/".join([f"{loc['lat']},{loc['lng']}" for loc in LOCATIONS])
    
    # ส่งข้อมูลทั้งหมดไปประกอบร่างในไฟล์ templates/index.html
    return render_template('index.html', locations=LOCATIONS, map_html=map_html, google_maps_route=google_maps_route)

if __name__ == '__main__':
    app.run(debug=True)
