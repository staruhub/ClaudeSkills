# Frontend Security Checklist

## Quick Security Review Checklist

When reviewing frontend code, check these critical security points:

### XSS (Cross-Site Scripting)
- [ ] No `dangerouslySetInnerHTML` with unsanitized user input
- [ ] User-generated content is properly escaped/sanitized
- [ ] No `eval()` or `Function()` with user input
- [ ] URLs validated before rendering in href or src
- [ ] Content Security Policy (CSP) configured

### Authentication & Session Management
- [ ] No tokens in localStorage or sessionStorage
- [ ] HttpOnly cookies used for session management
- [ ] Secure and SameSite flags set on cookies
- [ ] Protected routes check authentication
- [ ] Automatic logout on token expiration
- [ ] Password fields use `type="password"`
- [ ] No autocomplete on sensitive fields

### Sensitive Data
- [ ] No API keys or secrets in frontend code
- [ ] No sensitive data in console.log
- [ ] Environment variables used properly (NEXT_PUBLIC_ prefix)
- [ ] Sensitive data masked in UI (credit cards, etc.)
- [ ] Generic error messages (no stack traces in production)

### CSRF (Cross-Site Request Forgery)
- [ ] CSRF tokens included in state-changing requests
- [ ] SameSite cookie attribute set
- [ ] Origin/Referer headers checked for sensitive operations

### Input Validation
- [ ] All form inputs validated before submission
- [ ] File uploads restricted by type and size
- [ ] Schema validation (Zod, Yup) for form data
- [ ] Special characters handled safely

### Secure Communication
- [ ] HTTPS enforced in production
- [ ] No mixed content (HTTP resources on HTTPS page)
- [ ] Security headers configured (X-Frame-Options, etc.)
- [ ] API requests use relative URLs or validated origins

### Dependencies
- [ ] No known vulnerabilities (`npm audit`)
- [ ] Dependencies regularly updated
- [ ] Only necessary packages installed
- [ ] Lockfile (package-lock.json) committed

## Detailed Security Issues

### 1. XSS Prevention

#### Critical Issues

```typescript
// 🚨 CRITICAL: XSS vulnerability
function Comment({ text }: { text: string }) {
  return <div dangerouslySetInnerHTML={{ __html: text }} />;
}
// User can inject: <img src=x onerror="alert(document.cookie)">

// ✅ FIX: Render as text or sanitize
import DOMPurify from 'dompurify';

function Comment({ text }: { text: string }) {
  return <div>{text}</div>; // Safe
  // OR if HTML is needed:
  // return <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(text) }} />;
}
```

```typescript
// 🚨 CRITICAL: Unsafe URL rendering
function UserLink({ url }: { url: string }) {
  return <a href={url}>Link</a>;
}
// User can inject: javascript:alert('XSS')

// ✅ FIX: Validate URL protocol
function UserLink({ url }: { url: string }) {
  const isValidUrl = (url: string) => {
    try {
      const parsed = new URL(url);
      return ['http:', 'https:'].includes(parsed.protocol);
    } catch {
      return false;
    }
  };

  if (!isValidUrl(url)) return <span>Invalid URL</span>;

  return <a href={url} rel="noopener noreferrer">{url}</a>;
}
```

### 2. Authentication & Token Storage

#### Critical Issues

```typescript
// 🚨 CRITICAL: Token in localStorage (XSS vulnerability)
const token = await login(credentials);
localStorage.setItem('token', token);
// If attacker injects XSS, they can steal: localStorage.getItem('token')

// ✅ FIX: Use HttpOnly cookies (server-side)
// Server sets:
res.cookie('auth-token', token, {
  httpOnly: true,  // Not accessible to JavaScript
  secure: true,    // HTTPS only
  sameSite: 'strict',
  maxAge: 900000   // 15 minutes
});

// Frontend: Cookies sent automatically
fetch('/api/user', {
  credentials: 'include' // Include cookies
});
```

```typescript
// 🚨 CRITICAL: Hardcoded API key
const API_KEY = 'sk_live_abc123xyz456def';

// ✅ FIX: Environment variable
const API_KEY = process.env.NEXT_PUBLIC_API_KEY;

// ⚠️ WARNING: Only use NEXT_PUBLIC_ for truly public keys
// Never expose:
// - Private API secrets
// - Database credentials
// - OAuth client secrets
```

### 3. CSRF Prevention

#### High Priority Issues

```typescript
// ⚠️ HIGH: No CSRF protection
async function deleteAccount() {
  await fetch('/api/account/delete', {
    method: 'DELETE'
  });
}
// Attacker can trigger this from their site if user is logged in

// ✅ FIX: CSRF token
async function deleteAccount() {
  const csrfToken = getCsrfToken(); // From meta tag or cookie

  await fetch('/api/account/delete', {
    method: 'DELETE',
    headers: {
      'X-CSRF-Token': csrfToken
    }
  });
}
```

### 4. Input Validation

#### High Priority Issues

