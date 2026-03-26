# 完整代码示例

## 性能监控设置

```javascript
import Stats from 'stats-gl';
import GUI from 'lil-gui';

// Stats
const stats = new Stats();
document.body.appendChild(stats.dom);

// GUI 面板
const gui = new GUI();
const params = {
  shadowMapSize: 1024,
  lightIntensity: 1,
  bloomStrength: 0.5
};

gui.add(params, 'shadowMapSize', [512, 1024, 2048, 4096]).onChange(v => {
  light.shadow.mapSize.set(v, v);
  light.shadow.map?.dispose();
  light.shadow.map = null;
});
gui.add(params, 'lightIntensity', 0, 2).onChange(v => {
  light.intensity = v;
});

// 动画循环中
function animate() {
  stats.begin();
  renderer.render(scene, camera);
  stats.end();
  requestAnimationFrame(animate);
}
```

## 完整内存清理

```javascript
function disposeScene(scene) {
  scene.traverse(object => {
    if (object.isMesh) {
      object.geometry?.dispose();
      
      const materials = Array.isArray(object.material) 
        ? object.material 
        : [object.material];
        
      materials.forEach(material => {
        if (!material) return;
        
        // 释放所有纹理
        Object.keys(material).forEach(key => {
          const value = material[key];
          if (value?.isTexture) {
            value.source?.data?.close?.(); // ImageBitmap
            value.dispose();
          }
        });
        
        material.dispose();
      });
    }
    
    if (object.isLight && object.shadow?.map) {
      object.shadow.map.dispose();
    }
  });
  
  // 释放渲染目标
  if (composer) {
    composer.passes.forEach(pass => {
      pass.dispose?.();
    });
  }
}

// 使用
window.addEventListener('beforeunload', () => {
  disposeScene(scene);
  renderer.dispose();
});
```

## 完整对象池

```javascript
class GameObjectPool {
  constructor(createFn, resetFn, initialSize = 50) {
    this.create = createFn;
    this.reset = resetFn;
    this.available = [];
    this.active = new Set();
    
    // 预热
    for (let i = 0; i < initialSize; i++) {
      const obj = this.create();
      obj.visible = false;
      this.available.push(obj);
    }
  }
  
  acquire() {
    let obj = this.available.pop();
    if (!obj) {
      obj = this.create();
      console.warn('Pool expanded - consider larger initial size');
    }
    obj.visible = true;
    this.active.add(obj);
    return obj;
  }
  
  release(obj) {
    if (!this.active.has(obj)) return;
    
    this.reset(obj);
    obj.visible = false;
    this.active.delete(obj);
    this.available.push(obj);
  }
  
  releaseAll() {
    this.active.forEach(obj => this.release(obj));
  }
  
  get stats() {
    return {
      available: this.available.length,
      active: this.active.size,
      total: this.available.length + this.active.size
    };
  }
}

// 使用示例：子弹池
const bulletGeometry = new SphereGeometry(0.1);
const bulletMaterial = new MeshBasicMaterial({ color: 0xffff00 });

const bulletPool = new GameObjectPool(
  () => {
    const mesh = new Mesh(bulletGeometry, bulletMaterial);
    scene.add(mesh);
    return mesh;
  },
  (bullet) => {
    bullet.position.set(0, 0, 0);
    bullet.userData.velocity = null;
  },
  100
);

// 发射
function fireBullet(position, direction) {
  const bullet = bulletPool.acquire();
  bullet.position.copy(position);
  bullet.userData.velocity = direction.multiplyScalar(50);
}

// 更新循环
function updateBullets(delta) {
  bulletPool.active.forEach(bullet => {
    bullet.position.addScaledVector(bullet.userData.velocity, delta);
    
    if (bullet.position.length() > 1000) {
      bulletPool.release(bullet);
    }
  });
}
```

## WebGPU 粒子系统完整示例

```javascript
import { 
  WebGPURenderer,
  Scene,
  PerspectiveCamera,
  InstancedMesh,
  SphereGeometry,
  MeshBasicNodeMaterial
} from 'three/webgpu';

import {
  instancedArray,
  compute,
  instanceIndex,
  time,
  sin,
  cos,
  vec3,
  float
} from 'three/tsl';

async function init() {
  const renderer = new WebGPURenderer();
  await renderer.init();
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.body.appendChild(renderer.domElement);
  
  const scene = new Scene();
  const camera = new PerspectiveCamera(75, window.innerWidth / window.innerHeight);
  camera.position.z = 50;
  
  const PARTICLE_COUNT = 100000;
  
  // GPU 缓冲区
  const positions = instancedArray(PARTICLE_COUNT, 'vec3');
  const velocities = instancedArray(PARTICLE_COUNT, 'vec3');
  
  // 初始化计算着色器
  const initCompute = compute(() => {
    const i = instanceIndex;
    const angle = float(i).mul(0.1);
    const radius = float(i).div(PARTICLE_COUNT).mul(20);
    
    positions.element(i).assign(vec3(
      cos(angle).mul(radius),
      sin(angle.mul(1.5)).mul(5),
      sin(angle).mul(radius)
    ));
    
    velocities.element(i).assign(vec3(0, 0, 0));
  }).compute(PARTICLE_COUNT);
  
  // 更新计算着色器
  const updateCompute = compute(() => {
    const i = instanceIndex;
    const pos = positions.element(i);
    const vel = velocities.element(i);
    
    // 简单螺旋运动
    const t = time.mul(0.5);
    const newPos = vec3(
      pos.x.mul(cos(t.mul(0.01))).sub(pos.z.mul(sin(t.mul(0.01)))),
      pos.y.add(sin(t.add(float(i).mul(0.001))).mul(0.1)),
      pos.x.mul(sin(t.mul(0.01))).add(pos.z.mul(cos(t.mul(0.01))))
    );
    
    positions.element(i).assign(newPos);
  }).compute(PARTICLE_COUNT);
  
  // 材质使用位置数据
  const material = new MeshBasicNodeMaterial({
    color: 0x00ffff
  });
  material.positionNode = positions.element(instanceIndex);
  
  // 创建实例化网格
  const geometry = new SphereGeometry(0.1, 8, 8);
  const mesh = new InstancedMesh(geometry, material, PARTICLE_COUNT);
  scene.add(mesh);
  
  // 初始化位置
  await renderer.computeAsync(initCompute);
  
  // 动画循环
  async function animate() {
    await renderer.computeAsync(updateCompute);
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }
  
  animate();
}

init();
```

