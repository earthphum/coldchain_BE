# ColdChain++ 
## Overview
ColdChain++ is a backend system that manages real-time sensor data (temperature, humidity, location) for cold chain logistics. It works with OSRM to find the best routes automatically. The system also handles orders, customer information, and rider history, making it easy to plan and track deliveries. This helps maintain product quality, reduce travel time, and improve overall cold chain operations.
## Detail : TSP Solver using OSRM + Dynamic Programming
This project solves the classic Traveling Salesman Problem (TSP) using a combination of OSRM (Open Source Routing Machine) and Dynamic Programming with Bitmasking. The goal is to find the shortest possible route that visits each location exactly once and returns to the starting point.
###  Using OSRM for Real-World Distance
I use OSRM to calculate real driving distances between coordinates (not just straight-line distance). The result is a distance matrix that serves as input to the TSP algorithm.
  - OSRM considers actual road networks, which makes results more accurate for real-world use cases like delivery routes or travel planning.
### Solving TSP with Dynamic Programming
Once I have the > *distance_matrix* < , I apply a Dynamic Programming (DP) + Bitmasking approach to solve the TSP efficiently:
 * It considers all subsets of visited cities.
 
 * It calculates the minimum cost to reach each city.
 
 * It uses backtracking to reconstruct the optimal path.
 
 * The output includes:
 
   * The minimum total travel distance
 
   * The optimal sequence of cities to visit

## Technical Details
Algorithms & Implementation
  * K-Means Clustering
     * Used for grouping delivery locations or sensor data points to streamline route planning and reduce computational overhead.
     * Clusters deliveries into routes for each rider
  * Dynamic Programming for solve Traveling Salesman Problem
     * Applied to create efficient delivery schedules that minimize total travel time.
  * OSRM Integration
     * Provides base distance matrix .
## Tech Stack
* Django 
* Django REST Framework
* djangorestframework-jwt
* django-cors-headers
* OSRM(Open Source Routing Machine)
## Project Structure
```bash
├── api_services
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models
│   │   ├── __init__.py
│   │   ├── customers_data.py
│   │   ├── orders_data.py
│   │   ├── origin_data.py
│   │   ├── rider_history_data.py
│   │   └── sensors_data.py
│   ├── serializers
│   │   ├── __init__.py
│   │   ├── customers_data_serializer.py
│   │   ├── orders_data_serializer.py
│   │   ├── origin_data_serializer.py
│   │   ├── rider_history_data_serializer.py
│   │   ├── route_planner_serializer.py
│   │   └── sensors_data_serializer.py
│   ├── services
│   │   ├── create_customer.py
│   │   └── route_planner_service.py
│   ├── urls.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── address_to_coordinate.py
│   │   ├── clustering.py
│   │   ├── dynamic_programming.py
│   │   └── traveling_salesman_problem.py
│   └── views
│       ├── __init__.py
│       ├── customers_data_view.py
│       ├── orders_data_view.py
│       ├── origin_data_view.py
│       ├── rider_history_data_view.py
│       ├── route_planner_view.py
│       └── sensor_data_view.py
├── coldchain
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── manage.py
```
## JWT Authentication Flow
1. Login (POST /api/login/token/)
  → Send username and password to receive access and refresh tokens.

2. Authenticated Access
  → Use the access token in the header as Authorization: Bearer <access_token> to access protected API routes.

3. Token Refresh (POST /api/login/token/refresh/)
  → Use the refresh token to get a new access token when the current one expires.

4. Logout (POST /api/login/token/logout)
→ Send the refresh token to blacklist it, effectively logging the user out.
## Installation
Before running this project, make sure to properly set the required **environment variables** or **configuration values**, especially:

- **GOOGLE_MAPS_API_KEY**: Your Google Maps API key.
- **OSRM_IP**: The URL or IP address for your OSRM service.
1. Clone the repository
   ```bash
     git clone https://github.com/earthphum/coldchain_backend.git
   ```
2. Create and activate a virtual environment
For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install the dependencies
``` bash
pip install -r requirements.txt
```
4. Set up the database
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create a superuser (admin account)
```bash
python manage.py createsuperuser
```
6. Run the development server
```bash
python manage.py runserver
```
## ⚠️ Important Notes for Production Deployment
Before deploying this Django project to production, please review and update the following security-critical settings:
### Secret Key
  * DO NOT use the development secret key in production.
  
  * Generate a new, strong, and unique secret key and store it securely (e.g., in environment variables).
``` python
# NEVER hardcode in production settings:
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
```
###  Debug Mode
* Set DEBUG = False in production to prevent sensitive error information from being exposed.
```python
DEBUG = False
```
### Allowed Hosts
* Replace ALLOWED_HOSTS = ['*'] with a list of trusted domain names/IPs:
```python
ALLOWED_HOSTS = ['yourdomain.com', 'api.yourdomain.com']
```
### CORS Policy
 * CORS_ALLOW_ALL_ORIGINS = True is dangerous in production.
 
 * Instead, define specific frontend origins that are allowed to access your API:
     ```python
         CORS_ALLOW_ALL_ORIGINS = False
         CORS_ALLOWED_ORIGINS = [
             "https://your-frontend-domain.com",
         ]
     ```
### Token Settings (SimpleJWT)
* Consider enabling the following for higher security:
  ```python
  "ROTATE_REFRESH_TOKENS": True,
  "BLACKLIST_AFTER_ROTATION": True,
  ```
### HTTPS & Headers
Always deploy behind HTTPS (use SSL).

Set security headers like:
 
 * SECURE_HSTS_SECONDS
 
 * SECURE_SSL_REDIRECT
 
 * SECURE_BROWSER_XSS_FILTER
 
 * SECURE_CONTENT_TYPE_NOSNIFF
 
 * SESSION_COOKIE_SECURE = True
 
 * CSRF_COOKIE_SECURE = True
## 🛡 License

This project is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

© 2025 Warodom Phumprasert  
Project, King Mongkut's Institute of Technology Ladkrabang

📖 [View License](https://creativecommons.org/licenses/by-nc-sa/4.0/)
