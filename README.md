# glance-apps

Pixel-art for a Glance SCROLL LED panel (192x32), served as private apps.

| App | File | Raw URL |
|---|---|---|
| Uncrustables assembly line (GIF, reference only) | uncrustables-line.gif | https://raw.githubusercontent.com/Dmoney87/glance-apps/main/uncrustables-line.gif |

## Uncrustables line as a working private app

The Glance can't play the GIF: private apps show one still PNG and re-fetch it
on a refresh interval. `uncrustables-line/` holds a tiny server that hands the
panel the next keyframe on every refresh, so the line advances one beat per
refresh and loops every 10 beats. See
[`uncrustables-line/worker/README.md`](uncrustables-line/worker/README.md) for
the Cloudflare deploy and Glance Setup steps.

- `uncrustables-line/worker/` — the Cloudflare Worker (`_worker.js` + `wrangler.toml` + reference `frames/`), live at http://uncrustables-line.87dustinsmith.workers.dev/ (the Glance needs plain http, which workers.dev serves and Pages does not)
- `uncrustables-line/serve.py` — same thing on a Mac or Raspberry Pi over the LAN
- `uncrustables-line/build_worker.py` — regenerates the keyframes and worker from `uncrustables-line.gif`