## R3F 完整性能优化模板

```jsx
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Suspense, useRef, useMemo, memo } from 'react';
import { Detailed, useGLTF, Preload } from '@react-three/drei';
import { Perf } from 'r3f-perf';

// 预加载
useGLTF.preload('/model-high.glb');
useGLTF.preload('/model-low.glb');

// 优化的动画组件
const AnimatedMesh = memo(({ speed = 1 }) => {
  const meshRef = useRef();
  const targetPos = useMemo(() => new Vector3(), []);
  
  useFrame((state, delta) => {
    if (!meshRef.current) return;
    
    // 直接修改，不触发 React
    meshRef.current.rotation.y += delta * speed;
    
    // 复用向量
    targetPos.set(Math.sin(state.clock.elapsedTime), 0, 0);
    meshRef.current.position.lerp(targetPos, delta * 2);
  });
  
  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial />
    </mesh>
  );
});

// LOD 模型
function LODModel({ position }) {
  return (
    <Detailed distances={[0, 20, 50]} position={position}>
      <HighDetailModel />
      <MediumDetailModel />
      <LowDetailModel />
    </Detailed>
  );
}

// 主场景
function Scene() {
  return (
    <>
      <ambientLight intensity={0.5} />
      <directionalLight 
        position={[10, 10, 5]} 
        castShadow
        shadow-mapSize={[1024, 1024]}
      />
      
      <AnimatedMesh speed={0.5} />
      
      {/* 实例化大量对象 */}
      <Instances limit={1000}>
        {positions.map((pos, i) => (
          <Instance key={i} position={pos} />
        ))}
      </Instances>
    </>
  );
}

// App
export default function App() {
  return (
    <Canvas
      frameloop="demand"  // 按需渲染
      shadows
      gl={{
        antialias: false,
        powerPreference: 'high-performance'
      }}
      camera={{ position: [0, 5, 10], fov: 50 }}
    >
      <Perf position="top-left" />
      
      <Suspense fallback={<Loader />}>
        <Scene />
        <Preload all />
      </Suspense>
    </Canvas>
  );
}
```

## 后处理完整设置

### WebGL

```javascript
import { EffectComposer, EffectPass, RenderPass, SMAAEffect } from 'postprocessing';
import { BloomEffect, VignetteEffect, ToneMappingEffect } from 'postprocessing';

// 渲染器配置
const renderer = new WebGLRenderer({
  powerPreference: 'high-performance',
  antialias: false,
  stencil: false,
  depth: false
});
renderer.toneMapping = NoToneMapping; // 由后处理处理

// 效果组合器
const composer = new EffectComposer(renderer, {
  multisampling: 0 // 禁用多重采样提升性能
});

composer.addPass(new RenderPass(scene, camera));

// 合并多个效果为单次通道
const bloom = new BloomEffect({
  luminanceThreshold: 0.9,
  luminanceSmoothing: 0.3,
  intensity: 0.5
});

const vignette = new VignetteEffect({
  darkness: 0.5
});

const toneMapping = new ToneMappingEffect();

composer.addPass(new EffectPass(camera, bloom, vignette, toneMapping));

// 抗锯齿放最后
composer.addPass(new EffectPass(camera, new SMAAEffect()));

// 渲染循环
function animate() {
  composer.render();
  requestAnimationFrame(animate);
}
```

### WebGPU

```javascript
import { WebGPURenderer, PostProcessing } from 'three/webgpu';
import { pass, bloom, fxaa, dof, vignettePass } from 'three/tsl';

const renderer = new WebGPURenderer({ antialias: false });
await renderer.init();

const postProcessing = new PostProcessing(renderer);
const scenePass = pass(scene, camera);

// 链式管线
postProcessing.outputNode = scenePass
  .pipe(bloom({ luminanceThreshold: 0.9 }))
  .pipe(vignettePass({ offset: 0.5 }))
  .pipe(fxaa());

// 渲染
function animate() {
  postProcessing.render();
  requestAnimationFrame(animate);
}
```

## 上下文丢失恢复

```javascript
const canvas = renderer.domElement;

canvas.addEventListener('webglcontextlost', (event) => {
  event.preventDefault();
  cancelAnimationFrame(animationId);
  console.warn('WebGL context lost');
});

canvas.addEventListener('webglcontextrestored', () => {
  console.log('WebGL context restored');
  
  // 重新初始化必要资源
  initScene();
  initMaterials();
  
  // 恢复动画循环
  animate();
});
```
