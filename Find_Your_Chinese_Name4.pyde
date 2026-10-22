# Find Your Chinese Name - Version 4 - Startup diagnostics
#
# Name tags and overall meanings are design interpretations for this prototype, not the only possible interpretations.
#
# Reference: official Processing Python Mode API.
# https://py.processing.org/reference/millis
# https://py.processing.org/reference/vertex
# The API documentation explains the functions; it is not the source of the entire project code.
# https://py.processing.org/reference/
#
# Program structure:
# 1. Data: word list and name list.
# 2. State: current page, selected words, and animation timing.
# 3. Drawing: cover, selection page, and results page.
# 4. Interaction: clicking, changing batches, matching, and restarting.

from random import shuffle
import sys
import traceback

# DEBUG controls console messages only; they do not appear in the project interface.
# Set this to False after debugging; exception details will still be printed.
DEBUG = True

def debug_log(message):
    if DEBUG:
        print(message)
        sys.stdout.flush()

debug_log("[1/5] Sketch source loaded")

# Each tuple stores a word and its English explanation.
# Personality, meaning, and style words are mixed together; users do not have to choose one from each category.
words = [
    ("Calm", "Having a quiet and relaxed personality."),
    ("Creative", "Enjoying new ideas and imagination."),
    ("Brave", "Facing challenges with confidence."),
    ("Kind", "Showing care and warmth to others."),
    ("Cheerful", "Having a happy and positive personality."),
    ("Peace", "A wish for a calm and balanced life."),
    ("Wisdom", "A wish for knowledge and understanding."),
    ("Nature", "A connection with plants, mountains and sky."),
    ("Hope", "A belief in a bright and promising future."),
    ("Strength", "Staying strong through difficulties."),
    ("Traditional", "A style with a classic and familiar feeling."),
    ("Modern", "A style with a fresh and contemporary feeling."),
    ("Elegant", "A style expressing grace and refinement."),
    ("Poetic", "A style suggesting imagery and imagination."),
    ("Simple", "A style that feels clear and understated.")
]

