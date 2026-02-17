import time
import threading
import libre_monitor # Ensure this has your updated get_current_value
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw, ImageFont
from collections import deque

history_log = deque(maxlen=5)
REFRESH_SECONDS = 60
_running = True

def fetch_bg_value():
    token, account_id = libre_monitor.login_get_auth()
    user_id = libre_monitor.get_user_id(token, account_id)
    return libre_monitor.get_current_value(token, user_id, account_id)

# -----------------------------
# Icon Rendering
# -----------------------------
def create_text_icon(text, is_arrow=False):
    # Using 32x32 for high-DPI crispness
    SIZE = 32
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Use a thick, bold font. 
    # If it's an arrow, we might want it slightly larger.
    font_size = 30 if is_arrow else 26
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", font_size)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # Precise centering
    x = (SIZE - w) // 2 - bbox[0]
    y = (SIZE - h) // 2 - bbox[1]
    
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    return img

def update_icons(icon_l, icon_r):
    global _running
    while _running:
        try:
            glucose_raw, trend, api_time = fetch_bg_value()
            glucose_str = str(glucose_raw)

            # Add to history (store as a formatted string)
            history_entry = f"{glucose_raw} {trend} ({api_time})"
            hover_text = f"{glucose_raw} {trend} {api_time[-5:]}"
            history_log.appendleft(history_entry) # newest at the top

            # Logic for First 2 Characters
            display_val = glucose_str[:2]
            if "." in display_val:
                display_val = glucose_str[0]

            # Update Icons
            icon_l.icon = create_text_icon(display_val, is_arrow=False)
            icon_l.title = hover_text
            icon_r.icon = create_text_icon(trend, is_arrow=True)
            icon_r.title = hover_text

            # Rebuild the menu to show the latest history
            new_menu = build_menu(icon_l, icon_r)
            icon_l.menu = new_menu
            icon_r.menu = new_menu
            
        except Exception as e:
            print(f"Update error: {e}")
        
        time.sleep(REFRESH_SECONDS)

# -----------------------------
# Menu Builder
# -----------------------------
def build_menu(icon_l, icon_r):
    # Create a list of MenuItems from the history_log
    # We use 'enabled=False' to make them read-only (grayed out/unclickable)
    history_items = [MenuItem(item, lambda: None, enabled=False) for item in history_log]

    return Menu(
        MenuItem("- History -", lambda: None, enabled=False),
        *history_items,
        Menu.SEPARATOR,
        MenuItem("Quit All", lambda icon, item: on_quit_all(icon_l, icon_r))
    )

def on_quit_all(icon_l, icon_r):
    global _running
    _running = False
    icon_l.stop()
    icon_r.stop()
# -----------------------------
# Main Entry Point
# -----------------------------
def on_quit(icon, item):
    global _running
    _running = False
    icon.stop()

def main():
    # Initial placeholders
    icon_l = Icon("glucose_val", create_text_icon(".."), title="Fetching...")
    icon_r = Icon("trend_arrow", create_text_icon(".."), title="Fetching...")

    menu = Menu(MenuItem("Quit All", on_quit))
    icon_l.menu = menu
    icon_r.menu = menu

    # Background Thread
    updater = threading.Thread(target=update_icons, args=(icon_l, icon_r), daemon=True)
    updater.start()

    # Run icons (one in thread, one in main loop)
    threading.Thread(target=icon_r.run, daemon=True).start()
    time.sleep(0.5) # Brief pause to ensure R registers first
    icon_l.run()

if __name__ == "__main__":
    main()