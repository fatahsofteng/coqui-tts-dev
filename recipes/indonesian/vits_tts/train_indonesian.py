"""
Indonesian TTS Training Recipe with VITS
Minimal configuration for CPU-based sanity check

This is a minimal config optimized for:
- MacBook Pro 2015 (CPU-only, no CUDA)
- Quick pipeline testing
- Small batch size for low memory usage
"""
import os

from trainer import Trainer, TrainerArgs

from TTS.tts.configs.shared_configs import BaseDatasetConfig
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits, VitsAudioConfig
from TTS.tts.utils.text.tokenizer import TTSTokenizer
from TTS.utils.audio import AudioProcessor

# Get paths
output_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(output_path, "../../../dataset_indonesian/")

# Dataset configuration
dataset_config = BaseDatasetConfig(
    formatter="coqui",  # Use the 'coqui' formatter (simple pipe-separated format)
    meta_file_train="metadata.csv",
    path=dataset_path,
    language="id",  # Indonesian language code
    dataset_name="indonesian_dataset",
)

# Audio configuration - use minimal settings for faster processing
audio_config = VitsAudioConfig(
    sample_rate=22050,  # Standard sample rate
    win_length=1024,
    hop_length=256,
    num_mels=80,
    mel_fmin=0,
    mel_fmax=None,
)

# VITS configuration - MINIMAL for CPU sanity check
config = VitsConfig(
    audio=audio_config,
    run_name="vits_indonesian_test",

    # MINIMAL batch sizes for CPU
    batch_size=2,  # Very small for CPU
    eval_batch_size=1,
    batch_group_size=0,  # Disable batch grouping

    # MINIMAL workers for CPU
    num_loader_workers=0,  # Use main thread only (safer for CPU)
    num_eval_loader_workers=0,

    # Evaluation settings
    run_eval=True,
    test_delay_epochs=5,  # Don't test for first 5 epochs
    epochs=10,  # Very few epochs for sanity check

    # Text processing - Use eSpeak for Indonesian
    text_cleaner="phoneme_cleaners",
    use_phonemes=True,
    phoneme_language="id",  # Indonesian language code for eSpeak
    phoneme_cache_path=os.path.join(output_path, "phoneme_cache"),
    compute_input_seq_cache=True,

    # Logging
    print_step=1,  # Print every step (since we have so few)
    print_eval=True,
    save_step=50,  # Save checkpoint every 50 steps
    save_n_checkpoints=2,  # Keep only 2 checkpoints to save space
    save_best_after=100,  # Start saving best model after 100 steps

    # Performance settings for CPU
    mixed_precision=False,  # Disable mixed precision (not supported on CPU)
    cudnn_benchmark=False,

    # Output
    output_path=output_path,
    datasets=[dataset_config],

    # Test sentences in Indonesian
    test_sentences=[
        ["Selamat pagi, apa kabar?"],
        ["Saya belajar bahasa Indonesia."],
        ["Terima kasih banyak."],
        ["Hari ini cuaca sangat cerah."],
        ["Saya suka membaca buku."],
    ],
)

# INITIALIZE THE AUDIO PROCESSOR
print(" > Initializing audio processor...")
ap = AudioProcessor.init_from_config(config)

# INITIALIZE THE TOKENIZER
print(" > Initializing tokenizer...")
tokenizer, config = TTSTokenizer.init_from_config(config)

# LOAD DATA SAMPLES
print(" > Loading dataset samples...")
try:
    train_samples, eval_samples = load_tts_samples(
        dataset_config,
        eval_split=True,
        eval_split_max_size=config.eval_split_max_size,
        eval_split_size=config.eval_split_size,
    )
    print(f" > Found {len(train_samples)} training samples")
    print(f" > Found {len(eval_samples)} evaluation samples")
except Exception as e:
    print(f" [!] Error loading dataset: {e}")
    print(f" [!] Please check:")
    print(f"     1. Dataset path: {dataset_path}")
    print(f"     2. Metadata file: {os.path.join(dataset_path, 'metadata.csv')}")
    print(f"     3. Audio files exist in: {os.path.join(dataset_path, 'wavs/')}")
    raise

# INITIALIZE MODEL
print(" > Initializing VITS model...")
model = Vits(config, ap, tokenizer, speaker_manager=None)

# INITIALIZE TRAINER
print(" > Initializing trainer...")
trainer = Trainer(
    TrainerArgs(
        continue_path="",  # Start from scratch
        restore_path=None,
        skip_train_epoch=False,
        use_accelerate=False,  # Disable accelerate for CPU
    ),
    config,
    output_path,
    model=model,
    train_samples=train_samples,
    eval_samples=eval_samples,
)

# START TRAINING 🚀
print(" > Starting training...")
print(" > NOTE: This is running on CPU and will be SLOW.")
print(" > For actual training, use a GPU (Google Colab, cloud GPU, etc.)")
print(" > This is just a sanity check to verify the pipeline works.")
print("")
trainer.fit()
