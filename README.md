# Mini Game Jam Workshop — Assets (CDN)

This public repo is the CDN for student-made workshop assets. The deployed game
fetches every file here at runtime via `raw.githubusercontent.com`, with a
`?v=<timestamp>` cache-buster, so **overwriting a file and pushing updates the
live game on the next page reload** — no rebuild.

Managed by the push script in the game repo (`tools/push-assets.ps1`). Do not
add, rename, or remove files: the set of slots is frozen; only the bytes behind
a slot change.

**Never put student names in filenames or commit messages — this repo is public.**

## Slots

| Slot file | Type | Role in game |
|---|---|---|
| `audio/music.mp3` | music (MP3) | Background music, looped |
| `audio/player_steps.mp3` | SFX (MP3) | Player footsteps |
| `sprites/player_idle.png` | sprite (PNG, 32 px/unit, center pivot) | Player idle frame (`Player/Idle_0`) |
| `sprites/player_walk.png` | sprite (PNG, 32 px/unit, center pivot) | Player walk frame (`Player/Walk_0`) |

Audio is always MP3 (the push script transcodes whatever students export).
Reverting a bad upload = `git revert` the commit.
