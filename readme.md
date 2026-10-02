# PS2 Controller to PSP — RP2040 Zero

โปรเจกต์สำหรับใช้ **RP2040 Zero** เชื่อมต่อกับ **PlayStation 2 DualShock 2 Controller** และแปลงการกดปุ่มให้ทำงานเป็นปุ่มของ **PSP**

> **Current Version:** Main Button Mapping
> **Platform:** Raspberry Pi Pico / RP2040 Zero
> **Programming Language:** MicroPython

---

# 🇹🇭 ภาษาไทย

## 📖 เกี่ยวกับโปรเจกต์

โปรเจกต์นี้มีเป้าหมายเพื่อสร้างตัวแปลง

```text
PlayStation 2 DualShock 2
          │
          ▼
     RP2040 Zero
          │
          ▼
       PSP
```

RP2040 Zero ทำหน้าที่อ่านข้อมูลจาก PS2 Controller ผ่านโปรโตคอล PS2 Controller และแปลงปุ่มที่กดเป็นสัญญาณ LOW ไปยังวงจร PSP

โปรเจกต์นี้พัฒนาต่อยอดจากแนวคิด **PS2 to PSP Controller Adapter**

---

## ⚠️ สถานะปัจจุบัน

เวอร์ชันนี้เน้นเฉพาะ **Main Button Mapping**

รองรับ:

* D-Pad
* L1
* R1
* Cross
* Circle
* Triangle
* Square
* Start
* Select

ยัง **ไม่รวม**:

* L2
* R2
* L3
* R3
* Analog Stick
* X9C103S Digital Potentiometer
* PSP Home
* PSP Display
* PSP Power
* Secondary Mapping
* Analog Mode

ฟังก์ชันเหล่านี้จะเพิ่มในเวอร์ชันถัดไป

---

# 🔌 Wiring

## PS2 Controller → RP2040 Zero

| PS2 Pin | Function  |        RP2040 |
| ------: | --------- | ------------: |
|       1 | DAT       |           GP0 |
|       2 | CMD       |           GP1 |
|       3 | GND       |           GND |
|       4 | VCC       |      3V3(OUT) |
|       5 | ATT / SEL |           GP2 |
|       6 | CLK       |           GP3 |
|       7 | IRQ       | Not connected |
|       8 | ACK       | Not connected |

---

# 🎮 PSP Button Mapping

| PS2 Controller | RP2040 GPIO | PSP      |
| -------------- | ----------: | -------- |
| D-Pad UP       |        GP15 | UP       |
| D-Pad DOWN     |        GP13 | DOWN     |
| D-Pad LEFT     |        GP14 | LEFT     |
| D-Pad RIGHT    |        GP16 | RIGHT    |
| L1             |        GP17 | L1       |
| R1             |         GP7 | R1       |
| CROSS (×)      |         GP4 | CROSS    |
| CIRCLE (○)     |         GP5 | CIRCLE   |
| TRIANGLE (△)   |         GP6 | TRIANGLE |
| SQUARE (□)     |         GP8 | SQUARE   |
| START          |         GP9 | START    |
| SELECT         |        GP10 | SELECT   |

---

# 🔧 PSP GPIO

PSP button lines ถูกควบคุมในลักษณะ **Active LOW**

เมื่อกดปุ่ม:

```text
RP2040 GPIO
     │
     └── OUTPUT LOW
```

เมื่อปล่อยปุ่ม:

```text
RP2040 GPIO
     │
     └── HIGH-Z / INPUT
```

วิธีนี้ทำให้ RP2040 จำลองการกดปุ่มบนวงจร PSP โดยไม่ขับ HIGH เข้าหาสายปุ่มโดยตรง

---

# 📁 Project Files

```text
PS2-to-PSP-RP2040/
│
├── main.py
├── ps1controller_library.py
└── README.md
```

### `main.py`

โปรแกรมหลักสำหรับ:

* เชื่อมต่อ PS2 Controller
* อ่านปุ่ม
* Mapping ปุ่ม PS2 → PSP
* ควบคุม PSP GPIO
* Debug ปุ่มผ่าน Serial / Thonny

### `ps1controller_library.py`

Library สำหรับสื่อสารกับ PS2 DualShock Controller

รองรับการอ่าน:

* Digital buttons
* Analog buttons
* Analog stick data
* Controller mode

---

# 💻 Software

ต้องใช้:

* MicroPython
* RP2040 Zero
* Thonny หรือโปรแกรมสำหรับ upload MicroPython
* PS2 DualShock / DualShock 2 Controller

