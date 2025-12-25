# Predicting Crime Hotspots for Public Safety Using Big Data Analytics
*A PySpark-based Approach to Geospatial and Temporal Crime Analysis*

This project leverages Big Data analytics, geospatial analysis, and machine learning to identify crime hotspots and uncover temporal and spatial crime patterns. Using a large-scale crime dataset from the [Chicago Police Department](https://data.cityofchicago.org/), the system provides actionable insights to support proactive law enforcement and public safety planning.

---

## Project Objectives
- Analyze large-scale crime data to identify high-risk areas
- Explore temporal crime trends and seasonality
- Detect crime hotspots using unsupervised learning
- Enable data-driven decision-making for public safety agencies

---

## Dataset
- **Source:** [Chicago Police Department (public crime records)](https://data.cityofchicago.org/)  
- **Size:** 7.8M+ records, 22 attributes  
- **Time Range:** 2001–2024 (adjust as needed)  
- **Key Features:**  
  - **Crime details:** primary type, description, arrest, domestic  
  - **Temporal data:** date, year, month, day-of-week  
  - **Geospatial data:** latitude, longitude, community area

---

## Technologies Used
- **Big Data Processing:** Apache Spark (PySpark)  
- **Programming:** Python (Pandas, NumPy, Matplotlib, Seaborn)  
- **Machine Learning:** Spark MLlib (K-Means Clustering, Feature Engineering)  
- **Analysis:** Geospatial & Temporal Analysis

---

## Data Processing Pipeline
1. **Data Ingestion**
   - Combined multiple CSV files into a single Spark DataFrame
   - Processed over 7.8 million records

2. **Data Cleaning & Preprocessing**
   - Handled missing and invalid values
   - Converted date fields to timestamps
   - Filtered incomplete records in critical columns

3. **Feature Engineering**
   - Extracted year, month, and day-of-week
   - Prepared latitude and longitude features for clustering
   - Scaled features for K-Means clustering

---

## Analysis & Insights

### Temporal Analysis
- Crime rates peak during summer months (June–August)
- Lower crime activity observed in winter months
- Overall decline in crime trends over recent years

### Spatial Analysis
- Identified high-crime community areas such as Austin, Near North Side, and Englewood
- Majority of crimes occur in public spaces like streets and sidewalks

---

## Hotspot Detection (Machine Learning)
- Applied **K-Means clustering** on latitude and longitude features
- Grouped crime incidents into high-density geographical clusters
- Identified urban crime hotspots aligned with major roads and high-traffic areas
- **Number of clusters:** 15 (chosen based on silhouette score and elbow method)

---

## Key Takeaways
- Big Data analytics enables proactive crime prevention
- Geospatial clustering reveals actionable crime hotspots
- Temporal patterns help optimize resource allocation
- Supports data-driven public safety strategies

---

## Future Improvements
- Incorporate predictive models for future crime forecasting
- Add interactive crime heatmaps using GIS tools
- Integrate socioeconomic and weather data for deeper insights
- Deploy as a real-time monitoring dashboard
- Explore streaming data for immediate hotspot detection

---

## Contributors
- Zain Nofal
- Ibrahim Mehmood

---

## License
This project is licensed under the MIT License.
