# Indonesian TTS Training with Coqui TTS

This folder contains training recipes for Indonesian Text-to-Speech models.

## Quick Start Guide

### 1. Prepare Your Dataset

You have two options:

#### Option A: Use Your Own Voice Recordings

1. Record your voice speaking Indonesian sentences
2. Place WAV files in `dataset_indonesian/wavs/`
3. Create `dataset_indonesian/metadata.csv` with format:
   ```
   audio_file|text|speaker_name
   wavs/sample_001.wav|Selamat pagi, apa kabar?|indonesian_speaker
   wavs/sample_002.wav|Saya belajar bahasa Indonesia.|indonesian_speaker
   ```

#### Option B: Generate Test Samples Automatically

```bash
# Generate test samples using eSpeak-NG or gTTS
python scripts/generate_test_samples_indonesian.py
```

### 2. Install Dependencies

```bash
# Install Coqui TTS
pip install -e .

# Install eSpeak-NG for phonemization (required!)
# macOS:
brew install espeak-ng

# Ubuntu/Debian:
sudo apt-get install espeak-ng

# Windows:
# Download from https://github.com/espeak-ng/espeak-ng/releases
```

### 3. Verify Dataset

```bash
# Check your dataset structure
ls -la dataset_indonesian/
ls -la dataset_indonesian/wavs/
cat dataset_indonesian/metadata.csv
```

### 4. Run Sanity Check Training

```bash
# Run minimal training test (CPU-friendly)
cd recipes/indonesian/vits_tts
python train_indonesian.py
```

**Note for MacBook Pro 2015 Users:**
- This config is optimized for CPU training
- Training will be SLOW (this is normal on CPU)
- This is just a pipeline test to verify everything works
- For actual training, use a GPU (Google Colab, cloud GPU, etc.)

### 5. Monitor Training

Training outputs will be saved to:
```
recipes/indonesian/vits_tts/
├── vits_indonesian_test-[timestamp]/
│   ├── checkpoints/          # Model checkpoints
│   ├── train.log             # Training log
│   └── events.out.tfevents*  # TensorBoard logs
```

View logs:
```bash
tail -f recipes/indonesian/vits_tts/vits_indonesian_test-*/train.log
```

### 6. (Optional) Use TensorBoard

```bash
# Install TensorBoard
pip install tensorboard

# View training progress
tensorboard --logdir recipes/indonesian/vits_tts/
```

## Configuration Details

### Current Configuration (`train_indonesian.py`)

- **Model**: VITS (single-stage E2E TTS)
- **Phonemizer**: eSpeak-NG (language: `id` for Indonesian)
- **Batch size**: 2 (minimal for CPU)
- **Epochs**: 10 (just for testing)
- **Sample rate**: 22050 Hz
- **Workers**: 0 (single-threaded for CPU)

### For Production Training

For actual production-quality training, you'll need:

1. **More data**: At least 5000+ samples (3-10 hours)
2. **GPU**: NVIDIA GPU with 8GB+ VRAM
3. **Larger batch size**: 32-64
4. **More epochs**: 1000+

To modify for GPU training, edit `train_indonesian.py`:

```python
config = VitsConfig(
    # ... other settings ...
    batch_size=32,              # Increase for GPU
    eval_batch_size=16,
    num_loader_workers=8,       # Use multiple workers
    epochs=1000,                # Train for longer
    mixed_precision=True,       # Enable for faster training on GPU
)
```

## Troubleshooting

### Error: "No module named 'espeak'"

Install eSpeak-NG:
```bash
# macOS
brew install espeak-ng

# Ubuntu/Debian
sudo apt-get install espeak-ng
```

### Error: "No training samples found"

Check:
1. `dataset_indonesian/metadata.csv` exists
2. Audio files exist in `dataset_indonesian/wavs/`
3. Paths in metadata.csv match actual files

### Training is very slow

This is normal on CPU! Options:
1. Use Google Colab (free GPU)
2. Use cloud GPU (AWS, GCP, Azure)
3. Use a local machine with NVIDIA GPU

### Error: "CUDA out of memory"

If training on GPU and getting OOM:
1. Reduce `batch_size`
2. Reduce `num_loader_workers`
3. Disable `mixed_precision`

## Next Steps

After successful sanity check:

1. **Collect more data**: Record or collect more Indonesian speech
2. **Move to GPU**: Use Google Colab or cloud GPU for faster training
3. **Train longer**: Run for 500-1000+ epochs
4. **Fine-tune**: Adjust hyperparameters based on results
5. **Inference**: Use trained model for synthesis

## Resources

- [Coqui TTS Documentation](https://github.com/coqui-ai/TTS)
- [VITS Paper](https://arxiv.org/abs/2106.06103)
- [eSpeak-NG](https://github.com/espeak-ng/espeak-ng)
- [Indonesian Phonology](https://en.wikipedia.org/wiki/Indonesian_phonology)

## Support

For issues, questions, or contributions:
- Check the main Coqui TTS repository
- Review existing issues and discussions
- Create a new issue with details about your problem
