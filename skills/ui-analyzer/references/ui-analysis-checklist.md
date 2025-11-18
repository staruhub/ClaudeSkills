# UI Analysis Checklist

## Overview

This checklist provides a systematic approach to analyzing UI design screenshots and extracting actionable implementation details.

## Step 1: Initial Assessment

### Screen Type Identification
- [ ] Login/Registration page
- [ ] Dashboard/Home page
- [ ] List/Table view
- [ ] Detail/Profile page
- [ ] Form/Data entry
- [ ] Settings page
- [ ] Modal/Dialog
- [ ] Navigation/Menu
- [ ] Landing page
- [ ] Other: _______

### Device/Platform
- [ ] Desktop (>1024px)
- [ ] Tablet (768px - 1024px)
- [ ] Mobile (<768px)
- [ ] Responsive (multiple breakpoints visible)

## Step 2: Layout Analysis

### Overall Structure
- [ ] Identify main layout type (single column, sidebar, grid, etc.)
- [ ] Note header presence and content
- [ ] Note footer presence and content
- [ ] Identify sidebar (left/right, fixed/collapsible)
- [ ] Map main content area structure

### Grid System
- [ ] Determine number of columns in grid layouts
- [ ] Identify grid gaps/gutters
- [ ] Note any asymmetric layouts
- [ ] Check for nested grids

### Spacing & Alignment
- [ ] Consistent padding values (estimate in px: 8, 16, 24, 32, etc.)
- [ ] Consistent margin values
- [ ] Vertical rhythm (spacing between sections)
- [ ] Horizontal alignment patterns
- [ ] Content max-width constraints

## Step 3: Component Identification

### Navigation Components
- [ ] Top navigation bar
- [ ] Sidebar navigation
- [ ] Breadcrumbs
- [ ] Tabs
- [ ] Pagination
- [ ] Dropdown menus

### Data Display Components
- [ ] Cards
- [ ] Tables
- [ ] Lists (ordered/unordered)
- [ ] Charts/Graphs
- [ ] Stats/Metrics displays
- [ ] Badges/Tags
- [ ] Avatars/Profile images
- [ ] Icons

### Input Components
- [ ] Text inputs
- [ ] Textareas
- [ ] Select dropdowns
- [ ] Radio buttons
- [ ] Checkboxes
- [ ] Switches/Toggles
- [ ] Date pickers
- [ ] File uploads
- [ ] Search bars

### Action Components
- [ ] Primary buttons
- [ ] Secondary buttons
- [ ] Icon buttons
- [ ] Link buttons
- [ ] Floating action buttons (FAB)

### Feedback Components
- [ ] Alerts/Notifications
- [ ] Toasts
- [ ] Progress bars
- [ ] Loading spinners
- [ ] Empty states
- [ ] Error messages

### Overlay Components
- [ ] Modals/Dialogs
- [ ] Drawers/Sidesheets
- [ ] Tooltips
- [ ] Popovers
- [ ] Dropdown menus

## Step 4: Visual Design Analysis

### Color Palette
Extract and categorize colors:
- [ ] Primary color (main brand color)
- [ ] Secondary color(s)
- [ ] Accent color(s)
- [ ] Background colors (main, secondary, tertiary)
- [ ] Text colors (primary, secondary, muted)
- [ ] Border colors
- [ ] Success color (green)
- [ ] Warning color (yellow/orange)
- [ ] Error color (red)
- [ ] Info color (blue)

For each color, note:
- Hex value (estimate)
- Where it's used
- Tailwind equivalent (if applicable)

### Typography
- [ ] Primary font family (serif/sans-serif/monospace)
- [ ] Heading hierarchy (H1, H2, H3, etc.)
  - Font sizes
  - Font weights
  - Line heights
  - Letter spacing
- [ ] Body text size and weight
- [ ] Small/caption text size
- [ ] Link styling (color, underline, hover state)

### Shadows & Depth
- [ ] Card shadows (sm, md, lg)
- [ ] Button shadows
- [ ] Dropdown/modal shadows
- [ ] Layering system (z-index hierarchy)

### Borders & Radius
- [ ] Border widths (1px, 2px, etc.)
- [ ] Border radius values (rounded corners)
  - None (0px)
  - Small (2-4px)
  - Medium (6-8px)
  - Large (12-16px)
  - Full (rounded-full for pills/circles)

