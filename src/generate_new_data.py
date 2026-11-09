import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

# Project Constants
NUM_ACCIDENTS = 12000
LOCALITIES = ['Kalyani', 'Bandel', 'Kolkata', 'Howrah', 'Hooghly', 'Burdwan']
ACCIDENT_TYPES = ['Two-wheeler crash', 'Pedestrian collision', 'Vehicle collision', 'Heavy Truck accident']
SEVERITIES = ['Minor', 'Serious', 'Critical', 'Fatal']

print("Generating 8 Relational CSV Files (12,000+ Records) as per Sir's requirement...")

# ==========================================
# 1. Generate Road Segments
# ==========================================
road_ids = [f"RD{str(i).zfill(3)}" for i in range(1, 101)]
road_segments = pd.DataFrame({
    'road_id': road_ids,
    'road_name': [f"Road_{i}" for i in range(1, 101)],
    'locality': np.random.choice(LOCALITIES, 100),
    'road_type': np.random.choice(['Highway', 'Arterial', 'Local', 'Intersection'], 100),
    'lanes': np.random.choice([2, 4, 6], 100),
    'speed_limit': np.random.choice([40, 60, 80], 100),
    'lighting': np.random.choice(['Good', 'Poor', 'None'], 100),
    'surface_condition': np.random.choice(['Dry', 'Wet', 'Potholes'], 100),
    'traffic_signal': np.random.choice(['Yes', 'No'], 100)
})
road_segments.to_csv(os.path.join(RAW_DIR, 'road_segments.csv'), index=False)

# ==========================================
# 2. Generate Accidents
# ==========================================
acc_ids = [f"ACC{str(i).zfill(5)}" for i in range(1, NUM_ACCIDENTS + 1)]
dates = [(datetime(2026, 1, 1) + timedelta(days=random.randint(0, 300))) for _ in range(NUM_ACCIDENTS)]
assigned_roads = np.random.choice(road_ids, NUM_ACCIDENTS)

# Link localities based on the road selected
road_locality_dict = dict(zip(road_segments.road_id, road_segments.locality))
acc_localities = [road_locality_dict[r] for r in assigned_roads]

accidents = pd.DataFrame({
    'accident_id': acc_ids,
    'date': [d.strftime("%Y-%m-%d") for d in dates],
    'time': [f"{random.randint(0,23):02d}:{random.randint(0,59):02d}" for _ in range(NUM_ACCIDENTS)],
    'road': assigned_roads,
    'locality': acc_localities,
    'latitude': np.random.uniform(22.0, 23.0, NUM_ACCIDENTS),
    'longitude': np.random.uniform(88.0, 89.0, NUM_ACCIDENTS),
    'accident_type': np.random.choice(ACCIDENT_TYPES, NUM_ACCIDENTS, p=[0.4, 0.2, 0.3, 0.1]),
    'severity': np.random.choice(SEVERITIES, NUM_ACCIDENTS, p=[0.5, 0.3, 0.15, 0.05]),
    'vehicles_involved': np.random.choice([1, 2, 3], NUM_ACCIDENTS, p=[0.5, 0.4, 0.1]),
    'fatalities': np.random.choice([0, 1, 2, 3], NUM_ACCIDENTS, p=[0.85, 0.10, 0.04, 0.01]),
    'injuries': np.random.randint(0, 5, NUM_ACCIDENTS)
})
accidents.to_csv(os.path.join(RAW_DIR, 'accidents.csv'), index=False)

# ==========================================
# 3. Generate Vehicles
# ==========================================
vehicles = pd.DataFrame({
    'vehicle_id': [f"VEH{str(i).zfill(5)}" for i in range(1, NUM_ACCIDENTS + 1)],
    'accident_id': acc_ids,
    'vehicle_type': np.random.choice(['Car', 'Motorcycle', 'Bus', 'Truck', 'Bicycle'], NUM_ACCIDENTS),
    'driver_age_group': np.random.choice(['18-25', '26-40', '41-60', '60+'], NUM_ACCIDENTS),
    'direction': np.random.choice(['North', 'South', 'East', 'West'], NUM_ACCIDENTS),
    'damage_level': np.random.choice(['Minor', 'Moderate', 'Severe', 'Totaled'], NUM_ACCIDENTS)
})
vehicles.to_csv(os.path.join(RAW_DIR, 'vehicles.csv'), index=False)

