# Mini Game Jam Workshop — Assets (CDN)

This public repo is the CDN for student-made workshop assets. The deployed game
fetches every file here at runtime via `raw.githubusercontent.com`, with a
`?v=<timestamp>` cache-buster, so **overwriting a file and pushing updates the
live game on the next page reload** — no rebuild.

Managed by the push script in the game repo (`tools/push-assets.ps1`). Keep this
list, the push script's slot map, and the `RemoteAssetLoader` component in the
game in sync. Only the bytes behind a slot change; the set of slots is frozen.

**Never put student names in filenames or commit messages — this repo is public.**

## Layout — mirrors the game's `Assets/Resources/` folders

The game fetches each file from the exact path below (case-sensitive). Files must
sit in the matching folder, and the folder names mirror the game's `Resources/`:

- `Audio/` — MP3.
- `Bilder/Spieler/` — PNG, 256 px/unit, centre pivot. Feed the `Spieler` SpriteLibrary category.
- `Bilder/Partikel/` — PNG. Particle material `_BaseMap`.
- `Bilder/Spuren/` — PNG. Trail material `_BaseMap`.
- `Bilder/Linien/` — PNG. Aim-line material `_BaseMap`.

> ⚠️ **A file in the wrong folder or with a different name/case is invisible to
> the game — it 404s and the baked dummy is used instead.**
> `raw.githubusercontent.com` is case-sensitive: `Audio/`, `Bilder/`, and every
> filename must match capitalisation exactly (`Spieler_Stehen-1.png`, not
> `spieler_stehen-1.png`).

## Slots

### Audio (`Audio/`, MP3)
| Slot file | Role in game |
|---|---|
| `Audio/Musik.mp3` | Background music, looped |
| `Audio/Spieler-Laufen.mp3` | Player footsteps |

### Player sprites (`Bilder/Spieler/`, PNG, 256 px/unit, centre pivot) — SpriteLibrary category `Spieler`
| Slot file | Library label |
|---|---|
| `Bilder/Spieler/Spieler_Stehen-1.png` | `Stehen-1` (idle) |
| `Bilder/Spieler/Spieler_Stehen-2.png` | `Stehen-2` (idle) |
| `Bilder/Spieler/Spieler_Laufen-1.png` | `Laufen-1` (run) |
| `Bilder/Spieler/Spieler_Laufen-2.png` | `Laufen-2` (run) |
| `Bilder/Spieler/Spieler_Springen-1.png` | `Springen-1` (jump) |
| `Bilder/Spieler/Spieler_Springen-2.png` | `Springen-2` (jump) |
| `Bilder/Spieler/Spieler_Springen-3.png` | `Springen-3` (jump) |
| `Bilder/Spieler/Spieler_Projektil.png` | `Projektil` |

### Effect textures (`Bilder/{Partikel,Spuren,Linien}/`, PNG → material `_BaseMap`)
| Slot file | Effect material |
|---|---|
| `Bilder/Partikel/Partikel_Laufen.png` | RunParticles |
| `Bilder/Partikel/Partikel_Springen.png` | JumpParticles |
| `Bilder/Partikel/Partikel_Landen.png` | LandingParticles |
| `Bilder/Partikel/Partikel_Werfen.png` | ThrowParticles |
| `Bilder/Partikel/Partikel_Projektil.png` | ProjectileParticles |
| `Bilder/Spuren/Spur_Laufen.png` | PlayerTrail |
| `Bilder/Spuren/Spur_Projektil.png` | ProjectileTrail |
| `Bilder/Linien/Linie_Zielen.png` | AimLine |

Audio is always MP3 (the push script transcodes whatever students export).
Reverting a bad upload = `git revert` the commit.
