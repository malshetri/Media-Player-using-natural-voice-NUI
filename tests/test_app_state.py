import pytest
from echo_sync.app import parse_wake_word
from echo_sync.interaction.state_machine import AppState, StateMachine

def test_parse_wake_word_only():
    woken, cmd = parse_wake_word("echo", "echo")
    assert woken is True
    assert cmd == ""

def test_parse_wake_word_with_command():
    woken, cmd = parse_wake_word("echo pause", "echo")
    assert woken is True
    assert cmd.lower() == "pause"

    woken, cmd = parse_wake_word("Echo I am tired", "echo")
    assert woken is True
    assert cmd == "I am tired"

def test_parse_wake_word_no_wake_word():
    woken, cmd = parse_wake_word("random speech", "echo")
    assert woken is False
    assert cmd == "random speech"

def test_parse_wake_word_greetings():
    woken, cmd = parse_wake_word("Hey Eko", "echo")
    assert woken is True
    assert cmd == ""

    woken, cmd = parse_wake_word("Hi Echo, play music", "echo")
    assert woken is True
    assert cmd.lower() == "play music"

def test_state_machine_initial_state():
    sm = StateMachine()
    assert sm.state == AppState.SLEEPING
    assert sm.is_passive() is True
    assert sm.is_awake() is False

def test_state_machine_wake():
    sm = StateMachine()
    sm.wake()
    assert sm.state == AppState.AWAKE_WAITING_COMMAND
    assert sm.is_awake() is True

def test_state_machine_clarify():
    sm = StateMachine()
    sm.wake()
    sm.start_clarifying()
    assert sm.state == AppState.AWAKE_CLARIFYING
    assert sm.is_awake() is True

def test_state_machine_play():
    sm = StateMachine()
    sm.wake()
    sm.start_playing_passive()
    assert sm.state == AppState.PLAYING_PASSIVE
    assert sm.is_passive() is True

def test_state_machine_sleep_from_awake():
    sm = StateMachine()
    sm.wake()
    sm.sleep()
    assert sm.state == AppState.SLEEPING
    assert sm.is_passive() is True
