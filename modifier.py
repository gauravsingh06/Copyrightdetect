import json
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
import moviepy.video.fx.all as effects

class VideoModifier:
    def __init__(self):
        # Load compare.json for file paths
        with open('compare.json', 'r') as compare_file:
            compare_data = json.load(compare_file)
            self.input_path = compare_data["input_video_path"]
            self.output_path = compare_data["output_video_path"]
        
        # Load modify.json for modification settings
        with open('modify.json', 'r') as modify_file:
            self.modify_settings = json.load(modify_file)
        
        self.clip = VideoFileClip(self.input_path)
    
    def apply_modifications(self):
        # Apply resize
        if self.modify_settings["resize"]["enabled"]:
            width = self.modify_settings["resize"]["width"]
            height = self.modify_settings["resize"]["height"]
            self.clip = self.clip.resize(newsize=(width, height) if width and height else (width or self.clip.w, height or self.clip.h))

        # Apply speed change
        if self.modify_settings["change_speed"]["enabled"]:
            factor = self.modify_settings["change_speed"]["factor"]
            self.clip = self.clip.fx(effects.speedx, factor)
        
        # Add border
        if self.modify_settings["add_border"]["enabled"]:
            size = self.modify_settings["add_border"]["size"]
            color = tuple(self.modify_settings["add_border"]["color"])
            self.clip = self.clip.margin(size, color=color)
        
        # Apply color filter
        if self.modify_settings["apply_color_filter"]["enabled"]:
            filter_type = self.modify_settings["apply_color_filter"]["filter_type"]
            if filter_type == 'grayscale':
                self.clip = self.clip.fx(effects.blackwhite)
            elif filter_type == 'invert':
                self.clip = self.clip.fx(effects.invert_colors)
            elif filter_type == 'sepia':
                self.clip = self.clip.fx(effects.colorx, 0.3)
        
        # Overlay text
        if self.modify_settings["overlay_text"]["enabled"]:
            text = self.modify_settings["overlay_text"]["text"]
            position = self.modify_settings["overlay_text"]["position"]
            fontsize = self.modify_settings["overlay_text"]["fontsize"]
            color = self.modify_settings["overlay_text"]["color"]
            txt_clip = TextClip(text, fontsize=fontsize, color=color, size=(self.clip.w, None)).set_position(("center", position)).set_duration(self.clip.duration)
            self.clip = CompositeVideoClip([self.clip, txt_clip])
        
        # Reverse video
        if self.modify_settings["reverse_video"]["enabled"]:
            self.clip = self.clip.fx(effects.time_mirror)
        
        # Adjust audio pitch
        if self.modify_settings["adjust_audio_pitch"]["enabled"]:
            pitch_factor = self.modify_settings["adjust_audio_pitch"]["pitch_factor"]
            self.clip = self.clip.fx(effects.volumex, pitch_factor)

    def save(self):
        self.clip.write_videofile(self.output_path, codec='libx264', audio_codec='aac')

# Example Usage
modifier = VideoModifier()
modifier.apply_modifications()
modifier.save()
