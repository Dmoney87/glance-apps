# Uncrustables line as a Glance private app

The panel can't play the GIF. Glance private apps show **one still PNG** (max
192x32) and re-fetch it at the refresh interval you set in Glance Setup, and
GDN apps are still frames too (animation is "not yet" per the Glance FAQ). So
this folder turns the GIF into the closest thing that works: a tiny server that
hands the panel the **next keyframe on every refresh**. The line advances one
beat per refresh and loops every 10 beats. The keyframes are pulled straight
out of `uncrustables-line.gif`, so they look exactly like the GIF.

| beat | keyframe | shows |
|---|---|---|
| 0 | k00 | empty breads waiting on the belt |
| 1 | k01 | PB bar #1 down, squirting |
| 2 | k02 | PB #1 done, bar retracting |
| 3 | k03 | jelly bar down, squirting |
| 4 | k04 | jelly done, bar gone |
| 5 | k05 | PB bar #2 down, squirting |
| 6 | k06 | PB #2 done, bar retracting |
| 7 | k07 | lids dropping on |
| 8 | k08 | finished row + crimp sparkle |
| 9 | k09 | batch rides the belt off the front edge |

## Deploy to Cloudflare Pages (free, nothing to keep running)

1. Sign in at https://dash.cloudflare.com, then **Workers & Pages → Create → Pages → Upload assets**.
2. Name the project (for example `uncrustables-line`) and drag **this `worker` folder** in. `_worker.js` is the whole app; the `frames/` PNGs are just there for reference and `serve.py`.
3. Cloudflare gives you a URL like `https://uncrustables-line.pages.dev/`. Open `https://uncrustables-line.pages.dev/preview` in a browser to see all ten keyframes and the live one.

Or from a terminal, from this folder:

```bash
npx wrangler login
npx wrangler pages deploy . --project-name uncrustables-line
```

Re-deploy the same way whenever the GIF changes (run `build_worker.py` first).

## Add it to the Glance

1. Glance Setup app → **Apps** → **Private Apps** tab → **+**.
2. Image URL: `http://uncrustables-line.pages.dev/` (your project's URL).
3. Refresh interval: **60 seconds**. This must equal `STEP` in `_worker.js` (60), or the beats won't line up. If Glance Setup won't accept 60, pick the smallest it allows and change `STEP` to match, then re-deploy.
4. Width 192, height 32.

## Testing in a browser

- `/` is the live frame for right now.
- `/?frame=4` forces keyframe 4 (0–9).
- `/?step=120` plays one beat every 2 minutes instead (for a slower refresh).
- `/preview` shows every keyframe scaled up.

## Run it locally instead (Raspberry Pi, or a Mac that stays on)

```bash
python3 ../serve.py            # http://<this machine's LAN ip>:8787/
```

Paste that `http://<ip>:8787/` URL into Glance Setup with the same 60 s refresh. Only the standard library is needed. The machine has to stay awake and on the same network as the Glance.

## Regenerate after changing the GIF

```bash
"../../../glance-dev-network/.venv/bin/python" ../build_worker.py            # uses ../../uncrustables-line.gif
```

`KEYFRAMES` at the top of `build_worker.py` lists which GIF frame each beat uses; change the indices there to pick different moments or add beats.
