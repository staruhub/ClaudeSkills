# WCAG 2.1 Accessibility Guide

## Overview

This guide covers WCAG 2.1 Level AA compliance for frontend applications. Accessibility ensures your app is usable by everyone, including people with disabilities.

## Four Principles (POUR)

1. **Perceivable** - Information must be presentable to users in ways they can perceive
2. **Operable** - UI components must be operable by all users
3. **Understandable** - Information and operation must be understandable
4. **Robust** - Content must be robust enough to work with various technologies

## 1. Semantic HTML

### Use Proper HTML Elements

```typescript
// ❌ BAD: Divs for everything
<div onClick={handleSubmit}>Submit</div>
<div onClick={handleClick}>Click me</div>
<div>Navigation</div>

// ✅ GOOD: Semantic elements
<button type="submit" onClick={handleSubmit}>Submit</button>
<button onClick={handleClick}>Click me</button>
<nav>Navigation</nav>
```

### Proper Document Structure

```typescript
// ❌ BAD: No structure
<div>
  <div>Welcome</div>
  <div>Section 1</div>
  <div>Content</div>
</div>

// ✅ GOOD: Semantic structure
<main>
  <h1>Welcome</h1>
  <section>
    <h2>Section 1</h2>
    <p>Content</p>
  </section>
</main>
```

### Heading Hierarchy

```typescript
// ❌ BAD: Skipping heading levels
<h1>Page Title</h1>
<h3>Subsection</h3> {/* Skipped h2 */}
<h2>Section</h2> {/* Out of order */}

// ✅ GOOD: Logical hierarchy
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
```

## 2. Keyboard Navigation

### Tab Order

```typescript
// ❌ BAD: Positive tabIndex (disrupts natural flow)
<button tabIndex={5}>First</button>
<button tabIndex={1}>Second</button>
<button tabIndex={3}>Third</button>

// ✅ GOOD: Natural tab order (or 0 for custom elements)
<button>First</button>
<button>Second</button>
<button>Third</button>

// ✅ GOOD: Custom interactive element
<div role="button" tabIndex={0} onClick={handleClick}>
  Custom Button
</div>
```

### Keyboard Event Handlers

```typescript
// ❌ BAD: Only mouse events
<div onClick={handleClick}>Click me</div>

// ✅ GOOD: Both mouse and keyboard
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  Click me
</div>

// ✅ BETTER: Use button element
<button onClick={handleClick}>Click me</button>
```

### Focus Management

```typescript
// ❌ BAD: No visible focus
button:focus {
  outline: none; /* Don't do this! */
}

// ✅ GOOD: Clear focus indicator
button:focus-visible {
  outline: 2px solid #4A90E2;
  outline-offset: 2px;
}

// Modal focus trap
function Modal({ isOpen, onClose, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements?.[0] as HTMLElement;
    const lastElement = focusableElements?.[focusableElements.length - 1] as HTMLElement;

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    document.addEventListener('keydown', handleTabKey);
    firstElement?.focus();

    return () => {
      document.removeEventListener('keydown', handleTabKey);
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 bg-black bg-opacity-50"
    >
      <div className="bg-white p-6 rounded">
        {children}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}
```

### Skip Links

```typescript
// ✅ GOOD: Skip to main content
function Layout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <nav>Navigation</nav>
      <main id="main-content">{children}</main>
    </>
  );
}

// CSS
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: #000;
  color: white;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

## 3. ARIA Attributes

### ARIA Labels

```typescript
// ❌ BAD: No label
<button>
  <SearchIcon />
</button>

// ✅ GOOD: aria-label for icon buttons
<button aria-label="Search">
  <SearchIcon />
</button>

// ❌ BAD: Placeholder as label
<input type="text" placeholder="Email" />

// ✅ GOOD: Proper label
<label htmlFor="email">Email</label>
<input id="email" type="text" />

// ✅ GOOD: aria-label when visual label isn't possible
<input type="text" aria-label="Email" />
```

### ARIA Described By

```typescript
// ✅ GOOD: Associate error message with input
function EmailInput() {
  const [error, setError] = useState('');

  return (
    <div>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        aria-invalid={!!error}
        aria-describedby={error ? 'email-error' : undefined}
      />
      {error && (
        <p id="email-error" role="alert" className="text-red-500">
          {error}
        </p>
      )}
    </div>
  );
}
```

### ARIA Live Regions

```typescript
// ✅ GOOD: Announce dynamic updates
function Notifications() {
  const [message, setMessage] = useState('');

  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className="sr-only" // Screen reader only
    >
      {message}
    </div>
  );
}

