# Tasks: Image Upload Web Service

**Input**: Design documents from `/specs/001-build-an-image/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [X] T001 Create project folder structure: `backend/src/app.py`, `backend/src/config.py`, `backend/src/blueprints/main.py`, `backend/src/blueprints/api.py`, `backend/src/models/image.py`, `backend/src/services/image_service.py`, `backend/instance/images.db`, `backend/uploads/`, `backend/requirements.txt`, `backend/.env`, `frontend/static/css/`, `frontend/static/js/`, `frontend/templates/index.html`, `frontend/templates/image_detail.html`
- [X] T002 Set up Python virtual environment in `.venv` folder
- [X] T003 Install Flask and required dependencies via `pip` using `requirements.txt`
- [X] T004 Create `.env` file with `SECRET_KEY`, `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`, `SQLALCHEMY_DATABASE_URI`, `FLASK_ENV`
- [X] T005 Initialize SQLite database (`instance/images.db`) and create tables

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [X] T006 [P] Contract test POST /api/upload in `backend/tests/contract/test_api_upload.py`
- [X] T007 [P] Contract test GET /api/images in `backend/tests/contract/test_api_images_list.py`
- [X] T008 [P] Contract test GET /api/images/<id> in `backend/tests/contract/test_api_images_get.py`
- [X] T009 [P] Contract test DELETE /api/images/<id> in `backend/tests/contract/test_api_images_delete.py`
- [X] T010 [P] Contract test GET /health in `backend/tests/contract/test_api_health.py`
- [X] T011 [P] Integration test: Python client uploads image successfully in `backend/tests/integration/test_upload_success.py`
- [X] T012 [P] Integration test: Web gallery displays images and metadata in `frontend/tests/integration/test_gallery_display.py`
- [X] T013 [P] Integration test: Web gallery sorts images by upload date in `frontend/tests/integration/test_gallery_sort.py`
- [X] T014 [P] Integration test: Invalid/corrupted image upload handling in `backend/tests/integration/test_upload_invalid.py`
- [X] T015 [P] Integration test: Concurrent uploads handling in `backend/tests/integration/test_concurrent_uploads.py`
- [X] T016 [P] Integration test: Image exceeding size limit handling in `backend/tests/integration/test_upload_size_limit.py`

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [X] T017 [P] Implement Image model in `backend/src/models/image.py`
- [X] T018 [P] Implement Flask application factory in `backend/src/app.py`
- [X] T019 [P] Implement configuration in `backend/src/config.py`
- [X] T020 [P] Implement API Blueprint in `backend/src/blueprints/api.py`
- [X] T021 [P] Implement Main Blueprint in `backend/src/blueprints/main.py`
- [X] T022 Implement Image upload endpoint (POST /api/upload) in `backend/src/blueprints/api.py`
- [X] T023 Implement List images endpoint (GET /api/images) in `backend/src/blueprints/api.py`
- [X] T024 Implement Get image metadata endpoint (GET /api/images/<id>) in `backend/src/blueprints/api.py`
- [X] T025 Implement Delete image endpoint (DELETE /api/images/<id>) in `backend/src/blueprints/api.py`
- [X] T026 Implement Health check endpoint (GET /health) in `backend/src/blueprints/api.py`
- [ ] T027 Implement Serve image files endpoint (GET /uploads/<date>/<filename>) in `backend/src/blueprints/main.py`
- [X] T028 [P] Implement Image service for file operations and metadata handling in `backend/src/services/image_service.py`
- [X] T029 [P] Implement HTML templates (`frontend/templates/index.html`, `frontend/templates/image_detail.html`)
- [ ] T030 [P] Implement CSS/JS for frontend (`frontend/static/css/`, `frontend/static/js/`)

## Phase 3.4: Integration
- [ ] T031 Connect ImageService to SQLite DB
- [ ] T032 Implement error handling for API endpoints
- [ ] T033 Configure logging with Flask's `app.logger`
- [ ] T034 Configure CORS for localhost only
- [ ] T035 Implement input validation for all endpoints

## Phase 3.5: Polish
- [ ] T036 [P] Unit tests for image validation in `backend/tests/unit/test_image_validation.py`
- [ ] T037 Performance tests to meet response time and throughput goals
- [ ] T038 Update documentation (e.g., API usage, setup instructions)
- [ ] T039 Review and remove any code duplication
- [ ] T040 Conduct manual testing via browser and Python client

## Dependencies
- Setup (T001-T005) before Tests (T006-T016)
- Tests (T006-T016) before Core Implementation (T017-T030)
- T017 blocks T022, T023, T024, T025, T028, T031
- T018 blocks T020, T021, T033, T034
- T020 blocks T022, T023, T024, T025, T026
- T021 blocks T027, T029
- Core Implementation (T017-T030) before Integration (T031-T035)
- Integration (T031-T035) before Polish (T036-T040)

## Parallel Example
```
# Launch T006-T010 (Contract tests) together:
Task: "Contract test POST /api/upload in backend/tests/contract/test_api_upload.py"
Task: "Contract test GET /api/images in backend/tests/contract/test_api_images_list.py"
Task: "Contract test GET /api/images/<id> in backend/tests/contract/test_api_images_get.py"
Task: "Contract test DELETE /api/images/<id> in backend/tests/contract/test_api_images_delete.py"
Task: "Contract test GET /health in backend/tests/contract/test_api_health.py"

# Launch T011-T016 (Integration tests) together:
Task: "Integration test: Python client uploads image successfully in backend/tests/integration/test_upload_success.py"
Task: "Integration test: Web gallery displays images and metadata in frontend/tests/integration/test_gallery_display.py"
Task: "Integration test: Web gallery sorts images by upload date in frontend/tests/integration/test_gallery_sort.py"
Task: "Integration test: Invalid/corrupted image upload handling in backend/tests/integration/test_upload_invalid.py"
Task: "Integration test: Concurrent uploads handling in backend/tests/integration/test_concurrent_uploads.py"
Task: "Integration test: Image exceeding size limit handling in backend/tests/integration/test_upload_size_limit.py"

# Launch T017-T021 (Core Implementation - initial parallel tasks) together:
Task: "Implement Image model in backend/src/models/image.py"
Task: "Implement Flask application factory in backend/src/app.py"
Task: "Implement configuration in backend/src/config.py"
Task: "Implement API Blueprint in backend/src/blueprints/api.py"
Task: "Implement Main Blueprint in backend/src/blueprints/main.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task