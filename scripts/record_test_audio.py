"""
Record test audio samples for Echo-Sync testing.

Usage:
    python scripts/record_test_audio.py
    python scripts/record_test_audio.py --duration 5 --output test_sample.wav
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main():
    parser = argparse.ArgumentParser(description="Record test audio samples")
    parser.add_argument(
        "--duration", "-d",
        type=float,
        default=5.0,
        help="Maximum recording duration in seconds (default: 5)",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="test_recording.wav",
        help="Output file name (default: test_recording.wav)",
    )
    args = parser.parse_args()

    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy as np

        print(f"Recording for up to {args.duration} seconds...")
        print("Speak now! Press Ctrl+C to stop early.")

        sample_rate = 16000
        recording = sd.rec(
            int(args.duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()

        output_path = Path(args.output)
        sf.write(str(output_path), recording, sample_rate)
        print(f"Saved recording to: {output_path}")
        print(f"Duration: {len(recording) / sample_rate:.2f}s")

    except KeyboardInterrupt:
        print("\nRecording stopped.")
    except ImportError:
        print("Error: sounddevice and soundfile are required.")
        print("Install: pip install sounddevice soundfile")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
