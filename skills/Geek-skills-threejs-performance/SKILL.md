---
name: Geek-skills-threejs-performance
version: 1.1.0
description: Three.js 性能优化指南。当 Three.js/React Three Fiber 项目出现掉帧、内存增长、加载缓慢、绘制调用过多，或需要迁移 WebGPU、实现大规模粒子/实例化渲染、配置资源压缩管线时使用。触发关键词："Three.js 优化"、"WebGPU"、"draw calls"、"内存泄漏"、"TSL"、"InstancedMesh"、"R3F 优化"等。不用于：通用 React 性能问题（用 vercel-react-best-practices）、WebGL/Three.js 入门教学、3D 美术资产的制作本身。
---

# Three.js 性能优化指南

## 黄金法则

**绘制调用 < 100 次/帧。** 三角形数量不如绘制调用数量重要；超过 500 次绘制调用，强大 GPU 也会吃力。用 `renderer.info.render.calls` 监控（完整监控代码见 `references/examples.md`）。

## 诊断决策树

| 症状 | 先查 | 深入 |
|------|------|------|
| 掉帧、卡顿 | `renderer.info.render.calls` 是否 >100 | 实例化/合批（下文），后处理链 |
| 内存持续增长 | `renderer.info.memory` 的 geometries/textures 计数是否只增不减 | dispose 铁律（下文），`references/examples.md` 完整清理代码 |
| 加载慢、显存爆 | 模型是否未压缩 | `references/assets.md` 压缩管线 |
| 粒子/物理瓶颈 | CPU 粒子是否 >5 万 | WebGPU 计算着色器，`references/webgpu.md` |
| R3F 项目莫名重渲染 | useFrame 里是否 setState | R3F 三规则（下文） |

## 各领域规则速查

### WebGPU：何时迁移
绘制调用密集掉帧 / 需要计算着色器做物理粒子（CPU 约 5 万上限，GPU 可达数百万）/ 复杂后处理链卡顿。
`WebGPURenderer` 必须 `await renderer.init()`。TSL 写一次自动编译 WGSL/GLSL。
浏览器支持下限（记录时点数据，现查 caniuse 为准）：Chrome/Edge 113+，Firefox 141+，Safari 26+。
初始化回退、TSL 完整指南、计算着色器示例：`references/webgpu.md`。

### 绘制调用优化
- 大量**相同**几何体（树、石头）→ `InstancedMesh`：1000 棵树 = 1 次绘制
- 多个**不同**几何体共享材质 → `BatchedMesh`
- 静态小物件 → `mergeGeometries` 合并
- 材质**共享复用**，永远不要在循环里 `new Material`

### 资源压缩（收益数字）
- Draco 几何体压缩：体积减 90-95%
- KTX2 纹理：GPU 内存约降 10 倍
- 一条命令：`gltf-transform optimize model.glb out.glb --texture-compress ktx2 --compress draco`
- 解码器路径配置与 Meshopt/Draco 选型：`references/assets.md`

### 内存铁律
**Three.js 不会自动回收 GPU 资源。** 移除对象必须：geometry.dispose() + 遍历 material 的所有 texture 属性逐个 dispose + material.dispose()；GLTF 的 ImageBitmap 还要 `texture.source.data.close()`。频繁增删对象用对象池。完整代码：`references/examples.md`。

### 着色器三规则
① 移动端 `precision mediump float`（约快 2 倍）② 用 `mix/step` 替代 if 分支（分支破坏 GPU 并行）③ 数据打包进 vec4，一次纹理取 4 个值。

### 光照阴影预算
活动光源 ≤3；PointLight 阴影 = 每光源 6 次阴影贴图渲染；贴图尺寸移动端 512-1024、桌面 1024-2048；静态场景 `shadowMap.autoUpdate = false` 手动触发 + 烘焙光照。

### React Three Fiber 三规则
① 动画走 `useFrame` 直改 ref，**永远不在 useFrame 里 setState** ② 静态场景用 `frameloop="demand"` + `invalidate()` 按需渲染 ③ 显隐切 `visible` 属性，不要条件挂载 `{show && <Model/>}`（重挂载重建资源）。完整优化模板：`references/examples.md`。

### 后处理选型
WebGL → `pmndrs/postprocessing`（多效果合并 EffectPass）；WebGPU → 原生 TSL 后处理管线。两者完整设置：`references/examples.md`。

## 验收标准（优化任务完成前自查）

- [ ] `renderer.info.render.calls` < 100（超出需给出场景理由）
- [ ] `renderer.info.memory` 计数在增删对象后回落，无单调增长
- [ ] 目标设备实测帧率达标（移动端也要测，不只桌面）
- [ ] 发布资源经过 Draco/KTX2 压缩管线
- [ ] 每条优化建议都对应用户场景的实测症状，不是清单式全量套用

## 不做什么

- React 组件层的通用性能问题（memo/useMemo/bundle）→ `vercel-react-best-practices`
- Three.js 基础教学、场景搭建入门
- 模型/贴图美术制作本身（只管加载与渲染性能）
- 未量测先优化：没有 renderer.info 或帧率数据时，先装监控再动手

## 已知陷阱

| 陷阱 | 具体表现 | 应对 |
|------|---------|------|
| dispose 不彻底 | 只 dispose 了 geometry，material 上挂的 texture 全泄漏 | 遍历 material 属性逐个 dispose；GLTF ImageBitmap 还需 close() |
| useFrame 里 setState | 每帧触发 React 重渲染，帧率断崖 | 直改 ref；状态只在交互事件里更新 |
| 条件挂载切换模型 | `{show && <Model/>}` 每次重建几何体和纹理 | 切 visible 属性 |
| demand 模式忘 invalidate | 相机动了画面不动，被当成"卡死" | 交互回调里调用 invalidate() |
| 循环里 new Material | 1000 个网格 1000 个材质，合批全部失效 | 材质提到循环外共享 |
| PointLight 随手加阴影 | 一个点光 6 次阴影渲染，移动端直接跪 | 优先 SpotLight/DirectionalLight 阴影，点光阴影只留一个 |

## 调试工具

**stats-gl**（FPS/CPU/GPU）· **lil-gui**（实时调参）· **Spector.js**（WebGL 帧捕获）· **three-mesh-bvh**（8 万+ 面 @60fps 射线检测）· **r3f-perf**（R3F 监控）

## 参考文档（按需加载）

| 文件 | 何时读 |
|------|--------|
| `references/webgpu.md` | 迁移 WebGPU / 写 TSL / 计算着色器时 |
| `references/assets.md` | 配置压缩管线、LOD、渐进加载时 |
| `references/examples.md` | 需要完整可粘贴代码时（监控/内存清理/对象池/粒子/R3F 模板/后处理/上下文丢失恢复） |
