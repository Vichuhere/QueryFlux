# nltk_setup.py
"""
NLTK Data Setup Script
Downloads required NLTK corpora for natural language processing
(Optional - for enhanced text tokenization and processing)
"""

import nltk
import sys

print("=" * 60)
print("📚 NLTK Data Setup Script")
print("=" * 60)

# List of required NLTK data packages
required_packages = [
    'punkt',           # Sentence tokenizer
    'wordnet',         # Word synonyms and definitions
    'averaged_perceptron_tagger',  # POS tagger
    'maxent_ne_chunker',  # Named entity recognizer
]

print(f"\nDownloading {len(required_packages)} NLTK data packages...\n")

success_count = 0
for package in required_packages:
    try:
        print(f"  Downloading {package}...", end=" ")
        nltk.download(package, quiet=True)
        print("✓")
        success_count += 1
    except Exception as e:
        print(f"✗ Error: {e}")

print(f"\n✓ Setup complete! {success_count}/{len(required_packages)} packages installed successfully.")
print("\n" + "=" * 60)
print("You can now run: python app.py")
print("=" * 60)



