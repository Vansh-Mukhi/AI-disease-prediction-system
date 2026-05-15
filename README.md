# AI Multi-Disease Prediction System

A production-ready, microservices-based web application to predict multiple diseases using Machine Learning.

## 🚀 Project Overview
This project is built for a final-year B.Tech project. It leverages Machine Learning to predict the likelihood of a patient having:
- Diabetes
- Heart Disease
- Parkinson's Disease
- Liver Disease
- Kidney Disease

The system is fully containerized using Docker and Docker Compose, following a robust microservices architecture.

## 🏗️ Architecture Diagram
```text
[ User (Browser) ]
        |
        v
[ Nginx API Gateway (:80) ]
        |
    +---+---+
    |       |
    v       v
[ Frontend ] [ Backend Flask API (:5000) ]
(Static UI)     |          |
                |          |
                v          v
   [ ML Predictor (:5001) ] [ MongoDB (:27017) ]
        (Scikit-Learn)         (User Data & History)
```

## 🛠️ Tech Stack
- **Frontend**: HTML5, CSS3 (Glassmorphism, Modern UI), Vanilla JS
- **Backend API**: Python 3.10, Flask, PyJWT, bcrypt
- **ML Service**: Flask, Scikit-Learn, Pandas, NumPy, Joblib
- **Database**: MongoDB
- **DevOps**: Docker, Docker Compose, Nginx

## ⚙️ Installation & Setup

### Prerequisites
- Docker
- Docker Compose

### Step-by-Step Guide
1. **Clone the repository** (if applicable) or navigate to the project root directory.

2. **Build and Start Services**:
   ```bash
   docker-compose up --build -d
   ```
   *This command will build the frontend, backend, and ml-service images, start MongoDB and Redis, generate the trained ML models, and boot up the Nginx gateway.*

3. **Access the Application**:
   - Web Interface: http://localhost
   - Backend API: http://localhost/api/
   - ML Service (Internal): http://localhost:5001

4. **Stopping the Services**:
   ```bash
   docker-compose down
   ```

## 📚 API Documentation

### Authentication Routes (`/api/auth`)
- `POST /signup` - Register a new user. Body: `{ "name": "", "email": "", "password": "" }`
- `POST /login` - Login. Body: `{ "email": "", "password": "" }`

### Prediction Routes (`/api/predict`) - Requires JWT
- `POST /diabetes` - Predict diabetes. Body: `{ "features": [8 numeric values] }`
- `POST /heart` - Predict heart disease. Body: `{ "features": [13 numeric values] }`
- `POST /parkinsons` - Predict Parkinson's. Body: `{ "features": [22 numeric values] }`
- `POST /liver` - Predict liver disease. Body: `{ "features": [10 numeric values] }`
- `POST /kidney` - Predict kidney disease. Body: `{ "features": [24 numeric values] }`

### User Routes (`/api/user`) - Requires JWT
- `GET /profile` - Get logged-in user details.
- `GET /history` - Get user's prediction history.

## 🧠 Machine Learning Models
Currently, the system automatically trains and serializes *synthetic* Random Forest classifiers on startup using Scikit-Learn's `make_classification`. This ensures the API pipeline is instantly fully functional out of the box for demonstration purposes.

To use real medical datasets, simply replace the data loading logic in `ml-service/training/train_models.py` with your real `.csv` files (e.g., UCI Machine Learning Repository datasets).

## 🔮 Future Improvements
- Integrate real clinical datasets for higher accuracy.
- Add Redis caching for frequently requested predictions.
- Set up CI/CD pipelines using GitHub Actions.
- Deploy to AWS/GCP using Kubernetes (Minikube/EKS).
- Implement a graphical Admin Panel for user management.
