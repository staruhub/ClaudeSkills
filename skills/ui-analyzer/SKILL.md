---
name: ui-analyzer
description: Analyze UI design screenshots and generate React components with TypeScript and Tailwind CSS. Use this skill when the user provides UI mockups, design screenshots, or Figma exports and requests implementation. Provides detailed layout analysis, component breakdown, design token extraction, and production-ready code generation following best practices.
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# UI Analyzer

This skill provides a systematic approach to analyzing UI design screenshots and translating them into production-ready React components using TypeScript and Tailwind CSS.

## Purpose

Transform UI design screenshots into well-structured, accessible, and maintainable React components. The skill guides through analyzing layouts, extracting design tokens, identifying components, and generating clean code that matches the design while following best practices.

## When to Use This Skill

Use this skill when:
- The user provides a UI design screenshot, mockup, or Figma export
- The user requests "implement this design" or "build this UI"
- The user asks to "analyze this screenshot"
- The user wants to convert a design to code
- The user needs help understanding a UI's structure
- The user requests matching an existing design

## Analysis Workflow

Follow these steps systematically when analyzing a UI screenshot:

### Step 1: Initial Observation and Screenshot Reading

**Read the provided screenshot first** using the Read tool if a file path is provided, or if the user has shared an image in the conversation.

After viewing the screenshot:
1. Describe what you see in the UI
2. Identify the screen/page type (login, dashboard, form, etc.)
3. Determine the target device (desktop, mobile, responsive)
4. Note the overall aesthetic (modern, minimal, colorful, etc.)
5. Confirm understanding with the user before proceeding

### Step 2: Layout Analysis

Identify the high-level layout structure:

1. **Main layout type** - Consult `references/layout-patterns.md` to identify:
   - Single column
   - Sidebar layout
   - Header + content
   - Grid layout
   - Split screen
   - Dashboard
   - Master-detail
   - Other patterns

2. **Layout hierarchy** - Break down into sections:
   - Header/navigation
   - Main content area
   - Sidebar (if present)
   - Footer (if present)
   - Nested structures

3. **Responsive considerations**:
   - How should layout adapt to mobile?
   - Which elements stack or hide?
   - Breakpoint strategy

Reference `references/layout-patterns.md` for Tailwind implementation patterns.

### Step 3: Component Identification

Systematically identify all UI components using `references/ui-analysis-checklist.md`:

**Navigation Components**:
- Top nav, sidebar nav, breadcrumbs, tabs, etc.

**Data Display Components**:
- Cards, tables, lists, stats, badges, avatars, icons, etc.

**Input Components**:
- Text inputs, selects, checkboxes, radios, switches, date pickers, etc.

**Action Components**:
- Buttons (primary, secondary, etc.), icon buttons, links, etc.

**Feedback Components**:
- Alerts, toasts, progress bars, loading states, etc.

**Overlay Components**:
- Modals, drawers, tooltips, popovers, dropdowns, etc.

List all identified components with:
- Component type and purpose
- Location in the layout
- Approximate size and styling
- Interactive states (if visible)

### Step 4: Design Token Extraction

Extract design system values using `references/design-tokens.md`:

**Color Palette**:
1. Identify all unique colors in the design
2. Categorize by usage:
   - Primary brand color
   - Secondary/accent colors
   - Background colors (main, secondary)
   - Text colors (primary, secondary, muted)
   - Border colors
   - State colors (success, warning, error, info)
3. Map each color to nearest Tailwind color or note custom color needed
4. Create a color reference table

**Typography**:
1. Identify font family (serif, sans-serif, monospace)
2. List all text sizes observed
3. Map to Tailwind typography scale (`text-xs` to `text-6xl`)
4. Note font weights used (normal, medium, semibold, bold)
5. Identify heading hierarchy (H1-H6)

**Spacing**:
1. Observe padding patterns (card padding, button padding, etc.)
2. Observe margin/gap patterns (between sections, between items)
3. Map to Tailwind spacing scale (p-4, m-6, gap-8, etc.)
4. Note the spacing unit (usually 4px or 8px base)

**Other Tokens**:
- Border radius (rounded-none to rounded-full)
- Shadows (shadow-sm to shadow-2xl)
- Border widths
- Icon sizes

