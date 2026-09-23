# Sowala — Weighted Sensory Companions

חומרי שיווק והסבר למוצר **Sowala**: בובות חושיות משוקללות (עצלן ופנדה אדומה, שני גדלים) עם כיס משקולת נשלף, תוסף חימום/קירור נשלף, ומפת מרקמים למגע. נבנה עבור מרכז לילדים על הספקטרום האוטיסטי שמוכר להורים.

Marketing and explainer materials for **Sowala**, a weighted sensory companion concept (sloth + red panda, two sizes each) with a removable weighted pouch, a removable warm/cool insert and a map of tactile textures. Built for a center for children on the autism spectrum that sells to parents.

## What is here / מה יש כאן

| Folder | Contents |
|--------|----------|
| `poster/A`, `poster/B`, `poster/C`, `poster/C2` | Four finished poster variants for the client to choose from. Each folder has `poster-X-18x24.png` (2700×3600, print), `poster-X-18x24.pdf`, `poster-X-social-1080x1350.png` (Instagram / WhatsApp 4:5) and the HTML sources |
| `video/` | `demo-en.mp4` (1920×1080, 30 fps, 59.5 s, English captions, synthesized music bed), `contact-sheet-en.png`, `storyboard.md`, `scenes/` (HTML/CSS sources of every scene), `music.py` |
| `explainer/` | `index.html` — the visual explainer (English, light/dark): story, the four comforts, belly cutaway, texture maps, how it works, sizes, market context, safety & positioning with sources, manufacturing notes, next steps |
| `assets/` | original shop photo, background-removed cutouts, texture close-ups, the shop clip (mp4 + webm), fonts |
| `BRIEF.md` | the creative + technical brief every deliverable follows (copy, claims rules, palette, specs) |

## How the pieces were made / איך זה נבנה

- Every visual is HTML/CSS/SVG rendered with headless Chromium (Playwright). The poster is one HTML page rendered at 2× to 2700×3600 px; the video is a set of seekable CSS-animated scenes captured frame by frame and assembled with ffmpeg; the music bed is synthesized.
- The plush photos are the client's real photos, cut out with an open-source segmentation model. Nothing is drawn over them.
- Copy follows the claims rules in `BRIEF.md` section 3: we name the audience and tell the true origin story, but never promise a health outcome.

## Editing / עריכה

- Poster copy and layout: edit `poster/poster.html`, then re-render (see the commands in `BRIEF.md` section 6).
- Video captions: edit the scene HTML files in `video/scenes/`, re-capture the frames with the frame tool described in `BRIEF.md` section 6 and re-encode with ffmpeg (`storyboard.md` lists every scene and timing).
- Explainer: edit `explainer/index.html` (single file, inline CSS/SVG; images under `assets/`).
