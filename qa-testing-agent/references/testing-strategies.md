# Testing Strategies Reference — Live Developer Stack

## Testing by Language

### Python (pytest + pytest-asyncio)

#### Unit Test

```python
# tests/test_deliverable_service.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.deliverable_service import DeliverableService

@pytest.fixture
def mock_repo():
    repo = AsyncMock()
    repo.create.return_value = MagicMock(id=1, title="Brand Kit v2", status="draft")
    return repo

@pytest.fixture
def service(mock_repo):
    return DeliverableService(repo=mock_repo)

@pytest.mark.asyncio
async def test_create_deliverable_success(service, mock_repo):
    result = await service.create(title="Brand Kit v2", project_id=10)

    assert result.id == 1
    assert result.title == "Brand Kit v2"
    mock_repo.create.assert_called_once_with(title="Brand Kit v2", project_id=10)

@pytest.mark.asyncio
async def test_create_deliverable_empty_title_raises(service):
    with pytest.raises(ValueError, match="Title cannot be empty"):
        await service.create(title="", project_id=10)
```

#### Integration Test (FastAPI + httpx)

```python
# tests/test_api_deliverables.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_deliverable_api():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/deliverables", json={
            "title": "Brand Kit v2",
            "project_id": 10,
        })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Brand Kit v2"
    assert data["status"] == "draft"

@pytest.mark.asyncio
async def test_create_deliverable_missing_title():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/deliverables", json={
            "project_id": 10,
        })

    assert response.status_code == 422  # Validation error
```

#### Fixtures & Conftest

```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session

    await engine.dispose()
```

---

### TypeScript (Vitest)

#### Unit Test

```typescript
// tests/deliverableService.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { DeliverableService } from '../src/services/deliverableService.js'
import type { DeliverableRepo } from '../src/repos/deliverableRepo.js'

describe('DeliverableService', () => {
  let service: DeliverableService
  let mockRepo: DeliverableRepo

  beforeEach(() => {
    mockRepo = {
      create: vi.fn().mockResolvedValue({ id: '1', title: 'Brand Kit v2', status: 'draft' }),
      findById: vi.fn(),
      update: vi.fn(),
    }
    service = new DeliverableService(mockRepo)
  })

  it('creates a deliverable with valid data', async () => {
    const result = await service.create({ title: 'Brand Kit v2', projectId: '10' })

    expect(result.id).toBe('1')
    expect(result.title).toBe('Brand Kit v2')
    expect(mockRepo.create).toHaveBeenCalledOnce()
  })

  it('throws when title is empty', async () => {
    await expect(
      service.create({ title: '', projectId: '10' })
    ).rejects.toThrow('Title cannot be empty')
  })

  it('throws when title exceeds max length', async () => {
    const longTitle = 'a'.repeat(256)
    await expect(
      service.create({ title: longTitle, projectId: '10' })
    ).rejects.toThrow('Title too long')
  })
})
```

#### API Integration Test (Fastify)

```typescript
// tests/api/deliverables.test.ts
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { buildApp } from '../../src/app.js'
import type { FastifyInstance } from 'fastify'

describe('POST /api/deliverables', () => {
  let app: FastifyInstance

  beforeAll(async () => {
    app = await buildApp({ testing: true })
  })

  afterAll(async () => {
    await app.close()
  })

  it('returns 201 with valid data', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/deliverables',
      payload: { title: 'Brand Kit v2', projectId: '10' },
    })

    expect(response.statusCode).toBe(201)
    const body = response.json()
    expect(body.title).toBe('Brand Kit v2')
    expect(body.status).toBe('draft')
  })

  it('returns 400 with missing title', async () => {
    const response = await app.inject({
      method: 'POST',
      url: '/api/deliverables',
      payload: { projectId: '10' },
    })

    expect(response.statusCode).toBe(400)
  })
})
```

---

### PHP / Laravel (PHPUnit + Pest)

#### Feature Test

