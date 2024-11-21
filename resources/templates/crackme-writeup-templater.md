<%*
// Templater template for crackme writeups

const title = await tp.system.prompt("Crackme title (e.g., 'Simple KeyGen')");
const difficulty = await tp.system.suggester(["Easy", "Medium", "Hard"], ["Easy", "Medium", "Hard"], false, "Select difficulty");
const timeSpent = await tp.system.prompt("Time spent (e.g., '~2 hours')");
const status = await tp.system.suggester(["SOLVED", "WIP", "STUCK"], ["SOLVED", "WIP", "STUCK"], false, "Status");

const filename = await tp.system.prompt("Binary filename (e.g., 'crack', 'keygen.exe')");
const fileType = await tp.system.prompt("File type (e.g., 'ELF 64-bit LSB pie executable')");
const compiler = await tp.system.prompt("Compiler (e.g., 'GCC 15.2.1', 'MSVC')");
const protection = await tp.system.prompt("Protection mechanism (e.g., 'SHA256 hash comparison')");
const solution = await tp.system.prompt("Solution (password/key/flag)");

const crackmeUrl = await tp.system.prompt("Crackme source URL (leave empty if none)");
%>
# Crackme Solution: <% title %>

**Date:** <% tp.date.now("YYYY-MM-DD") %>
**Difficulty:** <% difficulty %>
**Time:** <% timeSpent %>
**Status:** <% status %>
<%* if (crackmeUrl && crackmeUrl.trim() !== "") { %>
**Source:** [crackmes.one](<% crackmeUrl %>)
<%* } %>

---

## File Info

| Property | Value |
| --- | --- |
| Filename | <% filename %> |
| Type | <% fileType %> |
| Compiler | <% compiler %> |
| Protection | <% protection %> |
| Solution | <% solution %> |

---

## Reconnaissance

```bash
file <% filename %>
# output:

strings <% filename %> | grep -i "pass\|key"
# output:

objdump -t <% filename %> | grep -i "debug"
# output:
```

[Your analysis here]

---

## Static Analysis

### Decompiled code

```c
// Paste decompiled code here
```

Algorithm:
1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## Attack

### Attempt 1: [Method name]

```bash
# Commands used
```

[Description and results]

### Attempt 2: [Method name]

```bash
# Commands used
```

Found: **<% solution %>**

---

## Solution

Password: **<% solution %>**

Verification:
```bash
echo "<% solution %>" | ./<% filename %>
# output:
```

---

## Timeline

```
00:00 - Started
00:XX - [milestone]
...

Total: <% timeSpent %>
```

---

## Notes

[Your notes and insights about this challenge]

---

## Screenshots

[Add screenshots if needed]
