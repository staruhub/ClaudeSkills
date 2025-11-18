# 前端代码规范

## React 组件规范

### 组件结构顺序（严格遵循）

```typescript
// 1. Imports
import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. Types/Interfaces
interface ComponentProps {
  title: string;
  onSubmit: (data: FormData) => void;
}

// 3. Component Function
export function Component({ title, onSubmit }: ComponentProps) {
  // 3.1 Hooks (状态、查询、引用)
  const [isOpen, setIsOpen] = useState(false);
  const { data, isLoading } = useQuery(...);
  const inputRef = useRef<HTMLInputElement>(null);

  // 3.2 Derived state (计算值)
  const itemCount = data?.length ?? 0;
  const hasItems = itemCount > 0;

  // 3.3 Event handlers
  const handleClick = () => {
    setIsOpen(true);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle submit
  };

  // 3.4 Effects
  useEffect(() => {
    // Side effects
  }, []);

  // 3.5 Early returns (loading, error states)
  if (isLoading) return <LoadingSpinner />;
  if (!data) return <ErrorMessage />;

  // 3.6 Main render
  return (
    <div>
      {/* JSX */}
    </div>
  );
}
```

### 组件拆分原则

**何时拆分**:
- 单一职责：组件只做一件事
- 文件行数：≤ 200 行（推荐），≤ 300 行（最大）
- 复杂度：超过 3 层嵌套
- 复用性：重复的 UI 模式

**拆分示例**:

```typescript
// ❌ BAD: 单个大组件
function UserDashboard() {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [notifications, setNotifications] = useState([]);

  // 300+ lines of logic and JSX
  return (
    <div>
      {/* User profile section */}
      {/* Posts list section */}
      {/* Notifications section */}
    </div>
  );
}

// ✅ GOOD: 拆分为多个组件
function UserDashboard() {
  return (
    <div>
      <UserProfile />
      <UserPosts />
      <UserNotifications />
    </div>
  );
}

function UserProfile() {
  const { user, isLoading } = useUser();
  // Profile-specific logic
}

function UserPosts() {
  const { posts, isLoading } = usePosts();
  // Posts-specific logic
}
```

### 组件命名规范

```typescript
// ✅ GOOD: PascalCase for components
export function UserProfile() { }
export function LoginForm() { }

// ✅ GOOD: Descriptive names
export function ProductCard() { }  // Not just Card
export function UserAvatar() { }   // Not just Avatar

// ❌ BAD: Generic names
export function Component() { }
export function MyComponent() { }
```

## TypeScript 规范

### 类型定义

```typescript
// ❌ BAD: 使用 any
function process(data: any) {
  return data.value;
}

// ✅ GOOD: 具体类型
interface UserData {
  id: string;
  name: string;
  email: string;
  age?: number;
}

function process(data: UserData): string {
  return data.name;
}

// ❌ BAD: 非空断言（不确定时）
const user = users.find(u => u.id === id)!;
user.name; // 可能崩溃

// ✅ GOOD: 安全处理
const user = users.find(u => u.id === id);
if (!user) {
  throw new Error('User not found');
}
return user.name;

// ✅ GOOD: 可选链
const userName = users.find(u => u.id === id)?.name ?? 'Unknown';
```

### 运行时验证（Zod）

```typescript
// ✅ GOOD: 结合 TypeScript 和运行时验证
import { z } from 'zod';

// 1. 定义 schema
const userSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(2).max(50),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

// 2. 推导 TypeScript 类型
type User = z.infer<typeof userSchema>;

// 3. 运行时验证
function createUser(data: unknown): User {
  return userSchema.parse(data); // 验证失败会抛出错误
}

// 4. 安全验证（不抛出错误）
function validateUser(data: unknown): User | null {
  const result = userSchema.safeParse(data);
  return result.success ? result.data : null;
}
```

### Props 类型定义

```typescript
// ✅ GOOD: 明确的 Props 接口
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  className?: string;
}

export function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  children,
  className,
}: ButtonProps) {
  // Implementation
}

// ✅ GOOD: 事件处理器类型
interface FormProps {
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onFocus: (e: React.FocusEvent<HTMLInputElement>) => void;
}

// ✅ GOOD: Children 类型
interface ContainerProps {
  children: React.ReactNode; // 最通用
  // 或
  children: React.ReactElement; // 单个 React 元素
  // 或
  children: string; // 只接受字符串
}
```

### 泛型组件

```typescript
// ✅ GOOD: 泛型组件
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

export function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <div>
      {items.map(item => (
        <div key={keyExtractor(item)}>
          {renderItem(item)}
        </div>
      ))}
    </div>
  );
}

// 使用
<List
  items={users}
  renderItem={(user) => <UserCard user={user} />}
  keyExtractor={(user) => user.id}
/>
```

