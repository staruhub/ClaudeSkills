# Common Layout Patterns

## Overview

This document catalogs common UI layout patterns and their Tailwind CSS implementations to help quickly translate design screenshots into code.

## 1. Single Column Layout

**Description**: Content centered in a single column with max-width constraint.

**Common Use Cases**:
- Blog posts
- Article pages
- Simple forms
- Landing pages

**Tailwind Implementation**:
```tsx
<div className="min-h-screen bg-gray-50">
  <div className="max-w-2xl mx-auto px-4 py-8">
    {/* Content */}
  </div>
</div>
```

**Variants**:
- Narrow: `max-w-xl` (576px)
- Standard: `max-w-2xl` (672px)
- Wide: `max-w-4xl` (896px)

## 2. Sidebar Layout (Fixed Sidebar)

**Description**: Fixed-width sidebar with flexible content area.

**Common Use Cases**:
- Admin dashboards
- Documentation sites
- Application settings
- Email clients

**Tailwind Implementation**:
```tsx
<div className="flex min-h-screen bg-gray-100">
  {/* Sidebar */}
  <aside className="w-64 bg-white border-r border-gray-200 fixed h-full overflow-y-auto">
    {/* Navigation */}
  </aside>

  {/* Main Content */}
  <main className="flex-1 ml-64 p-8">
    {/* Content */}
  </main>
</div>
```

**Responsive Variant**:
```tsx
<div className="flex min-h-screen bg-gray-100">
  {/* Mobile: Hidden sidebar with toggle */}
  <aside className="w-64 bg-white border-r border-gray-200 fixed h-full overflow-y-auto
                    transform -translate-x-full md:translate-x-0 transition-transform">
    {/* Navigation */}
  </aside>

  <main className="flex-1 md:ml-64 p-4 md:p-8">
    {/* Content */}
  </main>
</div>
```

**Common Sidebar Widths**:
- Narrow: `w-48` (192px)
- Standard: `w-64` (256px)
- Wide: `w-80` (320px)

## 3. Header + Content Layout

**Description**: Fixed header with scrollable content below.

**Common Use Cases**:
- Most web applications
- Marketing sites
- Blogs

**Tailwind Implementation**:
```tsx
<div className="min-h-screen bg-gray-50">
  {/* Header */}
  <header className="bg-white border-b border-gray-200 fixed top-0 left-0 right-0 z-10">
    <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      {/* Header content */}
    </div>
  </header>

  {/* Main Content */}
  <main className="pt-16">
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Content */}
    </div>
  </main>
</div>
```

**Common Header Heights**:
- Compact: `h-12` (48px)
- Standard: `h-16` (64px)
- Tall: `h-20` (80px)

## 4. Grid Layout (Cards/Products)

**Description**: Responsive grid of equal-sized items.

**Common Use Cases**:
- Product listings
- Image galleries
- Card collections
- Feature showcases

**Tailwind Implementation**:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map(item => (
    <div key={item.id} className="bg-white rounded-lg shadow-md p-6">
      {/* Card content */}
    </div>
  ))}
</div>
```

**Common Grid Configurations**:
- 2 columns: `grid-cols-1 md:grid-cols-2`
- 3 columns: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- 4 columns: `grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`
- Auto-fit: `grid-cols-[repeat(auto-fit,minmax(250px,1fr))]`

**Common Gap Sizes**:
- Tight: `gap-2` or `gap-4`
- Standard: `gap-6`
- Spacious: `gap-8` or `gap-10`

## 5. Split Screen Layout

**Description**: Two equal or weighted sections side by side.

**Common Use Cases**:
- Login pages (form + image)
- Feature comparisons
- Before/after views

**Tailwind Implementation (50/50)**:
```tsx
<div className="flex flex-col md:flex-row min-h-screen">
  {/* Left Section */}
  <div className="flex-1 bg-blue-600 flex items-center justify-center p-8">
    {/* Content */}
  </div>

  {/* Right Section */}
  <div className="flex-1 bg-white flex items-center justify-center p-8">
    {/* Content */}
  </div>
</div>
```

**Tailwind Implementation (40/60)**:
```tsx
<div className="flex flex-col lg:flex-row min-h-screen">
  <div className="lg:w-2/5 bg-gray-50 p-8">
    {/* Smaller section */}
  </div>

  <div className="lg:w-3/5 bg-white p-8">
    {/* Larger section */}
  </div>
</div>
```

## 6. Holy Grail Layout

**Description**: Header, footer, sidebar, and main content area.

**Common Use Cases**:
- Complex dashboards
- Enterprise applications
- Content management systems

**Tailwind Implementation**:
```tsx
<div className="flex flex-col min-h-screen">
  {/* Header */}
  <header className="bg-white border-b border-gray-200 h-16">
    {/* Header content */}
  </header>

  {/* Main area with sidebar */}
  <div className="flex flex-1">
    {/* Sidebar */}
    <aside className="w-64 bg-gray-50 border-r border-gray-200 overflow-y-auto">
      {/* Sidebar content */}
    </aside>

    {/* Main Content */}
    <main className="flex-1 overflow-y-auto p-8">
      {/* Content */}
    </main>
  </div>

  {/* Footer */}
  <footer className="bg-gray-100 border-t border-gray-200 p-4">
    {/* Footer content */}
  </footer>
