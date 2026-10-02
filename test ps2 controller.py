import time
from machine import Pin
# นำเข้าคลาสและค่าคงที่ทั้งหมดจาก ps2x.py
from ps2x import *

# -------------------------------------------------------------------
# 1. กำหนดขา Pin (สามารถเปลี่ยนเลข Pin ตามบอร์ดที่ใช้งาน เช่น ESP32)
# -------------------------------------------------------------------
PS2_CLK = 0
PS2_CMD = 2
PS2_ATT = 1
PS2_DAT = 3

# สร้าง Instance ของ PS2X
ps2 = PS2X(clk=PS2_CLK, cmd=PS2_CMD, att=PS2_ATT, dat=PS2_DAT)

# -------------------------------------------------------------------
# 2. เริ่มต้นเชื่อมต่อจอยแบบ Full Option
# -------------------------------------------------------------------
print("กำลังค้นหาและเชื่อมต่อจอย PS2...")

# pressures=True  -> เปิดใช้งานอ่านน้ำหนักแรงกดปุ่ม (0-255)
# rumble=True     -> เปิดใช้งานสั่น
# analog_mode=False -> ปิดไฟสีแดงตอนเริ่มต้น (กดเปิดปุ่ม Analog เองได้)
# lock_analog=False -> ปลดล็อคให้ผู้ใช้กดปุ่ม ANALOG สลับโหมดเองได้
error = 1
while error != 0:
    error = ps2.config_gamepad(pressures=True, rumble=True, analog_mode=False, lock_analog=False)
    if error == 0:
        print("\n==================================================")
        print(" [SUCCESS] เชื่อมต่อจอย PS2 สำเร็จ! (Full Option)")
        print("==================================================")
        print(" คำแนะนำในการทดสอบ:")
        print(" 1. หากต้องการทดสอบ Analog Stick ให้กดปุ่ม 'ANALOG' ที่จอยเพื่อเปิดไฟสีแดง")
        print(" 2. กดปุ่ม CROSS (X) ค้างไว้ -> ทดสอบมอเตอร์สั่นตัวเล็ก (Motor 1)")
        print(" 3. กดปุ่ม R2 ค้างไว้ -> ทดสอบมอเตอร์สั่นตัวใหญ่ (Motor 2) ตามแรงกด")
        print(" 4. ลองกดปุ่มต่างๆ เพื่อดู Event Pressed / Released")
        print("==================================================\n")
    else:
        print("[ERROR] ไม่พบการตอบรับจากจอย... กำลังลองใหม่ใน 1 วินาที")
        time.sleep(1)

# ตัวแปรควบคุมเวลาในการพิมพ์ค่าอนาล็อกลง Serial (กันจอเลื่อนเร็วเกินไป)
last_print_time = time.ticks_ms()

# -------------------------------------------------------------------
# 3. ลูปหลักสำหรับทดสอบฟังก์ชันทั้งหมด
# -------------------------------------------------------------------
while True:
    # --- กำหนดเงื่อนไขการสั่น ---
    vibrate_small = False
    vibrate_large = 0

    # ถ้ากดปุ่ม CROSS (X) ให้เปิดมอเตอร์สั่นตัวเล็ก
    if ps2.button(PSB_CROSS):
        vibrate_small = True

    # ถ้ากดปุ่ม R2 ให้นำค่าน้ำหนักแรงกดปุ่ม R2 (0-255) ไปปรับความเร็วการสั่นของมอเตอร์ตัวใหญ่
    if ps2.button(PSB_R2):
        vibrate_large = ps2.analog(PSAB_R2)
        if vibrate_large == 0:  # หากไม่ได้อยู่ในโหมดอ่านแรงกด ให้สั่นเต็มแรงแทน
            vibrate_large = 255

    # อ่านค่าสถานะล่าสุดของจอย พร้อมส่งคำสั่งสั่น (Rumble) ไปยังจอย
    ps2.read_gamepad(motor1=vibrate_small, motor2=vibrate_large)

    # ----------------------------------------------------
    # ตรวจสอบ Event ปุ่มกด (เพิ่งกด / เพิ่งปล่อย)
    # ----------------------------------------------------
    buttons = [
        (PSB_SELECT, "SELECT"), (PSB_START, "START"),
        (PSB_L3, "L3 (กดก้านซ้าย)"), (PSB_R3, "R3 (กดก้านขวา)"),
        (PSB_L1, "L1"), (PSB_R1, "R1"),
        (PSB_L2, "L2"), (PSB_R2, "R2"),
        (PSB_PAD_UP, "D-PAD UP"), (PSB_PAD_DOWN, "D-PAD DOWN"),
        (PSB_PAD_LEFT, "D-PAD LEFT"), (PSB_PAD_RIGHT, "D-PAD RIGHT"),
        (PSB_TRIANGLE, "TRIANGLE (▲)"), (PSB_CIRCLE, "CIRCLE (●)"),
        (PSB_CROSS, "CROSS (X)"), (PSB_SQUARE, "SQUARE (■)")
    ]

    for btn_mask, btn_name in buttons:
        if ps2.button_pressed(btn_mask):
            print(f"\n[EVENT] >>> กดปุ่ม: {btn_name}")
        if ps2.button_released(btn_mask):
            print(f"\n[EVENT] <<< ปล่อยปุ่ม: {btn_name}")

    # ----------------------------------------------------
    # แสดงผลค่าแกนอนาล็อกและแรงกดปุ่ม (อัปเดตทุกๆ 150 ms)
    # ----------------------------------------------------
    if time.ticks_diff(time.ticks_ms(), last_print_time) > 150:
        last_print_time = time.ticks_ms()

        # อ่านค่าก้านอนาล็อก (ค่าเริ่มต้น ~127-128, ขอบเขต 0-255)
        lx = ps2.analog(PSS_LX)
        ly = ps2.analog(PSS_LY)
        rx = ps2.analog(PSS_RX)
        ry = ps2.analog(PSS_RY)

        # อ่านค่าน้ำหนักแรงกดของปุ่มรูปทรง (0 = ไม่กด, 255 = กดสุด)
        p_tri = ps2.analog(PSAB_TRIANGLE)
        p_cir = ps2.analog(PSAB_CIRCLE)
        p_cro = ps2.analog(PSAB_CROSS)
        p_squ = ps2.analog(PSAB_SQUARE)

        # พิมพ์ค่าแบบเรียงบรรทัดทับบรรทัดเดิมด้วย \r
        print(f"Sticks [L: {lx:3d},{ly:3d} | R: {rx:3d},{ry:3d}] | Pressures [▲:{p_tri:3d} ●:{p_cir:3d} X:{p_cro:3d} ■:{p_squ:3d}]", end="\r")

    time.sleep_ms(20)