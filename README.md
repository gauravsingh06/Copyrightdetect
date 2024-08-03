Certainly! Below is the entire `README.md` file in one piece, which includes detailed instructions for using both the `VideoModifier` and `ContentFingerprint` scripts.

---

# Media Processing Scripts

This repository contains two Python scripts designed for video and audio processing:

1. **VideoModifier**: A script that allows you to apply various modifications to a video based on user-defined settings.
2. **ContentFingerprint**: A script that generates and compares fingerprints for audio and video content to identify similarities between media files.

## Prerequisites

Before running the scripts, ensure you have Python installed. You'll also need to install the required Python libraries. You can install them using the following command:

```bash
pip install -r requirements.txt
```

## Scripts Overview

### 1. VideoModifier

The `VideoModifier` script allows you to apply a variety of modifications to a video, such as resizing, changing speed, adding borders, applying color filters, overlaying text, reversing the video, and adjusting audio pitch.

#### Configuration Files

- **compare.json**: Specifies the input and output video paths.
- **modify.json**: Specifies the modifications to be applied.

#### Example `compare.json`

```json
{
    "input_video_path": "input_video.mp4",
    "output_video_path": "modified_video.mp4"
}
```

#### Example `modify.json`

```json
{
    "resize": {
        "enabled": true,
        "width": 640,
        "height": null
    },
    "change_speed": {
        "enabled": true,
        "factor": 1.5
    },
    "add_border": {
        "enabled": true,
        "size": 15,
        "color": [255, 0, 0]
    },
    "apply_color_filter": {
        "enabled": true,
        "filter_type": "sepia"
    },
    "overlay_text": {
        "enabled": true,
        "text": "Modified Video",
        "position": "top",
        "fontsize": 30,
        "color": "yellow"
    },
    "reverse_video": {
        "enabled": true
    },
    "adjust_audio_pitch": {
        "enabled": true,
        "pitch_factor": 1.2
    }
}
```

#### How to Use

1. Create the `compare.json` and `modify.json` files with the appropriate settings.
2. Run the `VideoModifier` script:

    ```bash
    python video_modifier.py
    ```

3. The modified video will be saved to the path specified in `compare.json`.

### 2. ContentFingerprint

The `ContentFingerprint` script is designed to generate and compare fingerprints for audio and video files, allowing you to identify similarities between different media files.

#### Configuration File

- **compare.json**: Specifies the input media path (audio or video) and the output path.

#### Example `compare.json`

```json
{
    "input_video_path": "input_video_or_audio_file.mp4",
    "output_video_path": "output_file_path.mp4"
}
```

#### How to Use

1. Create the `compare.json` file with the appropriate settings.
2. Run the `ContentFingerprint` script:

    ```bash
    python content_fingerprint.py
    ```

3. If you want to compare two media files, you would:
   - Create another `ContentFingerprint` object for the second file.
   - Use the `compare` method to compare the fingerprints of both files.
   - Example:

    ```python
    modifier1 = ContentFingerprint()
    modifier2 = ContentFingerprint()

    similarity = modifier1.compare(modifier2._generate_fingerprints())
    print(similarity)
    ```

#### Optional: Save Keyframes (for Video)

If you want to save the keyframes of a video for further analysis, use the `save_keyframes` method:

```python
modifier.save_keyframes('output_keyframes_directory')
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Disclaimer

These scripts are provided for educational purposes only. Please ensure that you comply with all relevant copyright laws and use these tools responsibly.

---

This `README.md` provides clear instructions for setting up and using both the `VideoModifier` and `ContentFingerprint` scripts, including how to configure them using JSON files and how to execute them. The details are presented in a structured way, ensuring that users can easily follow along.