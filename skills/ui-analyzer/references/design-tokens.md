# Design Tokens and Tailwind Mapping

## Overview

This document helps map visual design elements from screenshots to Tailwind CSS classes and design tokens.

## Color Mapping

### Primary Color Approximation

When analyzing screenshots, approximate colors to the nearest Tailwind color:

#### Blues
- `#EFF6FF` → `bg-blue-50`
- `#DBEAFE` → `bg-blue-100`
- `#BFDBFE` → `bg-blue-200`
- `#93C5FD` → `bg-blue-300`
- `#60A5FA` → `bg-blue-400`
- `#3B82F6` → `bg-blue-500` ⭐ Primary blue
- `#2563EB` → `bg-blue-600`
- `#1D4ED8` → `bg-blue-700`
- `#1E40AF` → `bg-blue-800`
- `#1E3A8A` → `bg-blue-900`

#### Grays (Most commonly used)
- `#F9FAFB` → `bg-gray-50` (Lightest background)
- `#F3F4F6` → `bg-gray-100` (Light background)
- `#E5E7EB` → `bg-gray-200` (Borders, dividers)
- `#D1D5DB` → `bg-gray-300`
- `#9CA3AF` → `bg-gray-400` (Disabled text)
- `#6B7280` → `bg-gray-500` (Secondary text)
- `#4B5563` → `bg-gray-600`
- `#374151` → `bg-gray-700` (Primary text)
- `#1F2937` → `bg-gray-800`
- `#111827` → `bg-gray-900` (Darkest text)

#### Greens (Success states)
- `#ECFDF5` → `bg-green-50`
- `#D1FAE5` → `bg-green-100`
- `#10B981` → `bg-green-500` ⭐ Success green
- `#059669` → `bg-green-600`
- `#047857` → `bg-green-700`

#### Reds (Error/Danger states)
- `#FEF2F2` → `bg-red-50`
- `#FEE2E2` → `bg-red-100`
- `#EF4444` → `bg-red-500` ⭐ Error red
- `#DC2626` → `bg-red-600`
- `#B91C1C` → `bg-red-700`

#### Yellows (Warning states)
- `#FFFBEB` → `bg-yellow-50`
- `#FEF3C7` → `bg-yellow-100`
- `#F59E0B` → `bg-yellow-500` ⭐ Warning yellow
- `#D97706` → `bg-yellow-600`

#### Purples/Indigos
- `#EEF2FF` → `bg-indigo-50`
- `#E0E7FF` → `bg-indigo-100`
- `#6366F1` → `bg-indigo-500` ⭐ Primary indigo
- `#4F46E5` → `bg-indigo-600`

### Color Usage Patterns

#### Background Colors
```tsx
// Page background
className="bg-gray-50"  // or bg-white

// Card background
className="bg-white"

// Hover background
className="hover:bg-gray-100"

// Selected/Active background
className="bg-blue-50"  // Tinted with primary color
```

#### Text Colors
```tsx
// Primary text
className="text-gray-900"

// Secondary text
className="text-gray-600"

// Muted/helper text
className="text-gray-500"

// Link text
className="text-blue-600 hover:text-blue-800"

// Error text
className="text-red-600"

// Success text
className="text-green-600"
```

#### Border Colors
```tsx
// Default border
className="border-gray-200"

// Stronger border
className="border-gray-300"

// Focus border
className="border-blue-500"

// Error border
className="border-red-500"
```

### Custom Color Identification

If the design uses custom colors not in Tailwind:

