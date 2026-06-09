# Test Plan

## Test Cases

| ID | Input | Expected Output | Category | Status |
|---|---|---|---|---|
| T01 | "Play jazz" | direct_command → play jazz | Direct Control | ⬜ |
| T02 | "Pause" | direct_command → pause | Direct Control | ⬜ |
| T03 | "Continue" | direct_command → resume | Direct Control | ⬜ |
| T04 | "Next song" | direct_command → next | Direct Control | ⬜ |
| T05 | "Previous song" | direct_command → previous | Direct Control | ⬜ |
| T06 | "Make it louder" | direct_command → volume up | Direct Control | ⬜ |
| T07 | "Lower the volume" | direct_command → volume down | Direct Control | ⬜ |
| T08 | "I am tired" | context_request → calm | Context/Mood | ⬜ |
| T09 | "I feel sad" | context_request → sad/soft music | Context/Mood | ⬜ |
| T10 | "I need energy" | context_request → energy | Context/Mood | ⬜ |
| T11 | "I want to focus" | context_request → focus | Context/Mood | ⬜ |
| T12 | "I am happy today" | context_request → happy | Context/Mood | ⬜ |
| T13 | "What can I say?" | help_request → examples | Guided Help | ⬜ |
| T14 | "Help me" | help_request → examples | Guided Help | ⬜ |
| T15 | "What is the weather?" | off_topic → polite rejection | Off-Topic | ⬜ |
| T16 | "What is 2+2?" | off_topic → polite rejection | Off-Topic | ⬜ |
| T17 | Silence 10 seconds | unclear → guided help | Error Handling | ⬜ |
| T18 | Unrecognized noise | unclear → clarification | Error Handling | ⬜ |
| T19 | "Play something" | unclear/context unknown → fallback | Edge Case | ⬜ |
| T20 | "Stop music" | direct_command → stop | Direct Control | ⬜ |
| T21 | "Volume up" | direct_command → volume_up | Direct Control | ⬜ |
| T22 | "Resume" | direct_command → resume | Direct Control | ⬜ |
| T23 | "I'm exhausted" | context_request → calm | Context/Mood | ⬜ |
| T24 | "Play something relaxing" | direct_command → play | Context/Edge | ⬜ |
| T25 | Empty string | unclear → clarify | Edge Case | ⬜ |

## Test Categories

### Direct Control (T01-T07, T20-T22, T24)
Tests basic media control commands handled by rule-based matching.

### Context/Mood (T08-T12, T23)
Tests AI-powered mood/context interpretation and playlist mapping.

### Guided Help (T13-T14)
Tests help request handling and progressive help.

### Off-Topic (T15-T16)
Tests polite rejection of non-music queries.

### Error Handling (T17-T18)
Tests silence timeout and unclear speech handling.

### Edge Cases (T19, T25)
Tests ambiguous or empty inputs.

## Automated Test Execution

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_intent_classifier.py -v

# Run with coverage
pytest tests/ --cov=echo_sync --cov-report=html
```

## Test Results

| Date | Tests Run | Passed | Failed | Notes |
|---|---:|---:|---:|---|
| [Fill in] | [Count] | [Count] | [Count] | [Notes] |