Reference `references/design-tokens.md` for complete mapping tables.

### Step 5: Detailed Component Analysis

For each major component identified:

1. **Component boundaries** - Where does it start/end?
2. **Props/data** - What data does it receive?
3. **Internal structure** - Sub-components and elements
4. **Styling details**:
   - Background color
   - Text color and size
   - Padding and margins
   - Border and radius
   - Shadow
5. **Interactive states** (if visible or inferable):
   - Hover
   - Active/pressed
   - Focused
   - Disabled
   - Loading
   - Error
6. **Accessibility needs**:
   - ARIA labels
   - Semantic HTML
   - Keyboard navigation

### Step 6: Implementation Strategy

Plan the implementation approach:

1. **Component hierarchy** - Which components to build first?
2. **Reusability** - Which patterns repeat? Extract to reusable components
3. **State management** - Does any component need Zustand or just local state?
4. **Integration with react-component-generator** - Can existing templates be used?
5. **File structure** - Where should components live?

**If the react-component-generator skill is available**:
- Reference its templates for common components (forms, cards, buttons, modals, etc.)
- Use its best practices for component structure
- Follow its naming conventions

### Step 7: Code Generation

Generate React components following these principles:

**Structure**:
1. Start with TypeScript interfaces for props
2. Use functional components with React.FC
3. Include JSDoc comments
4. Export both named and default exports

**Styling**:
1. Use Tailwind CSS exclusively for styling
2. Apply extracted design tokens
3. Organize classes logically (layout → spacing → colors → effects → states)
4. Use responsive classes where needed (sm:, md:, lg:, xl:)

**Best Practices**:
1. Use semantic HTML elements
2. Include ARIA attributes for accessibility
3. Handle loading and error states
4. Support keyboard navigation
5. Use proper TypeScript types (no `any`)
6. Keep components focused and composable

**Example Component Template**:
```tsx
import React from 'react';

interface ComponentNameProps {
  // Props based on analysis
  title: string;
  description?: string;
  onClick?: () => void;
  className?: string;
}

/**
 * ComponentName - Brief description based on UI purpose
 *
 * @param props - Component props
 * @returns JSX.Element
 */
export const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  description,
  onClick,
  className = ''
}) => {
  return (
    <div className={`/* Tailwind classes from design */ ${className}`}>
      {/* Implementation based on screenshot */}
    </div>
  );
};

export default ComponentName;
```

### Step 8: Verification and Refinement

After generating code:

1. **Review against screenshot** - Does it match the design?
2. **Check responsiveness** - Will it work on different screen sizes?
3. **Verify accessibility** - Are ARIA labels and semantic HTML present?
4. **Validate design tokens** - Are colors, spacing, typography correct?
5. **Consider edge cases** - Long text, empty states, loading states
6. **Note assumptions** - Clearly state what was assumed vs confirmed

### Step 9: Deliverables

Provide the user with:

1. **Analysis Summary**:
   - Layout description
   - Component breakdown
   - Design tokens extracted

2. **Generated Code**:
   - Complete React component(s)
   - TypeScript interfaces
   - Tailwind classes applied

3. **Implementation Notes**:
   - Installation requirements (if any packages needed)
   - Usage examples
   - Customization suggestions
   - Responsive behavior notes

4. **Next Steps**:
   - Suggest improvements or variations
   - Note areas that might need refinement
   - Offer to generate additional related components

## Common Scenarios

### Scenario 1: Simple Form Screenshot

**User**: "Implement this login form design [screenshot]"

**Approach**:
1. Read screenshot
2. Identify: Centered card layout with form inputs and button
3. Extract: Colors, input styling, button styling, spacing
4. Reference `layout-patterns.md` → "Centered Modal/Card" pattern
5. Reference `react-component-generator` → FormComponent template
6. Generate: LoginForm.tsx with proper validation structure
7. Apply Tailwind classes matching the design

### Scenario 2: Dashboard Screenshot

**User**: "Build this dashboard UI [screenshot]"

**Approach**:
1. Read screenshot
2. Identify: Header + sidebar layout with grid of stat cards
3. Break down into components:
   - Header component
   - Sidebar navigation
   - StatCard component (repeated)
   - Main dashboard layout
