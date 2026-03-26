# 资源优化指南

## GLTF 压缩工具链

### gltf-transform CLI

```bash
# 安装
npm install -g @gltf-transform/cli

# 仅 Draco 压缩
gltf-transform draco input.glb output.glb --method edgebreaker

# 仅 KTX2 纹理
gltf-transform uastc input.glb output.glb    # 高质量
gltf-transform etc1s input.glb output.glb    # 小体积

# 完整优化 (推荐)
gltf-transform optimize input.glb output.glb \
  --texture-compress ktx2 \
  --compress draco
```

### 压缩选择指南

| 纹理类型   | 推荐格式 | 原因                       |
| ---------- | -------- | -------------------------- |
| 法线贴图   | UASTC    | 需要高精度                 |
| 漫反射贴图 | ETC1S    | 可接受质量损失换取小体积   |
| 环境纹理   | ETC1S    | 次要资源                   |
| UI 纹理    | UASTC    | 需要清晰边缘               |

### 内存对比

| 格式       | 文件大小 | GPU 内存  |
| ---------- | -------- | --------- |
| PNG 4K     | 200KB    | 64MB+     |
| KTX2/UASTC | 5MB      | 5MB       |
| KTX2/ETC1S | 1MB      | 1MB       |

## Meshopt vs Draco

| 特性     | Draco        | Meshopt      |
| -------- | ------------ | ------------ |
| 压缩率   | 极高         | 高           |
| 解压速度 | 较慢         | 快           |
| Web Worker | 需要        | 可选         |
| 结合 gzip | 效果一般     | 接近 Draco   |

建议：对内容分发网络优化使用 Meshopt + gzip。

## 解码器托管

```javascript
// 推荐：自托管解码器
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('/static/draco/');

const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('/static/basis/');

// 备选：CDN
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
```

## LOD 实现

### 原生 Three.js

```javascript
import { LOD } from 'three';

const lod = new LOD();
lod.addLevel(highDetailMesh, 0);
lod.addLevel(mediumDetailMesh, 50);
lod.addLevel(lowDetailMesh, 100);
scene.add(lod);
```

### React Three Fiber

```jsx
import { Detailed } from '@react-three/drei';

<Detailed distances={[0, 20, 50, 100]}>
  <HighDetail />
  <MediumDetail />
  <LowDetail />
  <Billboard /> {/* 最远距离使用 2D 替代 */}
</Detailed>
```

## 纹理图集

减少纹理绑定次数：

```javascript
// 创建图集
const atlasTexture = new CanvasTexture(atlasCanvas);

// 更新 UV 坐标
geometry.attributes.uv.array = recalculatedUVs;
geometry.attributes.uv.needsUpdate = true;
```

工具：TexturePacker、Shoebox

## 渐进式加载

```javascript
// 1. 立即加载低分辨率
const lowRes = await loadModel('model-low.glb');
scene.add(lowRes);
renderOnce();

// 2. 后台加载高分辨率
loadModel('model-high.glb').then(highRes => {
  scene.remove(lowRes);
  disposeModel(lowRes);
  scene.add(highRes);
});
```

## 预加载策略

```html
<!-- HTML 预加载 -->
<link rel="preload" href="/critical-model.glb" as="fetch" crossorigin>
<link rel="preload" href="/hero-texture.ktx2" as="fetch" crossorigin>
```

```javascript
// JS 预加载
import { useGLTF } from '@react-three/drei';

// 组件外预加载
useGLTF.preload('/model.glb');
useGLTF.preload(['/model1.glb', '/model2.glb']);
```

## 流式加载大场景

```javascript
class ChunkLoader {
  constructor(chunkSize = 100) {
    this.chunkSize = chunkSize;
    this.loadedChunks = new Map();
  }
  
  update(cameraPosition) {
    const currentChunk = this.getChunkKey(cameraPosition);
    const nearby = this.getNearbyChunks(currentChunk);
    
    // 加载新块
    nearby.forEach(key => {
      if (!this.loadedChunks.has(key)) {
        this.loadChunk(key);
      }
    });
    
    // 卸载远块
    this.loadedChunks.forEach((chunk, key) => {
      if (!nearby.includes(key)) {
        this.unloadChunk(key);
      }
    });
  }
}
```

## 占位几何体

```javascript
// 加载时显示占位
const placeholder = new Mesh(
  new BoxGeometry(1, 1, 1),
  new MeshBasicMaterial({ 
    color: 0x808080, 
    wireframe: true 
  })
);
scene.add(placeholder);

// 加载完成后替换
loadModel().then(model => {
  scene.remove(placeholder);
  placeholder.geometry.dispose();
  placeholder.material.dispose();
  scene.add(model);
});
```