1. **Identify the hex value** (estimate from screenshot)
2. **Find closest Tailwind color** using the tables above
3. **Note if custom color needed** in tailwind.config.js:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'brand-primary': '#5B47FB',
        'brand-secondary': '#FF6B6B',
      }
    }
  }
}
```

## Typography Scale

### Font Sizes

Map observed text sizes to Tailwind classes:

| Observed Size | Tailwind Class | Pixels |
|---------------|----------------|--------|
| Very small text | `text-xs` | 12px |
| Small text | `text-sm` | 14px |
| Base text | `text-base` | 16px ⭐ |
| Medium text | `text-lg` | 18px |
| Large text | `text-xl` | 20px |
| H4 headings | `text-2xl` | 24px |
| H3 headings | `text-3xl` | 30px |
| H2 headings | `text-4xl` | 36px |
| H1 headings | `text-5xl` | 48px |
| Large H1 | `text-6xl` | 60px |

### Font Weights

| Observed Weight | Tailwind Class | Font Weight |
|-----------------|----------------|-------------|
| Thin | `font-thin` | 100 |
| Light | `font-light` | 300 |
| Normal/Regular | `font-normal` | 400 ⭐ |
| Medium | `font-medium` | 500 |
| Semibold | `font-semibold` | 600 |
| Bold | `font-bold` | 700 |
| Extra bold | `font-extrabold` | 800 |

### Common Typography Patterns

```tsx
// H1 - Page title
className="text-4xl font-bold text-gray-900"

// H2 - Section heading
className="text-3xl font-semibold text-gray-900"

// H3 - Subsection
className="text-2xl font-semibold text-gray-900"

// Body text
className="text-base text-gray-600"

// Small caption/helper text
className="text-sm text-gray-500"

// Button text
className="text-sm font-medium"  // or font-semibold

// Link text
className="text-blue-600 hover:text-blue-800 underline"
```

## Spacing Scale

### Padding & Margin

Map observed spacing to Tailwind scale:

| Pixels | Tailwind Class | Usage |
|--------|----------------|-------|
| 4px | `p-1` or `m-1` | Tiny spacing |
| 8px | `p-2` or `m-2` | Very small spacing |
| 12px | `p-3` or `m-3` | Small spacing |
| 16px | `p-4` or `m-4` | Base spacing ⭐ |
| 20px | `p-5` or `m-5` | Medium spacing |
| 24px | `p-6` or `m-6` | Large spacing |
| 32px | `p-8` or `m-8` | Extra large spacing |
| 48px | `p-12` or `m-12` | Section spacing |
| 64px | `p-16` or `m-16` | Large section spacing |
| 96px | `p-24` or `m-24` | Hero spacing |

### Common Spacing Patterns

```tsx
// Card padding
className="p-6"  // or p-4 for compact, p-8 for spacious

// Button padding
className="px-4 py-2"  // Standard
className="px-6 py-3"  // Large

// Input padding
className="px-3 py-2"  // Standard
className="px-4 py-3"  // Large

// Container padding
className="px-4 py-8"  // Mobile
className="md:px-6 lg:px-8"  // Responsive

// Stack spacing (vertical)
className="space-y-4"  // Standard gap between items
className="space-y-6"  // Larger gap
className="space-y-2"  // Tight gap

// Flex gap (horizontal)
className="gap-4"  // Standard
className="gap-2"  // Tight
className="gap-6"  // Spacious
```

## Border Radius

Map corner roundedness to Tailwind:

| Observed Roundness | Tailwind Class | Pixels |
|--------------------|----------------|--------|
| No rounding | `rounded-none` | 0px |
| Subtle | `rounded-sm` | 2px |
| Small | `rounded` | 4px ⭐ |
| Medium | `rounded-md` | 6px |
| Large | `rounded-lg` | 8px |
| Extra large | `rounded-xl` | 12px |
| 2X large | `rounded-2xl` | 16px |
| 3X large | `rounded-3xl` | 24px |
| Full/Pill | `rounded-full` | 9999px |

### Common Usage

```tsx
// Cards
className="rounded-lg"  // or rounded-xl

// Buttons
className="rounded-md"  // or rounded-lg

// Inputs
className="rounded-md"

// Badges/Pills
className="rounded-full"

