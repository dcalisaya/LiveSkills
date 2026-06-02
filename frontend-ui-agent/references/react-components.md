# React Components Reference — Live Developer Stack (LiveApp)

## Stack & Configuration

- **React 18+** with Vite 5 as build tool.
- **TypeScript** strict mode — never use `any`.
- **Styling**: TailwindCSS 3 + `cn()` utility (clsx + tailwind-merge).
- **State**: React Query (TanStack Query v5) for server state, Zustand for global client state.
- **Routing**: React Router v6 with data router pattern.
- **Forms**: React Hook Form + Zod resolver.
- **UI primitives**: shadcn/ui (Radix-based, copy-pasted, fully owned).

---

## Project Layout

```
src/
├── app/
│   ├── routes/              # Route components (pages)
│   ├── layouts/             # Layout wrappers (sidebar, auth, etc.)
│   └── router.tsx           # Route definitions
├── components/
│   ├── ui/                  # shadcn/ui primitives (Button, Card, Dialog, etc.)
│   ├── forms/               # Form components (bound to RHF + Zod)
│   ├── data/                # Data display (tables, stat cards, charts)
│   └── shared/              # Cross-feature components (Logo, UserMenu, etc.)
├── features/
│   ├── projects/            # Feature module: components, hooks, types
│   ├── deliverables/        # Feature module
│   └── clients/             # Feature module
├── hooks/                   # Shared custom hooks
├── lib/
│   ├── api.ts               # API client (fetch wrapper)
│   ├── cn.ts                # Class name utility
│   └── constants.ts         # App-wide constants
├── stores/                  # Zustand stores
├── types/                   # Global TypeScript types
└── main.tsx                 # App entry point
```

---

## Component Conventions

### File Naming

- Components: `PascalCase.tsx` (e.g., `ProjectCard.tsx`, `DeliverableTable.tsx`)
- Hooks: `useCamelCase.ts` (e.g., `useProjects.ts`, `useAuth.ts`)
- Types: co-located in `types.ts` within the feature module, or `src/types/` for shared types.
- Tests: `ComponentName.test.tsx` next to the component.

### Component Structure

```tsx
// src/features/deliverables/DeliverableCard.tsx
import { cn } from '@/lib/cn'
import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import type { Deliverable } from './types'

interface DeliverableCardProps {
  deliverable: Deliverable
  isSelected?: boolean
  onSelect?: (id: string) => void
}

export function DeliverableCard({
  deliverable,
  isSelected = false,
  onSelect,
}: DeliverableCardProps) {
  return (
    <Card
      className={cn(
        'cursor-pointer transition-all duration-150',
        isSelected && 'ring-2 ring-accent border-accent'
      )}
      onClick={() => onSelect?.(deliverable.id)}
    >
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-primary">
          {deliverable.title}
        </h3>
        <Badge variant={deliverable.status}>
          {deliverable.status}
        </Badge>
      </div>
      {deliverable.dueAt && (
        <p className="mt-1 text-xs text-muted-foreground">
          Due: {new Date(deliverable.dueAt).toLocaleDateString()}
        </p>
      )}
    </Card>
  )
}
```

### Rules

1. **Named exports only** — no `export default`. Easier to refactor and grep.
2. **Props interface above the component** — always typed, never inline.
3. **Destructure props** in the function signature.
4. **No business logic in components** — delegate to hooks or services.
5. **Use `cn()`** for conditional classes — never ternary string concatenation.

---

## cn() Utility

```typescript
// src/lib/cn.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs))
}
```

---

## Data Fetching — React Query

### Query Hook Pattern

```typescript
// src/features/projects/useProjects.ts
import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import type { Project } from './types'

export const projectKeys = {
  all:    ['projects'] as const,
  list:   (filters: Record<string, unknown>) => [...projectKeys.all, 'list', filters] as const,
  detail: (id: string) => [...projectKeys.all, 'detail', id] as const,
}

export function useProjects(filters: { status?: string; clientId?: string } = {}) {
  return useQuery({
    queryKey: projectKeys.list(filters),
    queryFn: () => api.get<Project[]>('/projects', { params: filters }),
    staleTime: 30_000, // 30 seconds
  })
}

export function useProject(id: string) {
  return useQuery({
    queryKey: projectKeys.detail(id),
    queryFn: () => api.get<Project>(`/projects/${id}`),
    enabled: !!id,
  })
}
```

### Mutation Hook Pattern

```typescript
// src/features/deliverables/useCreateDeliverable.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { projectKeys } from '../projects/useProjects'
import type { CreateDeliverableInput, Deliverable } from './types'

export function useCreateDeliverable() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: CreateDeliverableInput) =>
      api.post<Deliverable>('/deliverables', data),
    onSuccess: (_data, variables) => {
      // Invalidate related queries
      queryClient.invalidateQueries({
        queryKey: projectKeys.detail(variables.projectId),
      })
    },
  })
}
```

---

## Forms — React Hook Form + Zod