// For urgent updates
<div role="alert" aria-live="assertive">
  Error: Form submission failed
</div>
```

### ARIA Roles

```typescript
// ✅ GOOD: Proper roles for custom components
function CustomSelect() {
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState(0);

  return (
    <div>
      <button
        role="combobox"
        aria-expanded={open}
        aria-controls="listbox"
        aria-activedescendant={`option-${selected}`}
        onClick={() => setOpen(!open)}
      >
        Select option
      </button>
      {open && (
        <ul id="listbox" role="listbox">
          <li id="option-0" role="option" aria-selected={selected === 0}>
            Option 1
          </li>
          <li id="option-1" role="option" aria-selected={selected === 1}>
            Option 2
          </li>
        </ul>
      )}
    </div>
  );
}
```

## 4. Color and Contrast

### Minimum Contrast Ratios (WCAG AA)

- **Normal text**: 4.5:1
- **Large text** (18pt+): 3:1
- **UI components**: 3:1

```typescript
// ❌ BAD: Low contrast
<button className="bg-gray-200 text-gray-300">
  Submit
</button> // Contrast ratio: ~1.5:1

// ✅ GOOD: Sufficient contrast
<button className="bg-blue-600 text-white">
  Submit
</button> // Contrast ratio: 8.59:1

// ✅ GOOD: Error message with sufficient contrast
<p className="text-red-600">
  Error message
</p> // Against white: 5.14:1
```

### Don't Rely on Color Alone

```typescript
// ❌ BAD: Color only to indicate state
<button className={isActive ? 'bg-green-500' : 'bg-gray-500'}>
  Status
</button>

// ✅ GOOD: Color + text/icon
<button className={isActive ? 'bg-green-500' : 'bg-gray-500'}>
  {isActive ? '✓ Active' : 'Inactive'}
</button>

// ✅ GOOD: Required field indicator
<label htmlFor="name">
  Name <span aria-label="required">*</span>
</label>
<input id="name" required />
```

## 5. Forms and Inputs

### Labels

```typescript
// ❌ BAD: No label
<input type="text" placeholder="Email" />

// ✅ GOOD: Visible label
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// ✅ GOOD: Visually hidden label (if design requires)
<label htmlFor="search" className="sr-only">Search</label>
<input id="search" type="search" placeholder="Search..." />
```

### Error Handling

```typescript
// ✅ GOOD: Accessible error messages
function Form() {
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <form noValidate>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <p id="email-error" role="alert" className="text-red-600 text-sm">
            {errors.email}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
        {errors.password && (
          <p id="password-error" role="alert" className="text-red-600 text-sm">
            {errors.password}
          </p>
        )}
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}
```

### Required Fields

```typescript
// ✅ GOOD: Indicate required fields
<label htmlFor="name">
  Name <span aria-label="required" className="text-red-600">*</span>
</label>
<input id="name" type="text" required aria-required="true" />
```

### Autocomplete Attributes

```typescript
// ✅ GOOD: Help with autofill
<input
  type="email"
  name="email"
  autoComplete="email"
  aria-label="Email address"
/>

<input
  type="password"
  name="password"
  autoComplete="current-password"
  aria-label="Password"
/>

<input
  type="text"
  name="name"
  autoComplete="name"
  aria-label="Full name"
/>
```

## 6. Images and Media

### Alt Text

```typescript
// ❌ BAD: No alt text
<img src="/photo.jpg" />

// ❌ BAD: Redundant alt text
<img src="/photo.jpg" alt="Image of a photo" />

// ✅ GOOD: Descriptive alt text
<img src="/photo.jpg" alt="Team celebrating product launch" />

// ✅ GOOD: Empty alt for decorative images
<img src="/decorative-border.png" alt="" role="presentation" />

// ✅ GOOD: Complex image with description
<figure>
  <img
    src="/chart.png"
    alt="Sales growth chart"
    aria-describedby="chart-description"
  />
  <figcaption id="chart-description">
    Chart showing 25% sales growth from Q1 to Q4 2024
  </figcaption>
