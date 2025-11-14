# Indonesian TTS Dataset

## Folder Structure

```
dataset_indonesian/
├── wavs/                  # Put all your .wav audio files here
│   ├── sample_001.wav
│   ├── sample_002.wav
│   └── ...
├── metadata.csv           # Metadata file (pipe-separated)
└── README.md             # This file
```

## Metadata Format

The `metadata.csv` file should be pipe-separated (|) with the following columns:

```
audio_file|text|speaker_name
wavs/sample_001.wav|Selamat pagi, apa kabar?|indonesian_speaker
wavs/sample_002.wav|Saya belajar bahasa Indonesia.|indonesian_speaker
```

### Columns:
- **audio_file**: Relative path to the audio file (e.g., `wavs/filename.wav`)
- **text**: Indonesian transcription of the audio
- **speaker_name**: Speaker identifier (use same name if single speaker)

## Audio Requirements

- Format: WAV (16-bit PCM)
- Sample rate: 22050 Hz or 44100 Hz (will be resampled if needed)
- Mono channel
- Duration: Ideally 3-10 seconds per clip
- Minimum dataset size:
  - **For testing**: 10-20 samples
  - **For decent quality**: 1000+ samples (15-30 minutes)
  - **For good quality**: 5000+ samples (1-3 hours)
  - **For excellent quality**: 10000+ samples (10+ hours)

## Steps to Prepare Your Dataset

1. Place all your WAV files in the `wavs/` folder
2. Create/update `metadata.csv` with the format above
3. Ensure each line in metadata.csv corresponds to an actual audio file
4. Make sure transcriptions are accurate and use standard Indonesian spelling

## Example metadata.csv entry:
```
wavs/indonesian_001.wav|Halo, nama saya Budi.|indonesian_speaker
wavs/indonesian_002.wav|Hari ini cuaca sangat cerah.|indonesian_speaker
wavs/indonesian_003.wav|Saya suka membaca buku.|indonesian_speaker
```
