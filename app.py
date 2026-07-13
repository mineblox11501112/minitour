import os
from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลสถานที่ท่องเที่ยวในกำแพงเพชร พร้อมรูปภาพและพิกัด
ATTRACTIONS = [
    {
        "id": 1,
        "name": "อุทยานแห่งชาติคลองลาน",
        "lat": 16.1303,
        "lng": 99.2786,
        "desc": "น้ำตกคลองลานขนาดใหญ่ สวยงามอลังการ รายล้อมด้วยป่าไม้สมบูรณ์ มีจุดกางเต็นท์และเส้นทางศึกษาธรรมชาติให้เดินชม",
        "type": "ธรรมชาติ",
        "image": "https://images.unsplash.com/photo-1627564639148-7fa2536b5db3?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 2,
        "name": "อุทยานประวัติศาสตร์กำแพงเพชร",
        "lat": 16.4886,
        "lng": 99.5244,
        "desc": "มรดกโลกทางวัฒนธรรม ชมโบราณสถานเก่าแก่ที่สร้างด้วยศิลาแลง ไฮไลท์คือวัดช้างรอบ และวัดพระแก้วกลางเมือง",
        "type": "วัฒนธรรม",
        "image": "https://images.unsplash.com/photo-1596402184320-417e7178b2cd?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 3,
        "name": "บ่อน้ำพุร้อนพระร่วง",
        "lat": 16.6667,
        "lng": 99.4444,
        "desc": "ผ่อนคลายความเมื่อยล้ากับการแช่น้ำแร่ธรรมชาติเพื่อสุขภาพ มีทั้งบ่อแช่เท้าบริการฟรี และห้องแช่ส่วนตัวแบบเป็นส่วนตัว",
        "type": "สุขภาพ",
        "image": "https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 4,
        "name": "ริมแม่น้ำปิง (ตลาดโต้รุ่ง)",
        "lat": 16.4822,
        "lng": 99.5218,
        "desc": "จุดพักผ่อนหย่อนใจและชมวิวพระอาทิตย์ตกดินริมน้ำปิง พร้อมแหล่งรวมของกินและสตรีทฟู้ดรสเด็ดของเมืองกำแพงเพชร",
        "type": "ไลฟ์สไตล์",
        "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=600&q=80"
    }
    {
        "id": 5,
        "name": "ริมแม่น้ำปิง (ตลาดโต้รุ่ง)",
        "lat": 16.4822,
        "lng": 99.5218,
        "desc": "จุดพักผ่อนหย่อนใจและชมวิวพระอาทิตย์ตกดินริมน้ำปิง พร้อมแหล่งรวมของกินและสตรีทฟู้ดรสเด็ดของเมืองกำแพงเพชร",
        "type": "ไลฟ์สไตล์",
        "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=600&q=80"
    }
]

@app.route('/')
def index():
    # สร้างแผนที่เริ่มต้น โฟกัสไปที่ใจกลางจังหวัดกำแพงเพชร
    start_coords = [16.4886, 99.5244]
    m = folium.Map(location=start_coords, zoom_start=10, control_scale=True)

    # วนลูปปักหมุดสถานที่บนแผนที่
    for place in ATTRACTIONS:
        color_map = {
            "ธรรมชาติ": "green",
            "วัฒนธรรม": "darkred",
            "สุขภาพ": "blue",
            "ไลฟ์สไตล์": "orange"
        }
        marker_color = color_map.get(place["type"], "gray")

        # ลิงก์สำหรับกดเปิดแอป Google Maps นำทาง
        nav_url = f"https://www.google.com/maps/dir/?api=1&destination={place['lat']},{place['lng']}"

        # HTML Popup ตกแต่งแบบมีรูปภาพและปุ่มนำทางในหมุดแผนที่
        popup_html = f"""
        <div style="font-family: 'Sarabun', sans-serif; width: 220px;">
            <img src="{place['image']}" style="width:100%; height:100px; object-fit:cover; border-radius:6px; margin-bottom:8px;">
            <h4 style="margin: 0 0 4px 0; color: #0f172a; font-weight: bold; font-size:14px;">{place['name']}</h4>
            <span style="background-color: #f1f5f9; color: #475569; padding: 2px 6px; font-size: 11px; border-radius: 4px; font-weight:600;">{place['type']}</span>
            <p style="font-size: 12px; color: #475569; margin-top: 6px; line-height: 1.4; margin-bottom: 10px;">{place['desc']}</p>
            <a href="{nav_url}" target="_blank" style="display: block; text-align: center; background-color: #059669; color: white; text-decoration: none; padding: 6px; font-size: 12px; border-radius: 4px; font-weight: bold;">🚗 นำทางด้วย Google Maps</a>
        </div>
        """
        
        folium.Marker(
            location=[place["lat"], place["lng"]],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=place["name"],
            icon=folium.Icon(color=marker_color, icon="info-sign")
        ).add_to(m)

    map_html = m._repr_html_()
    return render_template('index.html', map_html=map_html, attractions=ATTRACTIONS)

if __name__ == '__main__':
    # ดึงค่า Port จากระบบเพื่อรองรับการ Deploy บน Render หากรันในเครื่องตัวเองจะใช้ Port 8000 อัตโนมัติ เพื่อเลี่ยงพอร์ต 5000 ที่มักจะชน
    port = int(os.environ.get("PORT", 5007))
    app.run(host='0.0.0.0', port=port, debug=True)
