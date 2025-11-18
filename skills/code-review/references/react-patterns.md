# React Patterns and Anti-Patterns

## Component Patterns

### 1. Composition Over Inheritance

```typescript
// ❌ BAD: Inheritance (not React way)
class BaseButton extends React.Component {
  render() {
    return <button>{this.props.children}</button>;
  }
}

class PrimaryButton extends BaseButton {
  render() {
    return <button className="primary">{this.props.children}</button>;
  }
}

// ✅ GOOD: Composition
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

function Button({ variant = 'primary', children }: ButtonProps) {
  const className = variant === 'primary' ? 'btn-primary' : 'btn-secondary';
  return <button className={className}>{children}</button>;
}
```

### 2. Container/Presentational Pattern

```typescript
// ❌ BAD: Logic and UI mixed
function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser().then(setUser).finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="profile">
      <img src={user.avatar} alt={user.name} />
      <h1>{user.name}</h1>
      <p>{user.bio}</p>
    </div>
  );
}

// ✅ GOOD: Separate concerns
// hooks/useUser.ts (Container/Logic)
export function useUser(userId: string) {
  const { data: user, isLoading } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  return { user, isLoading };
}

// components/UserProfileView.tsx (Presentational)
interface UserProfileViewProps {
  user: User;
}

export function UserProfileView({ user }: UserProfileViewProps) {
  return (
    <div className="profile">
      <img src={user.avatar} alt={user.name} className="w-24 h-24 rounded-full" />
      <h1 className="text-2xl font-bold">{user.name}</h1>
      <p className="text-gray-600">{user.bio}</p>
    </div>
  );
}

// components/UserProfile.tsx (Container)
export function UserProfile({ userId }: { userId: string }) {
  const { user, isLoading } = useUser(userId);

  if (isLoading) return <LoadingSpinner />;
  if (!user) return <ErrorMessage message="User not found" />;

  return <UserProfileView user={user} />;
}
```

### 3. Compound Components Pattern

```typescript
// ❌ BAD: Too many props, inflexible
interface TabsProps {
  tabs: Array<{ label: string; content: React.ReactNode }>;
  defaultTab?: number;
  onTabChange?: (index: number) => void;
}

function Tabs({ tabs, defaultTab = 0, onTabChange }: TabsProps) {
  // Implementation...
}

// ✅ GOOD: Compound components
interface TabsContextValue {
  activeTab: number;
  setActiveTab: (index: number) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

export function Tabs({ children }: { children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(0);

  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div className="tabs">{children}</div>
    </TabsContext.Provider>
  );
}

Tabs.List = function TabsList({ children }: { children: React.ReactNode }) {
  return <div className="tabs-list flex gap-2">{children}</div>;
};

Tabs.Tab = function Tab({ index, children }: { index: number; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('Tab must be used within Tabs');

  const { activeTab, setActiveTab } = context;
  const isActive = activeTab === index;

  return (
    <button
      className={`tab ${isActive ? 'active' : ''}`}
      onClick={() => setActiveTab(index)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function TabPanel({ index, children }: { index: number; children: React.ReactNode }) {
  const context = useContext(TabsContext);
  if (!context) throw new Error('TabPanel must be used within Tabs');

  const { activeTab } = context;
  if (activeTab !== index) return null;

  return <div className="tab-panel">{children}</div>;
};

// Usage
<Tabs>
  <Tabs.List>
    <Tabs.Tab index={0}>Profile</Tabs.Tab>
    <Tabs.Tab index={1}>Settings</Tabs.Tab>
  </Tabs.List>
  <Tabs.Panel index={0}>Profile content</Tabs.Panel>
  <Tabs.Panel index={1}>Settings content</Tabs.Panel>
</Tabs>
```

### 4. Render Props Pattern

