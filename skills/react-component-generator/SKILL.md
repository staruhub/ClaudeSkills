---
name: react-component-generator
description: Generate React components following best practices with TypeScript, Tailwind CSS, and Zustand state management. Use this skill when the user requests creating React components, UI elements, or mentions component generation. Supports common component patterns including basic components, forms, lists, cards, buttons, modals, and stateful components with Zustand integration.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# React Component Generator

This skill provides templates and best practices for generating high-quality React components using TypeScript, Tailwind CSS, and Zustand for state management.

## Purpose

Generate production-ready React components that follow industry best practices and maintain consistency across the codebase. The skill includes pre-built templates for common component patterns and comprehensive best practices documentation.

## When to Use This Skill

Use this skill when:
- The user requests creating a new React component
- The user asks for UI elements like forms, buttons, cards, lists, or modals
- The user mentions component generation or scaffolding
- The user needs a component with Zustand state management
- The user wants to follow React best practices

## Available Component Templates

The skill provides the following templates in the `assets/` directory:

### 1. BasicComponent.tsx
A simple presentational component template for UI elements without complex state.

**When to use:**
- Simple UI elements (headers, footers, containers)
- Presentational components that receive data via props
- Reusable layout components

**Key features:**
- TypeScript interface for props
- JSDoc documentation
- Tailwind CSS styling
- Children support

### 2. StatefulComponent.tsx
A component with integrated Zustand store for state management.

**When to use:**
- Components requiring complex local state
- Components with multiple related state values
- Components with state that might be shared across instances
- Components with async operations

**Key features:**
- Complete Zustand store setup
- State and actions separation
- TypeScript interfaces for store
- Loading state handling

### 3. FormComponent.tsx
A form component with validation, error handling, and submission logic.

**When to use:**
- Login/registration forms
- Contact forms
- Data entry forms
- Any form with validation requirements

**Key features:**
- Built-in validation logic
- Error state management
- Form submission handling
- Accessible form inputs with labels
- Loading state during submission

### 4. ListComponent.tsx
A reusable list component for displaying collections of items.

**When to use:**
- Todo lists
- User lists
- Product catalogs
- Any itemized data display

**Key features:**
- Generic item type support
- Item click handlers
- Delete functionality
- Empty state handling
- Responsive design

### 5. CardComponent.tsx
A flexible card component for content display.

**When to use:**
- Product cards
- User profile cards
- Content previews
- Dashboard widgets

**Key features:**
- Optional image section
- Header and footer sections
- Click handling
- Flexible content area

### 6. ButtonComponent.tsx
A versatile button component with multiple variants and states.

**When to use:**
- Any button needs in the application
- Call-to-action buttons
- Form submission buttons
- Action buttons

**Key features:**
- Multiple variants (primary, secondary, danger, success, outline)
- Multiple sizes (sm, md, lg)
- Loading state with spinner
- Disabled state
- Full-width option

### 7. ModalComponent.tsx
A modal/dialog component with backdrop and accessibility features.

**When to use:**
- Confirmation dialogs
- Content detail views
- Settings panels
- Any overlay UI

**Key features:**
- ESC key handling
- Backdrop click to close
- Body scroll prevention
- Multiple sizes
- Accessible markup

## How to Use Templates

When generating a component:

1. **Identify the component type** - Determine which template best fits the user's requirements.

2. **Read the appropriate template** - Load the template file from the `assets/` directory:
   ```
   Read assets/BasicComponent.tsx
   ```

3. **Customize the template** - Replace placeholder names and add specific functionality:
   - Replace `ComponentName` with the actual component name (PascalCase)
   - Update the interface name from `ComponentNameProps` to match
   - If using Zustand, update `useComponentNameStore` to match
   - Modify props to match requirements
   - Adjust Tailwind classes for styling
   - Add or remove features as needed

4. **Follow naming conventions** - Refer to `references/best-practices.md` for:
   - Component naming (PascalCase)
   - Props interface naming (ComponentName + "Props")
   - Store naming (use + ComponentName + "Store")
   - File organization

5. **Apply best practices** - Consult `references/best-practices.md` for guidance on:
   - TypeScript patterns
   - Zustand store structure
   - Tailwind CSS class organization
   - Accessibility requirements
   - Performance optimization
   - Error handling

## Component Naming Guidelines

Apply these naming rules when generating components:

1. **Component name**: Use PascalCase based on the user's description
   - "login form" → `LoginForm`
   - "user profile card" → `UserProfileCard`
   - "data table" → `DataTable`

2. **Props interface**: ComponentName + "Props"
   - `LoginForm` → `LoginFormProps`
   - `UserProfileCard` → `UserProfileCardProps`

3. **Zustand store**: "use" + ComponentName + "Store"
   - `LoginForm` → `useLoginFormStore`
   - `DataTable` → `useDataTableStore`

4. **File name**: Match the component name exactly
   - `LoginForm` → `LoginForm.tsx`
   - `UserProfileCard` → `UserProfileCard.tsx`

## Best Practices Reference

For detailed guidance, consult `references/best-practices.md` which covers:

- Component structure and file organization
- TypeScript best practices
- Zustand state management patterns
- Tailwind CSS organization and responsive design
- Component composition patterns
- Event handler naming
- Performance optimization (memoization, lazy loading)
- Accessibility (semantic HTML, ARIA, keyboard navigation)
- Error handling and boundaries
- Testing considerations

## Example Workflow

**User request**: "Create a user login form component"

**Steps**:
1. Identify that this requires a form component
2. Read `assets/FormComponent.tsx` template
3. Customize for login use case:
   - Rename to `LoginForm`
   - Update `LoginFormProps` interface
   - Modify form fields (username/email, password)
   - Add appropriate validation
   - Update styling with Tailwind classes
4. Place in appropriate directory (e.g., `components/auth/LoginForm.tsx`)
5. Verify accessibility and best practices

**User request**: "Create a product card with image and price"

**Steps**:
1. Identify that this requires a card component
2. Read `assets/CardComponent.tsx` template
3. Customize for product use case:
   - Rename to `ProductCard`
   - Update `ProductCardProps` to include price, product details
   - Adjust image section for product photos
   - Add price display in content or footer
   - Style with Tailwind for product display
4. Place in `components/products/ProductCard.tsx`

**User request**: "Create a todo list with Zustand"

**Steps**:
1. Identify that this requires a stateful list component
2. Read both `assets/StatefulComponent.tsx` and `assets/ListComponent.tsx`
3. Combine patterns:
   - Create Zustand store for todo state management
   - Use list display pattern for rendering todos
   - Add todo-specific actions (add, toggle, delete)
   - Integrate form for adding new todos
4. Name as `TodoList` with `useTodoListStore`
5. Place in `components/todos/TodoList.tsx`

## Notes

- Always use TypeScript with proper type definitions
- Follow Tailwind's mobile-first responsive design approach
- Include proper JSDoc comments for better IDE support
- Ensure components are accessible (ARIA labels, keyboard navigation)
- Consider performance (memoization for expensive operations)
- Keep components focused and composable
- Export both named and default exports for flexibility