# Each record stores: Chinese name, pinyin, character meanings, overall meaning, and tags.
# The u prefix marks a Unicode string so Chinese names are handled as text.
name_data = [
    (u"安宁", "An Ning", "An: peace and safety. Ning: tranquility.",
     "A peaceful and settled life.", ["Calm", "Peace", "Traditional", "Simple"]),
    (u"静怡", "Jing Yi", "Jing: quiet. Yi: happiness.",
     "Quiet happiness and inner peace.", ["Calm", "Cheerful", "Peace", "Elegant"]),
    (u"思宁", "Si Ning", "Si: thought. Ning: tranquility.",
     "A thoughtful mind and a peaceful heart.", ["Calm", "Wisdom", "Peace", "Simple"]),
    (u"云舒", "Yun Shu", "Yun: cloud. Shu: unfold or relax.",
     "A relaxed spirit, like clouds unfolding.", ["Calm", "Nature", "Peace", "Elegant", "Poetic"]),
    (u"清和", "Qing He", "Qing: clear or pure. He: harmony.",
     "Clarity, gentleness and balance.", ["Calm", "Peace", "Elegant", "Traditional"]),
    (u"知新", "Zhi Xin", "Zhi: know. Xin: new.",
     "A curious mind open to new understanding.", ["Creative", "Wisdom", "Modern", "Simple"]),
    (u"思远", "Si Yuan", "Si: thought. Yuan: distant.",
     "Thoughts reaching towards distant possibilities.", ["Creative", "Wisdom", "Hope", "Traditional"]),
    (u"睿思", "Rui Si", "Rui: insightful. Si: thought.",
     "Insightful and imaginative thinking.", ["Creative", "Wisdom", "Elegant"]),
    (u"文心", "Wen Xin", "Wen: writing or culture. Xin: heart.",
     "A heart drawn to learning and expression.", ["Creative", "Wisdom", "Traditional", "Poetic"]),
    (u"新语", "Xin Yu", "Xin: new. Yu: language or expression.",
     "A fresh voice and new ways of expressing ideas.", ["Creative", "Hope", "Modern", "Poetic"]),
    (u"凌峰", "Ling Feng", "Ling: rise above. Feng: mountain peak.",
     "The courage to reach a mountain summit.", ["Brave", "Strength", "Nature", "Modern"]),
    (u"志远", "Zhi Yuan", "Zhi: aspiration. Yuan: distant.",
     "The resolve to pursue far-reaching goals.", ["Brave", "Strength", "Hope", "Traditional"]),
    (u"毅然", "Yi Ran", "Yi: resolve. Ran: so or in that manner.",
     "A firm and determined spirit.", ["Brave", "Strength", "Simple"]),
    (u"致远", "Zhi Yuan", "Zhi: reach. Yuan: distant.",
     "Steady effort towards a distant goal.", ["Brave", "Strength", "Hope", "Traditional"]),
    (u"云帆", "Yun Fan", "Yun: cloud. Fan: sail.",
     "A sail moving towards open possibilities.", ["Brave", "Nature", "Hope", "Poetic"]),
    (u"嘉悦", "Jia Yue", "Jia: good or fine. Yue: delight.",
     "Appreciating goodness and finding joy.", ["Kind", "Cheerful", "Elegant", "Modern"]),
    (u"乐善", "Le Shan", "Le: take pleasure in. Shan: goodness.",
     "Finding joy in doing good.", ["Kind", "Cheerful", "Traditional", "Simple"]),
    (u"怀仁", "Huai Ren", "Huai: cherish. Ren: benevolence.",
     "Holding kindness close to the heart.", ["Kind", "Traditional", "Elegant"]),
    (u"惠宁", "Hui Ning", "Hui: kindness. Ning: tranquility.",
     "Kindness expressed with a peaceful spirit.", ["Kind", "Calm", "Peace", "Traditional"]),
    (u"思善", "Si Shan", "Si: think. Shan: goodness.",
     "Thoughtful choices guided by kindness.", ["Kind", "Wisdom", "Simple"]),
    (u"欣然", "Xin Ran", "Xin: delight. Ran: so or in that manner.",
     "A cheerful and willing spirit.", ["Cheerful", "Modern", "Simple"]),
    (u"乐宁", "Le Ning", "Le: happiness. Ning: tranquility.",
     "Happiness together with peace of mind.", ["Cheerful", "Calm", "Peace", "Simple"]),
    (u"向阳", "Xiang Yang", "Xiang: towards. Yang: sun.",
     "Turning towards warmth and light.", ["Cheerful", "Hope", "Nature", "Simple"]),
    (u"晨曦", "Chen Xi", "Chen: morning. Xi: sunlight.",
     "The first light of a new beginning.", ["Hope", "Nature", "Modern", "Poetic"]),
    (u"星辰", "Xing Chen", "Xing: star. Chen: celestial bodies.",
     "A sky full of stars and possibilities.", ["Creative", "Hope", "Nature", "Modern", "Poetic"]),
    (u"若竹", "Ruo Zhu", "Ruo: like. Zhu: bamboo.",
     "The grace and resilience of bamboo.", ["Nature", "Strength", "Elegant", "Poetic"]),
    (u"清溪", "Qing Xi", "Qing: clear. Xi: stream.",
     "The clear, peaceful flow of a stream.", ["Calm", "Peace", "Nature", "Elegant", "Poetic"]),
    (u"雨桐", "Yu Tong", "Yu: rain. Tong: the Chinese parasol tree.",
     "Fresh rain and the quiet beauty of a tree.", ["Nature", "Elegant", "Modern", "Poetic"]),
    (u"诗涵", "Shi Han", "Shi: poetry. Han: contain or embrace.",
     "A rich inner world with a poetic spirit.", ["Creative", "Elegant", "Poetic", "Modern"]),
    (u"松立", "Song Li", "Song: pine. Li: stand.",
     "Standing tall and steady like a pine tree.", ["Brave", "Nature", "Strength", "Simple"])
]

# Convert each record into a dictionary so its data can be accessed by field name.
names = []
for chinese, pinyin, meaning, description, tags in name_data:
    names.append({
        "name": chinese, "pinyin": pinyin, "meaning": meaning,
        "description": description, "tags": tags
    })

# RGB colour tuples; use * to pass the three values to fill when drawing.
BACKGROUND = (245, 242, 235)
TEXT = (40, 40, 40)
CARD = (220, 215, 205)
RED = (150, 65, 65)
GREEN = (65, 100, 90)
GRAY = (160, 160, 160)
WHITE = (255, 255, 255)

