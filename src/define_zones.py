# Define static zones (you can calibrate later based on resolution)
PLAYER_ZONES = {
    "P1": (0, 0, 320, 240),
    "P2": (320, 0, 640, 240),
    "P3": (0, 240, 320, 480),
    "P4": (320, 240, 640, 480)
}

def get_player_for_card(card_bbox):
    x1, y1, x2, y2 = card_bbox
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    for player, (zx1, zy1, zx2, zy2) in PLAYER_ZONES.items():
        if zx1 <= cx <= zx2 and zy1 <= cy <= zy2:
            return player
    return "Unknown"
