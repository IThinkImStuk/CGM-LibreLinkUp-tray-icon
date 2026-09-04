# 🩸 CGM LibreLinkUp Tray Icon

> **Keep an eye on your glucose levels without leaving your desktop workflow.**

**CGM LibreLinkUp Tray Icon** is a lightweight system tray app for Windows, macOS, and Linux. It connects to your LibreLinkUp follower account to display real-time blood glucose readings and trend arrows directly in your taskbar.

---

## 💡 Why I Built This

If you wear a CGM, you know how it goes: constantly picking up your phone to glance at your numbers throughout the day. Doing that during meetings, customer calls, or deep work sessions at your computer can be distracting—and sometimes feels awkward when you're supposed to be paying attention.

I built this tool to give myself **peace of mind at work**. By bringing my LibreLinkUp readings straight into my laptop's system tray, I can keep an eye on my glucose levels with a quick glance.

---

## ✨ Features

- 👁️ **At-a-Glance Monitoring:** See your current blood glucose reading directly in your system tray/menu bar.
- 📈 **Trend Arrow Indicators:** Displays whether your glucose is rising, stable, or falling.
- ⏱️ **Custom Sync Intervals:** Polling updates automatically without overwhelming your network or battery.
- 🌍 **Dual Unit Support:** Works with both `mg/dL` and `mmol/L`.

---

## 🛠️ How It Works

1. The app authenticates securely with the **LibreLinkUp API** using your follower credentials.
2. It fetches your latest sensor reading on a background timer.
3. It updates the system tray icon dynamically with your latest reading and trend direction.

> **Note:** You must have an active **LibreLinkUp** account set up as a follower for the target FreeStyle Libre sensor.

---

## ⚠️ Medical Disclaimer

This project is an **unofficial** built tool and is not affiliated with or endorsed by Abbot Laboratories. It is intended strictly for informational/convenience purposes and must not be used for medical decision-making or insulin dosing. Always rely on your official CGM reader or app for medical treatment.

