import ctypes
import winsound
import threading
import time

charging_sound_file = r"C:\Users\kench\Documents\iphone_charging_sound.wav"

class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ('ACLineStatus', ctypes.c_byte),
        ('BatteryFlag', ctypes.c_byte),
        ('BatteryLifePercent', ctypes.c_byte),
        ('Reserved1', ctypes.c_byte),
        ('BatteryLifeTime', ctypes.c_ulong),
        ('BatteryFullLifeTime', ctypes.c_ulong),
    ]

def is_charger_connected():
    power_status = SYSTEM_POWER_STATUS()
    ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(power_status))
    return power_status.ACLineStatus == 1

def play_sound(sound_file):
    winsound.PlaySound(sound_file, winsound.SND_FILENAME)

def charger_status_changed(connected):
    if connected:
        threading.Thread(target=play_sound, args=(charging_sound_file,)).start()

def charger_status_thread():
    previous_charger_status = is_charger_connected()

    while True:
        current_charger_status = is_charger_connected()
        
        if current_charger_status != previous_charger_status:
            charger_status_changed(current_charger_status)

        previous_charger_status = current_charger_status

        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=charger_status_thread).start()
