# WebGPU 渲染器详解

## 初始化与回退

```javascript
import { WebGPURenderer } from 'three/webgpu';

const renderer = new WebGPURenderer({
  antialias: false,           // 由后处理处理
  powerPreference: 'high-performance'
});
await renderer.init();        // 强制性！
```

不支持 WebGPU 时自动回退到 WebGL 2，无需单独代码路径。

## forceWebGL 选项

```javascript
const renderer = new WebGPURenderer({ forceWebGL: true });
```

用途：
- 测试 WebGL 回退行为
- 调试后端着色器编译差异
- 支持 WebGPU 尚不可用的特定 WebGL 扩展

## 特性检测

```javascript
const adapter = await navigator.gpu?.requestAdapter();
if (!adapter) {
  // 回退到 WebGL
  return;
}

const hasFloat32Filtering = adapter.features.has('float32-filterable');
const hasTimestamps = adapter.features.has('timestamp-query');

if (hasTimestamps) {
  const device = await adapter.requestDevice({
    requiredFeatures: ['timestamp-query']
  });
}
```

## TSL 完整指南

### 节点材质属性

```javascript
import { MeshStandardNodeMaterial } from 'three/webgpu';

const material = new MeshStandardNodeMaterial();
material.positionNode = positionLocal.add(displacement);
material.colorNode = vertexColor;
material.normalNode = customNormal;
material.emissiveNode = fresnel(normalWorld, viewDirection, 3.0).mul(color);
```

### 内置噪声函数

```javascript
import { 
  mx_noise_float, 
  mx_noise_vec3, 
  mx_fractal_noise_float 
} from 'three/tsl';

// 简单噪声
const n = mx_noise_float(positionLocal.mul(scale));

// 分形噪声 (带八度)
const fbm = mx_fractal_noise_float(positionLocal, octaves, lacunarity, gain);

// 3D 颜色噪声
const colorNoise = mx_noise_vec3(uv.mul(10));
```

### 存储纹理 (读写计算)

```javascript
import { storageTexture, textureStore, uvec2 } from 'three/tsl';

const outputTexture = new StorageTexture(width, height);
const store = textureStore(outputTexture, uvec2(x, y), computedColor);
```

### 工作组共享内存

```javascript
import { workgroupArray, workgroupBarrier } from 'three/tsl';

const sharedData = workgroupArray('float', 256);
sharedData.element(localIndex).assign(inputData);
workgroupBarrier(); // 同步所有线程
// 共享内存比全局内存快 10-100 倍
```

### 间接绘制 (GPU 驱动渲染)

```javascript
const drawIndirectBuffer = new IndirectStorageBufferAttribute(4, 'uint');

const cullCompute = compute(() => {
  // GPU 视锥剔除、LOD 选择
  if (visible) drawIndirectBuffer.element(1).atomicAdd(1);
});

mesh.drawIndirect = drawIndirectBuffer;
```

## 异步渲染

计算密集型场景使用 renderAsync：

```javascript
async function animate() {
  await renderer.renderAsync(scene, camera);
  requestAnimationFrame(animate);
}
```

确保计算通道在依赖渲染通道前完成。

## 缓冲区更新优化

```javascript
// ❌ 多次小更新
particles.forEach(p => p.buffer.update());

// ✅ 单次批量更新
const data = new Float32Array(particles.length * 4);
particles.forEach((p, i) => data.set(p.data, i * 4));
batchBuffer.update(data);
```

## 地形生成示例

```javascript
const heightmap = storageTexture(resolution, resolution);

const terrainCompute = compute(() => {
  const uv = uvec2(instanceIndex.mod(resolution), instanceIndex.div(resolution));
  const height = mx_noise_float(uv.mul(scale)).mul(amplitude);
  textureStore(heightmap, uv, vec4(height, 0, 0, 1));
});
```

## 调试

1. Chrome GPU 调试: `chrome://gpu`
2. 启用 "WebGPU Developer Features" in `chrome://flags`
3. 性能面板跟踪 GPU 工作
4. 控制台着色器编译错误比 WebGL 更详细
