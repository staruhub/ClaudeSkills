# Frontend Security Best Practices

## XSS (Cross-Site Scripting) Prevention

### 1. Avoid dangerouslySetInnerHTML

```typescript
// ❌ CRITICAL: XSS vulnerability
function UserBio({ bio }: { bio: string }) {
  return <div dangerouslySetInnerHTML={{ __html: bio }} />;
}
// User can inject: <img src=x onerror="alert('XSS')">

// ✅ GOOD: Render as text
function UserBio({ bio }: { bio: string }) {
  return <div>{bio}</div>;
}

// ⚠️ USE WITH CAUTION: Sanitize if HTML is absolutely necessary
import DOMPurify from 'dompurify';

function UserBio({ bio }: { bio: string }) {
  const sanitizedBio = DOMPurify.sanitize(bio, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  });

  return <div dangerouslySetInnerHTML={{ __html: sanitizedBio }} />;
}
```

### 2. Sanitize URLs

```typescript
// ❌ BAD: User-controlled href
function UserLink({ url, label }: { url: string; label: string }) {
  return <a href={url}>{label}</a>;
}
// User can inject: javascript:alert('XSS')

// ✅ GOOD: Validate URL protocol
function UserLink({ url, label }: { url: string; label: string }) {
  const isValidUrl = (url: string) => {
    try {
      const parsed = new URL(url);
      return ['http:', 'https:'].includes(parsed.protocol);
    } catch {
      return false;
    }
  };

  if (!isValidUrl(url)) {
    return <span>{label}</span>;
  }

  return <a href={url} rel="noopener noreferrer" target="_blank">{label}</a>;
}
```

### 3. Content Security Policy (CSP)

```typescript
// next.config.js (Next.js example)
const cspHeader = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' blob: data: https:;
  font-src 'self';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
  upgrade-insecure-requests;
`;

module.exports = {
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: cspHeader.replace(/\n/g, ''),
          },
        ],
      },
    ];
  },
};
```

## CSRF (Cross-Site Request Forgery) Prevention

### 1. CSRF Tokens for State-Changing Operations

```typescript
// ❌ BAD: No CSRF protection
async function deleteAccount() {
  await fetch('/api/account/delete', {
    method: 'DELETE',
  });
}

// ✅ GOOD: Include CSRF token
async function deleteAccount() {
  const csrfToken = document.querySelector<HTMLMetaElement>(
    'meta[name="csrf-token"]'
  )?.content;

  await fetch('/api/account/delete', {
    method: 'DELETE',
    headers: {
      'X-CSRF-Token': csrfToken || '',
    },
  });
}
```

### 2. SameSite Cookies

```typescript
// Server-side: Set SameSite cookie attribute
res.cookie('session', sessionId, {
  httpOnly: true,
  secure: true, // HTTPS only
  sameSite: 'strict', // or 'lax'
  maxAge: 24 * 60 * 60 * 1000, // 24 hours
});
```

### 3. Double Submit Cookie Pattern

```typescript
// Client generates and sends CSRF token
function getCsrfToken(): string {
  const token = crypto.randomUUID();
  document.cookie = `csrf-token=${token}; SameSite=Strict; Secure`;
  return token;
}

async function submitForm(data: FormData) {
  const csrfToken = getCsrfToken();

  await fetch('/api/form', {
    method: 'POST',
    headers: {
      'X-CSRF-Token': csrfToken,
    },
    body: data,
  });
}
```

## Authentication & Authorization

### 1. Secure Token Storage

```typescript
// ❌ CRITICAL: Token in localStorage (vulnerable to XSS)
localStorage.setItem('token', accessToken);

// ❌ CRITICAL: Token in sessionStorage (also vulnerable)
sessionStorage.setItem('token', accessToken);

// ✅ GOOD: HttpOnly cookie (set by server, not accessible to JS)
// Server response:
res.cookie('auth-token', token, {
  httpOnly: true, // Not accessible via JavaScript
  secure: true, // HTTPS only
  sameSite: 'strict',
  maxAge: 15 * 60 * 1000, // 15 minutes
});

