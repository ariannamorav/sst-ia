### Datasets Base de Señalización y Tránsito
https://www.kaggle.com/datasets/tuanai/traffic-signs-dataset
https://universe.roboflow.com/universidad-de-las-fuerzas-armadas-espe-vq89f/senales-de-transito-8f0y5
https://www.kaggle.com/c/ml-medellin-mar2019/data
https://universe.roboflow.com/yolo-mooix/construction-safety-gsnvb-tid2p
https://universe.roboflow.com/b-l07ov/detection-de-pannaux-de-signalisation-avec-yolo
https://universe.roboflow.com/yolosigns-wquu1/yolo-sign-data/dataset/1
https://universe.roboflow.com/deteccin-seales-de-transito-en-colombia/deteccion-senales-de-transito
https://universe.roboflow.com/deteccin-seales-de-transito-en-colombia/deteccion-senales-de-transito-2
https://universe.roboflow.com/malcoms-workspace-vw8ef/senales-de-transito-1

### Nuevos Datasets Específicos SST (Camillas, Gabinetes y Advertencias)
#### Camillas de Emergencia (Primeros Auxilios / Evacuación)
- https://universe.roboflow.com/pruebas-de-200/stretcher-gvv6u
- https://universe.roboflow.com/practicas-preprofesionales/stretcher-ggvtd
- https://universe.roboflow.com/yuvai-ttusg/stretcher

#### Gabinetes y Mangueras contra Incendios
- https://universe.roboflow.com/fire-eetbm/fire-cabinet-b8afv
- https://universe.roboflow.com/pramma-uappf/fire-hose-box
- https://universe.roboflow.com/014nirut-numluea/fire-cabinet-project

#### Señales de Advertencia y Riesgo Locativo (Piso Mojado / Caídas)
- https://universe.roboflow.com/thesis-workspace-94rew/final-wet-hazard-sign-jx6g5
- https://universe.roboflow.com/project1-awc5u/warning-sign

Traffic-Signs-Dataset
Unlock Road Safety: Explore 52 Types of Traffic Signs in High-Resolution Imagery

Traffic-Signs-Dataset

Code

Download

About Dataset
The Traffic-Signs-Dataset is a comprehensive collection of images used for computer vision tasks, particularly in traffic sign detection and recognition. It comprises a diverse range of images showcasing 52 different types of traffic signs commonly encountered in urban and rural settings. Each image is labeled, enabling supervised learning algorithms to be trained effectively. This dataset is instrumental for researchers, developers, and practitioners in the field, facilitating the development and evaluation of machine learning models and computer vision algorithms for accurate interpretation of traffic signs in various real-world conditions.

Usability
8.24

License
Apache 2.0

Expected update frequency
Annually

Tags
Image
Law
Image Classification
Image Generator
Image Augmentation
labels.csv(1.01 kB)

2 of 2 columns


ClassId

Name
Label	Count
0.00 - 5.10	6
5.10 - 10.20	5
10.20 - 15.30	5
15.30 - 20.40	5
20.40 - 25.50	5
25.50 - 30.60	5
30.60 - 35.70	5
35.70 - 40.80	5
40.80 - 45.90	5
45.90 - 51.00	6
Label	Count
0.00 - 5.10	6
5.10 - 10.20	5
10.20 - 15.30	5
15.30 - 20.40	5
20.40 - 25.50	5
25.50 - 30.60	5
30.60 - 35.70	5
35.70 - 40.80	5
40.80 - 45.90	5
45.90 - 51.00	6
0
51
Bicycles crossing
4%
Speed limit (5km/h)
2%
Other (49)
94%
0
Speed limit (5km/h)
1
Speed limit (15km/h)
2
Speed limit (30km/h)
3
Speed limit (40km/h)
4
Speed limit (50km/h)
5
Speed limit (60km/h)
6
Speed limit (70km/h)
7
speed limit (80km/h)
8
Dont Go straight or left
9
Unknown7
10
Dont Go straight
11
Dont Go Left
12
Dont Go Left or Right
13
Dont Go Right
14
Dont overtake from Left
15
No Uturn
16
No Car
17
No horn
18
No entry
19
No stopping
20
Go straight or right
21
Go straight
22
Go Left
23
Go Left or right
24
Go Right
25
keep Left
26
keep Right
27
Roundabout mandatory
28
watch out for cars
29
Horn
30
Bicycles crossing
31
Uturn
32
Road Divider
33
Unknown6
34
Danger Ahead
35
Zebra Crossing
36
Bicycles crossing
37
Children crossing
38
Dangerous curve to the left
39
Dangerous curve to the right
40
Unknown1
41
Unknown2
42
Unknown3
43
Go right or straight
44
Go left or straight
45
Unknown4
46
ZigZag Curve
47
Train Crossing
48
Under Construction
49
Unknown5
50
Fences
51
Heavy Vehicle Accidents
No more data to show
Data Explorer
Version 1 (243.82 MB)

DATA

TEST

labels.csv

Summary
6117 files

2 columns

See what others are saying about this dataset
What have you used this dataset for?

Learning 2

Research 2

Application 1

LLM Fine-Tuning 0
How would you describe this dataset?

# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = ""

# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "tuanai/traffic-signs-dataset",
  file_path,
  # Provide any additional arguments like 
  # sql_query or pandas_kwargs. See the 
  # documenation for more information:
  # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)

print("First 5 records:", df.head())

python dataset/test_workflow.py "ruta_a_tu_imagen.jpg"


python dataset/camara_workflow.py


python dataset/inspeccion_sst_app.py


python dataset/servidor_api_sst.py


python dataset/inspeccion_sst_app.py


python dataset/servidor_api_sst.py
