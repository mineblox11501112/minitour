from flask import Flask, render_template
import folium

app = Flask(__name__)

LOCATIONS = [
    {
        "id": 1,
        "name": "ร้าน ครัวเก๋ากึ๊ก",
        "lat": 7.8807810948116,
        "lng": 98.38026804421995,
        "description": "ร้านอาหารพื้นเมืองภูเก็ต บรรยากาศย้อนยุค ลิ้มลองรสชาติปักษ์ใต้แท้ๆ ในสไตล์โฮมเมด",
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 2,
        "name": "โรงเรียนภูเก็ตไทยหัวอาเซียนวิทยา",
        "lat": 7.883744348639161,
        "lng": 98.37355537007042,
        "description": "แหล่งเรียนรู้ทางประวัติศาสตร์และสถาปัตยกรรมชิโน-โปรตุกีสอันโดดเด่น",
        "image_url": "https://images.unsplash.com/photo-1577985051167-0d49eec21977?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 3,
        "name": "สวนเฉลิมพระเกียรติ",
        "lat": 7.876576971991001,
        "lng": 98.37616999111417,
        "description": "พื้นที่สีเขียวใจกลางเมือง เหมาะสำหรับการพักผ่อนหย่อนใจและเดินเล่นรับลม",
        "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 4,
        "name": "ขนมจีนบ้านรสทิพย์",
        "lat": 7.879316505443622,
        "lng": 98.37236894452104,
        "description": "ร้านขนมจีนขึ้นชื่อรสชาติจัดจ้านสไตล์เมืองคอน พร้อมผักเหนาะสดๆ หลากหลายชนิด",
        "image_url": "https://images.unsplash.com/photo-1617093727343-374698b1b08d?auto=format&fit=crop&w=600&q=80"
    },
    {
        "id": 5,
        "name": "หาดกะรน",
        "lat": 7.843915520247151,
        "lng": 98.29361836977061,
        "description": "ชายหาดขาวสะอาดยาวสุดสายตา เลื่องชื่อเรื่องเม็ดทรายละเอียด",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=600&q=80"
    }
]

@app.route('/')
def index():
    m = folium.Map(tiles="OpenStreetMap")
    
    route_points = [(loc["lat"], loc["lng"]) for loc in LOCATIONS]
    folium.PolyLine(route_points, color="#222222", weight=3, opacity=0.6).add_to(m)
    
    # คำนวณขอบเขตแผนที่ให้พอดีกับหมุด (แก้ปัญหาแผนที่ซูมออกไกลเกินไป)
    sw = [min([loc["lat"] for loc in LOCATIONS]), min([loc["lng"] for loc in LOCATIONS])]
    ne = [max([loc["lat"] for loc in LOCATIONS]), max([loc["lng"] for loc in LOCATIONS])]
    m.fit_bounds([sw, ne])
    
    for loc in LOCATIONS:
        html_popup = f"""
        <div style="font-family: sans-serif; width: 200px;">
            <h4 style="margin: 0 0 8px 0; color: #222; font-size: 14px;">{loc['name']}</h4>
            <img src="{loc['image_url']}" style="width: 100%; height: 100px; object-fit: cover; border-radius: 4px; margin-bottom: 8px;">
            <p style="font-size: 12px; color: #666; margin: 0 0 10px 0; line-height: 1.4;">{loc['description']}</p>
        </div>
        """
        iframe = folium.IFrame(html_popup, width=220, height=240)
        popup = folium.Popup(iframe, max_width=220)
        
        folium.Marker(
            location=[loc["lat"], loc["lng"]],
            popup=popup,
            icon=folium.Icon(color="black", icon="info-sign")
        ).add_to(m)
    
    map_html = m._repr_html_()
    google_maps_route = "https://www.google.com/maps/dir/" + "/".join([f"{loc['lat']},{loc['lng']}" for loc in LOCATIONS])
    
    # ส่งตัวแปร locations ไปให้ index.html ด้วย
    return render_template('index.html', locations=LOCATIONS, map_html=map_html, google_maps_route=google_maps_route)

if __name__ == '__main__':
    # สำหรับการ Deploy ขึ้น Production แนะนำให้ตั้ง debug=False 
    # แต่สามารถใช้พอร์ตเดิมตามที่คุณตั้งไว้ได้เลยครับ
    app.run(debug=True, host='0.0.0.0', port=5007)
