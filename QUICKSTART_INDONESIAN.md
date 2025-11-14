# Quick Start: Indonesian TTS Training Pipeline Test

This guide will help you run a **sanity check** on the Indonesian TTS training pipeline.

## 🎯 Goal

Verify that the entire training pipeline works on your MacBook Pro 2015 (CPU-only) before committing to full-scale training.

## ⚡ Quick Steps

### 1. Install Dependencies

```bash
# Install Coqui TTS and dependencies
pip install -e .

# Install eSpeak-NG (REQUIRED for Indonesian phonemization)
brew install espeak-ng

# Verify eSpeak-NG installation
espeak-ng --version
espeak-ng -v id "Halo, apa kabar?"  # Should speak in Indonesian
```

### 2. Generate Test Audio Samples

```bash
# Automatically generate 10 test samples
python scripts/generate_test_samples_indonesian.py
```

**OR** if you have your own recordings:

```bash
# Put your WAV files in dataset_indonesian/wavs/
# Update dataset_indonesian/metadata.csv
```

### 3. Verify Dataset

```bash
# Check dataset structure
ls -la dataset_indonesian/wavs/

# Check metadata
cat dataset_indonesian/metadata.csv

# Should see:
# audio_file|text|speaker_name
# wavs/sample_001.wav|Selamat pagi, apa kabar?|indonesian_speaker
# ...
```

### 4. Run Sanity Check Training

```bash
# Navigate to recipe folder
cd recipes/indonesian/vits_tts

# Start training (CPU-only, will be slow!)
python train_indonesian.py
```

### 5. What to Expect

**Expected behavior:**
- ✅ Audio processor initializes
- ✅ Tokenizer initializes with Indonesian phonemes
- ✅ Dataset loads successfully
- ✅ Model initializes (VITS)
- ✅ Training starts (very slow on CPU)
- ✅ Checkpoints save every 50 steps
- ✅ Evaluation runs after each epoch

**Expected output:**
```
 > Initializing audio processor...
 > Initializing tokenizer...
 > Loading dataset samples...
 > Found 9 training samples
 > Found 1 evaluation samples
 > Initializing VITS model...
 > Initializing trainer...
 > Starting training...
 > NOTE: This is running on CPU and will be SLOW.
...
```

**Training speed (CPU):**
- ~30-60 seconds per step (normal on CPU!)
- ~5-10 minutes per epoch (with 10 samples)
- This is just for testing; real training needs GPU

### 6. Stop Training (After Sanity Check)

Once you see training progressing (5-10 steps), you can stop:

```bash
# Press Ctrl+C to stop training
```

## ✅ Success Criteria

Your pipeline works if you see:
- ✅ No errors during initialization
- ✅ Dataset loads correctly
- ✅ Training starts and progresses
- ✅ Loss values are printed
- ✅ Checkpoints are saved

## 🚨 Common Issues

### Issue: `ModuleNotFoundError: No module named 'trainer'`

**Solution:**
```bash
pip install -e .
```

### Issue: `espeak-ng: command not found`

**Solution:**
```bash
brew install espeak-ng
```

### Issue: `No training samples found`

**Solution:**
Check dataset:
```bash
ls -la dataset_indonesian/wavs/
cat dataset_indonesian/metadata.csv
```

### Issue: Training is extremely slow

**Expected!** CPU training is 10-100x slower than GPU.
- For sanity check: This is fine
- For real training: Use GPU (Google Colab, cloud GPU, etc.)

## 📊 Next Steps After Sanity Check

### If Successful ✅

1. **Collect Real Data**
   - Record 1000+ samples (1-3 hours of speech)
   - Or use existing Indonesian speech dataset

2. **Move to GPU**
   - Google Colab (free T4 GPU)
   - Cloud GPU (AWS, GCP, Azure)
   - Local machine with NVIDIA GPU

3. **Update Configuration**
   - Edit `train_indonesian.py`
   - Increase batch_size to 32-64
   - Increase epochs to 1000+
   - Enable mixed_precision
   - Increase num_loader_workers

4. **Train Production Model**
   ```bash
   # On GPU machine
   python recipes/indonesian/vits_tts/train_indonesian.py
   ```

### If Failed ❌

1. Check error messages carefully
2. Verify all dependencies are installed
3. Check dataset format and file paths
4. Review `recipes/indonesian/README.md` for troubleshooting

## 🎓 Understanding the Configuration

Current config (`train_indonesian.py`):
- **Minimal** settings for CPU testing
- **2 samples** per batch (very small)
- **10 epochs** total (just for testing)
- **No mixed precision** (CPU doesn't support it)
- **0 workers** (single-threaded)

Production config (for GPU):
- **32-64** samples per batch
- **1000+** epochs
- **Mixed precision** enabled
- **8** workers for data loading

## 📚 Resources

- Full guide: `recipes/indonesian/README.md`
- Dataset format: `dataset_indonesian/README.md`
- Coqui TTS docs: https://github.com/coqui-ai/TTS
- VITS paper: https://arxiv.org/abs/2106.06103

## 🎉 Ready?

Let's run the sanity check!

```bash
# Generate samples
python scripts/generate_test_samples_indonesian.py

# Run training test
cd recipes/indonesian/vits_tts
python train_indonesian.py
```

Good luck! 🚀
