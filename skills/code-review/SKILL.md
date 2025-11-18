---
name: code-review
description: Frontend-focused code review skill for React/TypeScript/Tailwind projects. Analyzes code quality, security vulnerabilities (XSS, CSRF), performance issues, accessibility (WCAG), React best practices, hooks usage, component architecture, responsive design, and SEO. Use when users request code review, want feedback on components, ask about frontend security, performance optimization, or accessibility compliance. Provides actionable feedback with severity levels and fix suggestions.
allowed-tools: Read, Grep, Glob, Bash
---

# Frontend Code Review

This skill provides comprehensive, production-ready code review for modern frontend applications with actionable feedback focused on React/TypeScript/Tailwind stack.

## Purpose

Transform frontend code review from manual inspection into systematic analysis covering:
1. **Frontend Security** - XSS, CSRF, sensitive data exposure, auth issues
2. **React Performance** - Re-renders, memoization, bundle size, lazy loading
3. **Code Quality** - Readability, maintainability, React best practices
4. **Component Architecture** - Layered architecture, separation of concerns, reusability
5. **Type Safety** - TypeScript usage, type correctness, runtime validation
6. **Accessibility** - WCAG compliance, keyboard navigation, screen readers
7. **Responsive Design** - Mobile-first, breakpoints, Tailwind patterns
8. **SEO & Meta** - Meta tags, semantic HTML, performance metrics
9. **Testing** - Component tests, hooks tests, edge cases
10. **State Management** - Zustand/Context patterns, React Query usage

## When to Use This Skill

Use this skill when:
- User asks for code review or feedback
- User mentions: "review", "check", "feedback", "quality", "security"
- After generating components or features
- User asks about performance or accessibility
- Before committing major changes
- Examples:
  - "Review this component"
  - "Is this React code optimized?"
  - "Can you check for accessibility issues?"
  - "How can I improve this?"
  - "Review my feature implementation"

## Review Process

### Step 1: Understand Context

Before reviewing, gather context:

1. **Code Type**:
   - React Component (UI, Form, List, etc.)
   - Custom Hook (business logic)
   - Utility function (helpers, transforms)
   - API integration (React Query, fetch)
   - Store/State management (Zustand, Context)
   - Styling (Tailwind, CSS-in-JS)

2. **Review Scope**:
   - Single component/hook
   - Entire feature (multiple files)
   - Page/route implementation
   - Shared utilities

3. **Priority**:
   - Security-critical (auth, payment forms)
   - Performance-critical (large lists, complex calculations)
   - User-facing (accessibility, UX)
   - Internal (utilities, helpers)

### Step 2: Initial Scan

Quickly scan for obvious issues:

**Critical Issues (🚨 CRITICAL)**:
- XSS vulnerabilities (dangerouslySetInnerHTML)
- CSRF vulnerabilities (missing tokens)
- Sensitive data exposure (tokens in localStorage)
- Authentication bypass
- Hardcoded secrets/API keys

**High Priority (⚠️ HIGH)**:
- Performance bottlenecks (unnecessary re-renders, no memoization)
- Memory leaks (missing cleanup in useEffect)
- Error handling gaps
- Accessibility violations (no ARIA labels, keyboard support)
- Missing input validation

**<br>Medium Priority (⚡ MEDIUM)**:
- Code duplication
- Unclear component/variable names
- Missing loading/error states
- Poor TypeScript usage (any types)
- Inconsistent Tailwind usage

**Low Priority (💡 LOW)**:
- Code style inconsistencies
- Missing comments for complex logic
- Minor optimizations
- Documentation gaps

### Step 3: Deep Analysis

Perform systematic review across all dimensions:

#### 3.1 Frontend Security Review

Check against common frontend vulnerabilities:

```typescript
// ❌ BAD: XSS vulnerability
function UserComment({ comment }: { comment: string }) {
  return <div dangerouslySetInnerHTML={{ __html: comment }} />;
}

// ✅ GOOD: Sanitized HTML
import DOMPurify from 'dompurify';

function UserComment({ comment }: { comment: string }) {
  return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(comment) }} />;
}

// ✅ BETTER: No HTML, just text
function UserComment({ comment }: { comment: string }) {
  return <div>{comment}</div>;
}

// ❌ BAD: Token in localStorage (XSS vulnerable)
localStorage.setItem('token', response.token);

// ✅ GOOD: HttpOnly cookie (set by server)
// Or use secure session management library

// ❌ BAD: Hardcoded API key
const API_KEY = "pk_live_abc123xyz";

// ✅ GOOD: Environment variable
const API_KEY = process.env.NEXT_PUBLIC_API_KEY;

// ❌ BAD: No CSRF protection
async function transferMoney(to: string, amount: number) {
  await fetch('/api/transfer', {
    method: 'POST',
    body: JSON.stringify({ to, amount })
  });
}

// ✅ GOOD: Include CSRF token
async function transferMoney(to: string, amount: number) {
  const csrfToken = getCsrfToken();
  await fetch('/api/transfer', {
    method: 'POST',
    headers: {
      'X-CSRF-Token': csrfToken
    },
    body: JSON.stringify({ to, amount })
  });
}
```

