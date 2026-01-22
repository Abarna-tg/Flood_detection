🌊 Green AI – Flood Prediction and Visualization System
📌 Project Overview

This project focuses on providing location-based flood awareness using data-driven analysis and interactive maps.
By taking a user’s place name as input, the system identifies the user’s geographic location, locates the three nearest dams, analyzes rainfall and water resource data, and visualizes potential flood risk on a map.
The project follows a Green AI approach, ensuring low computational cost while delivering meaningful societal impact.

🎯 Problem Statement

Flood-related damages increase due to delayed warnings, fragmented data sources, and lack of clear visualization for the public.
Existing systems are often complex and not easily understandable by common users.
This project aims to bridge that gap by offering a simple, visual, and data-driven flood awareness system.

💡 Solution Approach

User provides a place name as input

The system converts the place into latitude and longitude

The three nearest dams are identified using geographic distance

Rainfall and dam water level data are analyzed

Flood risk is visually highlighted on an interactive map

Note: This version avoids SMS or notification services and focuses purely on visual decision support.

🧠 Use of AI

This project does not use deep learning models in its current version.
Instead, it applies AI-inspired data analysis techniques, including:

Data preprocessing

Rule-based risk assessment

Geographic intelligence

Intelligent visualization

These techniques enable informed decision-making without heavy computational overhead, aligning with Green AI principles.

🗺️ Key Features

User location identification

Nearest dam detection (Top 3)

Rainfall and water resource analysis

Interactive flood risk map

Low-power, eco-friendly computation

🛠️ Technology Stack

Programming Language: Python

Platform: Google Colab

Libraries Used:

Pandas

Geopy

Folium

TQDM

Data Source: Tamil Nadu water resources dataset

🚀 How to Run the Project
Step 1: Install Required Libraries
pip install pandas geopy folium tqdm

Step 2: Upload Dataset

Upload the file tamilnadu_water_resources.csv to your Google Colab environment.

Step 3: Execute the Notebook

Run all cells in sequence

Enter the place name when prompted

View the generated interactive map output

👥 Target Users

General public

Disaster management authorities

Researchers and students

Local administrative bodies

🌟 Highlights

Map-based flood awareness system

Simple user input with clear visual output

Green AI approach with minimal computational load

Practical real-world application

🔮 Future Enhancements

Machine learning-based flood prediction

Real-time rainfall API integration

Mobile-responsive dashboard

Historical flood trend analysis

📚 Conclusion

This project demonstrates that effective flood awareness does not require complex or resource-intensive AI models.
By combining geographic intelligence, data analysis, and visualization, it delivers a practical and environmentally responsible solution aligned with Green AI principles.
