# Test Plan

## Test Cases

| ID | Input | Expected Output | Category | Status |
|---|---|---|---|---|
| T01 | "Play jazz" | direct_command → play jazz | Direct Control | ✅ |
| T02 | "Pause" | direct_command → pause | Direct Control | ✅ |
| T03 | "Continue" | direct_command → resume | Direct Control | ✅ |
| T04 | "Next song" | direct_command → next | Direct Control | ✅ |
| T05 | "Previous song" | direct_command → previous | Direct Control | ✅ |
| T06 | "Make it louder" | direct_command → volume up | Direct Control | ✅ |
| T07 | "Lower the volume" | direct_command → volume down | Direct Control | ✅ |
| T08 | "I am tired" | context_request → calm | Context/Mood | ✅ |
| T09 | "I feel sad" | context_request → sad/soft music | Context/Mood | ✅ |
| T10 | "I need energy" | context_request → energy | Context/Mood | ✅ |
| T11 | "I want to focus" | context_request → focus | Context/Mood | ✅ |
| T12 | "I am happy today" | context_request → happy | Context/Mood | ✅ |
| T13 | "What can I say?" | help_request → examples | Guided Help | ✅ |
| T14 | "Help me" | help_request → examples | Guided Help | ✅ |
| T15 | "What is the weather?" | off_topic → polite rejection | Off-Topic | ✅ |
| T16 | "What is 2+2?" | off_topic → polite rejection | Off-Topic | ✅ |
| T17 | Silence 10 seconds | unclear → guided help | Error Handling | ✅ |
| T18 | Unrecognized noise | unclear → clarification | Error Handling | ✅ |
| T19 | "Play something" | direct_command → play | Edge Case | ✅ |
| T20 | "Stop music" | direct_command → stop | Direct Control | ✅ |
| T21 | "Volume up" | direct_command → volume_up | Direct Control | ✅ |
| T22 | "Resume" | direct_command → resume | Direct Control | ✅ |
| T23 | "I'm exhausted" | context_request → calm | Context/Mood | ✅ |
| T24 | "Play something relaxing" | context_request → calm playlist | Context/Mood | ✅ |
| T25 | Empty string | unclear → clarify | Edge Case | ✅ |
| T26 | "Play calm music" | context_request → calm playlist | Playlist Command | ✅ |
| T27 | "Play focus music" | context_request → focus playlist | Playlist Command | ✅ |
| T28 | "I don't know" | help_request → help | Guided Help | ✅ |
| T29 | "Who is the president?" | off_topic → reject | Off-Topic | ✅ |
| T30 | "Tell me about dogs" | off_topic → reject | Off-Topic | ✅ |

## Test Categories

### Direct Control (T01-T07, T20-T22)
Tests basic media control commands handled by rule-based matching.

### Context/Mood (T08-T12, T23-T24)
Tests mood/context interpretation and playlist mapping — now handled by rule-based matching for reliability.

### Playlist Commands (T26-T27)
Tests "play \<keyword\> music" patterns that directly select the right playlist.

### Guided Help (T13-T14, T28)
Tests help request handling, progressive help, and "I don't know" responses.

### Off-Topic (T15-T16, T29-T30)
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
pytest tests/test_demo_routing.py -v
pytest tests/test_ducking.py -v

# Run with coverage
pytest tests/ --cov=echo_sync --cov-report=html
```

## Test Results

| Date | Tests Run | Passed | Failed | Notes |
|---|---:|---:|---:|---|
| 2026-06-13 | 121 | 121 | 0 | All rule-based, ducking, routing, help, safety, playlist, and context tests pass |

## Test File Inventory

| File | Tests | What it covers |
|---|---:|---|
| `test_intent_classifier.py` | 21 | Rule-based + schema validation |
| `test_demo_routing.py` | 47 | Demo flow, playlist cmds, context, off-topic, help |
| `test_ducking.py` | 8 | Smart ducking safety and idempotency |
| `test_guided_help.py` | 11 | Silence, unclear, help, off-topic responses |
| `test_context_mapper.py` | 11 | Context-to-folder mapping |
| `test_playlist_manager.py` | 13 | Playlist scanning and selection |
| `test_safety_filter.py` | 10 | AI output validation |
