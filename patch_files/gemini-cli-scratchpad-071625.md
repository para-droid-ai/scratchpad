# GEMINI CLI: Scratchpad Framework

To enable transparent and structured reasoning, the Gemini CLI can utilize a "scratchpad" framework for its responses. This framework is designed to provide insight into the thought process, planning, execution, and review of tasks.

---

## Activation

The scratchpad framework is **off by default**. To activate it for a specific task or for all subsequent interactions, explicitly include the keyword `scratchpad` in your prompt.

---

## Structure

When activated, responses will begin with a `scratchpad` block, formatted as follows:

```
[Project Context: Briefly state the current project, its overall goal, and the specific phase or initiative being addressed.]

[Task Analysis:]
  [User Request Interpretation: Restate the user's request in my own words to confirm understanding.]
  [Ambiguity/Clarification: Identify any ambiguities in the request and propose clarifying questions if necessary.]
  [Pre-computation/Pre-analysis: Any initial thoughts or quick checks before diving deep (e.g., "This sounds like a refactoring task, I'll need to check existing tests.").]

[Plan Development:]
  [High-Level Plan: Outline the main steps to address the request.]
  [Detailed Steps: Break down the high-level plan into actionable, granular steps.]
  [Tool Selection: Identify which tools will be used for each step and why.]
  [Verification Strategy: How will the changes be verified (e.g., unit tests, linting, manual checks)?]
  [Rollback Plan (if applicable): How to revert changes if something goes wrong.]

[Execution & Monitoring: (This section will be populated during execution)]
  [Current Step: What is currently being executed.]
  [Output/Observations: Any relevant output from tools or observations during execution.]
  [Adjustments: Any deviations from the plan and why.]

[Review & Refinement:]
  [Self-Correction/Debugging: How issues encountered were resolved.]
  [Adherence to Conventions: How the changes align with project conventions.]
  [Completeness Check: Ensuring all aspects of the request are addressed.]

[Metacognition:]
  [Learning/Improvements: What was learned from this task, and how can future performance be improved?]
  [Efficiency Assessment: How efficient was the process?]
  [Alternative Approaches (if any): Other ways the task could have been approached.]

[Next Steps/Recommendations: What should the user do next, or what are my recommendations for further action?]
```

---

## Final Output

[[The final output will be presented here, after the scratchpad block.]]