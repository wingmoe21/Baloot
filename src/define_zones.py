from collections import deque
from datetime import datetime

import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")
# 1- no dublicates in logs 2- center cant win a round 3- max 8 rounds then reset 4- a way to determain winner
cap = cv2.VideoCapture(0)

# Zones
ZONES = {
    "P1": (213, 0, 426, 160),
    "P2": (426, 160, 640, 320),
    "P3": (213, 320, 426, 480),
    "P4": (0, 160, 213, 320),
    "CENTER": (213, 160, 426, 320)
}

def get_zone(xc, yc):
    for player, (x1, y1, x2, y2) in ZONES.items():
        if x1 <= xc <= x2 and y1 <= yc <= y2:
            return player
    return "UNKNOWN"

# Active round tracking
round_cards = {}
past_rounds = []
card_history = deque(maxlen=20)  # Store last 20 frames

round_id = 1
collecting = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, verbose=False)
    detected = []

    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            xc = int((x1 + x2) / 2)
            yc = int((y1 + y2) / 2)
            label = model.names[int(box.cls[0])]
            zone = get_zone(xc, yc)

            detected.append({'label': label, 'center': (xc, yc), 'zone': zone})

            # Draw
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f"{label} ({zone})", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    # Update history
    card_history.append(detected)

    # Check if 4 cards are in CENTER → start round
    center_cards = [c for c in detected if c["zone"] == "CENTER"]
    if len(center_cards) == 4 and not collecting:
        round_cards = {c["label"]: c for c in center_cards}
        collecting = True
        print(f"[ROUND {round_id} STARTED] Cards: {[c['label'] for c in center_cards]}")

    # If collecting, check where the cards go next
    if collecting:
        current_labels = {c['label'] for c in detected}
        all_moved = all(label not in current_labels for label in round_cards.keys())

        if all_moved:
            # Wait for cards to reappear in a player zone
            for past_frame in reversed(card_history):
                candidates = [c for c in past_frame if c['label'] in round_cards]
                if candidates and len(set(c['zone'] for c in candidates)) == 1:
                    winner = candidates[0]['zone']
                    print(f"[ROUND {round_id} WINNER] Player: {winner} took {list(round_cards.keys())}")
                    past_rounds.append({
                        "round": round_id,
                        "winner": winner,
                        "cards": list(round_cards.keys()),
                        "time": datetime.now().strftime("%H:%M:%S")
                    })
                    round_id += 1
                    round_cards = {}
                    collecting = False
                    break

    for name, (x1, y1, x2, y2) in ZONES.items():
        color = (0, 0, 255) if name == "CENTER" else (255, 0, 0)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, name, (x1 + 5, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow("Baloot Round Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save to file
with open("round_log.txt", "w") as f:
    for r in past_rounds:
        f.write(f"{r['time']} - Round {r['round']}: {r['winner']} won with {r['cards']}\n")

cap.release()
cv2.destroyAllWindows()