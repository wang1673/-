# 前 200 个任务：阶段结果

已完成当前阶段的生成与客观评测，余下 550 个任务保持暂停。
任务按原配置顺序选取：13 首完整歌曲和第 14 首的前 5 个任务（当上限为 200 时）。
这是便于检查效果的顺序子集，不代表全部 750 个任务的最终表现。

| 指标 | 均值 | 总体标准差 | 有效任务 |
| --- | ---: | ---: | ---: |
| CLAP | 0.366880 | 0.079560 | 200 |
| LPAPS | 4.785495 | 0.465056 | 200 |
| CQT1_PCC | 0.312406 | 0.216796 | 200 |

## 试听对比

以下按编辑分轨选取不同歌曲的例子，未按客观分数筛选。比较原混音和编辑结果时，留意目标音色、非目标伴奏、旋律节奏和伪影。

- AM Contra - Heart Peripheral / vocals2violin：A recording of a smooth violin, deep bass, atmospheric synth and punchy drums.
  服务器试听路径：`review_first200/01-vocals-vocals2violin/source.wav` / `review_first200/01-vocals-vocals2violin/edited.wav`
- Detsky Sad - Walkie Talkie / vocals2marimba：A recording of a resonant marimba, deep bass, distorted electric guitar and punchy drums.
  服务器试听路径：`review_first200/02-vocals-vocals2marimba/source.wav` / `review_first200/02-vocals-vocals2marimba/edited.wav`
- AM Contra - Heart Peripheral / drums2electronic：A recording of soulful female vocals, deep bass, atmospheric synth and crisp electronic drums.
  服务器试听路径：`review_first200/03-drums-drums2electronic/source.wav` / `review_first200/03-drums-drums2electronic/edited.wav`
- Enda Reilly - Cur An Long Ag Seol / drums2taiko：A recording of a soft male vocals, a fingerpicked acoustic guitar, a warm bass guitar and powerful taiko drums.
  服务器试听路径：`review_first200/04-drums-drums2taiko/source.wav` / `review_first200/04-drums-drums2taiko/edited.wav`
- AM Contra - Heart Peripheral / bass2upright：A recording of soulful female vocals, an upright bass, atmospheric synth and punchy drums.
  服务器试听路径：`review_first200/05-bass-bass2upright/source.wav` / `review_first200/05-bass-bass2upright/edited.wav`
- Enda Reilly - Cur An Long Ag Seol / bass2synth：A recording of a soft male vocals, a fingerpicked acoustic guitar, a smooth synth bass and light percussion or brush snare.
  服务器试听路径：`review_first200/06-bass-bass2synth/source.wav` / `review_first200/06-bass-bass2synth/edited.wav`
- AM Contra - Heart Peripheral / guitar2piano：A recording of soulful female vocals, deep bass, a bright piano and punchy drums.
  服务器试听路径：`review_first200/07-other-guitar2piano/source.wav` / `review_first200/07-other-guitar2piano/edited.wav`
- Forkupines - Semantics / guitar2choir：A recording of a clear male vocals, a powerful choir, a tight bass guitar and fast drums.
  服务器试听路径：`review_first200/08-other-guitar2choir/source.wav` / `review_first200/08-other-guitar2choir/edited.wav`

裁剪为每首中间 10 秒；作者未公开准确裁剪清单。本阶段不能宣称精确重现论文表 1。
全部已生成音频仍保存在 audio/；逐任务分数见 metrics/per_task.first200.csv。

详细独立校验见 [stage200.audit.json](records/stage200.audit.json)。8 组试听仅保留在服务器和本机交付目录，不上传公开仓库。没有执行主观试听或 MOS。
