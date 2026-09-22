# BRIEF — "Weighted Sensory Companions" (working title)

Shared creative + technical brief for everyone building the poster, the demo video and the visual explainer.
Read all of it before producing anything. Paths are absolute.

## 1. Context
- Client: Roy (California, US businesses). Project: the **Sowala / Piga** sensory-toy line. Target market: USA (parents, gift shops, sensory/OT-adjacent retail). Marketing materials are in **English**. The explainer is **bilingual EN + HE** (Hebrew, RTL) because the client reads Hebrew more easily.
- Product: four existing plush toys photographed in the client's shop, to be redesigned as **multi-sensory weighted comfort animals**:
  - **Red Panda** with a curly "lion-mane" hood, closed happy eyes, cream waffle-knit belly, brown embroidered paw pads on the feet. Comes in two sizes (large ≈16 in, small ≈12 in).
  - **Sloth** in taupe long-pile fur, cream face mask + white ear insides, dark nose, white felt claws, paw-pad feet. Also two sizes (large / small). The small sloth has a second sleeping face embroidered on its back.
  - So the "four animals" in the photo are really **2 designs × 2 sizes** — use that as a feature (size + weight tiering), not as four different characters.
- The client's concept text is quoted verbatim in section 9. It is the source of truth for features.

## 2. The system (the story every deliverable tells)
"One companion, four kinds of comfort." All inserts are removable so the outer plush can be washed.

| # | Function | Copy (EN) | Copy (HE) | Color token |
|---|----------|-----------|-----------|-------------|
| 1 | **WEIGHT** | Removable weighted pouch in the lower belly. Deep, even pressure — a hug that stays. Prototype target: Large 3 lb, Small 2 lb (to be tuned in testing). Double-sealed inner pouch, poly pellets, not reachable in normal use, take it out to wash. | כיס משקולת נשלף בבטן התחתונה. לחץ עמוק ואחיד — חיבוק שנשאר. יעד אב-טיפוס: גדול 3 lb, קטן 2 lb. | `--weight` lavender |
| 2 | **WARM & COOL** | Second pocket, separate insert. Chill the reusable gel pack in the fridge, or warm the microwaveable temperature-limited insert (made for plush; no wires, no batteries). Thermal and weighted materials never share a pouch. | כיס שני עם תוסף נפרד: ג׳ל לקירור במקרר, או תוסף לחימום במיקרוגל עם הגבלת טמפרטורה (ללא חוטים וסוללות). | `--warm` coral / `--cool` teal |
| 3 | **TOUCH** | Every animal feels different. Red Panda: curly mane, silky-smooth ears, ribbed paw pads, waffle-knit belly, crinkle tail. Sloth: long-pile fur, smooth face, textured claws, raised-dot belly patch, sherpa inside the arms. Hidden texture patches — nothing looks clinical. | כל חיה מרגישה אחרת: רעמה מתולתלת, אוזניים חלקות, כריות כפות מחורצות, בטן וופל, זנב מרשרש (פנדה); פרווה ארוכה, פנים חלקות, טפרים עם מרקם, כתם נקודות בולט, שרפה בפנים הידיים (עצלן). | `--touch` green |
| 4 | **CALM & FIDGET** | One signature feature per animal. Red Panda: squeezable crinkle tail + ribbed paw pads for thumb-rubbing. Sloth: extra-long hugging arms that wrap around the child and fasten with child-safe hook-and-loop (no magnets). Kids pick the animal by the feel they like. | פיצ׳ר חתימה לכל חיה: זנב לחיץ מרשרש וכריות מחורצות (פנדה); ידיים ארוכות במיוחד שמתחבקות ונסגרות בסקוץ׳ בטיחותי (עצלן). | `--calm` = animal color |

Extra facts you may use: removable inserts → machine-washable outer plush; inserts sold as spares/replacements; the two pockets are separate; "prototype" and "target" wording for weights.

