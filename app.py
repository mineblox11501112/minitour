from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลสถานที่
locations = [
    {
        "id": 1,
        "name": "ร้าน ครัวเก๋ากึ๊ก",
        "lat": 7.8807810948116,
        "lon": 98.38026804421995,
        "description": "ร้านอาหารพื้นเมืองชื่อดังที่เสิร์ฟเมนูต้นตำรับ รสชาติจัดจ้าน บรรยากาศเป็นกันเอง เหมาะสำหรับการเริ่มต้นทริป",
        "img_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=7.8807810948116,98.38026804421995"
    },
    {
        "id": 2,
        "name": "โรงเรียนภูเก็ตไทยหัวอาเซียนวิทยา(ฝั่งมัธยม)",
        "lat": 7.883744348639161,
        "lon": 98.37355537007042,
        "description": "แวะชมสถาปัตยกรรมและบรรยากาศรอบๆ โรงเรียนเก่าแก่ที่มีเอกลักษณ์ทางวัฒนธรรมและประวัติศาสตร์ยาวนาน",
        "img_url": "https://images.unsplash.com/photo-1577717903315-1691ae25ab3f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=7.883744348639161,98.37355537007042"
    },
    {
        "id": 3,
        "name": "สวนเฉลิมพระเกียรติ",
        "lat": 7.876576971991001,
        "lon": 98.37616999111417,
        "description": "พื้นที่สีเขียวใจกลางเมือง เหมาะสำหรับการเดินเล่นพักผ่อนหย่อนใจ ถ่ายรูป และสัมผัสวิถีชีวิตคนท้องถิ่น",
        "img_url": "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=7.876576971991001,98.37616999111417"
    },
    {
        "id": 4,
        "name": "ขนมจีนบ้านรสทิพย์ (ขนมจีนเมืองคอน ณ ภูเก็ต)",
        "lat": 7.879316505443622,
        "lon": 98.37236894452104,
        "description": "ฝากท้องมื้อเที่ยงกับขนมจีนเส้นสดและน้ำยาปักษ์ใต้รสเด็ด พร้อมผักเหนาะแบบจัดเต็มในสไตล์มินิมอล",
        "img_url": "https://images.unsplash.com/photo-1626804475297-41609ea004eb?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=7.879316505443622,98.37236894452104"
    },
    {
        "id": 5,
        "name": "หาดกะรน",
        "lat": 7.843915520247151,
        "lon": 98.29361836977061,
        "description": "ปิดทริปที่ชายหาดทรายขาวละเอียด ฟังเสียงคลื่นและชมพระอาทิตย์ตกดินในบรรยากาศเงียบสงบ",
        "img_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "gmap_url": "https://www.google.com/maps/search/?api=1&query=7.843915520247151,98.29361836977061"
    }
]

@app.route('/')
def index():
    # หาค่าเฉลี่ยพิกัดเพื่อตั้งจุดกึ่งกลางของแผนที่
    center_lat = sum([loc['lat'] for loc in locations]) / len(locations)
    center_lon = sum([loc['lon'] for loc in locations]) / len(locations)

    # สร้างแผนที่ Folium (ใช้ tiles='CartoDB positron' เพื่อสไตล์แผนที่แบบมินิมอลสีอ่อน)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles='CartoDB positron')

    # เพิ่ม Marker
    for loc in locations:
        # ใช้ Icon สีดำเพื่อความมินิมอล
        icon = folium.Icon(color='black', icon='map-marker')
        
        # ปรับแต่ง Popup
        popup_html = f"<b>{loc['name']}</b>"
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=loc['name'],
            icon=icon
        ).add_to(m)

    # แปลงแผนที่เป็น HTML string เพื่อส่งไปที่ template
    map_html = m._repr_html_()

    return render_template('index.html', locations=locations, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
