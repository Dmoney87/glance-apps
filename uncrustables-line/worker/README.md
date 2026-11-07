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

## Deploy as a Cloudflare Worker (free, nothing to keep running)

The Glance can only load **plain `http://`** URLs. `workers.dev` serves plain
http, so the worker lives there. (Cloudflare Pages forces a redirect to https
and the Glance rejects it with "Image verification failed".)

From this folder (first time: `npx wrangler login`):

```bash
npx wrangler deploy
```

`wrangler.toml` names the worker `uncrustables-line`, so it deploys to
`http://uncrustables-line.<your-subdomain>.workers.dev/`. The one deployed on
2026-11-07 is:

    http://uncrustables-line.87dustinsmith.workers.dev/

Open `http://uncrustables-line.87dustinsmith.workers.dev/preview` in a browser
to see all ten keyframes and the live one. Re-run `npx wrangler deploy`
whenever the GIF changes (run `build_worker.py` first).

## Add it to the Glance

1. Glance Setup app → **Apps** → **Private Apps** tab → **+**.
2. Image URL: `http://uncrustables-line.87dustinsmith.workers.dev/` (must start with `http://`, not `https://`).
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
