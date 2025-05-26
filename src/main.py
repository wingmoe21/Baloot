import cv2

from define_zones import get_player_for_card
from detect_cards import detect_cards

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cards = detect_cards(frame)
    for card in cards:
        player = get_player_for_card(card['bbox'])
        label = f"{card['label']} ({player})"
        x1, y1, x2, y2 = map(int, card['bbox'])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    cv2.imshow("Baloot Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
