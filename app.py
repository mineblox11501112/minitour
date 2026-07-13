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
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkZ4_2zbjiVK7ueWTUZjYWb0w9flnsDZ18rJktWEX1S3Y4HAKLViPYbBc&s=10"
    },
    {
        "id": 2,
        "name": "โรงเรียนภูเก็ตไทยหัวอาเซียนวิทยา",
        "lat": 7.883744348639161,
        "lng": 98.37355537007042,
        "description": "แหล่งเรียนรู้ทางประวัติศาสตร์และสถาปัตยกรรมชิโน-โปรตุกีสอันโดดเด่น",
        "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZH5_qrgng7LQj6JRcJ_HiId4PlpOaAKKv-MUqWE8PkHA-W5Vgs0V5OpUh&s=10"
    },
    {
        "id": 3,
        "name": "สวนเฉลิมพระเกียรติ",
        "lat": 7.876576971991001,
        "lng": 98.37616999111417,
        "description": "พื้นที่สีเขียวใจกลางเมือง เหมาะสำหรับการพักผ่อนหย่อนใจและเดินเล่นรับลม",
        "image_url": "https://mpics.mgronline.com/pics/Images/568000011830705.JPEG"
    },
    {
        "id": 4,
        "name": "ขนมจีนบ้านรสทิพย์",
        "lat": 7.879316505443622,
        "lng": 98.37236894452104,
        "description": "ร้านขนมจีนขึ้นชื่อรสชาติจัดจ้านสไตล์เมืองคอน พร้อมผักเหนาะสดๆ หลากหลายชนิด",
        "image_url": "https://scontent-bkk1-2.xx.fbcdn.net/v/t39.30808-6/577979606_1379055050861917_8996505482751270036_n.jpg?stp=dst-jpg_tt6&cstp=mx2048x1366&ctp=s2048x1366&_nc_cat=103&ccb=1-7&_nc_sid=cc71e4&_nc_eui2=AeFc4rHjwQM6TPZy9fJryCsbjXqyVP3SJiiNerJU_dImKCTDMxOXrM0dCBC3AUTEyb1zEIik2pZ_mV_OU_wKeL-t&_nc_ohc=dR8wNAZP13AQ7kNvwGefxNn&_nc_oc=Adqr1vWLI1zio21SyHGBXat7adS2A3nVvU4D7oTplzYNfhLhgs_G1iLbBt0ElxpViYY&_nc_zt=23&_nc_ht=scontent-bkk1-2.xx&_nc_gid=51WM-PXgQ3xbQGFMCeK2Ag&_nc_ss=7b2a8&oh=00_AQDOZ_WqB-Q2wWbD6u4FwAaHSDCAvRBn6QazojW9oGGmgA&oe=6A5A201A"
    },
    {
        "id": 5,
        "name": "หาดกะรน",
        "lat": 7.843915520247151,
        "lng": 98.29361836977061,
        "description": "ชายหาดขาวสะอาดยาวสุดสายตา เลื่องชื่อเรื่องเม็ดทรายละเอียด",
        "image_url": "https://lh3.googleusercontent.com/gps-cs-s/AHRPTWlUCYOBNfJVrWpfxDVTnesZf9E1cB8uc9nbmmBXS3lER0PQWIf9_R5FLTqNgbpKoInG57Ri07uFJwcDUWVJPR3coUes1g2mOxDdbNDU0xDagnjgzetde9A83iON0L_VhBfTXdnHoQ=w408-h306-k-no"
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
