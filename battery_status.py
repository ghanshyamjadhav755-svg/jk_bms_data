import serial
import time

PORT = "/dev/ttyUSB0"
SERIAL_BAUD = 2000000   # Waveshare variable protocol speed

ser = serial.Serial(PORT, SERIAL_BAUD, timeout=1)
time.sleep(2)

# ---------------------------
# Configure 250 kbps Standard Frame
# ---------------------------
def checksum(data):
    return sum(data[2:]) & 0xFF

config = [
    0xAA,0x55,
    0x12,      # Variable protocol
    0x05,      # 250 kbps
    0x01,      # Standard frame
    0x00,0x00,0x00,0x00,  # Filter
    0x00,0x00,0x00,0x00,  # Mask
    0x00,      # Normal mode
    0x00,      # Auto resend
    0x00,0x00,0x00,0x00
]

config.append(checksum(config))
ser.write(bytes(config))

print("JK BMS Monitor Started (250kbps Standard Frame)\n")

# ---------------------------
# Decode Functions
# ---------------------------

def decode_battery(data):
    voltage = int.from_bytes(data[0:2], 'little') * 0.1
    current = int.from_bytes(data[2:4], 'little') * 0.1 - 400
    soc = data[4]
    discharge_time = int.from_bytes(data[6:8], 'little')

    print("----- BATTERY STATUS -----")
    print(f"Voltage        : {voltage:.2f} V")
    print(f"Current        : {current:.2f} A")
    print(f"SOC            : {soc} %")
    print(f"Discharge Time : {discharge_time} h")
    print("--------------------------\n")


def decode_cell(data):
    max_v = int.from_bytes(data[0:2], 'little')
    max_cell = data[2]
    min_v = int.from_bytes(data[3:5], 'little')
    min_cell = data[5]
    delta = max_v - min_v

    print("----- CELL VOLTAGE -----")
    print(f"Max Cell : {max_v} mV (Cell {max_cell})")
    print(f"Min Cell : {min_v} mV (Cell {min_cell})")
    print(f"Delta    : {delta} mV")
    print("------------------------\n")


def decode_alarm(data):
    value = int.from_bytes(data[0:4], 'little')

    alarm_map = {
        "Cell Overvoltage":        (value >> 0) & 0x03,
        "Cell Undervoltage":       (value >> 2) & 0x03,
        "Pack Overvoltage":        (value >> 4) & 0x03,
        "Pack Undervoltage":       (value >> 6) & 0x03,
        "Cell Voltage Difference": (value >> 8) & 0x03,
        "Discharge Overcurrent":   (value >> 10) & 0x03,
        "Charge Overcurrent":      (value >> 12) & 0x03,
        "Over Temperature":        (value >> 14) & 0x03,
        "Under Temperature":       (value >> 16) & 0x03,
        "Temperature Difference":  (value >> 18) & 0x03,
        "Low SOC":                 (value >> 20) & 0x03,
        "Insulation Fault":        (value >> 22) & 0x03,
        "HV Interlock Fault":      (value >> 24) & 0x03,
        "External Comm Fault":     (value >> 26) & 0x03,
        "Internal Comm Fault":     (value >> 28) & 0x03,
    }

    print("***** ALARM STATUS *****")

    active = False
    for name, level in alarm_map.items():
        if level != 0:
            active = True
            print(f"{name} → Level {level}")

    if not active:
        print("No Active Alarms")

    print("************************\n")


# ---------------------------
# Main Receive Loop
# ---------------------------

while True:
    header = ser.read(2)

    if len(header) < 2:
        continue

    if header[0] == 0xAA and (header[1] & 0xC0) == 0xC0:

        length = header[1] & 0x0F
        is_extended = header[1] & 0x20

        if is_extended:
            frame_len = length + 5
        else:
            frame_len = length + 3

        data = ser.read(frame_len)

        if len(data) != frame_len:
            continue

        if data[-1] != 0x55:
            continue

        if not is_extended:
            can_id = data[1] << 8 | data[0]
            payload = data[2:2+length]

            if can_id == 0x02F4:
                decode_battery(payload)

            elif can_id == 0x04F4:
                decode_cell(payload)

            elif can_id == 0x07F4:
                decode_alarm(payload)

        else:
            # Extended frames ignored unless required
            pass