## Tailwind CSS 规范

### 响应式设计（Mobile-first）

```typescript
// ✅ GOOD: Mobile-first 方法
<div className="w-full md:w-1/2 lg:w-1/3 xl:w-1/4">
  {/* 移动端全宽，平板1/2，桌面1/3，大屏1/4 */}
</div>

// ✅ GOOD: 响应式字体
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
  标题
</h1>

// ✅ GOOD: 响应式间距
<div className="p-4 md:p-6 lg:p-8">
  内容
</div>

// ✅ GOOD: 响应式布局
<div className="flex flex-col lg:flex-row gap-4 lg:gap-8">
  <aside className="w-full lg:w-64">侧边栏</aside>
  <main className="flex-1">主内容</main>
</div>
```

### 样式组织

```typescript
// ❌ BAD: 过长的 className
<button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 active:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 shadow-md hover:shadow-lg">

// ✅ GOOD: 使用变量
const buttonBaseStyles = "px-4 py-2 rounded-lg transition-colors duration-200";
const buttonPrimaryStyles = "bg-blue-500 text-white hover:bg-blue-600 active:bg-blue-700";
const buttonDisabledStyles = "disabled:opacity-50 disabled:cursor-not-allowed";

<button className={`${buttonBaseStyles} ${buttonPrimaryStyles} ${buttonDisabledStyles}`}>

// ✅ BETTER: 创建可复用组件
interface ButtonProps {
  variant: 'primary' | 'secondary';
  size: 'sm' | 'md' | 'lg';
}

function Button({ variant, size, children }: ButtonProps) {
  const baseStyles = "rounded-lg transition-colors";
  const variantStyles = {
    primary: "bg-blue-500 text-white hover:bg-blue-600",
    secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
  };
  const sizeStyles = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg",
  };

  return (
    <button className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]}`}>
      {children}
    </button>
  );
}
```

### Tailwind 工具函数

```typescript
// ✅ GOOD: 使用 clsx 或 classnames 合并样式
import clsx from 'clsx';

interface CardProps {
  active?: boolean;
  disabled?: boolean;
  className?: string;
}

function Card({ active, disabled, className }: CardProps) {
  return (
    <div
      className={clsx(
        'p-4 rounded-lg border',
        {
          'bg-blue-50 border-blue-500': active,
          'bg-gray-50 border-gray-300': !active,
          'opacity-50 cursor-not-allowed': disabled,
        },
        className // 允许外部覆盖
      )}
    >
      Content
    </div>
  );
}
```

## 性能优化规范

### Memoization

```typescript
// ✅ GOOD: 昂贵计算使用 useMemo
function ProductList({ products }: { products: Product[] }) {
  const sortedProducts = useMemo(
    () => [...products].sort((a, b) => b.price - a.price),
    [products]
  );

  const totalPrice = useMemo(
    () => products.reduce((sum, p) => sum + p.price, 0),
    [products]
  );

  return <div>{/* Render sorted products */}</div>;
}

// ✅ GOOD: 回调函数使用 useCallback
function Parent() {
  const [count, setCount] = useState(0);

  const handleIncrement = useCallback(() => {
    setCount(c => c + 1);
  }, []); // 不依赖外部变量

  const handleAdd = useCallback((amount: number) => {
    setCount(c => c + amount);
  }, []); // 使用函数式更新

  return <Child onIncrement={handleIncrement} onAdd={handleAdd} />;
}

// ✅ GOOD: 子组件使用 memo
const ExpensiveChild = memo(function ExpensiveChild({ data }: { data: Data }) {
  // 复杂的渲染逻辑
  return <div>{/* Complex rendering */}</div>;
});

// ❌ BAD: 不必要的 useMemo
const value = useMemo(() => props.value, [props.value]); // 没必要
const doubled = useMemo(() => count * 2, [count]); // 计算太简单
```

### Code Splitting & Lazy Loading

```typescript
// ✅ GOOD: 路由级别懒加载
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
const Profile = lazy(() => import('./pages/Profile'));

