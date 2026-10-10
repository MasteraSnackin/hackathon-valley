#!/usr/bin/env python3
"""Finish the rendered demo with measured narration level, captions and chapters."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-show_chapters', '-of', 'json', str(path)]).stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--render', type=Path, required=True)
    parser.add_argument('--captions', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Output exists; choose a new versioned filename.')
    measurement = run(['ffmpeg', '-hide_banner', '-i', str(args.render), '-vn', '-af', 'loudnorm=I=-16:TP=-2:LRA=11:print_format=json', '-f', 'null', '-']).stderr
    measured = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', measurement, re.S)[-1])
    af = 'loudnorm=I=-16:TP=-2:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:linear=true:print_format=json'.format(**measured)
    chapters = [(0, 8, 'Tenant request'), (8, 19, 'Two independent checks'), (19, 25, 'One check remains'), (25, 37, 'Workflow resumes'), (37, 46, 'Policy settings'), (46, 54, 'Result and demo boundary')]
    metadata = ';FFMETADATA1\ntitle=Property Desk working product demo\ncomment=Fictional local demo. External actions simulated. Physical repair not confirmed.\n'
    for start, end, title in chapters:
        metadata += f'[CHAPTER]\nTIMEBASE=1/1000\nSTART={start * 1000}\nEND={end * 1000}\ntitle={title}\n'
    with tempfile.TemporaryDirectory(prefix='property-demo-finish-') as td:
        m = Path(td) / 'chapters.txt'
        m.write_text(metadata)
        command = ['ffmpeg', '-hide_banner', '-i', str(args.render), '-i', str(args.captions), '-f', 'ffmetadata', '-i', str(m), '-map', '0:v:0', '-map', '0:a:0', '-map', '1:0', '-map_metadata', '2', '-map_chapters', '2', '-c:v', 'copy', '-af', af, '-ar', '48000', '-c:a', 'aac', '-b:a', '160k', '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng', '-metadata:s:s:0', 'title=English', '-movflags', '+faststart', '-t', '54', str(args.output)]
        result = run(command)
    outmeta = probe(args.output)
    final_measurement = run(['ffmpeg', '-hide_banner', '-i', str(args.output), '-vn', '-af', 'loudnorm=I=-16:TP=-2:LRA=11:print_format=json', '-f', 'null', '-']).stderr
    final_audio = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', final_measurement, re.S)[-1])
    run(['ffmpeg', '-v', 'error', '-i', str(args.output), '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'])
    info = {'output': args.output.name, 'sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(), 'bytes': args.output.stat().st_size, 'duration_seconds': float(outmeta['format']['duration']), 'render_audio_measurement': measured, 'final_audio_measurement': final_audio, 'streams': outmeta['streams'], 'chapters': outmeta['chapters'], 'full_stream_decode': 'passed', 'perceptual_review': 'Not established by this script'}
    args.output.with_suffix('.technical-check.json').write_text(json.dumps(info, indent=2) + '\n')
    print(json.dumps({k: info[k] for k in ('output', 'sha256', 'bytes', 'duration_seconds', 'full_stream_decode')}, indent=2))


if __name__ == '__main__':
    main()
