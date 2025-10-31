# Code Review Prompt

English | [简体中文](./code-review.zh-CN.md)

## Description
A comprehensive prompt for conducting thorough code reviews with Claude AI.

## Category
- Primary: Coding
- Tags: code-review, quality-assurance, best-practices

## Prompt Template

```
Please review the following code and provide feedback on:

1. **Code Quality**
   - Readability and maintainability
   - Naming conventions
   - Code organization

2. **Best Practices**
   - Language-specific best practices
   - Design patterns usage
   - SOLID principles adherence

3. **Potential Issues**
   - Bugs or logic errors
   - Security vulnerabilities
   - Performance bottlenecks

4. **Improvements**
   - Refactoring suggestions
   - Optimization opportunities
   - Alternative approaches

Code to review:
```[language]
[Your code here]
```

Please provide:
- Specific line-by-line feedback where applicable
- Priority levels (Critical, High, Medium, Low)
- Code examples for suggested improvements
```

## Example Usage

```
Please review the following code and provide feedback on:
[... full prompt ...]

Code to review:
```python
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price'] * item['quantity']
    return total
```
```

## Expected Output

Claude will provide structured feedback including:
- Code quality assessment
- Specific issues found
- Improvement suggestions with examples
- Priority ratings for each issue

## Tips

- Specify the programming language for better context
- Include relevant context about the codebase
- Mention specific concerns if you have any
- Ask for examples of improved code

## Variations

### Quick Review
```
Quick code review focusing on critical issues only:
[code]
```

### Security-Focused Review
```
Security-focused code review. Check for:
- SQL injection vulnerabilities
- XSS vulnerabilities
- Authentication/authorization issues
- Data validation problems

[code]
```

### Performance Review
```
Performance-focused code review. Analyze:
- Time complexity
- Space complexity
- Optimization opportunities
- Scalability concerns

[code]
```

