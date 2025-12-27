# 🎮 JoyBox – Open Source Handheld Console

**JoyBox** is an open-source, low-cost handheld console project designed to bring joy to children who might not receive much at Christmas or during difficult times.

This is a passion project. It isn't about profit – it's about kindness, creativity, and giving children something that says:

> **"You matter. Someone made this for you."**

---

## 🌟 Project Goals

* Build a portable handheld console powered by Raspberry Pi
* Keep hardware costs as low as reasonably possible
* Create a library of small, fun, educational, and adventure games
* Make JoyBox giftable to families and children who may be struggling
* Encourage community contributions: games, tools, art, sound, testing

---

## 💻 Tech Stack

| Area        | Technology                               |
| ----------- | ---------------------------------------- |
| Programming | Python, Pygame                           |
| Hardware    | Raspberry Pi (Zero/Zero 2, Pi 3B+, Pi 4) |
| Display     | SPI TFT Screens / HDMI for dev           |
| Controls    | GPIO buttons or USB controller           |
| Case        | 3D printed or cardboard prototype        |

### Minimum Target Hardware

The current development baseline is:

```
Raspberry Pi 3B+
Python 3.12.x
Pygame 2.5.x
```

We aim to support lower and higher tiers as the project grows.

---

## 📂 Project Structure (Early Stage)

```
joybox-console/
  src/
    joybox/
      engine/          # core class: GameApp, Scene system
      games/           # each game lives in its own folder
      assets_shared/   # shared fonts, sounds, sprites
      main.py          # launcher entry point
  docs/                # hardware notes, setup guides
  tools/               # build tools and utility scripts
  release/             # packaged versions for devices
  requirements.txt
```

---

## 🚀 Running the Project (Development)

```sh
git clone https://github.com/AJECooper/joybox-console.git
cd joybox-console
python -m pip install -r requirements.txt
python src/joybox/main.py
```

You should see a window appear that says:

**🎮 JoyBox Started!**

---

## 🤝 Contributing

JoyBox is open to contributions of all sizes.
We welcome:

* Python / Pygame developers
* Writers and quest designers
* Pixel artists and 2D animators
* Hardware tinkerers and case designers
* Raspberry Pi testers (Zero, 3B+, 4)
* Educators or parents with ideas for learning games

Check out [`CONTRIBUTING.md`](CONTRIBUTING.md) to learn more.

---

## 🏗️ Hardware Profiles (Planning)

As the project grows, games will declare compatibility like so:

| Profile          | Examples      | Target Games                            |
| ---------------- | ------------- | --------------------------------------- |
| `pi_lite`        | Zero / Zero 2 | Simple 2D, educational                  |
| `pi_standard`    | Pi 3B+        | RPGs, scrolling maps                    |
| `pi_performance` | Pi 4          | Larger maps, effects, bigger adventures |

This helps prevent installing games that won't run well on certain models.

---

## ❤️ Why This Matters

Some children won’t get anything for Christmas.
Some families are struggling.

If JoyBox puts a smile on even *one* child’s face, it’s already a success.

**This project exists to remind them:**

* They are seen.
* They are valued.
* They deserve joy, just like anyone else.

---

## 📩 Get Involved

* Report issues
* Suggest improvements
* Submit a game or prototype
* Ask questions
* Share ideas

> You don’t need permission to care.
> You can start helping today.

---

📜 License: CC BY-NC 4.0 (Free to use, modify, and share – NOT for commercial sale)