### Icons
- [ ] Icon style (outlined, filled, rounded)
- [ ] Icon sizes (16px, 20px, 24px, etc.)
- [ ] Icon library suggestion (Heroicons, Lucide, Material Icons, etc.)
- [ ] Icon colors and usage patterns

## Step 5: Interactive Elements Analysis

### Buttons
For each button type, note:
- [ ] Size (height, padding)
- [ ] Background color
- [ ] Text color
- [ ] Border style
- [ ] Border radius
- [ ] Hover state appearance
- [ ] Active/pressed state
- [ ] Disabled state
- [ ] Icon position (left/right/only)

### Form Inputs
For each input type, note:
- [ ] Size (height, padding)
- [ ] Border style (color, width)
- [ ] Focus state (ring, border color change)
- [ ] Error state styling
- [ ] Success state styling
- [ ] Placeholder text styling
- [ ] Label positioning (top, left, floating)
- [ ] Helper text style

### Links
- [ ] Default color
- [ ] Hover color
- [ ] Visited state (if different)
- [ ] Underline style
- [ ] Active state

## Step 6: Responsive Design Considerations

### Breakpoint Analysis
- [ ] Mobile layout changes (stacked columns, hidden elements)
- [ ] Tablet layout changes
- [ ] Desktop layout optimizations
- [ ] Navigation changes (hamburger menu vs full nav)

### Content Reflow
- [ ] Which elements stack vertically on mobile
- [ ] Which elements hide on smaller screens
- [ ] Font size adjustments across breakpoints
- [ ] Padding/margin adjustments

## Step 7: Accessibility Considerations

### Visual Accessibility
- [ ] Color contrast ratios (text vs background)
- [ ] Non-color indicators (icons, patterns)
- [ ] Focus indicators visible
- [ ] Text size readable (minimum 16px for body)

### Semantic Structure
- [ ] Logical heading hierarchy
- [ ] Form labels present
- [ ] Button text descriptive
- [ ] Link text meaningful
- [ ] Alt text needed for images

### Keyboard Navigation
- [ ] Tab order logical
- [ ] All interactive elements accessible
- [ ] Skip links needed
- [ ] Focus trapping in modals

## Step 8: Content Analysis

### Text Content
- [ ] Primary heading text
- [ ] Supporting text/descriptions
- [ ] Call-to-action copy
- [ ] Error messages
- [ ] Helper text
- [ ] Placeholder text

### Images & Media
- [ ] Hero images
- [ ] Product images
- [ ] User avatars
- [ ] Icons
- [ ] Logos
- [ ] Background images

### Data Patterns
- [ ] Example data shown
- [ ] Data format (dates, numbers, currency)
- [ ] Empty state content
- [ ] Loading state content
- [ ] Error state content

## Step 9: State Analysis

### Component States
For interactive components, identify:
- [ ] Default/idle state
- [ ] Hover state
- [ ] Active/pressed state
- [ ] Focused state
- [ ] Disabled state
- [ ] Loading state
- [ ] Success state
- [ ] Error state

### Application States
- [ ] Empty states (no data)
- [ ] Loading states
- [ ] Error states
- [ ] Success states (after actions)

## Step 10: Implementation Priority

### Must Have (P0)
Components and features critical to core functionality:
- [ ] List critical components
- [ ] Note essential interactions

### Should Have (P1)
Important but not blocking:
- [ ] List important components
- [ ] Note nice-to-have interactions

### Nice to Have (P2)
Polish and enhancements:
- [ ] List enhancement ideas
- [ ] Note optional features

## Output Format

After completing the analysis, organize findings into:

1. **Component Breakdown**: List of all unique components identified
2. **Layout Structure**: Hierarchy and organization
3. **Design Tokens**: Colors, typography, spacing values
4. **Implementation Notes**: Technical considerations and suggestions
5. **Accessibility Recommendations**: ARIA labels, semantic HTML suggestions
6. **Responsive Behavior**: Breakpoint-specific changes needed

## Tips for Accurate Analysis

1. **Use browser dev tools** if analyzing a live site to inspect actual values
2. **Estimate conservatively** when exact values are unknown - use Tailwind standard values
3. **Look for patterns** - repeated spacing/colors indicate a design system
4. **Consider the design system** - if Tailwind is the target, map to Tailwind classes
5. **Note uncertainties** - clearly mark assumptions vs confirmed details
6. **Take measurements** - use screen rulers or design tools to estimate sizes
7. **Check multiple states** - analyze all visible interaction states
8. **Consider edge cases** - long text, empty states, error states