ติดตั้ง MicroPython ลง RP2040 Zero ก่อน จากนั้น copy:

```text
main.py
ps1controller_library.py
```

ลงใน RP2040

---

# ▶️ การใช้งาน

1. ต่อ PS2 Controller เข้ากับ RP2040
2. ต่อ RP2040 เข้ากับ PSP
3. เปิด Thonny
4. Upload:

```text
main.py
ps1controller_library.py
```

5. Reset RP2040
6. โปรแกรมจะพยายามค้นหา PS2 Controller

หากเชื่อมต่อสำเร็จจะแสดง:

```text
==============================
 PS2 -> PSP CONTROLLER
==============================

Connecting PS2 controller...
PS2 controller connected!
Mapping started.
```

จากนั้นสามารถกดปุ่ม PS2 Controller เพื่อควบคุม PSP ได้

---

# 🧪 Debug

เมื่อกดปุ่ม โปรแกรมจะแสดงสถานะผ่าน Serial / Thonny เช่น:

```text
PS2 buttons: 4000
  PRESS: CROSS
```

หรือ:

```text
PS2 buttons: 0808
  PRESS: START
  PRESS: SELECT
```

ใช้สำหรับตรวจสอบว่า PS2 Controller อ่านข้อมูลถูกต้องหรือไม่

---

# 🛠️ Roadmap

### Version 1 — Main Mapping

* [x] PS2 Controller communication
* [x] D-Pad mapping
* [x] L1 / R1
* [x] Cross
* [x] Circle
* [x] Triangle
* [x] Square
* [x] Start
* [x] Select

### Version 2 — Analog Control

* [ ] X9C103S driver
* [ ] Left analog stick
* [ ] Right analog stick
* [ ] Analog center calibration
* [ ] Analog deadzone

### Version 3 — L2 / R2 / L3 / R3

* [ ] L2 mapping
* [ ] R2 mapping
* [ ] L3 mode switch
* [ ] R3 mode switch
* [ ] Secondary mapping
* [ ] PSX-style analog mode

### Version 4 — PSP Functions

* [ ] HOME
* [ ] DISPLAY
* [ ] POWER
* [ ] Volume control
* [ ] PSP status LED

---

# ⚠️ Hardware Warning

โปรเจกต์นี้เชื่อมต่อเข้ากับวงจรภายใน PSP โดยตรง

ควรตรวจสอบแรงดันไฟฟ้าและวงจรของ PSP ก่อนเชื่อมต่อ RP2040

**ห้ามนำ 5V เข้า GPIO ของ RP2040**

RP2040 GPIO ใช้ระดับ Logic **3.3V**

สำหรับ PS2 Controller ในโปรเจกต์นี้ใช้:

```text
PS2 VCC → RP2040 3V3(OUT)
```

และต้องต่อ GND ร่วมกัน

---

# 📜 License

โปรเจกต์นี้จัดทำขึ้นเพื่อการศึกษา การทดลอง และการดัดแปลงฮาร์ดแวร์

หากนำโค้ดไปใช้งานหรือดัดแปลง กรุณาอ้างอิงโปรเจกต์ต้นฉบับ

---

# 🇬🇧 English

## 📖 About

This project uses an **RP2040 Zero** to connect a **PlayStation 2 DualShock / DualShock 2 controller** to a **PSP**.

The RP2040 reads the PS2 controller protocol and converts controller button presses into signals that emulate PSP button presses.

Basic architecture:

```text
PlayStation 2 DualShock 2
          │
          ▼
     RP2040 Zero
          │
          ▼
          PSP
```

The project is based on the concept of a **PS2 to PSP Controller Adapter**.

---

# ⚠️ Current Status

The current version focuses on **Main Button Mapping only**.

Supported:

* D-Pad
* L1
* R1
* Cross
* Circle
* Triangle
* Square
* Start
* Select

Not implemented yet:

* L2
* R2
* L3
* R3
* Analog Stick
* X9C103S Digital Potentiometer
* PSP Home
* PSP Display
* PSP Power
* Secondary Mapping
* Analog Modes

These features are planned for future versions.

---

# 🔌 Wiring

## PS2 Controller → RP2040 Zero

| PS2 Pin | Function  |        RP2040 |
| ------: | --------- | ------------: |
|       1 | DAT       |           GP0 |
|       2 | CMD       |           GP1 |
|       3 | GND       |           GND |
|       4 | VCC       |      3V3(OUT) |
|       5 | ATT / SEL |           GP2 |
|       6 | CLK       |           GP3 |
|       7 | IRQ       | Not connected |
|       8 | ACK       | Not connected |

---