```php
// tests/Feature/DeliverableTest.php
use App\Models\User;
use App\Models\Project;

test('can create a deliverable', function () {
    $user = User::factory()->create();
    $project = Project::factory()->for($user)->create();

    $this->actingAs($user)
        ->postJson("/api/projects/{$project->id}/deliverables", [
            'title' => 'Brand Kit v2',
        ])
        ->assertCreated()
        ->assertJsonPath('data.title', 'Brand Kit v2')
        ->assertJsonPath('data.status', 'draft');
});

test('cannot create deliverable without title', function () {
    $user = User::factory()->create();
    $project = Project::factory()->for($user)->create();

    $this->actingAs($user)
        ->postJson("/api/projects/{$project->id}/deliverables", [])
        ->assertUnprocessable()
        ->assertJsonValidationErrors(['title']);
});

test('cannot create deliverable on another users project', function () {
    $user = User::factory()->create();
    $otherUser = User::factory()->create();
    $project = Project::factory()->for($otherUser)->create();

    $this->actingAs($user)
        ->postJson("/api/projects/{$project->id}/deliverables", [
            'title' => 'Unauthorized',
        ])
        ->assertForbidden();
});
```

---

## Mocking Patterns

### When to Mock

| Mock | Don't Mock |
|---|---|
| External APIs (Anthropic, Stripe) | Pure business logic |
| Database (in unit tests) | Data transformations |
| Time/dates (for determinism) | The code under test |
| File system (when testing logic) | Simple utility functions |
| Email/notification services | Integration boundaries (in integration tests) |

### Mock vs Stub vs Spy

| Type | Purpose | Example |
|---|---|---|
| **Mock** | Verify interactions (was it called?) | `expect(mock.create).toHaveBeenCalledOnce()` |
| **Stub** | Provide canned responses | `mock.findById.mockResolvedValue(fakeProject)` |
| **Spy** | Observe without changing behavior | `vi.spyOn(service, 'validate')` |

---

## Test Data Patterns

### Factories (Generate Realistic Data)

```typescript
// tests/factories/project.ts
import { faker } from '@faker-js/faker'
import type { Project } from '../../src/types'

export function buildProject(overrides: Partial<Project> = {}): Project {
  return {
    id: faker.string.uuid(),
    name: faker.company.name() + ' Website Redesign',
    clientId: faker.string.uuid(),
    status: 'active',
    createdAt: faker.date.recent().toISOString(),
    ...overrides,
  }
}

// Usage
const project = buildProject({ status: 'archived' })
```

### Fixtures (Static, Predictable Data)

```typescript
// tests/fixtures/deliverables.ts
export const DELIVERABLE_DRAFT = {
  id: 'del-001',
  title: 'Brand Kit v2',
  status: 'draft' as const,
  projectId: 'proj-001',
  dueAt: '2026-06-15T00:00:00Z',
}

export const DELIVERABLE_APPROVED = {
  ...DELIVERABLE_DRAFT,
  id: 'del-002',
  status: 'approved' as const,
}
```

---

## Coverage Strategy

### What to Cover

| Priority | Target | Why |
|---|---|---|
| **Critical path** | 100% | User-facing flows that generate revenue |
| **Business logic** | 90%+ | Rules, calculations, transformations |
| **API endpoints** | 80%+ | Contract between frontend and backend |
| **Edge cases** | Targeted | Nulls, empty, boundaries, concurrent |
| **Error handling** | All paths | Every catch block should have a test |
| **UI components** | Key interactions | Clicks, form submits, state changes |

### What NOT to Cover

- Generated code (migrations, types)
- Third-party library internals
- Simple getters/setters with no logic
- Configuration files
- CSS/styling (use visual regression instead)

### Running Coverage

```bash
# Python
pytest --cov=app --cov-report=html --cov-report=term-missing

# TypeScript
npx vitest run --coverage

# PHP
php artisan test --coverage --min=80
```

---

## Test Naming Convention

```
test_<unit>_<scenario>_<expected_result>

# Python
def test_create_deliverable_with_empty_title_raises_value_error():
def test_get_project_with_invalid_id_returns_none():

# TypeScript
it('creates a deliverable with valid data')
it('throws when title exceeds max length')
it('returns 404 when project not found')

# PHP
test('cannot create deliverable without title')
test('returns paginated results with default limit')
```

---

## CI Integration

```yaml
# Run tests on every PR
- run: npm test -- --coverage --reporter=verbose
- run: |
    COVERAGE=$(npx vitest run --coverage --reporter=json 2>/dev/null | jq '.total.lines.pct')
    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
      echo "Coverage $COVERAGE% is below 80% threshold"
      exit 1
    fi
```