// Frontend: Cookies sent automatically with requests
async function fetchUserData() {
  const response = await fetch('/api/user', {
    credentials: 'include', // Send cookies
  });
  return response.json();
}
```

### 2. Protect Sensitive Routes

```typescript
// ❌ BAD: No authentication check
function AdminDashboard() {
  return <div>Admin Panel</div>;
}

// ✅ GOOD: Authentication check
function AdminDashboard() {
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/login');
    }
  }, [user, isLoading]);

  if (isLoading) return <LoadingSpinner />;
  if (!user) return null;

  return <div>Admin Panel</div>;
}

// ✅ BETTER: Higher-order component
function withAuth<P extends object>(
  Component: React.ComponentType<P>,
  requiredRole?: string
) {
  return function AuthenticatedComponent(props: P) {
    const { user, isLoading } = useAuth();

    useEffect(() => {
      if (!isLoading && !user) {
        router.push('/login');
      }

      if (!isLoading && requiredRole && user?.role !== requiredRole) {
        router.push('/unauthorized');
      }
    }, [user, isLoading]);

    if (isLoading) return <LoadingSpinner />;
    if (!user) return null;
    if (requiredRole && user.role !== requiredRole) return null;

    return <Component {...props} />;
  };
}

// Usage
const AdminDashboard = withAuth(AdminDashboardComponent, 'admin');
```

### 3. Secure Password Handling

```typescript
// ❌ BAD: No validation, plain text
function PasswordInput() {
  const [password, setPassword] = useState('');

  return <input type="text" value={password} onChange={e => setPassword(e.target.value)} />;
}

// ✅ GOOD: Validation, proper input type
import { z } from 'zod';

const passwordSchema = z.string()
  .min(12, 'Password must be at least 12 characters')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[a-z]/, 'Must contain lowercase letter')
  .regex(/[0-9]/, 'Must contain number')
  .regex(/[^A-Za-z0-9]/, 'Must contain special character');

function PasswordInput() {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setPassword(value);

    const result = passwordSchema.safeParse(value);
    if (!result.success) {
      setError(result.error.errors[0].message);
    } else {
      setError('');
    }
  };

  return (
    <div>
      <input
        type="password"
        value={password}
        onChange={handleChange}
        autoComplete="new-password"
        aria-describedby="password-error"
      />
      {error && <p id="password-error" role="alert">{error}</p>}
    </div>
  );
}
```

## Sensitive Data Exposure Prevention

### 1. Never Log Sensitive Data

```typescript
// ❌ CRITICAL: Sensitive data in console
console.log('Login attempt:', { email, password, creditCard });

// ✅ GOOD: Only log non-sensitive data
console.log('Login attempt:', { email, timestamp: new Date() });
```

### 2. Mask Sensitive Information

```typescript
// ❌ BAD: Show full credit card number
function CreditCard({ number }: { number: string }) {
  return <div>{number}</div>; // Shows: 4532-1234-5678-9010
}

// ✅ GOOD: Mask sensitive digits
function CreditCard({ number }: { number: string }) {
  const masked = `****-****-****-${number.slice(-4)}`;
  return <div>{masked}</div>; // Shows: ****-****-****-9010
}
```

### 3. Secure Environment Variables

```typescript
// ❌ BAD: Hardcoded secrets
const API_KEY = 'sk_live_abc123xyz';
const DATABASE_URL = 'postgresql://user:password@host/db';

// ✅ GOOD: Environment variables
const API_KEY = process.env.NEXT_PUBLIC_API_KEY;

// ⚠️ IMPORTANT: Only use NEXT_PUBLIC_ for truly public keys
// Never expose:
// - API secrets
// - Database credentials
// - Private keys
// - Internal URLs
```

### 4. Sanitize Error Messages

```typescript
// ❌ BAD: Expose internal details
catch (error) {
  setError(`Database error: ${error.message}`);
  // Exposes: "Connection to postgres://user:pass@internal-db failed"
}

