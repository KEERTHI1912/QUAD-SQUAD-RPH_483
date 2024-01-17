import cv2
import numpy as np
import os
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static
import folium
import requests
from requests.exceptions import ConnectionError
from pretty_notification_box import notification_box



def config():
    file_path = "./components/img/"
    img = Image.open(os.path.join(file_path, 'rjp logo.png'))
    st.set_page_config(page_title='QUAD SQUAD', page_icon=img, layout="wide", initial_sidebar_state="expanded")

    # code to check turn of setting and footer
    st.markdown(""" <style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """, unsafe_allow_html=True)

    # encoding format
    encoding = "utf-8"

    st.markdown(
        """
        <style>
            .stProgress > div > div > div > div {
                background-color: #1c4b27;
            }
        </style>""",
        unsafe_allow_html=True,
    )

   


def get_geolocation():
    key = "8ee23d92d2e349178b1e7bc254957669"
    response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + key)
    return response.json()

def main1():
    
    capture = cv2.VideoCapture(0)

    while True:
        is_capture, frame = capture.read()
        if not is_capture:
            print("Cannot access the camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        canny_img = cv2.Canny(gray, 0, 255)
        mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 3)
        and_mask = cv2.bitwise_and(mask, canny_img)

        nonzero_area = cv2.countNonZero(and_mask)
        if nonzero_area < 800:
            print("Camera blocked")
            frame = cv2.putText(frame, "Camera is blocked", (20, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA, False)
        
        else:
            frame = cv2.putText(frame, "Camera is not blocked", (20, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA, False)

        cv2.imshow("frame", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            print("Terminating the program")
            break
    st.subheader("Component with constant args")

    styles = {'material-icons':{'color': 'red'},
          'title': {'font-weight':'bold'},
          'notification-content-container': {'':''},
          'title-text-url-container': {'',''},
          'notification-text-link-close-container': {'',''},
          'external-link': {'',''},
          'close-button': {'',''}}

    notification_box(icon='warning', title='Warning', textDisplay='CAMERA VIEW IS BLOCKED', externalLink='view more details',
                                url='https://www.cdc.gov/healthywater', styles=None, key='foo')
    capture.release()
    cv2.destroyAllWindows()






def other_tab():
    st.header("CAMERA OBSTRUCTION ALERTS")
    main1()

def camdisp():
    st.header("CAMERA DISPLACEMENT REPORT")
    st.title("Webcam Live Feed")
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        _, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)
    else:
        st.write('Stopped')
    
    



def home():
    try:
        with st.spinner("Please wait your request is being processed ......"):
            response = get_geolocation()
            st.header("IP GeoTagging System 🕵️‍♂️")
            col1, col2 = st.columns([8, 4])

            with col1:
                m = folium.Map(location=[response["latitude"], response["longitude"]], zoom_start=16)
                tooltip = "The Approx Location"
                folium.Marker(
                    [response["latitude"], response["longitude"]],
                    popup="The Approx Location", tooltip=tooltip
                ).add_to(m)
                folium_static(m,width=500,height=400)



            with col2:
                st.markdown(f"""
                <table>
                <thead>
                   <th>Data</th>
                   <th>Value</td>
                </thead>
                
                <tr>
                   <td>Ip Address</td>
                   <td>{response["ip"]}</td>
                </tr>
                
                <tr>
                   <td>City</td>
                   <td>{response["city"]}</td>
                </tr>
                
                <tr>
                   <td>District</td>
                   <td>{response["district"]}</td>
                </tr>
                
                <tr>
                   <td>Province</td>
                   <td>{response["state_prov"]}</td>
                </tr>
                
                <tr>
                   <td>Calling Code</td>
                   <td>{response["calling_code"]}</td>
                </tr>
                <tr>
                   <td>Latitude</td>
                   <td>{response["latitude"]}</td>
                </tr>
                
                <tr>
                   <td>Longitude</td>
                   <td>{response["longitude"]}</td>
                </tr>
                           
                <tr>
                   <td>Country</td>
                   <td><img src="{response['country_flag']}" style="width:30%;max-width:40%"> {response["country_name"]}</td>
                </tr>
                

    
                </table>


""",unsafe_allow_html=True)

            with st.expander("More Information regarding this IP"):
                st.subheader("Currency")
                df = pd.DataFrame.from_dict(response["currency"], orient="index", dtype=str, columns=['Value'])
                st.write(df)
                st.subheader("ISP")
                st.write("isp",{response["isp"]})
                st.write("connection_type",{response["connection_type"]})
                st.write("organization", {response["organization"]})

                st.subheader("TimeZone")
                df_1 = pd.DataFrame.from_dict(response["time_zone"], orient="index", dtype=str, columns=['Value'])
                st.write(df_1)
            
            video_file = open('sample-inp-2_trim.mp4', 'rb')
            video_bytes = video_file.read()

            st.video(video_bytes)








    except ConnectionError as e:
        st.error("The APP has failed to connect please check your connection 😥")


def main():
    config()
    with st.sidebar:
        choice = option_menu("Main Menu", ["CCTV GEOTAGGED DATA", 'CCTV OBSTRUCTION ALERTS', 'CCTV DISPLACEMENT REPORT'], icons=['house', 'list-task','list-task'], menu_icon="cast",
                             default_index=0)

    if (choice == "CCTV GEOTAGGED DATA"):
        home()
    elif (choice == "CCTV OBSTRUCTION ALERTS"):
        other_tab() 
    else:
        camdisp() 


if __name__ == '__main__':
    main()
