import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

BASE_DIR = "/home/das/Documents/game_review"
IMAGES_DIR = os.path.join(BASE_DIR, "images")

def add_header(slide, title_text, category_text, prs_width, bg_color=RGBColor(245, 247, 250)):
    # Banner at top
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

def add_image_card(slide, img_path, left, top, max_w, max_h, title="", caption=""):
    # Calculate dimensions
    if not os.path.exists(img_path):
        return
    with Image.open(img_path) as im:
        iw, ih = im.size
        aspect = iw / ih

    # Card container
    card = create_card(slide, left, top, max_w, max_h, RGBColor(255, 255, 255), RGBColor(207, 216, 220))
    
    # Text at bottom
    text_h = Inches(1.1)
    content_h = max_h - text_h - Inches(0.2)
    
    # Fit image inside (max_w - 0.3, content_h)
    target_w = max_w - Inches(0.4)
    target_h = content_h
    
    if target_w / target_h > aspect:
        fit_h = target_h
        fit_w = fit_h * aspect
    else:
        fit_w = target_w
        fit_h = fit_w / aspect
        
    img_left = left + (max_w - fit_w) / 2
    img_top = top + Inches(0.15) + (content_h - fit_h) / 2
    
    slide.shapes.add_picture(img_path, img_left, img_top, fit_w, fit_h)
    
    # Caption box
    c_box = slide.shapes.add_textbox(left + Inches(0.2), top + max_h - text_h, max_w - Inches(0.4), text_h)
    tf = c_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.bold = True
    p1.font.size = Pt(12)
    p1.font.color.rgb = RGBColor(38, 50, 56)
    
    p2 = tf.add_paragraph()
    p2.text = caption
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(100, 116, 139)

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
    
    # Accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(1.8), Inches(0.15), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(255, 111, 0) # Amber orange
    bar.line.fill.background()
    
    t_box = s1.shapes.add_textbox(Inches(1.4), Inches(1.8), Inches(10.5), Inches(3.6))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "QA & UX EVALUATION REPORT"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 179, 0)
    
    p2 = tf.add_paragraph()
    p2.text = "Little Singham: Play & Learn"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    
    p3 = tf.add_paragraph()
    p3.text = "Technical Gameplay, Audio Architecture, Orientation & Navigation Audit"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(207, 216, 220)
    
    meta_box = s1.shapes.add_textbox(Inches(1.4), Inches(5.6), Inches(10.5), Inches(1.2))
    mtf = meta_box.text_frame
    p_meta = mtf.paragraphs[0]
    p_meta.text = "Package: com.ct.littlesingham  |  Device: Vivo V2153 (Android 14)  |  Resolution: 2400×1080"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = RGBColor(176, 190, 197)

    # --- SLIDE 2: Executive Overview ---
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Overview & Product Architecture", "Application Profile", prs.slide_width)
    
    # Left Card
    c1 = create_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb1 = s2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "Product Details & Target Audience"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(26, 35, 126)
    
    items = [
        ("Game Name", "Little Singham: Play & Learn"),
        ("Developer", "Creative Galileo (Reliance Animation IP)"),
        ("Package Identifier", "com.ct.littlesingham"),
        ("Target Demographic", "Ages 3–8 (Early Preschool to Class 2)"),
        ("Curriculum Scope", "Phonics, Numbers, Colors, Hindi & English rhymes"),
        ("Core Architecture", "Native Android wrapper embedding WebView GameViewActivity with HTML5/Canvas interactive modules.")
    ]
    for label, val in items:
        p = tf1.add_paragraph()
        p.text = f"•  {label}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(55, 71, 79)
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = RGBColor(84, 110, 122)

    # Right Card: Key Highlights
    c2 = create_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb2 = s2.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    
    p = tf2.paragraphs[0]
    p.text = "Core Strengths & UX Observations"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(255, 111, 0)
    
    highlights = [
        ("Culturally Resonant IP", "Capitalizes on Little Singham animated franchise to keep children naturally engaged with recognizable voiceovers."),
        ("Dynamic Orientation Strategy", "Distinguishes child experience (Landscape 2400×1080) from parent management zone (Portrait 1080×2400)."),
        ("Child-Friendly Safe Audio", "Dedicated one-tap mute button inside gameplay gives instant quiet control without interrupting child progress."),
        ("Accessible Progression Bar", "Uses intuitive visual fill tubes and incremental 1-to-3 golden stars instead of punitive game-over fail screens."),
        ("Robust Parental Protection", "Arithmetic challenge gate ensures children do not accidentally access account or subscription menus.")
    ]
    for h_title, h_desc in highlights:
        p = tf2.add_paragraph()
        p.text = f"✔  {h_title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(46, 125, 50)
        p_desc = tf2.add_paragraph()
        p_desc.text = f"    {h_desc}"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = RGBColor(100, 116, 139)

    # --- SLIDE 3: Evaluation Checklist Table ---
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Comprehensive QA Parameter Checklist", "Evaluation Matrix", prs.slide_width)
    
    rows, cols = 8, 4
    table_shape = s3.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(1.6)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(5.3)
    
    headers = ["Evaluation Parameter", "Status", "Visual Reference", "Key QA Findings"]
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
        ("Splash Screen & Loading", "PASS", "01_splash_loading.png", "Animated branding with responsive loading bar; zero crashes on launch."),
        ("Landscape Mode (Gameplay)", "PASS", "02_landscape_main_hub.png", "Strict 2400×1080 landscape locked for all interactive child modules."),
        ("Parental Gate", "PASS", "03_parental_math_gate.png", "Randomized arithmetic question (e.g. 55 + 6 = 61) prevents unauthorized access."),
        ("Dynamic Portrait Mode", "PASS", "04_portrait_parent_home.png", "Seamlessly rotates display to Portrait (1080×2400) upon entering parent area."),
        ("BGM / Audio Toggle", "AVAILABLE", "05_audio_settings_bgm.png", "Preferences menu features global Background Music toggle switch."),
        ("In-Game Audio Controls", "PASS", "07_in_game_audio_mute.png", "Dedicated speaker icon inside gameplay allows instant mute/unmute."),
        ("Score, Stars & Rewards", "PASS", "08_level_progress_stars.png", "Vertical tube filling mechanism and 1–3 golden stars reward completion.")
    ]
    for row_idx, data in enumerate(checklist_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10.5)
                if col_idx == 1:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(46, 125, 50) if "PASS" in text else RGBColor(230, 81, 0)
                else:
                    p.font.color.rgb = RGBColor(55, 71, 79)

    # --- SLIDE 4: Visual Walkthrough - Splash & Main Hub ---
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Visual Walkthrough: Launch Flow & Main Child Hub", "User Experience Evidence", prs.slide_width)
    add_image_card(s4, os.path.join(IMAGES_DIR, "singham/01_splash_loading.png"),
                   Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
                   "01. Splash & Loading Screen",
                   "Branded launch screen with animated characters and dynamic asset loading status bar.")
    add_image_card(s4, os.path.join(IMAGES_DIR, "singham/02_landscape_main_hub.png"),
                   Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
                   "02. Landscape Interactive Hub",
                   "Rich horizontal dashboard displaying curriculum categories (English, Math, Hindi, Colors).")

    # --- SLIDE 5: Visual Walkthrough - Parental Gate & Dynamic Portrait Switch ---
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Visual Walkthrough: Parental Protection & Dynamic Rotation", "User Experience Evidence", prs.slide_width)
    add_image_card(s5, os.path.join(IMAGES_DIR, "singham/03_parental_math_gate.png"),
                   Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
                   "03. Arithmetic Parental Gate",
                   "Calculation challenge prevents accidental in-app purchases and verifies adult presence.")
    add_image_card(s5, os.path.join(IMAGES_DIR, "singham/04_portrait_parent_home.png"),
                   Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
                   "04. Dynamic Portrait Parent Zone",
                   "Hardware automatically rotates to portrait (1080×2400) optimized for single-hand adult browsing.")

    # --- SLIDE 6: Visual Walkthrough - Audio Controls & Navigation ---
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Visual Walkthrough: Audio Architecture & Quick In-Game Mute", "User Experience Evidence", prs.slide_width)
    add_image_card(s6, os.path.join(IMAGES_DIR, "singham/05_audio_settings_bgm.png"),
                   Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
                   "05. Global BGM Toggle in Settings",
                   "Parent preferences toggle allows switching off persistent background cartoon music.")
    add_image_card(s6, os.path.join(IMAGES_DIR, "singham/07_in_game_audio_mute.png"),
                   Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
                   "06. Instant Gameplay Mute Button",
                   "Prominent speaker icon in top-right enables immediate one-touch sound muting.")

    # --- SLIDE 7: Visual Walkthrough - Gameplay Navigation & Reward Progression ---
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Visual Walkthrough: Navigation & Positive Reinforcement", "User Experience Evidence", prs.slide_width)
    add_image_card(s7, os.path.join(IMAGES_DIR, "singham/06_gameplay_navigation_buttons.png"),
                   Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
                   "07. Child-Oriented Navigation",
                   "Prominent orange Back button ('<') and carousel navigation designed for toddler tap accuracy.")
    add_image_card(s7, os.path.join(IMAGES_DIR, "singham/08_level_progress_stars.png"),
                   Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
                   "08. Star Rewards & Progress Tube",
                   "Visual filling bar and 3-star milestone celebrations provide clear learning incentives.")

    # --- SLIDE 8: Recommendations & Conclusion ---
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Key Recommendations & QA Summary", "Strategic Recommendations", prs.slide_width)
    
    c_rec1 = create_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb_rec1 = s8.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.6))
    tfr1 = tb_rec1.text_frame
    tfr1.word_wrap = True
    
    p = tfr1.paragraphs[0]
    p.text = "Identified UX & Audio Improvements"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(198, 40, 40)
    
    recs = [
        ("Granular Volume Sliders", "Currently only a binary BGM toggle is available. Adding separate Master, SFX, and Voice sliders would prevent voice prompts from being overwhelmed by music."),
        ("Replay Voice Prompt Button", "Adding an explicit, high-contrast repeat audio button on all gameplay screens would assist auditory learners who miss spoken instructions."),
        ("Smooth Rotation Transitions", "Screen rotation between landscape gameplay and portrait settings has a brief frame flash; adding an orientation fade transition would improve polish.")
    ]
    for r_title, r_desc in recs:
        p = tfr1.add_paragraph()
        p.text = f"▲  {r_title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(198, 40, 40)
        p_desc = tfr1.add_paragraph()
        p_desc.text = f"    {r_desc}"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = RGBColor(100, 116, 139)

    c_rec2 = create_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb_rec2 = s8.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.6))
    tfr2 = tb_rec2.text_frame
    tfr2.word_wrap = True
    
    p = tfr2.paragraphs[0]
    p.text = "Final QA Verdict"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(46, 125, 50)
    
    p_verdict = tfr2.add_paragraph()
    p_verdict.text = "STATUS: CERTIFIED CHILD-READY (HIGH ENGAGEMENT)"
    p_verdict.font.bold = True
    p_verdict.font.size = Pt(13)
    p_verdict.font.color.rgb = RGBColor(46, 125, 50)
    
    v_points = [
        "Little Singham: Play & Learn demonstrates excellent COPPA compliance with effective parental gating.",
        "Zero crash events observed across launching, orientation switches, and gameplay modules.",
        "UI hit targets are well scaled for early childhood fine motor skills (minimum 48dp+ buttons).",
        "Reward loops utilize positive reinforcement without high-stress timers or punitive failure states."
    ]
    for pt in v_points:
        p = tfr2.add_paragraph()
        p.text = f"✔  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(55, 71, 79)

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
    
    # Accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1), Inches(1.8), Inches(0.15), Inches(3.6))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(142, 36, 170) # Purple
    bar.line.fill.background()
    
    t_box = s1.shapes.add_textbox(Inches(1.4), Inches(1.8), Inches(10.5), Inches(3.6))
    tf = t_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "QA & UX EVALUATION REPORT"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(179, 229, 252)
    
    p2 = tf.add_paragraph()
    p2.text = "LogicLike: ABC & Math"
    p2.font.size = Pt(40)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    
    p3 = tf.add_paragraph()
    p3.text = "Interactive Logic Puzzles, Confetti FX, Word-PIN Gate & Audio Design Review"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(227, 242, 253)
    
    meta_box = s1.shapes.add_textbox(Inches(1.4), Inches(5.6), Inches(10.5), Inches(1.2))
    mtf = meta_box.text_frame
    p_meta = mtf.paragraphs[0]
    p_meta.text = "Package: com.logicappkids  |  Device: Vivo V2153 (Android 14)  |  Resolution: 2400×1080"
    p_meta.font.size = Pt(12)
    p_meta.font.color.rgb = RGBColor(187, 222, 251)

    # --- SLIDE 2: Executive Overview ---
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Overview & App Architecture", "Application Profile", prs.slide_width)
    
    # Left Card
    c1 = create_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb1 = s2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "Product Details & Target Audience"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(21, 101, 192)
    
    items = [
        ("Game Name", "LogicLike: ABC & Math"),
        ("Developer", "LogicLike Educational Games"),
        ("Package Identifier", "com.logicappkids"),
        ("Target Demographic", "Ages 4–12 (Early Logic, Math & Spatial Reasoning)"),
        ("Curriculum Scope", "3D Puzzles, Math, Spatial deduction, Word riddles"),
        ("Core Architecture", "High-performance native client with custom vector/2D rendering engine and dynamic portrait-landscape switcher.")
    ]
    for label, val in items:
        p = tf1.add_paragraph()
        p.text = f"•  {label}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(55, 71, 79)
        run = p.add_run()
        run.text = val
        run.font.bold = False
        run.font.color.rgb = RGBColor(84, 110, 122)

    # Right Card: Key Highlights
    c2 = create_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb2 = s2.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    
    p = tf2.paragraphs[0]
    p.text = "Core Strengths & UX Highlights"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(142, 36, 170)
    
    highlights = [
        ("Exceptional Reward FX", "Vibrant multi-colored star confetti particles burst upon completion with energetic sound cues (+4 ⭐)."),
        ("Built-in Voice Assistance", "Persistent speaker button on every puzzle reads instructions aloud, empowering non-reading kids."),
        ("Word-PIN Parental Protection", "Presents written English numbers ('THREE FIVE SIX') with numeric keypad, requiring adult comprehension."),
        ("Clear Navigation & Dismissals", "Uniform Close 'X' icons allow friction-free exits from paywalls, puzzles, and feedback dialogs."),
        ("Adaptive Onboarding", "Starts in mobile-natural Portrait mode before transitioning to Landscape for puzzle manipulation.")
    ]
    for h_title, h_desc in highlights:
        p = tf2.add_paragraph()
        p.text = f"✔  {h_title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(46, 125, 50)
        p_desc = tf2.add_paragraph()
        p_desc.text = f"    {h_desc}"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = RGBColor(100, 116, 139)

    # --- SLIDE 3: Evaluation Checklist Table ---
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Comprehensive QA Parameter Checklist", "Evaluation Matrix", prs.slide_width)
    
    rows, cols = 8, 4
    table_shape = s3.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(1.6)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(5.3)
    
    headers = ["Evaluation Parameter", "Status", "Visual Reference", "Key QA Findings"]
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
        ("Splash Screen & Launch", "PASS", "01_portrait_welcome_splash.png", "Animated mascot video preview with clear 'Get Started' call-to-action."),
        ("Portrait Onboarding Flow", "PASS", "02_onboarding_next_continue.png", "Vertical step-by-step age and goal configuration wizard."),
        ("Paywall Close 'X' Button", "PASS", "03_paywall_close_x.png", "High-contrast 'X' in top-left allows immediate dismissal without entrapment."),
        ("Landscape Learning Hub", "PASS", "04_landscape_learning_hub.png", "Smooth rotation to Landscape (2400×1080) for wide course selection."),
        ("Parental Word-PIN Gate", "PASS", "05_parental_pin_gate.png", "English word prompt ('THREE FIVE SIX') protects account & settings."),
        ("Audio / Music Toggle", "AVAILABLE", "06_audio_settings_music.png", "Parent settings provide master 'Music' toggle on/off switch."),
        ("Voice Replay & Close Buttons", "PASS", "07_gameplay_close_voice_buttons.png", "Bottom-left audio replay speaker and top-left exit button in puzzle view.")
    ]
    for row_idx, data in enumerate(checklist_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10.5)
                if col_idx == 1:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(46, 125, 50) if "PASS" in text else RGBColor(230, 81, 0)
                else:
                    p.font.color.rgb = RGBColor(55, 71, 79)

    # --- SLIDE 4: Visual Walkthrough - Welcome Splash & Onboarding ---
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Visual Walkthrough: Onboarding & Setup Flow (Portrait)", "User Experience Evidence", prs.slide_width)
    add_image_card(s4, os.path.join(IMAGES_DIR, "logiclike/01_portrait_welcome_splash.png"),
                   Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
                   "01. Dynamic Welcome Splash",
                   "Live mascot video demonstration with primary 'Get Started' action.")
    add_image_card(s4, os.path.join(IMAGES_DIR, "logiclike/02_onboarding_next_continue.png"),
                   Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
                   "02. Step-by-Step Onboarding",
                   "Age selection wizard with progress bar and accessible 'Continue' button.")

    # --- SLIDE 5: Visual Walkthrough - Paywall Close & Landscape Hub ---
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Visual Walkthrough: Subscription Dismissal & Course Hub", "User Experience Evidence", prs.slide_width)
    add_image_card(s5, os.path.join(IMAGES_DIR, "logiclike/03_paywall_close_x.png"),
                   Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
                   "03. Paywall with Dismiss 'X'",
                   "Transparent subscription modal with prominent close icon.")
    add_image_card(s5, os.path.join(IMAGES_DIR, "logiclike/04_landscape_learning_hub.png"),
                   Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
                   "04. Landscape Curriculum Track",
                   "Expansive horizontal course map displaying chapters and star tiers.")

    # --- SLIDE 6: Visual Walkthrough - Parental Gate & Audio Settings ---
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Visual Walkthrough: Parental Word-PIN & Music Settings", "User Experience Evidence", prs.slide_width)
    add_image_card(s6, os.path.join(IMAGES_DIR, "logiclike/05_parental_pin_gate.png"),
                   Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
                   "05. Parental Word-PIN Challenge",
                   "Security keypad requiring reading of word numbers ('THREE FIVE SIX').")
    add_image_card(s6, os.path.join(IMAGES_DIR, "logiclike/06_audio_settings_music.png"),
                   Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
                   "06. Background Music Toggle",
                   "Parent preferences toggle for disabling ambient soundtrack.")

    # --- SLIDE 7: Visual Walkthrough - Gameplay, Voice, Confetti & Exit ---
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Visual Walkthrough: Puzzle Voice, Star Confetti & Exit Flow", "User Experience Evidence", prs.slide_width)
    add_image_card(s7, os.path.join(IMAGES_DIR, "logiclike/07_gameplay_close_voice_buttons.png"),
                   Inches(0.8), Inches(1.6), Inches(3.7), Inches(5.2),
                   "07. Voice Speaker & Close 'X'",
                   "In-game audio prompt button to repeat instructions aloud.")
    add_image_card(s7, os.path.join(IMAGES_DIR, "logiclike/08_score_stars_confetti.png"),
                   Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.2),
                   "08. Confetti & Star Score",
                   "Explosion of colorful star confetti rewarding +4 ⭐.")
    add_image_card(s7, os.path.join(IMAGES_DIR, "logiclike/09_exit_close_modal.png"),
                   Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
                   "09. Exit Feedback Modal",
                   "Friendly feedback modal with prominent close 'X' button.")

    # --- SLIDE 8: Recommendations & Conclusion ---
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Key Recommendations & QA Summary", "Strategic Recommendations", prs.slide_width)
    
    c_rec1 = create_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb_rec1 = s8.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.6))
    tfr1 = tb_rec1.text_frame
    tfr1.word_wrap = True
    
    p = tfr1.paragraphs[0]
    p.text = "Identified UX & Localization Opportunities"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(198, 40, 40)
    
    recs = [
        ("Multilingual Parental PIN", "Parental challenge displays English words ('THREE FIVE SIX'). Supporting regional languages (Hindi, etc.) or mathematical operations would benefit non-English speaking parents."),
        ("Direct In-Puzzle Mute Toggle", "While music can be toggled in parent settings, an in-game sound toggle alongside the voice replay speaker would give immediate volume control."),
        ("Confetti Particle Duration", "Celebratory confetti animation is visually spectacular but could allow instant tap-to-skip for rapid puzzle solvers.")
    ]
    for r_title, r_desc in recs:
        p = tfr1.add_paragraph()
        p.text = f"▲  {r_title}"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(198, 40, 40)
        p_desc = tfr1.add_paragraph()
        p_desc.text = f"    {r_desc}"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = RGBColor(100, 116, 139)

    c_rec2 = create_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb_rec2 = s8.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.6))
    tfr2 = tb_rec2.text_frame
    tfr2.word_wrap = True
    
    p = tfr2.paragraphs[0]
    p.text = "Final QA Verdict"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(46, 125, 50)
    
    p_verdict = tfr2.add_paragraph()
    p_verdict.text = "STATUS: CERTIFIED CHILD-READY (PREMIUM UX)"
    p_verdict.font.bold = True
    p_verdict.font.size = Pt(13)
    p_verdict.font.color.rgb = RGBColor(46, 125, 50)
    
    v_points = [
        "LogicLike exhibits best-in-class visual polish, high-frame-rate animations, and child accessibility.",
        "Clear audio guidance ensures pre-literate children can independently solve reasoning puzzles.",
        "Zero dark UX patterns: paywalls and dialogs feature prominent, unmistakable close 'X' buttons.",
        "Star score (+4 ⭐) and confetti particles deliver immediate positive dopamine feedback."
    ]
    for pt in v_points:
        p = tfr2.add_paragraph()
        p.text = f"✔  {pt}"
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(55, 71, 79)

    out_path = os.path.join(BASE_DIR, "LogicLike_ABC_and_Math.pptx")
    prs.save(out_path)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    build_singham_presentation()
    build_logiclike_presentation()
