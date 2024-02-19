import os
from pathlib import Path
import subprocess

def convert_flac_to_wav(flac_file_path):
    """
    Converts a FLAC file to WAV format using the FLAC command-line tool.
    First checks if the WAV file exists, and if so, deletes it before conversion.
    """
    flac_file_path = Path(flac_file_path)  # Ensure flac_file_path is a Path object
    wav_file_path = flac_file_path.with_suffix('.wav')
    
    # Check if WAV file exists and delete it if it does
    if wav_file_path.exists():
        wav_file_path.unlink()

    subprocess.run(['flac', '-d', '-s', '-f', str(flac_file_path)], check=True)

def read_transcripts(file_path):
    with file_path.open('r', encoding='utf-8') as f:
        for line in f:
            flac_file, transcript = line.strip().split(maxsplit=1)
            yield flac_file.rsplit('.', 1)[0], transcript

def process_directory(input_path, output_path):
    input_path = Path(input_path)
    output_path = Path(output_path)
    text_path = output_path / 'text'
    wav_path = output_path / 'wav.scp'
    utt2spk_path = output_path / 'utt2spk'

    wav_list = []
    text_list = []
    utt2spk_list = []

    #with text_path.open('w', encoding='utf-8') as f:
    #get all .trans.txt files 
    for txt_file in input_path.rglob('*.trans.txt'):
            speaker, chapter = txt_file.parent.relative_to(input_path).parts
            for file_prefix, transcript in read_transcripts(txt_file):
                flac_file_path = txt_file.parent / (file_prefix + '.flac')
                wav_file_path = txt_file.parent / (file_prefix + '.wav')
                # Convert FLAC to WAV here, assuming the WAV file should be in the same directory
                convert_flac_to_wav(flac_file_path)
                id = f'libri-{file_prefix}'
                text_list.append(f'{id} {transcript}\n')
                wav_list.append(f'{id} {wav_file_path}\n')
                utt2spk_list.append(f'{id} libri-{speaker}\n')

    #write files
    with text_path.open('w', encoding='utf-8') as f:
        for line in text_list:
            f.write(line)

    with wav_path.open('w', encoding='utf-8') as f:
        for line in wav_list:
            f.write(line)

    with utt2spk_path.open('w', encoding='utf-8') as f:
        for line in utt2spk_list:
            f.write(line)

if __name__ == "__main__":
    input_path = '/l/users/hawau.toyin/lab7_data/LibriSpeech/dev-clean/'
    output_path = 'data/train/'
    process_directory(input_path, output_path)

