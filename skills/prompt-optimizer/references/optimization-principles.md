# Prompt Optimization Principles

## Overview

This document outlines principles and techniques for optimizing user prompts to improve clarity, completeness, and effectiveness when working with AI assistants.

## Core Principles

### 1. Clarity
Prompts should be unambiguous and easy to understand.

**Indicators of Poor Clarity**:
- Vague language ("something", "stuff", "thing")
- Ambiguous pronouns without clear referents
- Multiple possible interpretations
- Unclear desired outcome

**Optimization Techniques**:
- Use specific, concrete language
- Replace vague terms with precise descriptions
- Clarify pronouns and references
- State the desired outcome explicitly

**Examples**:
```
❌ Poor: "Fix the thing in the code"
✅ Better: "Fix the null pointer exception in UserService.java line 45"

❌ Poor: "Make it look better"
✅ Better: "Improve the visual design by adding more whitespace and using consistent colors"

❌ Poor: "Can you help with this?"
✅ Better: "Can you help me debug why my React component is re-rendering infinitely?"
```

### 2. Specificity
Prompts should provide sufficient detail about what's needed.

**Indicators of Poor Specificity**:
- Missing context about the problem domain
- No examples provided when examples would help
- Unclear scope or boundaries
- Missing technical requirements

**Optimization Techniques**:
- Include relevant context and background
- Provide examples when helpful
- Define scope and constraints
- Specify technical requirements (language, framework, version, etc.)

**Examples**:
```
❌ Poor: "Create a login form"
✅ Better: "Create a React login form component with email/password fields, validation, and a submit button using TypeScript and Tailwind CSS"

❌ Poor: "Optimize this code"
✅ Better: "Optimize this Python data processing code for better performance - it currently takes 5 minutes to process 1 million records"

❌ Poor: "Write tests"
✅ Better: "Write unit tests for the UserRepository class using Jest, covering the create, update, and delete methods"
```

### 3. Completeness
Prompts should include all necessary information to complete the task.

**Indicators of Incomplete Prompts**:
- Missing required inputs or data
- Undefined behavior for edge cases
- No success criteria specified
- Missing dependencies or prerequisites

**Optimization Techniques**:
- Include all relevant inputs, data, and context
- Specify expected behavior for edge cases
- Define what "done" looks like
- Mention dependencies and prerequisites

**Examples**:
```
❌ Poor: "Generate API documentation"
✅ Better: "Generate OpenAPI 3.0 documentation for the User Management API, including all CRUD endpoints, request/response schemas, authentication requirements, and error codes"

❌ Poor: "Refactor this component"
✅ Better: "Refactor this React component to use hooks instead of class components, maintain the same functionality, and ensure all existing tests still pass"
```

### 4. Structure
Well-structured prompts are easier to understand and act upon.

**Optimization Techniques**:
- Break complex requests into clear steps
- Use bullet points for lists
- Separate context from the actual request
- Order information logically (context → task → constraints)

**Examples**:
```
❌ Poor: "I need a dashboard with charts and it should show user stats and be responsive and use dark mode and have filters by date range and also export to CSV"

✅ Better:
Create a responsive analytics dashboard with the following requirements:

Features:
- Display user statistics using charts
- Date range filters
- CSV export functionality
- Dark mode support

Technical:
- Use React with TypeScript
- Chart library: Chart.js or Recharts
- Responsive design with Tailwind CSS
```

### 5. Actionability
Prompts should clearly indicate what action is needed.

**Indicators of Poor Actionability**:
- No clear verb or action requested
- Confusing or conflicting instructions
- Passive voice making the request unclear
- Missing indication of what the output should be

**Optimization Techniques**:
- Start with a clear action verb (create, fix, analyze, optimize, etc.)
- Use active voice
- Specify the expected output format
- Avoid conflicting instructions

**Examples**:
```
❌ Poor: "There's a bug in the authentication module"
✅ Better: "Debug and fix the authentication bug that prevents users from logging in with Google OAuth"

❌ Poor: "Something about database performance"
✅ Better: "Analyze the database query performance and suggest optimization strategies to reduce response time from 2s to under 500ms"
```

## Prompt Quality Checklist

Use this checklist to evaluate prompt quality:

### Context
- [ ] Relevant background information provided
- [ ] Problem domain explained
- [ ] Current state described (if applicable)
- [ ] Desired outcome specified

### Task Definition
- [ ] Clear action verb (create, fix, analyze, etc.)
- [ ] Specific task boundaries defined
- [ ] Success criteria stated
- [ ] Deliverable format specified

### Technical Requirements
- [ ] Programming language specified (if relevant)
- [ ] Framework/library mentioned (if relevant)
- [ ] Version constraints noted (if relevant)
- [ ] Platform/environment specified (if relevant)

### Constraints
- [ ] Time constraints mentioned (if any)
- [ ] Resource constraints noted (if any)
- [ ] Style/format requirements specified (if any)
- [ ] Edge cases considered (if relevant)

### Examples
- [ ] Examples provided when helpful
- [ ] Input/output examples given (for functions/APIs)
- [ ] Visual references included (for UI/design)

## Common Prompt Patterns

### Pattern 1: Code Implementation
```
Create a [language] [component/function/class] that [core functionality].

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Technical constraints:
- [Constraint 1]
- [Constraint 2]

Example usage:
[Code example]
```

