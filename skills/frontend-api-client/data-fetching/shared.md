# Data Fetching & Caching — Shared

## Use the generated hooks directly
Orval's `react-query` mode generates a `useQuery`/`useMutation` hook per endpoint alongside the raw functions. Verified by actually rendering them — not just checking they exist as exports — via Testing Library against the live backend: `useListTasksApiV1TasksGet` correctly shows a loading state, then real server data; `useCreateTaskApiV1TasksPost`'s mutation fires a real request and its `onSuccess` callback correctly drives cache invalidation. Prefer the hooks in component code; the plain functions are for non-component contexts (scripts, other hooks' internals).

Note on naming: query hooks are generated as `export function useXxx(...)`, not `export const useXxx = ...` — grepping for `export const use` alone will miss them.

## Cache invalidation matches the backend's own invalidation logic
`fastapi-production`'s `cache/shared.md` invalidates the Redis-side task list cache on every write. Mirror that on the frontend — invalidate the corresponding TanStack Query key on the matching mutation, or the UI silently shows stale data even though the backend itself is already consistent:
```ts
const queryClient = useQueryClient();
const { mutate } = useCreateTaskApiV1TasksPost({
  mutation: { onSuccess: () => queryClient.invalidateQueries({ queryKey: ['/api/v1/tasks'] }) },
});
```

## Forbidden
- refetching on every render instead of relying on TanStack Query's cache (defeats the point of using it)
- a mutation with no cache invalidation, relying on a full page reload to see the result