// Images/Avatars
className="rounded-full"  // Circle
className="rounded-lg"    // Rounded corners
```

## Shadows

Map shadow depth to Tailwind:

| Shadow Depth | Tailwind Class | Usage |
|--------------|----------------|-------|
| None | `shadow-none` | Flat elements |
| Subtle | `shadow-sm` | Slight elevation |
| Default | `shadow` | Standard cards |
| Medium | `shadow-md` | Raised cards ⭐ |
| Large | `shadow-lg` | Modals, dropdowns |
| Extra large | `shadow-xl` | Important modals |
| 2X large | `shadow-2xl` | Hero elements |

### Common Shadow Patterns

```tsx
// Cards
className="shadow-md hover:shadow-lg transition-shadow"

// Dropdowns/Modals
className="shadow-xl"

// Buttons (subtle)
className="shadow-sm hover:shadow-md"

// Floating action button
className="shadow-lg"
```

## Component Size Standards

### Buttons

```tsx
// Small
className="px-3 py-1.5 text-sm"

// Medium (default)
className="px-4 py-2 text-base"

// Large
className="px-6 py-3 text-lg"
```

### Inputs

```tsx
// Small
className="h-8 px-3 text-sm"

// Medium (default)
className="h-10 px-3 text-base"

// Large
className="h-12 px-4 text-lg"
```

### Avatars

```tsx
// Extra small
className="h-6 w-6"

// Small
className="h-8 w-8"

// Medium
className="h-10 w-10"

// Large
className="h-12 w-12"

// Extra large
className="h-16 w-16"
```

### Icons

```tsx
// Small
className="h-4 w-4"  // 16px

// Medium
className="h-5 w-5"  // 20px

// Large
className="h-6 w-6"  // 24px

// Extra large
className="h-8 w-8"  // 32px
```

## Transition & Animation

### Common Transitions

```tsx
// Color transitions (buttons, links)
className="transition-colors duration-200"

// All transitions
className="transition-all duration-300"

// Shadow transitions (cards)
className="transition-shadow duration-200"

// Transform transitions (modals, drawers)
className="transition-transform duration-300"
```

## Z-Index Layering

```tsx
// Dropdown menus
className="z-10"

// Sticky headers
className="z-20"

// Modals backdrop
className="z-40"

// Modals content
className="z-50"

// Tooltips
className="z-50"
```

## Responsive Breakpoint Strategy

### Container Widths

```tsx
// Full width on mobile, constrained on larger screens
className="w-full max-w-7xl mx-auto"

// Common max-widths
className="max-w-sm"   // 384px - Small cards
className="max-w-md"   // 448px - Forms
className="max-w-lg"   // 512px - Modals
className="max-w-xl"   // 576px - Articles
className="max-w-2xl"  // 672px - Wide articles
className="max-w-4xl"  // 896px - Dashboards
className="max-w-6xl"  // 1152px - Full layouts
className="max-w-7xl"  // 1280px - Large layouts
```

### Responsive Text Sizes

```tsx
// Responsive headings
className="text-3xl md:text-4xl lg:text-5xl"

// Responsive body text
className="text-sm md:text-base"
```

### Responsive Spacing

```tsx
// Responsive padding
className="p-4 md:p-6 lg:p-8"

// Responsive gaps
className="gap-4 md:gap-6 lg:gap-8"
```

## Quick Reference: Design Token Extraction

When analyzing a UI screenshot:

1. **Identify color palette** (5-10 main colors max)
2. **Map to Tailwind colors** (or note custom colors needed)
3. **Identify spacing unit** (usually 4px or 8px base)
4. **Note typography scale** (font sizes and weights used)
5. **Observe border radius** (consistent or varies by component?)
6. **Check shadow usage** (flat design or elevated?)
7. **Look for patterns** (repeated spacing, consistent button styles, etc.)

This creates a "design system snapshot" that guides implementation.
