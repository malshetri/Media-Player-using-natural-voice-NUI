# Interaction Flow

## Main Interaction Flow Diagram

```mermaid
flowchart TD
    Start([System Start]) --> Welcome[Play welcome message]
    Welcome --> Listen[Listen for speech]
    Listen --> HasSpeech{Speech detected?}
    
    HasSpeech -->|No - Timeout| Silence[Handle silence]
    Silence --> SilenceResponse[Provide guided help]
    SilenceResponse --> Listen
    
    HasSpeech -->|Yes| Transcribe[Transcribe speech]
    Transcribe --> TranscribeOK{Transcription OK?}
    
    TranscribeOK -->|No| STTFail[Handle STT failure]
    STTFail --> Listen
    
    TranscribeOK -->|Yes| RuleCheck{Rule-based match?}
    
    RuleCheck -->|Yes| DirectExec[Execute direct command]
    DirectExec --> SuccessEarcon[Play success earcon]
    SuccessEarcon --> Listen
    
    RuleCheck -->|No| AIClassify[AI Intent Classification]
    AIClassify --> IntentType{Intent type?}
    
    IntentType -->|direct_command| DirectExec
    IntentType -->|context_request| ContextMap[Map context to playlist]
    IntentType -->|help_request| Help[Provide help]
    IntentType -->|unclear| Clarify[Ask for clarification]
    IntentType -->|off_topic| Reject[Polite rejection]
    
    ContextMap --> LoadPlaylist[Load playlist]
    LoadPlaylist --> PlayMusic[Play music]
    PlayMusic --> MoodEarcon[Play mood earcon]
    MoodEarcon --> Listen
    
    Help --> HelpEarcon[Play help earcon]
    HelpEarcon --> Listen
    
    Clarify --> HelpEarcon
    Reject --> ErrorEarcon[Play error earcon]
    ErrorEarcon --> Listen
```

## Decision Points

### 1. Direct Command?
- **Input matches rule-based pattern** → Execute immediately (fast path)
- **Input does not match** → Send to AI classifier

### 2. Context Request?
- **AI identifies mood/context** → Map to music category → Load playlist
- **Unknown context** → Use fallback playlist

### 3. Help Request?
- **Explicit help request** → Provide progressive help
- **First time** → General overview
- **Repeated** → More specific commands and moods

### 4. Off-Topic?
- **Non-music question** → Polite rejection with examples
- **Alternate gentle/firm** → Prevent frustration

### 5. Low Confidence?
- **AI confidence < 0.6** → Override to 'unclear' → Ask clarification
- **Safety filter catches** → Prevents wrong actions

### 6. Silence?
- **No speech for 10 seconds** → Progressive guidance
- **First silence** → Basic help
- **Repeated silence** → More detailed help
- **User takes time** → Patient encouragement

## Smart Ducking Flow

```mermaid
sequenceDiagram
    participant Music as Music Playback
    participant Ducker as Smart Ducker
    participant User as User Speech
    
    Note over Music: Playing at 80% volume
    User->>Ducker: Speech starts
    Ducker->>Music: Reduce to 30%
    Note over Music: Playing at 30% volume
    User->>Ducker: Speech ends
    Note over Ducker: Processing...
    Ducker->>Music: Fade to 80% over 1.5s
    Note over Music: Playing at 80% volume
```
