---
name: request-analyzer
description: Proactively analyze user requests at the start of conversations to determine task type, assess prompt quality, and intelligently recommend which skills to activate. Should activate for ALL user requests to ensure optimal workflow. Evaluates clarity, specificity, and completeness to suggest prompt-optimizer when needed. Identifies UI design tasks for ui-analyzer and component requests for react-component-generator. Acts as intelligent skill coordinator.
allowed-tools: Read, Glob, Grep, Skill
---

# Request Analyzer

This skill proactively analyzes user requests to determine the task type, assess prompt quality, and intelligently recommend which other skills should be activated to best serve the user's needs.

## Purpose

Act as an intelligent coordinator that:
1. Analyzes every user request systematically
2. Assesses prompt quality (clarity, specificity, completeness)
3. Identifies the task type and appropriate workflow
4. Recommends activating specific skills when beneficial
5. Ensures users get the best possible assistance

## When to Use This Skill

**This skill should activate for EVERY user request** at the start of conversations to ensure optimal workflow orchestration.

Specifically activate when:
- A new conversation begins
- User submits a new request or question
- User asks for help with a task
- Any coding, design, or technical request is made
- User's intent needs clarification

## Core Analysis Process

### Step 1: Quick Assessment

Immediately evaluate the request on three dimensions:

**Clarity (0-100%)**:
- Is the request unambiguous?
- Are terms clearly defined?
- Is there only one reasonable interpretation?

**Specificity (0-100%)**:
- Is sufficient context provided?
- Are technical requirements specified?
- Is the scope well-defined?

**Completeness (0-100%)**:
- Is all necessary information present?
- Are success criteria defined?
- Are constraints mentioned?

### Step 2: Task Type Identification

Classify the request into one of these categories:

1. **Code Implementation** - Creating new code
2. **Debugging/Fixing** - Resolving bugs or errors
3. **Analysis/Review** - Examining code or systems
4. **Design Implementation** - Building UI from designs
5. **Refactoring** - Improving existing code
6. **Explanation/Learning** - Understanding concepts
7. **General Question** - Non-technical queries

Reference `references/skill-activation-guide.md` for detailed classification criteria.

### Step 3: Skill Recommendation

Based on assessment and task type, determine which skills would be beneficial:

**Consider prompt-optimizer if**:
- Clarity score < 60%
- Specificity score < 60%
- Completeness score < 60%
- Overall quality < 70%
- Critical information missing
- Multiple interpretations possible

**Consider ui-analyzer if**:
- User mentions: screenshot, design, mockup, Figma, image
- User provides or references an image file
- Request includes "implement this design"
- Task involves analyzing UI layout

**Consider react-component-generator if**:
- User requests creating React component
- Mentions: component, form, button, modal, card, list
- After ui-analyzer identifies components to build
- Clear component requirements are present

### Step 4: Decision and Action

Make one of these decisions:

**Option A: Recommend Optimization**
If prompt quality is low, explicitly suggest using prompt-optimizer:
```
"I notice your request could benefit from more clarity. Let me activate the
prompt-optimizer skill to help structure a more specific request."
```

**Option B: Recommend Specific Skill**
If request is clear but matches a skill's domain:
```
"This looks like a UI design implementation task. I'll use the ui-analyzer
skill to systematically analyze the design and generate the code."
```

**Option C: Proceed Directly**
If request is clear, complete, and doesn't need specialized skills:
```
"Your request is clear. I'll proceed with [task description]."
```

**Option D: Ask for Clarification**
If critical information is missing and cannot be assumed:
```
"To help you effectively, I need to know: [specific questions]"
```

## Analysis Workflow

### For Every Request

1. **Read the request carefully**
2. **Score on three dimensions** (Clarity, Specificity, Completeness)
3. **Identify task type** using the classification system
4. **Check skill activation criteria** from the reference guide
5. **Make recommendation** (optimize, activate skill, proceed, or clarify)
6. **Take action** based on the decision

### Detailed Steps

**Step 1: Initial Read**
- Understand user intent
- Note any attachments or references
- Consider conversational context

**Step 2: Quality Scoring**

Clarity Check:
- [ ] No vague language ("thing", "something", "stuff")?
- [ ] All terms defined?
- [ ] Single clear interpretation?
- [ ] Action verb present?

Specificity Check:
- [ ] Context provided?
- [ ] Technical specs mentioned (for code)?
- [ ] Scope defined?
- [ ] Examples given (if helpful)?

