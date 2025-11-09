#!/usr/bin/env python3
"""
Video OCR Extractor - Extract text from video frames
Specifically designed for extracting lyrics or subtitles superimposed on videos
"""

import cv2
import pytesseract
import argparse
import os
from pathlib import Path
from tqdm import tqdm
import difflib


class VideoOCR:
    def __init__(self, video_path, output_path=None, frame_interval=1, similarity_threshold=0.85,
                 lang='eng', preprocess=True, region=None):
        """
        Initialize Video OCR extractor

        Args:
            video_path (str): Path to input video file
            output_path (str): Path to output text file (default: video_name_lyrics.txt)
            frame_interval (int): Process every Nth frame (default: 1 for every frame)
            similarity_threshold (float): Threshold for considering text as duplicate (0-1)
            lang (str): Tesseract language code (default: 'eng')
            preprocess (bool): Apply image preprocessing for better OCR
            region (tuple): Optional (x, y, width, height) to crop specific region
        """
        self.video_path = video_path
        self.frame_interval = frame_interval
        self.similarity_threshold = similarity_threshold
        self.lang = lang
        self.preprocess = preprocess
        self.region = region

        # Set output path
        if output_path is None:
            video_name = Path(video_path).stem
            self.output_path = f"{video_name}_lyrics.txt"
        else:
            self.output_path = output_path

        self.previous_text = ""
        self.extracted_texts = []

    def preprocess_frame(self, frame):
        """
        Preprocess frame to improve OCR accuracy

        Args:
            frame: OpenCV image frame

        Returns:
            Preprocessed frame
        """
        # Crop to region of interest if specified
        if self.region:
            x, y, w, h = self.region
            frame = frame[y:y+h, x:x+w]

        if not self.preprocess:
            return frame

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to make text more clear
        # Using Otsu's thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Optional: Apply denoising
        denoised = cv2.fastNlMeansDenoising(thresh)

        # Optional: Increase contrast
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)

        return enhanced

    def text_similarity(self, text1, text2):
        """
        Calculate similarity ratio between two texts

        Args:
            text1 (str): First text
            text2 (str): Second text

        Returns:
            float: Similarity ratio (0-1)
        """
        return difflib.SequenceMatcher(None, text1, text2).ratio()

    def extract_text_from_frame(self, frame):
        """
        Extract text from a single frame using OCR

        Args:
            frame: OpenCV image frame

        Returns:
            str: Extracted text
        """
        processed_frame = self.preprocess_frame(frame)

        # Configure Tesseract
        custom_config = r'--oem 3 --psm 6'  # PSM 6: Assume a single uniform block of text

        # Extract text
        text = pytesseract.image_to_string(processed_frame, lang=self.lang, config=custom_config)

        return text.strip()

    def is_new_text(self, text):
        """
        Check if text is significantly different from previous text

        Args:
            text (str): Current extracted text

        Returns:
            bool: True if text is new/different enough
        """
        if not text:
            return False

        if not self.previous_text:
            return True

        similarity = self.text_similarity(text, self.previous_text)
        return similarity < self.similarity_threshold

    def process_video(self):
        """
        Process entire video and extract text from frames

        Returns:
            list: List of extracted unique texts with timestamps
        """
        # Open video file
        video = cv2.VideoCapture(self.video_path)

        if not video.isOpened():
            raise ValueError(f"Could not open video file: {self.video_path}")

        # Get video properties
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)

        print(f"Processing video: {self.video_path}")
        print(f"Total frames: {total_frames}")
        print(f"FPS: {fps}")
        print(f"Processing every {self.frame_interval} frame(s)")

        frame_count = 0
        results = []

        # Process frames with progress bar
        with tqdm(total=total_frames // self.frame_interval, desc="Extracting text") as pbar:
            while True:
                ret, frame = video.read()

                if not ret:
                    break

                # Process every Nth frame
                if frame_count % self.frame_interval == 0:
                    text = self.extract_text_from_frame(frame)

                    # Only save if text is new/different
                    if self.is_new_text(text):
                        timestamp = frame_count / fps
                        results.append({
                            'timestamp': timestamp,
                            'frame': frame_count,
                            'text': text
                        })
                        self.previous_text = text
                        self.extracted_texts.append(text)

                    pbar.update(1)

                frame_count += 1

        video.release()
        return results

    def save_results(self, results):
        """
        Save extracted text to output file

        Args:
            results (list): List of extraction results
        """
        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.write(f"Extracted Text from Video: {self.video_path}\n")
            f.write(f"{'='*80}\n\n")

            for result in results:
                timestamp = result['timestamp']
                minutes = int(timestamp // 60)
                seconds = timestamp % 60

                f.write(f"[{minutes:02d}:{seconds:05.2f}] Frame {result['frame']}\n")
                f.write(f"{result['text']}\n")
                f.write(f"{'-'*80}\n\n")

        print(f"\nResults saved to: {self.output_path}")
        print(f"Total unique text segments extracted: {len(results)}")

    def run(self):
        """
        Run the complete OCR extraction process
        """
        results = self.process_video()
        self.save_results(results)
        return results


def main():
    parser = argparse.ArgumentParser(
        description='Extract text (lyrics, subtitles) from video files using OCR',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python video_ocr.py input_video.mp4

  # Process every 30th frame (faster, good for lyrics that change slowly)
  python video_ocr.py input_video.mp4 --frame-interval 30

  # Extract from specific region (x, y, width, height)
  python video_ocr.py input_video.mp4 --region 100 400 1000 200

  # Custom output file
  python video_ocr.py input_video.mp4 --output lyrics.txt

  # Without preprocessing (if video already has clear text)
  python video_ocr.py input_video.mp4 --no-preprocess
        """
    )

    parser.add_argument('video', help='Path to input video file')
    parser.add_argument('-o', '--output', help='Output text file path')
    parser.add_argument('-i', '--frame-interval', type=int, default=30,
                        help='Process every Nth frame (default: 30)')
    parser.add_argument('-s', '--similarity', type=float, default=0.85,
                        help='Text similarity threshold 0-1 (default: 0.85)')
    parser.add_argument('-l', '--lang', default='eng',
                        help='Tesseract language code (default: eng)')
    parser.add_argument('--no-preprocess', action='store_true',
                        help='Disable image preprocessing')
    parser.add_argument('-r', '--region', type=int, nargs=4, metavar=('X', 'Y', 'W', 'H'),
                        help='Crop region (x, y, width, height) before OCR')

    args = parser.parse_args()

    # Check if video file exists
    if not os.path.exists(args.video):
        print(f"Error: Video file not found: {args.video}")
        return 1

    # Create OCR processor
    ocr = VideoOCR(
        video_path=args.video,
        output_path=args.output,
        frame_interval=args.frame_interval,
        similarity_threshold=args.similarity,
        lang=args.lang,
        preprocess=not args.no_preprocess,
        region=tuple(args.region) if args.region else None
    )

    # Run extraction
    try:
        ocr.run()
        return 0
    except Exception as e:
        print(f"Error processing video: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
