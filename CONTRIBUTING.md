# Contribution

## Localhost setup

1. Clone this repository:
   ```shell
   git clone git@github.com:merixstudio/simple-storage.git
   ```
2. Enter the `simple-storage` directory:
   ```shell
   cd simple-storage/
   ```
3. Create a virtual environment
    ```shell
    virtualenv .venv
    ```
4. Activate the virtual environment you just created.
    ```shell
   source .venv/bin/activate
    ```
5. Having the virtual environment activated, install required dependencies:
    ```shell
    pip install mypy flake8 pytest pytest-cov pytest-xdist boto3
    ```
6. Set all the required environment variables:
    ```shell
   export STORAGES_BACKEND=storags.backends.file_system.FileSystemStorage
   export STORAGES_PATH=.
   export STORAGES_AWS_ACCESS_KEY_ID=YOURAWSACCESSKEYID
   export STORAGES_AWS_SECRET_ACCESS_KEY=YOURAWSSECRETACCESSKEY
   export STORAGES_BUCKET_NAME=your-bucket-name
    ```

## Running tests

To run the tests simply execute the following command:

```shell
pytest -n 5 --cov=storages
```

> **Note:** tests are being run in parallel using [pytest-xdist][1] package. The `-n 5` parameter tells the `pytest-xdist` package how many workers should be spawned to run the tests.

Additionally, a test coverage report would be generated (`--cov=storages` argument).
We are aiming to maintain the **100% test coverage** of this package.

## The workflow

### 💻 Start working on the feature or bugfix

1. We expect you to create a branch per each new feature / bugfix.
2. We are not enforcing any specific branch naming convention.
3. Write the code.

### ⏩ Before pushing

1. Auto-format the code using `black` and `isort`:
   ```shell
   black storages/
   isort storages/
   ```
2. Make sure that `flake8` and `mypy` don't report any problems:
   ```shell
   flake8 storages/
   mypy storages/
   ```
3. Run the tests and make sure that you've got 100% test coverage:
   ```shell
   pytest -n 5 --cov=storages
   ```

> **Note:** Each time you push new code to the repository a GitHub Action called `Lint and test` will be triggered.
> This action will run tests and lint your code, no surprises here 😉.
> 
> If the linting process fails or tests wouldn't pass the whole build will fail, so please remember to go through the
> steps 1-3 and make sure that no problems are being reported to avoid these sad ❌ symbols next to your build.

### ⏩ Before creating a Pull Request

1. Make sure that you've maintained the 100% test coverage of the codebase.
2. Make sure you've updated the `README.md` file if there are any changes in that may make the `README.md` file obsolete.

### ✅ When creating a Pull Request

1. We expect you to be as descriptive as possible when creating a pull request.
2. Please include the following information:
   - what feature is being added and what was the reasoning
   - which issues does this pull request refer to (if applicable)
3. The target branch for merging any new feature should be `staging`.
4. Remember to mark the Pull Request with a proper label.

**Thank you** for your contributions! 😁

[1]: https://pypi.org/project/pytest-xdist/
