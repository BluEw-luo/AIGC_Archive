# 刷り損じ / MISPRINT

> 一本链条装订的校样书被逐页翻开：碎石、黑丝、红绒、伪日文大字、镀铬的罗马数字表盘。一次 T2VA 直出，14 个镜头，10 秒。

- **日期**：2026-11-15（B 站发布）
- **平台 / 链接**：B 站 · https://www.bilibili.com/video/BV152sW6xEfQ/ ，标题《为MiniMax H3正名——H3本地部署测试一例》
- **模型**：`minimax_h3_fl2va_pruned_int8_convrot.safetensors`（MiniMax H3 FL2VA，int8）+ `pika_h3_flex_fl2va_v1_bf16.safetensors`（Pika H3 Flex LoRA，6 step 加速）
- **工作流**：`workflow.json`（ComfyUI，主体是名为 `Image to Video (Pika H3 Flex)` 的子图）
- **示例**：`sample.mp4` 为 **未超分原片**（1344 × 768，10.125 s，含 H3 同一次生成的音轨）；`01.png` / `02.png` 是从原片截的两帧。B 站发布版是 RealESRGAN 4× 逐帧超分（5376 × 3072），脚本在 [`code/upscale/`](../../code/upscale/)
- **许可**：提示词、工作流、视频按 CC BY 4.0（见仓库根目录 `LICENSE`）；底模另受 MiniMax H3 Community License Agreement 约束，商用前请自行核对

## 正向提示词

原样保存、未折行——整段就是一整串，可以直接粘进 `MiniMax H3 Image to Video` 节点的 `prompt`。H3 的 prompt 分三段：`integrated_multimodal_description`（分镜 / 画面）、`overall_soundscape`（同期声）、`non_diegetic_music`（配乐）。

