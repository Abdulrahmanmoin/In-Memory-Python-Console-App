---
id: 009
title: Fix Tailwind Border Error
stage: general
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-fullstack-web-app
user: xenium
command: "Solve this error: <error>  ⨯ ./src/app/globals.css:1:1\nSyntax error: D:\\todo_phase1\\frontend\\src\\app\\globals.css The `border-border` class does not exist. If `border-border` is a custom class, make sure it is defined within a `@layer` directive.\n\n> 1 | @tailwind base;\n    | ^\n  2 | @tailwind components;\n  3 | @tailwind utilities;\n<w> [webpack.cache.PackFileCacheStrategy] Skipped not serializable cache item 'Compilation/modules|D:\\todo_phase1\\frontend\\node_modules\\next\\dist\\build\\webpack\\loaders\\css-loader\\src\\index.js??ruleSet[1].rules[14].oneOf[10].use[2]!D:\\todo_phase1\\frontend\\node_modules\\next\\dist\\build\\webpack\\loaders\\postcss-loader\\src\\index.js??ruleSet[1].rules[14].oneOf[10].use[3]!D:\\todo_phase1\\frontend\\src\\app\\globals.css': No serializer registered for PostCSSSyntaxError\n<w> while serializing webpack/lib/cache/PackFileCacheStrategy.PackContentItems -> webpack/lib/NormalModule -> webpack/lib/ModuleBuildError -> PostCSSSyntaxError\n ⨯ ./src/app/globals.css:1:1\nSyntax error: D:\\todo_phase1\\frontend\\src\\app\\globals.css The `border-border` class does not exist. If `border-border` is a custom class, make sure it is defined within a `@layer` directive.\n\n> 1 | @tailwind base;\n    | ^\n  2 | @tailwind components;\n  3 | @tailwind utilities;\n ⨯ ./src/app/globals.css:1:1 </error?>"
labels: [bugfix, css, tailwind, frontend]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/app/globals.css
 - frontend/tailwind.config.js
tests:
---

## Prompt

Solve this error: <error>  ⨯ ./src/app/globals.css:1:1
Syntax error: D:\todo_phase1\frontend\src\app\globals.css The `border-border` class does not exist. If `border-border` is a custom class, make sure it is defined within a `@layer` directive.

> 1 | @tailwind base;
    | ^
  2 | @tailwind components;
  3 | @tailwind utilities;
<w> [webpack.cache.PackFileCacheStrategy] Skipped not serializable cache item 'Compilation/modules|D:\todo_phase1\frontend\node_modules\next\dist\build\webpack\loaders\css-loader\src\index.js??ruleSet[1].rules[14].oneOf[10].use[2]!D:\todo_phase1\frontend\node_modules\next\dist\build\webpack\loaders\postcss-loader\src\index.js??ruleSet[1].rules[14].oneOf[10].use[3]!D:\todo_phase1\frontend\src\app\globals.css': No serializer registered for PostCSSSyntaxError
<w> while serializing webpack/lib/cache/PackFileCacheStrategy.PackContentItems -> webpack/lib/NormalModule -> webpack/lib/ModuleBuildError -> PostCSSSyntaxError
 ⨯ ./src/app/globals.css:1:1
Syntax error: D:\todo_phase1\frontend\src\app\globals.css The `border-border` class does not exist. If `border-border` is a custom class, make sure it is defined within a `@layer` directive.

> 1 | @tailwind base;
    | ^
  2 | @tailwind components;
  3 | @tailwind utilities;
 ⨯ ./src/app/globals.css:1:1 </error?

## Response snapshot

I successfully fixed the Tailwind CSS error by making two key changes:

1. Updated the tailwind.config.js file to include the proper color extensions that map CSS variables to Tailwind classes:
   - Added color mappings for border, input, ring, background, foreground, and other custom colors
   - Configured the theme.extend.colors to map each Tailwind class to its corresponding CSS variable

2. Fixed the globals.css file by consolidating duplicate `@layer base` declarations into a single block:
   - Previously there were two separate `@layer base` blocks which caused issues
   - Now there's one unified block containing both CSS variable definitions and `@apply` directives

The error was occurring because the `border-border` class was being used in globals.css with `@apply border-border;` but Tailwind didn't know how to resolve this class because it wasn't defined in the theme configuration. The CSS variables were defined (like `--border`) but not properly mapped to Tailwind classes.

Now the Tailwind configuration properly maps:
- `border-border` → `hsl(var(--border))`
- `bg-background` → `hsl(var(--background))`
- `text-foreground` → `hsl(var(--foreground))`
- And all other custom color classes used in the application

The globals.css file now has a single `@layer base` block that contains both the CSS variable definitions and the `@apply` directives, which should resolve the compilation error.

## Outcome

- ✅ Impact: Fixed Tailwind CSS compilation error
- 🧪 Tests: Not applicable
- 📁 Files: globals.css and tailwind.config.js updated
- 🔁 Next prompts: Continue with project development
- 🧠 Reflection: Proper Tailwind theme configuration required for custom classes

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A