# Scene Distillation Zine v1.3

Turn a supplied photo into an original, expressive zine-poster illustration. The source image informs the idea and composition, but no photographic pixels, tracing, collage, or photorealistic regions appear in the finished artwork.

中文版说明见下方。

## What it does

- Distils a photo into an editorial, paper-based illustration with generous negative space.
- Preserves the source's emotional and semantic core instead of copying its literal composition.
- Supports portrait `3:5` and landscape `5:3` outputs.
- Uses one purposeful high-chroma accent by default.
- Enables a strict one-contiguous-color-field treatment with the exact Chinese trigger `单色块模式`.

## Install

### Option 1 — Ask Codex to install it

After this repository is on GitHub, ask Codex:

```text
Use $skill-installer to install the skill at https://github.com/<OWNER>/scene-distillation-zine-v1-3/tree/main/skills/scene-distillation-zine-v1-3
```

Replace `<OWNER>` with the GitHub account or organization that owns this repository. The skill will be available in the next Codex task.

### Option 2 — Install manually

```bash
git clone https://github.com/<OWNER>/scene-distillation-zine-v1-3.git
mkdir -p ~/.codex/skills
cp -R scene-distillation-zine-v1-3/skills/scene-distillation-zine-v1-3 ~/.codex/skills/
```

Start a new Codex task after installation.

## Use

Attach a photo, then ask in Chinese or English:

```text
Use $scene-distillation-zine-v1-3 to transform this photo into an expressive zine illustration.
```

For the strict single-color-field variant, include the exact trigger:

```text
用 $scene-distillation-zine-v1-3 的单色块模式处理这张图片
```

## Requirements

- Codex with image-generation access.
- A user-supplied reference photo.

## Privacy

The skill instructs Codex to use the photo only as a semantic and visual reference. It does not direct Codex to browse, share, or save the source image. The generation service receives the reference image and generation prompt when an image is created.

## License

Released under the [MIT License](LICENSE).

---

# 中文说明

这是一个把用户照片转化为原创纸刊风插画海报的 Codex Skill。它提取照片中的情绪、关系和视觉线索重新创作，成图不会保留原照片像素，也不做描摹、拼贴或写实复制。

## 它能做什么

- 将照片蒸馏为具有留白、纸张质感和编辑性表达的插画海报。
- 保留照片的情感核心，而非照搬构图。
- 自动适配竖版 `3:5` 和横版 `5:3`。
- 默认使用一个有明确作用的高饱和色彩重点。
- 在请求中出现精确触发词 `单色块模式` 时，切换为「一整块高饱和彩色 + 中性墨色」的严格模式。

## 安装

### 方式一：让 Codex 安装（推荐）

仓库发布到 GitHub 后，直接对 Codex 说：

```text
Use $skill-installer to install the skill at https://github.com/<OWNER>/scene-distillation-zine-v1-3/tree/main/skills/scene-distillation-zine-v1-3
```

把 `<OWNER>` 改成你的 GitHub 用户名或组织名。安装完成后，在下一次 Codex 任务中即可使用。

### 方式二：手动安装

```bash
git clone https://github.com/<OWNER>/scene-distillation-zine-v1-3.git
mkdir -p ~/.codex/skills
cp -R scene-distillation-zine-v1-3/skills/scene-distillation-zine-v1-3 ~/.codex/skills/
```

安装完成后，新开一个 Codex 任务。

## 使用方式

上传照片后输入：

```text
用 $scene-distillation-zine-v1-3 把这张图片变成一张具有艺术表达的纸刊插画海报
```

如需严格单色块风格，必须带上准确触发词：

```text
用 $scene-distillation-zine-v1-3 的单色块模式处理这张图片
```

## 使用条件与隐私

- 需要具备图片生成能力的 Codex。
- 需要由用户上传参考照片。
- Skill 只将原图用作语义和视觉参考；不会要求浏览、分享或保存原图。生成时，图片生成服务会接收原图和生成指令。

## 许可

本项目使用 [MIT License](LICENSE) 开源。
