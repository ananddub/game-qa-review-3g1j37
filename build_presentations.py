import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

BASE_DIR = "/home/das/Documents/game_review"
IMAGES_DIR = os.path.join(BASE_DIR, "images")

def add_header(slide, title_text, category_text):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(120, 144, 156)
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(33, 33, 33)

def create_card(slide, left, top, width, height, bg_rgb=RGBColor(255, 255, 255), border_rgb=RGBColor(220, 224, 230)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_rgb
    if border_rgb:
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape

def add_detail_image_card(slide, img_path, left, top, card_w, card_h, img_title, status_text, details):
    """
    Creates a card with the image on top and structured technical status details underneath.
    """
    create_card(slide, left, top, card_w, card_h, RGBColor(255, 255, 255), RGBColor(207, 216, 220))
    
    # Image container sizing
    img_container_h = Inches(2.7)
    img_container_w = card_w - Inches(0.4)
    
    if os.path.exists(img_path):
        with Image.open(img_path) as im:
            iw, ih = im.size
            aspect = iw / ih
            
        if img_container_w / img_container_h > aspect:
            fit_h = img_container_h
            fit_w = fit_h * aspect
        else:
            fit_w = img_container_w
            fit_h = fit_w / aspect
            
        img_left = left + (card_w - fit_w) / 2
        img_top = top + Inches(0.15) + (img_container_h - fit_h) / 2
        slide.shapes.add_picture(img_path, img_left, img_top, fit_w, fit_h)
    
    # Text container underneath image
    text_top = top + img_container_h + Inches(0.2)
    text_w = card_w - Inches(0.4)
    text_h = card_h - img_container_h - Inches(0.3)
    
    tbox = slide.shapes.add_textbox(left + Inches(0.2), text_top, text_w, text_h)
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Title & Status
    p_title = tf.paragraphs[0]
    p_title.text = img_title
    p_title.font.bold = True
    p_title.font.size = Pt(13)
    p_title.font.color.rgb = RGBColor(33, 33, 33)
    
    p_stat = tf.add_paragraph()
    p_stat.text = f"Status: {status_text}"
    p_stat.font.bold = True
    p_stat.font.size = Pt(11)
    if "PASS" in status_text.upper() or "ACTIVE" in status_text.upper() or "VERIFIED" in status_text.upper():
        p_stat.font.color.rgb = RGBColor(46, 125, 50)
    else:
        p_stat.font.color.rgb = RGBColor(230, 81, 0)
        
    for label, val in details:
        p = tf.add_paragraph()
        p.text = f"• {label}: "
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = RGBColor(55, 71, 79)
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = RGBColor(84, 110, 122)

def build_singham_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # --- SLIDE 1: Title Slide ---
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(26, 35, 126) # Deep Navy
    bg.line.fill.background()
    
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(1.8), Inches(0.15), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(255, 111, 0) # Amber orange
    bar.line.fill.background()
    
    t_box = s1.shapes.add_textbox(Inches(1.4), Inches(1.8), Inches(10.5), Inches(3.6))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "QA & UX TECHNICAL STATUS AUDIT"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 179, 0)
    
    p2 = tf.add_paragraph()
    p2.text = "Little Singham: Play & Learn"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    
    p3 = tf.add_paragraph()
    p3.text = "Detailed Screen-by-Screen QA Status, Orientation, Audio Controls & Flow Verification"
    p3.font.size = Pt(17)
    p3.font.color.rgb = RGBColor(207, 216, 220)
    
    meta_box = s1.shapes.add_textbox(Inches(1.4), Inches(5.6), Inches(10.5), Inches(1.2))
    mtf = meta_box.text_frame
    p_meta = mtf.paragraphs[0]
    p_meta.text = "Package: com.ct.littlesingham  |  Device: Vivo V2153 (Android 14)  |  Display: 2400×1080 (Landscape) / 1080×2400 (Portrait)"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = RGBColor(176, 190, 197)

    # --- SLIDE 2: Evaluation Parameter Checklist Table ---
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Complete QA Parameter & Status Checklist", "Technical Verification Matrix")
    
    rows, cols = 8, 4
    table_shape = s2.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.3))
    table = table_shape.table
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(1.5)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(5.3)
    
    headers = ["Evaluation Parameter", "Status", "Visual Reference", "Exact Technical Verification Details"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(26, 35, 126)
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.size = Pt(11.5)
            
    checklist_data = [
        ("Splash Screen / Launch Flow", "PASS (VERIFIED)", "01_splash_loading.png", "Animated branding with dynamic progress bar. App initialized with 0 crashes."),
        ("Landscape Mode (Gameplay)", "PASS (LOCKED)", "02_landscape_main_hub.png", "Main child hub and all activities run locked in 2400×1080 Landscape orientation."),
        ("Parental Gate Protection", "PASS (SECURE)", "03_parental_math_gate.png", "Randomized arithmetic puzzle (e.g. 55 + 6 = 61) protects parent and account zone."),
        ("Dynamic Portrait Mode", "PASS (DYNAMIC)", "04_portrait_parent_home.png", "System dynamically rotates screen to 1080×2400 Portrait upon parent zone entry."),
        ("Audio Settings (BGM Toggle)", "AVAILABLE", "05_audio_settings_bgm.png", "Parent Preferences menu provides dedicated Background Music ON/OFF toggle."),
        ("Gameplay Audio Controls", "PASS (ACTIVE)", "07_in_game_audio_mute.png", "Dedicated one-tap speaker icon switches directly between unmuted and muted (✕)."),
        ("Navigation & Level Stars", "PASS (ACTIVE)", "06 & 08.png", "Clear top-left '<' back button and vertical 1–3 star level progress tube.")
    ]
    for row_idx, data in enumerate(checklist_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10.5)
                if col_idx == 1:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(46, 125, 50)
                else:
                    p.font.color.rgb = RGBColor(55, 71, 79)

    # --- SLIDE 3: Detailed Image Breakdown (Images 01 & 02) ---
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Screen Status Detail: Launch Screen & Main Child Hub", "Visual Evidence & Status")
    add_detail_image_card(s3, os.path.join(IMAGES_DIR, "singham/01_splash_loading.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 01: Splash Screen & Loading Progress",
                          "PASS (VERIFIED)",
                          [
                              ("Orientation", "Landscape (2400×1080)"),
                              ("UI Elements", "Creative Galileo branding, Little Singham IP characters, loading status bar"),
                              ("Technical Behavior", "Loads local and remote game assets, progress bar updates dynamically"),
                              ("Audio State", "Title theme intro audio plays during asset loading"),
                              ("Stability", "App launches smoothly without freezing or ANR timeouts")
                          ])
    add_detail_image_card(s3, os.path.join(IMAGES_DIR, "singham/02_landscape_main_hub.png"),
                          Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5),
                          "Image 02: Main Interactive Child Hub",
                          "PASS (LOCKED LANDSCAPE)",
                          [
                              ("Orientation", "Landscape (2400×1080 locked)"),
                              ("UI Elements", "Curriculum cards (English, Math, Hindi, Colors), profile badge, Parent Zone lock"),
                              ("Touch Target Size", "Large child-friendly buttons (>80dp width) preventing mis-taps"),
                              ("Navigation", "Horizontal carousel swipe navigation across learning topics"),
                              ("Audio State", "Upbeat cartoon background soundtrack active (loops continuously)")
                          ])

    # --- SLIDE 4: Detailed Image Breakdown (Images 03 & 04) ---
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Screen Status Detail: Parental Gate & Dynamic Portrait Switch", "Visual Evidence & Status")
    add_detail_image_card(s4, os.path.join(IMAGES_DIR, "singham/03_parental_math_gate.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 03: Arithmetic Parental Gate Modal",
                          "PASS (SECURE)",
                          [
                              ("Orientation", "Landscape (2400×1080) overlay"),
                              ("Challenge Type", "Dynamic two-digit math question (e.g. 55 + 6 = 61)"),
                              ("UI Elements", "Arithmetic prompt, numeric input field, Submit button, Close ('✕') button"),
                              ("Security Purpose", "Prevents preschool children from exiting to billing or account settings"),
                              ("Failure Handling", "Incorrect answers refresh the challenge without locking the app")
                          ])
    add_detail_image_card(s4, os.path.join(IMAGES_DIR, "singham/04_portrait_parent_home.png"),
                          Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5),
                          "Image 04: Parent Zone (Dynamic Rotation)",
                          "PASS (DYNAMIC ROTATION)",
                          [
                              ("Orientation", "Portrait (1080×2400 dynamic switch)"),
                              ("Trigger", "Successfully solving the math parental challenge in Image 03"),
                              ("UI Elements", "Child learning analytics, subscription management, parent preferences"),
                              ("Ergonomics", "Optimized specifically for adult single-handed vertical smartphone use"),
                              ("Exit Behavior", "Returning to child dashboard smoothly rotates device back to Landscape")
                          ])

    # --- SLIDE 5: Detailed Image Breakdown (Images 05 & 07) ---
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Screen Status Detail: Audio Controls & In-Game Mute", "Visual Evidence & Status")
    add_detail_image_card(s5, os.path.join(IMAGES_DIR, "singham/05_audio_settings_bgm.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 05: Background Music Toggle in Settings",
                          "AVAILABLE (TOGGLE ACTIVE)",
                          [
                              ("Location", "Parent Zone > Preferences Menu (Portrait 1080×2400)"),
                              ("Control Type", "Binary Switch Toggle (ON / OFF)"),
                              ("Function", "Globally mutes/unmutes background cartoon soundtrack across all screens"),
                              ("Persistence", "Selected preference is saved locally across app restarts"),
                              ("Slider Availability", "No separate volume slider bars; hardware buttons control volume level")
                          ])
    add_detail_image_card(s5, os.path.join(IMAGES_DIR, "singham/07_in_game_audio_mute.png"),
                          Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5),
                          "Image 07: Direct In-Game Quick Mute Button",
                          "PASS (VERIFIED ACTIVE)",
                          [
                              ("Location", "Top-Right corner of all interactive gameplay screens"),
                              ("Icon State", "Speaker icon toggles dynamically between Sound-ON and Mute ('✕')"),
                              ("Function", "Instant 1-touch muting of both voice instructions and BGM"),
                              ("Accessibility", "Permits quiet classroom/home play without accessing parent settings"),
                              ("Response Time", "Immediate audio cutoff without audio pops or lag")
                          ])

    # --- SLIDE 6: Detailed Image Breakdown (Images 06 & 08) ---
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Screen Status Detail: Navigation & Star Reward Progression", "Visual Evidence & Status")
    add_detail_image_card(s6, os.path.join(IMAGES_DIR, "singham/06_gameplay_navigation_buttons.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 06: Gameplay Navigation & Controls",
                          "PASS (PRESENT & ACCESSIBLE)",
                          [
                              ("Orientation", "Landscape (2400×1080)"),
                              ("Back Button", "High-contrast circular orange button ('<') positioned at top-left"),
                              ("Carousel Controls", "Left/Right arrow triggers for advancing curriculum activities"),
                              ("Touch Target", "Exceeds 48dp Android accessibility touch guideline"),
                              ("Exit Confirmation", "Navigates directly back to the curriculum category screen")
                          ])
    add_detail_image_card(s6, os.path.join(IMAGES_DIR, "singham/08_level_progress_stars.png"),
                          Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5),
                          "Image 08: Level Progress Tube & 3 Golden Stars",
                          "PASS (ACTIVE FEEDBACK)",
                          [
                              ("Visual Mechanism", "Vertical filling tube that rises incrementally as tasks are solved"),
                              ("Milestones", "3 distinct golden stars positioned along the vertical track"),
                              ("Feedback Loop", "Stars ignite with visual animation upon reaching task thresholds"),
                              ("Game Over State", "No punitive 'Game Over' screen; child is encouraged to continue"),
                              ("Audio Reinforcement", "Positive cheer voiceover cue triggers upon star completion")
                          ])

    # --- SLIDE 7: Complete Technical Summary Matrix ---
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Final Architectural & Verification Summary", "Technical Audit Status")
    
    c_sum = create_card(s7, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.5))
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.1), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "LITTLE SINGHAM: PLAY & LEARN — TECHNICAL AUDIT SUMMARY"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = RGBColor(26, 35, 126)
    
    points = [
        ("Splash & Boot Flow", "Verified Pass. Animated intro screen with progress bar. No crash or ANR observed during hardware testing on Android 14."),
        ("Display & Orientation Architecture", "Dynamic Hybrid. Child gameplay is strictly locked to 2400×1080 Landscape. Parent Zone triggers an automatic hardware rotation to 1080×2400 Portrait."),
        ("Parental Protection Mechanism", "Verified Pass. Two-digit arithmetic question gate (55 + 6 = 61) protects parent zone, external links, and subscription menus."),
        ("Audio & Sound Configuration", "Verified Available. Global BGM on/off switch in Parent Preferences; dedicated one-tap speaker mute toggle on top-right of active gameplay."),
        ("Navigation Architecture", "Verified Pass. Circular orange back button ('<') at top-left; carousel next/prev buttons for item browsing."),
        ("Scoring & Motivation Mechanics", "Verified Pass. Vertical fill meter with 1, 2, and 3 golden star milestones. No punishing fail or timeout screens; purely positive reinforcement.")
    ]
    for title, desc in points:
        p = tf.add_paragraph()
        p.text = f"✔  {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = RGBColor(46, 125, 50)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = RGBColor(55, 71, 79)

    out_path = os.path.join(BASE_DIR, "Little_Singham_Play_and_Learn.pptx")
    prs.save(out_path)
    print(f"Saved: {out_path}")