```typescript
// ⚠️ HIGH: No validation
function SearchForm() {
  const [query, setQuery] = useState('');

  const handleSubmit = () => {
    router.push(`/search?q=${query}`); // Injection risk
  };
}

// ✅ FIX: Validate input
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

    router.push(`/search?q=${encodeURIComponent(result.data)}`);
  };
}
```

```typescript
// ⚠️ HIGH: No file validation
function FileUpload() {
  const handleUpload = (file: File) => {
    uploadFile(file); // Can upload .exe, malicious files
  };
}

// ✅ FIX: Validate file type and size
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/gif'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function FileUpload() {
  const [error, setError] = useState('');

  const handleUpload = (file: File) => {
    if (!ALLOWED_TYPES.includes(file.type)) {
      setError('Only JPEG, PNG, GIF allowed');
      return;
    }

    if (file.size > MAX_SIZE) {
      setError('File must be less than 5MB');
      return;
    }

    uploadFile(file);
  };
}
```

### 5. Sensitive Data Exposure

#### High Priority Issues

```typescript
// ⚠️ HIGH: Sensitive data in logs
console.log('Login:', { email, password, creditCard });

// ✅ FIX: Only log non-sensitive data
console.log('Login attempt:', { email, timestamp: Date.now() });
```

```typescript
// ⚠️ HIGH: Detailed error messages
catch (error) {
  setError(`Database error: ${error.message}`);
  // Exposes: "Connection to internal-db-host:5432 failed"
}

// ✅ FIX: Generic messages
catch (error) {
  console.error('Internal error:', error); // Log for debugging
  setError('Something went wrong. Please try again.');
}
```

```typescript
// ⚠️ HIGH: Full credit card visible
function CreditCard({ number }: { number: string }) {
  return <div>{number}</div>; // Shows: 4532-1234-5678-9010
}

// ✅ FIX: Mask sensitive digits
function CreditCard({ number }: { number: string }) {
  const masked = `****-****-****-${number.slice(-4)}`;
  return <div>{masked}</div>; // Shows: ****-****-****-9010
}
```

### 6. Secure Communication

#### Medium Priority Issues

```typescript
// ⚡ MEDIUM: Missing security headers
// Add in next.config.js

const securityHeaders = [
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN' // Prevent clickjacking
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff' // Prevent MIME sniffing
  },
  {
    key: 'X-XSS-Protection',
    value: '1; mode=block'
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin'
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()'
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=31536000; includeSubDomains'
  }
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders
      }
    ];
  }
};
```

### 7. Content Security Policy

```typescript
// ✅ GOOD: Strict CSP
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

// Add to next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: cspHeader.replace(/\n/g, '')
          }
        ]
      }
    ];
  }
};
```

## Security Testing

### Automated Tools

1. **npm audit**: Check for vulnerable dependencies
   ```bash
   npm audit
   npm audit fix
   ```

2. **Browser DevTools**: Check security warnings
   - Console warnings
   - Network tab (HTTPS, mixed content)
   - Application tab (cookies, storage)

3. **Lighthouse**: Security audit
   - Run in Chrome DevTools
   - Check security score and recommendations

4. **OWASP ZAP**: Web application security scanner
   - Automated vulnerability scanning
   - Manual testing support

### Manual Testing

1. **XSS Testing**:
   - Try injecting: `<script>alert('XSS')</script>`
   - Try: `<img src=x onerror="alert('XSS')">`
   - Check all user input fields

2. **Authentication Testing**:
   - Check if tokens are in localStorage (bad)
   - Try accessing protected routes without auth
   - Check if session expires properly

3. **CSRF Testing**:
   - Try making requests from different origin
   - Check if CSRF tokens are validated

4. **Input Validation**:
   - Try special characters: `<>'";&|`
   - Try very long inputs
   - Try uploading different file types

## Severity Assessment

### 🚨 CRITICAL (Fix Immediately)

- XSS vulnerabilities (`dangerouslySetInnerHTML` with user input)
- Tokens in localStorage/sessionStorage
- Hardcoded API keys or secrets
- No authentication on sensitive routes
- Exposed sensitive data in logs or error messages

### ⚠️ HIGH (Fix Before Production)

- Missing CSRF protection on state-changing operations
- No input validation on forms
- No file upload restrictions
- Detailed error messages exposing internals
- Missing HTTPS enforcement

### ⚡ MEDIUM (Should Fix)

- Missing security headers
- Weak Content Security Policy
- No rate limiting on client side
- Autocomplete on sensitive fields
- Outdated dependencies with known vulnerabilities

### 💡 LOW (Nice to Have)

- Additional CSP restrictions
- Subresource Integrity (SRI) for CDN resources
- Additional security headers
- More restrictive CORS policies

## Quick Wins

1. **Enable HTTPS**: Always use HTTPS in production
2. **Add Security Headers**: Use helmet.js or configure manually
3. **Run npm audit**: Fix known vulnerabilities
4. **Use HttpOnly Cookies**: Never store tokens in localStorage
5. **Validate All Inputs**: Use Zod or similar library
6. **Sanitize Output**: Never use dangerouslySetInnerHTML without DOMPurify
7. **Enable CSP**: Start with report-only mode, then enforce

Use this checklist for every frontend security review!
