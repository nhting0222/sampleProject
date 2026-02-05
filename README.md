# Sample Projects Collection

This repository contains two full-stack web applications built with modern technologies.

## 🛡️ XDR Management Platform

A comprehensive Security Operations Center (SOC) platform for Extended Detection and Response (XDR).

### Features
- **Interactive Dashboard** with real-time charts and statistics
- **Security Events** monitoring and management
- **Incident Tracking** with detailed timelines
- **Asset Management** with risk scoring
- **Geographic Threat Map** for location-based threat visualization
- **Real-time Notifications** via WebSocket
- **Alert Rules** configuration
- **Reports** generation

### Tech Stack
- **Frontend**: Vue 3, Pinia, Vue Router, ECharts
- **Backend**: Python FastAPI, WebSocket
- **Features**: Real-time updates, Interactive charts, REST API

### Running the XDR Platform

#### Frontend
```bash
cd xdr-management
npm install
npm run dev
```
Access at: http://localhost:5175

#### Backend
```bash
cd xdr-management/backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
API docs at: http://localhost:8000/docs

---

## 🏠 Silver Share House

A modern platform for senior shared housing solutions.

### Features
- **House Listings** with search and filter
- **Detailed Property Views** with image galleries
- **Favorites System** with localStorage persistence
- **Contact Form** with validation
- **Responsive Design** for all devices
- **Toast Notifications** for user feedback
- **Page Transitions** and animations

### Tech Stack
- **Frontend**: Vue 3, Pinia, Vue Router
- **State Management**: Pinia with composables
- **Features**: SPA, Responsive UI, Form validation

### Running Silver Share House

```bash
cd silver-share-house
npm install
npm run dev
```
Access at: http://localhost:5174

---

## 📦 Project Structure

```
sample/
├── xdr-management/          # XDR Security Platform
│   ├── backend/             # FastAPI backend
│   │   ├── app/
│   │   │   ├── data/        # Mock data
│   │   │   └── models.py    # Pydantic models
│   │   ├── main.py          # FastAPI app
│   │   └── requirements.txt
│   └── src/                 # Vue frontend
│       ├── components/
│       ├── views/
│       ├── stores/
│       └── utils/
│
└── silver-share-house/      # Senior Housing Platform
    └── src/
        ├── components/
        ├── views/
        ├── stores/
        └── composables/
```

## 🚀 Key Technologies

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Next generation frontend tooling
- **Pinia** - State management
- **Vue Router** - Official router
- **FastAPI** - Modern Python web framework
- **ECharts** - Powerful charting library
- **WebSocket** - Real-time communication
- **Axios** - HTTP client

## 📊 XDR Dashboard Features

- Event trends (24-hour timeline)
- Severity distribution (pie chart)
- Event types (bar chart)
- Geographic threat distribution (interactive map)
- Response time trends
- Top affected assets
- MITRE ATT&CK coverage radar
- Recent incidents timeline

## 🎯 Silver Share House Features

- Advanced search with multiple filters
- Favorites management
- Form validation with custom composables
- Toast notification system
- Smooth page transitions
- Responsive card layouts

## 📝 License

This project is created for educational purposes.

## 👥 Contributors

- SOC Analyst
- Co-Authored-By: Claude Sonnet 4.5

---

Built with ❤️ using Vue 3 + FastAPI