# page controls the three screens: cover, home, and results.
page = "cover"
selected = []
current_batch = []
seen_words = set()
results = []
notice = ""

# The animation still has 8 poses, each displayed for 90 milliseconds.
# Draw the book directly on the main canvas to reduce off-screen canvas creation and image cropping at startup.
# This is a time-based geometric animation, no longer sprite-sheet playback.
BOOK_W = 144
BOOK_H = 96
BOOK_FRAMES = 8
BOOK_FRAME_MS = 90
COVER_CYCLE_MS = 2400

book_frame = 0
book_started = 0
book_turning = False
cover_started = 0

# Initialise in stages: show a startup message first, then load the Chinese font.
startup_stage = 0
fatal_error = ""
first_frame_reported = False

# Use Microsoft YaHei on Windows; on Mac, this can be changed to PingFang SC.
# Do not scan all system fonts. Missing Chinese fonts may cause characters to appear as boxes.
FONT_NAME = "Microsoft YaHei"


def record_error(stage):
    global fatal_error
    fatal_error = stage
    print("ERROR: " + stage)
    traceback.print_exc()
    sys.stdout.flush()


def setup():
    global cover_started
    # Keep size as the first executable statement in setup, using the default 2D renderer.
    size(720, 760)
    debug_log("[2/5] setup entered; window created")
    try:
        frameRate(30)
        change_batch()
        cover_started = millis()
        debug_log("[3/5] Word data ready")
    except Exception:
        record_error("setup")


def draw():
    global startup_stage, cover_started, first_frame_reported
    if fatal_error:
        # Do not repeatedly execute failed code; keep the full exception details in the console.
        # A red background clearly distinguishes an error from a frozen grey-white window.
        background(150, 65, 65)
        return
    try:
        if startup_stage == 0:
            # Complete one drawing pass first so the user can see that draw has started running.
            background(245, 242, 235)
            fill(40, 40, 40)
            textSize(20)
            text("Starting Find Your Chinese Name...", 70, 350)
            startup_stage = 1
            debug_log("[4/5] First draw completed; loading font next")
            return

        if startup_stage == 1:
            # Avoid calling PFont.list() to reduce potential delays from listing system fonts.
            # If the font fails to load, print a message and continue using the default font.
            try:
                textFont(createFont(FONT_NAME, 20))
            except Exception:
                print("Font could not load; using the default font.")
                traceback.print_exc()
                sys.stdout.flush()
            cover_started = millis()
            startup_stage = 2

        update_book_animation()
        background(*BACKGROUND)
        noStroke()
        if page == "cover":
            draw_cover()
        else:
            draw_text("Find Your Chinese Name", 40, 25, 28)
            draw_book(572, -2, 108, 72)
            if page == "home":
                draw_home()
            else:
                draw_results()
        if not first_frame_reported:
            debug_log("[5/5] Cover drawn; ready for Start")
            first_frame_reported = True
    except Exception:
        record_error("draw / " + page)


def draw_text(content, x, y, font_size=16, colour=TEXT):
    fill(*colour)
    textSize(font_size)
    textAlign(LEFT, TOP)
    text(content, x, y)


def centered_text(content, x, y, font_size=16, colour=TEXT):
    fill(*colour)
    textSize(font_size)
    textAlign(CENTER, CENTER)
    text(content, x, y)


def is_inside(x, y, w, h):
    return x <= mouseX <= x + w and y <= mouseY <= y + h


def draw_button(title, x, y, w, h, colour, enabled=True):
    noStroke()
    fill(*colour)
    rect(x, y, w, h, 6)

    # Add a light overlay on hover to show that the button is clickable.
    if enabled and is_inside(x, y, w, h):
        fill(255, 255, 255, 22)
        rect(x, y, w, h, 6)
    centered_text(title, x + w / 2.0, y + h / 2.0, 17, WHITE)


