# PHP / Laravel Reference — Live Developer Stack

## Runtime & Stack

- PHP **8.2+**. Strict types declared: `declare(strict_types=1);` in every file.
- Laravel **11.x** for SaaS backends (LiveApp, LiveCMS Pro).
- Deployment target: Ubuntu 24.04 VMs (Proxmox) + cPanel (Apache/LiteSpeed) for client sites.
- Frontend pairing: React + Vite + TailwindCSS (LiveApp), vanilla PHP/HTML for cPanel sites.

## Architecture Layers

```
app/
├── Http/
│   ├── Controllers/     # Thin — delegate to services
│   ├── Requests/        # FormRequest validation
│   └── Resources/       # API transformers (JsonResource)
├── Services/            # Business logic — no HTTP, no Eloquent directly
├── Repositories/        # DB abstraction (optional, for complex queries)
├── Models/              # Eloquent — relationships, scopes, casts
├── Jobs/                # Queue jobs
├── Events/ + Listeners/ # Domain events
└── Agents/              # Agent step classes (pipeline context)
```

## Code Patterns

### Controller (thin)

```php
<?php
declare(strict_types=1);

namespace App\Http\Controllers;

use App\Http\Requests\StoreDeliverableRequest;
use App\Http\Resources\DeliverableResource;
use App\Services\DeliverableService;
use Illuminate\Http\JsonResponse;

class DeliverableController extends Controller
{
    public function __construct(private DeliverableService $service) {}

    public function store(StoreDeliverableRequest $request): JsonResponse
    {
        $deliverable = $this->service->create($request->validated());
        return (new DeliverableResource($deliverable))
            ->response()
            ->setStatusCode(201);
    }
}
```

### Service

```php
<?php
declare(strict_types=1);

namespace App\Services;

use App\Models\Deliverable;
use Illuminate\Support\Facades\DB;

class DeliverableService
{
    public function create(array $data): Deliverable
    {
        return DB::transaction(function () use ($data) {
            $deliverable = Deliverable::create($data);
            // dispatch events, jobs, etc.
            return $deliverable;
        });
    }
}
```

### Eloquent Model with casts and scopes

```php
<?php
declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Builder;

class Deliverable extends Model
{
    protected $fillable = ['title', 'status', 'project_id', 'due_at'];

    protected $casts = [
        'due_at'     => 'datetime',
        'meta'       => 'array',
    ];

    public function scopePending(Builder $query): Builder
    {
        return $query->where('status', 'pending');
    }
}
```

### Queue Job

```php
<?php
declare(strict_types=1);

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class ProcessDeliverableReview implements ShouldQueue
{
    use Queueable, InteractsWithQueue, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;

    public function __construct(private int $deliverableId) {}

    public function handle(): void
    {
        // agent step logic here
    }

    public function failed(\Throwable $e): void
    {
        \Log::error('ProcessDeliverableReview failed', [
            'deliverable_id' => $this->deliverableId,
            'error' => $e->getMessage(),
        ]);
    }
}
```

## Migrations

```php
Schema::create('deliverables', function (Blueprint $table) {
    $table->id();
    $table->foreignId('project_id')->constrained()->cascadeOnDelete();
    $table->string('title');
    $table->string('status', 32)->default('draft')->index();
    $table->jsonb('meta')->nullable();
    $table->timestamp('due_at')->nullable();
    $table->timestamps();
    $table->softDeletes();
});
```

## Security Checklist

- Use `FormRequest` for all input validation — never validate in controllers.
- API tokens via Laravel Sanctum. Never expose Eloquent models directly — always use API Resources.
- Encrypt sensitive config values at rest (ADR-013 baseline: use `encrypt()`/`decrypt()` helpers).
- Rate limiting: `throttle:api` middleware on all public endpoints.
- CORS: configured via `config/cors.php`, not ad-hoc headers.

## Testing

```php
// tests/Feature/DeliverableTest.php
public function test_can_create_deliverable(): void
{
    $user = User::factory()->create();
    $project = Project::factory()->for($user)->create();

    $this->actingAs($user)
        ->postJson("/api/projects/{$project->id}/deliverables", [
            'title' => 'Brand Kit v2',
        ])
        ->assertCreated()
        ->assertJsonPath('data.title', 'Brand Kit v2');
}
```

## cPanel / Vanilla PHP Sites

For client sites on cPanel (not Laravel):
- PHP 8.2, no framework. Vanilla PHP with custom Router if needed.
- `public_html/` is the docroot. Assets in `public_html/assets/`.
- Database: MySQL 8 via PDO with prepared statements only.
- No Composer autoload unless the project explicitly requires it.