```text
integrated_multimodal_description: [Shot 1] Experimental collage-motion design: a chain-bound proof book opened flat, 16:9, printed edge to edge with no border. Golden-section page: thin white seams cut each page into a dominant 1.618:1 stage, a tall 0.618 side block and a low 0.382 base strip; each page reads as one wide composition — one big stage, one or two edge blocks, deep negative space — not a grid of equal tiles. Panels hold flat ink or macro material photographs — crushed stone, black silk, red velvet, blackened metal, pierced lattice — while type and one bright iron chain overrun the seams and the canvas edges, the chain running through every page and binding the book. Shared language: the arch-with-cross die, the twelve-spoke register wheel, red/black/white inks, chrome only on the die and needle, one hard red raking key from the left, grain, red fringing, bloom, vignette. Poster type is pseudo-Japanese in three layers — a giant glyph spanning the full width, a medium bar or column in the side block, 1px microtext in the seams — except the cross page, which uses a ring of flickering symbols, and the final dial, where engraved Roman numerals become the giant layer. Camera: IMPRESS (static push into a panel), SCAN (vertical slide down the page), SPIN (roll of the whole page). Opening page: a white stage with the giant black "神" cropped at both edges; the base strip is crushed stone with the chrome die in the rubble, red ink on its mirror-cut arch; the side block is black silk; the chain cuts diagonally through all three and exits the top-right corner; a red column "神は印刷された" in the seam, black microtext along the base seam. IMPRESS punches into the die; one white frame.

[Shot 2] At 00:00.400, the shot cuts to a page where the stage is a pierced stone lattice, the side block deep red glass, the base strip white paper; carved vine and light pins; the chain runs diagonal through all three and exits the right edge. Giant black half-glyph "聖" spans the full width and crops at both edges; red column "頁ごとに救われる" in the side seam; black microtext rules the base seam. SCAN tracks up the chain at grazing macro with large amplitude at fast speed, brakes at the apex; last two frames negative.

[Shot 3] At 00:00.900, the shot cuts to a golden board: crushed stone in the side block, black silk across the stage, red velvet in the base strip, three iron chains crossing every seam diagonally and running off the left and right edges; a black metal strip and a marble chip at the crossings; giant black "縛" spans the page, white columns "祈りは版になり、版は擦り切れた" and "十字架の在庫あり" in the side block, black-thread microtext in the seams. Whip pan left with large amplitude at fast speed along the chains, counterclockwise roll, brake; a chain rings.

[Shot 4] At 00:01.250, the shot cuts to black silk filling the stage and holds for 1.4 seconds in one continuous SPIN. The camera arcs slowly around the billowing cloth while the giant type above it hard-replaces every one or two frames — mostly single frames, about thirty changes — cycling "神は印刷された", "アーメン、赤", "鐘が鳴らない夜", "光あれ", "聖なるインク切れ", "第七印象", "刷り損じ", "インクは血", "骨まで赤い", "マリア・マリア・マリア" in alternating white and red, with a one-frame white-ground/black-type inversion every fourth change; three white columns on a black band in the side block re-set every fourth frame, black microtext ticks in the seams, and the chain crosses the base seam and exits the right edge. The side block is red velvet, the base strip crushed stone; the silk gusts slowly under the storm. This is the longest held image in the film and the only place where the type moves faster than the cut.

[Shot 5] At 00:02.650, the shot cuts to a burst of four single-frame page-cards in 0.10 seconds, hard strobe: stone stage with black "光"; metal side block with red "神は印刷された" and drilled dots; black velvet base strip stamped with the arch; the arch in white hairlines on black iron; the chain in a different corner each card. Static; the press stutters.

[Shot 6] At 00:02.750, the stage is a wall of raw chipped stone blocks, the seams cutting across it; the arch overprinted in one continuous IMPRESS push-in: ground twice, halftone three times, type layer four times, each on its own beat. Halftone is stippled pits flooded black, the giant type carved and flooded red and broken by the chipped edges, black microtext ruling the joints; the word cycles "神は印刷された", "第七印象", "刷り損じ", "インクは血". The red plate slips two millimeters here and stays slipped; the chain crosses the base seam and runs off the right edge.

[Shot 7] At 00:03.200, eight dense page-cards in 0.35 seconds, one frame each, the chain whipping through: "インクは血" etched in iron; "骨まで赤い" pressed into white velvet; "マリア・マリア・マリア" cut through a pierced metal screen; "第七印象" cut through a second screen; "刷り損じ" filled with stone dust; "聖なるインク切れ" printed on flat red; drilled red ticks on black stone; then a gray field of stippled pits collapsing the microtext and the medium lines, leaving one giant glyph. Static, strobe only.

[Shot 8] At 00:03.550, the stage is red velvet, still closed, a white seam down its middle; the side block white paper, the base strip crushed stone. Two black sleeves punch through and grip both halves; one hard pull sweeps the arms wide in under half the shot, fingers releasing as the velvet rips open, the halves snapping past the stage seams and white light flooding the page. The figure steps forward, arms wide and slightly past horizontal, the long sleeves and train overrunning the panel lines — pointed hood, void face, cope with stitched orphrey, stole with red crosses, bell sleeves whose long points whip and keep swinging after the body stops, knotted cincture with black beads, heavy train spilling off the bottom edge; hood, arms and train form the arch-and-cross silhouette. Matte black vestments, red rim on the left sleeve, red lining at the hem, contour only stitched hems and pleats. Giant red "聖" spans the full width behind, revealed as the panel tears; a black metal bar in the foreground carries red "赦しの再版"; black-thread microtext in the velvet; the chain crosses the base seam. Arms settle from overshoot into a wide cross. Camera pushes through the tear at fast speed; slip four millimeters.

[Shot 9] At 00:04.350, three inversion cycles on the settled figure — two frames black on white, two frames white on red — the chain flipping with it, a thin halo ring widening behind the hood. On the last frame the slip is six millimeters, the figure leaves a red ghost, the frame blows white.

[Shot 10] At 00:04.750, the seams fall away under one full-stage cross panel; a single white seam still crosses behind it. A towering blackened-bronze cross on a low plinth of stacked rough stone blocks under a tenth of its height — quatrefoil-pierced arms, crocketed buds hooking up, barley-twist shaft leaning a few degrees, two diagonal iron braces, a hollow boss pooled with red ink. The camera starts directly overhead, looking straight down the shaft as the arms foreshorten into a plus, the plinth a small block below; then it swings in one continuous vertical arc around the cross's axis, down past eye level to a steep low angle at the foot of the plinth, the wide lens tilted up so the cross towers over the top edge of the 16:9 frame and presses down into it, the arms converging overhead and the shaft bending with wide-angle distortion, the red key raking the metal and the cross throwing a hard shadow across the stones. The type is gone: a ring of pseudo-Japanese glyphs, registration crosses and tick marks orbits the cross in red, white and black, each symbol snapping on and off at its own frame, passing in front of and behind the arms, part of the ring running off both sides of the canvas. A V-cut "CRUX" stays on a stone block; the chain crosses the base seam. Slip six millimeters.

[Shot 11] At 00:06.050, the stage holds an unfinished marble angel, hands clasped, wings folded — chisel facets, drill marks, veins and dust in the creases, one rough wing overrunning the side seam — with crushed stone in the side block and white paper in the base strip; the chain crosses the page's elbow. SPIN at grazing macro from behind the rough wing to the face, red rim sliding along the chisel ridges. Giant red "祈" spans the top and crops at both edges; red column "肉は石に、石は頁に" in the side seam; "MATER" V-cut into a stone block; black engraved microtext down the robe.

[Shot 12] At 00:07.150, a crushed-stone field fills the stage and the base strip, thick red ink splattering across the chipped stones and running into the gaps, glossy on matte dust; chisel ticks and drilled rings, stippled pits, one carved glyph flooded red and cropped, black "インクは血" half swallowed; black microtext in the seams; the chain crosses the top and exits the left edge. Camera snaps a 90-degree clockwise roll as the ink lands, then brakes.

[Shot 13] At 00:07.650, the page becomes the dial: red bleeds to all four edges, the seams dissolving; engraved white Roman numerals I–XII ring the face like a clock, cropped at the canvas edges, black halftone wedges between them; a thin white circle and a ring of radial ticks enclose a large black diamond, its points reaching the ticks, holding the same unfinished marble angel, hands clasped, printed clean in black-and-white, perfectly still. The chain wraps once around the outer ring and exits the right edge. The dial turns in layers — numeral ring clockwise, tick ring counterclockwise, halftone wedges faster — the diamond and angel unmoving. Camera arcs into an overhead SPIN, numerals streaking and overrunning the frame.

[Shot 14] At 00:08.350, the dial complete: rings counter-rotating, the diamond fixed; a thin chrome needle slides out from behind it and sweeps the tick ring in a fast blur. A black band crosses the bottom edge with the white line "神は印刷されなかった", its last six characters eaten into holes showing red, so only "神は印刷" survives; 1px microtext fills the ticks. The numeral ring decelerates, XII returning to the top exactly as the needle snaps dead on it at 00:09.600; the chain slips free and falls out of frame; a last red splat lands across the numerals; the camera holds a slow overhead orbit with almost no roll, letting the dial turn. At 00:09.850 the printed sheet's corner lifts at the bottom-right edge and holds through 00:10.000. No fade.

overall_soundscape: Every cut lands with a dry paper slap over the low thud of a press closing, and the foreground changes with the material — chisel scrapes and stone grit, a dragged brush over velvet pile, a ringing scrape across metal burrs, wind threading the pierced lattice. The long silk hold is only fabric gusts, a soft chain tick and the room hum; the curtain rips open, the vestment cloth whips once, the rough stone blocks grind as the cross page falls past them. Red ink splats twice, the escapement runs under the needle sweep and ticks once as it stops, and the printed sheet's corner peels off with a dry crackle.

non_diegetic_music: Fully instrumental at 112 BPM in 4/4, syncopated and layered: a dry kick holds every cut, a distorted funk bass plays octave pops and ghost notes, a clavinet-like synth chops off-beat chords, gated snare and tape-hiss hats answer on displaced 16ths over a sidechained sub, and low brass-synth swells add weight; a thin two-note music-box phrase, shadowed by a detuned whistle, carries the weak melody. The track moves in four parts — stripped intro, build, cross, resolution: detuned saw stabs, a 16th-note arpeggio and bitcrushed percussion drive the build; at 00:04.750 the cross lands on a slammed synth-brass chord, a riser and filter sweep peak, the key steps up a whole tone, and a sustained analog-string chord is pulled upward through the 180-degree orbit. The long silk hold (01.250–02.650) drops the drums to a half-time bass, clavinet, arpeggio and music box; at 00:07.150 the low end falls to one synth tone and a noise swell, then kick, bass, clavinet, brass and toms return doubled under the dial, resolve on the raised tonic and stop dead at 00:09.700.
```

