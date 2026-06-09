# Three Modalities

Echo-Sync implements three distinct interaction modalities to cover the full range of user needs.

---

## Modality 1 — Direct Control

**User context:** The user knows exactly what they want.

**Function:** Immediate media control.

**Complexity:** Low.

**Example Dialogue:**
```
User: "Play jazz."
System: [success earcon] "Playing jazz."

User: "Pause."
System: [success earcon] "Music paused."

User: "Turn it up."
System: [success earcon] "Volume increased to 90 percent."
```

**Accessibility Benefit:** Provides a fast, predictable interaction pattern that blind users can memorize and rely on. No ambiguity, no delay.

**Implementation:** Rule-based pattern matching handles common commands before the AI is called, ensuring speed and reliability.

---

## Modality 2 — Context-Based / Affective Request

**User context:** The user expresses a mood, energy level, or situation but does not know exactly what music to play.

**Function:** Interpret the user's wording and map it to an appropriate music category.

**Complexity:** Medium.

**Example Dialogue:**
```
User: "I am exhausted."
System: [mood earcon] "I'll play something calm and relaxing for you."

User: "I need energy."
System: [mood earcon] "Playing energetic music to boost your energy!"

User: "I want to study."
System: [mood earcon] "Playing ambient music to help you focus."
```

**Accessibility Benefit:** Users don't need to know their music library. They express how they feel, and the system finds appropriate music. This is especially valuable for users who cannot browse visual playlists.

**Implementation:** The AI classifier identifies mood/context keywords and maps them to predefined music categories (calm, energy, focus, happy, sad).

> **Important:** We use the term "interpreted context" instead of "detected emotion." The system interprets user wording — it does not perform medical or psychological emotion detection.

---

## Modality 3 — Guided Help and Error Handling

**User context:** New user, uncertain user, silence, unclear speech, or off-topic request.

**Function:** Guide the user, provide clarification, or politely reject inappropriate requests.

**Complexity:** High.

**Example Dialogue:**
```
User: "What is the weather?"
System: "I'm only specialized in music. You can say: play jazz, pause, or play something relaxing."

User: [silence for 10 seconds]
System: "I'm still here. Do you need help? You can say: play something calm."

User: "Blarghhh" [unclear speech]
System: "I didn't quite catch that. You can say: play, pause, next song, or tell me how you feel."

User: "What can I say?"
System: "You can say: play, pause, next song, volume up, or tell me how you feel and I'll find the right music."
```

**Accessibility Benefit:** Blind users cannot see help text or UI hints. Progressive audio guidance ensures they can always discover available features. Error handling is gentle, never blaming the user.

**Implementation:** Uses progressive help (responses get more detailed with repeated requests), silence timeout detection, and AI-based off-topic filtering.
