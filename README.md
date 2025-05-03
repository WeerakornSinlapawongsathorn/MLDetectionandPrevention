# Simulated SIEM Tool with Integrated Machine Learning for Threat Detection and Prevention
# Abstract

Cyberattacks have increasing with the higher internet usages and advancing technologies. Traditional security methods encounter a growing volume of data and complexity of network traffic, failing to detect suspicious network traffic and leading to unauthorized access to the system. Machine learning (ML) has become a critical approach for improving data processing and security. This study investigated several ML models, Logistic Regression (LR), Random Forest (RF), Decision Tree (DT), and K-Nearest Neighbors (KNN) – and compared with Deep Learning (DL) using CIC-IDS2017 dataset. The best performance model, RF, achieved approximately 99% accuracy and was selected to simulate Security Information and Event Management (SIEM) on cloud for real-time monitoring. SIEM dashboard was developed by Flask and Streamlit in Python. The proposed SIEM achieved by continuously parsing Suricata log, providing downloadable results for prevention efforts. However, while the system effectively supported real-time monitoring, the threat categories for Suricata Alerts should be improved. It is recommended to evaluate the system, develop functions and extend log utilizations, including cloud log, and endpoint log.  

# Introduction

Cybercriminals have become increasing with various techniques, including cross site scripting, phishing, denial of service (DoS) etc. The Intrusion Detection System (IDS) has been developed for decades, which aims to detect abnormal traffic and alert users. Nevertheless, it does not provide prevention for the malicious traffic, its function only alerts users to be aware of and manage the cyberattacks. Intrusion Prevention System (IPS) has been proposed to suddenly prevent cybercriminals. These systems are categorized as signature and behavior based. Signature-based IDS spotted known cybercriminals, including specific rules for detection. Behavior based IDS set up thresholds to identify abnormalities, this is effective to unknown threats. However, even though these are proficient in threat detection and prevention. Cybercriminals have been increasing and adapting AI to enhance complexity. Dataset is multiplied and traditional technologies are burdened. ML is beneficial to handle large datasets. ML consists of supervised and unsupervised learnings: learning from labeled data and non-labeled data. In this study, CIC-IDS2017 datasets were trained and tested by LR, RF, KNN, DT, and DL. These algorithms were compared, and the highest performance was deployed to detect real scenario. 

## A.	Statement of the Problem

As an increase of internet utilization and AI corporation, traditional IDS/IPS encounter challenges in managing the detection, making it difficult to detect evolving threats such as phishing, distributed denial of service (DDoS). This could result in high false positive and false negative, limiting the effectiveness of the systems. Therefore, ML offers a solution to not only handle an increasing amount of cyberthreats but also provide high performance for detection.
 
## B.	Objectives

The proposed study applied multiple MLs to classify malicious traffic, the highest performance among them was deployed as IDS/IPS:
 -	To perform various supervised machine learnings: LR, RF, KNN, DT and DL
 -	To build a comprehensive comparison of these algorithms based on their performance
 -	To deploy the best performance on cloud to establish SIEM tool for real-time cyberattacks detection

# Literature Review

## A.	Intrusion Detection and Prevention System

IDS/IPS are essential in ensuring network security that has been developed for decades. Network intrusion is a suspicious behavior through network traffic that harms network systems to gain unauthorized access or causes network misconfiguration or malware injections [1]. IDS identifies misbehavior based on rules and threshold, then reporting users to block the specific network traffic. IDS is classified as signature-based and anomaly-based intrusion detections. Signature-based intrusion detection (SIDS) detects suspicious activities from predefined rules, which unknown threats can overcome this detection. Meanwhile, anomaly-based intrusion detection (AIDS) provides thresholds to determine suspicious behaviors, it learns the pattern of attacks and identify unknown threats [1-2]. In contrast, IDS only specifies abnormal activities to alert the system, it does not act as a threat prevention. IPS advanced detections by blocking suspicious network traffic. Nevertheless, traditional IDS and IPS are based on rules and statistical models and limited to the amount of dataset or incoming network traffic. Due to an increasing number of internet users, the traditional IDS/IPS encounters large network traffic. The systems could be corrupted and fail to detect or prevent suspicious network traffic. ML plays an important role in large data handling. Therefore, the proposed study utilized ML to enhance detection systems’ performance.
 
