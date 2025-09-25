# Big Data Project Instructions and Scoring Framework

## 📘 Student Instruction Sheet

### 1. Project Overview
You will work in teams of 3 on one realistic Big Data scenario (allocated to you).  
Your project will simulate an **end-to-end Big Data pipeline**:  
**Ingestion → Storage → Processing → Analytics → Visualization → Business Insights**.  

Duration: **4 weeks** (compressed milestones).

---

### 2. Technical Requirements
- **Tools / Frameworks**:  
  • Hadoop ecosystem: HDFS, Hive, Spark (mandatory)  
  • Kafka/Flume/Sqoop optional but encouraged  
  • **Open-source visualization only**: Apache Superset, Redash, Grafana, Kibana, Zeppelin/Jupyter  
- **Data**: Use provided synthetic data configs (or open datasets). Scale: 1–5 GB.  
- **Environment**: Local (Docker/VM) or Cloud (Databricks, EMR, GCP).  

---

### 3. Execution Plan (Milestones)

| Week | Milestone              | Expected Outcome |
|------|------------------------|------------------|
| 1    | Setup & Data Acquisition | Install Hadoop ecosystem, finalize scenario, acquire/generate dataset |
| 2    | Ingestion & Storage    | Implement ingestion pipeline, load into HDFS Bronze/Silver/Gold, define Hive schema |
| 3    | Processing & Analytics | Develop Spark/MapReduce jobs for KPIs; optional MLlib/streaming |
| 4    | Insights & Visualization | Build dashboards (Superset/Redash/Grafana/Kibana/Zeppelin), deliver insights, report & demo |

---

### 4. Expected Outcomes
- End-to-end pipeline: ingestion → HDFS → Spark → Hive → dashboard  
- 3–5 KPIs per domain scenario  
- At least one actionable business recommendation  

---

### 5. Deliverables
- **Technical**: Code repo (ingestion, Spark jobs, schema)  
- **Business**: Dashboard + KPIs  
- **Report**: 12–15 pages  
- **Presentation**: Demo & slides (10 minutes)  

---

### 6. Factors Influencing Marks
- Robust setup of Hadoop ecosystem  
- Correct ingestion pipeline  
- Logical Bronze/Silver/Gold storage design  
- Efficiency and correctness of Spark jobs  
- Clarity & relevance of KPIs  
- Quality of dashboards (open-source)  
- Report depth & teamwork  

---
## 7. Team Allocation – Big Data Project

### Agriculture

1. Crop yield prediction using soil + weather data
2. Precision farming with IoT sensor streams
3. Market price trend analysis for major crops
4. Pest/disease outbreak detection via image/IoT feeds
5. Irrigation optimization using weather and soil moisture
6. Farm-to-market supply chain analytics
7. Climate-resilient seed variety performance analysis

### Healthcare

8. Patient readmission risk prediction
9. Real-time epidemic spread monitoring
10. Hospital resource utilization analytics
11. Medical image metadata lake & analysis
12. Wearables IoT patient vitals monitoring
13. Drug effectiveness and adverse reaction detection
14. Appointment no-show prediction and scheduling optimization

### Finance & Banking

15. Card transaction fraud detection
16. Customer segmentation and offers
17. Credit scoring with alternate data
18. Real-time transaction anomaly detection
19. Market sentiment vs price movement
20. ATM cash demand forecasting
21. Real-time AML suspicious pattern clustering

### Retail & E-Commerce

22. Product recommendation engines
23. Shopping basket analysis
24. Dynamic pricing optimization
25. Customer churn prediction
26. Review sentiment analysis
27. Supply chain/logistics optimization
28. Inventory stockout prediction and auto-replenishment

### Transportation

29. Route optimization for buses/trains
30. Real-time vehicle breakdown/delay detection
31. Ride demand forecasting (cab/auto services)
32. Traffic congestion prediction from IoT sensors
33. Ticketing & revenue leakage analysis
34. Multi-modal integration analytics
35. First/last-mile connectivity optimization

### Energy & Utilities

36. Smart grid load forecasting
37. Predictive maintenance of transformers
38. Energy theft anomaly detection
39. Solar/wind generation forecasting
40. Household consumption patterns
41. Dynamic electricity pricing
42. EV charging station load prediction

### Telecommunications

43. Call drop analysis and network optimization
44. Subscriber churn modeling
45. Usage behavior segmentation
46. SIM/identity fraud detection
47. Real-time network anomaly detection
48. Social graph analysis of call/data records
49. 5G small-cell placement optimization analytics

### Education

50. Student performance prediction & risk alerts
51. Adaptive learning recommendation engines
52. MOOC clickstream engagement
53. Skill gap analysis from course data
54. Placement/job market trend analytics
55. Admin resource allocation optimization
56. Proctoring anomaly detection in online exams

### Social Media

57. Topic sentiment tracking
58. Fake news/rumor detection
59. Influencer network analytics
60. Video recommendation telemetry
61. Toxic comment detection in communities
62. User engagement and churn analytics
63. Spam bot network detection via temporal behavior

### Government & Public Policy

64. Smart city sensor analytics
65. Crime hotspot prediction
66. Tax fraud detection in filings
67. Public welfare scheme usage analysis
68. Disaster response analytics
69. Citizen feedback policy sentiment
70. Public grievance redressal SLA compliance analytics

---