```typescript
// ❌ BAD: Hardcoded rendering
function DataFetcher({ url }: { url: string }) {
  const { data, loading } = useFetch(url);

  if (loading) return <div>Loading...</div>;

  return <div>{JSON.stringify(data)}</div>; // Always renders the same way
}

// ✅ GOOD: Render props for flexibility
interface DataFetcherProps<T> {
  url: string;
  children: (data: T, loading: boolean) => React.ReactNode;
}

function DataFetcher<T>({ url, children }: DataFetcherProps<T>) {
  const { data, loading } = useFetch<T>(url);
  return <>{children(data, loading)}</>;
}

// Usage - full control over rendering
<DataFetcher<User> url="/api/user">
  {(user, loading) => (
    loading ? <Spinner /> : <UserCard user={user} />
  )}
</DataFetcher>
```

## Hooks Patterns

### 1. Custom Hooks for Reusable Logic

```typescript
// ❌ BAD: Logic duplicated across components
function ComponentA() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/data')
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  // ...
}

function ComponentB() {
  // Same logic repeated...
}

// ✅ GOOD: Extract to custom hook
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;

    fetch(url)
      .then(res => res.json())
      .then(data => {
        if (!cancelled) setData(data);
      })
      .catch(error => {
        if (!cancelled) setError(error);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [url]);

  return { data, loading, error };
}

// Usage
function ComponentA() {
  const { data, loading, error } = useFetch<User>('/api/user');
  // ...
}
```

### 2. useReducer for Complex State

```typescript
// ❌ BAD: Multiple related useState calls
function ShoppingCart() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [discount, setDiscount] = useState(0);
  const [loading, setLoading] = useState(false);

  const addItem = (item) => {
    setItems([...items, item]);
    setTotal(total + item.price);
    // Complex logic spread across multiple setters
  };

  const removeItem = (id) => {
    const item = items.find(i => i.id === id);
    setItems(items.filter(i => i.id !== id));
    setTotal(total - item.price);
  };

  // More functions...
}

// ✅ GOOD: useReducer for related state
interface CartState {
  items: CartItem[];
  total: number;
  discount: number;
  loading: boolean;
}

type CartAction =
  | { type: 'ADD_ITEM'; payload: CartItem }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'APPLY_DISCOUNT'; payload: number }
  | { type: 'SET_LOADING'; payload: boolean };

function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM':
      return {
        ...state,
        items: [...state.items, action.payload],
        total: state.total + action.payload.price,
      };

    case 'REMOVE_ITEM':
      const item = state.items.find(i => i.id === action.payload);
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload),
        total: state.total - (item?.price || 0),
      };

    case 'APPLY_DISCOUNT':
      return {
        ...state,
        discount: action.payload,
      };

    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload,
      };

    default:
      return state;
  }
}

function ShoppingCart() {
  const [state, dispatch] = useReducer(cartReducer, {
    items: [],
    total: 0,
    discount: 0,
    loading: false,
  });

  const addItem = (item: CartItem) => {
    dispatch({ type: 'ADD_ITEM', payload: item });
  };

  const removeItem = (id: string) => {
    dispatch({ type: 'REMOVE_ITEM', payload: id });
  };

  // ...
}
```

### 3. Optimistic Updates with useMutation

```typescript
// ❌ BAD: No optimistic update
function TodoList() {
  const { data: todos } = useQuery({ queryKey: ['todos'], queryFn: fetchTodos });
  const mutation = useMutation({ mutationFn: toggleTodo });

  const handleToggle = async (id: string) => {
    await mutation.mutateAsync(id);
    // UI only updates after server responds (slow UX)
  };

  // ...
}

// ✅ GOOD: Optimistic update
function TodoList() {
  const queryClient = useQueryClient();
  const { data: todos } = useQuery({ queryKey: ['todos'], queryFn: fetchTodos });

  const mutation = useMutation({
    mutationFn: toggleTodo,
    onMutate: async (todoId) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['todos'] });

      // Snapshot previous value
      const previousTodos = queryClient.getQueryData(['todos']);

      // Optimistically update
      queryClient.setQueryData(['todos'], (old: Todo[]) =>
        old.map(todo =>
          todo.id === todoId ? { ...todo, completed: !todo.completed } : todo
        )
      );

      return { previousTodos };
    },
    onError: (err, todoId, context) => {
      // Rollback on error
      queryClient.setQueryData(['todos'], context?.previousTodos);
    },
    onSettled: () => {
      // Refetch after mutation
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  const handleToggle = (id: string) => {
    mutation.mutate(id); // UI updates immediately
  };

  // ...
}
```

