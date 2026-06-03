# Color Grade Philosophy

## 色彩风格哲学

我一直觉得，好看的调色不是“套一个滤镜”那么简单。

有些摄影大师的照片，明明颜色不夸张，却很耐看。肤色、阴影、冷暖、灰度、对比，全都像被轻轻拿捏过。以前我只会说“好看”，但说不出为什么好看。

所以我做了这个 Skill：它可以解析摄影作品中的色彩风格，拆出创作者到底在怎么处理色彩，以及这些色彩为什么成立。

它不是让你机械复制某张图的调色，而是先理解背后的调色哲学：这张照片为什么压暗高光？为什么阴影偏青？为什么整体降低饱和度反而更高级？为什么某种肤色处理会显得安静、克制、真实？

以后看到喜欢的照片，你可以把它收藏成风格包。等你要修自己的照片时，它会基于你过去收藏过的审美偏好，推荐更适合当前照片的调色方向。

我最喜欢的一点是：它不是帮你“偷一个风格”，而是帮你慢慢看懂风格。

相比直接套用，我更想学会理解。因为真正提升审美的，不是拥有多少预设，而是知道一张照片为什么动人。

I have always felt that beautiful color grading is not as simple as applying a filter.

Some great photographs are not visually loud, yet they remain deeply memorable. Skin tone, shadows, warmth, coolness, grayness, and contrast all feel gently and precisely handled. I used to simply say “this looks good,” but I could not explain why.

That is why I created this Skill. It analyzes photographic color styles and breaks down how a creator handles color, and more importantly, why those choices work.

It does not ask you to mechanically copy the grading of a reference image. Instead, it tries to understand the color philosophy behind it: Why are the highlights compressed? Why do the shadows lean cyan? Why does lower saturation sometimes feel more refined? Why does a certain skin-tone treatment feel quiet, restrained, and real?

When you see a photograph you love, you can save it as a reusable style package. Later, when you edit your own photos, the Skill can recommend a grading direction based on your saved visual preferences and the actual needs of the target image.

My favorite part is this: it does not help you “steal a style.” It helps you slowly learn how to see style.

Compared with direct application, I care more about understanding. Because what truly improves aesthetic judgment is not owning more presets, but knowing why an image is moving.

## 核心理念 / Core Idea

迁移调色师的决策逻辑，而不是参考图表面的颜色。

大多数 AI 风格迁移会把参考图当成调色盘，直接复制颜色。这很容易导致脆弱的结果：草地被染成海水蓝，皮肤变冷，食物失去食欲感，产品颜色偏移，目标照片也不再像它自己。

Color Grade Philosophy 的目标不是复制颜色，而是重建调色判断。

Transfer the colorist’s decision logic, not the source image’s surface colors.

Most AI style-transfer workflows treat a reference image as a palette source. This often creates brittle results: grass becomes ocean blue, skin turns cold, food loses appetite, product colors drift, and the target scene stops feeling like itself.

Color Grade Philosophy is not about copying colors. It is about rebuilding grading decisions.

## 工作流 / Workflow

```text
解析 -> 打包 -> 推荐 -> 语义适配 -> 生成模型参考版 -> 输出本地原尺寸调色版 -> 质检

Analyze -> Package -> Recommend -> Adapt -> Generate model reference -> Produce local full-resolution grade -> Quality check
```

这个 Skill 会把参考照片视为一种“调色哲学”的证据：情绪意图、明暗结构、色相策略、主体保护、质感处理、场景依赖和失败风险。

它会先判断目标照片是否真的适合某个风格，而不是把所有风格都强行套上去。

This Skill treats a reference photo as evidence of a grading philosophy: emotional intent, tonal architecture, hue strategy, subject protection, texture, scene dependency, and failure risks.

It first decides whether a target image actually benefits from a style, instead of forcing every look onto every photo.

## 风格包 / Style Packages

保存下来的风格不是一个 prompt，而是一个结构化风格包。它同时包含客观色彩信息和主观调色判断。

一个有效的风格包包括：

```text
style_philosophy
semantic_transfer_rules
compatibility
technical_profile
model_prompt
retrieval metadata
```

这样风格就可以被收藏、检索、推荐、复用，并在不同照片之间做语义化适配。

A saved style is not just a prompt. It is a structured style package containing both objective color information and subjective colorist reasoning.

A useful style package includes:

```text
style_philosophy
semantic_transfer_rules
compatibility
technical_profile
model_prompt
retrieval metadata
```

This makes styles collectible, searchable, recommendable, reusable, and adaptable across different photographs.

## 语义化色彩迁移 / Semantic Color Transfer

这个 Skill 不会盲目地把一种物体的颜色复制到另一种物体上，而是根据目标场景的语义重新映射调色策略。

比如，参考图是海边，使用了青蓝色海水和深蓝阴影；目标图是山地草原。正确做法不是把草地变成海水蓝，而是保持草地的绿色身份，同时降低饱和度并冷却到鼠尾草绿或橄榄绿；森林阴影可以推向蓝绿或深蓝；岩石保持冷灰；皮肤保留暖色；白色衣物不被污染。