Completeness Check:
- [ ] All inputs provided?
- [ ] Success criteria stated?
- [ ] Constraints mentioned?
- [ ] Edge cases considered?

**Step 3: Task Classification**

Match against patterns in `references/skill-activation-guide.md`:
- Code Implementation patterns
- Debugging patterns
- Analysis patterns
- Design Implementation patterns
- Refactoring patterns

**Step 4: Skill Matching**

For each available skill, check if activation criteria are met:

```
prompt-optimizer:
- Quality score < 70%? → Consider
- Missing critical info? → Consider
- Vague language present? → Consider
- Multiple interpretations? → Consider

ui-analyzer:
- Screenshot/design mentioned? → Activate
- Image provided? → Activate
- "Implement design" request? → Activate

react-component-generator:
- React component requested? → Consider
- After prompt optimization? → Consider
- Clear component spec? → Activate
```

**Step 5: Recommendation**

Based on analysis, formulate recommendation:
- Which skill(s) to activate
- Why they're beneficial
- What to expect from them

**Step 6: Execution**

Either:
- Explicitly note the skill activation (for transparency)
- Seamlessly integrate skill usage
- Ask for user confirmation if uncertain

## Output Formats

### Format 1: Optimization Recommended (Low Quality Prompt)

```markdown
## Request Analysis

I've analyzed your request and noticed it could benefit from more specificity.

**Current Request**: [User's request]

**Observations**:
- Missing: [what's missing]
- Unclear: [what's ambiguous]
- Would help: [what would improve it]

**Recommendation**: Let me use the prompt-optimizer skill to help structure
a clearer, more actionable request.

[Then activate prompt-optimizer]
```

### Format 2: Skill Recommended (Good Prompt, Specific Domain)

```markdown
## Request Analysis

Your request is clear and matches our ui-analyzer skill's capabilities.

**Task Type**: Design Implementation
**Recommended Approach**:
1. Use ui-analyzer to examine the screenshot
2. Extract design tokens and components
3. Generate React code with Tailwind CSS

Proceeding with UI analysis...

[Then activate ui-analyzer]
```

### Format 3: Direct Execution (High Quality, No Special Skill Needed)

```markdown
## Request Analysis

Your request is clear and complete. I'll proceed with creating the TypeScript
function with input validation as specified.

[Proceed with implementation]
```

### Format 4: Clarification Needed

```markdown
## Request Analysis

To help you effectively, I need some additional information:

1. [Question 1]
2. [Question 2]
3. [Question 3]

Once I have these details, I can [what you'll do].
```

## Integration with Other Skills

### With prompt-optimizer

**When to Delegate**:
- Quality scores indicate issues
- Request is vague or incomplete
- Multiple interpretations exist
- Critical information missing

**How**:
1. Identify the quality issues
2. Explain why optimization would help
3. Mention activating prompt-optimizer
4. Let prompt-optimizer take over

**Example Flow**:
```
User: "Make a form"
↓
request-analyzer: Detects low specificity
↓
request-analyzer: "This request needs more details. Activating prompt-optimizer..."
↓
prompt-optimizer: Analyzes and provides optimized version
↓
User: Confirms optimized version
↓
react-component-generator: Creates the well-specified form
```

### With ui-analyzer

**When to Delegate**:
- Screenshot or design mentioned
- Image file provided
- Design implementation requested

**How**:
1. Confirm it's a design implementation task
2. Verify image is available or referenced
3. Explain ui-analyzer will handle it
4. Let ui-analyzer take over

**Example Flow**:
```
User: "Build this UI [screenshot attached]"
↓
request-analyzer: Detects design implementation task
↓
request-analyzer: "I'll use ui-analyzer to examine your design..."
↓
ui-analyzer: Analyzes screenshot and generates code
```

### With react-component-generator

**When to Delegate**:
- React component requested
- Specifications are clear
- No design screenshot (verbal description)

**How**:
1. Confirm component requirements are clear
2. If not clear, use prompt-optimizer first
3. Once clear, mention using react-component-generator
4. Let it handle component creation

**Example Flow**:
```
User: "Create a React login form with email/password, validation, TypeScript"
↓
request-analyzer: Detects high-quality component request
↓
request-analyzer: "Clear component spec. Using react-component-generator..."
↓
react-component-generator: Creates the component
```

## Decision Matrix

| Prompt Quality | Has Screenshot | Task Type | Action |
|---------------|----------------|-----------|--------|
| Low (<70%) | No | Any | → prompt-optimizer |
| Low (<70%) | Yes | Design | → prompt-optimizer first, then ui-analyzer |
| High (>80%) | Yes | Design | → ui-analyzer |
| High (>80%) | No | Component | → react-component-generator |
| High (>80%) | No | General Code | → Proceed directly |
| Medium (70-80%) | No | Any | → Ask clarifying questions OR proceed |