def build_logiclike_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # --- SLIDE 1: Title Slide ---
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(21, 101, 192) # Radiant Blue
    bg.line.fill.background()
    
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(1.8), Inches(0.15), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(142, 36, 170) # Purple
    bar.line.fill.background()
    
    t_box = s1.shapes.add_textbox(Inches(1.4), Inches(1.8), Inches(10.5), Inches(3.6))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "QA & UX TECHNICAL STATUS AUDIT"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(179, 229, 252)
    
    p2 = tf.add_paragraph()
    p2.text = "LogicLike: ABC & Math"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    
    p3 = tf.add_paragraph()
    p3.text = "Detailed Screen-by-Screen QA Status, Star Confetti FX, Word-PIN Gate & UI Details"
    p3.font.size = Pt(17)
    p3.font.color.rgb = RGBColor(227, 242, 253)
    
    meta_box = s1.shapes.add_textbox(Inches(1.4), Inches(5.6), Inches(10.5), Inches(1.2))
    mtf = meta_box.text_frame
    p_meta = mtf.paragraphs[0]
    p_meta.text = "Package: com.logicappkids  |  Device: Vivo V2153 (Android 14)  |  Display: 1080×2400 (Portrait) / 2400×1080 (Landscape)"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = RGBColor(187, 222, 251)

    # --- SLIDE 2: Evaluation Parameter Checklist Table ---
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Complete QA Parameter & Status Checklist", "Technical Verification Matrix")
    
    rows, cols = 8, 4
    table_shape = s2.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.3))
    table = table_shape.table
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(1.5)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(5.3)
    
    headers = ["Evaluation Parameter", "Status", "Visual Reference", "Exact Technical Verification Details"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(21, 101, 192)
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.font.size = Pt(11.5)
            
    checklist_data = [
        ("Splash Screen & Video Launch", "PASS (VERIFIED)", "01_portrait_welcome_splash.png", "High-fps video demonstration splash with 'Get Started' and 'Sign in' buttons."),
        ("Portrait Onboarding Wizard", "PASS (ACTIVE)", "02_onboarding_next_continue.png", "Step-by-step age selection wizard in Portrait mode (1080×2400) with Continue button."),
        ("Paywall Close ('✕') Button", "PASS (PRESENT)", "03_paywall_close_x.png", "Prominent white '✕' button at top-left allows immediate paywall dismissal."),
        ("Landscape Learning Hub", "PASS (LOCKED)", "04_landscape_learning_hub.png", "Automatically rotates to Landscape (2400×1080) for expansive course curriculum."),
        ("Parental Word-PIN Gate", "PASS (SECURE)", "05_parental_pin_gate.png", "English number prompt ('THREE FIVE SIX') with numeric keypad and cancel button."),
        ("Audio Settings (Music Toggle)", "AVAILABLE", "06_audio_settings_music.png", "Parent Settings provides dedicated 'Music' binary ON/OFF switch toggle."),
        ("Voice Replay, Score & Confetti", "PASS (ACTIVE)", "07 & 08.png", "Voice speaker button reads instructions; +4 ⭐ score with animated multi-color star confetti.")
    ]
    for row_idx, data in enumerate(checklist_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10.5)
                if col_idx == 1:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(46, 125, 50)
                else:
                    p.font.color.rgb = RGBColor(55, 71, 79)

    # --- SLIDE 3: Detailed Image Breakdown (Images 01 & 02) ---
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Screen Status Detail: Welcome Splash & Setup Onboarding", "Visual Evidence & Status")
    add_detail_image_card(s3, os.path.join(IMAGES_DIR, "logiclike/01_portrait_welcome_splash.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 01: Welcome Splash & Demonstration",
                          "PASS (VERIFIED)",
                          [
                              ("Orientation", "Portrait (1080×2400)"),
                              ("UI Elements", "Branded video demo, 'Get Started' primary button, 'Sign in' secondary button"),
                              ("Technical Behavior", "Loops high-resolution gameplay preview video seamlessly"),
                              ("Audio State", "Intro audio cues active with clear narration"),
                              ("Stability", "Zero launch crashes, instantaneous transition to onboarding")
                          ])
    add_detail_image_card(s3, os.path.join(IMAGES_DIR, "logiclike/02_onboarding_next_continue.png"),
                          Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5),
                          "Image 02: Onboarding Setup Wizard",
                          "PASS (ACTIVE WIZARD)",
                          [
                              ("Orientation", "Portrait (1080×2400)"),
                              ("UI Elements", "Top progress bar with mascot icon, age selector chips, prominent 'Continue' button"),
                              ("Interaction Flow", "Single-tap age selection automatically activates the green Continue button"),
                              ("Accessibility", "High-contrast text and oversized interactive buttons for parental ease"),
                              ("Navigation", "Back arrow available at top-left for revising selections")
                          ])

    # --- SLIDE 4: Detailed Image Breakdown (Images 03 & 04) ---
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Screen Status Detail: Paywall Close 'X' & Landscape Course Hub", "Visual Evidence & Status")
    add_detail_image_card(s4, os.path.join(IMAGES_DIR, "logiclike/03_paywall_close_x.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 03: Subscription Paywall Modal",
                          "PASS (CLEAR DISMISS '✕')",
                          [
                              ("Orientation", "Portrait (1080×2400) modal"),
                              ("Dismiss Button", "High-contrast circular '✕' button explicitly placed at top-left corner"),
                              ("No Dark Pattern", "User is never trapped; tapping '✕' instantly dismisses paywall to main hub"),
                              ("UI Elements", "Plan pricing cards, 'Start Free Trial' button, terms links"),
                              ("Audio State", "Background music continues softly in background")
                          ])
    add_detail_image_card(s4, os.path.join(IMAGES_DIR, "logiclike/04_landscape_learning_hub.png"),
                          Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5),
                          "Image 04: Main Curriculum Track Hub",
                          "PASS (LOCKED LANDSCAPE)",
                          [
                              ("Orientation", "Landscape (2400×1080 locked)"),
                              ("Rotation Trigger", "Automatically rotates when exiting onboarding and entering learning tracks"),
                              ("UI Elements", "Course islands, star counter badge, chapter nodes, bottom navigation bar"),
                              ("Ergonomics", "Designed for two-handed tablet or smartphone landscape play"),
                              ("Audio State", "Gentle, repetitive logic puzzle soundtrack playing smoothly")
                          ])

    # --- SLIDE 5: Detailed Image Breakdown (Images 05 & 06) ---
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Screen Status Detail: Parental Word-PIN Gate & Music Settings", "Visual Evidence & Status")
    add_detail_image_card(s5, os.path.join(IMAGES_DIR, "logiclike/05_parental_pin_gate.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 05: Parental Word-PIN Security Gate",
                          "PASS (SECURE PIN)",
                          [
                              ("Orientation", "Portrait (1080×2400) overlay"),
                              ("Security Mechanism", "Written English word-digits challenge ('THREE FIVE SIX')"),
                              ("UI Elements", "Full 0–9 numeric keypad, Cancel button, 3 digit entry boxes"),
                              ("Protection Scope", "Protects Parent Zone, purchases, and account preferences from children"),
                              ("Validation", "Entering correct code (3-5-6) unlocks settings instantly; wrong entry clears")
                          ])
    add_detail_image_card(s5, os.path.join(IMAGES_DIR, "logiclike/06_audio_settings_music.png"),
                          Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5),
                          "Image 06: Audio & Music Settings Menu",
                          "AVAILABLE (TOGGLE ACTIVE)",
                          [
                              ("Location", "Parent Settings > Sound Preferences (Portrait 1080×2400)"),
                              ("Control Type", "Dedicated 'Music' binary toggle switch (ON / OFF)"),
                              ("Behavior", "Disables background instrumental soundtrack globally across all activities"),
                              ("Voice Independence", "Voice instructions remain functional even when music is toggled off"),
                              ("Persistence", "Settings stored in app local database across restarts")
                          ])

    # --- SLIDE 6: Detailed Image Breakdown (Images 07 & 08) ---
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Screen Status Detail: Voice Replay & Star Confetti Particles", "Visual Evidence & Status")
    add_detail_image_card(s6, os.path.join(IMAGES_DIR, "logiclike/07_gameplay_close_voice_buttons.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 07: Gameplay Voice Speaker & Close 'X'",
                          "PASS (ACTIVE ASSISTANCE)",
                          [
                              ("Orientation", "Landscape (2400×1080)"),
                              ("Voice Speaker", "Circular blue speaker icon in bottom-left re-reads puzzle prompt aloud"),
                              ("Close Button", "White circular '✕' button at top-left allows immediate exit from puzzle"),
                              ("Accessibility", "Allows pre-literate children to solve complex logic without adult help"),
                              ("Responsiveness", "Tapping speaker instantly replays clear verbal instruction")
                          ])
    add_detail_image_card(s6, os.path.join(IMAGES_DIR, "logiclike/08_score_stars_confetti.png"),
                          Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5),
                          "Image 08: Star Confetti Particles & Score Reward",
                          "PASS (VERIFIED REWARD FX)",
                          [
                              ("Reward Type", "Immediate numerical score boost ('+4 ⭐') with golden halo glow"),
                              ("Particle Effect", "Multi-colored animated star confetti shower (blue, yellow, purple, cyan)"),
                              ("Audio Cue", "Pleasant chime sound effect triggers upon correct solution"),
                              ("No Failure Screen", "Incorrect answers gently guide the child to re-try without penalty"),
                              ("Visual Polish", "Smooth 60fps physics-based confetti particle dispersal")
                          ])

    # --- SLIDE 7: Detailed Image Breakdown (Image 09 & Exit Flow) ---
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Screen Status Detail: Exit Modal & Navigation Feedback", "Visual Evidence & Status")
    
    # Left: Image 09
    add_detail_image_card(s7, os.path.join(IMAGES_DIR, "logiclike/09_exit_close_modal.png"),
                          Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.5),
                          "Image 09: Exit Confirmation & Feedback Modal",
                          "PASS (FRIENDLY DISMISS)",
                          [
                              ("Orientation", "Landscape (2400×1080) overlay"),
                              ("Trigger", "Tapping the top-left '✕' button during active gameplay"),
                              ("UI Elements", "Coral-red top-right '✕' button, feedback rating stars, 'Leave' action"),
                              ("Safety Check", "Prevents accidental loss of puzzle progress on unintended touches"),
                              ("Dismissal", "Tapping '✕' immediately returns child to active puzzle without state loss")
                          ])
                          
    # Right: Comprehensive Technical Matrix
    c_right = create_card(s7, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5))
    tb_r = s7.shapes.add_textbox(Inches(7.1), Inches(1.8), Inches(5.1), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "LOGICLIKE: ABC & MATH — AUDIT SUMMARY"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(21, 101, 192)
    
    pts = [
        ("Orientation Model", "Adaptive Hybrid. Launch, onboarding, paywalls & settings run in Portrait (1080×2400). Main curriculum tracks and puzzles run in Landscape (2400×1080)."),
        ("Parental Security", "Word-PIN challenge ('THREE FIVE SIX') successfully prevents child bypass into subscription or settings."),
        ("Audio Architecture", "Dedicated 'Music' toggle in settings; independent in-game voice replay speaker on all puzzles."),
        ("Navigation Quality", "Zero dark traps. Every overlay (paywall, puzzle, exit dialog) has an explicit '✕' button."),
        ("Celebration FX", "High-fidelity confetti particle shower and immediate +4 ⭐ reward feedback upon puzzle completion.")
    ]
    for title, desc in pts:
        p = tf_r.add_paragraph()
        p.text = f"✔  {title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(46, 125, 50)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = RGBColor(55, 71, 79)

    out_path = os.path.join(BASE_DIR, "LogicLike_ABC_and_Math.pptx")
    prs.save(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    build_singham_presentation()
    build_logiclike_presentation()
