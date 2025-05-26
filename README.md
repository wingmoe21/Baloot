# 🃏 Baloot AI Game Tracker

An AI-powered system that uses computer vision to track the gameplay of the popular Middle Eastern card game **Baloot**. This tool detects cards on the table using a webcam, identifies which player played each card, and automatically applies Baloot rules to calculate scores for each team.

## 🎯 Project Goals

- Detect playing cards in real-time using a camera and YOLOv8.
- Assign cards to one of four players based on position.
- Evaluate tricks based on صن or حكم game logic.
- Display real-time scoring and game progression.
- (Optional) Export game data for replays or analytics.

---

## 🧠 Technologies Used

- **YOLOv8** (Ultralytics) – Card detection
- **OpenCV** – Image and video processing
- **Python** – Core game logic
- **Tkinter / Streamlit** – UI (for scoreboard and visualizations)
- **LabelImg** – Manual annotation tool for training

---

## 🗂️ Project Structure

baloot-ai/
├── data/ # Card images and YOLO labels
├── models/ # Trained YOLOv8 models
├── src/
│ ├── detect_cards.py # Detect cards from webcam
│ ├── define_zones.py # Assign cards to players
│ ├── game_logic.py # Evaluate Baloot rules
│ ├── main.py # Entry point
│ └── utils.py # Helper functions
├── ui/
│ └── scoreboard.py # Simple game UI
├── requirements.txt # Python dependencies
└── README.md # You're here!

---

## 🚀 Getting Started

### 1. Create Virtual Environment
```sh
python -m venv venv
venv\\Scripts\\activate  # or source venv/bin/activate on Mac
yolo detect train data=data/data.yaml model=yolov8n.pt epochs=50 imgsz=640
```
### 2. Install Requirements
``` sh
pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html
```