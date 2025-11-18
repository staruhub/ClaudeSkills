# Layered Architecture for React Features

## Overview

This document defines the layered architecture approach for building complete React features with clear separation of concerns.

## Architecture Layers

```
┌─────────────────────────────────────────┐
│         Presentation Layer (UI)         │  ← Components, Hooks, Styling
├─────────────────────────────────────────┤
│       Business Logic Layer              │  ← State, Validation, Rules
├─────────────────────────────────────────┤
│       Data Access Layer (API)           │  ← API Calls, Data Fetching
├─────────────────────────────────────────┤
│       External Services                 │  ← Backend APIs, Third-party
└─────────────────────────────────────────┘
```

## Layer 1: Presentation Layer (UI)

**Responsibility**: Display data and handle user interactions

**Technologies**:
- React components
- Tailwind CSS
- react-component-generator templates

**Structure**:
```
features/
└── user-auth/
    └── components/
        ├── LoginForm.tsx
        ├── RegisterForm.tsx
        └── PasswordResetForm.tsx
```

**Example**:
```typescript
// features/user-auth/components/LoginForm.tsx
import { useAuth } from '../hooks/useAuth';

export const LoginForm: React.FC = () => {
  const { login, isLoading, error } = useAuth();

  const handleSubmit = async (data: LoginFormData) => {
    await login(data);  // Business logic in hook
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* UI components */}
    </form>
  );
};
```

**Principles**:
- ✅ Components only handle UI rendering and events
- ✅ No business logic in components
- ✅ No direct API calls
- ✅ Receive data via props or hooks
- ✅ Emit events upward

## Layer 2: Business Logic Layer

**Responsibility**: Business rules, state management, data transformation

**Technologies**:
- Zustand (global state)
- React hooks (local logic)
- Validation libraries (Zod)

**Structure**:
```
features/
└── user-auth/
    ├── hooks/
    │   ├── useAuth.ts          # Authentication logic
    │   └── useLoginForm.ts     # Form-specific logic
    ├── stores/
    │   └── authStore.ts        # Global auth state
    ├── utils/
    │   ├── validation.ts       # Validation rules
    │   └── transforms.ts       # Data transformations
    └── types/
        └── auth.types.ts       # TypeScript types
```

### 2.1 Custom Hooks (Business Logic)

```typescript
// features/user-auth/hooks/useAuth.ts
import { useAuthStore } from '../stores/authStore';
import { authApi } from '../api/authApi';

export function useAuth() {
  const { setUser, setToken, clearAuth } = useAuthStore();

  const login = async (credentials: LoginCredentials) => {
    // Business logic
    const response = await authApi.login(credentials);

    // Store token
    setToken(response.accessToken);

    // Store user
    setUser(response.user);

    // Side effects
    localStorage.setItem('token', response.accessToken);

    return response;
  };

  const logout = () => {
    // Business logic
    clearAuth();
    localStorage.removeItem('token');
    // Redirect or other side effects
  };

  return { login, logout };
}
```

### 2.2 State Management (Zustand)

```typescript
// features/user-auth/stores/authStore.ts
import { create } from 'zustand';

interface AuthStore {
  // State
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;

  // Actions
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  // Initial state
  user: null,
  token: null,
  isAuthenticated: false,

  // Actions
  setUser: (user) => set({ user, isAuthenticated: true }),
  setToken: (token) => set({ token }),
  clearAuth: () => set({ user: null, token: null, isAuthenticated: false }),
}));
```

### 2.3 Validation Rules

```typescript
// features/user-auth/utils/validation.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export const registerSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase letter')
    .regex(/[0-9]/, 'Must contain number'),
  name: z.string().min(2, 'Name must be at least 2 characters'),
});

export function validateLogin(data: unknown) {
  return loginSchema.parse(data);
}
```

## Layer 3: Data Access Layer (API)

**Responsibility**: HTTP requests, data fetching, caching

**Technologies**:
- React Query / TanStack Query
- Axios / fetch
- API client functions

**Structure**:
```
features/
└── user-auth/
    └── api/
        ├── authApi.ts          # API client
        ├── queries.ts          # React Query hooks
        └── types.ts            # API types
```

