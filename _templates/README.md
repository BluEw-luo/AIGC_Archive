# 模板说明

新增一件作品时，在本目录复制 `prompt.md` 和 `meta.json`：

```bash
cp -r _templates prompts/2026-03-my-work
```

然后：

1. 改名 `2026-03-my-work` → `YYYY-MM-<slug>`，slug 用小写英文和连字符；
2. 填写 `prompt.md`：提示词原样粘贴，参数表填全，迭代记录尽量具体；
3. 填写 `meta.json`：`slug` 与目录名保持一致，`media` 列出实际文件名；
4. 放入成图 `01.png`、`02.png`……（正文图按顺序编号）；
5. 从 ComfyUI 导出工作流：菜单 `Workflow → Save`，存为本目录的 `workflow.json`；
   若需要给脚本调用，再 `Export (API)` 存为 `workflow.api.json`；
6. 提交：`git add prompts/2026-03-my-work && git commit -m "add: 2026-03-my-work"`。

## 注意

- **不要删 `human_authorship` 字段**。它记录你的创作投入，是将来主张权利时最重要的证据；
- 改编自他人提示词的部分，在 `credits` 里写清来源，并确认原作者允许再分发；
- `model_license` 请照抄底模的许可名称，不要凭印象写。
