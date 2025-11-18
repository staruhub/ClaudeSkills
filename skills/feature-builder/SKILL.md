---
name: feature-builder
description: Build complete React features with proper layered architecture including UI components, business logic, API integration, and state management. Use this skill when users request implementing features like "user authentication", "shopping cart", "product listing", "file upload", or any complete functionality that requires UI + business logic + data fetching. Generates all layers - presentation (components), business logic (hooks/stores/validation), and data access (API calls/React Query). Integrates with react-component-generator for UI and provides production-ready, maintainable code following best practices.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Feature Builder

This skill builds complete, production-ready React features with proper separation of concerns across presentation, business logic, and data access layers.

## Purpose

Transform feature requirements into complete, working implementations that include:
1. **UI Components** - Using react-component-generator
2. **Business Logic** - Hooks, stores, validation, transformations
3. **API Integration** - Data fetching, mutations, caching
4. **State Management** - Zustand for global state, React Query for server state
5. **Error Handling** - Comprehensive error management
6. **Type Safety** - Full TypeScript support

## When to Use This Skill

Use this skill when:
- User requests a complete feature (not just a UI component)
- Request involves business logic and data management
- User mentions: "implement", "build", "create feature"
- Examples:
  - "Implement user authentication"
  - "Build a shopping cart"
  - "Create a product listing with filters"
  - "Add file upload functionality"
  - "Implement real-time notifications"

## Architecture

Features are built with **3-layer architecture**:

```
┌──────────────────────────────────────┐
│   Presentation Layer                 │  ← UI Components
│   (React components, Tailwind CSS)   │
├──────────────────────────────────────┤
│   Business Logic Layer               │  ← Hooks, Stores, Validation
│   (Zustand, hooks, utils)            │
├──────────────────────────────────────┤
│   Data Access Layer                  │  ← API Calls, React Query
│   (API client, queries, mutations)   │
└──────────────────────────────────────┘
```

Reference `references/layered-architecture.md` for complete details.

## Workflow

### Step 1: Analyze Feature Request

When user requests a feature, analyze:

1. **Feature Type**:
   - Authentication/Authorization
   - CRUD operations
   - File handling
   - Real-time updates
   - Search/Filter
   - Complex workflows (multi-step, cart, checkout)

2. **Required Layers**:
   - Does it need UI? (Almost always yes)
   - Does it need business logic? (Forms, validation, calculations)
   - Does it need API integration? (Server data, persistence)
   - Does it need global state? (Shared across components)

3. **Dependencies**:
   - What other features does it depend on?
   - What APIs does it need?
   - What libraries are required? (React Query, Zustand, Zod)

### Step 2: Plan Architecture

Design the feature structure:

```
features/
└── [feature-name]/
    ├── components/         # Presentation Layer
    │   ├── FeatureMain.tsx
    │   ├── FeatureForm.tsx
    │   └── index.ts
    ├── hooks/              # Business Logic
    │   ├── useFeature.ts
    │   └── index.ts
    ├── stores/             # Global State (if needed)
    │   ├── featureStore.ts
    │   └── index.ts
    ├── api/                # Data Access
    │   ├── featureApi.ts
    │   ├── queries.ts
    │   └── index.ts
    ├── utils/              # Utilities
    │   ├── validation.ts
    │   └── transforms.ts
    ├── types/              # TypeScript Types
    │   └── feature.types.ts
    └── index.ts            # Public API
```

### Step 3: Clarify Requirements (Interactive)

Use `AskUserQuestion` to gather necessary details:

```typescript
AskUserQuestion({
  questions: [
    {
      question: "What data needs to be managed?",
      header: "Data",
      multiSelect: false,
      options: [
        { label: "User data", description: "Authentication, profiles" },
        { label: "Products", description: "E-commerce items" },
        { label: "Posts/Content", description: "Blog posts, articles" },
        { label: "Files", description: "File uploads/downloads" },
      ]
    },
    {
      question: "What operations are needed?",
      header: "Operations",
      multiSelect: true,
      options: [
        { label: "Create", description: "Add new items" },
        { label: "Read/List", description: "Fetch and display data" },
        { label: "Update", description: "Modify existing items" },
        { label: "Delete", description: "Remove items" },
        { label: "Search", description: "Find specific items" },
        { label: "Filter", description: "Filter by criteria" },
      ]
    },
    {
      question: "Does this need authentication?",
      header: "Auth",
      multiSelect: false,
      options: [
        { label: "Yes, required", description: "User must be logged in" },
        { label: "Optional", description: "Works with or without auth" },
        { label: "No", description: "Public feature" },
      ]
    },
    {
      question: "Any additional requirements?",
      header: "Extra",
      multiSelect: false,
      options: [
        { label: "No, that's all", description: "Just the basics" },
        { label: "Yes, let me specify", description: "Use 'Other' to describe" },
      ]
    }
  ]
})
```

### Step 4: Generate Feature Code

Generate code for each layer:

#### 4.1 Types First

```typescript
// features/user-auth/types/auth.types.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  accessToken: string;
  refreshToken: string;
}
```

#### 4.2 API Layer

```typescript
// features/user-auth/api/authApi.ts
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) throw new Error('Login failed');
    return response.json();
  },
  // ... other methods
};

// features/user-auth/api/queries.ts
import { useMutation } from '@tanstack/react-query';

export function useLogin() {
  return useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      // Handle success
    },
  });
}
```

#### 4.3 Business Logic Layer

