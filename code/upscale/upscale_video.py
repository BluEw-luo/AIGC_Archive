"""Frame-by-frame RealESRGAN x4plus upscale of one video, streaming decode -> GPU -> encode."""
import json
import queue
import subprocess
import sys
import threading
import time

import torch

from rrdbnet import load_model, enhance

SRC = sys.argv[1]
DST = sys.argv[2]
MODEL = '/home/bluew_luo/comfy/ComfyUI/models/upscale_models/RealESRGAN_x4plus.pth'
SCALE = 4
TILE = 512
TILE_PAD = 16


def probe(path):
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
         'stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,'
         'color_space,color_transfer,color_primaries,color_range',
         '-of', 'json', path], capture_output=True, text=True, check=True)
    s = json.loads(out.stdout)['streams'][0]
    fps = s.get('r_frame_rate')
    if fps in (None, '0/0'):
        fps = s['avg_frame_rate']
    fps = fps.split('/')
    fps = float(fps[0]) / float(fps[1]) if len(fps) == 2 else float(fps[0])
    total = int(s['nb_frames']) if s.get('nb_frames') not in (None, 'N/A') else 0
    colors = {k: s.get(k) for k in ('color_space', 'color_transfer', 'color_primaries', 'color_range')}
    return s['width'], s['height'], fps, total, colors


W, H, FPS, TOTAL, COLORS = probe(SRC)
OW, OH = W * SCALE, H * SCALE
FRAME_BYTES = W * H * 3
if not TOTAL:
    TOTAL = 1

# Carry the source colour description through to the output so players do not shift tones.
x264_params, color_args = [], []
for key, x264_key in (('color_space', 'colormatrix'), ('color_transfer', 'transfer'),
                      ('color_primaries', 'colorprim')):
    if COLORS[key] not in (None, 'unknown', 'reserved'):
        x264_params.append(f'{x264_key}={COLORS[key]}')
for key, flag in (('color_space', '-colorspace'), ('color_range', '-color_range')):
    if COLORS[key] not in (None, 'unknown', 'reserved'):
        color_args += [flag, COLORS[key]]
if x264_params:
    color_args += ['-x264-params', ':'.join(x264_params)]

print(f'{SRC}: {W}x{H} {FPS:g}fps {TOTAL} frames -> {OW}x{OH}', flush=True)


def drain(stream, path):
    with open(path, 'wb') as f:
        while chunk := stream.read(65536):
            f.write(chunk)


model = load_model(MODEL, half=True)

decode = subprocess.Popen(
    ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', SRC,
     '-map', '0:v:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=FRAME_BYTES * 4)

encode = subprocess.Popen(
    ['ffmpeg', '-hide_banner', '-loglevel', 'error',
     '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}', '-r', f'{FPS:g}', '-i', '-',
     '-i', SRC,
     '-map', '0:v:0', '-map', '1:a:0?',
     '-c:v', 'libx264', '-preset', 'medium', '-crf', '16',
     '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '6.1',
     *color_args,
     '-movflags', '+faststart',
     '-c:a', 'copy', '-y', DST],
    stdin=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=FRAME_BYTES * 4)
threading.Thread(target=drain, args=(encode.stderr, 'encoder.log'), daemon=True).start()

frames = queue.Queue(maxsize=6)


def reader():
    while True:
        buf = decode.stdout.read(FRAME_BYTES)
        if len(buf) < FRAME_BYTES:
            frames.put(None)
            return
        frames.put(buf)


threading.Thread(target=reader, daemon=True).start()

t0 = time.time()
n = 0
while (buf := frames.get()) is not None:
    src = torch.frombuffer(bytearray(buf), dtype=torch.uint8).reshape(H, W, 3)
    img = src.permute(2, 0, 1).unsqueeze(0).to('cuda').half().div_(255.0)
    out = enhance(model, img, tile=TILE, tile_pad=TILE_PAD)
    rgb = out[0].float().mul_(255.0).round_().clamp_(0, 255).to(torch.uint8)
    arr = rgb.permute(1, 2, 0).contiguous().cpu().numpy()
    encode.stdin.write(arr.reshape(-1).data)
    n += 1
    if n % 10 == 0 or n == TOTAL:
        el = time.time() - t0
        print(f'{n}/{TOTAL}  {el:6.1f}s elapsed  {el / n:4.2f}s/frame  '
              f'eta {el / n * max(TOTAL - n, 0) / 60:4.1f} min', flush=True)

encode.stdin.close()
enc_rc = encode.wait()
dec_rc = decode.wait()
print(f'done: {n} frames, decode rc={dec_rc}, encode rc={enc_rc}, {time.time() - t0:.1f}s total',
      flush=True)
if enc_rc != 0 or n != TOTAL:
    sys.exit(1)