## Performance Patterns

### 1. Memoization

```typescript
// ❌ BAD: Re-creating objects/functions on every render
function ExpensiveComponent({ data }: { data: Data[] }) {
  const sortedData = data.sort((a, b) => a.value - b.value);
  const handleClick = () => console.log('clicked');

  return (
    <div>
      {sortedData.map(item => (
        <ChildComponent key={item.id} item={item} onClick={handleClick} />
      ))}
    </div>
  );
}

// ✅ GOOD: Memoize expensive calculations and callbacks
function ExpensiveComponent({ data }: { data: Data[] }) {
  const sortedData = useMemo(
    () => [...data].sort((a, b) => a.value - b.value),
    [data]
  );

  const handleClick = useCallback(() => {
    console.log('clicked');
  }, []);

  return (
    <div>
      {sortedData.map(item => (
        <ChildComponent key={item.id} item={item} onClick={handleClick} />
      ))}
    </div>
  );
}

const ChildComponent = memo(function ChildComponent({
  item,
  onClick,
}: {
  item: Data;
  onClick: () => void;
}) {
  return <div onClick={onClick}>{item.value}</div>;
});
```

### 2. Code Splitting & Lazy Loading

```typescript
// ❌ BAD: Import everything upfront
import HeavyChart from './HeavyChart';
import HeavyEditor from './HeavyEditor';
import HeavyCalendar from './HeavyCalendar';

function Dashboard() {
  return (
    <div>
      <HeavyChart />
      <HeavyEditor />
      <HeavyCalendar />
    </div>
  );
}

// ✅ GOOD: Lazy load heavy components
const HeavyChart = lazy(() => import('./HeavyChart'));
const HeavyEditor = lazy(() => import('./HeavyEditor'));
const HeavyCalendar = lazy(() => import('./HeavyCalendar'));

function Dashboard() {
  return (
    <div>
      <Suspense fallback={<ChartSkeleton />}>
        <HeavyChart />
      </Suspense>
      <Suspense fallback={<EditorSkeleton />}>
        <HeavyEditor />
      </Suspense>
      <Suspense fallback={<CalendarSkeleton />}>
        <HeavyCalendar />
      </Suspense>
    </div>
  );
}
```

### 3. Virtualization for Long Lists

```typescript
// ❌ BAD: Render all 10,000 items
function LargeList({ items }: { items: Item[] }) {
  return (
    <div>
      {items.map(item => (
        <ItemRow key={item.id} item={item} />
      ))}
    </div>
  );
}

// ✅ GOOD: Virtualize with react-window
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

## State Management Patterns

### 1. Lift State Up (When Needed)

```typescript
// ❌ BAD: Duplicated state
function Parent() {
  return (
    <>
      <FilterA />
      <FilterB />
      <Results />
    </>
  );
}

function FilterA() {
  const [filter, setFilter] = useState('');
  // Filter state isolated
}

function FilterB() {
  const [filter, setFilter] = useState('');
  // Duplicated state, not synced
}

// ✅ GOOD: Lift state to common ancestor
function Parent() {
  const [filterA, setFilterA] = useState('');
  const [filterB, setFilterB] = useState('');

  return (
    <>
      <FilterA value={filterA} onChange={setFilterA} />
      <FilterB value={filterB} onChange={setFilterB} />
      <Results filterA={filterA} filterB={filterB} />
    </>
  );
}
```

### 2. Context for Avoiding Prop Drilling

```typescript
// ❌ BAD: Prop drilling
function App() {
  const [theme, setTheme] = useState('light');

  return <Layout theme={theme} setTheme={setTheme} />;
}