</div>
```

## 7. Dashboard Layout (Stats Grid)

**Description**: Grid of metric/stat cards.

**Common Use Cases**:
- Analytics dashboards
- Admin panels
- Monitoring systems

**Tailwind Implementation**:
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
  {stats.map(stat => (
    <div key={stat.id} className="bg-white rounded-lg shadow p-6">
      <div className="text-sm font-medium text-gray-600">{stat.label}</div>
      <div className="mt-2 text-3xl font-bold text-gray-900">{stat.value}</div>
      <div className="mt-2 text-sm text-green-600">{stat.change}</div>
    </div>
  ))}
</div>
```

## 8. Centered Modal/Card

**Description**: Single card or modal centered on page.

**Common Use Cases**:
- Login forms
- Registration forms
- Simple wizards
- Coming soon pages

**Tailwind Implementation**:
```tsx
<div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
  <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
    {/* Form or content */}
  </div>
</div>
```

**Common Card Widths**:
- Small: `max-w-sm` (384px)
- Medium: `max-w-md` (448px)
- Large: `max-w-lg` (512px)

## 9. List + Detail (Master-Detail)

**Description**: List of items on left, selected item details on right.

**Common Use Cases**:
- Email clients
- Messaging apps
- File browsers
- Contact lists

**Tailwind Implementation**:
```tsx
<div className="flex h-screen">
  {/* List */}
  <div className="w-80 bg-white border-r border-gray-200 overflow-y-auto">
    {items.map(item => (
      <div key={item.id} className="p-4 border-b border-gray-200 hover:bg-gray-50 cursor-pointer">
        {/* List item */}
      </div>
    ))}
  </div>

  {/* Detail */}
  <div className="flex-1 bg-gray-50 overflow-y-auto p-8">
    {/* Selected item details */}
  </div>
</div>
```

## 10. Hero Section

**Description**: Large banner section with headline and CTA.

**Common Use Cases**:
- Landing pages
- Marketing sites
- Product pages

**Tailwind Implementation**:
```tsx
<section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
  <div className="max-w-7xl mx-auto px-4 py-24 text-center">
    <h1 className="text-5xl font-bold mb-6">
      Your Headline Here
    </h1>
    <p className="text-xl mb-8 max-w-2xl mx-auto">
      Supporting text that explains the value proposition
    </p>
    <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-gray-100">
      Call to Action
    </button>
  </div>
</section>
```

**Common Hero Heights**:
- Short: `py-16` or `py-20`
- Medium: `py-24` or `py-32`
- Full viewport: `min-h-screen flex items-center`

## 11. Tab Layout

**Description**: Tabbed interface with content panels.

**Common Use Cases**:
- Settings pages
- Profile pages
- Multi-step forms
- Product details

**Tailwind Implementation**:
```tsx
<div className="bg-white rounded-lg shadow">
  {/* Tab Headers */}
  <div className="border-b border-gray-200">
    <nav className="flex space-x-8 px-6" aria-label="Tabs">
      <button className="border-b-2 border-blue-500 py-4 px-1 text-sm font-medium text-blue-600">
        Tab 1
      </button>
      <button className="border-b-2 border-transparent py-4 px-1 text-sm font-medium text-gray-500 hover:text-gray-700 hover:border-gray-300">
        Tab 2
      </button>
    </nav>
  </div>

  {/* Tab Content */}
  <div className="p-6">
    {/* Active tab content */}
  </div>
</div>
```

## 12. Sticky Sidebar + Content

**Description**: Sidebar that sticks while content scrolls.

**Common Use Cases**:
- Documentation
- Long-form articles with TOC
- Product pages with filters

**Tailwind Implementation**:
```tsx
<div className="max-w-7xl mx-auto px-4 py-8">
  <div className="flex gap-8">
    {/* Sticky Sidebar */}
    <aside className="w-64 flex-shrink-0">
      <div className="sticky top-8">
        {/* Sidebar content */}
      </div>
    </aside>

    {/* Scrollable Content */}
    <main className="flex-1">
      {/* Long content */}
    </main>
  </div>
</div>
```

## Common Spacing Patterns

### Container Padding
- Mobile: `px-4` (16px)
- Tablet: `md:px-6` (24px)
- Desktop: `lg:px-8` (32px)

### Vertical Spacing
- Section gaps: `py-12` or `py-16` or `py-24`
- Component gaps: `space-y-6` or `space-y-8`
- Content gaps: `space-y-4`

### Max Width Containers
- Small: `max-w-4xl` (896px)
- Medium: `max-w-5xl` (1024px)
- Large: `max-w-6xl` (1152px)
- Extra Large: `max-w-7xl` (1280px)

## Responsive Strategy

### Mobile First Approach
Always start with mobile layout, then add larger breakpoints:

```tsx
// Mobile: Stack vertically
// Tablet: 2 columns
// Desktop: 3 columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
```

### Common Breakpoints (Tailwind)
- `sm`: 640px (small tablets)
- `md`: 768px (tablets)
- `lg`: 1024px (laptops)
- `xl`: 1280px (desktops)
- `2xl`: 1536px (large desktops)

### Hiding Elements Responsively
```tsx
// Show on mobile only
<div className="block md:hidden">Mobile menu</div>

// Hide on mobile
<div className="hidden md:block">Desktop menu</div>

// Show on tablet and up
<div className="hidden md:block">Tablet+ content</div>
```
