# Common Business Logic Patterns

## Overview

This document provides ready-to-use patterns for common business logic scenarios in React applications.

## Pattern 1: Authentication & Authorization

### Login Flow

```typescript
// hooks/useAuth.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthStore {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (credentials) => {
        try {
          const response = await authApi.login(credentials);

          set({
            user: response.user,
            token: response.accessToken,
            isAuthenticated: true,
          });

          // Store token
          localStorage.setItem('token', response.accessToken);

          // Set default auth header
          axios.defaults.headers.common['Authorization'] = `Bearer ${response.accessToken}`;
        } catch (error) {
          set({ user: null, token: null, isAuthenticated: false });
          throw error;
        }
      },

      logout: () => {
        set({ user: null, token: null, isAuthenticated: false });
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
      },

      checkAuth: async () => {
        const token = localStorage.getItem('token');
        if (!token) {
          set({ isAuthenticated: false });
          return;
        }

        try {
          const user = await authApi.getCurrentUser();
          set({ user, token, isAuthenticated: true });
        } catch (error) {
          get().logout();
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ token: state.token }),
    }
  )
);

// Usage in component
export function LoginPage() {
  const login = useAuthStore((state) => state.login);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: LoginFormData) => {
    try {
      await login(data);
      router.push('/dashboard');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return <LoginForm onSubmit={handleSubmit} error={error} />;
}
```

### Protected Routes

```typescript
// components/ProtectedRoute.tsx
export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const checkAuth = useAuthStore((state) => state.checkAuth);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
```

### Role-Based Access Control

```typescript
// hooks/usePermission.ts
export function usePermission() {
  const user = useAuthStore((state) => state.user);

  const can = (permission: string) => {
    return user?.permissions?.includes(permission) ?? false;
  };

  const isRole = (role: string) => {
    return user?.role === role;
  };

  return { can, isRole };
}

// Usage
export function AdminPanel() {
  const { isRole } = usePermission();

  if (!isRole('admin')) {
    return <div>Access Denied</div>;
  }

  return <AdminDashboard />;
}
```

## Pattern 2: Form Handling with Validation

### Complex Form with Validation

```typescript
// hooks/useForm.ts
export function useForm<T extends Record<string, any>>(
  initialValues: T,
  validationSchema: z.ZodSchema<T>
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (field: keyof T) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setValues({ ...values, [field]: e.target.value });

    // Clear error on change
    if (errors[field]) {
      setErrors({ ...errors, [field]: undefined });
    }
  };

  const handleBlur = (field: keyof T) => () => {
    setTouched({ ...touched, [field]: true });

    // Validate single field
    try {
      validationSchema.shape[field].parse(values[field]);
      setErrors({ ...errors, [field]: undefined });
    } catch (err) {
      if (err instanceof z.ZodError) {
        setErrors({ ...errors, [field]: err.errors[0].message });
      }
    }
  };

  const validate = () => {
    try {
      validationSchema.parse(values);
      setErrors({});
      return true;
    } catch (err) {
      if (err instanceof z.ZodError) {
        const formattedErrors = err.errors.reduce((acc, error) => {
          const field = error.path[0] as keyof T;
          acc[field] = error.message;
          return acc;
        }, {} as Partial<Record<keyof T, string>>);
        setErrors(formattedErrors);
      }
      return false;
    }
  };

  const handleSubmit = (onSubmit: (values: T) => Promise<void>) => {
    return async (e: React.FormEvent) => {
      e.preventDefault();

      if (!validate()) return;

      setIsSubmitting(true);
      try {
        await onSubmit(values);
      } finally {
        setIsSubmitting(false);
      }
    };
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  };

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    reset,
    setValues,
  };
}

// Usage
const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(2),
});

export function RegistrationForm() {
  const form = useForm(
    { email: '', password: '', name: '' },
    userSchema
  );

  const onSubmit = async (data) => {
    await authApi.register(data);
    router.push('/login');
  };

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <input
        value={form.values.email}
        onChange={form.handleChange('email')}
        onBlur={form.handleBlur('email')}
      />
      {form.touched.email && form.errors.email && (
        <span className="text-red-600">{form.errors.email}</span>
      )}
      {/* Other fields */}
    </form>
  );
}
```

## Pattern 3: Data Fetching with React Query

### Basic Data Fetching