</figure>
```

### Video and Audio

```typescript
// ✅ GOOD: Captions and transcripts
<video controls>
  <source src="/video.mp4" type="video/mp4" />
  <track
    kind="captions"
    src="/captions.vtt"
    srcLang="en"
    label="English"
    default
  />
  Your browser doesn't support video.
</video>

// ✅ GOOD: Provide transcript link
<audio controls>
  <source src="/podcast.mp3" type="audio/mpeg" />
</audio>
<a href="/transcript.txt">Download transcript</a>
```

## 7. Interactive Elements

### Buttons vs Links

```typescript
// ❌ BAD: Link that acts like button
<a href="#" onClick={handleClick}>Submit</a>

// ✅ GOOD: Button for actions
<button onClick={handleClick}>Submit</button>

// ✅ GOOD: Link for navigation
<a href="/about">About Us</a>
```

### Disabled States

```typescript
// ❌ BAD: Disabled without explanation
<button disabled>Submit</button>

// ✅ GOOD: Explain why disabled
<button
  disabled={!isFormValid}
  aria-describedby="submit-help"
>
  Submit
</button>
{!isFormValid && (
  <p id="submit-help" className="text-sm text-gray-600">
    Please fill in all required fields
  </p>
)}
```

## 8. Responsive and Mobile Accessibility

### Touch Target Size

```typescript
// ❌ BAD: Too small touch targets
<button className="w-6 h-6 p-1">×</button>

// ✅ GOOD: Minimum 44x44px touch targets
<button className="min-w-11 min-h-11 p-2" aria-label="Close">
  ×
</button>
```

### Zoom and Reflow

```typescript
// ✅ GOOD: Support 200% zoom without horizontal scrolling
<meta name="viewport" content="width=device-width, initial-scale=1" />

// ✅ GOOD: Use relative units
<div className="text-base p-4 max-w-prose">
  Content
</div>
```

## Accessibility Testing Checklist

### Automated Testing

- [ ] Run Lighthouse accessibility audit
- [ ] Use axe DevTools browser extension
- [ ] Run automated tests (jest-axe, @testing-library)

### Manual Testing

- [ ] Navigate entire app using only keyboard (Tab, Enter, Arrow keys)
- [ ] Test with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Verify color contrast ratios
- [ ] Test with browser zoom at 200%
- [ ] Disable CSS and check content order
- [ ] Test with browser dark mode

### Code Review Checklist

- [ ] All images have alt text
- [ ] All form inputs have labels
- [ ] Focus indicators are visible
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Keyboard navigation works for all interactive elements
- [ ] ARIA attributes used correctly
- [ ] Semantic HTML used throughout
- [ ] No keyboard traps
- [ ] Skip links present
- [ ] Error messages announced to screen readers
- [ ] Touch targets are at least 44x44px
- [ ] Heading hierarchy is logical (h1, h2, h3)

## Common ARIA Patterns

### Dialog/Modal

```typescript
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-description"
>
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-description">Are you sure you want to delete this item?</p>
  <button onClick={handleConfirm}>Confirm</button>
  <button onClick={handleCancel}>Cancel</button>
</div>
```

### Accordion

```typescript
<div>
  <h3>
    <button
      aria-expanded={isOpen}
      aria-controls="panel-1"
      onClick={() => setIsOpen(!isOpen)}
    >
      Section 1
    </button>
  </h3>
  {isOpen && (
    <div id="panel-1" role="region" aria-labelledby="section-1">
      Content
    </div>
  )}
</div>
```

### Tabs

```typescript
<div>
  <div role="tablist" aria-label="Content tabs">
    <button
      role="tab"
      aria-selected={activeTab === 0}
      aria-controls="panel-0"
      id="tab-0"
    >
      Tab 1
    </button>
    <button
      role="tab"
      aria-selected={activeTab === 1}
      aria-controls="panel-1"
      id="tab-1"
    >
      Tab 2
    </button>
  </div>
  <div
    role="tabpanel"
    id="panel-0"
    aria-labelledby="tab-0"
    hidden={activeTab !== 0}
  >
    Panel 1 content
  </div>
  <div
    role="tabpanel"
    id="panel-1"
    aria-labelledby="tab-1"
    hidden={activeTab !== 1}
  >
    Panel 2 content
  </div>
</div>
```

Use this guide to ensure your frontend applications are accessible to all users!
