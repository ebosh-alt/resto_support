# Development Guidelines for Resto Support Bot

This document provides essential information for developers working on the Resto Support Bot project.

## Build and Configuration

### Environment Setup

1. The project uses Poetry for dependency management. Ensure you have Poetry 2.0.1+ installed:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create a `.env` file in the `data/` directory with the following variables:
   ```
   # Telegram
   tg_bot_token=your_telegram_bot_token
   
   # Database
   db_host=path_to_database_or_connection_string
   
   # Redis
   redis_host=localhost
   redis_port=6379
   
   # API (Bitrix)
   api_host=your_bitrix_api_url
   ```

### Docker Setup

The project can be run using Docker:

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. The setup includes two containers:
   - `bot_support`: The main bot application
   - `redis_server`: Redis instance for caching and message queuing

3. Data persistence:
   - SQLite data is stored in a Docker volume (`sqlite_data`)
   - Environment variables are loaded from `data/.env`

## Testing

### Running Tests

1. Run all tests:
   ```bash
   python -m pytest
   ```

2. Run specific test file:
   ```bash
   python -m pytest tests/test_simple.py
   ```

3. Run tests with verbose output:
   ```bash
   python -m pytest -v
   ```

### Writing Tests

1. Create test files in the `tests/` directory with names starting with `test_`.

2. Use pytest fixtures for setup and teardown:
   ```python
   @pytest.fixture(scope="module")
   def client():
       return ClientBitrix()
   ```

3. For asynchronous tests, use the `@pytest.mark.asyncio` decorator:
   ```python
   @pytest.mark.asyncio
   async def test_async_function():
       result = await some_async_function()
       assert result == expected_value
   ```

4. Example of a simple test:
   ```python
   def test_get_task_status_name():
       assert get_task_status_name(COMPLETE_TASK_ID) == "Готово"
       assert get_task_status_name(999999) == "Unknown status"
   ```

### Test Configuration

- The project uses pytest-asyncio with auto mode for async tests
- The asyncio fixture loop scope is set to "function" by default
- Configuration is defined in the `pyproject.toml` file

## Development Information

### Project Structure

- `data/`: Configuration, settings, and database files
- `entities/`: Data models and database entities
- `handlers/`: Telegram bot handlers for different types of updates
- `services/`: Business logic and external service integrations
- `tests/`: Test files

### Logging

The project uses loguru for logging:

1. Logs are configured in `services/logger.py`
2. To enable logging in your module:
   ```python
   from loguru import logger
   
   logger.info("This is an info message")
   logger.error("This is an error message")
   ```

3. For exception handling, use the `@logger.catch()` decorator:
   ```python
   @logger.catch()
   async def function_that_might_raise_exception():
       # Your code here
   ```

### Asynchronous Programming

- The project uses asyncio for asynchronous operations
- Main entry point is in `main.py`
- Background tasks are created using `asyncio.create_task()`
- The scheduler runs as a background task

### Configuration Management

- Configuration is managed using Pydantic models
- Environment variables are loaded from `data/.env`
- Different configuration classes exist for different components (Telegram, Database, Redis, API)
- Access configuration through the `config` object imported from `data.config`

### Task Status Management

- Task statuses are defined in `data/config.py` as `STATUSES_TASK`
- Each status has an ID and a descriptive name
- Use the appropriate constants when checking task status (e.g., `COMPLETE_TASK_ID`, `WORK_TASK_ID`)