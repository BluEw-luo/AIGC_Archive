# 视频逐帧超分（RealESRGAN x4plus）

把 ComfyUI 直出的视频按帧解码、逐帧过 RealESRGAN x4plus、再编码回 mp4，音轨直接复制。用来把 MiniMax H3 的 1344×768 原片放大到 5376×3072，见 [`prompts/2026-11-misprint/`](../../prompts/2026-11-misprint/)。

本目录的脚本与说明按 **MIT** 授权（见 [`LICENSES/MIT.txt`](../../LICENSES/MIT.txt)）；作品归档说明仍按 CC BY 4.0。

## 文件

| 文件 | 作用 |
| --- | --- |
| `rrdbnet.py` | RealESRGAN 的 RRDBNet（x4plus）最小实现 + 分块推理（`tile` 控制显存占用） |
| `upscale_video.py` | 一次跑完一条视频：ffprobe 探参数 → ffmpeg 解码 → GPU 推理 → ffmpeg 编码 |

## 依赖

- Python 3 + PyTorch（CUDA）、ffmpeg / ffprobe；
- 权重 `RealESRGAN_x4plus.pth`：从 [xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) 下载后放到 `ComfyUI/models/upscale_models/`。
  **权重不入库**——模型文件既不进本仓库（`.gitignore` 拦截），再分发条款也看原作者。脚本里的 `MODEL` 常量是作者本机的路径，换机器时改这一行即可。

## 用法

```bash
python3 upscale_video.py input.mp4 output_x4.mp4
```

- 自动读取源视频的 fps、帧数、色彩描述（`color_space` / `color_transfer` / `color_primaries` / `color_range`），写进输出，避免播放器偏色；
- 视频用 `libx264 -crf 16 -preset medium`，`yuv420p`，`+faststart`；音频 `-c:a copy` 原样保留；
- 进度按每 10 帧打印一次，包含 `s/frame` 与 ETA。

## 耗时

没留跑分记录。作者本机是 RTX 3080、`tile=512`，跑 1344×768 → 5376×3072 的 243 帧；脚本每 10 帧打印一次 `s/frame` 与 ETA，自己跑一遍就知道。显存不够就把 `TILE` 调小（512 → 256），代价是慢一点。

## 已知限制

- 只能 4× 整数倍放大，输入边长不是 4 的倍数时会先 reflect pad 再裁掉；
- 逐帧独立推理，没有时序一致性约束，快速运动镜头放大后可能看到轻微的帧间闪烁；
- 没有 HDR / 10bit 通路，输出固定 8bit yuv420p。
