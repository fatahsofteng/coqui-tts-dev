#!/usr/bin/env python3
"""
Generate test audio samples for Indonesian TTS pipeline testing

This script generates synthetic audio samples using available TTS engines
or provides instructions for manual recording.
"""
import os
import sys
import subprocess
from pathlib import Path

# Test sentences in Indonesian
test_sentences = [
    "Selamat pagi, apa kabar?",
    "Saya belajar bahasa Indonesia.",
    "Terima kasih banyak.",
    "Hari ini cuaca sangat cerah.",
    "Saya suka membaca buku.",
    "Ini adalah tes untuk sistem text-to-speech.",
    "Nama saya adalah asisten virtual.",
    "Bagaimana kabar Anda hari ini?",
    "Saya senang bertemu dengan Anda.",
    "Sampai jumpa lagi nanti.",
]

def generate_with_espeak(output_dir, sentences):
    """Generate audio samples using eSpeak-NG"""
    print("Attempting to use eSpeak-NG...")

    # Check if espeak is installed
    try:
        subprocess.run(["espeak-ng", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("eSpeak-NG not found. Please install it:")
        print("  Ubuntu/Debian: sudo apt-get install espeak-ng")
        print("  macOS: brew install espeak-ng")
        print("  Windows: Download from https://github.com/espeak-ng/espeak-ng/releases")
        return False

    os.makedirs(output_dir, exist_ok=True)
    metadata_lines = []

    for idx, sentence in enumerate(sentences, 1):
        wav_file = f"sample_{idx:03d}.wav"
        wav_path = os.path.join(output_dir, wav_file)

        # Generate audio with eSpeak-NG (Indonesian language)
        cmd = [
            "espeak-ng",
            "-v", "id",  # Indonesian voice
            "-w", wav_path,
            "-s", "150",  # Speed (words per minute)
            sentence
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Generated: {wav_file}")
            metadata_lines.append(f"wavs/{wav_file}|{sentence}|indonesian_speaker")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to generate {wav_file}: {e}")
            return False

    # Write metadata.csv
    metadata_path = os.path.join(os.path.dirname(output_dir), "metadata.csv")
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write("audio_file|text|speaker_name\n")
        f.write("\n".join(metadata_lines))

    print(f"\n✓ Generated {len(metadata_lines)} samples")
    print(f"✓ Metadata written to: {metadata_path}")
    return True

def generate_with_gtts(output_dir, sentences):
    """Generate audio samples using Google Text-to-Speech (gTTS)"""
    print("Attempting to use gTTS (Google Text-to-Speech)...")

    try:
        from gtts import gTTS
        from pydub import AudioSegment
    except ImportError:
        print("gTTS or pydub not installed. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "gtts", "pydub"], check=True)
            from gtts import gTTS
            from pydub import AudioSegment
        except:
            print("Failed to install gTTS/pydub. Please install manually:")
            print("  pip install gtts pydub")
            return False

    os.makedirs(output_dir, exist_ok=True)
    metadata_lines = []

    for idx, sentence in enumerate(sentences, 1):
        wav_file = f"sample_{idx:03d}.wav"
        mp3_file = f"sample_{idx:03d}.mp3"
        wav_path = os.path.join(output_dir, wav_file)
        mp3_path = os.path.join(output_dir, mp3_file)

        try:
            # Generate MP3 with gTTS
            tts = gTTS(text=sentence, lang='id', slow=False)
            tts.save(mp3_path)

            # Convert MP3 to WAV
            audio = AudioSegment.from_mp3(mp3_path)
            audio = audio.set_frame_rate(22050).set_channels(1)  # Mono, 22050 Hz
            audio.export(wav_path, format="wav")

            # Remove temporary MP3
            os.remove(mp3_path)

            print(f"✓ Generated: {wav_file}")
            metadata_lines.append(f"wavs/{wav_file}|{sentence}|indonesian_speaker")
        except Exception as e:
            print(f"✗ Failed to generate {wav_file}: {e}")
            continue

    if not metadata_lines:
        return False

    # Write metadata.csv
    metadata_path = os.path.join(os.path.dirname(output_dir), "metadata.csv")
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write("audio_file|text|speaker_name\n")
        f.write("\n".join(metadata_lines))

    print(f"\n✓ Generated {len(metadata_lines)} samples")
    print(f"✓ Metadata written to: {metadata_path}")
    return True

def print_manual_instructions(output_dir):
    """Print instructions for manual recording"""
    print("\n" + "="*60)
    print("MANUAL RECORDING INSTRUCTIONS")
    print("="*60)
    print("\nSince automated generation failed, please record audio manually:")
    print("\n1. Use any recording software (QuickTime, Audacity, Voice Memos, etc.)")
    print("2. Record the following sentences in Indonesian:")
    print()

    for idx, sentence in enumerate(test_sentences, 1):
        print(f"   {idx:2d}. {sentence}")

    print("\n3. Save each recording as:")
    print(f"   {output_dir}/sample_001.wav")
    print(f"   {output_dir}/sample_002.wav")
    print("   ... and so on")

    print("\n4. Audio requirements:")
    print("   - Format: WAV")
    print("   - Sample rate: 22050 Hz or 44100 Hz")
    print("   - Channels: Mono (1 channel)")
    print("   - Duration: 3-10 seconds per clip")

    print("\n5. After recording, update metadata.csv with:")
    metadata_path = os.path.join(os.path.dirname(output_dir), "metadata.csv")
    print(f"\n   File: {metadata_path}")
    print("   Format:")
    print("   audio_file|text|speaker_name")
    for idx, sentence in enumerate(test_sentences, 1):
        print(f"   wavs/sample_{idx:03d}.wav|{sentence}|indonesian_speaker")
    print("\n" + "="*60)

def main():
    # Get the dataset directory
    script_dir = Path(__file__).parent.absolute()
    repo_root = script_dir.parent
    dataset_dir = repo_root / "dataset_indonesian"
    wavs_dir = dataset_dir / "wavs"

    print("="*60)
    print("INDONESIAN TTS TEST SAMPLE GENERATOR")
    print("="*60)
    print(f"\nDataset directory: {dataset_dir}")
    print(f"Audio output directory: {wavs_dir}")
    print(f"Number of test sentences: {len(test_sentences)}")
    print()

    # Try different methods
    methods = [
        ("eSpeak-NG", generate_with_espeak),
        ("gTTS (Google TTS)", generate_with_gtts),
    ]

    for method_name, method_func in methods:
        print(f"\n--- Trying: {method_name} ---")
        if method_func(str(wavs_dir), test_sentences):
            print(f"\n✓ SUCCESS! Generated samples using {method_name}")
            print(f"\nNext steps:")
            print(f"  1. Check the samples in: {wavs_dir}")
            print(f"  2. Verify metadata.csv in: {dataset_dir}")
            print(f"  3. Run training: python recipes/indonesian/vits_tts/train_indonesian.py")
            return 0
        print(f"✗ {method_name} failed, trying next method...")

    # If all methods failed, print manual instructions
    print("\n✗ All automated methods failed.")
    print_manual_instructions(str(wavs_dir))
    return 1

if __name__ == "__main__":
    sys.exit(main())
