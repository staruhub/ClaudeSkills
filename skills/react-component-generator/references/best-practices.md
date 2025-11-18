# React Component Best Practices

## Component Structure

### File Organization
```
ComponentName/
├── ComponentName.tsx       # Main component file
├── ComponentName.test.tsx  # Unit tests
├── index.ts               # Barrel export
└── types.ts               # Type definitions (if complex)
```

### Naming Conventions

1. **Component Names**: Use PascalCase
   - ✅ `UserProfile`, `DataTable`, `LoginForm`
   - ❌ `userProfile`, `dataTable`, `login_form`

2. **File Names**: Match component names exactly
   - ✅ `UserProfile.tsx`
   - ❌ `userProfile.tsx`, `user-profile.tsx`

3. **Props Interface**: ComponentName + "Props"
   - ✅ `UserProfileProps`
   - ❌ `IUserProfileProps`, `Props`, `UserProfileProperties`

4. **Store Names**: use + ComponentName + "Store"
   - ✅ `useUserProfileStore`
   - ❌ `UserProfileStore`, `userStore`

## TypeScript Best Practices

### Props Definition
```typescript
// ✅ Good - Clear, well-typed interface
interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
  className?: string;
  children?: React.ReactNode;
}

// ❌ Avoid - Using 'any' or loose types
interface UserProfileProps {
  userId: any;
  onUpdate?: Function;
  className?: string;
}
```

### Export Patterns
```typescript
// ✅ Preferred - Named export with default export
export const UserProfile: React.FC<UserProfileProps> = (props) => {
  // ...
};

export default UserProfile;

// ✅ Also acceptable - Named export only
export const UserProfile: React.FC<UserProfileProps> = (props) => {
  // ...
};
```

## Zustand State Management

### Store Structure
```typescript
// ✅ Good - Clear separation of state and actions
interface UserStore {
  // State
  user: User | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setUser: (user: User) => void;
  fetchUser: (id: string) => Promise<void>;
  clearError: () => void;
  reset: () => void;
}

export const useUserStore = create<UserStore>((set, get) => ({
  // Initial state
  user: null,
  isLoading: false,
  error: null,

  // Actions
  setUser: (user) => set({ user }),
  fetchUser: async (id) => {
    set({ isLoading: true, error: null });
    try {
      const user = await api.fetchUser(id);
      set({ user, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
  clearError: () => set({ error: null }),
  reset: () => set({ user: null, isLoading: false, error: null }),
}));
```

### Store Usage
```typescript
// ✅ Good - Select only needed state
const { user, isLoading } = useUserStore();

// ⚠️ Acceptable but may cause unnecessary re-renders
const store = useUserStore();

// ✅ Best - Use selector for derived state
const userName = useUserStore((state) => state.user?.name);
```

## Tailwind CSS Best Practices

### Class Organization
```typescript
// ✅ Good - Organized by category
className="
  flex items-center justify-between  // Layout
  px-4 py-2                          // Spacing
  bg-blue-500 text-white             // Colors
  rounded-lg shadow-md               // Effects
  hover:bg-blue-600                  // States
  transition-colors                  // Transitions
"

// ❌ Avoid - Random order
className="text-white hover:bg-blue-600 px-4 flex bg-blue-500 py-2 rounded-lg"
```

### Dynamic Classes
```typescript
// ✅ Good - Template literals for conditional classes
className={`px-4 py-2 rounded ${
  variant === 'primary' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'
} ${className}`}

// ✅ Better - Use a helper library like clsx or classnames
import clsx from 'clsx';

className={clsx(
  'px-4 py-2 rounded',
  {
    'bg-blue-500 text-white': variant === 'primary',
    'bg-gray-200 text-gray-800': variant === 'secondary',
  },
  className
)}
```

### Responsive Design
```typescript
// ✅ Good - Mobile-first responsive design
className="
  text-sm md:text-base lg:text-lg    // Typography
  p-2 md:p-4 lg:p-6                  // Spacing
  grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3  // Layout
"
```

