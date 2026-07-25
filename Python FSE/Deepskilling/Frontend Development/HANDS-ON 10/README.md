# Hands-On 10 — API Integration & Advanced State Management

This project is the React implementation (Task 1 + Task 2). It reuses the
Hands-On 6 project as a base and adds:

- `src/api/apiClient.js` — one configured Axios instance (baseURL, timeout,
  request interceptor for auth, response interceptor that unwraps `data` and
  standardises errors).
- `src/api/courseApi.js` — `getAllCourses()`, `getCourseById(id)`,
  `enrollStudent(studentId, courseId)`. Components never call Axios directly.
- `src/store/coursesSlice.js` — `createAsyncThunk('courses/fetchAll', ...)`
  with `pending` / `fulfilled` / `rejected` handled in `extraReducers`, plus
  `selectCourses` / `selectCoursesLoading` / `selectCoursesError` selectors.
- `src/components/ErrorBoundary.jsx` — global error handler for React.

To test the rejected-thunk path (step 147), temporarily break the URL in
`apiClient.js` (e.g. change `jsonplaceholder.typicode.com` to a typo) and
confirm the courses page shows the error message instead of the list.

## Task 3 — NgRx concept (Angular)

NgRx follows the same Redux pattern used in `coursesSlice.js`, but splits it
into four pieces instead of one slice:

- **Actions** (`courses.actions.ts`) — plain objects describing what happened,
  e.g. `loadCourses`.
- **Reducers** (`courses.reducer.ts`) — pure functions that take the current
  state + an action and return new state. No API calls allowed here.
- **Effects** (`courses.effects.ts`) — listen for an action (e.g.
  `loadCourses`), call `CourseService`, and dispatch a success/failure action
  when the API call resolves. This is where side effects (HTTP calls) live.
- **Selectors** — memoized functions that read a slice of state, the NgRx
  equivalent of `selectCourses` above.

Data flow: `Component → dispatch(loadCourses) → Effect → CourseService (HTTP)
→ dispatch(loadCoursesSuccess) → Reducer → Store → Selector → Component`.

If you build this out in the Hands-On 7 Angular project, add:
```
src/app/store/courses.actions.ts
src/app/store/courses.reducer.ts
src/app/store/courses.effects.ts
src/app/store/courses.selectors.ts
```
and install `@ngrx/store` + `@ngrx/effects`.

## Task 3 — Pinia advanced patterns (Vue)

Already implemented in the Hands-On 8 project, `src/stores/enrollment.js`:

- `fetchAndEnroll(courseId)` — an async action that calls the API and updates
  state in one step, instead of splitting fetch/update across the component.
- `$reset()` — Pinia's built-in method to clear a store back to its initial
  state (useful for logout / test teardown).
- `storeToRefs(store)` — used in `Header.vue` and `ProfileView.vue` to
  destructure `enrolledCourses` / `totalCredits` while keeping reactivity.
  Plain destructuring (`const { enrolledCourses } = store`) would break
  reactivity because it copies the value instead of keeping a live reference.

Vue's global error handler is set in `src/main.js`:
`app.config.errorHandler = (err, instance, info) => { ... }`.

## Framework state-management comparison

| | React + Redux Toolkit | Angular + NgRx | Vue + Pinia |
|---|---|---|---|
| Boilerplate | Low — one file per slice (`createSlice`) | Higher — actions, reducers, effects, selectors as separate files | Lowest — one store file, plain functions |
| Async handling | `createAsyncThunk` generates 3 action types automatically | `Effects` (RxJS-based) listen for actions and dispatch new ones | Plain `async`/`await` inside a store action, no extra wiring |
| Learning curve | Moderate — need to understand actions/reducers/immutable updates (eased by Immer) | Steepest — requires RxJS fluency on top of the action/reducer/effect split | Gentlest — feels like writing a Vue component with shared state |
| Built-in tooling | Redux DevTools (time-travel debugging) | Redux DevTools support via `@ngrx/store-devtools` | Vue DevTools has a dedicated Pinia tab |
| Type safety | Good with TypeScript, some manual typing of thunks | Strongest — Angular's DI and strict templates catch errors early | Good, especially with `<script setup>` + TS |

All three solve the same problem — sharing state and centralising async logic
outside components — but trade off boilerplate against explicitness. Redux
Toolkit and Pinia both intentionally reduce the ceremony that plain
Redux/Vuex used to require; NgRx keeps the original Redux split because it
fits Angular's DI-and-RxJS architecture.
