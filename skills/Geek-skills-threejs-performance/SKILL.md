---
name: Geek-skills-threejs-performance
version: 1.0.0
description: Three.js 性能优化专家指南，涵盖 WebGPU 渲染器、资源压缩、绘制调用优化、内存管理、着色器优化、光照阴影、React Three Fiber、后处理等100+最佳实践。适用于：(1) 优化 Three.js 项目性能，(2) 迁移到 WebGPU 渲染器，(3) 减少绘制调用和内存泄漏，(4) 实现高效粒子系统和物理模拟，(5) 配置后处理效果，(6) React Three Fiber 性能调优。触发关键词："Three.js 优化"、"WebGPU"、"绘制调用"、"draw calls"、"性能瓶颈"、"内存泄漏"、"TSL 着色器"、"InstancedMesh"、"BatchedMesh"、"R3F 优化"等。
---

# Three.js 性能优化指南 (2026)

## 核心原则

**黄金法则：绘制调用 < 100 次/帧**

- 三角形数量不如绘制调用数量重要
- 使用 `renderer.info.render.calls` 监控
- 超过 500 次绘制调用，即使强大 GPU 也会吃力

## 快速诊断清单

```javascript
// 性能监控必备
setInterval(() => {
  console.log('调用:', renderer.info.render.calls);
  console.log('三角形:', renderer.info.render.triangles);
  console.log('几何体:', renderer.info.memory.geometries);
  console.log('纹理:', renderer.info.memory.textures);
}, 1000);
```

如果数值持续增长，存在内存泄漏。

## WebGPU 渲染器

### 何时迁移

在以下情况迁移到 WebGPU：
- 绘制调用密集场景掉帧
- 需要计算着色器进行物理/粒子模拟
- 复杂后处理链导致卡顿

### 基础设置

```javascript
import { WebGPURenderer } from 'three/webgpu';

const renderer = new WebGPURenderer();
await renderer.init(); // 必需！

function animate() {
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
```

浏览器支持：Chrome/Edge v113+，Firefox v141+，Safari v26+

### TSL (Three 着色器语言)

编写一次，自动编译为 WGSL (WebGPU) 或 GLSL (WebGL)：

```javascript
import { color, positionLocal, sin, time, Fn, float } from 'three/tsl';

// 基础用法
material.colorNode = color(1, 0, 0).mul(sin(time).mul(0.5).add(0.5));

// 可复用函数
const fresnel = Fn(([normal, viewDir, power]) => {
  const dotNV = normal.dot(viewDir).saturate();
  return float(1).sub(dotNV).pow(power);
});
```

### 计算着色器粒子系统

CPU 粒子约 50,000 个遇到瓶颈，GPU 计算着色器可达数百万：

```javascript
import { instancedArray, storage, compute } from 'three/tsl';

const positions = instancedArray(particleCount, 'vec3');
const velocities = instancedArray(particleCount, 'vec3');

const physicsCompute = compute(() => {
  const pos = positions.element(instanceIndex);
  const vel = velocities.element(instanceIndex);
  positions.element(instanceIndex).assign(pos.add(vel.mul(deltaTime)));
});

renderer.compute(physicsCompute);
```

## 绘制调用优化

### InstancedMesh (重复对象)

1,000 棵树 → 从 1,000 次绘制调用降为 1 次：

```javascript
const mesh = new InstancedMesh(geometry, material, 1000);
for (let i = 0; i < 1000; i++) {
  matrix.setPosition(positions[i]);
  mesh.setMatrixAt(i, matrix);
}
```

### BatchedMesh (不同几何体)

共享材质的多个不同几何体合并为单次绘制：

```javascript
const batchedMesh = new BatchedMesh(maxGeometries, maxVertices, maxIndices, material);
```

### 共享材质

```javascript
// ❌ 每个网格新材质
meshes.forEach(m => m.material = new MeshStandardMaterial({ color: 'red' }));

// ✅ 共享材质
const sharedMaterial = new MeshStandardMaterial({ color: 'red' });
meshes.forEach(m => m.material = sharedMaterial);
```

### 合并静态几何体

```javascript
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
const merged = mergeGeometries([geo1, geo2, geo3]);
```

## 资源优化

### 压缩命令

