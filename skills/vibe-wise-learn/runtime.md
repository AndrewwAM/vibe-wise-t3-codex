# Codex and T3 Code

Respect the active collaboration mode and the tools actually listed for the turn.
This skill does not change the runtime's Plan/Default mode or grant tool permissions.

In **Plan**, inspect and discuss without writing application code or learning notes.
Keep onboarding answers and pending decisions in the conversation. When the learner
is ready to implement, explain that T3 Code must be switched to Default. Do not
try to switch modes by writing instructions or assume a chat reply changed modes.
In **Default**, the explicit learning request establishes the teaching workflow.
Write notes and approved application changes within the user's authorized scope.

Use available file-reading, search, and editing tools. With shell tools, use
`rg` for discovery/search and bounded reads for complete relevant sections.
Do not prescribe Claude's Read, Glob, Bash, or AskUserQuestion tools.
Quote actual absolute paths; placeholders in examples must be substituted.

For onboarding preferences or design clarification, use a native question tool
only when available and permitted in the current mode. Prefer
`request_user_input_async` when available; otherwise use `request_user_input`
only if that tool's rules allow it. Ask one focused question at a time.
An asynchronous question does not authorize dependent work: end the turn and
wait when the answer is needed. Never treat a preselected option or silence as an answer.

For open-ended reasoning, implementation authorization, and learning resets,
ask a concise question in the final response and wait for the learner's reply.
Do not use a planning-only preference tool for approval. If no selector is
available, use ordinary prose, without a numbered imitation of a native picker.
Existing explicit authorization for the presented scope needs no second gate.

Read-only exploration may continue while a question is pending. Save evidence
when permitted, but do not supply the learner's design or write application code
while their reasoning or required authorization is still pending.