4. Extract design tokens for consistency
5. Reference `layout-patterns.md` → "Dashboard Layout" pattern
6. Generate components starting with reusable StatCard
7. Compose into main Dashboard component

### Scenario 3: Complex Page with Multiple Sections

**User**: "Implement this landing page [screenshot]"

**Approach**:
1. Read screenshot
2. Identify sections: Hero, features grid, testimonials, CTA
3. Analyze each section separately using checklist
4. Extract shared design tokens
5. Generate section components one by one
6. Show how sections compose into the full page
7. Provide responsive behavior notes

### Scenario 4: Component Library Screenshot

**User**: "Create components from this design system screenshot [screenshot]"

**Approach**:
1. Read screenshot
2. Identify: Multiple variations of buttons, inputs, cards shown
3. Extract design tokens for the system
4. Generate each component variant
5. Document the prop variations
6. Create a usage guide
7. Suggest how to organize in the project

## Reference Files Usage

### references/ui-analysis-checklist.md
- **When to use**: During Step 3 (Component Identification) and as a comprehensive analysis guide
- **Purpose**: Ensures no components or details are missed
- **How**: Work through checklist sections systematically

### references/layout-patterns.md
- **When to use**: During Step 2 (Layout Analysis) and Step 7 (Code Generation)
- **Purpose**: Quickly identify common patterns and get implementation code
- **How**: Match observed layout to pattern, adapt provided code

### references/design-tokens.md
- **When to use**: During Step 4 (Design Token Extraction) and Step 7 (Code Generation)
- **Purpose**: Map visual elements to Tailwind classes accurately
- **How**: Use color tables, spacing scale, and component size guides

## Tips for Accurate Analysis

1. **Be systematic** - Follow the workflow steps in order, don't skip ahead
2. **Take measurements** - Estimate sizes and spacing carefully
3. **Look for patterns** - Repeated elements indicate design system consistency
4. **Note uncertainties** - Clearly mark assumptions vs confirmed details
5. **Think responsive** - Always consider mobile behavior
6. **Prioritize accessibility** - Include ARIA labels and semantic HTML from the start
7. **Stay DRY** - Extract reusable components when patterns repeat
8. **Consult references** - Use the reference files liberally for accuracy
9. **Verify with user** - Confirm understanding before extensive code generation
10. **Iterate** - Expect refinement based on user feedback

## Integration with Other Skills

### With react-component-generator skill
When both skills are available:
1. Use ui-analyzer to understand the design and extract requirements
2. Reference react-component-generator templates for similar components
3. Apply ui-analyzer's extracted design tokens to the templates
4. Follow react-component-generator's naming and structure conventions

This creates a powerful workflow: analyze → identify template → customize → implement.

## Example Full Workflow

**User provides login page screenshot**

1. ✅ Read screenshot and describe the UI
2. ✅ Identify: Centered card layout, split-screen with image
3. ✅ Extract design tokens:
   - Primary blue: #3B82F6 → `bg-blue-500`
   - Text: #1F2937 → `text-gray-800`
   - Background: #F9FAFB → `bg-gray-50`
   - Card padding: ~32px → `p-8`
   - Input height: ~40px → `h-10`
   - Button: blue background, white text, rounded-md
4. ✅ Identify components:
   - Logo/brand element
   - Heading and subheading
   - Email input (with label)
   - Password input (with label, show/hide icon)
   - "Remember me" checkbox
   - "Forgot password?" link
   - Submit button
   - Sign up link at bottom
5. ✅ Reference layout-patterns.md → Split Screen + Centered Card patterns
6. ✅ Generate LoginForm.tsx:
   - TypeScript interfaces for props
   - Form validation structure
   - Tailwind classes matching design
   - Accessibility attributes
   - Responsive behavior (stacked on mobile)
7. ✅ Provide usage example and notes
8. ✅ Offer to generate the accompanying image section or adjust styling

## Notes

- Always read the screenshot first before any analysis
- Prioritize user confirmation of understanding before extensive code generation
- When in doubt about colors or spacing, choose the closest Tailwind default
- Document all assumptions clearly
- Provide complete, runnable code, not pseudocode
- Consider suggesting improvements while matching the design
- Be prepared to iterate based on user feedback
