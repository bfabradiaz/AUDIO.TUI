import pyautogui
import platform

class MediaController:
    """Handles system-wide media control simulation."""
    
    def __init__(self):
        # Configure pyautogui to not fail safe (we don't need mouse movement safety here)
        pyautogui.FAILSAFE = False
        self.os_name = platform.system()

    def play_pause(self):
        """Simulate Play/Pause media key."""
        pyautogui.press('playpause')

    def next_track(self):
        """Simulate Next Track media key."""
        pyautogui.press('nexttrack')

    def prev_track(self):
        """Simulate Previous Track media key."""
        pyautogui.press('prevtrack')

    def volume_up(self):
        """Simulate Volume Up media key."""
        pyautogui.press('volumeup')

    def volume_down(self):
        """Simulate Volume Down media key."""
        pyautogui.press('volumedown')

    def stop(self):
        """Simulate Stop media key."""
        pyautogui.press('stop')
