# 🤝 Contributing to JoyBox

Thank you for wanting to support **JoyBox** — an open-source handheld console project designed to bring joy to children who might not receive much at Christmas or during difficult times.

There are **no expectations of perfection** here.
If you want to help, you're welcome here. 💛

---

# 🌟 Ways You Can Contribute

| Skill / Interest    | How to Help                                            |
| ------------------- | ------------------------------------------------------ |
| Python / Pygame     | Build or improve games, fix bugs, add menus or UI      |
| Writers             | Game dialogue, quests, educational prompts, tutorials  |
| Pixel Artists       | Characters, tilesets, fonts, UI elements, spritesheets |
| Hardware Makers     | Case design, GPIO button layouts, wiring guides        |
| Testers             | Try on Raspberry Pi devices and report performance     |
| Educators / Parents | Suggest learning mechanics and accessibility ideas     |
| Anyone              | Ideas, feedback, encouragement, documentation          |

You don’t need to be an expert. If you care, you qualify.

---

# 🛠️ Getting Started (Development Setup)

```sh
git clone https://github.com/AJECooper/joybox-console.git
cd joybox-console
python -m pip install -r requirements.txt
python src/joybox/main.py
```

If the launcher window appears, you're set. 🎉

---

# 🗂️ Project Structure (Quick Overview)

```
joybox-console/
  src/
    joybox/
      engine/          # Framework (GameApp, Scene system)
      games/           # Each game lives here in its own folder
      assets_shared/   # Shared UI, fonts, SFX
      main.py          # Launcher entry point
  docs/
  tools/
  release/
```

---

# 🎮 Adding a New Game (Template)

Create a new folder under:

```
src/joybox/games/<your_game_name>/
```

Inside it, include at minimum:

* `game.py` → entry class (inherits from `Scene`)
* `data/` → JSON files, text, level definitions
* `assets/` → sprites, sounds, or placeholders

Register the game in the launcher (instructions will come as the system evolves).

If you're unsure how to start, open an Issue and we’ll pair you with guidance.

---

# 🧩 Coding Guidelines

* Keep code readable, not clever.
* Small commits > big “mystery box” changes.
* Comment logic that's not obvious.
* If a change affects hardware, **document it**.
* Avoid breaking existing games — backwards compatibility matters.

> JoyBox is meant to last and be approachable for newcomers.

---

# ⚙️ Hardware Profiles (Performance Guidance)

Not all games will run on all devices. This is okay.

**Suggested compatibility tags:**

| Tag              | Hardware                      | Game Scale                      |
| ---------------- | ----------------------------- | ------------------------------- |
| `pi_lite`        | Zero / Zero 2                 | Small puzzles or learning games |
| `pi_standard`    | Pi 3B+ (development baseline) | 2D RPGs and larger projects     |
| `pi_performance` | Pi 4+                         | Bigger worlds / heavier effects |

Add these in your PR so children don’t end up with games that run poorly on their device.

---

# 📝 Submitting Pull Requests

1. Fork the repo
2. Create a branch:

   ```sh
   git checkout -b feature/my-feature-name
   ```
3. Commit changes clearly:

   ```sh
   git commit -m "Add new mini-game: Forest Friends"
   ```
4. Push and open a PR
5. Add:

   * What you changed
   * Any hardware profile requirements
   * Any known limitations

We’re friendly — nobody will judge mistakes.

---

# 🚫 What This Project Is *Not*

* Not commercial
* Not pay-to-play
* Not ad-based
* Not here to make money off kids

If you want to monetise your game elsewhere, that’s fine — but code contributed *here* must stay open and free in the spirit of JoyBox.

---

# 💛 Final Message

Thank you for being here.
Thank you for caring.
Thank you for helping build something that might make a child feel like they matter.

> If JoyBox brings joy to even one child, this entire project is worth it.
