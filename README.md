````markdown
# 😃(Emoji Reactor)

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8.0-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange?style=for-the-badge&logo=google)

> 🎥 A real-time reaction system that turns your face and hand gestures into on-screen memes.

---

## 🔥 What is this?

This project is an **interactive computer vision tool** that reacts instantly to your expressions and gestures by spawning images (memes, emojis, reactions) on your screen.

Perfect for:
- 🎮 Streams (OBS / Twitch / YouTube)
- 🎤 Presentations
- 😂 Content creation (Reels, Shorts, TikTok)
- 🧪 Just having fun with AI

---

## ⚡ Demo

> *(Add your viral video link here — this is VERY important)*

---

## ✨ Features

- 👍 **Gesture Detection**  
  Detects gestures like **Thumbs Up** and **Pointing (You)** using MediaPipe Hands.

- 😲 **Facial Expression Recognition**  
  Detects emotions like **Happy** and **Scared** using facial geometry.

- 🚀 **Zero-Lag Popups**  
  Images are preloaded in RAM for instant display.

- 🪟 **Smart Window System**  
  Multiple popups displayed in an organized grid with auto-close cooldown.

- 🎯 **Highly Customizable**  
  Just drop your own images into the assets folder.

---

## 🧠 How does the Math Logic work?

The system does **NOT rely only on AI black-box predictions**.

Instead, it uses **real-time geometry calculations** based on facial landmarks.

Example:
- First → calculates mouth **vertical opening (hypotenuse)**
- Then → calculates **horizontal width**
- Then → applies custom thresholds

This avoids confusion between:
- 😄 Big Smile  
- 😱 Scared Face  

Result: **more accurate and controllable detection**

---

## 🛠️ Tech Stack

- **Python 3.10**
- **OpenCV**
- **MediaPipe**
- **NumPy**
- **Pillow**

---

## ⚠️ Requirements (IMPORTANT)

MediaPipe on Windows can break with newer Python versions.

👉 You MUST use **Python 3.10**

Check your version:
```bash
py --list
````

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/AoyaguiLabs/emoji-reactor.git
cd emoji-reactor
```

### 2. Create virtual environment (Python 3.10)

```powershell
py -3.10 -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

---

## 📁 Assets Setup

Create a folder called `assets`:

```
assets/
  ├── thumbsup_1.jpg
  ├── happy_1.jpg
  ├── scaryface_1.jpg
  └── you_1.jpg
```

💡 Tip:
You can add ANY images you want — memes, emojis, your face, etc.

---

## ▶️ Run the project

```bash
python main.py
```

---

## 🎮 How to Use

* 👍 Show a **thumbs up** → image appears
* 👉 Point to the camera → "YOU" reaction
* 😄 Smile → happy reaction
* 😱 Open mouth wide → scared reaction

---

## 🚀 Why this project?

This was created after a **viral video experiment**, where people loved the idea of:

👉 interacting with AI in real-time
👉 turning reactions into visual entertainment

Now it's open for anyone to use and build on.

---

## 💡 Ideas to expand

* OBS integration (browser source overlay)
* Sound effects on trigger
* Custom gesture training
* Stream alerts system
* Multiplayer / chat interaction

---

## 👤 Author

**Guilherme Aoyagui**
* 🚀 Focus: Computer Vision • Automation • AI Systems

---

## ⭐ Support

If you liked this project:

* ⭐ Star the repo
* 🍴 Fork it
* 🎥 Share your version online

---

## ⚠️ Disclaimer

This project is for **entertainment and educational purposes only**.

```
```