def draw_cover():
    centered_text("Find Your Chinese Name", 360, 85, 32)
    centered_text("Explore the meaning behind a name.", 360, 130, 17)

    # sin varies between -1 and 1, making the book float 6 pixels above and below its base position.
    elapsed = millis() - cover_started
    float_y = 6 * sin(elapsed / 650.0)
    draw_book(216, 190 + float_y, 288, 192)

    centered_text("A name begins with what matters to you.", 360, 423, 19)
    centered_text("Explore words about personality, meaning and style.", 360, 463, 15)
    centered_text("Choose two words to discover five suggested names.", 360, 491, 15)
    draw_button("Start", 180, 552, 360, 52, GREEN)
    centered_text("Take your time. Find words that feel like you.", 360, 640, 14)


def draw_home():
    draw_text("Choose two words about personality, meaning or style.", 40, 76, 15)

    for row, word_index in enumerate(current_batch):
        word, explanation = words[word_index]
        y = 115 + row * 78
        active = word in selected
        fill(*(RED if active else CARD))
        noStroke()
        rect(40, y, 640, 66, 6)
        colour = WHITE if active else TEXT
        draw_text(word, 56, y + 7, 20, colour)
        draw_text(explanation, 56, y + 37, 14, colour)
        if active:
            draw_text("Selected", 590, y + 10, 14, WHITE)

    # Buttons turn grey during the animation, and click events are also blocked.
    title = "Turning the page..." if book_turning else "Show Another Five"
    draw_button(title, 40, 520, 640, 44,
                GRAY if book_turning else GREEN, not book_turning)

    centered_text(str(len(selected)) + "/2", 360, 594, 23)
    caption = "Selected: " + " + ".join(selected) if selected else "No words selected yet."
    centered_text(caption, 360, 625, 15)
    if selected:
        centered_text("Clear selection", 360, 653, 14, RED)
    centered_text(notice, 360, 680, 13, RED)

    ready = len(selected) == 2 and not book_turning
    draw_button("Find My Name", 40, 703, 640, 42,
                GREEN if ready else GRAY, ready)


def draw_results():
    draw_text("Your words: " + " + ".join(selected), 40, 76, 18)
    draw_text("Five suggested given names, with the closest matches first.", 40, 104, 14)

    for index, result in enumerate(results):
        item = result["data"]
        y = 134 + index * 104
        noStroke()
        fill(*CARD)
        rect(40, y, 640, 96, 6)
        draw_text(item["name"], 54, y + 3, 27)
        draw_text(item["pinyin"], 140, y + 11, 18)
        draw_text(str(result["score"]) + "/2 matched", 560, y + 12, 14, GREEN)
        draw_text(item["meaning"], 54, y + 37, 13)
        draw_text(item["description"], 54, y + 56, 14)
        draw_text("Matches: " + ", ".join(result["matched"]), 54, y + 77, 12, GREEN)

    draw_text("Some names match one word. Tags are interpretations for this prototype.",
              40, 665, 12)
    draw_button("Back", 40, 703, 310, 42, GREEN)
    draw_button("Start Again", 370, 703, 310, 42, RED)


def change_batch():
    global current_batch, seen_words, notice
    # Exclude the previous batch and selected words so the five new options do not repeat the previous batch.
    available = []
    for index in range(len(words)):
        if index not in current_batch and words[index][0] not in selected:
            available.append(index)

    # Prioritise words that have not been shown in the current cycle.
    fresh = [index for index in available if index not in seen_words]
    shuffle(fresh)
    if len(fresh) >= 5:
        new_batch = fresh[:5]
    else:
        recycled = [index for index in available if index not in fresh]
        shuffle(recycled)
        new_batch = fresh + recycled[:5 - len(fresh)]
        seen_words = set(current_batch)

    current_batch = new_batch
    seen_words.update(current_batch)
    notice = ""


def select_word(word):
    global notice
    if word in selected:
        selected.remove(word)
        notice = ""
    elif len(selected) < 2:
        selected.append(word)
        notice = ""
    else:
        notice = "Two words selected. Deselect one or clear your selection."


def find_names():
    global results, page
    if len(selected) != 2:
        return

    # Shuffle first so names with the same score can appear in different orders.
    candidates = list(names)
    shuffle(candidates)
    ranked = []

    for item in candidates:
        matched = [word for word in selected if word in item["tags"]]
        if matched:
            ranked.append({
                "data": item,
                "score": len(matched),
                "matched": matched
            })

    # lambda specifies the sorting key; reverse=True places higher scores first.
    ranked.sort(key=lambda item: item["score"], reverse=True)
    results = ranked[:5]
    page = "results"


