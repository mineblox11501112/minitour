import os
from flask import Flask, render_template
import folium

app = Flask(__name__)

# ข้อมูลสถานที่ท่องเที่ยวในกำแพงเพชร พร้อมรูปภาพและพิกัด
ATTRACTIONS = [
    {
        "id": 1,
        "name": "ร้าน ครัวเก๋ากึ๊ก",
        "lat": 7.8807810948116,
        "lng": 98.38026804421995,
        "desc": "เมื่อก่อนใครที่ผ่านไปมาแถวถนนกระ จะพบเห็นร้านอาหารเก่าแก่ คนใช้บริการจำนวนมาก​ ชื่อว่าร้าน"เก๋ากึ๊ก" แต่ตอนนี้ย้ายมาตั้งอยู่บนถนนพัฒนา อ.เมือง​จ.ภูเก็ต​(ใกล้กับมิสเตอร์​คอม)​ อาหารที่นี่จะเด่นมากเรื่องข้าวต้มปลา จะใช้เนื้อปลาที่สดในการปรุง ไม่ว่าจะเป็นเนื้อปลากะพง หรือปลาเก๋า น้ำซุปหอมหวาน พร้อมผักเคียงเยอะมาก เพราะความสดของปลาคนจึงนิยมสั่งอาหารซีฟู้ด แต่จะบอกว่า เมื่อนึกถึงอาหารพื้นเมือง ที่นี่ไม่น้อยหน้าใครเลย",
        "type": "ร้านอาหาร",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRkZ4_2zbjiVK7ueWTUZjYWb0w9flnsDZ18rJktWEX1S3Y4HAKLViPYbBc&s=10"
    },
    {
        "id": 2,
        "name": "โรงเรียนภูเก็ตไทยหัวอาเซียนวิทยา(ฝั่งมัธยม)",
        "lat": 7.883744348639161,
        "lng": 98.37355537007042,
        "desc": "โรงเรียนเน้นการเรียนแบบบูรณาการ 3 ภาษา ไทย จีน อังกฤษ",
        "type": "การศึกษา",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZH5_qrgng7LQj6JRcJ_HiId4PlpOaAKKv-MUqWE8PkHA-W5Vgs0V5OpUh&s=10"
    },
    {
        "id": 3,
        "name": " สวนเฉลิมพระเกียรติ",
        "lat": 7.876576971991001,
        "lng": 98.37616999111417,
        "desc": "พญามังกรทอง” สวนเฉลิมพระเกียรติ 72 พรรษา มหาราชินีฯ แลนด์มาร์กจุดเช็กอินใกล้เมืองเก่าภูเก็ต",
        "type": "สถานที่ท่องเที่ยว",
        "image": "https://mpics.mgronline.com/pics/Images/568000011830705.JPEG"
    },
    {
        "id": 4,
        "name": "ขนมจีนบ้านรสทิพย์ (ขนมจีนเมืองคอน ณ ภูเก็ต)",
        "lat": 7.879316505443622,
        "lng": 98.37236894452104,
        "desc": "ร้านรสทิพย์ ขนมจีน พร้อมรับออเดอร์?",
        "type": "ร้านอาหาร",
        "image": "https://scontent-bkk1-2.xx.fbcdn.net/v/t39.30808-6/577979606_1379055050861917_8996505482751270036_n.jpg?stp=dst-jpg_tt6&cstp=mx2048x1366&ctp=s2048x1366&_nc_cat=103&ccb=1-7&_nc_sid=cc71e4&_nc_eui2=AeFc4rHjwQM6TPZy9fJryCsbjXqyVP3SJiiNerJU_dImKCTDMxOXrM0dCBC3AUTEyb1zEIik2pZ_mV_OU_wKeL-t&_nc_ohc=dR8wNAZP13AQ7kNvwGefxNn&_nc_oc=Adqr1vWLI1zio21SyHGBXat7adS2A3nVvU4D7oTplzYNfhLhgs_G1iLbBt0ElxpViYY&_nc_zt=23&_nc_ht=scontent-bkk1-2.xx&_nc_gid=51WM-PXgQ3xbQGFMCeK2Ag&_nc_ss=7b2a8&oh=00_AQDOZ_WqB-Q2wWbD6u4FwAaHSDCAvRBn6QazojW9oGGmgA&oe=6A5A201A"
    }
    {
        "id": 5,
        "name": "หาดกะรน",
        "lat": 7.843915520247151,
        "lng": 98.29361836977061,
        "desc": "หาดยาว 4 กม. มีน้ำทะเลใสสะอาดและเงียบสงบ รวมถึงหาดทรายสีทองทอดยาวที่มีรีสอร์ต",
        "type": "สถานที่ท่องเที่ยว",
        "image": "https://lh3.googleusercontent.com/gps-cs-s/AHRPTWlUCYOBNfJVrWpfxDVTnesZf9E1cB8uc9nbmmBXS3lER0PQWIf9_R5FLTqNgbpKoInG57Ri07uFJwcDUWVJPR3coUes1g2mOxDdbNDU0xDagnjgzetde9A83iON0L_VhBfTXdnHoQ=w408-h306-k-no"
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
            "ร้านอาหาร": "green",
            "การศึกษา": "darkred",
            "สถานที่ท่องเที่ยว": "blue",
            "ร้านอาหาร": "orange",
            "สถานที่ท่องเที่ยว": "red"
            
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
    app.run(debug=True, host='0.0.0.0', port=5007)

