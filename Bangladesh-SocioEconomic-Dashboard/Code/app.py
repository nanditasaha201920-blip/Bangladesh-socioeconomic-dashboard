import pandas as pd
import folium
import io

# ১. ডাটা লোড
csv_data = """district,lat,lon,poverty_rate,employment_rate,avg_income,literacy_rate
Dhaka,23.8103,90.4125,20,65,30000,85
Chattogram,22.3569,91.7832,25,60,25000,80
Rajshahi,24.3636,88.6241,35,55,18000,75
Khulna,22.8456,89.5403,30,58,20000,78
Barisal,22.7010,90.3535,40,50,15000,70
Sylhet,24.8949,91.8687,28,57,22000,77
Rangpur,25.7439,89.2752,45,48,14000,68
Mymensingh,24.7471,90.4203,38,52,16000,72"""

df = pd.read_csv(io.StringIO(csv_data))

# ২. ম্যাপ তৈরি
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB positron')

# ৩. ম্যাপে সার্কেল মার্কার যোগ করা
for index, row in df.iterrows():
    poverty = row['poverty_rate']
    # দারিদ্র্য হার অনুযায়ী কালার (বেশি দারিদ্র্য = লাল)
    color = '#d63031' if poverty >= 40 else '#fd9644' if poverty >= 30 else '#20bf6b'
    
    popup_text = f"""
    <div style="font-family: Arial; width: 180px;">
        <h4 style="margin:0 0 5px 0;">{row['district']}</h4>
        <b>Poverty Rate:</b> {poverty}%<br>
        <b>Employment:</b> {row['employment_rate']}%<br>
        <b>Avg Income:</b> {row['avg_income']:,} BDT<br>
        <b>Literacy:</b> {row['literacy_rate']}%
    </div>
    """
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['avg_income'] / 2000,  # আয় অনুযায়ী সার্কেল সাইজ
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=row['district'],
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        weight=1.5
    ).add_to(m)

# ৪. ম্যাপ সেভ
m.save("socioeconomic_map.html")
print("Socioeconomic Map created! Open 'socioeconomic_map.html'.")
m