function Layout({ theme, setTheme }) {
  return <Sidebar theme={theme} setTheme={setTheme} />;
}

function Sidebar({ theme, setTheme }) {
  return <ThemeToggle theme={theme} setTheme={setTheme} />;
}

function ThemeToggle({ theme, setTheme }) {
  // Finally using it here
}

// ✅ GOOD: Context for deeply nested props
interface ThemeContextValue {
  theme: string;
  setTheme: (theme: string) => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
}

// Usage
function App() {
  return (
    <ThemeProvider>
      <Layout />
    </ThemeProvider>
  );
}

function ThemeToggle() {
  const { theme, setTheme } = useTheme(); // Direct access
  // ...
}
```

### 3. Zustand for Global State

```typescript
// ❌ BAD: Complex Context with many values
const AppContext = createContext({
  user: null,
  cart: [],
  notifications: [],
  settings: {},
  // ... many more
});

// ✅ GOOD: Zustand store
import { create } from 'zustand';

interface AppStore {
  user: User | null;
  cart: CartItem[];
  notifications: Notification[];
  settings: Settings;

  setUser: (user: User | null) => void;
  addToCart: (item: CartItem) => void;
  removeFromCart: (id: string) => void;
  addNotification: (notification: Notification) => void;
  updateSettings: (settings: Partial<Settings>) => void;
}

export const useAppStore = create<AppStore>((set) => ({
  user: null,
  cart: [],
  notifications: [],
  settings: {},

  setUser: (user) => set({ user }),

  addToCart: (item) =>
    set((state) => ({ cart: [...state.cart, item] })),

  removeFromCart: (id) =>
    set((state) => ({ cart: state.cart.filter(i => i.id !== id) })),

  addNotification: (notification) =>
    set((state) => ({ notifications: [...state.notifications, notification] })),

  updateSettings: (settings) =>
    set((state) => ({ settings: { ...state.settings, ...settings } })),
}));

// Usage - only re-renders when specific slice changes
function UserProfile() {
  const user = useAppStore(state => state.user);
  // Only re-renders when user changes
}

function Cart() {
  const cart = useAppStore(state => state.cart);
  const addToCart = useAppStore(state => state.addToCart);
  // Only re-renders when cart changes
}
```

## Anti-Patterns to Avoid

### 1. Mutating State Directly

```typescript
// ❌ CRITICAL: Direct mutation
const [items, setItems] = useState([]);

items.push(newItem); // WRONG!
items[0].name = 'New name'; // WRONG!

// ✅ GOOD: Create new references
setItems([...items, newItem]);
setItems(items.map((item, i) => i === 0 ? { ...item, name: 'New name' } : item));
```

### 2. Setting State from Props Directly

```typescript
// ❌ BAD: Derive state from props incorrectly
function Component({ initialValue }: { initialValue: number }) {
  const [value, setValue] = useState(initialValue);
  // If initialValue changes, value doesn't update!
}

// ✅ GOOD: Use controlled component
function Component({ value, onChange }: { value: number; onChange: (v: number) => void }) {
  return <input value={value} onChange={e => onChange(Number(e.target.value))} />;
}

// ✅ GOOD: Or derive from props directly
function Component({ initialValue }: { initialValue: number }) {
  const displayValue = initialValue * 2; // Computed on each render
  return <div>{displayValue}</div>;
}
```

### 3. Using Index as Key

```typescript
// ❌ BAD: Index as key (causes bugs when list changes)
{items.map((item, index) => (
  <Item key={index} item={item} />
))}

// ✅ GOOD: Unique ID as key
{items.map(item => (
  <Item key={item.id} item={item} />
))}
```

Use these patterns to write clean, performant React code!