```tsx
// src/features/deliverables/CreateDeliverableForm.tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { useCreateDeliverable } from './useCreateDeliverable'

const schema = z.object({
  title: z.string().min(1, 'Title is required').max(255),
  projectId: z.string().uuid(),
  dueAt: z.string().datetime().optional(),
})

type FormData = z.infer<typeof schema>

interface CreateDeliverableFormProps {
  projectId: string
  onSuccess?: () => void
}

export function CreateDeliverableForm({
  projectId,
  onSuccess,
}: CreateDeliverableFormProps) {
  const mutation = useCreateDeliverable()

  const form = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: { title: '', projectId },
  })

  const handleSubmit = form.handleSubmit(async (data) => {
    await mutation.mutateAsync(data)
    form.reset()
    onSuccess?.()
  })

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="title" className="text-sm font-medium text-primary">
          Title
        </label>
        <Input
          id="title"
          {...form.register('title')}
          placeholder="e.g., Brand Kit v2"
          className="mt-1"
        />
        {form.formState.errors.title && (
          <p className="mt-1 text-xs text-destructive">
            {form.formState.errors.title.message}
          </p>
        )}
      </div>

      <Button
        type="submit"
        disabled={mutation.isPending}
        className="w-full"
      >
        {mutation.isPending ? 'Creating...' : 'Create Deliverable'}
      </Button>
    </form>
  )
}
```

---

## State Management — Zustand

```typescript
// src/stores/uiStore.ts
import { create } from 'zustand'

interface UIState {
  sidebarOpen: boolean
  toggleSidebar: () => void

  activeModal: string | null
  openModal: (id: string) => void
  closeModal: () => void
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),

  activeModal: null,
  openModal: (id) => set({ activeModal: id }),
  closeModal: () => set({ activeModal: null }),
}))
```

### When to Use What

| State Type | Solution | Examples |
|---|---|---|
| Server data (fetched) | React Query | Projects list, user profile, deliverables |
| Global UI state | Zustand | Sidebar open/close, active modal, theme |
| Local UI state | `useState` | Form field, dropdown open, hover |
| URL-driven state | React Router (searchParams) | Filters, pagination, sort |
| Complex form state | React Hook Form | Multi-step forms, validation |

---

## Routing — React Router v6

```tsx
// src/app/router.tsx
import { createBrowserRouter } from 'react-router-dom'
import { AppLayout } from './layouts/AppLayout'
import { DashboardPage } from './routes/DashboardPage'
import { ProjectsPage } from './routes/ProjectsPage'
import { ProjectDetailPage } from './routes/ProjectDetailPage'
import { NotFoundPage } from './routes/NotFoundPage'

export const router = createBrowserRouter([
  {
    element: <AppLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'projects', element: <ProjectsPage /> },
      { path: 'projects/:id', element: <ProjectDetailPage /> },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
])
```

---

## API Client

```typescript
// src/lib/api.ts
import { config } from './config'

class ApiError extends Error {
  constructor(
    public status: number,
    public data: unknown,
    message: string,
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function request<T>(
  path: string,
  options: RequestInit & { params?: Record<string, string> } = {},
): Promise<T> {
  const { params, ...fetchOptions } = options
  const url = new URL(path, config.API_BASE_URL)

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value) url.searchParams.set(key, value)
    })
  }

  const response = await fetch(url.toString(), {
    ...fetchOptions,
    headers: {
      'Content-Type': 'application/json',
      ...fetchOptions.headers,
    },
    credentials: 'include',
  })

  if (!response.ok) {
    const data = await response.json().catch(() => null)
    throw new ApiError(
      response.status,
      data,
      `API ${response.status}: ${response.statusText}`,
    )
  }

  return response.json() as Promise<T>
}

export const api = {
  get: <T>(path: string, opts?: { params?: Record<string, string> }) =>
    request<T>(path, { method: 'GET', ...opts }),

  post: <T>(path: string, body: unknown) =>
    request<T>(path, { method: 'POST', body: JSON.stringify(body) }),

  put: <T>(path: string, body: unknown) =>
    request<T>(path, { method: 'PUT', body: JSON.stringify(body) }),

  delete: <T>(path: string) =>
    request<T>(path, { method: 'DELETE' }),
}
```

---

## Loading, Error & Empty States

Always implement all three states — this defines a production-grade UI.

```tsx
// Pattern for any data-fetching component
export function ProjectList() {
  const { data, isLoading, error } = useProjects()

  if (isLoading) return <ProjectListSkeleton />
  if (error) return <ErrorState message="Failed to load projects" onRetry={() => {}} />
  if (!data?.length) return <EmptyState title="No projects yet" action="Create Project" />

  return (
    <div className="grid gap-4">
      {data.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  )
}
```

---

## Testing with Vitest

```tsx
// src/features/deliverables/DeliverableCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { DeliverableCard } from './DeliverableCard'

const mockDeliverable = {
  id: '1',
  title: 'Brand Kit v2',
  status: 'pending_review' as const,
  dueAt: '2026-06-15T00:00:00Z',
}

describe('DeliverableCard', () => {
  it('renders title and status', () => {
    render(<DeliverableCard deliverable={mockDeliverable} />)

    expect(screen.getByText('Brand Kit v2')).toBeInTheDocument()
    expect(screen.getByText('pending_review')).toBeInTheDocument()
  })

  it('calls onSelect when clicked', () => {
    const onSelect = vi.fn()
    render(
      <DeliverableCard deliverable={mockDeliverable} onSelect={onSelect} />
    )

    fireEvent.click(screen.getByText('Brand Kit v2'))
    expect(onSelect).toHaveBeenCalledWith('1')
  })
})
```

---

## Common Pitfalls

- Using `any` — always use `unknown` and narrow types explicitly.
- Putting API calls directly in components — always use React Query hooks.
- Forgetting `key` prop on list items — causes rendering bugs.
- Using `useEffect` for data fetching — use React Query instead.
- Creating god-components — split into feature modules with their own hooks/types.
- Importing from `../../../` — configure `@/` path alias in `tsconfig.json` and `vite.config.ts`.
- Mutating state directly in Zustand — always return a new object from `set()`.
