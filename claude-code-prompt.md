# Claude Code Prompt: Deploy Skyland Haven Guest Guide to GitHub Pages

## What I Need

I have a single `index.html` file that is a complete static website for my Airbnb property guest guide. I need you to:

1. Create a new GitHub repository called `skyland-haven`
2. Initialize it, commit the `index.html` file, and push to GitHub
3. Enable GitHub Pages so it's live at `https://justin-pitt.github.io/skyland-haven/`

## My GitHub

- GitHub username: `justin-pitt`
- GitHub: `github.com/justin-pitt`
- I should already be authenticated via `gh` CLI or git credentials

## The File

The `index.html` file is located at: `./index.html` (in my current working directory)

It's a single self-contained HTML file — no dependencies, no build step, no npm. Just static HTML/CSS/JS. It includes:

- A property manual for my Airbnb (Skyland Haven, Woodfin NC)
- A hot tub guide (AquaRest AR-600)
- A QR code generator page with printable signs
- All fonts loaded from Google Fonts CDN
- Zero external JS libraries — the QR code generator is pure vanilla JS

## Steps

1. **Create the repo on GitHub:**
   ```
   gh repo create skyland-haven --public --description "Skyland Haven Airbnb Guest Guide" --clone
   ```

2. **Copy `index.html` into the repo folder**

3. **Add a simple `README.md`:**
   ```markdown
   # Skyland Haven · Guest Guide

   Static guest guide for [Skyland Haven](https://www.airbnb.com/rooms/907933203969939408) — an Airbnb in Woodfin, NC near Asheville.

   **Live site:** https://justin-pitt.github.io/skyland-haven/

   ## What's Included
   - Property manual (WiFi, check-in/out, house rules, local spots, emergency contacts)
   - Hot tub guide (AquaRest AR-600 — controls, heating modes, troubleshooting)
   - QR code generator + printable signs for the property

   ## Hosting
   Hosted via GitHub Pages. Single `index.html` file, no build step.
   ```

4. **Commit and push:**
   ```
   git add .
   git commit -m "Initial commit: Skyland Haven guest guide"
   git push -u origin main
   ```

5. **Enable GitHub Pages:**
   ```
   gh api repos/justin-pitt/skyland-haven/pages -X POST -f source.branch=main -f source.path="/"
   ```
   If that errors because Pages is already enabled or needs a different approach, try:
   ```
   gh repo edit skyland-haven --enable-pages --pages-branch main --pages-path /
   ```

6. **Verify it's live** by checking: `https://justin-pitt.github.io/skyland-haven/`

## Important Notes

- The repo should be **public** (GitHub Pages requires public for free accounts unless I have Pro)
- Deploy from the **main** branch, root `/` directory
- There is NO build process — no Jekyll, no npm, no static site generator. Just serve the raw HTML file.
- Add a `.nojekyll` empty file to the repo root so GitHub doesn't try to process it through Jekyll
- If the `gh` CLI isn't available, fall back to using `git` commands and create the repo through the GitHub API with `curl`

## After Deployment

Once the site is live, tell me:
1. The live URL
2. Confirm the QR code page works (it auto-generates QR codes pointing to the live URL, but guests will need to update the base URL field on the QR Codes tab to match the actual deployed URL)

That's it — single file, no build, just push and serve.