function App() {
  return (
    <Suspense fallback={<LoadingScreen />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Suspense>
  );
}

// ✅ GOOD: 组件级别懒加载
const HeavyChart = lazy(() => import('./components/HeavyChart'));
const VideoPlayer = lazy(() => import('./components/VideoPlayer'));

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>显示图表</button>
      {showChart && (
        <Suspense fallback={<ChartSkeleton />}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

### 列表虚拟化

```typescript
// ❌ BAD: 渲染 10,000 个项目
function LargeList({ items }: { items: Item[] }) {
  return (
    <div>
      {items.map(item => (
        <ItemRow key={item.id} item={item} />
      ))}
    </div>
  );
}

// ✅ GOOD: 使用虚拟化（react-window）
import { FixedSizeList } from 'react-window';

function LargeList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      <ItemRow item={items[index]} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

## 状态管理规范

### 本地 State vs 全局 State

```typescript
// ✅ GOOD: 本地状态 - 仅组件内使用
function Modal() {
  const [isOpen, setIsOpen] = useState(false); // 只在这个组件用
  return <div>{/* Modal UI */}</div>;
}

// ✅ GOOD: 全局状态 - Zustand（跨组件共享）
import { create } from 'zustand';

interface UserStore {
  user: User | null;
  setUser: (user: User | null) => void;
  logout: () => void;
}

export const useUserStore = create<UserStore>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  logout: () => set({ user: null }),
}));

// 在任何组件中使用
function Header() {
  const user = useUserStore(state => state.user);
  const logout = useUserStore(state => state.logout);
  // ...
}

// ✅ GOOD: 服务器状态 - React Query（API 数据）
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
    staleTime: 5 * 60 * 1000, // 5 分钟内不重新请求
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return <div>{user.name}</div>;
}
```

### 状态更新规则

```typescript
// ❌ BAD: 直接修改状态
const [items, setItems] = useState<Item[]>([]);
items.push(newItem); // 错误！
items[0].name = 'New Name'; // 错误！

// ✅ GOOD: 创建新引用
setItems([...items, newItem]); // 添加
setItems(items.filter(item => item.id !== id)); // 删除
setItems(items.map(item =>
  item.id === id ? { ...item, name: 'New Name' } : item
)); // 更新

// ✅ GOOD: 函数式更新（使用当前值）
setCount(c => c + 1);
setItems(prevItems => [...prevItems, newItem]);

// ❌ BAD: 在循环中多次 setState
items.forEach(item => {
  setCount(c => c + item.value); // 每次都触发重渲染
});

// ✅ GOOD: 批量计算后一次 setState
const total = items.reduce((sum, item) => sum + item.value, 0);
setCount(c => c + total);
```

## 导入顺序规范

```typescript
// 1. React 和 Next.js
import { useState, useEffect, useMemo } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

// 2. 第三方库（按字母排序）
import { useQuery, useMutation } from '@tanstack/react-query';
import clsx from 'clsx';
import { z } from 'zod';

// 3. 项目内部（按路径分组，从最通用到最具体）
// 3.1 共享组件
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';

// 3.2 Features
import { useAuth } from '@/features/auth/hooks/useAuth';
import { userApi } from '@/features/user/api/userApi';

// 3.3 Utils
import { formatDate } from '@/utils/date';
import { cn } from '@/utils/classnames';

// 4. 类型导入（使用 type 关键字）
import type { User } from '@/types/user';
import type { Product } from '@/features/products/types';

// 5. 样式和资源
import styles from './Component.module.css';
import logo from '@/assets/logo.png';
```

## 错误处理规范

```typescript
// ✅ GOOD: 组件级错误边界
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <ErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}

// 使用
<ErrorBoundary fallback={<div>出错了</div>}>
  <App />
</ErrorBoundary>

// ✅ GOOD: 异步操作错误处理
async function handleSubmit(data: FormData) {
  try {
    const result = await submitForm(data);
    toast.success('提交成功');
    return result;
  } catch (error) {
    if (error instanceof ValidationError) {
      toast.error(error.message);
    } else if (error instanceof NetworkError) {
      toast.error('网络错误，请重试');
    } else {
      toast.error('未知错误');
      console.error('Unexpected error:', error);
    }
    throw error; // 重新抛出以便上层处理
  }
}
```

## 测试规范

```typescript
// ✅ GOOD: 组件测试
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should display validation error for invalid email', () => {
    render(<LoginForm />);

    const emailInput = screen.getByLabelText(/email/i);
    fireEvent.change(emailInput, { target: { value: 'invalid' } });
    fireEvent.blur(emailInput);

    expect(screen.getByText(/invalid email/i)).toBeInTheDocument();
  });

  it('should call onSubmit with form data when submitted', async () => {
    const onSubmit = jest.fn();
    render(<LoginForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' }
    });
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' }
    });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123'
    });
  });
});

// ✅ GOOD: Hook 测试
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('should increment count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('should reset count', () => {
    const { result } = renderHook(() => useCounter({ initialValue: 5 }));

    act(() => {
      result.current.reset();
    });

    expect(result.current.count).toBe(0);
  });
});
```

使用这些规范确保代码的一致性、可维护性和高质量！