def draw_book(x, y, w, h):
    # Draw directly on the main canvas without calling createGraphics, get, or image.
    # push/pop preserve the coordinate system and drawing style so later text and buttons are unaffected.
    pushMatrix()
    pushStyle()
    try:
        translate(x, y)
        scale(w / float(BOOK_W), h / float(BOOK_H))
        noStroke()
        fill(40, 30, 20, 28)
        ellipse(72, 82, 118, 12)
        fill(150, 65, 65)
        rect(14, 25, 116, 56, 5)
        fill(255, 251, 238)
        rect(20, 28, 52, 46, 3)
        rect(72, 28, 52, 46, 3)
        stroke(196, 185, 161)
        strokeWeight(2)
        for line_y in [40, 49, 58, 67]:
            line(29, line_y, 62, line_y)
            line(82, line_y, 115, line_y)

        # Frame 0 shows the complete pages as the resting pose.
        # Frames 1 to 7 show the page turning from right to left.
        if book_frame > 0:
            progress = book_frame / float(BOOK_FRAMES - 1)
            tip_x = 72 + 52 * cos(PI * progress)
            lift = 19 * sin(PI * progress)
            fill(249, 240, 216)
            stroke(187, 168, 134)
            strokeWeight(1)
            beginShape()
            vertex(72, 28)
            vertex(tip_x, 28 - lift)
            vertex(tip_x, 74 - lift)
            vertex(72, 74)
            endShape(CLOSE)
        stroke(150, 65, 65)
        strokeWeight(1)
        line(72, 28, 72, 76)
    finally:
        popStyle()
        popMatrix()


def start_book_turn():
    global book_turning, book_started, book_frame, notice
    if book_turning:
        return
    book_turning = True
    book_started = millis()
    book_frame = 0
    notice = ""


def update_book_animation():
    global book_turning, book_frame
    if page == "cover":
        # On the cover, play a page turn every 2.4 seconds and hold the resting pose between turns.
        # % restarts the cycle time from 0 at the end of each cycle.
        cycle_time = (millis() - cover_started) % COVER_CYCLE_MS
        if cycle_time < BOOK_FRAMES * BOOK_FRAME_MS:
            book_frame = int(cycle_time // BOOK_FRAME_MS)
        else:
            book_frame = 0

    elif book_turning:
        # On the selection page, play once; timing does not depend on the actual drawing frame rate.
        elapsed = millis() - book_started
        next_frame = int(elapsed // BOOK_FRAME_MS)
        if next_frame >= BOOK_FRAMES:
            book_turning = False
            book_frame = 0
            change_batch()
        else:
            book_frame = next_frame


def reset_project():
    global page, current_batch, seen_words, results, notice
    global book_turning, book_frame, cover_started
    # Clear the user state and return to the animated cover.
    selected[:] = []
    current_batch = []
    seen_words = set()
    results = []
    notice = ""
    book_turning = False
    book_frame = 0
    change_batch()
    cover_started = millis()
    page = "cover"


def mousePressed():
    # Print click-handling errors in the console to help locate problems.
    if startup_stage < 2 or fatal_error:
        return
    try:
        handle_click()
    except Exception:
        record_error("mousePressed / " + page)


def handle_click():
    global page, notice, book_frame
    if page == "cover":
        if is_inside(180, 552, 360, 52):
            page = "home"
            book_frame = 0
        return

    # Ignore repeated clicks during the batch-change animation to prevent conflicting state changes.
    if book_turning:
        return

    if page == "home":
        for row, word_index in enumerate(current_batch):
            if is_inside(40, 115 + row * 78, 640, 66):
                select_word(words[word_index][0])
                return
        if is_inside(40, 520, 640, 44):
            start_book_turn()
            return
        if selected and is_inside(285, 639, 150, 28):
            selected[:] = []
            notice = ""
            return
        if is_inside(40, 703, 640, 42):
            find_names()
            return

    elif page == "results":
        if is_inside(40, 703, 310, 42):
            page = "home"
            notice = ""
        elif is_inside(370, 703, 310, 42):
            reset_project()
