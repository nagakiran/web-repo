# Video OCR - Extract Text from Videos

Extract text (lyrics, subtitles, captions) from video files using Optical Character Recognition (OCR). Perfect for extracting lyrics that are superimposed on music videos.

## Features

- 🎥 Process any video format supported by OpenCV
- 📝 Extract text using Tesseract OCR
- 🎯 Optional region-of-interest cropping for better accuracy
- 🔄 Smart deduplication to avoid repeated text
- ⚡ Configurable frame sampling rate for faster processing
- 🎨 Automatic image preprocessing for improved OCR accuracy
- ⏱️ Timestamped output with frame numbers
- 📊 Progress bar for long videos

## Prerequisites

Before running the script, you need to install Tesseract OCR:

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

### macOS
```bash
brew install tesseract
```

### Windows
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd web-repo
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Extract text from a video (processes every 30th frame by default):
```bash
python video_ocr.py your_video.mp4
```

This will create a file named `your_video_lyrics.txt` with the extracted text.

### Advanced Options

**Custom frame interval** (process every 10th frame for more detail):
```bash
python video_ocr.py video.mp4 --frame-interval 10
```

**Custom output file**:
```bash
python video_ocr.py video.mp4 --output my_lyrics.txt
```

**Extract from specific region** (useful when text appears in same location):
```bash
# Format: x y width height
python video_ocr.py video.mp4 --region 100 400 1000 200
```

**Adjust similarity threshold** (lower = more strict, fewer duplicates):
```bash
python video_ocr.py video.mp4 --similarity 0.9
```

**Disable preprocessing** (if your video already has very clear text):
```bash
python video_ocr.py video.mp4 --no-preprocess
```

**Different language** (e.g., Spanish):
```bash
python video_ocr.py video.mp4 --lang spa
```

### Finding the Right Region

If lyrics always appear in the same area of the video:

1. Open your video in a media player and note the position/size of the text area
2. Use a screenshot tool to get approximate coordinates
3. Use the `--region` flag with those coordinates:
   ```bash
   python video_ocr.py video.mp4 --region <x> <y> <width> <height>
   ```

Example: If text appears in the bottom center of a 1920x1080 video:
```bash
python video_ocr.py video.mp4 --region 400 800 1120 200
```

## Output Format

The output file contains:
- Timestamp of each text appearance (MM:SS.SS format)
- Frame number
- Extracted text
- Separator lines for readability

Example output:
```
[00:12.50] Frame 375
Never gonna give you up
Never gonna let you down
--------------------------------------------------------------------------------

[00:18.30] Frame 549
Never gonna run around
And desert you
--------------------------------------------------------------------------------
```

## Tips for Best Results

1. **Frame Interval**:
   - Use smaller intervals (5-15) for rapidly changing text
   - Use larger intervals (30-60) for slowly changing lyrics to speed up processing

2. **Region of Interest**:
   - If text always appears in the same area, use `--region` to focus OCR on that area
   - This significantly improves accuracy and speed

3. **Preprocessing**:
   - Keep preprocessing enabled (default) for videos with complex backgrounds
   - Disable with `--no-preprocess` if text is already very clear

4. **Language**:
   - Install additional Tesseract language packs if extracting non-English text
   - List available languages: `tesseract --list-langs`

5. **Video Quality**:
   - Higher resolution videos generally produce better OCR results
   - Ensure text in the video is clear and readable

## Troubleshooting

**"Command 'tesseract' not found"**
- Install Tesseract OCR (see Prerequisites section)

**Poor OCR accuracy**
- Try adjusting the `--region` parameter to focus on text area
- Ensure text in video is clear and high contrast
- Try different frame intervals
- Check if correct language is specified with `--lang`

**Too many duplicate texts**
- Increase `--similarity` threshold (e.g., 0.9 or 0.95)
- Increase `--frame-interval` to process fewer frames

**Processing is too slow**
- Increase `--frame-interval` (e.g., 60 or 90)
- Use `--region` to process only relevant area
- Consider processing a shorter clip first to test settings

## Dependencies

- `opencv-python`: Video processing
- `pytesseract`: OCR engine wrapper
- `Pillow`: Image processing
- `numpy`: Numerical operations
- `tqdm`: Progress bars

## License

This project is open source and available for personal and educational use.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
