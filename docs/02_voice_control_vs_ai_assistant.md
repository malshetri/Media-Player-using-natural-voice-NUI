# Voice Control vs. AI Assistant

## Voice Control

Voice Control handles **direct, predictable commands** for media playback. These are simple, rule-based interactions that execute immediately.

### Characteristics
- **Low complexity**: One command → one action
- **High reliability**: Rule-based matching, no AI needed
- **Fast response**: No API call required
- **Predictable**: Same input always produces same output

### Examples
| User Says | System Action |
|---|---|
| "Play" | Start playback |
| "Pause" | Pause playback |
| "Next song" | Skip to next track |
| "Volume up" | Increase volume by 10% |
| "Stop" | Stop playback |

## AI Assistant

The AI Assistant handles **complex, ambiguous, or context-based requests** that require natural language understanding.

### Characteristics
- **Medium-high complexity**: Requires interpretation
- **Flexible**: Handles varied phrasing and context
- **Context-aware**: Maps user wording to music categories
- **Bounded**: Only responds to music-related topics

### Examples
| User Says | Interpretation | Action |
|---|---|---|
| "I am exhausted" | Interpreted context: calm | Plays calm music |
| "I need energy" | Interpreted context: energy | Plays energetic music |
| "What is the weather?" | Off-topic detection | Polite rejection |
| "What can I say?" | Help request | Lists available commands |

## How Both Work Together

```
User speaks
    │
    ├── Rule-based check (fast path)
    │   ├── Match found → Execute direct command
    │   └── No match → Continue to AI
    │
    └── AI Intent Classifier
        ├── direct_command → Execute media command
        ├── context_request → Map mood → Select playlist
        ├── help_request → Provide guided help
        ├── off_topic → Polite rejection
        └── unclear → Ask for clarification
```

The system first tries **rule-based matching** for common commands (play, pause, stop, etc.). This makes simple commands fast and reliable without depending on the AI. Only when the input doesn't match a known command does the system call the **AI classifier** for flexible interpretation.

This dual approach provides both speed and flexibility.