# ==========================================
# 4. Generate Responses
# ==========================================
alert_times = pd.to_datetime(accidents['date'] + " " + accidents['time']) + pd.to_timedelta(np.random.randint(2, 15, NUM_ACCIDENTS), unit='m')
dispatch_times = alert_times + pd.to_timedelta(np.random.randint(1, 5, NUM_ACCIDENTS), unit='m')
arrival_times = dispatch_times + pd.to_timedelta(np.random.randint(5, 30, NUM_ACCIDENTS), unit='m')
clearance_times = arrival_times + pd.to_timedelta(np.random.randint(20, 120, NUM_ACCIDENTS), unit='m')

responses = pd.DataFrame({
    'response_id': [f"RES{str(i).zfill(5)}" for i in range(1, NUM_ACCIDENTS + 1)],
    'accident_id': acc_ids,
    'alert_time': alert_times.dt.strftime("%Y-%m-%d %H:%M:%S"),
    'dispatch_time': dispatch_times.dt.strftime("%Y-%m-%d %H:%M:%S"),
    'arrival_time': arrival_times.dt.strftime("%Y-%m-%d %H:%M:%S"),
    'clearance_time': clearance_times.dt.strftime("%Y-%m-%d %H:%M:%S"),
    'response_team': np.random.choice(['Team Alpha', 'Team Bravo', 'Team Charlie'], NUM_ACCIDENTS)
})
responses.to_csv(os.path.join(RAW_DIR, 'responses.csv'), index=False)

# ==========================================
# 5. Generate Road Users
# ==========================================
road_users = pd.DataFrame({
    'accident_id': acc_ids,
    'user_type': np.random.choice(['Driver', 'Passenger', 'Pedestrian', 'Cyclist'], NUM_ACCIDENTS),
    'age_group': np.random.choice(['Child', 'Youth', 'Adult', 'Senior'], NUM_ACCIDENTS),
    'gender': np.random.choice(['Male', 'Female', 'Other'], NUM_ACCIDENTS),
    'injury_status': accidents['severity'],
    'safety_equipment': np.random.choice(['Helmet', 'Seatbelt', 'None'], NUM_ACCIDENTS)
})
road_users.to_csv(os.path.join(RAW_DIR, 'road_users.csv'), index=False)

# ==========================================
# 6. Generate Blackspots
# ==========================================
blackspots = pd.DataFrame({
    'blackspot_id': [f"BS{str(i).zfill(3)}" for i in range(1, 21)],
    'road_id': np.random.choice(road_ids, 20, replace=False),
    'location': [f"Intersection {i}" for i in range(1, 21)],
    'identified_date': [(datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d") for _ in range(20)],
    'intervention_type': np.random.choice(['Speed Bump', 'New Traffic Light', 'Street Lighting'], 20),
    'intervention_date': [(datetime(2026, 1, 1) + timedelta(days=random.randint(0, 100))).strftime("%Y-%m-%d") for _ in range(20)],
    'status': np.random.choice(['Monitored', 'Resolved'], 20)
})
blackspots.to_csv(os.path.join(RAW_DIR, 'blackspots.csv'), index=False)

# ==========================================
# 7. Generate Weather
# ==========================================
weather_dates = pd.date_range(start='2026-01-01', end='2026-10-30')
weather_records = []
for d in weather_dates:
    for loc in LOCALITIES:
        weather_records.append({
            'date': d.strftime("%Y-%m-%d"),
            'time': '12:00:00',
            'locality': loc,
            'rainfall_mm': round(random.uniform(0, 50), 1) if random.random() > 0.8 else 0,
            'temperature_c': random.randint(15, 40),
            'visibility_km': random.randint(1, 10),
            'weather_condition': np.random.choice(['Clear', 'Rain', 'Fog'], p=[0.7, 0.2, 0.1])
        })
weather = pd.DataFrame(weather_records)
weather.to_csv(os.path.join(RAW_DIR, 'weather.csv'), index=False)

# ==========================================
# 8. Generate Traffic Volume
# ==========================================
traffic_volume = pd.DataFrame({
    'date': [(datetime(2026, 1, 1) + timedelta(days=random.randint(0, 300))).strftime("%Y-%m-%d") for _ in range(2000)],
    'time': [f"{random.randint(0,23):02d}:00" for _ in range(2000)],
    'road_id': np.random.choice(road_ids, 2000),
    'vehicle_count': np.random.randint(500, 5000, 2000),
    'average_speed': np.random.randint(20, 80, 2000)
})
traffic_volume.to_csv(os.path.join(RAW_DIR, 'traffic_volume.csv'), index=False)

print("✅ All 8 CSV files have been successfully created in 'data/raw/'!")