## 3. Positioning and claims (hard rules)
- ALLOWED language: weighted sensory companion · warm & cool comfort insert · multiple tactile textures · designed for sensory exploration and comfort · calming deep-pressure feel · cozy, soothing, grounding.
- FORBIDDEN: any claim that the product treats, helps, relieves or is for autism, ADHD, anxiety, stress disorders, pain, insomnia, sensory processing disorder or any condition; the words "therapy", "therapeutic", "clinical", "medical", "doctor-recommended"; "proven", "scientifically"; sleep claims. Never write "helps with anxiety". (Marketing a children's product with health claims requires substantiation the client does not have.)
- Age / safety line (short form for poster & video): **Ages 3+ · Not for infants · Not a sleep product · Adult supervision with the warm insert**
- Footer disclaimer (poster + explainer): *Not a medical device. Concept prototype — final weights, materials and age grading are subject to third-party safety testing (ASTM F963 / CPSIA) before sale.*
- Brand line: **Sowala · Piga** (small, placeholder — the client will swap in the final brand). Product name on materials: **Weighted Sensory Companions**. Animals are called "Red Panda" and "Sloth" (sizes "Large" / "Small"). Do not invent character names.

## 4. Visual direction
- Mood: warm, cozy, premium-but-playful. Modern kids' brand (think Jellycat / Warmies shelf appeal), NOT a clinical/OT catalog. Real photos of the plush are the heroes — never replace them with cartoon drawings. Icons are simple inline SVG (line or flat), never emoji.
- Palette (define as CSS tokens on :root):
  `--bg:#F7F1E8; --paper:#FFFDF9; --ink:#33251C; --ink-soft:#6B5A4C; --rust:#C8552A; --rust-light:#E8865A; --taupe:#A28E74; --taupe-light:#D9CCB9; --weight:#8F7FC4; --warm:#F0894B; --cool:#4E9DBF; --touch:#7FA86B; --line:#E7DDD0`
- Type: **Fredoka** 600–700 for display, **Nunito** 400/600/700 for body, **Heebo** for Hebrew. Local font CSS: `assets/fonts/fonts.css` (use a relative `<link>` from your HTML). For the published web explainer also add the Google Fonts `<link>` (families Fredoka, Nunito, Heebo) as a fallback.
- Layout craft: generous margins, one dominant hero, clear hierarchy (1 headline, 1 subline, 4 feature callouts, 1 age/safety line, 1 disclaimer, brand). No text overflow, no clipped photos, no orphan words in headlines. Contrast ≥ 4.5:1 for body text.

## 5. Assets (all under /home/user/my-soundboard/sensory-companions/assets/)
- `store-photo.jpg` — original photo, 1932×2576, shop counter background.
- `group-cutout.png` (1545×1708, RGBA) and `group-cutout-1200.png` — all four plush, background removed. Best hero image.
- `redpanda-large.png`, `redpanda-small.png`, `sloth-large.png`, `sloth-small.png` — rough single-animal RGBA crops (they overlap each other; the large red panda is partly hidden behind the small one).
- `redpanda-pair.png`, `sloth-pair.png` — the two red pandas / the two sloths, RGBA.
- `closeups/` JPG texture close-ups: `curly-mane`, `redpanda-face`, `waffle-belly`, `paw-pad`, `paw-pad-2`, `sloth-face`, `sloth-claws`, `sloth-fur`, `sloth-foot`, `sloth-belly-patch`.
- `user-clip.mp4` — the client's 43 s handheld phone clip (464×832 portrait, H.264, has room-noise audio) of the plush in the shop: hands squeezing the red panda's mane and belly, the sloth pair, the small sloth's back face, a hug. `user-clip.webm` — same clip as VP9 (Chromium here cannot decode H.264 — use the .webm in any `<video>` you capture).
- Fonts: `assets/fonts/fonts.css` + woff2 files.
- LOOK at images with the Read tool before using them (you can view PNG/JPG).

## 6. Tooling (scratchpad S = /tmp/claude-0/-home-user-my-soundboard/0bae543d-54b7-5c74-b4f4-c802d116c901/scratchpad)
- Always `export NODE_PATH=/opt/node22/lib/node_modules` before running node scripts that require playwright.
- Screenshot an HTML file: `node $S/tools/shot.js in.html out.png <width> <height> <deviceScaleFactor> <fullPage 0|1>`
- Capture animation frames deterministically: `node $S/tools/frames.js scene.html outdir <fps> <durationSec> [w=1920] [h=1080] [startSec=0]` — it pauses all CSS/Web animations and sets `currentTime`, seeks `<video>` elements (`data-start` = second the video should begin), and calls `window.__seek(t)` if defined. Build scenes as CSS keyframe animations with absolute `animation-delay`s on one timeline (e.g. `animation: fadeUp 0.6s 3.2s both`) — that is fully seekable. Do not rely on JS timers.
- ffmpeg (full static build, libx264/aac/libvpx): `$S/bin/ffmpeg`. Assemble: `$S/bin/ffmpeg -framerate 30 -i frames/frame_%05d.png -i music.wav -c:v libx264 -pix_fmt yuv420p -crf 19 -c:a aac -b:a 160k -shortest out.mp4`
- PDF: write a tiny playwright script using `page.pdf({path, width:'18in', height:'24in', printBackground:true, preferCSSPageSize:false})` after `page.emulateMedia({media:'screen'})`.
- Python 3 with Pillow + numpy is available (`python3`). Use it for image cropping and for synthesizing a music bed (write a WAV with numpy).
- Put intermediates (frames, tests) under `$S/work/<your-task>/`. Put deliverables under `/home/user/my-soundboard/sensory-companions/<poster|video|explainer>/`. Never write thousands of frames into the repo folder.
- Always render and LOOK at your result (Read the PNG) before you report it finished. Check every text box for overflow/clipping, every image for stretching, and read every word for typos and forbidden claims.

## 7. Deliverable specs
### Poster
- Print: 18×24 in portrait. Build `poster.html` at **1350×1800 CSS px**, render with device scale factor 2 → **2700×3600 px PNG** (150 dpi) and a **PDF at 18×24 in**.
- Social: also produce a **1080×1350 px** (4:5) variant of the same design (`poster-social.html` or a media query), rendered at DSF 1 → 1080×1350 PNG.
- Must include: headline, one-line promise, the four functions with short copy, the two animals with sizes/prototype weights, the age/safety line, the disclaimer, brand line. Hero = real cutout photo(s).
### Demo video
- 1920×1080, 30 fps, 45–60 s, H.264 yuv420p, AAC audio (generated soft music bed, −18 dBFS-ish, fade out). English captions burned in. Also a Hebrew-caption version (same scenes, `?lang=he` or a JS constant) if time allows — English first.
- Structure: hook with the client's real footage → "one companion, four kinds of comfort" → one scene per function with an animated diagram (pocket opens, pouch slides in, thermometer warm/cool, texture callouts, hugging arms) → the two animals & sizes → safety/age line → brand end card.
- Use the real footage inside a rounded phone-style frame or as a blurred full-bleed background with the sharp portrait clip centered; never stretch it.
### Visual explainer
- Single-file responsive HTML (`explainer/index.html`), light + dark tokens, phone width 390 px up to desktop, **EN/HE toggle** (`dir="rtl"` + Heebo when Hebrew), all diagrams inline SVG. Images referenced relative to `../assets/...` (they will be attached as supporting files when published).
- Sections: hero · "one companion, four comforts" overview · exploded cutaway diagram (outer plush → belly pocket A weighted pouch → pocket B thermal insert → closures) · per-animal texture map (hotspots on the cutout photo) · how it works in 3 steps (chill/warm → slide in → hug) · sizes & prototype weights table · signature features · safety & positioning (what we say / what we never say) · manufacturing notes (materials, closures, washability, spare inserts) · next steps (prototype → wear test → accredited lab test) · footer disclaimer.

## 8. Quality bar / review checklist (used by verifiers)
1. No forbidden claims (section 3). 2. No text overflow, clipping, overlap, or unreadable contrast. 3. Photos not stretched or drawn-over. 4. Copy matches section 2 facts (weights say "prototype target"). 5. Hebrew renders in Heebo, RTL, with correct punctuation order. 6. Brand line + disclaimer + age line present. 7. Video: captions on screen ≥ 2.5 s each, no scene cut mid-word, audio present, first & last frames clean. 8. Files saved where section 6 says, with the exact names in section 7.

## 9. Client's concept text (verbatim)
> This concept can work very well as a multi-sensory weighted comfort animal, and the four plush animals in your photo are especially suitable because their fur, faces, ears, paws, and body shapes already provide different tactile experiences.
> I'd design each animal around four sensory functions in one toy: weight/deep-pressure input, hot/cold therapy, tactile exploration, and calming/fidget features.
> For the weight, I would avoid making the entire animal permanently heavy. Instead, put a removable weighted pouch in the lower belly/bottom. For roughly a 12–16 inch plush, I'd prototype around 2–3 lb, then test other weights rather than automatically going to 4 lb. Use a securely sealed inner pouch with plastic/poly pellets or another purpose-designed weighting material. The pouch should be inaccessible to the child during normal use and removable so the outer plush can be washed.
> For the hot/cold component, create a second removable pouch that slides into a separate bottom/belly pocket. A reusable gel pack could be chilled for cooling. For warmth, I would strongly favor a microwaveable, temperature-limited insert designed specifically for plush products rather than an electrical heating pad with wires or batteries. Keeping the thermal insert separate from the weighted material makes manufacturing, cleaning, replacement, and safety much easier.
> The most interesting opportunity is making each animal feel completely different. For example, the red panda could have curly textured fur around its head, smooth ears, ribbed paw pads and a crinkly or textured tail. The sloth could have very soft long-pile fur, smoother face material, textured claws and slow-moving/flexible arms. You could also hide tactile patches on the belly, paws or ears—minky, corduroy, satin, sherpa, raised dots, etc.—so a child can explore the animal without it looking like a clinical therapy product.
> I would also add one signature sensory feature per animal. The red panda might have a squeezable tail or textured paw pads; the sloth could have extra-long arms that hug around the child, possibly using child-safe fastening. That gives children a reason to choose an animal based on the sensory input they prefer rather than just appearance.
> One important distinction: I wouldn't market the product as treating autism, anxiety, pain, or another medical condition without appropriate substantiation. Positioning such as "weighted sensory companion," "warm & cool comfort insert," "multiple tactile textures," and "designed for sensory exploration and comfort" is much cleaner. Because this is a children's product involving weight and heated components, you'll also want the final design reviewed against applicable U.S. toy/product safety requirements and have the finished product tested by an appropriate lab.
> For your Sowala/Piga sensory-toy project, I think this is stronger than simply selling a weighted stuffed animal because the removable Weight + Warm/Cool + Touch system gives you three clearly demonstrable features in one product.
