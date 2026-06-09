"""
Echo-Sync state machine.

Tracks the application state for the interaction flow.
States: idle, listening, processing, playing, ducking, helping.
"""

import logging
from enum import Enum, auto
from typing import Optional

logger = logging.getLogger(__name__)


class AppState(Enum):
    """Application states for the Echo-Sync interaction loop."""

    IDLE = auto()           # System is waiting, not actively listening
    LISTENING = auto()      # Microphone is recording user speech
    PROCESSING = auto()     # Transcribing and classifying intent
    EXECUTING = auto()      # Executing the classified action
    PLAYING = auto()        # Music is playing, system is passive
    DUCKING = auto()        # Music volume reduced for speech
    HELPING = auto()        # System is providing guided help
    ERROR = auto()          # An error occurred
    SHUTTING_DOWN = auto()  # System is shutting down


# ── Valid state transitions ─────────────────────────────────────────────────
VALID_TRANSITIONS: dict[AppState, set[AppState]] = {
    AppState.IDLE: {AppState.LISTENING, AppState.SHUTTING_DOWN},
    AppState.LISTENING: {
        AppState.PROCESSING,
        AppState.HELPING,      # Silence timeout
        AppState.ERROR,
        AppState.SHUTTING_DOWN,
    },
    AppState.PROCESSING: {
        AppState.EXECUTING,
        AppState.HELPING,
        AppState.ERROR,
        AppState.SHUTTING_DOWN,
    },
    AppState.EXECUTING: {
        AppState.PLAYING,
        AppState.IDLE,
        AppState.HELPING,
        AppState.ERROR,
        AppState.SHUTTING_DOWN,
    },
    AppState.PLAYING: {
        AppState.LISTENING,
        AppState.DUCKING,
        AppState.IDLE,
        AppState.SHUTTING_DOWN,
    },
    AppState.DUCKING: {
        AppState.LISTENING,
        AppState.PLAYING,
        AppState.SHUTTING_DOWN,
    },
    AppState.HELPING: {
        AppState.LISTENING,
        AppState.IDLE,
        AppState.SHUTTING_DOWN,
    },
    AppState.ERROR: {
        AppState.LISTENING,
        AppState.IDLE,
        AppState.SHUTTING_DOWN,
    },
    AppState.SHUTTING_DOWN: set(),  # Terminal state
}


class StateMachine:
    """
    Simple state machine for tracking Echo-Sync application state.

    Enforces valid state transitions and provides logging.
    """

    def __init__(self, initial_state: AppState = AppState.IDLE) -> None:
        self._state = initial_state
        self._previous_state: Optional[AppState] = None
        logger.info("State machine initialized: %s", self._state.name)

    @property
    def state(self) -> AppState:
        """Current application state."""
        return self._state

    @property
    def previous_state(self) -> Optional[AppState]:
        """Previous application state."""
        return self._previous_state

    def transition(self, new_state: AppState) -> bool:
        """
        Attempt to transition to a new state.

        Args:
            new_state: The target state.

        Returns:
            True if the transition was valid and executed.
            False if the transition is not allowed.
        """
        valid = VALID_TRANSITIONS.get(self._state, set())
        if new_state not in valid:
            logger.warning(
                "Invalid state transition: %s → %s",
                self._state.name,
                new_state.name,
            )
            return False

        self._previous_state = self._state
        self._state = new_state
        logger.debug(
            "State: %s → %s",
            self._previous_state.name,
            self._state.name,
        )
        return True

    def force_state(self, new_state: AppState) -> None:
        """Force a state change without validation (for error recovery)."""
        self._previous_state = self._state
        self._state = new_state
        logger.warning(
            "Forced state: %s → %s",
            self._previous_state.name,
            self._state.name,
        )

    def is_active(self) -> bool:
        """Check if the system is in an active (non-terminal) state."""
        return self._state != AppState.SHUTTING_DOWN

    def is_playing(self) -> bool:
        """Check if the system is in a playing state."""
        return self._state in {AppState.PLAYING, AppState.DUCKING}