```typescript
// api/queries/useProducts.ts
export function useProducts(filters?: ProductFilters) {
  return useQuery({
    queryKey: ['products', filters],
    queryFn: () => productApi.getProducts(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// Usage
export function ProductList() {
  const [filters, setFilters] = useState<ProductFilters>({});
  const { data, isLoading, error } = useProducts(filters);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return <ProductGrid products={data} />;
}
```

### Mutation with Optimistic Updates

```typescript
// api/queries/useCreateProduct.ts
export function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: productApi.createProduct,

    // Optimistic update
    onMutate: async (newProduct) => {
      // Cancel outgoing queries
      await queryClient.cancelQueries({ queryKey: ['products'] });

      // Snapshot previous value
      const previousProducts = queryClient.getQueryData(['products']);

      // Optimistically update
      queryClient.setQueryData(['products'], (old: Product[]) => [
        ...old,
        { ...newProduct, id: 'temp-id' },
      ]);

      return { previousProducts };
    },

    // On error, rollback
    onError: (err, newProduct, context) => {
      queryClient.setQueryData(['products'], context.previousProducts);
    },

    // Always refetch after error or success
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] });
    },
  });
}
```

### Infinite Scroll / Pagination

```typescript
// api/queries/useInfiniteProducts.ts
export function useInfiniteProducts() {
  return useInfiniteQuery({
    queryKey: ['products', 'infinite'],
    queryFn: ({ pageParam = 1 }) => productApi.getProducts({ page: pageParam }),
    getNextPageParam: (lastPage, pages) => {
      return lastPage.hasMore ? pages.length + 1 : undefined;
    },
    initialPageParam: 1,
  });
}

// Usage with intersection observer
export function InfiniteProductList() {
  const {
    data,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteProducts();

  const observerTarget = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasNextPage) {
          fetchNextPage();
        }
      },
      { threshold: 1 }
    );

    if (observerTarget.current) {
      observer.observe(observerTarget.current);
    }

    return () => observer.disconnect();
  }, [fetchNextPage, hasNextPage]);

  return (
    <div>
      {data?.pages.map((page) =>
        page.products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))
      )}
      <div ref={observerTarget} />
      {isFetchingNextPage && <LoadingSpinner />}
    </div>
  );
}
```

## Pattern 4: File Upload

### File Upload with Progress

```typescript
// hooks/useFileUpload.ts
export function useFileUpload() {
  const [progress, setProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const upload = async (file: File) => {
    setIsUploading(true);
    setError(null);
    setProgress(0);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / (progressEvent.total ?? 1)
          );
          setProgress(percentCompleted);
        },
      });

      return response.data;
    } catch (err) {
      setError('Upload failed');
      throw err;
    } finally {
      setIsUploading(false);
    }
  };

  return { upload, progress, isUploading, error };
}

// Usage
export function FileUploader() {
  const { upload, progress, isUploading } = useFileUpload();
  const [preview, setPreview] = useState<string | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Preview
    setPreview(URL.createObjectURL(file));

    // Upload
    try {
      const result = await upload(file);
      console.log('Uploaded:', result.url);
    } catch (error) {
      console.error('Upload failed');
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      {preview && <img src={preview} alt="Preview" />}
      {isUploading && (
        <div className="w-full bg-gray-200 rounded">
          <div
            className="bg-blue-600 h-2 rounded"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
}
```

## Pattern 5: Search & Filtering

### Debounced Search

```typescript
// hooks/useDebounce.ts
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}

// Usage
export function ProductSearch() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearch = useDebounce(searchTerm, 500);

  const { data, isLoading } = useQuery({
    queryKey: ['products', 'search', debouncedSearch],
    queryFn: () => productApi.search(debouncedSearch),
    enabled: debouncedSearch.length > 2,
  });

  return (
    <div>
      <input
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search products..."
      />
      {isLoading && <span>Searching...</span>}
      {data && <ProductList products={data} />}
    </div>
  );
}
```

### Multi-Filter State Management