### 3.1 API Client

```typescript
// features/user-auth/api/authApi.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

export const authApi = {
  login: async (credentials: LoginCredentials) => {
    const { data } = await apiClient.post('/auth/login', credentials);
    return data;
  },

  register: async (userData: RegisterData) => {
    const { data } = await apiClient.post('/auth/register', userData);
    return data;
  },

  logout: async () => {
    const { data } = await apiClient.post('/auth/logout');
    return data;
  },

  refreshToken: async (refreshToken: string) => {
    const { data } = await apiClient.post('/auth/refresh', { refreshToken });
    return data;
  },
};
```

### 3.2 React Query Integration

```typescript
// features/user-auth/api/queries.ts
import { useMutation, useQuery } from '@tanstack/react-query';
import { authApi } from './authApi';

export function useLogin() {
  return useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      // Handle success (store token, redirect, etc.)
    },
    onError: (error) => {
      // Handle error
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: authApi.register,
  });
}

export function useCurrentUser() {
  return useQuery({
    queryKey: ['currentUser'],
    queryFn: authApi.getCurrentUser,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
```

## Complete Feature Structure

```
features/
└── user-auth/
    ├── components/                 # Presentation Layer
    │   ├── LoginForm.tsx
    │   ├── RegisterForm.tsx
    │   └── index.ts
    ├── hooks/                      # Business Logic Layer
    │   ├── useAuth.ts
    │   ├── useLoginForm.ts
    │   └── index.ts
    ├── stores/                     # Business Logic Layer
    │   ├── authStore.ts
    │   └── index.ts
    ├── api/                        # Data Access Layer
    │   ├── authApi.ts
    │   ├── queries.ts
    │   └── index.ts
    ├── utils/                      # Business Logic Layer
    │   ├── validation.ts
    │   ├── transforms.ts
    │   └── index.ts
    ├── types/                      # Shared Types
    │   ├── auth.types.ts
    │   └── index.ts
    └── index.ts                    # Public API
```

## Data Flow

```
User Action
    ↓
UI Component (Presentation Layer)
    ↓
Custom Hook (Business Logic Layer)
    ↓
API Call (Data Access Layer)
    ↓
Backend API (External Service)
    ↓
Response flows back up
    ↓
State Update (Business Logic Layer)
    ↓
UI Re-render (Presentation Layer)
```

## Example: Complete Login Feature

### Step 1: Types

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

### Step 2: API Layer

```typescript
// features/user-auth/api/authApi.ts
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials),
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    return response.json();
  },
};
```

### Step 3: Business Logic Layer

```typescript
// features/user-auth/stores/authStore.ts
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

  const { mutate: login, isPending, error } = useMutation({
    mutationFn: authApi.login,
    onSuccess: (data) => {
      setToken(data.accessToken);
      setUser(data.user);
      localStorage.setItem('token', data.accessToken);
    },
  });

  return { login, isLoading: isPending, error };
}
```

### Step 4: Presentation Layer

```typescript
// features/user-auth/components/LoginForm.tsx
export const LoginForm: React.FC = () => {
  const { login, isLoading, error } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        className="w-full px-4 py-2 border rounded"
      />
      <input
        type="password"
        value={formData.password}
        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        className="w-full px-4 py-2 border rounded"
      />
      {error && <p className="text-red-600">{error.message}</p>}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full px-4 py-2 bg-blue-500 text-white rounded"
      >
        {isLoading ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
};
```

## Benefits of This Architecture

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Each layer can be tested independently
3. **Reusability**: Business logic can be shared across components
4. **Maintainability**: Changes are localized to specific layers
5. **Scalability**: Easy to add new features following the same pattern
6. **Type Safety**: TypeScript types flow through all layers

## Best Practices

1. **Never skip layers**: UI shouldn't call APIs directly
2. **Keep components dumb**: Move logic to hooks/stores
3. **Centralize state**: Use Zustand for shared state
4. **Use React Query**: For server state management
5. **Validate early**: Validate in business logic layer
6. **Handle errors**: At every layer appropriately
7. **Type everything**: Use TypeScript throughout

This architecture ensures clean, maintainable, and scalable React features!
