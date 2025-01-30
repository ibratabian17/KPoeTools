import librosa
import numpy as np
import json
import sys
import os

def audio_to_karaoke_timeline(audio_file, min_volume_threshold_percent=30, lyrics=None):
    print('Loading Audio...')
    y, sr = librosa.load(audio_file)
    print('Done...')
    print('Using Lyrics TMLs time') if lyrics else print('Using Automatic Generated TMLs time')
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    max_volume = magnitudes.max()
    min_volume_threshold = max_volume * (min_volume_threshold_percent / 100)

    karaoke_data = {"vocalKeys": []}
    times = librosa.times_like(pitches, sr=sr)
    prev_pitch = None
    current_entry = None
    note_start = times[0]  # Initialize note start at the first time
    
    # If lyrics are provided, we will align the pitch with the lyrics timing
    lyrics_index = 0
    last_detected_pitch = None  # Keep track of the last valid pitch

    for i, t in enumerate(times):
        # Skip if the current time is less than the next lyric time
        if lyrics and lyrics_index < len(lyrics) and t < lyrics[lyrics_index]["time"] / 1000:
            continue

        frame_magnitudes = magnitudes[:, i]
        max_magnitude = frame_magnitudes.max()

        # Detect pitch if the frame magnitude is above the threshold
        if max_magnitude > min_volume_threshold:
            pitch = pitches[:, i].max()
            midi_pitch = int(librosa.hz_to_midi(pitch)) if pitch > 0 else None
            if pitch > 0:
                last_detected_pitch = midi_pitch
        elif lyrics is None:
            pitch = 0
            midi_pitch = None
        else:
            pitch = pitches[:, i].max()
            midi_pitch = int(librosa.hz_to_midi(pitch)) if pitch > 0 else None
            if pitch > 0:
                last_detected_pitch = midi_pitch
        
        # If we are aligning with lyrics
        if lyrics and lyrics_index < len(lyrics) and t >= lyrics[lyrics_index]["time"] / 1000:
            lyric = lyrics[lyrics_index]
            lyric_start_time = lyric["time"] / 1000
            lyric_duration = lyric["duration"] / 1000

            # If no valid pitch was detected for this lyric, use the last detected pitch
            if midi_pitch is None and last_detected_pitch is not None:
                midi_pitch = last_detected_pitch

            # Calculate the average pitch for the entire duration of the lyric
            avg_pitch = 0
            num_frames = 0
            for j, time_point in enumerate(times):
                if lyric_start_time <= time_point <= (lyric_start_time + lyric_duration):
                    frame_magnitudes = magnitudes[:, j]
                    max_magnitude = frame_magnitudes.max()

                    # Only consider frames where the magnitude exceeds the threshold
                    if max_magnitude > min_volume_threshold:
                        pitch = pitches[:, j].max()
                        if pitch > 0:
                            avg_pitch += pitch
                            num_frames += 1

            # If we have valid frames, calculate the average pitch
            if num_frames > 0:
                avg_pitch /= num_frames
                midi_pitch = int(librosa.hz_to_midi(avg_pitch))

            # Create karaoke entry based on the lyric timing
            current_entry = {
                "time": int(lyric_start_time * 1000),
                "duration": int(lyric_duration * 1000),
                "pitch": float(avg_pitch),  # Use the average pitch for the lyric
                "key": midi_pitch
            }
            karaoke_data["vocalKeys"].append(current_entry)
            lyrics_index += 1
        else:
            if lyrics and lyrics_index > len(lyrics):
                pass
            # Continue using auto-generated pitch if no lyrics to match
            if midi_pitch != prev_pitch:
                if current_entry:
                    # Calculate the duration of the previous entry
                    current_entry["duration"] = int((t - current_entry["time"] / 1000) * 1000)
                    # Append entry only if "key" is not null
                    if current_entry["key"] is not None:
                        karaoke_data["vocalKeys"].append(current_entry)
                
                # Start a new entry with the current pitch
                current_entry = {
                    "time": int(t * 1000),
                    "duration": 0,
                    "pitch": float(pitch),  # Convert to float for JSON compatibility
                    "key": midi_pitch
                }
                prev_pitch = midi_pitch
                note_start = t  # Update start time for the new note
            else:
                # Update duration if the pitch is the same
                if current_entry:
                    current_entry["duration"] = int((t - note_start) * 1000)

        # Simple text-based progress bar
        if i % (len(times) // 100) == 0:  # Updates every 1%
            progress = int((i / len(times)) * 100)
            print(f"\rProgress: [{'#' * (progress // 2)}{' ' * (50 - progress // 2)}] {progress}%", end='')

    # Append the last entry if any and if "key" is not null
    if current_entry and current_entry["key"] is not None:
        current_entry["duration"] = int((times[-1] - note_start) * 1000)
        karaoke_data["vocalKeys"].append(current_entry)

    print("\nProcessing complete.")
    return karaoke_data

def main():
    # Check if the audio file and volume threshold arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python pitchTMLGen.py <audiofile> <min_volume_threshold_percent> [lyricsfile]")
        sys.exit(1)

    audio_file = sys.argv[1]
    min_volume_threshold_percent = float(sys.argv[2])
    lyrics_file = sys.argv[3] if len(sys.argv) > 3 else None
    output_dir = 'output/'

    lyrics = None
    if lyrics_file:
        try:
            with open(lyrics_file, 'r', encoding="utf-8") as f:
                lyrics_data = json.load(f)
                if "lyrics" in lyrics_data:
                    lyrics = lyrics_data["lyrics"]
        except Exception as e:
            print(f"Error reading lyrics file: {e}")
            sys.exit(1)

    try:
        # Process audio file
        karaoke_timeline = audio_to_karaoke_timeline(audio_file, min_volume_threshold_percent, lyrics)
        
        # Generate the output file path
        output_file = os.path.join(output_dir, f'{os.path.splitext(os.path.basename(audio_file))[0]}.json')
        
        with open(output_file, 'w', encoding="utf-8") as outfile:
            json.dump(karaoke_timeline, outfile, indent=4)
            print(f"\nAudio TMLS. Saved to {output_file}")

    except Exception as e:
        print(f"Failed to process file: {e}")

if __name__ == "__main__":
    main()