```typescript
// stores/filterStore.ts
interface FilterStore {
  filters: ProductFilters;
  setFilter: (key: keyof ProductFilters, value: any) => void;
  clearFilters: () => void;
  appliedFilters: () => ProductFilters;
}

export const useFilterStore = create<FilterStore>((set, get) => ({
  filters: {
    category: null,
    priceRange: [0, 1000],
    inStock: true,
    sortBy: 'name',
  },

  setFilter: (key, value) => {
    set((state) => ({
      filters: { ...state.filters, [key]: value },
    }));
  },

  clearFilters: () => {
    set({
      filters: {
        category: null,
        priceRange: [0, 1000],
        inStock: true,
        sortBy: 'name',
      },
    });
  },

  appliedFilters: () => {
    const { filters } = get();
    // Remove null/default values
    return Object.entries(filters).reduce((acc, [key, value]) => {
      if (value !== null && value !== undefined) {
        acc[key] = value;
      }
      return acc;
    }, {} as ProductFilters);
  },
}));

// Usage
export function ProductFilters() {
  const { filters, setFilter, clearFilters } = useFilterStore();

  return (
    <div className="space-y-4">
      <select
        value={filters.category || ''}
        onChange={(e) => setFilter('category', e.target.value || null)}
      >
        <option value="">All Categories</option>
        <option value="electronics">Electronics</option>
        <option value="clothing">Clothing</option>
      </select>

      <input
        type="checkbox"
        checked={filters.inStock}
        onChange={(e) => setFilter('inStock', e.target.checked)}
      />

      <button onClick={clearFilters}>Clear Filters</button>
    </div>
  );
}
```

## Pattern 6: Shopping Cart

### Cart State Management

```typescript
// stores/cartStore.ts
interface CartItem {
  productId: string;
  quantity: number;
  price: number;
}

interface CartStore {
  items: CartItem[];
  addItem: (product: Product, quantity: number) => void;
  removeItem: (productId: string) => void;
  updateQuantity: (productId: string, quantity: number) => void;
  clearCart: () => void;
  total: () => number;
  itemCount: () => number;
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (product, quantity) => {
        const { items } = get();
        const existingItem = items.find((item) => item.productId === product.id);

        if (existingItem) {
          set({
            items: items.map((item) =>
              item.productId === product.id
                ? { ...item, quantity: item.quantity + quantity }
                : item
            ),
          });
        } else {
          set({
            items: [
              ...items,
              { productId: product.id, quantity, price: product.price },
            ],
          });
        }
      },

      removeItem: (productId) => {
        set((state) => ({
          items: state.items.filter((item) => item.productId !== productId),
        }));
      },

      updateQuantity: (productId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(productId);
          return;
        }

        set((state) => ({
          items: state.items.map((item) =>
            item.productId === productId ? { ...item, quantity } : item
          ),
        }));
      },

      clearCart: () => set({ items: [] }),

      total: () => {
        return get().items.reduce(
          (sum, item) => sum + item.price * item.quantity,
          0
        );
      },

      itemCount: () => {
        return get().items.reduce((sum, item) => sum + item.quantity, 0);
      },
    }),
    {
      name: 'cart-storage',
    }
  )
);

// Usage
export function AddToCartButton({ product }: { product: Product }) {
  const addItem = useCartStore((state) => state.addItem);
  const [quantity, setQuantity] = useState(1);

  const handleAdd = () => {
    addItem(product, quantity);
    toast.success('Added to cart!');
  };

  return (
    <div className="flex gap-2">
      <input
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(parseInt(e.target.value))}
        min="1"
        className="w-20 px-2 py-1 border rounded"
      />
      <button onClick={handleAdd} className="px-4 py-2 bg-blue-500 text-white rounded">
        Add to Cart
      </button>
    </div>
  );
}
```

## Pattern 7: Real-time Updates (WebSocket)

```typescript
// hooks/useWebSocket.ts
export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<any>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);

    ws.onopen = () => setIsConnected(true);
    ws.onclose = () => setIsConnected(false);
    ws.onmessage = (event) => {
      setLastMessage(JSON.parse(event.data));
    };

    wsRef.current = ws;

    return () => ws.close();
  }, [url]);

  const sendMessage = (message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  return { isConnected, lastMessage, sendMessage };
}

// Usage for real-time notifications
export function NotificationBell() {
  const { lastMessage } = useWebSocket('wss://api.example.com/notifications');
  const [notifications, setNotifications] = useState<Notification[]>([]);

  useEffect(() => {
    if (lastMessage?.type === 'notification') {
      setNotifications((prev) => [lastMessage.data, ...prev]);
      toast.info(lastMessage.data.message);
    }
  }, [lastMessage]);

  return (
    <div className="relative">
      <BellIcon />
      {notifications.length > 0 && (
        <span className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center">
          {notifications.length}
        </span>
      )}
    </div>
  );
}
```

These patterns cover most common business logic scenarios in React applications!