### Pattern 2: Debugging
```
Debug the [component/function/system] that is experiencing [problem description].

Current behavior:
[What's happening now]

Expected behavior:
[What should happen]

Context:
- [Relevant file/location]
- [Error message if any]
- [Steps to reproduce]
```

### Pattern 3: Code Review/Analysis
```
Analyze [code/system/component] for [specific aspect: performance/security/maintainability].

Focus areas:
- [Area 1]
- [Area 2]
- [Area 3]

Provide:
- Issues found
- Severity assessment
- Specific recommendations
```

### Pattern 4: Design/Architecture
```
Design a [system/component/feature] for [use case].

Requirements:
- [Functional requirement 1]
- [Functional requirement 2]

Constraints:
- [Constraint 1]
- [Constraint 2]

Deliverables:
- Architecture diagram
- Component descriptions
- Data flow explanation
```

### Pattern 5: Refactoring
```
Refactor [code/component] to [improvement goal].

Current issues:
- [Issue 1]
- [Issue 2]

Requirements:
- Maintain existing functionality
- Keep all tests passing
- [Additional requirement]
```

## Red Flags in Prompts

Watch for these indicators of poor prompt quality:

### Vague Language
- "Something", "stuff", "thing", "it"
- "Better", "good", "nice" (without defining criteria)
- "Some kind of", "sort of", "maybe"

### Missing Information
- No programming language specified for code tasks
- No context about the problem
- No success criteria
- No examples when examples would help

### Ambiguity
- Multiple possible interpretations
- Unclear which of several options is wanted
- Conflicting requirements
- Undefined terms or acronyms

### Scope Issues
- Too broad ("build an app")
- Too narrow without context
- No clear boundaries
- Unrealistic scope

## Optimization Strategies by Problem Type

### For Vague Prompts
1. Ask clarifying questions to extract specifics
2. Provide options and ask user to choose
3. Make reasonable assumptions but state them clearly
4. Suggest a more specific alternative prompt

### For Incomplete Prompts
1. Identify missing information
2. Request specific details needed
3. Suggest adding context, requirements, or constraints
4. Provide a template with placeholders

### For Overly Complex Prompts
1. Break into smaller, manageable sub-tasks
2. Suggest a phased approach
3. Identify the core request vs. nice-to-haves
4. Recommend prioritization

### For Unclear Goal Prompts
1. Clarify the desired outcome
2. Ask about success criteria
3. Identify the underlying need
4. Suggest concrete deliverables

## Optimization Process

### Step 1: Analyze
- Read the original prompt carefully
- Identify issues using the checklist
- Note missing information
- Flag ambiguities

### Step 2: Categorize Issues
- Clarity problems
- Specificity gaps
- Completeness deficiencies
- Structure issues
- Actionability concerns

### Step 3: Enhance
- Add missing context
- Replace vague terms with specific ones
- Structure information logically
- Add examples if helpful
- Define success criteria

### Step 4: Validate
- Check against quality checklist
- Ensure all issues addressed
- Verify no new ambiguities introduced
- Confirm actionability

### Step 5: Present
- Show original prompt
- List identified issues
- Provide optimized version
- Explain key improvements
- Offer to refine further

## Examples of Full Optimizations

### Example 1: Code Request

**Original**:
```
Make a button component
```

**Issues**:
- No language/framework specified
- No styling requirements
- No props/API defined
- No use case context

**Optimized**:
```
Create a reusable Button component in React with TypeScript and Tailwind CSS.

Requirements:
- Support variants: primary, secondary, danger
- Support sizes: sm, md, lg
- Accept onClick handler and children
- Include loading and disabled states
- Use proper TypeScript types for props

Example usage:
<Button variant="primary" size="md" onClick={handleClick}>
  Click me
</Button>
```

### Example 2: Bug Fix Request

**Original**:
```
The app crashes sometimes
```

**Issues**:
- No specific error described
- No reproduction steps
- No context about when/where
- No error messages

**Optimized**:
```
Debug and fix the crash that occurs in the Shopping Cart component.

Observed behavior:
- App crashes when clicking the "Checkout" button
- Only happens when cart has more than 5 items
- Error in console: "Cannot read property 'price' of undefined"

Context:
- Component: src/components/ShoppingCart.tsx
- Occurs in production and development
- Started after recent refactor of pricing logic

Expected behavior:
- Checkout button should navigate to checkout page regardless of cart size
```

### Example 3: Analysis Request

**Original**:
```
Look at my code
```

**Issues**:
- No code provided or referenced
- No analysis goal specified
- No specific concerns mentioned
- No output format requested

**Optimized**:
```
Analyze the UserService.ts file for potential performance issues.

Focus on:
- Database query efficiency
- Unnecessary data fetching
- Missing caching opportunities
- N+1 query problems

Current performance:
- getUserProfile() takes 2-3 seconds
- Called frequently (on every page load)

Provide:
- List of identified issues with line numbers
- Severity assessment for each issue
- Specific optimization recommendations
- Estimated performance impact of fixes
```

## Tips for Self-Optimization

Encourage users to:
1. **Be specific** - Replace "thing" with the actual thing
2. **Add context** - Explain the "why" behind the request
3. **Show examples** - A sample input/output is worth a thousand words
4. **Define success** - What does "done" look like?
5. **Specify constraints** - Language, framework, time, resources
6. **Structure clearly** - Use bullet points and sections
7. **Review before sending** - Read it as if you're receiving it
