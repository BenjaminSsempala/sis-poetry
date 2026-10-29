# Crane and Dove Poetry

Poetry and Spoken Word lessons for the Crane and Dove class at Stephens International School, hosted free on GitHub Pages:

**https://benjaminssempala.github.io/sis-poetry/**

Open a lesson from the home page. Each lesson is one self contained page, so once it has loaded it keeps working if the internet drops. After the first visit, the whole site also opens with no internet on that computer.

## Add a lesson

1. Finish the lesson as a single HTML file (fonts, pictures and sound inside the file).
2. From this folder, run:

   ```bash
   python3 add_lesson.py "path/to/lesson.html" --id my-lesson --title "My Lesson" --week 9 --dates "2 to 6 Nov" --icon "🎤" --about "One short line for the lesson card"
   ```

   This copies the page into `lessons/my-lesson/`, adds the home button and the offline helper, and adds the lesson to `lessons.json`.
3. Publish:

   ```bash
   git add -A && git commit -m "Add My Lesson" && git push
   ```

   The site updates in a minute or two.

Without the command line: upload the page to a new folder `lessons/<id>/index.html` on GitHub, and add a matching entry to `lessons.json` (copy an existing one). The home button and offline helper will be missing until `add_lesson.py` is run on it.

## Preview on this computer

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## What is in here

- `index.html`: the home page (lesson cards, newest first)
- `lessons.json`: the list of lessons the home page shows
- `lessons/`: one folder per lesson
- `sw.js` and `manifest.webmanifest`: offline use and Install as an app
- `assets/`: school logo, icons and font
- `add_lesson.py`: adds or updates a lesson

All lesson words are original or used with permission. The site is public but kept out of search engines.