# 🎮 PSP Button Mapping

| PS2 Controller | RP2040 GPIO | PSP      |
| -------------- | ----------: | -------- |
| D-Pad UP       |        GP15 | UP       |
| D-Pad DOWN     |        GP13 | DOWN     |
| D-Pad LEFT     |        GP14 | LEFT     |
| D-Pad RIGHT    |        GP16 | RIGHT    |
| L1             |        GP17 | L1       |
| R1             |         GP7 | R1       |
| CROSS (×)      |         GP4 | CROSS    |
| CIRCLE (○)     |         GP5 | CIRCLE   |
| TRIANGLE (△)   |         GP6 | TRIANGLE |
| SQUARE (□)     |         GP8 | SQUARE   |
| START          |         GP9 | START    |
| SELECT         |        GP10 | SELECT   |

---

# 🔧 PSP GPIO Handling

The PSP button lines are handled as **active LOW** signals.

When a button is pressed:

```text
RP2040 GPIO
     │
     └── OUTPUT LOW
```

When the button is released:

```text
RP2040 GPIO
     │
     └── HIGH-Z / INPUT
```

This allows the RP2040 to emulate the PSP button switch without actively driving the button line HIGH.

---

# 📁 Project Structure

```text
PS2-to-PSP-RP2040/
│
├── main.py
├── ps1controller_library.py
└── README.md
```

### `main.py`

Main application responsible for:

* Connecting to the PS2 controller
* Reading button states
* Mapping PS2 buttons to PSP buttons
* Controlling PSP GPIO
* Serial / Thonny debugging

### `ps1controller_library.py`

MicroPython library for communicating with the PS2 DualShock controller.

It provides access to:

* Digital buttons
* Analog button data
* Analog stick data
* Controller mode

---

# 💻 Requirements

Hardware:

* RP2040 Zero
* PlayStation 2 DualShock / DualShock 2 controller
* PSP
* Appropriate wiring

Software:

* MicroPython
* Thonny or another MicroPython-compatible tool

Upload the following files to the RP2040:

```text
main.py
ps1controller_library.py
```

---

# ▶️ Usage

1. Connect the PS2 controller to the RP2040.
2. Connect the RP2040 to the PSP.
3. Open Thonny.
4. Upload:

```text
main.py
ps1controller_library.py
```

5. Reset the RP2040.
6. The program will attempt to detect the PS2 controller.

When the controller is detected, the serial output should show:

```text
==============================
 PS2 -> PSP CONTROLLER
==============================

Connecting PS2 controller...
PS2 controller connected!
Mapping started.
```

The PS2 controller can then be used to control the PSP.

---

# 🧪 Debugging

Button presses are printed to the Thonny serial console.

Example:

```text
PS2 buttons: 4000
  PRESS: CROSS
```

Another example:

```text
PS2 buttons: 0808
  PRESS: START
  PRESS: SELECT
```

This makes it easier to verify the PS2 controller communication and button mapping before connecting the complete PSP system.

---

# 🛠️ Roadmap

## Version 1 — Main Mapping

* [x] PS2 controller communication
* [x] D-Pad mapping
* [x] L1 / R1
* [x] Cross
* [x] Circle
* [x] Triangle
* [x] Square
* [x] Start
* [x] Select

## Version 2 — Analog Control

* [ ] X9C103S driver
* [ ] Left analog stick
* [ ] Right analog stick
* [ ] Analog center calibration
* [ ] Analog deadzone

## Version 3 — L2 / R2 / L3 / R3

* [ ] L2 mapping
* [ ] R2 mapping
* [ ] L3 mode switch
* [ ] R3 mode switch
* [ ] Secondary mapping
* [ ] PSX-style analog mode

## Version 4 — PSP Functions

* [ ] HOME
* [ ] DISPLAY
* [ ] POWER
* [ ] Volume control
* [ ] PSP status LED

---

# ⚠️ Hardware Warning

This project connects directly to the internal PSP button circuitry.

Always verify the PSP circuit and voltage levels before connecting the RP2040.

**Do not apply 5V to RP2040 GPIO pins.**

RP2040 GPIO uses **3.3V logic**.

For the PS2 controller:

```text
PS2 VCC → RP2040 3V3(OUT)
PS2 GND → RP2040 GND
```

A common ground is required.

---

# 📜 License

This project is intended for educational, experimental, and hardware modification purposes.

If you use or modify this project, please give appropriate credit to the original project.

---

## Project Status

🚧 **Work in Progress**

The project is being developed step-by-step, starting with reliable PS2-to-PSP main button mapping before implementing analog control and additional PSP functions.
