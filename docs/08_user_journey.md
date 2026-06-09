# User Journey Maps

## Journey 1: Blind User Wants to Play Music

| Step | User Action | System Response | Earcon |
|---|---|---|---|
| 1 | Launches Echo-Sync | Welcome message with available commands | listening |
| 2 | "Play jazz" | "Playing jazz." | success |
| 3 | Music plays | Continuous playback | — |
| 4 | "Turn it up" | "Volume increased to 90 percent." | success |
| 5 | "Next song" | "Playing next song." | success |
| 6 | "Stop" | "Music stopped." | success |

**Pain points addressed:** No screen needed, clear audio confirmation, predictable commands.

---

## Journey 2: Tired User Doesn't Know What to Play

| Step | User Action | System Response | Earcon |
|---|---|---|---|
| 1 | System is listening | — | listening |
| 2 | "I'm really tired today" | "I'll play something calm and relaxing for you." | mood_detected |
| 3 | Calm music starts playing | Continuous playback | — |
| 4 | "Actually, I need to study" | "Playing ambient music to help you focus." | mood_detected |
| 5 | Focus music starts playing | Playlist switches | — |

**Pain points addressed:** User doesn't need to know music library, natural expression works.

---

## Journey 3: New User Doesn't Know Commands

| Step | User Action | System Response | Earcon |
|---|---|---|---|
| 1 | Launches Echo-Sync | Welcome message with examples | listening |
| 2 | "What can I say?" | "You can say: play, pause, next song, volume up, or tell me how you feel." | help |
| 3 | "Help me" | "Available commands: play, pause, resume, stop, next, previous, volume up, down." | help |
| 4 | "Play" | "Playing music." | success |

**Pain points addressed:** Progressive help, no need to read documentation.

---

## Journey 4: Off-Topic Request

| Step | User Action | System Response | Earcon |
|---|---|---|---|
| 1 | Music is playing | — | — |
| 2 | "What is the weather?" | "I'm only specialized in music. You can say: play jazz, pause, or play something relaxing." | error |
| 3 | "What is 2+2?" | "I can only help with music. Would you like me to play something calm, energetic, or focused?" | error |
| 4 | "Play something energetic" | "Playing energetic music to boost your energy!" | mood_detected |

**Pain points addressed:** Clear boundaries, no confusing off-topic answers, gentle redirection.

---

## Journey 5: Error / Silence Case

| Step | User Action | System Response | Earcon |
|---|---|---|---|
| 1 | System is listening | — | listening |
| 2 | [silence for 10 seconds] | "I'm still here. Do you need help? You can say: play something calm." | help |
| 3 | [more silence] | "Take your time. When you're ready, just say: play something calm." | help |
| 4 | [unclear speech] | "I didn't quite catch that. You can say: play, pause, next song, or tell me how you feel." | help |
| 5 | "Play" | "Playing music." | success |

**Pain points addressed:** No dead silence, progressive guidance, patient interaction.