## 反向提示词

```text
（无）
```

T2VA 单提示词直出：工作流里没有负向编码器，材质、镜头、时间码、文字清单全部写在正向提示词里。

## 参数

| 项 | 值 |
| --- | --- |
| 底模 | `minimax_h3_fl2va_pruned_int8_convrot.safetensors` |
| 文本编码器 | `qwen3vl_32b_minimax_h3_int8_convrot.safetensors`（CLIP type = `minimax`） |
| VAE | 画面 `minimax_h3_sol_vae_int8_convrot.safetensors`；音频 `minimax_h3_audio_vae_fp32.safetensors` |
| LoRA | `pika_h3_flex_fl2va_v1_bf16.safetensors`，强度 1.0 |
| 采样器 | `lcm`（`SamplerCustomAdvanced` + `BasicGuider`，无 CFG） |
| 调度器 | `ManualSigmas`：`1.0, 0.972973, 0.923077, 0.8, 0.571429, 0.333333, 0.0` |
| 步数 | 6 |
| CFG | 不适用（`BasicGuider` 没有 CFG 输入） |
| 种子 | 112844716115522 |
| 分辨率 | 1344 × 768（16:9，0.96 MP，`ResolutionSelector`） |
| 时长 / 帧数 | duration 10 s → 243 帧 @ 24 fps = 10.125 s |
| 音频 | 与画面同一次生成（32 kHz 立体声），未使用外部音频 |
| 硬件 | RTX 3080 本地部署，约 99 s / step |