## Special Considerations

### Conversational Context

If this is a follow-up in an ongoing conversation:
- Previous messages may provide missing context
- Don't over-analyze brief follow-ups
- "Now add validation" is fine after "Create a form"
- Consider the full conversation history

### User Experience

Balance thoroughness with efficiency:
- Don't over-process simple, clear requests
- Avoid creating friction for experienced users
- Be helpful but not pedantic
- Transparent about why skills are beneficial

### Confidence Levels

**High Confidence (>90%)** - Act decisively:
- Prompt clearly matches skill domain
- Quality issues are obvious
- Recommendation is unambiguous

**Medium Confidence (60-90%)** - Suggest and explain:
- Partial match to skill domain
- Some quality concerns
- Explain the benefit of using a skill

**Low Confidence (<60%)** - Ask or proceed cautiously:
- Unclear match
- No obvious quality issues
- Might not need special skills

## Reference Usage

Consult `references/skill-activation-guide.md` for:

- **Available Skills** - Full list with activation criteria
- **Request Type Classification** - Detailed patterns
- **Decision Tree** - Visual workflow guide
- **Multi-Skill Scenarios** - Complex activation patterns
- **Activation Confidence Levels** - When to activate
- **Common Patterns** - Recognize typical requests
- **Edge Cases** - Handle special situations

## Examples

### Example 1: Vague Request

```
User: "Fix my code"

Analysis:
- Clarity: 20% (what code? what's wrong?)
- Specificity: 10% (no file, no error, no context)
- Completeness: 15% (no reproduction steps, no expected behavior)
- Overall: 15% → Very Low

Decision: Activate prompt-optimizer

Output:
"I notice your request needs more details to be actionable. Let me help
structure it using the prompt-optimizer skill.

Missing information:
- Which file or code section?
- What's the current behavior?
- What error messages appear?
- What should happen instead?

[Activating prompt-optimizer...]"
```

### Example 2: UI Design Request

```
User: "Implement this login page design [screenshot]"

Analysis:
- Clarity: 85% (clear intent)
- Specificity: 80% (has design, mentions login page)
- Completeness: 75% (might need tech stack clarification)
- Task Type: Design Implementation
- Has Screenshot: Yes

Decision: Activate ui-analyzer (might clarify tech stack within workflow)

Output:
"I'll analyze your login page design and generate the React components.

Using the ui-analyzer skill to:
1. Examine the layout and components
2. Extract design tokens (colors, spacing, typography)
3. Generate React + TypeScript + Tailwind code

[Activating ui-analyzer...]"
```

### Example 3: Clear Component Request

```
User: "Create a React Button component with TypeScript, supporting primary/
secondary/danger variants, sm/md/lg sizes, and Tailwind CSS styling"

Analysis:
- Clarity: 95% (very clear)
- Specificity: 95% (all tech specs present)
- Completeness: 90% (comprehensive requirements)
- Task Type: Code Implementation (React component)
- Overall: 93% → Excellent

Decision: Activate react-component-generator directly

Output:
"Excellent! Your component requirements are clear and complete. I'll use the
react-component-generator skill to create this button component.

[Activating react-component-generator...]"
```

### Example 4: General Question

```
User: "What's the difference between useState and useReducer in React?"

Analysis:
- Clarity: 100% (perfectly clear)
- Task Type: Explanation/Learning
- No coding task
- No design implementation

Decision: Proceed directly (no special skill needed)

Output:
"Great question! Let me explain the differences between useState and useReducer..."

[Provide explanation directly - no skill activation needed]
```

## Best Practices

1. **Be proactive but not intrusive** - Help without creating friction
2. **Explain the value** - Tell users why a skill will help
3. **Stay transparent** - Mention which skills you're using and why
4. **Respect user time** - Don't over-analyze trivial requests
5. **Learn from context** - Consider conversation history
6. **Balance automation with judgment** - Skills are tools, not rules
7. **Prioritize user success** - The goal is better outcomes, not perfect process

## Important Notes

- This skill is a coordinator, not a blocker
- High-quality prompts should flow smoothly without intervention
- Skills should enhance, not hinder, the user experience
- When in doubt, ask the user rather than making assumptions
- Transparency builds trust - explain your reasoning
- The ultimate goal is helping users succeed with their tasks