// ✅ GOOD: Generic user-facing message
catch (error) {
  console.error('Internal error:', error); // Log for debugging
  setError('Something went wrong. Please try again.');
}
```

## Input Validation

### 1. Validate All User Input

```typescript
// ❌ BAD: No validation
function SearchForm() {
  const [query, setQuery] = useState('');

  const handleSubmit = () => {
    fetch(`/api/search?q=${query}`); // SQL injection risk
  };

  return <form onSubmit={handleSubmit}>...</form>;
}

// ✅ GOOD: Validate and sanitize
import { z } from 'zod';

const searchSchema = z.string()
  .min(1)
  .max(100)
  .regex(/^[a-zA-Z0-9\s\-]+$/, 'Invalid characters');

function SearchForm() {
  const [query, setQuery] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const result = searchSchema.safeParse(query);
    if (!result.success) {
      setError(result.error.errors[0].message);
      return;
    }

    fetch('/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ q: result.data }),
    });
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### 2. File Upload Security

```typescript
// ❌ BAD: No validation
function FileUpload() {
  const handleUpload = (file: File) => {
    uploadFile(file); // Can upload .exe, .sh, etc.
  };

  return <input type="file" onChange={e => handleUpload(e.target.files[0])} />;
}

// ✅ GOOD: Validate file type and size
const ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/gif'];
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB

function FileUpload() {
  const [error, setError] = useState('');

  const handleUpload = (file: File) => {
    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
      setError('Invalid file type. Only JPEG, PNG, GIF allowed.');
      return;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError('File too large. Maximum 5MB.');
      return;
    }

    uploadFile(file);
  };

  return (
    <div>
      <input
        type="file"
        accept="image/jpeg,image/png,image/gif"
        onChange={e => e.target.files?.[0] && handleUpload(e.target.files[0])}
      />
      {error && <p role="alert">{error}</p>}
    </div>
  );
}
```

## Secure Communication

### 1. HTTPS Only

```typescript
// ❌ BAD: Allow HTTP
if (window.location.protocol === 'http:') {
  // Continue anyway
}

// ✅ GOOD: Force HTTPS
if (window.location.protocol === 'http:') {
  window.location.href = window.location.href.replace('http:', 'https:');
}

// ✅ BETTER: Configure in next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Strict-Transport-Security',
            value: 'max-age=31536000; includeSubDomains',
          },
        ],
      },
    ];
  },
};
```

### 2. Security Headers

```typescript
// Add these headers in next.config.js or server middleware
const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on',
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=31536000; includeSubDomains',
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block',
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin',
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()',
  },
];
```

## Frontend Security Checklist

When reviewing frontend code, always check:

**XSS Prevention**:
- [ ] No `dangerouslySetInnerHTML` with user input
- [ ] User-generated content is sanitized
- [ ] URLs are validated (no javascript: protocol)
- [ ] Content Security Policy (CSP) is configured

**Authentication & Authorization**:
- [ ] No tokens in localStorage/sessionStorage
- [ ] HttpOnly cookies for session management
- [ ] Protected routes check authentication
- [ ] Role-based access control implemented
- [ ] Secure password input (type="password")

**Sensitive Data**:
- [ ] No sensitive data in console.log
- [ ] No hardcoded secrets or API keys
- [ ] Environment variables used properly
- [ ] Sensitive data masked in UI
- [ ] Generic error messages (no internal details)

**Input Validation**:
- [ ] All user input validated
- [ ] File uploads restricted (type, size)
- [ ] Form data validated with schema (Zod)
- [ ] Special characters escaped properly

**Secure Communication**:
- [ ] HTTPS enforced in production
- [ ] Security headers configured
- [ ] CORS configured properly
- [ ] API calls use credentials: 'include' when needed

**Dependencies**:
- [ ] No known vulnerabilities (npm audit)
- [ ] Dependencies up to date
- [ ] Only necessary packages installed

Use this guide to ensure frontend security in all code reviews!
