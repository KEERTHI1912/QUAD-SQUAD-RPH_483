# IP BASED GEO TAGGING SYSTEM
Problem Statement: 
To locate and detect the coordinates of private cameras in a neighborhood to assist police in investigating crimes by giving precise location information and permitting speedy identification and access to critical video evidence. It also focuses on creating image processing algorithms for analyzing massive video streams to identify individual items and ways to trigger real-time alerts for specific object identification, informing the Command and Control Centre of unauthorized personnel or suspicious things.
Solution: 
1. Location Tracking: 
Encode location information in metadata using standard geospatial formats (e.g., GeoJSON). We geotag the private cameras using IP address tracking without the help of GPS. 
For Example:
{
  "cameraID": "CCTV_RJ_001",
  "location": "Jaipur, Rajasthan, India",
  "latitude": 26.9124,
  "longitude": 75.7873,
  "visibilityRange": 30,
  "cameraSpecs": {
    "model": "XYZ-5000",
    "resolution": "4K Ultra HD",
    "fieldOfView": 120,
    "nightVision": true
                                  },
  "owner": {
    "contactPerson": "Mr. John Doe",
    "contactPhone": "+91 98765 43210"
  }
}
2. Database Integration and Key Generation: 
A database in Azure PostgreSQL contains the coordinates of different cameras categorized by location pin codes. 
       3. Video Processing: 
The footage is processed to detect the contours of the objects in the video. This is done to enhance the quality of the video footage which could help in accurate prediction. 
4. Real-time Monitoring and Reporting of Crime:
This includes a YOLO model that detects crimes such as chain snatching, women's harassment, pickpockets, purse snatchers, etc. The YOLO model is trained using the number of video inputs of crimes and the model detects the real-time crime and alerts the nearby police and the control center immediately using various messaging protocols (eg. MQTT).
![image](https://github.com/KEERTHI1912/RJPOLICE_HACK_483_QUADSQUAD_6/assets/75976487/3751ed38-197e-47b3-af09-319e1d44fe16)
![image](https://github.com/KEERTHI1912/RJPOLICE_HACK_483_QUADSQUAD_6/assets/75976487/4d8607fd-df63-4a14-b86a-9c7323357e1d)

6. Displacement Control: 
The displacement of the CCTV camera can be identified by implementing AI vision-based algorithms like the SIFT algorithm that can detect disorientation of camera angles or object intrusion by matching the coordinates and values of the original feed and the displaced feed.

Software and Technology: 
1. Programming Languages: 
● Python
2. Frameworks: 
● YOLO, SIFT, Tensorflow
3. Cloud Services: 
● Microsoft Azure PostgreSQL
4. Web App Development:
Streamlit for primary deployment

Team Members & Responsibilities: 
KEERTHI U - Frontend Developer 
ADITYA GURJALE S - ML Developer  
MITHUNESH RAJAN A - Database Manager
HEMANTH KUMAR C S - Computer Vision Developer


#### To install relevant packages
Open your shell or terminal and install the relevant packages using the command below

```python
pip install -r requirements.txt
```

#### To run this Application
Open the root folder of the project and run the command below:
```python
streamlit run main.py
```