**Frontend Security Checklist**:
- [ ] No `dangerouslySetInnerHTML` with user input
- [ ] No sensitive tokens in localStorage
- [ ] No hardcoded API keys or secrets
- [ ] CSRF protection for state-changing operations
- [ ] Input validation on all form inputs
- [ ] Output sanitization for user-generated content
- [ ] HTTPS enforced (check in production)
- [ ] No sensitive data in console.log
- [ ] Proper authentication checks on protected routes
- [ ] Secure password input (no autocomplete on sensitive fields)

#### 3.2 React Performance Review

Identify bottlenecks and optimization opportunities:

```typescript
// ❌ BAD: Unnecessary re-renders
function ProductList({ products }: { products: Product[] }) {
  const sortedProducts = products.sort((a, b) => b.price - a.price);
  // Re-sorts on every render!

  return (
    <div>
      {sortedProducts.map(p => (
        <ProductCard key={p.id} product={p} onUpdate={() => updateProduct(p.id)} />
      ))}
    </div>
  );
}

// ✅ GOOD: Memoized sorting and callbacks
function ProductList({ products }: { products: Product[] }) {
  const sortedProducts = useMemo(
    () => [...products].sort((a, b) => b.price - a.price),
    [products]
  );

  const handleUpdate = useCallback((id: string) => {
    updateProduct(id);
  }, []);

  return (
    <div>
      {sortedProducts.map(p => (
        <ProductCard key={p.id} product={p} onUpdate={() => handleUpdate(p.id)} />
      ))}
    </div>
  );
}

// ❌ BAD: No memoization for expensive child
function ExpensiveChild({ data }: { data: Data }) {
  // Complex rendering logic
  return <div>{/* ... */}</div>;
}

// ✅ GOOD: Memoized component
const ExpensiveChild = memo(function ExpensiveChild({ data }: { data: Data }) {
  // Complex rendering logic
  return <div>{/* ... */}</div>;
});

// ❌ BAD: Memory leak - no cleanup
function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);
    // No cleanup!
  }, []);

  return <div>{count}</div>;
}

// ✅ GOOD: Proper cleanup
function Timer() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(c => c + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return <div>{count}</div>;
}

// ❌ BAD: No lazy loading for large components
import HeavyChart from './HeavyChart';
import HeavyEditor from './HeavyEditor';

// ✅ GOOD: Lazy loading
const HeavyChart = lazy(() => import('./HeavyChart'));
const HeavyEditor = lazy(() => import('./HeavyEditor'));

function Dashboard() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart />
      <HeavyEditor />
    </Suspense>
  );
}

// ❌ BAD: Inline object/function props
<Child
  config={{ theme: 'dark' }}
  onUpdate={() => doSomething()}
/>

// ✅ GOOD: Memoized props
const config = useMemo(() => ({ theme: 'dark' }), []);
const handleUpdate = useCallback(() => doSomething(), []);

<Child config={config} onUpdate={handleUpdate} />
```

**React Performance Checklist**:
- [ ] Memoization for expensive calculations (useMemo)
- [ ] Memoized callbacks (useCallback) for child components
- [ ] memo() for expensive child components
- [ ] Proper cleanup in useEffect (intervals, subscriptions)
- [ ] Lazy loading for heavy components
- [ ] Code splitting for routes
- [ ] Virtualization for long lists (react-window)
- [ ] Debouncing for frequent events (search, scroll)
- [ ] Image optimization (next/image, lazy loading)
- [ ] No inline objects/functions as props
- [ ] Proper key usage (unique IDs, not indexes)
- [ ] Avoid deep prop drilling (use Context/Zustand)

#### 3.3 Component Architecture Review

Check for proper separation of concerns:

```typescript
// ❌ BAD: Everything in one component
function UserProfile() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // API call in component
  useEffect(() => {
    setLoading(true);
    fetch('/api/user')
      .then(res => res.json())
      .then(data => {
        setUser(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, []);

  // Business logic in component
  const fullName = user ? `${user.firstName} ${user.lastName}` : '';
  const isAdult = user?.age >= 18;

  // Validation in component
  const validateEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return <div>{fullName}</div>;
}

// ✅ GOOD: Layered architecture
// api/userApi.ts (Data Access Layer)
export const userApi = {
  getUser: async (): Promise<User> => {
    const response = await fetch('/api/user');
    if (!response.ok) throw new Error('Failed to fetch user');
    return response.json();
  }
};

// hooks/useUser.ts (Business Logic Layer)
export function useUser() {
  const { data: user, isLoading, error } = useQuery({
    queryKey: ['user'],
    queryFn: userApi.getUser
  });

  const fullName = user ? `${user.firstName} ${user.lastName}` : '';
  const isAdult = user?.age >= 18;

  return { user, fullName, isAdult, isLoading, error };
}

// utils/validation.ts (Business Logic Layer)
export const emailSchema = z.string().email();

export function validateEmail(email: string): boolean {
  return emailSchema.safeParse(email).success;
}

// components/UserProfile.tsx (Presentation Layer)
export function UserProfile() {
  const { fullName, isLoading, error } = useUser();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return <div className="text-lg font-semibold">{fullName}</div>;
}
```

**Architecture Checklist**:
- [ ] Layered architecture (Presentation, Business Logic, Data Access)
- [ ] No API calls directly in components
- [ ] No business logic in components
- [ ] Hooks for reusable logic
- [ ] Zustand/Context for global state
- [ ] React Query for server state
- [ ] No circular dependencies
- [ ] Single Responsibility Principle
- [ ] Components are small and focused (<200 lines)
- [ ] Proper prop types (TypeScript interfaces)

#### 3.4 Type Safety Review

Check for proper TypeScript usage:

```typescript
// ❌ BAD: Using 'any'
function processData(data: any) {
  return data.value;
}

// ✅ GOOD: Proper types
interface ProcessData {
  value: string;
  count: number;
}

function processData(data: ProcessData): string {
  return data.value;
}

// ❌ BAD: Non-null assertion without justification
function getUser(users: User[], id: string) {
  return users.find(u => u.id === id)!.name; // Dangerous!
}

// ✅ GOOD: Proper null handling
function getUser(users: User[], id: string): string | null {
  return users.find(u => u.id === id)?.name ?? null;
}

// ❌ BAD: No runtime validation
function LoginForm() {
  const handleSubmit = (data: unknown) => {
    // Assuming data structure without validation
    login(data);
  };
}

// ✅ GOOD: Runtime validation with Zod
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

type LoginData = z.infer<typeof loginSchema>;

function LoginForm() {
  const handleSubmit = (data: unknown) => {
    try {
      const validatedData = loginSchema.parse(data);
      login(validatedData); // Type-safe
    } catch (err) {
      // Handle validation errors
    }
  };
}

// ❌ BAD: Implicit any in event handlers
<input onChange={(e) => setValue(e.target.value)} />
// 'e' is implicitly 'any' in some configs

// ✅ GOOD: Explicit types
<input onChange={(e: React.ChangeEvent<HTMLInputElement>) => setValue(e.target.value)} />

// ✅ BETTER: Typed handler
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

<input onChange={handleChange} />
```

**Type Safety Checklist**:
- [ ] No 'any' types (except where truly necessary)
- [ ] No non-null assertions (!) without justification
- [ ] Proper interface/type definitions for props
- [ ] Runtime validation with Zod for external data
- [ ] Type guards for discriminated unions
- [ ] Explicit types for event handlers
- [ ] Strict mode enabled in tsconfig.json
- [ ] No implicit any
- [ ] Proper generic usage in hooks

#### 3.5 Accessibility Review

Check WCAG 2.1 AA compliance:

```typescript
// ❌ BAD: No keyboard support, no ARIA labels
<div onClick={handleClick}>
  <input type="text" placeholder="Name" />
  <div className="text-red-500">Error message</div>
</div>

// ✅ GOOD: Semantic HTML, ARIA labels, keyboard support
<form onSubmit={handleSubmit}>
  <label htmlFor="name" className="block text-sm font-medium">
    Name
  </label>
  <input
    id="name"
    type="text"
    aria-label="Enter your name"
    aria-describedby="name-error"
    aria-invalid={hasError}
    className="mt-1 block w-full"
  />
  {hasError && (
    <p id="name-error" role="alert" className="text-red-500 text-sm">
      Error message
    </p>
  )}
  <button type="submit" className="mt-4 px-4 py-2 bg-blue-500">
    Submit
  </button>
</form>

// ❌ BAD: No alt text, poor color contrast
<div className="bg-gray-200 text-gray-300">
  <img src="/icon.png" />
  Click here
</div>

// ✅ GOOD: Alt text, proper contrast (WCAG AA)
<div className="bg-gray-900 text-white">
  <img src="/icon.png" alt="Settings icon" />
  <button className="text-lg font-medium">
    Open Settings
  </button>
</div>

// ❌ BAD: Custom select without keyboard navigation
function CustomSelect({ options }) {
  const [open, setOpen] = useState(false);

  return (
    <div onClick={() => setOpen(!open)}>
      {open && options.map(opt => (
        <div onClick={() => selectOption(opt)}>{opt}</div>
      ))}
    </div>
  );
}

// ✅ GOOD: Accessible custom select
function CustomSelect({ options }: { options: string[] }) {
  const [open, setOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      setSelectedIndex(i => Math.min(i + 1, options.length - 1));
    } else if (e.key === 'ArrowUp') {
      setSelectedIndex(i => Math.max(i - 1, 0));
    } else if (e.key === 'Enter') {
      selectOption(options[selectedIndex]);
    }
  };

  return (
    <div
      role="combobox"
      aria-expanded={open}
      aria-haspopup="listbox"
      tabIndex={0}
      onKeyDown={handleKeyDown}
      onClick={() => setOpen(!open)}
    >
      {open && (
        <ul role="listbox">
          {options.map((opt, index) => (
            <li
              key={opt}
              role="option"
              aria-selected={index === selectedIndex}
              onClick={() => selectOption(opt)}
            >
              {opt}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

**Accessibility Checklist**:
- [ ] Semantic HTML elements (button, nav, main, etc.)
- [ ] ARIA labels for interactive elements
- [ ] Keyboard navigation support (Tab, Enter, Arrows)
- [ ] Focus management (visible focus states)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Alt text for all images
- [ ] Form labels properly associated (htmlFor)
- [ ] Error messages use role="alert"
- [ ] No keyboard traps
- [ ] Skip links for main content
- [ ] Headings in logical order (h1, h2, h3)
- [ ] Interactive elements have proper roles

#### 3.6 Responsive Design Review

Check Tailwind/responsive patterns:

```typescript
// ❌ BAD: Fixed widths, no responsive classes
<div className="w-800 h-600">
  <img src="/hero.jpg" className="w-full" />
</div>

// ✅ GOOD: Responsive Tailwind classes
<div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <img
    src="/hero.jpg"
    alt="Hero"
    className="w-full h-auto object-cover md:h-96 lg:h-[500px]"
  />
</div>

// ❌ BAD: No mobile considerations
<div className="flex gap-8">
  <Sidebar />
  <MainContent />
</div>

// ✅ GOOD: Mobile-first responsive layout
<div className="flex flex-col lg:flex-row gap-4 lg:gap-8">
  <aside className="w-full lg:w-64">
    <Sidebar />
  </aside>
  <main className="flex-1">
    <MainContent />
  </main>
</div>

// ❌ BAD: Fixed font sizes
<h1 className="text-32">Title</h1>

// ✅ GOOD: Responsive typography
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
  Title
</h1>
```

**Responsive Design Checklist**:
- [ ] Mobile-first approach (base styles for mobile)
- [ ] Proper breakpoints (sm, md, lg, xl, 2xl)
- [ ] Flexible layouts (flex, grid)
- [ ] Responsive images (w-full h-auto, object-fit)
- [ ] Responsive typography (responsive text sizes)
- [ ] Touch-friendly hit areas (min 44x44px)
- [ ] No horizontal scrolling on mobile
- [ ] Tested on multiple screen sizes

#### 3.7 Code Quality Review

Evaluate readability and maintainability:

```typescript
// ❌ BAD: Unclear names, deeply nested
function p(d) {
  if (d) {
    if (d.u) {
      if (d.u.n) {
        if (d.u.n.length > 0) {
          return d.u.n;
        }
      }
    }
  }
  return 'Anonymous';
}

// ✅ GOOD: Clear names, early returns
function getUserName(data: UserData | null): string {
  if (!data?.user?.name) return 'Anonymous';
  if (data.user.name.length === 0) return 'Anonymous';

  return data.user.name;
}

// ✅ BETTER: Optional chaining
function getUserName(data: UserData | null): string {
  return data?.user?.name || 'Anonymous';
}

// ❌ BAD: Magic numbers and strings
if (user.age > 18 && status === 'active') {
  grantAccess();
}