## B.	Machine Learning

ML methods are widely used in data analysis and security assessments such as Security Information and Event Management (SIEM) tools, vulnerability scanner etc. ML learning can be categorized as supervised learning, unsupervised learning, and semi-supervised learning [1].  Supervised learning is a classification method required a labeled dataset to train and test the model [2]. Unsupervised learning classifies data with unlabeled training dataset [3]. These learnings consist of LR, RF, KNN, DT, DL etc. LR is beneficial for linear separation. KNN is defined for clustering samples, k means an observation for n clusters to group the same type of sample together, if k is very high, a model will consume high computation and time [2,4]. DT provides nodes, arcs, and leaves. Each node has a specific attribute, each arc is defined as a value for each leaf under the node. These leaves are identified for classification [2]. RF is popular for classification; the model contains a group of DTs to find the best possible result [5]. DL comprises hidden neural network layers, one input and one output [6]. The hidden neural network layers are effective to handle growing data, it improves the learning ability by adapting environment to increase accuracy [6]. This model requires higher computational power. The performance of these models is usually measured by accuracy, precision, recall, F1-score, and cross-validation (CV) [3].

There are few studies designing machine learning for threat detections. [7] built LR, RF, and XGboost using dataset from Kaggle.com, which contained public cyber threats. [7] extracted 13 features including payload size. [7] resulted LR at 81.39 accuracy rate, RF and XGboost at perfect accuracy. [9] designed RF, KNN, and Support Vector Machine (SVM) for DoS, DDoS, and Web Attack detections. The models of [9] achieved over 0.99 accuracy. Meanwhile, [8] applied CSE-CIC-IDS2018 dataset containing DDoS detection from AWS to train the model, 69 features were extracted and 80% of training data. From the adaptive environment, [8] indicated 98.97 accuracy of the proposed model. However, [9] and [8] did not demonstrate various threat types, only a few presented in the dataset, multiple anomalies could reduce their efficiency. Moreover, these studies did not perform machine learning integrating with real-time detection. This study applied LR, RF, KNN, DT, and DL to detect suspicious activities and build an online SIEM dashboard to detect a log file.

# Methodology and Implementation
## A.	Methodology Overview

CIC-IDS2017 datasets contain over 100,000 samples, which are categorized into Benign, DDoS and others. In this study, various ML algorithms, including LR, RF, KNN, DT and DL were applied to classify the samples and identify cyber threats. The performance of each algorithm was evaluated, and the one that presented the highest accuracy was selected for IDS/IPS. The IP addresses associated with detected cyberattacks were compiled as a blacklist, which could be used to block or prevent malicious traffic.