这就是“调色哲学迁移”，而不是“颜色复制”。

This Skill does not blindly copy colors from one object type to another. It remaps the grading strategy according to the semantics of the target scene.

For example, if a seaside reference uses cyan water and navy shadows, and the target image is a mountain grassland, the right move is not to turn grass into ocean blue. Instead, grass should remain green while being muted and cooled toward sage or olive; forest shadows may move toward blue-green or navy; rocks stay cool slate gray; skin keeps its warmth; white clothing remains clean.

This is philosophical color transfer, not color copying.

## 兼容性模式 / Compatibility Modes

在应用风格前，Skill 会先判断适配强度：

```text
direct_apply   -> 参考图和目标图高度相似，可以直接应用
semantic_adapt -> 风格哲学可迁移，但需要语义重映射
inspired_only  -> 只能借用少量气质或处理方式
reject         -> 风格会破坏图像用途或主体真实性，应拒绝
```

Before applying a style, the Skill first decides the adaptation mode:

```text
direct_apply   -> source and target are highly similar
semantic_adapt -> the philosophy transfers, but needs remapping
inspired_only  -> borrow only a few ideas
reject         -> the style would damage the image purpose or subject truth
```

## 双轨最终输出 / Dual-Track Final Output

对于本地图片调色，这个 Skill 使用“保真优先”的双轨输出机制。

第一轨是 **生图模型参考版**。它使用图像编辑模型理解风格哲学，展示审美方向。这个版本适合判断气质和方向，但可能改变像素、细节或尺寸。

第二轨是 **原尺寸本地调色版**。它基于同一个语义适配方案，在本地对原图做确定性调色，保留原始尺寸、构图、身份、物体和局部色彩真实性。默认情况下，这个版本才是最终交付版。

For local image grading, this Skill uses a preservation-first dual-output workflow.

The first output is a **model reference grade**. It uses an image editing model to interpret the style philosophy and show the intended creative direction. This version is useful for mood and taste alignment, but it may alter pixels, details, or dimensions.

The second output is a **full-resolution local grade**. It applies a deterministic local color grade to the original image using the same semantic adaptation plan, preserving the original dimensions, composition, identity, objects, and local color truth. By default, this is the delivery asset.

## 仓库结构 / Repository Layout

```text
.
├── SKILL.md
├── agents/
├── scripts/
├── references/
├── color-styles/
│   ├── <style-id>/
│   │   ├── style.json
│   │   ├── reference.<ext>
│   │   ├── thumbnail.jpg
│   │   └── swatches.png
│   └── _index/recent-styles.json
└── analysis/
    ├── color-grade-philosophy-report.md
    ├── color-grade-philosophy-report.zh.md
    ├── style-index.json
    └── contact-sheet.jpg
```

## 使用方式 / Usage

设置共享风格库位置：

Set a shared style-library location:

```bash
export COLOR_GRADE_STYLES_ROOT="/path/to/color-styles"
```

解析一张参考图并创建风格包：

Analyze a reference image and create a style package:

```bash
python scripts/create_style_package.py reference.jpg --name "Quiet Green Portrait"
```

刷新最近风格索引：

Refresh the recent-style index:

```bash
python scripts/index_style_library.py --styles-root color-styles
```

为目标图做客观色彩分析：

Extract an objective color profile from a target image:

```bash
python scripts/extract_image_profile.py target.jpg --out target-profile.json
```

为目标场景推荐风格：

Score style compatibility for a target scene:

```bash
python scripts/score_style_fit.py --styles-root color-styles --target-scene "mountain travel portrait" --has-human --has-sky
```

## 素材边界 / Asset Notes

这个仓库中的风格包用于研究和审美分析。若你准备公开发布或商业使用，请确认参考图、缩略图、拼图和示例图的授权状态；如果没有明确授权，建议只公开 `style.json`、色板、分析文本和你自己拥有版权的示例图。

The style packages in this repository are intended for research and aesthetic analysis. Before public release or commercial use, verify the rights for reference images, thumbnails, contact sheets, and examples. If rights are unclear, publish only `style.json`, swatches, analysis text, and examples you own.

## 为什么需要它 / Why It Exists

调色不是复制调色盘。好的调色会保护主体、尊重场景，并做出有意识的取舍。

Color Grade Philosophy 把这种调色判断变成一个可复用的工作流：能解析、能保存、能推荐、能适配，也能避免很多一次性 prompt 带来的失真和漂移。

它最终想做的不是让你拥有更多滤镜，而是帮你更清楚地看见：一张照片为什么动人。

Color grading is not palette copying. A good grade protects the subject, respects the scene, and makes deliberate tradeoffs.

Color Grade Philosophy turns this kind of colorist reasoning into a reusable workflow: it can analyze, save, recommend, adapt, and reduce the distortion and drift that often come with one-off prompts.

Its ultimate goal is not to give you more filters, but to help you see more clearly why a photograph moves you.
