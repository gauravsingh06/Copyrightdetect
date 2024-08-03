import json
import numpy as np
import librosa
import cv2
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import moviepy.video.fx.all as effects
import os

class ContentFingerprint:
    def __init__(self):
        # Load compare.json for file paths
        with open('compare.json', 'r') as compare_file:
            compare_data = json.load(compare_file)
            self.input_path = compare_data["input_video_path"]
            self.output_path = compare_data["output_video_path"]
        
        # Determine media type based on file extension
        if self.input_path.endswith(('.mp4', '.avi', '.mkv', '.mov')):
            self.media_type = 'video'
        elif self.input_path.endswith(('.mp3', '.wav', '.flac', '.aac')):
            self.media_type = 'audio'
        else:
            raise ValueError("Unsupported file format.")

        self.clip = VideoFileClip(self.input_path) if self.media_type == 'video' else None
        self.samples = self._load_audio() if self.media_type == 'audio' else None

    ### Audio Processing Methods ###
    def _load_audio(self):
        # Load and preprocess the audio part of the media file
        audio = librosa.load(self.input_path, sr=22050, mono=True)[0]
        return audio

    def _generate_audio_spectrogram(self):
        # Compute the Short-Time Fourier Transform (STFT) for audio
        spectrogram = librosa.stft(self.samples)
        spectrogram_db = librosa.amplitude_to_db(np.abs(spectrogram))
        return spectrogram_db

    def _generate_audio_fingerprints(self, min_peak_height=10):
        # Generate fingerprints for the audio part
        spectrogram_db = self._generate_audio_spectrogram()
        local_max = maximum_filter(spectrogram_db, size=20) == spectrogram_db
        peaks = np.where((spectrogram_db > min_peak_height) & local_max)
        fingerprints = list(zip(peaks[1], peaks[0]))  # (time, frequency)
        return fingerprints

    ### Video Processing Methods ###
    def _extract_keyframes(self):
        # Extract key frames from the video
        frames = []
        success, image = self.clip.reader.read_frame()
        while success:
            frames.append(image)
            success, image = self.clip.reader.read_frame()
        return frames

    def _generate_video_fingerprints(self):
        # Generate fingerprints for the video part
        frames = self._extract_keyframes()
        fingerprints = []
        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (32, 32), interpolation=cv2.INTER_AREA)
            hash_val = self._average_hash(resized)
            fingerprints.append(hash_val)
        return fingerprints

    def _average_hash(self, image):
        # Create a hash of the image using average hashing
        mean = np.mean(image)
        return ''.join('1' if pixel > mean else '0' for pixel in image.flatten())

    ### Combined Comparison Method ###
    def compare(self, other_fingerprints):
        # Compare both audio and video fingerprints with another media file
        audio_similarity = None
        video_similarity = None

        if self.media_type == 'audio':
            audio_similarity = self._compare_fingerprints(self._generate_audio_fingerprints(), other_fingerprints['audio'])
        elif self.media_type == 'video':
            video_similarity = self._compare_fingerprints(self._generate_video_fingerprints(), other_fingerprints['video'])

        return {
            'audio_similarity': audio_similarity,
            'video_similarity': video_similarity,
            'overall_similarity': (audio_similarity if audio_similarity is not None else 0) + 
                                  (video_similarity if video_similarity is not None else 0)
        }

    def _compare_fingerprints(self, fingerprints1, fingerprints2):
        # Compare two sets of fingerprints
        matches = sum(1 for fp1, fp2 in zip(fingerprints1, fingerprints2) if fp1 == fp2)
        return matches / max(len(fingerprints1), len(fingerprints2))

    ### Utility Methods ###
    def save_keyframes(self, output_dir):
        # Save extracted keyframes to the specified directory
        if self.media_type == 'video':
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            for i, frame in enumerate(self._extract_keyframes()):
                cv2.imwrite(os.path.join(output_dir, f"frame_{i}.jpg"), frame)

# Example Usage
modifier = ContentFingerprint()

# Assuming you have another ContentFingerprint object to compare against
# You need to generate the other fingerprints similarly
# e.g., other_fingerprints = some_other_ContentFingerprint_object._generate_fingerprints()

# Example comparison
# similarity = modifier.compare(other_fingerprints)
# print(similarity)

# Save keyframes if needed
# modifier.save_keyframes('output_keyframes_directory')