![image](https://github.com/user-attachments/assets/ad1df155-3c38-4bf9-b31e-cbc5a540a244)

Fig. 1. Methodology Overview

## B.	Machine Learning Algorithms

The dataset is an excel file from a network sniffing tool, consisting of IP addresses, protocol, Label Column etc. The label column indicates types of cyberattacks and is treated as a target for this study. Since the dataset exhibits an imbalance – where benign network traffic outweighs cyber threats. The dataset was normalized by StandardScaler for scaling and adjusting features to have mean in 0 and standard deviation of 1. 70% of the dataset were trained, and the rest was tested. 

Due to multiple labels for cyberattacks in the dataset, LR performed multi-class algorithm with one-vs-rest (OVR), 1,000 max iteration, and Limited-memory Broyden-Fetcher-Goldfarb-Shanno (Lbfgs) optimization. Random Forest model was set with 5 estimators, KNN with 5 neighbors, and Decision Tree with default. For deep neuron network, three layers were built with CrossEntropyLoss for multi-class classification. The model was trained over 100 epochs using Adam optimizer.
 
## C.	Performance Analysis

Each algorithm was evaluated by accuracy, precision, recall, F1-score, and cross-validation accuracy. Accuracy measures the ratio of correct classification to the total. Precision is used for true positive outputs among predicted positive samples. Recall evaluates the ability of a model to detect attacks. F1-score is defined as an average of precision and recall. Cross-validation (CV) played an important role in this study. It evaluates the performance of models to ensure reliability. The dataset after splitting for training and testing and pure dataset were assessed by cross-validation with 5 folds. These measurements were compared to selecting the best performance model for detection.

## D.	SIEM Dashboard

After choosing the top performance model, the model was deployed on Google Cloud, which provides scalability for large data. SIEM Dashboard was created by Flask API and Streamlit library. This dashboard allowed users to upload log files for the detection. Moreover, the proposed SIEM was also used for real-time detection, integrating Suricata open source. The results presented a bar chart and a pie chart to distinguish different cyber-attacks. Users could download the result to implement their blacklist. 

### Installing SURICATA

https://docs.suricata.io/en/latest/quickstart.html

# Results and Discussion
## A.	Machine Learning Algorithms

After training and evaluating the algorithms, Deep Neuron Network (DNN) exhibited the lowest accuracy at 0.84. At the same time, LR presented a 0.97 accuracy rate, yet its precision at 0.57, recall at 0.48 and F1-score at 0.51 were significantly lower, indicating poor performance in identifying cyberattacks. These two algorithms were affected by imbalanced dataset – outnumber of Benign traffic. In contrast, the top performance models were RF, KNN, and DT. Both RF and DT algorithms achieved a perfect accuracy score of 1.00. While KNN was closely with 0.99 accuracy, it required considerably more computational time, making it less suitable for real-time deployment.

Additionally, CV results also supported the consistency of these models. RF with both estimators maintained strong efficiency with 0.99 accuracy, while DT showed slightly more variability in precision, recall, and F1 scores. Throughout all evaluation metrics, RF, with 50 estimators, was selected as the most accurate and smaller computational time compared to 100 estimators for deployment in the intrusion detection system. This study’s results were aligned with [7, 9]. Meanwhile, DL, 0.84 accuracy, was lower than [8], indicating 98.97%, which was only trained by DDoS attack. 

![image](https://github.com/user-attachments/assets/98be7c7c-865c-4212-9503-62af728314c6)

Fig. 1. Confusion Metrics of Random Forest

## B.	SIEM Dashboard

The proposed SIEM successfully integrated with ML model and real-time monitoring capabilities. Although evaluation has not yet been conducted, the functional behavior demonstrated correct performance. The system allowed users to upload CSV files containing network traffic. After processing the data, the dashboard displayed the prediction results with a list of detected threats along with bar and pie charts, as shown in Fig 2. Moreover, the system extracted source IP addresses, providing a downloadable result and IP blocklist to support prevention.

The real-time monitored by parsing the logs from Suricata, depicted in Fig 3. The alerts based on Suricata rules were pushed to backend and reflected on the dashboard, which displayed both a list of detections and a list of IPs to block. The dashboard provided buttons to download the results for both detection and IP blocklist. Nevertheless, the real-time detection alerted from Suricata was predicted as Suricata Alert instead of the specific threat type, the system should be assessed and improve signature extraction for future work. 

![image](https://github.com/user-attachments/assets/9e5fd31b-5c4a-4df2-b1b3-73d9839be7a8)

Fig. 2. Threat Detection Results from Uploaded Network Traffic

![image](https://github.com/user-attachments/assets/155c75af-8910-4df5-b085-a5864cd1bb75)

Fig. 3. Real-Time SIEM Monitoring	

# Conclusion and Recommendations
## A.	Recommendations

Currently, the proposed SIEM tool was successfully deployed on cloud and worked properly. However, real-time alerts from Suricata were labeled incorrectly. It is suggested to improve these alerts by mapping them to a threat type. Future work should include performance evaluation of the system. Automated incident response should be considered to forward the IP blocklist to firewalls. Additional functions should be implemented. Furthermore, the logs for real-time detection should be extended to include system logs, cloud logs, or endpoint data.
 
## B.	Conclusion

Due to an increase of data or internet utilization, traditional IDS/IPS encounters false positive and false negative. ML provides solutions to handle large data feed and high performance. RF indicated excellent performance among the selected algorithms: LR, KNN, and DT. RF was deployed on cloud to build SIEM to simulate SOC environment. The proposed SIEM system demonstrated a successful integration between ML and real-time monitoring. The system allowed interactive analysis through user-friendly dashboard, enabling security analysts to view threat detection, download alerts, and monitor live IP blocklist. The system architecture leveraged Flask and Streamlit, which offers integration with external alert feeds. Although the system could perform successfully, the system should be assessed or evaluated to improve its performance. Log extension should be considered by including cloud log, and endpoint log. The SIEM tool should be developed to simulate real scenario as SOC analyst for future work.

# REFERENCES
[1] F. Zhao, H. Li, K. Niu, J. Shi, and R. Song, “Application of deep learning-based intrusion detection system (IDS) in network anomaly traffic detection,” Applied and Computational Engineering 86: 231-237, 2024, doi: 10.54254/2755-2721/86/20241604

[2] S. Omar, A. Ngadi, and H. H. Jebur, “Machine Learning Techniques for Anomaly Detection: An Overview,” International Journal of Computer Applications, vol. 79 no. 2, October 2013.

[3] H. Liu, and B. Lang, “Machine Learning and Deep Learning Methods for Intrusion Detection Systems: A Survey,” applied sciences, vol. 9, no. 20, October 2019, doi: 10.3390/app9204396

[4] S. Das and M. J. Nene, "A survey on types of machine learning techniques in intrusion prevention systems," 2017 International Conference on Wireless Communications, Signal Processing and Networking (WiSPNET), Chennai, India, 2017, pp. 2296-2299, doi: 10.1109/WiSPNET.2017.8300169.

[5] J. A. Abraham and V. R. Bindu, "Intrusion Detection and Prevention in Networks Using Machine Learning and Deep Learning Approaches: A Review," 2021 International Conference on Advancements in Electrical, Electronics, Communication, Computing and Automation (ICAECA), Coimbatore, India, 2021, pp. 1-4, doi: 10.1109/ICAECA52838.2021.9675595.

[6] V. Praneeth, K.R. Kumar, and N. Karyemsetty, “Security: intrusion prevention system using deep learning on the internet of vehicles,” International Journal of Safety and Security Engineering, vol. 11, no. 3, June 2021, pp. 231 – 237, doi: 10.18280/ijsse.110303

[7] M. R. Islam, M. Nasiruddin, M. Karmakar, R. Akter, M. T. Khan, A. A. Sayeed, and A. Amin, "Leveraging advanced machine learning algorithms for enhanced cyberattack detection on US business networks," J. Bus. Manag. Stud., vol. 6, no. 5, pp. 213–224, 2024.

[8] M. Gopalsamy, "Predictive cyber attack detection in cloud environments with machine learning from the CICIDS 2018 dataset," Int. J. Sci. Res. Technol. (IJSART), vol. 10, no. 10, 2024.

[9] E. Berei, M. A. Khan and A. Oun, "Machine Learning Algorithms for DoS and DDoS Cyberattacks Detection in Real-Time Environment," 2024 IEEE 21st Consumer Communications & Networking Conference (CCNC), Las Vegas, NV, USA, 2024, pp. 1048-1049, doi: 10.1109/CCNC51664.2024.10454755.