// ✅ GOOD: Named constants
const MINIMUM_AGE = 18;
const USER_STATUS = {
  ACTIVE: 'active',
  INACTIVE: 'inactive'
} as const;

if (user.age > MINIMUM_AGE && status === USER_STATUS.ACTIVE) {
  grantAccess();
}

// ❌ BAD: Long component with multiple responsibilities
function UserDashboard() {
  // 300 lines of code handling:
  // - User data fetching
  // - Analytics tracking
  // - Notification handling
  // - UI rendering
}

// ✅ GOOD: Split into focused components
function UserDashboard() {
  return (
    <div>
      <UserProfile />
      <UserAnalytics />
      <UserNotifications />
    </div>
  );
}
```

**Code Quality Checklist**:
- [ ] Clear, descriptive names (getUserName, not gn)
- [ ] No magic numbers or strings (use constants)
- [ ] Early returns instead of deep nesting
- [ ] Small functions/components (<100 lines)
- [ ] Single Responsibility Principle
- [ ] DRY (Don't Repeat Yourself)
- [ ] No commented-out code
- [ ] No console.log in production code
- [ ] Consistent code style
- [ ] Proper error handling

#### 3.8 React Hooks Best Practices

```typescript
// ❌ BAD: Missing dependencies
useEffect(() => {
  fetchData(userId, filter);
}, []); // userId and filter are missing!

// ✅ GOOD: All dependencies included
useEffect(() => {
  fetchData(userId, filter);
}, [userId, filter]);

// ❌ BAD: Object dependency (recreated every render)
const options = { sort: 'asc', limit: 10 };

useEffect(() => {
  fetchData(options);
}, [options]); // Will run every render!

// ✅ GOOD: Memoized object
const options = useMemo(() => ({
  sort: 'asc',
  limit: 10
}), []);

useEffect(() => {
  fetchData(options);
}, [options]);

// ❌ BAD: Stale closure
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(count + 1); // Uses stale count!
    }, 1000);

    return () => clearInterval(interval);
  }, []); // Empty deps, count is stale

  return <div>{count}</div>;
}

// ✅ GOOD: Functional update
function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCount(c => c + 1); // Uses current count
    }, 1000);

    return () => clearInterval(interval);
  }, []); // Empty deps OK now

  return <div>{count}</div>;
}
```

### Step 4: Provide Structured Feedback

Format review results clearly:

```markdown
## Code Review: [Component/Feature Name]

### Summary
[Brief overall assessment: Excellent/Good/Needs Improvement/Critical Issues]

### Critical Issues 🚨
1. **[Issue Title]** - [file:line]
   - **Problem**: [Description]
   - **Impact**: [Security/Performance/Accessibility]
   - **Fix**:
   ```typescript
   // Suggested fix
   ```

### High Priority ⚠️
[Same format]

### Medium Priority ⚡
[Same format]

### Low Priority 💡
[Same format]

### What's Good ✅
- [Highlight positive aspects]
- [Good practices used]

### Recommendations
1. [Actionable improvement]
2. [Actionable improvement]

### Overall Score
- Security: 8/10
- Performance: 7/10
- Code Quality: 9/10
- Accessibility: 6/10
- Type Safety: 8/10

**Overall: 7.6/10**
```

## Integration with Other Skills

### With feature-builder
- Review complete features (UI + business logic + API)
- Ensure layered architecture is properly implemented

### With react-component-generator
- Review generated components
- Check template usage and customization

### With ui-analyzer
- Review UI code generated from design screenshots
- Verify responsive design implementation

## Best Practices

1. **Be Constructive**: Always provide actionable fixes with code examples
2. **Prioritize**: Focus on critical issues (security, accessibility) first
3. **Explain Why**: Help user understand the reasoning and impact
4. **Show Before/After**: Provide clear code examples
5. **Be Specific**: Reference exact lines and files
6. **Balance**: Highlight what's good too
7. **Be Practical**: Consider project constraints and deadlines
8. **Educate**: Explain React/frontend concepts when needed

## Severity Levels

- 🚨 **CRITICAL**: Security vulnerabilities (XSS, CSRF), data exposure, crashes
- ⚠️ **HIGH**: Performance issues (memory leaks), accessibility violations, broken UX
- ⚡ **MEDIUM**: Code quality, maintainability, missing TypeScript types
- 💡 **LOW**: Code style, documentation, minor optimizations

## Reference Files

- `references/frontend-security.md` - Frontend security best practices
- `references/react-patterns.md` - React patterns and anti-patterns
- `references/accessibility-guide.md` - WCAG compliance guide

This skill enables thorough, professional frontend code reviews that improve code quality, security, and user experience!
