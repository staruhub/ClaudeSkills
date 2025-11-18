# Skill Activation Guide

## Overview

This guide helps identify when specific skills should be activated based on user request characteristics.

## Available Skills and Activation Criteria

### prompt-optimizer

**When to Activate**:
- User prompt contains vague language ("thing", "something", "stuff", "it")
- Request lacks technical specifications (no language/framework mentioned)
- Missing context or background information
- No success criteria or deliverables specified
- Overly broad or ambiguous requests
- Multiple possible interpretations
- User asks a question without providing necessary details

**Indicators**:
- ❌ "Fix the code" (what code? what's wrong?)
- ❌ "Make it better" (what? how?)
- ❌ "Build an app" (too broad)
- ❌ "Create a button" (missing specs)
- ❌ "Help with this" (with what?)

**Don't Activate When**:
- Prompt is already clear and specific
- User is just chatting or asking general questions
- Request is a simple command with obvious intent
- All necessary information is present

### react-component-generator

**When to Activate**:
- User requests creating a React component
- User mentions: "component", "React", "UI element"
- User asks for: buttons, forms, cards, lists, modals, etc.
- User wants to scaffold new React code

**Indicators**:
- ✅ "Create a login form component"
- ✅ "I need a button component"
- ✅ "Build a modal dialog"
- ✅ "Generate a card component"

**Don't Activate When**:
- User wants to debug existing components (not create new)
- Request is about React concepts, not component creation
- Different framework mentioned (Vue, Angular, etc.)

### ui-analyzer

**When to Activate**:
- User provides a UI screenshot or design mockup
- User mentions: "screenshot", "design", "mockup", "Figma"
- User asks to "implement this design" or "build this UI"
- User shares an image and asks for code
- User requests analyzing a UI layout

**Indicators**:
- ✅ "Analyze this UI screenshot"
- ✅ "Implement this design [image]"
- ✅ "Create components from this mockup"
- ✅ "What components are in this screenshot?"
- ✅ User uploads/references an image file

**Don't Activate When**:
- No visual design provided
- User describing UI verbally (use react-component-generator instead)
- Request is about analyzing existing code, not designs

## Request Type Classification

### Type 1: Code Implementation
**Characteristics**:
- Requests creating new code
- Mentions programming language
- Describes functionality to build

**Relevant Skills**:
- `react-component-generator` (if React-specific)
- `prompt-optimizer` (if request is vague)

**Example**:
```
"Create a user authentication system"
→ Check if specific enough
→ If vague, activate prompt-optimizer
→ Once clarified, proceed with implementation
```

### Type 2: Debugging/Fixing
**Characteristics**:
- Mentions bugs, errors, crashes
- Describes unexpected behavior
- References existing code

**Relevant Skills**:
- `prompt-optimizer` (if error details missing)

**Example**:
```
"The app crashes"
→ Too vague, activate prompt-optimizer
→ Need: where, when, error message, reproduction steps
```

### Type 3: Analysis/Review
**Characteristics**:
- Asks to analyze, review, or assess
- Requests feedback or suggestions
- Wants to understand something

**Relevant Skills**:
- `ui-analyzer` (if analyzing UI design)
- `prompt-optimizer` (if analysis goal unclear)

**Example**:
```
"Review this code"
→ Vague, what aspect? Performance? Security? Style?
→ Activate prompt-optimizer
```

### Type 4: Design Implementation
**Characteristics**:
- Mentions UI, design, screenshot, mockup
- Requests implementing visual design
- Shares image files

**Relevant Skills**:
- `ui-analyzer` (primary)
- `react-component-generator` (after analysis)
- `prompt-optimizer` (if design requirements unclear)

**Example**:
```
"Build this UI [screenshot]"
→ Activate ui-analyzer
→ UI analyzer may use react-component-generator for components
```

### Type 5: Refactoring/Optimization
**Characteristics**:
- Requests improving existing code
- Mentions performance, readability, maintainability
- Asks to restructure or reorganize

**Relevant Skills**:
- `prompt-optimizer` (if optimization goals unclear)

**Example**:
```
"Optimize this code"
→ Unclear what aspect to optimize
→ Activate prompt-optimizer to clarify goals
```

## Decision Tree

```
User Request Received
│
├─ Contains vague language? → YES → Consider prompt-optimizer
│  (thing, something, stuff, it)
│
├─ Missing critical info? → YES → Consider prompt-optimizer
│  (no specs, no context, no success criteria)
│
├─ Mentions UI screenshot/design? → YES → Activate ui-analyzer
│  (screenshot, mockup, design, image)
│
├─ Requests React component? → YES → Activate react-component-generator
│  (component, form, button, modal, card)
│
├─ Clear and complete? → YES → Proceed directly
│  (all info present, specific, actionable)
│
└─ Ambiguous or broad? → YES → Consider prompt-optimizer
   (multiple interpretations, too broad)
```

## Multi-Skill Activation Scenarios

### Scenario 1: Vague Component Request
```
User: "Make a form"
│
├─ Analysis: Vague (what fields? styling? validation?)
│
├─ Activate: prompt-optimizer FIRST
│  └─ Optimize to: "Create a React login form with email/password fields,
│                    validation, TypeScript, and Tailwind CSS"
│
└─ Then Activate: react-component-generator
   └─ Generate the specified component
```

### Scenario 2: UI Screenshot with Missing Details
```
User: "Build this [screenshot]"
│
├─ Analysis: Has design, but might lack technical specs
│
├─ Activate: ui-analyzer FIRST
│  ├─ Analyze the screenshot
│  ├─ Extract design tokens
│  └─ If implementation details unclear, mention prompt-optimizer
│
└─ Use: react-component-generator (as part of ui-analyzer workflow)
   └─ Generate components matching the design
```

### Scenario 3: Clear, Complete Request
```
User: "Create a React TypeScript Button component with primary/secondary
       variants, using Tailwind CSS, accepting onClick and children props"
│
├─ Analysis: Clear, specific, complete
│
├─ Skip: prompt-optimizer (not needed)
│
└─ Activate: react-component-generator DIRECTLY
   └─ All necessary information provided
```

## Activation Confidence Levels

### High Confidence (90%+) - Activate Immediately
- User prompt explicitly matches skill description
- Clear indicators present
- No ambiguity about intent

**Examples**:
- "Analyze this UI screenshot" → ui-analyzer
- "Create a React modal component with TypeScript" → react-component-generator
- "Fix the thing" → prompt-optimizer

### Medium Confidence (60-90%) - Consider Activation
- Request partially matches skill description
- Some indicators present
- Minor ambiguity

**Examples**:
- "I need a form" → Could benefit from prompt-optimizer first
- "Implement this design" (no image yet) → Wait for image, then ui-analyzer

### Low Confidence (<60%) - Don't Activate
- Request doesn't match skill purpose
- Different approach needed
- Would add no value

**Examples**:
- "What is React?" → General knowledge, no skill needed
- "Tell me a joke" → Conversational, no skill needed

## Prompt Quality Thresholds

### When to Activate prompt-optimizer

**Clarity Score < 60%**:
- Multiple vague terms (>2 instances of "thing", "something", etc.)
- Ambiguous pronouns without referents
- Multiple possible interpretations

**Specificity Score < 60%**:
- Missing technology stack for code requests
- No context or background provided
- Undefined scope or boundaries

**Completeness Score < 60%**:
- Missing required inputs or data
- No success criteria specified
- Edge cases not considered

**Calculation**:
```
If any score < 60% OR
   Overall average < 70% OR
   Critical information missing
   → Activate prompt-optimizer
```

### When NOT to Activate prompt-optimizer

**All scores > 80%** AND:
- Clear action verb
- Specific deliverables
- All context provided
- No ambiguity
→ Skip optimization, proceed directly

## Common Patterns

### Pattern: "Create X"
- X is specific (e.g., "login form") → Might be okay
- X is vague (e.g., "component") → Optimize first
- X includes specs → Proceed directly
- X lacks context → Optimize first

### Pattern: "Fix/Debug X"
- Includes error message → Might be okay
- No error details → Optimize first
- Has reproduction steps → Proceed directly
- Just "X is broken" → Optimize first

### Pattern: "Analyze/Review X"
- Specifies what to analyze → Might be okay
- No focus area mentioned → Optimize first
- Includes success criteria → Proceed directly
- Just "look at X" → Optimize first

### Pattern: "Build/Implement X"
- X references a design/screenshot → ui-analyzer
- X is well-defined → Proceed directly
- X is vague or broad → Optimize first
- X includes all requirements → Proceed directly

## Edge Cases

### Edge Case 1: Conversational Context
If the current request references previous conversation:
- Consider the full context, not just the latest message
- Previous messages may have provided necessary details
- Don't over-optimize if context is clear from history

### Edge Case 2: Follow-up Requests
If this is a follow-up to a previous task:
- Shared context from earlier may make brief requests acceptable
- "Now add validation" (following form creation) is specific enough
- Don't require re-stating all details each time

### Edge Case 3: Exploratory Questions
If user is exploring or brainstorming:
- They may not have all details yet
- Prompting for details might be premature
- Engage in dialogue rather than forcing optimization

## Tips for Effective Activation

1. **Read the full request carefully** - Don't trigger on keywords alone
2. **Consider the user's level** - Beginners may need more guidance
3. **Check for attachments** - Images, files may provide missing context
4. **Look for patterns** - Repeated issues suggest skill could help
5. **Balance helpfulness with efficiency** - Don't over-process simple requests
6. **Trust your judgment** - Skills are guides, not rules
7. **When in doubt, ask** - Clarifying question > wrong skill activation