```bash
# Draco 几何体压缩 (减少 90-95%)
gltf-transform draco model.glb compressed.glb --method edgebreaker

# KTX2 纹理压缩 (GPU 内存减少约 10 倍)
gltf-transform uastc model.glb optimized.glb  # 高质量
gltf-transform etc1s model.glb optimized.glb  # 小体积

# 完整优化管线
gltf-transform optimize model.glb output.glb \
  --texture-compress ktx2 \
  --compress draco
```

### 解码器配置

```javascript
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/draco/');

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('/basis/');
```

## 内存管理

**关键：Three.js 不会自动垃圾回收 GPU 资源！**

### 完整释放模式

```javascript
function cleanupMesh(mesh) {
  mesh.geometry.dispose();
  
  if (Array.isArray(mesh.material)) {
    mesh.material.forEach(mat => {
      Object.values(mat).forEach(prop => {
        if (prop?.isTexture) prop.dispose();
      });
      mat.dispose();
    });
  } else {
    Object.values(mesh.material).forEach(prop => {
      if (prop?.isTexture) prop.dispose();
    });
    mesh.material.dispose();
  }
  
  scene.remove(mesh);
}

// GLTF ImageBitmap 特殊处理
texture.source.data.close?.();
texture.dispose();
```

### 对象池模式

```javascript
class ObjectPool {
  constructor(factory, reset, initialSize = 20) {
    this.factory = factory;
    this.reset = reset;
    this.pool = Array.from({ length: initialSize }, () => {
      const obj = factory();
      obj.visible = false;
      return obj;
    });
  }
  
  acquire() {
    const obj = this.pool.pop() || this.factory();
    obj.visible = true;
    return obj;
  }
  
  release(obj) {
    this.reset(obj);
    obj.visible = false;
    this.pool.push(obj);
  }
}
```

## 着色器优化

### 移动端优先

```glsl
precision mediump float;  // 比 highp 快约 2 倍
```

### 无分支替代

```glsl
// ❌ 分支破坏 GPU 并行性
if (value > 0.5) color = colorA; else color = colorB;

// ✅ 无分支
color = mix(colorB, colorA, step(0.5, value));
```

### 数据打包

```glsl
vec4 data = texture2D(dataTex, uv);
// 4 个值只需 1 次纹理获取
float v1 = data.r, v2 = data.g, v3 = data.b, v4 = data.a;
```

## 光照和阴影

- 活动光源 ≤ 3 个
- PointLight 阴影 = 6 次阴影贴图渲染/光源
- 阴影贴图尺寸：移动 512-1024，桌面 1024-2048
- 静态场景烘焙光照贴图

```javascript
// 静态场景禁用阴影自动更新
renderer.shadowMap.autoUpdate = false;
renderer.shadowMap.needsUpdate = true; // 需要时手动触发
```

## React Three Fiber

### 核心规则

```javascript
// ❌ 触发 React 重新渲染
const [rotation, setRotation] = useState(0);
useFrame(() => setRotation(r => r + 0.01));

// ✅ 直接修改
const meshRef = useRef();
useFrame((state, delta) => {
  meshRef.current.rotation.x += delta * speed; // 帧率无关
});
```

### 按需渲染

```jsx
<Canvas frameloop="demand">
  <Scene />
</Canvas>

// 需要时触发
const invalidate = useThree(state => state.invalidate);
invalidate();
```

### 切换可见性而非重新挂载

```jsx
// ❌ 卸载/挂载重建资源
{showModel && <Model />}

// ✅ 可见性切换
<Model visible={showModel} />
```

## 后处理

### WebGL 使用 pmndrs/postprocessing

```javascript
import { EffectComposer, Bloom, Vignette } from 'postprocessing';

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new EffectPass(camera, new Bloom(), new Vignette()));
```

### WebGPU 使用原生 TSL 后处理

```javascript
import { pass, bloom, fxaa } from 'three/tsl';

const postProcessing = new PostProcessing(renderer);
const scenePass = pass(scene, camera);
postProcessing.outputNode = scenePass.pipe(bloom()).pipe(fxaa());
```

## 调试工具

- **stats-gl**: FPS/CPU/GPU 监控
- **lil-gui**: 实时参数调整
- **Spector.js**: WebGL 帧捕获
- **three-mesh-bvh**: 快速射线检测 (80,000+ 多边形 @ 60fps)
- **r3f-perf**: React Three Fiber 性能监控

## 详细参考

- **WebGPU 详解**: 见 [references/webgpu.md](references/webgpu.md)
- **资源优化指南**: 见 [references/assets.md](references/assets.md)
- **完整代码示例**: 见 [references/examples.md](references/examples.md)
