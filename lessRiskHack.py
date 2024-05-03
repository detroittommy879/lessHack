import pyuac
import time
import os
from pynput import mouse

def main():
    print("This is running as an admin!")
    sec = 5000  # Set the number of seconds for the countdown
    idle_time_start = None
    countdown_seconds = sec
    wifi_disabled = False  # Track the WiFi state

    def manage_wifi(state):
        """ Enable or disable WiFi based on the state. """
        command = "enable" if state else "disable"
        os.system(f"netsh interface set interface \"Wi-Fi\" {command}")
        print(f"WiFi {command}d.")

    def on_move(x, y):
        nonlocal idle_time_start, countdown_seconds, wifi_disabled
        idle_time_start = None
        countdown_seconds = sec  # Reset countdown
        if wifi_disabled:
            manage_wifi(True)
            wifi_disabled = False

    def on_scroll(x, y, dx, dy):
        on_move(x, y)  # Call the on_move function since the logic is the same

    # Start listening for mouse events
    listener = mouse.Listener(on_move=on_move, on_scroll=on_scroll)
    listener.start()

    while True:
        if idle_time_start is None:
            idle_time_start = time.time()
        elif time.time() - idle_time_start > 1:  # Check every second
            countdown_seconds -= 1
            #print(f"Seconds until WiFi turns off: {countdown_seconds}")
            print(f"\rSeconds until WiFi turns off: {countdown_seconds}", end="")
            if countdown_seconds == 0:
                # Turn off WiFi when countdown reaches 0
                manage_wifi(False)
                wifi_disabled = True
                countdown_seconds = sec  # Reset countdown

        time.sleep(1)

    # This line will not be reached; consider handling this in a control structure if necessary.
    input("Press Enter to close the window.")

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:
        main()