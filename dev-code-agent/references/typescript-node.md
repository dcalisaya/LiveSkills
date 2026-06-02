# TypeScript / Node.js Reference — Live Developer Stack

## Runtime & Configuration

- Node.js **20 LTS** (or 22 LTS). Use `engines` field in `package.json`.
- TypeScript **5.4+**. Strict mode: `"strict": true` in `tsconfig.json`.
- Module system: ESM (`"type": "module"` in package.json, `.js` extensions in imports).
- Package manager: `npm` with exact versions pinned (`npm install --save-exact`).
- Local inference: Ollama on Mac Studio M4 Max — connect via `http://localhost:11434`.

## tsconfig Baseline

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "outDir": "dist",
    "rootDir": "src",
    "declaration": true,
    "sourceMap": true
  },
  "include": ["src"]
}
```

## Preferred Libraries

| Purpose | Library |
|---|---|
| HTTP API | Fastify 4 |
| Validation | Zod |
| HTTP client | native `fetch` (Node 20+) |
| DB (PostgreSQL) | `postgres` (postgres.js) or Drizzle ORM |
| Testing | Vitest |
| CLI tools | `commander` or `@clack/prompts` |
| LLM client | `@anthropic-ai/sdk` |
| Environment | `dotenv` + `zod` for typed config |

## Code Patterns

### Fastify API Route

```typescript
import Fastify from 'fastify'
import { z } from 'zod'

const app = Fastify({ logger: true })

const CreateProjectBody = z.object({
  name: z.string().min(1).max(100),
  clientId: z.number().int().positive(),
})

app.post('/projects', async (request, reply) => {
  const body = CreateProjectBody.safeParse(request.body)
  if (!body.success) {
    return reply.status(400).send({ errors: body.error.issues })
  }
  const project = await projectService.create(body.data)
  return reply.status(201).send(project)
})

export { app }
```

### Typed Environment Config

```typescript
// src/config.ts
import { z } from 'zod'
import 'dotenv/config'

const Config = z.object({
  DATABASE_URL: z.string().url(),
  ANTHROPIC_API_KEY: z.string().min(1),
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
})

export const config = Config.parse(process.env)
```

### LLM Agent Step (Anthropic SDK)

```typescript
import Anthropic from '@anthropic-ai/sdk'
import { config } from './config.js'

const client = new Anthropic({ apiKey: config.ANTHROPIC_API_KEY })

interface AgentStepInput {
  systemPrompt: string
  userMessage: string
  maxTokens?: number
}

interface AgentStepResult {
  text: string
  inputTokens: number
  outputTokens: number
}

export async function runAgentStep(input: AgentStepInput): Promise<AgentStepResult> {
  const response = await client.messages.create({
    model: 'claude-opus-4-6',
    max_tokens: input.maxTokens ?? 2048,
    system: input.systemPrompt,
    messages: [{ role: 'user', content: input.userMessage }],
  })

  const textBlock = response.content.find(b => b.type === 'text')
  if (!textBlock || textBlock.type !== 'text') {
    throw new Error('No text block in response')
  }

  return {
    text: textBlock.text,
    inputTokens: response.usage.input_tokens,
    outputTokens: response.usage.output_tokens,
  }
}
```

### Sequential Agent Pipeline

```typescript
type PipelineStep<TIn, TOut> = (input: TIn) => Promise<TOut>

async function runPipeline<T>(
  initial: T,
  steps: PipelineStep<unknown, unknown>[]
): Promise<unknown> {
  let current: unknown = initial
  for (const step of steps) {
    current = await step(current)
  }
  return current
}
```

## Project Layout

```
project/
├── package.json
├── tsconfig.json
├── .env.example
├── src/
│   ├── index.ts         # Entry point
│   ├── config.ts        # Typed env config
│   ├── app.ts           # Fastify app factory
│   ├── routes/          # Route handlers
│   ├── services/        # Business logic
│   ├── agents/          # Agent step functions
│   └── db/              # Database client + queries
└── tests/
    └── *.test.ts
```

## Testing with Vitest

```typescript
// tests/projects.test.ts
import { describe, it, expect, vi } from 'vitest'
import { projectService } from '../src/services/projectService.js'

describe('projectService', () => {
  it('creates a project with valid data', async () => {
    const project = await projectService.create({ name: 'Test', clientId: 1 })
    expect(project.id).toBeDefined()
    expect(project.name).toBe('Test')
  })
})
```

## React / Vite (Frontend — LiveApp)

When the task is React + Vite + TailwindCSS (LiveApp frontend):
- Component files: `PascalCase.tsx`. Hooks: `useCamelCase.ts`.
- State: React Query for server state; Zustand for global client state.
- Styling: TailwindCSS utility classes. Use `cn()` (clsx + tailwind-merge) for conditional classes.
- Routing: React Router v6 (data router pattern).
- Forms: React Hook Form + Zod resolver.
- Never use `any`. Prefer `unknown` and narrow types explicitly.