```typescript
// features/user-auth/stores/authStore.ts
import { create } from 'zustand';

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  setUser: (user) => set({ user, isAuthenticated: true }),
  setToken: (token) => set({ token }),
  clearAuth: () => set({ user: null, token: null, isAuthenticated: false }),
}));

// features/user-auth/hooks/useAuth.ts
export function useAuth() {
  const { setUser, setToken } = useAuthStore();
  const { mutate: login, isPending, error } = useLogin();

  const handleLogin = async (credentials: LoginCredentials) => {
    return new Promise((resolve, reject) => {
      login(credentials, {
        onSuccess: (data) => {
          setToken(data.accessToken);
          setUser(data.user);
          localStorage.setItem('token', data.accessToken);
          resolve(data);
        },
        onError: (error) => reject(error),
      });
    });
  };

  return { login: handleLogin, isLoading: isPending, error };
}

// features/user-auth/utils/validation.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});
```

#### 4.4 Presentation Layer

```typescript
// features/user-auth/components/LoginForm.tsx
import { useAuth } from '../hooks/useAuth';
import { loginSchema } from '../utils/validation';

export const LoginForm: React.FC = () => {
  const { login, isLoading, error } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validate
    try {
      loginSchema.parse(formData);
      setValidationErrors({});
    } catch (err) {
      if (err instanceof z.ZodError) {
        const errors = err.errors.reduce((acc, error) => {
          acc[error.path[0]] = error.message;
          return acc;
        }, {} as Record<string, string>);
        setValidationErrors(errors);
        return;
      }
    }

    // Submit
    try {
      await login(formData);
      router.push('/dashboard');
    } catch (err) {
      // Error handled by useAuth
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
        />
        {validationErrors.email && (
          <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md"
        />
        {validationErrors.password && (
          <p className="mt-1 text-sm text-red-600">{validationErrors.password}</p>
        )}
      </div>

      {error && (
        <p className="text-sm text-red-600">Invalid email or password</p>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50"
      >
        {isLoading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};
```

### Step 5: Provide Implementation Guide

After generating code, provide:

1. **Installation requirements**:
```bash
npm install @tanstack/react-query zustand zod axios
```

2. **Setup instructions**:
```typescript
// app/providers.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

3. **Usage examples**:
```typescript
// app/login/page.tsx
import { LoginForm } from '@/features/user-auth';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <LoginForm />
    </div>
  );
}
```

4. **Testing suggestions**:
```typescript
// features/user-auth/__tests__/useAuth.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useAuth } from '../hooks/useAuth';

describe('useAuth', () => {
  it('should login successfully', async () => {
    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.login({
        email: 'test@example.com',
        password: 'password123',
      });
    });

    expect(result.current.error).toBeNull();
  });
});
```

## Integration with Other Skills

### With react-component-generator

When building UI components:
1. Use react-component-generator templates as base
2. Enhance with business logic integration
3. Connect to hooks and stores

### With ui-analyzer

When implementing from design:
1. Use ui-analyzer to extract UI structure
2. Build business logic layer
3. Connect UI to business logic

### With prompt-optimizer

If feature request is vague:
1. Activate prompt-optimizer first
2. Clarify requirements
3. Then build feature

## Common Feature Patterns

Reference `references/business-logic-patterns.md` for detailed patterns:

1. **Authentication & Authorization**
2. **Form Handling with Validation**
3. **Data Fetching with React Query**
4. **File Upload**
5. **Search & Filtering**
6. **Shopping Cart**
7. **Real-time Updates (WebSocket)**

## Best Practices

1. **Always use layered architecture** - Separation of concerns
2. **TypeScript everything** - Full type safety
3. **Validate on both sides** - Client (UX) and server (security)
4. **Handle errors gracefully** - User-friendly error messages
5. **Optimize for performance** - React Query caching, memoization
6. **Make it accessible** - ARIA labels, keyboard navigation
7. **Test business logic** - Unit tests for hooks and stores
8. **Document complex logic** - Comments for future maintenance

## Example Complete Feature: User Authentication

**User Request**: "Implement user authentication with login and registration"

**Generated Structure**:
```
features/
└── user-auth/
    ├── components/
    │   ├── LoginForm.tsx
    │   ├── RegisterForm.tsx
    │   ├── ProtectedRoute.tsx
    │   └── index.ts
    ├── hooks/
    │   ├── useAuth.ts
    │   ├── usePermission.ts
    │   └── index.ts
    ├── stores/
    │   ├── authStore.ts
    │   └── index.ts
    ├── api/
    │   ├── authApi.ts
    │   ├── queries.ts
    │   └── index.ts
    ├── utils/
    │   ├── validation.ts
    │   └── index.ts
    ├── types/
    │   └── auth.types.ts
    └── index.ts
```

**Includes**:
- ✅ Login form with validation
- ✅ Registration form with validation
- ✅ JWT token management
- ✅ Protected routes
- ✅ Permission checking
- ✅ Persistent auth state
- ✅ Error handling
- ✅ Loading states
- ✅ Type-safe API calls

## Output Format

When generating a feature, provide:

```markdown
## [Feature Name] Implementation

### Overview
[Brief description of what was implemented]

### Structure
[Directory tree showing all files]

### Installation
```bash
[Required dependencies]
```

### Code

#### Types
[TypeScript interfaces and types]

#### API Layer
[API client and React Query hooks]

#### Business Logic
[Zustand stores and custom hooks]

#### UI Components
[React components]

#### Validation
[Validation schemas]

### Setup Instructions
[How to integrate into the project]

### Usage Examples
[How to use the feature]

### Testing
[Test examples]

### Next Steps
[What else might be needed]
```

This skill enables rapid development of production-ready features with proper architecture and best practices!