## Component Patterns

### Controlled vs Uncontrolled Components
```typescript
// ✅ Controlled - Parent manages state
interface InputProps {
  value: string;
  onChange: (value: string) => void;
}

export const Input: React.FC<InputProps> = ({ value, onChange }) => {
  return (
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  );
};

// ✅ Uncontrolled - Internal state management
export const Input: React.FC = () => {
  const [value, setValue] = useState('');

  return (
    <input
      value={value}
      onChange={(e) => setValue(e.target.value)}
    />
  );
};
```

### Composition over Props
```typescript
// ✅ Good - Use children for flexibility
interface CardProps {
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ children, footer }) => {
  return (
    <div className="card">
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
};

// Usage
<Card footer={<button>Submit</button>}>
  <h2>Title</h2>
  <p>Content</p>
</Card>
```

### Event Handlers
```typescript
// ✅ Good - Clear naming with 'handle' prefix
const handleClick = () => {
  // ...
};

const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  // ...
};

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  // ...
};

// Props use 'on' prefix
interface ComponentProps {
  onClick?: () => void;
  onSubmit?: (data: FormData) => void;
  onChange?: (value: string) => void;
}
```

## Performance Optimization

### Memoization
```typescript
// ✅ Use React.memo for expensive components
export const ExpensiveComponent = React.memo<ExpensiveComponentProps>(
  ({ data }) => {
    // Heavy rendering logic
    return <div>...</div>;
  }
);

// ✅ Use useMemo for expensive calculations
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// ✅ Use useCallback for event handlers passed to child components
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

### Lazy Loading
```typescript
// ✅ Good - Lazy load heavy components
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

export const App = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
};
```

## Accessibility

### Semantic HTML
```typescript
// ✅ Good - Use semantic elements
<button onClick={handleClick}>Click me</button>
<nav>...</nav>
<main>...</main>
<article>...</article>

// ❌ Avoid - Generic divs with click handlers
<div onClick={handleClick}>Click me</div>
```

### ARIA Attributes
```typescript
// ✅ Good - Proper ARIA labels
<button
  aria-label="Close dialog"
  aria-pressed={isPressed}
>
  <CloseIcon />
</button>

<input
  aria-describedby="email-error"
  aria-invalid={!!error}
/>
{error && <span id="email-error">{error}</span>}
```

### Keyboard Navigation
```typescript
// ✅ Good - Support keyboard events
const handleKeyDown = (e: React.KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') {
    handleClick();
  }
};

<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={handleKeyDown}
>
  Interactive element
</div>
```

## Error Handling

### Error Boundaries
```typescript
// ✅ Create error boundaries for graceful failures
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <div>Something went wrong.</div>;
    }

    return this.props.children;
  }
}
```

### Try-Catch in Async Operations
```typescript
// ✅ Good - Proper error handling
const fetchData = async () => {
  setIsLoading(true);
  setError(null);

  try {
    const data = await api.fetchData();
    setData(data);
  } catch (error) {
    setError(error instanceof Error ? error.message : 'An error occurred');
    console.error('Failed to fetch data:', error);
  } finally {
    setIsLoading(false);
  }
};
```

## Testing Considerations

### Component Structure for Testing
```typescript
// ✅ Good - Extract testable logic
const useFormValidation = (formData: FormData) => {
  const validateEmail = (email: string) => {
    return /\S+@\S+\.\S+/.test(email);
  };

  const validateForm = () => {
    // Validation logic
  };

  return { validateEmail, validateForm };
};

// Component uses the hook
export const Form: React.FC = () => {
  const { validateForm } = useFormValidation(formData);
  // ...
};
```

### Test IDs
```typescript
// ✅ Good - Add data-testid for testing
<button data-testid="submit-button" onClick={handleSubmit}>
  Submit
</button>

<input data-testid="email-input" type="email" />
```
