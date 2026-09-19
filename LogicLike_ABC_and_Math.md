# LogicLike: ABC & Math — QA & UX Review with Screenshots

## 1. Overview & Basic Details
- **Game Name:** LogicLike: ABC & Math
- **Package Name:** `com.logicappkids`
- **Target Audience:** Children aged 4–12 (Math, Logic puzzles, ABC & Reasoning)
- **Engine / Architecture:** Modern native app with custom 2D rendering and responsive UI engine.

---

## 2. Evaluation Parameter Checklist

| Parameter | Status | Visual Reference | Key Details |
| :--- | :---: | :---: | :--- |
| **Splash Screen / Launch** | ✅ Pass | ![Welcome Splash](images/logiclike/01_portrait_welcome_splash.png) | High-end video demonstration showcase with "Get Started" and "Sign in" buttons. |
| **Orientation (Portrait)** | 🔄 Hybrid | ![Onboarding](images/logiclike/02_onboarding_next_continue.png) | Onboarding wizard, subscription paywall, and Parent zone operate in **Portrait** mode. |
| **Orientation (Landscape)** | 🔄 Hybrid | ![Landscape Hub](images/logiclike/04_landscape_learning_hub.png) | Main child learning track, courses, and interactive puzzles rotate to **Landscape** mode. |
| **Close Button ('X')** | ✅ Present | ![Paywall Close](images/logiclike/03_paywall_close_x.png) | Top-left 'X' on paywalls, gameplay puzzles, and coral-red top-right 'X' on exit feedback modals. |
| **Parental PIN Gate** | ✅ Pass | ![Parental PIN](images/logiclike/05_parental_pin_gate.png) | Word-to-digit challenge (*"THREE FIVE SIX"*) with numeric keypad and cancel button. |
| **Audio Settings (Music)** | ✅ Available | ![Audio Settings](images/logiclike/06_audio_settings_music.png) | Dedicated **Music** toggle switch in Parent Settings (Global On/Off). |
| **Voice Replay Button** | ✅ Present | ![Voice Speaker](images/logiclike/07_gameplay_close_voice_buttons.png) | Speaker icon in bottom-left re-reads instructions loudly and clearly. |
| **Scores & Star Rewards** | ✅ Present | ![Score & Stars](images/logiclike/08_score_stars_confetti.png) | Immediate numerical reward (`+4 ⭐`) with glowing halos and star counters. |
| **Confetti & Particle FX** | ✅ Present | ![Confetti](images/logiclike/08_score_stars_confetti.png) | Blue, purple, and gold star confetti shower celebrating correct answers. |
| **Exit Flow & Modals** | ✅ Present | ![Exit Modal](images/logiclike/09_exit_close_modal.png) | Tapping top-left Close button triggers friendly exit dialog before navigating to hub. |

---

## 3. Visual Walkthrough & Evidence

### 3.1 Onboarding Splash & Setup Wizard (Portrait)
Starts in Portrait orientation with video previews, mascot progress bar, and "Continue" next buttons.
<p align="center">
  <img src="images/logiclike/01_portrait_welcome_splash.png" width="48%" alt="Welcome Splash" />
  <img src="images/logiclike/02_onboarding_next_continue.png" width="48%" alt="Onboarding Continue" />
</p>

### 3.2 Subscription Modal (Close 'X') & Landscape Child Hub
Paywall features an explicit close 'X' button. Entering the main curriculum automatically switches the screen to Landscape.
<p align="center">
  <img src="images/logiclike/03_paywall_close_x.png" width="48%" alt="Paywall Close X" />
  <img src="images/logiclike/04_landscape_learning_hub.png" width="48%" alt="Landscape Learning Hub" />
</p>

### 3.3 Parental Gate & Audio Music Settings
Parent zone is protected by an English number PIN and contains global background music toggle.
<p align="center">
  <img src="images/logiclike/05_parental_pin_gate.png" width="48%" alt="Parental PIN Gate" />
  <img src="images/logiclike/06_audio_settings_music.png" width="48%" alt="Settings Music Toggle" />
</p>

### 3.4 Interactive Puzzle Gameplay (Voice, Close 'X', Confetti & Score)
Features top-left Close button, bottom-left audio speaker for re-reading instructions, and energetic `+4 ⭐` star confetti on correct answers.
<p align="center">
  <img src="images/logiclike/07_gameplay_close_voice_buttons.png" width="48%" alt="Gameplay UI" />
  <img src="images/logiclike/08_score_stars_confetti.png" width="48%" alt="Score Stars Confetti" />
</p>

### 3.5 Exit Confirmation Modal
Smooth exit flow with rating/feedback overlay and dismiss button.
<p align="center">
  <img src="images/logiclike/09_exit_close_modal.png" width="70%" alt="Exit Modal" />
</p>
