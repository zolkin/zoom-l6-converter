import os
from pydub import AudioSegment

def transcode_32bit_to_24bit(input_path, output_path):
    """
    Transcodes a 32-bit float WAV file to 24-bit WAV.
    Skips conversion if output file already exists.
    """
    try:
        # Check if the output file already exists
        if os.path.exists(output_path):
            print(f"Skipping {input_path} as {output_path} already exists.")
            return
        
        # Load the 32-bit float .wav file
        audio = AudioSegment.from_wav(input_path)
        
        # Check sample width of the loaded audio
        if audio.sample_width == 4:
            print(f"Transcoding {input_path} to 24-bit format.")
        else:
            print(f"Warning: {input_path} is not a 32-bit float. Skipping.")
            return
        
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Export to 24-bit depth .wav
        audio.export(output_path, format="wav", parameters=["-sample_fmt", "s16", "-ac", "2", "-ar", "44100"])
        print(f"Successfully transcoded: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def traverse_and_convert(input_dir, output_dir):
    """
    Traverses through a directory (including subdirectories), converting all 32-bit float WAV files to 24-bit WAV.
    Skips conversion if the output file already exists.
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.wav'):  # Only process .wav files
                input_file_path = os.path.join(root, file)
                # Create corresponding output file path in the output directory
                relative_path = os.path.relpath(input_file_path, input_dir)
                output_file_path = os.path.join(output_dir, relative_path)
                
                # Transcode the file if it hasn't already been processed
                transcode_32bit_to_24bit(input_file_path, output_file_path)

# Example usage
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Directory 32-bit to 24 bit .wav file converter')
    parser.add_argument('input_dir', type=str, help='input directory')
    parser.add_argument('output_dir', type=str, help='output directory')
    args = parser.parse_args()
    traverse_and_convert(args.input_dir, args.output_dir)