## 迭代记录

提示词一共改了 12 版（成片用 v12）。下面只写**能对上本地文件的变化**（v5–v12 共 8 份草稿）。

1. **v3–v4（结构期）**：先试「链条 + 校样书」的页面语法。v3 渲染 3 次、v4 渲染 2 次；这两版没留下提示词文件。
2. **v5**（8825 字符，15 镜，时间线到 00:07.000）：材质集定下来（碎石 / 黑丝 / 红绒 / 黑铁 / 镂空石格），`[Shot]` 逐镜写清每个分栏放什么。本版渲染 5 次。
3. **v6–v7**（9531 / 10395 字符，仍是 15 镜）：加厚分镜与声音层；v7 把时间线推到 00:08.300。
4. **v8–v9**（10627 / 11583 字符）：把表盘结尾的走针与 XII 归位写进具体时间码，时间线推到 00:09.850；分镜仍 15 个，但第 4–6 镜是连续的「单帧 page-card」抽卡（七张牌 → 黑丝 → 四张牌）。
5. **v10**（14 镜）：上面那几段单帧抽卡被合并成一镜——第 4 镜「黑丝连续 SPIN 1.4 秒，文字逐帧硬切」，成为全片最长的持留镜头；整条时间线同时前移（00:00.500 → 00:00.400 等）。
6. **v11**：把尾巴补到 10 秒——00:09.600 走针正点 XII、00:09.850 纸角起翘，hold 到 00:10.000，不淡出。
7. **v12 = final**：只重写 `non_diegetic_music` 一段。v11 是「16th-note feel + fingerstyle bass + 一堆零散乐器」的松散描述，v12 改成四段结构（stripped intro / build / cross / resolution）并钉死卡点：00:04.750 十字架落位、00:07.150 低频抽掉、00:09.700 骤停。这一版抽了 5 次（其中 2 次做了 4× 超分），成片取 `_00004_`。

整个 MISPRINT 系列共 18 次渲染（v3 三次、v4 两次、v5 五次、v6 之后各版共八次）。本地只留下 v5 起的草稿，v1–v4 没有提示词文件，只能从渲染文件名看出 v3、v4 跑过。

## 备注

- **后期**：只做了 RealESRGAN x4plus 逐帧超分（[`code/upscale/upscale_video.py`](../../code/upscale/upscale_video.py)），没有手工调色、剪辑、补帧或重绘。本目录的 `sample.mp4` 是未超分原片，B 站发布的是 4× 超分版；4× 文件 165 MB，没入库（仓库上限 100 MB）。
- **画面里的日文是伪日文**：提示词里明写 "pseudo-Japanese"，模型拼出来的字并不都能读通，这是设计的一部分。
- **种子**：`112844716115522`。工作流里它在子图实例的 `noise_seed` 上；子图内部的 `RandomNoise` 节点另存着 `20261220`（control_after_generate = randomize），容易看错。`sample.mp4` 的容器 metadata 里嵌着当时实际执行的 API prompt，`RandomNoise` 的值就是 `112844716115522`，可以对照。
- **灵感来源**：部分画面思路（几何排版与文字表现）来自 B 站 UP「AI幻想局局长」的[《MiniMax H3这个视觉效果谁敢信是一次抽卡...》](https://www.bilibili.com/video/BV1XvMy6iEvL/)。没有使用对方的画面、音频或提示词原文，只借鉴了「几何 + 文字」的排版方向。
- **已知问题**：10 秒里塞了 14 个镜头，00:02.650–00:03.550 那几镜「一帧一张卡」在 24 fps 下必然糊成频闪（提示词本来就是这么写的）；这是密度的代价，不是压缩问题。
